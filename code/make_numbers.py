"""Derive every number quoted in the note from the CSVs and write note/numbers.tex (LaTeX macros)
plus note/table_classes.tex (the per-class table).  Nothing in the note is typed by hand."""
import os, sys, hashlib, json
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
DATA = os.path.join(HERE, "..", "data"); NOTE = os.path.join(HERE, "..", "note")

st = pd.read_csv(os.path.join(DATA, "stationary_rates.csv"))
z = pd.read_csv(os.path.join(DATA, "zero_noise_per_rule.csv"))
es = pd.read_csv(os.path.join(DATA, "epsilon_star.csv"))
fh = pd.read_csv(os.path.join(DATA, "finite_horizon_per_rule.csv"))
r2 = pd.read_csv(os.path.join(DATA, "radius2_boundary.csv"))
r2z = pd.read_csv(os.path.join(DATA, "radius2_zero_noise.csv"))
zs = pd.read_csv(os.path.join(DATA, "zero_noise_per_state.csv.gz"))

macros = {}
def M(name, value):
    macros[name] = value

def fmt(x, nd=3):
    return f"{x:.{nd}f}"

reps = sorted(z.rep.unique())
assert len(reps) == 88
zr = z[z.rule.isin(reps)].set_index("rule")

# ---------------- zero noise ----------------
M("ZeroFracFullAll", fmt(100 * (zs.class_size == 1).mean(), 1))          # % of all (rule, x0) pairs
M("ZeroPairsTotal", f"{len(zs):,}")
M("ZeroPairsFull", f"{int((zs.class_size == 1).sum()):,}")
M("ZeroMeanClass", fmt(zs.class_size.mean(), 2))
M("ZeroMaxClass", str(int(zs.class_size.max())))
M("ZeroMaxTau", str(int(zs.tau.max())))
M("ZeroMedianTau", str(int(zs.tau.median())))
M("ZeroMeanTau", fmt(zs.tau.mean(), 1))
M("ZeroMaxTauRule", ", ".join(str(int(z.loc[z.rule == r, "rep"].iloc[0])) for r in sorted(set(zs[zs.tau == zs.tau.max()].rule.map(lambda r: int(z.loc[z.rule == r, "rep"].iloc[0]))))))
cls_counts = zs.class_size.value_counts().sort_index()
_big = {k: v for k, v in cls_counts.items() if 100 * v / len(zs) >= 0.05}
_rest = sum(v for k, v in cls_counts.items() if k not in _big)
M("ZeroClassHist", ", ".join(f"$|C_\\infty|={k}$: {100*v/len(zs):.1f}\\%" for k, v in _big.items()) + (f", larger: {100*_rest/len(zs):.2f}\\%" if _rest else ""))
M("ZeroBestClassFrac", fmt(100 * zr.frac_full_identification.max(), 1))
M("ZeroBestClassRule", " and ".join(str(r) for r in zr[zr.frac_full_identification == zr.frac_full_identification.max()].index))
M("ZeroWorstClassFrac", fmt(100 * zr.frac_full_identification.min(), 1))
M("ZeroWorstClassRules", ", ".join(str(r) for r in zr[zr.frac_full_identification == zr.frac_full_identification.min()].index))
M("NumClassesBproved", str(int((zr.limit_type == "B_proved").sum())))
M("NumClassesUndet", str(int((zr.limit_type == "undetermined").sum())))
M("NumRulesBproved", str(int((z.limit_type == "B_proved").sum())))
M("NumRulesUndet", str(int((z.limit_type == "undetermined").sum())))
M("NumClassesAllCyclesFull", str(int(zr.all_cycles_full.sum())))

