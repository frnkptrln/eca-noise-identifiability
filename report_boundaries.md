# Open boundaries: noise-selected cycles of ECA on a row with null walls

Status (updated as the work proceeds):

- 24 Nov 2026, start. Base: commit 2765f7e (= origin/main, version 0.4). The worktree
  `~/git/eca-open-boundaries` could not be created from the sandbox (`git fetch` and `git worktree add` fail with
  "Operation not permitted" on `.git`), and no git identity is visible inside the sandbox, so nothing is committed.
  The work was done in a copy of 2765f7e (`git archive 2765f7e`; tree e0bb588 = tree of 2765f7e) in the session
  workspace; every finished file was saved as an artifact, and Section 9 lists the commands that recreate the
  step commits in the worktree. `nice 10` is refused in the sandbox (`setpriority: Operation not permitted`);
  every batch ran under `taskpolicy -c utility` (macOS low QoS) instead, with at most 2 worker processes.
- Step 0 (literature): done, `literature_boundaries.md` (Section 1).
- Step 1 (definitions, symmetries, code, guarding test): done (Section 2).
- Step 2 (predictions): sealed 24 Nov 2026 before any computation under walls, `PREDICTIONS_boundaries.md`,
  sha256 d5e5b52061bb5434b128bb5c0e8a1eef4ab17b13545742d386b5a4e4217ec33d. The literature review was still
  running when the predictions were sealed, so they use no literature found in this session.
- Step 3 (computation): done. Null walls, all 160 reflection classes, n = 4..16; the 12 classes whose side
  changes in n = 8..16, n = 17..20; certificates n <= 14 (all) and n = 15, 16 (45 classes); independent GTH check
  n = 4..9, all 256 rules (Section 4).
- Step 4 (comparison, mechanisms): done for every class whose side depends on n for n >= 8 (Section 5).
  Proved: the affine classes for every n (5.1). Everything else is computed or observed, as tagged.
- Step 5 (reflecting walls, n = 4..12): done (Section 6).
- Predictions scored (Section 7), open points and plain-words summary (Section 8), commit commands (Section 9): done.
  Everything planned is done; nothing is committed (Section 9).

Tags: [proved] = proof written out here (or in the cited source, location given); [computed] = exact result in
the named data file, produced by the named command; [observed] = pattern seen in computed data, not proved.

## Contents
1. Literature (Step 0)
2. Definitions and symmetries (Step 1)
3. Predictions (Step 2, sealed)
4. Computation (Step 3)
5. Ring vs null comparison and mechanisms (Step 4)
6. Reflecting walls (Step 5)
7. Predictions scored
8. Open points; plain-words summary for a later README
9. How to recreate the commits

## 1. Literature (Step 0)

`literature_boundaries.md` was compiled in this session by a sub-agent working under the literature rule (only
texts opened and read in this session, every statement with its location, no citation after others, no
"not read" entries). Nine sources were read (two in full, seven in the sections named there); nineteen further
candidates could not be obtained as full text and are not cited. I re-read two statements in the downloaded
arXiv copy of Vadali and Turner myself: Theorem 3.4 (p. 6, Jordan structure of null-boundary rule 90) and
Theorem 6.2 (p. 12, reflection principle). Used below:

* Null-boundary rule 90 is invertible iff n is even (Martín del Rey 2015, Prop. 3.1(a), pp. 113-114;
  Vadali and Turner 2026, Thm. 3.4, p. 6) and nilpotent if n + 1 is a power of two (Vadali and Turner,
  Thm. 5.1, p. 9; Tadaki 1994, eq. (2.4), p. 3 of the arXiv version, numerical for N <= 32). The converse is not
  stated in these sources; it follows from Vadali and Turner, Thms. 3.4 and 3.6, and is re-proved in 5.1.
* Null-boundary rule 60 (and 102) is invertible for every n (Martín del Rey, Section 4, pp. 120-121); rule 150 is
  invertible for n = 0, 1 mod 3 (Martín del Rey, p. 121, stated) and has transients exactly at N = 3m + 2
  (Tadaki, p. 4 and Table I, numerical, N <= 32). The "only if" for rule 150 was not found proved; it is in 5.1.
* The reflection principle: a null row of n cells under rule 90 is the mirror-symmetric part of a ring of
  2n + 2 cells (Vadali and Turner, Thm. 6.2, p. 12, and Lemma B.3, p. 20); they remark that for other automata
  the principle "usually does not work" (pp. 12-13). Lemma M in 5.1 states which ECA it works for.
* Reachability under null boundary for one n by the reachability tree (Bhattacharjee et al. 2020, Section 3.3,
  pp. 13-14); reversibility for all n by two graphs (Wang et al. 2025, Thms. 1-5, pp. 5-8). Wang et al., Table 1
  (p. 10), lists rule 195 (the complement of rule 60) as never reversible under null walls; that conflicts with
  Martín del Rey's triangular-matrix argument and with this computation (rule 195, class {153, 195}, is
  bijective at every n = 4..16 in `data/boundaries/null_sweep.csv` [computed]). Either the entry or our reading
  of their rule string is wrong.
* Stochastic stability: the tree representation and "only noise-free recurrent classes can be stochastically
  stable" hold on any finite configuration space (Miękisz 2008, Section 7, pp. 22-24); all spatial examples read
  there use rings.
* Not found in the sources read: anything on noise-selected cycles, stochastic potentials or zero-noise limits of
  ECA (or other CA) on a row with fixed or reflecting walls, or on a path graph rather than a cycle.

## 2. Definitions and symmetries (Step 1)

**Model.** A row of n cells 0..n-1. Null walls: cells -1 and n are 0 at every step; the noise flips cells
0..n-1 only, so the resistance is still r(x -> y) = H(F(x), y) on {0,1}^n. Cell i reads the code
c = 4 x_{i-1} + 2 x_i + x_{i+1} with the wall values inserted: the left edge cell reads codes 0..3, the right
edge cell even codes. The code set of a state is the set of codes read at the n cells; the observer reads the
rule on every visited code, edge codes included. For n >= 3 every code occurs in some state (at an interior
cell). Fixed-1 walls ("one") and reflecting walls ("reflect": cell -1 copies cell 0, cell n copies cell n-1)
are defined the same way. Nothing else changes: the note's Theorem (orders via the Markov chain tree theorem),
the ring paper's Lemma 1, Lemma 2 and Theorem A, and Lemma B for q = 1 are statements about a finite chain
with kernel eps^r (1 - eps)^(n - r) and use no rotation. What does use the ring: Lemma B for q > 1 (gamma
constant on a rotation orbit), Lemma Z (the states one flip from 0 are the rotations of e_0), Lemma H (local
healing on Z/nZ), and the rotation orbits that the solver uses to save BFS runs.

**Symmetries [proved].** Let phi be a bijection of {0,1}^n that preserves Hamming distance, with
phi o F_R = F_R' o phi, and let pi be a permutation of codes with codes(phi x) = pi(codes(x)). Then phi maps
the noisy chain of R to that of R' (transition probabilities depend only on H(F x, y)), cycles to cycles,
R(C -> C') to R(phi C -> phi C'), gamma to gamma; so the noise-selected cycles correspond and
k'_{pi(c)} = k_c, k*' = k*, and the missed codes are mapped by pi.
(i) Reflection x_i -> x_{n-1-i} is such a phi for R' = refl R and every boundary type considered (ring, null,
one, reflect), with pi swapping 1 <-> 4 and 3 <-> 6: reversing the row turns the wall at -1 into the wall at n.
(ii) Complement x -> NOT x is such a phi for R' = R* (the complement conjugate, f*(c) = 1 - f(7 - c)) with
pi(c) = 7 - c, but it maps null walls to fixed-1 walls: (NOT x) seen with walls 1 is NOT of (x seen with walls
0). It preserves ring and reflecting walls. Hence fixed-1 walls need no run of their own: R under fixed-1 walls
is R* under null walls. Complement is not a symmetry of the null problem.
Checked numerically (`code/fw/test_boundaries.py`, tests WALL_reflection_conjugation and
WALL_complement_maps_null_to_one): for all 256 rules and n = 1..10, the conjugation identities of the
successor maps and of the code masks hold exactly [computed].

