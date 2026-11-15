# Rule 94 on rings with 3 | n: every cycle reaches the crystal by single flips

Part 2 of the ring-size verification (new proof, reported separately from the checking of the study).
Folder: `verify_ring_size/part2_94/`. All numbers below are taken from files written in this folder (section 7
is a verbatim copy of `out/tables.md`, which `make_tables.py` builds from the output files).

## 0. Result in brief

| item | status |
|---|---|
| Theorem 1: for every n >= 6 with 3 \| n, the closed classes of the one-flip graph G1 of rule 94 are exactly the three singletons {A_1}, {A_2}, {A_3} (the phases of the crystal (011)^(n/3)); every other cycle has a directed G1 path into A | **proved** (sections 3, 4; no computer-assisted step) |
| Corollary 1: S = A (the noise-selected cycles are the three crystal phases) for every n >= 6 with 3 \| n | **proved**, given Theorem A of the study (S is a union of closed classes of G1) |
| Corollary 2: k_c = 0 for c in {3, 5, 6}, k_c = 1 for c in {0, 1, 2, 4, 7}, hence k* = 1, for every n >= 6 with 3 \| n | **proved**, given Theorem A and the definition of k_c in the note (Section 6) |
| Lemmas 1-6 | **proved**; each also tested exhaustively at small n (Table 1) |
| Closed classes of G1 computed directly, without the proof | **computed for n = 6, 9, ..., 27** (Table 2; n = 24 and n = 27 extend the exhaustive range of the study and of the sealed sample) |
| The chain of flips constructed in the proof, executed step by step | **computed**: every cycle for n = 6, ..., 21; samples up to n = 300 (Table 3) |
| Rings with 3 not dividing n | **not attempted** (remark in section 6) |

The argument does not break anywhere; no sub-statement remains open for the family 3 | n, n >= 6.
No claim of novelty is made.

## 1. Setting and notation

Ring of n cells, indices mod n. Rule 94: f(a,b,c) = bit (4a+2b+c) of 94 = 01011110 in binary, i.e.

    f(000) = 0, f(101) = 0, f(111) = 0, and f = 1 on the codes 001, 010, 011, 100, 110.

Equivalently: a cell in state 1 becomes 0 iff both neighbours are 1; a cell in state 0 becomes 1 iff its two
neighbours differ. (F x)_i = f(x_(i-1), x_i, x_(i+1)). f(a,b,c) = f(c,b,a), so F commutes with the reflection
of the ring as well as with rotations.

Cycles are the periodic orbits of F. G1 has the cycles as nodes and an edge C -> C' (C != C') iff for some state
x of C and some cell j the orbit of x + e_j (x with cell j flipped) ends on C'. A closed class is a strongly
connected component of G1 without leaving edge.

For 3 | n the crystal is the state (011)^(n/3); its three rotations are fixed points (Lemma 2) and are written
A_1, A_2, A_3; A = {A_1, A_2, A_3}.

**Occurrences and the frozen set.** For a state x let Occ(x) be the set of cells i with
(x_(i-1), x_i, x_(i+1)) = (1,0,1) ("an occurrence of 101 centred at i"), and let

    W(x) = union over i in Occ(x) of {i-1, i, i+1}

be the *frozen set* of x. x is *fully frozen* if W(x) is the whole ring. Two elementary facts are used throughout:

* (O1) A cell c with x_c = 0 lies in W(x) iff c is in Occ(x). A cell c with x_c = 1 lies in W(x) iff c-1 or c+1
  is in Occ(x). (In an occurrence the centre is the only 0.)
* (O2) Flipping a cell j can remove from Occ only centres in {j-1, j, j+1}; if j is not in W(x) then no
  occurrence of x contains j and Occ(x + e_j) contains Occ(x).

**Block words.** A *block word* is a state that is a cyclic concatenation of blocks 01 ("short", s) and
011 ("long", l), cut at some cell: every 0 is isolated, every maximal run of 1s has length 1 or 2, and there
is at least one 0. With a short and b long blocks, 2a + 3b = n. The crystal phases are the block words with a = 0.

