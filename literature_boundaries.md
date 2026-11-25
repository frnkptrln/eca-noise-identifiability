# Literature review: elementary cellular automata on a finite row with null, fixed or reflecting boundaries

Compiled 24 November 2026 for the open-boundaries extension of the note "Rule identifiability in elementary cellular automata under dynamical noise".

## 0. Scope and reading rule

Scope: elementary cellular automata (ECA; radius 1, two states) on a row of n cells whose outside neighbours are held fixed (null boundary: cells 0 and n+1 held at 0; other fixed values), and secondarily reflecting boundaries. The questions are: Q1 cycle structure and reachability (Garden-of-Eden states); Q2 additive rules 60, 90, 150 and 90/150 hybrids under null boundary (invertibility, nilpotency, polynomials, cycle lengths, relation to a ring of 2n+2 cells); Q3 reversibility of non-additive ECA under null or fixed boundaries; Q4 noisy or probabilistic CA with fixed boundaries, and stochastic stability on a path rather than a cycle.

Reading rule: every source in Section 1 was opened and read in this session (24 Nov 2026), either in full or in the sections named. Every attributed statement gives its location. Page numbers are those of the copy actually read. Where that copy is an arXiv version, the page numbers are the arXiv pages, not journal pages; this is stated per source. Statements that a source attributes to other works are reported only as that source's own statement, and the other works are not cited. Each DOI was checked to resolve to the listed title through the CrossRef-backed resolver of the full-text fetch tool; volume and page data were checked against the publisher or indexing pages found by search. Nineteen further candidate sources could not be obtained as full text in this session, because they were closed access, behind hosts blocked in this sandbox, or without a resolvable open copy. They are not listed.

Tags used below: [proved] means the source gives a proof; [numerical] means the source reports computation or simulation; [stated] means the source asserts it without proof in the part read; [our remark] means an observation made while writing this review that is not in any source.

Rule-number convention: all sources read use Wolfram numbering with the neighbourhood (x_{i-1}, x_i, x_{i+1}). Rule 60 is x_{i-1} XOR x_i ([S1] Table 1, p. 120; [S4] Table 2, p. 12). Rule 90 is x_{i-1} XOR x_{i+1}. Rule 150 is x_{i-1} XOR x_i XOR x_{i+1}. The rule-min-term (RMT) index of [S4] (Def. 5, p. 8) equals the note's code c = 4x_{i-1} + 2x_i + x_{i+1}.

---

## 1. Sources read

### [S1] Martín del Rey (2015), Rev. Unión Mat. Argentina 56(1)

A. Martín del Rey, "A note on the reversibility of the elementary cellular automaton with rule number 90", Revista de la Unión Matemática Argentina 56(1) (2015) 107-125. Open-access PDF: https://inmabb.criba.edu.ar/revuma/pdf/v56n1/v56n1a06.pdf (no DOI printed on the article).

Read: full text, pp. 107-125.

Relevant statements:
- Definition of null boundary: x_i^t = 0 for i < 1 or i > n at every t (p. 109). For a linear ECA the global map is X -> M_n X, with M_n tridiagonal; for null boundary the corner entries are 0 (p. 110).
- Lemma 2.1 (p. 110): a linear CA is reversible iff its local transition matrix is non-singular [stated, attributed to a book]. For a reversible CA the state-transition diagram has no trees: every configuration has exactly one predecessor (p. 110).
- Proposition 3.1 (p. 113) [proved, pp. 113-115, via the DETGTRI tridiagonal determinant algorithm]:
  - (a) Rule 90 with null boundary is reversible iff n is even; det M_n = 1 for n even and 0 for n odd (p. 114).
  - (b) Rule 90 with periodic boundary is irreversible for every n.
- Figure 3 (p. 114): the complete state-transition diagram of rule 90, null boundary, n = 4 (all configurations on cycles). Figure 4 (p. 114): the state-transition diagram for n = 7, which contains trees.
- Theorem 3.2 (p. 115) [proved, pp. 115-117]: explicit inverse of null-boundary rule 90 for even n, a block matrix built from 2x2 blocks. Worked example for n = 10 (pp. 117-118).
- Section 4 (pp. 119-123), the other linear ECA under null boundary:
  - Rule 60 is reversible for every n, because M_n is lower triangular with unit diagonal and det M_n = 1. The inverse matrix is given (pp. 120-121) [proved].
  - Rule 60 with periodic boundary is non-reversible for every n (p. 121) [proved].
  - Rule 102 is reversible with null boundary and non-reversible with periodic boundary (p. 121) [stated as analogous to rule 60].
  - Rule 150 with null boundary is reversible if n ≡ 0, 1 (mod 3) (p. 121) [stated, with inverse matrices in Prop. 4.1, pp. 121-122, attributed to earlier work]. The converse (non-reversibility for n ≡ 2 mod 3) is not stated explicitly on these pages.
  - Rule 150 with periodic boundary is reversible when n ≡ 1, 2 (mod 3) (p. 122) [stated].
  - Rule 170 is not reversible with null boundary; with periodic boundary it is reversible for every n (pp. 122-123).
  - Rule 240 is non-reversible with null boundary (p. 123).
  - Rule 204 (identity) is reversible for both boundaries (p. 123).

