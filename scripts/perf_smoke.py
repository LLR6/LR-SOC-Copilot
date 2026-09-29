import argparse
import json
import time
from pathlib import Path

from soc_copilot.cli import chunks, correlate, load_alerts, serialize_case


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a non-gating SOC Copilot performance smoke report")
    parser.add_argument("alerts", type=Path)
    parser.add_argument("--runbooks", type=Path, default=Path("runbooks"))
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be >= 1")

    alerts = load_alerts(args.alerts)
    docs = chunks(args.runbooks)
    durations = []
    case_count = 0
    for _ in range(args.repeats):
        start = time.perf_counter()
        cases = [serialize_case(x, docs) for x in correlate(alerts)]
        durations.append(time.perf_counter() - start)
        case_count = len(cases)

    mean = sum(durations) / len(durations)
    report = {
        "schema": "lr-soc-copilot-performance-smoke/v1",
        "alerts": len(alerts),
        "runbook_chunks": len(docs),
        "cases": case_count,
        "repeats": args.repeats,
        "seconds": {
            "mean": round(mean, 6),
            "min": round(min(durations), 6),
            "max": round(max(durations), 6),
        },
        "alerts_per_second_mean": round(len(alerts) / mean, 2) if mean else None,
        "note": "Non-gating smoke measurement. Compare trends only on similar runners and fixtures.",
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
