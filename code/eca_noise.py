"""Exact computations for "Rule identifiability in elementary cellular automata
under dynamical noise".

All quantities are computed without sampling: the noisy automaton on n cells is a
Markov chain on 2**n states, and every reported number is a stationary law, a
finite-horizon push-forward, or an exact orbit of that chain.

Conventions
-----------
* States are integers 0 .. 2**n-1; bit i (value 2**i) is cell i, indices mod n.
* A rule is an integer 0..255 (Wolfram numbering): the successor of cell i is
  bit  c  of the rule, where  c = 4*x_{i-1} + 2*x_i + x_{i+1}.
* Noise: X_{t+1} = F_f(X_t) XOR Z_t, Z_t i.i.d. Bernoulli(eps) per cell.
"""
from __future__ import annotations

import numpy as np

N = 12
S = 1 << N
CODES = 8


# ----------------------------------------------------------------------------
# state geometry
# ----------------------------------------------------------------------------
def all_bits(n: int = N) -> np.ndarray:
    """(2**n, n) array of cell values for every state."""
    x = np.arange(1 << n, dtype=np.int64)
    return ((x[:, None] >> np.arange(n)) & 1).astype(np.int8)


def neighborhood_codes(n: int = N) -> np.ndarray:
    """(2**n, n) array: neighborhood code 4*x_{i-1}+2*x_i+x_{i+1} at every position."""
    b = all_bits(n).astype(np.int64)
    left = np.roll(b, 1, axis=1)   # x_{i-1}
    right = np.roll(b, -1, axis=1)  # x_{i+1}
    return 4 * left + 2 * b + right


def code_counts(n: int = N) -> np.ndarray:
    """(2**n, 8) array n_c(x): number of positions of state x with neighborhood code c."""
    codes = neighborhood_codes(n)
    counts = np.zeros((1 << n, CODES), dtype=np.int64)
    for c in range(CODES):
        counts[:, c] = (codes == c).sum(axis=1)
    return counts


def successor_map(rule: int, n: int = N, codes: np.ndarray | None = None) -> np.ndarray:
    """(2**n,) array F_f(x) for every state x."""
    if codes is None:
        codes = neighborhood_codes(n)
    out = (rule >> codes) & 1                      # (S, n) successor bits
    return (out << np.arange(n)).sum(axis=1).astype(np.int64)


# ----------------------------------------------------------------------------
# rule symmetries (reflection, complementation)
# ----------------------------------------------------------------------------
def reflect_rule(rule: int) -> int:
    r = 0
    for c in range(8):
        a, b, d = (c >> 2) & 1, (c >> 1) & 1, c & 1
        c_ref = 4 * d + 2 * b + a
        r |= ((rule >> c) & 1) << c_ref
    return r


def complement_rule(rule: int) -> int:
    r = 0
    for c in range(8):
        c_comp = 7 - c
        r |= (1 - ((rule >> c) & 1)) << c_comp
    return r


def rule_class_representatives() -> tuple[list[int], dict[int, int]]:
    """Return the 88 class representatives (minimum rule number) and a map rule -> representative."""
    rep_of: dict[int, int] = {}
    reps: list[int] = []
    for r in range(256):
        orbit = {r, reflect_rule(r), complement_rule(r), reflect_rule(complement_rule(r))}
        m = min(orbit)
        rep_of[r] = m
        if m == r:
            reps.append(r)
    assert len(reps) == 88, len(reps)
    return reps, rep_of


# ----------------------------------------------------------------------------
# noise kernel
# ----------------------------------------------------------------------------
def lam(eps: float) -> float:
    """lambda(eps) = (1-2eps) log((1-eps)/eps), natural log."""
    if eps <= 0 or eps >= 1:
        return float("inf")
    return (1.0 - 2.0 * eps) * np.log((1.0 - eps) / eps)


def kernel_matrix(eps: float, n: int = N) -> np.ndarray:
    """Dense (2**n, 2**n) matrix K[z, y] = eps**H(z,y) (1-eps)**(n-H(z,y))."""
    k1 = np.array([[1.0 - eps, eps], [eps, 1.0 - eps]])
    K = np.array([[1.0]])
    for _ in range(n):
        K = np.kron(k1, K)
    return K


