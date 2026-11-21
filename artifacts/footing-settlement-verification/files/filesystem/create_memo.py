import docx
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

doc = docx.Document()

# Header
header_para = doc.add_paragraph()
header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = header_para.add_run('THELBRIDGE PROJECT MANAGEMENT SERVICES')
run.bold = True
run.font.size = Pt(14)
run.font.name = 'Calibri'

header_para2 = doc.add_paragraph()
header_para2.alignment = WD_ALIGN_PARAGRAPH.CENTER
run2 = header_para2.add_run('500 South High Street, Suite 720, Columbus, OH 43215  |  (614) 555-0125  |  thelbridgepm.com')
run2.font.size = Pt(10)
run2.font.name = 'Calibri'

title_para = doc.add_paragraph()
title_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
run3 = title_para.add_run('VERIFICATION MEMORANDUM')
run3.bold = True
run3.font.size = Pt(14)
run3.font.name = 'Calibri'

doc.add_paragraph()

# To/From/Date/Subject
def add_header_line(label, value):
    p = doc.add_paragraph()
    run_label = p.add_run(label)
    run_label.bold = True
    run_label.font.size = Pt(11)
    run_label.font.name = 'Calibri'
    run_val = p.add_run(value)
    run_val.font.size = Pt(11)
    run_val.font.name = 'Calibri'

add_header_line('To:\t\t', 'Adrian Vance, Project Engineer')
add_header_line('From:\t\t', 'Rahul Nimkar, Geotechnical Reviewer')
add_header_line('Date:\t\t', '07/18/2026')
add_header_line('Subject:\t', 'Verification Register Item 051 - Block C Spread Footings and Long-Term Settlement of Underlying Clay Aquitard (Package A)')

doc.add_paragraph()

# 1. PURPOSE
p = doc.add_paragraph()
run = p.add_run('1. PURPOSE')
run.bold = True
run.font.size = Pt(12)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('This memorandum addresses ').font.size = Pt(11)
run = p.add_run('Verification Register Item 051')
run.bold = True
run.font.size = Pt(11)
p.add_run(' on the Thelbridge Review Comment and Verification Register - Package A (Thelbridge_Verification_Register_PkgA.xlsx, REGISTER sheet, Row 52). Item 051 is assigned to the Geotechnical Reviewer (Rahul Nimkar) and falls due on ').font.size = Pt(11)
run = p.add_run('07/20/2026')
run.bold = True
run.font.size = Pt(11)
p.add_run(', two days before the contractual Level-3 concrete placement hold-point (07/22/2026).').font.size = Pt(11)

p2 = doc.add_paragraph()
p2.add_run('Item 051 covers: ').font.size = Pt(11)
run = p2.add_run('Block C spread footings and the long-term settlement of the clay beneath them')
run.bold = True
run.font.size = Pt(11)

p3 = doc.add_paragraph()
p3.add_run('The purpose of this verification is to determine whether the design, construction monitoring, and observed field performance of the Block C spread footings satisfy the settlement tolerances and geotechnical acceptance criteria for Package A, and whether the long-term consolidation settlement of the underlying normally-consolidated CL clay aquitard (Stratum 2, El. 738.0 to El. 720.0) has been adequately accounted for in the design and monitored in the field such that the Level-3 placement can proceed on 07/22/2026 without risk of exceeding the project settlement tolerances (total settlement <= 1.0 in, differential settlement <= 0.5 in per Spec 31 20 00 Article 3.6).').font.size = Pt(11)

# 2. DOCUMENTS REVIEWED
p = doc.add_paragraph()
run = p.add_run('2. DOCUMENTS REVIEWED')
run.bold = True
run.font.size = Pt(12)
run.font.name = 'Calibri'

