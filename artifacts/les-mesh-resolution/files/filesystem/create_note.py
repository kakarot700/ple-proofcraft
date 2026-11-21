from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import datetime

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Title
title = doc.add_heading('CFDME-2025-041 - Resolution Basis Note (rev A)', level=1)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Header info
p = doc.add_paragraph()
p.add_run('Project: ').bold = True
p.add_run('CFDME-2025-041 Ocotillo WUI Wildfire, Phase 1\n')
p.add_run('Deliverable: ').bold = True
p.add_run('Phase 1 Report rev B - Peer Review Checklist Item 4 (Resolution Basis)\n')
p.add_run('Prepared for: ').bold = True
p.add_run('Marguerite Falk, PE - Technical Director & Reviewing Engineer (AZ PE #42798)\n')
p.add_run('Prepared by: ').bold = True
p.add_run('Gordon Selby, PE - Owner & Principal Engineer (AZ PE #48213)\n')
p.add_run('Date: ').bold = True
p.add_run(datetime.date.today().strftime('%m/%d/%Y') + '\n')
p.add_run('Status: ').bold = True
p.add_run('FOR REVIEWER SIGN-OFF - resolves Checklist Item 4\n')

doc.add_paragraph('_' * 72)

# 1. Plume Resolution Index
doc.add_heading('1. Plume Resolution Index - Where It Lands', level=2)

doc.add_paragraph(
    'The three-grid verification study (Case/verification/three_grid_study_outputs.txt, 10/09/2025) '
    'reports the LES resolution assessment per CFDME_QA_Verification_Standard_rev3 Sec 5. '
    'The fine grid (background dx = 0.5 m) is the reporting grid for the six SOW Sec 3.1 wildfire cases.'
)

# Table for key values
table = doc.add_table(rows=7, cols=2, style='Light Shading Accent 1')
table.rows[0].cells[0].text = 'Parameter'
table.rows[0].cells[1].text = 'Value'
data = [
    ('Fire heat release rate (Qdot)', '30.1 MW (from 3.0 m front segment at 10,040 kW/m Byram intensity)'),
    ('Characteristic plume diameter (D*)', '3.76 m (computed per QA Standard Sec 2: D* = (Qdot/(rho_inf*cp*T_inf*sqrt(g)))^(2/5))'),
    ('Reference ambient (standard)', 'rho_inf = 1.204 kg/m3, cp = 1005 J/(kg*K), T_inf = 293.15 K (20 C), g = 9.81 m/s2'),
    ('Fine-grid background cell size (dx)', '0.5 m'),
    ('Plume resolution index (D*/dx)', '7.5 (reported as 7.52 in study; 3.76 / 0.5 = 7.52)'),
    ('Required band (QA Standard Sec 5.1)', '5 <= D*/dx <= 10'),
]
for i, (param, val) in enumerate(data, 1):
    table.rows[i].cells[0].text = param
    table.rows[i].cells[1].text = val

doc.add_paragraph()
p = doc.add_paragraph()
p.add_run('Result: ').bold = True
p.add_run('D*/dx = 7.5 falls within the required 5-10 band. The plume resolution index criterion is MET.')

# 2. Plume Length Scale Behind It
doc.add_heading('2. Plume Length Scale Behind the Index', level=2)

doc.add_paragraph(
    'The characteristic plume diameter D* = 3.76 m is derived from the design fire heat release rate of 30.1 MW, '
    'which itself comes from the Byram fireline-intensity chain evaluated at the site design conditions:'
)

bullets = [
    'Sonoran buffelgrass fuel model: fuel load w = 0.6 kg/m2, heat of combustion h = 18,600 kJ/kg',
    'Rate of spread at design wind: R = 0.9 m/s (Rothermel, from 10-yr Pima County ALERT meteorology)',
    'Byram fireline intensity: I = h*w*R = 10,040 kW/m',
    'LES sub-domain segment length: 3.0 m (fixed at project kickoff, Scoping Memo Sec 5)',
    'Total HRR for sub-domain: Qdot = I x 3.0 m = 30.1 MW',
    'Wind-tilted Byram flame length: L = 0.0775*I^0.46 = 5.4 m (this is a wind-tilted correlation length, not a still-air buoyant flame height)',
]
for b in bullets:
    doc.add_paragraph(b, style='List Bullet')

doc.add_paragraph(
    'The D* = 3.76 m is an axisymmetric-source property (kW total) derived from the 30.1 MW sub-domain source. '
    'The 5.4 m Byram length is a line-source wind-tilted correlation (kW/m); the two are not interchangeable. '
    'The 3.0 m segment is the specific conversion factor between them for this project (Scoping Memo Sec 5.1).'
)

# 3. Band Met?
doc.add_heading('3. Is the Required Band Met?', level=2)

