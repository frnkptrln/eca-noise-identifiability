"""Generate ../VERIFICATION_v02.md. Numbers come from files in out/ (own outputs) or, for quotations and macro values
of the work under review, from its files; every quotation is asserted to occur verbatim (Q)."""
import json, os, re, csv
F = json.load(open('out/facts.json'))
V = json.load(open('out/check_verifiers.json'))
MAC = open('out/check_macros.txt').read().strip().split('\n')
BT = list(csv.DictReader(open('lit/bagnoli_L17_table2.csv')))
REP = json.load(open('out/repro_compare.json')) if os.path.exists('out/repro_compare.json') else None
TXT = {}
def Q(path, s):
    if path not in TXT:
        TXT[path] = open(os.path.join('..', path)).read()
    assert s in TXT[path], (path, s)
    return s
def macro(path, name):
    m = re.search(r'\\newcommand\{\\' + name + r'\}\{([^}]*)\}', open(os.path.join('..', path)).read())
    return m.group(1)
def line(lst, key):
    hits = [l for l in lst if key in l]
    assert hits, key
    return hits[0]
def glog(sub):
    hits = [l for l in V['git_log'] if sub in l]
    assert hits, sub
    return hits[0]
def ct(key):
    return line(F['check_text'], key)[5:]
r6 = F['r106']
cc = {}
for l in open('out/cycle_counts_n17_n20.jsonl'):
    d = json.loads(l); cc[(d['n'], d['rule'])] = d['m_cycles']