docs = [
    '1. Kelbrook Geotechnical, Inc. - Geotechnical Investigation Report, Birchwood Village Expansion Program, Package A, Rev.2, 02/14/2025 (Report No. KGI-2024-0417).',
    '2. Vantree Materials Testing, LLC - Laboratory Consolidation Test Report, ASTM D2435, Report No. VMT-2025-0109-CON, 01/09/2025 (Consolidation_Test_Data_D2435.xlsx). Samples B-06 U3 and B-08 U2.',
    '3. Vantree Materials Testing, LLC - Geotechnical Laboratory Index Test Data, Package A, 01/09/2025 (Geotech_Index_Test_Data.xlsx).',
    '4. Calloway Braddock Structural Engineers, LLC - Design Calculation CB-GEO-007, "Block C Spread Footing Settlement," Rev.0, 09/30/2025 (CB-GEO-007_Settlement_BlockC.xlsx).',
    '5. Calloway Braddock Structural Engineers, LLC - Design Basis Memorandum CB-DBM-001, Rev.2, 11/14/2025 (Design_Basis_Memorandum_Rev2.pdf).',
    '6. Calloway Braddock Structural Engineers, LLC - Foundation Plan, S-101_Foundation_Plan_Rev4.pdf, 05/29/2026; Foundation Sections and Details, S-201_Foundation_Sections_Details_Rev4.pdf, 05/29/2026.',
    '7. Rowan Bay Constructors, Inc. - Settlement Monitoring Records, Block C Spread Footings, Workbook SM-BLKC-2026-Rev14.xlsx, latest reading 06/26/2026 (Settlement_Monitoring_BlockC.xlsx).',
    '8. Specification Section 31 20 00 - Earthwork, Article 3.6 (Settlement Tolerances): total settlement <= 1.0 in, differential settlement <= 0.5 in.',
    '9. Specification Section 03 20 00 - Concrete Reinforcing, Article 3.2 (Clear Cover).',
    '10. Thelbridge Project Management Services - Progress Meeting Minutes No. 26, 07/10/2026 (Progress_Meeting_Minutes_026_20260709.docx).',
    '11. Rachel Marlbeck (Owner) - Verification Directive Email, 07/06/2026 (20260706_Marlbeck_Verification_Directive.eml).',
]

for text in docs:
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    p.paragraph_format.left_indent = Inches(0.25)

# 3. BASIS OF REVIEW
p = doc.add_paragraph()
run = p.add_run('3. BASIS OF REVIEW')
run.bold = True
run.font.size = Pt(12)
run.font.name = 'Calibri'

basis_items = [
    ('Governing Code:', 'Ohio Building Code (2024 edition, adopting IBC 2021 with Ohio amendments), Chapter 16 and ASCE 7-16 for loads and load combinations.'),
    ('Geotechnical Design Parameters:', 'Kelbrook Geotechnical Investigation Report Rev.2 (KGI-2024-0417) and Vantree ASTM D2435 Consolidation Test Report (VMT-2025-0109-CON) for Stratum 2 (CL clay aquitard, El. 738.0 to El. 720.0): H = 18 ft, gamma_t = 120 pcf, Cc = 0.28, Cr = 0.045, e0 = 0.92, sigma\'0 = 1,850 psf, sigma\'p = 1,900 psf, OCR approx 1.03 (normally consolidated), c_v approx 4.4E-4 cm2/s (approx 0.041 ft2/day), double drainage (H_dr = 9 ft).'),
    ('Settlement Tolerances:', 'Specification Section 31 20 00 Article 3.6 - total settlement <= 1.0 in, differential settlement <= 0.5 in. These are the acceptance criteria for verification.'),
    ('Foundation Design:', 'Block C spread footings bear on the upper sand (SP-SM) at underside El. 746.0 ft (top of footing El. 748.0 ft, thickness 2 ft). Allowable bearing pressure 4,000 psf net per S-201 Detail 3/S-201 and Kelbrook report 9.1. Footing sizes vary: interior footings 10.5 ft x 10.5 ft x 36 in; edge footings 9.5 ft x 9.5 ft x 30 in; corner footings 8.5 ft x 8.5 ft x 30 in.'),
    ('Structural Loading:', 'CB-GEO-007 computes stress increases at mid-depth of the clay aquitard from column loads transmitted through the spread footings. The heaviest tributary load is at interior footing FTG-C7 (MP-7).'),
    ('Monitoring Requirements:', 'Thelbridge Verification Register Item 051 requires verification against monitored field performance. Settlement monitoring began 12/12/2025 (baseline) with 15 rounds through 06/26/2026 (SM-BLKC-2026-Rev14.xlsx).'),
    ('Consolidation Time-Rate:', 'With c_v approx 0.041 ft2/day and H_dr = 9 ft, T_v = c_v x t / H_dr2. For 90% primary consolidation (T_v = 0.848), t_90 approx (0.848 x 9^2) / 0.041 approx 1,676 days approx 4.6 years. The monitoring period (12/12/2025 to 06/26/2026 approx 196 days) covers only ~12% of t_90. Primary consolidation is far from complete.'),
    ('Hold-Point:', 'Level-3 concrete placement contractual hold-point is 07/22/2026. Verification must be complete by 07/20/2026 per Owner directive.'),
]

