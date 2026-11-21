from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = title.add_run('MEMORANDUM')
run.bold = True
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0, 0, 0)

# Header block
header_data = [
    ('TO:', 'Callaway Land Partners \u2014 Garrett Nokes, VP Land Development'),
    ('FROM:', 'Sundial Engineering & Survey \u2014 Jonathan R. Kessler, PE (NV PE No. 14203), Principal-in-Charge'),
    ('DATE:', 'October 31, 2026'),
    ('RE:', 'Desert Sage Ranch Phase 3 \u2014 Emergency Spillway on Sheet C-9: Disposition of Comment G-4 (09/28/2026 Phase 2 Comment Set), Freeboard Dimensioning, Sizing Calculations, Apron Details, and Master Study Amendment Trigger'),
    ('PROJECT:', 'Desert Sage Ranch Phase 3 \u2014 Improvement Plans (IP-26-100288)'),
    ('JOB NO.:', '2201-03'),
]

for label, value in header_data:
    p = doc.add_paragraph()
    run = p.add_run(label + '\t')
    run.bold = True
    run.font.size = Pt(11)
    run = p.add_run(value)
    run.font.size = Pt(11)

# Horizontal line
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(6)
run = p.add_run('_' * 85)
run.font.size = Pt(8)
run.font.color.rgb = RGBColor(128, 128, 128)

# 1. Executive Summary
h = doc.add_heading('1. Executive Summary', level=1)
p = doc.add_paragraph()
p.add_run('This memo responds to the request to evaluate whether the emergency spillway on Sheet C-9 of the Desert Sage Ranch Phase 3 Improvement Plans (first submittal 08/21/2026) holds up against Comment G-4 from the Clark County Public Works Phase 2 first-round comments (letter dated 09/28/2026), the QA/QC checklist, the accepted Master Drainage Study (Revision 1, 02/2022, CCRFCD acceptance 02/28/2022), the Phase 3 storm drain and detention worksheets, and the CCRFCD acceptance letter. ').font.size = Pt(11)
p.add_run('Conclusion: The spillway as drawn does not fully satisfy Comment G-4. Freeboard dimensioning is partially shown but not explicitly called out on the spillway detail; downstream apron details are shown but lack explicit sizing calculations for the design overflow discharge; the spillway section and erosion protection are present but the sizing calculations are not on the sheet. The revisions required to fully address G-4 do not change the Phase 3 detention allocation (6.4 ac-ft), the 100-year WSEL (2,857.91 ft), the spillway crest (2,858.50 ft), or the shared outfall cap (78 cfs), and therefore do not trigger a formal amendment to the accepted Master Drainage Study. The overflow leaving the berm discharges to a downstream open swale in Common-Area Parcel "E" and exits at the Windmill Lane gutter line.').font.size = Pt(11)

