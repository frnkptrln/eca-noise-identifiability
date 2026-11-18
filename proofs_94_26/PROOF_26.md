# Rule 26 on rings of n = 2^k cells: a quantity that cannot increase, the periodic states without 111, and the path of every cycle to the zero state

Folder: `proofs_94_26/`. Starting points: `report_ring_size.md`, Sections 5.3, 5.7, 5.8, and
`verify_ring_size/part2_154/PROOF_154.md` (cited as P154). All numbers below are taken from files written by the scripts of
this folder (section 8 is a verbatim copy of `out/tables_26.md`, which `make_tables.py` builds from the output files).
Tags: [proved] = the argument covers every n in the stated range and uses no computation; [proved, given Theorem A] = in
addition Theorem A of the report (Section 4) is used as given; [computed for n = ...] = seen in enumeration only;
[attempted (gap: ...)] = not proved, the gap is named.

## 0. Result in brief

| item | statement | status | where |
|---|---|---|---|
| Lemma 2 | for every even n, the number c(x) of parity changes in the cyclic sequence of the ones of x does not increase under rule 26; it is constant on every cycle | **[proved]** | section 3 |
| Theorem 1 | periodic states for every even n: states on one parity class that are periodic under rule 90; the *domain states* (an explicit set, permuted by F); and periodic states whose orbit contains 111. For n = 2^k the first kind is 0 alone | **[proved]** | section 4 |
| Theorem 2 (the goal) | for n = 2^k >= 4 every cycle other than {0} has a directed path to {0} in G1 (an explicit chain of flips); for every even n >= 4 every cycle has a G1 path to a cycle on one parity class | **[proved]** | section 4 |
| Theorem 3 | for n = 2^k >= 4: {0} is the only closed class of G1; gamma({0}) = m - 1, gamma(C) >= m for every other cycle, with equality iff C is reachable in G1 from a cycle at resistance 2 from {0}; S = {{0}}; for n >= 8 every domain cycle has gamma = m | **[proved]** (Theorem A is not needed) | section 4 |
| Theorem 4(a) | for n = 2^k >= 8: k_0 = 0 and k_c = 1 for c = 1, ..., 6 | **[proved]** | section 5 |
| Theorem 4(b) | for n = 2^k >= 8: k_7 is 1 or 2, and k_7 = 1 iff some cycle that contains 111 has gamma = m, i.e. is reachable in G1 from a cycle at resistance 2 from {0}; k* = k_7 | **[proved]** | section 5 |
| Theorem 4(c) | for n = 2^k with k odd, k >= 3 (n = 8, 32, 128, ...): k_7 = 1, hence k* = 1 | **[proved]** | section 5 |
| k* for k even | n = 16: k_7 = 2, k* = 2. n = 4: k = (0, 1, 1, 2, 1, 1, 2, 2), k* = 2 | **[computed for n = 4, 16]** (from the definitions, gamma by Chu-Liu/Edmonds for every root; for n = 16 also from Theorem 4(b) and the enumeration of the cycles with 111) | Table 3 |
| k* for k even, k >= 6 | whether a cycle with 111 is reachable from the domain cycles at n = 64, 256, ... | **[attempted (gap: no description of the cycles that contain 111; the bound on c that settles n = 16 fails for other even n, see n = 22 in Table 2)]** | section 7 |
| Theorem 5 (optional part) | for every even n >= 6 that is not a power of two: G1 has exactly one closed class K; it contains {0}, all cycles on one parity class and all domain cycles; every cycle outside K contains 111; K carries the codes 0, ..., 6 | **[proved]** | section 6 |
| Corollary 5 | for these n: S = K, gamma_min = m - 1, k_c = 0 for c <= 6, and k* = 0 iff a cycle that contains 111 lies in K | **[proved, given Theorem A]**; which n have such a cycle in K: **[computed for even n <= 22]** | section 6; Table 2 |
| odd n | not treated (c is not defined on an odd ring) | not attempted | section 7 |
| Lemmas 1 to 9 | | **[proved]**; each also tested at small n: Lemmas 1 to 8 and Theorem 1 exhaustively in Table 1; Lemma 9 in Table 2 (one-parity cycles in K) and by the executed chains of Table 4, Part D | section 3; Tables 1, 2, 4 |
| G1, closed classes, potentials and k_c computed directly | | **[computed for even n = 4..22]**; k_c from the definitions for n = 4, 8, 16; no disagreement with the study's data and with the exploration of P154 where both exist | Tables 2, 3, 5 |
| chains of flips constructed in the proofs, executed step by step | | **[computed]**: every cycle for even n = 4..20; samples for n = 32..1024 | Table 4 |

The goal of the task is reached: for n = 2^k every cycle of rule 26 has a directed G1 path to {0}, {0} is the only closed
class and S = {{0}}. The indices k_c are determined for c <= 6 for every n = 2^k >= 8, and k_7 (hence k*) for odd k; for
even k >= 6 the value of k_7 is open, and the gap is stated in section 7. No claim of novelty is made.

The route differs from the one of P154 (rule 154 permutes the states with ones on both parities; rule 26 does not). It uses
a quantity that cannot increase (c) and a description of the periodic states without 111 (domain states), as the proof for
classes 43 and 142 uses the number of walls. The cycles that contain 111 are not described; the path to {0} does not need
their description, because every state that is not a domain state has a one whose deletion lowers c.

## 1. Setting and notation

Ring Z/nZ, n even and n >= 4 unless said otherwise, states x in {0,1}^n, e_i the state with a single one at i, sums mod 2. Rule 26:
f = 1 exactly on the codes 001, 011, 100; (F x)_i = f(x_(i-1), x_i, x_(i+1)). Rules 26 and 90 differ on the code 110 only;
rules 26 and 154 differ on the code 111 only. Cycles, G1, V, gamma, S, D_c, R(C -> D_c), k_c, k* as in P154, Section 1; m is
the number of cycles. A path of resistance d is a sequence of F-steps and d single flips. If x and x + e_j are periodic and
lie on different cycles, both G1 edges exist ("a flip between periodic states").

E, O: the states with ones on even, respectively odd, cells only; M: the states with a one on an even cell and a one on an
odd cell. A cycle is *contained in E ∪ O* ("on one parity class") if each of its states lies in E or in O, i.e. if c = 0
on it (c is defined below); by Lemma 6 such a cycle other than {0} alternates between E and O.

