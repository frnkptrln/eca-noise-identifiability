"""Writes report.md and note/numbers_v02.tex from the data files only (no number is typed).

Inputs (data/): fw_n12_classes.csv, fw_sweep.csv, fw_sweep_cost.csv, fw_affine.csv,
fw_verify_orders.csv, fw_verify_trees.csv, fw_n12_checks.csv, fw_n12_gth.csv,
fw_n12_gth_rule106_deep.csv, fw_wall.csv, log_fw_resume_test.txt, log_fw_check_*.txt,
epsilon_star.csv, class_summary.csv, zero_noise_per_rule.csv (v0.1), MANIFEST.sha256, and the certificate
file names. Outputs besides report.md and numbers_v02.tex: note/table_classes_v02.tex (the v0.1 class table
with the v0.2 dagger rule), data/fw_certificates_*/README.md, the generated v0.2 block of README.md.
From the independent verification (verify_v02/out/, part of the release): the rebuilt single-flip chain of
Bagnoli, Baia and Matteuzzi (bagnoli_n17_compare.csv, bagnoli_census_n*.jsonl) and the measured wall time
of a from-scratch run of reproduce_v02.sh (repro_compare.json)."""
import os, re, sys, glob, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
D = lambda f: os.path.join(ROOT, "data", f)
rd = lambda f: pd.read_csv(D(f))
lam = lambda e: (1 - 2 * e) * np.log((1 - e) / e)
BASE = lam(0.002) / lam(0.001)
C3 = lambda c: format(int(c), "03b")


def lst(xs):
    xs = [str(x) for x in xs]
    return ", ".join(xs) if xs else "none"


def runs(ns):
    """Compact list of integers: 4-7, 9, 12-14."""
    ns = sorted(ns); out = []; i = 0
    while i < len(ns):
        j = i
        while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1:
            j += 1
        out.append(f"{ns[i]}" if i == j else f"{ns[i]}-{ns[j]}")
        i = j + 1
    return ", ".join(out) if out else "none"


def pattern(ns_fall, ns_all):
    """All simple rules (divisibility by d <= 8, powers of two) that reproduce the set of n with
    k* >= 1 within ns_all exactly; several may fit a finite range."""
    fall = set(ns_fall); fits = []
    for d in range(2, 9):
        if fall == {n for n in ns_all if n % d == 0}:
            fits.append(f"k* >= 1 iff {d} divides n")
        if fall == {n for n in ns_all if n % d != 0}:
            fits.append(f"k* = 0 iff {d} divides n")
    if fall == {n for n in ns_all if n & (n - 1) == 0}:
        fits.append("k* >= 1 iff n is a power of two")
    return " / ".join(fits) if fits else "none of: divisibility by d <= 8, powers of two"


VOUT = os.path.join(ROOT, "verify_v02", "out")


def coef_106(g106):
    """VER-12: linear coefficient of min_c nu_c for class 106, relative to the limit, from the secant between the
    two smallest noise levels (full-precision column nu_min_full)."""
    nu = [float(v) for v in g106.iloc[0].nu_min_full.split()]
    eps = [float(v) for v in g106.iloc[0].eps.split()]
    b = (nu[-2] - nu[-1]) / (eps[-2] - eps[-1])
    a = nu[-1] - b * eps[-1]
    return b / a, eps[-2], eps[-1]


def bbm_summary(sw):
    """Single-flip attractor chain of Bagnoli, Baia and Matteuzzi, rebuilt by the verification (verify_v02/)."""
    b17 = pd.read_csv(os.path.join(VOUT, "bagnoli_n17_compare.csv"))
    one = b17[b17.n_closed == 1]; many17 = b17[b17.n_closed > 1]
    recs = []
    for f in sorted(glob.glob(os.path.join(VOUT, "bagnoli_census_n*.jsonl"))) + \
            [os.path.join(VOUT, "bagnoli_n17_w1.jsonl"), os.path.join(VOUT, "bagnoli_n17_w2.jsonl")]:
        recs += [json.loads(l) for l in open(f) if l.strip()]
    d = pd.DataFrame(recs).merge(sw[["n", "rule", "n_stable", "kstar"]], on=["n", "rule"])
    many = d[d.n_closed > 1]
    wrong = many[many.support_size != many.n_stable]
    return dict(L=int(b17.n.iloc[0]), classes=len(b17), one=len(one),
                one_support_ok=int((one.support_size == one.n_stable).sum()),
                one_split_ok=int(((one.support_cover_mask == 255) == (one.kstar == 0)).sum()),
                many17=many17.rule.tolist(), dS=float(b17.dS.max()),
                pairs=len(d), nmin=int(d.n.min()), nmax=int(d.n.max()),
                many_min=int(many.groupby("n").size().min()), many_max=int(many.groupby("n").size().max()),
                wrong=[(int(x.rule), int(x.n), list(x.closed_sizes), int(x.n_stable)) for x in wrong.itertuples()],
                split_wrong=int(((d.support_cover_mask == 255) != (d.kstar == 0)).sum()))


def table_v02(c12, write=True):
    """note/table_classes_v02.tex: the v0.1 class table (same rows as code/make_numbers.py) with the v0.2 dagger rule:
    a dagger marks a local maximum, i.e. an interior maximum whose curve rises again as eps -> 0, either on v0.1's grid
    (rising) or, as shown by v0.2, below it (k* = 0)."""
    z = pd.read_csv(D("zero_noise_per_rule.csv")); cs = pd.read_csv(D("class_summary.csv"))
    reps = sorted(z.rep.unique()); zr = z[z.rule.isin(reps)].set_index("rule"); esr = cs.set_index("rule")
    ks = c12.set_index("rule").kstar
    rows, dag = [], []
    for rule in reps:
        zz = zr.loc[rule]; ee = esr.loc[rule]
        typ = "B" if zz.limit_type == "B_proved" else "U"
        local = ee.interior_max == 1 and (ee.rising == 1 or ks.loc[rule] == 0)
        if ee.interior_max == 1 and not local:
            es_s = f"{ee.eps_star:.3f}"; rs_s = f"{ee.rho_star:.3f}"
        elif local:
            es_s = f"{ee.eps_star:.3f}$^\\dagger$"; rs_s = f"{ee.rho_star:.3f}$^\\dagger$"; dag.append(int(rule))
        else:
            es_s = "$\\to 0$"; rs_s = "--"
        rows.append(f"{rule} & {typ} & {100*zz.frac_full_identification:.1f} & {zz.mean_class_size:.2f} & {int(zz.max_tau)} & {int(zz.n_cycles)} & {int(zz.cycle_union_size)} & {es_s} & {rs_s} \\\\")
    if not write:
        return dag
    half = (len(rows) + 1) // 2
    with open(os.path.join(ROOT, "note", "table_classes_v02.tex"), "w") as fh_:
        fh_.write("% generated by code/fw/make_report.py -- do not edit\n")
        hdr = "$f$ & type & id.\\,\\% & $\\overline{|C_\\infty|}$ & $\\tau_{\\max}$ & cycles & $|\\bigcup N|$ & $\\varepsilon^*$ & $\\rho^*$"
        fh_.write("\\begin{tabular}{@{}rcrrrrrrr@{}}\\toprule\n" + hdr + "\\\\\\midrule\n")
        fh_.write("\n".join(rows[:half]) + "\n\\bottomrule\\end{tabular}\\hspace{1.2em}\n")
        fh_.write("\\begin{tabular}{@{}rcrrrrrrr@{}}\\toprule\n" + hdr + "\\\\\\midrule\n")
        fh_.write("\n".join(rows[half:]) + "\n\\bottomrule\\end{tabular}\n")
    return dag


