import tempfile,unittest
from pathlib import Path
from soc_copilot.cli import correlate,evidence_coverage,load_alerts,retrieve,serialize_case

SAMPLE=Path(__file__).parents[1]/"examples/alerts.jsonl"
class CopilotTests(unittest.TestCase):
 def test_shared_entities_form_one_case(self):
  cases=correlate(load_alerts(SAMPLE));self.assertEqual(len(cases),2);self.assertEqual(len(cases[0]["alerts"]),3)
 def test_evidence_keeps_source_lines(self):self.assertEqual(load_alerts(SAMPLE)[0]["_ref"],"alerts.jsonl:L1")
 def test_retrieval_is_grounded(self):
  docs=[{"ref":"a","text":"login failure account compromise"},{"ref":"b","text":"dns resolver"}]
  self.assertEqual(retrieve("login compromise",docs,1)[0]["ref"],"a")
 def test_evidence_coverage_reports_complete_rows(self):
  evidence=[
   {"source":"a:L1","timestamp":"2026-09-29T00:00:00Z","rule":"R1","entities":["host"]},
   {"source":"a:L2","timestamp":"2026-09-29T00:01:00Z","rule":"R2","entities":[]},
  ]
  self.assertEqual(evidence_coverage(evidence),{"complete":1,"total":2,"ratio":0.5})
 def test_serialize_case_limits_runbooks(self):
  case=correlate(load_alerts(SAMPLE))[0]
  docs=[
   {"ref":"a","text":"login failure account compromise"},
   {"ref":"b","text":"process triage powershell suspicious child"},
  ]
  out=serialize_case(case,docs,1)
  self.assertLessEqual(len(out["runbooks"]),1)
  self.assertIn("evidence_coverage",out)
if __name__=="__main__":unittest.main()
