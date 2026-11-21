from docx import Document
from docx.shared import Inches, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document('/filesystem/Halbray_Backfeed_Reply.docx')

# Find and update the first body paragraph to include ISA number and capacity
# The paragraph after salutation contains the background
for i, p in enumerate(doc.paragraphs):
    if 'We received your letter dated July 9, 2025' in p.text:
        # Update this paragraph to include ISA number and capacity
        new_text = ('We received your letter dated July 9, 2025 requesting a pre-PTO backfeed for '
                    'Halbray Field Solar Site 3 (PXA-2024-0002, ISA-Halbray-Field-Site-3) from feeder ALN-159 '
                    'on July 29, 2025, so that your contractor can run the inverters\' pre-start checks on utility power '
                    'with the generating facility disabled throughout the backfeed. The facility is a 2.3 MW ac (2,300 kW) '
                    'community solar site with four inverter skids. We have reviewed the site\'s records as they stand on '
                    'July 14, 2025. This letter confirms whether we can energize on July 29, 2025, and states the basis.')
        p.clear()
        run = p.add_run(new_text)
        run.font.size = Pt(11)
        break

doc.save('/filesystem/Halbray_Backfeed_Reply.docx')
print('Document updated successfully.')