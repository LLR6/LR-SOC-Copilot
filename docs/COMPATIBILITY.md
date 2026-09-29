# Compatibility

## Runtime

- Python: **3.10+**
- CI target: **3.10 / 3.11 / 3.12**
- CLI: `soc-copilot`

## Input expectations

Alerts are local JSONL records with timestamp, rule, severity, summary and entities.

## Output compatibility

Evidence source references use `filename:L<number>` form.
Case output includes correlation edges and evidence coverage.

Minor releases may add output fields. Existing evidence/source semantics should remain stable.

## Runbooks

Runbooks are local Markdown files. Retrieval behavior is regression-tested against labeled fixtures.