V(C, C') = 1 iff C -> C' is an edge of G1: a path of resistance 1 from C follows C, makes one flip at a state F(x) with x
in C (again a state of C), and then follows F; conversely the orbit of x + e_j is such a path.

* **Moving frame.** sigma is the rotation (sigma x)_i = x_(i-1) and U = sigma F. U commutes with F and sigma^n = 1, so a
  state is periodic under F iff it is periodic under U. Statements
  about codes, about c and about the existence of flips are invariant under rotation, so they can be read in either frame.
* **c.** List the ones of x in cyclic order. c(x) is the number of cyclically consecutive pairs of ones whose positions have
  different parity (c = 0 if x has fewer than two ones). c is even, and c(x) = 0 iff x is in E or O.
* **Groups, sources.** For x in M the cyclic sequence of ones splits into c(x) maximal runs of ones of equal parity, the
  *groups*; consecutive groups have different parity. The first one of a group (in cyclic order) is its *source*. A group
  with a single one is a *singleton group*.
* **Domain states.** x in M is a *domain state* if any two cyclically consecutive sources are at distance at least 3 (the
  distance is odd). The cells from a source s up to the cell before the next source s' form a *domain* of odd length
  d = s' - s >= 3: the source s carries 1, the cells s + 1, s + 3, ..., s + d - 2 carry 0, and the cells
  s + 2, s + 4, ..., s + d - 1 (the *free cells*) carry the other ones of the group, in any combination. Conversely any
  choice of an even number of sources of alternating parity at distances >= 3 and of the values of the free cells is a
  domain state.
* **Carrier words.** Cyclic words over the blocks 11100 and 100 with at least one block 11100.

## 2. Statements

**Theorem 1 (periodic states, even n) [proved].** Let n >= 4 be even. c is constant on every cycle. A state x is periodic
iff one of the following holds: (i) x lies in E or O and is periodic under rule 90 (for n = 2^k: x = 0); (ii) x is a domain
state; (iii) x is periodic, lies in M, is not a domain state, and then the orbit of x contains the block 111. Every domain
state is periodic, F permutes the domain states, and no domain state contains 111.

**Theorem 2 (paths to the zero state) [proved].** Let n >= 4 be even and C a cycle not contained in E ∪ O. Then there is a
directed path in G1 from C to a cycle contained in E ∪ O; along the path c drops at most c(C)/2 times, each time by at
least 2 after the deletion of a singleton group, and the other steps are flips between periodic domain states. For n = 2^k the path ends at {0}.

**Theorem 3 (closed class and potentials, n = 2^k) [proved].** Let n = 2^k >= 4 and let m be the number of cycles.
(a) No single flip leaves {0}: V({0}, C) >= 2 for every other cycle C.
(b) {0} is the only closed class of G1.
(c) gamma({0}) = m - 1. For C != {0}: gamma(C) >= m, and gamma(C) = m iff C is reachable in G1 from a cycle C_1 with
    V({0}, C_1) = 2 (C = C_1 allowed). The noise-selected set is S = {{0}}.
(d) For n >= 8 every domain cycle has gamma = m.

**Theorem 4 (the indices k_c, n = 2^k >= 8) [proved].**
(a) k_0 = 0 and k_c = 1 for c = 1, ..., 6.
(b) k_7 is 1 or 2; k_7 = 1 iff some cycle that contains 111 has gamma = m. Hence k* = k_7.
(c) If k is odd (n = 2 mod 3), the carrier word 11100 (100)^((n-5)/3) lies on a cycle with gamma = m; so k_7 = 1 and k* = 1.

**Theorem 5 (even n that is not a power of two) [proved].** Let n >= 6 be even and not a power of two. G1 has exactly one
closed class K. K contains {0}, every cycle contained in E ∪ O, and every domain cycle. Every cycle outside K contains
111. The states of the cycles of K contain the codes 0, ..., 6.

**Corollary 5 [proved, given Theorem A].** For these n: S = K, gamma_min = m - 1, k_c = 0 for c = 0, ..., 6, and k* = 0 iff
some cycle that contains 111 lies in K.

## 3. Lemmas

**Lemma 1 (moving frame) [proved].** For every n >= 3 and every state u,
U(u)(j) = f(u(j-2), u(j-1), u(j)) = u(j) + u(j-2) [1 + u(j-1) (1 + u(j))] (mod 2).
In words: the cell j changes only if u(j-2) = 1 (the cell j is *attacked*); an attack toggles u(j), except that it has no
effect when u(j-1) = 1 and u(j) = 0. In particular a 0 at j becomes 1 iff u(j-2) = 1 and u(j-1) = 0, and a 1 at j becomes 0
iff u(j-2) = 1.

*Proof.* U(u)(j) = (F u)(j-1) = f(u(j-2), u(j-1), u(j)). f(0, b, c) = c (codes 000, 001, 010, 011) and f(1, b, c) = 1 iff
b = c = 0 (codes 100, 101, 110, 111); the formula takes these eight values. []

**Lemma 2 (c does not increase) [proved].** Let n be even. Then c(F x) <= c(x) for every state x. Moreover a single flip
changes c by -2, 0 or 2, and deleting a one does not increase c.

*Proof.* c is invariant under rotation, so c(F x) = c(U x); write u = x and u' = U(u). For a one p of u let N(p) be the set
consisting of p if u'(p) = 1, and of p + 2 if u(p+1) = u(p+2) = 0 (then u'(p+2) = 1 by Lemma 1). Every one of u' lies in
some N(p): if u'(j) = 1 and u(j) = 1 then j is in N(j); if u(j) = 0, then u(j-2) = 1 and u(j-1) = 0 by Lemma 1, so j is in
N(j-2). If p + 2 is in N(p), the cells p + 1 and p + 2 carry no one of u, and u'(p+1) = 0 (a 0 at p + 1 would need u(p) = 0
to become 1). So the ones of u', in cyclic order, are obtained by listing the ones p of u in cyclic order and replacing each
p by the elements of N(p), which are 0, 1 or 2 cells of the parity of p. The cyclic sequence of parities of u' is therefore
obtained from that of u by deleting letters and doubling letters. Doubling a letter does not change the number of cyclic
changes, and deleting a letter does not increase it. The same two facts give the statement on flips: deleting a one deletes
a letter; adding a one inserts a letter, which changes the number of cyclic changes by 0 or 2. []

