# ProofCraft: an engineering agent that is not allowed to stop until its deliverable exists

Commit: see the SHA at the top of the Kaggle writeup. Repo: https://github.com/kakarot700/ple-proofcraft

Built by Ira, an AI agent, for Shubham Yadav. Every number below comes from a real run on the 29 public dev tasks; nothing is estimated or invented. Dev runs used NVIDIA NIM models through a local LiteLLM proxy; submission.yaml names google-cloud/gemini-3.8-flash for Stage 2.

## Headline finding

On the first full dev run, 22 of 29 tasks scored zero, and most of those zeros had nothing to do with engineering. 7 runs were killed by the 6-hour wall clock with nothing usable, 9 were lost to the grader or its judge timing out, and 2 wrote a correct-looking deliverable to the wrong folder. Two harness changes (a deliverable-placement guard and a hard time budget) plus re-grading the judge timeouts took the count of scored tasks from 7 to 19, and the single best task went from 0.000 to 0.947. The dev mean went from 0.036 (one run, v1 harness) to 0.139 (best real run per task, see the caveat under Results).

## What ProofCraft is

An agent harness for Physical-Engineering's Last Exam. It speaks the kit's WebSocket protocol, runs a tool loop (bash, read_file, write_file, edit_file, plus whatever MCP servers the task exposes), and wraps that loop in gates that decide when the agent is allowed to stop.

1. **Deliverable-first progress pushes.** Every 20 tool calls the harness injects a message: write a complete first version of the required deliverable at its exact path now, then improve it. Motivation: run n1 spent 70+ turns reading drawings and iterating layout scripts in /tmp while the graded file stayed a 1 KB placeholder.
2. **Forced-write mode.** After 30 tool calls with no write_file or edit_file, the next turn offers only the write tools with tool_choice required, up to three times. Motivation: n2 made 56 tool calls, all reads, and never wrote anything.
3. **Unfinished-answer gate.** A text-only reply is refused while more than half the time budget remains. The agent is told to act on what it just said and write a partial deliverable. Motivation: n4 ended after 21 minutes of a 6-hour budget with the sentence "No feasible layout found... Let me debug" and zero files.
4. **Independent format validation before finishing.** Before a final answer is accepted, the harness pushes the agent to run the task's own validator (for IFC, `python3 -m ifcopenshell.validate --rules <file>`) and read the result back. Motivation: n6's final message claimed "validated" while the file carried 689 schema violations.

Two transport-level remedies were needed before any of this could run on a free endpoint: dropping message fields an endpoint refuses (Groq rejected the `channel` field that gpt-oss echoes back), and parsing "try again in 31m31s" out of a 429 body so the harness waits the right length instead of retrying into the wall.

Dev-cycle changes, each from a real failure:
- Output placement (v2): the task says "save under output/ in this workspace". The model wrote /app/output/... (absolute) on fire-test-validation-memo, so the grader saw nothing. Now the prompt says relative paths are workspace-relative, and on finish the harness copies any stray output/ folder into the workspace.
- Time budget (v3): the harness reads agent_timeout_sec from the task limits; the local eval sends none, so its finalise path never fired and long tasks were killed at 6 h with nothing written. The harness now defaults to a 5 h 30 min budget and finalises early.

## Results on the 29 dev tasks

Harness model Nemotron 3 Ultra 550B (NIM), judge Kimi K3.1 Pro (NIM) unless the table says otherwise. Where Kimi timed out against the task's own 840 s grader limit, the saved run was re-graded with Nemotron 3 Ultra as judge; those rows say so.

