"""Reader's check of the affine statements of report_boundaries.md, Section 5.1 (Proposition L, Theorems 90 and 150),
by own linear algebra over GF(2). Claude, 25 November 2026. It uses Proposition L (k* >= 1 iff the periodic states
jointly miss a code); walls.py checks that proposition by enumeration for n <= 16.
Rows of matrices are Python integers (bit j = column j)."""
import csv, sys, os
Z=os.environ.get('WALLS_DATA', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data', 'boundaries'))+'/'
def affine_coeffs(rule):
    f=lambda l,c,r:(rule>>(4*l+2*c+r))&1
    e=f(0,0,0); a=f(1,0,0)^e; b=f(0,1,0)^e; d=f(0,0,1)^e
    ok=all(f(l,c,r)==(a&l)^(b&c)^(d&r)^e for l in (0,1) for c in (0,1) for r in (0,1))
    return (a,b,d,e) if ok else None
def step(x,n,a,b,d,e):
    full=(1<<n)-1
    y=0
    if a: y^=(x<<1)&full      # cell i gets x[i-1]
    if b: y^=x
    if d: y^=x>>1             # cell i gets x[i+1]
    if e: y^=full
    return y
def rank_basis(vecs):
    basis=[]
    for v in vecs:
        for b in basis: v=min(v,v^b)
        if v: basis.append(v)
    return basis
def analyse(rule,n):
    a,b,d,e=affine_coeffs(rule)
    lin=lambda x: step(x,n,a,b,d,0)
    cols=[1<<i for i in range(n)]
    for _ in range(n): cols=[lin(c) for c in cols]          # M^n e_i
    basis=rank_basis(cols)                                    # V_inv
    x=0
    for _ in range(n): x=step(x,n,a,b,d,e)                   # a periodic state
    cover=0
    for i in range(n):
        def pat(v):
            l=(v>>(i-1))&1 if i>0 else 0
            r=(v>>(i+1))&1 if i<n-1 else 0
            return 4*l+2*((v>>i)&1)+r
        pb=rank_basis([pat(v) for v in basis]) if basis else []
        span={0}
        for p in pb: span|={s^p for s in span}
        base=pat(x)
        for s in span: cover|=1<<(base^s)
    return len(basis), ''.join(str(c) for c in range(8) if not (cover>>c)&1)
rules=[r for r in range(256) if affine_coeffs(r)]
print('affine rules:',rules)
tot=bad=0; mine={}
for r in csv.DictReader(open(Z+'affine_null.csv')):
    rule,n=int(r['rule']),int(r['n'])
    dim,missed=analyse(rule,n); mine[(rule,n)]=(dim,missed); tot+=1
    m2=r['missed'].strip(); m2='' if m2 in('-','nan') else m2
    if dim!=int(r['dim_periodic']) or missed!=m2 or (dim==n)!=(r['bijective']=='1') or (missed!='')!=(r['kstar_ge1']=='1'):
        bad+=1; print('DIFF',rule,n,dim,missed,r)
print('affine_null.csv: compared',tot,'records, differences',bad)
print('rule 90, k*>=1 at n =',[n for n in range(3,129) if mine[(90,n)][1]])
print('rule 165, k*>=1 at n =',[n for n in range(3,129) if mine[(165,n)][1]])
print('rule 150, k*>=1 at n =',[n for n in range(3,129) if mine[(150,n)][1]], '; not bijective exactly at n=2 mod 3:', all((mine[(150,n)][0]<n)==(n%3==2) for n in range(3,129)))
print('rule 105, k*>=1 at n =',[n for n in range(3,129) if mine[(105,n)][1]])
print('rule 60 bijective at every n:', all(mine[(60,n)][0]==n for n in range(3,129)), '; rule 153:', all(mine[(153,n)][0]==n for n in range(3,129)))
print('rule 90 nilpotent at n =',[n for n in range(3,129) if mine[(90,n)][0]==0], '; bijective iff n even:', all((mine[(90,n)][0]==n)==(n%2==0) for n in range(3,129)))
