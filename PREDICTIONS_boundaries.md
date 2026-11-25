# Predictions: noise-selected cycles of ECA on a row with null boundaries

Written 24 November 2026 before any stochastic potential, cycle structure or k* was computed under walls.
Computed before this file was written: only the ring tests of Step 1 (ring results for n = 4..12 recomputed
and compared with `data/fw_sweep.csv`) and deterministic symmetry checks of the successor maps (reflection
conjugation, complement null <-> fixed-1, unit tests of the edge codes). The hand derivations below
(marked "by hand") were made on paper from the rule tables; no program enumerated a state space under walls.
This file is not edited after it is sealed (sha256 recorded in `report_boundaries.md`); outcomes go into the
report.

## Setting

Row of n cells 0..n-1; cells -1 and n are 0 at every step (null walls); noise flips cells 0..n-1 only. The
edge cells read codes that include the wall value (left edge: codes 0..3; right edge: even codes) and the
observer reads the rule on every visited code, edge codes included. k_c, k*, noise-selected cycles as in the
note. A rule R under fixed-1 walls is the complement conjugate R* = complement_rule(R) under null walls
(Step 1), so "R under 1-walls" below means "R* under null walls". Under null walls the symmetry left is
reflection only; the unit is the 160 reflection classes (Section 2 of the report). Each ring class
{R, refl R, R*, refl R*} becomes the null class of R and the null class of R*; the two coincide only for 16 of
the 88 ring classes (among the named ones: 43, 142, 150).

Confidence: H (high: follows from an argument I consider complete), M (medium), L (low: a guess).
"k* >= 1 pattern" statements refer to n = 4..16 unless stated; small n (4..7) are marked separately where
I expect edge effects to dominate.

## General expectations

G1 (M). The ring conditions p | n and n = 2^k do not survive as such. Where a ring mechanism survives,
the walls act as cells of the pattern, so the arithmetic moves to n + 1 (the row is half of a ring of
2n + 2 cells for reflection-symmetric rules with f(000) = f(101) = 0; and the null row of rule 90 is
nilpotent iff n + 1 is a power of two).

G2 (M). Travelling crystals and travelling defect families (classes 43, 142, 35; also the travelling
(100)-crystal behind class 26 off 2^k) cannot exist between fixed walls, so the mechanisms built on them
disappear; I expect the corresponding null classes not to show the ring's divisibility pattern.

G3 (H, proved by the argument that will be written out in the report as Proposition L). For an affine rule
under null walls (F x = M x + b over GF(2)), every cycle reaches every other cycle by one-flip steps in both
directions: write the state space as V_nil + V_inv (Fitting decomposition of M); the cycle reached after a
flip e_i from a periodic state x is the cycle of x + b_i, b_i the V_inv-component of e_i; flipping the same
cell again at x + b_i returns to the cycle of x; the b_i span V_inv. So G1 has one closed class, all cycles
are noise-selected (ring paper, Theorem A, which does not use the ring), and k* = 0 iff the periodic states
jointly contain all eight codes. If M is nilpotent the only cycle is one fixed point.

G4 (H for the bijective statement, M for the values). Bijective rules have k* = 0 under any boundary: the
argument of the note (P(x, y) = q(F(x) XOR y) with F a bijection is doubly stochastic, the uniform law is
stationary, every state has order 0, and for n >= 3 every code occurs at an interior cell) uses no ring.
Rules that are bijective on every ring but not under walls change: the shifts 170 and 240 become nilpotent
(after n steps everything has left through a wall), the only cycle is 0, and k* = 3 at every n (code 111
needs three flips placed on a moving block; codes 011, 110, 101 need two) (M for the value 3, H for
k* >= 1). Rules 15 and 85 (complemented shifts) become affine with nilpotent M and a unique fixed point
(1010... from the wall), k* = 1 at every n (M).

G5 (L). Overall, more rules have k* >= 1 under null walls than on the ring at the same n (n = 12..14),
because walls destroy travelling cycles and pin structures at the edges.

G6 (M). Of the ring classes with k* >= 1 at every n >= 8 on the ring, at least 90 % of the corresponding
256 rules keep k* >= 1 under null walls at n = 12..14.

G7 (L). Between 15 and 40 of the 160 null classes change k* between 0 and >= 1 somewhere in n = 8..14.

## Frank's expectations (from his chat with Claude; scored like mine)

(a) Reflection-symmetric rules with f(000) = f(101) = 0 (among them 22, 90, 94, 150): the null row of n
cells is exactly the mirror-symmetric subspace of the ring of 2n + 2 cells with two zero cells. Rule 94 has
a fixed point using exactly the codes {3, 5, 6} iff 3 | (n + 1); rule 90 is nilpotent iff n + 1 is a power
of two. Expectation: k* >= 1 iff 3 | (n + 1) for 94, and iff n + 1 is a power of two for 90. (One flip in the
row is two flips in the ring, so the potentials are not inherited.)

