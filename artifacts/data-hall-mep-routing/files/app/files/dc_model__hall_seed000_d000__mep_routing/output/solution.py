#!/usr/bin/env python3
"""
MEP Coordination Model for Data Hall dc_model/hall_seed000_d000
Builds IFC4 model with coordinated overhead services (cable tray, busway, chilled water)
Rebuilt from 7 drawing sheets: A-101, A-301, A-601, A-602, E-101, F-101, M-101
"""

import sys
import math
import json
import os
import numpy as np
import ifcopenshell as ifc
import ifcopenshell.api
import ifcopenshell.api.unit
import ifcopenshell.guid

# ─── CONSTANTS FROM DRAWING RECONCILIATION ───
# Room: ~27m x 21m, 128 cabinets
# Grid from A-101: 128 racks in 8 rows of 16, each rack 600mm wide x 1200mm deep
# A-301 section: FFL=0, access floor 300mm, clear height 2600mm above access floor top
# CRAH units at perimeter, PDUs at row ends, columns on 6m grid
# Sprinklers on 3m grid at ceiling (3200mm AFF)
# M-101: CHW entry at (2000, 5000) from column A1, flow to all rows + 6 CRAHs
# E-101: Busway entry at (2000, 5000), PDUs at row ends, 800mm wide dedicated zone above PDU
# F-101: Sprinkler grid 3m x 3m, deflector at 3200mm AFF

# Room dimensions
ROOM_W = 27000  # X span
ROOM_D = 21000  # Y span
COL_GRID = 6000  # structural column grid

# Access floor
AF_H = 300  # access floor height
FFL = 0  # finished floor level (top of slab)
AF_TOP = FFL + AF_H  # top of access floor tiles = 300
CLEAR_H = 2600  # min clear height above access floor
CEILING_H = AF_TOP + CLEAR_H  # ceiling / slab soffit = 2900
SPRINKLER_DEFLECTOR_H = 3200  # above FFL
SPRINKLER_CLEARANCE = 460  # below deflector
SPRINKLER_CLEAR_ZONE = SPRINKLER_DEFLECTOR_H - SPRINKLER_CLEARANCE  # 2740 - nothing above this

# Rack: 600w x 1200d x 2000h (from A-601)
RACK_W = 600
RACK_D = 1200
RACK_H = 2000
ROW_COUNT = 8
RACKS_PER_ROW = 16
ROW_SPACING = 2400  # center-to-center Y (cold/hot aisle pattern)
RACK_SPACING = 600  # center-to-center X (touching)

# First rack position (from A-101 plan)
FIRST_RACK_CX = 1500  # from wall
FIRST_RACK_CY = 1500  # from wall

# CRAH units (from A-101/M-101): 6 units, 2 per long wall, 1 per short wall
CRAH_W = 2400
CRAH_D = 1200
CRAH_H = 2400
CRAH_POSITIONS = [
    (ROOM_W/2, 0),  # bottom wall center
    (ROOM_W/2, ROOM_D),  # top wall center
    (0, ROOM_D/3),  # left wall
    (0, 2*ROOM_D/3),
    (ROOM_W, ROOM_D/3),  # right wall
    (ROOM_W, 2*ROOM_D/3),
]

# PDU (from E-101): at each row end, 800w x 1000d x 2200h
PDU_W = 800
PDU_D = 1000
PDU_H = 2200
PDU_DEDICATED_H = 1800  # no CHW in 1800mm above PDU top

# Structural columns: 400x400, full height to ceiling
COL_W = 400
COL_D = 400

# Services - redesigned tiers to fit below sprinkler clearance (2740) and ceiling (2900)
# Stack order from bottom: CHW (165mm), Tray (100mm), Busway (200mm)
# With 300mm separation between tray and busway on Z axis
# All tops must be <= 2740 (sprinkler clearance)

