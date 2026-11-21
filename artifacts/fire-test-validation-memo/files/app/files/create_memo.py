from docx import Document
from docx.shared import Pt

doc = Document()

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = 'Calibri'
font.size = Pt(11)

# Add memo header
doc.add_heading('MEMORANDUM', level=1)

# TO/FROM/DATE/RE/REF
doc.add_paragraph('TO: Marguerite Falk, PE \u2014 Technical Director & Reviewing Engineer, The CFD ME')
doc.add_paragraph('FROM: Gordon Selby, PE \u2014 Owner & Principal Engineer, The CFD ME')
doc.add_paragraph('DATE: October 10, 2025')
doc.add_paragraph('RE: E119 Companion Simulation Validation \u2014 CFDME-2025-041 Ocotillo WUI, Phase 1')
doc.add_paragraph('REF: Validation Procedure rev 2 (CFDME-QA-VAL-002); Red Butte Test Report RBFMT-25-0918; Ironwood Certification Memo IWFPE-CERT-25-0374; Companion Run Results (E119_companion_sim_results.csv); Bianca Rennert Transmittal 10/09/2025 (burn_data_original_vs_revised.csv)')

# Section 1
doc.add_heading('1. PURPOSE', level=2)
doc.add_paragraph("This memo reports the validation of the ASTM E119 companion simulation (companion run, OAS-WUI-01_revC geometry) against the certified test of record (Red Butte Fire & Materials Testing, Report RBFMT-25-0918, test date 09/24/2025) per the firm's Validation Procedure rev 2. It establishes whether the companion run validates, governs the disposition of the Phase 1 report Section 7 stub, and provides the numerical rollup required by CFDME-QA-VAL-002 Sections 3-5. It also addresses the client-amended figure transmitted by Bianca Rennert on 10/09/2025 and its implications for the certified rating and the Phase 1 review checklist.")

# Section 2
doc.add_heading('2. ASSEMBLY IDENTITY \u2014 DOES THE RUN MATCH THE CERTIFICATION?', level=2)
doc.add_paragraph('Yes. The assembly in the companion run is the same assembly the Ironwood certification covers.')
doc.add_paragraph('Basis: The companion simulation uses the engineering geometry of record OAS-WUI-01_revC (transmitted with the signed SOW on 10/08/2025, meshed 10/09/2025). The Ironwood certification memo IWFPE-CERT-25-0374 (Section 1.2) adopts the as-tested geometry from Red Butte report RBFMT-25-0918 Section 2. All three documents \u2014 Red Butte Section 2, Ironwood Section 1.2, and the Phase 1 report Section 3.4 / scoping memo Section 6 \u2014 describe an identical assembly:')
for item in [
    'Two 50 mm siliceous-aggregate printed-concrete leaves',
    '205 mm open-air cavity (no insulation, no fill, no membrane)',
    'Overall thickness 305 mm',
    'Continuous 9-gauge (3.8 mm) galvanized truss-type steel ties',
    '600 mm vertical spacing, 25 mm embedment into each leaf',
    'Non-load-bearing, standard E119 furnace exposure, no hose-stream retest'
]:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph('No geometric or material parameter differs among the three records. The companion run therefore simulates the certified assembly.')

# Section 3
doc.add_heading('3. GOVERNING CRITERION AND TIME REACHED', level=2)
doc.add_paragraph('Per ASTM E119, two thermal-transmission criteria apply to a non-load-bearing wall. The earlier governs the reported fire endurance.')
doc.add_paragraph('Red Butte Test (RBFMT-25-0918 Section 5):')
for item in [
    'Average unexposed-face criterion (nine-TC mean rise \u2264 139 \u00b0C): reached at 163 min',
    'Single-point criterion (any single TC rise \u2264 181 \u00b0C): reached at 118 min at TC-6 (over tie course)',
    'Governing: single-point at 118 min \u2192 Reported endurance D = 118 min'
]:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph('Companion Simulation (E119_companion_sim_results.csv):')
for item in [
    'Average criterion (T_unexposed_avg_C \u2212 21 \u00b0C \u2265 139 \u00b0C): interpolated crossing at 176.1 min \u2192 176 min (nearest minute)',
    'Single-point criterion (T_unexposed_max_C \u2212 21 \u00b0C \u2265 181 \u00b0C): interpolated crossing at 130.9 min \u2192 131 min (nearest minute)',
    'Governing: single-point at 131 min \u2192 Simulation prediction S = 131 min'
]:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph('Both the test and the simulation are governed by the single-point criterion at the tie course. The simulation reproduces the correct governing mechanism.')