p = doc.add_paragraph()
p.add_run('Yes. ').bold = True
p.add_run(
    'D*/dx = 7.52 (reported as 7.5) lies within the 5-10 band specified in '
    'CFDME_QA_Verification_Standard_rev3 Sec 5.1. The index is not marginal - it sits near the middle of the band.'
)

# 4. Resolution Acceptance Basis
doc.add_heading('4. What the Resolution Acceptance Rests On', level=2)

doc.add_paragraph(
    'Per CFDME_QA_Verification_Standard_rev3 Sec 5, the firm accepts either of two criteria for LES resolution adequacy; '
    'meeting either alone is acceptable, meeting both is preferred. The three-grid study reports both:'
)

table2 = doc.add_table(rows=3, cols=3, style='Light Shading Accent 1')
table2.rows[0].cells[0].text = 'Criterion'
table2.rows[0].cells[1].text = 'Requirement'
table2.rows[0].cells[2].text = 'Result'
table2.rows[1].cells[0].text = 'Plume resolution index (D*/dx)'
table2.rows[1].cells[1].text = '5 <= D*/dx <= 10 (QA Standard Sec 5.1)'
table2.rows[1].cells[2].text = '7.5 - MET'
table2.rows[2].cells[0].text = 'Pope resolved-TKE fraction'
table2.rows[2].cells[1].text = 'k_res/(k_res+k_sgs) >= 0.80 (QA Standard Sec 5.2)'
table2.rows[2].cells[2].text = '0.84 (84%) - MET'

doc.add_paragraph()
doc.add_paragraph(
    'Both criteria are met on the fine grid (dx = 0.5 m). The resolved-TKE fraction of 0.84 was evaluated '
    'at the centreline probe (0.75*D* above the source top surface) over a sampling window of >=20 puffing cycles '
    'at t >= 8 s (three-grid study, LES Resolution Assessment block).'
)

doc.add_paragraph(
    'The verification evidence is the three-grid study outputs file (Case/verification/three_grid_study_outputs.txt), '
    'authored by Renata Ellsworth on 10/09/2025. The LES Resolution Assessment block in that file is the resolution '
    'evidence the QA Standard requires in the Verification section of the report body.'
)

# 5. Decision Needed from Marguerite?
doc.add_heading('5. Does Anything About This Basis Need a Decision from Marguerite?', level=2)

p = doc.add_paragraph()
p.add_run('No. ').bold = True
p.add_run(
    'The resolution basis is fully defined in the firm standards (QA Verification Standard rev 3 Sec 5), '
    'the Scoping Memo (rev A, 10/08/2025, signed by both engineers), and the three-grid study outputs (10/09/2025). '
    'Both acceptance criteria are numerically satisfied on the reporting grid. Nothing about the basis is open, '
    'ambiguous, or subject to engineering judgement - the criteria are pass/fail thresholds with computed values '
    'that exceed them. The only action required is for the Verification section of the Phase 1 Report rev B to '
    'state the required values in the body (Qdot, D*, dx, D*/dx, Pope fraction, probe location, averaging window) '
    'per QA Standard Sec 6, which the current report draft does not yet do (Checklist Item 4 is open for that reason). '
    'Once the Verification section is written to the standard, the item closes on the existing evidence.'
)

# 6. Resolved-Energy Figure Location
doc.add_heading('6. Was the Resolved-Energy Figure Taken Inside the Region the Index Describes?', level=2)

p = doc.add_paragraph()
p.add_run('Yes. ').bold = True
p.add_run(
    'The Pope resolved-TKE fraction (k_res/(k_res+k_sgs) = 0.84) was evaluated at the centreline probe '
    'located at 0.75*D* above the source top surface - i.e., at z approx 2.8 m above the fire source. '
    'This probe location is within the buoyancy-dominated plume region that the D*/dx index describes '
    '(the "region of interest" per QA Standard Sec 5.2: "Point probes shall be located within the buoyancy-dominated '
    'flow, not on the periphery of the domain"). The averaging window covered no fewer than 20 puffing cycles '
    'at t >= 8 s, satisfying the "ten or more puffing cycles" requirement in QA Standard Sec 5.2.'
)

# 7. Ambient Values Represent the Site?
doc.add_heading('7. Do the Ambient Values Behind the Plume Length Scale Represent the Site?', level=2)

doc.add_paragraph(
    'The D* = 3.76 m reported in the three-grid study uses the standard reference-atmosphere conditions '
    '(rho_inf = 1.204 kg/m3, T_inf = 293.15 K = 20 C) per the Scoping Memo Sec 5.1 and the QA Standard Sec 2 definition. '
    'The site design envelope from the 10-year Pima County ALERT record (Avra Valley WUI) is:'
)

bullets_site = [
    'Ambient temperature: 35-42 C (308-315 K) during fire-season daytime hours',
    'Relative humidity: 10-25%',
    '20-ft wind speed: 5-12 m/s',
    'Prevailing hot-hour wind sector: 270 deg (67 of 75 hot hours in record)',
]
for b in bullets_site:
    doc.add_paragraph(b, style='List Bullet')

