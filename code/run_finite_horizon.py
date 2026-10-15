"""Stage T: finite-horizon evidence margins m_T(f; x0, eps) = lambda(eps) * min_c sum_{t<T} E[n_c(X_t) | x0]
for all 256 rules, all 4096 initial states, eps in EPS_T and T in HORIZONS (exact, adjoint evolution).

Writes
  data/finite_horizon_per_rule.csv      : per (rule, eps, T) summaries over x0
  data/finite_horizon_per_state.csv.gz  : per (rule, x0): m_T for T=32 at every eps in EPS_T, plus the eps=0 class size
"""
import sys, os, csv, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca_noise as E

EPS_T = [0.005, 0.01, 0.02, 0.05, 0.1, 0.2]
HORIZONS = [8, 16, 32, 64]
T_STORE = 32
THRESH = np.log(100.0)     # evidence threshold used for the 'fraction above' summaries


def main(out="data"):
    codes = E.neighborhood_codes(); counts = E.code_counts()
    fh_rule = open(os.path.join(out, "finite_horizon_per_rule.csv"), "w", newline="")
    wr = csv.writer(fh_rule)
    wr.writerow(["rule", "eps", "T", "lambda", "m_min", "m_q10", "m_median", "m_mean", "m_max",
                 "frac_m_above_ln100", "frac_m_zero_class_gt1", "m_median_class_gt1", "m_median_class_eq1"])
    fh_state = gzip.open(os.path.join(out, "finite_horizon_per_state.csv.gz"), "wt", newline="")
    ws = csv.writer(fh_state)
    ws.writerow(["rule", "x0", "class_size_eps0"] + [f"m32_eps{e}" for e in EPS_T])
    for rule in range(256):
        succ = E.successor_map(rule, codes=codes)
        z = E.zero_noise_classes(succ, counts)
        cls = z["class_size"]
        store = {}
        for eps in EPS_T:
            cum = E.finite_horizon_cumcounts(succ, counts, eps, HORIZONS)
            lam = E.lam(eps)
            for T in HORIZONS:
                m = lam * cum[T].min(axis=1)
                gt1 = cls > 1
                wr.writerow([rule, eps, T, lam, m.min(), np.quantile(m, 0.1), np.median(m), m.mean(), m.max(),
                             float((m >= THRESH).mean()),
                             float((m[gt1] >= THRESH).mean()) if gt1.any() else float("nan"),
                             float(np.median(m[gt1])) if gt1.any() else float("nan"),
                             float(np.median(m[~gt1])) if (~gt1).any() else float("nan")])
                if T == T_STORE:
                    store[eps] = m
        for x0 in range(E.S):
            ws.writerow([rule, x0, int(cls[x0])] + [f"{store[e][x0]:.6g}" for e in EPS_T])
        fh_rule.flush()
        print(f"rule {rule} done", flush=True)
    fh_rule.close(); fh_state.close()


if __name__ == "__main__":
    main()
