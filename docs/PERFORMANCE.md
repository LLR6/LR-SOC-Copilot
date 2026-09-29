# Performance Policy

SOC Copilot CI publishes a non-gating performance smoke report using the bundled alert fixture and local runbooks.

It records:

- alert count;
- runbook chunk count;
- resulting Case count;
- repeated runtime;
- mean/min/max latency;
- mean alerts processed per second.

## Interpretation

Use this report for trend detection only.

Runbook retrieval and Case correlation are intentionally transparent and local. A future optimization should preserve:

- source-line evidence;
- correlation edges;
- retrieval determinism;
- benchmark behavior.

A faster implementation that removes evidence or changes ranking semantics without documentation is not automatically better.