**Unit of classification.** Under null walls only reflection remains, so the right unit is the reflection
class: 256 rules form **160 null classes** (64 rules are reflection-symmetric). Each of the 88 ring classes
{R, refl R, R*, refl R*} becomes two null classes, [R] and [R*], except for 16 ring classes where they
coincide (15, 23, 29, 43, 51, 57, 77, 105, 142, 150, 156, 170, 178, 184, 204, 232) [computed,
`code/fw/null_classes.py`]. The 160 null classes cover the null and the fixed-1 boundary at once. The named
rules split as follows (null class of R; null class of R* = R under fixed-1 walls):

| ring class | null class of R | null class of R* |
|---|---|---|
| 22 | {22} | {151} |
| 26 | {26, 82} | {167, 181} |
| 35 | {35, 49} | {59, 115} |
| 37 | {37} | {91} |
| 43 | {43, 113} | same |
| 45 | {45, 101} | {75, 89} |
| 60 | {60, 102} | {153, 195} |
| 73 | {73} | {109} |
| 90 | {90} | {165} |
| 94 | {94} | {133} |
| 122 | {122} | {161} |
| 142 | {142, 212} | same |
| 154 | {154, 210} | {166, 180} |
| 150 | {150} | same |

**Code.** `code/fw/fwlib.py`: `succ_map(rule, n, boundary="ring")`, `code_mask(n, boundary="ring")`,
`CycleStructure(..., boundary="ring")`, `classify(..., boundary="ring")` with `boundary` in
{"ring", "null", "one", "reflect"}. The ring code path is unchanged (the wall versions are a separate branch
of each function). With walls the solver uses the trivial symmetry group (one BFS per cycle; `rot1` is the
identity), so EdgeStore and the Edmonds contraction are used unchanged. `cert.py` writes a `boundary` field
for wall certificates only (ring certificates stay byte-identical); `check_cert.py` reads it and builds its own
successor map and code mask from an explicitly padded row (independent of `fwlib`).

**Guarding test** (`code/fw/test_boundaries.py`, 20 tests, 3 s): (1) succ_map and code_mask on the ring equal
verbatim copies of the version-0.4 functions for all 256 rules, n = 1..12; (2) the ring results for n = 4..12
and all 88 class representatives, recomputed with the modified code, equal `data/fw_sweep.csv` in every
result field (792 records); (3) six ring certificates regenerate byte for byte; (4) the checker's ring maps
are unchanged; (5) wall maps and code masks agree with a naive per-cell implementation and with the checker;
(6) the edge-code statements above; (7) the two conjugations. The existing suites `code/fw/test_fw.py`
(21 tests) and `code/ring_size/test_ring_size.py` (16 tests) pass unchanged [computed; logs in
`data/boundaries/log_step1_tests.txt`].

## 3. Predictions (Step 2)

Sealed in `PREDICTIONS_boundaries.md` (sha256 above; saved before the first computation under walls and not
edited since). Scored in Section 7.

## 4. Computation (Step 3)

