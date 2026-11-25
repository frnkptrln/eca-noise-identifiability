"""Reader's check of the local statements of report_boundaries.md (Sections 5.2, 5.3, 5.5; Lemmas M and M') by own
simulation. Claude, 25 November 2026. Bit i of a state is cell i. "Radius 2" of a cycle: every single flip of every
state of the cycle runs back into the cycle."""
def stepper(rule, n, wall=0, ring=False, reflect=False):
    full=(1<<n)-1
    def F(x):
        if ring:
            L=((x<<1)|(x>>(n-1)))&full; R=(x>>1)|((x&1)<<(n-1))
        elif reflect:
            L=((x<<1)|(x&1))&full; R=(x>>1)|(x&(1<<(n-1)))
        else:
            L=((x<<1)|wall)&full; R=(x>>1)|(wall<<(n-1))
        y=0
        for c in range(8):
            if (rule>>c)&1:
                y|=(L if c&4 else ~L)&(x if c&2 else ~x)&(R if c&1 else ~R)
        return y&full
    return F
def lands_on(F, x, target, cap=10**6):
    seen=set()
    while x not in seen and len(seen)<cap:
        if x in target: return True
        seen.add(x); x=F(x)
    return False
def radius2(F, n, cyc):
    """every single flip of every state of the cycle runs back into the cycle"""
    T=set(cyc)
    return all(lands_on(F, x^(1<<i), T) for x in cyc for i in range(n))
def bits(s): return sum(1<<i for i,ch in enumerate(s) if ch=='1')

# 94, null walls: crystal 11011...011 at n = 2 mod 3
F=lambda n: stepper(94,n)
res=[]
for n in range(5,63,3):
    x=bits(('110'*n)[:n]); assert F(n)(x)==x and x>>(n-2)==3
    res.append(radius2(F(n),n,[x]))
print('94 null, crystal 110..11 fixed and radius 2 at every n=2 mod 3, 5..62:', all(res))
# 133 (= 94 under one-walls): (010)^(n/3) at 3 | n
res=[]
for n in range(6,61,3):
    x=bits('010'*(n//3)); G=stepper(133,n); assert G(x)==x
    res.append(radius2(G,n,[x]))
print('133 null, (010)^k fixed and radius 2 at every 3|n, 6..60:', all(res))
# same statement in the 94 picture: rule 94 with one-walls, state (101)^(n/3)
ok=all(stepper(94,n,wall=1)(bits('101'*(n//3)))==bits('101'*(n//3)) for n in range(6,61,3)); print('94 with one-walls fixes (101)^k:', ok)
# 75 null: crystal 110..11 at n = 2 mod 3; radius
r75={}
for n in range(5,63,3):
    x=bits(('110'*n)[:n]); G=stepper(75,n); assert G(x)==x
    r75[n]=radius2(G,n,[x])
print('75 null, crystal radius 2 at n =',[n for n in r75 if r75[n]], '; not at n =',[n for n in r75 if not r75[n]])
# 22 null: all single flips die (by reflection symmetry the seeds i < (n+1)/2 suffice)
dies=[]; undecided=[]; decided_not=[]
for n in range(4,63):
    G=stepper(22,n); out=[]
    for i in range((n+1)//2):
        x=1<<i; seen=set(); t=0
        while x and x not in seen and t<20000: seen.add(x); x=G(x); t+=1
        out.append('dies' if x==0 else ('cycle' if t<20000 else '?'))
    if all(o=='dies' for o in out): dies.append(n)
    elif 'cycle' in out: decided_not.append(n)
    else: undecided.append(n)
print('22 null, every single flip of 0 dies at n =',dies,'; some flip runs into another cycle at every other n in 4..62 except n =',undecided,'(no flip decided within 20000 steps)')
# Proposition N: 154 and 26 follow rule 90 from a single flip; all die iff n+1 power of two
okN=True; dieN=[]
for n in range(3,70):
    f154,f26,f90=stepper(154,n),stepper(26,n),stepper(90,n); alldie=True
    for i in range(n):
        a=b=c=1<<i; died=False
        for t in range(4*n+10):
            a,b,c=f154(a),f26(b),f90(c)
            if not(a==b==c): okN=False
            if c==0: died=True; break
        alldie&=died
    if alldie: dieN.append(n)
print('154/26 single-flip orbits equal rule-90 orbits (n=3..69):',okN,'; all flips die at n =',dieN)
# 122 null: checkerboard 2-cycle radius 2
r122=[]
for n in range(4,62):
    G=stepper(122,n); x=bits(('01'*n)[:n]); y=G(x)
    if G(y)==x and radius2(G,n,[x,y]): r122.append(n)
print('122 null, checkerboard 2-cycle has radius 2 at n =',r122)
# 137 null: 2-cycle 1000 1000 ... <-> 0010 0010 ...
r137=[]
for n in range(4,62):
    G=stepper(137,n); x=bits(('1000'*n)[:n]); y=G(x)
    if G(y)==x and x!=y and radius2(G,n,[x,y]): r137.append(n)
print('137 null, the 2-cycle from 1000 1000.. has radius 2 at n =',r137)
# Lemma M and Lemma M'
import itertools
def lemmaM(rule,n):
    N=2*n+2; G=stepper(rule,n); R=stepper(rule,N,ring=True)
    for x in range(1<<n):
        def lift(v): 
            u=v
            for j in range(n): u|=((v>>j)&1)<<(N-2-j)
            return u
        if R(lift(x))!=lift(G(x)): return False
    return True
good=[r for r in range(256) if all(lemmaM(r,n) for n in range(1,8))]
print('Lemma M holds (n=1..7) exactly for rules',good)
def lemmaMr(rule,n):
    N=2*n; G=stepper(rule,n,reflect=True); R=stepper(rule,N,ring=True)
    for x in range(1<<n):
        lift=lambda v: v|sum(((v>>j)&1)<<(N-1-j) for j in range(n))
        if R(lift(x))!=lift(G(x)): return False
    return True
goodr=[r for r in range(256) if all(lemmaMr(r,n) for n in range(1,8))]
sym=[r for r in range(256) if all(((r>>c)&1)==((r>>(((c&1)<<2)|(c&2)|(c>>2)))&1) for c in range(8))]
print("Lemma M' holds (n=1..7) for",len(goodr),'rules; equal to the 64 reflection-symmetric rules:',goodr==sym)
