from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Margins
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

# Letterhead
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.LEFT
run = p.add_run('ALLENIOM UTILITIES \u2014 DER PROGRAM OFFICE')
run.bold = True
run.font.size = Pt(12)

p = doc.add_paragraph()
run = p.add_run('4200 Veldmere Boulevard, Halston, Alleron 01HA')
run.font.size = Pt(10)

p = doc.add_paragraph()
run = p.add_run('(612) 555-0100 \u00b7 alleniom.com')
run.font.size = Pt(10)

# Date
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
run = p.add_run('July 14, 2025')
run.font.size = Pt(11)

# Addressee
p = doc.add_paragraph()
run = p.add_run('Ms. Imogen Strathe')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Project Manager')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Halbray Community Solar LP')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('6120 Halbray Road')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Kelloway Township, Alleron 07KT')
run.font.size = Pt(11)

# Reference line
p = doc.add_paragraph()
p.space_before = Pt(12)
run = p.add_run('Re: Pre-PTO Backfeed Request \u2014 Halbray Field Solar Site 3 (PXA-2024-0002), Feeder ALN-159')
run.bold = True
run.font.size = Pt(11)

# Salutation
p = doc.add_paragraph()
p.space_before = Pt(12)
run = p.add_run('Dear Ms. Strathe,')
run.font.size = Pt(11)

