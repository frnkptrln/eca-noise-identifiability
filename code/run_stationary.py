"""Stage S: stationary laws, expected neighborhood counts nu_c, and identifiability rates
rho(f; eps) = lambda(eps) * min_c nu_c for every rule on the eps grid.

Usage: python3 run_stationary.py [--rules reps|rest|all] [--out data/] [--check yes|no]
Writes <out>/stationary_rates.csv (one row per rule x eps) incrementally; resumable.

Each entry is computed by a dense linear solve (exact up to floating point) and, with
--check yes, verified by power iteration from three initial laws (uniform, delta at the
all-zero state, delta at the all-one state). An entry is 'resolved' when all three agree
with the dense solve to CHECK_TOL in every nu_c; disagreement signals metastability (the
chain mixes too slowly for the stationary law to be resolved numerically at that eps).
"""
import sys, os, time, argparse, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca_noise as E

EPS_GRID = [0.001, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
CHECK_ITERS = 50_000
CHECK_TOL = 1e-6      # max |nu_start - nu_dense| over codes, all three starts


def power_check(succ, eps, nu_dense, counts, pi0, max_iter, every=50, stop_tol=1e-9):
    """Power iteration from pi0; every `every` steps compare nu with the dense solution.
    Returns (max |nu_power - nu_dense|, iterations used)."""
    pi = pi0.copy()
    for it in range(1, max_iter + 1):
        pi = E.apply_kernel_rows(E.push_forward(pi, succ), eps)
        if it % every == 0:
            d = float(np.abs(pi @ counts - nu_dense).max())
            if d < stop_tol:
                return d, it
    return float(np.abs(pi @ counts - nu_dense).max()), max_iter


def solve_entry(rule, eps, succ, counts, K, check=True):
    pi, res = E.stationary_dense(succ, eps, K=K)
    nu = E.expected_code_counts(pi, counts)
    rec = dict(rule=rule, eps=eps, residual=res, min_pi=float(pi.min()))
    for c in range(8):
        rec[f"nu{c}"] = float(nu[c])
    rec["nu_min"] = float(nu.min()); rec["argmin_code"] = int(nu.argmin())
    rec["lambda"] = E.lam(eps); rec["rho"] = E.rate_from_nu(nu, eps)
    if check:
        starts = {"uniform": np.full(E.S, 1.0 / E.S), "zero": np.eye(E.S)[0], "ones": np.eye(E.S)[E.S - 1]}
        worst = 0.0; its = {}
        for name, s in starts.items():
            d, it = power_check(succ, eps, nu, counts, s, CHECK_ITERS)
            worst = max(worst, d); its[name] = it
        rec["check_max_dev"] = worst; rec["check_iters"] = max(its.values())
        rec["resolved"] = int(worst < CHECK_TOL)
    else:
        rec["check_max_dev"] = float("nan"); rec["check_iters"] = -1; rec["resolved"] = -1
    return rec, pi


FIELDS = ["rule", "eps", "lambda"] + [f"nu{c}" for c in range(8)] + \
    ["nu_min", "argmin_code", "rho", "residual", "min_pi", "check_max_dev", "check_iters", "resolved"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rules", default="reps"); ap.add_argument("--out", default="data"); ap.add_argument("--check", default="yes")
    ap.add_argument("--grid", default=None, help="comma-separated eps values (default: EPS_GRID)")
    a = ap.parse_args()
    grid = EPS_GRID if a.grid is None else [float(v) for v in a.grid.split(",")]
    codes = E.neighborhood_codes(); counts = E.code_counts()
    reps, rep_of = E.rule_class_representatives()
    if a.rules == "reps":
        rules = reps
    elif a.rules == "rest":
        rules = [r for r in range(256) if r not in reps]
    else:
        rules = list(range(256))
    fn = os.path.join(a.out, "stationary_rates.csv")
    exists = os.path.exists(fn)
    done = set()
    if exists:
        with open(fn) as fh:
            for row in csv.DictReader(fh):
                done.add((int(row["rule"]), float(row["eps"])))
    fh = open(fn, "a", newline=""); w = csv.DictWriter(fh, fieldnames=FIELDS)
    if not exists:
        w.writeheader()
    Ks = {}
    t0 = time.time()
    for i, rule in enumerate(rules):
        succ = E.successor_map(rule, codes=codes)
        for eps in grid:
            if (rule, eps) in done:
                continue
            if eps not in Ks:
                Ks[eps] = E.kernel_matrix(eps)
            rec, _ = solve_entry(rule, eps, succ, counts, Ks[eps], check=(a.check == "yes"))
            w.writerow({k: rec[k] for k in FIELDS}); fh.flush()
        print(f"[{i+1}/{len(rules)}] rule {rule} done at {time.time()-t0:.0f}s", flush=True)
    fh.close()


if __name__ == "__main__":
    main()
