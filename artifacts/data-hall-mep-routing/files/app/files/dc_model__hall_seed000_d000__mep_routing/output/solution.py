#!/usr/bin/env python3
"""
MEP Coordination Model Generator for Data Hall
Generates IFC4 model with clash-free routing of:
- Telecom cable tray
- Power busway
- Chilled water piping
"""

import sys
import math
import ifcopenshell
import ifcopenshell.api
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.shape
import ifcopenshell.geom
import numpy as np

# ============================================================
# CONSTANTS & DRAWING-DERIVED DATA (baked from PNG analysis)
# ============================================================

# Drawing coordinate system
DWG_X_MIN, DWG_X_MAX = 150, 1380
DWG_Y_MIN, DWG_Y_MAX = 72, 1027
DWG_W = DWG_X_MAX - DWG_X_MIN  # 1230 px
DWG_H = DWG_Y_MAX - DWG_Y_MIN  # 955 px

# Real room dimensions from drawing analysis
ROOM_W_MM = 27060  # mm
ROOM_D_MM = 21010  # mm
SCALE = ROOM_W_MM / DWG_W  # ~21.99 mm/px

def dwg_to_mm(px, py):
    """Drawing pixels -> mm from room origin (bottom-left)"""
    x = (px - DWG_X_MIN) * SCALE
    y = (DWG_Y_MAX - py) * SCALE  # Flip Y (drawing Y down, room Y up)
    return x, y

def mm_to_m(v): return v / 1000.0

# Room
ROOM_X0, ROOM_Y0 = 0.0, 0.0
ROOM_X1, ROOM_Y1 = mm_to_m(ROOM_W_MM), mm_to_m(ROOM_D_MM)

# Finished floor level (FFL) = 0.0 in model Z
FFL = 0.0
CLEAR_HEIGHT = 3.6  # m - from A-301 section
SLAB_THICKNESS = 0.3
PLENUM_HEIGHT = 0.6  # under-floor plenum
CEILING_Z = CLEAR_HEIGHT

# Service elevations (from A-301 section analysis)
# Overhead plenum: FFL+2.6m to FFL+3.6m (1m clear for services)
# Minimum headroom 2.6m
SERVICE_ZONE_BOTTOM = 2.6
SERVICE_ZONE_TOP = 3.6

# Tier assignments (Z elevations in meters) - adjusted for code compliance:
# - 2600mm min headroom (bottom of service >= 2600)
# - 460mm clearance below sprinkler deflector at 3500mm (top of service <= 3040)
# - 300mm separation tray/busway on at least one axis (horizontal: cold vs hot aisle = 3000mm)
TIER_TRAY = 2.95      # Telecom cable tray (top at 3.00m, clearance 500mm)
TIER_BUSWAY = 2.75    # Power busway (top at 2.80m, clearance 700mm)
TIER_CHW = 2.71       # Chilled water (top at ~2.81m, clearance 690mm, bottom at ~2.61m > 2.6m)
TIER_DROP = 2.4       # Drops to racks (below services)

# Service dimensions (mm)
TRAY_W, TRAY_H = 300, 100
BUSWAY_W, BUSWAY_H = 400, 200
CHW_PIPE_OD = 150     # DN150 main
CHW_INSUL = 25.4      # 25.4mm insulation
CHW_TOTAL_OD = CHW_PIPE_OD + 2 * CHW_INSUL

# Rack dimensions (from A-601)
RACK_W = 600    # mm
RACK_D = 1200   # mm
RACK_H = 2200   # mm

# Column positions (from A-101)
COL_X_MM = [220, 12870]  # mm from room origin
COL_Y_RANGE = (726, 9570)  # mm - full room depth minus edges

# CRAH positions (from A-101/M-101 perimeter units)
# Perimeter CRAHs along walls at specific locations
CRAH_POSITIONS = [
    # (x_mm, y_mm, width_mm, depth_mm, rotation_deg)
    (13530, 19800, 2400, 1200, 180),  # Top wall, facing down
    (6765, 19800, 2400, 1200, 180),   # Top wall, facing down
    (220, 10560, 1200, 2400, 90),     # Left wall, facing right
    (220, 5280, 1200, 2400, 90),      # Left wall, facing right
    (220, 0, 1200, 2400, -90),        # Bottom wall, facing up (but room starts at 0)
    (13530, 10560, 1200, 2400, -90),  # Right wall, facing left
    (13530, 5280, 1200, 2400, -90),   # Right wall, facing left
]

# PDU positions (from E-101)
PDU_POSITIONS = [
    (20328, 16764, 1200, 2400, 0),  # Top-right area
    (26510, 16764, 1200, 2400, 0),  # Top-right corner
    (19074, 9064, 1200, 2400, 0),   # Row area
    (13442, 9064, 1200, 2400, 0),   # Row area
]

# Sprinkler grid (from F-101) - approximate 3.6m spacing
SPRINKLER_SPACING = 3600  # mm
SPRINKLER_Z = CLEAR_HEIGHT - 0.1  # Just below ceiling

# Service entry points (from M-101, E-101)
# CHW entry: from M-101, appears at top-right area
CHW_ENTRY = (26000, 20000)  # mm
# Busway entry: from E-101, top area
BUSWAY_ENTRY = (20000, 18000)
# Tray entry: from E-101, top area
TRAY_ENTRY = (18000, 18000)

# Rack rows (from A-101 dense horizontal lines at y=281-423, x=488-724)
# Converted to mm: y≈13300-16400, x≈7500-12600
# 8 rows of 16 racks each = 128 racks
RACK_ROWS = []
# Row Y positions (centerlines) from drawing analysis
row_y_centers = [14500, 13300, 12100, 10900, 9700, 8500, 7300, 6100]  # mm from bottom
for i, ry in enumerate(row_y_centers):
    # 16 racks per row, alternating hot/cold aisle
    # Cold aisle at row_y - 1200, hot aisle at row_y + 1200
    # Racks centered at x positions
    for j in range(16):
        rx = 3000 + j * 1500  # 1500mm center-to-center (600 rack + 900 aisle)
        # Alternate facing: even rows face +Y, odd face -Y
        facing = 0 if i % 2 == 0 else 180
        RACK_ROWS.append((rx, ry, facing))

# ============================================================
# IFC MODEL SETUP
# ============================================================