def apply_kernel_rows(M: np.ndarray, eps: float, n: int = N) -> np.ndarray:
    """Return M @ K for M of shape (..., 2**n) using the tensor-product structure (exact)."""
    shape = M.shape
    T = M.reshape(shape[:-1] + (2,) * n)
    for axis in range(T.ndim - n, T.ndim):
        T = (1.0 - eps) * T + eps * np.flip(T, axis=axis)
    return T.reshape(shape)


def push_forward(v: np.ndarray, succ: np.ndarray) -> np.ndarray:
    """(v F)(y) = sum_{x: F(x)=y} v(x) for a vector v."""
    return np.bincount(succ, weights=v, minlength=len(succ))


def transition_matrix(succ: np.ndarray, eps: float, n: int = N, K: np.ndarray | None = None) -> np.ndarray:
    """Dense transition matrix P[x, y] = K[F(x), y]."""
    if K is None:
        K = kernel_matrix(eps, n)
    return K[succ, :]


# ----------------------------------------------------------------------------
# stationary law
# ----------------------------------------------------------------------------
def stationary_dense(succ: np.ndarray, eps: float, n: int = N, K: np.ndarray | None = None,
                     refine_steps: int = 2) -> tuple[np.ndarray, float]:
    """Exact (floating point) stationary law of the chain by a dense linear solve.

    Solves pi (I - P) = 0 with sum(pi) = 1, then applies `refine_steps` exact
    power-iteration steps pi <- pi P (which can only reduce the residual), and
    returns (pi, residual) with residual = ||pi - pi P||_1.
    """
    P = transition_matrix(succ, eps, n, K)
    A = (np.eye(len(succ)) - P).T          # A pi = 0
    A[-1, :] = 1.0                          # replace one (redundant) equation by normalisation
    b = np.zeros(len(succ)); b[-1] = 1.0
    pi = np.linalg.solve(A, b)
    pi = np.maximum(pi, 0.0)
    pi /= pi.sum()
    for _ in range(refine_steps):
        pi = apply_kernel_rows(push_forward(pi, succ), eps, n)
    res = float(np.abs(pi - apply_kernel_rows(push_forward(pi, succ), eps, n)).sum())
    return pi, res


def stationary_power(succ: np.ndarray, eps: float, n: int = N, tol: float = 1e-13,
                     max_iter: int = 2_000_000, pi0: np.ndarray | None = None) -> tuple[np.ndarray, float, int]:
    """Stationary law by power iteration with the fast kernel (independent check)."""
    pi = np.full(len(succ), 1.0 / len(succ)) if pi0 is None else pi0.copy()
    for it in range(1, max_iter + 1):
        new = apply_kernel_rows(push_forward(pi, succ), eps, n)
        res = float(np.abs(new - pi).sum())
        pi = new
        if res < tol:
            return pi, res, it
    return pi, res, max_iter


# ----------------------------------------------------------------------------
# identifiability quantities
# ----------------------------------------------------------------------------
def expected_code_counts(pi: np.ndarray, counts: np.ndarray) -> np.ndarray:
    """nu_c = sum_x pi(x) n_c(x), shape (8,)."""
    return pi @ counts


def rate_from_nu(nu: np.ndarray, eps: float) -> float:
    """rho(f; eps) = lambda(eps) * min_c nu_c.  (Lemma: the hardest alternative is a one-bit neighbour.)"""
    return lam(eps) * float(nu.min())


def evidence_all_alternatives(nu: np.ndarray, rule: int, eps: float) -> np.ndarray:
    """lambda * E_pi[d_{fg}] for every g in 0..255 (g == rule gives 0)."""
    g = np.arange(256)
    diff = ((g[:, None] ^ rule) >> np.arange(8)) & 1     # (256, 8) indicator f != g on code c
    return lam(eps) * (diff @ nu)


