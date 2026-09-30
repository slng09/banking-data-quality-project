import unittest,subprocess,sys,csv
from pathlib import Path
P=Path(__file__).resolve().parents[1]
class PipelineTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):subprocess.run([sys.executable,str(P/'src/run.py')],check=True,capture_output=True)
 def test_source_count(self):
  with (P/'data/source_transactions.csv').open() as f:self.assertEqual(len(list(csv.DictReader(f))),1002)
 def test_exception_types(self):
  with (P/'reports/exception_detail.csv').open() as f:types={r['type'] for r in csv.DictReader(f)}
  self.assertEqual(types,{'DUPLICATE_ID','MISSING_ACCOUNT','INVALID_CURRENCY','INVALID_AMOUNT','MISSING_TARGET','AMOUNT_MISMATCH','CURRENCY_MISMATCH'})
 def test_valid_counts(self):
  with (P/'reports/feed_summary.csv').open() as f:rows=list(csv.DictReader(f))
  self.assertEqual(sum(int(r['valid_rows']) for r in rows),995)
