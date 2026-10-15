"""Stage M (boundary check): generators outside the family.  Three radius-2 rules are run
through the same chain, and scored by the radius-1 observer:

  * apparent identifiability rate within R:  lambda * min_c |a_{c,1} - a_{c,0}|
    (rate at which the posterior over the 256 radius-1 rules concentrates on the best one, g*)
  * misfit evidence rate:                     lambda * sum_c min_v a_{c,v}
    (KL rate between the true chain and the chain of g*, i.e. what a goodness-of-fit test can see)

where a_{c,v} = E_pi[ #positions with radius-1 code c whose true successor bit is v ].
At eps = 0 the script also counts, over all 4096 initial states, how often the orbit of the
radius-2 rule is consistent with *some* radius-1 rule (silent misspecification).

Writes data/radius2_boundary.csv and data/radius2_zero_noise.csv
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca_noise as E

EPS_GRID = [0.001, 0.002, 0.005, 0.01, 0.02, 0.03, 0.05, 0.075, 0.1, 0.125, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]


def codes5(n=E.N):
    b = E.all_bits(n).astype(np.int64)
    return (16 * np.roll(b, 2, axis=1) + 8 * np.roll(b, 1, axis=1) + 4 * b
            + 2 * np.roll(b, -1, axis=1) + np.roll(b, -2, axis=1))


def table_from_function(fn):
    """32-entry table h[c5] from a function of the five cells (a,b,c,d,e) = (x_{i-2},...,x_{i+2})."""
    t = np.zeros(32, dtype=np.int64)
    for c5 in range(32):
        a, b, c, d, e = (c5 >> 4) & 1, (c5 >> 3) & 1, (c5 >> 2) & 1, (c5 >> 1) & 1, c5 & 1
        t[c5] = int(fn(a, b, c, d, e))
    return t


def eca_bit(rule, b, c, d):
    return (rule >> (4 * b + 2 * c + d)) & 1


GENERATORS = {
    "majority5": table_from_function(lambda a, b, c, d, e: (a + b + c + d + e) >= 3),
    "parity5": table_from_function(lambda a, b, c, d, e: (a + b + c + d + e) % 2),
    "rule110_defect10101": table_from_function(
        lambda a, b, c, d, e: eca_bit(110, b, c, d) ^ int((a, b, c, d, e) == (1, 0, 1, 0, 1))),
}


def reducible_to_radius1(table):
    """True iff the output never depends on x_{i-2} or x_{i+2}."""
    for c5 in range(32):
        if table[c5] != table[c5 ^ 16] or table[c5] != table[c5 ^ 1]:
            return False
    return True


def successor_r2(table, c5):
    out = table[c5]
    return (out << np.arange(E.N)).sum(axis=1).astype(np.int64)


def main(out="data"):
    codes3 = E.neighborhood_codes(); counts = E.code_counts(); c5 = codes5()
    rows = []; zrows = []
    for name, table in GENERATORS.items():
        assert not reducible_to_radius1(table), name
        succ = successor_r2(table, c5)
        outbits = table[c5]                                     # (S, n) true successor bits
        # per state: A[x, c, v] = #positions with code c and successor bit v
        A = np.zeros((E.S, 8, 2))
        for c in range(8):
            for v in (0, 1):
                A[:, c, v] = ((codes3 == c) & (outbits == v)).sum(axis=1)
        # ---- zero noise: silent misspecification over all x0
        z = E.zero_noise_classes(succ, counts)
        n_silent = 0; detect_times = []; silent_class_sizes = []
        for x0 in range(E.S):
            seen = {}; x = x0; t = 0; detected = -1; visited = set()
            while x not in visited:
                visited.add(x)
                for c in range(8):
                    for v in (0, 1):
                        if A[x, c, v] > 0:
                            if seen.get(c, v) != v:
                                detected = t; break
                            seen[c] = v
                    if detected >= 0: break
                if detected >= 0: break
                x = int(succ[x]); t += 1
            if detected < 0:
                n_silent += 1; silent_class_sizes.append(2 ** (8 - len(seen)))
            else:
                detect_times.append(detected)
        zrows.append(dict(generator=name, frac_silent=n_silent / E.S,
                          mean_silent_class_size=float(np.mean(silent_class_sizes)) if silent_class_sizes else float("nan"),
                          mean_detect_time=float(np.mean(detect_times)) if detect_times else float("nan"),
                          max_detect_time=int(max(detect_times)) if detect_times else -1,
                          mean_tau=float(z["tau"].mean()), max_tau=int(z["tau"].max())))
        print(name, zrows[-1], flush=True)
        # ---- noisy chain
        for eps in EPS_GRID:
            K = E.kernel_matrix(eps)
            pi, res = E.stationary_dense(succ, eps, K=K)
            a = np.einsum("x,xcv->cv", pi, A)                     # (8, 2)
            gstar = int(sum((1 << c) for c in range(8) if a[c, 1] > a[c, 0]))
            misfit = float(a.min(axis=1).sum())
            margin = float(np.abs(a[:, 1] - a[:, 0]).min())
            lam = E.lam(eps)
            # independent check by power iteration from uniform
            p = np.full(E.S, 1.0 / E.S)
            for it in range(1, 50001):
                p = E.apply_kernel_rows(E.push_forward(p, succ), eps)
                if it % 50 == 0 and np.abs(np.einsum("x,xcv->cv", p, A) - a).max() < 1e-9:
                    break
            dev = float(np.abs(np.einsum("x,xcv->cv", p, A) - a).max())
            rows.append(dict(generator=name, eps=eps, **{"lambda": lam}, g_star=gstar, misfit_per_step=misfit,
                             misfit_rate=lam * misfit, apparent_margin=margin, apparent_rate=lam * margin,
                             ratio_apparent_to_misfit=(margin / misfit if misfit > 0 else float("inf")),
                             residual=res, check_dev=dev, check_iters=it))
            print(name, eps, rows[-1]["g_star"], f"misfit {misfit:.4g} margin {margin:.4g}", flush=True)
    with open(os.path.join(out, "radius2_boundary.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    with open(os.path.join(out, "radius2_zero_noise.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(zrows[0].keys())); w.writeheader(); w.writerows(zrows)


if __name__ == "__main__":
    main()