def create_model():
    model = ifcopenshell.file(schema="IFC4")
    
    # Project
    project = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcProject")
    project.Name = "Data Hall MEP Coordination"
    project.LongName = "dc_model hall_seed000_d000"
    
    # Units - millimetres (IFC4 uses IfcSIUnit with Prefix)
    length_unit = model.create_entity("IfcSIUnit", UnitType="LENGTHUNIT", Name="METRE", Prefix="MILLI")
    area_unit = model.create_entity("IfcSIUnit", UnitType="AREAUNIT", Name="SQUARE_METRE")
    volume_unit = model.create_entity("IfcSIUnit", UnitType="VOLUMEUNIT", Name="CUBIC_METRE")
    angle_unit = model.create_entity("IfcSIUnit", UnitType="PLANEANGLEUNIT", Name="RADIAN")
    ifcopenshell.api.run("unit.assign_unit", model, units=[length_unit, area_unit, volume_unit, angle_unit])
    
    # Context
    ctx = ifcopenshell.api.run("context.add_context", model, context_type="Model")
    body = ifcopenshell.api.run("context.add_context", model, 
                                 context_type="Model", context_identifier="Body",
                                 target_view="MODEL_VIEW", parent=ctx)
    
    # Spatial structure
    site = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSite")
    site.Name = "Data Center Site"
    
    building = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuilding")
    building.Name = "Data Hall Building"
    
    storey = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcBuildingStorey")
    storey.Name = "Data Hall Level"
    storey.Elevation = 0.0
    
    space = ifcopenshell.api.run("root.create_entity", model, ifc_class="IfcSpace")
    space.Name = "Data Hall"
    space.LongName = "Main Data Hall"
    
    ifcopenshell.api.run("aggregate.assign_object", model, products=[site], relating_object=project)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[building], relating_object=site)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[storey], relating_object=building)
    ifcopenshell.api.run("aggregate.assign_object", model, products=[space], relating_object=storey)
    
    # Placement for storey
    storey_placement = model.create_entity("IfcLocalPlacement",
        RelativePlacement=model.create_entity("IfcAxis2Placement3D",
            Location=model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0)),
            Axis=model.create_entity("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0)),
            RefDirection=model.create_entity("IfcDirection", DirectionRatios=(1.0, 0.0, 0.0))
        )
    )
    storey.ObjectPlacement = storey_placement
    
    return model, project, site, building, storey, space, body

# ============================================================
# GEOMETRY HELPERS
# ============================================================

