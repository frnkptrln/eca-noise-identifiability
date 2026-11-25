# Open boundaries: noise-selected cycles of ECA on a row with null boundaries

Status (updated as the work proceeds; the last line of this block is the current state):

- 24 Nov 2026, start. Base: commit 2765f7e (= origin/main, version 0.4). The worktree
  `~/git/eca-open-boundaries` could not be created from the sandbox (`git fetch` and `git worktree add` fail with
  "Operation not permitted" on `.git`), and no git identity is visible inside the sandbox, so nothing is committed.
  The work is done in a copy of 2765f7e (`git archive 2765f7e`) in the session workspace; every finished file is
  saved as an artifact, and Section 9 lists the commands that recreate the step commits in the worktree.
- Step 0 (literature): running.
- Step 1 (definitions, symmetries, code, guarding test): running.
- Steps 2-5: not started.

## Contents
1. Literature (Step 0)
2. Definitions and symmetries (Step 1)
3. Predictions (Step 2, sealed)
4. Computation (Step 3)
5. Ring vs null comparison and mechanisms (Step 4)
6. Reflecting boundaries (Step 5)
7. Predictions scored
8. Open points; plain-words summary for a later README
9. How to recreate the commits

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
