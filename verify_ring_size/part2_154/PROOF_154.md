# Rule 154 on rings of n = 2^k cells: every cycle reaches the zero state by one-flip steps

Part 2 of the ring-size verification (new proof; reported separately from the checking of the study).
Folder: `verify_ring_size/part2_154/`. All numbers below are taken from files written in this folder
(`out/`); the tables are copied from `out/tables.md`, which `make_tables.py` generates from the other outputs.

Tags used: **[proved]**, **[proved (computer-assisted: script, output)]**, **[attempted (gap: ...)]**,
**[computed for n = ...]**. No claim of novelty is made for any statement.

## 0. Result

**Status: proved for all n = 2^k, k >= 2.** For rule 154 on a ring of n = 2^k >= 4 cells, every cycle has a
directed path in the one-flip graph G1 to the fixed point 0, of length at most n/2; {0} is the only closed class
of G1; the stochastic potential is m - 1 at {0} and m at every other cycle (m = number of cycles), so the
noise-selected set is S = {0}, and k* = 1 (Theorem 1). The proof is elementary and uses no computation.

The key step, which is not in the study, is a description of all periodic states: on every even ring, rule 154
permutes the set M of states that have a one on an even site and a one on an odd site (Lemma 6). So every state
of M is periodic, a single flip that stays in M moves between cycles without any transient, and the one-flip
graph on the cycles in M is the cube graph on M with each cycle contracted to a point. The remaining states live
on one parity class, where rule 154 is rule 90 (Lemma 2), which is nilpotent exactly at n = 2^k (Lemma 3).

By-product (Theorem 2, proved): for every n >= 3 that is not a power of two, G1 is strongly connected, all cycles
are selected and k* = 0. Hence for rule 154: **k* = 1 if n is a power of two (n >= 4), k* = 0 otherwise**, for
all n >= 3. This covers n = 22, which neither the study nor the sealed sample computed.

Step 9 (rules 122 and 26, lower priority) is in Section 7: four lemmas on rule 122 are proved (in particular
{0, checkerboard} is a closed class of G1 at every n = 2^k - 2 >= 6); the selection of the checkerboard at the other
even n and the pattern of rule 26 are described in terms of closed classes from enumerations up to n = 26 and are
not proved.

## 1. Setting