for label, text in basis_items:
    p = doc.add_paragraph()
    run_label = p.add_run(label + ' ')
    run_label.bold = True
    run_label.font.size = Pt(11)
    run_label.font.name = 'Calibri'
    run_text = p.add_run(text)
    run_text.font.size = Pt(11)
    run_text.font.name = 'Calibri'

# 4. FINDINGS
p = doc.add_paragraph()
run = p.add_run('4. FINDINGS')
run.bold = True
run.font.size = Pt(12)
run.font.name = 'Calibri'

# Finding 1
p = doc.add_paragraph()
run = p.add_run('Finding 1 - Design Settlement Prediction (CB-GEO-007) vs. Tolerances')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('CB-GEO-007 (Rev.0, 09/30/2025) computes the long-term consolidation settlement of the CL clay aquitard under the stress increase from Block C spread footing loads. The calculation uses the one-dimensional consolidation equation for normally-consolidated clay:').font.size = Pt(11)

p = doc.add_paragraph()
p.add_run('  S_c = (Cc / (1 + e0)) x H x log10((sigma\'0 + Delta sigma) / sigma\'0)').font.size = Pt(11)
p.runs[-1].font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('Key parameters from CB-GEO-007 and the geotechnical report:').font.size = Pt(11)

finding1_data = [
    ('Cc', '0.28'),
    ('e0', '0.92'),
    ('H', '18 ft = 216 in'),
    ('sigma\'0 (mid-depth of clay at El. 729)', '1,850 psf'),
    ('Delta sigma at mid-clay under FTG-C7 (heaviest interior footing, 10.5 ft x 10.5 ft)', 'approx 420 psf (computed via 2:1 distribution from net bearing pressure approx 4,000 psf at El. 746)'),
    ('sigma\'0 + Delta sigma', '2,270 psf'),
]

for param, val in finding1_data:
    p = doc.add_paragraph()
    run = p.add_run(f'* {param}: {val}')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    p.paragraph_format.left_indent = Inches(0.5)

p = doc.add_paragraph()
p.add_run('Computed settlement at FTG-C7 (MP-7):').font.size = Pt(11)
p = doc.add_paragraph()
p.add_run('  S_c = (0.28 / 1.92) x 216 x log10(2270 / 1850) = 0.1458 x 216 x 0.0885 approx 2.79 in').font.size = Pt(11)
p.runs[-1].font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('This predicted long-term primary consolidation settlement (2.79 in at the worst footing) ').font.size = Pt(11)
run = p.add_run('exceeds the total settlement tolerance of 1.0 in by a factor of 2.8')
run.bold = True
run.font.size = Pt(11)
p.add_run('. Even at the lightest corner footings (FTG-C1, FTG-C4, FTG-C9, FTG-C12), where Delta sigma is lower (~250 psf), the predicted settlement is approximately 1.8 in, still exceeding the 1.0 in tolerance.').font.size = Pt(11)

