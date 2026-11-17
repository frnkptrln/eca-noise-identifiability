"""Order of nu_c(eps) from the stationary law itself (no potentials, no Theorem A), n = 4..8.

pi_eps is computed by GTH elimination (subtraction-free, accurate at small eps in float64) for the kernel
P(y|x) = eps^H(Fx,y) (1-eps)^(n-H(Fx,y)) on all 2^n states. nu_c = sum_x pi(x) n_c(x). The order k_c is
estimated as log(nu_c(e1)/nu_c(e2)) / log(e1/e2) for e1 = 1e-4, e2 = 1e-5 and rounded; the estimate and
the rounding error are recorded. Also: the stationary mass on the cycles of the selected set.

Usage: python stationary.py NMAX  -> out/stationary.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eca import global_map, popcount, Dynamics


def gth(P):
    P = P.copy()
    N = P.shape[0]
    for k in range(N - 1, 0, -1):
        s = P[k, :k].sum()
        P[:k, k] /= s
        P[:k, :k] += np.outer(P[:k, k], P[k, :k])
    pi = np.zeros(N); pi[0] = 1.0
    for k in range(1, N):
        pi[k] = pi[:k] @ P[:k, k]
    return pi / pi.sum()


def code_counts(n):
    xs = np.arange(1 << n)
    cnt = np.zeros((1 << n, 8))
    for i in range(n):
        c = 4 * ((xs >> ((i - 1) % n)) & 1) + 2 * ((xs >> i) & 1) + ((xs >> ((i + 1) % n)) & 1)
        cnt[xs, c] += 1
    return cnt


def stationary(rule, n, eps):
    N = 1 << n
    xs = np.arange(N)
    F = global_map(rule, n, xs)
    H = popcount(F[:, None] ^ xs[None, :])
    P = eps ** H * (1 - eps) ** (n - H)
    return gth(P)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    pots = {}
    if os.path.exists("out/potentials.jsonl"):
        for line in open("out/potentials.jsonl"):
            r = json.loads(line); pots[(r["rule"], r["n"])] = r
    out = []
    e1, e2 = 1e-4, 1e-5
    for n in range(4, nmax + 1):
        cc = code_counts(n)
        for rule in (43, 142):
            p1, p2 = stationary(rule, n, e1), stationary(rule, n, e2)
            nu1, nu2 = p1 @ cc, p2 @ cc
            est = np.log(nu1 / nu2) / np.log(e1 / e2)
            k = np.rint(est).astype(int)
            rec = dict(rule=rule, n=n, k_from_pi=k.tolist(), estimate=[round(float(v), 4) for v in est],
                       max_rounding_error=round(float(np.abs(est - k).max()), 4))
            P = pots.get((rule, n))
            if P:
                sel = np.array(P["selected_states"], dtype=int)
                rec["k_from_potentials"] = P["k"]
                rec["agree"] = rec["k_from_pi"] == P["k"]
                rec["mass_on_selected_cycles_eps1e-5"] = float(p2[sel].sum())
            out.append(rec)
            print(rec, flush=True)
    json.dump(out, open("out/stationary.json", "w"), indent=1)
