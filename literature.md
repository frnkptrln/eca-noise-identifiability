# Literature note for v0.2: stochastic stability of cycles of noisy ECA on finite rings

Scope: ECA on Z/nZ, X_{t+1} = F(X_t) XOR Z_t, Z_t i.i.d. Bernoulli(eps) per cell; resistance r(x->y) = H(F(x), y).
Prepared for the v0.2 report of "Rule identifiability in elementary cellular automata under dynamical noise" (concept DOI 10.5281/zenodo.23399100).

## 0. Access limits and deviations (read first)

- Full text was obtained only through an open-access fetcher (DOI-based). Direct web access from the analysis sandbox was unavailable: arxiv.org, numdam.org, projecteuclid.org and dklevine.com were all refused by the sandbox proxy (hard refusal, not grantable).
- Consequence: **the economics and large-deviation primary sources were NOT read in full text.** This covers Young 1993, Kandori–Mailath–Rob 1993, Ellison 1993/2000, Freidlin–Wentzell ch. 6, Ventcel–Freidlin 1970, Leighton–Rivest, Anantharam–Tsoucas, Chu–Liu, GTH 1985, O'Cinneide 1993, Catoni 1992/1999, Trouvé 1996, Wuensche–Lesser 1992 and Mairesse–Marcovici 2014. They are listed in §2 with bibliographic data only. No theorem number from them is confirmed here, including "Young Theorem 4" and the Freidlin–Wentzell formula W(x) = min_i[W(K_i) + V(K_i,x)].
- Where a full text was read, it was in several cases the arXiv version, not the version of record. This is stated per entry.
- The answer to Q1 rests on the sources in §1 plus web-search metadata. It is **provisional**: "not found in the searched sources", not "never done".
- Correction to the brief: the 2016/2017 J. Nonlinear Sci. paper lists its authors as **Tingyue Gan and Maria Cameron**, in that order. Cite it as Gan & Cameron.
- DOI caveat: 10.1111/1467-937X.00121, tried for Ellison (2000), resolves to a different paper, a "Contagion" working paper. Ellison (2000) is therefore given without a DOI.

## 1. Sources read in full text

**[GC17] T. Gan, M. Cameron, "A graph-algorithmic approach for the study of metastability in Markov chains", J. Nonlinear Sci. (2017). DOI 10.1007/s00332-016-9355-0.** Read: arXiv:1607.00078v2 (27 Nov 2016), 45 pp. Volume and pages were not checked against the publisher record.
- Setting: continuous-time finite Markov chains with rates L_ij ≍ exp(−U_ij/ε). Assumption 1: finite state space. Assumption 2: a unique closed communicating class.
- Def. 2.1: a W-graph with m sinks is an acyclic subgraph in which n−m vertices have exactly one outgoing arc. It is a forest of in-trees. Def. 2.2: an optimal W-graph minimises the sum of arc weights, jointly over the choice of sinks and arcs.
- Thm 2.3 (attributed to Wentzell 1972): eigenvalue exponents Δ_m = V(g*_m) − V(g*_{m+1}). Footnote 1 says Wentzell gave no proof and that the authors know of no published proof.
- Thm 2.4: sharp eigenvalue asymptotics with prefactors under Assumption 3 (all optimal W-graphs unique). Thm 2.5: weak nested property of optimal W-graphs.
- Algorithm 1 extends the "single-sweep" algorithm (their ref. [12], Cameron & Gan 2016, Mol. Simul.; not read). It produces Freidlin's cycle hierarchy and the critical timescales. Worst-case cost is O((nd)² log(nd)) for n vertices and maximum degree d. Algorithm 2 (Sect. 5) drops Assumptions 3–5 to handle symmetric chains.
- Relevance: these are the graph objects behind stochastic potentials, computed by an algorithm. The paper targets eigenvalues and timescales and states no per-state formula for the order of the stationary law. Two points matter for ECA:
  - The noisy ECA chain is invariant under rotations, which typically breaks Assumption 3, so Algorithm 1 is not directly applicable. Algorithm 2, or a direct method, is needed.
  - Here d = 2^n (every state reachable in one step) unless the chain is sparsified, e.g. by the two-layer graph of the brief, which has degree n+1.
- Discrete versus continuous time: πP = π if and only if π(P − I) = 0. The stationary law of our discrete chain therefore equals that of the generator L = P − I, and stationary-law statements transfer exactly.

