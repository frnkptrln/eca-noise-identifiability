"""Step 2, part C: the study's derived tables against own data.
zero_mechanism.csv, code_carriers.csv, rule35_blocks.csv, g1_distance_154.csv, verify_mech_*.csv (coverage only).
Writes out/compare_derived.json and appends mismatches to out/compare_derived_mismatches.csv."""
import csv
import json
import os
import sys
from collections import defaultdict

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import p2lib as P
from p2lib import K
import compare_sample as CS   # re-runs the record comparison; reuses its loaders

D = CS.D
OUT = CS.OUT
sample, extras = CS.sample, CS.extras
res = {}
mism = []


def note(table, key, field, study, own):
    if study != own:
        mism.append({"table": table, "key": str(key), "field": field, "study": str(study)[:160], "own": str(own)[:160]})
        return 0
    return 1


def seed_returns(rule, n):
    F, cm = K.build_F(rule, n)
    assert F[0] == 0
    x, seen = 1, set()
    while x not in seen:
        if x == 0:
            return 1
        seen.add(x)
        x = int(F[x])
    return 0


# ---- zero_mechanism.csv
rows = list(csv.DictReader(open(os.path.join(D, "zero_mechanism.csv"))))
ok = defaultdict(int)
coincide = defaultdict(lambda: [0, 0])
for r in rows:
    key = (int(r["rule"]), int(r["n"]))
    s = sample[key]
    sel = CS.selected_rows(*key)
    zero_alone = int(len(sel) == 1 and sel[0]["rep"] == "0" * key[1])
    sr = seed_returns(*key)
    lb = {d["rep"]: d for d in extras[key]["lemmaB_candidates"]}
    g2 = bool(zero_alone and lb.get("0" * key[1], {}).get("g2_holds", False))
    if int(r["seed_returns"]) == -1:      # the study did not compute the seed orbit for this rule (60, 90)
        ok["seed_returns_study_has_no_value"] += 1
    else:
        ok["seed_returns"] += note("zero_mechanism", key, "seed_returns", int(r["seed_returns"]), sr)
    ok["zero_alone_selected"] += note("zero_mechanism", key, "zero_alone_selected", int(r["zero_alone_selected"]), zero_alone)
    ok["kstar"] += note("zero_mechanism", key, "kstar", int(r["kstar"]), s["kstar"])
    ok["g2_holds"] += note("zero_mechanism", key, "g2_holds", r["g2_holds"] == "True", g2)
    c = coincide[key[0]]
    c[0] += 1
    c[1] += int(sr == zero_alone)
    if zero_alone:
        ok["zero_alone_and_study_g2_holds"] += int(r["g2_holds"] == "True")
        ok["zero_alone_cases"] += 1
        ok["zero_alone_and_lemmaB"] += int(g2)
        ok["zero_alone_single_cycle_map"] += int(s["n_cycles"] == 1)
res["zero_mechanism"] = {"rows": len(rows), "fields_equal": dict(ok),
                         "seed_returns_equals_zero_alone_by_rule": {str(k): v for k, v in coincide.items()},
                         "pairs_22_26_122_154": sum(coincide[r][0] for r in (22, 26, 122, 154)),
                         "coincide_22_26_122_154": sum(coincide[r][1] for r in (22, 26, 122, 154))}

# ---- code_carriers.csv
rows = list(csv.DictReader(open(os.path.join(D, "code_carriers.csv"))))
ok = defaultdict(int)
for r in rows:
    key = (int(r["rule"]), int(r["n"]))
    code = r["code"]
    oo = CS.own_orbits(*key)
    selreps = CS.sel_cache[key]
    car = [rep for rep, o in oo.items() if code in o["codes"]]
    ok["carrier_orbits"] += note("code_carriers", key + (code,), "carrier_orbits", int(r["carrier_orbits"]), len(car))
    ok["selected_carrier_orbits"] += note("code_carriers", key + (code,), "selected_carrier_orbits",
                                          int(r["selected_carrier_orbits"]), sum(rep in selreps for rep in car))
    ok["kstar"] += note("code_carriers", key + (code,), "kstar", int(r["kstar"]), sample[key]["kstar"])