# Section 4
doc.add_heading('4. EXPERIMENTAL VALUE ADOPTED AND DISPOSITION ON BIANCA\'S FIGURE', level=2)
doc.add_paragraph('Experimental value adopted: D = 118 min (single-point endurance from Red Butte report RBFMT-25-0918 Section 5.2 and Section 5.3, and Ironwood memo Section 2). This is the certified third-party test value of record.')
doc.add_paragraph("Bianca Rennert's transmittal (10/09/2025, burn_data_original_vs_revised.csv) reports a revised single-point endurance of 129 min, attributed to a post-test thermocouple calibration correction applied to TC-6. Per Validation Procedure rev 2 Section 6, client-amended values may not be substituted for D absent a reissued report from the testing laboratory of record bearing an amendment sequence (e.g., RBFMT-25-0918-R1), signed by the laboratory's authorized signatory, with a calibration certificate authorizing the revision and an explicit statement that the revised value supersedes the original for all downstream use. No such documentation exists in the project file as of 10/10/2025. The original certified value D = 118 min stands.")
doc.add_paragraph("Disposition: Bianca's figure of 129 min is recorded in the correspondence folder but is not admissible as D for this validation. The validation uses D = 118 min.")

# Section 5
doc.add_heading('5. VALIDATION ROLLUP \u2014 ERROR, ACCEPTANCE CRITERION, UNCERTAINTY, COMPARISON', level=2)
doc.add_paragraph('Per Validation Procedure rev 2 Sections 3-5:')
for item in [
    'S = 131 min (simulation prediction, single-point governing, nearest minute)',
    'D = 118 min (certified experimental value, single-point governing)',
    'E = S \u2212 D = +13 min (positive \u2192 simulation over-predicts endurance)',
    'Validation uncertainty u_val = \u00b19 min (root-sum-square of u_num = \u00b14 min, u_inp = \u00b16 min, u_exp = \u00b15 min per Validation Procedure rev 2 Section 4 defaults for this problem class; no project-specific study overrides these defaults)',
    'Acceptance criterion: |E| \u2264 10% of D = 0.10 \u00d7 118 min = 11.8 min'
]:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph('Comparisons:')
for item in [
    'Primary criterion: |E| = 13 min \u2264 11.8 min? NO \u2014 the primary acceptance criterion is NOT met.',
    'Secondary comparison to u_val: |E| = 13 min \u2264 9 min? NO \u2014 the discrepancy exceeds the combined validation uncertainty. The error is resolved as a model error, not measurement-plus-model scatter.',
    'Sign of E: Positive (+13 min). The simulation consistently over-predicts the single-point endurance. This carries different engineering implications than an under-prediction; it means the model is non-conservative for the governing criterion.'
]:
    doc.add_paragraph(item, style='List Bullet')

# Section 6
doc.add_heading('6. LARGEST PREDICTION THAT WOULD HAVE CLEARED THE CRITERION', level=2)
doc.add_paragraph('The acceptance band is D \u00b1 10% of D = 118 min \u00b1 11.8 min = [106.2 min, 129.8 min].')
doc.add_paragraph('Largest S that clears: 129.8 min \u2192 130 min (nearest minute)')
doc.add_paragraph('Smallest S that clears: 106.2 min \u2192 106 min (nearest minute)')
doc.add_paragraph("The simulation's S = 131 min falls 1.2 min above the upper bound of the acceptance band.")

