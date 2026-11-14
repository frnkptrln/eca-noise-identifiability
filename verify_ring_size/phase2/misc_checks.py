"""Small checks: (f) block maps of width <= 4 intertwining rule 154 with a radius-1 rule (factor_search.csv);
the '169 pairs agree with v0.2' sentence against the sealed sample; data/ring_size/MANIFEST.sha256.
Writes out/misc_checks.json."""
import csv
import hashlib
import json
import os
import sys
from collections import Counter

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
D = os.path.join(REPO, "data", "ring_size")
res = {}

# ---- (f) factor search: phi: {0,1}^w -> {0,1} with phi(F_154 x) = F_g(phi x) for a radius-1 rule g
def f154(a, b, c):
    return (154 >> (4 * a + 2 * b + c)) & 1


own = Counter()
partial = Counter()
for w in range(1, 5):
    L = w + 2
    wins = [[(v >> (L - 1 - i)) & 1 for i in range(L)] for v in range(1 << L)]
    idx = lambda bits: int("".join(map(str, bits)), 2)
    A = np.array([idx(x[0:w]) for x in wins])
    B = np.array([idx(x[1:w + 1]) for x in wins])
    C = np.array([idx(x[2:w + 2]) for x in wins])
    # image window: needs w cells of F(x), i.e. w + 2 cells of x -> but phi is applied to the w cells 1..w of F(x),
    # which depend on cells 0..w+1 of x: exactly the window of length w + 2
    Dn = np.array([idx([f154(x[i - 1], x[i], x[i + 1]) for i in range(1, w + 1)]) for x in wins])
    for phi in range(1 << (1 << w)):
        tab = np.array([(phi >> k) & 1 for k in range(1 << w)])
        t = 4 * tab[A] + 2 * tab[B] + tab[C]
        d = tab[Dn]
        g, ok, und = 0, True, 0
        for code in range(8):
            v = d[t == code]
            if len(v) == 0:
                und += 1
            elif v.min() != v.max():
                ok = False
                break
            elif v[0]:
                g |= 1 << code
        if ok and und == 0:
            own[(w, g)] += 1
        elif ok:
            partial[w] += 1
study = {(int(r["width"]), int(r["target_rule"])): int(r["block_maps"]) for r in csv.DictReader(open(os.path.join(D, "factor_search.csv")))}
res["factor_search"] = {"own_counts_width_target": sorted([[k[0], k[1], v] for k, v in own.items()]),
                        "study_counts_width_target": sorted([[k[0], k[1], v] for k, v in study.items()]),
                        "equal": dict(own) == study,
                        "target_rules_own": sorted({k[1] for k in own}),
                        "additive_targets_found": sorted({k[1] for k in own} & {0, 60, 90, 102, 105, 150, 153, 165, 170, 195, 204, 240, 15, 51, 85, 255}),
                        "consistent_maps_with_undetermined_target_codes_by_width": {str(k): v for k, v in sorted(partial.items())}}

# ---- v0.2 sweep against the sealed sample, 13 classes, n = 8..20
sample = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(ROOT, "out", "sample.jsonl")))}
n_cmp, bad = 0, []
bij_gamma0 = 0
for r in csv.DictReader(open(os.path.join(REPO, "data", "fw_sweep.csv"))):
    key = (int(r["rule"]), int(r["n"]))
    if key in sample and key[1] <= 20:
        s = sample[key]
        n_cmp += 1
        for f, a, b in [("cycles", int(r["cycles"]), s["n_cycles"]), ("n_stable", int(r["n_stable"]), s["selected"]["n_cycles"]),
                        ("k_c", r["k_c"], "-".join(map(str, s["k"]))), ("kstar", int(r["kstar"]), s["kstar"])]:
            if a != b:
                bad.append([key[0], key[1], f, a, b])
        if int(r["gamma_min"]) != s["min_gamma"]:
            if s["bijective"] and int(r["gamma_min"]) == 0:
                bij_gamma0 += 1
            else:
                bad.append([key[0], key[1], "gamma_min", int(r["gamma_min"]), s["min_gamma"]])
res["v02_sweep_vs_sample"] = {"pairs_compared": n_cmp, "differences": bad,
                              "gamma_min_0_placeholder_in_bijective_rows": bij_gamma0}

# ---- manifest
ok = miss = wrong = 0
listed = set()
for line in open(os.path.join(D, "MANIFEST.sha256")):
    h, name = line.split(None, 1)
    name = name.strip().lstrip("*")
    p = os.path.join(D, name)
    listed.add(os.path.normpath(name))
    if not os.path.exists(p):
        miss += 1
    elif hashlib.sha256(open(p, "rb").read()).hexdigest() == h:
        ok += 1
    else:
        wrong += 1
present = set()
for dp, dn, fn in os.walk(D):
    for f in fn:
        present.add(os.path.normpath(os.path.relpath(os.path.join(dp, f), D)))
res["manifest"] = {"entries": len(listed), "sha_ok": ok, "sha_wrong": wrong, "listed_but_missing": miss,
                   "files_not_listed": sorted(present - listed)}
json.dump(res, open(os.path.join(HERE, "out", "misc_checks.json"), "w"), indent=1)
print(json.dumps(res, indent=0))