doc.add_paragraph(
    'Using the site daytime ambient temperature (approx 40 C = 313 K) instead of the standard 20 C (293 K) '
    'reduces D* by approximately 2.6% (D* proportional to T_inf^(-2/5)). At T_inf = 313 K, D* approx 3.64 m, '
    'giving D*/dx approx 7.3. This remains well within the 5-10 band. The standard-atmosphere D* is slightly conservative '
    '(larger D* gives a slightly higher index); the site conditions do not threaten the band.'
)

p = doc.add_paragraph()
p.add_run('Conclusion: ').bold = True
p.add_run(
    'The ambient values used for the reported D* are the standard reference values mandated by the QA Standard '
    'for cross-case comparability. The site\'s actual conditions would lower D* marginally and keep D*/dx '
    'comfortably within the band. No adjustment is required and no decision is needed.'
)

# 8. Can the Item Close?
doc.add_heading('8. Can Checklist Item 4 Close?', level=2)

p = doc.add_paragraph()
p.add_run('Not yet - but only because the Verification section of the report body does not yet state the required values. ').bold = True

doc.add_paragraph(
    'The resolution evidence itself is complete and acceptable:'
)

bullets_close = [
    'D* = 3.76 m (from Qdot = 30.1 MW at standard reference atmosphere)',
    'dx = 0.5 m (fine grid background cell size)',
    'D*/dx = 7.5 - within 5-10 band',
    'Pope resolved-TKE = 84% - above 80% minimum',
    'Probe location: centreline at 0.75*D* above source',
    'Averaging window: >=20 puffing cycles, t >= 8 s',
    'Both criteria MET on the reporting grid',
]
for b in bullets_close:
    doc.add_paragraph(b, style='List Bullet')

doc.add_paragraph(
    'What remains is purely editorial: the Phase 1 Report rev B Verification section (Sec 6) must state these values '
    'directly in the body of the report per CFDME_QA_Verification_Standard_rev3 Sec 6. The current draft places '
    'the three-grid table in Sec 6.1 and the resolution detail in Appendix C, which does not satisfy the standard\'s '
    'requirement that "These values shall appear in the running text or in a table in the Verification section itself. '
    'Placement of any of these values in an appendix, with only a cross-reference in the Verification section, '
    'does not satisfy this standard."'
)

doc.add_paragraph(
    'Once the Verification section is rewritten to include the required values in the body (Qdot, D*, dx, D*/dx, '
    'Pope fraction, probe location, averaging window, and the single-sentence acceptance statement per QA Standard Sec 3(d)), '
    'Checklist Item 4 can close. No new simulations, no new mesh studies, and no new judgements are required - '
    'everything needed is already on the file server.'
)

# 9. What Would Settle It
doc.add_heading('9. What Would Settle Item 4', level=2)

doc.add_paragraph(
    'Edit the Verification section (Sec 6) of CFDME-2025-041_Phase1_report_revB.docx to include, in the body:'
)

bullets_settle = [
    'The fire heat release rate Qdot = 30.1 MW used to compute D*',
    'The characteristic plume diameter D* = 3.76 m',
    'The representative cell edge length dx = 0.5 m in the plume region',
    'The plume resolution index D*/dx = 7.5 (dimensionless)',
    'The Pope resolved-TKE fraction k_res/(k_res+k_sgs) = 0.84 (84%)',
    'The probe location: centreline, 0.75*D* above the source top surface',
    'The averaging window: >=20 puffing cycles at t >= 8 s',
    'A single-sentence acceptance statement, e.g.: '
    '"LES resolution acceptance: PASS on both criteria (D*/dx = 7.5 within 5-10 band; '
    'Pope resolved-TKE = 84% above 80% minimum)."',
]
for b in bullets_settle:
    doc.add_paragraph(b, style='List Bullet')

doc.add_paragraph(
    'After that edit, the Verification section will comply with CFDME_QA_Verification_Standard_rev3 Sec 3 and Sec 6, '
    'and Checklist Item 4 can be marked closed. The three-grid study file in Case/verification/ and the '
    'Scoping Memo remain the underlying evidence; nothing new needs to be run.'
)

# Footer
doc.add_paragraph('_' * 72)
p = doc.add_paragraph()
p.add_run('Prepared by: ').bold = True
p.add_run('Gordon Selby, PE - AZ PE #48213\n')
p.add_run('Owner & Principal Engineer, The CFD ME\n')
p.add_run('Date: ' + datetime.date.today().strftime('%m/%d/%Y') + '\n')
p.add_run('\n')
p.add_run('This note addresses Checklist Item 4 only. Items 2, 3, 5, 6, 7, 9, and 10 remain open per the '
           'peer-review checklist and are not addressed here.')

# Save
output_path = '/filesystem/CFDME-2025-041_resolution_note_revA.docx'
doc.save(output_path)
print(f'Saved to {output_path}')