res["code_carriers"] = {"rows": len(rows), "fields_equal": dict(ok),
                        "rule_code_pairs": sorted({(int(r["rule"]), int(r["code"])) for r in rows})}

# ---- rule35_blocks.csv: family = cyclic word over the blocks 10 and 100
def blocks(word):
    """(is a cyclic word over {10, 100}, number of 10-blocks, number of 100-blocks)."""
    n = len(word)
    if "1" not in word:
        return False, -1, -1
    k = word.index("1")
    w = word[k:] + word[:k]
    runs = [len(z) for z in w.split("1")[1:]]      # zero-run after each 1
    if any(z not in (1, 2) for z in runs):
        return False, -1, -1
    return True, runs.count(1), runs.count(2)


rows = list(csv.DictReader(open(os.path.join(D, "rule35_blocks.csv"))))
ok = defaultdict(int)
law = defaultdict(lambda: {"code5_not_family": 0, "family_all_states_checked": 0, "family_state_not_word": 0,
                           "family_a_not_a0_mod3": 0, "sel_a": set(), "notsel_a": set(), "nonfamily_not_selected": 0,
                           "family_a_ge1_without_code5": 0, "code5_selected": 0, "code5_orbits": 0})
by_n = defaultdict(list)
for r in rows:
    by_n[int(r["n"])].append(r)
for n, rs in sorted(by_n.items()):
    key = (35, n)
    oo = CS.own_orbits(*key)
    selreps = CS.sel_cache[key]
    F, cm = K.build_F(35, n)
    m, cyc, attr, minstate, length, ccodes = K.find_cycles(n, F, cm)
    no, rot1, orb, reps, osz, omin = K.rotation_orbits(n, m, cyc, minstate)
    ok["orbit_rows_equal_own_orbit_count"] += note("rule35_blocks", key, "rows", len(rs), no)
    L = law[n]
    for r in rs:
        x = int(r["pattern"], 2)
        rep = P.bits(omin[orb[cyc[x]]], n)
        own = oo[rep]
        fam, a, b = blocks(rep)
        if fam:   # every state of the cycle must be such a word with the same a
            for y in P.cycle_states(F, int(x)):
                f2, a2, b2 = blocks(P.bits(y, n))
                L["family_all_states_checked"] += 1
                if not (f2 and a2 == a):
                    L["family_state_not_word"] += 1
        has5 = "5" in own["codes"]
        selected = rep in selreps
        a0 = (2 * n) % 3
        ok["family"] += note("rule35_blocks", key + (r["pattern"],), "family", int(r["family"]), int(fam))
        ok["a"] += note("rule35_blocks", key + (r["pattern"],), "a", int(r["a"]), a)
        ok["a0"] += note("rule35_blocks", key + (r["pattern"],), "a0", int(r["a0"]), a0)
        ok["has_code5"] += note("rule35_blocks", key + (r["pattern"],), "has_code5", int(r["has_code5"]), int(has5))
        ok["selected"] += note("rule35_blocks", key + (r["pattern"],), "selected", int(r["selected"]), int(selected))
        L["code5_orbits"] += has5
        L["code5_selected"] += (has5 and selected)
        L["code5_not_family"] += (has5 and not (fam and a >= 1))
        L["family_a_ge1_without_code5"] += (fam and a >= 1 and not has5)
        if fam:
            L["family_a_not_a0_mod3"] += (a % 3 != a0)
            (L["sel_a"] if selected else L["notsel_a"]).add(a)
        else:
            L["nonfamily_not_selected"] += (not selected)
res["rule35_blocks"] = {"rows": len(rows), "fields_equal": dict(ok),
                        "law_by_n": {str(n): {k: (sorted(v) if isinstance(v, set) else int(v)) for k, v in L.items()}
                                     for n, L in sorted(law.items())}}