# CHW pipe: DN100 (114mm OD) + 25.4mm insulation = 165mm OD
PIPE_OD = 114
PIPE_INSUL = 25.4
PIPE_TOTAL_OD = PIPE_OD + 2*PIPE_INSUL  # 165mm

# Tier elevations (centerline heights)
# Busway top at 2740 -> center at 2740 - 100 = 2640
BUS_TIER_H = 2640  # centerline, top=2740, bottom=2540
# 300mm Z separation -> tray center at 2640 - 300 = 2340
TRAY_TIER_H = 2340  # centerline, top=2390, bottom=2290
# CHW below tray with gap -> CHW center at 2340 - 150 = 2190 (but use 2200 for round number)
CHW_TIER_H = 2200  # centerline, top=2282, bottom=2118

TRAY_W = 300
TRAY_H = 100
TRAY_COVER_H = 20
BUS_W = 400
BUS_H = 200

# Minimum separations
TRAY_BUS_SEP = 300  # 300mm on at least one axis (we use Z: 2640 - 2340 = 300)
HEADROOM_MIN = 2600  # above access floor

# ─── IFC HELPER FUNCTIONS ───
def create_ifc_file():
    f = ifc.file(schema="IFC4")
    project = f.createIfcProject(ifc.guid.new(), None, "Data Hall MEP Coordination", None, None, None, None, None, None)
    lu = ifcopenshell.api.unit.add_si_unit(f, unit_type='LENGTHUNIT', prefix='MILLI')
    au = ifcopenshell.api.unit.add_si_unit(f, unit_type='AREAUNIT', prefix=None)
    vu = ifcopenshell.api.unit.add_si_unit(f, unit_type='VOLUMEUNIT', prefix=None)
    pa = ifcopenshell.api.unit.add_si_unit(f, unit_type='PLANEANGLEUNIT', prefix=None)
    ifcopenshell.api.unit.assign_unit(f, units=[lu, au, vu, pa])
    return f

def create_axis2_placement3d(f, origin, z_dir=(0.0,0.0,1.0), x_dir=(1.0,0.0,0.0)):
    return f.createIfcAxis2Placement3D(
        f.createIfcCartesianPoint([float(o)/1000.0 for o in origin]),
        f.createIfcDirection([float(v) for v in z_dir]),
        f.createIfcDirection([float(v) for v in x_dir])
    )

def create_local_placement(f, origin, rel_to=None, z_dir=(0,0,1), x_dir=(1,0,0)):
    if rel_to:
        return f.createIfcLocalPlacement(rel_to, create_axis2_placement3d(f, origin, z_dir, x_dir))
    return f.createIfcLocalPlacement(None, create_axis2_placement3d(f, origin, z_dir, x_dir))

def create_extruded_solid(f, profile_pts, depth, placement):
    pts = [f.createIfcCartesianPoint([float(p[0])/1000.0, float(p[1])/1000.0]) for p in profile_pts]
    if pts[0] != pts[-1]:
        pts.append(pts[0])
    polyline = f.createIfcPolyline(pts)
    profile = f.createIfcArbitraryClosedProfileDef("AREA", None, polyline)
    dir_z = f.createIfcDirection([0.0, 0.0, 1.0])
    extrude = f.createIfcExtrudedAreaSolid(profile, placement, dir_z, float(depth)/1000.0)
    return extrude

def create_rect_profile(f, w, h, cx=0, cy=0):
    hw, hh = w/2, h/2
    return [(cx-hw, cy-hh), (cx+hw, cy-hh), (cx+hw, cy+hh), (cx-hw, cy+hh)]

def create_representation(f, solids, context):
    items = []
    for s in solids:
        if isinstance(s, list):
            items.extend(s)
        else:
            items.append(s)
    return f.createIfcShapeRepresentation(context, "Body", "SweptSolid", items)

def add_pset(f, element, pset_name, props):
    """Add property set to element"""
    pset = f.createIfcPropertySet(ifc.guid.new(), None, pset_name, None, [
        f.createIfcPropertySingleValue(k, None, f.createIfcLabel(str(v)), None) for k,v in props.items()
    ])
    f.createIfcRelDefinesByProperties(ifc.guid.new(), None, None, None, [element], pset)

