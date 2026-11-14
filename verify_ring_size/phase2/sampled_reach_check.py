"""Step 3 (e): the sampled reachability table 5.6.
(1) target radius flags re-derived with own code (seed orbits / crystal flips);
(2) the table columns recomputed from the study's files data/ring_size/sampled_reach/*.csv;
(3) for the first K sampled initial states of each file: limit cycle recomputed (period, label), and an own
    best-first search for a path of one-flip steps into the target; every step of the found path is then
    re-verified with the Python big-integer step.  The study's files store only the path length, not the path.
Writes out/sampled_reach_check.json and out/sampled_paths_own.jsonl."""
import csv
import ctypes as C
import glob
import heapq
import json
import os
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbitlib as O

HERE = O.HERE
OUT = os.path.join(HERE, "out")
D = os.path.join(os.path.dirname(os.path.dirname(HERE)), "data", "ring_size", "sampled_reach")
_SRC, _LIB = os.path.join(HERE, "p2reach.c"), os.path.join(HERE, "build", "p2reach.dylib")
if (not os.path.exists(_LIB)) or os.path.getmtime(_LIB) < os.path.getmtime(_SRC):
    subprocess.check_call(["/usr/bin/clang", "-O3", "-shared", "-fPIC", "-o", _LIB + ".tmp", _SRC])
    os.replace(_LIB + ".tmp", _LIB)
lib = C.CDLL(_LIB)
u64 = C.c_uint64
lib.limit_info.argtypes = [C.c_int, C.c_int, u64, u64, C.c_int, C.POINTER(u64), C.POINTER(u64), C.POINTER(C.c_int), C.POINTER(u64)]
lib.successors.argtypes = [C.c_int, C.c_int, u64, u64, u64, C.c_int, C.c_long, C.POINTER(u64), C.POINTER(u64),
                           C.POINTER(C.c_int), C.POINTER(C.c_int), C.POINTER(C.c_long)]
lib.successors.restype = C.c_long
MAXSTEPS = 5 * 10 ** 7
CAP = 200000
K = int(sys.argv[1]) if len(sys.argv) > 1 else 5
BUDGET = 600           # cycles expanded per sample
t_start = time.process_time()


def limit(rule, n, x, allowed):
    l, p, mu, h = u64(0), u64(0), u64(0), C.c_int(0)
    ok = lib.limit_info(rule, n, x, MAXSTEPS, allowed, C.byref(l), C.byref(p), C.byref(h), C.byref(mu))
    assert ok
    return int(l.value), int(p.value), int(h.value), int(mu.value)


_lab, _st = (u64 * CAP)(), (u64 * CAP)()
_cell, _hv = (C.c_int * CAP)(), (C.c_int * CAP)()


def succ(rule, n, x0, P, allowed):
    cnt = C.c_long(0)
    seen = lib.successors(rule, n, x0, P, MAXSTEPS, allowed, CAP, _lab, _st, _cell, _hv, C.byref(cnt))
    assert seen >= 0
    return [(int(_lab[i]), int(_st[i]), int(_cell[i]), int(_hv[i])) for i in range(cnt.value)]


def py_limit(rule, n, x):
    """Limit cycle by the Python big-integer step and a dictionary (independent of the C code)."""
    seen = {}
    t = 0
    while x not in seen:
        seen[x] = t
        x = O.step(rule, n, x)
        t += 1
    cyc = [x]
    y = O.step(rule, n, x)
    while y != x:
        cyc.append(y)
        y = O.step(rule, n, y)
    return min(cyc), len(cyc), set(cyc)


def target_spec(target, n):
    if target == "zero":
        return 1 << 0, None
    word = target.split(":")[1]
    codes = set()
    w = word * 3
    for i in range(len(word)):
        codes.add(int(w[i + len(word) - 1] + w[i + len(word)] + w[i + len(word) + 1], 2))
    return sum(1 << c for c in codes), word


res = {"files": {}, "paths_checked": 0, "paths_found": 0, "paths_verified_step_by_step": 0, "path_failures": [],
       "period_mismatch": 0, "label_mismatch": 0, "own_path_longer_than_study": 0, "own_path_shorter_than_study": 0}
