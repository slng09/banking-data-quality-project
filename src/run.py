import csv,random,sqlite3,html
from pathlib import Path
from collections import Counter
from datetime import date,timedelta
P=Path(__file__).resolve().parents[1]
random.seed(42)
rows=[]
for i in range(1,1001):
 rows.append(dict(id=f'TX{i:05}',day=(date(2026,8,1)+timedelta(days=i%30)).isoformat(),feed='CARDS' if i%2 else 'CORE',account=f'AC{random.randrange(1000,2000)}',amount_cents=random.randrange(100,100000),currency='SGD'))
source=[r.copy() for r in rows];source[9]['account']='';source[39]['currency']='XYZ';source[69]['amount_cents']=-100;source.append(source[99].copy());source.append(source[299].copy())
target=[r.copy() for r in rows if r['id'] not in {'TX00151','TX00451','TX00751'}]
for r in target:
 if r['id'] in {'TX00201','TX00601'}:r['amount_cents']+=1250
 if r['id']=='TX00801':r['currency']='USD'
def write(path,data):
 with path.open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
write(P/'data/source_transactions.csv',source);write(P/'data/target_transactions.csv',target)
db=P/'data/quality.db';db.unlink(missing_ok=True);con=sqlite3.connect(db)
con.executescript('CREATE TABLE source(id TEXT,day TEXT,feed TEXT,account TEXT,amount_cents INTEGER,currency TEXT);CREATE TABLE target(id TEXT PRIMARY KEY,day TEXT,feed TEXT,account TEXT,amount_cents INTEGER,currency TEXT);CREATE TABLE exceptions(id TEXT,day TEXT,feed TEXT,type TEXT,detail TEXT);')
cols=['id','day','feed','account','amount_cents','currency']
con.executemany('INSERT INTO source VALUES (?,?,?,?,?,?)',[[r[c] for c in cols] for r in source]);con.executemany('INSERT INTO target VALUES (?,?,?,?,?,?)',[[r[c] for c in cols] for r in target]);counts=Counter(r['id'] for r in source);t={r['id']:r for r in target};exc=[];valid=[];matched=0;missing=0;variance=0
def issue(r,typ,detail):exc.append(dict(id=r['id'],day=r['day'],feed=r['feed'],type=typ,detail=detail))
for r in source:
 bad=False
 for cond,typ,detail in [(counts[r['id']]>1,'DUPLICATE_ID','Repeated source ID'),(not r['account'],'MISSING_ACCOUNT','Blank account'),(r['currency']!='SGD','INVALID_CURRENCY','Unexpected currency'),(r['amount_cents']<=0,'INVALID_AMOUNT','Nonpositive amount')]:
  if cond:issue(r,typ,detail);bad=True
 if bad:continue
 valid.append(r);other=t.get(r['id'])
 if not other:issue(r,'MISSING_TARGET','Not found in target');missing+=1;continue
 mismatch=False
 if r['amount_cents']!=other['amount_cents']:issue(r,'AMOUNT_MISMATCH','Source/target amount differs');variance+=other['amount_cents']-r['amount_cents'];mismatch=True
 if r['currency']!=other['currency']:issue(r,'CURRENCY_MISMATCH','Source/target currency differs');mismatch=True
 if not mismatch:matched+=1
con.executemany('INSERT INTO exceptions VALUES (?,?,?,?,?)',[[r[c] for c in ['id','day','feed','type','detail']] for r in exc]);con.commit()
write(P/'reports/exception_detail.csv',exc)
summary=[]
for feed in ['CARDS','CORE']:
 s=[r for r in source if r['feed']==feed];v=[r for r in valid if r['feed']==feed];e=[r for r in exc if r['feed']==feed]
 summary.append(dict(feed=feed,source_rows=len(s),valid_rows=len(v),validation_pass_pct=round(100*len(v)/len(s),2),exception_events=len(e)))
write(P/'reports/feed_summary.csv',summary)
daily=[]
for day in sorted(set(r['day'] for r in source)):
 s=[r for r in source if r['day']==day];v=[r for r in valid if r['day']==day];e=[r for r in exc if r['day']==day]
 daily.append(dict(day=day,source_rows=len(s),valid_rows=len(v),exception_events=len(e)))
write(P/'reports/daily_kpis.csv',daily)
ct=Counter(r['type'] for r in exc)
cards=''.join(f'<article><small>{label}</small><h2>{value}</h2></article>' for label,value in [('Source rows',len(source)),('Validation pass rate',f'{100*len(valid)/len(source):.2f}%'),('Matched IDs',matched),('Missing target IDs',missing),('Amount variance',f'SGD {variance/100:,.2f}')]);table=''.join(f'<tr><td>{html.escape(k)}</td><td>{v}</td></tr>' for k,v in ct.most_common())
(P/'dashboard/index.html').write_text(f'''<!doctype html><html><head><meta charset="utf-8"><title>Banking Data Quality Monitor</title><style>body{{font:16px system-ui;background:#f2f6f8;color:#183047;margin:0}}header{{background:#17354b;color:white;padding:32px}}main{{max-width:1100px;margin:auto;padding:30px}}section{{display:flex;flex-wrap:wrap;gap:16px}}article{{background:white;border-radius:12px;padding:22px;min-width:145px;flex:1}}small{{color:#5b7686}}h2{{color:#087f80}}table{{background:white;width:100%;border-collapse:collapse}}td,th{{padding:12px;text-align:left;border-bottom:1px solid #ddd}}</style></head><body><header><h1>Banking Data Quality Monitor</h1><p>Fictional bank · Synthetic transactions · Reporting readiness prototype</p></header><main><section>{cards}</section><h2>Exception events</h2><table><tr><th>Type</th><th>Count</th></tr>{table}</table><p>For transaction-level investigation, see reports/exception_detail.csv.</p></main></body></html>''')
print(f'Processed {len(source)} source rows, {len(valid)} valid rows, {matched} matched IDs, {len(exc)} exception events')
