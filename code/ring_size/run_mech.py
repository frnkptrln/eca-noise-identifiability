"""Batch runner: mechanism analysis (mech.analyze) for given rules and ring sizes.

Checkpoint data/ring_size/mech.jsonl (append-only, fsynced, one record per (n, rule), resumable; via
code/fw/ckpt.py). Final tables, sorted and independent of the run order:
  data/ring_size/mechanisms.csv     one row per (rule, n)
  data/ring_size/cycle_orbits.csv.gz one row per rotation orbit of cycles (all orbits)
  data/ring_size/mech_cost.csv      wall time, CPU time and peak memory per job (CPU time is recorded for
                                    jobs run after the verification of 14 Nov 2026; empty for earlier jobs)
Every record is compared with the v0.2 sweep (data/fw_sweep.csv) where that has the same (rule, n):
cycles, n_selected, gamma_min, k_c, k* must agree. For bijective maps gamma_min is m - 1 (every state is
periodic, single flips join the cycles in both directions, so G1 is strongly connected and Theorem A gives
m - 1); v0.2 stores the placeholder 0 there, so gamma_min is not compared on bijective records.

No time or memory cap is enforced by this script. Cost is measured per job as wall time and as CPU time
(time.process_time); any statement about a cost cap must refer to CPU time.

Usage: python3 run_mech.py --nmin 8 --nmax 20 --rules 22,26,... --workers 2 [--tag _x] [--out DIR]
       python3 run_mech.py --finalize-only [--tag _x] [--out DIR]     rebuild the tables from the checkpoint
"""
import argparse, os, sys, time, resource, json, gzip
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "fw"))
import numpy as np, pandas as pd
import ckpt, fwlib, mech, rsdata

DATA = os.path.join(HERE, "..", "..", "data")
OUT = os.path.join(DATA, "ring_size")
SWITCHING = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]


def job(args):
    n, rule, list_all = args
    t0 = time.time(); c0 = time.process_time()
    F = fwlib.succ_map(rule, n)
    if fwlib.is_bijective(F):
        cs = fwlib.CycleStructure(rule, n, F)
        rec = dict(rule=rule, n=n, cycles=cs.m, bijective=1, n_selected=cs.m, kstar=0, gamma_min=cs.m - 1,
                   k_c="0-0-0-0-0-0-0-0", selected_cover="01234567")
        orbits = []
    else:
        rec, orbits = mech.analyze(rule, n, res=fwlib.classify(rule, n, F=F), list_all=list_all)
        rec["bijective"] = 0
    rec["key"] = [n, rule]
    rec["orbits"] = orbits
    rec["cost_seconds"] = round(time.time() - t0, 2)                 # wall time
    rec["cost_cpu_seconds"] = round(time.process_time() - c0, 2)     # CPU time of this job's process
    rec["cost_maxrss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
    return rec


def finalize(tag):
    recs = ckpt.load(os.path.join(OUT, f"mech{tag}.jsonl"))
    rows = [{k: v for k, v in r.items() if k not in ("orbits", "key")} for r in recs.values()]
    df = pd.DataFrame(rows).sort_values(["rule", "n"]).reset_index(drop=True)
    # bijective maps: gamma_min = m - 1 (checkpoint records written before 14 Nov 2026 hold the placeholder 0)
    bij = df.bijective.astype(int) == 1
    df.loc[bij, "gamma_min"] = df.loc[bij, "cycles"] - 1
    df["gamma_min"] = df.gamma_min.astype(int)
    if "cost_cpu_seconds" not in df:
        df["cost_cpu_seconds"] = np.nan
    cost = df[["rule", "n", "cycles", "cost_seconds", "cost_cpu_seconds", "cost_maxrss_mb"]].rename(
        columns={"cost_seconds": "wall_seconds", "cost_cpu_seconds": "cpu_seconds", "cost_maxrss_mb": "maxrss_mb"})
    df.drop(columns=["cost_seconds", "cost_cpu_seconds", "cost_maxrss_mb"]).to_csv(os.path.join(OUT, f"mechanisms{tag}.csv"), index=False)
    cost.to_csv(os.path.join(OUT, f"mech_cost{tag}.csv"), index=False)
    orb = pd.DataFrame([o for r in recs.values() for o in r["orbits"]])
    if len(orb):
        orb = orb.sort_values(["rule", "n", "orbit_rep_min_state"]).reset_index(drop=True)
        with gzip.open(os.path.join(OUT, f"cycle_orbits{tag}.csv.gz"), "wt", newline="") as fh:
            orb.to_csv(fh, index=False)
    # comparison with v0.2
    v02 = pd.read_csv(os.path.join(DATA, "fw_sweep.csv"))
    mrg = df.merge(v02, on=["rule", "n"], suffixes=("", "_v02"))
    bad = rsdata.v02_disagreements(mrg)
    nbij = int((mrg.bijective.astype(int) == 1).sum())
    print(f"finalize: {len(df)} records, {len(mrg)} compared with v0.2, {len(bad)} disagreements {bad[:10]} "
          f"(gamma_min not compared on the {nbij} bijective records)")
    return df, bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=8)
    ap.add_argument("--nmax", type=int, default=20)
    ap.add_argument("--rules", default="switching")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--selected-only", action="store_true", help="orbit table: selected orbits only (atlas)")
    ap.add_argument("--finalize-only", action="store_true", help="run no job; rebuild the tables from the checkpoint")
    a = ap.parse_args()
    globals()["OUT"] = a.out
    if a.finalize_only:
        finalize(a.tag)
        return
    assert a.workers <= 2, "load budget: at most 2 worker processes"
    if a.rules == "switching":
        rules = SWITCHING
    elif a.rules == "all":
        rules = fwlib.class_reps()
    else:
        rules = [int(v) for v in a.rules.split(",")]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"mech{a.tag}.jsonl")
    done = ckpt.load(path)
    jobs = [(n, r) for n in range(a.nmin, a.nmax + 1) for r in rules if (n, r) not in done]
    jobs.sort(key=lambda j: -j[0])            # largest rings first: the longest jobs start early
    jobs = [(n, r, not a.selected_only) for n, r in jobs]
    print(f"{len(jobs)} jobs to run, {len(done)} already in checkpoint", flush=True)
    t0 = time.time()
    if a.workers == 1:
        it = map(job, jobs)
    else:
        import multiprocessing as mp
        pool = mp.get_context("spawn").Pool(a.workers, maxtasksperchild=1)
        it = pool.imap_unordered(job, jobs)
    for rec in it:
        ckpt.append(path, rec)
        print(f"[{time.time() - t0:7.0f}s] n={rec['n']} rule={rec['rule']} k*={rec['kstar']} "
              f"wall={rec['cost_seconds']}s cpu={rec['cost_cpu_seconds']}s rss={rec['cost_maxrss_mb']}MB", flush=True)
    finalize(a.tag)


if __name__ == "__main__":
    main()
