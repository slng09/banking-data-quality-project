import json,subprocess,sys,sqlite3,unittest
from pathlib import Path
P=Path(__file__).resolve().parents[1]
class TestQuality(unittest.TestCase):
 @classmethod
 def setUpClass(cls):subprocess.run([sys.executable,str(P/'src'/'run.py')],check=True,capture_output=True)
 def test_controlled_defects(self):
  m=json.loads((P/'reports'/'metrics.json').read_text())
  self.assertEqual(m['source_rows'],1002)
  self.assertEqual(m['valid_rows'],995)
  self.assertEqual(m['missing_target_ids'],2)
  self.assertEqual(m['exception_counts']['AMOUNT_MISMATCH'],2)
  self.assertEqual(m['exception_counts']['CURRENCY_MISMATCH'],1)
 def test_reconciliation_counts(self):
  m=json.loads((P/'reports'/'metrics.json').read_text())
  self.assertEqual(m['matched_ids'],m['valid_rows']-m['missing_target_ids']-3)
 def test_sqlite_evidence(self):
  with sqlite3.connect(P/'data'/'banking_quality.sqlite') as c:
   self.assertEqual(c.execute('SELECT COUNT(*) FROM exceptions').fetchone()[0],json.loads((P/'reports'/'metrics.json').read_text())['exception_events'])
