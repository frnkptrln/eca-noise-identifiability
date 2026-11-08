"""Verifier (a), stage B: compare cached GTH slopes (verify_stationary.py) with the solver's
predicted orders ord pi_eps(x) for every state, and with k_c for every code.

Output: data/fw_verify_orders.csv, one row per (n, rule): states, largest |slope - predicted order|
at the smallest pair of noise levels (1e-11, 1e-12) and at the pair before, the same for nu_c,
predicted and observed k_c strings, ok flag (all deviations < TOL)."""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, orders
from verify_stationary import cache_path, TOL

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")


def compare(rule, n):
    z = np.load(cache_path(rule, n))
    sl_pi, sl_nu = z["sl_pi"], z["sl_nu"]
    res = fwlib.classify(rule, n, keep_dists=True)
    ordp = orders.state_orders(res)
    k_c = res["k_c"]
    return dict(n=n, rule=rule, states=1 << n, cycles=res["m"],
                max_dev_pi=float(np.abs(sl_pi[-1] - ordp).max()),
                max_dev_pi_prev=float(np.abs(sl_pi[-2] - ordp).max()),
                max_dev_nu=float(np.abs(sl_nu[-1] - k_c).max()),
                max_ord=int(ordp.max()),
                k_c_pred="-".join(str(int(v)) for v in k_c),
                k_c_obs="-".join(str(int(np.rint(v))) for v in sl_nu[-1]),
                kstar_pred=int(res["kstar"]), kstar_obs=int(np.rint(sl_nu[-1].max())),
                ok=int(np.abs(sl_pi[-1] - ordp).max() < TOL and np.abs(sl_nu[-1] - k_c).max() < TOL))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=3); ap.add_argument("--nmax", type=int, default=11)
    a = ap.parse_args()
    rows = [compare(r, n) for n in range(a.nmin, a.nmax + 1) for r in range(256)]
    df = pd.DataFrame(rows)
    df.to_csv(os.path.join(OUT, "fw_verify_orders.csv"), index=False)
    print("rows", len(df), "failures", int((df.ok == 0).sum()),
          "max dev pi", df.max_dev_pi.max(), "max dev nu", df.max_dev_nu.max())


if __name__ == "__main__":
    main()