# ----------------------------------------------------------------------------
# zero-noise orbits
# ----------------------------------------------------------------------------
def zero_noise_classes(succ: np.ndarray, counts: np.ndarray) -> dict[str, np.ndarray]:
    """For every initial state: transient length, period, tau = transient+period,
    the union N_inf of neighborhood codes along the orbit (as an 8-bit mask), and
    |C_inf| = 2**(8 - |N_inf|).  Also the mask of codes covered by all cycle states.
    """
    S = len(succ)
    mask_state = np.zeros(S, dtype=np.int64)
    for c in range(CODES):
        mask_state |= (counts[:, c] > 0).astype(np.int64) << c

    # cycle detection in the functional graph
    on_cycle = np.zeros(S, dtype=bool)
    color = np.zeros(S, dtype=np.int8)       # 0 unvisited, 1 in progress, 2 done
    dist = np.full(S, -1, dtype=np.int64)    # distance to the cycle (0 on cycle)
    period = np.zeros(S, dtype=np.int64)
    for s0 in range(S):
        if color[s0]:
            continue
        path = []
        s = s0
        while color[s] == 0:
            color[s] = 1
            path.append(s)
            s = succ[s]
        if color[s] == 1:                    # found a new cycle at s
            k = path.index(s)
            cyc = path[k:]
            for v in cyc:
                on_cycle[v] = True
                dist[v] = 0
                period[v] = len(cyc)
            tail = path[:k]
        else:
            tail = path
        # propagate along the tail backwards
        d = dist[s]; p = period[s]
        for v in reversed(tail):
            d += 1
            dist[v] = d
            period[v] = p
        for v in path:
            color[v] = 2

    # union of masks along the orbit: process states in order of decreasing distance
    union = np.zeros(S, dtype=np.int64)
    # first cycles: union over each cycle
    visited = np.zeros(S, dtype=bool)
    for s0 in range(S):
        if on_cycle[s0] and not visited[s0]:
            cyc = [s0]
            visited[s0] = True
            s = succ[s0]
            while s != s0:
                cyc.append(s); visited[s] = True; s = succ[s]
            m = 0
            for v in cyc:
                m |= mask_state[v]
            for v in cyc:
                union[v] = m
    order = np.argsort(dist, kind="stable")
    for v in order:
        if dist[v] > 0:
            union[v] = mask_state[v] | union[succ[v]]
    n_inf = np.array([bin(int(m)).count("1") for m in union], dtype=np.int64)
    cycle_union_mask = 0
    for v in range(S):
        if on_cycle[v]:
            cycle_union_mask |= int(mask_state[v])
    return {
        "transient": dist,
        "period": period,
        "tau": dist + period,
        "N_inf_mask": union,
        "N_inf_size": n_inf,
        "class_size": 2 ** (8 - n_inf),
        "cycle_union_mask": np.array(cycle_union_mask),
        "on_cycle": on_cycle,
    }


# ----------------------------------------------------------------------------
# finite horizon, all initial states at once (adjoint / backward evolution)
# ----------------------------------------------------------------------------
def finite_horizon_cumcounts(succ: np.ndarray, counts: np.ndarray, eps: float,
                             horizons: list[int], n: int = N) -> dict[int, np.ndarray]:
    """For every initial state x0 and every T in `horizons`, the exact
    sum_{t=0}^{T-1} E[n_c(X_t) | X_0 = x0], shape (2**n, 8).

    Uses G_t = P^t counts, computed as G_{t} = (K G_{t-1})[F(.), :]  (K symmetric),
    so each step costs O(8 * n * 2**n) instead of a dense matrix product.
    """
    G = counts.astype(float)
    acc = np.zeros_like(G)
    out: dict[int, np.ndarray] = {}
    T_max = max(horizons)
    for t in range(1, T_max + 1):
        acc += G                       # adds the term for time t-1
        if t in horizons:
            out[t] = acc.copy()
        if t < T_max:
            KG = apply_kernel_rows(G.T, eps, n).T
            G = KG[succ, :]
    return out
