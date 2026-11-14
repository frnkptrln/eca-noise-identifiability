"""Lead audit of selected findings of verify_ring_size/phase2/FINDINGS_part1.md.
Own code from the definitions; reads the sealed sample and the study's files; imports no study code."""
import json, sys, time, csv, gzip, os, subprocess
out = {}
t0 = time.process_time()
# --- F1: rule 22, n = 241, single-seed orbit (Python integers; bit i = cell i)
def step22(x, n, mask):
    l = ((x << 1) | (x >> (n - 1))) & mask      # value of the neighbour i-1 at bit i
    r = ((x >> 1) | (x << (n - 1))) & mask      # value of the neighbour i+1 at bit i
    # rule 22: exactly one of the three cells is 1
    return (l ^ x ^ r) & ~(l & x & r) & ~((l & x) | (x & r) | (l & r)) & mask | 0
def f22_bruteforce(a, b, c): return (22 >> (4 * a + 2 * b + c)) & 1
# check the bit formula against the rule table on all states of n = 9
n = 9; mask = (1 << n) - 1; bad = 0
for x in range(1 << n):
    y = 0
    for i in range(n):
        y |= f22_bruteforce((x >> ((i - 1) % n)) & 1, (x >> i) & 1, (x >> ((i + 1) % n)) & 1) << i
    bad += (y != step22(x, n, mask))
out["rule22_bit_formula_mismatches_n9"] = bad
res = {}
for n, cap in ((241, 2_000_000), (121, 2_000_000), (125, 2_000_000), (253, 2_000_000)):
    mask = (1 << n) - 1; x = 1; t = 0
    while x and t < cap:
        x = step22(x, n, mask); t += 1
    res[n] = {"reached_zero": x == 0, "steps": t}
out["F1_rule22_seed_orbit"] = res
# --- F4, F5, F8 from the sealed sample
S = {(r["rule"], r["n"]): r for r in map(json.loads, open("verify_ring_size/out/sample.jsonl"))}
def nsel(r):
    s = r["selected"]; return s.get("n_selected_cycles", s.get("n_cycles_selected", None)) if isinstance(s, dict) else None
out["sample_selected_keys"] = sorted(S[(45, 18)]["selected"].keys()) if isinstance(S[(45, 18)]["selected"], dict) else str(type(S[(45, 18)]["selected"]))
out["F4_class45"] = {n: {"cycles": S[(45, n)]["n_cycles"], "gamma_hist": S[(45, n)]["gamma_hist"], "kstar": S[(45, n)]["kstar"]} for n in (10, 12, 14, 16, 18, 20, 22)}
out["F5_class73"] = {n: {"cycles": S[(73, n)]["n_cycles"], "min_gamma": S[(73, n)]["min_gamma"], "gamma_hist_head": S[(73, n)]["gamma_hist"][:3], "kstar": S[(73, n)]["kstar"]} for n in (9, 21, 22)}
out["F8_class26"] = {n: {"kstar": S[(26, n)]["kstar"], "codes_missing": S[(26, n)]["codes_missing"]} for n in range(8, 23) if S[(26, n)]["kstar"] >= 1}
# study's own orbit table for F4/F5: uniform 2-cycle rows
rows = []
with gzip.open("data/ring_size/cycle_orbits.csv.gz", "rt") as fh:
    rd = csv.DictReader(fh); out["cycle_orbits_columns"] = rd.fieldnames
    for r in rd:
        if r["rule"] in ("45", "73") and r["n"] in ("18", "22", "9") and set(r["pattern"]) <= {"0"}:
            rows.append({k: r[k] for k in rd.fieldnames if k in ("rule", "n", "pattern", "temporal_period", "gamma", "selected", "radius")})
out["study_rows_uniform_cycle"] = rows
# --- F6: the study's own evidence files
out["stopped_runs_csv"] = open("data/ring_size/stopped_runs.csv").read()
out["log_mech_154_n22"] = open("data/ring_size/log_mech_154_n22.txt").read()
st = os.stat("data/ring_size/log_mech_154_n22.txt")
out["log_mech_154_n22_times"] = {"birth": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(getattr(st, "st_birthtime", 0))), "mtime": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(st.st_mtime))}
out["cpu_seconds"] = round(time.process_time() - t0, 1)
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1)[:6000])
