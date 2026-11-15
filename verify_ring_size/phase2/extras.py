"""Step 2 supplement (computed after the seal, own code): for each of the 194 sample cases, one row per
rotation orbit of cycles (canonical representative, orbit size, periods, codes, exact radius, closed-class
membership; gamma where the sealed solve took < GAMMA_CPU_LIMIT CPU-seconds) and the hypotheses of Lemma B for
every rotation orbit of radius >= 2.  Checkpoint: one JSON line per case in out/extras.jsonl, one csv per case
in out/own_orbits/.  Usage: python extras.py [NMIN NMAX]"""
import csv
import json
import os
import resource
import sys
import time

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P
from p2lib import K

GAMMA_CPU_LIMIT = 30.0
OUT = os.path.join(P.HERE, "out")
os.makedirs(os.path.join(OUT, "own_orbits"), exist_ok=True)
sample = [json.loads(l) for l in open(os.path.join(P.ROOT, "out", "sample.jsonl"))]
nmin, nmax = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (0, 99)
done = set()
ck = os.path.join(OUT, "extras.jsonl")
if os.path.exists(ck):
    done = {(r["rule"], r["n"]) for r in map(json.loads, open(ck))}
for s in sorted(sample, key=lambda s: (s["n"], s["rule"])):
    rule, n = s["rule"], s["n"]
    if (rule, n) in done or not (nmin <= n <= nmax):
        continue
    t0 = time.process_time()
    c = P.Case(rule, n)
    assert c.m == s["n_cycles"] and c.no == s["n_orbits"]
    rad = c.radius()
    sp, tr, sr = K.cycle_geometry(n, c.F, c.omin)
    gamma = None
    if s["cpu_seconds"] < GAMMA_CPU_LIMIT:
        V, kd = c.full_V()
        gamma = K.edmonds_all_roots(V)
        del V
        assert int(gamma.min()) == s["min_gamma"]
    cand = [o for o in range(c.no) if rad[c.reps[o]] >= 2]
    lb = []
    for o in cand:
        assert (rad[c.orbit_members(o)] >= 2).all()
        d = c.lemmaB(o, rad)
        d.update(rep=P.bits(c.omin[o], n), radius=int(rad[c.reps[o]]))
        lb.append(d)
    path = os.path.join(OUT, "own_orbits", "orb_r%d_n%d.csv" % (rule, n))
    with open(path + ".tmp", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rule", "n", "rep", "orbit_size", "temporal_period", "spatial_period", "t_rot", "rot", "codes",
                    "radius", "in_closed_class", "scc", "gamma"])
        for o in np.argsort(c.omin, kind="stable"):
            r = c.reps[o]
            w.writerow([rule, n, P.bits(c.omin[o], n), int(c.osz[o]), int(c.length[r]), int(sp[o]), int(tr[o]),
                        int(sr[o]), P.codes_str(c.ccodes[r]), int(rad[r]), int(c.in_closed[r]), int(c.lab[r]),
                        "" if gamma is None else int(gamma[r])])
    os.replace(path + ".tmp", path)
    rec = {"rule": rule, "n": n, "m": int(c.m), "n_orbits": int(c.no), "bijective": bool(c.bijective),
           "n_scc": int(c.ncomp), "n_closed": int(c.closed_comp.sum()), "n_edges": int(len(c.src)),
           "radius_hist": [[int(a), int(b)] for a, b in zip(*np.unique(rad, return_counts=True))],
           "gamma_per_orbit": gamma is not None, "lemmaB_candidates": lb,
           "cpu_seconds": round(time.process_time() - t0, 3),
           "peak_rss_mb": round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / (1024 * 1024), 1)}
    with open(ck, "a") as fh:
        fh.write(json.dumps(rec, sort_keys=True) + "\n")
    print(rule, n, rec["cpu_seconds"], flush=True)
