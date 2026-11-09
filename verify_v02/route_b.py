"""Route (b): small-noise orders from minimum resistances and minimum in-trees.

Resistance of a step x -> y: r(x, y) = Hamming(F(x), y) (P(x,y) = eps^r (1-eps)^(n-r)).
Path costs are computed in the graph G with edges u -> F(u) (cost 0) and u -> u xor e_i (cost 1);
a path from a cycle state in G has the same minimal cost as the cheapest noisy trajectory.

1. V[i, j] = minimal path cost from cycle K_i to cycle K_j (0-1 BFS from all states of K_i).
2. Cycle orders: tropical GTH on V = minimum in-tree weight rooted at each cycle, minus the minimum
   (tree theorem + no cancellation; validated against the full 2^n-state tropical GTH for n <= 12).
3. All states: ord pi(x) = min_y [ord pi(y) + r(y, x)] (pi = pi P, all terms positive), whose solution
   is the multi-source shortest path from the cycle states with initial values from step 2.
4. k_c = min over states x containing code c of ord pi(x);  k* = max_c k_c.
"""
import numpy as np
from numba import njit
import eca, gth

BIG = 1 << 30


@njit(cache=True)
def _bfs(F, n, src_nodes, src_level, cid, m, stop_when_all_cycles):
    N = F.shape[0]
    dist = np.full(N, BIG, dtype=np.int64)
    done = np.zeros(N, dtype=np.bool_)
    reach = np.full(m, BIG, dtype=np.int64)
    nreached = 0
    order = np.argsort(src_level)
    sp = 0
    stack = np.empty(N + 1, dtype=np.int64)
    nxt = np.empty(N + len(src_nodes) + 1, dtype=np.int64)
    nn = 0
    d = 0
    remaining = True
    while remaining:
        top = 0
        # tentative nodes at level d from the previous level's flips
        for t in range(nn):
            u = nxt[t]
            if not done[u] and dist[u] == d:
                stack[top] = u; top += 1
        nn = 0
        while sp < len(order) and src_level[order[sp]] == d:
            u = src_nodes[order[sp]]; sp += 1
            if dist[u] > d:
                dist[u] = d
            if not done[u]:
                stack[top] = u; top += 1
        while top > 0:
            top -= 1
            u = stack[top]
            if done[u]:
                continue
            done[u] = True
            c = cid[u]
            if c >= 0 and reach[c] == BIG:
                reach[c] = d
                nreached += 1
            v = F[u]
            if dist[v] > d:
                dist[v] = d
                stack[top] = v; top += 1
            for i in range(n):
                w = u ^ (1 << i)
                if dist[w] > d + 1:
                    dist[w] = d + 1
                    nxt[nn] = w; nn += 1
        if stop_when_all_cycles and nreached == m:
            break
        remaining = (nn > 0) or (sp < len(order))
        d += 1
    return dist, reach


def cycle_structure(rule, n):
    F = eca.step_map(rule, n).astype(np.int64)
    cid, cycles = eca.cycles_of(F)
    return F, cid, cycles


def cycle_cost_matrix(F, n, cid, cycles):
    m = len(cycles)
    V = np.zeros((m, m), dtype=np.int64)
    for i, K in enumerate(cycles):
        _, reach = _bfs(F, n, K.astype(np.int64), np.zeros(len(K), np.int64), cid, m, True)
        V[i] = reach
    return V


def orders_route_b(rule, n, N_codes=None, return_states=False):
    F, cid, cycles = cycle_structure(rule, n)
    m = len(cycles)
    V = cycle_cost_matrix(F, n, cid, cycles)
    if m == 1:
        hc = np.zeros(1, dtype=np.int64)
    else:
        hc = gth.gth_tropical(V)
    src = np.concatenate(cycles).astype(np.int64)
    lev = np.concatenate([np.full(len(K), hc[i]) for i, K in enumerate(cycles)]).astype(np.int64)
    h, _ = _bfs(F, n, src, lev, cid, m, False)
    # consistency: the shortest-path solution must not lower a cycle state's order
    consistent = bool(np.all(h[src] == lev))
    if N_codes is None:
        N_codes = eca.code_counts(n)
    k = [int(h[N_codes[c] > 0].min()) for c in range(8)]
    res = dict(rule=int(rule), n=int(n), m_cycles=int(m), k_c=k, k_star=int(max(k)),
               cycle_orders=[int(v) for v in hc], cycle_lengths=[int(len(K)) for K in cycles],
               cycle_min_state=[int(K.min()) for K in cycles], consistent=consistent,
               max_h=int(h.max()), argmin_codes=[c for c in range(8) if k[c] == max(k)])
    if return_states:
        return res, h, V
    return res


def full_tropical_orders(rule, n):
    """Validation route: tropical GTH on the full 2^n chain with W[x,y] = Hamming(F(x), y)."""
    F = eca.step_map(rule, n).astype(np.uint32)
    N = 1 << n
    ys = np.arange(N, dtype=np.uint32)
    W = np.empty((N, N), dtype=np.int64)
    pc = eca.popcount(ys)  # popcount table
    for x in range(N):
        W[x] = pc[ys ^ F[x]]
    return gth.gth_tropical(W)