# Body paragraphs
paragraphs = [
    'We received your letter dated July 9, 2025 requesting a pre-PTO backfeed for Halbray Field Solar Site 3 (PXA-2024-0002) from feeder ALN-159 on July 29, 2025, so that your contractor can run the inverters\u2019 pre-start checks on utility power with the generating facility disabled throughout the backfeed. We have reviewed the site\u2019s records as they stand on July 14, 2025. This letter confirms whether we can energize on July 29, 2025, and states the basis.',

    'Short answer: No, we cannot energize on July 29, 2025. The following conditions on the record stand in the way:',

    '1. Kelloway Township final electrical inspection (permit EP-25-0418) \u2014 not yet completed\n   Basis: Permit EP-25-0418, issued May 12, 2025 by Kelloway Township Building Department, states: "No permitted work shall be energized before final approval." The final inspection is booked for July 24, 2025. If the inspection passes on that date, this condition is satisfied before July 29, 2025. If it does not pass, or if the inspection is delayed, energization cannot proceed until the Township grants final approval. Action required: Tamsworth Electrical Constructors Inc. (permit holder, Alleron Electrical Contractor Lic. #EC-11847) must obtain final approval from Kelloway Township Building Department (Inspector Graham Telford) on or before July 24, 2025.',

    '2. Utility-owned RTU and SCADA telemetry \u2014 not yet confirmed live at SCADA for backfeed date\n   Basis: TCS-02 \u00a75 requires that for in-scope DER sites (\u2265500 kW), the utility-owned RTU must be physically installed, configured, and end-to-end commissioned per \u00a73.6, communicating over an approved transport at the required refresh cadence, and presenting all required data points as valid at the SCADA operator display before Permission to Operate (PTO) can be issued. The commissioning checklist (CX-HB-03, Rev 0, dated 07/14/2025) shows: "Utility RTU installed and end-to-end point-to-point test \u2014 Accepted by SCADA/EMS Engineering (Marcus Deele), 07/02/2025." This indicates the RTU is installed and the point-to-point test is accepted. However, the SOC PTO-Hold Log (DER-EQP-SOC-PTOH, Rev \u2014, dated 07/14/2025) confirms that TCS-02 \u00a75 contains no interim provision for pre-PTO backfeed: live telemetry is required at the moment PTO is requested. A backfeed is not PTO, but the same telemetry infrastructure is the utility\u2019s means of observing the site during any energized condition. If the RTU end-to-end commissioning is complete and the telemetry is live at SCADA on July 29, 2025, this condition is satisfied. Action required: SCADA/EMS Engineering (Marcus Deele) must confirm that the RTU is fully commissioned end-to-end per TCS-02 \u00a73.6 and that live telemetry is presenting at SCADA on July 29, 2025.',

    '3. POI recloser site acceptance (DPS-07 \u00a76.2) \u2014 complete and accepted\n   Basis: The commissioning checklist shows "POI recloser site acceptance, items 1 to 7 \u2014 Complete and accepted in writing by Distribution Protection Engineering (N. Achterberg, P.E.), 07/07/2025." This condition is satisfied.',

    '4. Revenue meter RM-0002 \u2014 set by Alleniom Metering on July 8, 2025\n   Basis: The commissioning checklist shows "Revenue meter RM-0002 \u2014 Set by Alleniom Metering, 07/08/2025." This condition is satisfied.',

    '5. Inverter Certified Equipment List (CEL) check \u2014 satisfied\n   Basis: The site uses eight (8) Nordreem NG-XT-225 and four (4) NG-XT-125 string inverters. Both models are listed in the body of the current CEL-2025-Q2 (published 04/30/2025, effective 04/30/2025): NG-XT-125 (125 kW, UL 1741-SB, effective 08/26/2024) and NG-XT-225 (225 kW, UL 1741-SB, effective 12/16/2024). Per ENG-PRC-014 \u00a74.1, this makes the site waiver-eligible for the witness test. The commissioning checklist notes "Inverter CEL check \u2014 NG-XT-225 (8) and NG-XT-125 (4) located in the body of CEL-2025-Q2." This condition is satisfied for waiver eligibility.',

    '6. Witness test determination \u2014 not required for backfeed; required at PTO request\n   Basis: ENG-PRC-014 \u00a74.1 states the witness test determination is made "At the permission-to-operate request." A pre-PTO backfeed is not PTO. The ISA pre-PTO backfeed term provides that during a backfeed the generating facility stays disabled and does not operate in parallel. This condition does not block the backfeed.',

    '7. Distribution Operations switching order \u2014 required but not yet issued\n   Basis: The ISA pre-PTO backfeed term states: "Distribution Operations performs the switching for a backfeed under its own switching order." No switching order is on file as of July 14, 2025. Action required: Distribution Operations must issue a switching order for the backfeed before July 29, 2025.',

    'Summary: The Kelloway Township final inspection (booked July 24) and the Distribution Operations switching order (not yet issued) are the two items that must be completed before July 29, 2025 for the backfeed to proceed. The RTU/telemetry condition (TCS-02 \u00a75) must also be live at SCADA on the backfeed date; SCADA/EMS Engineering should confirm this. All other commissioning items on the checklist are complete or satisfied.',

    'If the Township final inspection passes on July 24, 2025, and Distribution Operations issues a switching order, and SCADA/EMS Engineering confirms live telemetry at SCADA on July 29, 2025, we can energize on July 29, 2025. If any of these three conditions is not met, we cannot energize on that date.',

    'Please let us know if you have questions. We will confirm the backfeed date once the switching order is issued and the Township inspection result is known.'
]

for text in paragraphs:
    p = doc.add_paragraph()
    p.space_after = Pt(6)
    run = p.add_run(text)
    run.font.size = Pt(11)

# Closing
p = doc.add_paragraph()
p.space_before = Pt(12)
run = p.add_run('Sincerely,')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Commissioning, DER Program Office')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Alleniom Utilities')
run.font.size = Pt(11)

# cc line
p = doc.add_paragraph()
p.space_before = Pt(12)
run = p.add_run('cc:')
run.bold = True
run.font.size = Pt(10)

cc_items = [
    'Marcus Deele, SCADA/EMS Engineering',
    'N. Achterberg, P.E., Distribution Protection Engineering',
    'Distribution Operations',
    'Meera Vellanki, Interconnection Studies (queue position)',
    'Interconnection Studies (system impact study and conditions)',
    'S. Rennick, Commissioning Coordinator'
]
for item in cc_items:
    p = doc.add_paragraph()
    p.space_after = Pt(2)
    run = p.add_run(item)
    run.font.size = Pt(10)

doc.save('/filesystem/Halbray_Backfeed_Reply.docx')
print('Document saved successfully.')