**[Edm67] J. Edmonds, "Optimum branchings", J. Res. Natl. Bur. Stand. 71B(4) (1967) 233–240. DOI 10.6028/jres.071B.032.** Read: NIST scan of the version of record.
- An arborescence has every edge directed toward a different node; the root has no incoming edge. This is an **out-tree**, with edges pointing away from the root.
- Sect. 2 reduces the problem of a minimum-weight spanning arborescence with prescribed root r to an optimum branching, by negating weights and adding a new edge into r. Sect. 3, Theorem 1: a "good" (polynomial) algorithm exists for optimum branchings.
- Use for us: the in-trees of the Freidlin–Wentzell/Young theory become Edmonds arborescences once every edge is reversed.

**[PT18] J. Pitman, W. Tang, "Tree formulas, mean first passage times and Kemeny's constant of a Markov chain", Bernoulli 24 (2018). DOI 10.3150/16-BEJ916.** Read: arXiv:1603.09017v3 (8 Feb 2018).
- Thm 1.1 (Markov chain tree theorem, irreducible case): Σ_i Σ_i p_ij = Σ_j, where Σ_j is the sum over spanning trees directed toward root j of the product of p over the tree's edges. Hence π_j = Σ_j / Σ_k Σ_k.
- Sect. 3 attributes the irreducible case to Ventcel and Freidlin 1970, "Lemma 7.1" by their citation, and gives a three-sentence proof via cycle-rooted spanning trees.
- Thm 3.1 is the general, not necessarily irreducible, version, attributed to Leighton and Rivest. They mention Anantharam–Tsoucas as an alternative proof.
- This is the source used here for the MCTT statement. The original LR and AT papers were not read.

**[GKMS13] B. Benek Gursoy, S. Kirkland, O. Mason, S. Sergeev, "On the Markov chain tree theorem in the max algebra", Electron. J. Linear Algebra 26 (2013) 15–27. DOI 10.13001/1081-3810.1636.** Read: version of record.
- Thm 1.1 restates the classical MCTT and calls it the Freidlin–Wentzell formula, citing the 1984 English edition of FW.
- Thm 2.4: for an irreducible max-stochastic matrix A (each row has maximum 1), the vector w_i = max over i-trees of the tree weight satisfies A^T ⊗ w = w in the max algebra. Thm 2.5 proves the same by dequantisation.
- Relevance: put a_ij = ε^{r_ij}. The condition min_j r_ij = 0 holds for ECA, because r(x,F(x)) = 0. With these entries Thm 2.4 is the tropical (min-plus) form of the MCTT: V(x) = min over x-trees of total resistance satisfies V(x) = min_y [V(y) + r(y,x)]. That equation alone does not single out V.

**[BMM13] A. Bušić, J. Mairesse, I. Marcovici, "Probabilistic cellular automata, invariant measures, and perfect sampling", Adv. Appl. Probab. 45(4) (2013) 960–980. DOI 10.1239/aap/1386857853.** Read: version of record.
- Thm 3.1: a deterministic CA on Z is ergodic if and only if it is nilpotent. Cor. 3.1: ergodicity is undecidable.
- Sect. 5 treats the "majority-flip" PCA: each cell applies rule 232 with probability α and otherwise flips its own value. On Z/nZ the invariant measure is unique. It is (δ_(01)^{n/2} + δ_(10)^{n/2})/2 for even n and has full support for odd n. Exact invariant measures were computed only up to n = 9.
- This noise model is not ours (it flips the old cell value, not the rule output), and no small-noise selection theory is used.

**[MST19] I. Marcovici, M. Sablik, S. Taati, "Ergodicity of some classes of cellular automata subject to noise", Electron. J. Probab. 24 (2019). DOI 10.1214/19-EJP297.** Read: arXiv:1712.05500 (version dated 25 May 2022).
- Configurations live on the infinite lattice Z^d. The paper proves ergodicity of noisy CA in several families: nilpotent, permutive, gliders, spreading symbol, surjective, algebraic.
- It notes that the only known 1-D CA that stays non-ergodic under small positive noise is Gács's construction.
- It contains no finite-ring stochastic-potential computation and no reference to Freidlin–Wentzell.

**[MS25] H. Marsan, M. Sablik, "Strong stochastic stability of cellular automata", Electron. J. Probab. 30 (2025) 1–32. DOI 10.1214/25-EJP1396.** Read: arXiv:2403.19932v1 (29 Mar 2024).
- Def. 2.1: a measure is stochastically stable if it is a weak limit of F_ε-invariant measures along some ε_n → 0. Def. 2.2: F is strongly stochastically stable if exactly one such measure exists.
- Thm 3.1: for nilpotent CA, ‖δ_0 − π_ε‖_A ≤ C|A|ε. Thm 4.2: in 1-D with a spreading state 0 and 0-positive noise, the error is O(ε). Thm 4.9: binary case under zero-range noise.
- Thm 6.1: whether δ_0 is stochastically stable under uniform noise is undecidable.
- Everything is on A^{Z^d}. There are no finite rings, no cycle potentials and no Freidlin–Wentzell references, although the paper cites L.-S. Young's work on SRB measures.