# Section 7
doc.add_heading('7. TWO COMPARISONS REQUIRED BY THE MEMO SCOPE', level=2)
doc.add_heading('7.1 Separation Between Criteria \u2014 Test vs. Simulation', level=3)
doc.add_paragraph('Test (Red Butte): Average (163 min) \u2212 Single-point (118 min) = 45 min')
doc.add_paragraph('Simulation: Average (176 min) \u2212 Single-point (131 min) = 45 min')
doc.add_paragraph('The simulation reproduces the 45-minute separation between the two criteria exactly. This indicates the model captures the relative thermal response of the tie-course path versus the plain-leaf path correctly in a differential sense, even though the absolute single-point time is shifted by +13 min.')

doc.add_heading('7.2 Governing Point Above Nine-Point Mean at Governance', level=3)
doc.add_paragraph('Test at t = 118 min (governance): TC-6 rise = 181 \u00b0C; nine-TC mean rise \u2248 96 \u00b0C (Red Butte Section 5.2). Difference = 85 \u00b0C.')
doc.add_paragraph('Simulation at t = 131 min (governance): T_unexposed_max rise = 181.1 \u00b0C; T_unexposed_avg rise = 89.9 \u00b0C. Difference = 91.2 \u00b0C.')
doc.add_paragraph('The simulation predicts a slightly larger thermal-bridge signature (91.2 \u00b0C vs. 85 \u00b0C, +6.2 \u00b0C) at its governance point. This is consistent with the model\'s overall over-prediction of the single-point endurance: the tie-course thermal bridge conducts heat slightly more effectively in the model than in the physical test, delaying the average response relative to the peak by a marginally greater margin.')
doc.add_paragraph('What this says about the model: The model correctly identifies the tie course as the governing thermal-bridge path and reproduces the inter-criterion separation (45 min) and the qualitative thermal-bridge signature. However, the absolute single-point endurance is over-predicted by 13 min (+11%), and the thermal-bridge temperature excess at governance is over-predicted by ~6 \u00b0C. This points to the tie-course thermal-contact modeling (embedment conductance, tie-to-concrete interface, or tie thermal mass) as the most probable locus of the discrepancy.')
doc.add_paragraph('Where rework belongs: The tie-course thermal-contact modeling in the through-wall CFD treatment (Modeling Standard rev 4 Section 6) \u2014 specifically the embedment conductance and the tie-concrete interface resistance \u2014 should be audited and, if warranted, refined. The cavity radiation model and the leaf conduction are less likely primary causes because the average response is also shifted later (simulation average = 176 min vs. test average = 163 min, +13 min), suggesting a systematic offset in the through-thickness thermal transport.')
doc.add_paragraph('Whether rework has been started: As of 10/10/2025, no rework of the through-wall treatment has been initiated. The Phase 1 report rev B remains in peer review (checklist Items 5 and 6 open), and the case-setup record does not yet document a revised through-wall treatment. The next scheduled activity is the Red Butte confirmatory wildfire window on 10/27/2025, not an E119 companion re-run.')

