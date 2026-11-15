# Literature review: ring-size dependence of noise-selected cycles in ECA

Scope: elementary cellular automata (ECA) on Z/nZ with i.i.d. bit-flip noise, X_{t+1} = F(X_t) XOR Z_t. Question: why does the small-noise classification depend on n (3 | n, 4 | n, n = 2^k)? Rule 154 = l XOR r XOR (l AND c) = r XOR (l AND NOT c).

Reading rule used here: "read" means the text was opened and read in this session; every statement in Section 1 comes from that text. Statements taken from a search-engine snippet or a publisher abstract are marked as such and are not marked as read.

## Update after the independent verification (15 November 2026)

This review records what the study session read. The independent verification of 14 November 2026 checked
it against sources it could obtain (`verify_ring_size/literature/literature_check.md`; findings A20 to A31
of `VERIFICATION_ring_size.md`). The points below correct or complete the review; "read by the
verification" refers to that check, not to the study session. Passages changed in place are marked
"(corrected ...)" or "(added ...)".

* **Sources now read (by the verification).** Martin, Odlyzko and Wolfram (1984) in full (author copy at
  content.wolfram.com); the published version of Ellison (2000) in part (journal pp. 17, 20, 22-26, 28-31,
  36-39 of 17-45; scan hosted at economics.mit.edu); Fedoriaka (arXiv:2501.06648) in full and Bhattacharjee
  and Das (arXiv:1903.06011) in part, through a text extraction. Jen (1986, 1988): abstracts only.
  Wuensche and Lesser (1992) and the Wolfram Atlas: still not obtained. The access statements of Section 0
  describe the study session (A29).
* **Known results behind Theorem A and Lemma B (A20, A21).** Lemma 1, Lemma 2 and the first sentence of
  Theorem A correspond to the results on "mutation-connected" and "locally stable" components of Samuelson
  (1994) and Nöldeke and Samuelson (1993, Proposition 1); Lemma B is in substance the
  single-mutation-chain lemma that Ellison (2000, Section 6.2, journal pp. 37-38; working paper p. 30)
  attributes to Samuelson (1994) and Nöldeke and Samuelson (1993, 1997). The primary texts of Samuelson
  and of Nöldeke and Samuelson were **not read**, neither by the study nor by the verification; the
  correspondence rests on Ellison's text, the abstract of Samuelson (1994) and secondary descriptions. Not
  found in the sources read: the explicit potentials gamma_min = m - 1 and gamma_min = m + q - 2. The
  report presents both statements as restatements of known results.
* **Ellison (2000), Theorem 2 (A22, A23).** The published article has the same numbering as the working
  paper: Definition 1 p. 20; radius and coradius pp. 23-24; Theorem 1 p. 24; modified coradius pp. 28-29;
  Theorem 2, Section 4.2, p. 30; Theorem 3 p. 38. Theorem 2 has two conclusions: (a) containment of the
  long-run stochastically stable set in Ω, (b) W(y, Ω, ε) = O(ε^(−CR*(Ω))) for every y outside Ω. When Ω
  is a single limit set, (a) gives equality (p. 38).
* **Bijectivity of rules 154 and 45 at odd n (A24)** is stated in Bhattacharjee and Das
  (arXiv:1903.06011, Example 2) and in Fedoriaka (arXiv:2501.06648, Section 3: exhaustive computation for
  N in [4, 20] with explicit circuit constructions, not a proof for all odd N), and by its abstract in
  Nobe and Yura (2004). Rule 45 is the output complement of the mirror image of rule 154.
* **Rule 90 at n = 2^k (A25).** Martin, Odlyzko and Wolfram (1984), Lemma 3.5 (p. 230); the "iff" follows
  from their Theorems 3.3 and 3.4 with corollaries.
* **Precedents of Proposition R154 (A26).** OEIS A070886, comment: rules 18, 26, 82, 90, 146, 154, 210 and
  218 give the same pattern from a single cell on the line; Martin, Odlyzko and Wolfram, Section 5 (p. 247):
  the same reduction for rule 18; OEIS A334504 and A334507: single-cell periods of rules 26 and 122 on
  rings, which agree with `data/ring_size/seed_orbits.csv` for n = 4..120. The ring statements for rules
  154 and 22 were not found in the sources read.
* **The class-94 crystal (A30).** The three shifts of 011011... are the non-null fixed points of rule 90
  for N a multiple of 3 (Martin, Odlyzko and Wolfram, Lemma 3.7, p. 234).
* **Proved since by the verification** (not literature; see Section 5.7 of the report): k* = 1 iff n is a
  power of two for rule 154 at every n >= 3; k* = 1 for class 94 at every n >= 6 divisible by 3. No search
  for these two statements was made after they were proved.

---

## 0. Access limits

Hard-refused by the sandbox: the host resolved to a private or reserved IP. The user approved access each time, but the connection still failed, and approval cannot fix this.

| Host | Needed for | Result |
|---|---|---|
| www.wolframscience.com, wolframscience.com | NKS online (Sect. 6.4 and notes) | refused; the same text was read from Wolfram's own CDN files.wolframcdn.com (see 1.1) |
| atlas.wolfram.com | Wolfram Atlas finite-size data (rules 154, 94, 43, 142, 35, 122, 90) | refused; **not read** |
| www.stephenwolfram.com | author copy of Martin–Odlyzko–Wolfram 1984 | refused |
| www-users.cse.umn.edu | Odlyzko's copy of the same paper | refused |
| projecteuclid.org | open-access CMP copies (Martin–Odlyzko–Wolfram 1984; Jen 1988) | refused |
| arxiv.org (direct) | arXiv:2501.06648, 2406.10704, 1802.01763, 2509.07797 | refused. The fetch tool did reach arXiv copies when Unpaywall mapped a journal DOI to them: Bagnoli et al. and Marsan–Sablik were obtained that way. Preprints without a journal DOI were not obtainable. |
| www.dklevine.com | Levine archive copies of Ellison 1993 and 2000 | refused; author copies were read from MIT instead (1.3, 1.4) |
| www.ddlab.org | Wuensche–Lesser atlas, DDLab manual (jump graph) | refused; **not read** |
| fun.repo.nii.ac.jp | green-OA copies of Nobe–Yura 2004 and 2007 (handles 10445/1023 and 10445/1024) | refused; **not read** |
| api.crossref.org, api.semanticscholar.org, api.unpaywall.org (direct python) | metadata | blocked by the allowlist; not requested, because the fetch tool covers these services |