seed_own = {(r["rule"], r["n"]): r for r in csv.DictReader(open(os.path.join(OUT, "seed_orbits_own.csv")))}
cr_own = {(r["rule"], r["n"]): r for r in csv.DictReader(open(os.path.join(OUT, "crystal_radius_own.csv")))}
paths_fh = open(os.path.join(OUT, "sampled_paths_own.jsonl"), "w")
for f in sorted(glob.glob(os.path.join(D, "rule*_n*.csv"))):
    rows = list(csv.DictReader(open(f)))
    rule, n, target = int(rows[0]["rule"]), int(rows[0]["n"]), rows[0]["target"]
    allowed, word = target_spec(target, n)
    # (1) radius flag
    if target == "zero":
        own_flag = int(seed_own[(str(rule), str(n))]["returns_to_zero"])
    else:
        own_flag = int(cr_own[(str(rule), str(n))]["radius_ge2"])
    # (2) table columns
    tab = {"sampled": len(rows), "distinct_cycles": len({r["cycle_label"] for r in rows}),
           "reach_target": sum(int(r["found"]) for r in rows), "max_path_len": max(int(r["path_len"]) for r in rows),
           "target_radius_ge2_study": int(rows[0]["target_radius_ge2"]), "target_radius_ge2_own": own_flag}
    # (3) own search for the first K samples
    done = []
    own_orbit_labels, own_cycle_labels = set(), set()
    for r in rows[:K]:
        x0 = int(r["x0"])
        lab, P, h, mu = limit(rule, n, x0, allowed)
        res["period_mismatch"] += int(P != int(r["period"]))
        res["label_mismatch"] += int(lab != int(r["cycle_label"]))
        # the study's label: smallest state over the cycle and all its rotations (found by reading sample_reach.py)
        cset0 = py_limit(rule, n, x0)[2]
        mask = (1 << n) - 1
        canon = min(((s << k) | (s >> (n - k))) & mask for s in cset0 for k in range(n))
        res["label_mismatch_rotation_canonical"] = res.get("label_mismatch_rotation_canonical", 0) + int(canon != int(r["cycle_label"]))
        own_orbit_labels.add(canon)
        own_cycle_labels.add(lab)
        # best-first search on cycles: priority (h, depth)
        parent = {lab: None}
        info = {lab: (P, h)}
        pq = [(h, 0, lab)]
        goal = lab if h == 0 else None
        expanded = 0
        while pq and goal is None and expanded < BUDGET:
            hcur, dep, cur = heapq.heappop(pq)
            expanded += 1
            for (l2, s, j, h2) in succ(rule, n, cur, info[cur][0], allowed):
                if l2 in parent:
                    continue
                parent[l2] = (cur, s, j)
                P2 = limit(rule, n, l2, allowed)[1]
                info[l2] = (P2, h2)
                if h2 == 0:
                    goal = l2
                    break
                heapq.heappush(pq, (h2, dep + 1, l2))
        res["paths_checked"] += 1
        rec = {"rule": rule, "n": n, "target": target, "sample": int(r["sample"]), "x0": x0, "start_cycle": lab,
               "period": P, "study_path_len": int(r["path_len"]), "found": goal is not None, "expanded": expanded}
        if goal is None:
            res["path_failures"].append([rule, n, int(r["sample"]), "no path within %d expansions" % BUDGET])
        else:
            path = []
            cur = goal
            while parent[cur] is not None:
                prev, s, j = parent[cur]
                path.append({"from_cycle": prev, "state": s, "cell": j, "to_cycle": cur})
                cur = prev
            path.reverse()
            rec["path"] = path
            rec["own_path_len"] = len(path)
            res["paths_found"] += 1
            res["own_path_longer_than_study"] += int(len(path) > int(r["path_len"]))
            res["own_path_shorter_than_study"] += int(len(path) < int(r["path_len"]))
            # step-by-step verification with the Python step
            ok = True
            curlab, curP, curset = py_limit(rule, n, x0)
            ok &= (curlab == lab)
            for stp in path:
                ok &= (stp["from_cycle"] == curlab and stp["state"] in curset)
                curlab, curP, curset = py_limit(rule, n, stp["state"] ^ (1 << stp["cell"]))
                ok &= (curlab == stp["to_cycle"])
            if target == "zero":
                ok &= (curset == {0})
            else:
                ok &= all(O.to_str(s, n) in {(word[k:] + word[:k]) * (n // len(word)) for k in range(len(word))} for s in curset)
            rec["verified_step_by_step"] = bool(ok)
            res["paths_verified_step_by_step"] += int(ok)
            if not ok:
                res["path_failures"].append([rule, n, int(r["sample"]), "verification failed"])
        paths_fh.write(json.dumps(rec) + "\n")
        done.append(rec.get("own_path_len"))
    tab["own_path_len_max"] = max(d for d in done if d is not None) if any(d is not None for d in done) else None
    tab["own_paths_found"] = sum(d is not None for d in done)
    tab["own_distinct_rotation_orbits_of_cycles"] = len(own_orbit_labels)
    tab["own_distinct_cycles"] = len(own_cycle_labels)
    tab["samples_with_own_path_longer_than_study"] = sum(1 for d, r in zip(done, rows[:K]) if d is not None and d > int(r["path_len"]))
    tab["samples_with_own_path_shorter_than_study"] = sum(1 for d, r in zip(done, rows[:K]) if d is not None and d < int(r["path_len"]))
    res["files"][os.path.basename(f)] = tab
paths_fh.close()

# report table 5.6 against the recomputed columns
rep = open(os.path.join(os.path.dirname(os.path.dirname(HERE)), "report_ring_size.md")).read().split("\n")
i = next(k for k, l in enumerate(rep) if l.startswith("| rule | n | target | target_radius_ge2"))
tab_bad = []
n_rows = 0
for l in rep[i + 2:]:
    if not l.startswith("|"):
        break
    c = [v.strip() for v in l.strip().strip("|").split("|")]
    n_rows += 1
    t = res["files"]["rule%s_n%s.csv" % (c[0], c[1])]
    own = [str(t["target_radius_ge2_own"]), str(t["sampled"]), str(t["distinct_cycles"]), str(t["reach_target"]), str(t["max_path_len"])]
    if c[3:] != own:
        tab_bad.append({"row": c, "own": own})
res["table_5_6_rows"] = n_rows
res["table_5_6_differences"] = tab_bad
res["radius_flag_differences"] = [k for k, t in res["files"].items() if t["target_radius_ge2_study"] != t["target_radius_ge2_own"]]
res["samples_per_file_checked"] = K
res["cpu_seconds"] = round(time.process_time() - t_start, 1)
json.dump(res, open(os.path.join(OUT, "sampled_reach_check.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in res.items() if k != "files"}))
for k, t in res["files"].items():
    print(k, t)