p = doc.add_paragraph()
p.add_run('Differential settlement between the heaviest interior footing (FTG-C7) and the lightest corner footing (FTG-C12) is predicted at approximately 1.0 in, ').font.size = Pt(11)
run = p.add_run('exceeding the differential tolerance of 0.5 in by a factor of 2.0')
run.bold = True
run.font.size = Pt(11)
p.add_run('.').font.size = Pt(11)

p = doc.add_paragraph()
p.add_run('CB-GEO-007 acknowledges this exceedance and notes that the design relies on the fact that only a fraction of primary consolidation will have occurred by the time the structure is fully loaded, and that the settlement tolerance is intended to apply to the as-built condition at the end of construction, not to the theoretical ultimate primary consolidation. However, the calculation does not explicitly demonstrate that the projected settlement at the Level-3 placement date (07/22/2026) and at substantial completion will remain within tolerances.').font.size = Pt(11)

# Finding 2
p = doc.add_paragraph()
run = p.add_run('Finding 2 - Observed Field Settlement to Date (SM-BLKC-2026-Rev14.xlsx)')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('Settlement monitoring at 12 points (MP-1 through MP-12) began 12/12/2025 (baseline) with the latest reading on 06/26/2026 (Round 15). Cumulative settlements (inches, negative = downward) at Round 15:').font.size = Pt(11)

# Table
table = doc.add_table(rows=14, cols=3, style='Table Grid')
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Monitoring Point', 'Footing', 'Cumulative Settlement (in) at 06/26/2026']
for i, h in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)
            run.font.name = 'Calibri'

data = [
    ('MP-1', 'FTG-C1 (Corner)', '-0.42'),
    ('MP-2', 'FTG-C2 (Edge)', '-0.51'),
    ('MP-3', 'FTG-C3 (Edge)', '-0.38'),
    ('MP-4', 'FTG-C4 (Corner)', '-0.55'),
    ('MP-5', 'FTG-C5 (Edge)', '-0.47'),
    ('MP-6', 'FTG-C6 (Interior)', '-0.58'),
    ('MP-7', 'FTG-C7 (Interior, Heaviest)', '-0.61'),
    ('MP-8', 'FTG-C8 (Edge)', '-0.54'),
    ('MP-9', 'FTG-C9 (Corner)', '-0.44'),
    ('MP-10', 'FTG-C10 (Edge)', '-0.36'),
    ('MP-11', 'FTG-C11 (Edge)', '-0.49'),
    ('MP-12', 'FTG-C12 (Corner)', '-0.31'),
    ('Maximum', 'MP-7 (FTG-C7)', '-0.61'),
]
for row_idx, (mp, ftg, sett) in enumerate(data, 1):
    table.rows[row_idx].cells[0].text = mp
    table.rows[row_idx].cells[1].text = ftg
    table.rows[row_idx].cells[2].text = sett
    for cell in table.rows[row_idx].cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(10)
                run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('Observations:').font.size = Pt(11)
p.runs[-1].bold = True
p.runs[-1].font.name = 'Calibri'

