# Benchmarks

## Local runbook retrieval

Fixture: `benchmarks/retrieval.json`

The benchmark contains labeled queries for:

- account compromise;
- process triage;
- beacon triage;
- DNS anomaly triage;
- network scan triage.

Run:

```bash
python scripts/evaluate_retrieval.py benchmarks/retrieval.json --fail-on-regression
```

Current gate requires the expected runbook file to rank Top-1 for every fixture.

## What this does not measure

It does not measure full incident-investigation quality, analyst usefulness, or production retrieval performance. It only guards the current deterministic local retrieval behavior against regressions.
