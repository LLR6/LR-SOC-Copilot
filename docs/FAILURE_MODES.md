# Known Failure Modes

- Shared infrastructure creates accidental Case merges.
  - Inspect `correlation_edges` and shared entities.
- One incident is split because the time window is too small.
  - Compare adjacent Cases and timeline.
- Runbook retrieval ranks a lexically similar but wrong guide.
  - Inspect Top-k results; benchmark local queries.
- Missing entities reduce correlation quality.
  - Evidence coverage exposes incomplete records.
- Triage score is mistaken for compromise probability.
  - Treat it only as review priority.
- A Case summary outruns its evidence.
  - Return to source refs before accepting a conclusion.
