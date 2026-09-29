# Engineering Decisions

## D1 — Source lines are primary evidence

Every investigation brief should allow a reviewer to return to the original alert line.

## D2 — Correlation must expose its edges

Case grouping stores shared entities and time deltas instead of hiding the reason alerts were linked.

## D3 — Retrieval stays local and inspectable

Runbook retrieval uses local Markdown and transparent similarity scoring.

## D4 — Triage scores are heuristics

A score controls review priority; it is never an incident verdict or probability of compromise.

## D5 — Runbooks include benign explanations

A useful investigation guide should tell the analyst what evidence could falsify the suspicious interpretation.
