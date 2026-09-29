# Network Scan / Port Fan-out Triage

Use when one source contacts many destination ports or services in a short window.

## Evidence to collect

- source and destination;
- distinct destination ports;
- time window;
- connection outcome where available;
- source asset owner / role;
- whether the source belongs to an approved scanner;
- whether the pattern is one-target-many-ports or many-targets-few-ports.

## Common benign sources

- vulnerability scanners;
- asset discovery;
- monitoring systems;
- deployment/orchestration tooling;
- troubleshooting by administrators;
- service-mesh or health-check behavior.

## Investigation sequence

1. Confirm the source asset identity.
2. Check approved scanner inventory and maintenance windows.
3. Review whether authentication attempts followed discovery.
4. Compare with historical behavior from the same source.
5. Correlate with endpoint process telemetry if available.
6. Preserve the actual port list and timing as evidence.

If discovery is followed by repeated authentication failure and then success, treat the sequence as materially stronger than the scan alert alone.
