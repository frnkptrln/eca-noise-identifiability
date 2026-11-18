# Rule 94 on rings with 3 not dividing n: one closed class, which contains every cycle with a 101 and all eight codes

Folder: `proofs_94_26/`. Starting point: `verify_ring_size/part2_94/PROOF_94.md` (cited as P94; its Lemmas 1 to 5 and
Corollaries 1a, 1b, 3 hold for every n in the ranges stated there, whether or not 3 divides n). All numbers below are taken
from files written by the scripts of this folder (section 7 is a verbatim copy of `out/tables_94.md`, which `make_tables.py`
builds from the output files). Tags: [proved] = the argument covers every n in the stated range and uses no computation;
[proved, given Theorem A] = in addition Theorem A of `report_ring_size.md` (Section 4) and the definition of k_c are used as
given; [computed for n = ...] = seen in enumeration only; [attempted (gap: ...)] = not proved, the gap is named.

## 0. Result in brief

| item | statement | status | where |
|---|---|---|---|
| Theorem 1 | description of all periodic states of rule 94 for every n >= 3: 0; doubled words with a periodic half word (even n); states with a non-empty frozen set all of whose windows are "live" (width = 2 mod 3 with one of two contents, or width 4 with one of three contents) | **[proved]** | Lemmas 7, 8, 9; section 4 |
| Theorem 2(a) | for every n >= 5 with 3 not dividing n, G1 has exactly one closed class K | **[proved]** | section 4 |
| Theorem 2(b), (c) | K contains every cycle that has an occurrence of 101; K is the set of cycles reachable from the block words; a cycle outside K has no 101, i.e. it is {0} or a cycle of doubled words (even n only) | **[proved]** | section 4 |
| Theorem 2(d) | K carries all eight codes | **[proved]** | Lemma 15, section 4 |
| Corollary 1 | for every n >= 5 with 3 not dividing n: S = K, gamma_min = m - 1, k_c = 0 for all c, k* = 0 | **[proved, given Theorem A]** | section 5 |
| Proposition 3 | for n >= 10 with 8 not dividing n no G1 edge enters {0}; hence for odd n >= 11 with 3 not dividing n, K is the set of all cycles other than {0}; for n = 5 and n = 7, K is the set of all cycles | **[proved]** | Lemma 16, section 4 |
| cycles without 101 on even rings | which cycles of doubled words belong to K (0 of 5 for n = 10, 7 of 9 for n = 14, 10 of 45 for n = 20, 0 of 33 for n = 22; Table 2, column "cycles of doubled words in K"), and whether {0} is in K when 8 divides n and n >= 16 (not for n = 16) | **[computed for n = 10, 14, 16, 20, 22]**; no rule was found | Table 2; section 6 |
| n = 4 | Theorem 2(d) fails: the closed class consists of the two checkerboards (the only block words; there is no long block) and carries the codes 2 and 5 only; (a), (b), (c) hold | **[computed for n = 4]** | Table 2 |
| Lemmas 7 to 16, Lemma W | | **[proved]**; each also tested at small n: Lemmas 7 to 13, W, 16 and Theorem 1 exhaustively in Table 1; Lemma 14 in Table 2 (block words in one strong component) and Table 3, Part A; Lemma 15 by the executed chains of Table 3, Part C | section 3; Tables 1 to 3 |
| closed classes computed directly, without the proofs | | **[computed for n = 4..23, 3 not dividing n]**; no disagreement with the study's data and with the computation of P94 where both exist | Tables 2, 4 |
| chains of flips constructed in the proofs, executed step by step | | **[computed]**: every cycle for n = 5..23 (3 not dividing n), samples up to n = 301 | Table 3 |

No sub-statement of the goal remains open: the closed class is unique, it is described up to the cycles without 101 on even
rings, and it carries all eight codes. What the document does not contain is listed in section 6 (in particular: the proofs
have had no reader outside the session that wrote them; Theorem A and the definition of k_c are used as given; no claim of
novelty is made).

The structure follows the model of the proof for classes 43 and 142: a quantity that cannot decrease along an orbit (the
frozen set of P94) plus a description of all periodic states (Theorem 1). The description makes the freezing moves reversible,
which is what P94 did not have and what decides which cycles form the closed class.

## 1. Setting, notation, and what is taken from P94

Ring of n cells, indices mod n. Rule 94: f = 0 on the codes 000, 101, 111 and f = 1 on 001, 010, 011, 100, 110;
(F x)_i = f(x_(i-1), x_i, x_(i+1)). A 1 becomes 0 iff both neighbours are 1; a 0 becomes 1 iff its neighbours differ.
Cycles, G1, closed classes, S, gamma, k_c, k* as in `report_ring_size.md`, Section 3. An edge C -> C' of G1 exists iff for
some state x of C and some cell j the orbit of x + e_j ends on C' != C. If x and x + e_j are both periodic and lie on
different cycles C, C', then C -> C' and C' -> C are both edges ("a flip between periodic states").

From P94 (all proved there, ranges as stated there):

* Occ(x) = set of centres of occurrences of 101; frozen set W(x) = union of the occurrences. (O1) a 0 is frozen iff it is a
  centre; a 1 is frozen iff a neighbour is a centre. (O2) if j is not in W(x) then Occ(x + e_j) contains Occ(x).
* Lemma 1 (n >= 3): W(x) is contained in W(F x) and F x = x on W(x). Corollary 1a: W is constant on a cycle; write W(C).
  Corollary 1b (confinement): if every cell outside a set I lies in W(y), then F^t y = y outside I for all t, and the cells
  of I evolve under f with the other cells held fixed.
* Lemma 2 (n >= 3): W(x) is the whole ring iff x is a block word (a cyclic word over the blocks s = 01 and l = 011); block
  words are fixed points. With a short and b long blocks, 2a + 3b = n.
* Corollary 3 (n >= 5): every cycle that is not a block word has a G1 edge to a cycle with a strictly larger frozen set. In
  particular every cycle with empty frozen set has an edge to a cycle with non-empty frozen set.

New notation.

* **Window map.** For w >= 1, phi = phi_w acts on words u = u_1 ... u_w by phi(u)_i = f(u_(i-1), u_i, u_(i+1)) with
  u_0 = u_(w+1) = 1. The *padded word* of u is c = c_0 c_1 ... c_(w+1) with c_0 = c_(w+1) = 1 and c_i = u_i otherwise.
  u is *unfrozen* if the padded word has no 101 centred at one of the cells 1..w. u is *live* if it is phi-periodic and every
  state of its phi-orbit is unfrozen.