# 2. Sources of Record
h = doc.add_heading('2. Sources of Record', level=1)
sources = [
    ('1.', 'Desert Sage Ranch Phase 3 Improvement Plans, Sheets C-1 through C-9, first submittal 08/21/2026 (Design-Drafting/Phase 3/DSR_Ph3_Improvement_Plans_C1-C9.pdf). Sheet C-9 is the primary reference for spillway geometry, basin sections, storage table, and basin notes.'),
    ('2.', 'Clark County Public Works \u2014 Phase 2 First-Round Plan Check Comments, dated 09/28/2022 (Correspondence/Agency/CC-PW_Ph2_Comments_1st_2nd.pdf), Comment G-4: "Sheet C-3: Add cross-lot drainage arrows on Lots 22\u201331 where finish-floor differentials exceed 2.5 ft. Provide swale sections at typical locations and reference the swale detail on Sheet C-8." Note: The Phase 3 first-round comment letter dated 10/09/2026 (Correspondence/Agency/CC-PW_1stReview_Comments_10092026.pdf) contains a separate G-4 specific to Phase 3: "The emergency spillway shown on Sheet C-9 lacks freeboard dimensioning and downstream apron details. Provide sizing calculations, spillway section, and erosion protection consistent with the RFCD Hydrologic Criteria and Drainage Design Manual." This Phase 3 G-4 is the governing comment for this memo.'),
    ('3.', 'Sundial Engineering & Survey \u2014 Phase 3 QA/QC Checklist, dated 08/18/2026 (Design-Drafting/Phase 3/DSR_Ph3_QAQC_Checklist.xlsx), Tab 3 Cross-Reference Check items 27, 28, 29 verifying spillway detail, basin section, and outlet swale section references on C-9.'),
    ('4.', 'Master Drainage Study \u2014 Desert Sage Ranch (140 acres), Revision 1 dated February 2022, accepted by CCRFCD 02/28/2022 (Reports-Studies/DSR_Master_Drainage_Study.pdf). Key sections: Table 4-1 (Phase 3 allocation 6.4 ac-ft), Section 4.4 (allocations fixed at acceptance), Section 5.2 (Q100 <= 78 cfs outfall cap), Section 7.3 (amendment triggers), Appendix D (Phase 3 stage/storage/discharge table including spillway crest at 2,858.50 ft with 41.5 cfs discharge).'),
    ('5.', 'CCRFCD Acceptance Letter, dated 02/28/2022 (Correspondence/Agency/FCD_MDS_Acceptance_Letter.pdf), confirming detention allocations, outfall cap, and amendment procedure.'),
    ('6.', 'Phase 3 Storm Drain HGL Worksheet, dated 07/2026 (Reports-Studies/DSR_Ph3_StormDrain_HGL.xlsx), confirming tailwater at basin outfall = 2,857.91 ft (100-yr WSEL), sensitivity check at spillway crest 2,858.50 ft.'),
    ('7.', 'Phase 3 Hydrology Worksheet, dated 07/2026 (Reports-Studies/DSR_Ph3_Hydrology_Worksheet.xlsx), confirming Phase 3 combined peak inflow at shared basin = 88.4 cfs, sub-basin breakdown per master study Appendix B.'),
    ('8.', 'Phase 3 Preliminary Detention Calculation, dated 09/25/2026 (Reports-Studies/DSR_Ph3_Detention_Calc_prelim.xlsx), internal working file showing routing with composite inflow and multi-stage outlet.'),
    ('9.', 'Phase 2 Comment Response Matrix, dated 11/07/2022 (Correspondence/Agency/DSR_Ph2_Comment_Response_Matrix.xlsx), showing resolution of Phase 2 G-3 (WSEL and freeboard callouts on plan) and G-4 (cross-lot drainage arrows and swale sections).'),
]

for num, text in sources:
    p = doc.add_paragraph(style='List Number')
    run = p.add_run(text)
    run.font.size = Pt(10)

# 3. Question 1
h = doc.add_heading('3. Disposition: Can Comment G-4 (Phase 3) Be Answered with What Is on Sheet C-9 Today?', level=1)

p = doc.add_paragraph()
p.add_run('No. The emergency spillway on Sheet C-9 does not fully satisfy the Phase 3 Comment G-4 (10/09/2026 letter): "The emergency spillway shown on Sheet C-9 lacks freeboard dimensioning and downstream apron details. Provide sizing calculations, spillway section, and erosion protection consistent with the RFCD Hydrologic Criteria and Drainage Design Manual."').font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('What is present on Sheet C-9 (Improvement Plans, 08/21/2026):')
run.bold = True
run.font.size = Pt(11)

items_present = [
    'Spillway geometry in "Detail \u2014 Emergency Spillway (Weir)" on C-9: broad-crested weir over compacted fill on east berm; crest elevation 2,858.50 ft; weir length 20 ft (along berm); weir width 6 ft (flow direction); surface 12" x 18" articulated concrete block over geotextile filter fabric.',
    'Downstream apron: 15 ft x 20 ft grouted rip-rap, D50 = 12", extending from weir toe to natural grade at elevation 2,853.00 ft.',
    'Design overflow discharge note: "flow spreads to downstream open swale in Common-Area Parcel "E" and exits at Windmill Ln. gutter line."',
    'Basin Notes on C-9 state: "Freeboard between the 100-year water surface (2,857.91\') and the top of berm (2,859.20\') is 1.29\', meeting the CCRFCD minimum freeboard requirement of 1.0 foot. Emergency spillway crest set at 2,858.50\', 0.60\' above the 100-year water surface and 0.70\' below the top of berm."',
    'Storage Summary Table on C-9 shows elevation 2,858.50 ft (spillway crest) with cumulative storage 7.12 ac-ft labeled "freeboard reserve" and elevation 2,859.20 ft (top of berm) with 8.02 ac-ft labeled "structural volume."',
    'Cross-Section B-B\' (Transverse, North-South) through basin midpoint shows side slopes, top-of-berm width 195 ft, bottom width 129 ft, but does not explicitly cut through the spillway location on the east berm.',
    'QA/QC Checklist Tab 3 items 27, 28, 29 confirm detail references are internally consistent (weir crest detail on C-9, basin sections on C-9).',
]

