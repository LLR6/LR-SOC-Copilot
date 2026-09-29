# LR-SOC-Copilot Research Card

## Question

Can local alert correlation and evidence-grounded runbook retrieval produce investigation briefs that remain easy to verify against source data?

## Hypotheses

1. Source-line evidence improves auditability of generated Case summaries.
2. Explicit correlation edges reduce uncertainty about why alerts were grouped.
3. Local runbook retrieval can remain useful without hiding scoring logic.
4. Negative retrieval cases are necessary to detect over-eager matching.

## Method

- Load line-oriented alerts and attach source references.
- Correlate by shared entities within a time window.
- Persist the pairwise correlation rationale.
- Retrieve local runbook chunks using transparent lexical similarity.
- Benchmark known query→runbook pairs plus unrelated negative queries.

## Metrics

- Evidence coverage ratio
- Case count
- Correlation edge count
- Retrieval Top-1 accuracy on labeled benchmark cases
- Negative-query false retrieval

## Current evidence

The repository currently demonstrates:

- source refs survive into investigation briefs;
- grouping rationale is machine-readable;
- local retrieval benchmark cases can be gated in CI;
- unrelated text can be required to produce no retrieval result.

It does not establish analyst productivity gains yet.

## Threats to validity

- small local runbook corpus;
- lexical retrieval baseline;
- synthetic alert examples;
- no analyst study;
- heuristic case score.

## Next experiment

Create a small analyst-style case set with alternate acceptable runbooks and measure retrieval quality with top-k and multiple-valid-answer evaluation.