Closed access, with no open-access copy reachable: Martin–Odlyzko–Wolfram 1984; Jen 1986 and 1988 (two papers); Wuensche 2018 (encyclopedia chapter); Mairesse–Marcovici 2014; Fatès 2020 (tutorial).

Read only partially, or a substitute version was read:
- Ellison (2000): the author's working paper of January 1999 was read (web.mit.edu/gellison/www/basins.pdf, 45 pp.), not the published journal text. Page numbers below are working-paper pages. Theorem and section numbers agree with how later authors cite the published version (Rozen 2008; Vicario 2021), but I saw those citations only as search snippets. The math in this PDF has no text layer. Formulas were taken from an image transcription and checked by eye for §4.1 (modified coradius).
- Ellison (1993): read from a scanned copy hosted at economics.mit.edu (ProQuest scan) via OCR. Theorem 1 was checked by eye. The OCR of PDF page 10 (journal p. 1056) was flagged as uncertain; the proof sketch there is used only qualitatively.
- Bagnoli, Baia, Matteuzzi: the extended arXiv version **v2 (30 Apr 2025)** was read. It carries a different title ("Discrete System Phase Space Modification by Vanishing Noise"). The ACRI 2024 LNCS chapter itself was **not** read.
- NKS: the chapter 6 PDF excerpt (with the chapter 6 notes, pp. 947–965) and the Section 6.4 excerpt were read. Formulas embedded in the notes lose their placement in the text layer. The note "Additive rules" (p. 963) was checked by eye. For p. 951 the formulas were reassembled from the text layer (marked below).
- Marsan–Sablik (2025): only the abstract, Definitions 2.1–2.2, the start of Theorem 3.1, and a keyword scan of the full text (arXiv v1 copy).

---

## 1. Sources read in full text

### 1.1 Wolfram, *A New Kind of Science* (2002): Section 6.4 and notes for Chapter 6
- Version read: Wolfram CDN PDF excerpts `nks-ch6-sec4.pdf` (Section 6.4, pp. 255–260) and `nks-ch6.pdf` (Chapter 6 with notes, pp. 223–296 and 947–965). Book pages are cited.
- **Section 6.4, pp. 255–260.**
  - p. 257: the repetition period of a finite system can depend strongly on its exact size and rule. Toy systems (adding or multiplying by a constant on a circle) get periods from n/gcd(m,n) and multiplicative orders. For the doubling map and odd n, the period is MultiplicativeOrder[2, n].
  - p. 258: in ECA with cyclic boundary conditions, the period fluctuates strongly with n. Of the elementary rules, only rule 45 has periods that stay close to the maximum 2^n.
  - p. 259 (figure): rule 90 started from a single black cell, period for n = 15…25: 15, **1** (n = 16), 15, 14, 511, 12, 63, 62, 2047, **8** (n = 24), 1023.
  - p. 260 (caption): the maximum period of rule 90 is 2^((n−1)/2) − 1.
  - Nothing on noise, and nothing on rules 154, 94, 43, 142, 35 or 122.
- **Note "Page 260 · Maximum periods" (p. 950).** A state with spatial period m can never evolve into a state with larger spatial period. The longest possible cycle on n cells is therefore s[n,k], the number of states with exact spatial period n (a Möbius sum). For k = 2 and n = 1…10 these values are listed in the note.
- **Note "Additive cellular automata" (p. 951).** Formulas reassembled from the text layer; not checked by eye.
  - Rule 60 and rule 90 are analysed through polynomials mod (x^n − 1, 2); the analysis is attributed to Martin, Odlyzko and Wolfram (1983).
  - Rule 60, odd n: the period divides 2^MultiplicativeOrder[2,n] − 1.
  - Rule 90, odd n: the period divides 2^MultiplicativeOrder[2,n,{1,−1}] − 1. It usually equals that bound; the first exception is n = 37.
- **Note "Systems of limited size" (pp. 961–963).**
  - p. 961: state transition networks. For the doubling map, odd n gives pure cycles and even n adds trees.
  - p. 962: networks for rules 254, 132, 30, 45 and 110 at small n; for the class 2 rule 132, the number of cycles grows with n.
- **Note "Additive rules" (p. 963), checked by eye.** For rules 60 and 90 every cycle state roots an identical tree.
  - Odd n: the tree is a single arc, and half of all states lie on cycles.
  - Even n: a balanced tree, of depth 2^IntegerExponent[n,2] and degree 2 for rule 60, and of depth 2^IntegerExponent[n/2,2] and degree 4 for rule 90.
  - The fraction of states on cycles is 2^(−2^IntegerExponent[n,2]) for both rules.
  - *Inference (mine, not stated in NKS):* for n = 2^k this fraction is 2^(−n), so only the null state lies on a cycle; rule 90 is nilpotent on rings of size 2^k. This agrees with the p. 259 figure (n = 16, period 1).
- **Note "Symmetries" (p. 963):** identical pieces of a network usually come from shifted copies, and their number then divides n.
- **Note "Rule 94" (p. 951):** with suitable initial conditions this class 2 rule gives nested and random patterns. Nothing on finite size.
- Text search of the Chapter 6 and Chapter 10 PDFs for rules 154, 43, 142 and 35: no hits. Rules 94 and 122 appear only in rule galleries and in an unrelated note on p. 958.

### 1.2 Bagnoli, Baia, Matteuzzi: arXiv:2406.15408 **v2** (30 Apr 2025), "Discrete System Phase Space Modification by Vanishing Noise", 16 pp.
- This is the extended version of the ACRI 2024 chapter "Effects of a Vanishing Noise on Elementary Cellular Automata Phase-Space Structure", LNCS 14978, pp. 45–57, doi 10.1007/978-3-031-71552-5_5. The fetch tool's Unpaywall lookup for that DOI returned this arXiv PDF. **The v2 text was read in full; the chapter was not.**
- **Noise model (§5).** The noise is a "vanishing" noise: at most a single flip, applied to attractor states. W(i|j) counts, over all states of cycle j and all one-site flips, how many land in the basin of attractor i. After normalising columns, W is iterated to a stationary Q, and S* is its normalised entropy. This is a single-flip transition count between attractors, **not** a stochastic-potential (Freidlin–Wentzell/Young) analysis. Multi-flip costs are not considered.
- **Lattice size.**
  - All ECA results are for **L = 17 only** (Table 2, p. 10). In §4 they enumerate all attractors for "small lattice sizes", up to 17.
  - The only remark on L-dependence is about rule 11: its cycles are few and their periods depend on lattice size (p. 4).
  - There is no study of how S, S* or the selected attractors vary with L, and nothing on divisibility.
