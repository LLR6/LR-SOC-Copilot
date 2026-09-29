# Contributing

Useful contributions include correlation logic, evidence provenance, local retrieval, benchmark cases, runbooks, and tests.

## Expectations

- Every derived conclusion must remain traceable to source evidence.
- New correlation logic should expose why alerts were connected.
- Retrieval changes should update or extend the labeled retrieval benchmark.
- Runbooks should include benign explanations and evidence to collect, not only escalation steps.
- Synthetic examples must not contain real credentials or customer data.

## Checks

```bash
python -m pip install -e .
python -m unittest discover -s tests
python scripts/evaluate_retrieval.py benchmarks/retrieval.json --fail-on-regression
```
