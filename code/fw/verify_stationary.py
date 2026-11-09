"""Verifier (a): high-precision stationary laws reproduce the predicted orders ord pi_eps(x).

For each rule (all 256) and ring size n, the stationary law at eps = 1e-3, ..., 1e-12 is computed with
the GTH algorithm (Grassmann, Taksar and Heyman 1985), which is subtraction-free and computes every
entry with small relative error (O'Cinneide 1993), so entries of order 1e-100 are as accurate as
entries of order 1. The transition matrix is built here from the definition (independent of fwlib).
The observed order of state x is the slope log10(pi(10^-a) / pi(10^-(a+1))) between the two smallest
noise levels; it must be within TOL of the predicted integer for every state, and so must the order of
every nu_c.

Stage A (this file, expensive, independent of the solver): GTH slopes for every state and every
nu_c, cached as data/cache/gth/n{n}_r{rule}.npz (written atomically; existing files are skipped, so
an interrupted run resumes to the same cache). Stage B (verify_orders.py) compares the cache with the
current solver.

Usage: python3 verify_stationary.py --nmin 3 --nmax 11 [--workers 11]
"""
import argparse, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np

EPS = [10.0 ** (-a) for a in range(3, 13)]
TOL = 1e-3


def gth(P):
    """Stationary law of an irreducible stochastic matrix by GTH elimination."""
    P = np.array(P, dtype=np.float64)
    N = len(P)
    for k in range(N - 1, 0, -1):
        s = P[k, :k].sum()
        P[:k, k] /= s
        P[:k, :k] += np.outer(P[:k, k], P[k, :k])
    x = np.zeros(N)
    x[0] = 1.0
    for j in range(1, N):
        x[j] = x[:j] @ P[:j, j]
    return x / x.sum()


def succ_def(rule, n):
    S = 1 << n
    out = np.zeros(S, dtype=np.int64)
    for x in range(S):
        y = 0
        for i in range(n):
            c = 4 * ((x >> ((i - 1) % n)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % n)) & 1)
            y |= ((rule >> c) & 1) << i
        out[x] = y
    return out


def counts_def(n):
    S = 1 << n
    cnt = np.zeros((S, 8), dtype=np.int64)
    for x in range(S):
        for i in range(n):
            c = 4 * ((x >> ((i - 1) % n)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % n)) & 1)
            cnt[x, c] += 1
    return cnt


def popcount(a):
    a = a.copy(); c = np.zeros_like(a)
    while a.any():
        c += a & 1; a >>= 1
    return c


def observed_orders(rule, n):
    F = succ_def(rule, n)
    S = 1 << n
    H = popcount(F[:, None] ^ np.arange(S)[None, :])
    cnt = counts_def(n)
    pis = []
    for e in EPS:
        P = e ** H * (1 - e) ** (n - H)
        pis.append(gth(P))
    pis = np.array(pis)                            # (len(EPS), S)
    nus = pis @ cnt                                # (len(EPS), 8)
    sl_pi = np.log10(pis[:-1] / pis[1:])           # slopes between consecutive decades
    sl_nu = np.log10(nus[:-1] / nus[1:])
    return sl_pi, sl_nu


CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "cache", "gth")


def cache_path(rule, n):
    return os.path.join(CACHE, f"n{n}_r{rule}.npz")


def work(args):
    rule, n = args
    t0 = time.time()
    sl_pi, sl_nu = observed_orders(rule, n)
    fn = cache_path(rule, n)
    tmp = fn + ".tmp.npz"
    np.savez(tmp, sl_pi=sl_pi[-2:], sl_nu=sl_nu[-2:], eps=np.array(EPS))
    with open(tmp, "rb") as fh:
        os.fsync(fh.fileno())
    os.replace(tmp, fn)
    return rule, n, time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=3); ap.add_argument("--nmax", type=int, default=11)
    ap.add_argument("--workers", type=int, default=11)
    a = ap.parse_args()
    os.makedirs(CACHE, exist_ok=True)
    jobs = [(r, n) for n in range(a.nmax, a.nmin - 1, -1) for r in range(256) if not os.path.exists(cache_path(r, n))]
    print(f"{len(jobs)} GTH jobs to run", flush=True)
    from multiprocessing import Pool
    t0 = time.time(); tot = 0.0
    with Pool(a.workers) as pool:
        for i, (r, n, dt) in enumerate(pool.imap_unordered(work, jobs)):
            tot += dt
            if (i + 1) % 128 == 0:
                print(f"{i+1}/{len(jobs)} wall {time.time()-t0:.0f}s cpu {tot:.0f}s", flush=True)
    print(f"done wall {time.time()-t0:.0f}s cpu {tot:.0f}s", flush=True)


if __name__ == "__main__":
    main()