**Lemma 3 (domain states) [proved].** Let n be even.
(a) A state x in M is a domain state iff it contains no pair of adjacent ones at (j, j+1) such that the one preceding j in
    cyclic order (possibly the cell j + 1 itself, if x has only these two ones) is at odd distance from j.
(b) Let u be a domain state. Then U(u) is a domain state with the same sources, and in each domain with source s and free
    cells c_k = u(s + 2k), k = 1, ..., (d-1)/2, c_0 = 1: U(u)(s + 2k) = c_k + c_(k-1).
(c) U, and hence F, permutes the set of domain states with a given set of sources; every domain state is periodic. A domain
    state contains no 111. Flipping a free cell of a domain state gives a domain state with the same sources.

*Proof.* (a) Consecutive sources s, s' have different parity. Their distance is 1 iff the group of s is {s} and s' = s + 1,
i.e. iff s and s + 1 carry ones and the one preceding s has the other parity than s. Conversely if j and j + 1 carry ones
and the one preceding j is at odd distance, j is a source, j + 1 is the next source, and their distance is 1.
(b) Let s, s' be consecutive sources, d = s' - s. Cells s + 2k, k >= 1: the attacker is s + 2k - 2 with value c_(k-1) and
the cell in between, s + 2k - 1, carries 0; by Lemma 1 the cell is toggled iff c_(k-1) = 1. Cells s + 2k + 1 with k >= 1:
the attacker s + 2k - 1 carries 0, so the cell keeps its 0. The cell s + 1: its attacker is s - 1 and the cell in between is
the source s, which carries 1; the target carries 0, so the attack has no effect. The source s': its attacker s' - 2 is the
cell s + d - 2 of the domain of s, which carries 0 (here d >= 3 is used); so s' keeps its 1. Hence U(u) has the same ones at
the sources, zeros at the odd offsets, and the stated values at the free cells; its sources are the same.
(c) By (b), U acts on the free cells of each domain by c -> c + (shift of c) + (constant), an invertible affine map of
GF(2)^((d-1)/2) (the shift is nilpotent). So U is a bijection of the finite set of domain states with given sources, and
every such state is U-periodic, hence F-periodic. In a domain state two adjacent ones occur only as a free cell followed by
the next source, and then the cell after the source carries 0. The last statement is the definition. []

**Lemma 4 (ancestors of 111) [proved].** Let n be even, r >= 0, and let u be a state with u(j) = u(j+1) = 1 whose one
preceding j in cyclic order is at distance 2r + 1 from j. Then U^r(u) carries 111 on the cells j - 1, j, j + 1. Hence the
F-orbit of every state of M that is not a domain state contains 111 after at most n/2 - 1 steps.

*Proof.* Induction on r; r = 0 is the hypothesis. Let r >= 1 and p = j - 2r - 1, so u(p) = 1, the cells p + 1, ..., j - 1
carry 0, and u(j) = u(j+1) = 1 (the cells p and j + 1 may coincide). By Lemma 1: the cell p + 2 is attacked by p with a 0
in between and becomes 1 (if r = 1 this is the cell j - 1); the cell p + 1 carries 0 and has the one p between it and its
attacker, so it stays 0; the cells p + 3, ..., j - 1 have attackers that carry 0 and stay 0; the cells j and j + 1 have the
attackers j - 2 and j - 1, which carry 0, and stay 1. So U(u) has ones at j and j + 1 and the one preceding j is p + 2, at
distance 2(r - 1) + 1. The last statement follows from Lemma 3(a), 2r + 1 <= n - 1, and the invariance of the block 111
under rotation. []

**Lemma 5 (singleton groups) [proved].** Let n be even. (a) Every state of M that is not a domain state has a singleton
group. (b) If {j} is a singleton group of x, then c(x + e_j) = c(x) - 2.

*Proof.* (a) By Lemma 3(a) there are adjacent ones at (j, j+1) with the one preceding j at odd distance; both neighbours of
j in the cyclic sequence of ones have the other parity. (b) The two neighbours of j in the sequence have the same parity,
so deleting j removes two changes (if x has only two ones, c drops from 2 to 0). []

**Lemma 6 (one parity class) [proved].** Let n be even. For x in E or O, F(x) is the image of x under rule 90,
(F x)_i = x_(i-1) + x_(i+1), and F maps E into O and O into E. If n = 2^k, then F^(n/2)(x) = 0 for every x in E or O; in
particular 0 is the only periodic state in E or O, every cycle other than {0} lies in M, and the orbit of a single flip of
0 returns to 0.

*Proof.* A state on one parity class has no two adjacent ones, so the code 110 does not occur. Rule 90 is linear,
L = sigma + sigma^(-1), and L^(n/2) = sigma^(n/2) + sigma^(-n/2) = 0 for n/2 a power of two (as in P154, Lemma 3). A periodic state other than 0 cannot lie in E or O, because its
orbit would reach 0. []

**Lemma 7 (carrier words) [proved].** For every cyclic word w over the blocks 11100 and 100 (n = 5p + 3q), F^2(w) = sigma w.
Hence w is periodic with period dividing 2n, and if p >= 1 every second state of its cycle contains 111.

*Proof.* The cell before a block is the last cell of a block, a 0; the cell after a block is the first cell of a block, a
1. So F(w) is obtained block by block: 11100 -> f(011), f(111), f(110), f(100), f(001) = 10011 and 100 -> f(010), f(100),
f(001) = 011. In F(w) the cell before an image block is a 1 (both image blocks end in 1) and the cell after it is some a.
10011 -> f(1,1,0), f(1,0,0), f(0,0,1), f(0,1,1), f(1,1,a) = 01110 and 011 -> f(1,0,1), f(0,1,1), f(1,1,a) = 010. These are
the blocks 11100 and 100 shifted by one cell, the cell before each block of w being 0. []

**Lemma 8 (codes 011 and 110) [proved].** Let n be even. Every domain cycle contains the codes 001, 010, 011, 100, 101,
110. For n = 2^k every cycle other than {0} contains the codes 011 and 110.

