"""Lead audit of verify_ring_size/part2_154/PROOF_154.md (rule 154 part).
Written from the rule table; imports nothing from part2_154/, code/ring_size/ or code/fw/.
State = integer, bit i = cell i. Exhaustive over all states for the n listed."""
import numpy as np, json, sys, time
RULE = 154
def Ftable(n):
    x = np.arange(1 << n, dtype=np.int64)
    out = np.zeros_like(x)
    for i in range(n):
        a = (x >> ((i - 1) % n)) & 1; b = (x >> i) & 1; c = (x >> ((i + 1) % n)) & 1
        out |= ((RULE >> (4 * a + 2 * b + c)) & 1) << i
    return out
def periodic_mask(F):
    N = len(F); alive = np.ones(N, bool)
    while True:                      # states in the eventual image F^t(S), t large
        img = np.zeros(N, bool); img[F[alive]] = True
        new = alive & img
        if new.sum() == alive.sum(): return new
        alive = new
def attractor_labels(F, per):
    """label[x] = smallest state of the cycle reached from x."""
    N = len(F); lab = np.full(N, -1, np.int64)
    for s in np.nonzero(per)[0]:
        if lab[s] >= 0: continue
        cyc = [s]; y = F[s]
        while y != s: cyc.append(y); y = F[y]
        lab[cyc] = min(cyc)
    x = np.arange(N); cur = x.copy()
    todo = lab < 0
    while todo.any():
        cur[todo] = F[cur[todo]]
        hit = todo & (lab[cur] >= 0)
        lab[hit] = lab[cur[hit]]; todo &= ~hit
    return lab

res = {"rule": RULE, "cases": {}}
t0 = time.process_time()
for n in range(3, 17):
    F = Ftable(n); N = 1 << n; x = np.arange(N, dtype=np.int64)
    r = {}
    # Lemma 1
    a = np.roll(np.arange(n), 1)
    lhs = np.zeros(N, np.int64)
    for i in range(n):
        xi = (x >> i) & 1; xm = (x >> ((i - 1) % n)) & 1; xp = (x >> ((i + 1) % n)) & 1
        lhs |= ((xp + xm * (1 + xi)) & 1) << i
    r["lemma1_formula_ok"] = bool((lhs == F).all())
    # Lemma 5: all collisions
    order = np.argsort(F, kind="stable"); Fs = F[order]
    same = np.nonzero(Fs[1:] == Fs[:-1])[0]
    r["collision_pairs_adjacent_in_sort"] = int(len(same))
    r["bijective"] = bool(len(np.unique(F)) == N)
    if n % 2 == 0:
        Emask = sum(1 << i for i in range(0, n, 2)); Omask = sum(1 << i for i in range(1, n, 2))
        inE = (x & Omask) == 0; inO = (x & Emask) == 0; M = ~(inE | inO)
        # every preimage class of size > 1 must be a pair of the three stated kinds
        cnt = np.bincount(F, minlength=N)
        r["max_preimages"] = int(cnt.max())
        # all pairs inside every preimage class of size > 1 (first version checked only sorted neighbours)
        bad = 0; npairs = 0
        import itertools
        multi = np.nonzero(cnt > 1)[0]
        pre = {int(v): [] for v in multi}
        for u in np.nonzero(cnt[F] > 1)[0]: pre[int(F[u])].append(int(u))
        for v, us in pre.items():
            for u, w in itertools.combinations(us, 2):
                npairs += 1; d = u ^ w
                ok = (inE[u] and inE[w] and d == Emask) or (inO[u] and inO[w] and d == Omask) or ({u, w} == {Emask, Omask})
                bad += (not ok)
        r["lemma5_pairs_checked"] = npairs
        r["lemma5_violations"] = int(bad)
        r["lemma4_F_M_subset_M"] = bool(M[F[M]].all())
        per = periodic_mask(F)
        r["periodic_states"] = int(per.sum()); r["size_M"] = int(M.sum())
        r["lemma6_M_all_periodic"] = bool(per[M].all())
        pow2 = (n & (n - 1)) == 0
        if pow2:
            r["periodic_equals_M_plus_zero"] = bool(per.sum() == M.sum() + 1 and per[0])
        lab = attractor_labels(F, per)
        cycles = np.unique(lab[per]); r["cycles"] = int(len(cycles))
        # G1 edges and reachability of {0}
        src = []; dst = []
        ps = np.nonzero(per)[0]
        for i in range(n):
            t = lab[ps ^ (1 << i)]; s = lab[ps]; keep = t != s
            src.append(s[keep]); dst.append(t[keep])
        src = np.concatenate(src); dst = np.concatenate(dst)
        E = np.unique(np.stack([src, dst], 1), axis=0)
        r["g1_edges"] = int(len(E))
        r["zero_has_out_edge"] = bool((E[:, 0] == 0).any())
        # backward BFS from cycle {0}
        idx = {int(c): k for k, c in enumerate(cycles)}
        pred = [[] for _ in cycles]
        for s_, d_ in E: pred[idx[int(d_)]].append(idx[int(s_)])
        dist = [-1] * len(cycles); dist[idx[0]] = 0; q = [idx[0]]
        for u in q:
            for w in pred[u]:
                if dist[w] < 0: dist[w] = dist[u] + 1; q.append(w)
        r["cycles_not_reaching_zero"] = int(sum(d < 0 for d in dist))
        r["max_g1_distance_to_zero"] = int(max(dist))
        # forward reachability from {0}: strongly connected iff all reach 0 and 0 reaches all
        succ = [[] for _ in cycles]
        for s_, d_ in E: succ[idx[int(s_)]].append(idx[int(d_)])
        seen = {idx[0]}; q = [idx[0]]
        for u in q:
            for w in succ[u]:
                if w not in seen: seen.add(w); q.append(w)
        r["g1_strongly_connected"] = bool(len(seen) == len(cycles) and all(d >= 0 for d in dist))
        if pow2:
            # Theorem 1(c): bound mu(C) = min over states of min(#even ones, #odd ones)
            pe = np.array([bin(int(v) & Emask).count("1") for v in ps]); po = np.array([bin(int(v) & Omask).count("1") for v in ps])
            mu = {}
            for v, m_ in zip(lab[ps], np.minimum(pe, po)):
                mu[int(v)] = min(mu.get(int(v), 99), int(m_))
            r["theorem1c_distance_le_mu_violations"] = int(sum(dist[idx[c]] > mu[c] for c in mu if c != 0))
    res["cases"][n] = r
res["cpu_seconds"] = round(time.process_time() - t0, 1)
json.dump(res, open(sys.argv[1], "w"), indent=1)
for n, r in res["cases"].items(): print(n, r)
print("cpu", res["cpu_seconds"])