- **Table 2 rows (L = 17; number of attractors n, entropies S, S_f, S\*):**

  | rule | attractors | S | S_f | S\* |
  |---|---|---|---|---|
  | 154 | 1688 | 1.0 | 1.0 | 1.0 |
  | 90 | 4404 | 0.941 | 0.941 | 0.941 |
  | 60 | 260 | 0.941 | 0.941 | 0.941 |
  | 94 | 1191 | 0.561 | 0.564 | 0.526 |
  | 43 | 316 | 0.572 | 0.572 | 0.393 |
  | 142 | 317 | 0.572 | 0.572 | 0.393 |
  | 35 | 429 | 0.68 | 0.689 | 0.683 |
  | 122 | 120 | 0.584 | 0.588 | 0.588 |
  | 22 | 52 | 0.438 | 0.44 | 0.46 |
  | 26 | 148 | 0.782 | 0.792 | 0.809 |
  | 37 | 349 | 0.531 | 0.531 | 0.517 |
  | 45 | 22 | 1.0 | 1.0 | 1.0 |
  | 73 | 1361 | 0.699 | 0.71 | 0.681 |

  Rule 154 appears only in this table row. The text does not discuss it, nor rules 94, 43, 142, 35 or 122.
- *Inference (mine):* S = 1 for rule 154 at the odd size L = 17 is consistent with F_154 being a bijection on odd rings, so that all 2^17 states lie on cycles. That bijectivity is reported elsewhere (Section 2, Nobe–Yura) and was not verified here.

### 1.3 Ellison (2000), "Basins of attraction, long-run stochastic stability, and the speed of step-by-step evolution", *Rev. Econ. Stud.* 67(1):17–45. DOI **10.1111/1467-937X.00119** (verified by title)
- **Version read:** author working paper, MIT, January 1999 (web.mit.edu/gellison/www/basins.pdf, 45 PDF pages). Page numbers are working-paper pages. The DOI ending in .00121 noted in the earlier session is not this paper.
- **Definition 1 (p. 5).** A model of evolution with noise is a triple (Z, P, P(ε)):
  - Z is finite and P is a Markov matrix;
  - P(ε) is ergodic for ε > 0, continuous in ε, with P(0) = P;
  - there is a cost function c: Z×Z → R+ ∪ {∞} such that P_zz'(ε)/ε^c(z,z') has a positive limit when c < ∞.
- **Long-run stochastic stability (§2.2, p. 7).** μ* = lim_{ε→0} μ^ε. A state z is long-run stochastically stable if μ*(z) > 0. Limit sets are the recurrent classes of P.
- **Waiting time (p. 8).** W(x, Y, ε) is the expected wait until Y is first reached from x.
- **§3.1, pp. 9–10: radius and coradius.**
  - Basin: D(Ω) is the set of states from which the unperturbed process converges to Ω with probability 1.
  - Path from X to Y: a finite sequence of **distinct** states (z_1, …, z_T) with z_1 ∈ X, z_t ∉ Y for 2 ≤ t ≤ T−1, and z_T ∈ Y. S(X, Y) is the set of such paths, and c(path) = Σ c(z_t, z_{t+1}).
  - **Radius:** R(Ω) = min over paths in S(Ω, Z − D(Ω)) of c(path).
  - **Coradius:** CR(Ω) = max_{x∉Ω} min over paths in S(x, Ω) of c(path). The maximum is attained at a state in a limit set. Equivalently, CR(Ω) = max_{x∉D(Ω)} min over paths in S(x, D(Ω)) of c(path).
  - p. 9, with footnote 8: in all of Ellison's examples c(x,y) = min_{z: P_xz(0)>0} d(z,y), with d obeying the triangle inequality. Under that structure, footnote 9 (p. 10) gives a sufficient condition for the cheapest exit path to be a direct one-step path.
  - *Inference (mine):* the ECA model has exactly this form, with c(x,y) = d_H(F(x), y), Hamming distance.
- **Theorem 1 (§3.2, p. 10).** If Ω is a union of limit sets with R(Ω) > CR(Ω), then:
  - (a) the long-run stochastically stable set is contained in Ω;
  - (b) for every y ∉ Ω, W(y, Ω, ε) = O(ε^(−CR(Ω))).
- **§4.1, p. 17: modified coradius** (checked by eye).
  - Let (z_1, …, z_T) be a path from x to Ω, and let L_1, L_2, …, L_r be the sequence of limit sets it passes through consecutively (a limit set may repeat, but not twice in a row). L_r ⊂ Ω, and L_i ⊄ Ω for i < r.
  - **Modified cost:** c*(z_1…z_T) = c(z_1…z_T) − Σ_{i=2}^{r−1} R(L_i). R(L_1) is explicitly excluded.
  - Point-to-set modified cost: c*(x, Ω) = min over paths in S(x, Ω) of c*(path).
  - **Modified coradius:** CR*(Ω) = max_{x∉Ω} c*(x, Ω). Always CR*(Ω) ≤ CR(Ω).
  - pp. 18–19: in a worked three-state example, W(x, Ω, ε) ~ ε^(−CR*(Ω)). The subtraction reflects that the exit from an intermediate limit set y should be counted conditionally on leaving y.
- **Theorem 2 (§4.2, p. 19).** If Ω is a union of limit sets with **R(Ω) > CR*(Ω)**, then:
  - (a) the long-run stochastically stable set is contained in Ω;
  - (b) for every y ∉ Ω, W(y, Ω, ε) = O(ε^(−CR*(Ω))).

  The proof (pp. 19–20) uses the steady-state formula in Lemma 1 (appendix) and the bounds W = O(ε^(−CR*)) and 1/N(Ω, y, ω) = O(ε^(R(Ω))) (Lemmas 2 and 6). p. 20: Lemmas 2 and 3 give W(ℓ, Z − D(L), ε) ~ ε^(−R(L)) for every state ℓ of a single limit set L.

  Caveat: Theorem 2 gives **containment** of the stochastically stable set in Ω. It does not state that every part of Ω is selected. Uniqueness holds when Ω is a single limit set.
