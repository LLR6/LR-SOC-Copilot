# DNS Anomaly Triage

Use for long labels, high-entropy subdomains, unusual query volume or other DNS signals.

## Evidence to collect

- client / source host;
- full query and registered domain;
- queried record type;
- label length and entropy;
- request frequency;
- unique-subdomain ratio;
- NXDOMAIN ratio;
- resolver used;
- process responsible for the lookup if available.

## Do not over-interpret entropy

High entropy may be produced by legitimate:

- CDNs;
- tracking identifiers;
- telemetry;
- anti-abuse tokens;
- cloud service discovery;
- software update systems.

Compare against other hosts and the same application's normal behavior.

## Investigation sequence

1. Confirm the raw query in the source telemetry.
2. Split registered domain from generated subdomain labels.
3. Check whether many hosts show the same pattern.
4. Compare volume, uniqueness and timing.
5. Correlate with process, network and authentication alerts.
6. Search local allowlists and service-owner documentation.
7. Record benign explanations and unresolved questions.

DNS heuristics should raise investigation priority, not independently declare tunneling.