**Runs** (`code/fw/run_boundaries.py`; at most 2 worker processes, low QoS; checkpoint
`data/boundaries/null_sweep.jsonl`, append-only and fsynced through `code/fw/ckpt.py`; final table
`data/boundaries/null_sweep.csv`; per (rule, n) a detail file `data/boundaries/null_details/n{n}_rule_{r}.json.gz`
with every cycle (smallest state, period, code mask), gamma of every cycle, the selected cycles, k_c, k* and the
missed codes; certificates in `data/boundaries/null_certificates/`). The unit is the 160 reflection classes
(Section 2); every class at every n, bijective ones included, has a record. Bijective rules were not solved but
recorded with k* = 0 (justified in 5.1: the note's argument uses no ring; the GTH check below confirms them).

| batch | command | estimate | measured wall |
|---|---|---|---|
| n = 4..9, 160 classes | `run_boundaries.py --nmin 4 --nmax 9 --workers 2` | (first batch, timing run) | 104 s |
| n = 10..11 | `--nmin 10 --nmax 11` | from n <= 9 | 37 s |
| n = 12..14 | `--nmin 12 --nmax 14` (log `log_null_n12_14.txt`) | a few minutes | 90 s |
| n = 15..16, 45 classes, certificates | `--nmin 15 --nmax 16 --cert-nmax 16 --rules ...` | 0.8 min | 36 s |
| n = 15..16, remaining 115 classes | `--nmin 15 --nmax 16 --cert-nmax 14` | 1.1 min (BUG-B1) | 3.4 min |
| n = 17..20, 12 classes | `--nmin 17 --nmax 20 --cert-nmax 16 --rules 22,37,75,90,91,94,122,126,133,135,137,165` | 4.8 min | 6.4 min |
| reflecting walls, n = 4..12, 88 classes | `--boundary reflect --nmin 4 --nmax 12 --cert-nmax 12 --rules <88 class reps>` | about 1 min | 1.5 min |

Estimates: `code/fw/wall_estimate_boundaries.py` (per-rule growth factor). BUG-B1: the first version used one
common "last n" column, so the classes without data at n = 16 counted as zero; fixed (per-rule last n).
The largest job was class 76 at n = 16 (52 s, 531 MB; 19 k cycles, no rotation symmetry under walls).
n = 17..20 was not run for all classes: the dense V rows grow as m^2 (class 76: about 4 GB at n = 18).

**Checks.**
* Independent stationary laws [computed]: `code/fw/verify_boundaries.py --nmin 4 --nmax 9` builds the chain from an
  explicitly padded row (not fwlib) and computes pi by GTH at eps = 1e-11 and 1e-12 for **all 256 rules** (so the
  reflection symmetry is tested too). Every observed order of every state and of every nu_c agrees with the
  solver within 7.0e-06: 1536 of 1536 (rule, n) pass (`data/boundaries/verify_null_gth.csv`). A first run with
  eps = 1e-8, 1e-9 failed for rules 238 and 252 at n = 9 by 7e-3; the slope converges by a factor 10 per decade
  (a large second-order coefficient), so the check was moved to smaller eps; no solver change.
* Certificates [computed]: `code/fw/check_cert.py` (own successor map from a padded row, Dijkstra on the
  two-layer graph) accepted all 1760 certificates n = 4..14 and all 90 certificates at n = 15, 16
  (`log_check_null_certs*.txt`). No certificates for n >= 17.
* Tests: `code/fw/test_boundaries.py` (Section 2) and `code/fw/test_boundaries_results.py` (Proposition L by linear
  algebra agrees with the sweep for all 16 affine rules, n = 4..16; reflection partners have equal k* and mirrored
  k_c at n = 8 for all 256 rules; R under fixed-1 walls equals R* under null walls for 40 random rules, n = 6..9;
  reflecting walls are complement-symmetric): 24 passed; `test_fw.py` 21 and `test_ring_size.py` 16 passed
  unchanged (`data/boundaries/log_tests_final.txt`).
* Deterministic facts of expectation (a) (`code/fw/check_mirror.py`, `data/boundaries/check_mirror.txt`): the
  mirror embedding holds for all n = 1..10 for exactly the 16 reflection-symmetric rules with
  f(000) = f(101) = 0 (0, 4, 18, 22, 72, 76, 90, 94, 128, 132, 146, 150, 200, 204, 218, 222); rule 94 has a fixed
  point with code set exactly {3, 5, 6} iff 3 | (n + 1) for n = 3..20, but not at n = 2 (the fixed point 11 has
  codes {3, 6}); rule 90 is nilpotent exactly at n = 1, 3, 7, 15 among n = 1..20.

**Global counts** (`data/boundaries/null_sweep.csv`, `data/boundaries/ring_vs_null.csv`, `code/fw/compare_boundaries.py`) [computed]:
* 160 null classes at n = 8..16: 110 have k* >= 1 at every n, 38 have k* = 0 at every n, 12 change side
  (22, 37, 75, 90, 91, 94, 122, 126, 133, 135, 137, 165). In n = 4..14, 31 classes change side somewhere.
* Rules (all 256) with k* >= 1: ring 180, 174, 172, 188 at n = 12, 13, 14, 16; null 186, 187, 189, 187.
* Rules whose cycles jointly miss a code ("B-type", k* >= 1 by the note's Lemma 3 without any potential):
  ring 138 and 142 at n = 12 and 16; null 181 and 180. Under walls most of the classification is decided at zero
  noise.
* In 2038 of the 2040 non-bijective null records gamma_min = m - 1, i.e. G1 has a single closed class and it is
  the selected set (Theorem A of the ring paper, which uses no rotation); the exceptions are rule 218 at n = 7 and
  n = 15. 562 records have a single cycle.
* Bijective under null walls: classes 51, 60, 153, 204 at every n = 4..16; 90, 165 at even n; 150, 105 at
  n != 2 mod 3; no other class at any n = 4..16. On the ring, 154 and 45 are bijective at every odd n; under walls
  never in this range.

## 5. Ring vs null: comparison and mechanisms (Step 4)

### 5.0 Table

k* by n (`data/boundaries/ring_vs_null.csv`, printed by `code/fw/compare_boundaries.py`) [computed]. "ring" is the
ring class (data/fw_sweep.csv); "null" the null class of the same rule; "null (= fixed-1 of R)" the null class of
the complement conjugate R*, which is R under fixed-1 walls (Section 2). Empty cells: not computed (null n >= 17
only for the 12 classes that change side in n = 8..16). Classes 30, 110, 126 are added because their
fixed-1 partners (135, 137, 129) change side under walls.

| ring class | boundary | rule | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 94 | ring | 94 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| | null | 94 | 1 | 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| | null (= fixed-1 of 94) | 133 | 0 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 43 | ring | 43 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| | null | 43 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| 142 | ring | 142 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| | null | 142 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| 35 | ring | 35 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| | null | 35 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| | null (= fixed-1 of 35) | 59 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| 26 | ring | 26 | 2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 2 | 0 | 1 | 1 | 0 |
| | null | 26 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 |  |  |  |  |
| | null (= fixed-1 of 26) | 167 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| 37 | ring | 37 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| | null | 37 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| | null (= fixed-1 of 37) | 91 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 |
| 154 | ring | 154 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| | null | 154 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 1 |  |  |  |  |
| | null (= fixed-1 of 154) | 166 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| 22 | ring | 22 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| | null | 22 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| | null (= fixed-1 of 22) | 151 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| 60 | ring | 60 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| | null | 60 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| | null (= fixed-1 of 60) | 153 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| 90 | ring | 90 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| | null | 90 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 |
| | null (= fixed-1 of 90) | 165 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 122 | ring | 122 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| | null | 122 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| | null (= fixed-1 of 122) | 161 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| 45 | ring | 45 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| | null | 45 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| | null (= fixed-1 of 45) | 75 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 1 |
| 73 | ring | 73 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| | null | 73 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| | null (= fixed-1 of 73) | 109 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| 150 | ring | 150 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| | null | 150 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| 30 | ring | 30 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| | null | 30 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |
| | null (= fixed-1 of 30) | 135 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 |
| 110 | ring | 110 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| | null | 110 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |
| | null (= fixed-1 of 110) | 137 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 126 | ring | 126 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| | null | 126 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| | null (= fixed-1 of 126) | 129 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  |  |  |  |


Short form, n >= 8 (`ring` from the ring paper; `null` from this table; n <= 20 where computed):

| ring class | ring | null, R | null, R* (= R under fixed-1 walls) |
|---|---|---|---|
| 94 | k* >= 1 iff 3 \| n | k* >= 1 iff 3 \| (n + 1) (+ n = 4, 7) | 133: k* >= 1 iff 3 \| n (+ n = 5) |
| 43, 142 | k* >= 1 iff 4 \| n | k* = 1 at every n (B-type) | same classes |
| 35 | k* >= 1 iff 3 \| n | k* = 1 at every n (B-type, one cycle) | 59: k* = 1 at every n (B-type) |
| 60 | k* >= 1 iff n = 2^k | k* = 0 (bijective) | 153: k* = 0 (bijective) |
| 90 | k* >= 1 iff n = 2^k | k* = 2 iff n + 1 = 2^k, else 0 [proved] | 165: k* = 1 iff n + 1 = 2^k, else 0 [proved] |
| 154 | k* >= 1 iff n = 2^k | k* = 2 iff n + 1 = 2^k, else 1 (B-type) | 166: k* = 1 at every n (B-type) |
| 26 | 2^k: zero state; else code 7 | same as 154 | 167: k* = 0 at every n |
| 22 | seed set {2^k - 2, 2^k - 1, 2^k, ...} | k* = 1 at n = 14 only (n = 7..20) | 151: k* = 0 |
| 122 | k* = 0 iff 4 \| n (to 20) | k* = 1 at n = 15 only (n = 8..20) | 161: k* = 1 at every n (B-type) |
| 37 | k* = 0 iff n mod 6 in {0, 5} | k* = 0 iff n = 1 mod 3 | 91: k* >= 1 iff n = 1 mod 3 |
| 45 | only n = 8 | k* = 0 at every n | 75: k* = 0 iff 3 \| n |
| 73 | only n = 9 | k* = 0 at every n | 109: k* = 0 at every n |
| 150 | 0 (n >= 7) | k* = 0 at every n >= 6 [proved] | (self) |
| 30 | 0 (n >= 7) | k* = 1 at every n (B-type) | 135: k* >= 1 iff n even |
| 110 | 0 (n >= 6) | k* = 0 | 137: k* >= 1 iff n odd and n >= 11 (to 19) |
| 126 | 1 | k* = 1 at n = 8, 15 only (n = 8..20) | 129: k* = 1 at every n (B-type) |

In words: none of the ring's arithmetic conditions survives unchanged. Two survive shifted (the walls act as
cells of the pattern): the period-3 crystal of class 94, now at 3 | (n + 1) with zero walls and at 3 | n with
one-walls, and the nilpotency of rule 90, now at n + 1 = 2^k. The travelling mechanisms (43, 142, 35) disappear,
and with them the switching: these classes become B-type (a code on no cycle at all), so k* >= 1 at every n.
New dependences on n appear that have no ring counterpart (37 and 91 mod 3, 75 mod 3, 135 parity, 137 odd n).

### 5.1 Affine rules [proved]

Under null (or fixed-1) walls an affine ECA f(l, c, r) = a l + b c + d r + e (over GF(2); 16 rules) acts as
F x = M x + e·1, M tridiagonal with a below, b on and d above the diagonal (the walls contribute 0; with
fixed-1 walls they add a constant vector, which keeps F affine).

**Lemma 0 (one-flip edges; PROOF_154.md, Lemma 0, uses no ring).** For cycles C != C', V(C, C') = 1 iff there
are x in C and a cell i such that the F-orbit of x + e_i enters C'. (Proof as there: a resistance-1 path makes
one flip after a step that lands on a state of C.)

