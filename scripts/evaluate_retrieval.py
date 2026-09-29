import argparse
import json
from pathlib import Path

from soc_copilot.cli import chunks, retrieve


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate local runbook retrieval against labeled queries")
    parser.add_argument("benchmark", type=Path)
    parser.add_argument("--runbooks", type=Path, default=Path("runbooks"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-on-regression", action="store_true")
    args = parser.parse_args()

    data = json.loads(args.benchmark.read_text(encoding="utf-8"))
    if data.get("schema") != "lr-soc-copilot-retrieval-benchmark/v1":
        parser.error("unsupported benchmark schema")

    docs = chunks(args.runbooks)
    results = []
    passed = 0
    for case in data.get("cases", []):
        hits = retrieve(case["query"], docs, 1)
        top = hits[0]["ref"] if hits else None
        expected_file = case.get("expected_file")
        ok = (top is None) if expected_file is None else bool(top and top.startswith(expected_file + "#"))
        passed += int(ok)
        results.append({
            "id": case["id"],
            "query": case["query"],
            "expected_file": case["expected_file"],
            "top_ref": top,
            "passed": ok,
        })

    total = len(results)
    report = {
        "schema": "lr-soc-copilot-retrieval-report/v1",
        "passed": passed,
        "total": total,
        "top1_accuracy": round(passed / total, 4) if total else 0.0,
        "results": results,
    }
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 2 if args.fail_on_regression and passed != total else 0


if __name__ == "__main__":
    raise SystemExit(main())