* **A_w, B_w.** Let A = (111100)^infinity and B = (100111)^infinity, indexed from 0, with letters
  A(i), B(i): A(i) = 0 iff i mod 6 is 4 or 5, B(i) = 0 iff i mod 6 is 1 or 2. Note B(i) = A(i+3) and A(i) = B(i+3). For
  w = 2 (mod 3), A_w and B_w are the words A(1) ... A(w) and B(1) ... B(w) (A_2 = 11, B_2 = 00, A_5 = 11100, B_5 = 00111,
  A_8 = 11100111, B_8 = 00111100). A(i), B(i) always denote letters and A_w, B_w always denote words.
* **Windows of a state.** If W(y) is neither empty nor the whole ring, the *windows* of y are the maximal runs of cells
  outside W(y).
* **Doubled words.** For even n, h = n/2, v in {0,1}^h and p in {0,1}, D_p(v) is the state with cells 2k + p and 2k + p + 1
  equal to v_k (k mod h). V_per is the set of periodic points of the linear map v -> v + Sv on GF(2)^h, (Sv)_k = v_(k+1).

## 2. Statements

**Theorem 1 (periodic states) [proved].** Let n >= 3. A state x is periodic under rule 94 iff one of the following holds.

1. x = 0.
2. n is even and x = D_p(v) for some p and some v in V_per, v != 0. (These are the periodic states with empty frozen set
   other than 0; for n = 2^(e+1) q, q odd, there are 2 (2^(n/2 - 2^e) - 1) of them; none if n is odd or a power of two.)
3. W(x) is not empty, and every window of x has either width w = 2 (mod 3) and content A_w or B_w, or width 4 and content
   0000, 1001 or 1111. (No window at all: x is a block word.) The period of such a state divides 6.

**Theorem 2 (the closed class) [proved].** Let n >= 5 with 3 not dividing n.

(a) G1 has exactly one closed class K.
(b) K contains every cycle C with W(C) not empty. Equivalently: a cycle outside K consists of states without 101, so it is
    {0} or, for even n, a cycle of doubled words.
(c) All block words lie in K, and K is the set of cycles that can be reached in G1 from a block word.
(d) The states of the cycles of K contain all eight codes.

**Corollary 1 [proved, given Theorem A].** For n >= 5 with 3 not dividing n: S = K, gamma_min = m - 1 (m = number of
cycles), k_c = 0 for every code c, and k* = 0.

**Proposition 3 (the zero state) [proved].** (i) For n = 5, 7, 8 the cycle {0} belongs to K. (ii) For n >= 10 with 8 not
dividing n, no G1 edge enters {0}; if moreover 3 does not divide n, {0} is not in K. (iii) Hence for odd n >= 11 with 3 not
dividing n, K is the set of all cycles except {0}, and for n = 5 and n = 7, K is the set of all cycles.

## 3. Lemmas

**Lemma 7 (windows) [proved].** Let n >= 3 and let y be a state with W(y) neither empty nor the whole ring.
(a) Both neighbours of every window are frozen cells with value 1, and every window has at most n - 3 cells.
(b) For all t >= 0, F^t y = y on W(y), and for every window I, F^t y restricted to I is phi^t(y|I) (phi of width |I|).
(c) y is periodic iff y|I is phi-periodic for every window I; in that case every y|I is live and the period of y is the
    least common multiple of the phi-periods.

*Proof.* (a) A cell next to a window is frozen. If it carried 0 it would be a centre (O1), and both its neighbours would
belong to its occurrence, hence be frozen; but one of them is a window cell. W(y) contains an occurrence, i.e. three cells.
(b) The first statement is Lemma 1 of P94. For a window cell i, (F^(t+1) y)_i = f of the cells i-1, i, i+1 of F^t y; these
are cells of the same window or neighbours of the window, which are frozen with value 1 by (a). Induction on t.
(c) By (b), F^T y = y iff phi^T(y|I) = y|I for every window I. If y is periodic, W(F^t y) = W(y) for all t (Corollary 1a),
so no cell of I lies in an occurrence of F^t y. An occurrence of 101 in the padded word of phi^t(y|I) centred at a window
cell would be an occurrence of F^t y containing that cell. So every state of the phi-orbit is unfrozen. []

**Lemma W (windows cut out of a block word) [proved].** Let x be a block word and I = {p+1, ..., p+w} with 1 <= w <= n - 3
such that (x_(p-1), x_p) = (0, 1) and (x_(p+w+1), x_(p+w+2)) = (1, 0). Then for every state y that agrees with x outside I,
every cell outside I lies in W(y), F^t y = y outside I, and F^t y restricted to I is phi_w^t(y|I).

*Proof.* The cells p-1, p, p+w+1, p+w+2 are outside I (w <= n - 3; for w = n - 3 the cells p-1 and p+w+2 coincide). In the
block word x every 0 is a centre and every 1 is next to a 0. Let q be outside I. If x_q = 0, its neighbours are 1s of x; a
neighbour inside I would force q = p or q = p+w+1, which carry 1; so the occurrence centred at q lies outside I and is an
occurrence of y. If x_q = 1 and q is not p or p+w+1, both neighbours of q are outside I, one of them is a 0 of x, and by the
previous case it is a centre in y. The cells p and p+w+1 are next to the zeros p-1 and p+w+2, which are centres in y. So every
cell outside I is frozen in y; Corollary 1b of P94 gives the rest, the two neighbours of I being held at 1. []

**Lemma 8 (live window orbits) [proved].** The live phi_w-orbits are exactly the following.
(i) For w = 2 (mod 3): the 2-cycle {A_w, B_w}.
(ii) For w = 4: the 3-cycle 0000 -> 1001 -> 1111 -> 0000.
For all other w there is no live state.

*Proof.* Let u be live, with orbit u(t), t in Z (the orbit is periodic, so it extends to all t), and let c = c(t) be the
padded words. A *run* of c is a maximal interval of [0, w+1] on which c is constant; the first run contains the cell 0, the
last run the cell w+1, the other runs are *interior*. All statements below are about an arbitrary state of the orbit, and
the image of a state of the orbit is again one.

(1) *Image rule.* For 1 <= i <= w: phi(c)_i = 1 iff c_(i-1) != c_i or c_i != c_(i+1). Indeed f = 0 exactly on 000, 101, 111,
and 101 centred at i is excluded.

(2) *No isolated window cell.* There is no i in [1, w] with c_(i-1) != c_i != c_(i+1). If c_i = 0 this is a 101 centred at i.
If c_i = 1 then c_(i-1) = c_(i+1) = 0, so i-1 and i+1 are window cells (the cells 0 and w+1 carry 1). Let c' be the
predecessor of c in the orbit. By (1), c_(i-1) = 0 gives c'_(i-2) = c'_(i-1) = c'_i and c_(i+1) = 0 gives
c'_i = c'_(i+1) = c'_(i+2); then c'_(i-1) = c'_i = c'_(i+1) and c_i = 0 by (1), a contradiction.