*Proof.* Work in the moving frame (codes are invariant under rotation). In a domain with source s, length d and free cells
c_1, ..., c_r (r = (d-1)/2 >= 1), c_1 is toggled at every step (Lemma 3(b), c_0 = 1), and if c_(k-1) = 1 at some time then
c_k changes at that time; so every c_k takes both values along the cycle. When c_1 = 1, the cells s, s+1, s+2 carry 1 0 1
(code 101 at s + 1). When c_1 = 0 they carry 1 0 0 (code 100 at s + 1). When c_r = 1, the cells s + d - 2, ..., s + d + 1
carry 0 1 1 0 (an odd offset, the last free cell, the next source, an odd offset): codes 011 and 110. When c_r = 0, the
cells s + d - 2, ..., s + d + 1 carry 0 0 1 0: code 001 at the last free cell and code 010 at the next source.
For n = 2^k a cycle other than {0} lies in M (Lemma 6) and is a domain cycle or contains 111 (Theorem 1); in the second
case a maximal run of at least two ones, which is not the whole ring (1^n is not periodic: F(1^n) = 0), starts with 011
and ends with 110. []

**Lemma 9 (cycles on one parity class) [proved].** Let n be even. The cycles contained in E ∪ O (including {0}) lie in one
strongly connected component of G1.

*Proof.* F^2 maps E into E and is linear there (Lemma 6). Let P be the set of periodic states in E, a linear subspace, and
let T be an even number that is a multiple of the period of every state of P and at least the length of every transient in
E. Then pi = F^T restricted to E is a linear map of E onto P that is the identity on P. For x in P and an even cell j, the
orbit of x + e_j contains F^T(x + e_j) = x + pi(e_j), a state of P; so the cycle of x + pi(e_j) is equal to the cycle of x
or is its G1 successor. The e_j with j even span E, so the pi(e_j) span P, and any two states of P are joined by such steps.
Every cycle in E ∪ O contains a state of P (F maps O into E). []

## 4. Proofs of Theorems 1, 2, 3

*Theorem 1.* c does not increase along an orbit (Lemma 2), so it is constant on a cycle. Let x be periodic. If c(x) = 0, x
lies in E or O, where F is rule 90 (Lemma 6); for n = 2^k then x = 0. Otherwise the whole cycle lies in M (c is constant).
If every state of the cycle is a domain state we are in case (ii). If not, some state of the cycle is not a domain state,
and by Lemma 4 the cycle contains 111. The remaining statements are Lemma 3(c). []