**Proposition L.** Let F x = M x + v on {0,1}^n (any boundary for which F is affine). Then G1 is strongly
connected; all cycles are noise-selected, gamma_min = m - 1, and k* = 0 iff the periodic states jointly contain
all eight codes.
*Proof.* Fitting decomposition: V = V_nil + V_inv with M nilpotent on V_nil (M^n = 0 there) and invertible on
V_inv; V_inv = M^T V for every T >= n. For T >= n, F^T(x) = M^T x + s_T with s_T = sum_{j<T} M^j v, so the
eventual image, which is the set P of periodic states, is the coset s_T + V_inv, and F permutes P. Choose T >= n
a multiple of the order of that permutation; then F^T(y) = y for y in P and, for y in P and any cell i,
F^T(y + e_i) = F^T(y) + M^T e_i = y + g_i with g_i := M^T e_i in V_inv. So by Lemma 0 the cycle of y has a
G1-edge to the cycle of y + g_i (when different), for every y in a cycle and every i. The reverse edge exists:
from y + g_i (a periodic state) flip cell i again to reach the cycle of y + g_i + g_i = y. The g_i span
M^T V = V_inv, so for y, y' in P, y' - y = g_{i1} + ... + g_{ik} gives a G1-path. Hence G1 (on m cycles) is
strongly connected, its unique closed class is the set of all cycles, and by Theorem A of the ring paper (whose
proof uses no rotation) every cycle is selected with gamma_min = m - 1; k* = 0 iff the selected cycles, i.e. all
periodic states, jointly contain every code (note, Theorem 1). If M is nilpotent, P is a single fixed point. ∎

**Lemma F (fixed points).** A fixed point x of any ECA under any walls contains only codes c with
f(c) = middle bit of c (cell i reads c and keeps its value). ∎

**Lemma W (window).** Let M be symmetric (a = d) and P = x* + V_inv as above. If no nonzero vector supported on
the cells {0, 1, 2} lies in V_nil, then all eight codes occur at cell 1 in states of P.
*Proof.* For K >= n, V_inv = im M^K and, M being symmetric, V_inv^perp = ker (M^K)^t = ker M^K = V_nil. The
projection of V_inv to the coordinates {0, 1, 2} is onto GF(2)^3 iff no nonzero functional supported there
vanishes on V_inv, i.e. iff no nonzero u supported on {0, 1, 2} lies in V_nil. A translate of an onto projection is
onto, so every pattern (x_0, x_1, x_2), i.e. every code at cell 1, occurs in P. ∎

**Lemma M (mirror embedding).** For a reflection-symmetric rule with f(000) = f(101) = 0, define the lift of a
row x (n cells) to the ring of N = 2n + 2 cells by ring cell j = x_j and ring cell N - 2 - j = x_j (0 <= j < n),
ring cells n and N - 1 equal to 0. Then F_ring(lift x) = lift(F_null x).
*Proof.* The lift is invariant under the two reflections j -> -2 - j and j -> 2n - j of Z/NZ, which fix the
cells N - 1 and n. A reflection-symmetric rule commutes with both, so the image is invariant too. A cell fixed
by a reflection whose two neighbours are mirror images reads a code (a, b, a) with b its own value; with b = 0
the new value is f(a0a) in {f(000), f(101)} = {0}. So the wall cells stay 0, and the cells 0..n-1 read exactly
the codes they read in the null row. ∎ (For rule 90 this is Vadali and Turner, Thm. 6.2, p. 12. Checked for all
256 rules, n <= 10: it holds for exactly the 16 rules with these properties, `check_mirror.txt`.)

For linear rules the lift is an injective linear map with M_ring · lift = lift · M_null, so it maps V_nil of
the row into the generalised kernel of M_ring. On the ring, identify a state with a polynomial modulo z^N - 1.