obs_items = [
    'Maximum observed settlement to date is 0.61 in at MP-7 (FTG-C7, interior, heaviest tributary load). This is within the 1.0 in total tolerance but represents 61% of the allowable after only ~12% of the primary consolidation time (t_90 approx 4.6 years).',
    'The round-to-round incremental settlement rate at MP-7 has NOT decreased over the monitoring period. Increments over the last three 14-day intervals: -0.06 in (05/15-05/29), -0.06 in (05/29-06/12), -0.07 in (06/12-06/26). The rate is stable or slightly increasing (approx 0.0043 to 0.0050 in/day), not decelerating as would be expected if primary consolidation were approaching completion.',
    'The settlement vs. time curve (SM-BLKC-2026-Rev14.xlsx, Trend Chart sheet) shows a downward concave curvature with no inflection to concave-up (decelerating) behavior through 06/26/2026. This is consistent with early-stage primary consolidation in a normally-consolidated clay where T_v << 0.848.',
    'Differential settlement between MP-7 (max, -0.61 in) and MP-12 (min, -0.31 in) is currently 0.30 in, within the 0.5 in differential tolerance. However, the differential is widening with each round (Round 1: 0.01 in; Round 8: 0.12 in; Round 15: 0.30 in).',
    'Structure loading during monitoring (per Notes sheet): Block C footings complete 12/2025; Level-1/2 framing 01-02/2026; Level-3 framing, roof steel 03-05/2026; podium slab-on-grade 06/2026. The full dead load from the superstructure is NOT yet applied - Level-3 concrete placement (07/22/2026) and Levels 4-6 remain.',
]

for item in obs_items:
    p = doc.add_paragraph()
    run = p.add_run(f'* {item}')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    p.paragraph_format.left_indent = Inches(0.5)

# Finding 3
p = doc.add_paragraph()
run = p.add_run('Finding 3 - Consolidation Time-Rate Analysis')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('With c_v approx 0.041 ft2/day (from Vantree D2435, both specimens) and H_dr = 9 ft (double drainage, H = 18 ft):').font.size = Pt(11)

time_data = [
    ('t_90 (90% primary consolidation)', 'approx 1,676 days approx 4.6 years'),
    ('Time from baseline (12/12/2025) to Level-3 pour (07/22/2026)', 'approx 222 days - T_v approx 0.112 - U approx 38% (average degree of consolidation)'),
    ('Time from baseline to substantial completion (est. 10/2026)', 'approx 313 days - T_v approx 0.158 - U approx 45%'),
    ('Time to reach 90% consolidation (U = 90%)', 'approx 4.6 years from baseline - mid-2030'),
]

for label, val in time_data:
    p = doc.add_paragraph()
    run = p.add_run(f'* {label}: {val}')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    p.paragraph_format.left_indent = Inches(0.5)

p = doc.add_paragraph()
p.add_run('At the Level-3 pour date (07/22/2026), only ~38% of primary consolidation will have occurred under the current loading. The remaining ~62% of the predicted 2.79 in ultimate settlement (approx 1.73 in) will occur AFTER the Level-3 pour, continuing for years.').font.size = Pt(11)
run = p.add_run(' The settlement tolerance of 1.0 in will be exceeded during the service life of the structure unless mitigation is provided.')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
p.add_run('The current observed settlement (0.61 in at MP-7) is consistent with ~38% of the predicted 2.79 in (0.38 x 2.79 approx 1.06 in). The observed value is somewhat lower, likely because: (a) the full superstructure dead load is not yet applied; (b) the 2:1 stress distribution may overestimate Delta sigma at mid-clay for the larger footings; (c) the clay may have slightly higher c_v or lower Cc in situ than lab specimens. However, the trend is clear: settlement is ongoing, rate is not decreasing, and the full load is not yet applied.').font.size = Pt(11)

# Finding 4
p = doc.add_paragraph()
run = p.add_run('Finding 4 - Design Basis Memorandum and Specification Reconciliation')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('CB-DBM-001 Rev.2 (7.3, 9) states: "Block C is founded on isolated spread footings bearing on the upper sand (SP-SM) above the compressible CL clay layer. Settlement of the clay layer is a serviceability consideration and is checked in CB-GEO-007. Bearing capacity is checked under strength-level combinations; settlement is checked under service-level combinations with tolerances established in Spec 31 20 00 Article 3.6 (total 1.0 in, differential 0.5 in)."').font.size = Pt(11)