# ─── ROUTING HELPER: Build connected network from spine with branches ───
def build_connected_segments(entry_point, spine_x, spine_z, row_ys, row_serve_starts, row_serve_ends, crah_connections, tier_z):
    """
    Build a connected network where all segments meet at endpoints.
    
    Strategy: 
    1. Collect all Y positions where branches connect to spine (entry_y, row_ys, crah_cys, extents)
    2. Sort them and create spine segments between consecutive Y positions
    3. Add horizontal branches from each spine node to row serve spans
    4. Add CRAH horizontal + vertical connections
    
    Returns list of ((sx,sy,sz), (ex,ey,ez)) segments
    """
    segments = []
    
    # All Y positions where spine has a node
    spine_nodes_y = set()
    spine_nodes_y.add(entry_point[1])  # entry Y
    
    # Row connections
    for row_y in row_ys:
        spine_nodes_y.add(row_y)
    
    # CRAH connections (only those that connect horizontally to spine)
    for cx, cy in crah_connections:
        spine_nodes_y.add(cy)
    
    # Extents - extend spine beyond first/last row
    min_row_y = min(row_ys) if row_ys else entry_point[1]
    max_row_y = max(row_ys) if row_ys else entry_point[1]
    spine_nodes_y.add(min_row_y - 2000)
    spine_nodes_y.add(max_row_y + 2000)
    
    # Sort spine nodes by Y
    sorted_spine_y = sorted(spine_nodes_y)
    
    # Create spine segments between consecutive nodes
    for i in range(len(sorted_spine_y) - 1):
        y1 = sorted_spine_y[i]
        y2 = sorted_spine_y[i+1]
        segments.append(((spine_x, y1, tier_z), (spine_x, y2, tier_z)))
    
    # Entry horizontal from entry_x to spine_x at entry_y
    ex, ey, ez = entry_point
    if ex != spine_x:
        segments.append(((ex, ey, tier_z), (spine_x, ey, tier_z)))
    
    # Row horizontal branches: from spine (spine_x, row_y) to serve_start, then to serve_end
    for row_y, serve_start, serve_end in zip(row_ys, row_serve_starts, row_serve_ends):
        segments.append(((spine_x, row_y, tier_z), (serve_start, row_y, tier_z)))
        segments.append(((serve_start, row_y, tier_z), (serve_end, row_y, tier_z)))
    
    # CRAH connections: horizontal from spine to CRAH, then vertical drop
    CRAH_CONN_H = 800  # AF_TOP + 500
    for cx, cy in crah_connections:
        # Horizontal from spine to CRAH at tier_z
        if cx != spine_x:
            segments.append(((spine_x, cy, tier_z), (cx, cy, tier_z)))
        # Vertical drop from tier_z to CRAH connection height
        segments.append(((cx, cy, tier_z), (cx, cy, CRAH_CONN_H)))
    
    return segments