# ---------------- stationary / rates ----------------
str_ = st[st.rule.isin(reps)]
n_entries = len(str_); n_unres = int((str_.resolved == 0).sum())
M("StatEntries", str(n_entries)); M("StatUnresolved", str(n_unres))
M("StatUnresolvedRules", ", ".join(str(r) for r in sorted(str_[str_.resolved == 0].rule.unique())))
M("StatUnresolvedEpsMax", fmt(str_[str_.resolved == 0].eps.max(), 3) if n_unres else "--")
M("StatMaxResidual", f"{str_.residual.max():.1e}")
M("StatMaxCheckDevResolved", f"{str_[str_.resolved == 1].check_max_dev.max():.1e}")
M("EpsGrid", ", ".join(f"{e:g}" for e in sorted(st.eps.unique())) + ", 0.5")
M("EpsGridN", str(st.eps.nunique() + 1))
# symmetry check over all 256 rules (if the 'rest' stage has run)
if st.rule.nunique() == 256:
    from eca_noise import reflect_rule, complement_rule
    # nu permutes under the symmetries: reflection c=(a,b,d)->(d,b,a); complement c->7-c
    def perm_ref(nu):
        out = np.zeros(8)
        for c in range(8):
            a, b, d = (c >> 2) & 1, (c >> 1) & 1, c & 1
            out[4 * d + 2 * b + a] = nu[c]
        return out
    def perm_comp(nu):
        return nu[::-1].copy()
    nu_cols = [f"nu{c}" for c in range(8)]
    worst = 0.0; n_pairs = 0
    resolved_rep = {(int(r), float(e)): int(v) for r, e, v in zip(st.rule, st.eps, st.resolved)}
    table = {(int(r), float(e)): row[nu_cols].values.astype(float) for (r, e), row in st.set_index(["rule", "eps"]).iterrows()}
    for rule in range(256):
        rep = int(z.loc[z.rule == rule, "rep"].iloc[0])
        for name, fn in [("ref", reflect_rule), ("comp", complement_rule), ("refcomp", lambda r: reflect_rule(complement_rule(r)))]:
            image = fn(rule)
            for eps in sorted(st.eps.unique()):
                if resolved_rep.get((rep, float(eps)), 0) != 1:
                    continue                       # only entries whose class representative is resolved
                nu_src = table[(rule, float(eps))]
                nu_pred = perm_ref(nu_src) if name == "ref" else (perm_comp(nu_src) if name == "comp" else perm_comp(perm_ref(nu_src)))
                worst = max(worst, float(np.abs(table[(image, float(eps))] - nu_pred).max())); n_pairs += 1
    M("SymmetryWorstDev", f"{worst:.1e}"); M("SymmetryPairs", f"{n_pairs:,}")
    M("SymmetryChecked", "yes")
else:
    M("SymmetryWorstDev", "n/a"); M("SymmetryPairs", "n/a"); M("SymmetryChecked", "no")

# small-noise trend from the two smallest RESOLVED grid points of each representative
trend = {}
for rule, g in str_[str_.resolved == 1].sort_values("eps").groupby("rule"):
    trend[rule] = float(g.rho.values[1] / g.rho.values[0])      # < 1: rho rising as eps -> 0
es = es.copy(); es["trend_ratio"] = es.rule.map(trend); es["rising"] = (es.trend_ratio < 1).astype(int)
# eps* statistics over classes
esr = es[es.rule.isin(reps)].set_index("rule")
interior = esr[(esr.interior_max == 1) & (esr.rising == 0)]      # interior maximum, curve falling as eps -> 0
boundary = esr[esr.interior_max == 0]
M("NumInterior", str(len(interior))); M("NumBoundaryMax", str(len(boundary)))
M("NumInteriorB", str(int((interior.limit_type == "B_proved").sum())))
M("NumInteriorU", str(int((interior.limit_type == "undetermined").sum())))
M("NumBoundaryB", str(int((boundary.limit_type == "B_proved").sum())))
M("NumBoundaryU", str(int((boundary.limit_type == "undetermined").sum())))
M("EpsStarMin", fmt(interior.eps_star.min(), 3)); M("EpsStarMax", fmt(interior.eps_star.max(), 3))
M("EpsStarMedian", fmt(interior.eps_star.median(), 3))
M("EpsStarMinRule", str(int(interior.eps_star.idxmin()))); M("EpsStarMaxRule", str(int(interior.eps_star.idxmax())))
M("RhoStarMin", fmt(interior.rho_star.min(), 4)); M("RhoStarMax", fmt(interior.rho_star.max(), 3))
M("RhoStarMinRule", str(int(interior.rho_star.idxmin()))); M("RhoStarMaxRule", str(int(interior.rho_star.idxmax())))
from scipy.stats import spearmanr
_mi = interior.join(zr[["frac_full_identification", "mean_class_size"]])
def _sci(x):
    m, e = f"{x:.0e}".split("e"); return f"{m}\\cdot10^{{{int(e)}}}"
