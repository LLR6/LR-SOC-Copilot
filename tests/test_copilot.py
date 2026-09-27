import tempfile,unittest
from pathlib import Path
from soc_copilot.cli import correlate,load_alerts,retrieve

SAMPLE=Path(__file__).parents[1]/"examples/alerts.jsonl"
class CopilotTests(unittest.TestCase):
 def test_shared_entities_form_one_case(self):
  cases=correlate(load_alerts(SAMPLE));self.assertEqual(len(cases),2);self.assertEqual(len(cases[0]["alerts"]),3)
 def test_evidence_keeps_source_lines(self):self.assertEqual(load_alerts(SAMPLE)[0]["_ref"],"alerts.jsonl:L1")
 def test_retrieval_is_grounded(self):
  docs=[{"ref":"a","text":"login failure account compromise"},{"ref":"b","text":"dns resolver"}]
  self.assertEqual(retrieve("login compromise",docs,1)[0]["ref"],"a")
if __name__=="__main__":unittest.main()