*Theorem 2.* Induction on c(C) >= 2. Let x be a state of C.
Case 1: some state x of C has a singleton group {j}. Then c(x + e_j) = c(C) - 2 (Lemma 5), and the cycle C' on which the
orbit of x + e_j ends has c(C') <= c(C) - 2 (Lemma 2). So C' != C and C -> C' is an edge.
Case 2: no state of C has a singleton group. By Lemma 5(a) all states of C are domain states. Take x in C and a group with
source s and further ones j_1 < ... < j_r (r >= 1) in cyclic order. The states x, x + e_(j_r), x + e_(j_r) + e_(j_(r-1)),
... are domain states with the same sources (Lemma 3(c)), hence periodic; consecutive ones lie on the same cycle or on
cycles joined by an edge. The last one has the singleton group {s}, and Case 1 applies to its cycle.
In both cases C has a G1 path to a cycle with a smaller c, or (c = 2) to a cycle on which c = 0, which lies in E ∪ O. By
induction every cycle has a path to a cycle in E ∪ O; for n = 2^k that cycle is {0} (Lemma 6). []

*Theorem 3.* (a) A path of resistance 1 from {0} is 0, ..., 0, e_j, F(e_j), ...; by Lemma 6 it returns to 0.
(b) By Theorem 2 every cycle other than {0} has a path to {0}; by (a) {0} has no leaving edge.
(c) Every spanning in-tree has m - 1 edges of weight at least 1. The edges of Theorem 2 towards {0} contain an in-tree of
weight m - 1 rooted at {0}. An in-tree rooted at C != {0} contains an edge leaving {0}, of weight at least 2 by (a); so
gamma(C) >= m > gamma({0}), and S = {{0}}. If gamma(C) = m, the tree has the edge {0} -> C_1 of weight 2 and all other
edges of weight 1; the tree path from C_1 to C is a G1 path. Conversely let C_1 = D_0, D_1, ..., D_l = C be a G1 path without repeated cycles with
V({0}, C_1) = 2 ({0} is none of the D_i, because {0} has no leaving edge and C != {0}). Give {0} the edge to C_1, each D_i (i < l) the edge to D_(i+1), and every other cycle its first edge on a
shortest G1 path to {0}. Following these edges from any cycle leads to {0} or to some D_i and then to C; so this is an
in-tree rooted at C, of weight m.
(d) Let n >= 8 and let x be a domain state with sources s_1 < ... < s_2g (cyclic order). The state x_0 = e_(s_1) + e_(s_2)
is a domain state (its two sources are at the distances s_2 - s_1 >= 3 and n - (s_2 - s_1) >= 3), and the step 0 -> x_0 has
resistance 2; so its cycle C_1 has V({0}, C_1) = 2 by (a). Add the ones s_3, ..., s_2g in this order, then the remaining
ones of x in any order. After adding s_i the ones are s_1, ..., s_i. For even i these are i singleton groups, with source
distances s_2 - s_1, ..., s_i - s_(i-1) and n - (s_i - s_1), which is a sum of domain lengths of x; all are at least 3. For
odd i the ones s_i and s_1 form one group, the sources are s_2, ..., s_i, and their distances are again sums of domain
lengths of x. So every intermediate state is a domain state, hence periodic (Lemma 3), and the later additions change free
cells only. Consecutive states lie on equal or G1-adjacent cycles: the cycle of x is reachable from C_1, and gamma = m by
(c). []

## 5. The indices k_c for n = 2^k >= 8 (Theorem 4)

By Theorem 3, min gamma = m - 1 is attained at {0} only, and gamma(C) >= m otherwise. Hence for every code c

    k_c = min( R({0} -> D_c),  min over C != {0} of [gamma(C) - (m - 1) + R(C -> D_c)] ),

and the second term is at least 1.

(a) k_0 = 0, since 0 contains 000. For c != 0, R({0} -> D_c) >= 1, so k_c >= 1. The state e_0 contains 001, 010, 100, and
F(e_0) = e_(-1) + e_1 contains 101; both are reached from {0} with resistance 1: k_1 = k_2 = k_4 = k_5 = 1. For c = 3, 6
take the cycle C_1 of e_0 + e_3, a domain state (n >= 8) at resistance 2 from 0: gamma(C_1) = m by Theorem 3(c), and C_1
contains 011 and 110 (Lemma 8), so k_c <= m - (m - 1) + 0 = 1.

(b) R({0} -> D_7) = 2. A path of resistance at most 1 from {0} stays in E and O (Lemma 6), where no two ones are adjacent.
A path of resistance 2: 0, e_0 (one flip), F(e_0) = e_(-1) + e_1, then F^2(e_0) + e_1 = e_(-2) + e_1 + e_2 (one flip;
n >= 8), whose image contains 111 on the cells -1, 0, 1 (Lemma 4 with r = 1). So k_7 <= 2. For C != {0} the term
gamma(C) - (m - 1) + R(C -> D_7) equals 1 iff gamma(C) = m and C contains 111, and is at least 2 otherwise. So k_7 = 1 iff
such a cycle exists, and k_7 = 2 otherwise. With (a), k* = k_7.

(c) Let k be odd, k >= 3. Then n = 2 (mod 3), q = (n - 5)/3 is an odd integer >= 1, and y = 11100 (100)^q is a carrier word:
periodic and containing 111 (Lemma 7). x = y + e_1 = 10100 (100)^q is a domain state: its sources are the cells 0, 5, 8, ...,
n - 3 (q + 1 of them, alternating in parity, at the distances 5, 3, ..., 3), the free cells of the first domain carry 1, 0
and the free cell of every other domain carries 0. So x is periodic, on a domain cycle C_x with gamma(C_x) = m
(Theorem 3(d)), and the flip of the cell 1 leads from x to y; C_x != C_y because C_y contains 111. So C_y is reachable from
C_x, gamma(C_y) = m by Theorem 3(c), and k_7 = 1 by (b). []

For k even nothing beyond (a), (b) is proved; see section 7. For n = 16, Table 3 gives k_7 = 2: the three cycles that
contain 111 are not reachable from the cycles at resistance 2 from {0}, and their potential, computed by the
Chu-Liu/Edmonds algorithm (as that of every other cycle), is m + 1 **[computed for n = 16]**. The report states k* = 2 at n = 16 (Section 5.3). For n = 4
the only cycle is {0} and k_c = R({0} -> D_c) **[computed for n = 4]** (Table 3).

## 6. Even n that is not a power of two (Theorem 5, Corollary 5)

*Proof of Theorem 5.* Let R90 be the set of cycles contained in E ∪ O. By Lemma 9, R90 lies in one strong component of
G1, and by Theorem 2 every cycle has a path into R90. Let K be the strong component of G1 that contains R90. K has no
leaving edge: if C is in K and C -> C' is an edge, then C' has a path into R90, hence into K, so C' is in the strong
component K. A closed class contains, with each of its cycles, every cycle reachable from it, hence a cycle of R90, hence
it meets K and equals K. So K is the only closed class.
*Domain cycles.* Write n = 2^(e+1) q with q >= 3 odd. Let x be a domain state. If x has more than two domains, take a group,
delete its ones other than the source one by one and then the source: all intermediate states are domain states (the
deletion of the source merges three domains into one of odd length at least 9), hence periodic. So we may assume that x has
two domains, of lengths L_1 + L_2 = n. The longer one has length L >= 2^(e+1) + 1 (if e = 0, L >= n/2 = q >= 3; if e >= 1,
n/2 is even, so L >= n/2 + 1 >= 3 * 2^e + 1). Let a be its source and b the other source. By flips of free cells (domain
states throughout) reach the state e_a + e_(a + 2^(e+1)) + e_b. Then y = e_a + e_(a + 2^(e+1)) lies on one parity class and
is periodic: on that class, with S the shift by two cells, F^2 = S^(-1) (1 + S)^2 and y = (1 + S^(2^e)) e_a = (1 + S)^(2^e)
e_a lies in the image of (1 + S)^(2^e), which is the set of periodic points of 1 + S on a ring of h = 2^e q cells: in
GF(2)[S]/(S^h - 1), S^h - 1 = (S^q - 1)^(2^e) and 1 + S divides S^q - 1 exactly once, so the kernels of (1 + S)^j stop
growing at j = 2^e, the space is the direct sum of the kernel and the image of (1 + S)^(2^e), and 1 + S is invertible on
the image. So y and y + e_b are periodic: the cycle of x is joined, by flips between periodic states, to
the cycle of y, which is in R90. Hence every domain cycle lies in K.
*Outside K.* A cycle outside K is not in R90 and is not a domain cycle; by Theorem 1 it contains 111.
*Codes.* {0} gives 000; a domain cycle (n >= 6: e_0 + e_3 is a domain state) gives 001, 010, 011, 100, 101, 110
(Lemma 8). []

*Proof of Corollary 5.* Theorem A gives S = K and gamma_min = m - 1 for a unique closed class; k_c = 0 iff a state of a
selected cycle contains c. []

Which even n have a cycle with 111 in K is **[computed for even n <= 22]** (Table 2): yes for n = 14, 20, 22; no for
n = 10, 18; there is no cycle with 111 for n = 6, 12. This agrees with what P154, Section 7.2, reports from enumeration,
and Theorem 5 proves, for even n that is not a power of two, the two statements that P154 lists there as computed: every
cycle without 111 belongs to the closed class, and the cycles outside it contain 111. (For n = 2^k the closed class is {0}
and the domain cycles lie outside it.)

## 7. Scope, and what is not shown

* **[attempted (gap: no description of the cycles that contain 111)] k_7 and k* for n = 2^k with k even, k >= 6.** By
  Theorem 4(b), k* = 2 iff no cycle that contains 111 is reachable from the cycles at resistance 2 from {0}. For n = 16 this
  holds, and the reason visible in Table 2 is: the cycles with 111 have c = 8, the domain cycles have c <= 4, and a G1 edge
  raises c by at most 2 (Lemma 2). The same argument would give k* = 2 for every even k if every cycle with 111 on a ring of
  n = 4^j cells had c >= (n + 8)/3. Carrier words satisfy this (c = (n + 4p)/3 with p >= 2 blocks 11100 when n = 1 mod 3),
  but they are not the only cycles with 111: for n = 16 one of the three cycles with 111 does not pass through a carrier
  word, and for n = 22 there is a cycle with 111 and c = 6 < n/3 (Table 2). So a lower bound on c for the cycles with 111
  at n = 2^k is not available, and for n = 64, 256, ... the value of k* (1 or 2) is not determined. What is proved about
  such cycles: c is constant on them; every state of such a cycle lies in M and is not a domain state (Lemma 3(c), Lemma 6 for
  n = 2^k), so it contains a pattern of Lemma 4 (Lemma 3(a)) and has a singleton group (Lemma 5); in one step 111 arises
  only from 10011 (Lemma Q1 of P154). It is not shown how an occurrence of 111 is related to patterns at earlier times.
* **Odd n** is not treated: on an odd ring the parity of a cell is not defined, and c has no meaning. For odd n only
  Proposition V26 of the report is known (0 can be left by one flip).
* **G1 distance to {0}.** Theorem 2 gives a path with at most c(C)/2 drops of c; the number of G1 edges between two drops is not
  bounded here. Computed maximum distance to {0}: Table 2.
* **Theorem A** is used only in Corollary 5. Theorems 2, 3, 4 do not use it.
* **No computer-assisted step** in the proofs. The computations of section 8 are tests of the lemmas, an independent
  direct computation of G1, V, gamma and k_c, and executions of the constructed chains.
* **Tests that were corrected.** The first version of the test of Lemma 3(a) did not treat the case of a state with exactly
  two ones, which are adjacent (the preceding one is then the other one of the pair); the statement of Lemma 3(a) and the
  test were completed before the results of Table 1 were produced.
* **Reading.** One adversarial second reading was made inside the session that wrote the proofs, by a reader that did not
  open the author's scripts and re-tested every statement with separate code for even n <= 16, including V, gamma (every
  root) and k_c from the definitions at n = 4, 8, 16 and the closed classes at n = 6, 10, 12, 14. It found no false
  statement and no broken step, and six points of wording, which are corrected (among them: "contained in E ∪ O" instead of
  "in E or O" for cycles, the restriction of the last sentence of section 6 to n that are not powers of two, and two cited
  steps of the proof of Theorem 5 that are now written out). That reader could not open the report, P154 or
  `PROOF_94_converse.md`, and did not recompute the tables beyond n = 16. No reader outside the session has checked the
  proofs.