for item in items_present:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(10)

p = doc.add_paragraph()
run = p.add_run('What is missing per G-4:')
run.bold = True
run.font.size = Pt(11)

items_missing = [
    'Freeboard dimensioning on the spillway detail itself: The Basin Notes state the freeboard values (1.29 ft top-of-berm, 0.60 ft spillway-crest-above-WSEL, 0.70 ft spillway-crest-below-top-of-berm), but the spillway detail (Detail \u2014 Emergency Spillway) does not dimension these freeboards graphically or with callout leaders on the detail. G-4 explicitly asks for "freeboard dimensioning" on the spillway.',
    'Sizing calculations for the spillway: The detail shows a 20 ft x 6 ft broad-crested weir at crest 2,858.50 ft. The master study Appendix D shows that at elevation 2,858.50 ft (spillway crest), the outflow is 41.5 cfs. However, no weir equation calculation (Q = C*L*H^(3/2)) is shown on the sheet to demonstrate that the 20 ft length and available head (top of berm 2,859.20 ft minus crest 2,858.50 ft = 0.70 ft) can pass the design overflow discharge (which per the master study routing at spillway crest is 41.5 cfs, and for storms exceeding the 100-yr 24-hr could be higher). The note says "Design overflow discharge (routing check under storm exceeding 100-year, 24-hour input)" but no quantitative check is shown.',
    'Spillway section: The detail shows a plan/partial section of the weir block and apron, but a full longitudinal section through the spillway (crest to downstream grade) with elevations, slopes, and erosion protection extents is not provided. Cross-Section B-B\' does not cut the spillway.',
    'Erosion protection details: The apron is called as "15\' x 20\' grouted rip-rap, D50 = 12\"" but no gradation table, thickness, filter fabric specification, toe-down detail, or transition to the downstream swale is shown. The CCRFCD Hydrologic Criteria and Drainage Design Manual (Section 800 and Standard Drawing SD-402 referenced on C-6) requires specific rip-rap sizing based on discharge velocity and Froude number, which is not demonstrated.',
    'Downstream apron details: The apron dimensions are given but the "details" (profile, section, toe, transition) are absent.',
]

for item in items_missing:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(10)

# 4. Question 2
h = doc.add_heading('4. Disposition: Do the Revisions Required to Address G-4 Trigger an Amendment to the Accepted Master Drainage Study?', level=1)

p = doc.add_paragraph()
p.add_run('No. The revisions required to fully address Comment G-4 (adding freeboard dimensioning to the spillway detail, providing weir sizing calculations, adding a spillway longitudinal section, and expanding the apron/erosion protection details) are detailing and documentation changes. They do not alter any of the following fixed parameters established in the accepted Master Drainage Study (Revision 1, 02/2022, CCRFCD acceptance 02/28/2022) and confirmed in the CCRFCD acceptance letter:').font.size = Pt(11)

fixed_params = [
    'Phase 3 detention allocation: 6.4 acre-feet (Master Study Table 4-1; CCRFCD Acceptance Letter p.1; C-9 Storage Summary Table).',
    'Phase 3 tributary area: 40.0 acres at 42% impervious (Master Study Table 3-1, Appendix B-3; Hydrology Worksheet).',
    '100-year, 24-hour design storm depth: 3.18 in. (Master Study Section 3.1; Hydrology Worksheet).',
    '100-year water surface elevation in Phase 3 basin: 2,857.91 ft (Master Study Appendix D; C-9 Storage Table; Storm Drain HGL tailwater).',
    'Emergency spillway crest elevation: 2,858.50 ft (Master Study Appendix D; C-9 Detail and Basin Notes).',
    'Top of berm elevation: 2,859.20 ft (C-9 Basin Notes and Sections).',
    'Freeboard (100-yr WSEL to top of berm): 1.29 ft, exceeding CCRFCD 1.0 ft minimum (C-9 Basin Notes; CCRFCD manual).',
    'Spillway crest above 100-yr WSEL: 0.60 ft (C-9 Basin Notes).',
    'Spillway crest below top of berm: 0.70 ft (C-9 Basin Notes).',
    'Shared outfall cap: Q100 <= 78 cfs for full 140-acre site (Master Study Section 5.2; CCRFCD Acceptance Letter p.2).',
    'Phase 3 combined peak inflow at shared basin: 88.4 cfs (Master Study Appendix C-2; Hydrology Worksheet).',
    'Outlet control orifice: 12" x 18" at invert 2,851.00 ft (C-9 Detail \u2014 Outlet Control Structure).',
    'Basin bottom elevation: 2,851.00 ft (C-9 Storage Table and Sections).',
    'Basin interior side slopes: 4H:1V; exterior berm slopes: 3H:1V (C-9 Sections and Basin Plan).',
    'Basin footprint at top of berm: ~293 ft x 195 ft, ~1.31 acres (C-6 Plan View).',
]

