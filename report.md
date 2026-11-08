# Noise-selected cycles and the small-noise order of rule identifiability in elementary cellular automata

Work report for the proposed v0.2 of *Rule identifiability in elementary cellular automata under dynamical noise* (F. Peterlein, v0.1, concept DOI [10.5281/zenodo.23399100](https://doi.org/10.5281/zenodo.23399100)). Branch `noise-selected-cycles`. Every number below is generated from the files in `data/` by `code/fw/make_report.py`; the predictions were sealed in `PREDICTIONS.md` (first commit of the branch) before the solver existed.

## 1. Question

For every elementary rule on a ring of n cells under i.i.d. bit-flip noise (X_{t+1} = F(X_t) XOR Z_t, Z_t i.i.d. Bernoulli(ε) per cell): which cycles of the deterministic map F are noise-selected (stochastically stable); does their union cover all eight neighbourhood codes; hence does the identifiability rate ρ(f;ε) = λ(ε)·min_c ν_c(f;ε) grow without bound or vanish as ε → 0, and if it vanishes, at which order k*? v0.1 proved ρ → 0 for 42 classes and left the other 46 (whose cycles jointly cover all codes) to a numerical trend (19 falling, 27 rising) at n = 12.

Not in scope: unknown ε, partial observation, generators outside the family, decoder error rates, any change to v0.1's definitions or numbers.

## 2. Verdict

**(a) Exact classification for n = 12 and for every n from 4 to 20.** For each of the 88 classes and each ring size n = 4-20, the noise-selected cycles, the orders k_c of all eight expected code counts and k* = max_c k_c are computed exactly in integer arithmetic. ρ → ∞ iff k* = 0; otherwise ρ(f;ε) ~ a·ε^{k*}·log(1/ε) with a > 0. Certificates (optimal in-tree hierarchy with dual values, witness trajectories) were written for n = 12 and n ≤ 14 and accepted by an independent checker (88 + 898 certificates, 0 failed). The classification depends on n: for n ≥ 8, 20 classes have k* = 0 at every computed n, 55 have k* ≥ 1 at every computed n, and 13 switch between the two (Section 7; patterns observed, not proved).

**(b) v0.1's open item at n = 12 is settled.** Of the 46 classes whose cycles jointly cover all codes, 28 have k* = 0 (ρ → ∞) and 18 have k* ≥ 1 (ρ → 0). 87 of 88 classes agree with v0.1's trend classification; the exception is class 106, which v0.1 lists as falling with an interior maximum and which in fact has k* = 0: its rate falls between ε = 0.01 and 0.001 and then rises again, as log(1/ε), at noise levels far below v0.1's grid. Rules 7, 19, 23 and 232 (v0.1's weakest cases) all have k* = 1: their trend classification stands.

**(c) Classes that resist:** none within the computed range. The wall for larger n is stated in Section 7.

## 3. Method

**Perturbed chain.** For 0 < ε < 1/2 the kernel is P_ε(x,y) = ε^{r(x,y)} (1−ε)^{n−r(x,y)} with resistance r(x,y) = H(F(x), y); r(x, F(x)) = 0. The chain is irreducible. By the Markov chain tree theorem (Pitman and Tang 2018, Thm 1.1) π_ε(x) is a ratio of sums over spanning in-trees of products of P_ε; each product is a polynomial in ε with lowest term ε^{r(T)} and coefficient +1, so no cancellation occurs and **ord π_ε(x) = W(x) − min_y W(y)** exactly, W(x) the minimum total resistance of an in-tree rooted at x.

**Reduction to cycles.** Let C_1..C_m be the cycles of F, R(u→v) the minimum path resistance, V(C,C') = R(C→C') (motion along a cycle is free, so R from any point of C is the same), and γ(C) the minimum weight of an in-tree on the cycles rooted at C with weights V. Then **W(x) − min W = min_C [γ(C) + R(C→x)] − min_C γ(C)** for every state x. Proof (ours; the Freidlin–Wentzell and Young sources could not be read, see Section 8): (i) censor the chain on K' = {cycle states} ∪ {x}; the censored law is π_ε restricted to K' and renormalised, its transition probabilities are convergent power series (any 2^n consecutive steps outside K' contain a flip) with positive leading coefficient, of order equal to the minimum resistance of paths avoiding K' in between; v0.1's Lemma 3 gives π_ε(K') → 1. (ii) Apply the tree theorem on K'; edges inside a cycle cost 0, so contract each cycle; replacing edge weights by shortest-path weights does not change the minimum in-tree value. (iii) In a minimum in-tree on {C_1..C_m, x} rooted at x, let S be the cycles pointing to x and C_x the cycle that x flows to at cost 0; redirect every member of S other than one (C_x if C_x ∈ S, otherwise the member on C_x's branch) to C_x, which costs no more because V(C', C_x) ≤ R(C'→x), and creates no cycle; the result is an in-tree on the cycles rooted at some C plus the edge C→x. The converse inequality is concatenation of a tree and a path. The formula is checked exactly against minimum in-trees on the full state graph for every state, all rules, n ≤ 5 (networkx), the 88 classes at n = 6 (networkx) and all rules for n ≤ 8 (the contraction below): 0 mismatching states.

