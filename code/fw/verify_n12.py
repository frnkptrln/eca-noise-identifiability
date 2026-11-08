"""Verifier (b)-(d) at n = 12.

(c) all 256 rules are classified independently; k* must be constant on the 88 classes, k_c must
    permute under reflection (code bits reversed) and complementation (c -> 7 - c), and the multiset
    of gamma - gamma_min and the number of noise-selected cycles must be class invariants.
(d) the 42 classes that v0.1 proved falling (some code on no cycle) must have k* >= 1; bijective
    rules must have k* = 0.
(b) k* = 0 iff v0.1 classifies the class as rising (trend in data/stationary_rates.csv); the
    expected trend ratio rho(0.002)/rho(0.001) ~ 2^k* * lambda(0.002)/lambda(0.001) is compared too.
    Disagreements are listed, not tuned away.
(b') --gth: high-precision GTH stationary laws at n = 12 for selected rules at eps = 1e-4 .. 1e-7;
    observed orders of every pi(x) and nu_c against the prediction (cached per rule and eps).

Outputs: data/fw_n12_all_rules.csv, data/fw_n12_checks.csv, data/fw_n12_gth.csv
"""
import argparse, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib, orders

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
DATA = os.path.join(ROOT, "data")
N = 12
lam = lambda e: (1 - 2 * e) * np.log((1 - e) / e)
refl_code = lambda c: 4 * (c & 1) + 2 * ((c >> 1) & 1) + (c >> 2)


def all_rules():
    rows = []
    for r in range(256):
        res = fwlib.classify(r, N)
        g = res["gamma"] - res["gmin"]
        rows.append(dict(rule=r, rep=fwlib.class_rep(r), cycles=res["m"], kstar=res["kstar"],
                         k_c="-".join(str(int(v)) for v in res["k_c"]),
                         n_stable=len(res["stable"]), gamma_min=res["gmin"],
                         gamma_profile="-".join(str(int(v)) for v in np.bincount(g)),
                         stable_cover=int(res["stable_cover"]),
                         bijective=int(fwlib.is_bijective(res["cs"].F))))
    return pd.DataFrame(rows)


def checks(df):
    out = []
    by = {r.rule: r for r in df.itertuples()}
    kc = {r: [int(v) for v in by[r].k_c.split("-")] for r in range(256)}
    for r in range(256):
        fr, fc = fwlib.reflect_rule(r), fwlib.complement_rule(r)
        ok_refl = all(kc[fr][refl_code(c)] == kc[r][c] for c in range(8))
        ok_comp = all(kc[fc][7 - c] == kc[r][c] for c in range(8))
        same = lambda a, b: (by[a].kstar, by[a].n_stable, by[a].gamma_profile, by[a].cycles) == \
                            (by[b].kstar, by[b].n_stable, by[b].gamma_profile, by[b].cycles)
        out.append(dict(check="c_symmetry", rule=r, ok=int(ok_refl and ok_comp and same(r, fr) and same(r, fc))))
    zr = pd.read_csv(os.path.join(DATA, "zero_noise_per_rule.csv"))
    for z in zr.itertuples():
        if z.limit_type == "B_proved":
            out.append(dict(check="d_Bproved_kstar_ge1", rule=z.rule, ok=int(by[z.rule].kstar >= 1)))
    for r in range(256):
        if by[r].bijective:
            out.append(dict(check="d_bijective_kstar0", rule=r, ok=int(by[r].kstar == 0)))
    return pd.DataFrame(out)


def trend_compare(df):
    cs = pd.read_csv(os.path.join(DATA, "class_summary.csv"))
    es = pd.read_csv(os.path.join(DATA, "epsilon_star.csv"))
    d = cs.merge(es[["rule", "rho_ratio_0002_over_0001", "smallest_resolved_eps"]], on="rule")
    d = d.merge(df[["rule", "kstar", "k_c", "n_stable", "cycles"]], on="rule")
    base = lam(0.002) / lam(0.001)
    d["v01_class"] = np.where(d.limit_type == "B_proved", "B", np.where(d.rising == 1, "U-rising", "U-falling"))
    d["v01_rising"] = d.rising
    d["fw_rising"] = (d.kstar == 0).astype(int)
    d["agree"] = (d.v01_rising == d.fw_rising).astype(int)
    d["ratio_expected"] = base * 2.0 ** d.kstar
    d["k_from_ratio"] = np.log2(d.rho_ratio_0002_over_0001 / base)
    return d