(b) 43 and 142: no travelling crystal survives fixed walls, so the 4 | n pattern disappears.

(c) Under null walls rule 60 is bijective for every n, and rule 150 exactly when n is not 2 mod 3. If the
bijective argument carries over, k* = 0 there. What 150 does at n = 2 mod 3 is open.

My view of (a)-(c): I share (a) for 90 (H for even n: bijective; H for n = 2^k - 1; M elsewhere, see below)
and for 94 (M). I share (b) (M). (c): the bijective argument does carry over (G4, H); for 150 at n = 2 mod 3
see below.

## Per class

Notation: "R [S]" = rule R and its null-boundary class S. For each ring class I give the null class of R
and the null class of R* (= R under 1-walls).

### Additive classes

60 [60, 102] (H): bijective for every n (M lower bidiagonal with unit diagonal) -> k* = 0 for every n. The
ring's power-of-two mechanism (nilpotency of 1 + t at n = 2^k) disappears.
153 [153, 195] = 60 under 1-walls (H): affine with the same M, bijective, k* = 0 for every n.

90 [90] (H at even n and at n = 2^k - 1; M at the other odd n): M = adjacency matrix of the path P_n. Even
n: det = 1 over GF(2) (one perfect matching), bijective, k* = 0. Odd n: kernel {0, 1010...1}. M is
nilpotent iff n + 1 is a power of two (characteristic polynomial x^n; by hand from p_{2m+1} = x p_m^2,
p_{2m} = (p_m + p_{m-1})^2 over GF(2)); then 0 is the only cycle and, since a rule-90 orbit started by one
flip keeps its ones on one parity class (never two adjacent ones), the codes 011, 110 and 111 need two flips:
**k* = 2 at n = 7 and n = 15**. At the other odd n (5, 9, 11, 13) G3 applies and I expect the periodic states
to cover all codes: k* = 0 (M; least sure at n = 5, where the periodic subspace has dimension 4).
Summary: k* >= 1 iff n + 1 is a power of two (agrees with (a)).

165 [165] = 90 under 1-walls (H at even n, M otherwise): affine with the same M. Even n bijective, k* = 0.
n = 2^k - 1: one fixed point, which can carry at most n codes; at n = 7 it misses at least one (H), at n = 15
I expect it to miss one as well (M). Other odd n: k* = 0 (M). Summary: k* >= 1 iff n + 1 is a power of two.

150 [150] (= its own complement class; H for n != 2 mod 3; H by hand at n = 5 and 11; M at 8, 14): bijective
iff n is not 2 mod 3, k* = 0 there. At n = 2 mod 3, G3. By hand: the characteristic polynomial of M = I + A
is (x + 1)^a x^(n - a) with a = 1 at n = 5 and a = 3 at n = 11, so the periodic subspace is tiny there.
n = 5: periodic states {00000, 10101}, codes {0, 2, 5} only -> **k* = 1 at n = 5** (each missing code is one
flip from 10101 or 00000). n = 11: periodic subspace spanned by 10101010101, 01000100010 and 00101000001; its
eight states cover all codes -> k* = 0. n = 8 and n = 14: periodic subspace of dimension 6 and 12, I expect
all codes -> k* = 0 (M). Summary: **k* >= 1 only at n = 5** in n = 4..16; no divisibility pattern.

### Zero-state classes

154 [154, 210] (H for the radius statement; M for selection and the values): rule 154 agrees with rule 90
on codes 0, 1, 2, 4, 5, and the edge cells see only codes with no adjacent ones along a rule-90 orbit started
by one flip; so under null walls the orbit of every e_i is the rule-90 null orbit, and r(0) >= 2 iff every
e_i dies iff M_90 is nilpotent iff n + 1 is a power of two. No parity condition is needed (on the ring odd n
was settled by bijectivity). Expected: 0 selected alone at n = 7, 15 (reachability of 0 by one-flip chains
as on the ring), **k* >= 1 iff n + 1 is a power of two**, with k* = 1 at n = 7 and 15 (codes needing two
adjacent ones are carried by cycles of potential gamma_min + 1, as on the ring at 2^k); k* = 0 at every
other n (M). Rule 154 is not bijective at n = 7, 15 (one flip of 0 dies).
166 [166, 180] = 154 under 1-walls (L): no zero-state mechanism (the fixed uniform state is 1...1, whose
single flips grow). Expected k* = 0 for n >= 8, no 2^k or 2^k - 1 pattern.