## 2. Statements

**Theorem 1 [proved].** Let n >= 6 and 3 | n. For rule 94 on the ring of n cells:

1. no single flip leaves a crystal phase: for every cell j, F^3(A_i + e_j) = A_i. Hence each {A_i} is a closed
   class of G1;
2. from every cycle C not in A there is a directed path in G1 from C to a crystal phase.

Consequently the closed classes of G1 are exactly {A_1}, {A_2}, {A_3}.

**Corollary 1 [proved, given Theorem A].** For n >= 6, 3 | n: the set S of noise-selected cycles is A.

**Corollary 2 [proved, given Theorem A].** For n >= 6, 3 | n: k_3 = k_5 = k_6 = 0 and
k_0 = k_1 = k_2 = k_4 = k_7 = 1; in particular k* = 1 (so k* >= 1).

The path of part 2 is explicit (section 4): first flips that enlarge the frozen set until the state is a block
word (Lemma 3), then swaps and merges of blocks (Lemmas 4, 5).

## 3. Lemmas

**Lemma 1 (freezing) [proved].** Let n >= 3. If i is in Occ(x) then i is in Occ(F x). Hence
W(x) is contained in W(F x), and F x agrees with x on W(x). By induction the same holds for F^t x, t >= 0.

*Proof.* Let (x_(i-1), x_i, x_(i+1)) = (1,0,1). Then (F x)_i = f(1,0,1) = 0;
(F x)_(i-1) = f(x_(i-2), 1, 0) = 1 because a 1 becomes 0 only if both neighbours are 1;
(F x)_(i+1) = f(0, 1, x_(i+2)) = 1 for the same reason. So the three cells keep their values. []

**Corollary 1a (frozen set of a cycle) [proved].** W is constant along a cycle: if F^T x = x then
W(x) <= W(F x) <= ... <= W(F^T x) = W(x) (inclusions). Write W(C) for a cycle C.

**Corollary 1b (confinement) [proved].** Let y be a state and I a set of cells such that every cell outside I
lies in W(y). Then for all t >= 0, F^t y agrees with y outside I, and the cells of I evolve under f with the
cells outside I held at their values in y. (Immediate from Lemma 1.)

**Lemma 2 (fully frozen states) [proved].** Let n >= 3. A state is fully frozen iff it is a block word. Every
block word is a fixed point of F.

*Proof.* Let x be fully frozen. By (O1) every 0 of x is a centre, so both its neighbours are 1: the 0s are
isolated. Every 1 of x is adjacent to a centre, i.e. to a 0: there is no run 111, and x is not the all-one
state. Hence x contains a 0, the 0s are isolated and the runs of 1s have length 1 or 2; cutting before every 0
gives blocks 01 and 011. Conversely, in a block word every 0 has two neighbours 1, so it is a centre, and every
1 is adjacent to a 0, so it lies in an occurrence; all cells are frozen. A fully frozen state is fixed by
Lemma 1. []

**Lemma 3 (growth move) [proved].** Let n >= 5 and let x be a state that is not fully frozen. Then there is a
cell j not in W(x) such that, for y = x + e_j and all t >= 2, W(F^t y) contains W(x) properly. More precisely:

* if x is not the all-zero state, j can be chosen so that W(y) contains W(x) and j (so already t >= 0 works);
* if x is the all-zero state, any j works and F^2 y has an occurrence of 101 centred at j.

*Proof.* Since j is not in W(x), Occ(y) contains Occ(x) by (O2), so W(y) contains W(x); by Lemma 1 so does
W(F^t y). It remains to find j with a new frozen cell.

(a) x all-zero. y = e_j. F y is 1 exactly on j-1, j, j+1 (codes 001, 010, 100 there, code 000 elsewhere).
In F y the cells j-2 and j+2 are 0 and differ from j-1, j, j+1 (n >= 5), so (F^2 y)_j = f(1,1,1) = 0,
(F^2 y)_(j-1) = f(0,1,1) = 1, (F^2 y)_(j+1) = f(1,1,0) = 1: an occurrence centred at j, frozen from then on
by Lemma 1.