for item in fixed_params:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(10)

p = doc.add_paragraph()
p.add_run('Per Master Study Section 4.4 and Section 7.3, and the CCRFCD Acceptance Letter p.2, an amendment is required only for changes to: detention allocations (Table 4-1), outfall allowance (Section 5), tributary area assumptions, impervious cover assumptions, hydrologic methodology, storage-indication inputs, phase boundaries, detention basin location, or shared outfall discharge cap. None of the G-4 revisions change any of these. The spillway geometry (crest elevation 2,858.50 ft, length 20 ft, width 6 ft) is already set and matches the master study Appendix D stage/storage/discharge table (elevation 2,858.50 ft -> 41.5 cfs outflow). Adding the weir calculation to the sheet merely documents that the as-designed spillway capacity is consistent with the master study routing; it does not change the routing.').font.size = Pt(11)

# 5. Question 3
h = doc.add_heading('5. Spillway Detail and Basin Notes on Sheet C-9 (As Currently Drawn)', level=1)

p = doc.add_paragraph()
run = p.add_run('Spillway Detail \u2014 "Detail \u2014 Emergency Spillway (Weir)" on Sheet C-9:')
run.bold = True
run.font.size = Pt(11)

spillway_detail = [
    'Type: Broad-crested weir over compacted fill on east berm.',
    'Weir crest elevation: 2,858.50 ft (NAVD 88).',
    'Weir length (along berm): 20 ft.',
    'Weir width (flow direction): 6 ft.',
    'Weir surface: 12" x 18" articulated concrete block over geotextile filter fabric.',
    'Downstream apron: 15 ft x 20 ft grouted rip-rap, D50 = 12", extending from weir toe to natural grade at elevation 2,853.00 ft.',
    'Design overflow discharge note: "Design overflow discharge (routing check under storm exceeding 100-year, 24-hour input): flow spreads to downstream open swale in Common-Area Parcel "E" and exits at Windmill Ln. gutter line."',
]

for item in spillway_detail:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(10)

p = doc.add_paragraph()
run = p.add_run('Basin Notes on Sheet C-9 (verbatim relevant excerpts):')
run.bold = True
run.font.size = Pt(11)

basin_notes = [
    '"Detention basin is sized to store the Phase 3 allocation of 6.4 acre-feet between basin bottom (elev. 2,851.00\') and 100-year water surface (elev. 2,857.91\') as tabulated in the Storage Summary Table on this sheet."',
    '"Basin allocation is keyed to the accepted Master Drainage Study \u2014 Desert Sage Ranch (140 acres), Table 4-1, Revision 1 dated February 2022, accepted by the Clark County Regional Flood Control District 02/28/2022."',
    '"Freeboard between the 100-year water surface (2,857.91\') and the top of berm (2,859.20\') is 1.29\', meeting the CCRFCD minimum freeboard requirement of 1.0 foot."',
    '"Emergency spillway crest set at 2,858.50\', 0.60\' above the 100-year water surface and 0.70\' below the top of berm."',
    '"Basin bottom shall be graded to drain to the outlet control structure at a minimum longitudinal slope of 0.5%."',
    '"No standing water within 72 hours of a design event."',
    '"Outlet control orifice sized to attenuate the phase inflow such that the shared outfall discharge for the fully developed 140-acre site remains at or below Q100 = 78 cfs per the master drainage study."',
    '"Basin maintenance, inspection and sediment removal shall be performed by the Desert Sage Ranch HOA in accordance with the approved operations and maintenance manual."',
]