- **Theorem 3 (§6.3, p. 31; "tree surgery").** Ω must be a **single** limit set. If R(Ω) > c*(x, Ω) for some x ∉ Ω, then μ*(x) = 0. If R(Ω) = c*(x, Ω), then μ*(x) > 0 implies μ*(Ω) > 0. The proof on p. 32 uses Freidlin–Wentzell x-trees.
- Ellison also gives an example in which the long-run stochastically stable set is a deterministic cycle (§3.3, pp. 12–13).

### 1.4 Ellison (1993), "Learning, local interaction, and coordination", *Econometrica* 61(5):1047–1071. DOI **10.2307/2951493** (verified by title)
- Version read: scanned journal pages from economics.mit.edu, read via OCR. Theorem 1 was checked by eye.
- **Model (p. 1050).** N players on a **circle**, a 2×2 coordination game, best response with probability 1−ε and random play with probability ε. Two-neighbour and 2k-neighbour matching are compared with uniform matching.
- **Theorem 1 (p. 1055).** For N sufficiently large:
  - (a) μ_A(ε) → 1 (the risk-dominant convention) under both uniform and 2k-neighbour matching;
  - (b) under uniform matching, μ_B(ε) = O(ε^(N − 2⌈q*(N−1)⌉ + 1)); under **two-neighbour** matching, μ_B(ε) = O(ε^(N−2)) for **N even** and O(ε^(N−1)) for **N odd**.
- **Where the parity comes from.**
  - p. 1056, proof of (b): for even N ≥ 4, the minimum-order trees route through the alternating state AB…, with t(A) = AB and t(AB) = B.
  - p. 1069 (proof of Theorem 2): for odd N the unperturbed two-neighbour dynamics has only the two monomorphic steady states and no cycles. Even N additionally has the 2-cycle AB → BA → AB.
- **Remark 2 (p. 1057).** If the matching is too concentrated, a two-player alternating cycle cannot vanish relative to A, because one mutation leads in and one leads out.
- **Theorem 3 (p. 1062).** Under local matching the expected waiting time to reach the risk-dominant equilibrium is bounded independently of N.
- **Relevance.** This is a ring-parity effect inside a stochastic-stability analysis on a circle. The parity changes the ε-order of a non-selected state, but **not** which state is selected.

### 1.5 Bušić, Mairesse, Marcovici (2013), "Probabilistic cellular automata, invariant measures, and perfect sampling", *Adv. Appl. Probab.* 45(4):960–980. DOI **10.1239/aap/1386857853** (verified)
- Version read: publisher PDF (Cambridge, bronze OA), full text.
- **Theorem 3.1 (p. 966).** For a deterministic CA on Z: ergodic ⇔ nilpotent; ergodicity is therefore undecidable (Corollary 3.1).
- **Example 4.1 (p. 974).** The majority-flip PCA on Z/nZ is ergodic for odd n.
- **§5.1 (p. 977): PCA Majority(α) on Z/nZ.** With probability α a cell applies majority; otherwise it flips. The chain behaves completely differently depending on the **parity of n**:
  - n **even**: the unique invariant measure is concentrated on the two alternating configurations (01)^{n/2} and (10)^{n/2};
  - n **odd**: the invariant measure has full support.

  This holds at fixed α ∈ (0,1); it is not a small-noise limit. It is still a direct example of a spatially periodic "crystal" that exists only for some ring sizes and then carries all the stationary mass.
- §5 also has an experimental study on Z (Conjecture 5.1). Exact invariant measures on odd rings were computed only up to n = 9 (p. 978).

### 1.6 Powley & Stepney (2009), "Automorphisms of transition graphs for elementary cellular automata", *J. Cellular Automata* 4(2):125–136 (no DOI; metadata from dblp and the publisher's issue list)
- Version read: author PDF (www-users.york.ac.uk/~ss44/bib/ss/nonstd/jca08.pdf), 12 pp., full text. Page references are to that PDF.
- **Method (pp. 3–7).** A(f, N) is the order of the automorphism group of the transition graph on N cells. Automorphisms are exactly the self-conjugacies of the global map (Theorem 1 and Corollary 1). A(f, N) is computed recursively over the cycle-and-tree structure (Lemmas 1–2, Theorem 2). All 88 classes were computed for N ≤ 16, and selected rules for N = 17.
- **Result (§5, Table 1, pp. 7–9).** Three sets:
  - L: log log A grows roughly linearly in N (79 classes);
  - **Z: log log A alternates between even and odd N for N ≤ 14**, less clearly for 15 ≤ N ≤ 17;
  - C: rules 30, 45 and 106.
- **Set Z** contains the nontrivial linear rules 60, 90, 105 and 150, the trivial linear rule 15, and **the single nonlinear rule 154** (§5.2, p. 9).
  - What 154 shares with the linear rules: a single nonzero cell produces a Sierpiński-type self-similar pattern.
  - On other initial conditions, 154 gives periodic patterns, whereas the linear rules give chaotic ones.
  - Table 1 rows for 154 (N = 10…17): 2.091, 2.077, 2.945, 2.674, 3.269, 3.268, 4.252, 3.856.
- No noise. Nothing on rules 94, 43, 142, 35 or 122 beyond their membership in set L.

### 1.7 Powley & Stepney (2009), "Automorphisms of transition graphs for linear cellular automata", *J. Cellular Automata* 4(4):293–310 (no DOI)
- Version read: author PDF (…/nonstd/jca09.pdf), 20 pp. Read: the statements of all lemmas and theorems, plus §6 (rule 90).
- This paper **restates** results of Martin–Odlyzko–Wolfram (1984) with their numbering. **I did not read MOW itself.** The MOW numbers below are therefore second-hand citations.
- Lemma 1 (= MOW Lemma 3.3): in a linear CA, all trees rooted at cycle states are isomorphic.
- Lemma 3 (= MOW Lemma 3.4): Π_N, the cycle length reached from a single 1, is the maximal cycle length, and all cycle lengths divide it.
- Lemma 6 (rule 90, odd N; citing MOW Theorems 3.2 and 3.3 and the corollary to 3.3): trees are single edges, reachable states have 2 predecessors, and 2^(N−1) states lie on cycles.
- Lemma 7 (rule 90, even N; citing MOW; in MOW the content is Theorems 3.2 and 3.4 and the first corollary to Theorem 3.4, and Theorem 3.2 has no corollary (corrected after the verification, A28; the wording in Powley–Stepney was not re-checked)):
  - D2(N) is the largest power of 2 dividing N;
  - trees are balanced of depth D2(N)/2;
  - reachable states have 4 predecessors;
  - 2^(N−D2(N)) states lie on cycles.