M("SpearmanEpsStarFrac", f"${spearmanr(_mi.frac_full_identification, _mi.eps_star).statistic:+.2f}$")
M("SpearmanEpsStarClass", f"${spearmanr(_mi.mean_class_size, _mi.eps_star).statistic:+.2f}$")
M("SpearmanPFrac", _sci(spearmanr(_mi.frac_full_identification, _mi.eps_star).pvalue))
M("SpearmanPClass", _sci(spearmanr(_mi.mean_class_size, _mi.eps_star).pvalue))
M("ArgminSevenCount", str(int((interior.argmin_code_star == 7).sum())))
M("ArgminZeroCount", str(int((interior.argmin_code_star == 0).sum())))
M("NumSignChangesGtOne", str(int((esr.sign_changes > 1).sum())))
M("SignChangesGtOneRules", ", ".join(str(r) for r in esr[esr.sign_changes > 1].index))
M("NumRisingB", str(int(((esr.limit_type == "B_proved") & (esr.rising == 1)).sum())))
M("NumRisingU", str(int(((esr.limit_type == "undetermined") & (esr.rising == 1)).sum())))
M("NumFallingU", str(int(((esr.limit_type == "undetermined") & (esr.rising == 0)).sum())))
M("NumRisingUInterior", str(int(((esr.limit_type == "undetermined") & (esr.rising == 1) & (esr.interior_max == 1)).sum())))
M("RisingUInteriorRules", ", ".join(str(r) for r in esr[(esr.limit_type == "undetermined") & (esr.rising == 1) & (esr.interior_max == 1)].index))
M("RisingTrendMin", fmt(esr[esr.rising == 1].trend_ratio.min(), 3)); M("RisingTrendMax", fmt(esr[esr.rising == 1].trend_ratio.max(), 3))
_trend_eps = {}
for rule, g in str_[str_.resolved == 1].sort_values("eps").groupby("rule"):
    _trend_eps[rule] = (float(g.eps.values[0]), float(g.eps.values[1]))
_late = {r: v for r, v in _trend_eps.items() if v[0] > 0.001}
M("TrendLateRules", ", ".join(f"{r} ({v[0]:g}/{v[1]:g})" for r, v in sorted(_late.items())))
M("TrendSecondEpsMax", f"{max(v[1] for v in _trend_eps.values()):g}")
M("FallingUTrendMin", fmt(esr[(esr.limit_type == "undetermined") & (esr.rising == 0)].trend_ratio.min(), 3))
M("FallingBTrendMin", fmt(esr[(esr.limit_type == "B_proved")].trend_ratio.min(), 3))
# the classes with nu_c = n/8 at every grid point (coinciding curves rho = (n/8) lambda)
nu_cols = [f"nu{c}" for c in range(8)]
flat = sorted(int(r) for r, g in str_.groupby("rule") if (np.abs(g[nu_cols].values - 1.5) < 1e-9).all())
M("UniformMarginalRules", ", ".join(str(r) for r in flat)); M("NumUniformMarginal", str(len(flat)))
M("UniformMarginalMaxDev", f"{max(np.abs(str_[str_.rule.isin(flat)][nu_cols].values - 1.5).max(), 0):.1e}")
add = pd.read_csv(os.path.join(DATA, "additive_rules.csv")).set_index("rule")
bij = [r for r in flat if r in add.index and add.loc[r, "bijective"] == 1]
aff = [r for r in flat if r in add.index and add.loc[r, "bijective"] == 0 and add.loc[r, "affine"] == 1]
other = [r for r in flat if r not in bij and r not in aff]
assert not other, other
M("BijectiveRules", ", ".join(str(r) for r in bij)); M("NumBijective", str(len(bij)))
M("AffineNonBijRules", ", ".join(str(r) for r in aff)); M("NumAffineNonBij", str(len(aff)))
M("AffineKernelDims", ", ".join(str(int(add.loc[r, "kernel_dim"])) for r in aff))
M("AffineBadCharacters", str(int(sum(add.loc[r, "bad_characters"] for r in aff))))
M("AffineMinPi", f"{str_[str_.rule.isin(aff) & (str_.eps == 0.1)].min_pi.min():.1e}")
M("UniformMarginalRhoSmall", fmt(str_[(str_.rule == flat[0]) & (str_.eps == 0.001)].rho.iloc[0], 3) if flat else "--")
M("LambdaSmall", fmt(str_[str_.eps == 0.001]["lambda"].iloc[0], 3))
M("NumRefineUnresolved", str(int((interior.refine_resolved == 0).sum())))
M("BoundaryMaxRules", ", ".join(str(r) for r in boundary.index))
# rule 0 analytic check: nu_7 = 12 eps^3
r0 = st[(st.rule == 0)].sort_values("eps")
M("RuleZeroNuSevenCheck", f"{np.abs(r0.nu7.values - 12 * r0.eps.values**3).max():.1e}")
M("RuleZeroEpsStar", fmt(esr.loc[0, "eps_star"], 3)); M("RuleZeroRhoStar", fmt(esr.loc[0, "rho_star"], 4))
M("RuleZeroStepsPerNat", str(int(round(1.0 / esr.loc[0, "rho_star"]))))
RULE_WORD = {30: "Thirty", 110: "OneTen", 204: "TwoOhFour", 232: "TwoThreeTwo", 128: "OneTwoEight", 18: "Eighteen", 90: "Ninety"}
for rule, word in RULE_WORD.items():
    row = esr.loc[rule]
    M(f"EpsStarRule{word}", fmt(row.eps_star, 3) if row.interior_max == 1 else "--")
    M(f"RhoStarRule{word}", fmt(row.rho_star, 3) if row.interior_max == 1 else "--")
    M(f"TypeRule{word}", "B" if row.limit_type == "B_proved" else "U")
    M(f"RhoSmallRule{word}", fmt(str_[(str_.rule == rule) & (str_.eps == 0.001)].rho.iloc[0], 3))
    M(f"RhoMidRule{word}", fmt(str_[(str_.rule == rule) & (str_.eps == 0.1)].rho.iloc[0], 3))