(3) *Runs.* By (1): an interior run [a, b] is mapped to 1 at a and b and to 0 strictly between them; the first run [0, b]
with b <= w is mapped to 1 at 0 and b and to 0 on [1, b-1]; the last run [a, w+1] with a >= 1 is mapped to 1 at a and w+1
and to 0 on [a+1, w]; if c is constant (all ones), the image is 1 0^w 1.

(4) *Lengths.* (i) Every run of zeros is interior and has even length. Its length L is at least 2 by (2). If L = 3 the image
contains 101 centred at a window cell. If L >= 4 the image has the run of zeros [a+1, b-1] of length L - 2 (the cells a and
b carry 1 in the image). By induction on L an odd length would lead to a run of length 3. (ii) Every interior run of ones has
even length: length 1 is excluded by (2), length 3 gives 101 in the image, and length L >= 4 gives a run of zeros of length
L - 2 in the image, which is even by (i). (iii) The first run has length 1 or an even length: for [0, b] with b <= w, b = 2
gives 101 centred at 1 in the image, and b >= 3 gives the run of zeros [1, b-1] in the image, so b - 1 is even. The same
holds for the last run. (iv) If c is all ones, the image has a run of zeros of length w, so w is even (w = 1 gives 101).

(5) *A first run of length 2.* Suppose the first run of c is [0, 1]. Let R_1 = [0, 1], R_2, ..., R_r be the runs and let q
be the largest index with |R_2| = ... = |R_q| = 2 (q = 1 if |R_2| != 2). The runs R_1, ..., R_q cover [0, 2q - 1], and every
window cell of this interval is the first or last cell of its run, so the image is 1 on [0, 2q - 1]. If q < r, the run
R_(q+1) starts at 2q and has length 1 (then it is the last run, 2q = w + 1, the image is all ones and w is odd, against
(4)(iv)) or length at least 4 by (4) (then the image is 1 at 2q and 0 at 2q + 1, so the first run of the image is [0, 2q],
of odd length at least 3, against (4)(iii)). Hence q = r: every run of c has length 2 and the image of c is all ones.

(6) *The orbit of the all-ones state.* Suppose some state of the orbit is all ones. Its image is 1 0^w 1 with w even, w >= 2.
For w = 2 the image of that is all ones again: the orbit is {11, 00} = {A_2, B_2}. For w >= 4 the next image is
1 1 0^(w-2) 1 1, whose first run has length 2; by (5) all its runs have length 2, so w = 4, and its image is all ones: the
orbit is 1111 -> 0000 -> 1001 -> 1111. Both orbits are indeed periodic and unfrozen.

(7) *Orbits without the all-ones state.* Suppose no state of the orbit is all ones. By (5) no state has a first run of length
2, and by the mirror image no state has a last run of length 2. By (4)(iii) the first run of every state has length 1 or an
even length at least 4.
If the first run of c has length 1, then c_1 = 0, the run of zeros is [1, b], and the image has c_1 = 1; so the first run of
the image has length at least 2, hence at least 4, i.e. the image is 1 at the cells 2 and 3. By (3) the image is 1 at the
cell 2 only if 2 is the last cell of [1, b]: b = 2. So c starts with 1 0 0 1 ("type beta").
If the first run of c is [0, b] with b >= 3, the image is 0 at the cell 1, so it is of type beta and is 1 at the cell 3; by
(3) this forces b = 3. So c starts with 1 1 1 1 0 ("type alpha"; in particular w >= 4), and its image is of type beta.
Thus the states of the orbit are alternately of type alpha and of type beta. We show by induction on m, 3 <= m <= w + 1:
every alpha state agrees with A on [0, m] and every beta state agrees with B on [0, m]. For m = 3 this was just shown.
Let 3 <= m <= w and let c be an alpha state, c+ its image (a beta state). The cell m is a window cell. If
c_(m-1) = c_m, then by (1) c_(m+1) = c_m iff c+_m = 0; if c_(m-1) != c_m, then c_(m+1) = c_m by (2). In both cases c_(m+1)
is determined by c on [0, m] and c+ on [0, m]. The words A and B satisfy the same two rules (B is the image of A under the
rule (1), and A has no isolated cell), so c_(m+1) = A(m+1). The same argument with a beta state and its image, an alpha
state, gives c_(m+1) = B(m+1), because A is the image of B under (1) and B has no isolated cell.
So the orbit is {A(1) ... A(w), B(1) ... B(w)} and A(w+1) = B(w+1) = 1. A(i) = 1 iff i mod 6 is in {0, 1, 2, 3} and
B(i) = 1 iff i mod 6 is in {0, 3, 4, 5}; both hold iff 3 divides w + 1. Hence w = 2 (mod 3) and the orbit is {A_w, B_w}.
Conversely, for w = 2 (mod 3), w >= 5, the padded words of A_w and B_w are A and B on [0, w+1]; they contain no 101, and
the rule (1) maps each to the other (at the cell w the right neighbour is A(w+1) = B(w+1) = 1, as in the infinite words).
So {A_w, B_w} is a live 2-cycle. []

**Lemma 9 (periodic states with empty frozen set) [proved].** Let n >= 3. A periodic state x with W(x) empty is 0, or n is
even and x = D_p(v) with v in V_per, v != 0. Conversely these states are periodic and have empty frozen set. For
n = 2^(e+1) q with q odd, V_per has 2^(n/2 - 2^e) elements.