**Theorem 90.** Under null walls, for n >= 4: rule 90 has k* = 2 if n + 1 is a power of two, and k* = 0
otherwise. Rule 165 (= rule 90 under fixed-1 walls) has k* >= 1 iff n + 1 is a power of two (k* = 1 computed
for n = 7, 15).
*Proof.* M = A (path adjacency), symmetric; rule 165 is A x + 1. Write n + 1 = 2^a b, b odd, N = 2^(a+1) b.
M_ring = z + z^(-1), and (z + z^(-1))^K U = 0 iff (1 + z)^(2K) U = 0 mod z^N - 1. With
z^N - 1 = (1 + z)^(2^(a+1)) Q^(2^(a+1)), Q = (z^b - 1)/(z - 1) (Q(1) = b = 1 mod 2, so Q is coprime to 1 + z),
U lies in the generalised kernel iff Q^(2^(a+1)) divides U.
(i) b = 1: z^N - 1 = (1 + z)^N, so (z + z^(-1))^N = 0, M_ring is nilpotent and so is A (the lift is injective).
P = {0} for rule 90: 0 is the only cycle. A resistance-1 path from 0 is a flip e_i followed by free steps, and
the rule-90 orbit of e_i has all its ones on one parity class at each time (each cell is the sum of its two
neighbours), so no state reached with resistance 1 contains 011, 110 or 111; codes 1, 2, 4 (e_i) and 5
(A e_i, interior i, n >= 3) cost 1, code 0 costs 0; two adjacent flips give 011 and 110, and a flip of cell i
at the state A e_i gives 111, each at cost 2: k* = 2. For rule 165, P is one fixed point; by Lemma F it contains only codes with c_mid = 1 + l + r, i.e.
{1, 2, 4, 7}; so it misses 0, 3, 5, 6 and k* >= 1 (Proposition L, or the note's Lemma 3).
(ii) b >= 3. If n is even (a = 0), A is invertible (det A = 1: the recursion p_n(0) = p_{n-2}(0), p_0 = 1,
p_1(0) = 0) and F is bijective: k* = 0. If a >= 1: let u != 0 be supported on {0, 1, 2}. Its lift has support in
{0, 1, 2, N - 4, N - 3, N - 2}; multiplied by z^4 it is a nonzero polynomial of degree <= 6. If u were in V_nil,
this polynomial would be in the generalised kernel, hence divisible by Q^(2^(a+1)), of degree
(b - 1) 2^(a+1) >= 2·4 = 8 > 6: impossible. By Lemma W all codes occur in P, and by Proposition L k* = 0
(for rule 165, P is a coset of the same V_inv). ∎
Linear-algebra check of the statement for n = 3..128, all 16 affine rules (`code/fw/affine_null.py`,
`data/boundaries/affine_null.csv`) [computed]: rule 90 and 165 have k* >= 1 exactly at n = 3, 7, 15, 31, 63, 127.

**Theorem 150.** Under null walls rule 150 is bijective iff n != 2 mod 3, and k* = 0 for every n >= 4 except
n = 5, where k* = 1. The same holds for rule 105 (= 150 + 1).
*Proof.* M = A + I, M_ring = z^(-1)(1 + z + z^2). Write N = 2n + 2 = 2^s q, q odd; z^N - 1 = (z^q - 1)^(2^s) with
z^q - 1 squarefree. 1 + z + z^2 is irreducible and divides z^q - 1 iff 3 | q iff 3 | (n + 1). If 3 does not divide
n + 1, M_ring is invertible, hence M is (lift injective): bijective, k* = 0. If 3 | (n + 1), write
z^q - 1 = (1 + z + z^2) R with R coprime to 1 + z + z^2; U is in the generalised kernel iff R^(2^s) divides U,
degree (q - 2) 2^s. A nonzero u in V_nil supported on {0, 1, 2} would give a nonzero polynomial of degree <= 6
divisible by R^(2^s), so (q - 2) 2^s <= 6; with 3 | q, q odd, s >= 1 this leaves q = 3, s in {1, 2}, i.e. N = 6
or 12, n = 2 or 5. For n >= 4, n = 2 mod 3, n != 5, Lemma W and Proposition L give k* = 0; also V_nil != 0, so F is
not bijective. At n = 5 the characteristic polynomial of M is (x + 1) x^4, so V_inv = ker(M + I) = ker A = {00000, 10101}
(10101 is a fixed point): codes {0, 2, 5}, so k* >= 1; k* = 1 [computed]. Non-bijectivity at n = 2 mod 3: the
state 11011...011 (blocks 110, ending in 11) is in ker M (every window sums to 0 with the walls). Rule 105 =
M x + 1 has the same M (k* = 1 at n = 5 computed). ∎

**Classes 60, 153 and the shifts.** Rule 60 (and 102, 153, 195) has M unit lower (upper) triangular, so F is
bijective at every n and k* = 0 (Martín del Rey, pp. 120-121, for 60 and 102). Rules 170, 240 (shifts) and
15, 85 (complemented shifts) have M nilpotent: one fixed point, which by Lemma F carries few codes: k* >= 1 at
every n (k* = 3 for 170/240 and 1 for 15/85 at n = 4..16 [computed]).

**Bijective rules (note's argument, checked for walls).** For bijective F, sum_x P(x, y) =
sum_x q(F(x) + y) = sum_z q(z) = 1 (q(z) = eps^|z| (1 - eps)^(n - |z|)), so P is doubly stochastic, the uniform law
is stationary, every state has order 0, and k* = 0 because every code occurs in some state (n >= 3, an interior
cell). Nothing in this uses the ring. [proved]

So the ring's power-of-two mechanism for 60 and 90 disappears for 60 (no nilpotency under walls) and moves to
n + 1 = 2^k for 90; 150 gains one exceptional size, n = 5.

### 5.2 Crystals with the walls as pattern cells: 94, 133, 75 [computed; radius computed to n = 62]

*Class 94, null walls.* At every n = 2 mod 3 in 8..20 the only selected cycle is the fixed point
11011...011 (the ring crystal (011) with the two walls as its zeros), codes {3, 5, 6}, gamma_min = m - 1 (G1 has a
single closed class, the crystal), k* = 1 (missed 0, 1, 2, 4, 7) (`null_details`). Its radius is 2 at every
n = 2 mod 3, 5 <= n <= 62 (every single flip of it returns; `code/fw/local_boundaries.py`,
`data/boundaries/local_radius.csv`). The crystal exists iff n = 2 mod 3 (n >= 5; check_mirror (2)), so at
n = 0, 1 mod 3 there is no capture and k* = 0 for n = 9..19 (all cycles but one selected; e.g. 336 of 337 at
n = 16). Exceptions n = 4 and 7: k* = 1 because the selected cycles (3 of 4, 7 of 8) contain no 000 (too short a
row). This is the ring mechanism (crystal capture, Lemma B with q = 1) with the arithmetic shifted from 3 | n to
3 | (n + 1), as expectation (a) said; one flip in the row is two symmetric flips on the ring of 2n + 2, and the
crystal still heals, because flips next to a wall heal like interior ones (checked, not proved for all n).
Not proved: reachability of the crystal from every cycle (computed n <= 20).

*Class 133 (= 94 under fixed-1 walls).* At every n = 0 mod 3 in 6..18 the only selected cycle is (010)^(n/3)
(in the 94 picture: 1|101101...101|1, the crystal with each wall as one of a pair of ones), codes {1, 2, 4},
k* = 1, radius 2 at every 3 | n, 6 <= n <= 60 (`local_radius.csv`). Other placements of the crystal against
one-walls exist at every n (my prediction relied on them), but they are not selected (n = 4 by hand: radius 1).
At n = 1, 2 mod 3 every cycle is selected and k* = 0 (n >= 7). Exception n = 5.

*Class 75 (= 45 under fixed-1 walls)*, new: rule 75 (codes 000, 001, 011, 110 -> 1) also fixes the (011) crystal.
n = 2 mod 3: the crystal 11011...011 is selected alone; n = 1 mod 3: a 2-cycle "crystal with a defect at the
right wall" (1101101...1100 <-> ...1101) is selected alone, missed codes 001 and 111; 3 | n: k* = 0 (n = 6..18;
at n = 12 all 7 cycles are selected). But the crystal's radius drops to 1 at n = 44, 47, ..., 62 (every n = 2 mod 3 from 44 in the
checked range; radius 2 for n <= 41) [computed], so the pattern "k* >= 1 iff 3 does not divide n" is not expected to
persist beyond about n = 41 [observed].

### 5.3 Zero state and single flips: 154, 26, 22, 122, 126

**Lemma Z' (zero state under walls).** If F(0) = 0, then r(0) >= 2 iff the orbit of every single flip e_i,
i = 0..n-1, returns to 0 (Lemma 0). Without rotation all n seeds count (n/2 for reflection-symmetric rules). [proved]

**Proposition N (154, 26) [proved].** Under null walls, for rules 154 and 26 the orbit of e_i equals the rule-90
orbit of e_i, so r(0) >= 2 iff n + 1 is a power of two.
*Proof.* Rule 154: f = r + l(1 + c); rule 26: f = l + r if c = 0, f = r(1 + l) if c = 1. Let x have all its ones
on one parity class (walls 0). At a cell with x_i = 0 both rules give l + r = (A x)_i; at a cell with x_i = 1 both
neighbours are 0 (same parity; walls 0), and both rules give 0 = (A x)_i. So F x = A x, which again has its
ones on one parity class (the other one). By induction F^t e_i = A^t e_i. All e_i die iff A is nilpotent iff
n + 1 = 2^k (Theorem 90, (i) and (ii): for b >= 3 the lift of e_0, z^2 + 1 after rotation, has degree 2 < 8). ∎

*What the computation adds [computed n = 4..16].* For both rules every cycle under null walls lies in the
one-parity set: no cycle contains 011, 110 or 111 (cycle codes union = {0, 1, 2, 4, 5} at every n except the
nilpotent n = 7, 15, where 0 is the only cycle). So both rules are B-type at every n: k* = 1, and k* = 2 at
n = 7, 15 (one cycle, as for rule 90). The two rules have identical cycle counts at every n = 4..16 (2, 3, 2, 1,
4, 4, 2, 6, 2, 6, 12, 1, 20). On the ring at even n, rule 154 permutes the states with ones on both parity
classes (PROOF_154.md, Lemma 6; its proof of F(M) ⊆ M goes once around the ring). Under walls the
"11" defect travels left one cell per step and disappears at the left wall (space-time printed in this session; the
left edge cell reads (0, x_0, x_1) and simply copies x_1), so the mixed-parity states are transient [observed;
the statement "every orbit enters the one-parity set" is not proved here]. The ring mechanism (nilpotency of
the single-flip orbit) carries over at n + 1 = 2^k; what changes the classification at every other n is that the
travelling defects that carried codes 3, 6, 7 on the ring are absorbed by a wall.

*Rules 167 and 166 (fixed-1 walls).* 167 (26 under fixed-1 walls): k* = 0 at every n = 4..16. 166 (154 under
fixed-1 walls): the cycles jointly carry only the codes {0, 2, 4} at every n = 4..16 (n = 10: the two fixed
points 0 and 100...0, both selected): B-type, k* = 1 at every n.

