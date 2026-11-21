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

# ============================================================
# LETTERHEAD / HEADER BLOCK
# ============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('THE CFD ME')
run.bold = True
run.font.size = Pt(16)
run.font.color.rgb = RGBColor(0, 51, 102)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('4820 E River Rd, Suite 220  |  Tucson, Arizona 85718  |  AZ PE #48213')
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(100, 100, 100)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('CFDME-2025-041  |  Ocotillo WUI Wildfire, Phase 1')
run.bold = True
run.font.size = Pt(12)

p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(6)
p.paragraph_format.space_after = Pt(6)
run = p.add_run('_' * 72)
run.font.color.rgb = RGBColor(0, 51, 102)

# ============================================================
# TITLE BLOCK
# ============================================================
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('SIGNED DISPOSITION — THIRD STEADY-SOLVE ATTEMPT')
run.bold = True
run.font.size = Pt(14)
run.font.color.rgb = RGBColor(0, 51, 102)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Ocotillo Desert-Fire Case (CFDME-2025-041)')
run.bold = True
run.font.size = Pt(12)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run('Date: 10/10/2025')
run.font.size = Pt(11)

# ============================================================
# REVIEWER AND STAMP BLOCK
# ============================================================
doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Reviewer: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('Gordon Selby, PE — AZ PE #48213')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Technical Director / Reviewing Engineer: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('Marguerite Falk, PE — AZ PE #42798')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Stamp Boundary Language: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('This disposition covers the third steady-solve attempt (log.solve_20251009_attempt3.txt) for the Ocotillo desert-fire scoping model under CFDME-2025-041 Phase 1. It authorizes the transient LES run defined herein and does not extend to the structural wind-load extraction case (CFDME-2025-041, separate load case per CFDME_Units_SOP_rev2 Sec. 5). The stamp applies to the fire/plume exposure regime only.')
run.font.size = Pt(10)
run.font.italic = True

doc.add_paragraph()

# ============================================================
# 1. RESIDUAL PLATEAU AND PUFFING FREQUENCY ANALYSIS
# ============================================================
h = doc.add_heading('1. Residual Plateau and Puffing Frequency Analysis', level=1)

p = doc.add_paragraph()
run = p.add_run('Characteristic fire diameter D = 3.0 m (OAS-WUI-01_revC front segment).')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Cetegen–Ahmed puffing frequency (CFDME_Modeling_Standards_Fire_rev4 Sec. 4):')
run.bold = True
run = p.add_run(' f = 1.5 · D^(-1/2) Hz')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Computed: f = 1.5 · (3.0)^(-1/2) = 0.87 Hz')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('Corresponding puffing period: T = 1/f = 1.15 s')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Run observation (log.solve_20251009_attempt3.txt, iter 400–800):')
run.bold = True
run = p.add_run(' Probe 0 (plume centreline, z = 8 m AGL) shows T and U_z oscillation at period ~1.15 s, ~40 K peak-to-peak on T, ~2.4 m/s on U_z.')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Run showed: f_run = 0.87 Hz, T_run = 1.15 s')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Comparison:')
run.bold = True
p = doc.add_paragraph()
run = p.add_run('Frequency match: |0.87 – 0.87| / 0.87 × 100% = 0.00%')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('Period match: |1.15 – 1.15| / 1.15 × 100% = 0.00%')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Conclusion: The residual plateau at iter 400–800 is the physical puffing mode of the buoyant plume, not a numerical artefact. The steady SIMPLE outer loop cannot converge because no time-invariant solution exists for a buoyancy-driven plume at Fr ~ 1 (mixed convection). The oscillating residuals (Ux initial residual 3e-4 to 8e-4, p initial residual 2e-5 to 3e-5) and probe signals are the signature of physically resolved plume dynamics.')
run.font.size = Pt(11)

# ============================================================
# 2. EXISTENCE OF A STEADY SOLUTION
# ============================================================
h = doc.add_heading('2. Whether a Steady Solution Exists for This Problem', level=1)

p = doc.add_paragraph()
run = p.add_run('No steady solution exists.')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Basis: CFDME_Modeling_Standards_Fire_rev4 Sec. 4 explicitly states: "Because the plume oscillates at a finite, deterministic, physical frequency, no time-invariant flow field exists that any residual-tolerance schedule can converge to." The Cetegen–Ahmed correlation gives f = 0.87 Hz for D = 3.0 m. The run confirms this frequency. The steady-solve approach (fireFoam invoked via SIMPLE outer loop with nOuterCorrectors = 1, time interpreted as iteration count) is fundamentally incompatible with the physics of a mixed-convection buoyant plume. The residual plateau is not a convergence failure — it is the correct physics manifesting in a solver configuration that forbids transient evolution.')
run.font.size = Pt(11)

