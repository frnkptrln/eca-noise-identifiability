"""Sweep under walls: k_c, k*, noise-selected cycles for the 160 reflection classes (null_classes.py) at
n = nmin..nmax with boundary null (default), one or reflect.

Bijective rules: analytic (the note's argument uses no ring: P(x, y) = q(F(x) XOR y) is doubly stochastic
for bijective F, so the uniform law is stationary, every state has order 0 and, for n >= 3, every code occurs
at an interior cell: k* = 0). Others: exact solver fwlib.classify(..., boundary=...).

Per (rule, n): checkpoint record in data/boundaries/{b}_sweep.jsonl (append-only, fsynced); detail file
data/boundaries/{b}_details/n{n}_rule_{rule}.json.gz with every cycle (smallest state, period, code mask),
gamma of every cycle, the noise-selected cycles, k_c, k*, missed codes; certificate (cert.py format with a
'boundary' field) in data/boundaries/{b}_certificates/ for n <= --cert-nmax. Final table
data/boundaries/{b}_sweep.csv (sorted, independent of interruptions) and {b}_sweep_cost.csv.

Usage: python3 run_boundaries.py --nmin 4 --nmax 14 --workers 2 [--boundary null] [--rules 90,94]
"""
import argparse, gzip, json, os, sys, time, resource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, ckpt, cert, null_classes

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "boundaries")
RESULT_FIELDS = ["boundary", "n", "rule", "bijective", "cycles", "max_period", "cycle_codes_union", "b_type",
                 "n_stable", "gamma_min", "stable_cover", "missed_codes", "k_c", "kstar", "stable_min_states"]


def codes_str(mask):
    return "".join(str(c) for c in range(8) if (mask >> c) & 1) or "-"


def write_json_gz(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as fh:
            fh.write(json.dumps(obj, separators=(",", ":"), sort_keys=True).encode())
        raw.flush(); os.fsync(raw.fileno())
    os.replace(tmp, path)


def job(args):
    n, rule, boundary, cert_nmax = args
    t0 = time.time(); c0 = time.process_time()
    F = fwlib.succ_map(rule, n, boundary)
    if fwlib.is_bijective(F):
        cs = fwlib.CycleStructure(rule, n, F, boundary)
        gamma = np.zeros(cs.m, dtype=np.int64); stable = np.arange(cs.m)
        k_c = np.zeros(8, dtype=np.int64); kstar = 0; gmin = 0
        cover = int(np.bitwise_or.reduce(cs.cyc_codes)); bij = 1; expanded = 0
        assert n < 3 or cover == 255
        if n <= cert_nmax:
            d = os.path.join(DATA, f"{boundary}_certificates"); os.makedirs(d, exist_ok=True)
            cert.write(cert.bijective_certificate(rule, n, F, boundary), os.path.join(d, f"n{n:02d}_rule_{rule:03d}.json.gz"))
    else:
        res = fwlib.classify(rule, n, F=F, boundary=boundary)
        cs = res["cs"]; gamma = res["gamma"]; stable = res["stable"]; k_c = res["k_c"]; kstar = int(res["kstar"])
        gmin = int(res["gmin"]); cover = int(res["stable_cover"]); bij = 0; expanded = int(res["expanded"])
        if n <= cert_nmax:
            d = os.path.join(DATA, f"{boundary}_certificates"); os.makedirs(d, exist_ok=True)
            cert.write(cert.make_certificate(res), os.path.join(d, f"n{n:02d}_rule_{rule:03d}.json.gz"))
    missed = 255 & ~cover
    d = os.path.join(DATA, f"{boundary}_details"); os.makedirs(d, exist_ok=True)
    write_json_gz(dict(boundary=boundary, n=n, rule=rule, bijective=bij, cycle_min=[int(v) for v in cs.cyc_min],
                       period=[int(v) for v in cs.period], cycle_codes=[int(v) for v in cs.cyc_codes],
                       gamma=[int(v) for v in gamma], gamma_min=gmin, stable=[int(v) for v in stable],
                       k_c=[int(v) for v in k_c], kstar=kstar, stable_cover=cover, missed_codes=missed),
                  os.path.join(d, f"n{n:02d}_rule_{rule:03d}.json.gz"))
    st = [int(cs.cyc_min[s]) for s in stable]
    rec = dict(boundary=boundary, n=n, rule=rule, bijective=bij, cycles=int(cs.m), max_period=int(cs.period.max()),
               cycle_codes_union=int(np.bitwise_or.reduce(cs.cyc_codes)), n_stable=int(len(stable)), gamma_min=gmin,
               stable_cover=cover, missed_codes=codes_str(missed), k_c="-".join(str(int(v)) for v in k_c), kstar=kstar,
               stable_min_states=";".join(str(v) for v in st[:20]) + (";..." if len(st) > 20 else ""))
    rec["b_type"] = int(rec["cycle_codes_union"] != 255)
    rec["key"] = [boundary, n, rule]
    rec["cost_seconds"] = round(time.time() - t0, 3)
    rec["cost_cpu_seconds"] = round(time.process_time() - c0, 3)
    rec["cost_maxrss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
    rec["cost_expanded"] = expanded
    return rec


def finalize(boundary):
    recs = ckpt.load(os.path.join(DATA, f"{boundary}_sweep.jsonl"))
    df = pd.DataFrame(list(recs.values())).sort_values(["n", "rule"]).reset_index(drop=True)
    df[RESULT_FIELDS].to_csv(os.path.join(DATA, f"{boundary}_sweep.csv"), index=False)
    df[["boundary", "n", "rule", "cycles", "cost_seconds", "cost_cpu_seconds", "cost_maxrss_mb", "cost_expanded"]].to_csv(
        os.path.join(DATA, f"{boundary}_sweep_cost.csv"), index=False)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=4); ap.add_argument("--nmax", type=int, default=14)
    ap.add_argument("--workers", type=int, default=2); ap.add_argument("--rules", default="")
    ap.add_argument("--boundary", default="null"); ap.add_argument("--cert-nmax", type=int, default=14)
    a = ap.parse_args()
    assert a.workers <= 2, "machine budget: at most 2 worker processes"
    os.makedirs(DATA, exist_ok=True)
    CK = os.path.join(DATA, f"{a.boundary}_sweep.jsonl")
    rules = [int(v) for v in a.rules.split(",")] if a.rules else null_classes.null_class_reps()
    done = ckpt.load(CK)
    jobs = [(n, r, a.boundary, a.cert_nmax) for n in range(a.nmin, a.nmax + 1) for r in rules
            if (a.boundary, n, r) not in done]
    jobs.sort(key=lambda j: (j[0], j[1]))
    print(f"{len(jobs)} jobs ({len(done)} in checkpoint)", flush=True)
    t0 = time.time()
    if a.workers <= 1:
        it = map(job, jobs)
    else:
        from multiprocessing import Pool
        pool = Pool(a.workers, maxtasksperchild=1)
        it = pool.imap_unordered(job, jobs)
    for i, rec in enumerate(it):
        ckpt.append(CK, rec)
        if rec["cost_seconds"] > 30 or (i + 1) % 160 == 0:
            print(f"[{i+1}/{len(jobs)}] n={rec['n']} rule={rec['rule']} {rec['cost_seconds']}s "
                  f"{rec['cost_maxrss_mb']}MB at {time.time()-t0:.0f}s", flush=True)
    if a.workers > 1:
        pool.close(); pool.join()
    df = finalize(a.boundary)
    print(f"done in {time.time()-t0:.0f}s; table has {len(df)} rows", flush=True)


if __name__ == "__main__":
    main()