- Lemma 9 (rule 90; citing MOW Lemma 3.5, Lemma 3.6 and Theorem 3.5):
  - (1) **N a power of 2 ⇒ Π_N = 1** (only the null cycle);
  - (2) N even but not a power of 2 ⇒ Π_N = 2Π_{N/2};
  - (3) N odd ⇒ Π_N divides 2^(sord_N(2)) − 1. Equality holds for most odd N; exceptions include N = 37, 95, 101, ….
- Theorem 8 gives the automorphism count of rule 90 from the cycle multiset. There is no statement about rule 154.

### 1.8 Marsan & Sablik (2025), "Strong stochastic stability of cellular automata", *Electron. J. Probab.* 30:1–32. DOI **10.1214/25-EJP1396** (verified) — **partially read**
- Version: arXiv v1 PDF (2403.19932), via Unpaywall.
- Read: the abstract; Definition 2.1 (a measure π is stochastically stable if it is a weak limit of invariant measures of ε_n-perturbations); Definition 2.2 (a CA is *strongly* stochastically stable if it has exactly one stochastically stable measure); the beginning of Theorem 3.1 (nilpotent CA); and a keyword scan of the full text.
- The setting is A^(Z^d) only. The keyword scan found no finite rings, no Z/nZ, and no elementary rule numbers.

---

## 2. Sources located but NOT read (metadata only)

- **Martin, Odlyzko, Wolfram (1984)**, "Algebraic properties of cellular automata", *Commun. Math. Phys.* 93:219–258, DOI 10.1007/BF01223745 (verified). Closed; all OA hosts refused. Its statement numbers are known here only through Powley–Stepney (1.7) and the NKS note (1.1). (Added after the verification: read in full by the verification from the author copy; see the update at the top.)
- **Jen (1988)**, "Cylindrical cellular automata", *Commun. Math. Phys.* 118:569–590, DOI 10.1007/BF01221109 (verified). **Not read.** Summary of the ADS/Springer abstract, as seen in search results:
  - a matrix A whose trace of A^n gives the number of fixed points on a cylinder of size n;
  - limit cycles counted through linear recurrences;
  - closed forms for all two-neighbour rules;
  - limit cycles described as shifts s/h.
- **Jen (1988)**, "Linear cellular automata and recurring sequences in finite fields", *Commun. Math. Phys.* 119:13–28, DOI 10.1007/BF01218258 (verified). Not read. According to the abstract, the shift size varies with the cylinder size n.
- **Jen (1986)**, "Global properties of cellular automata", *J. Stat. Phys.* 43:219–242, DOI 10.1007/BF01010579 (verified). Not read.
- **Jen (1989/1990)**: "Limit cycles in one-dimensional cellular automata" (in *Lectures in the Sciences of Complexity*, Addison-Wesley) and "Aperiodicity in one-dimensional cellular automata" (*Physica D* 45, 1990). Located only through reference lists; DOIs not verified. Not read.
- **Nobe & Yura (2004)**, "On reversibility of cellular automata with periodic boundary conditions", *J. Phys. A* 37(22):5789–5804, DOI 10.1088/0305-4470/37/22/006 (verified).
  - The abstract (via the fetch tool) says exactly 16 ECA rules are reversible for infinitely many cell sizes.
  - A search snippet (ResearchGate) shows "Proposition 1: the rule-154 ECA is reversible for the cell size N ≡ 1 (mod 2)", and says the reversible ECA rules are 150, 154, 170 and 204 up to automorphisms.
  - **Not read**; the green-OA host was refused.
- **Nobe & Yura (2007)**, "Linearizable cellular automata", *J. Phys. A* 40(26):7159, DOI 10.1088/1751-8113/40/26/004 (verified). The abstract says that for a class of reversible ECA with periodic boundaries, the initial value problem reduces to linear systems over a finite commutative ring. Whether rule 154 is in this class is **unknown (not read)**.
- **Fedoriaka (2025)**, arXiv:2501.06648, "Quantum circuits for elementary cellular automata". Search snippet only: lists rules 45, 75, 89, 101, 154, 166, 180 and 210 as reversible for odd N with periodic boundaries; writes 154 as a_{i+1} ⊕ (¬a_i · a_{i−1}). Not read. (Added after the verification: read in full by the verification; the list comes from exhaustive computation for N in [4, 20] plus explicit constructions.)
- **Wuensche & Lesser (1992)**, *The Global Dynamics of Cellular Automata: An Atlas of Basin of Attraction Fields of One-Dimensional Cellular Automata*, SFI Studies in the Sciences of Complexity, Addison-Wesley. Publisher data not verified against the book. Not obtainable (ddlab.org refused).
- **Wuensche: jump graph.**
  - "Exploring Discrete Dynamics" (Luniver Press 2011; 2nd ed. 2016; online update 2023), §20.7 jump-graph.
  - arXiv:2406.10704, "Interactive Graph Visualization in DDLab". Search snippet: the jump graph gives the probabilities of jumping between basins under all single-bit or single-value flips of attractor states.
  - Wuensche (2018), "Basins of attraction of cellular automata and discrete dynamical networks", Encyclopedia of Complexity and Systems Science, DOI 10.1007/978-1-4939-8700-9_674 (verified; closed).
  - None read. Conceptually the jump graph is the same single-flip attractor graph as Bagnoli et al.'s W.