### [S2] Tadaki (1994), Phys. Rev. E 49

S. Tadaki, "Orbits in one-dimensional finite linear cellular automata", Physical Review E 49(2) (1994) 1168-1173. DOI 10.1103/PhysRevE.49.1168.

Read: full text of the arXiv version cond-mat/9305012v1 (21 pages including tables and figures). Page numbers below are arXiv pages.

Relevant statements (rule 90 and rule 150, "Dirichlet" boundary a_0 = a_{N+1} = 0, i.e. null boundary; p. 3):
- Table I (pp. 11-12) [numerical]: the periodicity of the transfer matrix U for N = 3..32, for both rules, written as U^{Π+π} = U^{π}, with Π the maximum period and π the maximum transient. Examples for rule 90: N = 4: U^6 = I; N = 6: U^14 = I; N = 10: U^62 = I; N = 5: U^5 = U.
- Eq. (2.4a-c), p. 3 [numerical, results of the author's earlier paper]. For rule 90:
  - N even: U^{Π_N} = I, so every non-null state is periodic.
  - N odd: some states lie on transient paths.
  - N = 2^n − 1: U^N = 0, so every state reaches the null state within N steps.
- Rule 150 (p. 4) [numerical]:
  - N = 3n + 2: periodic orbits are reached through relaxation paths.
  - N ≠ 3n + 2: all states except the null state lie on periodic orbits.
  - No rule-150 case is drawn into the null state.
- Characteristic ("eigenvalue") polynomials over GF(2) (pp. 5-6):
  - Rule 90: D_N(λ) = λ D_{N−1} − D_{N−2}, eq. (3.3), with closed form eq. (3.4).
  - Rule 150: obtained by λ -> λ + 1, eqs. (3.6)-(3.8).
  - Table II (pp. 13-14) lists D_N for rule 90 and Table III (pp. 15-16) for rule 150, N = 3..32. For rule 90, D_N = λ^N for N = 3, 7, 15, 31.
- Statements on p. 6:
  - Nilpotent cases (D_N = λ^N) occur for rule 90 with N = 2^n − 1 (citing the author's earlier paper).
  - D_N has a constant term (U invertible) for rule 90 with even N and for rule 150 with N ≠ 3n + 2.
  - For rule 150 with N = 2^n − 1 the maximum period is N + 1.
- Eq. (3.9) and the identity D_{2n+1}(λ) = λ D_n(λ²) (p. 7) [derived in GF(2)].
- Eqs. (3.10)-(3.11) (p. 7) relate the maximum period Π and maximum transient π of N = 2n + 1 to those of N = n. In the text layer of the arXiv copy, (3.10) reads Π_{2n+1} = 2Π_n + 1; we could not check the typeset equation. Table I (N = 5, 9, 11 from N = 2, 4, 5) fits Π_{2n+1} = 2Π_n and π_{2n+1} = 2π_n + 1 instead [our remark]. Do not use (3.10) without checking the published version.
- Internal inconsistency: the concluding remarks (p. 7) assign relaxation paths for rule 150 to "N = 3n + 1". Section II (p. 4) and Table I (N = 5, 8, 11, ...) assign them to N = 3n + 2.

### [S3] Vadali and Turner (2026), Theor. Comput. Sci. 1074

A. Vadali, A. M. Turner, "Equality of cycle lengths in one- and two-dimensional σ automata", Theoretical Computer Science 1074 (2026) 115897. DOI 10.1016/j.tcs.2026.115897.

Read: arXiv version 2502.10898v2 (22 Feb 2026): Sections 1-3 (pp. 1-7), Section 5 (Theorem 5.1, p. 9; Theorem 5.4, p. 11), Section 6 (pp. 11-13) and Appendix B.4 (pp. 19-20). Sections 4 and 7 were skimmed only for statements quoted here. Page numbers are arXiv pages.

Relevant statements. The σ1(n) automaton is rule 90 on n cells with null boundary: the row is extended by one cell at each end held at 0 (Section 1.1, p. 2).
- Theorem 2.3 (p. 5) [proved]: over Z_2 the cycle length of a matrix is t·2^s. Here t is the lcm of the orders of the non-zero eigenvalues, and s = ⌈log2 m⌉ with m the size of the largest Jordan block with non-zero eigenvalue.
- The characteristic polynomial p_n of A_n is a Chebyshev polynomial of the second kind mod 2: p_i = λ p_{i−1} + p_{i−2}, eq. (3), p. 5. Theorem 3.2 (p. 5) gives p_{2i} = (p_i + p_{i−1})² and p_{2i+1} = λ p_i². Theorem 3.1 (p. 5) states that each eigenvalue has a single eigenvector; the proof is deferred to an earlier reference.
- Theorem 3.4 (p. 6) [proved]: write n + 1 = 2^a·b with b odd.
  - Each non-zero eigenvalue of A_n has one Jordan block, of size 2^{a+1}.
  - The eigenvalue 0 has one block of size 2^a − 1, absent if a = 0.
  - Hence A_n is invertible iff a = 0, i.e. iff n is even [immediate from the theorem].
- Theorem 3.5 (p. 6): for even n the eigenvalues are α^i + α^{−i}, i = 1..n/2, with α of order n + 1.
- Theorem 3.6 (p. 7):
  - The non-zero eigenvalues of A_n are those of A_{b−1}.
  - When n + 1 is a power of 2 there is a single Jordan block, with eigenvalue 0.
- Theorem 5.1 (p. 9): if n + 1 is a power of 2, then A_n^n = 0 (nilpotent).
- [our remark] The converse follows in one line from Theorems 3.4 and 3.6. If b > 1, then A_{b−1} (b − 1 even) is invertible, so A_n has non-zero eigenvalues and is not nilpotent. Hence null-boundary rule 90 is nilpotent iff n + 1 is a power of 2. The paper does not state the converse as such.
- Theorem 3.7 (p. 7): CL[A_n] = 2^{a+1}(2^{sord2(b)} − 1)/q, where q divides 2^{sord2(b)} − 1 and sord2(b) is the least j with 2^j ≡ ±1 (mod b).
- Table 1 (p. 3) gives cycle lengths CL for n = 6, 7, 8, 9, 14, 15, 16, 36: 14, 1, 14, 12, 30, 1, 30, 174762. These agree with Tadaki's Table I [S2] where both cover n.
- Reflection ("method of images") relation to a ring of 2n + 2 cells (Section 6, p. 12; Appendix B.4, p. 20):
  - A null-boundary configuration f on 1..n is extended to Z by mirrors at 0 and n + 1. The sites 0 and n + 1 (mod 2n + 2) are set to 0, and the pattern is reflected, giving a configuration with period 2n + 2 symmetric under x -> −x.
  - Theorem 6.2 [proved] states that the configuration evolves exactly as its reflected pattern restricted to 1..n. The mirror sites stay 0 because their two neighbours are equal.
  - Theorem 6.3: CL[σ1(n)] divides CL[ring of 2n + 2].
  - Lemma B.3 (p. 20): CL[σ1(n)] = CL[ring of 2n + 2].
  - The authors remark (pp. 12-13) that for other automata, when there are edges instead of periodic boundaries, the reflection principle "usually does not work".
- Section 1 (p. 1) states that σ1 dynamics were studied by Martin, Odlyzko and Wolfram; that work was not read here and is not cited.

### [S4] Bhattacharjee, Naskar, Roy and Das (2020), Natural Computing 19 (survey)

K. Bhattacharjee, N. Naskar, S. Roy, S. Das, "A survey of cellular automata: types, dynamics, non-uniformity and applications", Natural Computing 19 (2020) 433-461. DOI 10.1007/s11047-018-9696-8.

Read: arXiv draft 1607.02291 (43 pages): Sections 2.4-2.5 (pp. 7-8), 3.2-3.3 (pp. 12-14), 6 (p. 25), 6.1-6.2 (pp. 26-28), plus reference list entries for orientation. Page numbers are draft pages.

Relevant statements:
- Section 2.4 (pp. 7-8), boundary conditions:
  - In open (fixed) boundary CAs the missing neighbours are assigned fixed states. Null boundary (missing neighbours always 0) is "the most popular" among them and is used in VLSI design and test.
  - Further boundary types are named and defined:
    - adiabatic or reflecting: the missing neighbour of a boundary cell is the cell itself;
    - reflexive: the left and right neighbours of a boundary cell are the same cell;
    - intermediate: the missing neighbour is the neighbour's neighbour;
    - stochastic: boundary cells take states at random.
- Section 3.2 (pp. 12-13): under null boundary a linear (possibly hybrid) ECA on n cells is a tridiagonal characteristic matrix T over GF(2). There is a worked example for rule vector ⟨150, 150, 90, 150⟩, and y = T·x describes the global map.
- Section 3.3 (pp. 13-14), the reachability tree for n-cell non-uniform ECA under null boundary:
  - Definition 8 (p. 13): under null boundary, RMTs 4-7 of the first rule and RMTs 1, 3, 5, 7 of the last rule cannot occur.
  - A configuration is reachable iff it is a root-to-leaf path of the tree; non-reachable configurations are the Garden-of-Eden configurations (p. 14).
  - Figure 6 (p. 14) gives the example rule vector ⟨5, 73, 200, 80⟩, n = 4.
  - The survey states that the tree changes with the boundary condition, and that a periodic-boundary version and a d-state version exist (p. 14).
- Section 6.1 (p. 26):
  - The linear ECA rules are 60, 90, 102, 150, 170, 204, 240, plus rule 0.
  - Complemented rules are handled by adding an inversion vector F: y = T·x + F.
  - Section 6.1.1: a linear non-uniform ECA is a group CA (reversible) iff det T = 1.
- Section 6.1.1 (p. 27):
  - Maximal-length CAs (all non-zero configurations on a single cycle) have a primitive characteristic polynomial.
  - They are built from rules 90 and 150 under null boundary; "no single rule can produce a maximal length CA".
  - Under periodic boundary the characteristic polynomial is factorizable, so no maximal-length periodic-boundary CA exists [the survey's statement, attributed by it to earlier work].
- Section 6.1.2 (p. 27): non-group (irreversible) linear CAs are described by attractors, α-trees and depth (number of steps from a Garden-of-Eden state to the nearest cyclic state).
- Section 6.2 (p. 28) [stated, citing the authors' earlier work]:
  - Out of 256 ECA rules, only 62 can appear in the rule vector of a reversible non-uniform ECA under null boundary; under periodic boundary the number is 70.
  - The 62 rules fall into six classes with first-rule and last-rule tables (Tables 3-4).
  - The same tables decide which null-boundary linear CAs are group CAs.

### [S5] Wang, Ma, Wang, Lin and Chen (2025), Appl. Math. Comput. 489

C. Wang, J. Ma, C. Wang, D. Lin, W. Chen, "Two graphs: Resolving the periodic reversibility of one-dimensional finite cellular automata", Applied Mathematics and Computation 489 (2025) 129151. DOI 10.1016/j.amc.2024.129151.

Read: full text of arXiv version 2402.05404v2 (11 pages). Page numbers are arXiv pages.

Relevant statements:
- Section 2.1 (p. 3): the algorithm covers null ("n") and periodic ("p") boundaries. It is said to apply also to reflective boundaries, "but it will not be further elaborated upon".
- Proposition 1 (p. 4): for a finite CA, surjective ⇔ injective ⇔ reversible.
- Definitions 2.3-2.5 (p. 4): n-cell-reversible; strictly reversible (reversible for every n); reversibility sequence (0/1 per n), which is eventually periodic.
- Definition 3.1 (p. 5): the reversibility graph G_R for null boundary, a de Bruijn-type subset construction with root and end vertices fixed by the boundary zeros.
- Theorem 1 (p. 5) [proved by analogy with Amoroso's algorithm]: the CA is strictly reversible iff G_R has no negative vertex.
- Theorems 2 and 3 (p. 6) [proved]: a negative vertex at depth d gives irreversibility at n = d, and at d plus non-negative combinations of the lengths of elementary circuits through it.
- Theorem 4 (p. 7) is supported "by an example in place of a formal proof". Theorem 5 (p. 8): the reversibility period is the lcm of the gcds of circuit lengths over connected components of the circuit graph.
- Table 1 (p. 10) [numerical]: reversibility sequences for n = 1..12. Rule strings are written f(111)…f(000), by Eq. (1), p. 3. Null-boundary entries:
  - 10010110 (rule 150): 101101101101, i.e. reversible iff n ≢ 2 (mod 3) for n ≤ 12;
  - 10100101 (rule 165, the complement of 90): reversible iff n even;
  - 10101010 (rule 170): never reversible;
  - 11000011 (rule 195, the complement of 60): never reversible, 000000000000.
  - [our remark] The rule-195 entry conflicts with the triangular-matrix argument of [S1] p. 120: rule 195 under null boundary is the affine map x -> M_60 x + 1, which is bijective for every n. Either the entry or our reading of the rule string is wrong. Table 1 should be used with care until this is resolved.
- Text p. 9: "a large number of nonlinear FCA have a period of 1", i.e. irreversible for all large n; only a small portion show periodic reversibility (example 11010010 = rule 210) [numerical].

### [S6] Sfairopoulos, Causer, Mair and Garrahan (2023), Phys. Rev. B 108

K. Sfairopoulos, L. Causer, J. F. Mair, J. P. Garrahan, "Boundary conditions dependence of the phase transition in the quantum Newman-Moore model", Physical Review B 108 (2023) 174107. DOI 10.1103/PhysRevB.108.174107.

Read: arXiv version 2301.02826v4 (30 Jul 2025): Sections III.A-III.B (pp. 3-5) and Appendix A (p. 13). Page numbers are arXiv pages.

Relevant statements (marginal relevance):
- Section III.A (pp. 3-4), periodic rows of length L [stated, based on an earlier paper]:
  - Rule 90: 2^{L−1} configurations are unreachable for L odd and 3·2^{L−2} for L even.
  - Rule 60: 2^{L−1} are unreachable for every L.
  - Reachable configurations have 2 or 4 predecessors (rule 90, L odd or even) and always 2 (rule 60).
  - With open boundaries the single-seed pattern of rule 60 continues as a fractal, whereas with periodic boundaries at L = 32 it reaches the empty configuration (p. 3).
- Section III.B and Table I (p. 4): cycle lengths of rule 60 on periodic rows. For L a power of two, every initial state reaches the fixed point.
- Appendix A (p. 13): their "open boundary" (OBC) is defined by leaving the first cell of the row unchanged. This is a different boundary from null boundary.

### [S7] Salman (2013), IJCSIT 5(4)

K. Salman, "Analysis of elementary cellular automata boundary conditions", International Journal of Computer Science & Information Technology 5(4) (2013) 35-51. DOI 10.5121/ijcsit.2013.5403.

Read: Sections 1-2 (pp. 35-37) and Section 4.1 (pp. 42-43) with Tables 1-8 (pp. 43-45).

Relevant statements (weak evidence, [numerical] from space-time images only):
- Fixed boundary values written as two-bit labels 00, 01, 10, 11 (Fig. 2, p. 36).
- Runs use span K = 15 cells, T = 60 steps, one centre-seed and one random-seed initial condition, rule-30 subgroup (30, 86, 135, 149) and rule-45 subgroup (45, 101, 75, 89) (Section 4.1, p. 42).
- Reported observations (p. 42):
  - With boundaries 00, the whole rule-30 subgroup (30, 86, 135, 149) evolves to a fixed point; with 11, rules 135 and 149 also evolve to a fixed point.
  - With unequal boundaries (01, 10) the rule-30 subgroup becomes periodic with period 2.
  - Rules 30 and 86 with boundaries 11 also become periodic.
  - The rule-45 subgroup behaves similarly, with generally longer periods.
- No proofs and no systematic enumeration over n.

### [S8] Marcovici, Sablik and Taati (2019), Electron. J. Probab. 24

I. Marcovici, M. Sablik, S. Taati, "Ergodicity of some classes of cellular automata subject to noise", Electronic Journal of Probability 24 (2019), paper no. 41, 1-44. DOI 10.1214/19-EJP297.

Read: arXiv version 1712.05500v3: Section 1 (pp. 2-3), Section 2.3 (p. 7), Section 2.4 (pp. 8-9), and the opening definition of Section 5.1 (p. 30). Page numbers are arXiv pages.

Relevant statements:
- Setting: configurations on the infinite lattice Z^d (p. 2), not finite rows. A PCA is ergodic if it forgets its initial condition (p. 2).
- The authors state that the only known one-dimensional CA that stays non-ergodic under sufficiently small positive noise has a sophisticated construction (p. 2).
- Section 2.3 (p. 7) defines the noise models. Zero-range noise acts independently per site through a stochastic matrix θ. Additive noise means a -> a + N; flips with probability ε on {0,1} are additive noise in this sense [our remark].
- Section 2.4 (p. 8), summary table:
  - surjective CA with additive noise are ergodic modulo shift (Thm. 4.1);
  - XOR CA with zero-range noise are ergodic (Thm. 5.1);
  - permutive 1d CA with permutation noise are ergodic (Thm. 3.16);
  - nilpotent CA under small perturbation are ergodic (Thm. 3.9).
  - Theorem statements were not read beyond this table.
- Nothing on finite rows, fixed boundaries or zero-noise selection of attractors was found in the sections read.

### [S9] Miękisz (2008), Lecture Notes in Mathematics 1940

J. Miękisz, "Evolutionary game theory and population dynamics", in V. Capasso, M. Lachowicz (eds.), Multiscale Problems in the Life Sciences, Lecture Notes in Mathematics 1940, Springer (2008) 269-316. DOI 10.1007/978-3-540-78362-6_5.

Read: arXiv version q-bio/0703062v1: Section 7 (pp. 22-24) and Sections 9.3-9.4 (pp. 35-41). Page numbers are arXiv pages.

Relevant statements:
- Section 7 (p. 22): for spatial games, Ω = 2^Λ with Λ a finite subset of Z, Z² "or any other infinite graph". Mistakes with probability ε make the chain ergodic.
- Definition 2 (p. 23): X is stochastically stable if lim_{ε->0} μ^ε(X) > 0.
- Tree representation (Section 7, p. 23):
  - μ^ε(X) = q^ε(X) / Σ_Y q^ε(Y), eqs. (49)-(50), with q^ε(X) a sum over X-trees of products of transition probabilities. The notes attribute this representation to Freidlin and Wentzell.
  - When the noise-free dynamics has only absorbing states (no larger recurrent classes), only absorbing states can be stochastically stable (p. 23).
  - Restriction to trees on absorbing states with path-maximal transition weights, eq. (51) (p. 24).
- Example 8 (pp. 38-40): players on a finite subset of Z with periodic boundary ("the players are located on the circle"), three strategies.
  - Theorem 17 (p. 39) [proved]: C is stochastically stable under perturbed best response.
  - Theorem 18 (p. 39) [proved]: under log-linear dynamics the stochastically stable configuration switches between X_B and X_C at n = 2 + 1/(0.5 − α).
  - The author notes that "adding two players to the population may change the stochastic stability" (p. 40).
- Example 9 (pp. 40-41): again periodic boundary. Section 9.4 contains no example with fixed boundaries.

---

## 2. Answers to Q1-Q4

### Q1. Cycle structure and reachability of ECA under null or fixed boundaries

Known in the sources read:
- For a single n and an arbitrary (also non-linear, also non-uniform) ECA under null boundary, reachability is decided by the reachability tree. Non-reachable configurations are exactly the Garden-of-Eden configurations, and RMTs 4-7 of the first cell and 1, 3, 5, 7 of the last cell are excluded by the boundary ([S4] Section 3.3, Def. 8, pp. 13-14).
- For a finite map, surjective ⇔ injective, so "no Garden-of-Eden state" ⇔ bijective ([S5] Prop. 1, p. 4).
- For all n at once, the reversibility sequence of a null-boundary ECA is eventually periodic in n and is computable from the reversibility graph and circuit graph ([S5] Theorems 1-5, pp. 5-8).
- For linear rules, state-transition diagrams under null boundary are given explicitly only for small examples:
  - rule 90 at n = 4 (all cyclic) and n = 7 (with trees) ([S1] Figs. 3-4, p. 114);
  - rule 150 at N = 4 and rule 90 at N = 5 ([S2] Figs. 4-5, pp. 20-21).
- For linear non-group CAs the survey describes the diagram by attractors, α-trees and depth ([S4] Section 6.1.2, p. 27).
- For fixed boundaries other than 0, the only material read is the space-time observation of [S7] (pp. 42-43) for rules 30, 86, 135, 149, 45, 101, 75, 89 at a single size K = 15:
  - equal boundaries (00 or 11) often lead to a fixed point;
  - unequal boundaries (01, 10) lead to short cycles (period 2 for the rule-30 subgroup).
  - This is [numerical] and covers one size only.

Not found in the sources read:
- a complete classification of cycle structure (number and lengths of cycles, transients) of all 88 ECA classes under null or fixed boundaries as a function of n;
- a null-boundary analogue of the ring results (crystals of period 3 or 4, power-of-two conditions) for non-additive rules;
- any systematic treatment of fixed boundary value 1, or of mixed boundaries (0 on one side, 1 on the other), beyond [S7].

### Q2. Additive rules 60, 90, 150 and 90/150 hybrids under null boundary

| Statement | Status in sources read | Where |
|---|---|---|
| Rule 60 (and 102) null boundary bijective for every n | [proved]: unit lower-triangular matrix | [S1] Section 4, pp. 120-121 |
| Rule 60 periodic boundary never bijective | [proved] | [S1] p. 121 |
| Rule 90 null boundary bijective iff n even | [proved] | [S1] Prop. 3.1(a), pp. 113-114; [S3] Thm. 3.4, p. 6; [S2] p. 6 (constant term for even N) |
| Rule 150 null boundary invertible iff n ≢ 2 (mod 3) | "if" direction [stated] in [S1] p. 121 (inverse matrices Prop. 4.1); both directions [numerical] for N ≤ 32 in [S2] (p. 4, Table I pp. 11-12, Table III pp. 15-16) and for n ≤ 12 in [S5] Table 1, p. 10. A complete proof of the "only if" direction was not found | as listed |
| Rule 90 null boundary nilpotent iff n + 1 is a power of 2 | "if" [proved]: [S3] Thm. 3.6, p. 7 and Thm. 5.1, p. 9. "Only if": one-line consequence of [S3] Thms. 3.4 and 3.6 [our remark]. [numerical] N ≤ 32: [S2] Table I and Table II (D_N = λ^N exactly for N = 3, 7, 15, 31) | as listed |
| Rule 150 null boundary never nilpotent; for N = 2^n − 1 maximum period N + 1 | [stated/derived] | [S2] pp. 4, 6 |
| Characteristic polynomials | rule 90: D_N = λD_{N−1} + D_{N−2} over GF(2), closed form; rule 150 by λ -> λ + 1 | [S2] eqs. (3.3)-(3.8), pp. 5-6; [S3] eq. (3), Thm. 3.2, p. 5 |
| Jordan structure and minimal polynomial information, rule 90 | one Jordan block per eigenvalue; block size 2^{a+1} (non-zero eigenvalues), 2^a − 1 (eigenvalue 0), with n + 1 = 2^a·b | [S3] Thms. 3.1, 3.4, 3.6, pp. 5-7 |
| Cycle lengths, rule 90 null boundary | CL = 2^{a+1}(2^{sord2(b)} − 1)/q (Thm. 3.7, p. 7); tables in [S3] Table 1, p. 3 and [S2] Table I | as listed |
| Null row of n cells ↔ ring of 2n + 2 cells | [proved] for rule 90: mirror-symmetric extension with zeros at the two mirror sites evolves consistently (Thm. 6.2, p. 12); CL[null, n] = CL[ring, 2n + 2] (Thm. 6.3, p. 12; Lemma B.3, p. 20) | [S3] |
| 90/150 hybrids | maximal-length (primitive characteristic polynomial) hybrids exist under null boundary; no single uniform rule gives maximal length; none exist under periodic boundary | [S4] Section 6.1.1, p. 27 [stated] |

Not found in the sources read:
- The ring-to-row relation for reflection-symmetric rules other than 90. [S3] gives it only for σ automata, i.e. rule 90, and remarks that it "usually does not work" for other automata (pp. 12-13).
- [our remark, unchecked against any source] The argument of [S3] Thm. 6.2 only uses that the rule is mirror-symmetric (f(abc) = f(cba)) and that f(a0a) = 0 for a ∈ {0,1}, i.e. f(000) = f(101) = 0. Rule 150 satisfies both, so the same embedding should hold for rule 150. This would give the null row of n cells as the mirror-symmetric invariant subspace of the ring of 2n + 2 cells. Non-linear symmetric rules with f(000) = f(101) = 0 would also qualify. This needs its own proof or check before use.
- Not found: a proof that null-boundary rule 150 is non-invertible for every n ≡ 2 (mod 3), beyond the numerical tables.
- Not found: cycle-length formulas for rule 150 or rule 60 under null boundary.

### Q3. Reversibility of general (non-additive) ECA under null or fixed boundaries

Known in the sources read:
- Two algorithmic tools:
  - the reachability tree, for a given n, null boundary, uniform or hybrid ECA ([S4] Section 3.3, pp. 13-14; Section 6.2, p. 28);
  - the reversibility graph and circuit graph, giving the full reversibility sequence over all n for null or periodic boundary ([S5] Theorems 1-5, pp. 5-8). Theorem 4 of [S5] is supported by an example only (p. 7), and one Table 1 entry conflicts with [S1] (see [S5] above).
- Classification [stated]: only 62 of the 256 rules can occur in a reversible null-boundary rule vector, against 70 under periodic boundary ([S4] p. 28, Tables 3-4).
- [S5] reports that most non-linear finite ECA have reversibility period 1, i.e. are irreversible for all large n (p. 9) [numerical].
- Reflecting boundary is defined in [S4] (p. 7). [S5] says its algorithm also applies to reflective boundaries without giving details (p. 3).

Not found in the sources read:
- explicit per-rule lists of which uniform non-linear ECA are bijective under null boundary for which n (the 62-rule list is about rule vectors, and the tables in [S4] give the classes but not per-n results);
- any treatment of fixed boundary value 1, other than [S7]'s observations;
- results for reflecting boundaries beyond definitions.

### Q4. Noisy or probabilistic CA with fixed boundaries; stochastic stability on a path

Known in the sources read:
- The Freidlin-Wentzell tree representation of the stationary measure, and the rule that only noise-free recurrent classes can be stochastically stable, apply to any finite state space Ω = 2^Λ with Λ a finite subset of any graph ([S9] Section 7, pp. 22-24). Nothing in that formulation requires periodic boundaries.
- All spatial examples in [S9] Section 9.4 (pp. 38-41) use periodic boundary (a ring). One of them shows that the selected state can change with the number of players n (Thm. 18, p. 39; remark p. 40). This parallels the ring-size dependence in the note but is not about ECA.
- For noisy CA on the infinite lattice Z^d, [S8] proves ergodicity for broad classes, including XOR (additive) CA under zero-range noise and surjective CA under additive noise in the shift-invariant sense ([S8] Section 2.4, p. 8). That setting has no boundaries and does not address the zero-noise limit on finite rows.

Not found in the sources read:
- any work on noise-selected (stochastically stable) cycles of ECA, or of any deterministic CA, on a finite row with null or fixed boundaries;
- any stochastic-stability result for local-interaction games or CA on a path graph with endpoints, as opposed to a cycle;
- the original Freidlin-Wentzell, Young (1993), Kandori-Mailath-Rob (1993) and Ellison (1993, 2000) texts could not be obtained in this session, so nothing is reported from them.

---

## 3. BibTeX

```bibtex
@article{MartinDelRey2015rule90,
  author  = {Mart{\'\i}n del Rey, {\'A}ngel},
  title   = {A note on the reversibility of the elementary cellular automaton with rule number 90},
  journal = {Revista de la Uni{\'o}n Matem{\'a}tica Argentina},
  volume  = {56},
  number  = {1},
  pages   = {107--125},
  year    = {2015},
  url     = {https://inmabb.criba.edu.ar/revuma/pdf/v56n1/v56n1a06.pdf}
}

@article{Tadaki1994orbits,
  author  = {Tadaki, Shin-ichi},
  title   = {Orbits in one-dimensional finite linear cellular automata},
  journal = {Physical Review E},
  volume  = {49},
  number  = {2},
  pages   = {1168--1173},
  year    = {1994},
  doi     = {10.1103/PhysRevE.49.1168},
  eprint  = {cond-mat/9305012},
  archivePrefix = {arXiv}
}

@article{VadaliTurner2026sigma,
  author  = {Vadali, Avi and Turner, Ari M.},
  title   = {Equality of cycle lengths in one- and two-dimensional $\sigma$ automata},
  journal = {Theoretical Computer Science},
  volume  = {1074},
  pages   = {115897},
  year    = {2026},
  doi     = {10.1016/j.tcs.2026.115897},
  eprint  = {2502.10898},
  archivePrefix = {arXiv}
}

@article{Bhattacharjee2020survey,
  author  = {Bhattacharjee, Kamalika and Naskar, Nazma and Roy, Souvik and Das, Sukanta},
  title   = {A survey of cellular automata: types, dynamics, non-uniformity and applications},
  journal = {Natural Computing},
  volume  = {19},
  number  = {2},
  pages   = {433--461},
  year    = {2020},
  doi     = {10.1007/s11047-018-9696-8},
  eprint  = {1607.02291},
  archivePrefix = {arXiv}
}

@article{Wang2025twographs,
  author  = {Wang, Chen and Ma, Junchi and Wang, Chao and Lin, Defu and Chen, Weilin},
  title   = {Two graphs: Resolving the periodic reversibility of one-dimensional finite cellular automata},
  journal = {Applied Mathematics and Computation},
  volume  = {489},
  pages   = {129151},
  year    = {2025},
  doi     = {10.1016/j.amc.2024.129151},
  eprint  = {2402.05404},
  archivePrefix = {arXiv}
}

@article{Sfairopoulos2023newmanmoore,
  author  = {Sfairopoulos, Konstantinos and Causer, Luke and Mair, Jamie F. and Garrahan, Juan P.},
  title   = {Boundary conditions dependence of the phase transition in the quantum {Newman}-{Moore} model},
  journal = {Physical Review B},
  volume  = {108},
  pages   = {174107},
  year    = {2023},
  doi     = {10.1103/PhysRevB.108.174107},
  eprint  = {2301.02826},
  archivePrefix = {arXiv}
}

@article{Salman2013boundary,
  author  = {Salman, K.},
  title   = {Analysis of elementary cellular automata boundary conditions},
  journal = {International Journal of Computer Science \& Information Technology},
  volume  = {5},
  number  = {4},
  pages   = {35--51},
  year    = {2013},
  doi     = {10.5121/ijcsit.2013.5403}
}

@article{Marcovici2019ergodicity,
  author  = {Marcovici, Ir{\`e}ne and Sablik, Mathieu and Taati, Siamak},
  title   = {Ergodicity of some classes of cellular automata subject to noise},
  journal = {Electronic Journal of Probability},
  volume  = {24},
  pages   = {paper no. 41, 1--44},
  year    = {2019},
  doi     = {10.1214/19-EJP297},
  eprint  = {1712.05500},
  archivePrefix = {arXiv}
}

@incollection{Miekisz2008egt,
  author    = {Mi{\k{e}}kisz, Jacek},
  title     = {Evolutionary game theory and population dynamics},
  booktitle = {Multiscale Problems in the Life Sciences},
  editor    = {Capasso, Vincenzo and Lachowicz, Miros{\l}aw},
  series    = {Lecture Notes in Mathematics},
  volume    = {1940},
  pages     = {269--316},
  publisher = {Springer},
  address   = {Berlin, Heidelberg},
  year      = {2008},
  doi       = {10.1007/978-3-540-78362-6_5},
  eprint    = {q-bio/0703062},
  archivePrefix = {arXiv}
}
```