*Class 22 (mirror embedding applies).* k* = 1 at n = 14 (and 4, 5, 6) with the zero state selected alone
(n = 6: it is the only cycle; n = 14: 1 of 11 cycles, gamma_min = m - 1). Seed orbits (`local_seed.csv`): all
n single flips die exactly at n = 6, 14, 30, 62 among n = 4..54 and 58..62 (n = 55, 56, 57 undecided at 2·10^4
steps) [computed]. So the zero mechanism survives at n = 2^k - 2 (n + 1 = 2^k - 1); in the mirror picture the
ring has N = 2n + 2 = 2^(k+1) - 2 cells, a size at which the ring's own single seed returns (ring paper, 5.3:
14, 30, 62, 126 are in its return set). The other even ring return sizes (N = 2^k, e.g. N = 16 for n = 7) do
not appear. Why the symmetric pair of seeds
dies exactly there is not explained [observed].

*Class 122.* k* = 1 at n = 15 (and 4, 5, 7) with the checkerboard 2-cycle 0101... <-> 1010... selected alone
(radius 2, missed 0, 3, 6, 7). Under walls the checkerboard exists at every n (it carries code 010 at every n, so
the ring's parity obstruction for code 2 disappears), but its radius is 2 only at n = 7 and 15 among n = 4..61
(`local_radius2.csv`), so the pattern is not 2^k - 1: at n = 31 the checkerboard has radius 1 [computed]. The ring
mechanism for 122 (zero state at 2^k - 1, checkerboard at 4 | n) is replaced: the zero state never has radius 2
under walls (some single flip never dies at every n = 4..62), and the checkerboard is isolated only at 7 and 15.
*Class 126* (symmetric, f(101) = 1): k* = 1 at n = 7, 8, 15 (missed 000 at n = 8, 15; at n = 7 a single
selected 2-cycle missing 000, 001, 100); not explained.
*Class 161 (= 122 under fixed-1 walls)* and *129 (= 126 under fixed-1 walls)*: B-type at every n.

### 5.4 Travelling crystals disappear: 43, 142, 35 [computed n = 4..16]

Under null walls the ring's travelling crystals cannot exist, and none of the three classes switches: all are
B-type at every n = 4..16. Class 43: floor(n/2) cycles, code 101 on no cycle. Class 142: ceil(n/2) + 1 cycles,
codes 001, 011, 110, 111 on no cycle. Class 35: a single cycle at every n (codes {0, 3, 6, 7}); its partner 59:
codes 000, 011, 110, 111 on no cycle. Expectation (b) is confirmed: the 4 | n pattern disappears; what replaces it
is not a different selection but the absence of the codes from every cycle, decided at zero noise.

### 5.5 Dependences on n created by the walls: 37, 91, 135, 137 [computed n = 4..20; observed patterns]

* *37 (null): k* = 0 iff n = 1 mod 3* (n = 4..20 without exception). The selected set always contains the
  domain-wall 2-cycles (blocks 1^a 0^b <-> 0^a' 1^b', codes 0, 1, 3, 4, 6, 7). Codes 010 and 101 are carried
  only by the period-3 fixed points (010)^k (excess potential >= 1, not selected at n = 9..13, the sizes inspected) and, at n = 1 mod 3, by a
  6-cycle on the period-6 pattern 100000 (e.g. 1000001000 at n = 10, 0001000001000 at n = 13), which is
  selected; this is the ring's period-6 family (ring paper 5.5) placed between walls.
* *91 (= 37 under fixed-1 walls): k* >= 1 iff n = 1 mod 3* (n >= 7; also n = 4, 5, 6), missed code 5 (101): the
  complement of the 37 statement, i.e. with one-walls the same family loses the code exactly where with
  zero-walls it gains it.
* *135 (= 30 under fixed-1 walls): k* = 1 iff n is even* (n = 4..20): two cycles, both selected: the checkerboard
  fixed point 1010...10 and a 2-cycle that differs from it at the right end; missed codes 001 and 111. At odd n the
  second cycle is a 4-cycle carrying all codes.
* *137 (= 110 under fixed-1 walls): k* = 1 at odd n >= 11* (11..19; also 4, 5, 7). The 2-cycle 1000 1000 ... <->
  0010 0010 ... (spatial period 4; codes 0, 1, 2, 4) is selected alone, radius 2 at n = 7 and every odd n from 11
  to 61, not at n = 9 (`local_radius2.csv`). At even n the pattern is not periodic and all cycles carry all codes.
None of these four is proved; the descriptions of the carriers are from the detail files.

### 5.6 Where the ring mechanisms go

| ring mechanism | ring classes | under null walls |
|---|---|---|
| crystal of period p closes iff p \| n | 94 | **carries over shifted**: closes iff 3 \| (n + 1) (walls as zeros); with one-walls iff 3 \| n |
| travelling crystal (period 4, 3) | 43, 142, 35 | **disappears**; replaced by B-type at every n (codes absent from all cycles) |
| nilpotent single-flip orbit at n = 2^k | 60, 90, 154, 26 | 60: **disappears** (bijective); 90, 154, 26: **carries over shifted** to n + 1 = 2^k [proved]; 154, 26 off 2^k - 1: **replaced** by B-type (defects absorbed by the left wall) |
| zero state, seed returns | 22 | **carries over partly**: only at n = 2^k - 2 (to n = 62) |
| zero state at 2^k - 1, checkerboard at 4 \| n | 122 | **replaced**: checkerboard selected at n = 7, 15 only |
| period-6 defect family | 37 | **carries over** as a mod-3 condition (37: n = 1 mod 3), mirrored by 91 |
| isolated switches (45 at 8, 73 at 9) | 45, 73 | **disappear** (k* = 0 for n >= 6) |
| (none) | 75, 133, 135, 137 | **new**: wall-made crystals and patterns |

## 6. Reflecting walls (Step 5) [computed n = 4..12]

Cell -1 copies cell 0 and cell n copies cell n - 1. Both reflection and complement are symmetries (Section 2), so
the unit is the 88 ring classes. Run: `run_boundaries.py --boundary reflect --nmin 4 --nmax 12` (1.5 min);
`data/boundaries/reflect_sweep.csv`, details and 792 certificates (all accepted by `check_cert.py`); GTH check
n = 4..8, all 256 rules, 1280 of 1280 pass (`verify_reflect_gth.csv`).

**Lemma M' [proved].** For every reflection-symmetric rule, the reflecting row of n cells is the mirror-symmetric
subspace of the ring of 2n cells (ring cell j = x_j = ring cell 2n - 1 - j): the mirror axes lie between cells, a
cell next to an axis reads its own value as the outside neighbour, which is the reflecting wall. No condition on
f(000), f(101) is needed. Checked: holds for exactly the 64 symmetric rules, n = 1..10
(`code/fw/check_mirror_reflect.py`, `data/boundaries/check_mirror_reflect.txt`). Consequently rule 90 under
reflecting walls is nilpotent iff 2n is a power of two, i.e. n is (n = 1, 2, 4, 8, 16 among 1..16 [computed]).

| | ring | reflect |
|---|---|---|
| classes with k* >= 1 at n = 12 | 60 | 62 |
| B-type classes at n = 12 | 42 | 59 |
| classes changing side in n = 8..12 | 13 | 1 (class 90) |
| classes on the same side as the ring at every n = 8..12 | | 65 of 88 |

| class | boundary | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|
| 94 | ring | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| | reflect | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 43 | ring | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| | reflect | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 142 | ring | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| | reflect | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 35 | ring | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 |
| | reflect | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 26 | ring | 2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 |
| | reflect | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 37 | ring | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 |
| | reflect | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 154 | ring | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| | reflect | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 22 | ring | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| | reflect | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 60 | ring | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| | reflect | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 90 | ring | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| | reflect | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 122 | ring | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| | reflect | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 45 | ring | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| | reflect | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 73 | ring | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 |
| | reflect | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 150 | ring | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |
| | reflect | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 |

What carries over: the power-of-two mechanism of rule 90 (k* = 1 at n = 4, 8; nilpotent at powers of two) with
the ring's own arithmetic, because of Lemma M'. What disappears: everything else that switches on the ring.
Class 94: the crystal 101101... exists under reflecting walls exactly at 3 | n (n = 6, 9, 12, 15), but a single
flip at an edge leaves it (radius 1 at all four sizes, `check_mirror_reflect.txt`), and k* = 0 for n >= 5.
Class 154 has k* = 2 at every n = 4..12, 43, 142, 35, 37, 122 have k* = 1 at every n (B-type or capture, not
analysed), 26, 60, 45, 73 have k* = 0 for n >= 6. Rule 60 is not bijective under reflecting walls (cell 0 reads
x_0 + x_0 = 0); 150 is bijective iff 3 does not divide n (n = 4..12 [computed]; by Lemma M' this is
bijectivity of rule 150 on the ring of 2n).

## 7. Predictions scored

Scored on n = 4..16 (n = 17..20 where computed) against `data/boundaries/null_sweep.csv`.

| item | conf. | prediction (short) | outcome | score |
|---|---|---|---|---|
| G1 | M | ring conditions do not survive as such; where they survive, the arithmetic moves to n + 1 | 94 at 3 \| (n + 1), 90, 154, 26 at n + 1 = 2^k; but 22 at n + 1 = 2^k - 1, and under fixed-1 walls 133 at 3 \| n | correct for null walls; the fixed-1 shift was not foreseen |
| G2 | M | travelling mechanisms (43, 142, 35, 26 off 2^k) disappear | all four lose their ring pattern; replaced by B-type at every n | correct |
| G3 | H | Proposition L | proved (5.1); enumeration agrees for all 16 affine rules | correct |
| G4 | H/M | bijective => k* = 0; shifts 170/240 k* = 3, 15/85 k* = 1 at every n | as predicted (n = 4..16) | correct |
| G5 | L | more rules with k* >= 1 under null than on the ring at n = 12..14 | 186/187/189 vs 180/174/172 (at n = 16: 187 vs 188) | correct |
| G6 | M | >= 90 % of the ring's always-k* >= 1 rules keep k* >= 1 at n = 12..14 | 153 of 166 (92 %) at each n | correct |
| G7 | L | 15..40 null classes change side in n = 8..14 | 9 | wrong |
| (a) 94 | Frank | k* >= 1 iff 3 \| (n + 1) | true for n = 8..20; fails at n = 4 and 7 (k* = 1, missed 000) | correct for n >= 8 |
| (a) 90 | Frank | k* >= 1 iff n + 1 is a power of two | true; proved for every n >= 4 (Theorem 90), k* = 2 there | correct |
| (a) facts | Frank | mirror embedding; 94 fixed point {3,5,6} iff 3 \| (n + 1); 90 nilpotent iff n + 1 = 2^k | confirmed; embedding proved (Lemma M) and holds for exactly 16 rules; the fixed point statement fails only at n = 2 (outside his range) | correct |
| (b) | Frank | 4 \| n pattern of 43, 142 disappears | k* = 1 at every n = 4..16 (B-type) | correct |
| (c) | Frank | 60 bijective for all n, 150 iff n != 2 mod 3; then k* = 0 | confirmed and proved (5.1); open case answered: k* = 0 at n = 2 mod 3 except n = 5 (k* = 1) [proved] | correct |
| 60, 153 | H | k* = 0 every n | yes | correct |
| 90 | H/M | k* = 2 at 7, 15; 0 elsewhere | yes (and proved) | correct |
| 165 | H/M | k* >= 1 iff n + 1 = 2^k | yes (k* = 1), proved | correct |
| 150 | H/M | k* >= 1 only at n = 5 | yes, proved | correct |
| 154 | H/M | r(0) >= 2 iff n + 1 = 2^k (H); k* = 1 at 7, 15 and 0 elsewhere (M) | radius statement proved; but k* = 2 at 7, 15 and k* = 1 at every other n (B-type) | radius correct; values wrong |
| 166 | L | k* = 0 for n >= 8 | k* = 1 every n (B-type) | wrong |
| 26 | H/M/L | k* >= 1 at 7, 15 (M); k* = 0 at most other n (L) | k* >= 1 at 7, 15 (= 2); k* = 1 at every other n | partly (M part correct, L part wrong) |
| 167 | L | k* = 0 for n >= 8 | yes | correct |
| 22 | L | k* >= 1 at 7, 15, perhaps 6, 14; 0 at 9..13 | k* = 1 at 4, 5, 6, 14; 0 at 7..13, 15..20 | partly (6, 14, 9..13 right; 7, 15 wrong) |
| 151 | L | k* = 0 for n >= 8 | yes | correct |
| 122 | L | ring pattern disappears; k* = 0 at most n >= 8 | k* = 1 only at n = 15 in 8..20 | correct |
| 161 | L | k* = 0 at most n >= 8 | k* = 1 every n (B-type) | wrong |
| 94 | M | k* = 1 iff 3 \| (n + 1), n >= 5 (n = 4 possible exception) | correct for n >= 8, exception n = 4 as allowed, unforeseen exception n = 7 | partly |
| 133 | L | k* >= 1 at every n >= 8 (crystal fits at every n against one-walls) | k* >= 1 iff 3 \| n; only one placement is selected | wrong |
| 43, 142 | M/L | no 4 \| n; 142 k* >= 1 every n; 43 constant | yes (both k* = 1) | correct |
| 35, 59 | M/L | 3 \| n pattern disappears; k* constant | yes (k* = 1) | correct |
| 37 | L | mod-6 pattern disappears; k* >= 1 at most n | mod 6 gone, but k* = 0 iff n = 1 mod 3 | partly |
| 91 | L | k* >= 1 at most n | k* >= 1 iff n = 1 mod 3 (n >= 7) | wrong |
| 45 | L | k* = 0 for n >= 8 except isolated n | k* = 0 at every n | correct |
| 75 | L | k* = 0 for n >= 8 except isolated n | k* = 0 iff 3 \| n | wrong |
| 73, 109 | L | k* = 0 for n >= 8 except isolated n | yes, no exceptions | correct |

Mine: 28 items (G1-G7 and 21 class rows; 60/153, 43/142, 35/59, 73/109 count as one each): 17 correct,
5 partly correct, 6 wrong. All H statements held. All six wrong items were marked L; of the M statements, the
values for 154 and the exception n = 7 for 94 failed. The errors share one cause: I
expected walls to make the dynamics richer (wall-pinned structures carrying codes), whereas they mostly make it
poorer (codes absent from every cycle), and I did not foresee new crystals pinned by the walls (133, 75).
Frank's: 5 items, all correct; (a) for 94 holds for n >= 8, with the two small-n exceptions 4 and 7.

## 8. Open points

1. Class 94 (null): k* = 1 at every n = 2 mod 3 needs (i) radius 2 of the crystal (computed to n = 62; a
   locality argument with the ring paper's Lemma H, tau = 3, plus the finite check of flips near a wall would
   prove it, not written out) and (ii) one-flip reachability of the crystal from every cycle (computed n <= 20).
   k* = 0 at n = 0, 1 mod 3 is computed only (n <= 20). Same for 133 (3 | n) and 75.
2. Rules 154 and 26 (null): that every orbit enters the one-parity set (no cycle with 011, 110, 111) is computed
   for n <= 16, not proved. The "11"-defect absorption at the left wall is the observed reason.
3. Class 22: seeds all die at n = 6, 14, 30, 62 (to 62; n = 55..57 undecided). Not explained; k* beyond n = 20
   not computed.
4. Classes 122, 126 (n = 7, 15), 37/91 (n mod 3), 135 (parity), 137 (odd n >= 11): patterns observed in
   n <= 20 with the selected cycles described; none proved. For 122 the checkerboard has radius 1 at n = 31, so
   the 7, 15 pattern is not a power-of-two law. For 75 the crystal radius drops to 1 at n >= 44 (n = 2 mod 3), so
   its pattern is not expected to continue.
5. n >= 17 was computed only for 12 classes; without rotation symmetry the dense rows cost m^2 bytes (4 GB for
   class 76 at n = 18). No certificates for n >= 17.
6. Mixed walls (0 on one side, 1 on the other) were not computed; they are not covered by the symmetries.
7. Reflecting walls: only the symmetric-rule embedding (Lemma M') is explained; why 94's crystal loses its
   radius there and why 154 has k* = 2 at every n was not analysed.
8. Wang et al. 2025, Table 1, rule 195 under null walls: conflicts with the computation (Section 1).
9. The worktree, commits and `nice 10` could not be done from the sandbox (Section 9).

## Plain-words summary (for a later README; not inserted)

The earlier results were all computed on a ring: the last cell is a neighbour of the first. This study cuts the
ring open into a row whose two outer neighbours are held at 0 ("null walls"), and asks again which long-run
behaviour small noise picks out, and whether those patterns use the whole rule table.

On the ring, the answer for some rules depended on the arithmetic of the ring size: a pattern of period 3 or 4
fits only when the period divides the size, and the all-zero state shakes off any single error only when the
size is a power of two. With walls, two of these effects survive in shifted form. The period-3 pattern of
rule 94 now fits when the period divides n + 1, because the walls act as two of its cells; and the
power-of-two effect of rule 90 now appears when n + 1 is a power of two. For the additive rules 60, 90 and 150
this is proved for every row length: rule 60 never leaves part of its table unused under walls, rule 90 does
exactly when n + 1 is a power of two, and rule 150 only for a row of 5 cells.

The patterns that travel around the ring (rules 43, 142, 35) cannot travel between walls. These rules no longer
depend on the size: under walls their long-run patterns never show some neighbourhoods at all, whatever the noise,
so part of their rule table stays unobserved at every size. This is the most common effect of the walls: they
remove the travelling and rotating structures, and more rules end up with neighbourhoods that no long-run pattern
shows (181 of 256 rules at 12 cells, against 138 on the ring).

The walls also create new size effects that the ring does not have, for instance patterns that fit only when n is
a multiple of 3, or only when n is even. These are computed for rows up to 20 cells and described, but not proved.
Holding the walls at 1 instead of 0 is the same as complementing the rule, so it needs no separate computation;
reflecting walls behave much more like the ring.

## 9. How to recreate the commits

Nothing was committed: the sandbox cannot write to `~/git/eca-noise-identifiability/.git` (fetch, branch and
worktree creation fail with "Operation not permitted"), cannot create `~/git/eca-open-boundaries`, and sees no
git identity. The work tree was built from `git archive 2765f7e`; its base tree e0bb588 equals the tree of
2765f7e. The six step patches (`git diff --binary` between successive trees, saved as artifacts
`open_boundaries_step0.patch` ... `open_boundaries_step5.patch`) reproduce the steps; the git tree hash after
step 5 is given in the message that delivered the patches. Run in your own
terminal (with the patch files downloaded, here to ~/Downloads):

```sh
cd ~/git/eca-noise-identifiability
git fetch origin
git worktree add ~/git/eca-open-boundaries -b open-boundaries origin/main
cd ~/git/eca-open-boundaries
P=~/Downloads
git apply --check --numstat --summary $P/open_boundaries_step0.patch && git apply $P/open_boundaries_step0.patch && git add -A && git commit -m "Open boundaries, step 0: literature review (literature_boundaries.md)"
git apply --check --numstat --summary $P/open_boundaries_step1.patch && git apply $P/open_boundaries_step1.patch && git add -A && git commit -m "Open boundaries, step 1: boundary-aware succ_map/code_mask (ring default), symmetries, 160 null classes, guarding test"
git apply --check --numstat --summary $P/open_boundaries_step2.patch && git apply $P/open_boundaries_step2.patch && git add -A && git commit -m "Open boundaries, step 2: sealed predictions (PREDICTIONS_boundaries.md)"
git apply --check --numstat --summary $P/open_boundaries_step3.patch && git apply $P/open_boundaries_step3.patch && git add -A && git commit -m "Open boundaries, step 3: null-wall sweep n = 4..20 with checkpoints, certificates, GTH check"
git apply --check --numstat --summary $P/open_boundaries_step4.patch && git apply $P/open_boundaries_step4.patch && git add -A && git commit -m "Open boundaries, step 4: ring vs null comparison, mechanisms, affine rules proved, report"
git apply --check --numstat --summary $P/open_boundaries_step5.patch && git apply $P/open_boundaries_step5.patch && git add -A && git commit -m "Open boundaries, step 5: reflecting walls n = 4..12; report completed"
python3 -m pytest -q code/fw/test_boundaries.py code/fw/test_boundaries_results.py   # 24 tests, about 4 s
```

The commits then carry today's date, after the computations; the evidence that the predictions came first is the
artifact `PREDICTIONS_boundaries.md` saved on 24 Nov 2026 before the first wall computation, with the sha256 given
in the status block, which the committed file must match (`shasum -a 256 PREDICTIONS_boundaries.md`).
`data/MANIFEST.sha256` was not updated. Nothing was pushed.

To reproduce the data from scratch (at most 2 workers, about 20 min in total on this machine):

```sh
cd code/fw
python3 null_classes.py
python3 run_boundaries.py --nmin 4 --nmax 16 --workers 2 --cert-nmax 14
python3 run_boundaries.py --nmin 15 --nmax 16 --workers 2 --cert-nmax 16 --rules 9,22,25,37,47,54,62,73,75,90,91,94,95,105,109,111,122,123,126,127,131,133,135,137,150,151,165,169,173,182,183,26,154,166,167,161,43,142,35,59,45,60,153,15,170
python3 run_boundaries.py --nmin 17 --nmax 20 --workers 2 --cert-nmax 16 --rules 22,37,75,90,91,94,122,126,133,135,137,165
python3 verify_boundaries.py --nmin 4 --nmax 9 --workers 2
python3 check_cert.py ../../data/boundaries/null_certificates/*.json.gz
python3 run_boundaries.py --boundary reflect --nmin 4 --nmax 12 --workers 2 --cert-nmax 12 --rules $(python3 -c "import fwlib; print(','.join(map(str, fwlib.class_reps())))")
python3 verify_boundaries.py --boundary reflect --nmin 4 --nmax 8 --workers 2
python3 affine_null.py --nmax 128; python3 check_mirror.py; python3 check_mirror_reflect.py
python3 local_boundaries.py --nmax 62; python3 local_boundaries2.py; python3 compare_boundaries.py > ../../data/boundaries/table_ring_vs_null.md
```
(The second line recomputes nothing already in the checkpoint; certificates at n = 15, 16 for the 45 classes are
written only by the third line if those records are not yet in the checkpoint, so for an exact reproduction run
the third line before the second.)
