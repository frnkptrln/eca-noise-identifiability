"""Where the wall is: measured cost per ring size (data/fw_sweep_cost.csv) and the cycle structure at
n = 22 for the heaviest classes, giving CPU and memory estimates for an n = 22 sweep with the present
implementation. Output: data/fw_wall.csv (one row per statement / class)."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import fwlib

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data")
cost = pd.read_csv(os.path.join(DATA, "fw_sweep_cost.csv"))
sw = pd.read_csv(os.path.join(DATA, "fw_sweep.csv"))
pv = cost.pivot(index="rule", columns="n", values="cost_seconds")
rss = cost.pivot(index="rule", columns="n", values="cost_maxrss_mb")
orb = sw.pivot(index="rule", columns="n", values="cycle_orbits")
cyc = sw.pivot(index="rule", columns="n", values="cycles")
heavy = pv[20].sort_values(ascending=False).index[:6].tolist()
rows = []
for r in heavy:
    t = time.time()
    cs = fwlib.CycleStructure(r, 22)
    rep, _ = cs.rotation_orbits()
    m22, o22 = cs.m, len(np.unique(rep))
    rows.append(dict(rule=int(r), cycles20=int(cyc.loc[r, 20]), orbits20=int(orb.loc[r, 20]), cpu20=float(pv.loc[r, 20]),
                     rss20_mb=float(rss.loc[r, 20]), cycles22=int(m22), orbits22=int(o22),
                     cpu22_est=float(pv.loc[r, 20] * pv.loc[r, 20] / pv.loc[r, 18]),
                     vrows22_gb=o22 * m22 / 1e9, seconds=round(time.time() - t, 1)))
    print(rows[-1], flush=True)
df = pd.DataFrame(rows)
ratio = (pv[20] / pv[18]).replace([np.inf], np.nan)
cpu22 = float((pv[20] * ratio.fillna(1)).sum())
tot20 = float(pv[20].sum())
worst = df.sort_values("vrows22_gb", ascending=False).iloc[0]
stmt = (f"n = 20 is the largest ring size computed: {tot20:.0f} CPU seconds for the 88 classes, "
        f"longest job {pv[20].max():.0f} s (class {int(pv[20].idxmax())}), largest peak memory {rss[20].max():.0f} MB (class {int(rss[20].idxmax())}). "
        f"Cost grows by a factor {np.nanmedian(ratio.loc[heavy]):.0f} (median over the {len(heavy)} heaviest classes) from n = 18 to 20; "
        f"extrapolated with each class's own factor, n = 22 needs about {cpu22/3600:.1f} CPU hours, i.e. about {cpu22/2/3600:.1f} h wall at 2 workers. "
        f"The memory wall is the stored distance rows (one byte per cycle per rotation orbit): at n = 22 class {int(worst.rule)} has "
        f"{int(worst.cycles22)} cycles in {int(worst.orbits22)} rotation orbits, {worst.vrows22_gb:.1f} GB of rows. "
        "Both are properties of this implementation (dense V rows per orbit, one BFS over all 2^n states per orbit), not of the rules; "
        "keeping only the weight levels the contraction actually expands (and recomputing a row on demand) would reduce the memory term; the BFS term (orbits x 2^n) remains.")
df["statement"] = ""
df = pd.concat([pd.DataFrame([dict(rule=-1, statement=stmt)]), df], ignore_index=True)
df.to_csv(os.path.join(DATA, "fw_wall.csv"), index=False)
print(stmt)
