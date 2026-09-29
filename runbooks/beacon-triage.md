# Periodic Outbound Connection Triage

Use when an alert suggests low-jitter or repeated outbound connections.

## Questions to answer

1. Which host and process own the connections?
2. Is the destination expected for that host role?
3. Is the interval stable across a long enough window?
4. Does the pattern persist outside business hours?
5. Is the destination shared by many healthy hosts?
6. Does DNS/TLS/process evidence support or contradict the alert?

## Evidence to collect

- source host and destination;
- destination port / protocol;
- first and last seen;
- number of samples;
- mean interval and jitter/CV;
- process name and parent process where available;
- destination reputation from approved internal sources;
- DNS name / TLS SNI if available;
- comparison with peer hosts.

## Benign explanations

Periodic traffic can come from:

- monitoring agents;
- software update checks;
- backup clients;
- NTP-like scheduled services;
- cloud health checks;
- enterprise management software.

A periodic connection is not, by itself, proof of command-and-control.

## Escalation

Escalate when periodicity is accompanied by stronger evidence such as:

- unexpected process ancestry;
- a rare destination for the environment;
- suspicious authentication activity;
- DNS anomalies;
- unusual data transfer;
- a newly observed executable or persistence mechanism.

Record contradictory evidence before assigning an incident conclusion.