for item in basin_notes:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(10)

# 6. Question 4
h = doc.add_heading('6. Overflow Path Once It Leaves the Berm', level=1)

p = doc.add_paragraph()
p.add_run('Per the spillway detail note on Sheet C-9 and the Basin Plan on Sheet C-6:').font.size = Pt(11)

overflow_path = [
    'Flow overtops the emergency spillway at elevation 2,858.50 ft on the east berm of the detention basin (Common-Area Parcel "E").',
    'Flow passes over the 20 ft x 6 ft articulated concrete block weir and down the 15 ft x 20 ft grouted rip-rap apron (D50 = 12") to natural grade at elevation 2,853.00 ft.',
    'From the apron toe, flow "spreads to downstream open swale in Common-Area Parcel "E"" (C-9 spillway detail note).',
    'The open swale conveys flow south/southwest across Parcel "E" to the Windmill Lane gutter line (C-9 spillway detail note; C-6 Basin Plan shows Parcel "E" adjacent to Windmill Lane on the south side).',
    'At Windmill Lane, flow enters the street gutter and is conveyed west to the existing downstream regional CCRFCD facility via the shared outfall system (the same outfall that receives the basin\'s piped discharge through the 30" RCP outlet at the west end of the basin).',
    'The downstream regional facility is the CCRFCD-maintained facility at the southwest corner of the parent parcel (Master Study Section 2.4; CCRFCD Acceptance Letter). The shared outfall cap of 78 cfs applies to the combined piped + overland discharge at build-out.',
]

for item in overflow_path:
    p = doc.add_paragraph(style='List Number')
    p.add_run(item).font.size = Pt(10)

p = doc.add_paragraph()
p.add_run('Note: The master study Appendix D shows that at the spillway crest elevation (2,858.50 ft), the routed outflow from the basin is 41.5 cfs. This is the discharge that would enter the downstream swale and Windmill Lane gutter during an event exceeding the 100-year, 24-hour design storm. The swale and gutter capacity to convey this overflow without flooding adjacent lots is not explicitly analyzed on the current sheets; this should be verified as part of the G-4 response.').font.size = Pt(11)

# 7. Required Revisions
h = doc.add_heading('7. Required Revisions to Sheet C-9 to Close Comment G-4', level=1)

p = doc.add_paragraph()
p.add_run('The following revisions shall be made to Sheet C-9 and clouded/triangled per Clark County resubmittal protocol:').font.size = Pt(11)

