"""Ring-size sweep: k_c, k*, noise-selected cycles for the 88 class representatives at n = nmin..nmax.

Bijective rules: analytic (uniform stationary law, k* = 0). Others: exact solver (fwlib.classify).
Checkpoint: data/fw_sweep.jsonl (append-only, fsynced; one record per (n, rule)); final tables
data/fw_sweep.csv (results only, sorted; identical for resumed and uninterrupted runs) and
data/fw_sweep_cost.csv (wall time and peak memory per job). Certificates for n <= --cert-nmax in
data/fw_certificates_sweep/n{n}_rule_{rule}.json.gz.

Usage: python3 run_sweep.py --nmin 4 --nmax 16 --workers 2 [--rules 0,1,...] [--cert-nmax 14]
"""
import argparse, os, sys, time, resource
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, ckpt

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
RESULT_FIELDS = ["n", "rule", "bijective", "cycles", "cycle_orbits", "cycle_codes_union", "b_type",
                 "n_stable", "gamma_min", "stable_cover", "k_c", "kstar", "stable_min_states"]


def job(args):
    n, rule, cert_nmax, tag = args
    t0 = time.time()
    F = fwlib.succ_map(rule, n)
    cs = None
    if fwlib.is_bijective(F):
        cs = fwlib.CycleStructure(rule, n, F)
        rec = dict(bijective=1, cycles=cs.m, cycle_orbits=-1, n_stable=cs.m, gamma_min=0,
                   stable_cover=255, k_c="0-0-0-0-0-0-0-0", kstar=0, stable_min_states="all")
        cyc_union = int(np.bitwise_or.reduce(cs.cyc_codes))
        expanded = 0
    else:
        res = fwlib.classify(rule, n, F=F)
        cs = res["cs"]
        st = res["stable"]
        rec = dict(bijective=0, cycles=res["m"], cycle_orbits=int(len(res["es"].reps)), n_stable=len(st),
                   gamma_min=int(res["gmin"]), stable_cover=int(res["stable_cover"]),
                   k_c="-".join(str(int(v)) for v in res["k_c"]), kstar=int(res["kstar"]),
                   stable_min_states=";".join(str(int(cs.cyc_min[s])) for s in st[:20]) + (";..." if len(st) > 20 else ""))
        cyc_union = int(np.bitwise_or.reduce(cs.cyc_codes))
        expanded = int(res["expanded"])
        if n <= cert_nmax:
            import cert
            d = os.path.join(DATA, f"fw_certificates_sweep{tag}"); os.makedirs(d, exist_ok=True)
            cert.write(cert.make_certificate(res), os.path.join(d, f"n{n:02d}_rule_{rule:03d}.json.gz"))
    rec.update(n=n, rule=rule, cycle_codes_union=cyc_union, b_type=int(cyc_union != 255))
    rec["key"] = [n, rule]
    rec["cost_seconds"] = round(time.time() - t0, 3)
    rec["cost_maxrss_mb"] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e6, 1)
    rec["cost_expanded"] = expanded
    return rec


def finalize(tag=""):
    recs = ckpt.load(os.path.join(DATA, f"fw_sweep{tag}.jsonl"))
    df = pd.DataFrame(list(recs.values())).sort_values(["n", "rule"]).reset_index(drop=True)
    df[RESULT_FIELDS].to_csv(os.path.join(DATA, f"fw_sweep{tag}.csv"), index=False)
    df[["n", "rule", "cycles", "cost_seconds", "cost_maxrss_mb", "cost_expanded"]].to_csv(
        os.path.join(DATA, f"fw_sweep{tag}_cost.csv"), index=False)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nmin", type=int, default=4); ap.add_argument("--nmax", type=int, default=16)
    ap.add_argument("--workers", type=int, default=2); ap.add_argument("--rules", default="")
    ap.add_argument("--cert-nmax", type=int, default=14)
    ap.add_argument("--tag", default="", help="suffix for checkpoint/output names (tests)")
    a = ap.parse_args()
    CK = os.path.join(DATA, f"fw_sweep{a.tag}.jsonl")
    rules = [int(v) for v in a.rules.split(",")] if a.rules else fwlib.class_reps()
    done = ckpt.load(CK)
    jobs = [(n, r, a.cert_nmax, a.tag) for n in range(a.nmin, a.nmax + 1) for r in rules if (n, r) not in done]
    print(f"{len(jobs)} jobs ({len(done)} in checkpoint)", flush=True)
    t0 = time.time()
    if a.workers <= 1:
        it = map(job, jobs)
    else:
        from multiprocessing import Pool
        pool = Pool(a.workers, maxtasksperchild=1)      # fresh process per job: per-job peak memory
        it = pool.imap_unordered(job, jobs)
    for i, rec in enumerate(it):
        ckpt.append(CK, rec)
        if rec["cost_seconds"] > 30 or (i + 1) % 88 == 0:
            print(f"[{i+1}/{len(jobs)}] n={rec['n']} rule={rec['rule']} {rec['cost_seconds']}s "
                  f"{rec['cost_maxrss_mb']}MB at {time.time()-t0:.0f}s", flush=True)
    if a.workers > 1:
        pool.close(); pool.join()
    df = finalize(a.tag)
    print(f"done in {time.time()-t0:.0f}s; table has {len(df)} rows", flush=True)


if __name__ == "__main__":
    main()