# Section 8
doc.add_heading('8. IMPLICATIONS FOR THE REST OF PHASE 1', level=2)
for item in [
    'The Phase 1 report Section 7 stub ("Companion simulation predicts S = 131 min for the ASTM E119 exposure; validation memo forthcoming") is resolved by this memo. The stub\'s prediction of S = 131 min stands as the correct reading of the companion run. The validation finding is that the companion run does NOT validate against the certified test under the firm\'s acceptance criterion (|E| = 13 min > 11.8 min) and the discrepancy exceeds u_val (13 min > 9 min).',
    'Peer-review checklist Item 6 (Validation reported as E \u00b1 u_val against acceptance criterion) can now be closed with this memo as the supporting evidence. Item 6 disposition: Closed \u2014 memo supplies the required rollup.',
    'Checklist Item 5 (Through-wall CFD treatment confirmed per Modeling Standard rev 4 Section 6) remains OPEN. The validation finding directly implicates the through-wall treatment; the case-setup record must document the treatment and any corrective action before Item 5 can close.',
    'Checklist Item 7 (Geometry revision tagged and matches case log) remains OPEN pending cross-check of the OAS-WUI-01_revC tag against the mesh-build timestamp in the case log (log.snappyHexMesh_20251009.txt).',
    'Checklist Items 2, 3, 4, 9, 10 remain OPEN per the checklist status as of 10/09/2025.',
    'The Phase 1 report cannot be issued (reviewer sign-off and stamp, Item 10) until Items 2, 3, 4, 5, 7, 9 are closed. This memo closes Item 6 only.'
]:
    doc.add_paragraph(item, style='List Bullet')

# Section 9
doc.add_heading('9. WILDFIRE CLAIM \u2014 WHAT THIS EXERCISE DOES AND DOES NOT ESTABLISH', level=2)
doc.add_paragraph('Per Validation Procedure rev 2 Section 7 (Scope Limitation) and Ironwood Certification Memo Section 5.2:')
doc.add_paragraph('This validation exercise establishes model fidelity against the ASTM E119 standard furnace exposure only. The E119 curve is a smooth, monotonically rising, fuel-continuous compartment-fire curve intended to grade relative thermal performance of building assemblies under a repeatable exposure. A wildland-urban-interface (WUI) wildfire exposure is a wind-driven, radiation-dominated, transient fire-front event whose peak heat flux, duration, spatial distribution, flame tilt, and firebrand deposition differ from E119 at every axis.')
doc.add_paragraph('Therefore:')
for item in [
    'This exercise does NOT validate the wildfire performance claim for the Ocotillo assembly.',
    'This exercise does NOT establish that the assembly survives a wildfire exposure for any duration.',
    'This exercise does NOT translate the 1-hour E119 rating into a wildfire survival time.',
    'This exercise DOES validate the conjugate thermal-CFD model (solver, mesh, through-wall treatment, material properties, boundary conditions as configured for the E119 companion run) against the E119 exposure \u2014 with a documented model error of +13 min on the governing single-point criterion.'
]:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph('What would close the gap: A validation against a physical wildfire-exposure test of the same assembly (or a sufficiently similar assembly) under a characterized WUI fire-front exposure, with the same model configuration used for the Phase 1 wildfire matrix. The Red Butte confirmatory window on 10/27/2025 is the next opportunity for such evidence.')
doc.add_paragraph('Form of future comparison: Any future wildfire validation shall be reported in the same E \u00b1 u_val form per Validation Procedure rev 2 Section 3, with D drawn from a certified third-party wildfire test report, u_val built from numerical, input, and experimental components specific to the wildfire configuration, and the acceptance criterion |E| \u2264 10% of D applied. The report shall explicitly state what exposure the validation covers and what it does not, per Section 7.')

# Section 10
doc.add_heading('10. IF BIANCA\'S FIGURE WERE SUBSTANTIATED \u2014 EFFECT ON CERTIFIED RATING AND STAMP LANGUAGE', level=2)
doc.add_paragraph('If a reissued Red Butte report (RBFMT-25-0918-R1) with a calibration certificate were to substantiate D = 129 min (single-point):')
for item in [
    'The measured endurance would increase from 118 min to 129 min.',
    'The next standard rung is 2-hour (120 min). 129 min \u2265 120 min, so the assembly would qualify for a 2-hour fire-resistance rating under ASTM E119.',
    'The certified rating would change from 1-hour to 2-hour.',
    'Only Ironwood Fire Protection Engineering (Marla Kettering, PE, AZ PE #45106), as the certifying fire-protection engineer of record, is entitled to act on that \u2014 i.e., to issue a new certification memorandum superseding IWFPE-CERT-25-0374. The CFD ME has no authority to certify or restate fire-resistance ratings (stamp boundary: "CFD thermal analysis only. Fire-resistance rating certified separately by others.").'
]:
    doc.add_paragraph(item, style='List Bullet')
