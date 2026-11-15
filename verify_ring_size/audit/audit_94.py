"""Lead audit of verify_ring_size/part2_94/PROOF_94.md.
Written from the rule table only; imports nothing from part2_94/, code/ring_size/ or code/fw/.
States are tuples of 0/1; pure Python; exhaustive for small n."""
import itertools, json, time, sys
RULE = 94
def f(a, b, c): return (RULE >> (4*a + 2*b + c)) & 1
def F(x):
    n = len(x); return tuple(f(x[i-1], x[i], x[(i+1) % n]) for i in range(n))
def occ(x):
    n = len(x); return {i for i in range(n) if (x[i-1], x[i], x[(i+1) % n]) == (1, 0, 1)}
def W(x):
    n = len(x); s = set()
    for i in occ(x): s |= {(i-1) % n, i, (i+1) % n}
    return s
def flip(x, j):
    y = list(x); y[j] ^= 1; return tuple(y)
def is_block_word(x):
    n = len(x)
    if 0 not in x: return False
    for i in range(n):
        if x[i] == 0 and (x[i-1] == 0 or x[(i+1) % n] == 0): return False
        if x[i] == 1 and x[i-1] == 1 and x[(i+1) % n] == 1: return False
    return True
def attractor(y):
    """Return (frozenset of cycle states) reached from y."""
    seen = {}; t = 0
    while y not in seen:
        seen[y] = t; y = F(y); t += 1
    cyc = [y]; z = F(y)
    while z != y: cyc.append(z); z = F(z)
    return frozenset(cyc)

res = {"rule": RULE, "tests": {}}
t0 = time.process_time()
# Lemma 1, Lemma 2, Lemma 3 on every state
l1 = l2 = l3 = 0; n1 = n3 = 0
for n in range(3, 15):
    for x in itertools.product((0, 1), repeat=n):
        Fx = F(x); wx = W(x); n1 += 1
        if not occ(x) <= occ(Fx) or any(Fx[i] != x[i] for i in wx): l1 += 1
        ff = (len(wx) == n)
        if ff != is_block_word(x) or (ff and Fx != x): l2 += 1
        if n >= 5 and not ff:
            n3 += 1; ok = False
            for j in range(n):
                if j in wx: continue
                y = F(F(flip(x, j)))
                if W(y) > wx: ok = True; break
            if not ok: l3 += 1
res["tests"]["L1_freezing_n3_14"] = {"states": n1, "violations": l1}
res["tests"]["L2_fully_frozen_n3_14"] = {"states": n1, "violations": l2}
res["tests"]["L3_growth_exists_n5_14"] = {"states": n3, "violations": l3}
# Lemmas 4, 5 on every block word; Lemma 6; full chain from every cycle for 3 | n
def block_words(n):
    return [x for x in itertools.product((0, 1), repeat=n) if is_block_word(x)]
l4 = l5 = n4 = n5 = n5x = l5x = 0
for n in range(6, 19):
    for x in block_words(n):
        nblocks = x.count(0)
        for p in range(n):
            w5 = tuple(x[(p+k) % n] for k in range(5))
            if w5 == (0, 1, 0, 1, 1) and nblocks >= 3:
                n4 += 1
                y = flip(x, (p+2) % n); Fy = F(y)
                xp = list(x)
                for k, v in enumerate((0, 1, 1, 0, 1)): xp[(p+k) % n] = v
                xp = tuple(xp)
                good = (F(Fy) == y and Fy != y and x not in (y, Fy) and flip(Fy, (p+2) % n) == xp
                        and is_block_word(xp) and F(xp) == xp)
                if not good: l4 += 1
            w6 = tuple(x[(p+k) % n] for k in range(6))
            if w6 == (0, 1, 0, 1, 0, 1):
                # Lemma 5 hypothesis: three consecutive SHORT blocks, i.e. the cell after the window is a 0.
                # (First version of this audit omitted that condition; the split below records both readings.)
                xpp = list(x)
                for k, v in enumerate((0, 1, 1, 0, 1, 1)): xpp[(p+k) % n] = v
                xpp = tuple(xpp)
                bad = not (F(flip(x, (p+3) % n)) == xpp and is_block_word(xpp) and xpp != x)
                if x[(p+6) % n] == 0:
                    n5 += 1; l5 += bad
                else:
                    n5x += 1; l5x += bad
res["tests"]["L4_swap_n6_18"] = {"occurrences": n4, "violations": l4}
res["tests"]["L5_merge_n6_18"] = {"occurrences": n5, "violations": l5}
res["tests"]["L5_window_010101_followed_by_1_not_covered_by_lemma"] = {"occurrences": n5x, "violations": l5x}
l6 = n6 = 0
for n in range(6, 61, 3):
    x = tuple([0, 1, 1] * (n // 3))
    for j in range(n):
        n6 += 1
        if F(F(F(flip(x, j)))) != x: l6 += 1
res["tests"]["L6_crystal_heals_n6_60"] = {"flips": n6, "violations": l6}
# Independent closed-class computation of G1 for 3 | n, n = 6..15 (all states)
cc = {}
for n in (6, 9, 12, 15):
    att = {}
    for x in itertools.product((0, 1), repeat=n):
        if x not in att:
            path = []; y = x
            while y not in att and y not in path: path.append(y); y = F(y)
            if y in att: a = att[y]
            else:
                k = path.index(y); a = frozenset(path[k:])
            for z in path: att[z] = a
    cycles = set(att.values())
    succ = {c: set() for c in cycles}
    for c in cycles:
        for x in c:
            for j in range(n):
                d = att[flip(x, j)]
                if d != c: succ[c].add(d)
    crystal = {frozenset([tuple(([0, 1, 1] * (n // 3))[r:] + ([0, 1, 1] * (n // 3))[:r])]) for r in range(3)}
    # cycles that can reach the crystal: reverse search
    pred = {c: set() for c in cycles}
    for c, ss in succ.items():
        for d in ss: pred[d].add(c)
    reach = set(crystal); stack = list(crystal)
    while stack:
        d = stack.pop()
        for c in pred[d]:
            if c not in reach: reach.add(c); stack.append(c)
    cc[n] = {"cycles": len(cycles), "crystal_phases_have_no_out_edge": all(not succ[c] for c in crystal),
             "cycles_without_G1_path_to_crystal": len(cycles) - len(reach)}
res["closed_class_check_3_divides_n"] = cc
res["cpu_seconds"] = round(time.process_time() - t0, 2)
json.dump(res, open(sys.argv[1], "w"), indent=1)
print(json.dumps(res, indent=1))