m154 = cc[(20, 154)]; est154_h = (4.0e-8 * 2**20 * m154 + 8.0e-11 * m154**3) / 3600
grid = [g[0] for g in r6['grid']]
two_state = sorted(int(r['rule']) for r in BT if abs(float(r['Sstar']) - 1 / 17) < 6e-4)
vary27 = ct('abstract').split('= ')[-1].split(':')[0]
vary27_list = ct('abstract').split(': ')[-1]
big17 = sorted([b for b in F['big'] if b['n'] == 17], key=lambda b: b['rule'])
big20 = sorted([b for b in F['big'] if b['n'] == 20], key=lambda b: b['rule'])
fb = lambda L: '; '.join(f"{b['rule']}: k* = {b['kstar']} (k_c {b['k_c']}, {b['m']} cycles, {b['sel']} noise-selected)" for b in L)
nolog = len(eval(F['manifest'][1].split('not in manifest: ')[1]))
NFU = macro('note/numbers.tex', 'NumFallingU'); NI = macro('note/numbers.tex', 'NumInterior')
wrong = '; '.join(f"class {w['rule']} at n = {w['n']} (closed classes of sizes {w['closed_sizes']}; fw_sweep.csv has {w['n_stable']} noise-selected cycles; their limit charges {w['support']} cycles)" for w in V['census_wrong_support'])
# quotations
q = dict(
 a1=Q('note/note_v0.2.tex', '\\NumFallingU{} further classes behave the same way'),
 a2=Q('note/note_v0.2.tex', 'For the \\NumInterior{} falling classes we locate the best noise level, $\\eps^*\\in[\\EpsStarMin,\\EpsStarMax]$'),
 a3=Q('note/note_v0.2.tex', 'For the \\NumInterior{} classes that fall towards $\\eps\\to0$, the interior maxima lie at $\\eps^*\\in[\\EpsStarMin,\\EpsStarMax]$'),
 t106=Q('note/table_classes.tex', '106 & U & 91.7 & 1.90 & 168 & 37 & 8 & 0.010 & 6.189'),
 dag=Q('note/note_v0.2.tex', 'a local maximum, the curve rises again as $\\eps\\to0$'),
 repdag=Q('report.md', "In v0.1's table the entry should carry the dagger (local maximum)"),
 vary=Q('note/note_v0.2.tex', 'the classification is computed for all classes; \\SweepVaryCount{} classes change side with the ring size'),
 est=Q('note/note_v0.2.tex', 'New in version 0.2, established exactly with checked certificates: the noise-selected cycles, $k_c$ and $k^*$ for all $88$ classes at $n=12$'),
 est2=Q('note/note_v0.2.tex', 'and for $n=\\SweepNmin,\\dots,\\SweepNmax$'),
 readme=Q('README.md', 'k_c and k* for all 88 classes at n = 12 and n = 4..20, with certificates'),
 rep9=Q('report.md', 'for n = 4-20 (certificates for n ≤ 14)'),
 certmax=Q('reproduce_v02.sh', '--cert-nmax 14'),
 pow2=Q('note/note_v0.2.tex', 'For the affine classes $60$ and $90$ the change is proved: $k^*\\ge1$ exactly when $n$ is a power of two, where the global map is nilpotent'),
 pow2b=Q('note/note_v0.2.tex', 'Proved for all $n$'),
 pow2c=Q('note/note_v0.2.tex', 'the power-of-two criterion for classes $60$ and $90$'),
 gf2=Q('report.md', 'the GF(2) analysis gives uniform marginals (k* = 0) at every other n = 4..64'),
 n3=Q('note/note_v0.2.tex', 'Fix $n\\ge3$'),
 doi=Q('note/note_v0.2.tex', 'this version is archived as \\href{https://doi.org/10.5281/zenodo.23399101}{doi:10.5281/zenodo.23399101}'),
 ai1=Q('note/note_v0.2.tex', 'its findings (among them a false claim that four additive rules are bijections) were corrected in this version'),
 ai2=Q('note/note_v0.2.tex', 'no independent verification session has yet reviewed version 0.2'),
 man=Q('note/note_v0.2.tex', 'a SHA-256 manifest of the \\ManifestFiles{} data files'),
 every=Q('note/note_v0.2.tex', 'Every number in this note is a function of the $4096$-state chain and is computed as such.'),
 every2=Q('note/note_v0.2.tex', 'so every quantity in this note is computed exactly'),
 bound=Q('note/note_v0.2.tex', '$n=12$ on a ring'),
 hours=Q('note/note_v0.2.tex', 'The whole computation runs in about two hours on two CPU cores.'),
 r15=Q('reproduce_v02.sh', 'about 1.5 h'),
 r47=Q('reproduce_v02.sh', 'the sweep at n = 19, 20 (47 min)'),
 rsweep=Q('code/fw/run_sweep.py', 'if (n, r) not in done]'),
 rep10=Q('report.md', 'verifiers, n = 12 classification, sweep, certificate checks, this report'),
 bbm=Q('report.md', 'Their leading-order law on cycles is correct only when the single-flip graph between cycles has one closed class'),
 nf=Q('report.md', 'it means "not found", not "never done"'),
 ie=Q('note/note_v0.2.tex', 'i.e.\\ iff the noise-selected cycles jointly contain all eight codes'),
 contr=Q('note/note_v0.2.tex', 'edges inside a cycle cost $0$, so cycles contract, and shortest-path weights do not change the minimum in-tree value'),
 pik=Q('note/note_v0.2.tex', '$\\pi(K\')\\to1$ by Lemma~\\ref{lem:ends}'),
 lin=Q('report.md', 'approached with a linear correction about 4102 times the limit'),
 cdesc=Q('report.md', 'optimal in-tree hierarchy with dual values, witness trajectories'),
 width=Q('note/note_v0.2.tex', 'to a width of $5\\cdot10^{-4}$'),
 nonleft=Q('report.md', 'every non-chain set is left by exactly one tree edge'),
)
secant = (r6['nu_min_small'][0][1] - r6['a_limit']) / (r6['a_limit'] * 1e-4)
md = []
w = md.append
w(f"""# Verification report: proposed v0.2 of "Rule identifiability in elementary cellular automata under dynamical noise" (branch `noise-selected-cycles`, 9 Nov 2026)

Object: branch `noise-selected-cycles` at commit 9ce96c6 (the six commits after b8ce5a5): `report.md`, `literature.md`, `note/note_v0.2.tex` with `note/numbers_v02.tex`, `code/fw/`, `data/` (certificates in `data/fw_certificates_n12/` and `data/fw_certificates_sweep/`), `reproduce_v02.sh`. Verifier code, sealed sample, outputs and logs: `verify_v02/` on branch `verify-v02`; own implementation from the definitions of the brief (`eca.py`, `gth.py`, `route_b.py`, `exact_small.py`, `check_certs.py`, ...). `code/fw/` was read only after the own results were committed; no computed value disagreed, so nothing had to be localised in it (only `run_sweep.py` and `check_cert.py` were read, for V9 and for the certificate format). This report is generated by `verify_v02/make_verification.py`: every number is read from a file in `verify_v02/out/` (or, for macro values and quotations of the work, from its own files), and every quotation is asserted verbatim against the quoted file.

Order of work (commits on `verify-v02`): (1) `verify_v02/SAMPLE.md` sealed before `report.md`, `note_v0.2.tex`, `literature.md` or any `data/fw_*` file was read; (2) blind results committed; (3) comparison with `data/` and the texts, own certificate checker; (4) post-seal additions, labelled as such below. Deviations from the brief: `git worktree add` is refused by the sandbox (no writes under `.git/worktrees`), so two separate clones outside `~/git` serve as worktrees, one for branch `verify-v02` (commits transferred into the original repository with `git fetch`, the original checkout was not touched) and one for the run of `reproduce_v02.sh`. While testing write permissions I left two empty probes in the original repository that the sandbox does not let me remove: the file `.git/zz_test` and the directory `.git/objects/zz` (untracked, no effect on git; please delete them). Before sealing I had seen a truncated note from an earlier session (v0.2 classifies all 88 classes at n = 12; 87 agree with v0.1) and a smoke test printing k_c = 0 for rule 30 at n = 12; both are recorded in `SAMPLE.md`.

## (A) Errors found

V1. ABSTRACT AND SECTION 3 CONTRADICT SECTION 5 ON CLASS 106 (note_v0.2.tex: abstract; Section 3.2 "Rates and the best noise level"; Figure 1(b) caption). The abstract keeps v0.1's "{q['a1']}" (ρ vanishes at both ends) and "{q['a2']}", with NumFallingU = {NFU}, NumInterior = {NI}, EpsStarMin = {macro('note/numbers.tex', 'EpsStarMin')} attained by rule {macro('note/numbers.tex', 'EpsStarMinRule')} (`note/numbers.tex`); the same abstract then says that only NumUfallingVtwo = {macro('note/numbers_v02.tex', 'NumUfallingVtwo')} of these classes have k* ≥ 1. Section 3.2 repeats "{q['a3']}" (smallest for rule {macro('note/numbers.tex', 'EpsStarMinRule')}), and the two Spearman correlations and Figure 1(b) are over the same {NI} classes, 106 included. Evidence: k* = 0 for 106 at n = 12 by route (a) and route (b); {F['r106_selected']} of its {F['r106_cycles']} cycles are noise-selected; own GTH gives min_c ν_c = {r6['nu_min_small'][-1][1]:.6f} at ε = 1e-9 (limit {r6['a_limit']:.6f}); ρ falls from {r6['rho_star_fit']:.4f} at the local maximum (ε = {r6['eps_star_fit']:.5f}) to {r6['min_rho_on_small_grid']:.4f} at ε = {V['r106_rho_min_eps']:g} and then grows like a·log(1/ε) (`out/rule106_summary.json`). So class 106 neither "behaves the same way" nor has a best noise level. Proposed fix: "{int(NFU) - 1} further classes behave the same way; class 106 falls over the computed grid but has ρ → ∞"; give the ε* range and the Spearman values over the {int(NI) - 1} classes without 106 (or flag 106 in each place).

V2. APPENDIX TABLE, CLASS 106 (note/table_classes.tex, unchanged from v0.1). The row reads "{q['t106']}", without dagger, while the v0.2 legend defines the dagger as "{q['dag']}" and Section 5 says the maximum of 106 is local; `report.md` Section 5 itself says "{q['repdag']}". Proposed fix: dagger on both ε* and ρ* of the 106 row.

V3. ABSTRACT, RING SIZE: "{q['vary']}", with SweepVaryCount = {macro('note/numbers_v02.tex', 'SweepVaryCount')}. That number counts the classes that change side for n ≥ 8 (as Section 5 says); over the range n = 4..20 named in the same sentence, {vary27} classes change side ({vary27_list}; from `data/fw_sweep.csv`, whose k* agree with mine wherever I computed them, see (B)). Proposed fix: "for n ≥ 8, {macro('note/numbers_v02.tex', 'SweepVaryCount')} classes change side" (or "{vary27} classes change side for some n in 4..20").

V4. SCOPE OF "ESTABLISHED WITH CHECKED CERTIFICATES" (note_v0.2.tex, "What is established, and what is not"): "{q['est']}" ... "{q['est2']}" (4..20). Certificates exist only for n = 12 and n = {F['cert_nrange'][0]}..{F['cert_nrange'][1]} ({F['cert12']} + {F['certsw']} files; the script runs the sweep with `{q['certmax']}`); for n = {F['cert_nrange'][1] + 1}..20 there are none. `README.md` invites the same reading: "{q['readme']}". `report.md` (Sections 2(a), 9: "{q['rep9']}") and the PR draft are correct. For n ≥ 15 there is now my independent recomputation of {V['indep_pairs_ge15']} distinct (n, class) pairs, all in agreement (B), which is evidence but not a certificate. Proposed fix: "with checked certificates for n = 12 and n ≤ 14; for n = 15..20 by the same solver, without certificates" (also in README).

V5. POWER-OF-TWO CRITERION FOR CLASSES 60 AND 90 (note_v0.2.tex, Section 5 "Ring size": "{q['pow2']}"; "What is established": "{q['pow2b']}: ... {q['pow2c']}"; also the PR draft). (i) The note contains no proof; `report.md` supports it by GF(2) enumeration and the solver only ("{q['gf2']}"). (ii) As stated it is false at n = 3, which the note admits ("{q['n3']}"): {F['affine_n3'][0]}; {F['affine_n3'][1]} (own route (b), `out/affine_n3.txt`); the work's own `data/fw_verify_orders.csv` also has k* = 1 for rules 60 and 90 at n = 3. (iii) For n ≥ 4 it is true, with a short proof the note should contain. Identify states with GF(2)[t]/(t^n - 1) and write n = 2^a m, m odd. Rule 60 is multiplication by L = 1 + t (up to orientation), rule 90 by t^-1 (1 + t)^2, both with b = 0. If m = 1, (1 + t)^n = 1 + t^n = 0, so L is nilpotent, the all-zero state is the only cycle, the codes 001..111 occur on no cycle, and k* ≥ 1 by Lemma 3. If m > 1, t^n - 1 = (t^m - 1)^(2^a) with 1 + t a simple factor of t^m - 1, so the generalised kernel of the transpose (the (1 + t)-primary part) is the set of multiples of ((t^m - 1)/(1 + t))^(2^a), of degree (m - 1) 2^a; a nonzero character on three adjacent cells is (a shift of) a polynomial of degree ≤ 2, which lies there only if (m - 1) 2^a ≤ 2, i.e. n = 3. Hence for n ≥ 4 not a power of two the three-cell marginals are uniform at every ε and k* = 0. My GF(2) computation agrees: rule 60 has non-uniform marginals exactly at n = {F['aff60_nonuniform']}, rule 90 at n = {F['aff90_nonuniform']}, L nilpotent at the same n, n = {V['affine_n'][0]}..{V['affine_n'][1]} (`out/affine_check.csv`). Proposed fix: "for n ≥ 4", with the proof (or downgrade to "checked for n = 4..64").

V6. DOI LINE (note_v0.2.tex, "Code and data"): "{q['doi']}" is copied from v0.1; 10.5281/zenodo.23399101 is v0.1's version DOI (commit "{glog('Add DOI (10.5281/zenodo.23399101)')}"), so the proposed v0.2 would claim to be archived under v0.1's record. Proposed fix: "Version 0.1 is archived as doi:10.5281/zenodo.23399101, all versions under doi:10.5281/zenodo.23399100"; add the v0.2 version DOI after a release. (`.zenodo.json` and `CITATION.cff` still say version "0.1", consistent with an unreleased branch; they need the same update at release.)

V7. STATEMENT ON THE USE OF AI (note_v0.2.tex). (i) The v0.1 sentence "{q['ai1']}" is kept verbatim; in v0.2 "this version" reads as v0.2. (ii) "{q['ai2']}" was true for the branch as reviewed and is superseded by this report. Otherwise accurate as far as checkable: the branch commits carry the author's name only and {'no trailers' if not V['git_trailers'] else 'trailers: ' + V['git_trailers']}, and "{glog('Seal predictions')}" precedes "{glog('Add exact small-noise solver')}". Proposed fix: "were corrected in version 0.1"; replace the last clause by a reference to this verification and to how its findings were handled.

V8. STALE v0.1 SCOPE STATEMENTS IN THE v0.2 NOTE. (i) "{q['man']}" with ManifestFiles = {macro('note/numbers.tex', 'ManifestFiles')}, whereas `data/MANIFEST.sha256` has {V['manifest_n']} entries. (ii) "{q['every']}", the abstract's "{q['every2']}" and the declared boundary "{q['bound']}" (Section 1.6) no longer hold: Section 5 reports n = 4..20. (iii) "{q['hours']}" covers v0.1 only; `reproduce_v02.sh` adds "{q['r15']}"{(' (' + REP['wall_h'] + ' h in my from-scratch run, below)') if REP else ''}. Proposed fix: update the three statements and regenerate `\\ManifestFiles`.

V9. THE REPRODUCTION SCRIPT DOES NOT RECOMPUTE THE SWEEP (reproduce_v02.sh, code/fw/run_sweep.py). The sweep's resumable checkpoint `data/fw_sweep.jsonl` is committed, and `run_sweep.py` builds its job list with "{q['rsweep']}", so on a fresh checkout `reproduce_v02.sh` only re-finalises `fw_sweep.csv` from the committed checkpoint: n = 4..20 is not recomputed and the n ≤ 14 certificates are not rewritten, although the script's header budgets "{q['r47']}" and `report.md` Section 10 lists "{q['rep10']}". Proposed fix: start the script by moving the checkpoint aside (or a `--fresh` flag), or state that the committed checkpoint is reused. I ran it from scratch with the checkpoint moved aside (B).

V10. RELATED WORK: THE READING OF BAGNOLI, BAIA AND MATTEUZZI IS TOO STRONG, AND THE NOTE DOES NOT CITE THEM (report.md Section 8, code/fw/report_literature.md; note_v0.2.tex). (i) "{q['bbm']}". One closed class is sufficient (the closed class is then exactly the set of noise-selected cycles, because all cycle-to-cycle resistances are ≥ 1, and their chain is the leading-order chain on it), but not necessary: with several closed classes their limit of Q' = WQ depends on the initial basin weights and can still be right, e.g. by symmetry. I rebuilt their construction from their Section 5 at L = 17 for all 88 classes (`bagnoli_compare.py`): {line(F['bag17'], 'attractor counts')}; {line(F['bag17'], 'S* rebuilt')}. {line(F['bag17'], 'single-flip graph')}: for class 232 these are the fixed points 0 and 1^17, where their basin-weighted answer (1/2, 1/2) is the correct law by complementation symmetry. {line(F['bag17'], 'support of their limit law')}; {line(F['bag17'], 'covers all 8 codes')}; {line(F['bag17'], 'own route (b) at n=17')}. So their L = 17 table already contains, for every class, the correct leading-order law on cycles and hence the k* = 0 / k* ≥ 1 dichotomy at L = 17 (they do not state it in these terms, and they have no orders k* ≥ 1 and no per-state orders). The condition does matter at other n: over n = 4..20 ({V['census_pairs']} pairs) several closed classes occur in {V['census_many_range'][0]} to {V['census_many_range'][1]} classes per n (`out/bagnoli_census_summary.txt`), and the limit of their chain has the wrong support in {len(V['census_wrong_support'])} case: {wrong}. (ii) The note does not cite them: `Bagnoli2024` (and `WuenscheLesser1992`) occur only as `\\bibitem`, in no `\\cite`, so the closest prior work is not discussed in the note. The novelty statements are phrased as required ("{q['nf']}", also in `literature.md` and `code/fw/report_literature.md`); none says "first". Proposed fix: "is guaranteed correct when the single-flip graph between cycles has one closed class, which holds for all classes but 232 at L = 17 (and 232 is correct by symmetry), so their table already determines the noise-selected cycles at L = 17; at other ring sizes the condition fails for a few classes, once with a wrong law"; cite them in Section 5 of the note.

V11. PROOF OF THEOREM 1 (note_v0.2.tex Section 5; report.md Section 3): correct in outline, four steps asserted rather than shown. (a) "{q['ie']}" needs ord π(x) = 0 iff x lies on a noise-selected cycle, i.e. R(C → x) = 0 iff x ∈ C (zero-resistance moves from a cycle stay on it). (b) "{q['contr']}" is asserted without argument (a minimum in-tree on the states of K' induces one on the contracted graph of no larger weight; a union of shortest paths contains an in-tree). (c) The redirect argument treats x as a node outside the cycles; x on a cycle is not covered explicitly. (d) "{q['pik']}" is not needed: censoring gives π restricted to K' and renormalised exactly, and the normaliser has order 0 since the cycle states carry order-0 mass. The statement itself holds: my derivation (ord π(x) = min_y [ord π(y) + H(F(y), x)], from π = πP with positive terms) gives the same formula, and it agrees state by state with the full 2^n-state minimum in-tree computation for {F['reduction_validated_pairs']} (n, class) pairs, n = 4..12 ({F['reduction_validated_bad']} mismatching states). Proposed fix: add the four lines.

V12. MINOR, CLASS 106 NUMBER (report.md Section 5): "{q['lin']}". The quoted value is the secant from ε = 1e-4 (own value {secant:.1f}); the linear coefficient at ε → 0 (secant between 1e-8 and 1e-9) is {r6['b_over_a']:.0f} times the limit. Proposed fix: "about {round(r6['b_over_a'], -1):.0f} times the limit", or omit.

V13. MINOR, CERTIFICATE WORDING. (i) `report.md` 2(a) calls the certificates "{q['cdesc']}"; {F['cert12_stubs']} of the {F['cert12']} files at n = 12 (classes {F['cert12_stub_rules']}) are stubs asserting bijectivity and k_c = 0 only (correct; my checker verifies bijectivity). (ii) "uncovered codes" (report.md Section 5 table; certificate field `uncovered_codes`) means "codes with k_c = k*", not "codes on no noise-selected cycle": for class 0 it lists 111 only, although 001..110 are also absent from the only noise-selected cycle. My checker's first version read the field literally and rejected {V['firstpass_c10_only']} certificates for this reason alone ({V['firstpass_exc']} more were crashes on the stubs; `logs/cert_check_firstpass_*.jsonl`); with the files' meaning all are accepted. Proposed fix: rename the column and field; mention the {F['cert12_stubs']} stubs.
""")
w(f"""## (B) Checked and correct

Blind sample (`verify_v02/SAMPLE.md`, commit bd22a01; results committed in 81d235e before any claim file was read): all 88 classes at n = 4 and 5; at n = 12 the {20 - len(F['n12_drawn'])} classes fixed by the brief plus {F['n12_drawn']} (seed {F['seed']}); n = 17: {sorted(F['n17'])}; n = 20: {sorted(F['n20'])} (four drawn with seed {F['seed_big']}, plus the class with most cycles under a cap of {F['cap']} cycles: 29 with {F['m17_max']} cycles at n = 17, 132 with {F['m20_max']} at n = 20).
- Route (a), exact: n = 4 and 5, stationary laws of all classes as exact rational functions of ε (tree theorem; principal minors of I - P as integer polynomials by exact evaluation and interpolation; each checked at ε = 1/7 against an exact rational linear solve: {F['exact_n4_check_ok']}/88 and {F['exact_n5_check_ok']}/88). Number of classes per k*: n = 4 {F['exact_n4_kstar_hist']}, n = 5 {F['exact_n5_kstar_hist']}. n = 12: own subtraction-free GTH in float64 at ε = 1e-4 ... 1e-9 for the 20 classes ({F['gth12_solves']} solves; largest |πP - π|/π = {F['gth12_maxres']:.1e}); k_c as slopes, largest deviation from an integer over the three smallest pairs {F['ab_n12_slope_dev']:.1e} (class 106).
- Route (b): own minimum resistances (0-1 BFS) and minimum in-trees (tropical, min-plus, GTH on the cycle-cost matrix, exact because GTH is subtraction-free), orders of all states from the Bellman equation of π = πP. Validated state by state against the full 2^n-state tropical GTH: {F['reduction_validated_pairs']} (n, class) pairs, n = 4..12, {F['reduction_validated_bad']} mismatches.
- Routes (a) and (b) agree on every k_c (mismatching classes: n = 4 {F['ab_n4_mismatch']}, n = 5 {F['ab_n5_mismatch']}, n = 12 {F['ab_n12_mismatch']}). k* at n = 12: {F['ab_n12_kstar']}.
- n = 17: {fb(big17)}. n = 20: {fb(big20)}. Largest job {max(b['sec'] for b in F['big']):.0f} s and {max(b['rss'] for b in F['big']):.0f} MB.

Comparison with `data/`: {F['compare_data'][0]}; `data/fw_n12_classes.csv` and `data/fw_n12_all_rules.csv` (all 256 rules recomputed rule by rule): {line(F['compare_data'], 'all 256 rules')}; `data/fw_n12_gth.csv`: ν_min of all 10 classes at the 4 noise levels equal to my GTH to the printed 6 digits (`out/compare_data.txt`).

Certificates (task 3), own checker `check_certs.py` written from the certificate files and the definitions (own map, cycles and BFS; checks the cycle list, the laminar structure, tightness of every selected edge, one cyclic permutation of the children inside every set, dual feasibility for all ordered pairs of cycles, γ(r) = Σ y - Σ_(X ∋ r) y_X, the explicit tree, the noise-selected set, every k_c witness trajectory, and k_c against an own shortest-path lower bound): n = 12 {F['cert12_ok']}/{F['cert12']} accepted ({F['cert12_stubs']} bijectivity stubs); sweep n = {F['cert_nrange'][0]}..{F['cert_nrange'][1]} {F['certsw_ok']}/{F['certsw']} accepted; sweep files plus bijective pairs of `fw_sweep.csv` = {V['sweep_certs_plus_bijective']} = all {V['pairs_n4_14']} pairs with n ≤ 14; largest m = {F['cert_max_m']}; {F['cert_sec']} s in total. Tamper test: {F['tamper_accepted']} of {F['tamper_n']} tampered copies of three certificates accepted ({', '.join(F['tamper_kinds'])}).

n = 15..20 without certificates (post-seal, cost-bounded): own route (b) for the {macro('note/numbers_v02.tex', 'SweepVaryCount')} classes that change side, at every n = 15..20 except class 154 at n = 20 ({m154} cycles, about {est154_h:.1f} h by my cost model): {F['switch_runs']} runs, k_c, k*, cycle counts and number of noise-selected cycles equal to `fw_sweep.csv` in all ({F['switch_bad']} mismatches; largest job {F['switch_sec_max']:.0f} s and {F['switch_rss_max']:.0f} MB; {F['switch_cpu']} CPU s). With the blind sample: {V['indep_pairs_ge15']} distinct pairs with n ≥ 15.

Proofs (task 4). Order formula (tree theorem, no cancellation): correct. Reduction to cycles, redirect argument: correct (redirecting C' ∈ S other than the kept member K to C_x costs V(C', C_x) ≤ R(C' → x) + R(x → C_x) = R(C' → x) and creates no cycle, since C_x's path to x runs through K), with the gaps of V11. Hierarchy certificate lemma (report Section 3): correct. Lower bound: y ≥ 0 and (3) give Σ_e V(e) ≥ Σ_S y_S #(tree edges leaving S) ≥ Σ_(S ∌ r) y_S = T - D(r) for every in-tree rooted at r. Upper bound: the top-down expansion is an in-tree; its weight is T - D(r) because the selected edge of X leaves exactly the sets S with t_X ∈ S ⊆ X (its head lies in X's parent by (2)), so tightness counts each non-chain set once. The report compresses this into "{q['nonleft']}" (true, but the reason is the sentence above), and (2) has to be read as one cyclic permutation of all children, which the certificates satisfy. ρ ~ a ε^k* log(1/ε), a = smallest leading coefficient among the codes with k_c = k*: correct (λ(ε) ~ log(1/ε); ν_c rational with positive leading coefficient); the exact n = 4, 5 rational functions give a for every class (`out/exact_n*.jsonl`). k* = 0 for bijective maps (doubly stochastic kernel): correct. Walsh identity and uniform-marginal criterion for affine maps: correct (if the L^T-orbit of χ avoids 0, |π̂(χ)| ≤ (1-2ε)^j for every j). Affine table `data/fw_affine.csv` ({V['affine_nclasses']} classes, n = {V['affine_n'][0]}..{V['affine_n'][1]}): {'; '.join(F['affine_compare'][1:5])}. Power-of-two criterion: see V5 (true for n ≥ 4, not proved in the note, false at n = 3).

Class 106 (task 5): k* = 0 at n = 12 (both routes; certificate accepted); {F['r106_selected']} of {F['r106_cycles']} cycles noise-selected (not selected, as (smallest state, period): {V['r106_nonselected']}). Own GTH on {len(grid)} noise levels between {min(grid):g} and {max(grid):g}: maximum at ε = {r6['eps_star_fit']:.5f}, ρ* = {r6['rho_star_fit']:.4f} (quadratic fit through {r6['fit_points']} solves), consistent with v0.1's {macro('note/numbers_v02.tex', 'RuleOneOhSixEpsStar')} / {macro('note/numbers_v02.tex', 'RuleOneOhSixRhoStar')} located "{q['width']}". It is local: ρ drops to {r6['min_rho_on_small_grid']:.3f} at ε = {V['r106_rho_min_eps']:g} and then grows. min_c ν_c at ε = 1e-4 ... 1e-9: {[round(v, 6) for _, v in r6['nu_min_small']]}, as in `report.md` to the printed digits; limit {r6['a_limit']:.6f}. Crossing level: λ(ε)(a + bε) = ρ* at ε = 10^{r6['log10_crossing']:.2f}, so "about 10^-57" holds (first-order expansion fitted at 1e-8, 1e-9; at that ε higher-order terms are negligible).

Related work (task 6): Bagnoli, Baia and Matteuzzi, arXiv:2406.15408v2 (30 Apr 2025, titled "Discrete System Phase Space Modification by Vanishing Noise", the extended version of the ACRI 2024 chapter), read in full. The report's description (all 88 minimal rules at L = 17; at most one flip per step; an attractor-level chain from single-flip basin jumps; entropies; no potentials, no resistances above one, no per-state orders) is accurate; their Table 2 is reproduced from their own description (V10); it singles out exactly rules {two_state} with S* = 1/17 (two equally weighted states), as `literature.md` says. Their L = 17 cycle counts equal mine for all 88 classes.

Text against data (task 7). {ct('per-n counts')}. {ct('n>=8')}. {ct('5(d)')}; {ct('5(c)')}; {ct('5(e)')}. {ct('switching table')}; {ct('own pattern')}. {ct('full k* table')}. {ct('k* distribution')}. {ct('46 U')}; {ct('agree with v0.1')}. {ct('s5 table')} (v0.1 types and ratios from v0.1's `class_summary.csv` and `epsilon_star.csv`, expected ratio 2^k* λ(0.002)/λ(0.001), number of noise-selected cycles, validity of every named covering cycle). Weak cases: {ct('class 7:')}; {ct('class 19:')}; {ct('class 23:')}; {ct('class 232:')}, as stated. Macros of `numbers_v02.tex`: {sum(l.startswith('OK') for l in MAC)} of {len(MAC)} reproduced (`out/check_macros.txt`). Report Section 4 against the work's files: (a) {V['orders_rows']} pairs, n = {V['orders_n'][0]}..{V['orders_n'][1]}, largest deviations {V['orders_max_dev_pi']:.1e} / {V['orders_max_dev_nu']:.1e}; (a') {V['trees_rows']} rows ([rows, n min, n max] per method: {V['trees_by_method']}), {V['trees_mismatches']} mismatches, min W = min γ: {V['trees_wmin_eq_gmin']}; (b) {V['gth12_max_dev']:.1e}; (c), (d) [ok, total]: {V['checks']}; all as stated. Cost and wall: {line(F['check_cost'], 'cost table rows')}; {line(F['check_cost'], 'n=20: CPU sum')}; {line(F['check_cost'], 'growth factors')}; {line(F['check_cost'], 'all-class n=22')}; as in Section 7. Manifest: {F['manifest'][0]} ({V['manifest_cert_entries']} of the entries are certificates); the {nolog} tracked files under `data/` outside it are all `log_*.txt`, as in v0.1. Novelty statements: all say "not found" (V10). The abstract agrees with Section 5 except for V1 and V3.
""")
if REP:
    w(f"""Reproduction (task 7): `reproduce_v02.sh` run once from scratch in a separate clone outside `~/git`, WORKERS=2, committed sweep checkpoint moved aside (V9). {REP['text']}
""")
w(f"""## (C) Not checked, and why

- Route (a) at n = 12 covers the 20 sealed classes only; the other classes at n = 12 by route (b) only. n = 17 and 20 by route (b) only, by design, under a cap of {F['cap']} cycles: above it are classes {V['over_cap_n17']} at n = 17 and {V['over_cap_n20']} at n = 20; in total {len(V['not_recomputed_n17'])} classes at n = 17 and {len(V['not_recomputed_n20'])} at n = 20 were not recomputed by me (the bijective ones follow from the analytic argument, which I checked).
- n = 15, 16, 18, 19: only the {macro('note/numbers_v02.tex', 'SweepVaryCount')} switching classes recomputed; n = 13, 14 only through the checked certificates; the other classes at n = 15..20 rest on the work's solver alone (not assessed at this depth).
- Leading coefficients a: computed (exact at n = 4, 5; numerical for the sealed classes at n = 12) but not compared, since the work claims no values of a.
- `literature.md` beyond the Bagnoli et al. entry and the novelty wording: the other sources were not read, so their theorem numbers and "not readable here" statuses are unchecked. The ACRI 2024 chapter itself was not available; only arXiv v2 was read, as in the work.
- The v0.2 note was not compiled (no LaTeX in the sandbox); macros and text were checked as source; figures were not regenerated or viewed.
- `code/fw/` was not reviewed as code; its tests ran only inside `reproduce_v02.sh`.
- v0.1 content carried unchanged into v0.2 (definitions, zero noise, finite horizon, boundary check) was not re-verified beyond what the reclassification of class 106 touches.

Verifier: independent Claude session, 9 November 2026, working from the definitions of the brief; code, sample, outputs and logs in `verify_v02/`.
""")
open('../VERIFICATION_v02.md', 'w').write('\n'.join(md))
print('written', sum(len(x) for x in md), 'chars')
