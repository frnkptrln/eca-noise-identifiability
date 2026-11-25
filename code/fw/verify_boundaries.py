"""Independent check of the wall solver: high-precision stationary laws (GTH, subtraction-free, as in
verify_stationary.py) from the definitions, for ALL 256 rules (not only class representatives, so the
reflection symmetry is tested too) at n = nmin..nmax under the given boundary.

The transition matrix and the code counts are built here from an explicitly padded row (wall cells -1 and
n), independent of fwlib. Observed order of pi(x) and of nu_c = slope log10(pi(10^-a)/pi(10^-(a+1))) between
the two smallest noise levels; compared with (i) the solver's predicted order of every state
(orders.state_orders on fwlib.classify(..., boundary)), and (ii) k_c from fwlib.classify. A pair passes if all
slopes are within TOL of the predicted integers. Output: data/boundaries/verify_{b}_gth.csv.

Usage: python3 verify_boundaries.py --nmin 4 --nmax 8 --boundary null --workers 2
"""
import argparse, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd

EPS = [10.0 ** (-a) for a in (11, 12)]   # slope between 1e-11 and 1e-12 (at 1e-8/1e-9 rule 238/252, n = 9, deviates by 7e-3: large second-order coefficient, converging x10 per decade)
TOL = 1e-3
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")


def gth(P):
    P = np.array(P, dtype=np.float64)
    N = len(P)
    for k in range(N - 1, 0, -1):
        s = P[k, :k].sum()
        P[:k, k] /= s
        P[:k, :k] += np.outer(P[:k, k], P[k, :k])
    x = np.zeros(N); x[0] = 1.0
    for j in range(1, N):
        x[j] = x[:j] @ P[:j, j]
    return x / x.sum()


def padded(x, n, boundary):
    cells = [(x >> i) & 1 for i in range(n)]
    wl = {"null": 0, "one": 1, "reflect": cells[0]}[boundary]
    wr = {"null": 0, "one": 1, "reflect": cells[-1]}[boundary]
    return [wl] + cells + [wr]


def definitions(rule, n, boundary):
    S = 1 << n
    F = np.zeros(S, dtype=np.int64); cnt = np.zeros((S, 8), dtype=np.int64)
    for x in range(S):
        w = padded(x, n, boundary)
        y = 0
        for i in range(n):
            c = 4 * w[i] + 2 * w[i + 1] + w[i + 2]
            cnt[x, c] += 1
            y |= ((rule >> c) & 1) << i
        F[x] = y
    return F, cnt


def work(args):
    rule, n, boundary = args
    import fwlib, orders
    t0 = time.time()
    F, cnt = definitions(rule, n, boundary)
    S = 1 << n
    H = np.array([[bin(int(F[x]) ^ y).count("1") for y in range(S)] for x in range(S)])
    pis = np.array([gth(e ** H * (1 - e) ** (n - H)) for e in EPS])
    nus = pis @ cnt
    sl_pi = np.log10(pis[-2] / pis[-1]); sl_nu = np.log10(nus[-2] / nus[-1])
    assert np.array_equal(F, fwlib.succ_map(rule, n, boundary))
    if fwlib.is_bijective(F):
        pred_pi = np.zeros(S); pred_k = np.zeros(8)
    else:
        res = fwlib.classify(rule, n, keep_dists=True, boundary=boundary)
        pred_pi = orders.state_orders(res); pred_k = res["k_c"]
    e_pi = float(np.abs(sl_pi - pred_pi).max()); e_nu = float(np.abs(sl_nu - pred_k).max())
    return dict(boundary=boundary, n=n, rule=rule, max_dev_state=round(e_pi, 6), max_dev_code=round(e_nu, 6),
                ok=int(e_pi < TOL and e_nu < TOL), kstar=int(max(pred_k)), seconds=round(time.time() - t0, 2))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=4); ap.add_argument("--nmax", type=int, default=8)
    ap.add_argument("--boundary", default="null"); ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    assert a.workers <= 2
    jobs = [(r, n, a.boundary) for n in range(a.nmin, a.nmax + 1) for r in range(256)]
    from multiprocessing import Pool
    t0 = time.time()
    with Pool(a.workers) as pool:
        rows = list(pool.imap_unordered(work, jobs, chunksize=8))
    df = pd.DataFrame(rows).sort_values(["n", "rule"])
    out = os.path.join(DATA, f"verify_{a.boundary}_gth.csv")
    df.to_csv(out, index=False)
    print(f"{len(df)} pairs, {int(df.ok.sum())} pass, max deviation state {df.max_dev_state.max():.2e} "
          f"code {df.max_dev_code.max():.2e}, wall {time.time()-t0:.0f}s")


if __name__ == "__main__":
    main()