p = doc.add_paragraph()
p.add_run('However, CB-GEO-007 does not demonstrate compliance with the 1.0 in / 0.5 in tolerances for the long-term condition. It computes the ultimate primary consolidation settlement (2.79 in max) and notes the exceedance but does not present a time-dependent settlement analysis showing that the tolerance will be met at any defined milestone (Level-3 pour, substantial completion, 1-year, 5-year). The design basis memorandum references the tolerances but the supporting calculation does not close against them.').font.size = Pt(11)

# Finding 5
p = doc.add_paragraph()
run = p.add_run('Finding 5 - Owner Verification Directive and Hold-Point')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('The Owner (Rachel Marlbeck) directive of 07/06/2026 states: "no permanent work on Package A proceeds until Thelbridge has issued a written verification... If any item cannot be verified in time, we would rather delay the pour than release non-conforming work." Item 051 is explicitly listed among the items that must be closed by 07/20/2026.').font.size = Pt(11)

p = doc.add_paragraph()
p.add_run('Progress Meeting Minutes No. 26 (07/10/2026) list Item 051 among "open verification items Items 048-057" for discussion at Meeting No. 27 (07/16/2026). The Level-3 hold-point is 07/22/2026.').font.size = Pt(11)

# 5. CONCLUSION AND RECOMMENDATION
p = doc.add_paragraph()
run = p.add_run('5. CONCLUSION AND RECOMMENDATION')
run.bold = True
run.font.size = Pt(12)
run.font.name = 'Calibri'

p = doc.add_paragraph()
run = p.add_run('DISPOSITION: Item 051 - CANNOT BE VERIFIED AS COMPLIANT')
run.bold = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)
run.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('Based on the review above, the Block C spread footings and the long-term settlement of the underlying clay aquitard ').font.size = Pt(11)
run = p.add_run('do not satisfy')
run.bold = True
run.font.size = Pt(11)
p.add_run(' the verification criteria for the following reasons:').font.size = Pt(11)

reasons = [
    'The predicted ultimate primary consolidation settlement (2.79 in at worst footing) exceeds the total settlement tolerance (1.0 in) by 179% and the differential tolerance (0.5 in) by 100%.',
    'The observed settlement to date (0.61 in at MP-7) is already at 61% of the total tolerance after only ~12% of the consolidation time, with a non-decelerating rate.',
    'At the Level-3 pour date (07/22/2026), only ~38% of primary consolidation will have occurred under current loading; the full superstructure dead load (Levels 3-6) is not yet applied, which will increase Delta sigma and thus the settlement rate and ultimate magnitude.',
    'CB-GEO-007 does not demonstrate that the settlement tolerances will be met at any project milestone (Level-3 pour, substantial completion, or long-term). The design basis memorandum cites the tolerances but the calculation does not close against them.',
    'The Owner has directed that non-conforming work not be released; the Level-3 pour should be delayed until this item is resolved.',
]

for r in reasons:
    p = doc.add_paragraph()
    run = p.add_run(f'* {r}')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    p.paragraph_format.left_indent = Inches(0.5)

p = doc.add_paragraph()
run = p.add_run('REQUIRED ACTIONS TO CLOSE ITEM 051:')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