26 [26, 82] (H for the radius statement as for 154: 26 differs from 90 only on code 6; M/L otherwise):
r(0) >= 2 iff n + 1 is a power of two. Expected **k* >= 1 at n = 7, 15** (zero state selected alone; M).
At other n the ring reason for k* >= 1 (code 111 carried only by defects in the travelling (100)-crystal)
should change because the crystal cannot travel between walls (G2); I expect k* to be 0 at most other n but
make no pattern prediction (L).
167 [167, 181] = 26 under 1-walls (L): k* = 0 for n >= 8, no pattern.

22 [22] (reflection-symmetric, f(000) = f(101) = 0: the mirror embedding of (a) applies; L/M):
zero-state mechanism with r(0) >= 2 iff the orbit of every single flip returns to 0. In the ring of
2n + 2 cells a single flip of the row is a symmetric pair of seeds, so the ring seed set {2^k - 2, 2^k - 1,
2^k, ...} is not inherited. Expected (L): k* >= 1 at n = 7 and 15 (where rule 90 null is nilpotent and the
rule-22 orbit follows rule 90 on isolated ones), possibly also at n = 6 and 14; k* = 0 at n = 9..13.
151 [151] = 22 under 1-walls (L): k* = 0 for n >= 8, no pattern.

122 [122] (L): f(101) = 1, so the mirror embedding does not apply. The checkerboard 2-cycle 1010... <->
0101... exists under null walls for every n (by hand), carrying codes {1, 2, 4, 5}; the ring's parity
obstruction (no carrier of code 2 at odd n) disappears. Expected: the ring pattern (k* = 0 iff 4 | n, zero
state at 2^k - 1) disappears; k* = 0 at most n >= 8 (L).
161 [161] = 122 under 1-walls (L): no pattern; k* = 0 at most n >= 8.

### Crystal classes

94 [94] (M): mirror embedding (a). The ring crystal (011) closes in the row with the walls as its zeros:
the fixed point 11011011...011 exists iff n = 2 mod 3, i.e. 3 | (n + 1), and uses the codes {3, 5, 6} only
(edge cells included: they read 011 and 110). Single flips of it heal locally (checked by hand at n = 5 for
every cell), so its radius should be 2 and, with one-flip reachability as on the ring, it is selected alone
(Lemma B with q = 1). Expected: **k* = 1 iff 3 | (n + 1)** for n >= 5; at 3 does not divide n + 1, k* = 0
(n = 4 may be an exception, as on the ring).
133 [133] = 94 under 1-walls (L): with walls equal to 1 the walls act as ones of the crystal, and the
(011)-crystal fits at every n (one placement, or two mirror placements when 3 | (n + 1)), again with codes
{3, 5, 6} only. If it keeps radius 2, k* >= 1 at every n. Against it: by hand at n = 4 a flip of the cell next
to a wall leads to a different 2-cycle (radius 1). Expected (L): k* >= 1 at every n >= 8; the divisibility
pattern disappears either way.

43 [43, 113] and 142 [142, 212] (M for "no 4 | n pattern", L for values): agree with (b). The ring cycle is
the travelling (0011)-crystal; walls stop it. For 142, by hand, a single flip of 0 becomes a travelling 11
block that stops at the left wall as the fixed point 100...0, so structures pinned at the walls take over.
Expected: k* does not depend on n mod 4 for n >= 8; k* >= 1 at every n >= 8 for 142 (wall-pinned fixed
points with few codes; L) and k* constant in n for 43 (value not predicted).

35 [35, 49] (M for "no 3 | n pattern", L for values): the ring mechanism is a travelling family of words over
the blocks 10 and 100; under walls it cannot travel (G2). Expected: the 3 | n pattern disappears; k* constant
in n for n >= 8 (value not predicted).
59 [59, 115] = 35 under 1-walls (L): same expectation.

### Other switching classes (no mechanism-based prediction)

37 [37] (L): ring codes 010 and 101 missing except n mod 6 in {0, 5} (period-6 defect family). f(000) = 1, no
mirror embedding. Expected: the mod-6 pattern disappears; k* >= 1 at most n >= 8.
91 [91] = 37 under 1-walls (L): k* >= 1 at most n >= 8.

45 [45, 101] (L): on the ring bijective at odd n; under walls I expect bijectivity to fail at most n (a
right-to-left preimage construction leaves one free bit and one constraint at the left wall). Expected:
k* = 0 at every n >= 8 except isolated n.
75 [75, 89] = 45 under 1-walls (L): k* = 0 at every n >= 8 except isolated n.

73 [73] (L): ring switch only at n = 9. Expected: k* = 0 at n >= 8 except isolated n.
109 [109] = 73 under 1-walls (L): same.

## What would count as confirming or refuting

Each per-class "Expected" line is scored on n = 4..14 (and 15, 16 where computed) as correct, partly correct
(right pattern with exceptions, or right side at most n) or wrong. Statements marked H that fail would mean an
error in an argument and will be traced. G5-G7 are scored on the counts in the sweep.