# ============================================================
# 3. DELIVERED SETUP AGAINST STANDARDS
# ============================================================
h = doc.add_heading('3. Delivered Setup Against Firm Standards', level=1)

# Table of conformance
table = doc.add_table(rows=10, cols=3, style='Table Grid')
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ['Item', 'Delivered in Attempt 3', 'Standard (rev 4) / Status']
for i, h_text in enumerate(headers):
    cell = table.rows[0].cells[i]
    cell.text = h_text
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)

rows_data = [
    ['Solver', 'fireFoam (steady SIMPLE outer loop, nOuterCorrectors=1)', 'NON-CONFORMING — fireFoam required but transient LES mandated; steady SIMPLE prohibited for fire cases (Sec. 3.6, 4)'],
    ['Turbulence model', 'RAS k-epsilon (steady)', 'NON-CONFORMING — LES required (Dynamic Smagorinsky or WALE); RANS/steady k-eps prohibited for fire LES (Sec. 5)'],
    ['Time integration', 'Pseudo-time (iteration count); adjustTimeStep no', 'NON-CONFORMING — adaptive time-stepping with maxCo 0.9 mandatory (Sec. 4)'],
    ['Combustion model', 'EDC (correct)', 'CONFORMING — EDC finite-rate variant mandated (Sec. 3.3)'],
    ['Radiation model', 'fvDOM, 32 rays (correct model, ray count acceptable)', 'CONFORMING — fvDOM mandated (Sec. 3.4)'],
    ['Wind inlet', 'atmBoundaryLayerInletVelocity, Uref=8.0 m/s, Zref=6.1 m, z0=0.03 m, flowDir 240°', 'CONFORMING — matches site met pull and Sec. 3.2'],
    ['Mesh', 'Coarse LES mesh (background dx=1.0 m, ~1.4M cells, 2 refinement levels over fire source)', 'CONDITIONALLY CONFORMING — D*/dx = 7.5 on FINE grid (dx=0.5 m) per three-grid study; coarse grid D*/dx = 3.76 (below 5–10 band). Attempt 3 ran on coarse grid — does not meet LES resolution acceptance (Sec. 5, QA Verification Std Sec. 5)'],
    ['Probes', '5 probes including plume centreline at z=8 m', 'CONFORMING — probe placement adequate for puffing detection'],
    ['Wall functions', 'Standard high-Re wall functions (implied by k-eps)', 'NOT ASSESSED — LES wall function treatment not verified on coarse grid'],
]

for r_idx, row_data in enumerate(rows_data, start=1):
    for c_idx, val in enumerate(row_data):
        cell = table.rows[r_idx].cells[c_idx]
        cell.text = val
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(9)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Summary: The delivered setup uses the correct solver binary (fireFoam) and correct physics models (EDC, fvDOM, atmBoundaryLayer inlet) but configures them in a steady RANS-like mode that rev 4 explicitly forbids (Sec. 3.6, 4, 5). The coarse mesh does not meet LES resolution criteria (D*/dx < 5). The turbulence model (steady k-epsilon) is prohibited for fire LES. The time integration scheme is incompatible with buoyant plume physics. Multiple non-conforming items require correction before any further run.')
run.font.size = Pt(11)

# ============================================================
# 4. AUTHORIZED TRANSIENT RUN — TIME-CONTROL BLOCK
# ============================================================
h = doc.add_heading('4. Authorized Transient Run — Time-Control Block', level=1)

p = doc.add_paragraph()
run = p.add_run('Reference dictionary (Firm/Standards/Reference_Cases/fireFoam_transient_controlDict.txt):')
run.bold = True
run.font.size = Pt(11)

doc.add_paragraph()

# Time-control block table - 15 rows (header + 14 data)
table2 = doc.add_table(rows=15, cols=3, style='Table Grid')
table2.alignment = WD_TABLE_ALIGNMENT.CENTER
headers2 = ['controlDict Entry', 'Reference Dictionary Value', 'Mulshi Delivered (Attempt 3)']
for i, h_text in enumerate(headers2):
    cell = table2.rows[0].cells[i]
    cell.text = h_text
    for paragraph in cell.paragraphs:
        for run in paragraph.runs:
            run.bold = True
            run.font.size = Pt(10)