**Resistances.** R(C→·) for all states by a 0-1 BFS on the state graph with edges x → F(x) (cost 0) and x → x XOR e_i (cost 1). This equals the two-layer graph (state → pre-noise point F(state) at cost 0, single flips between pre-noise points at cost 1, pre-noise point → state at cost 0), because a pre-noise point z is reached at the same cost as the state z whenever the sources are whole cycles. One BFS per rotation orbit of cycles; rows of the other members follow by rotation. Each BFS stops once every cycle and every code has been reached.

**Stochastic potentials of all cycles at once.** A root-free Edmonds contraction (path-growing variant, meldable heaps merged small-to-large, edges generated lazily by weight level with one sentinel per node standing for its unexpanded levels) produces a laminar family of sets X with dual values y_X ≥ 0 and one selected edge per set. With T = Σ y and D(r) = Σ_{X∋r} y_X, **γ(r) = T − D(r) for every root r**. Certificate: (1) each selected edge leaves its set and is tight, V(t_X, h_X) = Σ_{S∋t_X, S⊆X} y_S; (2) within every contracted set the children's selected edges form one directed cycle; (3) Σ_{S∋C, S∌C'} y_S ≤ V(C,C') for all C ≠ C'. (1)+(2) give an in-tree of weight T − D(r) for every r (top-down expansion: in a set with sink s, the child containing s keeps it, every other child Y uses its selected edge and takes its tail as sink; every non-chain set is left by exactly one tree edge and no chain set is left), and (3) gives the matching lower bound. Then k_c = min_C [γ(C) + R(C→D_c)] − min γ, D_c the states containing code c, and k* = max_c k_c. Since ν_c = Σ_x π_ε(x) n_c(x) is a rational function of ε with positive leading coefficient, ν_c ~ a_c ε^{k_c}, and ρ = λ·min_c ν_c with λ(ε) ~ log(1/ε).

**Bijective and affine rules.** If F is a bijection the kernel is doubly stochastic, the uniform law is stationary, every cycle is noise-selected and k* = 0. For affine F(x) = Lx + b over GF(2), v0.1's Walsh identity π̂(χ) = (1−2ε)^{|χ|}(−1)^{χ·b} π̂(Lᵀχ) gives uniform three-cell marginals (ν_c = n/8 at every ε, so k* = 0) iff no nonzero character supported on three adjacent cells lies in the generalised kernel of Lᵀ; this is checked by GF(2) linear algebra for n = 4..64 (`data/fw_affine.csv`).

## 4. Verification (before any class was classified)

- **(a) High-precision stationary laws.** GTH elimination (subtraction-free) at ε = 10^-3 … 10^-12 for all 256 rules, n = 3..10 (2048 (rule, n) pairs): the slope of log π_ε(x) between the two smallest noise levels equals the predicted integer order for every state (largest deviation 5.3e-08), and likewise for every ν_c (largest deviation 4.1e-09); 0 failures. The task asked for n ≤ 8; n = 9, 10 were affordable. n = 11 was stopped on the load budget.
- **(a') Exact trees.** Minimum in-trees on the full state graph, 2392 (n, rule, method) rows, 0 mismatching states; min W = min γ in every case: True.
- **(b) n = 12 against v0.1's trend.** 87/88 agree; the exception (class 106) is explained in Section 5 by GTH solves at n = 12 down to ε = 1e-09. GTH at n = 12 with ε = 10^-4 … 10^-7 for classes 106, 7, 19, 23, 232, 41, 200, 30, 22, 108: largest deviation of the observed ν_c order from the predicted k_c 1.7e-03.
- **(c) All 256 rules independently at n = 12:** symmetry consistency (k_c permuted under reflection and complementation, same γ profile, same number of selected cycles) 256/256.
- **(d)** the 138 rules of v0.1's 42 proved-falling classes have k* ≥ 1: 138/138; bijective rules have k* = 0: 6/6.
- **Certificates.** n = 12: 88 checked, 0 failed; sweep n = 4..14 (non-bijective classes): 898 checked, 0 failed. The checker (`code/fw/check_cert.py`) uses its own successor map, its own cycle enumeration and scipy Dijkstra on the explicit two-layer graph; it rejects tampered certificates (test).
- **Regression tests.** `code/fw/test_fw.py`: 12 test functions, 17 test cases passed, 0 failed (`data/log_fw_pytest.txt`). Every defect found during the work has a permanent test:
  - BUG-1: lazy levels started at weight 1, so zero-resistance edges u -> F(u) were never inserted; the contraction was wrong on the full state graph (not on cycle graphs, where V >= 1).
  - BUG-2: a torn last line swallowed the next appended record.
  - BUG-3: a multiprocessing Pool launched from a script read on stdin hangs on macOS; with one worker the n = 12 GTH check must not create a Pool.
  - BUG-4: the checker crashed (instead of rejecting) on a certificate with a truncated cycle list or with a k* inconsistent with its other fields.
  - PERF-1: an intermediate version raised one node per refinement round and recomputed the whole hierarchy (rule 108 at n = 12 needed > 100 rounds). The contraction must be a single pass.
  - PERF-2: merging heaps by re-heapifying the large heap made rule 76 at n = 16 take 52 s.
  - PERF-3: one explicit in-tree per noise-selected cycle made certificates quadratic in the number of cycles (rule 76 at n = 13: 422 s); the hierarchy certificate covers all roots at once.
- **Process finding.** The first run of verifier (a) used a superseded solver version (its worker processes had loaded the code before a rewrite). It was discarded (`data/cache/stale/`, not committed) and verifier (a) was split into a solver-independent stage (GTH slopes, cached) and a comparison stage that re-runs the current solver; the reported results are from the current solver.
- **Checkpointing.** Append-only fsynced JSON lines; a sweep killed after 5 s and resumed gave a byte-identical table to an uninterrupted run (sha256 78b6a9a00ce6cb21… for both; `data/log_fw_resume_test.txt`).

## 5. n = 12: all 88 classes, line by line against v0.1

v0.1 B classes (42): k* = 1 for 29, 2 for 5, 3 for 8. v0.1 U-falling (19): k* = 0 for 1, 1 for 17, 2 for 1. v0.1 U-rising (27): k* = 0 for 27.

**Class 106.** 35 of its 37 cycles are noise-selected, among them cycles carrying all eight codes, so k* = 0. High-precision solves give min_c ν_c = 0.06653, 0.04909, 0.04736, 0.04719, 0.04717, 0.04717 at ε = 0.0001, 1e-05, 1e-06, 1e-07, 1e-08, 1e-09: the limit is about 0.0472 > 0, approached with a linear correction about 4102 times the limit. v0.1's interior maximum ε* = 0.0095, ρ* = 6.189 is a local maximum; ρ ≈ 0.0472·log(1/ε) exceeds ρ* again only for ε below about 10^-57. In v0.1's table the entry should carry the dagger (local maximum).

**Weak cases.** Rule 7: k* = 1, noise-selected cycles (smallest state/period) 0/p2, codes with k_c = k*: 001,010,011,100,101,110. Rule 19: k* = 1, noise-selected cycles (smallest state/period) 0/p2, codes with k_c = k*: 001,010,011,100,101,110. Rule 23: k* = 1, noise-selected cycles (smallest state/period) 0/p2, codes with k_c = k*: 001,010,011,100,101,110. Rule 232: k* = 1, noise-selected cycles (smallest state/period) 0/p1;4095/p1, codes with k_c = k*: 001,010,011,100,101,110.

Columns: v0.1 type and trend ratio ρ(0.002)/ρ(0.001); expected ratio 2^{k*}·λ(0.002)/λ(0.001); k* and k_c (codes 000..111); number of cycles and of noise-selected cycles; for k* ≥ 1 the codes with k_c = k* (uncovered), for k* = 0 a set of noise-selected cycles covering all codes (smallest state/period).

| class | v0.1 | v0.1 ratio | expected | k* | k_c | cycles | selected | uncovered codes / covering cycles | agree |
|---:|---|---:|---:|---:|---|---:|---:|---|---|
| 0 | B | 7.182 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 1 | 1 | 111 | yes |
| 1 | B | 1.792 | 1.795 | 1 | 0-0-0-0-0-1-0-0 | 162 | 162 | 101 | yes |
| 2 | B | 3.590 | 3.591 | 2 | 0-0-0-1-0-1-1-2 | 11 | 11 | 111 | yes |
| 3 | B | 1.793 | 1.795 | 1 | 0-0-0-0-0-1-0-0 | 39 | 39 | 101 | yes |
| 4 | B | 1.810 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 322 | 322 | 011,110,111 | yes |
| 5 | U-rising | 0.901 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 435 | 435 | 1/p2 | yes |
| 6 | B | 1.799 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 28 | 28 | 111 | yes |
| 7 | U-falling | 1.822 | 1.795 | 1 | 0-1-1-1-1-1-1-0 | 10 | 1 | 001,010,011,100,101,110 | yes |
| 8 | B | 7.203 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 1 | 1 | 111 | yes |
| 9 | U-rising | 0.889 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 14 | 13 | 11/p12 | yes |
| 10 | B | 1.799 | 1.795 | 1 | 0-0-0-0-0-1-0-1 | 31 | 31 | 101,111 | yes |
| 11 | B | 1.797 | 1.795 | 1 | 1-0-1-0-0-1-0-1 | 32 | 1 | 000,010,101,111 | yes |
| 12 | B | 1.806 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 322 | 322 | 011,110,111 | yes |
| 13 | B | 1.789 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 30 | 2 | 000,001,011,100,110,111 | yes |
| 14 | B | 1.782 | 1.795 | 1 | 1-0-1-0-0-1-0-1 | 36 | 1 | 000,010,101,111 | yes |
| 15 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 352 | 352 | all | yes |
| 18 | B | 1.807 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 20 | 18 | 111 | yes |
| 19 | B | 1.797 | 1.795 | 1 | 0-1-1-1-1-1-1-0 | 162 | 1 | 001,010,011,100,101,110 | yes |
| 22 | U-rising | 0.947 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 23 | 19 | 15/p5 | yes |
| 23 | U-falling | 1.796 | 1.795 | 1 | 0-1-1-1-1-1-1-0 | 164 | 1 | 001,010,011,100,101,110 | yes |
| 24 | B | 3.587 | 3.591 | 2 | 0-0-0-1-0-1-1-2 | 11 | 11 | 111 | yes |
| 25 | U-rising | 0.900 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 21 | 19 | 11/p24 | yes |
| 26 | B | 1.783 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 64 | 64 | 111 | yes |
| 27 | U-rising | 0.901 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 44 | 44 | 1/p24 | yes |
| 28 | B | 1.790 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 75 | 2 | 000,001,011,100,110,111 | yes |
| 29 | U-rising | 0.899 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 751 | 751 | 1/p2 | yes |
| 30 | U-rising | 0.954 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 12 | 7 | 9/p102 | yes |
| 32 | B | 7.210 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 2 | 1 | 111 | yes |
| 33 | U-falling | 1.795 | 1.795 | 1 | 0-0-0-0-0-1-0-0 | 163 | 162 | 101 | yes |
| 34 | B | 1.806 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 31 | 31 | 011,110,111 | yes |
| 35 | U-falling | 1.763 | 1.795 | 1 | 0-0-0-0-0-1-0-0 | 42 | 39 | 101 | yes |
| 36 | B | 1.795 | 1.795 | 1 | 0-0-0-1-0-1-1-1 | 98 | 98 | 011,101,110,111 | yes |
| 37 | U-rising | 0.916 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 58 | 55 | 65/p6 | yes |
| 38 | B | 1.792 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 52 | 52 | 111 | yes |
| 40 | B | 7.253 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 5 | 1 | 111 | yes |
| 41 | U-rising | 0.986 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 28 | 24 | 1/p12 | yes |
| 42 | B | 1.795 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 132 | 132 | 111 | yes |
| 43 | U-falling | 1.752 | 1.795 | 1 | 1-0-1-0-0-1-0-1 | 61 | 1 | 000,010,101,111 | yes |
| 44 | B | 1.795 | 1.795 | 1 | 0-0-0-1-0-1-1-1 | 99 | 98 | 011,101,110,111 | yes |
| 45 | U-rising | 0.915 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 33 | 33 | 11/p156 | yes |
| 46 | B | 1.792 | 1.795 | 1 | 0-0-1-0-0-0-0-1 | 11 | 10 | 010,111 | yes |
| 50 | B | 1.790 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 163 | 1 | 000,001,011,100,110,111 | yes |
| 51 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 2048 | 2048 | all | yes |
| 54 | U-rising | 0.850 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 33 | 24 | 65/p4 | yes |
| 56 | B | 1.796 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 34 | 31 | 011,110,111 | yes |
| 57 | U-falling | 1.843 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 8 | 1 | 000,001,011,100,110,111 | yes |
| 58 | U-falling | 1.786 | 1.795 | 1 | 1-1-1-0-1-0-0-1 | 9 | 1 | 000,001,010,100,111 | yes |
| 60 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 24 | 24 | 17/p12 | yes |
| 62 | U-rising | 0.901 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 92 | 51 | 195/p3 | yes |
| 72 | B | 3.598 | 3.591 | 2 | 0-1-1-1-1-2-1-2 | 98 | 1 | 101,111 | yes |
| 73 | U-rising | 0.860 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 162 | 158 | 3/p5 | yes |
| 74 | U-rising | 0.899 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 29 | 26 | 7/p12 | yes |
| 76 | B | 1.795 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 1499 | 1499 | 111 | yes |
| 77 | U-falling | 1.796 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 325 | 2 | 000,001,011,100,110,111 | yes |
| 78 | B | 1.783 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 30 | 2 | 000,001,011,100,110,111 | yes |
| 90 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 70 | 70 | 119/p4 | yes |
| 94 | U-falling | 1.738 | 1.795 | 1 | 1-1-1-0-1-0-0-1 | 147 | 3 | 000,001,010,100,111 | yes |
| 104 | U-falling | 3.627 | 3.591 | 2 | 0-1-1-1-1-2-1-2 | 50 | 1 | 101,111 | yes |
| 105 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 10 | 10 | 273/p2;819/p1;1911/p2 | yes |
| 106 | U-falling | 1.689 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 37 | 35 | 13/p168 | **no** |
| 108 | U-rising | 0.921 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 674 | 672 | 5/p2 | yes |
| 110 | U-rising | 0.882 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 11 | 8 | 103/p9 | yes |
| 122 | U-rising | 0.866 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 21 | 19 | 7/p14;1365/p2 | yes |
| 126 | B | 1.790 | 1.795 | 1 | 0-0-1-0-0-0-0-0 | 20 | 18 | 010 | yes |
| 128 | B | 7.182 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 2 | 1 | 111 | yes |
| 130 | B | 3.594 | 3.591 | 2 | 0-0-0-1-0-1-1-2 | 12 | 11 | 111 | yes |
| 132 | B | 1.811 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 323 | 322 | 011,110,111 | yes |
| 134 | U-falling | 1.802 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 29 | 28 | 111 | yes |
| 136 | B | 7.225 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 2 | 1 | 111 | yes |
| 138 | B | 1.794 | 1.795 | 1 | 0-0-0-0-0-1-0-0 | 77 | 76 | 101 | yes |
| 140 | B | 1.815 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 323 | 322 | 011,110,111 | yes |
| 142 | U-falling | 1.752 | 1.795 | 1 | 1-0-1-0-0-1-0-1 | 61 | 1 | 000,010,101,111 | yes |
| 146 | U-falling | 1.815 | 1.795 | 1 | 0-0-0-0-0-0-0-1 | 21 | 18 | 111 | yes |
| 150 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 10 | 10 | 273/p2 | yes |
| 152 | B | 3.607 | 3.591 | 2 | 0-0-0-1-0-1-1-2 | 12 | 11 | 111 | yes |
| 154 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 308 | 308 | 3/p24 | yes |
| 156 | U-falling | 1.821 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 76 | 2 | 000,001,011,100,110,111 | yes |
| 160 | B | 7.210 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 3 | 1 | 111 | yes |
| 162 | B | 1.804 | 1.795 | 1 | 0-0-0-1-0-0-1-1 | 32 | 31 | 011,110,111 | yes |
| 164 | U-falling | 1.801 | 1.795 | 1 | 0-0-0-1-0-1-1-1 | 108 | 98 | 011,101,110,111 | yes |
| 168 | B | 7.283 | 7.182 | 3 | 0-1-1-2-1-2-2-3 | 32 | 1 | 111 | yes |
| 170 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 352 | 352 | all | yes |
| 172 | U-falling | 1.805 | 1.795 | 1 | 0-0-0-1-0-1-1-1 | 109 | 98 | 011,101,110,111 | yes |
| 178 | U-falling | 1.796 | 1.795 | 1 | 1-1-0-1-1-0-1-1 | 164 | 1 | 000,001,011,100,110,111 | yes |
| 184 | U-rising | 0.916 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 61 | 61 | 5/p12;1367/p12 | yes |
| 200 | B | 2.222 | 1.795 | 1 | 0-1-1-1-1-1-1-1 | 853 | 1 | 001,010,011,100,101,110,111 | yes |
| 204 | U-rising | 0.898 | 0.898 | 0 | 0-0-0-0-0-0-0-0 | 4096 | 4096 | all | yes |
| 232 | U-falling | 1.796 | 1.795 | 1 | 0-1-1-1-1-1-1-0 | 325 | 2 | 001,010,011,100,101,110 | yes |

## 6. Predictions (sealed) against outcome

1. Survival at n = 12: predicted 27/27 rising and 19/19 falling U classes survive. Outcome: 27/27 rising and 18/19 falling survive; the flip (106) was falling → rising, a direction the predictions did not name.
2. Rules 7, 19, 23, 232 do not flip and have k* = 1: confirmed (k* = 1, 1, 1, 1).
3. Per-class orders k_pred from the v0.1 trend: 87/88 correct (miss: 106). Rule 200 (low confidence): k* = 1.
4. B classes k* ≥ 1 with distribution 29/5/8 for k* = 1/2/3: outcome 29/5/8.
5. Dependence on n. (a) Classes 60 and 90 have k* >= 1 exactly at the powers of two: solver over n = 4-20: confirmed for both; the GF(2) analysis gives uniform marginals (k* = 0) at every other n = 4..64. (b) Bijective classes k* = 0 at every n: confirmed. (c) 'at most about 10 classes change with n, at least 70 keep their n = 12 classification for every n ≥ 8': 13 change and 75 keep it — the first half is wrong, the second holds. (d) small rings deviate more: 27 classes differ at some n = 4-7 from their n = 12 status, against 13 that vary for n ≥ 8. (e) where k* ≥ 1 for all n ≥ 8, the value is constant in n for 53 of 55 classes.
6. Cost wall: see Section 7.

## 7. Ring sizes

Number of classes with k* = 0 per n: n=4: 16, n=5: 26, n=6: 22, n=7: 30, n=8: 24, n=9: 27, n=10: 30, n=11: 32, n=12: 28, n=13: 30, n=14: 30, n=15: 27, n=16: 25, n=17: 32, n=18: 29, n=19: 30, n=20: 30.

Classes whose k* = 0 / k* ≥ 1 status changes for n ≥ 8 (n = 8-20):

| class | n with k* = 0 | n with k* ≥ 1 | pattern (observed) |
|---:|---|---|---|
| 22 | 9-13, 17-20 | 8, 14-16 | none of: divisibility by d <= 8, powers of two |
| 26 | 11, 14, 17, 20 | 8-10, 12-13, 15-16, 18-19 | none of: divisibility by d <= 8, powers of two |
| 35 | 8, 10-11, 13-14, 16-17, 19-20 | 9, 12, 15, 18 | k* >= 1 iff 3 divides n |
| 37 | 11-12, 17-18 | 8-10, 13-16, 19-20 | none of: divisibility by d <= 8, powers of two |
| 43 | 9-11, 13-15, 17-19 | 8, 12, 16, 20 | k* >= 1 iff 4 divides n |
| 45 | 9-20 | 8 | none of: divisibility by d <= 8, powers of two |
| 60 | 9-15, 17-20 | 8, 16 | k* >= 1 iff 8 divides n / k* >= 1 iff n is a power of two |
| 73 | 8, 10-20 | 9 | none of: divisibility by d <= 8, powers of two |
| 90 | 9-15, 17-20 | 8, 16 | k* >= 1 iff 8 divides n / k* >= 1 iff n is a power of two |
| 94 | 8, 10-11, 13-14, 16-17, 19-20 | 9, 12, 15, 18 | k* >= 1 iff 3 divides n |
| 122 | 8, 12, 16, 20 | 9-11, 13-15, 17-19 | k* = 0 iff 4 divides n |
| 142 | 9-11, 13-15, 17-19 | 8, 12, 16, 20 | k* >= 1 iff 4 divides n |
| 154 | 9-15, 17-20 | 8, 16 | k* >= 1 iff 8 divides n / k* >= 1 iff n is a power of two |

Affine classes (GF(2) analysis, n = 4..64): class 0: marginals not uniform at n = 4-64, bijective at n = none; class 15: marginals not uniform at n = none, bijective at n = 4-64; class 51: marginals not uniform at n = none, bijective at n = 4-64; class 60: marginals not uniform at n = 4, 8, 16, 32, 64, bijective at n = none; class 90: marginals not uniform at n = 4, 8, 16, 32, 64, bijective at n = none; class 105: marginals not uniform at n = 6, bijective at n = 4-5, 7-8, 10-11, 13-14, 16-17, 19-20, 22-23, 25-26, 28-29, 31-32, 34-35, 37-38, 40-41, 43-44, 46-47, 49-50, 52-53, 55-56, 58-59, 61-62, 64; class 150: marginals not uniform at n = 6, bijective at n = 4-5, 7-8, 10-11, 13-14, 16-17, 19-20, 22-23, 25-26, 28-29, 31-32, 34-35, 37-38, 40-41, 43-44, 46-47, 49-50, 52-53, 55-56, 58-59, 61-62, 64; class 170: marginals not uniform at n = none, bijective at n = 4-64; class 204: marginals not uniform at n = none, bijective at n = 4-64. Consistency with the solver where the analysis gives k* = 0: 128/128.

Cost per ring size (2 worker processes; CPU seconds summed over the 88 classes, longest single job, largest peak memory of a job, largest number of cycles of a non-bijective class):

| n | CPU s | longest job s | peak MB | max cycles |
|---:|---:|---:|---:|---:|
| 4 | 0 | 0.0 | 73 | 11 |
| 5 | 0 | 0.0 | 75 | 21 |
| 6 | 0 | 0.0 | 77 | 39 |
| 7 | 0 | 0.0 | 78 | 71 |
| 8 | 0 | 0.0 | 75 | 131 |
| 9 | 0 | 0.0 | 75 | 241 |
| 10 | 1 | 0.0 | 74 | 443 |
| 11 | 2 | 0.1 | 74 | 815 |
| 12 | 4 | 0.2 | 76 | 1499 |
| 13 | 7 | 0.5 | 77 | 2757 |
| 14 | 18 | 1.5 | 86 | 5071 |
| 15 | 10 | 0.9 | 94 | 9327 |
| 16 | 33 | 3.1 | 122 | 17155 |
| 17 | 92 | 11.8 | 210 | 31553 |
| 18 | 361 | 37.5 | 404 | 58035 |
| 19 | 1052 | 131.3 | 1068 | 106743 |
| 20 | 4416 | 510.4 | 2554 | 196331 |

**Where the wall is.** n = 20 is the largest ring size computed: 4416 CPU seconds for the 88 classes, longest job 510 s (class 76), largest peak memory 2554 MB (class 76). Cost grows by a factor 14 (median over the 6 heaviest classes) from n = 18 to 20; extrapolated with each class's own factor, n = 22 needs about 16.0 CPU hours, i.e. about 8.0 h wall at 2 workers. The memory wall is the stored distance rows (one byte per cycle per rotation orbit): at n = 22 class 76 has 664183 cycles in 30229 rotation orbits, 20.1 GB of rows. Both are properties of this implementation (dense V rows per orbit, one BFS over all 2^n states per orbit), not of the rules; keeping only the weight levels the contraction actually expands (and recomputing a row on demand) would reduce the memory term; the BFS term (orbits x 2^n) remains.

| class | cycles n=20 | orbits n=20 | CPU s n=20 | peak MB n=20 | cycles n=22 | orbits n=22 | CPU s n=22 (est.) | V rows GB n=22 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 76 | 196331 | 9844 | 510 | 2554 | 664183 | 30229 | 6942 | 20.1 |
| 154 | 41626 | 10904 | 503 | 1208 | 76600 | 38328 | 8873 | 2.9 |
| 42 | 9844 | 9844 | 494 | 544 | 30229 | 30229 | 7565 | 0.9 |
| 29 | 98167 | 4935 | 247 | 871 | 332093 | 15134 | 3396 | 5.0 |
| 138 | 3855 | 3855 | 227 | 449 | 10764 | 10764 | 3295 | 0.1 |
| 200 | 76725 | 3855 | 195 | 830 | 236282 | 10764 | 2361 | 2.5 |

Full k* table (rows: class; columns: n):

| class | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 4 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 5 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 6 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 7 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 8 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 9 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 10 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 11 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 12 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 13 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 14 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 15 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 18 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 |
| 19 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 22 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 0 | 0 |
| 23 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 24 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 25 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 26 | 2 | 0 | 1 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 0 | 1 | 2 | 0 | 1 | 1 | 0 |
| 27 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 28 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 29 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 30 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 32 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 33 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 34 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 35 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 36 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 37 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 0 | 0 | 1 | 1 | 1 | 1 | 0 | 0 | 1 | 1 |
| 38 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 40 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 41 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 42 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 43 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 44 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 45 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 46 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 50 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 51 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 54 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 56 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 57 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 58 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 60 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 62 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 72 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 73 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 74 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 76 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 77 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 78 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 90 | 2 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 0 |
| 94 | 1 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 1 | 0 | 0 |
| 104 | 1 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 105 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 106 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 108 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 110 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 122 | 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0 |
| 126 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 128 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 130 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 132 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 134 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 136 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 138 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 140 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 142 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 1 |
| 146 | 2 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 2 | 2 | 1 | 1 | 1 | 1 |
| 150 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 152 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |
| 154 | 1 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 156 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 160 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 162 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 164 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 168 | 1 | 2 | 2 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| 170 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 172 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 178 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 184 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 200 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 204 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 232 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

## 8. Literature

The full literature note, with read/not-read status per source and BibTeX, is `literature.md`. In short:

- **Computed before?** No computation of Freidlin–Wentzell/Young stochastic potentials of the cycles of noisy elementary CA on finite rings, or of per-state small-noise orders, was found in the sources searched. This is a provisional finding: it means "not found", not "never done". The closest work is Bagnoli, Baia and Matteuzzi (ACRI 2024, doi:10.1007/978-3-031-71552-5_5; read in the extended arXiv version 2406.15408v2). They cover all 88 classes at L = 17 under "vanishing noise" (at most one flip per step), using a chain between attractors built from single-flip basin jumps. They compute no potentials, no resistances above one and no per-state orders. Their leading-order law on cycles is correct only when the single-flip graph between cycles has one closed class; the present computation does not need that assumption.
- **Related noisy-CA theory, other settings:**
  - Marsan and Sablik (EJP 2025, doi:10.1214/25-EJP1396) and Marcovici, Sablik and Taati (EJP 2019, doi:10.1214/19-EJP297): stochastic stability and ergodicity on the infinite lattice.
  - Bušić, Mairesse and Marcovici (AAP 2013, doi:10.1239/aap/1386857853): a different majority-flip PCA on Z/nZ, with exact invariant measures up to n = 9.
- **Tools used, read in full:**
  - Markov chain tree theorem: Pitman and Tang (Bernoulli 2018, doi:10.3150/16-BEJ916), Thm 1.1 and Thm 3.1; its max-algebra form is Benek Gursoy, Kirkland, Mason and Sergeev (ELA 2013, doi:10.13001/1081-3810.1636), Thm 2.4.
  - Optimum branchings: Edmonds (1967, doi:10.6028/jres.071B.032). His arborescences are out-trees, so in-trees here correspond to reversed edges.
  - Freidlin's cycle hierarchy, computed by graph algorithms: Gan and Cameron (J. Nonlinear Sci. 2017, doi:10.1007/s00332-016-9355-0). Their Algorithm 1 assumes unique optimal W-graphs, which the rotation symmetry of ECA breaks. The present all-roots contraction does not need uniqueness.
- **Not readable here (closed access or blocked by the sandbox):** Young (Econometrica 1993), Kandori, Mailath and Rob (1993), Ellison (1993, 2000), Freidlin and Wentzell ch. 6, Grassmann, Taksar and Heyman (1985), O'Cinneide (1993), Catoni, Trouvé, Wuensche and Lesser (1992), Mairesse and Marcovici (2014). They are cited for attribution of concepts only, never for a statement used in a proof. This is why Section 3 proves the reduction to cycles itself. Nothing relies on the GTH accuracy theorem either: GTH results were cross-checked against dense solves at moderate ε and, through the predicted orders, against exact minimum in-trees.

## 9. What is established, and what is not

Established exactly (integer computation, independently checked certificates where stated): the noise-selected cycles, k_c and k* for all 88 classes at n = 12 (certificates) and for n = 4-20 (certificates for n ≤ 14); the reclassification of class 106; the analytic results for bijective rules (all n) and for the affine rules (n = 4..64). Proved for all n: the order formula for π_ε (tree theorem), its reduction to cycles (Section 3), ρ ~ a ε^{k*} log(1/ε), and the hierarchy certificate lemma. Verified numerically: the predicted orders of every state for n ≤ 10 and for ten classes at n = 12.

Observed, not proved: every statement about how the classification depends on n (Section 7) outside the affine and bijective classes; the divisibility patterns are fitted to the computed range only. Not claimed: anything for n outside the computed range for non-affine classes; the size of the leading coefficient a (it decides at which ε the asymptotic regime starts — for class 106 it starts far below any practical noise level); unknown ε, partial observation, generators outside the family, decoder error rates.

## 10. Reproduction

`reproduce.sh` (v0.1 steps unchanged) followed by `reproduce_v02.sh` (new): verifiers, n = 12 classification, sweep, certificate checks, this report. Code in `code/fw/`; tests `python3 -m pytest -q code/fw/test_fw.py`. Data files and SHA-256 sums in `data/MANIFEST.sha256`.