revisions = [
    'Add freeboard dimension leaders and values directly on the "Detail \u2014 Emergency Spillway (Weir)": (a) 100-yr WSEL 2,857.91 ft to spillway crest 2,858.50 ft = 0.60 ft; (b) spillway crest 2,858.50 ft to top of berm 2,859.20 ft = 0.70 ft; (c) 100-yr WSEL 2,857.91 ft to top of berm 2,859.20 ft = 1.29 ft. Label each per CCRFCD minimum 1.0 ft freeboard requirement.',
    'Add a weir sizing calculation block on the sheet (or as a referenced calculation appendix): Q = C*L*H^(3/2). Use C = 2.6\u20133.0 for broad-crested weir (CCRFCD manual); L = 20 ft; H = available head = top of berm (2,859.20) \u2013 crest (2,858.50) = 0.70 ft. Compute Q_capacity = 2.8 * 20 * 0.70^(3/2) = 2.8 * 20 * 0.5857 = 32.8 cfs (using C=2.8). Compare to master study routed outflow at spillway crest = 41.5 cfs. Note: the available head of 0.70 ft yields ~32.8 cfs, which is less than the 41.5 cfs routed outflow at that elevation per the master study. This indicates the spillway as dimensioned (20 ft length, 0.70 ft head to top of berm) may be undersized for the master study\'s routed discharge at the spillway crest. The design must either: (i) increase weir length, (ii) lower crest elevation (reducing freeboard below 0.60 ft above 100-yr WSEL, not recommended), or (iii) demonstrate that the routed 41.5 cfs at elevation 2,858.50 ft includes both orifice and weir flow and the weir alone does not need to pass the full 41.5 cfs at exactly 0.70 ft head. Per master study Appendix D, at elev. 2,857.91 ft (100-yr WSEL) outflow = 27.9 cfs (orifice + weir); at elev. 2,858.50 ft (spillway crest) outflow = 41.5 cfs. The incremental 13.6 cfs is the weir contribution over the 0.59 ft head above 100-yr WSEL. The weir calculation must be consistent with this routing. This calculation must be shown.',
    'Add a longitudinal section through the emergency spillway (Profile: crest -> apron -> downstream swale) showing: crest elevation 2,858.50 ft, weir block thickness, apron slope, apron toe elevation 2,853.00 ft, downstream swale invert and slope, and transition to Windmill Lane gutter.',
    'Expand rip-rap apron detail: specify rip-rap layer thickness (minimum 2xD50 = 24" per CCRFCD SD-402), filter fabric (non-woven, AASHTO M288 Class 2), toe-down depth (minimum 18"), gradation table for D50 = 12", and transition detail to downstream earthen swale (velocity dissipation, scour protection). Reference CCRFCD Standard Drawing SD-402.',
    'Add downstream swale typical section on C-9: bottom width, side slopes, slope, lining (vegetated / rip-rap), and capacity check for 41.5 cfs (or design overflow discharge). Show that swale conveys flow to Windmill Lane gutter without overtopping Parcel "E" boundary.',
    'Add a note referencing the CCRFCD Hydrologic Criteria and Drainage Design Manual section governing emergency spillway design (typically Section 800 or 1100) and Standard Drawing SD-402.',
    'Update the revision block on C-9 (and all affected sheets) with revision triangle, date, and description "Emergency spillway freeboard dimensioning, sizing calculations, and apron details added per CC-PW Comment G-4 (10/09/2026)".',
]

for i, item in enumerate(revisions, 1):
    p = doc.add_paragraph(style='List Number')
    p.add_run(item).font.size = Pt(10)

# 8. Conclusion
h = doc.add_heading('8. Conclusion and Recommendation', level=1)

conclusions = [
    'Comment G-4 (Phase 3, 10/09/2026) cannot be answered with the current Sheet C-9. The spillway detail lacks explicit freeboard dimensioning on the detail, weir sizing calculations, a longitudinal spillway section, and complete erosion protection/apron details.',
    'The revisions required to close G-4 are detailing and documentation changes. They do not alter any fixed parameter of the accepted Master Drainage Study (detention allocation, WSEL, spillway crest, outfall cap, tributary area, impervious cover, phase boundaries). Therefore, no formal amendment to the Master Drainage Study is triggered.',
    'The spillway detail and basin notes on C-9 establish: crest 2,858.50 ft, 20 ft x 6 ft broad-crested weir, articulated concrete block, 15\'x20\' grouted rip-rap apron (D50=12"), freeboard 1.29 ft (top of berm), 0.60 ft (spillway above 100-yr WSEL), 0.70 ft (spillway below top of berm).',
    'Overflow leaving the berm flows across the rip-rap apron to a downstream open swale in Common-Area Parcel "E", then to the Windmill Lane gutter line, and ultimately to the shared outfall and downstream CCRFCD regional facility. The swale and gutter capacity for the design overflow (41.5 cfs per master study at spillway crest) should be verified and documented in the G-4 response.',
    'Recommendation: Direct the drainage lead to implement the seven revisions listed in Section 7 on Sheet C-9, perform the weir capacity check consistent with the master study Appendix D routing, verify downstream swale/gutter capacity, and return a clouded/triangled revised C-9 with the annotated comment matrix for the Phase 3 resubmittal. No Master Drainage Study amendment submittal to CCRFCD is required.',
]

for item in conclusions:
    p = doc.add_paragraph(style='List Bullet')
    p.add_run(item).font.size = Pt(11)

# Signature block
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(24)
run = p.add_run('Respectfully submitted,')
run.font.size = Pt(11)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(36)
run = p.add_run('Jonathan R. Kessler, PE')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Nevada Professional Engineer No. 14203')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Principal-in-Charge, Sundial Engineering & Survey')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('NV COA #C-3874')
run.font.size = Pt(11)

# Save
output_path = '/filesystem/Memo_to_Callaway_Spillway_2026-10-31.docx'
doc.save(output_path)
print(f'Saved to {output_path}')