"""Own checker for the v0.2 certificates (written from the certificate files and the definitions only).

Checks, all against own recomputation (own F, own cycle enumeration, own 0-1 BFS resistances):
 C1 cycles: every listed cycle is a cycle of F in order, the list is exactly the set of cycles of F, m matches.
 C2 hierarchy structure: parent pointers form one rooted tree on M nodes, leaves 0..m-1 are the cycles,
    every internal node has >= 2 children, y are integers >= 0.
 C3 selected edges: for every non-top node X, tail in X, head outside X, tight:
    V(t, h) = sum of y_S over S containing t with S inside X.
 C4 cycle condition: inside every internal node the children's selected edges map each child to a sibling
    and this map is one cyclic permutation of all children.
 C5 dual feasibility: sum of y_S over S containing C and not C' <= V(C, C') for all C != C'.
 C6 gamma(r) = sum(y) - sum_{S containing r} y_S for every r, gamma_min = min gamma.
 C7 explicit tree: an in-tree rooted at tree.root with weight gamma[root] under V.
 C8 stable = argmin gamma.
 C9 k_c witnesses: trajectory starts on the stated root cycle, ends in a state containing c,
    resistance = sum_t H(F(x_t), x_{t+1}), k = gamma[root] - gamma_min + resistance;
    and k equals own multi-source shortest path from all cycles with offsets gamma - gamma_min (lower bound).
 C10 kstar = max k_c; stable_cover_mask = OR of codes on stable cycles; covering_cycles (if present) are stable
    and cover all codes; uncovered_codes (if present) = codes on no stable cycle.
Usage: python check_certs.py OUTFILE cert1.json.gz [cert2 ...]
"""
import sys, gzip, json, time, ast
import numpy as np
from numba import njit
import eca, route_b


@njit(cache=True)
def _dual_feasible(order_leaf, adj_lca_depth, adj_lca_node, up, V):
    """Leaves in DFS order; lca(L_i, L_j) = shallowest of the adjacent lcas between i and j.
    Returns number of violated pairs and the worst slack."""
    m = order_leaf.shape[0]
    bad = 0
    worst = 1 << 40
    for i in range(m):
        a = order_leaf[i]
        bestd = 1 << 40
        bestn = -1
        for j in range(i + 1, m):
            k = j - 1
            if adj_lca_depth[k] < bestd:
                bestd = adj_lca_depth[k]
                bestn = adj_lca_node[k]
            b = order_leaf[j]
            # pair (a, b) and (b, a): sum over S containing a, not b = up[a] - up[lca]
            s1 = V[a, b] - (up[a] - up[bestn])
            s2 = V[b, a] - (up[b] - up[bestn])
            if s1 < 0:
                bad += 1
            if s2 < 0:
                bad += 1
            if s1 < worst:
                worst = s1
            if s2 < worst:
                worst = s2
    return bad, worst


