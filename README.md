# ProofCraft

An agent harness for **Physical-Engineering's Last Exam** (PLE).

ProofCraft runs the kit's WebSocket protocol and drives a tool loop, wrapped in four gates that decide when the agent may stop: deliverable-first progress pushes, forced-write mode, an unfinished-answer gate, and independent format validation before a final answer is accepted.

- `serve.py` — the harness (protocol, tool loop, gates)
- `taskbridge.py` — bridge to the task environment's tools
- `submission.yaml` — kit configuration
- `artifacts/` — development artifacts produced by `eval/run.py`
- `writeup.md` — the writeup
- `figures/` — architecture, score-vs-cost, failure breakdown, cover

Licensed Apache-2.0. Built on the Apache-2.0 `custom-openai` sample from `google-research/ple`.
