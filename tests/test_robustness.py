import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from soc_copilot.cli import chunks, correlate, load_alerts, retrieve


class RobustnessTests(unittest.TestCase):
    def test_bad_json_reports_source_line(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "alerts.jsonl"
            path.write_text('{"timestamp":"2026-09-29T00:00:00Z","entities":[]}\n{bad}\n', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, r"alerts\.jsonl:2"):
                load_alerts(path)

    def test_empty_alert_file_produces_no_cases(self):
        with TemporaryDirectory() as d:
            path = Path(d) / "alerts.jsonl"
            path.write_text("", encoding="utf-8")
            self.assertEqual(correlate(load_alerts(path)), [])

    def test_empty_runbook_directory_returns_no_hits(self):
        with TemporaryDirectory() as d:
            docs = chunks(Path(d))
            self.assertEqual(retrieve("anything", docs), [])


if __name__ == "__main__":
    unittest.main()
