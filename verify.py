from pathlib import Path
import hashlib,json,zipfile,xml.etree.ElementTree as E
p=Path(__file__).resolve().parent
for f in json.loads((p/'manifest.json').read_text(encoding='utf8')):
 b=(p/f['file']).read_bytes(); assert len(b)==f['bytes']; assert hashlib.sha256(b).hexdigest()==f['sha256']; print('SHA256 OK',f['file'],f['sha256'])
ns={'x':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
for file,expected in [('scoring.xlsx',5),('monthly.xlsx',4)]:
 with zipfile.ZipFile(p/file) as z:
  assert z.testzip() is None
  sheets=E.fromstring(z.read('xl/workbook.xml')).find('x:sheets',ns); assert len(sheets)==expected
  formula_counts=[len(E.fromstring(z.read(n)).findall('.//x:f',ns)) for n in z.namelist() if n.startswith('xl/worksheets/sheet') and n.endswith('.xml')]
  print('XLSX OK',file,'sheets',len(sheets),'formulas',formula_counts)
  if file=='scoring.xlsx': assert formula_counts[1]==40 and formula_counts[2]==40 and formula_counts[3]==12
  else: assert formula_counts[0]==24 and formula_counts[1]==24
c=json.loads((p/'checks.json').read_text(encoding='utf8')); assert len(c)==127 and all(t['pass'] for t in c); print('Recorded calculation assertions: 127/127 PASS (not rerun)')
