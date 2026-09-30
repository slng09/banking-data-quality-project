import csv,json
from pathlib import Path
from collections import Counter
p=Path(__file__).resolve().parents[1]
def read(name):
    return list(csv.DictReader((p/name).open()))
src=read('data/source_transactions.csv'); target=read('data/target_transactions.csv')
counts=Counter(r['id'] for r in src); targets={r['id']:r for r in target}
assert len(targets)==len(target)
data=[]
for i,r in enumerate(src):
    issues=[]; amount=int(r['amount_cents']); t=targets.get(r['id'])
    if counts[r['id']]>1: issues.append('Duplicate ID')
    if not r['account'].strip(): issues.append('Missing account')
    if r['currency']!='SGD': issues.append('Invalid currency')
    if amount<=0: issues.append('Invalid amount')
    valid=not issues; delta=None
    if valid:
        if t is None: issues.append('Missing target')
        else:
            delta=int(t['amount_cents'])-amount
            if delta: issues.append('Amount mismatch')
            if t['currency']!=r['currency']: issues.append('Currency mismatch')
    data.append(dict(row=i+1,id=r['id'],day=r['day'],feed=r['feed'],amount=amount,currency=r['currency'],valid=valid,matched=valid and not issues,issues=issues,delta=delta))
summary=dict(source=len(data),valid=sum(r['valid'] for r in data),matched=sum(r['matched'] for r in data),events=sum(len(r['issues']) for r in data),missing=sum('Missing target' in r['issues'] for r in data),variance=sum(r['delta'] or 0 for r in data))
assert summary==dict(source=1002,valid=995,matched=989,events=13,missing=3,variance=2500),summary
assert summary['events']==len(read('reports/exception_detail.csv'))
for f in read('reports/feed_summary.csv'):
    subset=[r for r in data if r['feed']==f['feed']]
    assert len(subset)==int(f['source_rows'])
    assert sum(len(r['issues']) for r in subset)==int(f['exception_events'])
for day in read('reports/daily_kpis.csv'):
    subset=[r for r in data if r['day']==day['day']]
    assert len(subset)==int(day['source_rows'])
    assert sum(r['valid'] for r in subset)==int(day['valid_rows'])
    assert sum(len(r['issues']) for r in subset)==int(day['exception_events'])
html=(Path(__file__).parent/'template.html').read_text(encoding='utf-8').replace('__DATA__',json.dumps(data,separators=(',',':')))
out=p/'index.html'
out.write_text(html,encoding='utf-8')
print(json.dumps(summary));print(out)