* **Literature (short search, two queries, 17 November 2026).** Found: Aguiar and Severino, "Two elementary cellular
  automata with a new kind of dynamic", Complex Systems 24(2), study rules 26 and 154 on finite rings and with fixed
  boundaries and note that the two rules differ in the response to 111 only (abstract and search excerpt read; the paper was
  not read); Li and Packard, "The structure of the elementary cellular automata rule space", list rules 26, 73, 154 as
  locally chaotic (search excerpt only). The reduction of rule 26 to rule 90 on one parity class is the report's
  Proposition R154, with the sources named there. No source was found for the quantity c, for the domain states, or for
  the path to {0}; the search was short, and no claim of novelty is made for any statement.

## 8. Computations (verbatim copy of `out/tables_26.md`)

### Table 1. Exhaustive tests of the lemmas (`check_lemmas_26.py` -> `out/check_lemmas_26.json`)

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| M1 | Lemma 1 (moving frame): sigma F (u)(j) = u(j) + u(j-2)[1 + u(j-1)(1 + u(j))]; every state | 4..14 | 32752 | 0 |
| M2 | Lemma 2 (c does not increase): c(F x) <= c(x); every state | 4..20 (even) | 1398096 | 0 |
| M2f | Lemma 2, remark: one flip changes c by -2, 0 or 2, and deleting a one does not raise c; every state, every cell | 4..16 (even) | 1339840 | 0 |
| M3 | Lemma 3 (domain states): the description by sources equals "ones on both parities and no pattern 1 0^(2r) 1 1"; in the moving frame the sources stay, the free cells follow c_k -> c_k + c_(k-1), the other cells stay 0; F permutes the domain states; every state | 4..18 (even) | 349520 | 0 |
| M4 | Lemma 4: if u(j) = u(j+1) = 1 and the preceding one is at distance 2r+1 from j, then after r steps the cells j-1, j, j+1 of the moving frame carry 111; every state, every such pattern | 4..16 (even) | 223330 | 0 |
| M5 | Theorem 1 (periodic states, even n): c is constant on a cycle; a periodic state is 0, or lies on one parity class, or is a domain state, or its orbit contains 111; domain states are periodic; for n = 4, 8, 16 no periodic state other than 0 lies on one parity class; every periodic state | 4..18 (even) | 41267 | 0 |
| M6 | Lemma 5: every state with ones on both parities that is not a domain state has a singleton group, and deleting a singleton group lowers c by 2; every such state | 4..16 (even) | 73843 | 0 |
| M7 | Lemma 7 (carrier words): F^2(w) is w shifted by one cell for every cyclic word over the blocks 11100 and 100 that contains 11100; every such word, every rotation | 5..31 | 1444 | 0 |
| M8 | Lemma 6: on one parity class rule 26 is rule 90 and maps E into O and O into E (every state of E and O, even n = 4..16); F^(n/2) = 0 there for n = 2^k (every state of E and O for n = 4, 8, 16; the two single seeds for n = 32..1024) | 4..16 (even); 32..1024 (powers of two) | 1580 | 0 |
| M9 | Lemma 8: every domain cycle contains the codes 001, 010, 011, 100, 101, 110; for n = 8, 16 every cycle other than {0} contains 011 and 110; every such cycle | 6..18 (even) | 1219 | 0 |

All tests passed: True. CPU time 6.42 s.

Numbers of domain states (test M3), by n: 4: 0, 6: 12, 8: 64, 10: 240, 12: 816, 14: 2688, 16: 8704, 18: 27840.

Periodic states by kind (test M5), n: zero / on one parity class / domain states / orbit with 111: 4: 1 / 0 / 0 / 0; 6: 1 / 6 / 12 / 0; 8: 1 / 0 / 64 / 16; 10: 1 / 30 / 240 / 5; 12: 1 / 30 / 816 / 0; 14: 1 / 126 / 2688 / 56; 16: 1 / 0 / 8704 / 80; 18: 1 / 510 / 27840 / 36.

