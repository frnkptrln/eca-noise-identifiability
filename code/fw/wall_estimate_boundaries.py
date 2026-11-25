"""Wall-time estimate for the next wall-boundary batch, from the measured CPU cost per job
(data/boundaries/{b}_sweep_cost.csv): each rule's cost at n_last is extrapolated with its own growth factor
cost(n_last)/cost(n_last - 1) (at least 2, at most 6), plus 0.25 s process start per job (maxtasksperchild=1).
Usage: python3 wall_estimate_boundaries.py --nmax 16 [--rules ...] [--workers 2]"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import null_classes

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")


def estimate(cost, rules, n_targets, workers=2):
    p = cost.pivot(index="rule", columns="n", values="cost_cpu_seconds").loc[rules]
    # per rule: its own last computed n (BUG-B1: a common last column made rules without data at that n
    # count as zero; the n = 15..16 estimate of the remaining rules was 1.1 min, measured 3.4 min)
    last = p.apply(lambda r: int(r.last_valid_index()), axis=1)
    c_last = np.array([p.loc[r, last[r]] for r in p.index]); c_prev = np.array([p.loc[r, last[r] - 1] for r in p.index])
    g = np.clip(c_last / np.maximum(c_prev, 1e-3), 2, 6)
    tot, worst = 0.0, 0.0
    for n in n_targets:
        c = c_last * g ** (n - last.values)
        tot += float(c.sum()) + 0.25 * len(rules); worst = max(worst, float(c.max()))
    return tot, tot / workers, worst


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--boundary", default="null"); ap.add_argument("--nmin", type=int); ap.add_argument("--nmax", type=int)
    ap.add_argument("--rules", default=""); ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    cost = pd.read_csv(os.path.join(DATA, f"{a.boundary}_sweep_cost.csv"))
    rules = [int(v) for v in a.rules.split(",")] if a.rules else null_classes.null_class_reps()
    cpu, wall, worst = estimate(cost, rules, range(a.nmin, a.nmax + 1), a.workers)
    print(f"{len(rules)} rules, n = {a.nmin}..{a.nmax}: about {cpu/60:.1f} CPU-min, {wall/60:.1f} min wall at "
          f"{a.workers} workers, longest job about {worst/60:.1f} min")