# ---- g1_distance_154.csv
rows = list(csv.DictReader(open(os.path.join(D, "g1_distance_154.csv"))))
ok = defaultdict(int)
g1d = {}
for n in sorted({int(r["n"]) for r in rows}):
    c = P.Case(154, n)
    z = int(c.cyc[0])
    # distance to the zero cycle along directed G1 edges: breadth-first search on the reversed graph
    dist = np.full(c.m, -1, np.int64)
    dist[z] = 0
    order = np.argsort(c.dst, kind="stable")
    ss, dd = c.src[order], c.dst[order]
    starts = np.searchsorted(dd, np.arange(c.m + 1))
    front = [z]
    while front:
        nxt = []
        for v in front:
            for u in ss[starts[v]:starts[v + 1]]:
                if dist[u] < 0:
                    dist[u] = dist[v] + 1
                    nxt.append(int(u))
        front = nxt
    ones = np.zeros(c.m)
    for j in range(c.m):
        st = P.cycle_states(c.F, c.minstate[j])
        ones[j] = np.mean([bin(v).count("1") for v in st])
    rs = [r for r in rows if int(r["n"]) == n]
    ok["rows_equal_cycle_count"] += note("g1_distance_154", n, "rows", len(rs), c.m)
    for r in rs:
        j = int(c.cyc[int(r["pattern"], 2)])
        ok["distance"] += note("g1_distance_154", (n, r["pattern"]), "g1_distance_to_zero", int(r["g1_distance_to_zero"]), int(dist[j]))
        ok["period"] += note("g1_distance_154", (n, r["pattern"]), "period", int(r["period"]), int(c.length[j]))
        ok["mean_ones"] += note("g1_distance_154", (n, r["pattern"]), "mean_ones", round(float(r["mean_ones"]), 3), round(float(ones[j]), 3))
    rad = c.radius()
    g1d[str(n)] = {"cycles": int(c.m), "unreachable": int((dist < 0).sum()), "max_distance": int(dist.max()),
                   "spearman_mean_ones_vs_distance": round(float(spearmanr(ones, dist)[0]), 4),
                   "cycles_radius_ge2": int((rad >= 2).sum()), "radius_zero_cycle": int(rad[z]),
                   "min_gamma_sample": sample[(154, n)]["min_gamma"]}
res["g1_distance_154"] = {"rows": len(rows), "fields_equal": dict(ok), "own": g1d}

# ---- verify_mech_*.csv: coverage and the agree column (read only; nothing recomputed here)
cov = {}
reps, refl, comp = P.class_reps()
for name in ["verify_mech_n4_8_all.csv", "verify_mech_n9_10_switching.csv"]:
    rs = list(csv.DictReader(open(os.path.join(D, name))))
    pairs = {(int(r["rule"]), int(r["n"])) for r in rs}
    if "all" in name:
        want = {(r, n) for r in reps for n in range(4, 9)}
    else:
        want = {(r, n) for r in [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154] for n in (9, 10)}
    missing = sorted(want - pairs)
    bij_missing = []
    for (r, n) in missing:
        F, cm = K.build_F(r, n)
        bij_missing.append(len(np.unique(F)) == (1 << n))
    cov[name] = {"rows": len(rs), "agree_1": sum(r["agree"] == "1" for r in rs), "pairs_expected_from_report_text": len(want),
                 "pairs_missing": len(missing), "missing_all_bijective": bool(all(bij_missing)),
                 "missing_examples": missing[:8]}
res["verify_mech_files"] = cov
res["n_class_representatives"] = len(reps)
res["n_mismatches"] = len(mism)
json.dump(res, open(os.path.join(OUT, "compare_derived.json"), "w"), indent=1, sort_keys=True)
with open(os.path.join(OUT, "compare_derived_mismatches.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, ["table", "key", "field", "study", "own"])
    w.writeheader()
    w.writerows(mism)
print(json.dumps(res, indent=0, sort_keys=True)[:6000])