# rate at smallest eps vs at 0.002 for the undetermined classes with boundary max: ratio
u_b = esr[(esr.limit_type == "undetermined") & (esr.interior_max == 0)]
M("UndetBoundaryRatioMin", fmt(u_b.rho_ratio_0002_over_0001.min(), 3) if len(u_b) else "--")
M("UndetBoundaryRatioMax", fmt(u_b.rho_ratio_0002_over_0001.max(), 3) if len(u_b) else "--")
# the largest rho on the grid overall
M("GridMaxRhoOverall", fmt(str_.rho.max(), 3)); M("GridMaxRhoRule", str(int(str_.loc[str_.rho.idxmax(), "rule"])))
M("GridMaxRhoEps", fmt(str_.loc[str_.rho.idxmax(), "eps"], 3))

# ---------------- finite horizon ----------------
fhr = fh[fh.rule.isin(reps)]
def fh_val(eps, T, col):
    return fhr[(fhr.eps == eps) & (fhr["T"] == T)][col].mean()
EPS_TAG = {0.005: "a", 0.01: "b", 0.05: "c", 0.1: "d", 0.2: "e"}   # letters only: LaTeX macro names
T_TAG = {8: "A", 16: "B", 32: "C", 64: "D"}
for eps, et in EPS_TAG.items():
    for T, tt in T_TAG.items():
        M(f"FHall{et}{tt}", fmt(100 * fh_val(eps, T, "frac_m_above_ln100"), 1))
        M(f"FHgt{et}{tt}", fmt(100 * fh_val(eps, T, "frac_m_zero_class_gt1"), 1))
M("FHlnThreshold", fmt(np.log(100), 2))
fhs = pd.read_csv(os.path.join(DATA, "finite_horizon_per_state.csv.gz"))
fhs = fhs[fhs.rule.isin(reps)]
for eps, et in EPS_TAG.items():
    col = f"m32_eps{eps}"
    gt1 = fhs.class_size_eps0 > 1
    M(f"FHpooledGt{et}C", fmt(100 * (fhs.loc[gt1, col] >= np.log(100)).mean(), 1))
    M(f"FHpooledAll{et}C", fmt(100 * (fhs[col] >= np.log(100)).mean(), 1))
M("FHnonIdStatesPerClassMin", str(int(fhs[fhs.class_size_eps0 > 1].groupby("rule").size().min())))
M("FHnonIdStatesPerClassMax", str(int(fhs[fhs.class_size_eps0 > 1].groupby("rule").size().max())))
# eps maximizing the worst-case margin at T=32
t32 = fhr[fhr["T"] == 32]
best = t32.loc[t32.groupby("rule")["m_min"].idxmax()]
M("FHbestEpsHist", ", ".join(f"$\\varepsilon={e:g}$: {c}" for e, c in best.eps.value_counts().sort_index().items()))
M("FHbestEpsMedian", f"{best.eps.median():g}")