- **Martínez et al.**, arXiv:1802.01763, "Simple networks on complex cellular automata: from de Bruijn diagrams to jump-graphs". Search snippet: a jump graph of ECA rule 54 at n = 20. Not read.
- **Wolfram Atlas** (atlas.wolfram.com): not read (refused).
- **Mairesse & Marcovici (2014)**, "Around probabilistic cellular automata", *Theor. Comput. Sci.* 559:42–72, DOI 10.1016/j.tcs.2014.09.009 (verified; closed). Not read.
- **Asynchronous-update literature.** This is a different noise model (random update order, not state flips). Ring size, including divisibility, is reported to matter there. None of these was read.
  - Fatès, Morvan, Schabanel, Thierry (2006), *Theor. Comput. Sci.* 362:1–16 (fully asynchronous double-quiescent ECA on rings of size n).
  - Fatès (2020), "A tutorial on elementary cellular automata with fully asynchronous updating", *Natural Computing*, DOI 10.1007/s11047-020-09782-7 (verified; not readable).
  - Sethi, Roy, Das (2018), "Convergence of asynchronous cellular automata: does size matter?", *J. Cell. Autom.* 13(5–6):527–542.
  - Per citing snippets (arXiv:2509.07797), Sethi–Roy–Das give ring-size conditions for convergence, including even n for rules 6, 14 and 22, and rings of size a multiple of 3 for rules 45 and 37.
  - A skew-asynchronous follow-up (Natural Computing, 2026, per snippet) reports critical behaviour for n ∈ 2N, 3N and 4N.
- **Kanada (1994)**, "The effects of randomness in asynchronous 1D cellular automata", Artificial Life IV (poster). Not read.

---

## 3. Answers

**(Q1) Has the dependence of noise-selected attractors (stochastically stable states or cycles) on the ring size been studied? Not found in the searched sources for ECA under i.i.d. bit-flip noise with minimum-stochastic-potential selection.**

The closest material:
1. Bagnoli–Baia–Matteuzzi (arXiv v2, §5–6, Table 2) treat all 88 ECA classes under a vanishing single-flip noise. They work at a single size, L = 17, use a single-flip attractor Markov chain rather than stochastic potential, and do not study L-dependence (1.2).
2. Ellison (1993), Theorem 1(b), p. 1055: in a two-neighbour coordination model on a circle, the parity of N changes the ε-order of the non-selected state, through a 2-cycle that exists only for even N. The selected state does not depend on N (1.4).
3. Bušić–Mairesse–Marcovici (2013), §5.1, p. 977: the majority-flip PCA on Z/nZ concentrates its unique invariant measure on the two alternating configurations exactly when n is even. This is fixed noise, not a small-noise limit (1.5). It is the closest published analogue of "crystal capture" found.
4. Asynchronous-update studies report ring-size and divisibility conditions (2, 3, 4) for convergence to fixed points. These were not read, and the noise model is different (Section 2).

**(Q2) Has rule 154 under noise been studied? Not found, apart from one table row.** Bagnoli et al. (v2, Table 2, p. 10) list rule 154 at L = 17 with 1688 attractors and S = S_f = S* = 1.0; it is not discussed. No other source on rule 154 with noise was found.

**(Q3) Known exact statements on rule 154 vs rule 90.**
- *Read:* Powley–Stepney (2009a, §5.2) group 154 with the linear rules: the automorphism count of the transition graph alternates between even and odd N for N ≤ 14. The common property they name is the Sierpiński pattern from a single seed. 154 is otherwise periodic (1.6).
- *Not read (snippet or abstract only):* rule 154 is reversible for odd N (Nobe–Yura 2004, Proposition 1; also listed by Fedoriaka 2025; stated for rules 45 and 154 in Bhattacharjee–Das, arXiv:1903.06011, Example 2 (added after the verification)). Nobe–Yura (2007) linearise a class of reversible ECA over a finite commutative ring; whether 154 belongs to it is unknown.
- *Not found:* a conjugacy or factor map between rule 154 and rule 90; nilpotency or other statements about 154 at n = 2^k; its cycle structure as a function of n.
- *Known for rule 90 only* (NKS p. 963, read; MOW Lemma 3.5 as cited by Powley–Stepney 2009b, Lemma 9): for N a power of 2, every state reaches the null configuration (Π_N = 1). The project's own data (31 and 4081 cycles for rule 154 at n = 8 and 16) show that 154 is not nilpotent there. No such statement about rule 154 was found in the sources read (corrected after the verification, A27).

**(Q4) Ellison's radius and modified coradius. Read**, in the January 1999 working paper (see 1.3 for the full definitions).
- R(Ω) = min cost of a path from Ω out of D(Ω).
- CR(Ω) = max_{x∉Ω} min cost of a path from x to Ω.
- c*(path) = c(path) − Σ_{i=2}^{r−1} R(L_i), over the intermediate limit sets the path passes through.
- CR*(Ω) = max_{x∉Ω} min over paths of c*.
- **Theorem 2 (§4.2):** R(Ω) > CR*(Ω) ⇒ (a) the long-run stochastically stable set ⊂ Ω; (b) W(y, Ω, ε) = O(ε^(−CR*(Ω))) for all y ∉ Ω.
- Theorem 1 is the same statement with CR in place of CR*.
- Theorem 3 (§6.3) is the pointwise version for a **single** limit set Ω: R(Ω) > c*(x, Ω) ⇒ μ*(x) = 0.

If the note cites theorem numbers, add "(numbering of the 1999 working paper; consistent with later citations of the published version)", or check against the journal text. Paths must consist of distinct states. Theorem 2 gives containment in Ω, not equality. (Added after the verification: the published article has the same numbering, Theorem 2, Section 4.2, p. 30; it also gives the waiting-time bound, and equality when Ω is a single limit set, p. 38.)

**(Q5) Cycle structure vs ring size for non-additive ECA.**
- NKS 6.4 (read): periods depend strongly on n (figures for rules 30 and 45; rule 45 near the maximum). The bound s[n,k] comes from spatial periods: a state cannot evolve to a larger spatial period (p. 950). The networks on pp. 962–963 show identical pieces related by shifts, so their number divides n.
- Powley–Stepney (read): a symmetry-based classification as a function of N, with set Z containing the linear rules and 154.
- Jen (1988, "Cylindrical CA"): by its abstract, a general transfer-matrix method that counts fixed points (trace A^n) and limit cycles of any period on any cylinder size, with limit cycles described as shifts. **Not read**, so no specific statement for rules 94, 43, 142, 35, 122 or 154 can be reported.
- Wuensche (atlas, DDLab): not read.
- For rules 94, 43, 142, 35 and 122, no source read here states how their cycle structure depends on n.