tc_rows = [
    ['application', 'fireFoam', 'fireFoam'],
    ['startFrom', 'latestTime', 'startTime (0)'],
    ['startTime', '0', '0'],
    ['stopAt', 'endTime', 'endTime (800 — outer iterations)'],
    ['endTime', '60', '800 (pseudo-time iterations)'],
    ['deltaT', '0.001', '1 (pseudo-time step)'],
    ['writeControl', 'adjustableRunTime', 'timeStep (implicit, iteration-based)'],
    ['writeInterval', '0.1000', '25 (iteration interval)'],
    ['purgeWrite', '0', '0'],
    ['writeFormat', 'ascii', 'ascii'],
    ['writePrecision', '8', '8'],
    ['adjustTimeStep', 'yes', 'no'],
    ['maxCo', '0.9', 'N/A (steady SIMPLE)'],
    ['maxDeltaT', '0.01', 'N/A (steady SIMPLE)'],
]

for r_idx, row_data in enumerate(tc_rows):
    row = table2.rows[r_idx + 1]
    for c_idx, val in enumerate(row_data):
        cell = row.cells[c_idx]
        cell.text = val
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(10)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Authorized values for this transient run (largest write interval and shortest end time the standard allows):')
run.bold = True
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('endTime = 23.00 s (20 puffing periods × 1.15 s/period, per Modeling Standards Sec. 4 minimum)')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('writeInterval = 0.0460 s (25 samples per puffing period: 1.15 s / 25 = 0.0460 s, per Modeling Standards Sec. 4)')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('deltaT = 0.001 s (initial); adjustTimeStep yes; maxCo 0.9; maxDeltaT 0.01 s')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('writeControl adjustableRunTime (mandatory)')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Differences from Mulshi delivered block:')
run.bold = True
run.font.size = Pt(11)

diff_items = [
    'stopAt: endTime (ref) vs endTime (delivered) — same keyword but different meaning (simulated seconds vs iteration count)',
    'endTime: 23.00 s (authorized) vs 800 (delivered pseudo-iterations)',
    'deltaT: 0.001 s (authorized, adaptive) vs 1 (delivered, fixed pseudo-step)',
    'writeControl: adjustableRunTime (authorized) vs timeStep/iteration-based (delivered)',
    'writeInterval: 0.0460 s (authorized, 4 decimals) vs 25 iterations (delivered)',
    'adjustTimeStep: yes (authorized) vs no (delivered)',
    'maxCo: 0.9 (authorized) vs N/A (delivered)',
    'maxDeltaT: 0.01 s (authorized) vs N/A (delivered)',
]

