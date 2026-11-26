"""Small check of the Lean statements on rule 154 (lean/RingSize/Rule154/Statement.lean), from the definitions.

1. For n = 1..6 and 8: the cycles of rule 154 and V({0}, C) for every cycle C != {0}, where V is the least
   resistance of a path from 0 to a state of C and a step x -> y has resistance H(F x, y). Paths are searched up to
   total resistance 3 only; a larger value would be printed as 99. Theorem_3_9_b says: least value >= 2 for n = 2^(k+1).
2. For n = 2, 4, 6, 8, 16: Lemma_3_3 for every state of E or O (F x = L x, F x in the other class, F^t x = L^t x
   for t <= n), and for powers of two Lemma_3_4_a (F^(n/2) x = 0).

Uses no code of the repository. Run: python3 check.py > out.txt (a few seconds).

Claude, 26 November 2026
"""
import itertools, heapq
def f154(a,b,c): return (154>>(4*a+2*b+c))&1
def F(x):
    n=len(x); return tuple(f154(x[(i-1)%n],x[i],x[(i+1)%n]) for i in range(n))
def L(x):
    n=len(x); return tuple((x[(i-1)%n]+x[(i+1)%n])%2 for i in range(n))
def cycles(n):
    S=list(itertools.product((0,1),repeat=n)); cyc={}
    for x in S:
        y=x
        for _ in range(2**n): y=F(y)
        # y periodic
        c=[y]; z=F(y)
        while z!=y: c.append(z); z=F(z)
        cyc[frozenset(c)]=1
    return list(cyc)
def dist_from(n,src):
    # resistance r(x,y)=H(F x,y); Dijkstra from set src
    d={x:0 for x in src}; pq=[(0,x) for x in src]
    while pq:
        w,x=heapq.heappop(pq)
        if w>d[x]: continue
        fx=F(x)
        for k in range(0,n+1):
            if w+k>3: break
            for pos in itertools.combinations(range(n),k):
                y=list(fx)
                for p in pos: y[p]^=1
                y=tuple(y)
                if d.get(y,99)>w+k: d[y]=w+k; heapq.heappush(pq,(w+k,y))
    return d
for n in (1,2,3,4,5,6,8):
    zero=tuple([0]*n); C=cycles(n); d=dist_from(n,[zero])
    V=sorted(min(d.get(x,99) for x in c) for c in C if c!=frozenset([zero]))
    print("n",n,"cycles",len(C),"V({0},C) values:",V[:6],"min",min(V) if V else None)
# Lemma 3.3 / 3.4(a) with parity by representative
for n in (2,4,6,8,16):
    ok33=True; ok34=True
    for x in itertools.product((0,1),repeat=n):
        E=all(x[i]==0 for i in range(n) if i%2==1); O=all(x[i]==0 for i in range(n) if i%2==0)
        if E:
            y=F(x); ok33&=(y==L(x)) and all(y[i]==0 for i in range(n) if i%2==0)
        if O:
            y=F(x); ok33&=(y==L(x)) and all(y[i]==0 for i in range(n) if i%2==1)
        if E or O:
            a=b=x
            for t in range(n):
                a=F(a); b=L(b); ok33&=(a==b)
            if n&(n-1)==0:
                y=x
                for _ in range(n//2): y=F(y)
                ok34&=(y==tuple([0]*n))
    print("n",n,"Lemma 3.3:",ok33,"Lemma 3.4(a):",ok34 if n&(n-1)==0 else "n/a")