---

## 4. BibTeX

```bibtex
@book{Wolfram2002NKS,
  author    = {Stephen Wolfram},
  title     = {A New Kind of Science},
  publisher = {Wolfram Media},
  address   = {Champaign, IL},
  year      = {2002},
  note      = {Read: Section 6.4 (pp. 255--260) and notes for Chapter 6 (pp. 947--965; in particular pp. 950, 951, 961--963), from the Wolfram CDN PDF excerpts nks-ch6-sec4.pdf and nks-ch6.pdf. p. 963 checked by eye; p. 951 formulas reassembled from the text layer.}
}

@misc{BagnoliBaiaMatteuzzi2025arXiv,
  author        = {Franco Bagnoli and Michele Baia and Tommaso Matteuzzi},
  title         = {Discrete System Phase Space Modification by Vanishing Noise},
  year          = {2025},
  eprint        = {2406.15408},
  archivePrefix = {arXiv},
  note          = {Read: full text of arXiv v2 (30 Apr 2025), 16 pp. Extended version of the ACRI 2024 chapter below. ECA results only at L = 17 (Table 2); single-flip attractor transition matrix W (Sect. 5).}
}

@inproceedings{BagnoliBaiaMatteuzzi2024ACRI,
  author    = {Franco Bagnoli and Michele Baia and Tommaso Matteuzzi},
  title     = {Effects of a Vanishing Noise on Elementary Cellular Automata Phase-Space Structure},
  booktitle = {Cellular Automata (ACRI 2024)},
  series    = {Lecture Notes in Computer Science},
  volume    = {14978},
  pages     = {45--57},
  publisher = {Springer},
  year      = {2024},
  doi       = {10.1007/978-3-031-71552-5_5},
  note      = {Not read (chapter itself). Only the extended arXiv v2 was read; see BagnoliBaiaMatteuzzi2025arXiv.}
}

@article{Ellison2000,
  author  = {Glenn Ellison},
  title   = {Basins of Attraction, Long-Run Stochastic Stability, and the Speed of Step-by-Step Evolution},
  journal = {Review of Economic Studies},
  volume  = {67},
  number  = {1},
  pages   = {17--45},
  year    = {2000},
  doi     = {10.1111/1467-937X.00119},
  note    = {Read: author working paper (MIT, January 1999, 45 pp., web.mit.edu/gellison/www/basins.pdf): Def. 1, Sects. 2.2, 3.1--3.2 (radius, coradius, Thm 1), 4.1--4.2 (modified coradius, Thm 2 and proof outline), 6.3 (Thm 3). Published journal text not read; page numbers refer to the working paper.}
}

@article{Ellison1993,
  author  = {Glenn Ellison},
  title   = {Learning, Local Interaction, and Coordination},
  journal = {Econometrica},
  volume  = {61},
  number  = {5},
  pages   = {1047--1071},
  year    = {1993},
  doi     = {10.2307/2951493},
  note    = {Read: full scanned text (economics.mit.edu copy) via OCR; Theorem 1 (p. 1055) checked by eye. N-parity in Thm 1(b); Thm 3 (p. 1062).}
}

@article{BusicMairesseMarcovici2013,
  author  = {Ana Bu{\v{s}}i{\'c} and Jean Mairesse and Irène Marcovici},
  title   = {Probabilistic Cellular Automata, Invariant Measures, and Perfect Sampling},
  journal = {Advances in Applied Probability},
  volume  = {45},
  number  = {4},
  pages   = {960--980},
  year    = {2013},
  doi     = {10.1239/aap/1386857853},
  note    = {Read: full text (publisher PDF). Thm 3.1 (p. 966); Example 4.1 (p. 974); Sect. 5.1 (p. 977): majority PCA on Z/nZ, parity of n.}
}

@article{PowleyStepney2009ECA,
  author  = {Edward J. Powley and Susan Stepney},
  title   = {Automorphisms of Transition Graphs for Elementary Cellular Automata},
  journal = {Journal of Cellular Automata},
  volume  = {4},
  number  = {2},
  pages   = {125--136},
  year    = {2009},
  note    = {Read: full text, author PDF (www-users.york.ac.uk/~ss44/bib/ss/nonstd/jca08.pdf). Set Z = linear rules + rule 154 (Sect. 5.2, Table 1).}
}

@article{PowleyStepney2009Linear,
  author  = {Edward J. Powley and Susan Stepney},
  title   = {Automorphisms of Transition Graphs for Linear Cellular Automata},
  journal = {Journal of Cellular Automata},
  volume  = {4},
  number  = {4},
  pages   = {293--310},
  year    = {2009},
  note    = {Read: author PDF (jca09.pdf): all lemma/theorem statements and Sect. 6. Restates Martin--Odlyzko--Wolfram 1984 results with their numbering (Lemmas 3.3--3.6, Thms 3.2--3.5).}
}

@article{MarsanSablik2025,
  author  = {Hugo Marsan and Mathieu Sablik},
  title   = {Strong stochastic stability of cellular automata},
  journal = {Electronic Journal of Probability},
  volume  = {30},
  pages   = {1--32},
  year    = {2025},
  doi     = {10.1214/25-EJP1396},
  note    = {Partially read: abstract, Defs. 2.1--2.2, start of Thm 3.1, keyword scan (arXiv v1 copy). Setting A^{Z^d}; no finite rings.}
}

@article{MartinOdlyzkoWolfram1984,
  author  = {Olivier Martin and Andrew M. Odlyzko and Stephen Wolfram},
  title   = {Algebraic properties of cellular automata},
  journal = {Communications in Mathematical Physics},
  volume  = {93},
  pages   = {219--258},
  year    = {1984},
  doi     = {10.1007/BF01223745},
  note    = {Not read (closed; OA hosts refused by sandbox). Statement numbers known only via PowleyStepney2009Linear.}
}

@article{Jen1988Cylindrical,
  author  = {Erica Jen},
  title   = {Cylindrical cellular automata},
  journal = {Communications in Mathematical Physics},
  volume  = {118},
  pages   = {569--590},
  year    = {1988},
  doi     = {10.1007/BF01221109},
  note    = {Not read (abstract seen via search results only).}
}

@article{Jen1988Linear,
  author  = {Erica Jen},
  title   = {Linear cellular automata and recurring sequences in finite fields},
  journal = {Communications in Mathematical Physics},
  volume  = {119},
  pages   = {13--28},
  year    = {1988},
  doi     = {10.1007/BF01218258},
  note    = {Not read.}
}

@article{Jen1986Global,
  author  = {Erica Jen},
  title   = {Global properties of cellular automata},
  journal = {Journal of Statistical Physics},
  volume  = {43},
  pages   = {219--242},
  year    = {1986},
  doi     = {10.1007/BF01010579},
  note    = {Not read.}
}

@article{NobeYura2004,
  author  = {Atsushi Nobe and Fumitaka Yura},
  title   = {On reversibility of cellular automata with periodic boundary conditions},
  journal = {Journal of Physics A: Mathematical and General},
  volume  = {37},
  number  = {22},
  pages   = {5789--5804},
  year    = {2004},
  doi     = {10.1088/0305-4470/37/22/006},
  note    = {Not read (abstract only; Prop. 1 on rule 154, N odd, seen only in a search snippet).}
}

@article{NobeYura2007,
  author  = {Atsushi Nobe and Fumitaka Yura},
  title   = {Linearizable cellular automata},
  journal = {Journal of Physics A: Mathematical and Theoretical},
  volume  = {40},
  number  = {26},
  pages   = {7159},
  year    = {2007},
  doi     = {10.1088/1751-8113/40/26/004},
  note    = {Not read (abstract only).}
}

@misc{Fedoriaka2025,
  author        = {Dmytro Fedoriaka},
  title         = {Quantum Circuits for Elementary Cellular Automata},
  year          = {2025},
  eprint        = {2501.06648},
  archivePrefix = {arXiv},
  note          = {Not read (search snippet only).}
}

@book{WuenscheLesser1992,
  author    = {Andrew Wuensche and Mike Lesser},
  title     = {The Global Dynamics of Cellular Automata: An Atlas of Basin of Attraction Fields of One-Dimensional Cellular Automata},
  series    = {Santa Fe Institute Studies in the Sciences of Complexity},
  publisher = {Addison-Wesley},
  year      = {1992},
  note      = {Not read (not obtainable; ddlab.org refused). Publisher data not verified against the book.}
}

@incollection{Wuensche2018Basins,
  author    = {Andrew Wuensche},
  title     = {Basins of Attraction of Cellular Automata and Discrete Dynamical Networks},
  booktitle = {Cellular Automata (Encyclopedia of Complexity and Systems Science series)},
  publisher = {Springer},
  year      = {2018},
  doi       = {10.1007/978-1-4939-8700-9_674},
  note      = {Not read (closed). Jump-graph described there per search snippet.}
}

@misc{Wuensche2024DDLabGraphs,
  author        = {Andrew Wuensche},
  title         = {Interactive Graph Visualization in DDLab},
  year          = {2024},
  eprint        = {2406.10704},
  archivePrefix = {arXiv},
  note          = {Not read (search snippet only; jump-graph = single-bit flips of attractor states).}
}

@article{MairesseMarcovici2014,
  author  = {Jean Mairesse and Irène Marcovici},
  title   = {Around probabilistic cellular automata},
  journal = {Theoretical Computer Science},
  volume  = {559},
  pages   = {42--72},
  year    = {2014},
  doi     = {10.1016/j.tcs.2014.09.009},
  note    = {Not read (closed).}
}

@article{FatesMorvanSchabanelThierry2006,
  author  = {Nazim Fat{\`e}s and Michel Morvan and Nicolas Schabanel and {\'E}ric Thierry},
  title   = {Fully asynchronous behavior of double-quiescent elementary cellular automata},
  journal = {Theoretical Computer Science},
  volume  = {362},
  pages   = {1--16},
  year    = {2006},
  note    = {Not read (metadata from citing works; DOI not verified).}
}

@article{Fates2020Tutorial,
  author  = {Nazim Fat{\`e}s},
  title   = {A tutorial on elementary cellular automata with fully asynchronous updating},
  journal = {Natural Computing},
  year    = {2020},
  doi     = {10.1007/s11047-020-09782-7},
  note    = {Not read (no reachable OA copy).}
}

@article{SethiRoyDas2018,
  author  = {Biswanath Sethi and Souvik Roy and Sukanta Das},
  title   = {Convergence of Asynchronous Cellular Automata: Does Size Matter?},
  journal = {Journal of Cellular Automata},
  volume  = {13},
  number  = {5--6},
  pages   = {527--542},
  year    = {2018},
  note    = {Not read (metadata from dblp/citing works).}
}

@misc{Kanada1994,
  author       = {Yasusi Kanada},
  title        = {The effects of randomness in asynchronous 1D cellular automata},
  howpublished = {Poster, Artificial Life IV},
  year         = {1994},
  note         = {Not read.}
}

@misc{WolframAtlas,
  author       = {{Wolfram Research}},
  title        = {Wolfram Atlas of Simple Programs: elementary cellular automata},
  howpublished = {\url{https://atlas.wolfram.com/01/01/}},
  note         = {Not read (host refused by sandbox).}
}

@article{Samuelson1994,
  author  = {Samuelson, Larry},
  title   = {Stochastic stability in games with alternative best replies},
  journal = {Journal of Economic Theory},
  volume  = {64},
  pages   = {35--65},
  year    = {1994},
  note    = {Not read (abstract only, by the verification). Added after the verification.}
}

@article{NoeldekeSamuelson1993,
  author  = {N{\"o}ldeke, Georg and Samuelson, Larry},
  title   = {An evolutionary analysis of backward and forward induction},
  journal = {Games and Economic Behavior},
  volume  = {5},
  pages   = {425--454},
  year    = {1993},
  note    = {Not read (known through Ellison 2000, Sect. 6.2, and secondary descriptions). Added after the verification.}
}

@misc{BhattacharjeeDas2019,
  author       = {Bhattacharjee, Kamalika and Das, Sukanta},
  title        = {On finite 1-dimensional cellular automata: reversibility and semi-reversibility},
  howpublished = {arXiv:1903.06011},
  year         = {2019},
  note         = {Not read by the study; read in part by the verification (Example 2). Added after the verification.}
}
```