(b) x not all-zero. Let i be a cell not in W(x). We show there is a cell j not in W(x) such that y = x + e_j
has an occurrence containing j; then W(y) contains W(x) and j.

* x_i = 1 and x_(i-1) = x_(i+1) = 1: take j = i. Then (y_(i-1), y_i, y_(i+1)) = (1,0,1).
* x_i = 1 and x_(i-1) = 0: since i is not frozen, i-1 is not a centre, so x_(i-2) = 0. Take j = i-2. The cell j
  is a 0 whose right neighbour is 0, so it is not a centre and by (O1) not in W(x).
  (y_j, y_(j+1), y_(j+2)) = (1, 0, x_i) = (1,0,1).
* x_i = 1 and x_(i+1) = 0: the mirror image of the previous case, j = i+2.
* x_i = 0: since i is not a centre, not both neighbours are 1.
  * x_(i-1) = 0, x_(i+1) = 1: take j = i-1, a 0 with right neighbour 0, so not in W(x);
    (y_(i-1), y_i, y_(i+1)) = (1,0,1).
  * x_(i-1) = 1, x_(i+1) = 0: mirror image, j = i+1.
  * x_(i-1) = x_(i+1) = 0: as x is not all-zero, let k >= 2 be least with x_(i+k) = 1. Then
    x_(i+k-2) = x_(i+k-1) = 0; take j = i+k-2, a 0 with right neighbour 0, so not in W(x);
    (y_j, y_(j+1), y_(j+2)) = (1,0,1).

In every case the three cells involved are distinct because n >= 3. []

**Corollary 3 (edge of G1) [proved].** Let n >= 5 and let C be a cycle whose states are not fully frozen. Then
there is an edge C -> C' of G1 with W(C') containing W(C) properly.

*Proof.* Take x in C, j and y as in Lemma 3, and let C' be the cycle on which the orbit of y ends. C' contains
F^t y for all large t, so W(C') contains W(x) = W(C) properly (Corollary 1a). In particular C' != C. []

**Lemma 4 (swap) [proved].** Let x be a block word with at least three blocks, and let cells p, ..., p+4 carry
two consecutive blocks short, long: (x_p, ..., x_(p+4)) = (0,1,0,1,1). Let x' be x with these five cells
replaced by (0,1,1,0,1) (long, short). Then x' is a block word and G1 contains a path {x} -> C2 -> {x'},
where C2 = {y, F y}, y = x + e_(p+2), is a cycle of period 2.