### Table 2. G1 and its closed classes computed directly, even n (`g1_26.py` -> `out/g1_26.jsonl`)

| n | 2^k | cycles | periodic states | G1 edges | closed classes (sizes) | {0} in the closed class | cycles on one parity class (not {0}) | domain cycles | cycles with 111 | one-parity cycles in K | domain cycles in K | cycles with 111 in K | codes on K | c of the domain cycles | c of the cycles with 111 | cycles with 111 through a carrier word | largest increase of c along a G1 edge | cycles with a G1 path to {0} | max G1 distance to {0} | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | yes | 1 | 1 | 0 | 1 [1] | True | 0 | 0 | 0 | 0 of 0 | 0 of 0 | 0 of 0 | [0] | - | - | 0 | None | 1 of 1 | 0 | 0.0 | 54 |
| 6 | no | 7 | 19 | 33 | 1 [7] | True | 3 | 3 | 0 | 3 of 3 | 3 of 3 | 0 of 0 | [0, 1, 2, 3, 4, 5, 6] | [2] | - | 0 | 2 | 7 of 7 | 2 | 0.0 | 54 |
| 8 | yes | 10 | 81 | 73 | 1 [1] | True | 0 | 8 | 1 | 0 of 0 | 0 of 8 | 0 of 1 | [0] | [2] | [4] | 1 | 2 | 10 of 10 | 1 | 0.01 | 54 |
| 10 | no | 19 | 276 | 259 | 1 [18] | True | 5 | 12 | 1 | 5 of 5 | 12 of 12 | 0 of 1 | [0, 1, 2, 3, 4, 5, 6] | [2] | [6] | 1 | 2 | 19 of 19 | 3 | 0.0 | 54 |
| 12 | no | 64 | 847 | 1665 | 1 [64] | True | 9 | 54 | 0 | 9 of 9 | 54 of 54 | 0 of 0 | [0, 1, 2, 3, 4, 5, 6] | [2, 4] | - | 0 | 2 | 64 of 64 | 3 | 0.01 | 54 |
| 14 | no | 76 | 2871 | 2493 | 1 [76] | True | 9 | 64 | 2 | 9 of 9 | 64 of 64 | 2 of 2 | [0, 1, 2, 3, 4, 5, 6, 7] | [2, 4] | [6] | 1 | 2 | 76 of 76 | 3 | 0.03 | 54 |
| 16 | yes | 552 | 8785 | 32240 | 1 [1] | True | 0 | 548 | 3 | 0 of 0 | 0 of 548 | 0 of 3 | [0] | [2, 4] | [8] | 2 | 2 | 552 of 552 | 3 | 245.24 | 192 |
| 18 | no | 567 | 28387 | 33364 | 1 [566] | True | 39 | 526 | 1 | 39 of 39 | 526 of 526 | 0 of 1 | [0, 1, 2, 3, 4, 5, 6] | [2, 4, 6] | [10] | 1 | 2 | 567 of 567 | 4 | 0.38 | 193 |
| 20 | no | 2816 | 88956 | 191625 | 1 [2815] | True | 45 | 2766 | 4 | 45 of 45 | 2766 of 2766 | 3 of 4 | [0, 1, 2, 3, 4, 5, 6, 7] | [2, 4, 6] | [8, 12] | 2 | 2 | 2816 of 2816 | 5 | 1.37 | 231 |
| 22 | no | 3695 | 281315 | 292094 | 1 [3684] | True | 33 | 3648 | 13 | 33 of 33 | 3648 of 3648 | 2 of 13 | [0, 1, 2, 3, 4, 5, 6, 7] | [2, 4, 6] | [6, 10] | 3 | 2 | 3695 of 3695 | 5 | 4.68 | 407 |

K denotes the closed class that contains {0} (the only closed class in every row). For n = 4, 8, 16, K = {0}.

### Table 3. n = 4, 8, 16: resistances, potentials and k_c from the definitions (`g1_26.py`)

| n | m | V({0}, C): value: number of cycles | cycles with V({0}, C) = 2 (T2) | cycles reachable from T2 in G1 | domain cycles reachable from T2 | cycles with 111 reachable from T2 | gamma({0}) | gamma by kind of cycle (roots computed by Edmonds) | gamma agrees with Theorem 3 | G1 edges = pairs with V = 1 | R({0} -> D_c), c = 0..7 | k_c, c = 0..7 | k* | how gamma was obtained |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 | {'0': 1} | 0 | 0 | 0 of 0 | 0 of 0 | 0 | {'zero': [0]} | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | [0, 1, 1, 2, 1, 1, 2, 2] | 2 | Edmonds, all roots |
| 8 | 10 | {'0': 1, '2': 8, '3': 1} | 8 | 10 | 8 of 8 | 1 of 1 | 9 | {'domain': [10], 'with_111': [10], 'zero': [9]} | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | [0, 1, 1, 1, 1, 1, 1, 1] | 1 | Edmonds, all roots |
| 16 | 552 | {'0': 1, '2': 88, '3': 392, '4': 68, '5': 3} | 88 | 549 | 548 of 548 | 0 of 3 | 551 | {'domain': [552], 'with_111': [553], 'zero': [551]} | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | [0, 1, 1, 1, 1, 1, 1, 2] | 2 | Edmonds, all roots |

### Table 4. The chains of the proofs, executed step by step (`chains_26.py` -> `out/chains_26.json`)

Part A: every cycle, chain of Theorem 2 down to a cycle on one parity class.

| n | cycles | all chains end on one parity class | chains ending at {0} | max flips | max number of drops of c |
|---|---|---|---|---|---|
| 4 | 1 | True | 1 | 0 | 0 |
| 6 | 7 | True | 1 | 1 | 1 |
| 8 | 10 | True | 10 | 2 | 2 |
| 10 | 19 | True | 1 | 2 | 2 |
| 12 | 64 | True | 1 | 3 | 2 |
| 14 | 76 | True | 1 | 4 | 3 |
| 16 | 552 | True | 552 | 4 | 3 |
| 18 | 567 | True | 1 | 5 | 4 |
| 20 | 2816 | True | 1 | 7 | 5 |

Part B: cycles reached from random states, n = 2^k, chain of Theorem 2 to {0}.

