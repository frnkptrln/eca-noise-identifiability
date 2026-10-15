"""Stage R: locate eps*(f) = argmax_eps rho(f; eps) for every class representative by
golden-section search between the grid neighbours of the grid maximum (dense solves),
and classify the shape of the grid curve.  Writes data/epsilon_star.csv.
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import eca_noise as E
from run_stationary import power_check, CHECK_ITERS, CHECK_TOL

GR = (np.sqrt(5) - 1) / 2


def rho_at(succ, counts, eps):
    pi, res = E.stationary_dense(succ, eps, K=E.kernel_matrix(eps))
    nu = E.expected_code_counts(pi, counts)
    return E.rate_from_nu(nu, eps), nu, pi, res


def main(out="data", tol=5e-4):
    codes = E.neighborhood_codes(); counts = E.code_counts()
    d = pd.read_csv(os.path.join(out, "stationary_rates.csv"))
    z = pd.read_csv(os.path.join(out, "zero_noise_per_rule.csv")).set_index("rule")
    rows = []
    for rule, g in d.groupby("rule"):
        g = g.sort_values("eps")
        eps = g.eps.values; rho = g.rho.values; resolved = g.resolved.values == 1
        # shape of the grid curve (resolved entries only)
        rr = rho[resolved]; ee = eps[resolved]
        diffs = np.sign(np.diff(rr)); diffs = diffs[diffs != 0]
        sign_changes = int((np.diff(diffs) != 0).sum()) if len(diffs) > 1 else 0
        k = int(np.argmax(rr))
        rec = dict(rule=rule, limit_type=z.loc[rule, "limit_type"], n_resolved=int(resolved.sum()),
                   grid_argmax_eps=float(ee[k]), grid_max_rho=float(rr[k]), sign_changes=sign_changes,
                   rho_at_smallest_resolved=float(rr[0]), smallest_resolved_eps=float(ee[0]),
                   rho_ratio_0002_over_0001=float(rho[1] / rho[0]) if rho[0] > 0 else float("inf"))
        succ = E.successor_map(rule, codes=codes)
        if k == 0:
            rec.update(eps_star=float("nan"), rho_star=float("nan"), interior_max=0, refine_resolved=-1, refine_evals=0)
        else:
            lo = ee[k - 1]; hi = ee[k + 1] if k + 1 < len(ee) else 0.5
            a, b = lo, hi
            c = b - GR * (b - a); dd = a + GR * (b - a)
            fc = rho_at(succ, counts, c)[0]; fd = rho_at(succ, counts, dd)[0]; evals = 2
            while (b - a) > tol:
                if fc > fd:
                    b, dd, fd = dd, c, fc
                    c = b - GR * (b - a); fc = rho_at(succ, counts, c)[0]
                else:
                    a, c, fc = c, dd, fd
                    dd = a + GR * (b - a); fd = rho_at(succ, counts, dd)[0]
                evals += 1
            es = (a + b) / 2
            rs, nu, pi, res = rho_at(succ, counts, es)
            worst = 0.0
            for s in (np.full(E.S, 1.0 / E.S), np.eye(E.S)[0], np.eye(E.S)[E.S - 1]):
                dev, it = power_check(succ, es, nu, counts, s, CHECK_ITERS); worst = max(worst, dev)
            rec.update(eps_star=float(es), rho_star=float(rs), interior_max=1,
                       refine_resolved=int(worst < CHECK_TOL), refine_evals=evals + 1,
                       **{f"nu{c}_star": float(nu[c]) for c in range(8)}, argmin_code_star=int(nu.argmin()))
        rows.append(rec)
        print(rule, rec.get("eps_star"), rec.get("rho_star"), rec["limit_type"], "signchg", sign_changes, flush=True)
    fields = sorted({k for r in rows for k in r}, key=lambda s: (s not in rows[0], s))
    with open(os.path.join(out, "epsilon_star.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) + [f for f in fields if f not in rows[0]])
        w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