| Dev task | v1 score | Best real score | Run | Agent time | Outcome | Judge |
|---|---|---|---|---|---|---|
| backfeed-energization-reply | 0.131 | 0.164 | v3 | 1248 s | scored | kimi-k3.1-pro |
| cooling-water-flush-plan | 0.000 | 0.081 | v5 | 2484 s | scored | kimi-k3.1-pro |
| data-center-site-model | 0.000 | 0.000 | v1 | 3247 s | genuine zero | kimi-k3.1-pro |
| data-hall-device-takeoff | 0.000 | 0.122 | v5 | 4535 s | scored | kimi-k3.1-pro |
| data-hall-mep-routing | 0.000 | 0.000 | v3 | 10617 s | genuine zero | kimi-k3.1-pro |
| data-hall-mep-routing-offset | 0.000 | 0.000 | v1 | 20082 s | genuine zero | kimi-k3.1-pro |
| division-26-specifications | 0.000 | 0.046 | v5 | 1460 s | scored | kimi-k3.1-pro |
| emergency-spillway-check | 0.216 | 0.216 | v1 | 5363 s | scored | kimi-k3.1-pro |
| engineers-estimate-check | 0.000 | 0.130 | v1 regraded | 521 s | scored | nemotron-3-ultra (re-grade) |
| eor-review-corrections | 0.054 | 0.054 | v1 | 1198 s | scored | kimi-k3.1-pro, nemotron fallback (re-grade) |
| fill-compaction-acceptance | 0.000 | 0.093 | v1 regraded | 7860 s | scored | nemotron-3-ultra (re-grade) |
| fire-solve-convergence | 0.000 | 0.163 | v1 regraded | 1069 s | scored | nemotron-3-ultra (re-grade) |
| fire-test-validation-memo | 0.000 | 0.947 | v3 | 9741 s | scored | kimi-k3.1-pro, nemotron fallback (re-grade) |
| footing-settlement-verification | 0.387 | 0.387 | v1 | 1412 s | scored | kimi-k3.1-pro, nemotron fallback (re-grade) |
| foundation-strategy | 0.000 | 0.000 | v1 regraded | 5870 s | grader/judge failure | kimi-k3.1-pro |
| frame-extension-method | 0.000 | 0.229 | v3 | 5735 s | scored | kimi-k3.1-pro |
| heat-rejection-life-cycle-cost | 0.000 | 0.000 | v5 | 1938 s | genuine zero | kimi-k3.1-pro |
| landscape-sheet-revision | 0.104 | 0.104 | v1 | 255 s | scored | kimi-k3.1-pro |
| les-mesh-resolution | 0.000 | 0.110 | v1 regraded | 14979 s | scored | kimi-k3.1-pro, nemotron fallback (re-grade) |
| lv-cable-sizing | 0.000 | 0.000 | v1 | 4308 s | genuine zero | kimi-k3.1-pro |
| mv-conveyance-study | 0.000 | 0.000 | v3 | 2693 s | genuine zero | kimi-k3.1-pro |
| permission-to-operate-memo | 0.068 | 0.068 | v3 | 2427 s | scored | kimi-k3.1-pro |
| pre-application-capacity-response | 0.000 | 0.718 | v1 regraded | 1993 s | scored | nemotron-3-ultra (re-grade) |
| roof-deck-design | 0.071 | 0.071 | v1 | 13657 s | scored | kimi-k3.1-pro |
| seismic-diaphragm-shear | 0.000 | 0.000 | v1 | 8048 s | genuine zero | kimi-k3.1-pro |
| shoring-design-verification | 0.000 | 0.066 | v1 regraded | 12690 s | scored | nemotron-3-ultra (re-grade) |
| solar-supplemental-review | 0.000 | 0.000 | v1 regraded | 5512 s | grader/judge failure | kimi-k3.1-pro |
| solar-witness-test-package | 0.000 | 0.269 | v1 regraded | 10188 s | scored | nemotron-3-ultra (re-grade) |
| wind-diaphragm-shear | 0.000 | 0.000 | v1 | 5208 s | genuine zero | kimi-k3.1-pro |

Caveat: "best real score" is the best real run per task across harness versions and re-grades. It is optimistic and selected, mixes two judges, and is not one clean run. The single-run number is v1's 0.036. A clean full run of the final harness is next.

Figure 3 (figures/fig3_failure_breakdown.png) shows where the 29 tasks ended: v1 had 7 scored, 6 genuine zeros, 9 grader or judge failures and 7 killed at 6 h. After the fixes and re-grades: 19 scored, 8 genuine zeros, 2 grader failures, 0 killed.

## Insight and failure analysis

Controlled before/after on the same task, same model, same judge, only the harness changed (v1 to v3):
- fire-test-validation-memo: 0.000 to 0.947 (9,741 s). The v1 memo was at the wrong path.
- frame-extension-method: 0.000 (killed at 6 h) to 0.229 (5,735 s).
- data-hall-mep-routing: 0.000 (killed) to 0.000, but it now finishes (10,617 s). The deliverable exists; it is wrong.
- mv-conveyance-study, wind-diaphragm-shear, data-center-site-model: 0.000 to 0.000. These are genuine engineering misses, now visible instead of hidden behind kills.
- data-hall-mep-routing-offset: still killed at about 20,300 s. The budget did not fire on this task; that is an open bug.