# ─── MAIN BUILD FUNCTION ───
def build_model(out_path: str):
    f = create_ifc_file()
    project = f.by_type("IfcProject")[0]
    
    # Context
    ctx3d = f.createIfcGeometricRepresentationContext(
        "Model", "Model", 3, 1.0e-5,
        f.createIfcAxis2Placement3D(
            f.createIfcCartesianPoint([0.0,0.0,0.0]),
            f.createIfcDirection([0.0,0.0,1.0]),
            f.createIfcDirection([1.0,0.0,0.0])
        ), None
    )
    
    # Spatial structure
    site_pl = create_local_placement(f, (0,0,0))
    site = f.createIfcSite(ifc.guid.new(), None, "Data Hall Site", None, None, site_pl, None, None, None, None)
    
    bldg_pl = create_local_placement(f, (0,0,0), site)
    bldg = f.createIfcBuilding(ifc.guid.new(), None, "Data Hall", None, None, bldg_pl, None, None, None, None, None, None)
    
    storey_pl = create_local_placement(f, (0,0,FFL), bldg)
    storey = f.createIfcBuildingStorey(ifc.guid.new(), None, "Data Hall Level", None, None, storey_pl, None, None, None)
    
    f.createIfcRelAggregates(ifc.guid.new(), None, None, None, project, [site])
    f.createIfcRelAggregates(ifc.guid.new(), None, None, None, site, [bldg])
    f.createIfcRelAggregates(ifc.guid.new(), None, None, None, bldg, [storey])
    
    # Space for the hall (7 args)
    space_pl = create_local_placement(f, (0,0,FFL), storey)
    space_prof = create_rect_profile(f, ROOM_W, ROOM_D, ROOM_W/2, ROOM_D/2)
    space_solid = create_extruded_solid(f, space_prof, CEILING_H - FFL, create_axis2_placement3d(f, (0,0,FFL)))
    space_rep = create_representation(f, [space_solid], ctx3d)
    space = f.createIfcSpace(ifc.guid.new(), None, "Data Hall Space", None, "SPACE", space_pl, space_rep)
    f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [space], storey)
    add_pset(f, space, "Pset_DCM_Space", {"RoomWidth": ROOM_W, "RoomDepth": ROOM_D, "ClearHeight": CLEAR_H})
    
    # ─── STRUCTURAL COLUMNS (7 args) ───
    for cx in range(0, ROOM_W+1, COL_GRID):
        for cy in range(0, ROOM_D+1, COL_GRID):
            if cx == 0 or cx == ROOM_W or cy == 0 or cy == ROOM_D:
                continue
            prof = create_rect_profile(f, COL_W, COL_D)
            pl = create_axis2_placement3d(f, (cx, cy, FFL))
            solid = create_extruded_solid(f, prof, CEILING_H - FFL, pl)
            rep = create_representation(f, [solid], ctx3d)
            col_pl = create_local_placement(f, (cx, cy, FFL))
            col = f.create_entity("IfcColumn", ifc.guid.new(), None, f"Column_{cx}_{cy}", None, "STRUCTURAL", col_pl, rep, None, "COLUMN")
            f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [col], storey)
            add_pset(f, col, "Pset_DCM_Column", {"GridX": cx, "GridY": cy, "Width": COL_W, "Depth": COL_D})
    
    # ─── ACCESS FLOOR (7 args) ───
    af_prof = create_rect_profile(f, ROOM_W, ROOM_D, ROOM_W/2, ROOM_D/2)
    af_pl_axis = create_axis2_placement3d(f, (0, 0, FFL))
    af_solid = create_extruded_solid(f, af_prof, AF_H, af_pl_axis)
    af_rep = create_representation(f, [af_solid], ctx3d)
    af_pl = create_local_placement(f, (0,0,FFL))
    af = f.create_entity("IfcSlab", ifc.guid.new(), None, "AccessFloor", None, "RAISED_FLOOR", af_pl, af_rep, None, "FLOOR")
    f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [af], storey)
    add_pset(f, af, "Pset_DCM_AccessFloor", {"Height": AF_H, "TileSize": 600})
    
    # ─── RACKS (7 args) ───
    rack_prof = create_rect_profile(f, RACK_W, RACK_D)
    row_ys = []
    row_serve_starts = []
    row_serve_ends = []
    for row in range(ROW_COUNT):
        row_y = FIRST_RACK_CY + row * ROW_SPACING
        row_ys.append(row_y)
        row_start_x = FIRST_RACK_CX - RACK_W/2
        row_end_x = FIRST_RACK_CX + (RACKS_PER_ROW-1)*RACK_SPACING + RACK_W/2
        serve_start = row_start_x + (row_end_x - row_start_x) * 0.1
        serve_end = row_end_x - (row_end_x - row_start_x) * 0.1
        row_serve_starts.append(serve_start)
        row_serve_ends.append(serve_end)
        
        facing = 1 if row % 2 == 0 else -1
        rot_z = 0 if facing > 0 else math.pi
        for i in range(RACKS_PER_ROW):
            rack_x = FIRST_RACK_CX + i * RACK_SPACING
            cx, cy = rack_x, row_y
            pl_axis = create_axis2_placement3d(f, (cx, cy, AF_TOP), (0,0,1), (math.cos(rot_z), math.sin(rot_z), 0))
            solid = create_extruded_solid(f, rack_prof, RACK_H, pl_axis)
            rep = create_representation(f, [solid], ctx3d)
            rack_pl = create_local_placement(f, (cx, cy, AF_TOP), None, (0,0,1), (math.cos(rot_z), math.sin(rot_z), 0))
            rack = f.createIfcFurniture(ifc.guid.new(), None, f"Rack_R{row}_U{i}", None, "Rack", rack_pl, rep)
            f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [rack], storey)
            add_pset(f, rack, "Pset_DCM_Rack", {"Row": row, "Index": i, "Facing": facing, "Width": RACK_W, "Depth": RACK_D, "Height": RACK_H})
    
    # ─── CRAH UNITS (7 args) ───
    crah_prof = create_rect_profile(f, CRAH_W, CRAH_D)
    for idx, (cx, cy) in enumerate(CRAH_POSITIONS):
        pl_axis = create_axis2_placement3d(f, (cx, cy, AF_TOP))
        solid = create_extruded_solid(f, crah_prof, CRAH_H, pl_axis)
        rep = create_representation(f, [solid], ctx3d)
        crah_pl = create_local_placement(f, (cx, cy, AF_TOP))
        crah = f.createIfcUnitaryEquipment(ifc.guid.new(), None, f"CRAH_{idx}", None, "CRAH", crah_pl, rep)
        f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [crah], storey)
        add_pset(f, crah, "Pset_DCM_CRAH", {"Index": idx, "Width": CRAH_W, "Depth": CRAH_D, "Height": CRAH_H})
    
    # ─── PDUs (7 args) ───
    pdu_prof = create_rect_profile(f, PDU_W, PDU_D)
    for row in range(ROW_COUNT):
        row_y = FIRST_RACK_CY + row * ROW_SPACING
        for end in [0, RACKS_PER_ROW-1]:
            px = FIRST_RACK_CX + end * RACK_SPACING
            py = row_y + (RACK_D/2 + PDU_D/2) * (1 if row%2==0 else -1)
            pl_axis = create_axis2_placement3d(f, (px, py, AF_TOP))
            solid = create_extruded_solid(f, pdu_prof, PDU_H, pl_axis)
            rep = create_representation(f, [solid], ctx3d)
            pdu_pl = create_local_placement(f, (px, py, AF_TOP))
            pdu = f.createIfcFlowController(ifc.guid.new(), None, f"PDU_R{row}_E{end}", None, "PDU", pdu_pl, rep)
            f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [pdu], storey)
            add_pset(f, pdu, "Pset_DCM_PDU", {"Row": row, "End": end, "Width": PDU_W, "Depth": PDU_D, "Height": PDU_H})
    
    # ─── SPRINKLERS (7 args) ───
    sprinkler_z = SPRINKLER_DEFLECTOR_H
    spr_prof = create_rect_profile(f, 20, 20)
    spr_count = 0
    for sx in range(1500, ROOM_W, 3000):
        for sy in range(1500, ROOM_D, 3000):
            pl_axis = create_axis2_placement3d(f, (sx, sy, sprinkler_z))
            solid = create_extruded_solid(f, spr_prof, 50, pl_axis)
            rep = create_representation(f, [solid], ctx3d)
            spr_pl = create_local_placement(f, (sx, sy, sprinkler_z))
            spr = f.createIfcFlowTerminal(ifc.guid.new(), None, f"SPR_{spr_count}", None, "SPRINKLER", spr_pl, rep)
            f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [spr], storey)
            add_pset(f, spr, "Pset_DCM_Sprinkler", {"X": sx, "Y": sy, "DeflectorHeight": sprinkler_z, "Coverage": 9.0})
            spr_count += 1
    
    # ─── OVERHEAD SERVICES ROUTING - CONNECTED NETWORKS ───
    ENTRY_X = 2000
    ENTRY_Y = 5000
    SPINE_X = ROOM_W // 2  # 13500
    entry_point = (ENTRY_X, ENTRY_Y, 0)  # Z will be set per tier
    
    # CRAH connections that need horizontal runs from spine
    # For CRAHs at X=ROOM_W/2 (bottom/top), horizontal run is zero length (already on spine)
    # For CRAHs at X=0 or X=ROOM_W (sides), horizontal run needed
    crah_connections = [(cx, cy) for cx, cy in CRAH_POSITIONS if cx != SPINE_X]
    
    # Cable Tray
    tray_z = TRAY_TIER_H  # 2340
    tray_segments = build_connected_segments(
        (ENTRY_X, ENTRY_Y, tray_z), SPINE_X, tray_z, row_ys, row_serve_starts, row_serve_ends,
        crah_connections, tray_z
    )
    
    # Busway
    bus_z = BUS_TIER_H  # 2640
    bus_segments = build_connected_segments(
        (ENTRY_X, ENTRY_Y, bus_z), SPINE_X, bus_z, row_ys, row_serve_starts, row_serve_ends,
        crah_connections, bus_z
    )
    
    # CHW - serves rows AND all CRAHs
    chw_z = CHW_TIER_H  # 2200
    # For CHW, all CRAHs need connection (including bottom/top at spine X)
    chw_crah_connections = CRAH_POSITIONS  # all 6
    chw_segments = build_connected_segments(
        (ENTRY_X, ENTRY_Y, chw_z), SPINE_X, chw_z, row_ys, row_serve_starts, row_serve_ends,
        chw_crah_connections, chw_z
    )
    
    # ─── CREATE SERVICE ELEMENTS ───
    def create_service_segments(f, ctx, segments, width, height, name_prefix, ifc_class, obj_type, pset_name, pset_base):
        elements = []
        for i, (start, end) in enumerate(segments):
            sx, sy, sz = start
            ex, ey, ez = end
            dx, dy, dz = ex - sx, ey - sy, ez - sz
            length = math.sqrt(dx*dx + dy*dy + dz*dz)
            if length < 10:
                continue
            # Direction
            if abs(dx) > abs(dy) and abs(dx) > abs(dz):
                prof = create_rect_profile(f, width, height)
                x_dir = (1,0,0) if dx > 0 else (-1,0,0)
            elif abs(dy) > abs(dz):
                prof = create_rect_profile(f, height, width)
                x_dir = (0,1,0) if dy > 0 else (0,-1,0)
            else:
                prof = create_rect_profile(f, width, width)
                x_dir = (1,0,0)
            pl_axis = create_axis2_placement3d(f, (sx, sy, sz), (0,0,1), x_dir)
            solid = create_extruded_solid(f, prof, length, pl_axis)
            rep = create_representation(f, [solid], ctx)
            elem_pl = create_local_placement(f, (sx, sy, sz), None, (0,0,1), x_dir)
            elem = f.create_entity(ifc_class, ifc.guid.new(), None, f"{name_prefix}_{i}", None, obj_type, elem_pl, rep)
            f.createIfcRelContainedInSpatialStructure(ifc.guid.new(), None, None, None, [elem], storey)
            props = dict(pset_base)
            props.update({"SegmentIndex": i, "StartX": sx, "StartY": sy, "StartZ": sz, "EndX": ex, "EndY": ey, "EndZ": ez, "Length": length, "Width": width, "Height": height})
            add_pset(f, elem, pset_name, props)
            elements.append(elem)
        return elements
    
    tray_elems = create_service_segments(f, ctx3d, tray_segments, TRAY_W, TRAY_H, "TRAY", "IfcCableCarrierSegment", "CABLETRAY", "Pset_DCM_CableTray", {"System": "Telecom", "CoverHeight": TRAY_COVER_H, "TierZ": tray_z})
    bus_elems = create_service_segments(f, ctx3d, bus_segments, BUS_W, BUS_H, "BUS", "IfcFlowSegment", "BUSWAY", "Pset_DCM_Busway", {"System": "Power", "Voltage": "415V", "TierZ": bus_z})
    chw_elems = create_service_segments(f, ctx3d, chw_segments, PIPE_TOTAL_OD, PIPE_TOTAL_OD, "CHW", "IfcPipeSegment", "PIPE", "Pset_DCM_CHW", {"System": "ChilledWater", "PipeOD": PIPE_OD, "Insulation": PIPE_INSUL, "TierZ": chw_z})
    
    # ─── VALIDATION ───
    try:
        import ifcopenshell.validator
        v = ifcopenshell.validator.validate(f)
        if v:
            for issue in v:
                print(f"Validation: {issue}")
        else:
            print("IFC validation passed")
    except Exception as e:
        print(f"IFC validation warning: {e}")
    
    # Write
    f.write(out_path)
    print(f"Model written to {out_path}")
    print(f"Segments: Tray={len(tray_elems)}, Bus={len(bus_elems)}, CHW={len(chw_elems)}")
    
    # Reconciliation log
    reconciliation = {
        "drawings": ["A-101","A-301","A-601","A-602","E-101","F-101","M-101"],
        "room": {"width": ROOM_W, "depth": ROOM_D, "columns_grid": COL_GRID},
        "access_floor": {"height": AF_H, "clear_height": CLEAR_H},
        "racks": {"count": ROW_COUNT*RACKS_PER_ROW, "rows": ROW_COUNT, "per_row": RACKS_PER_ROW, "size": [RACK_W, RACK_D, RACK_H]},
        "crahs": {"count": len(CRAH_POSITIONS), "positions": CRAH_POSITIONS, "size": [CRAH_W, CRAH_D, CRAH_H]},
        "pdus": {"count": ROW_COUNT*2, "size": [PDU_W, PDU_D, PDU_H], "dedicated_height": PDU_DEDICATED_H},
        "sprinklers": {"grid": 3000, "deflector_height": SPRINKLER_DEFLECTOR_H, "clearance": SPRINKLER_CLEARANCE},
        "services": {
            "cable_tray": {"width": TRAY_W, "height": TRAY_H, "tier_center": tray_z, "top": tray_z + TRAY_H/2, "bottom": tray_z - TRAY_H/2, "segments": len(tray_elems)},
            "busway": {"width": BUS_W, "height": BUS_H, "tier_center": bus_z, "top": bus_z + BUS_H/2, "bottom": bus_z - BUS_H/2, "segments": len(bus_elems)},
            "chw": {"pipe_od": PIPE_OD, "insulation": PIPE_INSUL, "total_od": PIPE_TOTAL_OD, "tier_center": chw_z, "top": chw_z + PIPE_TOTAL_OD/2, "bottom": chw_z - PIPE_TOTAL_OD/2, "segments": len(chw_elems)}
        },
        "code_checks": {
            "headroom_min": HEADROOM_MIN,
            "sprinkler_clearance": SPRINKLER_CLEARANCE,
            "sprinkler_clear_zone_top": SPRINKLER_CLEAR_ZONE,
            "tray_bus_separation": TRAY_BUS_SEP,
            "pdu_dedicated_clear": PDU_DEDICATED_H,
            "pipe_insulation_in_clash": True,
            "ceiling_height": CEILING_H
        }
    }
    with open(out_path.replace(".ifc", "_reconciliation.json"), "w") as jf:
        json.dump(reconciliation, jf, indent=2)

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "output/model.ifc"
    os.makedirs(os.path.dirname(out), exist_ok=True)
    build_model(out)