| n | start states | all chains end at {0} | max c of the start cycle | max flips | max number of drops of c |
|---|---|---|---|---|---|
| 32 | 100 | True | 10 | 9 | 5 |
| 64 | 100 | True | 16 | 20 | 8 |
| 128 | 50 | True | 30 | 39 | 15 |
| 256 | 50 | True | 58 | 79 | 29 |
| 512 | 20 | True | 112 | 160 | 56 |
| 1024 | 10 | True | 218 | 302 | 109 |

Part C: chain of Theorem 4(c): 0, e_0 + e_5 (resistance 2), then single flips between periodic domain states up to 10100 (100)^q, then one flip to the carrier word 11100 (100)^q.

| n | q | flips between domain states after e_0 + e_5 | all intermediate states periodic domain states | last flip gives the carrier word, periodic, with 111 | period of the carrier cycle | c of the last domain state | c of the carrier |
|---|---|---|---|---|---|---|---|
| 8 | 1 | 2 | True | True | 16 | 2 | 4 |
| 32 | 9 | 10 | True | True | 64 | 10 | 12 |
| 128 | 41 | 42 | True | True | 256 | 42 | 44 |
| 512 | 169 | 170 | True | True | 1024 | 170 | 172 |

Part D: even n that are not powers of two. Every cycle on one parity class is joined to {0} in both directions (Lemma 9), and every domain cycle is joined to a cycle on one parity class by flips between periodic states (Theorem 5).

| n | one-parity cycles joined to {0} both ways | domain cycles joined to a one-parity cycle |
|---|---|---|
| 6 | 3 | 3 |
| 10 | 5 | 12 |
| 12 | 9 | 54 |
| 14 | 9 | 64 |
| 18 | 39 | 526 |
| 20 | 45 | 2766 |

Part E: Theorem 3(d). From e_(s1) + e_(s2) (resistance 2 from 0; s1, s2 two consecutive sources) to a given domain state by single flips; every intermediate state is asserted to be a periodic domain state.

| n | target domain states | which | all intermediate states periodic domain states | max flips |
|---|---|---|---|---|
| 8 | 8 | every domain cycle | True | 2 |
| 16 | 548 | every domain cycle | True | 6 |
| 32 | 200 | cycles reached from random states | True | 15 |
| 64 | 200 | cycles reached from random states | True | 30 |

Part F: Theorem 4(b). The path 0, e_0, F(e_0), F^2(e_0) + e_1, whose next state contains 111, and the orbit of a single flip of 0 (no two adjacent ones, returns to 0): executed for n = 8, 16, 32, 64, 128, 256, 512, 1024; all as stated: True.

CPU time of `chains_26.py`: 36.61 s.

### Table 5. Comparison with data already in the repository (`crosscheck_data.py` -> `out/crosscheck_data.json`)

| compared with | ring sizes n | fields compared | disagreements |
|---|---|---|---|
| data/ring_size/mechanisms.csv | 8, 10, 12, 14, 16, 18, 20, 22 | cycles; selected cycles = size of the closed class; gamma_min = m - 1; k_c and k* (n = 8, 16: all values; other n: the codes with k_c = 0 are the codes on the closed class) | 0 |
| verify_ring_size/part2_154/out/explore_122_26.jsonl | 4, 6, 8, 10, 12, 14, 16, 18, 20, 22 | closed-class sizes; cycles; cycles that contain 111 (where recorded) | 0 |

k_c of the study and of this folder at the powers of two in the study: n = 8: study [0, 1, 1, 1, 1, 1, 1, 1], here [0, 1, 1, 1, 1, 1, 1, 1]; n = 16: study [0, 1, 1, 1, 1, 1, 1, 2], here [0, 1, 1, 1, 1, 1, 1, 2].

Notes on the tables.

* Table 2 is independent of the proofs: all 2^n states are tabulated, the periodic states and the cycle every state falls
  to are determined, all single flips of all periodic states are followed, and strong components are computed. "Cycles with
  111 through a carrier word" counts the cycles with 111 that contain a cyclic word over 11100 and 100.
* Table 3: V and R are distances in the graph on the states with F-steps of cost 0 and flips of cost 1; gamma is computed
  for every root by an own implementation of the Chu-Liu/Edmonds algorithm (tested against networkx on random matrices
  during development; that comparison is not part of the scripts), and k_c then follows from the definition.
* Table 5: the study's records exist for n = 8..22. For n = 8 and n = 16 the vectors k_c are compared entry by entry; for
  the other n the study's codes with k_c = 0 are compared with the codes on the closed class (Corollary 5). The comparison
  reads the files of the repository and changes none.
* Table 4: every flip is applied to a periodic state, the flipped state is iterated until periodic, and the script asserts
  what the lemma predicts (a drop of c and a new cycle, or a periodic domain state).

## 9. Files (all under `proofs_94_26/`)

| file | content |
|---|---|
| `PROOF_26.md` | this document |
| `ring.py`, `r26.py` | tools (NumPy, own code): F on all states, cycles, G1; c, groups, domain states, carrier words |
| `check_lemmas_26.py`, `out/check_lemmas_26.json` | exhaustive tests of Lemmas 1 to 8 and of Theorem 1 |
| `g1_26.py`, `out/g1_26.jsonl` | G1 and closed classes for even n; V, gamma, k_c from the definitions for n = 4, 8, 16 |
| `chains_26.py`, `out/chains_26.json` | execution of the chains of Theorems 2, 3(d), 4(b), 4(c), 5 and Lemma 9 |
| `crosscheck_data.py`, `out/crosscheck_data.json` | comparison with `data/ring_size/mechanisms.csv` and `verify_ring_size/part2_154/out/explore_122_26.jsonl` (read only) |
| `make_tables.py`, `out/tables_26.md` | tables of section 8 |
| `test_proofs_94_26.py` | tests of the folder (both documents) |

To reproduce (repository root; Python with NumPy and SciPy; one process; about 6 minutes of CPU time, of which 4 for the potentials at n = 16; peak memory about
0.4 GB at n = 22):

    python proofs_94_26/check_lemmas_26.py
    python proofs_94_26/g1_26.py 4 6 8 10 12 14 16 18 20 22
    python proofs_94_26/chains_26.py
    python proofs_94_26/crosscheck_data.py      (after the rule 94 scripts of PROOF_94_converse.md, section 8)
    python proofs_94_26/make_tables.py