*Proof.* x has at least three blocks, so n >= 7, the block following the long one is a third block, and its
first two cells p+5, p+6 are different from p, ..., p+4: x_(p+5) = 0, x_(p+6) = 1. The cell p-1 is the last
cell of the block preceding the short one and is different from p, ..., p+4: x_(p-1) = 1.
The only occurrence of x containing the cell p+2 (a 0) is the one centred at p+2, with cells p+1, p+2, p+3.
In y = x + e_(p+2): the cell p+1 still lies in the occurrence centred at p (cells p-1, p, p+1); the cell p+4
lies in the occurrence centred at p+5 (cells p+4, p+5, p+6); neither occurrence contains p+2. Every cell
outside {p+1, ..., p+4} lies in an occurrence of x other than the one centred at p+2, hence not containing p+2. So every cell outside I = {p+2, p+3} is in W(y), and
y_(p+1) = y_(p+4) = 1. By Corollary 1b the pair (u,v) on I evolves by u' = f(1,u,v), v' = f(u,v,1):
(1,1) -> (0,0) -> (1,1). Hence y has period 2, C2 = {y, F y} is a cycle, and x is not in C2
(x has (0,1) on I). So {x} -> C2 is an edge of G1.
The state F y has (0,1,0,0,1) on p, ..., p+4. Flipping its cell p+2 gives (0,1,1,0,1) there, i.e. the state x',
which is a block word (blocks long, short on these cells, all other blocks unchanged), hence a fixed point by
Lemma 2, and not in C2. So C2 -> {x'} is an edge of G1. []

**Lemma 5 (merge) [proved].** Let n >= 6, let x be a block word and let cells p, ..., p+5 carry three
consecutive short blocks: (x_p, ..., x_(p+5)) = (0,1,0,1,0,1). Let x'' be x with these six cells replaced by
(0,1,1,0,1,1) (two long blocks). Then x'' is a block word, F(x + e_(p+3)) = x'', and {x} -> {x''} is an edge
of G1.

*Proof.* x_(p-1) = 1 (last cell of the preceding block) and x_(p+6) = 0, x_(p+7) = 1 (first two cells of the
following block; for n = 6 these are the cells p, p+1). The cell p+3 is a 1; the occurrences of x containing
it are those centred at p+2 and p+4, with cells in {p+1, ..., p+5}. In y = x + e_(p+3): the cell p+1 lies in
the occurrence centred at p, whose cells p-1, p, p+1 do not include p+3 (n >= 6); the cell p+5 lies in the
occurrence centred at p+6, whose cells p+5, p+6, p+7 do not include p+3 (n >= 6); every cell outside
{p+1, ..., p+5} lies in an occurrence of x not containing p+3. So every cell outside I = {p+2, p+3, p+4} is in
W(y), with y_(p+1) = y_(p+5) = 1, and y = (0,0,0) on I. By Corollary 1b, F y on I is
(f(1,0,0), f(0,0,0), f(0,0,1)) = (1,0,1) and F y = y elsewhere, i.e. F y = x''. x'' is a block word, hence
fixed, and x'' != x. []

**Lemma 6 (the crystal cannot be left by one flip) [proved].** Let n >= 6, 3 | n, x a crystal phase. For every
cell j, F^3(x + e_j) = x.

*Proof.* x is a block word of long blocks 0 1 1.

(a) j carries a 0. Then (x_(j-2), ..., x_(j+2)) = (1,1,0,1,1) and x_(j-3) = x_(j+3) = 0. The only occurrence
containing j is centred at j; its other cells j-1, j+1 lie in no other occurrence (their other neighbours are
1s). The cells j-2 and j+2 lie in the occurrences centred at j-3 and j+3, which do not contain j (for n = 6
these two occurrences coincide). So in y = x + e_j every cell outside I = {j-1, j, j+1} is frozen, with
y_(j-2) = y_(j+2) = 1, and y = (1,1,1) on I. By Corollary 1b: (1,1,1) -> (0,0,0) -> (1,0,1) on I, which is x.

(b) j carries the first 1 of a block, the block being on cells p, p+1, p+2 and j = p+1. Then
(x_(p-2), ..., x_(p+3)) = (1,1,0,1,1,0). The only occurrence containing p+1 is centred at p (cells p-1, p,
p+1); the cell p-1 lies in no other occurrence (x_(p-2) = 1). The cell p-2 lies in the occurrence centred at
p-3, the cell p+2 in the occurrence centred at p+3; neither contains p+1. So in y = x + e_(p+1) every cell
outside I = {p-1, p, p+1} is frozen, with y_(p-2) = y_(p+2) = 1, and y = (1,0,0) on I. By Corollary 1b:
(1,0,0) -> (f(1,1,0), f(1,0,0), f(0,0,1)) = (1,1,1) -> (0,0,0) -> (1,0,1) on I, which is x.

(c) j carries the second 1 of a block: the reflection of the ring maps x to a crystal phase and j to the first
1 of a block; apply (b) and the reflection symmetry of F. []

## 4. Proof of Theorem 1

*Part 1.* Lemma 6: for a fixed point x the states reached with one flip are x + e_j and their forward orbits,
which return to x. So no edge of G1 leaves {A_i}, and {A_i} is a strongly connected component without leaving
edge.

*Part 2.* Let C be a cycle not in A.

Stage 1. As long as the current cycle is not fully frozen, Corollary 3 gives an edge of G1 to a cycle with a
strictly larger frozen set. The frozen set has at most n cells, so after at most n edges a fully frozen cycle
is reached; by Lemma 2 it is a fixed point {x}, x a block word.

Stage 2. Let x be a block word with a short and b long blocks; 2a + 3b = n and 3 | n give 3 | a. If a = 0, x is
a crystal phase and we are done. Otherwise a >= 3. Cut the cyclic sequence of blocks at a block boundary to
obtain a linear word w over {s, l} of length a + b >= 3.
While w contains an adjacent pair "s l", apply Lemma 4 to these two blocks (they are consecutive on the ring
and x has at least three blocks): two edges of G1 lead to the block word whose word, cut at the same cell, is
w with this pair replaced by "l s". Each swap lowers the number of inversions of w (pairs of positions k < k'
with w_k = s, w_k' = l) by one, so after at most ab swaps w = l^b s^a. This word contains three consecutive s
(a >= 3); Lemma 5 gives one edge of G1 to a block word with a - 3 short and b + 2 long blocks. Induction on a
ends at a = 0, a crystal phase.

All steps are edges of G1 between distinct cycles, so the concatenation is a directed path from C into A.

*Consequence.* Let K be a closed class. If K contains a cycle C not in A, the path from C into A stays in K
(no edge leaves K), so some A_i is in K; K is strongly connected and A_i has no outgoing edge, so K = {A_i},
contradicting C in K. Hence every closed class is one of the {A_i}, and these are closed classes by part 1. []

## 5. Corollaries

*Corollary 1.* By Theorem A of the study (re-derived independently by the lead of this verification; used
here as given), S is a union of closed classes of G1, so S is a non-empty subset of A. The resistances are
invariant under rotation of the ring, hence so are V, gamma and S; A is one rotation orbit; so S = A. []

*Corollary 2.* Definition (note v0.2, Section 6): k_c = min over cycles C of [gamma(C) + R(C -> D_c)] - min gamma,
D_c the set of states containing code c, and k* = max_c k_c; R(C -> x) = 0 iff x is in C. Hence k_c = 0 iff a
state of a cycle of S contains code c. The crystal contains exactly the codes 011, 101, 110 (3, 5, 6), so by
Corollary 1 k_c = 0 for c in {3,5,6} and k_c >= 1 otherwise. For the upper bound take C = A_i, x its state and
the flip of Lemma 6 (b): y = x + e_(p+1) costs resistance 1, and y, F y, F^2 y are reached from it at no further
cost. On cells p-2, ..., p+3, y = (1,1,0,0,1,0): code 100 at p, code 001 at p+1, code 010 at p+2 (the cell
p+2 is a 1 between y_(p+1) = 0 and x_(p+3) = 0). F y = (1,1,1,1,1,0) there: code 111 at p. F^2 y = (1,0,0,0,1,0):
code 000 at p. So R(A_i -> D_c) <= 1 for c in {0,1,2,4,7} and k_c <= gamma(A_i) + 1 - min gamma = 1. []

(The values k = (1,1,1,0,1,0,0,1) and k* = 1 agree with the sealed sample for n = 9, 12, 15, 18, 21, see
`verify_ring_size/SAMPLE.md`, section 7, rule 94.)

## 6. Remarks, scope, and what is not shown

* **Where 3 | n enters.** Lemmas 1-5 and Corollary 3 hold for every n in the stated ranges, whether or not 3
  divides n: on every ring with n >= 5 every cycle has a G1 path to a block word. Divisibility is used only in
  stage 2 (3 | a, so that merges can remove all short blocks) and in Lemma 6. For 3 not dividing n the residue
  of a mod 3 is fixed by n and no block word is free of short blocks.
* **Not attempted:** the converse statement for 3 not dividing n (k* = 0, computed in the study and in the
  sealed sample for n <= 22). It does not follow from the lemmas above without an additional argument about
  which cycles lie in the closed class; nothing is claimed here.
* **n = 3** is excluded (the crystal 011 is a fixed point, but the ring is too short for the lemmas as stated);
  not examined.
* **No computer-assisted step.** The proof uses only the rule table. The computations of section 7 are tests
  of the lemmas and an independent direct computation of the closed classes; the theorem does not rely on
  them.
* **Structure seen in the experiments (not needed for the proof, not proved):** besides fixed points and
  2-cycles, rule 94 has cycles of other periods (3, 4, 6, 14 for n <= 18; also 8, 12, 62 for n <= 27;
  `out/g1_classes.jsonl`, field `period_hist`), among them cycles without any occurrence of 101 on which the rule acts like an additive rule
  on doubled words, with periods growing irregularly with n (Table 3, part C). A classification of all cycles
  is therefore not available in closed form; the proof avoids it because Lemma 3 applies to every state.
* **Relation to the study.** The study states the radius of the crystal as proved and the reachability as
  computed/sampled (`report_ring_size.md`, section 5, mechanism table and 5.1; only these lines of the report
  were read). Lemma 6 re-proves the radius
  statement by a different argument (frozen walls instead of a light cone, valid from n = 6 without a separate
  computation); part 2 of Theorem 1 supplies the reachability statement for all n.
* **Code.** The compiled solver of the sealed sample could not be loaded in the execution environment used for
  this part (loading a shared library from the repository folder was refused), so the computations here use
  separate NumPy code written from the definitions (`ring94.py`, `g1_classes.py`). Its results agree with the
  sealed sample wherever both exist (n = 8..22, Table 2, last paragraph). Nothing from `code/ring_size/` or
  `code/fw/` was imported or read.

## 7. Computations (verbatim copy of `out/tables.md`)

### Table 1. Exhaustive tests of the lemmas (`check_lemmas.py` -> `out/check_lemmas.json`)

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| L1 | Lemma 1 (freezing), every state | 3..20 | 2097144 states | 0 |
| L2 | Lemma 2 (fully frozen = block word, fixed), every state | 3..20 | 1123 fully frozen states among 2097144 | 0 |
| L3a | Lemma 3 (growth move), every state that is not fully frozen | 5..16 | 130685 states | 0 |
| L3b | Corollary 3 (edge of G1 to a cycle with larger frozen set), every periodic state that is not fully frozen; frozen set constant on every cycle | 5..20 | 32176 periodic states (12600 cycles) | 0 |
| L4 | Lemma 4 (swap), every block word, every occurrence | 5..30 | 51068 occurrences | 0 |
| L5 | Lemma 5 (merge), every block word, every occurrence | 6..30 | 38549 occurrences | 0 |
| L6 | Lemma 6 (every flip of the crystal heals; healing time [3]) | 6..99 (step 3) | 1680 flips | 0 |
| C2 | Corollary 2 (one flip of the crystal meets codes 0, 1, 2, 4, 7) | 6..99 (step 3) | 32 ring sizes | 0 |

All tests passed: True. CPU time 3.39 s, peak memory 122 MB.

### Table 2. G1 and its closed classes computed directly, 3 | n (`g1_classes.py` -> `out/g1_classes.jsonl`)

| n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | closed classes = the three crystal phases | cycles with no G1 path to the crystal | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 9 | 12 | 15 | 9 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 9 | 31 | 58 | 189 | 5 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 12 | 147 | 348 | 1628 | 14 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 15 | 509 | 1189 | 6705 | 5 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 18 | 1881 | 4998 | 32820 | 44 | 3 [1, 1, 1] | True | 0 | 0.02 | 62 |
| 21 | 6927 | 18988 | 132573 | 5 | 3 [1, 1, 1] | True | 0 | 0.10 | 121 |
| 24 | 26475 | 80116 | 601304 | 74 | 3 [1, 1, 1] | True | 0 | 0.61 | 428 |
| 27 | 101407 | 323383 | 2598588 | 5 | 3 [1, 1, 1] | True | 0 | 3.91 | 2946 |

For comparison, 3 not dividing n (same script): n = 5: 11 cycles, closed classes [11]; n = 7: 22 cycles, closed classes [22]; n = 8: 27 cycles, closed classes [27]; n = 10: 73 cycles, closed classes [67]; n = 11: 78 cycles, closed classes [77]; n = 13: 209 cycles, closed classes [208]; n = 14: 320 cycles, closed classes [317]; n = 16: 747 cycles, closed classes [746]; n = 17: 1191 cycles, closed classes [1190]; n = 19: 2832 cycles, closed classes [2831]; n = 20: 4513 cycles, closed classes [4477]; n = 22: 10827 cycles, closed classes [10793]; n = 23: 16952 cycles, closed classes [16951].

Cross-check with the sealed blind sample (`crosscheck_sample.py` -> `out/crosscheck_sample.json`): numbers of cycles, periodic states, G1 edges and the closed-class sizes compared for n = 8..22 (15 ring sizes); all agree: True.

### Table 3. The chain of the proof, executed and checked step by step (`constructive_paths.py` -> `out/constructive_paths.json`)

| part | n | start cycles | all chains end on a crystal phase | longest chain (flips) | mean | max growth steps | max swap flips | max merges |
|---|---|---|---|---|---|---|---|---|
| A: every cycle | 6 | 9 | True | 1 | 0.67 | 1 | 0 | 1 |
| A: every cycle | 9 | 31 | True | 3 | 1.84 | 2 | 0 | 1 |
| A: every cycle | 12 | 147 | True | 10 | 4.39 | 3 | 6 | 2 |
| A: every cycle | 15 | 509 | True | 14 | 6.58 | 4 | 10 | 2 |
| A: every cycle | 18 | 1881 | True | 19 | 8.53 | 4 | 14 | 3 |
| A: every cycle | 21 | 6927 | True | 25 | 10.80 | 6 | 18 | 3 |
| B: cycles reached from 200 random states | 24 | 200 | True | 26 | 10.54 | 5 | 22 | 4 |
| B: cycles reached from 200 random states | 27 | 200 | True | 31 | 12.21 | 4 | 26 | 4 |
| B: cycles reached from 200 random states | 30 | 200 | True | 35 | 13.49 | 5 | 30 | 4 |
| B: cycles reached from 200 random states | 45 | 200 | True | 57 | 24.20 | 8 | 50 | 6 |
| B: cycles reached from 200 random states | 60 | 200 | True | 67 | 34.58 | 7 | 62 | 7 |
| B: cycles reached from 200 random states | 99 | 200 | True | 108 | 62.27 | 12 | 98 | 12 |
| B: cycles reached from 200 random states | 150 | 200 | True | 153 | 97.05 | 14 | 136 | 19 |
| B: cycles reached from 200 random states | 300 | 200 | True | 283 | 201.20 | 23 | 244 | 32 |
| C: all-zero state and doubled words | 6 | 17 | True | 1 | 1.00 | 1 | 0 | 0 |
| C: all-zero state and doubled words | 18 | 21 | True | 18 | 4.86 | 3 | 14 | 2 |
| C: all-zero state and doubled words | 30 | 21 | True | 26 | 12.81 | 3 | 20 | 4 |
| C: all-zero state and doubled words | 42 | 21 | True | 50 | 24.76 | 2 | 44 | 6 |
| C: all-zero state and doubled words | 54 | 21 | True | 59 | 30.81 | 3 | 50 | 8 |
| C: all-zero state and doubled words | 66 | 21 | True | 75 | 36.48 | 2 | 66 | 10 |
| C: all-zero state and doubled words | 90 | 21 | True | 76 | 47.52 | 3 | 62 | 14 |
| C: all-zero state and doubled words | 150 | 21 | True | 155 | 98.52 | 3 | 136 | 24 |
| C: all-zero state and doubled words | 300 | 1 | True | 51 | 51.00 | 1 | 0 | 50 |

Part A total: 9504 cycles, of which 18 are the crystal phases themselves (chain of length 0). 
Part C start periods (period: count; None = longer than the search bound): n = 6: 1: 1, 2: 16; n = 18: 1: 1, 14: 20; n = 30: 1: 1, 30: 20; n = 42: 1: 1, 126: 20; n = 54: 1: 1, 1022: 20; n = 66: 1: 1, 62: 20; n = 90: 1: 1, 8190: 20; n = 150: 1: 1, None: 20; n = 300: 1: 1.
CPU time 15.38 s, peak memory 185 MB.

Total CPU time of the three scripts as recorded in their output files: 24.0 s.

Notes on the tables.

* Table 2 is independent of the proof: all 2^n states are tabulated, the periodic states and the cycle every
  state falls to are determined (method in the header of `g1_classes.py`), all single flips of all periodic
  states are followed, strongly connected components are computed, and the cycles with a G1 path to a crystal
  phase are found by a reverse search. n = 24 and n = 27 are beyond the exhaustive range of the study (n <= 22;
  it reports sampled reachability for larger n) and of the sealed sample (n <= 21 for 3 | n). Cost was declared and recorded in
  `verify_ring_size/logs/BATCHES_phase2.md`.
* Table 3: in every chain each flip is applied to a state of the current cycle, the flipped state is iterated
  until periodic, and the script asserts that the cycle reached differs from the current one, that it is the
  one predicted by Lemmas 3-5, and that the chain ends on a crystal phase. Part C, n = 150: the periods of the
  doubled start states exceed the search bound of the script; that these states are periodic follows from the
  remark in the script (for m = n/2 odd the map u -> u + shift(u) is injective on words of even weight) and
  was checked directly only for n <= 90.
* The tests of Table 1 include ring sizes not divisible by 3 and, for Lemma 4, n = 5 (two blocks), which the
  statement of Lemma 4 does not need.

## 8. Files (all under `verify_ring_size/part2_94/`)

| file | content |
|---|---|
| `PROOF_94.md` | this document |
| `ring94.py` | small-n tools: table of F, cycles, attractor labels, G1, closed classes (NumPy, own code) |
| `check_lemmas.py` | exhaustive tests of Lemmas 1-6 and of the code coverage in Corollary 2 |
| `out/check_lemmas.json`, `out/check_lemmas_stdout.txt` | its output |
| `g1_classes.py` | direct computation of G1 and its closed classes for one ring size, memory-lean |
| `out/g1_classes.jsonl` | one record per n = 5..24 and 27 (closed-class members are listed when a class has at most 6 cycles) |
| `out/g1_classes_stdout_n05_22.txt`, `out/g1_classes_stdout_n23.txt`, `out/g1_classes_stdout_n24_27.txt` | run logs (the last two with the process times reported by `/usr/bin/time`) |
| `crosscheck_sample.py`, `out/crosscheck_sample.json`, `out/crosscheck_sample_stdout.txt` | comparison with `verify_ring_size/out/sample.jsonl` |
| `constructive_paths.py` | executes the chain of the proof and checks every step by simulation |
| `out/constructive_paths.json`, `out/constructive_paths_stdout.txt` | its output |
| `make_tables.py`, `out/tables.md` | tables of section 7 |

To reproduce (repository root, Python with NumPy and SciPy; about half a minute of CPU time, peak memory about
3 GB for n = 27; `g1_classes.py` skips ring sizes already present in `out/g1_classes.jsonl`):

    python verify_ring_size/part2_94/check_lemmas.py
    python verify_ring_size/part2_94/g1_classes.py 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 27
    python verify_ring_size/part2_94/crosscheck_sample.py
    python verify_ring_size/part2_94/constructive_paths.py
    python verify_ring_size/part2_94/make_tables.py