actions = [
    ('1. Time-Dependent Settlement Analysis (Required from: Gregory Nash, PE - Calloway Braddock Structural Engineers, LLC, Engineer of Record). ', 'CB-GEO-007 must be revised (or a supplementary calculation issued) to present a time-rate consolidation analysis using the c_v values from Vantree D2435 (c_v approx 4.4E-4 cm2/s approx 0.041 ft2/day, H_dr = 9 ft). The analysis must compute settlement at defined milestones: (a) Level-3 pour (07/22/2026), (b) substantial completion (estimated 10/2026), (c) 1 year post-completion, (d) 5 years post-completion, (e) ultimate (t_90). The analysis must use the actual construction loading sequence (footing loads - Level-1/2 framing - Level-3 placement - Levels 4-6 - roof - superimposed dead). The result must demonstrate whether the 1.0 in / 0.5 in tolerances are met at each milestone, or if not, what mitigation is required.'),
    ('2. Settlement Mitigation Design (Required from: Gregory Nash, PE - Calloway Braddock Structural Engineers, LLC, Engineer of Record; coordinated with Alden Roscombe, PE - Kelbrook Geotechnical, Inc.). ', 'If the time-rate analysis confirms that tolerances will be exceeded (which the current data strongly indicates), a mitigation scheme must be designed and approved. Options include but are not limited to: (a) preloading/surcharging the Block C footprint with temporary fill to accelerate consolidation before final construction (schedule impact); (b) wick drains or sand drains to reduce drainage path and accelerate consolidation (requires geotechnical redesign); (c) structural accommodation - design the superstructure (podium, columns, slabs) to tolerate the predicted differential settlement (e.g., articulated joints, flexible connections, increased deflection capacity); (d) deep foundations (piles or piers) to bypass the clay aquitard (major redesign, significant cost/schedule impact); (e) ground improvement (e.g., rigid inclusions, stone columns) to reduce compressibility. The Owner and EOR must select and approve a mitigation approach.'),
    ('3. Updated Monitoring Plan (Required from: Marcus Whitfield - Rowan Bay Constructors, Inc., Superintendent; Dennis Halloran, PLS - Survey Party Chief). ', 'If the Level-3 pour proceeds before mitigation is implemented (not recommended), the settlement monitoring must continue at the current 14-day interval through at least 1 year post-completion, with automatic trigger levels: (a) Alert at 0.75 in total at any point (75% of tolerance); (b) Action at 0.90 in total or 0.40 in differential (90% of tolerance / 80% of differential tolerance); (c) Stop-work at 1.0 in total or 0.5 in differential. The monitoring plan must be formalized in writing and accepted by the Owner\'s Representative.'),
    ('4. Owner Acceptance of Risk (Required from: Rachel Marlbeck - Thornbury State University, Owner). ', 'If the EOR and Geotechnical Consultant conclude that the settlement tolerances cannot be met without mitigation that is impractical within the current schedule, the Owner must formally accept the risk of exceeding the stated tolerances, with a documented basis for the revised acceptance criteria. This would be a deviation from Spec 31 20 00 Article 3.6 and requires Owner sign-off.'),
]

for label, detail in actions:
    p = doc.add_paragraph()
    run_label = p.add_run(label)
    run_label.bold = True
    run_label.font.size = Pt(11)
    run_label.font.name = 'Calibri'
    run_detail = p.add_run(detail)
    run_detail.font.size = Pt(11)
    run_detail.font.name = 'Calibri'

p = doc.add_paragraph()
p.add_run('Until Actions 1 and 2 are complete and accepted by the Owner\'s Representative, Item 051 remains OPEN and the Level-3 concrete placement hold-point (07/22/2026) should not be released.').font.size = Pt(11)
run = p.add_run(' Recommendation: Delay the Level-3 pour.')
run.bold = True
run.font.size = Pt(11)
run.font.color.rgb = RGBColor(0xCC, 0x00, 0x00)

doc.add_paragraph()

# Signature block
p = doc.add_paragraph()
run = p.add_run('Rahul Nimkar')
run.bold = True
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
run = p.add_run('Geotechnical Reviewer')
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
run = p.add_run('Thelbridge Project Management Services - Owner\'s Representative')
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
run = p.add_run('Date: 07/18/2026')
run.font.size = Pt(11)
run.font.name = 'Calibri'

p = doc.add_paragraph()
run = p.add_run('cc: Rachel Marlbeck - Thornbury State University, Office of Capital Programs')
run.font.size = Pt(11)
run.font.name = 'Calibri'

# Save
output_path = '/filesystem/Thelbridge_Verification_Memo_Item051_BlockC.docx'
doc.save(output_path)
print(f'Saved to {output_path}')