# Threat Model

LR-SOC-Copilot correlates local alerts and retrieves local runbook text. The main security objective is to preserve **evidence provenance** while reducing investigation noise.

## Assets

- alert source references;
- local runbooks;
- case membership and correlation rationale;
- investigation summaries;
- analyst privacy.

## Trust boundaries

```text
alert JSONL (untrusted)
       │
       ▼
 parser ──► source-line refs
       │
       ▼
 correlation graph
       │
       ├── local runbooks (operator-controlled)
       ▼
 case report
```

Alert content is untrusted evidence. Runbooks are trusted as analyst-maintained guidance, but not as facts about a specific case.

## Primary risks

### Incorrect case merging

Two unrelated alerts may share a common entity such as NAT IP, service account, or shared host.

Mitigations:

- bounded time window;
- explicit shared-entity edges;
- source references on both sides of every correlation edge;
- analyst checklist before incident conclusion.

### Retrieval overreach

A semantically related runbook may not be applicable to the case.

Mitigations:

- retrieval result includes source chunk reference and similarity;
- runbook content is guidance, not evidence;
- configurable retrieval depth;
- labeled retrieval benchmark detects obvious drift.

### Unverifiable summaries

A generated or formatted brief can sound authoritative even when evidence is incomplete.

Mitigations:

- evidence IDs map to source lines;
- evidence coverage reports field completeness;
- score is explicitly a triage heuristic;
- investigation conclusions remain analyst-owned.

### Sensitive incident data exposure

Real alerts may contain customer names, IPs, hostnames, credentials, or internal process details.

The repository examples must remain synthetic. Public issues must not contain real incident data.

## Non-goals

The tool does not:

- perform containment;
- execute response actions;
- query production systems;
- collect credentials;
- decide whether an incident is confirmed;
- replace an analyst.

## Security invariants

1. Every evidence item keeps a source reference.
2. Correlation has an inspectable rationale.
3. Runbook text never becomes source evidence.
4. Case score never becomes an incident verdict.
5. Local files are not uploaded by the tool.
