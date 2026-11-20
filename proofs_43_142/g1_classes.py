"""Direct computation of the one-flip graph G1 of rules 43 and 142 and of its closed classes (one process).

Independent of the proofs: all 2^n states are tabulated, the periodic states and the cycle every state falls to are
determined, every single flip of every periodic state is followed, the strongly connected components of G1 and the
closed classes are computed. The record of each (rule, n) is compared with the statements of PROOF_43_142.md:

  4 | n      : the only closed class is {X}, X the cycle of (0011)^(n/4); every cycle has a G1 path to X;
  otherwise  : the only closed class is the set of cycles whose wall count is w- or w+ (the even numbers next to n/2).

usage: python g1_classes.py n [n ...]      (appends to out/g1_classes.jsonl; (rule, n) already present are skipped)
"""
import json
import os
import resource
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ring  # noqa: E402

OUT = os.path.join(HERE, "out", "g1_classes.jsonl")


def levels(n):
    lo = max(w for w in range(0, n + 1, 2) if 2 * w < n)
    hi = min(w for w in range(0, n + 2, 2) if 2 * w > n)
    return lo, hi


def run(rule, n):
    t0 = time.process_time()
    A = ring.analyse(rule, n)
    cycles = A["cycles"]
    m = len(cycles)
    first = np.array([c[0] for c in cycles], np.int64)
    wcyc = np.array([ring.wall_count(int(s), n) for s in first], np.int64)
    E = ring.g1_edges(A)
    nscc, comp_, closed = ring.closed_classes(m, E)
    members = sorted(sum(closed, []))
    codes = set()
    for k in members:
        for s in cycles[k]:
            codes |= ring.codes_of(int(s), n)
    whist = {}
    for w in wcyc.tolist():
        whist[w] = whist.get(w, 0) + 1
    period_hist = {}
    for c in cycles:
        period_hist[len(c)] = period_hist.get(len(c), 0) + 1
    rec = dict(rule=rule, n=n, cycles=m, periodic_states=int(A["on"].sum()), g1_edges=int(len(E)),
               strong_components=int(nscc), closed_classes=len(closed), closed_class_sizes=sorted(len(c) for c in closed),
               closed_members=len(members), closed_wall_counts=sorted(set(wcyc[members].tolist())),
               closed_codes=sorted(codes), cycles_by_wall_count={str(k): v for k, v in sorted(whist.items())},
               period_hist={str(k): v for k, v in sorted(period_hist.items())})
    # out-degree 0 nodes (cycles that no single flip leaves)
    outdeg = np.bincount(E[:, 0], minlength=m) if len(E) else np.zeros(m, np.int64)
    rec["cycles_without_leaving_flip"] = int((outdeg == 0).sum())
    if n % 4 == 0:
        x0 = ring.from_string("0011" * (n // 4))
        kX = int(A["cid"][x0])
        rec["crystal_is_cycle_of_length"] = len(cycles[kX]) if kX >= 0 else 0
        rec["crystal_radius_ge2"] = bool(kX >= 0 and outdeg[kX] == 0)
        reach = ring.reaches(m, E, [kX])
        rec["cycles_without_path_to_crystal"] = int((~reach).sum())
        # longest shortest path to X in G1 (breadth-first search on the reversed graph)
        radj = [[] for _ in range(m)]
        for u, v in E.tolist():
            radj[v].append(u)
        dist = [-1] * m
        dist[kX] = 0
        q = [kX]
        for v in q:
            for u in radj[v]:
                if dist[u] < 0:
                    dist[u] = dist[v] + 1
                    q.append(u)
        rec["max_g1_distance_to_crystal"] = max(dist)
        rec["g1_distance_equals_wall_formula"] = bool(all(dist[k] == abs(int(wcyc[k]) - n // 2) // 2 for k in range(m)))
        rec["predicted"] = "closed classes = {X}"
        rec["prediction_holds"] = bool(len(closed) == 1 and members == [kX] and rec["cycles_without_path_to_crystal"] == 0
                                       and rec["crystal_radius_ge2"] and sorted(codes) == [1, 3, 4, 6])
    else:
        lo, hi = levels(n)
        pred = sorted(np.flatnonzero((wcyc == lo) | (wcyc == hi)).tolist())
        rec["w_minus"], rec["w_plus"] = lo, hi
        rec["cycles_on_levels"] = len(pred)
        rec["predicted"] = "one closed class = cycles with wall count w- or w+; all eight codes"
        rec["prediction_holds"] = bool(len(closed) == 1 and members == pred and sorted(codes) == list(range(8)))
    rec["cpu_seconds"] = round(time.process_time() - t0, 2)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rec["peak_mb"] = round(peak / 1e6 if sys.platform == "darwin" else peak / 1e3)
    return rec


def main():
    ns = [int(a) for a in sys.argv[1:]]
    done = set()
    if os.path.exists(OUT):
        with open(OUT) as fh:
            for line in fh:
                r = json.loads(line)
                done.add((r["rule"], r["n"]))
    for n in ns:
        for rule in (43, 142):
            if (rule, n) in done:
                print(f"rule {rule} n {n}: already present, skipped", flush=True)
                continue
            rec = run(rule, n)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec) + "\n")
            print(f"rule {rule} n {n}: cycles {rec['cycles']}, closed classes {rec['closed_class_sizes']}, "
                  f"prediction holds {rec['prediction_holds']}, CPU {rec['cpu_seconds']} s, peak {rec['peak_mb']} MB",
                  flush=True)


if __name__ == "__main__":
    main()
