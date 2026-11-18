# ProofCraft — gating an engineering agent on verified artifacts

**Repo:** REPO_PLACEHOLDER · **Commit:** SHA_PLACEHOLDER

## Headline finding

Across every full development run on the PLE dev set, the zero scores came from the agent's *output discipline*, not from its engineering reasoning. The model could read the drawings, reason about a data-hall layout and emit 450 KB of IFC. What it could not reliably do was leave a schema-valid file at the exact path the grader reads. Four failure modes account for all of them, and each one is now a mechanism in the harness rather than a hope.

## What ProofCraft is

An agent harness for Physical-Engineering's Last Exam. It speaks the kit's WebSocket protocol, runs a tool loop (bash, read_file, write_file, edit_file, plus whatever MCP servers the task exposes), and wraps that loop in gates that decide when the agent is allowed to stop.

1. **Deliverable-first progress pushes.** Every 20 tool calls the harness injects a message: write a complete first version of the required deliverable at its exact path now, then improve it. Motivation: run n1 spent 70+ turns reading drawings and iterating layout scripts in /tmp while the graded file stayed a 1 KB placeholder.
2. **Forced-write mode.** After 30 tool calls with no write_file or edit_file, the next turn offers only the write tools with tool_choice required, up to three times. Motivation: n2 made 56 tool calls, all reads, and never wrote anything.
3. **Unfinished-answer gate.** A text-only reply is refused while more than half the time budget remains. The agent is told to act on what it just said and write a partial deliverable. Motivation: n4 ended after 21 minutes of a 6-hour budget with the sentence "No feasible layout found... Let me debug" and zero files.
4. **Independent format validation before finishing.** Before a final answer is accepted, the harness pushes the agent to run the task's own validator (for IFC, `python3 -m ifcopenshell.validate --rules <file>`) and read the result back. Motivation: n6's final message claimed "validated" while the file carried 689 schema violations.

Two transport-level remedies were needed before any of this could run on a free endpoint: dropping message fields an endpoint refuses (NVIDIA NIM rejects the `channel` field that gpt-oss echoes back), and parsing "try again in 31m31s" out of a 429 body so the harness waits the right length instead of retrying into the wall.

## The runs, honestly

| Run | Task | Model | Score | Wall clock | What the agent left behind |
|---|---|---|---|---|---|
| n6 | data-hall-mep-routing | Nemotron 3 Ultra 550B | 0.000 | 5512 s | model.ifc 447 KB, reconciliation JSON, solution.py — 689 schema violations |
| n7 | data-hall-mep-routing | Nemotron 3 Ultra 550B | 0.000 | 4835 s | IFC 888 KB written to model_final.ifc, so the graded path was empty |
| n8 | fire-test-validation-memo | Nemotron 3 Ultra 550B | 0.409 | 1181 s | memo + artifacts, rubric-judged |
| c1 | fire-test-validation-memo | Nemotron 3.5 Lightning 30B | 0.149 | 1192 s | memo, 31 of 208 rubric points |
| n1–n5 | data-center-site-model | Nemotron 3 Ultra | no score | — | exploration only, or lost to sandbox resets |

The two zeros are the interesting ones, and they are different failures.

**n6 — the file was wrong.** The agent produced a real building: two-storey data hall, substation, generator yard, berm, stormwater basin, MV cable polyline, local CRS in metres. The verifier's first error was `IfcShapeRepresentation` placed directly in a product's Representation attribute instead of wrapped in `IfcProductDefinitionShape`. That is the single most common IFC authoring mistake there is, and it is exactly the kind of thing an engineer catches by running the schema check before handing the file over. The agent did not run it, and then said it had validated. That sentence is the failure: not the geometry, the claim.

**n7 was worse and more instructive.** The model produced a 1.0 MB IFC, a reconciliation JSON and a 44 KB solution.py, then renamed model.ifc to model_final.ifc while tidying up. The grader read an empty path. The verifier reported ERR_CONNECTIVITY with all six rows unserved, while gate_1_no_hard_clash passed — the engineering was fine, the file was in the wrong place. No amount of reasoning quality survives that.

Both failures are path-and-format failures, which is why the harness now checks declared deliverable paths and pushes the validator, rather than trying to make the model smarter.

## Cross-model generalizability

The same harness, the same memo task, two different NVIDIA models: 0.409 on Nemotron 3 Ultra 550B and 0.149 on Nemotron 3.5 Lightning 30B. The gates are model-agnostic by construction — they key on tool counts and elapsed time, never on the shape of the model's prose. What changed between the two models was how often the gates had to fire, not whether they worked.

One honest caveat: the judge used for the two memo runs was not identical in provenance, so the 0.409 versus 0.149 gap is indicative of a capability difference, not a controlled ablation. I am not claiming a clean model comparison.

## Efficiency and scaling

API spend across every run in this writeup: $0. Development ran on free-tier endpoints with a local LiteLLM proxy mapping the kit's model ids onto them, which the rules permit for development as long as the model is documented — it is, here.

n6 consumed 638k input and 47k output tokens over 5512 seconds; n7 was comparable. The gates cost nothing when the agent is behaving and one extra turn when it is not, which is a rounding error against a six-hour budget. The real cost driver is exploration: n1 and n2 burned 70 and 56 tool calls respectively before writing anything, and that is the behaviour the progress pushes exist to cut short.

Scaling to the full 29-task dev set is a throughput problem, not a design one: each task needs its own container image and up to six hours of wall clock, and the free endpoints rate-limit hard enough that a single task can take a day.

## Limitations

- Only two of the 29 dev tasks have produced artifacts. The dev score is a mean over 29, so it reads near zero even where a task scored 0.409.
- Path discipline is enforced by instruction and by the verify push, not yet by a programmatic check that the declared deliverable exists before a final answer is accepted. That check is the next thing to build, and validating it by converting a zero into a non-zero is the next experiment. I would rather say so than imply otherwise.
- Development ran on a sandbox that was reset repeatedly. Several runs (t4, t5, n1, n5) were lost mid-flight; their outcomes are unknown, and I have recorded them as unknown rather than as zeros.
- The IFC work is one task family. The memo task exercises a different path (rubric judging rather than a programmatic verifier), and the harness behaves differently on each.
