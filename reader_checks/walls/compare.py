"""Compares the reader's records (walls.py) with the data files of the study. Claude, 25 November 2026.
Usage: python compare.py <null|reflect|ringvsnull> <reader csv> [more reader csv]
Data files are read from ../../data/boundaries (or from the folder in the environment variable WALLS_DATA)."""
import csv, sys, os
Z=os.environ.get('WALLS_DATA', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'boundaries'))+'/'
def nm(x):
    x=x.strip()
    if x in('-','nan'): return ''
    if x.endswith('.0'): x=x[:-2]
    return x
def refl(x): return ''.join(sorted(x.translate(str.maketrans('1436','4163'))))
mine={}
REFL=[0]
for f in sys.argv[2:]:
    for r in csv.DictReader(open(f)):
        mine[(int(r['rule']),int(r['n']))]=r
which=sys.argv[1]
if which=='ringvsnull':
    tot=bad=full=0
    for r in csv.DictReader(open(Z+'ring_vs_null.csv')):
        k=(int(r['rule']),int(r['n']))
        if k not in mine or r['null_kstar']=='': continue
        m=mine[k]; tot+=1
        if m.get('side','')=='' : print('undecided',k); continue
        ks=int(float(r['null_kstar']))
        a=nm(r['null_missed'])
        if a!=m['missed'] and refl(a)==m['missed']: REFL[0]+=1; a=m['missed']
        if (ks>=1)!=(m['side']=='1') or a!=m['missed']: bad+=1; print('SIDE/MISSED DIFF',k,r['null_kstar'],r['null_missed'],m['side'],m['missed'])
        if m['kstar']!='':
            full+=1
            if int(m['kstar'])!=ks: bad+=1; print('KSTAR DIFF',k,ks,m['kstar'])
    print('ring_vs_null: missed codes given for the mirror rule in',REFL[0],'records'); print('ring_vs_null: compared',tot,'records; exact k* compared in',full,'; differences',bad)
else:
    fn={'null':'null_sweep.csv','reflect':'reflect_sweep.csv'}[which]
    tot=bad=full=0
    for r in csv.DictReader(open(Z+fn)):
        k=(int(r['rule']),int(r['n']))
        if k not in mine: continue
        m=mine[k]; tot+=1
        if r['bijective']=='1':
            # session did not solve bijective rules; it records k*=0
            ok = m['side']=='0' and int(m['selected'])==int(m['cycles'])
            if not ok: bad+=1; print('BIJ DIFF',k,m)
            continue
        d=[]
        if int(r['cycles'])!=int(m['cycles']): d.append('cycles')
        if m.get('side','')=='': print('undecided',k); continue
        if int(r['n_stable'])!=int(m['selected']): d.append('n_stable')
        if int(r['gamma_min'])!=int(m['gamma_min']): d.append('gamma_min')
        if nm(r['missed_codes'])!=m['missed']: d.append('missed')
        if int(r['b_type'])!=int(m['btype']): d.append('btype')
        if (int(r['kstar'])>=1)!=(m['side']=='1'): d.append('side')
        if m['kstar']!='':
            full+=1
            if r['k_c']!=m['kc'] or int(r['kstar'])!=int(m['kstar']): d.append('kc/kstar')
        if d: bad+=1; print('DIFF',k,d,r['k_c'],r['kstar'],m.get('kc'),m.get('kstar'))
    print(fn,': compared',tot,'records; exact k_c compared in',full,'; differences',bad)