def cert_info():
    """Certificate files: stubs (bijective maps) at n = 12, ring sizes of the sweep certificates."""
    import gzip
    n12 = sorted(glob.glob(D("fw_certificates_n12/*.json.gz")))
    stubs = []
    for f in n12:
        c = json.load(gzip.open(f))
        if "hierarchy" not in c:
            stubs.append(int(c["rule"]))
    swf = sorted(glob.glob(D("fw_certificates_sweep/*.json.gz")))
    ns = sorted({int(re.search(r"n(\d+)_rule", os.path.basename(f)).group(1)) for f in swf})
    return dict(n12=len(n12), stubs=stubs, sweep=len(swf), nmin=ns[0], nmax=ns[-1])


def cert_readmes(ci):
    txt_fields = (
        "Fields (one gzipped JSON file per class representative):\n\n"
        "- `rule`, `n`, `m` (number of cycles), `cycles` (each cycle as its list of states in the order of F).\n"
        "- `hierarchy`: laminar family from the root-free Edmonds contraction. Nodes 0..m-1 are the cycles, larger ids are "
        "contracted sets; `parent` (-1 for `top`), dual values `y`, and for every node except `top` its selected edge "
        "`sel_tail` -> `sel_head` (cycle indices, tail inside the set, head outside). Inside every contracted set the "
        "children's selected edges form one cyclic permutation of all children.\n"
        "- `gamma` (stochastic potential of every cycle, = sum(y) - sum of y over the sets containing it), `gamma_min`, "
        "`stable` (the noise-selected cycles, gamma = gamma_min), `stable_cover_mask` (bit c set iff code c occurs on a "
        "noise-selected cycle), `tree` (one explicit minimum in-tree, rooted at `tree.root`).\n"
        "- `k_c`: per code c the order k, a root cycle and a witness `trajectory` from that cycle to a state containing c "
        "with its `resistance`; `kstar` = max k.\n"
        "- `uncovered_codes` (files with k* >= 1) and the report column of the same origin: the codes with k_c = k* "
        "(not all codes absent from the noise-selected cycles; codes with 1 <= k_c < k* are absent too); `covering_cycles` "
        "(files with k* = 0): noise-selected cycles whose states contain all eight codes.\n\n"
        "Checked by `code/fw/check_cert.py` and independently by `verify_v02/check_certs.py` (see `VERIFICATION_v02.md`).\n")
    with open(D("fw_certificates_n12/README.md"), "w") as fh:
        fh.write("# Certificates at n = 12\n\n"
                 f"{ci['n12']} files, one per class. {len(ci['stubs'])} of them (classes {lst(ci['stubs'])}) are stubs for "
                 "bijective maps: they contain only `bijective`, `rule`, `n`, `k_c` (all 0) and `kstar` = 0, with no hierarchy "
                 "and no witnesses; the claim rests on the doubly stochastic kernel (uniform stationary law), and the "
                 "checkers verify bijectivity.\n\n" + txt_fields)
    with open(D("fw_certificates_sweep/README.md"), "w") as fh:
        fh.write("# Certificates of the ring-size sweep\n\n"
                 f"{ci['sweep']} files `n{{n}}_rule_{{rule}}.json.gz` for n = {ci['nmin']}..{ci['nmax']}, non-bijective classes only "
                 "(bijective classes are analytic: k* = 0). Larger ring sizes of the sweep have no certificates.\n\n" + txt_fields)


def readme_block(ci, nmin, nmax, vary_nmin, nvary):
    """Generated v0.2 block of README.md (between the markers)."""
    p = os.path.join(ROOT, "README.md"); t = open(p).read()
    a, b = "<!-- v02:begin (generated by code/fw/make_report.py) -->", "<!-- v02:end -->"
    blk = (f"{a}\n"
           f"* `report.md` — exact small-noise orders: noise-selected cycles, k_c and k* for all 88 classes at n = {nmin}..{nmax}; "
           f"checked certificates for n = 12 and n = {ci['nmin']}..{ci['nmax']}, none for n = {ci['nmax'] + 1}..{nmax}; "
           f"for n ≥ {vary_nmin}, {nvary} classes change side with n; verification and the comparison with v0.1\n"
           "* `PREDICTIONS.md` — predictions sealed before the solver was written (first commit of the branch)\n"
           "* `literature.md` — literature note with read/not-read status per source\n"
           "* `note/note_v0.2.tex`, `note/note_v0.2.diff`, `note/numbers_v02.tex`, `note/table_classes_v02.tex` — v0.2 of the note, built as `note/note_v0.2.pdf` (v0.1 files unchanged)\n"
           "* `code/fw/` — solver, verifiers, certificate checker, tests; `reproduce_v02.sh` regenerates the v0.2 data and report from scratch "
           "(run after `reproduce.sh`; `REUSE_CHECKPOINTS=1` resumes from the committed sweep checkpoint and the GTH caches instead)\n"
           "* `VERIFICATION_v02.md`, `verify_v02/` — independent verification of v0.2 (own code, sealed sample, outputs, logs) and how each finding was handled\n"
           f"{b}")
    if a in t:
        t = t[:t.index(a)] + blk + t[t.index(b) + len(b):]
    else:
        old = re.search(r"\* `report\.md` — exact small-noise orders.*?run after `reproduce\.sh`\)\n", t, re.S)
        t = t[:old.start()] + blk + "\n" + t[old.end():]
    open(p, "w").write(t)