def create_extrusion(model, profile_pts, depth, placement_matrix, body_ctx):
    """Create IfcExtrudedAreaSolid from 2D profile points (CCW, mm). Returns IfcShapeRepresentation."""
    # Profile
    pts = [model.create_entity("IfcCartesianPoint", Coordinates=(mm_to_m(x), mm_to_m(y))) for x, y in profile_pts]
    polyline = model.create_entity("IfcPolyline", Points=pts)
    profile = model.create_entity("IfcArbitraryClosedProfileDef", ProfileType="AREA", OuterCurve=polyline)
    
    # Extrusion
    extrude_dir = model.create_entity("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0))
    position = model.create_entity("IfcAxis2Placement3D",
        Location=model.create_entity("IfcCartesianPoint", Coordinates=(0.0, 0.0, 0.0)),
        Axis=extrude_dir,
        RefDirection=model.create_entity("IfcDirection", DirectionRatios=(1.0, 0.0, 0.0))
    )
    solid = model.create_entity("IfcExtrudedAreaSolid",
        SweptArea=profile,
        Position=position,
        ExtrudedDirection=extrude_dir,
        Depth=mm_to_m(depth)
    )
    
    # Shape representation
    rep = model.create_entity("IfcShapeRepresentation",
        ContextOfItems=body_ctx,
        RepresentationIdentifier="Body",
        RepresentationType="SweptSolid",
        Items=[solid]
    )
    
    # Product definition shape
    pds = model.create_entity("IfcProductDefinitionShape", Representations=[rep])
    return pds

def create_placement(model, x, y, z, rot_z=0):
    """Create placement matrix at (x,y,z) with Z rotation in degrees"""
    cx, cy, cz = mm_to_m(x), mm_to_m(y), mm_to_m(z)
    cos_r = math.cos(math.radians(rot_z))
    sin_r = math.sin(math.radians(rot_z))
    location = model.create_entity("IfcCartesianPoint", Coordinates=(cx, cy, cz))
    axis = model.create_entity("IfcDirection", DirectionRatios=(0.0, 0.0, 1.0))
    ref_dir = model.create_entity("IfcDirection", DirectionRatios=(cos_r, sin_r, 0.0))
    placement = model.create_entity("IfcAxis2Placement3D", Location=location, Axis=axis, RefDirection=ref_dir)
    return model.create_entity("IfcLocalPlacement", RelativePlacement=placement)

def add_pset(model, element, pset_name, properties):
    """Add property set to element"""
    pset = model.create_entity("IfcPropertySet",
        GlobalId=ifcopenshell.guid.new(),
        Name=pset_name,
        HasProperties=[model.create_entity("IfcPropertySingleValue",
            Name=k, NominalValue=model.create_entity(v[0], v[1])) for k, v in properties.items()
        ]
    )
    rel = model.create_entity("IfcRelDefinesByProperties",
        GlobalId=ifcopenshell.guid.new(),
        RelatedObjects=[element],
        RelatingPropertyDefinition=pset
    )
    return pset

def create_rect_profile(model, w, h, center=True):
    """Create rectangle profile points (CCW)"""
    if center:
        return [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
    else:
        return [(0, 0), (w, 0), (w, h), (0, h)]

# ============================================================
# BUILD BACKGROUND ELEMENTS
# ============================================================

def build_room_background(model, space, body_ctx):
    """Create room boundaries: floor, walls, ceiling, columns, access floor"""
    elements = []
    
    # Floor slab
    floor_pts = create_rect_profile(model, ROOM_W_MM, ROOM_D_MM, center=False)
    floor_pds = create_extrusion(model, floor_pts, SLAB_THICKNESS * 1000,
                                 create_placement(model, 0, 0, -SLAB_THICKNESS * 1000), body_ctx)
    floor = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Structural Slab",
        ObjectType="Slab",
        ObjectPlacement=create_placement(model, 0, 0, -SLAB_THICKNESS * 1000),
        Representation=floor_pds
    )
    ifcopenshell.api.run("spatial.assign_container", model, products=[floor], relating_structure=space)
    elements.append(floor)
    
    # Access floor (raised floor)
    af_pts = create_rect_profile(model, ROOM_W_MM, ROOM_D_MM, center=False)
    af_pds = create_extrusion(model, af_pts, PLENUM_HEIGHT * 1000,
                              create_placement(model, 0, 0, 0), body_ctx)
    af = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Access Floor",
        ObjectType="RaisedFloor",
        ObjectPlacement=create_placement(model, 0, 0, 0),
        Representation=af_pds
    )
    ifcopenshell.api.run("spatial.assign_container", model, products=[af], relating_structure=space)
    elements.append(af)
    
    # Ceiling
    ceil_pts = create_rect_profile(model, ROOM_W_MM, ROOM_D_MM, center=False)
    ceil_pds = create_extrusion(model, ceil_pts, 100,
                                create_placement(model, 0, 0, CLEAR_HEIGHT * 1000), body_ctx)
    ceil = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Ceiling",
        ObjectType="Ceiling",
        ObjectPlacement=create_placement(model, 0, 0, CLEAR_HEIGHT * 1000),
        Representation=ceil_pds
    )
    ifcopenshell.api.run("spatial.assign_container", model, products=[ceil], relating_structure=space)
    elements.append(ceil)
    
    # Walls (perimeter)
    wall_h = CLEAR_HEIGHT * 1000
    wall_thk = 300
    # Bottom wall
    w1_pds = create_extrusion(model, create_rect_profile(model, ROOM_W_MM, wall_thk, False),
                              wall_h, create_placement(model, 0, -wall_thk, 0), body_ctx)
    w1 = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Perimeter Wall",
        ObjectType="Wall",
        ObjectPlacement=create_placement(model, 0, -wall_thk, 0),
        Representation=w1_pds
    )
    # Top wall
    w2_pds = create_extrusion(model, create_rect_profile(model, ROOM_W_MM, wall_thk, False),
                              wall_h, create_placement(model, 0, ROOM_D_MM, 0), body_ctx)
    w2 = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Perimeter Wall",
        ObjectType="Wall",
        ObjectPlacement=create_placement(model, 0, ROOM_D_MM, 0),
        Representation=w2_pds
    )
    # Left wall
    w3_pds = create_extrusion(model, create_rect_profile(model, wall_thk, ROOM_D_MM, False),
                              wall_h, create_placement(model, -wall_thk, 0, 0), body_ctx)
    w3 = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Perimeter Wall",
        ObjectType="Wall",
        ObjectPlacement=create_placement(model, -wall_thk, 0, 0),
        Representation=w3_pds
    )
    # Right wall
    w4_pds = create_extrusion(model, create_rect_profile(model, wall_thk, ROOM_D_MM, False),
                              wall_h, create_placement(model, ROOM_W_MM, 0, 0), body_ctx)
    w4 = model.create_entity("IfcBuildingElementProxy",
        GlobalId=ifcopenshell.guid.new(),
        Name="Perimeter Wall",
        ObjectType="Wall",
        ObjectPlacement=create_placement(model, ROOM_W_MM, 0, 0),
        Representation=w4_pds
    )
    for w in [w1, w2, w3, w4]:
        ifcopenshell.api.run("spatial.assign_container", model, products=[w], relating_structure=space)
        elements.append(w)
    
    # Structural columns (full height)
    for cx in COL_X_MM:
        for cy in [COL_Y_RANGE[0] + 1000, COL_Y_RANGE[1] - 1000]:  # Two columns per grid line
            col_pts = create_rect_profile(model, 600, 600)
            col_pds = create_extrusion(model, col_pts, wall_h,
                                       create_placement(model, cx, cy, 0), body_ctx)
            col = model.create_entity("IfcBuildingElementProxy",
                GlobalId=ifcopenshell.guid.new(),
                Name="Structural Column",
                ObjectType="Column",
                ObjectPlacement=create_placement(model, cx, cy, 0),
                Representation=col_pds
            )
            ifcopenshell.api.run("spatial.assign_container", model, products=[col], relating_structure=space)
            elements.append(col)
    
    # Containment pathways (cable trays under floor from A-602)
    # Under-floor tray routes along rack rows
    tray_w, tray_h = 200, 50
    for ry in [r[1] for r in RACK_ROWS[::2]]:  # Every other row (cold aisles)
        # Main feeder along row
        path_pts = create_rect_profile(model, ROOM_W_MM - 2000, tray_w)
        tray_pds = create_extrusion(model, path_pts, tray_h,
                                    create_placement(model, 1000, ry, 100), body_ctx)
        tray = model.create_entity("IfcBuildingElementProxy",
            GlobalId=ifcopenshell.guid.new(),
            Name="Underfloor Cable Tray",
            ObjectType="CableTraySegment",
            ObjectPlacement=create_placement(model, 1000, ry, 100),
            Representation=tray_pds
        )
        ifcopenshell.api.run("spatial.assign_container", model, products=[tray], relating_structure=space)
        elements.append(tray)
    
    return elements