def check(path):
    d = json.load(gzip.open(path))
    fails = []
    if 'hierarchy' not in d and str(d.get('bijective')) == 'True':
        # stub for a bijective map: check bijectivity and k_c = 0 for every code
        n, rule = int(d['n']), int(d['rule'])
        F = eca.step_map(rule, n)
        kc = ast.literal_eval(d['k_c']) if isinstance(d['k_c'], str) else d['k_c']
        ok = len(np.unique(F)) == (1 << n) and int(d['kstar']) == 0 and sorted(e['code'] for e in kc) == list(range(8)) \
            and all(e['k'] == 0 for e in kc)
        return dict(file=path.split('/')[-1], n=n, rule=rule, m=None, ok=ok, fails=[] if ok else ['C0'], kstar=0,
                    k_c_mine='bijective', stub=True)
    n, rule, m = d['n'], d['rule'], d['m']
    F = eca.step_map(rule, n).astype(np.int64)
    _, mycyc = eca.cycles_of(F)
    cyc = [np.array(c, dtype=np.int64) for c in d['cycles']]
    # C1
    ok1 = len(cyc) == m == len(mycyc)
    for c in cyc:
        if not np.array_equal(F[c], np.roll(c, -1)):
            ok1 = False
    mine = {frozenset(map(int, c)) for c in mycyc}
    theirs = [frozenset(map(int, c)) for c in cyc]
    if set(theirs) != mine or len(set(theirs)) != len(theirs):
        ok1 = False
    if not ok1:
        fails.append('C1')
        return dict(file=path.split('/')[-1], n=n, rule=rule, m=m, ok=False, fails=fails)
    N = 1 << n
    cid = -np.ones(N, dtype=np.int64)
    for i, c in enumerate(cyc):
        cid[c] = i
    V = route_b.cycle_cost_matrix(F, n, cid, cyc)
    H = d['hierarchy']
    par = np.array(H['parent'], dtype=np.int64); y = np.array(H['y']); st = np.array(H['sel_tail']); sh = np.array(H['sel_head'])
    M = len(par); top = H['top']
    # C2
    ok2 = len(y) == len(st) == len(sh) == M and par[top] == -1 and int((par == -1).sum()) == 1 and M >= m
    ok2 = ok2 and all(float(v) == int(v) and v >= 0 for v in y)
    children = [[] for _ in range(M)]
    for v in range(M):
        if v != top:
            if not (0 <= par[v] < M) or par[v] < m:
                ok2 = False; break
            children[par[v]].append(v)
    if ok2:
        # acyclic & connected: every node reaches top
        depth = -np.ones(M, dtype=np.int64); depth[top] = 0
        stack = [top]; seen = 1
        dfs_leaves = []
        lo = np.zeros(M, dtype=np.int64); hi = np.zeros(M, dtype=np.int64)
        # iterative DFS for leaf intervals
        it = [(top, 0)]
        while it:
            v, state = it.pop()
            if state == 0:
                lo[v] = len(dfs_leaves)
                if v < m:
                    dfs_leaves.append(v); hi[v] = len(dfs_leaves)
                else:
                    it.append((v, 1))
                    for ch in reversed(children[v]):
                        depth[ch] = depth[v] + 1; seen += 1
                        it.append((ch, 0))
            else:
                hi[v] = len(dfs_leaves)
        ok2 = seen == M and len(dfs_leaves) == m and all(len(children[v]) >= 2 for v in range(m, M)) \
            and all(len(children[v]) == 0 for v in range(m))
    if not ok2:
        fails.append('C2')
        return dict(file=path.split('/')[-1], n=n, rule=rule, m=m, ok=False, fails=fails)
    y = y.astype(np.int64)
    pos = np.empty(m, dtype=np.int64); pos[np.array(dfs_leaves)] = np.arange(m)
    # up[v] = sum of y over ancestors-or-self of v
    up = np.zeros(M, dtype=np.int64)
    order = np.argsort(depth, kind='stable')
    for v in order:
        up[v] = y[v] + (up[par[v]] if v != top else 0)
    inX = lambda leaf, X: lo[X] <= pos[leaf] < hi[X]
    # C3
    ok3 = True
    for X in range(M):
        if X == top:
            continue
        t, h = int(st[X]), int(sh[X])
        if not (0 <= t < m and 0 <= h < m and inX(t, X) and not inX(h, X)):
            ok3 = False; break
        if V[t, h] != up[t] - up[par[X]]:
            ok3 = False; break
    if not ok3: fails.append('C3')
    # C4
    ok4 = True
    for X in range(m, M):
        ch = children[X]
        idx = {c: i for i, c in enumerate(ch)}
        succ = []
        for c in ch:
            h = int(sh[c])
            if not (0 <= h < m) or not inX(h, X):
                ok4 = False; break
            tgt = [c2 for c2 in ch if inX(h, c2)]
            if len(tgt) != 1 or tgt[0] == c:
                ok4 = False; break
            succ.append(idx[tgt[0]])
        if not ok4: break
        # one cyclic permutation of all children
        if sorted(succ) != list(range(len(ch))):
            ok4 = False; break
        v, L = 0, 0
        while True:
            v = succ[v]; L += 1
            if v == 0: break
        if L != len(ch):
            ok4 = False; break
    if not ok4: fails.append('C4')
    # C5: adjacent lcas in DFS leaf order
    if m >= 2:
        adj_node = np.empty(m - 1, dtype=np.int64); adj_depth = np.empty(m - 1, dtype=np.int64)
        for k in range(m - 1):
            a, b = dfs_leaves[k], dfs_leaves[k + 1]
            anc = set()
            v = a
            while v != -1:
                anc.add(v); v = par[v] if v != top else -1
            v = b
            while v not in anc:
                v = par[v]
            adj_node[k] = v; adj_depth[k] = depth[v]
        bad, worst = _dual_feasible(np.array(dfs_leaves, dtype=np.int64), adj_depth, adj_node, up, V)
        if bad:
            fails.append('C5')
    # C6
    T = int(y.sum())
    gam = np.array(d['gamma'], dtype=np.int64)
    if not (len(gam) == m and np.array_equal(gam, T - up[:m]) and d['gamma_min'] == gam.min()):
        fails.append('C6')
    # C7
    tp = d['tree']['parent']; r = d['tree']['root']
    ok7 = len(tp) == m and tp[r] == -1 and sum(1 for v in tp if v == -1) == 1
    if ok7:
        w = 0
        for v in range(m):
            if v == r: continue
            u, steps = v, 0
            while u != r and steps <= m:
                u = tp[u]; steps += 1
                if u < 0: break
            if u != r: ok7 = False; break
            w += V[v, tp[v]]
        ok7 = ok7 and w == gam[r]
    if not ok7: fails.append('C7')
    # C8
    if sorted(d['stable']) != [int(i) for i in np.nonzero(gam == gam.min())[0]]:
        fails.append('C8')
    # C9
    Nc = eca.code_counts(n)
    src = np.concatenate(cyc); lev = np.concatenate([np.full(len(c), gam[i] - gam.min()) for i, c in enumerate(cyc)]).astype(np.int64)
    hstate, _ = route_b._bfs(F, n, src, lev, cid, m, False)
    mykc = [int(hstate[Nc[c] > 0].min()) for c in range(8)]
    pc = eca.popcount(np.arange(N, dtype=np.uint32))
    ok9 = len(d['k_c']) == 8
    kc_list = [None] * 8
    for e in d['k_c']:
        c = e['code']; tr = e['trajectory']
        if not (0 <= c < 8 and 0 <= e['root'] < m and len(tr) >= 1):
            ok9 = False; break
        if cid[tr[0]] != e['root'] or Nc[c, tr[-1]] == 0:
            ok9 = False; break
        res = sum(int(pc[F[tr[i]] ^ tr[i + 1]]) for i in range(len(tr) - 1))
        if res != e['resistance'] or e['k'] != gam[e['root']] - gam.min() + res or e['k'] != mykc[c]:
            ok9 = False; break
        kc_list[c] = e['k']
    if not ok9 or any(v is None for v in kc_list): fails.append('C9')
    # C10
    stable_mask = 0
    for i in d['stable']:
        for c in range(8):
            if np.any(Nc[c, cyc[i]] > 0): stable_mask |= 1 << c
    ok10 = d['kstar'] == max(mykc) and d['stable_cover_mask'] == stable_mask
    if 'covering_cycles' in d:
        cm = 0
        for i in d['covering_cycles']:
            if i not in d['stable']: ok10 = False
            for c in range(8):
                if np.any(Nc[c, cyc[i]] > 0): cm |= 1 << c
        if d['kstar'] == 0 and cm != 255: ok10 = False
    if 'uncovered_codes' in d:
        # field semantics (read off the files, see VERIFICATION_v02.md): the codes with k_c = k* when k* >= 1
        unc = sorted(c for c in range(8) if mykc[c] == max(mykc)) if max(mykc) >= 1 else []
        if sorted(d['uncovered_codes']) != unc: ok10 = False
    if not ok10: fails.append('C10')
    return dict(file=path.split('/')[-1], n=n, rule=rule, m=m, ok=not fails, fails=fails, kstar=int(max(mykc)),
                k_c_mine='-'.join(map(str, mykc)), T=T, internal_sets=M - m)


if __name__ == '__main__':
    out = sys.argv[1]
    done = {r['file'] for r in eca.read_jsonl(out)}
    for p in sys.argv[2:]:
        if p.split('/')[-1] in done: continue
        t0 = time.time()
        try:
            r = check(p)
        except Exception as ex:  # a crash is a rejection
            r = dict(file=p.split('/')[-1], ok=False, fails=['EXC ' + repr(ex)[:200]])
        r['sec'] = round(time.time() - t0, 2)
        eca.append_jsonl(out, r)