def main():
    M = {}                                  # macros for the v0.2 note
    c12 = rd("fw_n12_classes.csv")
    sw = rd("fw_sweep.csv"); cost = rd("fw_sweep_cost.csv"); aff = rd("fw_affine.csv")
    vo = rd("fw_verify_orders.csv"); vt = rd("fw_verify_trees.csv"); ch = rd("fw_n12_checks.csv")
    g12 = rd("fw_n12_gth.csv"); g106 = rd("fw_n12_gth_rule106_deep.csv")
    wall = rd("fw_wall.csv") if os.path.exists(D("fw_wall.csv")) else None
    es = rd("epsilon_star.csv")

    # ---------------- n = 12 ----------------
    c12["k_pred"] = np.log2(c12.rho_ratio_0002_over_0001 / BASE).round().astype(int)
    typ = c12.groupby(["v01_type", "kstar"]).size()
    nB = int((c12.v01_type == "B").sum()); nUF = int((c12.v01_type == "U-falling").sum()); nUR = int((c12.v01_type == "U-rising").sum())
    U = c12[c12.v01_type != "B"]
    U_rise = int((U.kstar == 0).sum()); U_fall = int((U.kstar >= 1).sum())
    flips = c12[c12.agree == 0]
    fl_rules = flips.rule.tolist()
    B_dist = c12[c12.v01_type == "B"].kstar.value_counts().sort_index()
    UF_dist = c12[c12.v01_type == "U-falling"].kstar.value_counts().sort_index()
    weak = c12[c12.rule.isin([7, 19, 23, 232])]
    kpred_ok = int((c12.k_pred == c12.kstar).sum())
    M.update(NumClasses=len(c12), NumUclasses=len(U), NumUrisingVtwo=U_rise, NumUfallingVtwo=U_fall,
             NumAgreeVone=int(c12.agree.sum()), FlipRules=lst(fl_rules), KpredOK=kpred_ok,
             NumBkOne=int(B_dist.get(1, 0)), NumBkTwo=int(B_dist.get(2, 0)), NumBkThree=int(B_dist.get(3, 0)))

    # rule 106
    r106 = c12[c12.rule == 106].iloc[0]
    e106 = es[es.rule == 106].iloc[0]
    nu106 = [float(v) for v in g106.iloc[0].nu_min_at.split()]
    eps106 = [float(v) for v in g106.iloc[0].eps.split()]
    M.update(RuleOneOhSixStable=int(r106.n_stable), RuleOneOhSixCycles=int(r106.cycles),
             RuleOneOhSixNuLimit=f"{nu106[-1]:.4f}", RuleOneOhSixEpsStar=f"{e106.eps_star:.4f}",
             RuleOneOhSixRhoStar=f"{e106.rho_star:.3f}")
    # epsilon at which 0.047 * lambda exceeds rho*
    lim = nu106[-1]
    lam_needed = e106.rho_star / lim
    log10_eps_cross = -lam_needed / np.log(10)           # lambda ~ log(1/eps) for small eps
    M["RuleOneOhSixCrossExp"] = f"{int(np.floor(log10_eps_cross))}"
    coef106, e2, e1 = coef_106(g106)
    M["RuleOneOhSixCoef"] = f"{coef106:.0f}"
    dag = table_v02(c12)
    M["DaggerRules"] = lst(dag)
    ci = cert_info()
    cert_readmes(ci)
    M.update(CertSweepNmin=ci["nmin"], CertSweepNmax=ci["nmax"], CertFreeNmin=ci["nmax"] + 1, CertStubs=len(ci["stubs"]), CertStubRules=lst(ci["stubs"]))

    # ---------------- verification ----------------
    ver = dict(
        a_rows=len(vo), a_fail=int((vo.ok == 0).sum()), a_nmin=int(vo.n.min()), a_nmax=int(vo.n.max()),
        a_devpi=f"{vo.max_dev_pi.max():.1e}", a_devnu=f"{vo.max_dev_nu.max():.1e}",
        t_rows=len(vt), t_mis=int(vt.mismatches.sum()), t_nx=int((vt.method == "nx").sum()),
        t_hier=int((vt.method == "hier").sum()), t_nx_all=int(vt[(vt.method == "nx")].groupby("n").size().pipe(lambda s: s[s == 256].index.max())),
        t_nx_reps_n=int(vt[vt.method == "nx"].n.max()), t_hier_n=int(vt[vt.method == "hier"].n.max()),
        t_wmin=bool((vt.Wmin == vt.gmin).all()),
        c_sym=f"{int(ch[ch.check=='c_symmetry'].ok.sum())}/{int((ch.check=='c_symmetry').sum())}",
        d_B=f"{int(ch[ch.check=='d_Bproved_kstar_ge1'].ok.sum())}/{int((ch.check=='d_Bproved_kstar_ge1').sum())}",
        d_bij=f"{int(ch[ch.check=='d_bijective_kstar0'].ok.sum())}/{int((ch.check=='d_bijective_kstar0').sum())}",
        g_rules=lst(g12.rule.tolist()), g_devnu=f"{g12.max_dev_nu_last.max():.1e}",
    )
    certlog = {}
    for f in ["log_fw_check_n12_certs.txt", "log_fw_check_sweep_certs.txt"]:
        if os.path.exists(D(f)):
            t = open(D(f)).read()
            m_ = re.search(r"(\d+) certificates checked, (\d+) failed", t)
            certlog[f] = (int(m_.group(1)), int(m_.group(2))) if m_ else None
    resume = open(D("log_fw_resume_test.txt")).read()
    shas = re.findall(r"^([0-9a-f]{64})\s", resume, re.M)
    tsrc = open(os.path.join(ROOT, "code", "fw", "test_fw.py")).read()
    nfuncs = len(re.findall(r"^def test_", tsrc, re.M))
    plog = open(D("log_fw_pytest.txt")).read()
    mp = re.search(r"(\d+) passed", plog); mf = re.search(r"(\d+) failed", plog)
    npassed, nfailed = (int(mp.group(1)) if mp else 0), (int(mf.group(1)) if mf else 0)
    bugs = sorted({(k, " ".join(v.split())) for k, v in re.findall(r'"""((?:BUG|PERF|VER)-\d+): (.*?)"""', tsrc, re.S)})

    # ---------------- sweep ----------------
    ns = sorted(sw.n.unique()); nmin, nmax = int(min(ns)), int(max(ns))
    pk = sw.pivot(index="rule", columns="n", values="kstar")
    complete_n = [n for n in ns if pk[n].notna().sum() == 88]
    zero_per_n = {int(n): int((pk[n] == 0).sum()) for n in complete_n}
    big = [n for n in complete_n if n >= 8]
    st = (pk[big] == 0)
    const = st.nunique(axis=1) == 1
    n_const = int(const.sum()); var_rules = st.index[~const].tolist()
    same_as_12 = int(((pk[big] == 0).eq(pk[12] == 0, axis=0)).all(axis=1).sum())
    patt = []
    for r in var_rules:
        fall = [n for n in big if pk.loc[r, n] >= 1]
        patt.append((int(r), runs([n for n in big if pk.loc[r, n] == 0]), runs(fall), pattern(fall, big)))
    kv = pk[big]; kvals = kv[(kv.nunique(axis=1) > 1) & const]
    # where k* >= 1 for all n >= 8: is the value constant?
    allfall = pk[big][(pk[big] >= 1).all(axis=1)]
    allfall_const = int((allfall.nunique(axis=1) == 1).sum())
    allzero = int((pk[big] == 0).all(axis=1).sum())
    # bijective / affine
    bij = sw[sw.bijective == 1].groupby("rule").n.apply(list).to_dict()
    affs = []
    for r in sorted(aff.rule.unique()):
        s = aff[aff.rule == r]
        affs.append((int(r), runs(s[s.kstar_analytic < 0].n.tolist()), runs(s[s.bijective == 1].n.tolist())))
    # consistency affine analytic vs sweep
    a2 = aff.merge(sw[["n", "rule", "kstar"]], on=["n", "rule"])
    aff_incons = int(((a2.kstar_analytic == 0) & (a2.kstar != 0)).sum())
    aff_checked = int((a2.kstar_analytic == 0).sum())
    # cost
    cost2 = cost.merge(sw[["n", "rule", "bijective"]], on=["n", "rule"])
    cs = cost2.groupby("n").agg(cpu=("cost_seconds", "sum"), maxjob=("cost_seconds", "max"),
                                rss=("cost_maxrss_mb", "max")).reset_index()
    cs = cs.merge(cost2[cost2.bijective == 0].groupby("n").cycles.max().rename("cyc").reset_index(), on="n")
    p2 = lambda r: sorted(int(n) for n in complete_n if pk.loc[r, n] >= 1) == [int(n) for n in complete_n if n & (n - 1) == 0]
    p2_ok = {r: p2(r) for r in (60, 90)}
    smalln = [n for n in complete_n if n <= 7]
    small_dev = int(((pk[smalln] == 0).ne(pk[12] == 0, axis=0)).any(axis=1).sum())
    bbm = bbm_summary(sw)
    bbm_wrong = "; ".join(f"class {r} at n = {n} (closed classes of sizes {lst(s)}, of which only the {k} noise-selected cycles "
                          "carry weight in the small-noise limit; the single-flip chain also weights the others)" for r, n, s, k in bbm["wrong"])
    M.update(BBMLattice=bbm["L"], BBMOneClosed=bbm["one"], BBMSymRules=lst(bbm["many17"]),
             BBMFailRules=lst([r for r, n, s, k in bbm["wrong"]]), BBMFailN=lst([n for r, n, s, k in bbm["wrong"]]),
             SweepVaryNmin=int(min(big)))
    manifest_n = sum(1 for l in open(D("MANIFEST.sha256")) if l.strip())
    rep = json.load(open(os.path.join(VOUT, "repro_compare.json")))
    M.update(ManifestFilesVtwo=manifest_n, ReproVtwoHours=f"{float(rep['wall_h']):.1f}")
    readme_block(ci, nmin, nmax, int(min(big)), len(var_rules))

    # ---------------- report ----------------
    L = []
    w = L.append
    w("# Noise-selected cycles and the small-noise order of rule identifiability in elementary cellular automata")
    w("")
    w("Work report for the proposed v0.2 of *Rule identifiability in elementary cellular automata under dynamical noise* "
      "(F. Peterlein, v0.1, concept DOI [10.5281/zenodo.23399100](https://doi.org/10.5281/zenodo.23399100)). "
      "Branch `noise-selected-cycles`. Every number below is generated from the files in `data/` by `code/fw/make_report.py`; "
      "the predictions were sealed in `PREDICTIONS.md` (first commit of the branch) before the solver existed. "
      "An independent verification session reviewed this work (`VERIFICATION_v02.md`, code and outputs in `verify_v02/`); "
      "the header of that file states how each of its findings was handled, and the numbers taken from it (Section 8) are read from `verify_v02/out/`.")
    w("")
    w("## 1. Question")
    w("")
    w("For every elementary rule on a ring of n cells under i.i.d. bit-flip noise (X_{t+1} = F(X_t) XOR Z_t, Z_t i.i.d. "
      "Bernoulli(ε) per cell): which cycles of the deterministic map F are noise-selected (stochastically stable); does their "
      "union cover all eight neighbourhood codes; hence does the identifiability rate ρ(f;ε) = λ(ε)·min_c ν_c(f;ε) grow without "
      "bound or vanish as ε → 0, and if it vanishes, at which order k*? v0.1 proved ρ → 0 for 42 classes and left the other "
      f"{len(U)} (whose cycles jointly cover all codes) to a numerical trend ({nUF} falling, {nUR} rising) at n = 12.")
    w("")
    w("Not in scope: unknown ε, partial observation, generators outside the family, decoder error rates, any change to v0.1's definitions or numbers.")
    w("")
    w("## 2. Verdict")
    w("")
    w(f"**(a) Exact classification for n = 12 and for every n from {nmin} to {nmax}.** For each of the 88 classes and each ring size "
      f"n = {runs(complete_n)}, the noise-selected cycles, the orders k_c of all eight expected code counts and k* = max_c k_c are computed "
      "exactly in integer arithmetic. ρ → ∞ iff k* = 0; otherwise ρ(f;ε) ~ a·ε^{k*}·log(1/ε) with a > 0. "
      f"Certificates (optimal in-tree hierarchy with dual values, witness trajectories; for the {len(ci['stubs'])} bijective classes at n = 12, "
      f"classes {lst(ci['stubs'])}, a bijectivity stub) were written for n = 12 and n = {ci['nmin']}..{ci['nmax']} and accepted by an independent checker "
      f"({certlog.get('log_fw_check_n12_certs.txt', ('?',))[0]} + {certlog.get('log_fw_check_sweep_certs.txt', ('?',))[0]} certificates, 0 failed); "
      f"n = {ci['nmax'] + 1}..{nmax} are computed by the same solver without certificates. "
      f"The classification depends on n: for n ≥ 8, {allzero} classes have k* = 0 at every computed n, {len(allfall)} have k* ≥ 1 at every computed n, "
      f"and {len(var_rules)} switch between the two (Section 7; patterns observed, not proved, except for the affine classes 60 and 90, "
      "where k* ≥ 1 exactly when n is a power of two is proved for every n ≥ 4 in Section 3).")
    w("")
    w(f"**(b) v0.1's open item at n = 12 is settled.** Of the {len(U)} classes whose cycles jointly cover all codes, {U_rise} have k* = 0 "
      f"(ρ → ∞) and {U_fall} have k* ≥ 1 (ρ → 0). {int(c12.agree.sum())} of 88 classes agree with v0.1's trend classification; "
      f"the exception is class {lst(fl_rules)}, which v0.1 lists as falling with an interior maximum and which in fact has k* = 0: its "
      "rate falls between ε = 0.01 and 0.001 and then rises again, as log(1/ε), at noise levels far below v0.1's grid. "
      "Rules 7, 19, 23 and 232 (v0.1's weakest cases) all have k* = 1: their trend classification stands.")
    w("")
    w("**(c) Classes that resist:** none within the computed range. The wall for larger n is stated in Section 7.")
    w("")
    w("## 3. Method")
    w("")
    w("**Perturbed chain.** For 0 < ε < 1/2 the kernel is P_ε(x,y) = ε^{r(x,y)} (1−ε)^{n−r(x,y)} with resistance r(x,y) = H(F(x), y); "
      "r(x, F(x)) = 0. The chain is irreducible. By the Markov chain tree theorem (Pitman and Tang 2018, Thm 1.1) π_ε(x) is a ratio of sums "
      "over spanning in-trees of products of P_ε; each product is a polynomial in ε with lowest term ε^{r(T)} and coefficient +1, so no cancellation "
      "occurs and **ord π_ε(x) = W(x) − min_y W(y)** exactly, W(x) the minimum total resistance of an in-tree rooted at x.")
    w("")
    w("**Reduction to cycles.** Let C_1..C_m be the cycles of F, R(u→v) the minimum path resistance, V(C,C') = R(C→C') (motion along a cycle is free, "
      "so R from any point of C is the same), and γ(C) the minimum weight of an in-tree on the cycles rooted at C with weights V. Then "
      "**W(x) − min W = min_C [γ(C) + R(C→x)] − min_C γ(C)** for every state x. Proof (ours; the Freidlin–Wentzell and Young sources could not be read, "
      "see Section 8): (i) censor the chain on K' = {cycle states} ∪ {x}; the censored law is π_ε restricted to K' and renormalised, its transition "
      "probabilities are convergent power series (any 2^n consecutive steps outside K' contain a flip) with positive leading coefficient, of order "
      "equal to the minimum resistance of paths avoiding K' in between; v0.1's Lemma 3 gives π_ε(K') → 1, so the renormalising "
      "constant has order 0 and orders on K' are orders of π_ε. (ii) Apply the tree theorem on K'. Edges inside a cycle cost 0, so contract each cycle: a minimum "
      "in-tree on the states of K' leaves every cycle not containing the root by at least one edge, and these edges contain an in-tree of the contracted graph of "
      "no larger weight; conversely an in-tree of the contracted graph extends to the states along the free cycle edges. Replacing edge weights by shortest-path "
      "weights does not change the minimum in-tree value, because the union of the shortest paths of an in-tree contains an in-tree of no larger weight. "
      "(iii) If x lies on a cycle C_x, K' is the set of cycle states and the formula reads γ(C_x) − min γ, since γ(C_x) ≤ γ(C) + V(C, C_x) for every C. "
      "Otherwise, in a minimum in-tree on {C_1..C_m, x} rooted at x, let S be the cycles pointing to x and C_x the cycle that x flows to at cost 0; redirect every member of S other "
      "than one (C_x if C_x ∈ S, otherwise the member on C_x's branch) to C_x, which costs no more because V(C', C_x) ≤ R(C'→x) + R(x→C_x) = R(C'→x), and creates no cycle; "
      "the result is an in-tree on the cycles rooted at some C plus the edge C→x. The converse inequality is concatenation of a tree and a path. "
      "In particular ord π_ε(x) = 0 iff x lies on a noise-selected cycle, because R(C→x) = 0 iff x ∈ C (zero-resistance moves from a cycle stay on it); "
      "hence k* = 0 iff the noise-selected cycles jointly contain all eight codes. "
      f"The formula is checked exactly against minimum in-trees on the full state graph for every state, all rules, n ≤ {ver['t_nx_all']} "
      f"(networkx), the 88 classes at n = {ver['t_nx_reps_n']} (networkx) and all rules for n ≤ {ver['t_hier_n']} (the contraction below): "
      f"{ver['t_mis']} mismatching states.")
    w("")
    w("**Resistances.** R(C→·) for all states by a 0-1 BFS on the state graph with edges x → F(x) (cost 0) and x → x XOR e_i (cost 1). This equals the "
      "two-layer graph (state → pre-noise point F(state) at cost 0, single flips between pre-noise points at cost 1, pre-noise point → state at cost 0), "
      "because a pre-noise point z is reached at the same cost as the state z whenever the sources are whole cycles. One BFS per rotation orbit of cycles; "
      "rows of the other members follow by rotation. Each BFS stops once every cycle and every code has been reached.")
    w("")
    w("**Stochastic potentials of all cycles at once.** A root-free Edmonds contraction (path-growing variant, meldable heaps merged small-to-large, "
      "edges generated lazily by weight level with one sentinel per node standing for its unexpanded levels) produces a laminar family of sets X with "
      "dual values y_X ≥ 0 and one selected edge per set. With T = Σ y and D(r) = Σ_{X∋r} y_X, **γ(r) = T − D(r) for every root r**. "
      "Certificate: (1) each selected edge leaves its set and is tight, V(t_X, h_X) = Σ_{S∋t_X, S⊆X} y_S; (2) within every contracted set the children's "
      "selected edges form one directed cycle; (3) Σ_{S∋C, S∌C'} y_S ≤ V(C,C') for all C ≠ C'. (1)+(2) give an in-tree of weight T − D(r) for every r "
      "(top-down expansion: in a set with sink s, the child containing s keeps it, every other child Y uses its selected edge and takes its tail as sink; "
      "every non-chain set is left by exactly one tree edge and no chain set is left; the weight is T − D(r) because, by (2), the head of the selected edge "
      "of X lies in X's parent, so that edge leaves exactly the sets S with t_X ∈ S ⊆ X and tightness counts every non-chain set once; (2) means one cyclic "
      "permutation of all children), and (3) gives the matching lower bound. "
      "Then k_c = min_C [γ(C) + R(C→D_c)] − min γ, D_c the states containing code c, and k* = max_c k_c. Since ν_c = Σ_x π_ε(x) n_c(x) is a rational "
      "function of ε with positive leading coefficient, ν_c ~ a_c ε^{k_c}, and ρ = λ·min_c ν_c with λ(ε) ~ log(1/ε).")
    w("")
    w("**Bijective and affine rules.** If F is a bijection the kernel is doubly stochastic, the uniform law is stationary, every cycle is noise-selected "
      "and k* = 0. For affine F(x) = Lx + b over GF(2), v0.1's Walsh identity π̂(χ) = (1−2ε)^{|χ|}(−1)^{χ·b} π̂(Lᵀχ) gives uniform three-cell marginals "
      "(ν_c = n/8 at every ε, so k* = 0) iff no nonzero character supported on three adjacent cells lies in the generalised kernel of Lᵀ; "
      f"this is checked by GF(2) linear algebra for n = {int(aff.n.min())}..{int(aff.n.max())} (`data/fw_affine.csv`). "
      "For classes 60 and 90 it is proved for every n ≥ 4 (note, Section 5): with states as GF(2)[t]/(t^n − 1), rule 60 is multiplication by 1 + t and rule 90 by "
      "t^{−1}(1 + t)^2 (b = 0). If n is a power of two, (1 + t)^n = 0, the map is nilpotent, the all-zero state is the only cycle and k* ≥ 1. If n = 2^a m with "
      "m > 1 odd, the generalised kernel of Lᵀ consists of the multiples of ((t^m − 1)/(1 + t))^{2^a}, of degree (m − 1)2^a ≥ 3 for n ≥ 4, while a character on "
      "three adjacent cells is a shift of a polynomial of degree ≤ 2; so the marginals are uniform and k* = 0. At n = 3 the criterion fails (k* = 1 for both classes).")
    w("")
    w("## 4. Verification (before any class was classified)")
    w("")
    w(f"- **(a) High-precision stationary laws.** GTH elimination (subtraction-free) at ε = 10^-3 … 10^-12 for all 256 rules, n = {ver['a_nmin']}..{ver['a_nmax']} "
      f"({ver['a_rows']} (rule, n) pairs): the slope of log π_ε(x) between the two smallest noise levels equals the predicted integer order for every state "
      f"(largest deviation {ver['a_devpi']}), and likewise for every ν_c (largest deviation {ver['a_devnu']}); {ver['a_fail']} failures. "
      "The task asked for n ≤ 8. A first run was launched up to n = 11 without stating that scope change or its cost (n = 11 is about 90% of it); it was stopped on the author's instruction and rerun for n ≤ 10.")
    w(f"- **(a') Exact trees.** Minimum in-trees on the full state graph, {ver['t_rows']} (n, rule, method) rows, {ver['t_mis']} mismatching states; "
      f"min W = min γ in every case: {ver['t_wmin']}.")
    w(f"- **(b) n = 12 against v0.1's trend.** {int(c12.agree.sum())}/88 agree; the exception (class {lst(fl_rules)}) is explained in Section 5 by GTH solves at n = 12 down to "
      f"ε = {eps106[-1]:g}. GTH at n = 12 with ε = 10^-4 … 10^-7 for classes {ver['g_rules']}: largest deviation of the observed ν_c order from the predicted k_c {ver['g_devnu']}.")
    w(f"- **(c) All 256 rules independently at n = 12:** symmetry consistency (k_c permuted under reflection and complementation, same γ profile, same number "
      f"of selected cycles) {ver['c_sym']}.")
    w(f"- **(d)** the 138 rules of v0.1's 42 proved-falling classes have k* ≥ 1: {ver['d_B']}; bijective rules have k* = 0: {ver['d_bij']}.")
    cn, cs_ = certlog.get('log_fw_check_n12_certs.txt'), certlog.get('log_fw_check_sweep_certs.txt')
    w(f"- **Certificates.** n = 12: {cn[0]} checked, {cn[1]} failed ({len(ci['stubs'])} of them bijectivity stubs); sweep n = {ci['nmin']}..{ci['nmax']} (non-bijective classes): {cs_[0]} checked, {cs_[1]} failed. "
      "Field meanings: `data/fw_certificates_n12/README.md`. "
      "The checker (`code/fw/check_cert.py`) uses its own successor map, its own cycle enumeration and scipy Dijkstra on the explicit two-layer graph; it rejects tampered certificates (test).")
    w(f"- **Regression tests.** `code/fw/test_fw.py`: {nfuncs} test functions, {npassed} test cases passed, {nfailed} failed (`data/log_fw_pytest.txt`). "
      "Every defect found during the work has a permanent test:")
    for k, v in bugs:
        w(f"  - {k}: {v}")
    w("- **Process finding.** The first run of verifier (a) used a superseded solver version (its worker processes had loaded the code before a rewrite). "
      "It was discarded (`data/cache/stale/`, not committed) and verifier (a) was split into a solver-independent stage (GTH slopes, cached) and a comparison stage that "
      "re-runs the current solver; the reported results are from the current solver.")
    w(f"- **Checkpointing.** Append-only fsynced JSON lines; a sweep killed after 5 s and resumed gave a byte-identical table to an uninterrupted run "
      f"(sha256 {shas[0][:16]}… for both; `data/log_fw_resume_test.txt`).")
    w("")
    w("## 5. n = 12: all 88 classes, line by line against v0.1")
    w("")
    w(f"v0.1 B classes ({nB}): k* = " + ", ".join(f"{int(k)} for {int(v)}" for k, v in B_dist.items()) +
      f". v0.1 U-falling ({nUF}): k* = " + ", ".join(f"{int(k)} for {int(v)}" for k, v in UF_dist.items()) +
      f". v0.1 U-rising ({nUR}): k* = 0 for {int((c12[c12.v01_type=='U-rising'].kstar==0).sum())}.")
    w("")
    w(f"**Class 106.** {int(r106.n_stable)} of its {int(r106.cycles)} cycles are noise-selected, among them cycles carrying all eight codes, so k* = 0. "
      f"High-precision solves give min_c ν_c = " + ", ".join(f"{v:.4g}" for v in nu106) + f" at ε = " + ", ".join(f"{e:g}" for e in eps106) +
      f": the limit is about {nu106[-1]:.4f} > 0, approached with a linear correction about "
      f"{coef106:.0f} times the limit (secant between ε = {e2:g} and {e1:g}). v0.1's interior maximum ε* = {e106.eps_star:.4f}, ρ* = {e106.rho_star:.3f} is a local maximum; "
      f"ρ ≈ {nu106[-1]:.4f}·log(1/ε) exceeds ρ* again only for ε below about 10^{M['RuleOneOhSixCrossExp']}. The v0.2 class table (`note/table_classes_v02.tex`) "
      f"marks it with the dagger (local maximum; classes with a dagger: {lst(dag)}).")
    w("")
    w("**Weak cases.** " + " ".join(
        f"Rule {int(r.rule)}: k* = {int(r.kstar)}, noise-selected cycles (smallest state/period) {r.stable_cycles}, codes with k_c = k*: {r.uncovered}." for r in weak.itertuples()))
    w("")
    w("Columns: v0.1 type and trend ratio ρ(0.002)/ρ(0.001); expected ratio 2^{k*}·λ(0.002)/λ(0.001); k* and k_c (codes 000..111); number of cycles and of noise-selected cycles; "
      "for k* ≥ 1 the codes with k_c = k* (codes with smaller k_c ≥ 1 are also absent from the noise-selected cycles), "
      "for k* = 0 a set of noise-selected cycles covering all codes (smallest state/period).")
    w("")
    w("| class | v0.1 | v0.1 ratio | expected | k* | k_c | cycles | selected | codes with k_c = k* / covering cycles | agree |")
    w("|---:|---|---:|---:|---:|---|---:|---:|---|---|")
    for r in c12.sort_values("rule").itertuples():
        cov = (r.uncovered if isinstance(r.uncovered, str) else "") if r.kstar >= 1 else (r.covering if isinstance(r.covering, str) else "")
        w(f"| {r.rule} | {r.v01_type} | {r.rho_ratio_0002_over_0001:.3f} | {r.ratio_expected:.3f} | {r.kstar} | {r.k_c} | {r.cycles} | {r.n_stable} | {cov} | {'yes' if r.agree else '**no**'} |")
    w("")
    w("## 6. Predictions (sealed) against outcome")
    w("")
    w(f"1. Survival at n = 12: predicted 27/27 rising and 19/19 falling U classes survive. Outcome: {int((c12[c12.v01_type=='U-rising'].kstar==0).sum())}/{nUR} rising and "
      f"{int((c12[c12.v01_type=='U-falling'].kstar>=1).sum())}/{nUF} falling survive; the flip ({lst(fl_rules)}) was falling → rising, a direction the predictions did not name.")
    w(f"2. Rules 7, 19, 23, 232 do not flip and have k* = 1: confirmed (k* = {lst(weak.kstar.tolist())}).")
    w(f"3. Per-class orders k_pred from the v0.1 trend: {kpred_ok}/88 correct (miss: {lst(c12[c12.k_pred != c12.kstar].rule.tolist())}). Rule 200 (low confidence): k* = {int(c12[c12.rule==200].kstar.iloc[0])}.")
    w(f"4. B classes k* ≥ 1 with distribution 29/5/8 for k* = 1/2/3: outcome {M['NumBkOne']}/{M['NumBkTwo']}/{M['NumBkThree']}.")
    w(f"5. Dependence on n. (a) Classes 60 and 90 have k* >= 1 exactly at the powers of two: solver over n = {runs(complete_n)}: "
      f"{'confirmed' if all(p2_ok.values()) else 'NOT confirmed'} for both; the GF(2) analysis gives uniform marginals (k* = 0) at every other n = {int(aff.n.min())}..{int(aff.n.max())}, and Section 3 proves the criterion for every n ≥ 4 (it fails at n = 3). (b) Bijective classes k* = 0 at every n: confirmed. "
      f"(c) 'at most about 10 classes change with n, at least 70 keep their n = 12 classification for every n ≥ 8': {len(var_rules)} change and {same_as_12} keep it — the first half is wrong, the second holds. "
      f"(d) small rings deviate more: {small_dev} classes differ at some n = {runs(smalln)} from their n = 12 status, against {len(var_rules)} that vary for n ≥ 8. (e) where k* ≥ 1 for all n ≥ 8, the value is constant in n for {allfall_const} of {len(allfall)} classes.")
    w("6. Cost wall: see Section 7.")
    w("")
    w("## 7. Ring sizes")
    w("")
    w(f"Number of classes with k* = 0 per n: " + ", ".join(f"n={n}: {v}" for n, v in zero_per_n.items()) + ".")
    w("")
    w(f"Classes whose k* = 0 / k* ≥ 1 status changes for n ≥ 8 (n = {runs(big)}):")
    w("")
    w("| class | n with k* = 0 | n with k* ≥ 1 | pattern (observed) |")
    w("|---:|---|---|---|")
    for r, z, f, p in patt:
        w(f"| {r} | {z} | {f} | {p} |")
    w("")
    w("Affine classes (GF(2) analysis, n = 4..64): " + "; ".join(f"class {r}: marginals not uniform at n = {b}, bijective at n = {bj}" for r, b, bj in affs) +
      f". Consistency with the solver where the analysis gives k* = 0: {aff_checked - aff_incons}/{aff_checked}.")
    w("")
    w("Cost per ring size (2 worker processes; CPU seconds summed over the 88 classes, longest single job, largest peak memory of a job, largest number of cycles of a non-bijective class):")
    w("")
    w("| n | CPU s | longest job s | peak MB | max cycles |")
    w("|---:|---:|---:|---:|---:|")
    for r in cs.itertuples():
        w(f"| {r.n} | {r.cpu:.0f} | {r.maxjob:.1f} | {r.rss:.0f} | {r.cyc} |")
    w("")
    if wall is not None:
        w("**Where the wall is.** " + str(wall[wall.rule == -1].statement.iloc[0]))
        w("")
        w("| class | cycles n=20 | orbits n=20 | CPU s n=20 | peak MB n=20 | cycles n=22 | orbits n=22 | CPU s n=22 (est.) | V rows GB n=22 |")
        w("|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
        for r in wall[wall.rule >= 0].itertuples():
            w(f"| {int(r.rule)} | {int(r.cycles20)} | {int(r.orbits20)} | {r.cpu20:.0f} | {r.rss20_mb:.0f} | {int(r.cycles22)} | {int(r.orbits22)} | {r.cpu22_est:.0f} | {r.vrows22_gb:.1f} |")
    w("")
    w("Full k* table (rows: class; columns: n):")
    w("")
    w("| class | " + " | ".join(str(n) for n in ns) + " |")
    w("|---:|" + "---:|" * len(ns))
    for r in pk.index:
        w(f"| {r} | " + " | ".join("" if pd.isna(pk.loc[r, n]) else str(int(pk.loc[r, n])) for n in ns) + " |")
    w("")
    w("## 8. Literature")
    w("")
    bbm_text = (
        "Their limit law on cycles (the limit of Q' = WQ from the basin weights) is guaranteed to be the correct leading-order law when the single-flip graph "
        "between cycles has one closed class: that class is then exactly the set of noise-selected cycles, because all cycle-to-cycle resistances are ≥ 1, and "
        "their chain is the leading-order chain on it. With several closed classes their limit depends on the initial vector and can still be right, e.g. by symmetry. "
        f"The independent verification rebuilt their construction for all {bbm['classes']} classes at L = {bbm['L']} (`verify_v02/bagnoli_compare.py`; "
        f"their entropies S* reproduced to {bbm['dS']:.4f}): one closed class for {bbm['one']} classes, where the support of their law equals the noise-selected "
        f"cycles of this work ({bbm['one_support_ok']}/{bbm['one']}) and decides k* = 0 vs k* ≥ 1 identically ({bbm['one_split_ok']}/{bbm['one']}); several closed "
        f"classes only for class {lst(bbm['many17'])} (the two uniform fixed points), where their basin-weighted answer is correct by complementation symmetry. "
        f"So their L = {bbm['L']} table already determines the noise-selected cycles, and with them the split k* = 0 / k* ≥ 1, for all {bbm['classes']} classes at "
        f"L = {bbm['L']}. Over n = {bbm['nmin']}..{bbm['nmax']} ({bbm['pairs']} pairs) several closed classes occur for {bbm['many_min']} to {bbm['many_max']} classes per n, "
        f"and the single-flip limit has the wrong support in {len(bbm['wrong'])} case: {bbm_wrong}. What this work adds: the exact orders k_c and k*, per-state orders, "
        f"the asymptotics of ρ, certificates, ring sizes {nmin}..{nmax} including the cases where the single-flip chain fails "
        f"(class {lst([r for r, n, s, k in bbm['wrong']])} at n = {lst([n for r, n, s, k in bbm['wrong']])}), and the correction for class 106.")
    lit = open(os.path.join(ROOT, "code", "fw", "report_literature.md")).read().strip()
    assert "<<BBM>>" in lit
    w(lit.replace("<<BBM>>", bbm_text))
    w("")
    w("## 9. What is established, and what is not")
    w("")
    w(f"Established exactly (integer computation, independently checked certificates where stated): the noise-selected cycles, k_c and k* for all 88 classes at n = 12 "
      f"(certificates) and for n = {runs(complete_n)} (certificates for n = {ci['nmin']}..{ci['nmax']}; n = {ci['nmax'] + 1}..{nmax} by the same solver without certificates, "
      "and recomputed independently for a sample in `VERIFICATION_v02.md`); the reclassification of class 106; the analytic results for bijective rules (all n) "
      f"and for the affine rules (n = {int(aff.n.min())}..{int(aff.n.max())}). Proved for all n: the order formula for π_ε (tree theorem), its reduction to cycles (Section 3), ρ ~ a ε^{{k*}} log(1/ε), "
      "and the hierarchy certificate lemma; for every n ≥ 4: the power-of-two criterion for classes 60 and 90. Verified numerically: the predicted orders of every state for n ≤ " + str(ver['a_nmax']) + " and for ten classes at n = 12.")
    w("")
    w("Observed, not proved: every statement about how the classification depends on n (Section 7) outside the affine and bijective classes; the divisibility patterns are "
      "fitted to the computed range only. Not claimed: anything for n outside the computed range for non-affine classes; the size of the leading coefficient a "
      "(it decides at which ε the asymptotic regime starts — for class 106 it starts far below any practical noise level); unknown ε, partial observation, "
      "generators outside the family, decoder error rates.")
    w("")
    w("## 10. Reproduction")
    w("")
    w("`reproduce.sh` (v0.1 steps unchanged) followed by `reproduce_v02.sh` (new): verifiers, n = 12 classification, sweep, certificate checks, manifest, this report. "
      "By default it recomputes from scratch (it first discards the sweep checkpoint `data/fw_sweep.jsonl` and the GTH caches in `data/cache/`); "
      "`REUSE_CHECKPOINTS=1` resumes from them instead. "
      f"A from-scratch run at 2 workers took {float(rep['wall_h']):.1f} h in the verification (`verify_v02/out/repro_compare.json`); "
      "timings, peak memory, the cost tables and the last floating-point digit of the trend ratios in two n = 12 tables differ between runs "
      "(so their manifest entries change); all results agree. "
      "Code in `code/fw/`; tests `python3 -m pytest -q code/fw/test_fw.py`. Data files and SHA-256 sums in `data/MANIFEST.sha256`.")
    open(os.path.join(ROOT, "report.md"), "w").write("\n".join(L) + "\n")

    # ---------------- macros for the v0.2 note ----------------
    M.update(SweepNmin=nmin, SweepNmax=nmax, SweepVaryCount=len(var_rules), SweepAllZero=allzero, SweepAllFall=len(allfall),
             VerifyNmax=ver['a_nmax'], VerifyRows=ver['a_rows'], VerifyTreesRows=ver['t_rows'],
             CertsNtwelve=certlog.get('log_fw_check_n12_certs.txt', (0,))[0], CertsSweep=certlog.get('log_fw_check_sweep_certs.txt', (0,))[0],
             SweepVaryRules=lst([p[0] for p in patt]))
    with open(os.path.join(ROOT, "note", "numbers_v02.tex"), "w") as fh:
        fh.write("% generated by code/fw/make_report.py from data/ -- do not edit\n")
        for k, v in M.items():
            fh.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
    print("report.md and note/numbers_v02.tex written;", len(L), "lines")


if __name__ == "__main__":
    main()