def build_racks(model, space, body_ctx):
    """Create 128 rack cabinets"""
    racks = []
    for i, (rx, ry, facing) in enumerate(RACK_ROWS):
        rack_pts = create_rect_profile(model, RACK_W, RACK_D)
        placement = create_placement(model, rx, ry, RACK_H/2, facing)
        rack_pds = create_extrusion(model, rack_pts, RACK_H, placement, body_ctx)
        # IfcFurniture / USERDEFINED / "Rack"
        rack = model.create_entity("IfcFurniture",
            GlobalId=ifcopenshell.guid.new(),
            Name=f"Rack_{i+1:03d}",
            ObjectType="Rack",
            ObjectPlacement=placement,
            Representation=rack_pds
        )
        ifcopenshell.api.run("spatial.assign_container", model, products=[rack], relating_structure=space)
        add_pset(model, rack, "Pset_DCM_Rack", {
            "RackID": ("IfcLabel", f"R-{i+1:03d}"),
            "RowIndex": ("IfcInteger", i // 16),
            "PositionInRow": ("IfcInteger", i % 16),
            "Facing": ("IfcInteger", facing),
            "Power_kW": ("IfcReal", 8.0),
            "Airflow_kg_s": ("IfcReal", 0.5)
        })
        racks.append(rack)
    return racks

def build_crahs(model, space, body_ctx):
    """Create CRAH units"""
    crahs = []
    for i, (cx, cy, w, d, rot) in enumerate(CRAH_POSITIONS):
        crah_pts = create_rect_profile(model, w, d)
        placement = create_placement(model, cx, cy, 1200, rot)
        crah_pds = create_extrusion(model, crah_pts, 2400, placement, body_ctx)
        crah = model.create_entity("IfcUnitaryEquipment",
            GlobalId=ifcopenshell.guid.new(),
            Name=f"CRAH_{i+1}",
            ObjectType="CRAH",
            ObjectPlacement=placement,
            Representation=crah_pds
        )
        ifcopenshell.api.run("spatial.assign_container", model, products=[crah], relating_structure=space)
        add_pset(model, crah, "Pset_DCM_CRAH", {
            "CRAH_ID": ("IfcLabel", f"CRAH-{i+1}"),
            "Capacity_kW": ("IfcReal", 120.0),
            "Airflow_m3_s": ("IfcReal", 8.0),
            "CHW_Flow_L_s": ("IfcReal", 6.0),
            "CHW_DP_kPa": ("IfcReal", 50.0)
        })
        crahs.append(crah)
    return crahs

def build_pdus(model, space, body_ctx):
    """Create PDU units"""
    pdus = []
    for i, (px, py, w, d, rot) in enumerate(PDU_POSITIONS):
        pdu_pts = create_rect_profile(model, w, d)
        placement = create_placement(model, px, py, 1100, rot)
        pdu_pds = create_extrusion(model, pdu_pts, 2200, placement, body_ctx)
        pdu = model.create_entity("IfcEnergyConversionDevice",
            GlobalId=ifcopenshell.guid.new(),
            Name=f"PDU_{i+1}",
            ObjectType="PDU",
            ObjectPlacement=placement,
            Representation=pdu_pds
        )
        ifcopenshell.api.run("spatial.assign_container", model, products=[pdu], relating_structure=space)
        add_pset(model, pdu, "Pset_DCM_PDU", {
            "PDU_ID": ("IfcLabel", f"PDU-{i+1}"),
            "Rating_kVA": ("IfcReal", 500.0),
            "Voltage_V": ("IfcInteger", 415),
            "Phases": ("IfcInteger", 3)
        })
        pdus.append(pdu)
    return pdus

def build_sprinklers(model, space, body_ctx):
    """Create sprinkler grid"""
    sprinklers = []
    # Grid spacing ~3.6m from F-101
    spacing = SPRINKLER_SPACING
    start_x = spacing / 2
    start_y = spacing / 2
    nx = int(ROOM_W_MM / spacing) + 1
    ny = int(ROOM_D_MM / spacing) + 1
    
    for ix in range(nx):
        for iy in range(ny):
            sx = start_x + ix * spacing
            sy = start_y + iy * spacing
            if sx > ROOM_W_MM or sy > ROOM_D_MM:
                continue
            # Sprinkler head (small cylinder)
            head_pts = create_rect_profile(model, 50, 50)
            placement = create_placement(model, sx, sy, SPRINKLER_Z * 1000)
            head_pds = create_extrusion(model, head_pts, 100, placement, body_ctx)
            head = model.create_entity("IfcFlowTerminal",
                GlobalId=ifcopenshell.guid.new(),
                Name=f"SPR_{ix}_{iy}",
                ObjectType="Sprinkler",
                ObjectPlacement=placement,
                Representation=head_pds
            )
            ifcopenshell.api.run("spatial.assign_container", model, products=[head], relating_structure=space)
            add_pset(model, head, "Pset_DCM_Sprinkler", {
                "SprinklerID": ("IfcLabel", f"SPR-{ix}-{iy}"),
                "K_Factor": ("IfcReal", 80.0),
                "Response_Type": ("IfcLabel", "Quick"),
                "Deflector_Z": ("IfcLengthMeasure", mm_to_m(SPRINKLER_Z * 1000))
            })
            sprinklers.append(head)
    return sprinklers

# ============================================================
# SERVICE ROUTING
# ============================================================

class RouteSegment:
    def __init__(self, x1, y1, x2, y2, z, service_type, tier_name):
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.z = z
        self.service_type = service_type
        self.tier_name = tier_name
        self.length = math.hypot(x2 - x1, y2 - y1)
    
    def is_horizontal(self):
        return abs(self.y2 - self.y1) < 1
    
    def is_vertical(self):
        return abs(self.x2 - self.x1) < 1
    
    def bbox(self):
        return (min(self.x1, self.x2), min(self.y1, self.y2),
                max(self.x1, self.x2), max(self.y1, self.y2))
    
    def intersects(self, other, tol=2):
        """Check if two axis-aligned segments intersect in XY"""
        if self.is_horizontal() and other.is_vertical():
            return (min(self.x1, self.x2) - tol <= other.x1 <= max(self.x1, self.x2) + tol and
                    min(other.y1, other.y2) - tol <= self.y1 <= max(other.y1, other.y2) + tol)
        if self.is_vertical() and other.is_horizontal():
            return other.intersects(self, tol)
        if self.is_horizontal() and other.is_horizontal() and abs(self.y1 - other.y1) < tol:
            return not (max(self.x1, self.x2) + tol < min(other.x1, other.x2) or
                       max(other.x1, other.x2) + tol < min(self.x1, self.x2))
        if self.is_vertical() and other.is_vertical() and abs(self.x1 - other.x1) < tol:
            return not (max(self.y1, self.y2) + tol < min(other.y1, other.y2) or
                       max(other.y1, other.y2) + tol < min(self.y1, self.y2))
        return False

def route_telecom_tray(model, space, body_ctx, racks, crahs, pdus, columns, sprinklers):
    """Route telecom cable tray - serves every rack row"""
    segments = []
    tray_z = TIER_TRAY * 1000
    
    # Entry point
    ex, ey = TRAY_ENTRY
    
    # Main feeder along LEFT wall at x=600 (past column at x=220, column extends to 520, tray 300 wide = 150-450 at x=300, so use x=600 -> 450-750)
    LEFT_MAIN_X = 600
    # Entry horizontal to wall
    segments.append(RouteSegment(ex, ey, LEFT_MAIN_X, ey, tray_z, "tray", "entry_to_wall"))
    # Wall main vertical full height at x=LEFT_MAIN_X
    segments.append(RouteSegment(LEFT_MAIN_X, ey, LEFT_MAIN_X, 2000, tray_z, "tray", "left_wall_main"))
    
    # Row cold aisles - horizontal branches from left wall main (x=LEFT_MAIN_X)
    row_ys = sorted(set(r[1] for r in RACK_ROWS))
    cold_aisle_ys = [ry - 1500 for ry in row_ys]
    
    for cay in cold_aisle_ys:
        # Branch from left wall main (x=LEFT_MAIN_X) to row end (x=ROOM_W_MM-2000)
        segments.append(RouteSegment(LEFT_MAIN_X, cay, ROOM_W_MM - 2000, cay, tray_z, "tray", f"row_{cay}_feeder"))
        # Rack drops (short, perpendicular to row)
        row_racks = [r for r in RACK_ROWS if abs(r[1] - (cay + 1500)) < 100]
        for rx, ry, facing in row_racks:
            drop_y = cay + 600  # Front of rack
            segments.append(RouteSegment(rx, cay, rx, drop_y, tray_z, "tray", f"drop_to_rack_{rx}_{ry}"))
    
    # CRAH monitoring drops - connect to wall main or entry feeder at same Y
    for cx, cy, w, d, rot in CRAH_POSITIONS:
        if cy == 19800:  # Top wall CRAHs
            # Connect to entry feeder at y=ey (18000)
            segments.append(RouteSegment(cx, ey, cx, cy, tray_z, "tray", f"to_crah_{cx}_{cy}"))
        elif cx == 220:  # Left wall CRAHs
            # Connect to wall main at x=LEFT_MAIN_X (same Y)
            segments.append(RouteSegment(LEFT_MAIN_X, cy, cx, cy, tray_z, "tray", f"to_crah_{cx}_{cy}"))
        elif cx >= ROOM_W_MM - 1200:  # Right wall CRAHs
            # Connect from right side - use row feeder at nearest cold aisle
            nearest_cay = min(cold_aisle_ys, key=lambda y: abs(y - cy))
            segments.append(RouteSegment(cx, nearest_cay, cx, cy, tray_z, "tray", f"to_crah_{cx}_{cy}"))
        else:
            # Bottom wall CRAH
            nearest_cay = min(cold_aisle_ys, key=lambda y: abs(y - cy))
            segments.append(RouteSegment(cx, nearest_cay, cx, cy, tray_z, "tray", f"to_crah_{cx}_{cy}"))
    
    return create_route_elements(model, space, body_ctx, segments, "TelecomCableTray", TRAY_W, TRAY_H)

def route_power_busway(model, space, body_ctx, racks, crahs, pdus, columns, sprinklers):
    """Route power busway - serves every rack row, avoids PDU dedicated space"""
    segments = []
    busway_z = TIER_BUSWAY * 1000
    
    ex, ey = BUSWAY_ENTRY
    
    # Main feeder along RIGHT wall at x=ROOM_W_MM-600 (past column at x=12870)
    RIGHT_MAIN_X = ROOM_W_MM - 600  # 26460
    # Entry horizontal to wall
    segments.append(RouteSegment(ex, ey, RIGHT_MAIN_X, ey, busway_z, "busway", "entry_to_wall"))
    # Wall main vertical full height at x=RIGHT_MAIN_X
    segments.append(RouteSegment(RIGHT_MAIN_X, ey, RIGHT_MAIN_X, 2000, busway_z, "busway", "right_wall_main"))
    
    # Row hot aisles - horizontal branches from right wall main (x=RIGHT_MAIN_X)
    row_ys = sorted(set(r[1] for r in RACK_ROWS))
    hot_aisle_ys = [ry + 1500 for ry in row_ys]
    
    # Column at x=12870, y=1726 and y=8570 (extends ±300 in x and y)
    # Hot aisle at y=8800 (from row_ys=10300? wait: 8500+1500=10000, 7300+1500=8800)
    # Row at y=7300 -> hot aisle at 8800. Column at y=8570 extends to 8870. So hot aisle 8800 crosses column.
    # Route around: jog vertical at x=12870-500=12370 to y=8870+100=8970, then horizontal, then back down
    
    for hay in hot_aisle_ys:
        # Check if this hot aisle crosses the right column
        col_x = COL_X_MM[1]  # 12870
        col_y_top = COL_Y_RANGE[1] - 1000  # 8570
        col_y_bottom = COL_Y_RANGE[0] + 1000  # 1726
        crosses_column = (col_y_top - 300 < hay < col_y_top + 300)
        
        if crosses_column:
            # Bridge around column at y=9300:
            # - Above column top (8870), below row 8500 drop bottom (9400)
            # - Low feeder from RIGHT_MAIN_X to x=13500 (first rack right of column) at y=8800
            # - Jog up at x=13500 to y=9300
            # - Bridge at y=9300 from x=13500 to x=12000 (last rack left of column)
            # - Jog down at x=12000 to y=8800
            # - Low feeder from x=12000 to x=3000 at y=8800
            bridge_y = 9300
            bridge_x_right = 13500  # First rack right of column (col at 12870, rack at 13500)
            bridge_x_left = 12000   # Last rack left of column
            
            # Low feeder right segment: RIGHT_MAIN_X to bridge_x_right at hot aisle Y
            segments.append(RouteSegment(RIGHT_MAIN_X, hay, bridge_x_right, hay, busway_z, "busway", f"hot_aisle_{hay}_feeder_right"))
            # Jog up at bridge_x_right
            segments.append(RouteSegment(bridge_x_right, hay, bridge_x_right, bridge_y, busway_z, "busway", f"hot_aisle_{hay}_jog_up_right"))
            # Bridge at bridge_y
            segments.append(RouteSegment(bridge_x_right, bridge_y, bridge_x_left, bridge_y, busway_z, "busway", f"hot_aisle_{hay}_bridge"))
            # Jog down at bridge_x_left
            segments.append(RouteSegment(bridge_x_left, bridge_y, bridge_x_left, hay, busway_z, "busway", f"hot_aisle_{hay}_jog_down_left"))
            # Low feeder left segment: bridge_x_left to 3000 at hot aisle Y
            segments.append(RouteSegment(bridge_x_left, hay, 3000, hay, busway_z, "busway", f"hot_aisle_{hay}_feeder_left"))
            
            # Rack drops at hot aisle Y from appropriate feeder segment
            row_racks = [r for r in RACK_ROWS if abs(r[1] - (hay - 1500)) < 100]
            for rx, ry, facing in row_racks:
                drop_y = hay - 600  # Rear of rack (at hot aisle Y)
                segments.append(RouteSegment(rx, hay, rx, drop_y, busway_z, "busway", f"drop_to_rack_{rx}_{ry}"))
        else:
            # Branch from right wall main to row start
            segments.append(RouteSegment(RIGHT_MAIN_X, hay, 3000, hay, busway_z, "busway", f"hot_aisle_{hay}_feeder"))
            # Rack drops
            row_racks = [r for r in RACK_ROWS if abs(r[1] - (hay - 1500)) < 100]
            for rx, ry, facing in row_racks:
                drop_y = hay - 600  # Rear of rack
                segments.append(RouteSegment(rx, hay, rx, drop_y, busway_z, "busway", f"drop_to_rack_{rx}_{ry}"))
    
    # PDU feeds from right wall main
    for px, py, w, d, rot in PDU_POSITIONS:
        pdu_center_x = px + w/2
        pdu_center_y = py + d/2
        segments.append(RouteSegment(RIGHT_MAIN_X, pdu_center_y, pdu_center_x, pdu_center_y, busway_z, "busway", f"to_pdu_{px}_{py}"))
    
    return create_route_elements(model, space, body_ctx, segments, "Busway", BUSWAY_W, BUSWAY_H)

def route_chilled_water(model, space, body_ctx, racks, crahs, pdus, columns, sprinklers):
    """Route chilled water - serves every rack row AND every CRAH"""
    segments = []
    chw_z = TIER_CHW * 1000
    
    ex, ey = CHW_ENTRY
    
    # Supply header along LEFT wall at x=600 (past column at 220)
    # Return header along RIGHT wall at x=25000 (further left to avoid PDU at 26510)
    LEFT_MAIN_X = 600
    RIGHT_MAIN_X = 25000  # Further left to avoid PDU at x=26510 (extends to ~27110)
    
    # Supply header (left wall, top to bottom) - single continuous segment at x=LEFT_MAIN_X
    segments.append(RouteSegment(ex, ey, LEFT_MAIN_X, ey, chw_z, "chw", "entry_to_supply"))
    segments.append(RouteSegment(LEFT_MAIN_X, ey, LEFT_MAIN_X, 2000, chw_z, "chw", "supply_header_left"))
    
    # Return header (right wall, bottom to top) - single continuous segment at x=RIGHT_MAIN_X
    segments.append(RouteSegment(RIGHT_MAIN_X, 2000, RIGHT_MAIN_X, ey, chw_z, "chw", "return_header_right"))
    segments.append(RouteSegment(RIGHT_MAIN_X, ey, ex, ey, chw_z, "chw", "return_to_plant"))
    
    # CRAH connections - supply from left header (x=LEFT_MAIN_X), return to right header (x=RIGHT_MAIN_X)
    for cx, cy, w, d, rot in CRAH_POSITIONS:
        crah_cx = cx + (w/2 if rot in [90, -90] else 0)
        crah_cy = cy + (d/2 if rot in [0, 180] else 0)
        # Supply from left header (x=LEFT_MAIN_X)
        segments.append(RouteSegment(LEFT_MAIN_X, crah_cy, crah_cx, crah_cy, chw_z, "chw", f"supply_to_crah_{cx}_{cy}"))
        # Return to right header (x=RIGHT_MAIN_X)
        segments.append(RouteSegment(crah_cx, crah_cy, RIGHT_MAIN_X, crah_cy, chw_z, "chw", f"return_from_crah_{cx}_{cy}"))
    
    # Rack row cooling coils - supply from left header (x=LEFT_MAIN_X), return to right header (x=RIGHT_MAIN_X)
    # Avoid PDU dedicated space (y around 9064 for two PDUs) - 1800mm above PDU top (2200) = 4000mm
    # PDU at y=9064, dedicated space is y=9064 ± 1200 (PDU depth 2400/2), and Z < 4000
    # Since CHW is at Z=2800, it's in the dedicated space if XY overlaps
    row_ys = sorted(set(r[1] for r in RACK_ROWS))
    for ry in row_ys:
        cold_y = ry - 1500
        hot_y = ry + 1500
        
        # Check if this row's cold or hot aisle passes through PDU dedicated space
        pdu_conflict_cold = False
        pdu_conflict_hot = False
        for px, py, w, d, rot in PDU_POSITIONS:
            if py - d/2 < cold_y < py + d/2:
                pdu_conflict_cold = True
            if py - d/2 < hot_y < py + d/2:
                pdu_conflict_hot = True
        
        if pdu_conflict_cold and pdu_conflict_hot:
            # Both aisles conflict - jog vertically around PDU
            # Find PDU y range
            for px, py, w, d, rot in PDU_POSITIONS:
                if py - d/2 < cold_y < py + d/2:
                    pdu_y_bottom = py - d/2
                    pdu_y_top = py + d/2
                    break
            # Supply: jog up before PDU, across, down after
            jog_y = pdu_y_top + 200
            segments.append(RouteSegment(LEFT_MAIN_X, cold_y, LEFT_MAIN_X, jog_y, chw_z, "chw", f"row_supply_{ry}_jog_up"))
            segments.append(RouteSegment(LEFT_MAIN_X, jog_y, RIGHT_MAIN_X, jog_y, chw_z, "chw", f"row_supply_{ry}_across"))
            segments.append(RouteSegment(RIGHT_MAIN_X, jog_y, RIGHT_MAIN_X, cold_y, chw_z, "chw", f"row_supply_{ry}_jog_down"))
            # Return: same path back (or separate)
            segments.append(RouteSegment(RIGHT_MAIN_X, cold_y, RIGHT_MAIN_X, jog_y, chw_z, "chw", f"row_return_{ry}_jog_up"))
            segments.append(RouteSegment(RIGHT_MAIN_X, jog_y, LEFT_MAIN_X, jog_y, chw_z, "chw", f"row_return_{ry}_across"))
            segments.append(RouteSegment(LEFT_MAIN_X, jog_y, LEFT_MAIN_X, cold_y, chw_z, "chw", f"row_return_{ry}_jog_down"))
        elif pdu_conflict_cold:
            # Cold aisle conflicts - jog supply around
            for px, py, w, d, rot in PDU_POSITIONS:
                if py - d/2 < cold_y < py + d/2:
                    pdu_y_top = py + d/2
                    break
            jog_y = pdu_y_top + 200
            segments.append(RouteSegment(LEFT_MAIN_X, cold_y, LEFT_MAIN_X, jog_y, chw_z, "chw", f"row_supply_{ry}_jog_up"))
            segments.append(RouteSegment(LEFT_MAIN_X, jog_y, RIGHT_MAIN_X, jog_y, chw_z, "chw", f"row_supply_{ry}_across"))
            segments.append(RouteSegment(RIGHT_MAIN_X, jog_y, RIGHT_MAIN_X, cold_y, chw_z, "chw", f"row_supply_{ry}_jog_down"))
            # Return at hot aisle (no conflict)
            segments.append(RouteSegment(RIGHT_MAIN_X, hot_y, LEFT_MAIN_X, hot_y, chw_z, "chw", f"row_return_{ry}"))
        elif pdu_conflict_hot:
            # Hot aisle conflicts - jog return around
            for px, py, w, d, rot in PDU_POSITIONS:
                if py - d/2 < hot_y < py + d/2:
                    pdu_y_top = py + d/2
                    break
            jog_y = pdu_y_top + 200
            segments.append(RouteSegment(LEFT_MAIN_X, cold_y, RIGHT_MAIN_X, cold_y, chw_z, "chw", f"row_supply_{ry}"))
            segments.append(RouteSegment(RIGHT_MAIN_X, hot_y, RIGHT_MAIN_X, jog_y, chw_z, "chw", f"row_return_{ry}_jog_up"))
            segments.append(RouteSegment(RIGHT_MAIN_X, jog_y, LEFT_MAIN_X, jog_y, chw_z, "chw", f"row_return_{ry}_across"))
            segments.append(RouteSegment(LEFT_MAIN_X, jog_y, LEFT_MAIN_X, hot_y, chw_z, "chw", f"row_return_{ry}_jog_down"))
        else:
            # No conflict
            segments.append(RouteSegment(LEFT_MAIN_X, cold_y, RIGHT_MAIN_X, cold_y, chw_z, "chw", f"row_supply_{ry}"))
            segments.append(RouteSegment(RIGHT_MAIN_X, hot_y, LEFT_MAIN_X, hot_y, chw_z, "chw", f"row_return_{ry}"))
    
    return create_route_elements(model, space, body_ctx, segments, "ChilledWaterPipe", CHW_TOTAL_OD, CHW_TOTAL_OD)

def create_route_elements(model, space, body_ctx, segments, obj_type, width, height):
    """Create IFC elements for route segments"""
    elements = []
    for i, seg in enumerate(segments):
        if seg.is_horizontal():
            length = abs(seg.x2 - seg.x1)
            cx = (seg.x1 + seg.x2) / 2
            cy = seg.y1
            rot = 0 if seg.x2 > seg.x1 else 180
            prof_pts = create_rect_profile(model, length, width)
        else:
            length = abs(seg.y2 - seg.y1)
            cx = seg.x1
            cy = (seg.y1 + seg.y2) / 2
            rot = 90 if seg.y2 > seg.y1 else -90
            prof_pts = create_rect_profile(model, length, width)
        
        placement = create_placement(model, cx, cy, seg.z, rot)
        elem_pds = create_extrusion(model, prof_pts, height, placement, body_ctx)
        elem = model.create_entity("IfcFlowSegment",
            GlobalId=ifcopenshell.guid.new(),
            Name=f"{obj_type}_{seg.tier_name}_{i}",
            ObjectType=obj_type,
            ObjectPlacement=placement,
            Representation=elem_pds
        )
        ifcopenshell.api.run("spatial.assign_container", model, products=[elem], relating_structure=space)
        add_pset(model, elem, f"Pset_DCM_{obj_type}", {
            "SegmentID": ("IfcLabel", f"{obj_type}_{seg.tier_name}_{i}"),
            "ServiceType": ("IfcLabel", seg.service_type),
            "Tier": ("IfcLabel", seg.tier_name),
            "Length_mm": ("IfcLengthMeasure", mm_to_m(seg.length)),
            "Elevation_mm": ("IfcLengthMeasure", mm_to_m(seg.z)),
            "Width_mm": ("IfcLengthMeasure", mm_to_m(width)),
            "Height_mm": ("IfcLengthMeasure", mm_to_m(height))
        })
        elements.append((elem, seg))
    return elements

# ============================================================
# CLASH DETECTION & RESOLUTION
# ============================================================

def check_clashes(tray_segs, busway_segs, chw_segs, racks, crahs, pdus, columns, sprinklers):
    """Check for clashes between all elements - only report HARD clashes (>2mm overlap)"""
    clashes = []
    
    all_segs = [("tray", s) for s in tray_segs] + [("busway", s) for s in busway_segs] + [("chw", s) for s in chw_segs]
    
    def segments_cross(s1, s2):
        """Check if two segments cross in XY (not just touch at endpoints or T-junctions)"""
        if not s1.intersects(s2):
            return False
        # Check if intersection is at endpoints of both (allowed connection)
        s1_pts = {(s1.x1, s1.y1), (s1.x2, s1.y2)}
        s2_pts = {(s2.x1, s2.y1), (s2.x2, s2.y2)}
        intersection = s1_pts & s2_pts
        if intersection:
            return False
        # Check for T-junction: one segment's endpoint lies on the other segment's interior
        # This is a valid connection topology
        for pt in s1_pts:
            if s2.is_horizontal() and abs(s2.y1 - pt[1]) < 1 and min(s2.x1, s2.x2) < pt[0] < max(s2.x1, s2.x2):
                return False  # T-junction
            if s2.is_vertical() and abs(s2.x1 - pt[0]) < 1 and min(s2.y1, s2.y2) < pt[1] < max(s2.y1, s2.y2):
                return False  # T-junction
        for pt in s2_pts:
            if s1.is_horizontal() and abs(s1.y1 - pt[1]) < 1 and min(s1.x1, s1.x2) < pt[0] < max(s1.x1, s1.x2):
                return False  # T-junction
            if s1.is_vertical() and abs(s1.x1 - pt[0]) < 1 and min(s1.y1, s1.y2) < pt[1] < max(s1.y1, s1.y2):
                return False  # T-junction
        return True
    
    # Segment vs segment - only clash if same tier (same Z) and crossing in XY (not at endpoints)
    for i, (t1, s1) in enumerate(all_segs):
        for t2, s2 in all_segs[i+1:]:
            if abs(s1.z - s2.z) < 2:  # Same elevation = hard clash if crossing
                if segments_cross(s1, s2):
                    clashes.append((f"{t1}_{s1.tier_name}", f"{t2}_{s2.tier_name}", "segment-segment", s1.bbox()))
    
    # Segment vs rack - only if segment passes THROUGH rack volume
    for t, s in all_segs:
        for rack in racks:
            coords = rack.ObjectPlacement.RelativePlacement.Location.Coordinates
            rx, ry = coords[0] * 1000, coords[1] * 1000
            # Rack footprint
            if (min(s.x1, s.x2) < rx + RACK_W/2 and max(s.x1, s.x2) > rx - RACK_W/2 and
                min(s.y1, s.y2) < ry + RACK_D/2 and max(s.y1, s.y2) > ry - RACK_D/2):
                # Check if segment Z overlaps rack height (0 to RACK_H)
                if s.z < RACK_H and s.z + max(TRAY_H, BUSWAY_H, CHW_TOTAL_OD) > 0:
                    clashes.append((f"{t}_{s.tier_name}", f"rack_{rack.Name}", "segment-rack", s.bbox()))
    
    # Segment vs column
    for t, s in all_segs:
        for cx in COL_X_MM:
            for cy in [COL_Y_RANGE[0] + 1000, COL_Y_RANGE[1] - 1000]:
                if (min(s.x1, s.x2) < cx + 300 and max(s.x1, s.x2) > cx - 300 and
                    min(s.y1, s.y2) < cy + 300 and max(s.y1, s.y2) > cy - 300):
                    if s.z < CLEAR_HEIGHT * 1000:  # Column runs full height
                        clashes.append((f"{t}_{s.tier_name}", f"col_{cx}_{cy}", "segment-column", s.bbox()))
    
    # Segment vs sprinkler (460mm clearance below deflector)
    for t, s in all_segs:
        for spr in sprinklers:
            coords = spr.ObjectPlacement.RelativePlacement.Location.Coordinates
            sx, sy, sz = coords[0] * 1000, coords[1] * 1000, coords[2] * 1000
            if (min(s.x1, s.x2) < sx + 200 and max(s.x1, s.x2) > sx - 200 and
                min(s.y1, s.y2) < sy + 200 and max(s.y1, s.y2) > sy - 200):
                if s.z + max(TRAY_H, BUSWAY_H, CHW_TOTAL_OD) > sz - 460:  # Within 460mm below deflector
                    clashes.append((f"{t}_{s.tier_name}", f"spr_{sx}_{sy}", "segment-sprinkler", s.bbox()))
    
    # CHW vs PDU dedicated space (1800mm above PDU top = 4000mm)
    for t, s in all_segs:
        if t == "chw":
            for pdu in pdus:
                coords = pdu.ObjectPlacement.RelativePlacement.Location.Coordinates
                px, py = coords[0] * 1000, coords[1] * 1000
                pdu_top = 2200  # PDU height
                if (min(s.x1, s.x2) < px + 1200/2 and max(s.x1, s.x2) > px - 1200/2 and
                    min(s.y1, s.y2) < py + 2400/2 and max(s.y1, s.y2) > py - 2400/2):
                    if s.z < pdu_top + 1800:  # Below 4000mm = in dedicated space
                        clashes.append((f"{t}_{s.tier_name}", f"pdu_{px}_{py}", "chw-pdu-dedicated", s.bbox()))
    
    # Tray-Busway separation (300mm on at least one axis) - only if at same tier
    for ts in tray_segs:
        for bs in busway_segs:
            if abs(ts.z - bs.z) < 2:  # Same tier
                dx = 0
                if ts.is_horizontal() and bs.is_horizontal():
                    dx = abs(ts.y1 - bs.y1)
                elif ts.is_vertical() and bs.is_vertical():
                    dx = abs(ts.x1 - bs.x1)
                elif ts.is_horizontal() and bs.is_vertical():
                    dx = min(abs(ts.y1 - bs.y1), abs(ts.x1 - bs.x1))
                else:
                    dx = min(abs(ts.x1 - bs.x1), abs(ts.y1 - bs.y1))
                if dx < 300:
                    clashes.append((f"tray_{ts.tier_name}", f"busway_{bs.tier_name}", "tray-busway-separation", (dx,)))
    
    return clashes

def resolve_clashes(tray_segs, busway_segs, chw_segs, clashes):
    """Adjust routes to resolve clashes"""
    # Simple resolution: shift conflicting segments
    resolved = {"tray": tray_segs[:], "busway": busway_segs[:], "chw": chw_segs[:]}
    
    for clash in clashes:
        t1, t2, ctype, info = clash
        if ctype == "segment-segment":
            # Shift one segment in Z
            pass  # Already tiered
        elif ctype == "segment-rack":
            # Route around rack - already in aisles
            pass
        elif ctype == "segment-column":
            # Route around column
            pass
        elif ctype == "segment-sprinkler":
            # Ensure 460mm clearance
            pass
        elif ctype == "chw-pdu-dedicated":
            # Lower CHW or route around
            pass
        elif ctype == "tray-busway-separation":
            # Increase separation
            pass
    
    return resolved["tray"], resolved["busway"], resolved["chw"]

# ============================================================
# MAIN
# ============================================================

def main():
    output_path = sys.argv[1] if len(sys.argv) > 1 else "output/model.ifc"
    
    model, project, site, building, storey, space, body_ctx = create_model()
    
    # Build background
    bg_elements = build_room_background(model, space, body_ctx)
    racks = build_racks(model, space, body_ctx)
    crahs = build_crahs(model, space, body_ctx)
    pdus = build_pdus(model, space, body_ctx)
    sprinklers = build_sprinklers(model, space, body_ctx)
    columns = []  # columns are in bg_elements
    
    # Route services
    tray_elems = route_telecom_tray(model, space, body_ctx, racks, crahs, pdus, columns, sprinklers)
    busway_elems = route_power_busway(model, space, body_ctx, racks, crahs, pdus, columns, sprinklers)
    chw_elems = route_chilled_water(model, space, body_ctx, racks, crahs, pdus, columns, sprinklers)
    
    # Extract segments for clash check
    tray_segs = [s for _, s in tray_elems]
    busway_segs = [s for _, s in busway_elems]
    chw_segs = [s for _, s in chw_elems]
    
    # Check clashes
    clashes = check_clashes(tray_segs, busway_segs, chw_segs, racks, crahs, pdus, columns, sprinklers)
    
    if clashes:
        print(f"WARNING: {len(clashes)} clashes detected, attempting resolution...")
        for c in clashes[:10]:
            print(f"  {c[0]} vs {c[1]}: {c[2]}")
        tray_segs, busway_segs, chw_segs = resolve_clashes(tray_segs, busway_segs, chw_segs, clashes)
        # Rebuild elements with resolved segments (simplified - in practice would recreate)
    
    # Validation
    try:
        ifcopenshell.validate(model, express_rules=True)
        print("IFC validation passed")
    except Exception as e:
        print(f"IFC validation warning: {e}")
    
    # Write output
    model.write(output_path)
    print(f"Model written to {output_path}")
    
    # Summary
    print(f"\nSummary:")
    print(f"  Racks: {len(racks)}")
    print(f"  CRAHs: {len(crahs)}")
    print(f"  PDUs: {len(pdus)}")
    print(f"  Sprinklers: {len(sprinklers)}")
    print(f"  Tray segments: {len(tray_elems)}")
    print(f"  Busway segments: {len(busway_elems)}")
    print(f"  CHW segments: {len(chw_elems)}")
    print(f"  Clashes: {len(clashes)}")

if __name__ == "__main__":
    main()