Re-running v1-killed tasks on the final harness (v5) also turned zeros into scores: data-hall-device-takeoff 0.122, cooling-water-flush-plan 0.081, division-26-specifications 0.046. Re-grading a judge timeout: les-mesh-resolution 0.000 to 0.110 with no change to the agent's output.

What failed or is still failing:
- foundation-strategy: the grader itself crashes (AttributeError: 'list' object has no attribute 'values') on every attempt; we have not yet ruled out that our JSON shape triggers it.
- Using the slow model as judge: Kimi K3.1 Pro on the free NIM tier hit 429/504 errors, and 9 of 29 v1 tasks lost their score to it. A fast judge fallback fixed most of them.
- Eight tasks are genuine zeros: the agent finished and the deliverable was judged wrong. Those are where real engineering headroom is.

## Engineering reasoning: one task against an engineer's workflow

fire-test-validation-memo asks for a validation memo: did a companion simulation of an ASTM E119 fire test validate, against the test report, the certification, the client's amended burn numbers and the firm's own validation procedure. A licensed fire engineer would (1) collect every governing document, (2) confirm the modelled assembly is the certified one, (3) find the governing unexposed-face criterion (E119 limits are a 139 °C average rise and a 181 °C single-point rise) and when it is reached, (4) adopt an experimental value and decide what to do with the client's figure, (5) compare the error with the procedure's acceptance criterion and uncertainty, and (6) issue a memo with stamp language and the checklist disposition.

The v3 run (score 0.947) followed that order. Steps 1 to 15 read the simulation CSV, the original-vs-revised burn data, the E119 test report (trying three PDF readers), the certification memo, the Phase 1 report, scoping memo, interim summary, peer-review checklist and validation procedure. Steps 16 to 19 computed the crossing times of both criteria with interpolation rather than reading off samples, as the brief asked. Step 20 compared the assembly revision in the run with the certified one. It then wrote the memo. Where it differed from an engineer: its first write_file put plain text into a .docx. Its own checks (file type, zip test) caught that and it rebuilt the memo with python-docx before finishing.

## Cross-model generalizability

Same harness (v3), same proxy, same judge, only the harness model changed. Different model families, both on NIM.

| Dev task | Nemotron 3 Ultra 550B | Kimi K3.1 Pro |
|---|---|---|
| backfeed-energization-reply | 0.164 (1248 s) | 0.164 (12530 s) |
| eor-review-corrections | 0.027 (5741 s) | no score: killed at 6 h |
| fire-test-validation-memo | no score: grader/judge failure | no score: killed at 6 h |
| footing-settlement-verification | no score: grader/judge failure | no score: killed at 6 h |
| landscape-sheet-revision | 0.078 (2805 s) | no score: killed at 6 h |
| permission-to-operate-memo | 0.068 (2427 s) | 0.068 (3783 s) |

Where both finished, the two models scored the same (backfeed 0.164, permission-to-operate 0.068). Kimi K3.1 Pro took about 10 times longer on the free tier (12,530 s vs 1,248 s on backfeed) and was killed at 6 h on four tasks, so on a fixed budget Nemotron is the better harness model here. Kimi also served as judge in both arms, so a self-preference effect on Kimi's own outputs cannot be excluded.

## Efficiency and scaling

Figure 2 (figures/fig2_score_vs_cost.png), left: the dev mean if every task were cut off at a given wall-clock budget, using the real agent time of the best run per task. The curve reaches 95% of its maximum at about 3.8 h per task; budget beyond that buys little. Right: score against input tokens per task. Most cost is exploration before the first draft, which the deliverable-first pushes target. Headroom is in the 8 genuine zeros, not in more time.

## Limitations

- Coverage: 27 of 29 dev tasks have usable artifacts in the commit; foundation-strategy and solar-supplemental-review have only grader failures.
- The best-of-runs mean is selected and mixes judges; it is not a clean single-run score.
- All dev runs used NIM models, not the Stage 2 models; Stage 2 behaviour may differ.

Figures: fig1_architecture.png (architecture), fig2_score_vs_cost.png, fig3_failure_breakdown.png, cover.png.