Ring Z/nZ, n >= 3, states x in {0,1}^n, addition of states and of bits is mod 2. e_i is the state with a single
one at site i; sigma is the rotation, (sigma x)_i = x_(i-1). Rule 154: (F x)_i = f(x_(i-1), x_i, x_(i+1)) with
f(a,b,c) = bit (4a+2b+c) of 154. Resistance r(x,y) = H(F(x), y); V(C,C') = minimum total resistance of a path
x_0 in C, x_1, ..., x_T in C'; gamma(C) = minimum weight of a spanning in-tree on the cycles rooted at C with
weights V; S = set of cycles of minimum gamma; G1 has an edge C -> C' (C != C') iff V(C,C') = 1; a closed class
is a strongly connected component of G1 without outgoing edge. D_c = set of states containing code c,
R(C -> D_c) = minimum resistance of a path from C to D_c, k_c = min_C [gamma(C) + R(C -> D_c)] - min gamma,
k* = max_c k_c (conventions of `../SAMPLE.md`, Section 2). m always denotes the number of cycles.

For even n: E = {x : x_i = 0 for all odd i}, O = {x : x_i = 0 for all even i}, E ∩ O = {0},
M = {0,1}^n \ (E ∪ O) (the states with at least one 1 on an even site and at least one 1 on an odd site),
1_E and 1_O the states with ones exactly on the even, respectively odd, sites. |M| = (2^(n/2) - 1)^2.
|x|_E and |x|_O denote the numbers of ones of x on even and odd sites.

**Lemma 0 [proved].** For cycles C != C': V(C,C') >= 1, and V(C,C') = 1 iff there are x in C and a site i such
that the F-orbit of x + e_i enters C'.

*Proof.* A path of resistance 0 from C follows F and stays in C, so V >= 1. If the orbit of x + e_i enters C',
take y in C with F(y) = x (C is a cycle); the path y, x + e_i, F(x + e_i), ... has resistance 1. Conversely a path
of total resistance 1 has exactly one step s with x_(s+1) = F(x_s) + e_i and follows F otherwise; x_s = F^s(x_0)
is in C, so x := F(x_s) is in C, and the end point is F^(T-s-1)(x + e_i) in C'. ∎

## 2. Lemmas

**Lemma 1 [proved].** f(a,b,c) = c + a(1 + b) mod 2, i.e. (F x)_i = x_(i+1) + x_(i-1)(1 + x_i).

*Proof.* The eight codes: 000 -> 0, 001 -> 1, 010 -> 0, 011 -> 1, 100 -> 1, 101 -> 0, 110 -> 0, 111 -> 1, which are
the bits 0..7 of 154 = 10011010_2. ∎ (Also checked by `check_pair_graph.py` and `check_lemmas.py`.)

**Lemma 2 [proved].** Let n be even, n >= 4. If x is in E, then F(x) is in O and (F x)_i = x_(i-1) + x_(i+1) for
all i; the same holds with E and O exchanged. So on E ∪ O rule 154 coincides with rule 90, L = sigma + sigma^(-1),
and F^t(x) = L^t x for all t >= 0 and x in E ∪ O.

*Proof.* Let x be in E. For odd i, x_i = 0 and Lemma 1 gives (F x)_i = x_(i+1) + x_(i-1). For even i,
x_(i-1) = x_(i+1) = 0, so (F x)_i = 0 = x_(i-1) + x_(i+1). Hence F(x) = L x and F(x) is in O. The case x in O is
the same with the parities exchanged, and the last statement follows by induction on t. ∎

**Lemma 3 [proved].** (a) If n = 2^k, k >= 2, then F^(n/2)(x) = 0 for every x in E ∪ O. (b) If n is even and not a
power of two, then F^t(e_i) != 0 for all t >= 0 and all i.

*Proof.* By Lemma 2, F^t(x) = L^t x on E ∪ O. sigma generates a commutative algebra over GF(2), so
L^(2^j) = sigma^(2^j) + sigma^(-2^j). (a) For 2^j = n/2: L^(n/2) = sigma^(-n/2) (sigma^n + 1) = 0.
(b) Identify e_i with z^i in GF(2)[z]/(z^n + 1); then L^t e_0 = z^(-t) (1 + z)^(2t), which is 0 iff z^n + 1 divides
(1 + z)^(2t) in GF(2)[z]. Write n = 2^a q with q odd, q >= 3: z^n + 1 = (z^q + 1)^(2^a) and
z^q + 1 = (z + 1)(1 + z + ... + z^(q-1)); the second factor has the value q = 1 (mod 2) at z = 1, so it is not
divisible by z + 1, has degree q - 1 >= 2, and therefore has an irreducible factor different from z + 1, which
does not divide any power of 1 + z. By rotation the same holds for every e_i. ∎
(Part (a) and the single-seed case are the study's Proposition R154; they are re-proved here because the theorem
depends on them.)

**Lemma 4 [proved].** Let n be even, n >= 4. Then F(M) ⊆ M.

*Proof.* Let x be in M and suppose F(x) is in O, i.e. (F x)_i = 0 for every even i. By Lemma 1,
x_(i+1) = x_(i-1)(1 + x_i) for every even i; with j = i + 1: x_j = x_(j-2)(1 + x_(j-1)) <= x_(j-2) for every odd j.
The odd sites form one orbit of j -> j - 2 (n is even), so going once around gives x_j <= x_(j-2) <= ... <= x_j:
all odd sites carry the same value. Since x is in M, some odd site is 1, hence all are, and then
1 = 1 · (1 + x_(j-1)) for every odd j, i.e. all even sites are 0. This contradicts x in M. The case F(x) in E is
the same with the parities exchanged. ∎

**Lemma 5 (collisions) [proved].** Let n >= 3 and F(x) = F(x') with x != x'. Then n is even and one of the
following holds: x, x' are in E and x + x' = 1_E; or x, x' are in O and x + x' = 1_O; or {x, x'} = {1_E, 1_O}.
In particular F is a bijection when n is odd, and for even n two different states with the same image both lie in
E ∪ O.

*Proof.* Put d = x + x' != 0. By Lemma 1, (F x)_i = (F x')_i reads
(*) d_(i+1) = x_(i-1)(1 + x_i) + x'_(i-1)(1 + x'_i) for all i.
(i) If d_(i-1) = d_i = 0 then d_(i+1) = 0; hence if d had two cyclically consecutive zeros, d would be 0. So d
has no two consecutive zeros.
(ii) If d_(i-1) = 1 and d_i = 0, then x_i = x'_i =: b and (*) gives d_(i+1) = (1 + b)(x_(i-1) + x'_(i-1)) = 1 + b;
by (i) d_(i+1) = 1, so x_i = x'_i = 0.
(iii) If d_(i-1) = 0 and d_i = 1, then x_(i-1) = x'_(i-1) and (*) gives d_(i+1) = x_(i-1)(x_i + x'_i) = x_(i-1).
(iv) If d_(i-1) = d_i = 1, then x' = 1 + x at both sites and (*) gives
d_(i+1) = x_(i-1)(1 + x_i) + (1 + x_(i-1)) x_i = x_(i-1) + x_i.
*Case A: d_i = 0 for some i.* By (i), d_(i-1) = d_(i+1) = 1; by (ii), x_i = x'_i = 0; by (iii) applied to the
pair (i, i+1), d_(i+2) = x_i = 0. So the hypothesis of Case A holds again at i + 2, and by induction
d_(i+2s) = 0, x_(i+2s) = x'_(i+2s) = 0, d_(i+2s+1) = 1 for all s. If n were odd, the sites i + 2s would exhaust
the ring and d = 0; so n is even, x and x' vanish on the parity class of i and differ at every site of the
other class: both lie in E (or both in O) and x + x' = 1_E (or 1_O).
*Case B: d has no zero.* Then x' = 1 + x everywhere and (iv) gives x_(i-1) + x_i = 1 for all i: x alternates, so
n is even and {x, x'} = {1_E, 1_O}. ∎

The case analysis was re-done mechanically for all n at once: a pair (x, x') with F(x) = F(x') is a closed walk
of length n in a graph on the 16 local pairs (x_(i-1), x_i, x'_(i-1), x'_i); `check_pair_graph.py` lists the
off-diagonal nodes that lie on closed walks. There are 6 of them (out of 12), forming exactly the alternation
B -> A -> B of Case A and the two-node loop of Case B (`out/check_pair_graph.txt`, RESULT: PASS).

**Lemma 6 (periodic states) [proved].** Let n be even, n >= 4. F restricted to M is a permutation of M; every
state of M is periodic. The periodic states of F are the states of M and the periodic states of rule 90 in
E ∪ O. If n = 2^k (k >= 2), the periodic states are exactly M ∪ {0}, their number is (2^(n/2) - 1)^2 + 1, and the
cycles are {0} and the cycles contained in M.

*Proof.* F maps M into M (Lemma 4) and is injective on M (Lemma 5: two states with the same image lie in
E ∪ O). An injective self-map of a finite set is a permutation, so every x in M satisfies F^j(x) = x for some
j >= 1. E ∪ O is mapped into itself, where F = L (Lemma 2). For n = 2^k every state of E ∪ O reaches 0
(Lemma 3a), so 0 is the only periodic state outside M. A cycle that meets M stays in M (Lemma 4). ∎

**Lemma 7 (one-flip moves) [proved].** Let n be even, n >= 4, C a cycle contained in M, x in C, i a site and
y = x + e_i.
(a) If y is in M, then y lies on a cycle C_y ⊆ M, and either C_y = C or both C -> C_y and C_y -> C are edges of G1.
(b) If y is not in M, then y is in E ∪ O and the cycle reached from y lies in E ∪ O.
(c) Any two cycles contained in M are joined by a directed G1 path through cycles contained in M (in both
directions).

*Proof.* (a) y is periodic by Lemma 6, so the orbit of x + e_i is the cycle C_y; by Lemma 0 this is an edge
C -> C_y if C_y != C, and since x = y + e_i with y in C_y and x in C, also C_y -> C. (b) Lemma 2. (c) From any x
in M one reaches the all-ones state 1^n by setting the zeros of x to one, one at a time; all intermediate states
contain the ones of x and are in M. By (a) consecutive states lie on equal or G1-adjacent cycles, with edges in
both directions. So every cycle in M is joined in both directions to the cycle {1^n} (F(1^n) = 1^n). ∎

## 3. Theorem 1 (n = 2^k)

**Theorem 1 [proved].** Let n = 2^k, k >= 2, and let m be the number of cycles of rule 154 on the ring of n cells.
(a) The cycles are {0} and the cycles contained in M.
(b) {0} has no outgoing edge in G1 (V({0}, C) >= 2 for every other cycle C).
(c) Every cycle C != {0} has a directed path in G1 to {0}, of length at most
mu(C) := min over x in C of min(|x|_E, |x|_O) <= n/2.
(d) {0} is the only closed class of G1.
(e) gamma({0}) = m - 1 and gamma(C) = m for every cycle C != {0}; the noise-selected set is S = {{0}}.
(f) k_0 = 0 and k_c = 1 for c = 1, ..., 7; hence k* = 1.

*Proof.* (a) Lemma 6.

(b) A path of resistance 1 leaving {0} is 0, ..., 0, e_i, F(e_i), F^2(e_i), ... (Lemma 0). e_i lies in E ∪ O, so
by Lemmas 2 and 3a its orbit stays in E ∪ O and reaches 0 after at most n/2 steps; by (a) none of its states
is on a cycle other than {0}. So no one-flip path from {0} ends on another cycle.

(c) Choose x in C attaining mu = mu(C). x is in M, so mu >= 1. Assume |x|_O <= |x|_E (otherwise exchange the
parities) and let j_1, ..., j_mu be the odd sites carrying a one. Put x^(0) = x and
x^(s) = x^(s-1) + e_(j_s). For s < mu, x^(s) still has a one on an odd site and all even ones of x, so x^(s) is in
M and lies on a cycle C_s ⊆ M (Lemma 6), C_0 = C. For s < mu - 1, Lemma 7(a) applied to x^(s) and the site
j_(s+1) shows that C_(s+1) = C_s or C_s -> C_(s+1) is an edge of G1. Finally x^(mu) = x^(mu-1) + e_(j_mu) is in
E \ {0}, and its orbit ends in 0 (Lemma 3a); by Lemma 0 this is an edge C_(mu-1) -> {0}. After deleting
repetitions, C = C_0, C_1, ..., C_(mu-1), {0} is a directed path in G1 of length at most mu <= n/2.

(d) By (c) every strongly connected component other than {0} has an outgoing edge; by (b) {0} has none.

(e) Every spanning in-tree has m - 1 edges of weight >= 1 (Lemma 0). By (c) each cycle C != {0} has a G1 edge to a
cycle with smaller G1 distance to {0}; these m - 1 edges form an in-tree rooted at {0} of weight m - 1, so
gamma({0}) = m - 1. Let C != {0}. An in-tree rooted at C contains one edge leaving {0}, of weight >= 2 by (b),
so gamma(C) >= (m - 2) + 2 = m. Conversely, let C_* be the cycle of e_0 + e_1 (a state of M). The step
0 -> F(0) + e_0 + e_1 has resistance 2, so V({0}, C_*) <= 2; by Lemma 7(c) the m - 1 cycles in M have a spanning
in-tree rooted at C with all edges in G1 (weight m - 2); adding the edge {0} -> C_* gives an in-tree rooted at C
of weight m. Hence gamma(C) = m > gamma({0}).

(f) k_0 = 0 because {0} is selected and contains code 0. Let c != 0. For C = {0}: gamma = m - 1 and
R({0} -> D_c) >= 1, since 0 is not in D_c; for C != {0}: gamma(C) = m. So k_c >= 1. Upper bounds: e_0 contains the
codes 1, 2, 4 (at the sites -1, 0, 1), and F(e_0) = e_(-1) + e_1 (Lemma 2) contains code 5 at site 0 (n >= 4);
both are reached from {0} with resistance 1, so k_c <= 1 for c = 1, 2, 4, 5. The state e_0 + e_1 is in M, hence
on a cycle with gamma = m, and contains code 3 at site 0 and code 6 at site 1; the cycle {1^n} has gamma = m
and contains code 7. So k_c <= 1 for c = 3, 6, 7. ∎

Remarks. (1) Theorem A of the study (the selected set is a union of closed classes of G1) is not needed: (e)
computes gamma directly. With Theorem A, (b) and (c) alone give S = {{0}}. (2) (c) is the "reachability
statement" that the study leaves open for n = 2^k (its Section 5.3: "What is not proved is the reachability of 0
from every cycle at all n = 2^k"). (3) The study's observation that the G1 distance to {0} follows the mean
number of ones is consistent with the bound mu(C): the distance is at most the smaller of the two parity counts
of any state of the cycle.

## 4. Theorem 2 (all other n) — by-product

**Theorem 2 [proved].** Let n >= 3 not be a power of two. Then G1 is strongly connected, gamma(C) = m - 1 for
every cycle, all cycles are selected, and k* = 0.

*Proof.* *n odd.* F is a bijection (Lemma 5), every state is periodic, and a single flip of x in C gives a state
y on a cycle C_y; as in Lemma 7(a), C_y = C or C -> C_y and C_y -> C are edges. The cube graph is connected, so G1
is strongly connected.
*n even (n >= 6).* The cycles are those contained in M and those contained in E ∪ O (Lemma 6).
(1) The cycles in M are mutually reachable (Lemma 7(c)).
(2) Let C ⊆ E ∪ O be a cycle other than {0} and x in C, x != 0, say x in E. For an odd site j, y = x + e_j is in
M, hence on a cycle C_y ⊆ M; C -> C_y is an edge (Lemma 0), and so is C_y -> C because y + e_j = x lies on C.
(3) {0}: a single flip gives e_i, whose orbit stays in E ∪ O (Lemma 2) and never reaches 0 (Lemma 3b); it
ends on a cycle C_1 ⊆ E ∪ O, C_1 != {0}, so {0} -> C_1 is an edge, and C_1 reaches M by (2). In the other
direction y = 1_E + e_1 is in M, y + e_1 = 1_E and F(1_E) = L 1_E = 0, so C_y -> {0} is an edge.
By (1)-(3) G1 is strongly connected.
In both cases every root has a spanning in-tree of G1 edges, so gamma = m - 1 for all cycles and all are selected.
All eight codes occur on periodic states: code 0 on 0; code 7 on 1^n; codes 1, 3, 4, 6 on 0^(n-2)11 and codes
2, 5 on 0^(n-4)1011 (n >= 5; both states are in M for even n and periodic for odd n); for n = 3 the states 001
and 011 contain the codes 1, 2, 4 and 3, 5, 6. Hence k_c = 0 for all c. ∎

**Corollary [proved].** For rule 154 and every n >= 3: k* = 1 if n is a power of two (n >= 4), and k* = 0 otherwise.
The selected set is {0} in the first case and the set of all cycles in the second.

This agrees with every computed case: the sealed sample for n = 8..21 and the sealed solver for n = 4..7
(`out/cross_check.txt`; Section 5). It also settles n = 22, 24, ..., where no computation exists, and proves the
study's computed statement "at even n not a power of two all cycles form one strongly connected G1" for all n.

## 5. Tests of the lemmas and of the theorems [computed]

`check_lemmas.py` (own code, numpy only) tests for every n = 3..16, exhaustively over all 2^n states: Lemma 1;
Lemma 2 (F = rule 90 on E ∪ O, F(E) ⊆ O, F(O) ⊆ E); Lemma 3 (a: F^(n/2) = 0 on E ∪ O for n = 4, 8, 16; b: the single
seed is not attracted to 0 for n = 6, 10, 12, 14); Lemma 4; Lemma 5 (all colliding pairs enumerated and
classified; their number is 2^(n/2) + 1; bijectivity for odd n); Lemma 6 (injectivity on M, all of M periodic,
periodic set = M ∪ {0} and the count formula for n = 4, 8, 16); Lemma 7 / Theorem 1 on the graph G1 built from the
definition (flip every cell of every periodic state and follow F): symmetry of the edges between cycles in M,
connectivity inside M, out-degree of {0}, distances to {0}, the bound mu(C); Theorem 2 (strong connectivity).
Result (`out/check_lemmas.txt`): ALL LEMMA TESTS PASSED: True.

| n | periodic states | cycles | G1 edges | out-degree of {0} | every cycle reaches {0} | max G1 distance to {0} | G1 strongly connected | lemma tests run / failed |
|---|---|---|---|---|---|---|---|---|
| 3 | 8 | 3 | 4 | 1 | yes | 2 | yes | 2 / 0 |
| 4 | 10 | 4 | 8 | 0 | yes | 2 | no | 14 / 0 |
| 5 | 32 | 4 | 6 | 1 | yes | 3 | yes | 2 / 0 |
| 6 | 56 | 12 | 77 | 3 | yes | 3 | yes | 11 / 0 |
| 7 | 128 | 8 | 28 | 1 | yes | 4 | yes | 2 / 0 |
| 8 | 226 | 31 | 434 | 0 | yes | 4 | no | 14 / 0 |
| 9 | 512 | 18 | 152 | 1 | yes | 5 | yes | 2 / 0 |
| 10 | 992 | 62 | 1117 | 5 | yes | 5 | yes | 11 / 0 |
| 11 | 2048 | 50 | 884 | 1 | yes | 6 | yes | 2 / 0 |
| 12 | 4000 | 308 | 9824 | 6 | yes | 6 | yes | 11 / 0 |
| 13 | 8192 | 156 | 4190 | 1 | yes | 7 | yes | 2 / 0 |
| 14 | 16256 | 564 | 19149 | 7 | yes | 7 | yes | 11 / 0 |
| 15 | 32768 | 510 | 18098 | 1 | yes | 8 | yes | 2 / 0 |
| 16 | 65026 | 4081 | 221202 | 0 | yes | 8 | no | 14 / 0 |

For n = 2^k (`out/check_lemmas.jsonl`):

| n | size of M | (2^(n/2)-1)^2 | cycles in M | F^n = id on M | distance histogram (distance: cycles) | distance of the all-ones cycle | distance = min-parity bound for all cycles |
|---|---|---|---|---|---|---|---|
| 4 | 9 | 9 | 3 | yes | 0: 1, 1: 2, 2: 1 | 2 | yes |
| 8 | 225 | 225 | 30 | yes | 0: 1, 1: 16, 2: 11, 3: 2, 4: 1 | 4 | yes |
| 16 | 65025 | 65025 | 4080 | yes | 0: 1, 1: 480, 2: 1384, 3: 1344, 4: 666, 5: 176, 6: 27, 7: 2, 8: 1 | 8 | no |

`cross_check.py` compares with results obtained from the definitions without G1 (dense V, Edmonds for all roots):
the sealed sample `../out/sample.jsonl` for n = 8..21 and the sealed solver `../solve.py` run here for n = 4..7
(`out/solver_n4_7.jsonl`). Tested: numbers of cycles, of periodic states and of G1 edges (n <= 16); for n = 4, 8,
16: min gamma = m - 1, gamma histogram {m - 1: 1 cycle, m: m - 1 cycles}, selected set {0}, closed classes {0},
k = (0,1,1,1,1,1,1,1); for all other n = 5..21: all cycles selected, one closed class containing all cycles,
k* = 0. Result (`out/cross_check.txt`): ALL CROSS-CHECKS PASSED: True (18 values of n).

`sample_large_n.py` (not part of the proof) tests random states of M on rings that cannot be enumerated: F(x) in M,
periodicity (through F^n(x) = x, see O1 below) and the descent of Theorem 1(c) (every intermediate state periodic,
the last state reaches 0 within n/2 steps) (`out/sample_large_n.jsonl`):

| n | sampled states of M | F(x) in M | F^n(x) = x | descent: intermediate states tested / periodic | descents ending in 0 within n/2 steps |
|---|---|---|---|---|---|
| 32 | 2000 | 2000 | 2000 | 88 / 88 | 20 of 20 |
| 64 | 1000 | 1000 | 1000 | 220 / 220 | 20 of 20 |
| 128 | 300 | 300 | 300 | 517 / 517 | 20 of 20 |
| 256 | 100 | 100 | 100 | 890 / 890 | 20 of 20 |
| 512 | 30 | 30 | 30 | 3484 / 3484 | 20 of 20 |
| 1024 | 10 | 10 | 10 | 2913 / 2913 | 10 of 10 |

### Observations that are not proved

* **O1 [computed for n = 4, 8, 16 (all of M); sampled for n = 32..1024].** For n = 2^k, F^n(x) = x for every x in M,
  i.e. all cycle lengths divide n. Not needed for Theorem 1; no proof was found or attempted beyond a few minutes.
* **O2 [computed for n = 4, 8, 16].** The maximum G1 distance to {0} is n/2 and is attained by the cycle {1^n}
  (2, 4, 8). Theorem 1(c) proves only the upper bound. The bound mu(C) is the exact distance for every cycle at
  n = 4 and 8 and not for every cycle at n = 16 (table above).

## 6. Where the argument could have broken, and what remains open for rule 154

Nothing remains open for the stated goal: Theorem 1 holds for all k >= 2 with every step proved by hand
(k = 1, n = 2, is excluded because the neighbourhood degenerates). The step that carries the proof is Lemma 5;
it has a hand proof, an independent mechanical check valid for all n (`check_pair_graph.py`), and an exhaustive
test for n = 3..16. Open for rule 154: O1 and the lower bound in O2.

## 7. Step 9: rules 122 and 26 (lower priority)

Here Theorem A is used as given: S is a union of closed classes of G1, S is closed under G1 edges, and S equals
the closed class if it is unique. The enumerations below use `g1lib.py` and `explore_122_26.py` (own code: G1
from the definition, strongly connected components by scipy); for n <= 22 the numbers of cycles and the sizes of
the closed classes agree with the sealed sample (`../SAMPLE.md`). The cases n = 23..26 are beyond the study and
the sample and rest on this code alone; statements about S and k* for them use Theorem A and no computation of gamma.

### 7.1 Rule 122 on even rings: the checkerboard

Rule 122: f(a,b,c) = 1 iff (a or c) and not (a and b and c); it is reflection symmetric. Let n be even, n >= 4,
c_odd = 1_O, c_even = 1_E; CB = {c_odd, c_even} is a 2-cycle (code 010 -> 0, code 101 -> 1).
D_n := c_odd + e_0 (a checkerboard state with one zero set to one) and Omega_n := the cycle reached from D_n.
R_s denotes the rule-90 orbit of a single seed on Z: R_0 = indicator of 0, R_(s+1)(i) = R_s(i-1) + R_s(i+1);
R_s(i) = binomial(s, (s+i)/2) mod 2 for |i| <= s, i = s (mod 2), and 0 otherwise; R_s(-i) = R_s(i), R_s(±s) = 1,
R_s(0) = 0 for even s >= 2 (the central binomial coefficient is even), and R_s(i) = 1 for all admissible i when
s = 2^k - 1 (since (1 + z)^(2^k - 1) = (1 + z^(2^k))/(1 + z) = 1 + z + ... + z^(2^k - 1) over GF(2)).

**Lemma R1 [proved].** For even n >= 4 and 0 <= t <= n/2 - 1, F^t(e_0) has ones exactly at the sites
-t, -t+2, ..., t, and F^(n/2)(e_0) is a checkerboard state. Hence the only out-neighbour of {0} in G1 is CB.

*Proof.* Induction on t. Let x have ones exactly at -t, -t+2, ..., t (2t + 1 <= n - 1 sites in the window). A one
of x has two zero neighbours (code 010 -> 0). A zero strictly inside the window has two one neighbours
(101 -> 1). If t <= n/2 - 2, the sites t + 1 and -t - 1 are different, have the codes 100 and 001 (-> 1), and all
other sites have code 000; so F(x) has ones exactly at -t-1, ..., t+1. If t = n/2 - 1, the single site outside the
window is n/2 = t + 1 = -t - 1 (mod n) and has code 101 -> 1; F(x) has ones exactly on the sites of the parity of
t + 1. By rotation the same holds for every e_i, and by Lemma 0 these are all one-flip paths from {0}. ∎

**Lemma R2 [proved].** If x is a checkerboard state and x_p = 1, then F(x + e_p) = F(x). Hence the out-neighbours
of CB in G1 are exactly the rotations of Omega_n different from CB.

*Proof.* In x + e_p the site p has code 000 -> 0 = f(0,1,0) = F(x)_p; the sites p - 1 and p + 1 have the codes
100 and 001 -> 1 = f(1,0,1); nothing else changes. So flipping a one leads back to CB. The states obtained by
flipping a zero are c_odd + e_(2j) = sigma^(2j) D_n and c_even + e_(2j+1) = sigma^(2j+1) D_n, i.e. the n rotations
of D_n, and their limit cycles are the rotations of Omega_n. ∎

**Lemma R3 [proved].** Let n be even, n >= 4, 0 <= t <= n/2 - 1 and a = R_(t+1). With the sites written as
j in {-n/2 + 1, ..., n/2}:
F^t(D_n)_j = a(|j|) if |j| = t + 1 (mod 2) and |j| <= t + 1; = 1 if |j| = t + 1 (mod 2) and |j| >= t + 3;
= a(|j| + 1) if |j| = t (mod 2).
(In words: outside the window |j| <= t + 1 the checkerboard is undisturbed; inside, the rule-90 triangle appears
with every one doubled towards the centre.)

*Proof.* First on Z. Let X(t) be the configuration on Z defined by the right-hand side for all j in Z. X(0) has
ones at all odd j and at j = 0 (a = R_1), i.e. it is the infinite checkerboard with the zero at 0 set to one. We
show X(t+1) = F(X(t)); by symmetry of X(t) and of the rule it suffices to take j >= 0. Write a' = R_(t+2), so
a'(i) = a(i-1) + a(i+1), and note f(u,0,0) = u, f(0,0,u) = u, f(u,1,1) = 1 + u, f(1,1,u) = 1 + u, f(u,u,u) = 0,
f(u,0,u) = u, f(1,0,1) = 1, f(0,1,0) = 0.
- j = t (mod 2), 1 <= j <= t: the triple is (a(j-1), a(j+1), a(j+1)), with image a(j-1) + a(j+1) = a'(j), as
  required (j has the parity of (t+1) + 1 and j <= t + 2).
- j = t (mod 2), j = 0 (t even): the triple is (a(1), a(1), a(1)), image 0 = a'(0).
- j = t (mod 2), j >= t + 2: the neighbours have the parity of t + 1 and are >= t + 1, so both are 1 (a(t+1) = 1 or
  the checkerboard value); the centre is a(j+1) = 0; image f(1,0,1) = 1, as required (a'(t+2) = 1 for j = t + 2,
  and the checkerboard value 1 for j >= t + 4).
- j = t + 1 (mod 2), 1 <= j <= t + 1: the triple is (a(j), a(j), a(j+2)), image a(j) + a(j+2) = a'(j+1), as required.
- j = t + 1 (mod 2), j = 0 (t odd): the triple is (a(2), a(0), a(2)) with a(0) = R_(t+1)(0) = 0 (t + 1 even, >= 2);
  image a(2) = a(0) + a(2) = a'(1), as required.
- j = t + 1 (mod 2), j >= t + 3: the triple is (a(j), 1, a(j+2)) = (0, 1, 0), image 0 = a'(j+1), as required.
Now the ring. Claim: F^t(D_n)_j = X_j(t) for j in {-n/2+1, ..., n/2} and t <= n/2 - 1. It holds at t = 0. In the
step t -> t + 1 (t <= n/2 - 2) the ring and Z use the same neighbours except at the two ends: the site n/2 has the
ring neighbour -n/2 + 1 instead of n/2 + 1, and the site -n/2 + 1 has the ring neighbour n/2 instead of -n/2. The
second pair agrees by the symmetry X_(-j) = X_j. For the first we need X_(n/2+1)(t) = X_(n/2-1)(t): with
i = n/2 - 1 >= t + 1, if i = t + 1 (mod 2) both values are 1 (X_i = a(t+1) = 1 if i = t + 1, the checkerboard
value otherwise; i + 2 >= t + 3); if i = t (mod 2) then i >= t + 2 and both values are a(i+1) = a(i+3) = 0. ∎

**Lemma R4 [proved].** Let n = 2^k - 2, k >= 3 (n = 6, 14, 30, 62, ...). Then F^(n/2-1)(D_n) = 1^n and
F^(n/2)(D_n) = 0, so Omega_n = {0}. Consequently {0} -> CB and CB -> {0} are the only G1 edges leaving {0} and CB:
**{ {0}, CB } is a closed class of G1 with exactly two cycles.**

*Proof.* Lemma R3 with t = n/2 - 1: all |j| <= n/2 = t + 1 = 2^(k-1) - 1, and the values are a(|j|) or a(|j| + 1)
with a = R_(2^(k-1) - 1), which is 1 on all admissible arguments. So the state is 1^n, and f(1,1,1) = 0. The rest
is Lemmas R1 and R2. ∎

**Corollary R5 [proved, using Theorem A].** For every even n >= 4: if {0} is selected then CB is selected, and if
CB is selected then all rotations of Omega_n are selected. For n = 2^k - 2 (k >= 3) the selected set either
contains both {0} and CB or neither, and it is exactly { {0}, CB } (codes 0, 2, 5; k* >= 1) iff this closed class
has minimum gamma — in particular if it is the only closed class.

**[attempted (gap: uniqueness of the closed class)]** For n = 2^k - 2 the closed class { {0}, CB } is proved, but
not that every other cycle has a G1 path into it. This is computed for n = 6 and 14 (one closed class, of size 2,
table below) and open for n = 30, 62, ... . What would close it: a description of the cycles of rule 122 at
n = 2^k - 2 comparable to Lemma 6, or an enumeration at n = 30 (2^30 states, beyond the allowance of this track).

Tests (`cb_defect_122.py`, `out/cb_defect_122.txt`): R1, R2 and R3 hold on every even ring n = 4..256 (T1, T2, T3:
True); R4 holds for n = 6, 14, ..., 2046 (T4: True); the limit cycle of D_n agrees with the enumerated
out-neighbours of CB for the 12 even n <= 26 (T6: True).

**What decides the selection of the checkerboard [computed for even n = 4..26].**

| n | cycles | closed classes: sizes | 0 in closed class | CB in closed class | out-neighbours of {0} | out-degree of CB | smallest out-neighbour of CB (rep) | fate of the defect orbit | cycles with a G1 path to CB | CB has a G1 path to {0} | codes missing on the closed class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 4 | [4] | yes | yes | CB only | 2 | `0111` | other (transient 0, period 2) | 4 | yes | [1, 4] |
| 6 | 5 | [2] | yes | yes | CB only | 1 | `000000` | zero (transient 3, period 1) | 5 | yes | [1, 3, 4, 6, 7] |
| 8 | 8 | [8] | yes | yes | CB only | 4 | `00000111` | other (transient 2, period 6) | 8 | yes | none |
| 10 | 27 | [25] | no | no | CB only | 5 | `0000011011` | other (transient 3, period 4) | 2 | no | [2] |
| 12 | 21 | [19] | yes | yes | CB only | 6 | `000000000111` | other (transient 4, period 14) | 21 | yes | none |
| 14 | 46 | [2] | yes | yes | CB only | 1 | `00000000000000` | zero (transient 7, period 1) | 46 | yes | [1, 3, 4, 6, 7] |
| 16 | 80 | [38] | yes | yes | CB only | 8 | `0000000000000111` | other (transient 6, period 14) | 80 | yes | none |
| 18 | 167 | [99] | no | no | CB only | 9 | `000000000000011011` | other (transient 7, period 12) | 2 | no | [2] |
| 20 | 289 | [287] | yes | yes | CB only | 10 | `00000000000000000111` | other (transient 8, period 62) | 289 | yes | none |
| 22 | 466 | [365] | yes | yes | CB only | 11 | `0000000000000110000011` | other (transient 9, period 8) | 466 | yes | none |
| 24 | 641 | [132] | yes | yes | CB only | 12 | `000000000000000000000111` | other (transient 10, period 126) | 641 | yes | none |
| 26 | 1506 | [1363] | yes | yes | CB only | 13 | `00000000000000000000011011` | other (transient 11, period 28) | 1506 | yes | none |

(CB = checkerboard cycle; "rep" = numerically smallest state over the cycle and its rotations; "fate of the
defect orbit" = end of the orbit of D_n from `cb_defect_122.py`; "cycles with a G1 path to CB" counts CB itself.)

Reading, separated by status:
* [proved] {0} always leads to CB and to nothing else (R1); CB leads only to the rotations of Omega_n (R2).
  So {0} and CB are never selected separately "from below": {0} selected implies CB selected (R5).
* [computed, n = 4..26] There is exactly one closed class K at every n, so S = K (Theorem A). CB is in K iff {0} is
  in K. CB and {0} are transient exactly at n = 10 and 18. There, no cycle other than {0} and CB has a G1 path
  to CB (column "cycles with a G1 path to CB" = 2): the pair { {0}, CB } is a source of G1, left through Omega_n
  and never re-entered. At all other even n <= 26 the class K contains a cycle with a path back to CB (or K is
  the pair itself, n = 6, 14).
* [computed] So the selection of the checkerboard is decided by whether the closed class reached from Omega_n
  contains a state at Hamming distance 1 from the basin of CB or of 0. The type of Omega_n alone does not decide
  it: Omega_n is the cycle of the state 0...011011 at n = 10, 18 and also at n = 26, but at n = 26 the
  checkerboard is in the closed class. In particular the guess "not selected iff n = 2 (mod 8)" suggested by
  n = 10, 18 is false at n = 26.
* [computed, even n = 4..100] The orbit of D_n ends on 0 exactly for n = 6, 14, 30, 62, never on CB, and on another
  cycle otherwise (three cases undetermined), from `out/cb_defect_122.jsonl`:

- defect orbit ends on **zero**: n = 6, 14, 30, 62
- defect orbit ends on **checkerboard**: n = (none)
- defect orbit ends on **other**: n = 4, 8, 10, 12, 16, 18, 20, 22, 24, 26, 28, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 64, 66, 68, 70, 74, 76, 78, 80, 82, 84, 86, 88, 90, 94, 98, 100
- defect orbit ends on **undetermined**: n = 72, 92, 96
- undetermined cases: cycle not closed within 400000 steps; 0 or CB met within these steps: n = 72: no, n = 92: no, n = 96: no

  So, in this range, { {0}, CB } is a closed class exactly at n = 2^k - 2 (proved there by R4; for the other n the
  statement "not a closed class" is computed, and for n = 72, 92, 96 only "0 and CB not met within the steps run").
* [attempted (gap: no description of the cycles)] A proof of the selection pattern at general even n would need
  the closed class reached from Omega_n; nothing was proved beyond R1-R5.

Odd n, for completeness [computed for n = 5..25]: one closed class at every n; the zero state alone at n = 7 and
15 (the study's zero mechanism at 2^k - 1); code 2 is missing on the closed class at every odd n; {0} is
transient at n = 11, 19, 23:

| n (odd) | cycles | closed classes: sizes | 0 in closed class | out-degree of {0} | codes missing on the closed class |
|---|---|---|---|---|---|
| 5 | 6 | [6] | yes | 5 | [2] |
| 7 | 1 | [1] | yes | 0 | [1, 2, 3, 4, 5, 6, 7] |
| 9 | 19 | [19] | yes | 9 | [2] |
| 11 | 25 | [24] | no | 11 | [2] |
| 13 | 29 | [16] | yes | 13 | [2] |
| 15 | 51 | [1] | yes | 0 | [1, 2, 3, 4, 5, 6, 7] |
| 17 | 120 | [86] | yes | 17 | [2] |
| 19 | 229 | [95] | no | 19 | [2] |
| 21 | 379 | [358] | yes | 21 | [2] |
| 23 | 509 | [230] | no | 23 | [2] |
| 25 | 899 | [244] | yes | 25 | [2] |

### 7.2 Rule 26 away from powers of two: the code 111

**Lemma Q1 [proved (computer-assisted: `make_tables.py`, `out/tables.md`, 32 blocks)].** Under rule 26 the block
111 at the sites i-1, i, i+1 of F(x) occurs iff x has the block 10011 at the sites i-2, ..., i+2. (By hand: f = 1
only on the codes 001, 011, 100; three consecutive overlapping codes from this set must be 100, 001, 011.)
So every state of a cycle that carries the block 111 is the image of a state containing 10011 at the same
place, and a one-flip path can enter such a cycle only through a state that contains 10011.

**[computed for n = 4..26]** (`out/explore_122_26.jsonl`):

| n | n mod 3 | cycles | closed classes: sizes | transient cycles | cycles carrying 111 | of these in the closed class | transient cycles = 111-carriers outside the closed class | codes missing on the closed class | smallest 111-carrier in the closed class (rep) |
|---|---|---|---|---|---|---|---|---|---|
| 4 (2^k) | 1 | 1 | [1] | 0 | 0 | 0 | yes | [1, 2, 3, 4, 5, 6, 7] | - |
| 5 | 2 | 3 | [3] | 0 | 1 | 1 | yes | none | `00111` |
| 6 | 0 | 7 | [7] | 0 | 0 | 0 | yes | [7] | - |
| 7 | 1 | 3 | [3] | 0 | 0 | 0 | yes | [7] | - |
| 8 (2^k) | 2 | 10 | [1] | 9 | 1 | 0 | no | [1, 2, 3, 4, 5, 6, 7] | - |
| 9 | 0 | 5 | [5] | 0 | 0 | 0 | yes | [7] | - |
| 10 | 1 | 19 | [18] | 1 | 1 | 0 | yes | [7] | - |
| 11 | 2 | 12 | [12] | 0 | 3 | 3 | yes | none | `00001010011` |
| 12 | 0 | 64 | [64] | 0 | 0 | 0 | yes | [7] | - |
| 13 | 1 | 27 | [25] | 2 | 2 | 0 | yes | [7] | - |
| 14 | 2 | 76 | [76] | 0 | 2 | 2 | yes | none | `00100100100111` |
| 15 | 0 | 68 | [67] | 1 | 1 | 0 | yes | [7] | - |
| 16 (2^k) | 1 | 552 | [1] | 551 | 3 | 0 | no | [1, 2, 3, 4, 5, 6, 7] | - |
| 17 | 2 | 148 | [148] | 0 | 3 | 3 | yes | none | `00100100100100111` |
| 18 | 0 | 567 | [566] | 1 | 1 | 0 | yes | [7] | - |
| 19 | 1 | 390 | [385] | 5 | 5 | 0 | yes | [7] | - |
| 20 | 2 | 2816 | [2815] | 1 | 4 | 3 | yes | none | `00100100100100100111` |
| 21 | 0 | 1115 | [1111] | 4 | 4 | 0 | yes | [7] | - |
| 22 | 1 | 3695 | [3684] | 11 | 13 | 2 | yes | none | `0000101001000111010011` |
| 23 | 2 | 3142 | [3141] | 1 | 5 | 4 | yes | none | `00100100100100100100111` |
| 24 | 0 | 33606 | [33594] | 12 | 12 | 0 | yes | [7] | - |
| 25 | 1 | 8772 | [8757] | 15 | 15 | 0 | yes | [7] | - |
| 26 | 2 | 28748 | [28742] | 6 | 10 | 4 | yes | none | `00100100100100100100100111` |

- for every n in 4..26 that is not a power of two, the transient cycles are exactly the 111-carrying cycles outside the closed class: True
- n in 4..26 with a 111-carrying cycle in the closed class (k* = 0): [5, 11, 14, 17, 20, 22, 23, 26]
- rule 26, 5-blocks x_(i-2..i+2) whose image has 111 at i-1..i+1: ['10011']

Reading:
* [computed] At every n = 4..26 there is exactly one closed class K, so S = K (Theorem A). At n = 4, 8, 16, K = {0}
  (the zero mechanism). At every other n in the range, **every cycle without the block 111 belongs to K, and the
  transient cycles are exactly the 111-carrying cycles outside K**. Hence k* = 0 iff at least one 111-carrying
  cycle belongs to K, i.e. iff some 111-carrying cycle has an incoming G1 path from the cycles without 111.
* [computed] This happens at n = 5, 11, 14, 17, 20, 23, 26 (all n = 2 (mod 3) in the range that are not powers of
  two; the carrier is the crystal (001)^a with one block 00111, n = 3a + 5, among others) and at n = 22
  (carriers of another kind, smallest representative in the table). At n = 0, 1 (mod 3), n != 22, 111-carrying
  cycles exist at n = 10, 13, 15, 18, 19, 21, 24, 25 but none is in K. The new cases n = 23, 24, 25, 26 follow the
  mod-3 description (k* = 0 at 23 and 26, code 7 missing at 24 and 25); n = 22 remains the only exception up to 26.
* [attempted (gap: no description of the cycles)] Nothing beyond Lemma Q1 is proved. A proof of "n = 2 (mod 3)
  implies k* = 0" would need, for n = 3a + 5 not a power of two: (i) that the orbit of (001)^a 00111 is a cycle
  (a finite local computation that was not carried out), and (ii) a one-flip path into it from a cycle of K,
  which requires knowing K; (ii) is the open part. The exception n = 22 shows that the converse is false.
  The method of Theorem 1 does not transfer to rule 26 at n = 2^k: rule 26 is not permutive and has no analogue
  of Lemma 5 (at n = 16 it has 552 cycles, of which 551 are transient).

## 8. Summary of statements

| statement | tag |
|---|---|
| Lemma 0 (one-flip edges) | proved |
| Lemma 1 (f = c + a(1+b)) | proved |
| Lemma 2 (rule 154 = rule 90 on E ∪ O, even n) | proved |
| Lemma 3 (nilpotent on E ∪ O iff n = 2^k) | proved |
| Lemma 4 (F(M) ⊆ M, even n) | proved |
| Lemma 5 (collisions of F only inside E, inside O, or {1_E, 1_O}) | proved; mechanical re-check `check_pair_graph.py` |
| Lemma 6 (F permutes M; periodic states = M ∪ rule-90 cycles; = M ∪ {0} at 2^k) | proved |
| Lemma 7 (one-flip moves inside M are symmetric; cycles in M mutually reachable) | proved |
| Theorem 1 (n = 2^k: every cycle reaches {0} in G1 within n/2 steps; only closed class {0}; gamma; S = {0}; k* = 1) | proved |
| Theorem 2 (n not a power of two: G1 strongly connected, all cycles selected, k* = 0) | proved |
| O1 (F^n = id on M at n = 2^k) | computed for n = 4, 8, 16; sampled for n = 32..1024 |
| O2 (maximum G1 distance to {0} equals n/2) | computed for n = 4, 8, 16 (upper bound proved) |
| R1 (rule 122, even n: {0} leads only to CB) | proved |
| R2 (rule 122: CB leads only to the rotations of Omega_n) | proved |
| R3 (rule 122: formula for the orbit of D_n up to time n/2 - 1) | proved |
| R4 (rule 122, n = 2^k - 2: { {0}, CB } is a closed class) | proved |
| R5 ({0} selected implies CB selected implies Omega_n selected) | proved, using Theorem A |
| Rule 122, n = 2^k - 2: { {0}, CB } is the selected set | attempted (gap: uniqueness of the closed class); computed for n = 6, 14 |
| Rule 122, even n: CB selected iff in the unique closed class; fails only at n = 10, 18 | computed for n = 4..26 |
| Q1 (rule 26: 111 arises only from 10011) | proved (computer-assisted: `make_tables.py`, `out/tables.md`) |
| Rule 26: transient cycles = 111-carriers outside the unique closed class; k* = 0 at n = 5, 11, 14, 17, 20, 22, 23, 26 | computed for n = 4..26 |

## 9. Scripts and outputs (all in this folder)

| script | purpose | output |
|---|---|---|
| `check_lemmas.py` | exhaustive tests of Lemmas 1-7 and Theorems 1, 2 for n = 3..16 | `out/check_lemmas.jsonl`, `out/check_lemmas.txt` |
| `check_pair_graph.py` | mechanical case analysis of Lemma 5, valid for all n | `out/check_pair_graph.txt` |
| `cross_check.py` | comparison with the sealed sample (n = 8..21) and the sealed solver (n = 4..7) | `out/cross_check.txt`, `out/solver_n4_7.jsonl` |
| `sample_large_n.py` | sampled tests at n = 32..1024 (seeded) | `out/sample_large_n.jsonl` |
| `g1lib.py` | G1 from the definition (used by the next two) | - |
| `explore_122_26.py` | closed classes of G1 for rules 122 and 26, n = 4..26 | `out/explore_122_26.jsonl` |
| `regression_explore.py` | recomputation of the records for n = 4..24 with the final `g1lib.py` | `out/regression_explore.txt` |
| `cb_defect_122.py` | tests of R1-R4 and fate of the defect orbit, rule 122 | `out/cb_defect_122.jsonl`, `out/cb_defect_122.txt` |
| `make_tables.py` | tables of this file | `out/tables.md` |

To reproduce, from this folder and in this order: `python check_lemmas.py`, `python check_pair_graph.py`,
`python cross_check.py`, `python sample_large_n.py`, `python explore_122_26.py 4 26` (appends; skips cases already
in the output file), `python cb_defect_122.py 100`, `python regression_explore.py 24`, `python make_tables.py`.

Not used: any file under `code/ring_size/`, `code/fw/` or `data/ring_size/`. Read for context: the definitions
as restated in `../SAMPLE.md` (Section 2), and Sections 5.3-5.5 and 7 of `report_ring_size.md`.

## 10. Cost (CPU time; one process throughout)

| script | CPU seconds | source of the figure |
|---|---|---|
| check_lemmas.py (n = 3..16) | 0.50 | out/check_lemmas.txt |
| cross_check.py (solver for n = 4..7 and comparison) | 0.01 | out/cross_check.txt |
| sample_large_n.py (n = 32..1024) | 1.28 | out/sample_large_n.jsonl (cumulative, last record) |
| cb_defect_122.py (even n = 4..256, fate up to 100) | 2.2 | out/cb_defect_122.txt |
| explore_122_26.py, n = 4..20 (sum of the per-case figures) | 0.3 | out/explore_122_26.jsonl |
| explore_122_26.py, n = 21..24 (sum of the per-case figures) | 4.8 | out/explore_122_26.jsonl |
| explore_122_26.py, n = 25..26 (sum of the per-case figures) | 14.3 | out/explore_122_26.jsonl |

The only run announced beforehand was `explore_122_26.py` for n = 25, 26 (`../logs/BATCHES_phase2.md`): expected
about 1 CPU-minute and 1.5 GB; measured 14.5 CPU-seconds and a peak of 4329 MB, i.e. the memory estimate was
exceeded by a factor of about three for about 15 seconds. `regression_explore.py` (`out/regression_explore.txt`):
records for n = 4..24 (42 cases) identical to `out/explore_122_26.jsonl` apart from cpu_seconds: True;
cpu seconds: 5.1; peak RSS (MB): 1686.
