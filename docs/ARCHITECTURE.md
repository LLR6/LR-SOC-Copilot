# LR-SOC-Copilot Architecture

```text
alert JSONL
   ↓
source-line enrichment
   ↓
entity + time correlation
   ↓
Case
 ├─ evidence[]
 ├─ evidence_coverage
 ├─ correlation_edges
 └─ triage score
   ↓
local runbook retrieval
   ↓
Markdown / JSON investigation brief
```

## Evidence model

Source lines are primary evidence. Case summaries, scores and retrieval results are derived aids and should never overwrite source provenance.

## Correlation model

Alerts can be connected when they share entities within the configured time window. Every accepted relationship is persisted as a `correlation_edge`.

## Retrieval model

Runbooks are local Markdown chunks ranked by transparent lexical similarity. Retrieval benchmarks protect known query→runbook behavior.

## Non-goals

- autonomous incident declaration;
- automated containment;
- remote action against endpoints;
- replacing analyst verification.