**[BBM24] F. Bagnoli, M. Baia, T. Matteuzzi, "Effects of a vanishing noise on elementary cellular automata phase-space structure", in ACRI 2024, LNCS, Springer (2024), pp. 45–57. DOI 10.1007/978-3-031-71552-5_5.** Read: arXiv:2406.15408v2 (30 Apr 2025), an extended version titled "Discrete system phase space modification by vanishing noise" that adds a Hopfield model. The LNCS chapter itself was not read; the pages are taken from the authors' own citation of it.
- Exhaustive enumeration of cycles and basins for all 88 minimal ECA on rings up to L = 17 (Table 2, at L = 17).
- "Vanishing noise" means at most one flip per step. Sect. 5 builds a matrix W_ij that counts, over all states of cycle j and all single-site flips, how many land in the basin of attractor i. W is normalised over columns and iterated (Q' = WQ), with states uniform within a cycle.
- For rule 232 they describe domain walls performing an annihilating random walk, so that the noise drives the system to all-0 and all-1.
- Table 2 reports entropies S (dynamics only) and S* (with vanishing noise) for every minimal rule at L = 17. Observation, from their table (rebuilt and confirmed in `VERIFICATION_v02.md`): rules 7, 19, 23 and 232, the four weakest cases of v0.1, all have S* = 0.059.
- There is no resistance above 1, no Young/Freidlin–Wentzell potential and no per-state order. Reading (corrected after the independent verification, `VERIFICATION_v02.md`, finding V10): their W-chain is guaranteed to give the correct leading-order law on cycles when the resistance-1 inter-cycle graph has a single closed class, which is then exactly the set of noise-selected cycles. With several closed classes their limit depends on the initial vector and can still be right, e.g. by symmetry. The verification rebuilt their construction at L = 17: there the condition holds for every class except 232, whose two closed classes are the uniform fixed points and whose basin-weighted answer is correct by complementation symmetry. So their L = 17 table already determines the noise-selected cycles, and with them the split k* = 0 / k* ≥ 1, for all classes at L = 17. At other ring sizes the condition fails for a few classes, and for class 164 at n = 16 their limit also weights a cycle that is not noise-selected (numbers in `report.md`, Section 8, generated from `verify_v02/out/`).

**[Fat13] N. Fatès, "A guided tour of asynchronous cellular automata", AUTOMATA 2013, LNCS 8155 (2013) 15–30. DOI 10.1007/978-3-642-40867-0_2.** Read: arXiv:1406.0792, an extended preprint for J. Cellular Automata (27 Aug 2014).
- A survey of asynchronous updating. Sect. 3.5 points to studies mixing asynchrony with state noise: Kanada on the 256 ECA, and Silva–Correia 2013.
- p. 19 of the preprint remarks that asynchrony does not change fixed points.
- No small-noise selection of cycles.

**[Cam14] M. Cameron, "Computing the asymptotic spectrum for networks representing energy landscapes using the minimum spanning tree", Netw. Heterog. Media 9 (2014). DOI 10.3934/nhm.2014.9.383.** Read: arXiv:1402.2869v2.
- Restricted to time-reversible (detailed-balance) networks. It uses the minimum spanning tree to obtain eigenvalue asymptotics.
- Not applicable to noisy ECA, which are irreversible.

**[New18] J. Newton, "Evolutionary game theory: a renaissance", Games 9(2) (2018) 31. DOI 10.3390/g9020031.** Read: version of record. This is a secondary source.
- It defines the stochastic potential of a convention as the minimum weight of spanning trees over conventions rooted at that convention. It states that stochastically stable conventions are those of lowest stochastic potential, citing Kandori–Mailath–Rob and Young 1993.
- It credits Ellison (2000) with finite-state corollaries of Freidlin–Wentzell hitting-time results.
- Use only as a restatement of the content. It does not confirm Young's theorem numbering.

## 2. Sources located but NOT read in full text (metadata or abstract only; nothing below is cited as read)

| Key | Entry | What was accessible |
|---|---|---|
| Young93 | H. P. Young, "The evolution of conventions", Econometrica 61(1) (1993) 57–84. DOI 10.2307/2951778 | title via DOI only |
| KMR93 | M. Kandori, G. Mailath, R. Rob, "Learning, mutation, and long run equilibria in games", Econometrica 61(1) (1993) 29–56. DOI 10.2307/2951777 | title only |
| Ell93 | G. Ellison, "Learning, local interaction, and coordination", Econometrica 61(5) (1993) 1047–1071. DOI 10.2307/2951493 | full PDF was retrieved by the literature session but not text-extracted or read (correction added after review); content unverified. Players on a circle interacting with neighbours: closest to an ECA setting in economics, but content unverified |
| Ell00 | G. Ellison, "Basins of attraction, long-run stochastic stability, and the speed of step-by-step evolution", Rev. Econ. Stud. 67 (2000) 17–45 | not retrieved; DOI unverified |
| FW12 | M. I. Freidlin, A. D. Wentzell, Random Perturbations of Dynamical Systems, 3rd ed., Springer 2012, ch. 6 "Markov perturbations on large time intervals". DOI 10.1007/978-3-642-25847-3_6 | chapter title only |
| VF70 | A. D. Ventcel, M. I. Freidlin, "On small random perturbations of dynamical systems", Russian Math. Surveys 25(1) (1970) 1–55. DOI 10.1070/RM1970v025n01ABEH001254 | title; MCTT attribution via [PT18] |
| LR86 | F. T. Leighton, R. L. Rivest, "Estimating a probability using finite memory", IEEE Trans. Inf. Theory 32(6) (1986) 733–742. DOI 10.1109/TIT.1986.1057250 | title; content via [PT18] Thm 3.1 |
| AT89 | V. Anantharam, P. Tsoucas, "A proof of the Markov chain tree theorem", Stat. Probab. Lett. 8(2) (1989) 189–192. DOI 10.1016/0167-7152(89)90016-3 | title |
| CL65 | Y. J. Chu, T. H. Liu, "On the shortest arborescence of a directed graph", Scientia Sinica 14 (1965) 1396–1400 | citation via [GC17] |
| GTH85 | W. K. Grassmann, M. I. Taksar, D. P. Heyman, "Regenerative analysis and steady state distributions for Markov chains", Oper. Res. 33(5) (1985) 1107–1116. DOI 10.1287/opre.33.5.1107 | abstract: Gauss–Jordan variant using only nonnegative quantities, hence numerically stable |
| OC93 | C. A. O'Cinneide, "Entrywise perturbation theory and error analysis for Markov chains", Numer. Math. 65 (1993) 109–120. DOI 10.1007/BF01385743 | title. The entrywise relative-accuracy claim for GTH is unverified here |
| Cat92 | O. Catoni, "Rough large deviation estimates for simulated annealing: application to exponential schedules", Ann. Probab. 20(3) (1992) 1109–1146. DOI 10.1214/aop/1176989682 | abstract |
| Cat99 | O. Catoni, "Simulated annealing algorithms and Markov chains with rare transitions", Sém. Probab. XXXIII, LNM 1709 (1999) 69–119. DOI 10.1007/BFb0096510 | title |
| Tro96 | A. Trouvé, "Cycle decompositions and simulated annealing", SIAM J. Control Optim. 34(3) (1996) 966–986. DOI 10.1137/S0363012993258586 | abstract: the cycle decomposition is computable exactly by an implementable algorithm |
| WG05 | J. R. Wicks, A. Greenwald, "An algorithm for computing stochastically stable distributions with applications to multiagent learning in repeated games", UAI 2005, 623–632 (arXiv:1207.1424) | search snippet: claims the first exact algorithm for the stochastically stable distribution |
| BLR16 | V. Betz, S. Le Roux, "Stable states of perturbed Markov chains", MFCS 2016, LIPIcs 58, 18. DOI 10.4230/LIPIcs.MFCS.2016.18 | search snippet: computes stable states in O(n³) |
| WL92 | A. Wuensche, M. Lesser, The Global Dynamics of Cellular Automata, SFI Studies in the Sciences of Complexity, Addison-Wesley 1992 | citation only. Wuensche's DDLab "jump-graph" (single-bit flips at attractor states, probability of jumping between basins) is known from search snippets only |
| MM14 | J. Mairesse, I. Marcovici, "Around probabilistic cellular automata", Theor. Comput. Sci. 559 (2014) 42–72. DOI 10.1016/j.tcs.2014.09.009 | title |
| Gac01 | P. Gács, "Reliable cellular automata with self-organization", J. Stat. Phys. 103 (2001) 45–267 | citation via [BMM13] |
| Too80 | A. Toom, "Stable and attractive trajectories in multicomponent systems", in Multicomponent Random Systems, Adv. Probab. 6, Dekker (1980) 549–575 | citation via [MS25] |

## 3. Answers

### Q1. Has the stochastic stability of cycles of noisy ECA on finite rings been computed before?

Provisional answer: **no such computation was found in the sources searched.** No paper found computes Freidlin–Wentzell/Young stochastic potentials of the cycles of F for noisy ECA on Z/nZ, whether for all 88 classes or for specific rules. None gives the per-state orders of π_ε.

Closest prior work, nearest first:
1. [BBM24] Bagnoli–Baia–Matteuzzi. All 88 minimal ECA at L = 17 with single-flip "vanishing noise". They form an attractor-level chain from resistance-1 basin jumps and report entropies. This is a first-order truncation of the Young construction, with no potentials, no resistance above 1 and no per-state orders. Their L = 17 table also singles out rules 7, 19, 23 and 232. It already determines the noise-selected cycles, and hence which classes have ρ → ∞ (k* = 0), at L = 17 for every class (see the entry above); what v0.2 adds is the exact orders k_c and k*, per-state orders, the asymptotics of ρ, certificates, ring sizes 4–20 including the cases where the single-flip chain fails (class 164 at n = 16), and the correction for class 106.
2. Wuensche's DDLab jump-graph (WL92 lineage). Single-bit-flip basin-jump probabilities. Not read.
3. [BMM13]. Invariant measure of a related but different majority-flip PCA on Z/nZ, with a parity effect, exact up to n = 9.
4. [MS25] and [MST19]. Stochastic stability and ergodicity of noisy CA on the infinite lattice, including undecidability. Not finite rings.
5. Ellison 1993 (not read). Stochastic stability for local-interaction coordination on a circle, an economics model whose best-response map resembles a CA.

The algorithms for stochastic potentials are generic Markov-chain tools: [GC17]; Wicks–Greenwald and Betz–Le Roux (snippets only). None of them is applied to ECA.

### Q2. Exact statements

- (a) Young 1993, "Theorem 4": **not verified**, full text not accessible. [New18] (secondary) confirms only the content: stochastically stable equals minimum stochastic potential.
- (b) Freidlin–Wentzell ch. 6, the W-graph lemmas and W(x) = min_i [W(K_i) + V(K_i,x)]: **not verified**. [PT18] attributes the irreducible MCTT to Ventcel–Freidlin 1970, "Lemma 7.1". [GKMS13] calls the MCTT the "Freidlin–Wentzell formula".
- (c) Markov chain tree theorem: verified in [PT18] Thm 1.1 (irreducible) and Thm 3.1 (general, after Leighton–Rivest), and in [GKMS13] Thm 1.1. The max-algebra analogue is [GKMS13] Thm 2.4. The originals (LR, AT) were not read.
- (d) Edmonds 1967: verified, Theorem 1 and the Sect. 2 reductions; arborescences are out-trees. Chu–Liu was not read.
- (e) GTH 1985: abstract only. O'Cinneide 1993: not read. The entrywise-accuracy claim is unverified.
- (f) Ellison radius–coradius: not read.
- (g) Gan & Cameron: verified, Defs 2.1–2.2, Thms 2.3–2.5, Algorithms 1 and 2. Catoni and Trouvé: abstracts only.

### Q3. Which sources give ord π_ε(x) = min_C[γ(C) + r(C→x)] − min_C γ(C) exactly?

**None of the sources read states this cycle-reduced per-state formula.** What the read sources do support is the following.

Full-state exact order, our deduction from [PT18] Thm 1.1:
- For ε ∈ (0, 1/2) every transition probability p_ε(x,y) = ε^{r(x,y)} (1−ε)^{n−r(x,y)} is positive, so the chain is irreducible and π_ε(x) = Σ_x(ε) / Σ_y Σ_y(ε).
- Each tree term is a polynomial in ε. Its lowest-degree term is ε^{r(T)}, with coefficient +1.
- A sum of such terms cannot cancel. Hence π_ε(x) = (m_x/M) ε^{V(x)−V*} (1 + O(ε)), with:
  - V(x) the minimum total resistance over spanning in-trees rooted at x;
  - V* = min_y V(y);
  - m_x the number of minimising x-trees, and M the sum of m_y over the y with V(y) = V*.
- This is an exact asymptotic expansion, not a logarithmic large-deviation estimate, and it also gives the leading constant. Exactness rests on the polynomial form of p_ε, specific to this noise model.

Reduction to cycles, V(x) = min_C [γ(C) + R(C→x)] (R = minimum path resistance): this is the Freidlin–Wentzell/Young step. Its source was not read, so v0.2 should carry its own proof. A sketch follows; it is our argument and still needs checking.
1. Let K be the union of the cycles of F and K' = K ∪ {x}. The stationary law of the chain censored on K' is exactly π_ε restricted to K' and renormalised (stochastic complement).
2. Its transition probabilities are convergent power series in ε with positive leading coefficient. Their order is the minimum resistance of paths between points of K' that avoid K' in between. Convergence holds because any N = 2^n consecutive steps outside K' contain at least one flip.
3. Applying the MCTT order formula on K' and contracting cycles gives both bounds:
   - Upper bound, via paths: concatenate the optimal cycle tree with a minimum path to x, then extract a spanning in-tree. Every vertex reaches x, and costs are nonnegative.
   - Lower bound, via contraction: in any tree, every cycle node reaches the root, so an in-tree can be extracted on the contracted graph from a subset of edges. Then cut the edge into x on the branch that contains x's own attractor, and re-attach x to that attractor at cost 0.
   - The triangle inequality for the minimum path costs takes care of re-routed edges.

This yields ord π_ε(x) = min_C[γ(C) + R(C→x)] − min_C γ(C) for every state, with equality and not just a bound.

Recommended verifier (rule 3 of the brief), independent of this argument: for small n (n ≤ 8, N = 256), compute V(x) for every x directly with Edmonds/Chu–Liu on the reversed complete resistance graph, one run per root. Compare with the cycle formula computed by 0-1 BFS. As a second check, compute π_ε exactly with GTH in rational arithmetic at a few small ε and fit the exponents.

## 4. BibTeX

```bibtex
@article{GanCameron2017,
  author  = {Gan, Tingyue and Cameron, Maria},
  title   = {A Graph-Algorithmic Approach for the Study of Metastability in {Markov} Chains},
  journal = {Journal of Nonlinear Science},
  year    = {2017},
  doi     = {10.1007/s00332-016-9355-0},
  note    = {Read: arXiv:1607.00078v2. Volume/pages not verified.}
}
@article{Edmonds1967,
  author  = {Edmonds, Jack},
  title   = {Optimum Branchings},
  journal = {Journal of Research of the National Bureau of Standards, Section B},
  volume  = {71B}, number = {4}, pages = {233--240}, year = {1967},
  doi     = {10.6028/jres.071B.032}
}
@article{PitmanTang2018,
  author  = {Pitman, Jim and Tang, Wenpin},
  title   = {Tree Formulas, Mean First Passage Times and {Kemeny}'s Constant of a {Markov} Chain},
  journal = {Bernoulli}, volume = {24}, year = {2018},
  doi     = {10.3150/16-BEJ916},
  note    = {Read: arXiv:1603.09017v3. Pages not verified.}
}
@article{Gursoy2013,
  author  = {Benek Gursoy, Buket and Kirkland, Steve and Mason, Oliver and Sergeev, Serge{\u\i}},
  title   = {On the {Markov} Chain Tree Theorem in the Max Algebra},
  journal = {Electronic Journal of Linear Algebra},
  volume  = {26}, pages = {15--27}, year = {2013},
  doi     = {10.13001/1081-3810.1636}
}
@article{BusicMairesseMarcovici2013,
  author  = {Bu{\v{s}}i{\'c}, Ana and Mairesse, Jean and Marcovici, Ir{\`e}ne},
  title   = {Probabilistic Cellular Automata, Invariant Measures, and Perfect Sampling},
  journal = {Advances in Applied Probability},
  volume  = {45}, number = {4}, pages = {960--980}, year = {2013},
  doi     = {10.1239/aap/1386857853}
}
@article{MarcoviciSablikTaati2019,
  author  = {Marcovici, Ir{\`e}ne and Sablik, Mathieu and Taati, Siamak},
  title   = {Ergodicity of Some Classes of Cellular Automata Subject to Noise},
  journal = {Electronic Journal of Probability}, volume = {24}, year = {2019},
  doi     = {10.1214/19-EJP297},
  note    = {Read: arXiv:1712.05500.}
}
@article{MarsanSablik2025,
  author  = {Marsan, Hugo and Sablik, Mathieu},
  title   = {Strong Stochastic Stability of Cellular Automata},
  journal = {Electronic Journal of Probability},
  volume  = {30}, pages = {1--32}, year = {2025},
  doi     = {10.1214/25-EJP1396},
  note    = {Read: arXiv:2403.19932v1.}
}
@incollection{BagnoliBaiaMatteuzzi2024,
  author    = {Bagnoli, Franco and Baia, Michele and Matteuzzi, Tommaso},
  title     = {Effects of a Vanishing Noise on Elementary Cellular Automata Phase-Space Structure},
  booktitle = {Cellular Automata (ACRI 2024)}, series = {Lecture Notes in Computer Science},
  publisher = {Springer}, pages = {45--57}, year = {2024},
  doi       = {10.1007/978-3-031-71552-5_5},
  note      = {Read: extended version arXiv:2406.15408v2 (2025); chapter itself not read.}
}
@incollection{Fates2013,
  author    = {Fat{\`e}s, Nazim},
  title     = {A Guided Tour of Asynchronous Cellular Automata},
  booktitle = {Cellular Automata and Discrete Complex Systems (AUTOMATA 2013)},
  series    = {Lecture Notes in Computer Science}, volume = {8155},
  publisher = {Springer}, pages = {15--30}, year = {2013},
  doi       = {10.1007/978-3-642-40867-0_2},
  note      = {Read: extended preprint arXiv:1406.0792.}
}
@article{Cameron2014,
  author  = {Cameron, Maria},
  title   = {Computing the Asymptotic Spectrum for Networks Representing Energy Landscapes Using the Minimum Spanning Tree},
  journal = {Networks and Heterogeneous Media}, volume = {9}, year = {2014},
  doi     = {10.3934/nhm.2014.9.383},
  note    = {Read: arXiv:1402.2869v2.}
}
@article{Newton2018,
  author  = {Newton, Jonathan},
  title   = {Evolutionary Game Theory: A Renaissance},
  journal = {Games}, volume = {9}, number = {2}, pages = {31}, year = {2018},
  doi     = {10.3390/g9020031}
}
% ---- Not read in full text (metadata only) ----
@article{Young1993,
  author = {Young, H. Peyton}, title = {The Evolution of Conventions},
  journal = {Econometrica}, volume = {61}, number = {1}, pages = {57--84}, year = {1993},
  doi = {10.2307/2951778}, note = {Not read in full text.}
}
@article{KandoriMailathRob1993,
  author = {Kandori, Michihiro and Mailath, George J. and Rob, Rafael},
  title = {Learning, Mutation, and Long Run Equilibria in Games},
  journal = {Econometrica}, volume = {61}, number = {1}, pages = {29--56}, year = {1993},
  doi = {10.2307/2951777}, note = {Not read in full text.}
}
@article{Ellison1993,
  author = {Ellison, Glenn}, title = {Learning, Local Interaction, and Coordination},
  journal = {Econometrica}, volume = {61}, number = {5}, pages = {1047--1071}, year = {1993},
  doi = {10.2307/2951493}, note = {Not read in full text.}
}
@article{Ellison2000,
  author = {Ellison, Glenn},
  title = {Basins of Attraction, Long-Run Stochastic Stability, and the Speed of Step-by-Step Evolution},
  journal = {Review of Economic Studies}, volume = {67}, pages = {17--45}, year = {2000},
  note = {Not retrieved; DOI not verified.}
}
@book{FreidlinWentzell2012,
  author = {Freidlin, Mark I. and Wentzell, Alexander D.},
  title = {Random Perturbations of Dynamical Systems}, edition = {3},
  publisher = {Springer}, year = {2012},
  doi = {10.1007/978-3-642-25847-3},
  note = {Chapter 6 (doi:10.1007/978-3-642-25847-3_6) not read in full text.}
}
@article{VentcelFreidlin1970,
  author = {Ventcel, A. D. and Freidlin, M. I.},
  title = {On Small Random Perturbations of Dynamical Systems},
  journal = {Russian Mathematical Surveys}, volume = {25}, number = {1}, pages = {1--55}, year = {1970},
  doi = {10.1070/RM1970v025n01ABEH001254}, note = {Not read in full text.}
}
@article{LeightonRivest1986,
  author = {Leighton, F. Thomson and Rivest, Ronald L.},
  title = {Estimating a Probability Using Finite Memory},
  journal = {IEEE Transactions on Information Theory}, volume = {32}, number = {6}, pages = {733--742}, year = {1986},
  doi = {10.1109/TIT.1986.1057250}, note = {Not read in full text.}
}
@article{AnantharamTsoucas1989,
  author = {Anantharam, Venkat and Tsoucas, Pantelis},
  title = {A Proof of the {Markov} Chain Tree Theorem},
  journal = {Statistics \& Probability Letters}, volume = {8}, number = {2}, pages = {189--192}, year = {1989},
  doi = {10.1016/0167-7152(89)90016-3}, note = {Not read in full text.}
}
@article{ChuLiu1965,
  author = {Chu, Y. J. and Liu, T. H.},
  title = {On the Shortest Arborescence of a Directed Graph},
  journal = {Scientia Sinica}, volume = {14}, pages = {1396--1400}, year = {1965},
  note = {Not read.}
}
@article{GTH1985,
  author = {Grassmann, Winfried K. and Taksar, Michael I. and Heyman, Daniel P.},
  title = {Regenerative Analysis and Steady State Distributions for {Markov} Chains},
  journal = {Operations Research}, volume = {33}, number = {5}, pages = {1107--1116}, year = {1985},
  doi = {10.1287/opre.33.5.1107}, note = {Abstract only.}
}
@article{OCinneide1993,
  author = {O'Cinneide, Colm Art},
  title = {Entrywise Perturbation Theory and Error Analysis for {Markov} Chains},
  journal = {Numerische Mathematik}, volume = {65}, pages = {109--120}, year = {1993},
  doi = {10.1007/BF01385743}, note = {Not read in full text.}
}
@article{Catoni1992,
  author = {Catoni, Olivier},
  title = {Rough Large Deviation Estimates for Simulated Annealing: Application to Exponential Schedules},
  journal = {Annals of Probability}, volume = {20}, number = {3}, pages = {1109--1146}, year = {1992},
  doi = {10.1214/aop/1176989682}, note = {Abstract only.}
}
@incollection{Catoni1999,
  author = {Catoni, Olivier},
  title = {Simulated Annealing Algorithms and {Markov} Chains with Rare Transitions},
  booktitle = {S{\'e}minaire de Probabilit{\'e}s XXXIII}, series = {Lecture Notes in Mathematics},
  volume = {1709}, pages = {69--119}, publisher = {Springer}, year = {1999},
  doi = {10.1007/BFb0096510}, note = {Not read in full text.}
}
@article{Trouve1996,
  author = {Trouv{\'e}, Alain}, title = {Cycle Decompositions and Simulated Annealing},
  journal = {SIAM Journal on Control and Optimization}, volume = {34}, number = {3}, pages = {966--986}, year = {1996},
  doi = {10.1137/S0363012993258586}, note = {Abstract only.}
}
@inproceedings{WicksGreenwald2005,
  author = {Wicks, John R. and Greenwald, Amy},
  title = {An Algorithm for Computing Stochastically Stable Distributions with Applications to Multiagent Learning in Repeated Games},
  booktitle = {Proc. 21st Conference on Uncertainty in Artificial Intelligence (UAI 2005)}, pages = {623--632}, year = {2005},
  note = {arXiv:1207.1424. Not read.}
}
@inproceedings{BetzLeRoux2016,
  author = {Betz, Volker and Le Roux, St{\'e}phane},
  title = {Stable States of Perturbed {Markov} Chains},
  booktitle = {41st International Symposium on Mathematical Foundations of Computer Science (MFCS 2016)},
  series = {LIPIcs}, volume = {58}, pages = {18:1--18:14}, year = {2016},
  doi = {10.4230/LIPIcs.MFCS.2016.18}, note = {Not read; page range not verified.}
}
@book{WuenscheLesser1992,
  author = {Wuensche, Andrew and Lesser, Mike},
  title = {The Global Dynamics of Cellular Automata: An Atlas of Basin of Attraction Fields of One-Dimensional Cellular Automata},
  series = {Santa Fe Institute Studies in the Sciences of Complexity},
  publisher = {Addison-Wesley}, year = {1992}, note = {Not read.}
}
@article{MairesseMarcovici2014,
  author = {Mairesse, Jean and Marcovici, Ir{\`e}ne},
  title = {Around Probabilistic Cellular Automata},
  journal = {Theoretical Computer Science}, volume = {559}, pages = {42--72}, year = {2014},
  doi = {10.1016/j.tcs.2014.09.009}, note = {Not read in full text.}
}
@article{Gacs2001,
  author = {G{\'a}cs, Peter}, title = {Reliable Cellular Automata with Self-Organization},
  journal = {Journal of Statistical Physics}, volume = {103}, pages = {45--267}, year = {2001},
  note = {Not read.}
}
```
