"""Comparison of this verification's numbers with proofs_43_142/out/ and data/ring_size/mechanisms.csv.
Run only after test_lemmas.py, potentials.py, stationary.py, entry_cost.py. -> out/compare.json
"""
import csv, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eca import Dynamics, sccs, codes_present, walls

REPO = os.path.dirname(os.getcwd())
sess = {}
for line in open(os.path.join(REPO, "proofs_43_142/out/g1_classes.jsonl")):
    r = json.loads(line); sess[(r["rule"], r["n"])] = r
pots = {}
for line in open("out/potentials.jsonl"):
    r = json.loads(line); pots[(r["rule"], r["n"])] = r
mech = {}
for r in csv.DictReader(open(os.path.join(REPO, "data/ring_size/mechanisms.csv"))):
    if r["rule"] in ("43", "142"):
        mech[(int(r["rule"]), int(r["n"]))] = r

mine = {}
diffs = []
compared = 0
for n in range(3, 21):
    for rule in (43, 142):
        dyn = Dynamics(rule, n)
        edges = dyn.one_flip_graph()
        comps, closed = sccs(dyn.m, edges)
        N = 1 << n
        cp = codes_present(n, np.arange(N))
        w = walls(n, np.arange(N))
        cw = [int(w[s[0]]) for s in dyn.cycle_states]
        codes = 0
        for c in closed:
            for k in c:
                for x in dyn.cycle_states[k]:
                    codes |= int(cp[x])
        my = dict(cycles=dyn.m, periodic_states=int(dyn.periodic.sum()), g1_edges=len(edges),
                  strong_components=len(comps), closed_classes=len(closed),
                  closed_class_sizes=sorted(len(c) for c in closed),
                  closed_members=sum(len(c) for c in closed),
                  closed_codes=[c for c in range(8) if (codes >> c) & 1],
                  closed_wall_counts=sorted(set(cw[k] for c in closed for k in c)))
        mine[(rule, n)] = my
        s = sess.get((rule, n))
        if s is None:
            diffs.append(("missing in session", rule, n)); continue
        for key, val in my.items():
            sv = s.get(key)
            if key == "closed_class_sizes":
                sv = sorted(sv)
            compared += 1
            if sv != val:
                diffs.append((rule, n, key, "mine", val, "session", sv))
        print(rule, n, "ok" if not [d for d in diffs if d[:2] == (rule, n)] else "DIFF", flush=True)

# mechanisms.csv (study solver) against this verification
mech_cmp = []
for (rule, n), r in sorted(mech.items()):
    row = dict(rule=rule, n=n)
    if (rule, n) in pots:
        p = pots[(rule, n)]
        row["n_selected"] = (int(r["n_selected"]), p["n_selected"])
        row["gamma_min"] = (int(r["gamma_min"]), p["gamma_min"])
        row["k_c"] = (r["k_c"], "-".join(map(str, p["k"])))
        row["kstar"] = (int(r["kstar"]), p["kstar"])
        row["cycles"] = (int(r["cycles"]), p["m"])
        row["source"] = "potentials (definitions)"
    elif (rule, n) in mine:
        my = mine[(rule, n)]
        row["n_selected"] = (int(r["n_selected"]), my["closed_members"])
        row["gamma_min"] = (int(r["gamma_min"]), my["cycles"] - 1)
        row["cycles"] = (int(r["cycles"]), my["cycles"])
        row["source"] = "G1 closed class + Theorem A (m - 1)"
    else:
        row["source"] = "not computed here (n > 20)"
    row["agree"] = all(v[0] == v[1] for k, v in row.items() if isinstance(v, tuple))
    mech_cmp.append(row)

# entry costs: session test 'E' vs this verification
cl = json.load(open(os.path.join(REPO, "proofs_43_142/out/check_lemmas.json")))
sess_E = [r for r in cl["results"] if r["test"] == "E"]
mine_E = json.load(open("out/entry_cost.json"))
sess_tests = [dict(test=r["test"], rule=r.get("rule"), n_min=r.get("n_min"), n_max=r.get("n_max"),
                   cases=r.get("cases"), passed=r.get("passed", r.get("all_passed", r.get("ok"))))
              for r in cl["results"]]
out = dict(g1_fields_compared=compared, g1_differences=diffs, mechanisms=mech_cmp,
           mechanisms_all_agree=all(r["agree"] for r in mech_cmp),
           session_entry_cost_tests=[{k: v for k, v in r.items() if k in ("rule", "n_min", "n_max", "cases", "failures", "passed")} for r in sess_E],
           mine_entry_cost=[{k: r[k] for k in ("rule", "n", "m", "V_to_X_max", "failures")} for r in mine_E],
           session_lemma_tests=sess_tests, session_all_passed=cl["all_passed"])
json.dump(out, open("out/compare.json", "w"), indent=1, default=str)
print("g1 fields compared", compared, "differences", len(diffs))
for d in diffs[:20]:
    print(d)
print("mechanisms rows", len(mech_cmp), "all agree", out["mechanisms_all_agree"])
for r in mech_cmp:
    if not r["agree"]:
        print(r)