*Proof.* Let x be periodic with empty frozen set, x != 0. x is not 1^n (F(1^n) = 0 and F(0) = 0), so x is not constant. No
state of the cycle contains 101 (Corollary 1a), so (F y)_i = 1 iff y_(i-1) != y_i or y_i != y_(i+1) for every state y of the
cycle. As in (2) of Lemma 8 no state of the cycle has an isolated 1 (an isolated 0 is a 101). As in (4): a run of zeros of
length L >= 4 is mapped to a run of zeros of length L - 2, length 3 gives 101, so runs of zeros have even length; a run of
ones of length 3 gives 101 and one of length L >= 4 gives a run of zeros of length L - 2, so runs of ones have even length.
All runs being even, n is even, all run boundaries have the same parity, and x = D_p(v) for some p and a non-constant v.
For every v, using f(a, b, b) = a + b and f(a, a, b) = a + b (mod 2), F(D_0(v)) = D_1(v') with v'_k = v_k + v_(k+1), and
F(D_1(v)) = D_0(v'') with v''_(k+1) = v_k + v_(k+1). So on doubled words F^2 is conjugate to an invertible shift composed with
(1 + S)^2, and D_p(v) is periodic iff v is a periodic point of 1 + S. Doubled words contain no 101.
In GF(2)[S]/(S^h - 1), h = 2^e q, S^h - 1 = (S^q - 1)^(2^e) and 1 + S divides S^q - 1 exactly once; so the kernel of
(1 + S)^j has dimension min(j, 2^e), and V_per, the image of (1 + S)^(2^e), has dimension h - 2^e. The only constant
vectors are 0 and the all-ones vector, which lies in the kernel of 1 + S; so a non-zero v in V_per is not constant and
D_0(v), D_1(v') are different states for non-zero v, v' in V_per. []

**Lemma 10 (reversible freezing) [proved].** Let n >= 3 and let C be a cycle with W(C) neither empty nor the whole ring.
Then there are a state y of C and a cell j such that y + e_j is periodic and W(y + e_j) contains W(y) properly. Hence C and
the cycle C' of y + e_j are joined by G1 edges in both directions, and W(C') contains W(C) properly.

*Proof.* Let y be in C and let I = {p+1, ..., p+w} be a window of y; write c for the padded word (c_0 = y_p, c_i = y_(p+i)).
By Lemma 7 and Lemma 8, y|I is A_w or B_w with w = 2 (mod 3), or w = 4 and y|I is one of 0000, 1001, 1111; in the last case
replace y by a state of C in which this window is 0000 or 1111 (C contains one, by Lemma 7(b)).
* y|I = A_w: flip the window cell 2 (j = p + 2). Now c_1 c_2 c_3 = 1 0 1 (c_3 = A(3) = 1, the neighbour of the window if
  w = 2). The cells 1, 2, 3 are frozen. If w >= 5 the cells 4..w form a run between the frozen ones c_3 and c_(w+1), with
  content A(4) ... A(w) = B(1) ... B(w-3), i.e. the word B_(w-3), a live state.
* y|I = B_w: flip the window cell 1. Now c_1 c_2 c_3 = 1 0 1 (c_2 = B(2) = 0, c_3 = B(3) = 1). If w >= 5 the cells 4..w have
  content B(4) ... B(w) = A(1) ... A(w-3), i.e. the word A_(w-3), a live state.
* y|I = 1111: flip the window cell 1. Now c_0 c_1 c_2 = 1 0 1; the cells 3, 4 have content 11 = A_2 between the frozen ones
  c_2 and c_5.
* y|I = 0000: flip the window cell 2. Now c_1 c_2 c_3 = 0 1 0 and c_0 c_1 c_2 = 1 0 1; the cells 3, 4 have content 00 = B_2
  between the frozen ones c_2 and c_5.
In every case j is not in W(y), so Occ(y + e_j) contains Occ(y) (O2). The flip changes the codes of the cells j - 1, j,
j + 1 only, and among these exactly one becomes a centre, the one named above (the other two carry 1 after the flip, or, in
the case 0000, the cell 3 has the code 100). So W(y + e_j) is W(y) together with the cells of the new occurrence: two or
three new cells. The remaining part of I named above (the cells 4..w, respectively 3, 4; empty for w = 2) lies between
frozen ones, contains no centre and is next to no centre, so it is a window of y + e_j, and its content is live (Lemma 8).
The other windows of y + e_j are the windows of y other than I, with unchanged contents, which are phi-periodic by
Lemma 7(c) for y. By Lemma 7(c), y + e_j is periodic. It lies on another cycle because the frozen set is constant on a
cycle. []

**Lemma 11 (swap, both directions) [proved].** Let n >= 5, x a block word, and let the cells p, ..., p+4 carry the blocks
s l: (x_p, ..., x_(p+4)) = (0,1,0,1,1). Let x' be x with these cells replaced by (0,1,1,0,1) (blocks l s). Then
x + e_(p+2) and x + e_(p+3) are the two states of a cycle C2 of period 2, x' = x + e_(p+2) + e_(p+3) is a block word, and
{x} -> C2 -> {x'} -> C2 -> {x} are edges of G1.

*Proof.* Lemma W applies to I = {p+2, p+3}: (x_p, x_(p+1)) = (0,1), x_(p+4) = 1, and x_(p+5) = 0 is the first cell of the
next block (for n = 5 it is the cell p). The map phi_2 fixes 01 and 10 and exchanges 11 and 00. The window content of x is
01; one flip gives 11 or 00, a second flip gives 10. All four states are periodic. []

**Lemma 12 (merge; Lemma 5 of P94) [proved].** Let n >= 6, x a block word, and let the cells p, ..., p+5 carry three short
blocks, the next block starting at p+6. Let x'' be x with these six cells replaced by (0,1,1,0,1,1). Then
F(x + e_(p+3)) = x'' and {x} -> {x''} is an edge of G1. (Lemma W with I = {p+2, p+3, p+4}: content 010, after the flip 000,
and phi_3(000) = 101.)

**Lemma 13 (split) [proved].** Let n >= 8, x a block word, and let the cells p, ..., p+7 carry the blocks s l l:
(x_p, ..., x_(p+7)) = (0,1,0,1,1,0,1,1). Let x'' be x with these eight cells replaced by (0,1,0,1,0,1,0,1) (four short
blocks). Then y = x + e_(p+2) lies on a cycle C of period 2, and F^5(F(y) + e_(p+6)) = x''. So {x} -> C -> {x''} are edges
of G1.

*Proof.* Lemma W applies to I = {p+2, ..., p+6}: (x_p, x_(p+1)) = (0,1), x_(p+7) = 1 and x_(p+8) = 0 (first cell of the next
block; for n = 8 it is the cell p). The window content of x is 01101. With both neighbours 1:
phi_5(11101) = 00101 and phi_5(00101) = 11101 (a 2-cycle), and
00100 -> 11111 -> 00000 -> 10001 -> 11011 -> 01010, which is fixed. The content 01010 gives (0,1,0,1,0,1,0,1) on
p, ..., p+7. []

**Lemma 14 (block words) [proved].** Let n >= 5 with 3 not dividing n. All block words lie in one strongly connected
component of G1.

*Proof.* Every block word has a >= 1 short blocks, because 2a + 3b = n and 3 does not divide n.
(i) *Same (a, b), b >= 1.* Read a block word from a block start c as a linear word over {s, l}. Swaps s l -> l s
(Lemma 11) sort it to l^b s^a read from c; call this state X_c. The swaps are edges in both directions, so every block
word with a short and b long blocks is in the strong component of some X_c. Read X_c from its block start c + 3 (after the
first long block): the linear word is l^(b-1) s^a l, and sorting gives X_(c+3). So X_c and X_(c+3) are in the same strong
component; since 3 and n are coprime, all X_c are.
(ii) *Changing (a, b).* If a >= 3, some block word of the class has three consecutive short blocks (for b >= 1 by (i); for
b = 0 every block word has), and Lemma 12 gives a path to the class (a - 3, b + 2). If b >= 2, some block word of the class
has consecutive blocks s l l, and Lemma 13 gives a path to the class (a + 3, b - 2). The classes are (a_0 + 3i, b_0 - 2i),
i >= 0, with a_0 in {1, 2}, so consecutive classes are joined in both directions.
(iii) *b = 0* (n even). The class consists of the two checkerboards. Each is reached by Lemma 13 from a block word of the
class (a - 3, 2) in which s l l starts at a cell of the suitable parity (by (i) all rotations of a block word of that class
are available), and Lemma 12 leads back. []

**Lemma 15 (the code 000) [proved].** Let n >= 5 with 3 not dividing n, and let K be a closed class that contains every
cycle with a non-empty frozen set. Then some state of a cycle of K contains 000.

*Proof.* n = 7 or n >= 10: let z be the word 0 1 0 0 0 0 1 followed by a block word of length n - 7 written from a block
start (nothing for n = 7; n - 7 >= 3 and n - 7 is not 1, so such a word exists: n - 7 = 2a + 3b has a solution for every
n - 7 >= 2). The cell 0 is a centre (its neighbours are the cell 1 and the last cell of the ring, both 1), the cell 6 is
next to a centre, and the cells of the appended block word are frozen as in a block word. So W(z) is the complement of the
window {2, 3, 4, 5}, whose content 0000 is live (Lemma 8). By Lemma 7(c) z is periodic; its cycle has a non-empty frozen set
and z contains 000 at the cells 3 and 4.
n = 5: y = 01111 has the occurrence centred at 0 and the window {2, 3} with content 11 = A_2, so y is periodic with
non-empty frozen set, and its cycle is in K. y + e_0 = 1^5 and F(1^5) = 0. So K has an edge to {0}; K is closed, so {0} is
in K, and 0 contains 000.
n = 8: y = 01111010 has the occurrence centred at 5 only, and the window {7, 0, 1, 2, 3} with content 00111 = B_5; so y is
periodic with non-empty frozen set. By the rule table the orbit of y + e_5 is 01111110 -> 11000011 -> 01100110 -> 11111111 -> 0 (four
applications of f to every cell; the same orbit is recorded in Table 3, Part C). As before {0} is in K. []

**Lemma 16 (basin of the zero state) [proved].** Let n >= 3.
(i) F(x) = 0 iff x is 0 or 1^n.
(ii) F(x) = 1^n iff x is a cyclic word over the blocks 001 and 0011.
(iii) If F(z) is a cyclic word over the blocks 001 and 0011, then 8 divides n.
Hence, if 8 does not divide n, the states whose orbit ends in 0 are exactly 0, 1^n and the cyclic words over 001 and 0011.

*Proof.* (i) All codes of x are in {000, 101, 111}. A code 101 at i would be followed by the code (0, 1, x_(i+2)), which is
010 or 011. So all codes are 000 or 111 and x is constant. (ii) The codes of x avoid 000, 101, 111: x has both symbols, no
run of three zeros, no isolated zero, no run of three ones; so every run of zeros has length 2 and every run of ones has
length 1 or 2. (iii) Let y = F(z) and let (i, i+1) be a run of zeros of y. The codes of z at i and i+1 are in
{000, 101, 111}; 101 at i is impossible as in (i), so the code at i is 000 or 111; then z_i = z_(i+1), so the code at i+1 is not 101
either, and z is constant, say equal to a, on [i-1, i+2]. Since y_(i-1) = 1 and
y_(i+2) = 1, z_(i-2) and z_(i+3) differ from a: z has a run of length exactly 4 at [i-1, i+2]. If y contained a block 001,
the next run of zeros of y would be (i+3, i+4), and z would have a second run of length exactly 4 at [i+2, i+5], which
overlaps the first without being equal to it. So y = (0011)^(n/4), the runs of z of length 4 tile the ring and alternate in
value: 8 divides n. []

## 4. Proofs of the theorems

*Theorem 1.* Let x be periodic. If W(x) is empty, Lemma 9 gives case 1 or 2. If W(x) is the whole ring, x is a block word
(Lemma 2 of P94), which is case 3 without windows. Otherwise Lemma 7(c) and Lemma 8 give case 3. Conversely the states of
cases 1 and 2 are periodic (Lemma 9), block words are fixed, and a state as in case 3 with windows is periodic by Lemma 7(c),
because A_w, B_w, 0000, 1001, 1111 are phi-periodic (Lemma 8). The periods of the window contents are 2 and 3. The count in
case 2 is that of Lemma 9. []

*Theorem 2.* Let BW be the strong component of G1 that contains all block words (Lemma 14).
(b) and (c). Let C be a cycle with W(C) not empty. Applying Lemma 10 repeatedly gives cycles C = C_0, C_1, ..., C_r with
strictly increasing frozen sets, consecutive ones joined by edges in both directions, until the frozen set is the whole
ring; C_r is a block word (Lemma 2 of P94). So C lies in BW.
(a) Every cycle has a G1 path into BW: a cycle with empty frozen set has an edge to a cycle with non-empty frozen set
(Corollary 3 of P94, n >= 5), which lies in BW. If C is in BW and C -> C' is an edge, then C' has a path back into BW, so C'
is in the strong component BW. Hence BW has no leaving edge: it is a closed class, K := BW. Any closed class contains,
with one of its cycles, the cycles reachable from it, hence a cycle of K, hence equals K. So K is the only closed class, it
contains every cycle with non-empty frozen set, and it is the set of cycles reachable from the block words (reachable
cycles are in K because K is closed; cycles of K are reachable because K is strongly connected). The cycles outside K have
empty frozen set; by Theorem 1 they are {0} or cycles of doubled words.
(d) Take a block word x with a >= 1 and b >= 1 blocks (the class (a_0, b_0) has b_0 >= 1 for n >= 5) in which a short block
is followed by a long one. Short block followed by any block: 1 | 0 1 | 0 gives the codes 101 (at the 0) and 010 (at the 1).
Long block: 0 1 1 | 0 gives 011 and 110. The cycle C2 of Lemma 11 lies in K; its state with window content 11 has 1 1 1 1 on
p+1..p+4 (code 111), its state with window content 00 has 1 0 0 1 there (codes 100 and 001). The code 000 is Lemma 15. []

*Proposition 3.* (i) is contained in the proof of Lemma 15 for n = 5 and 8; for n = 7, y = 0111111 has the occurrence
centred at 0 and the window {2, ..., 5} with content 1111, so it is periodic with non-empty frozen set, and
y + e_0 = 1^7 -> 0.
(ii) Let n >= 10 with 8 not dividing n. An edge C -> {0} needs a periodic state y != 0 and a cell j such that the orbit of
y + e_j ends in 0, i.e. (Lemma 16) y + e_j is 0, 1^n or a word z over the blocks 001 and 0011.
y = e_j is not periodic: F^2(e_j) contains 101 (Lemma 3(a) of P94), e_j does not, and W is constant on cycles.
y = 1^n + e_j has the single occurrence centred at j and one window of width n - 3 >= 7 with content all ones; by
Theorem 1 it is periodic only if the all-ones word is A_w, B_w (w >= 5 contains a 0 in both) or 1111 (w = 4): not for
n >= 10.
y = z + e_j with z_j = 1: y has no 101 (z has none, and a new 0 at j would need z_(j-1) z_j z_(j+1) = 111), and y != 0. The
runs of ones of z have length 1 or 2 and its runs of zeros have length 2; removing a 1 creates a run of ones of length 1 or
a run of zeros of length 5. By Lemma 9 y is not periodic.
y = z + e_j with z_j = 0: the zeros of z come in pairs between ones, so y has exactly one occurrence, containing j, and one
window of width n - 3 >= 7 on which y = z. If y were periodic, the window content would be A_w or B_w with w >= 8
(Theorem 1), which contains three consecutive ones (A_w: the cells 1, 2, 3; B_w: the cells 3, 4, 5); z has no three
consecutive ones.
So no edge enters {0}. A closed class with more than one cycle is strongly connected, so {0} is not in K (K contains the
block words).
(iii) For odd n the cycles with empty frozen set are {0} only (Theorem 1), so by Theorem 2(b) K contains all other cycles;
{0} is in K for n = 5, 7 by (i) and not for odd n >= 11 by (ii) (8 does not divide an odd number). []

## 5. Corollary 1

By Theorem A (`report_ring_size.md`, Section 4; used as given), if G1 has a unique closed class K then S = K and
gamma_min = m - 1. By the definition of k_c (note v0.2, Section 6: k_c = min over cycles C of [gamma(C) + R(C -> D_c)] minus
min gamma, with R(C -> D_c) = 0 iff a state of C contains the code c), k_c = 0 iff a state of a selected cycle contains c.
Theorem 2(d) gives k_c = 0 for all eight codes, so k* = 0, for every n >= 5 with 3 not dividing n. Together with Theorem V94
of the report (k* = 1 for 3 | n, n >= 6): **for rule 94 and every n >= 5, k* = 1 if 3 divides n and k* = 0 otherwise
[proved, given Theorem A]**; for 3 | n, n >= 6 this is Theorem V94, and n = 3 is not covered by either proof. []

## 6. Scope, and what is not shown

* **Cycles without 101 on even rings.** For even n the cycles of doubled words (Theorem 1, case 2) exist unless n is a power
  of two. Whether such a cycle lies in K is decided by whether it has an incoming G1 path from K; Table 2 shows no regular
  pattern (in K: 0 of 5 for n = 10, 7 of 9 for n = 14, 10 of 45 for n = 20, 0 of 33 for n = 22). **[computed]**, no rule found, nothing
  claimed for larger n. This does not affect Theorem 2 or Corollary 1.
* **{0} when 8 divides n.** Lemma 16 describes the basin of 0 only when 8 does not divide n (for 8 | n it contains further
  levels, e.g. (00001111)^(n/8)). {0} is in K for n = 8 (Lemma 15) and has no incoming edge for n = 16 (Table 2,
  **[computed]**); for 8 | n, n >= 24 this is not determined.
* **n = 4.** The proofs need n >= 5 (Corollary 3 of P94; a long block for the codes 011 and 110). For n = 4 there is one
  closed class, the two checkerboards; it contains every cycle with a 101 and equals the set of cycles reachable from the
  block words, but it carries the codes 2 and 5 only (Table 2): (a), (b), (c) of Theorem 2 hold and (d) fails.
  **[computed for n = 4]**.
* **Theorem A and k_c** are used as given (Corollary 1 only).
* **No computer-assisted step.** The proofs use the rule table only. The computations of section 7 are tests of the lemmas,
  an independent direct computation of the closed classes, and executions of the constructed chains.
* **Tests that were corrected.** Two test definitions in `check_lemmas_94.py` were wrong in their first version and were
  corrected before the results of Table 1 were produced: the merge test (L12) matched 0 1 0 1 0 1 without requiring that the
  third block is short, and the split test (L13) iterated four steps instead of the five of Lemma 13. The lemmas were not
  changed.
* **Reading.** One adversarial second reading was made inside the session that wrote the proofs, by a reader that did not
  see the author's scripts and re-tested every statement with separate code for n <= 16 and window widths <= 16 (no
  violation; it found no false statement, one unjustified step in the proof of Lemma 10, which is now written out, and
  eight points of wording and labelling, which are corrected). That reader did not recompute the tables beyond n = 16 and
  did not check Theorem A, the definition of k_c or Theorem V94. No reader outside the session has checked the proofs.
* **Literature (short search, two queries, 17 November 2026).** Found: rule 94 is listed among the almost equicontinuous
  rules in the topological classification of elementary cellular automata (Schuele and Stoop, arXiv:1107.2080, search
  excerpt only), and its fixed points appear in a study of fuzzy cellular automata (Flocchini and Cezar, "Radial view of
  continuous cellular automata", search excerpt only). Neither text was read; no source was found for the frozen word 101,
  the window classification of Lemma 8, or the closed class. On configurations without 101 the walls of rule 94 evolve by
  rule 18 (two adjacent walls annihilate, otherwise rule 90); this relation was not searched for. No claim of novelty is
  made for any statement.

## 7. Computations (verbatim copy of `out/tables_94.md`)

### Table 1. Exhaustive tests of the lemmas (`check_lemmas_94.py` -> `out/check_lemmas_94.json`)

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| L7 | Lemma 7 (windows): boundary cells are frozen ones, width <= n-3, F^t = identity on the frozen set and = phi^t on every window, t = 1..10; every state with non-empty frozen set that is not fully frozen | 5..14 | 26454 | 0 |
| L8 | Lemma 8 (live window orbits): the periodic unfrozen orbits of the window map are {A_w, B_w} for w = 2 mod 3, the 3-cycle 0000, 1001, 1111 for w = 4, and none otherwise; all 2^w window states | w = 1..22 | 8388606 | 0 |
| L7c | Lemma 7(c): a state with non-empty frozen set is periodic iff all its window contents are phi-periodic; every state with non-empty frozen set | 5..16 | 112255 | 0 |
| L9 | Lemma 9: a periodic state with empty frozen set is 0 or has only runs of even length; their number is 1 for odd n and 2(2^(n/2 - 2^e) - 1) + 1 for even n = 2^(e+1) q, q odd (n >= 5); every periodic state | 3..20 | 1230 | 0 |
| T1 | Theorem 1 (periodic states): a state is periodic iff it is 0, or a doubled word with periodic half word, or has non-empty frozen set and only live windows; every state | 3..16 | 131064 | 0 |
| T1b | Theorem 1, direction "periodic implies the description"; every periodic state | 17..20 | 28285 | 0 |
| L10 | Lemma 10 (reversible freezing): in every state of the cycle whose first window is not 1001, the flip named in the lemma gives a periodic state of another cycle with a strictly larger frozen set; every cycle with non-empty frozen set that is not a block word | 5..20 | 11356 | 0 |
| L11 | Lemma 11 (swap, both directions): x + e_(p+2) and x + e_(p+3) form a 2-cycle and x + e_(p+2) + e_(p+3) is the block word with the two blocks exchanged; every block word, every pair of consecutive blocks short, long | 5..24 | 7343 | 0 |
| L12 | Lemma 12 (merge): F(x + e_(p+3)) is the block word with the three short blocks replaced by two long ones; every block word, every triple of consecutive short blocks | 6..24 | 5543 | 0 |
| L13 | Lemma 13 (split): x + e_(p+2) has period 2; five steps after flipping the cell p+6 of its other state the block word with short, long, long replaced by four short blocks is reached; every block word, every occurrence of short, long, long | 8..24 | 3156 | 0 |
| L16 | Lemma 16 (basin of 0): if 8 does not divide n, the states whose orbit ends in 0 are exactly 0, 1^n and the cyclic words over the blocks 001 and 0011 (case = one state of the basin of 0, or one such word) | 5..20 (8 not dividing n) | 544 | 0 |
| LW | Lemma W: every cell outside the window is frozen, F^t = identity outside and = phi^t inside, t = 1..6; every block word, every admissible window of width <= 7, every content (case = one content) | 5..13 | 62082 | 0 |
| L16a | Lemma 16 (i), (ii), (iii): F(x) = 0 iff x is 0 or 1^n; F(x) = 1^n iff x is a word over 001 and 0011; F(z) is such a word only if 8 divides n; every state (case = one state) | 3..16 | 131064 | 0 |

All tests passed: True. CPU time 88.01 s.

Live window orbits found (test L8), by width: w = 2: {00, 11}; w = 4: {0000, 1001, 1111}; w = 5: {00111, 11100}; w = 8: {00111100, 11100111}; w = 11: {00111100111, 11100111100}; w = 14: {00111100111100, 11100111100111}; w = 17: {00111100111100111, 11100111100111100}; w = 20: {00111100111100111100, 11100111100111100111}.

Numbers of periodic states with empty frozen set (test L9), by n: 3: 1, 4: 1, 5: 1, 6: 7, 7: 1, 8: 1, 9: 1, 10: 31, 11: 1, 12: 31, 13: 1, 14: 127, 15: 1, 16: 1, 17: 1, 18: 511, 19: 1, 20: 511.

### Table 2. G1 and its closed classes computed directly, 3 not dividing n (`g1_classes_94.py` -> `out/g1_classes_94.jsonl`)

| n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | block words | block words in one strong component | cycles with 101 in K | cycles without 101 in K ({0} included) | cycles of doubled words in K | periods of the cycles without 101 in K (period: count) | periods of the cycles without 101 outside K | {0} in K | G1 edges into {0} | codes on K | K = cycles reachable from the block words | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 3 | 3 | 4 | 2 | 1 [2] | 2 | True | 2 of 2 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [2, 5] | True | 0.0 | 53 |
| 5 | 11 | 16 | 55 | 1 | 1 [11] | 5 | True | 10 of 10 | 1 of 1 | 0 of 0 | {'1': 1} | - | True | 5 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 7 | 22 | 43 | 147 | 1 | 1 [22] | 7 | True | 21 of 21 | 1 of 1 | 0 of 0 | {'1': 1} | - | True | 7 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 8 | 27 | 43 | 146 | 1 | 1 [27] | 10 | True | 26 of 26 | 1 of 1 | 0 of 0 | {'1': 1} | - | True | 8 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 10 | 73 | 158 | 610 | 7 | 1 [67] | 17 | True | 67 of 67 | 0 of 6 | 0 of 5 | - | {'1': 1, '6': 5} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 11 | 78 | 144 | 638 | 2 | 1 [77] | 22 | True | 77 of 77 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.01 | 53 |
| 13 | 209 | 404 | 2145 | 2 | 1 [208] | 39 | True | 208 of 208 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.02 | 54 |
| 14 | 320 | 871 | 4284 | 4 | 1 [317] | 51 | True | 310 of 310 | 7 of 10 | 7 of 9 | {'14': 7} | {'1': 1, '14': 2} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.04 | 54 |
| 16 | 747 | 1723 | 10130 | 2 | 1 [746] | 90 | True | 746 of 746 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.15 | 55 |
| 17 | 1191 | 3112 | 18088 | 2 | 1 [1190] | 119 | True | 1190 of 1190 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.3 | 57 |
| 19 | 2832 | 7677 | 48773 | 2 | 1 [2831] | 209 | True | 2831 of 2831 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 1.14 | 68 |
| 20 | 4513 | 12498 | 86322 | 37 | 1 [4477] | 277 | True | 4467 of 4467 | 10 of 46 | 10 of 45 | {'12': 10} | {'1': 1, '6': 5, '12': 30} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 2.25 | 85 |
| 22 | 10827 | 33388 | 237886 | 35 | 1 [10793] | 486 | True | 10793 of 10793 | 0 of 34 | 0 of 33 | - | {'1': 1, '62': 33} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.92 | 182 |
| 23 | 16952 | 48301 | 358846 | 2 | 1 [16951] | 644 | True | 16951 of 16951 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 1.73 | 376 |

K denotes the closed class (unique in every row). n = 4 is listed for comparison only; the theorems need n >= 5.

### Table 3. The chains of the proofs, executed step by step (`chains_94.py` -> `out/chains_94.json`)

Part A: every cycle. Growth flip for the cycles without 101, freezing chain to a block word (every flip joins two periodic states), and the digraph of swaps, merges and splits on the block words with every move executed.

| n | cycles | cycles with 101 | growth flips | all chains end on a block word | max freezing flips | mean freezing flips | block words | moves executed | move graph strongly connected | max flips from a block word to l^b0 s^a0 | max flips from l^b0 s^a0 to a block word |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 11 | 10 | 1 | True | 1 | 0.55 | 5 | 10 | True | 4 | 4 |
| 7 | 22 | 21 | 1 | True | 2 | 1.05 | 7 | 14 | True | 6 | 6 |
| 8 | 27 | 26 | 1 | True | 2 | 0.89 | 10 | 32 | True | 5 | 6 |
| 10 | 73 | 67 | 6 | True | 2 | 1.1 | 17 | 60 | True | 7 | 8 |
| 11 | 78 | 77 | 1 | True | 3 | 1.29 | 22 | 77 | True | 7 | 8 |
| 13 | 209 | 208 | 1 | True | 3 | 1.56 | 39 | 169 | True | 8 | 9 |
| 14 | 320 | 310 | 10 | True | 4 | 1.77 | 51 | 224 | True | 8 | 10 |
| 16 | 747 | 746 | 1 | True | 4 | 2.06 | 90 | 464 | True | 10 | 12 |
| 17 | 1191 | 1190 | 1 | True | 5 | 2.16 | 119 | 646 | True | 10 | 12 |
| 19 | 2832 | 2831 | 1 | True | 5 | 2.48 | 209 | 1273 | True | 11 | 14 |
| 20 | 4513 | 4467 | 46 | True | 6 | 2.55 | 277 | 1780 | True | 11 | 14 |
| 22 | 10827 | 10793 | 34 | True | 6 | 2.86 | 486 | 3432 | True | 13 | 16 |
| 23 | 16952 | 16951 | 1 | True | 7 | 3.03 | 644 | 4761 | True | 13 | 16 |

Part B: cycles reached from 200 random states; freezing chain, sorting and merging down to l^b0 s^a0, chain to the cycle with the code 000 (Lemma 15).

| n | start states | all chains end on the cycle with code 000 | max freezing flips | max sorting and merging flips | mean flips |
|---|---|---|---|---|---|
| 25 | 200 | True | 5 | 51 | 28.23 |
| 26 | 200 | True | 5 | 58 | 32.22 |
| 31 | 200 | True | 6 | 78 | 43.55 |
| 40 | 200 | True | 6 | 120 | 72.43 |
| 50 | 200 | True | 7 | 181 | 110.56 |
| 64 | 200 | True | 9 | 283 | 175.55 |
| 100 | 200 | True | 13 | 685 | 421.35 |
| 200 | 200 | True | 23 | 2561 | 1675.88 |
| 301 | 200 | True | 27 | 5128 | 3764.47 |

Part C. Lemma 15, chain from l^b0 s^a0 to the cycle with a width-4 window in the state 0000, executed for n = 7 and 10..300, 3 not dividing n (195 ring sizes): all executed: True; flips: [2] for n = 1 mod 3, [4] for n = 2 mod 3.

Chains into {0} for n = 5, 7, 8 (a periodic state that is joined to a block word by flips between periodic states; one flip; the orbit then reaches 0):

| n | periodic state (cell 0 first) | its period | flipped cell | steps until 0 | orbit after the flip | flips between periodic states from the block word | block word |
|---|---|---|---|---|---|---|---|
| 5 | 01111 | 2 | 0 | 1 | - | 1 | 01101 |
| 7 | 0111111 | 3 | 0 | 1 | - | 2 | 0101101 |
| 8 | 01111010 | 2 | 5 | 4 | 01111110 -> 11000011 -> 01100110 -> 11111111 -> 00000000 | 2 | 01101011 |

CPU time of `chains_94.py`: 171.11 s.

### Table 4. Comparison with data already in the repository (`crosscheck_data.py` -> `out/crosscheck_data.json`)

| compared with | ring sizes n | fields compared | disagreements |
|---|---|---|---|
| data/ring_size/mechanisms.csv | 8, 10, 11, 13, 14, 16, 17, 19, 20, 22 | cycles; selected cycles = size of the closed class; gamma_min = m - 1; k_c = 0 for all c; k* = 0 | 0 |
| verify_ring_size/part2_94/out/g1_classes.jsonl | 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23 | cycles; periodic states; G1 edges; strong components; closed-class sizes | 0 |

Notes on the tables.

* Table 2 is independent of the proofs: all 2^n states are tabulated, the periodic states and the cycle every state falls
  to are determined, all single flips of all periodic states are followed, and strong components are computed.
* Table 4: the study's records exist for n = 8..22; the fields compared are named in the table. The comparison reads the
  files of the repository and changes none.
* Table 3: every flip is applied to a periodic state, the flipped state is iterated until periodic, and the script asserts
  that the cycle reached is the predicted one and differs from the current one. In the freezing chains both states of every
  flip are periodic, so the reversed chain is a chain of flips as well.

## 8. Files (all under `proofs_94_26/`)

| file | content |
|---|---|
| `PROOF_94_converse.md` | this document |
| `ring.py` | tools: F on all states, cycles, G1, closed classes, frozen set, block words, window map (NumPy, own code) |
| `check_lemmas_94.py`, `out/check_lemmas_94.json` | exhaustive tests of Lemmas 7 to 13, W, 16 and of Theorem 1 |
| `g1_classes_94.py`, `out/g1_classes_94.jsonl` | direct computation of G1 and its closed classes, one record per n |
| `chains_94.py`, `out/chains_94.json` | execution of the chains of the proofs |
| `crosscheck_data.py`, `out/crosscheck_data.json` | comparison with `data/ring_size/mechanisms.csv` and `verify_ring_size/part2_94/out/g1_classes.jsonl` (read only) |
| `make_tables.py`, `out/tables_94.md` | tables of section 7 |
| `test_proofs_94_26.py` | tests of the folder (both documents) |

To reproduce (repository root; Python with NumPy and SciPy; one process; about 5 minutes of CPU time in total, peak memory
about 0.5 GB at n = 23):

    python proofs_94_26/check_lemmas_94.py
    python proofs_94_26/g1_classes_94.py 4 5 7 8 10 11 13 14 16 17 19 20 22 23
    python proofs_94_26/chains_94.py
    python proofs_94_26/crosscheck_data.py      (after the rule 26 scripts of PROOF_26.md, section 9)
    python proofs_94_26/make_tables.py
