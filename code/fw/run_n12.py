"""Decider at n = 12: noise-selected cycles, code coverage, k_c, k* and a certificate for each of the 88
classes, and the line-by-line comparison with v0.1 (data/class_summary.csv, data/epsilon_star.csv).

Outputs: data/fw_certificates_n12/rule_RRR.json.gz (checked by check_cert.py), data/fw_n12_classes.csv."""
import os, sys, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, cert

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
N = 12
lam = lambda e: (1 - 2 * e) * np.log((1 - e) / e)
codes_str = lambda mask: ",".join(format(c, "03b") for c in range(8) if (mask >> c) & 1)


def main():
    outdir = os.path.join(DATA, "fw_certificates_n12")
    os.makedirs(outdir, exist_ok=True)
    rows = []
    t0 = time.time()
    for rule in fwlib.class_reps():
        F = fwlib.succ_map(rule, N)
        fn = os.path.join(outdir, f"rule_{rule:03d}.json.gz")
        if fwlib.is_bijective(F):
            c = cert.bijective_certificate(rule, N, F)
            cs = fwlib.CycleStructure(rule, N, F)
            rows.append(dict(rule=rule, cycles=cs.m, bijective=1, n_stable=cs.m, gamma_min="",
                             stable_cycles="all (uniform law)", stable_cover=codes_str(255), k_c="0-0-0-0-0-0-0-0",
                             kstar=0, uncovered="", covering="all", gamma_gap=""))
        else:
            res = fwlib.classify(rule, N, F=F)
            c = cert.make_certificate(res)
            cs = res["cs"]
            st = res["stable"]
            desc = ";".join(f"{int(cs.cyc_min[s])}/p{int(cs.period[s])}" for s in st[:12]) + (";..." if len(st) > 12 else "")
            g = res["gamma"] - res["gmin"]
            gap = int(g[g > 0].min()) if (g > 0).any() else ""
            rows.append(dict(rule=rule, cycles=res["m"], bijective=0, n_stable=len(st), gamma_min=res["gmin"],
                             stable_cycles=desc, stable_cover=codes_str(res["stable_cover"]),
                             k_c="-".join(str(int(v)) for v in res["k_c"]), kstar=res["kstar"],
                             uncovered=",".join(format(x, "03b") for x in c.get("uncovered_codes", [])),
                             covering=";".join(f"{int(cs.cyc_min[s])}/p{int(cs.period[s])}" for s in c.get("covering_cycles", [])),
                             gamma_gap=gap))
        cert.write(c, fn)
    df = pd.DataFrame(rows)
    cs_ = pd.read_csv(os.path.join(DATA, "class_summary.csv"))
    es = pd.read_csv(os.path.join(DATA, "epsilon_star.csv"))
    v = cs_.merge(es[["rule", "rho_ratio_0002_over_0001", "smallest_resolved_eps"]], on="rule")
    v["v01_type"] = np.where(v.limit_type == "B_proved", "B", np.where(v.rising == 1, "U-rising", "U-falling"))
    df = df.merge(v[["rule", "v01_type", "rising", "interior_max", "eps_star", "trend_ratio",
                     "rho_ratio_0002_over_0001", "smallest_resolved_eps"]], on="rule")
    df["v01_rising"] = df.rising; df = df.drop(columns="rising")
    df["fw_rising"] = (df.kstar == 0).astype(int)
    df["agree"] = (df.v01_rising == df.fw_rising).astype(int)
    df["ratio_expected"] = lam(0.002) / lam(0.001) * 2.0 ** df.kstar
    df.to_csv(os.path.join(DATA, "fw_n12_classes.csv"), index=False)
    print(f"{len(df)} classes in {time.time()-t0:.0f}s; agree with v0.1: {int(df.agree.sum())}; "
          f"disagree: {df[df.agree == 0].rule.tolist()}")
    print(df.groupby(["v01_type", "kstar"]).size().to_string())


if __name__ == "__main__":
    main()