def _solve(args):
    rule, e, fn = args
    from verify_stationary import gth, popcount
    F = fwlib.succ_map(rule, N)
    H = popcount(F[:, None] ^ np.arange(1 << N)[None, :])
    P = e ** H * (1 - e) ** (N - H)
    t0 = time.time(); pi = gth(P)
    np.save(fn + ".tmp.npy", pi)
    with open(fn + ".tmp.npy", "rb") as fh:
        os.fsync(fh.fileno())
    os.replace(fn + ".tmp.npy", fn)
    return rule, e, time.time() - t0


def gth_check(rules, eps_list, cache_dir, workers=2):
    os.makedirs(cache_dir, exist_ok=True)
    fn = lambda r, e: os.path.join(cache_dir, f"n12_r{r}_e{e:.0e}.npy")
    jobs = [(r, e, fn(r, e)) for r in rules for e in eps_list if not os.path.exists(fn(r, e))]
    print(f"{len(jobs)} GTH solves at n = 12", flush=True)
    from multiprocessing import Pool
    with Pool(workers) as pool:
        for r, e, dt in pool.imap_unordered(_solve, jobs):
            print(f"rule {r} eps {e:g}: {dt:.0f}s", flush=True)
    cnt = np.zeros((1 << N, 8), dtype=np.int64)
    x = np.arange(1 << N)
    for i in range(N):
        c = 4 * ((x >> ((i - 1) % N)) & 1) + 2 * ((x >> i) & 1) + ((x >> ((i + 1) % N)) & 1)
        np.add.at(cnt, (x, c), 1)
    rows = []
    for rule in rules:
        res = fwlib.classify(rule, N, keep_dists=True)
        ordp = orders.state_orders(res)
        pis = np.array([np.load(fn(rule, e)) for e in eps_list]); nus = pis @ cnt
        step = np.log10(eps_list[0] / eps_list[1])
        sl_pi = np.log10(pis[:-1] / pis[1:]) / step
        sl_nu = np.log10(nus[:-1] / nus[1:]) / step
        rows.append(dict(rule=rule, kstar_pred=res["kstar"],
                         k_c_pred="-".join(str(int(v)) for v in res["k_c"]),
                         k_c_obs="-".join(f"{v:.4f}" for v in sl_nu[-1]),
                         max_dev_pi_last=float(np.abs(sl_pi[-1] - ordp).max()),
                         max_dev_pi_first=float(np.abs(sl_pi[0] - ordp).max()),
                         max_dev_nu_last=float(np.abs(sl_nu[-1] - res["k_c"]).max()),
                         nu_min_at=" ".join(f"{v:.6g}" for v in nus.min(axis=1)),
                         eps=" ".join(f"{e:g}" for e in eps_list)))
    return pd.DataFrame(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gth", default="", help="comma-separated rules for the n = 12 GTH check")
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    t0 = time.time()
    df = all_rules()
    df.to_csv(os.path.join(DATA, "fw_n12_all_rules.csv"), index=False)
    ch = checks(df)
    ch.to_csv(os.path.join(DATA, "fw_n12_checks.csv"), index=False)
    print(f"(c)/(d): {len(ch)} checks, failures: {int((ch.ok == 0).sum())}; "
          + ", ".join(f"{k}: {int(v.ok.sum())}/{len(v)}" for k, v in ch.groupby("check")), flush=True)
    tr = trend_compare(df)
    tr.to_csv(os.path.join(DATA, "fw_n12_vs_v01.csv"), index=False)
    print(f"(b): {int(tr.agree.sum())}/{len(tr)} classes agree with the v0.1 trend; disagreements: "
          f"{tr[tr.agree == 0].rule.tolist()}; {time.time()-t0:.0f}s", flush=True)
    if a.gth:
        rules = [int(v) for v in a.gth.split(",")]
        g = gth_check(rules, [1e-4, 1e-5, 1e-6, 1e-7], os.path.join(DATA, "cache", "gth12"), a.workers)
        g.to_csv(os.path.join(DATA, "fw_n12_gth.csv"), index=False)
        print(g[["rule", "kstar_pred", "k_c_pred", "k_c_obs", "max_dev_pi_last", "max_dev_nu_last", "nu_min_at"]].to_string(index=False))


if __name__ == "__main__":
    main()