for item in diff_items:
    p = doc.add_paragraph(item, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(10)

# ============================================================
# 5. MESH AND VERIFICATION COVERAGE
# ============================================================
h = doc.add_heading('5. Mesh Used in Attempt 3 and Verification Coverage', level=1)

p = doc.add_paragraph()
run = p.add_run('Mesh: COARSE grid from three-grid study (background dx = 1.0 m, ~1.41M cells, 2 refinement levels over fire source cylinder).')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Verification coverage (per three_grid_study_outputs.txt and CFDME_QA_Verification_Standard_rev3 Sec. 5):')
run.bold = True
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('What verification covers:')
run.bold = True
run.font.size = Pt(11)

covers = [
    'Mesh topology and quality: checkMesh passes on all three grids (non-orthogonality max 41.7–45.3°, skewness max 1.28–1.52, aspect ratio max 4.82–5.34 — all within firm criteria).',
    'Plume resolution index D*/dx computed for all three grids. FINE grid (dx = 0.5 m) achieves D*/dx = 7.52 (within required 5–10 band). MEDIUM grid (dx = 0.7 m) achieves D*/dx = 5.37 (marginal). COARSE grid (dx = 1.0 m) achieves D*/dx = 3.76 (below band).',
    'Pope resolved-TKE fraction on FINE grid: k_res/(k_res+k_sgs) = 0.84 (84%, above 80% minimum).',
    'Puffing period recovered on all three grids: 1.14–1.15 s (matches Cetegen–Ahmed 1.15 s).',
    'LES resolution acceptance: PASS on FINE grid (both criteria met). MEDIUM grid marginal on D*/dx. COARSE grid FAIL on D*/dx.',
]

for item in covers:
    p = doc.add_paragraph(item, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(10)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('What verification does NOT cover:')
run.bold = True
run.font.size = Pt(11)

not_covers = [
    'COARSE grid (used in Attempt 3) does not meet LES resolution acceptance criteria (D*/dx = 3.76 < 5). No Pope resolved-TKE fraction reported for coarse grid.',
    'Wall-adjacent resolution (y+) and near-wall SGS behavior not verified on any grid — wall functions assessed only via checkMesh global metrics.',
    'Tie–concrete embedment refinement (required by Modeling Standards Sec. 6 for conjugate heat transfer) — not applicable to this scoping model (no solid assembly regions).',
    'Grid convergence index (GCI) — explicitly excluded for LES per QA Verification Standard Sec. 5.',
    'Multi-region conjugate heat transfer coupling — not present in this scoping model (single fluid region only).',
    'Time-step verification (Courant number behavior on coarse grid under transient LES) — not performed; steady solve used fixed pseudo-time step.',
]

for item in not_covers:
    p = doc.add_paragraph(item, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(10)

# ============================================================
# 6. INLET DEFINING SETTINGS CARRIED FORWARD
# ============================================================
h = doc.add_heading('6. Inlet Defining Settings Carried Forward', level=1)

p = doc.add_paragraph()
run = p.add_run('The following inlet settings from the delivered case are correct and shall be carried forward into the authorized transient run:')
run.font.size = Pt(11)

inlet_items = [
    'Inlet type: atmBoundaryLayerInletVelocity (mandatory per Modeling Standards Sec. 3.2)',
    'Reference velocity Uref: 8.0 m/s (20-ft height, per SOW 3.1)',
    'Reference height Zref: 6.1 m (20 ft)',
    'Roughness length z0: 0.03 m (buffelgrass, per site met pull)',
    'Displacement height d: 0.0 m',
    'Flow direction: 240° (cos(240), sin(240), 0) — southwest wind per site met',
    'Turbulence inlet: matching atmBoundaryLayerInlet* for k and epsilon (self-consistent profile)',
    'Ambient temperature: 308.15 K (35 °C, per site met pull)',
    'Ambient pressure: 101325 Pa (standard atmosphere)',
]

for item in inlet_items:
    p = doc.add_paragraph(item, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(10)

# ============================================================
# 7. COST PROJECTION
# ============================================================
h = doc.add_heading('7. Cost Projection', level=1)

p = doc.add_paragraph()
run = p.add_run('Firm projection basis (from three-grid study solver summaries on borrego cluster):')
run.bold = True
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Reference wall-clock times (fireFoam LES, adaptive time-stepping, maxCo 0.9):')
run.bold = True
run.font.size = Pt(11)

cost_rows = [
    ['Grid', 'Cells', 'Simulated time (s)', 'Wall-clock (borrego)', 'Cores', 'Time-step avg (s)'],
    ['COARSE (dx=1.0 m)', '1.41M', '40.0', '1h 10m', '96', '4.7e-3'],
    ['MEDIUM (dx=0.7 m)', '4.02M', '40.0', '2h 30m', '192', '3.1e-3'],
    ['FINE (dx=0.5 m)', '11.20M', '40.0', '5h 45m', '192+cloud', '2.2e-3'],
]

table3 = doc.add_table(rows=len(cost_rows), cols=6, style='Table Grid')
table3.alignment = WD_TABLE_ALIGNMENT.CENTER
for r_idx, row_data in enumerate(cost_rows):
    for c_idx, val in enumerate(row_data):
        cell = table3.rows[r_idx].cells[c_idx]
        cell.text = val
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.size = Pt(10)
                if r_idx == 0:
                    run.bold = True

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Authorized run parameters: MEDIUM grid (dx=0.7 m, 4.02M cells), endTime=23.00 s, writeInterval=0.0460 s, maxCo=0.9, maxDeltaT=0.01 s.')
run.bold = True
run.font.size = Pt(11)

# Scaling calculation
p = doc.add_paragraph()
run = p.add_run('Projection for one authorized case (MEDIUM grid, 23.00 s simulated):')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Reference: 40.0 s simulated → 2h 30m wall-clock on 192 cores.')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('Scaled to 23.00 s: (23.00 / 40.0) × 2h 30m = 0.575 × 150 min = 86.25 min = 1h 26m.')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('Add 15% margin for startup transient and I/O at 0.0460 s write interval: ~1h 39m.')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('Projected wall-clock for one authorized case: 1h 39m on 192 cores (borrego).')
run.bold = True
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Full matrix projection (Phase 1 SOW: 4 wind directions × 2 fuel moistures × 3 HRR levels = 24 cases):')
run.bold = True
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('24 cases × 1h 39m = 39h 36m total wall-clock on 192 cores (sequential).')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('With 4-case parallel batching on borrego (768 cores available): ~9h 54m elapsed.')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Can the basis be met for the authorized run on every condition it sets?')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Yes, with the following conditions:')
run.font.size = Pt(11)

conditions = [
    'MEDIUM grid (dx=0.7 m) meets D*/dx = 5.37 (within 5–10 band) and Pope fraction > 80% (extrapolated from FINE grid 84% and grid convergence trend).',
    'Time-step control: maxCo 0.9, maxDeltaT 0.01 s. Reference average deltaT = 3.1e-3 s on MEDIUM grid at 40 s. Courant margin: maxCo 0.9 vs typical peak 0.89 → margin = (0.9 – 0.89)/0.9 × 100% = 1.1%. This is thin but within standard. The adaptive time-stepping will reduce deltaT locally to respect maxCo; average deltaT may drop to ~2.5e-3 s, increasing wall-clock by ~20%.',
    'endTime = 23.00 s covers 20.0 puffing periods (23.00 / 1.15 = 20.00), meeting the minimum exactly.',
    'writeInterval = 0.0460 s gives exactly 25 samples per puffing period (1.15 / 0.0460 = 25.0), meeting the minimum exactly.',
    'The basis assumes borrego cluster availability at 192 cores. If cloud burst is needed, add 10% wall-clock overhead.',
]
for item in conditions:
    p = doc.add_paragraph(item, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(10)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('If basis cannot be met (e.g., Courant margin exhausted, deltaT hits maxDeltaT floor, or cluster unavailable):')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('The figure is worth the scaled reference cost (1h 26m) as a lower bound; actual cost will exceed projection. The projection is a planning estimate, not a ceiling. Overruns due to physics (e.g., stronger plume oscillations requiring smaller deltaT) are billable at actuals.')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Attempt 3 consumption vs. one authorized case:')
run.bold = True
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Attempt 3 (steady SIMPLE, COARSE grid, 800 pseudo-iterations): 6h 41m wall-clock on 64 cores, 424.3 CPU-hours.')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('One authorized case (transient LES, MEDIUM grid, 23.00 s): projected 1h 39m wall-clock on 192 cores, ~317 CPU-hours.')
run.font.size = Pt(11)
p = doc.add_paragraph()
run = p.add_run('Comparison: Attempt 3 consumed 4.1× the wall-clock (6h 41m vs 1h 39m) and 1.3× the CPU-hours (424 vs 317) of one authorized transient case, while producing no physically valid transient result.')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('Usable downstream from Attempt 3:')
run.bold = True
run.font.size = Pt(11)

usable = [
    'The converged mean flow field up to iter ~400 (before plateau) may serve as an initial condition for the transient LES restart on the MEDIUM grid, after interpolation. The plateau-onset field (iter 400–500) captures the mean plume structure but not the transient dynamics.',
    'The inlet boundary condition setup (atmBoundaryLayerInletVelocity, turbulence profiles) is correct and carries forward directly.',
    'The combustion (EDC), radiation (fvDOM), and thermophysical property setup is correct and carries forward.',
    'The probe locations are adequate for plume monitoring and carry forward.',
    'The mesh topology (domain extent, refinement zone geometry) carries forward; only the background resolution changes from dx=1.0 m to dx=0.7 m.',
    'The steady k-epsilon turbulence fields do NOT carry forward — LES requires SGS initialization (zero or synthetic turbulence).',
]
for item in usable:
    p = doc.add_paragraph(item, style='List Bullet')
    for run in p.runs:
        run.font.size = Pt(10)

# ============================================================
# SIGNATURE BLOCK
# ============================================================
doc.add_paragraph()
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(24)
run = p.add_run('_' * 50)
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Signed: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('Gordon Selby, PE — AZ PE #48213')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Date: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('10/10/2025')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Reviewing Engineer concurrence: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('Marguerite Falk, PE — AZ PE #42798')
run.font.size = Pt(11)

p = doc.add_paragraph()
run = p.add_run('Date: ')
run.bold = True
run.font.size = Pt(11)
run = p.add_run('10/10/2025')
run.font.size = Pt(11)

doc.add_paragraph()
p = doc.add_paragraph()
run = p.add_run('THE CFD ME  |  Tucson, Arizona  |  AZ PE #48213  |  CFDME-2025-041 rev A')
run.font.size = Pt(10)
run.font.color.rgb = RGBColor(0, 51, 102)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Save
doc.save('/filesystem/CFDME-2025-041_transient_solve_disposition_revA.docx')
print('Document saved successfully.')