# ---------------- boundary check ----------------
for gname, tag in [("majority5", "Maj"), ("parity5", "Par"), ("rule110_defect10101", "Def")]:
    d = r2[r2.generator == gname].sort_values("eps"); zz = r2z[r2z.generator == gname].iloc[0]
    M(f"Rii{tag}Silent", fmt(100 * zz.frac_silent, 1))
    M(f"Rii{tag}DetectMean", fmt(zz.mean_detect_time, 2)); M(f"Rii{tag}DetectMax", str(int(zz.max_detect_time)))
    M(f"Rii{tag}SilentClass", fmt(zz.mean_silent_class_size, 2))
    M(f"Rii{tag}GstarSmall", str(int(d.iloc[0].g_star)))
    M(f"Rii{tag}GstarAll", "yes" if d.g_star.nunique() == 1 else "no")
    M(f"Rii{tag}RatioMid", fmt(d[d.eps == 0.01].ratio_apparent_to_misfit.iloc[0], 1))
    M(f"Rii{tag}RatioSmall", fmt(d[d.eps == 0.001].ratio_apparent_to_misfit.iloc[0], 1))
    M(f"Rii{tag}RatioLarge", fmt(d[d.eps == 0.2].ratio_apparent_to_misfit.iloc[0], 2))
    M(f"Rii{tag}MisfitMax", fmt(d.misfit_per_step.max(), 3)); M(f"Rii{tag}MarginMax", fmt(d.apparent_margin.max(), 3))
    cross = d[d.misfit_rate > d.apparent_rate]
    M(f"Rii{tag}CrossEps", f"{cross.eps.min():g}" if len(cross) else "--")

# ---------------- class summary (used by make_figures.py) ----------------
_cs = esr.reset_index()[["rule", "limit_type", "rising", "interior_max", "eps_star", "rho_star", "trend_ratio"]]
_cs.to_csv(os.path.join(DATA, "class_summary.csv"), index=False)

# ---------------- manifest ----------------
files = sorted(f for f in os.listdir(DATA) if f.endswith((".csv", ".csv.gz")))
with open(os.path.join(DATA, "MANIFEST.sha256"), "w") as fh_:
    for f in files:
        h = hashlib.sha256(open(os.path.join(DATA, f), "rb").read()).hexdigest()
        fh_.write(f"{h}  {f}\n")
M("ManifestFiles", str(len(files)))

with open(os.path.join(NOTE, "numbers.tex"), "w") as fh_:
    fh_.write("% generated by code/make_numbers.py -- do not edit\n")
    for k, v in macros.items():
        fh_.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")

# ---------------- per-class table ----------------
rows = []
for rule in reps:
    zz = zr.loc[rule]; ee = esr.loc[rule]
    typ = "B" if zz.limit_type == "B_proved" else "U"
    if ee.interior_max == 1 and ee.rising == 0:
        es_s = f"{ee.eps_star:.3f}"; rs_s = f"{ee.rho_star:.3f}"
    elif ee.interior_max == 1 and ee.rising == 1:
        es_s = f"{ee.eps_star:.3f}$^\\dagger$"; rs_s = f"{ee.rho_star:.3f}$^\\dagger$"
    else:
        es_s = "$\\to 0$"; rs_s = "--"
    rows.append(f"{rule} & {typ} & {100*zz.frac_full_identification:.1f} & {zz.mean_class_size:.2f} & {int(zz.max_tau)} & {int(zz.n_cycles)} & {int(zz.cycle_union_size)} & {es_s} & {rs_s} \\\\")
half = (len(rows) + 1) // 2
with open(os.path.join(NOTE, "table_classes.tex"), "w") as fh_:
    fh_.write("% generated by code/make_numbers.py -- do not edit\n")
    hdr = "$f$ & type & id.\\,\\% & $\\overline{|C_\\infty|}$ & $\\tau_{\\max}$ & cycles & $|\\bigcup N|$ & $\\varepsilon^*$ & $\\rho^*$"
    fh_.write("\\begin{tabular}{@{}rcrrrrrrr@{}}\\toprule\n" + hdr + "\\\\\\midrule\n")
    fh_.write("\n".join(rows[:half]) + "\n\\bottomrule\\end{tabular}\\hspace{1.2em}\n")
    fh_.write("\\begin{tabular}{@{}rcrrrrrrr@{}}\\toprule\n" + hdr + "\\\\\\midrule\n")
    fh_.write("\n".join(rows[half:]) + "\n\\bottomrule\\end{tabular}\n")
print("wrote", len(macros), "macros and the class table")