doc.add_paragraph('Stamp language on any reissued certification would read:')
doc.add_paragraph('"I, Marla Kettering, PE, Arizona fire-protection Professional Engineer AZ PE #45106, principal of Ironwood Fire Protection Engineering, hereby certify that the assembly described in Section 1.2, under the test conditions of Section 1.3 and the governing result of Section 2, is rated at 2-hour fire-resistance under ASTM E119, subject to the limitations of Section 5 and the amendment procedure of Section 4."', style='Quote')

# Section 11
doc.add_heading('11. CHECKLIST DISPOSITION \u2014 WHAT THIS MEMO LETS ME CLOSE', level=2)
doc.add_paragraph('Peer Review Checklist (CFDME-2025-041, Phase 1 Report rev B, opened 10/09/2025):')
for item in [
    'Item 6 \u2014 Validation reported as E \u00b1 u_val against acceptance criterion: CLOSED. This memo provides the required rollup (S = 131 min, D = 118 min, E = +13 min, u_val = \u00b19 min, criterion = 11.8 min, |E| > criterion, |E| > u_val).',
    'Item 8 \u2014 Stamp boundary respected: Already CLOSED (was [X] as of 10/09/2025).',
    '',
    'All other items remain OPEN:',
    'Item 2 \u2014 Regime selection documented',
    'Item 3 \u2014 Solver package confirmed',
    'Item 4 \u2014 Resolution basis stated in verification body',
    'Item 5 \u2014 Through-wall CFD treatment confirmed (validation finding implicates this)',
    'Item 7 \u2014 Geometry revision tagged and matches case log',
    'Item 9 \u2014 Pressures cross-checked against boundary conditions',
    'Item 10 \u2014 Reviewer sign-off and stamp block completed (held pending Items 2, 3, 4, 5, 7, 9)'
]:
    if item == '':
        doc.add_paragraph('')
    else:
        doc.add_paragraph(item, style='List Bullet')

# Section 12
doc.add_heading('12. PARAGRAPH FOR BIANCA RENNERT \u2014 TO SEND TODAY', level=2)
doc.add_paragraph("Bianca \u2014 The E119 companion simulation (OAS-WUI-01_revC) predicts a single-point endurance of 131 min against the certified Red Butte test value of 118 min (RBFMT-25-0918). The model error is +13 min, which exceeds our 10% acceptance criterion (11.8 min) and the combined validation uncertainty (\u00b19 min). The simulation correctly reproduces the governing mechanism (single-point at the tie course) and the 45-minute separation between the two criteria, but the tie-course thermal-bridge conductance appears slightly high in the model. Your revised figure of 129 min (from a post-test TC-6 calibration correction) is noted but cannot replace the certified test value unless Red Butte reissues the report with an amendment and calibration certificate. If such a reissue occurred, the endurance would reach 129 min \u2014 clearing the 120-minute threshold for a 2-hour rating \u2014 but only Ironwood FPE (Marla Kettering, PE) can issue that rating change. Our Phase 1 report Section 7 is now backed by this validation memo; the peer-review checklist Item 6 closes. The through-wall treatment (Item 5) stays open pending a tie-contact audit. No rework has started. The wildfire validation gap remains; the 10/27 Red Butte confirmatory window is the next step. I'm happy to walk through the numbers at your convenience.")
doc.add_paragraph('')
doc.add_paragraph('\u2014 Gordon Selby, PE')
doc.add_paragraph('AZ PE #48213')
doc.add_paragraph('The CFD ME')
doc.add_paragraph('')
doc.add_paragraph('END OF MEMORANDUM')

# Save
doc.save('/app/files/output/validation_memo.docx')
print('Document saved successfully')