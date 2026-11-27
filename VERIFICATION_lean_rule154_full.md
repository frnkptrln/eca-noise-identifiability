# Verification: the Lean statements of the rest of Section 3.1 (rule 154) against the paper

> **Handling of the findings (27 November 2026).** Written by Claude, the reader outside the sessions, who wrote
> the Lean files that this report checks and then worked these findings in. The report below is unchanged. Its line
> numbers refer to the Lean files and `lean/README.md` as they stood at 20f1e9e.
>
> * Finding 1 (the cycle `{0}`): the comments of `Theorem_3_9`, `Theorem_3_11` and `Zero_cycle` and item 11 of the
>   differences in `lean/README.md` now say that both theorems are stated for every cycle `C0` with set of states
>   `{0}`, that `Zero_cycle` makes them non-empty, and that part (a) of `Theorem_3_9` does not itself say that `{0}`
>   is a cycle. The statements are unchanged.
> * Finding 2 (comment of `Lemma_3_7`): the comment and item 2 now say which clause of the third sentence is stated
>   and which is not; "Not formalized" names it. The clause is not added as a statement.
> * Finding 3 (two proof routes): added to items 8 and 9 of the differences.
> * Only comments in two statement files and `lean/README.md` were changed. After the changes: `lake build` without
>   error or warning, the same 39 theorems checked against their statements, the same three axioms. The reader did
>   not run the scripts in `verify_lean_rule154_full/`.

Branch `lean-rule-154-full`, commit 20f1e9e. Checked: `lean/RingSize/Rule154/StatementMain.lean` (131 lines), its
definitions and its eleven statements, against `paper/ring_size_paper.tex`, Section 3.1 (Lemma 3.4(b) to Theorem 3.11,
lines 409–598) and Theorem 3.1(a) (line 344). I also checked the last section of `lean/README.md` (lines 519–614), in
particular its eleven "Differences from the paper" (lines 548–587). 27 November 2026.

In this report "SM" is `StatementMain.lean`, "R154" is `Rule154/Statement.lean`, "St" is `TheoremA/Statement.lean`,
and "l." without a file name is a line of the paper. "E" stands for error in a statement, "D" for a difference that
must be stated, and "W" for wording.

## Summary

Each of the eleven statements of SM is the paper's statement, an equivalent form, or a weaker form whose weakening the
README states (Lemma 3.4(b) for the cell 0, the part "In particular" of Lemma 3.6, the first sentence of Lemma 3.7,
Lemma 3.8(b) without "through cycles contained in M", Theorem 3.9(c) without the length bound), and the statements that
also cover n = 1 or 2 are true there, so there is no finding of severity E or D. The three findings are wording: the
form "∀ C0 with C0.1 = {0}" in Theorems 3.9 and 3.11 is not vacuous only because of `Zero_cycle`, the comment of
`Lemma_3_7` claims more than is stated, and two proof routes are missing from the list of differences. An independent
Python model of the Lean definitions reproduces every conclusion of `Theorem_3_9`, `Theorem_3_10` and `Theorem_3_11`
for n = 3..12, Lemmas 3.5 to 3.8 for n ≤ 12, Lemma 3.4(b) for even n ≤ 24 and Theorem 3.9 (a)–(f) at n = 16 (via the
criterion of Lemma 2.3), and it agrees with all 17 records of rule 154 in `data/fw_sweep.csv`.

## Method

1. I read SM line by line next to the paper. For each definition and statement I wrote down its place in the paper
   and the comparison (tables A and B). I also read the definitions it uses in R154 (`F154`, `parE`, `parO`,
   `Zero_cycle`), in St (`Cyc`, `IsCycle`, `VE`, `Vc`, `R`, `gamma`, `gammaMin`, `Sel`, `G1`, `Reach`,
   `IsClosedClass`, `numCycles`, `kIndex`, `kStar`, `Code`, `flip`, `globalMap`, `ruleOfNumber`, `Contains`, `D`) and
   in `RingSize/Statement.lean` (`State`, `e`). I read `AxiomCheckRule154.lean`, which assigns to each theorem its
   `Prop` (14 `#check` lines). I did not run it.
2. `git diff cf6f77e 20f1e9e` shows that the paper is unchanged since the verification in
   `VERIFICATION_lean_rule154.md`. In St and R154 only comments changed. In the existing proof files, `par` in
   `Pow2.lean` was made visible and the lemma `mem_cycleOf` was added to `Paths.lean`. So the definitions checked in
   `VERIFICATION_lean_theorem_a.md` and `VERIFICATION_lean_rule154.md` are the ones used here.
3. For README items 6, 7 and 8 I checked the arguments the README describes on paper (section E). To see whether
   the description matches the Lean proof, I read the proofs of `theorem_3_9`, `theorem_3_10` and `theorem_3_11`
   (`Main.lean`, l. 334–595). I also read the helper lemmas `gamma_le_card_add`, `codes_in_M`, `code_010_in_M`,
   `code_010_flip`, `k_le_one_of_cycle` and `V_zero_le_two` (l. 56–256), and the statements of `hub_parM`,
   `hub_odd`, `hub_not_parM` and `exists_edge_to_zero` in `Moves.lean`. I did not read the rest of the proof files.
4. I wrote a literal Python model of the Lean definitions, `verify_lean_rule154_full/model.py`. It uses no code from
   the repository and needs only `networkx`. It keeps the Lean conventions:
   * a state is an int whose bit i is cell i, with i = `i.val`;
   * `parE` and `parO` go through `i.val`;
   * `IsCycle` means "the orbit of a periodic point";
   * `R` ranges over all non-empty lists (length 1 included), with `sInf ∅ = 0`;
   * `IsInTree` is coded as written;
   * `kIndex` uses natural subtraction;
   * `IsPowTwo` is "∃ k, n = 2^k".

   `R` is computed exactly by a 0-1 breadth-first search on a two-layer graph (go to `F x` at cost 0, flip cells one
   at a time at cost 1). For n ≤ 6 I checked it against Dijkstra on the complete graph of steps, for every V(C, C')
   and every R(C → D_v).

   γ is computed by Edmonds' algorithm (networkx). Each tree it returns is checked with the literal `IsInTree`, and
   its weight is compared with the lower bound Σ_{d ≠ c} min_{e ≠ d} V(d, e), which holds for every in-tree. The two
   agreed for every root at every n, so each γ is certified without relying on Edmonds. For m ≤ 6 (n ≤ 5) all parent
   maps were also enumerated. For n = 11, 12 the breadth-first G_1 tree is used, whose weight m − 1 equals the lower
   bound. Closed classes are found from the three clauses of `IsClosedClass`. A closed set contains Reach(a) for each
   of its elements, so the candidates are the sets Reach(a), and each candidate is tested.
5. Scripts, all in `verify_lean_rule154_full/`, run one at a time in one process each, with outputs in
   `verify_lean_rule154_full/out/`:
   * `theorems.py`: Theorems 3.9–3.11, n = 1..12, 14 s;
   * `lemmas.py`: Lemmas 3.5–3.8, n = 1..12, together with the checks of R and of G_1, 2 s;
   * `lemma_3_4_b.py`: even n ≤ 24, under 1 s;
   * `n16.py`: Theorem 3.9 at n = 4, 8, 16, under 1 s;
   * `sweep_compare.py`: comparison with `fw_sweep.csv`, done last, under 1 s.

## Findings

**1. (W) The cycle `{0}` enters Theorems 3.9 and 3.11 only through a universally quantified hypothesis.**
SM l. 95 (`Theorem_3_9`, all six parts) and l. 122 (`Theorem_3_11`, the clause on `S`); paper l. 509, 514, 593;
README item 11 (l. 584–585).
Both statements have the form "∀ C0 : Cyc (F154 n), C0.1 = {0} → …". On its own, such a statement would be vacuously
true if `{0}` were not a cycle. Part (a) of `Theorem_3_9` ("every C ≠ C0 is contained in M") also does not say that
`{0}` is a cycle, which the paper's "the cycles are {0} and the cycles contained in M" does. Existence is the separate
statement `Zero_cycle` (R154 l. 45), proved as `zero_cycle` (`Pow2.lean` l. 156) and listed in the axiom check. The
proof of `theorem_3_11` instantiates `C0` with `cycZero n` built from it (`Main.lean` l. 325, 587). So, together with
`Zero_cycle`, the Lean statements are equivalent to the paper's. A cycle is determined by its set (`Cyc` is a
subtype), so "S = {C0} for every such C0" is then "S = {{0}}". Without `Zero_cycle` the two would disagree on a map
without the fixed point 0. They do not disagree for rule 154, where my model finds `{0}` to be a cycle for every n =
1..12. README item 11 names only Theorem 3.11 and does not name `Zero_cycle`. The comment of `Zero_cycle` names only
`Theorem_3_9_b`. Proposal: say in item 11 that the form is also used for all of `Theorem_3_9`, and that `Zero_cycle`
makes it non-vacuous.

**2. (W) The comment of `Lemma_3_7` overstates what is stated.** SM l. 62–63; paper l. 474–476; README item 2
(l. 553–555).
The comment says "its third sentence is part (a) of `Theorem_3_9`". The third sentence has two clauses: "If n = 2^k,
k ≥ 2, the periodic states are exactly the states of M ∪ {0}", and "the cycles are {0} and the cycles contained in
M". Only the second is part (a). The first clause is not stated in Lean. It follows from `Lemma_3_7`,
`Theorem_3_9`(a) and `Zero_cycle` once one uses that the periodic points are the union of the cycles, but that step is
not stated either. README item 2 is correct as far as it goes ("Of the third sentence, '…' is part (a)"). It does not
say that the first clause is left out, and "Not formalized" (l. 598) does not mention it. My model confirms the clause
for n = 4 and 8, and confirms the second sentence of Lemma 3.7 for every even n ≤ 12 (`out/lemmas.txt`). There is no
disagreement, only an unstated clause.

**3. (W) Two proof routes that differ from the paper are not among the differences.** README l. 564–582; `Main.lean`
l. 463–468 and 528–531; paper l. 550–553 and 583.
Items 6–9 list the places where the Lean proofs take another route, but two are missing:
(i) Theorem 3.9(f), lower bound k_v ≥ 1 for v ≠ 000. Lean gets it from `S = {C0}` and Lemma 2.2 (`kIndex_eq_zero_iff`:
k_v = 0 would need a selected cycle containing v, and 0 contains only 000). The paper uses γ({0}) = m − 1, γ(C) = m
and R({0} → D_v) ≥ 1 in (1). Item 8 covers only the upper bounds.
(ii) Theorem 3.10, γ(C) = m − 1. Lean gets it from Theorem 2.8 applied to the closed class "all cycles"
(`closed_univ_of_connected`, then `section_2_4_ECA`): S = all cycles and γ_min = m − 1. The paper uses a spanning
in-tree of G_1 edges rooted at each cycle.
Both Lean routes are valid: they use statements already proved, and the hypotheses are in place. This is wording only.

No other difference between SM and the paper was found. In particular, no statement claims more than the paper on the
paper's ring sizes. Every extension to n = 1 or 2 is true there, and every hypothesis that restricts n is needed (see
section D).

## A. Definitions

| SM | Paper | Comparison |
|---|---|---|
| `parM n = (parE n ∪ parO n)ᶜ` (l. 23–24) | M = {0,1}^n \ (E ∪ O), l. 374, for even n | Same for even n. For odd n the Lean set is defined (through `i.val`) but is used only under `Even n` (Lemmas 3.5, 3.7, 3.8) or `n = 2^k` (Theorem 3.9). For example, at n = 3 `parM` has 3 states and is not invariant (`out/lemmas.txt`), which no statement claims. |
| `V154 n = VE n (ruleOfNumber 154)` (l. 27–28) | V(C, C') = R(C → C'), l. 207 | Abbreviation. `VE` was checked in the earlier reports. |
| `k154 n v = kIndex n (ruleOfNumber 154) v` (l. 31–32) | k_v, (1), l. 219 | Abbreviation. For n ≤ 2 `kIndex` gives 0 on codes that no state contains (earlier report). SM uses `k154` only with n ≥ 3 (Theorems 3.9–3.11). |
| `kStar154 n = kStar n (ruleOfNumber 154)` (l. 35–36) | k* = max_v k_v, l. 219 | Abbreviation. |
| `IsPowTwo n := ∃ k, n = 2^k` (l. 39–40) | "n is a power of two", l. 344, 411, 562, 592 | Includes n = 1 and n = 2 (README item 10). Where it matters: (i) `Lemma_3_4_b_zero` (¬IsPowTwo, even) excludes n = 2, as it must, because at n = 2 F(e_0) = 0 (`out/lemma_3_4_b.txt`). (ii) In `Theorem_3_10`, n ≥ 1 and ¬IsPowTwo already imply n ≥ 3, so the hypothesis `3 ≤ n` is redundant there (harmless; the paper writes the same). (iii) In `Theorem_3_11` the hypothesis `3 ≤ n` is needed: with IsPowTwo, it leaves exactly n = 2^k, k ≥ 2, the paper's "(n ≥ 4)". |

`m` is `numCycles (F154 n) = Nat.card (Cyc (F154 n))` (St l. 135–136), as in l. 372 and l. 202.

## B. Statements

| SM | Paper | Comparison | Example where they would differ |
|---|---|---|---|
| `Lemma_3_4_b_zero` (l. 44–45) | Lemma 3.4(b), l. 411 | Weaker: the cell j = 0 only (README item 4). Same ring sizes: even, n ≥ 1, not a power of two, that is, n ≥ 6. "∀ t : ℕ" includes t = 0, as "t ≥ 0" does. | The paper claims, and Lean does not, F^t(e_3) ≠ 0 at n = 6. It is true (checked for all cells, even n ≤ 24). |
| `Lemma_3_5` (l. 49–50) | Lemma 3.5, l. 428–430 | Same conclusion. Stronger in ring size: even n ≥ 2 (paper n ≥ 4). True at n = 2, where M = {11} and F(11) = 11. | None: at n = 2 the paper says nothing. |
| `Lemma_3_6_in_particular` (l. 55–59) | Lemma 3.6, "In particular", l. 442–443 | Equivalent to the part "In particular". The conjunct `Even n` in the first clause comes from the first sentence ("Then n is even") but already follows from the second clause (bijective for odd n). The list of the three forms is not stated (README item 1). Stronger in ring size: n ≥ 1 (paper n ≥ 3). True at n = 1 (F is the identity) and n = 2 (the 3 colliding pairs are in E ∪ O). | The paper's three forms are not stated. My model finds that every colliding pair has one of the three forms for n = 2..12 (1 + 1 + 1 pairs at n = 2, 32 + 32 + 1 at n = 12, none otherwise). |
| `Lemma_3_7` (l. 64–66) | Lemma 3.7, first sentence, l. 473–474 | Same. `Set.BijOn F M M` (maps to, injective on, onto) is "the restriction of F to M is a permutation of M". `periodicPts` is "F^t x = x for some t ≥ 1". Even n ≥ 2 (paper n ≥ 4); true at n = 2. Second sentence not stated; third sentence: see finding 2. | — |
| `Lemma_3_8_a` (l. 71–75) | Lemma 3.8(a), l. 488–491 | Same. Even n ≥ 2 (paper n ≥ 4). At n = 2 the statement is vacuous: the only state of M is 11, and its flips 01 and 10 are not in M. | — |
| `Lemma_3_8_b` (l. 81–83) | Lemma 3.8(b), l. 492–493 | Hypothesis "x ∈ C, x ∈ M" instead of "C ⊆ M": for even n the two are equivalent, because a cycle that meets M is contained in M. In Lean this is `cycle_subset_parM`; my model confirms it for every cycle at even n ≤ 12. Conclusion `Reach C C'` for all such C, C', which gives both directions. Weaker: the clause "through cycles contained in M" is missing (README item 3). Even n ≥ 2; at n = 2 only the cycle {11} meets M and the statement is `Reach C C`. | A graph in which the only G_1 path between two cycles of M passes through a cycle in E ∪ O would satisfy Lean and not the paper. Rule 154 has no such case: G_1 restricted to the cycles in M is strongly connected for every even n ≤ 12. |
| `Theorem_3_9` (l. 93–103) | Theorem 3.9, l. 506–517 | Section C. Same as the paper except (c), which lacks the bound, together with finding 1. | (c): the paper's "length at most μ(C) ≤ n/2" is not stated. At n = 4 and 8 my model finds a shortest path of length ≤ μ(C) for every C; the longest is 2 = n/2 and 4 = n/2. |
| `Theorem_3_10` (l. 107–113) | Theorem 3.10, l. 561–564 | Same, all five claims. "G_1 strongly connected" is "∀ C C', Reach C C'", the definition of strong connectivity (`Reach` is the reflexive-transitive closure of the G_1 relation). Same ring sizes. | — |
| `Theorem_3_11` (l. 118–127) | Theorem 3.11, l. 591–595; Theorem 3.1(a), l. 344 | Section C. Same, together with finding 1. | — |

## C. The points named in the task

**Theorem_3_11.**
* Both cases are stated with all their claims: k* = 1, S, k_000 = 0, and k_v = 1 for v ≠ 000 (l. 121–123); and
  k* = 0, every cycle selected (that is, S = the set of all cycles), and k_v = 0 for all v (l. 125–127). Together the
  eight k_v are stated in each case: `k154 n (0,0,0)` plus `∀ v ≠ (0,0,0)` in the first, `∀ v` in the second. The
  order of `Code` is (a, b, c) with a = x_{i−1}, as in the paper. The values are symmetric under a ↔ c, so the
  orientation does not matter here.
* `3 ≤ n` is the paper's hypothesis. The cases are `IsPowTwo n` and its negation, so every n ≥ 3 is covered. The
  first case is not empty (n = 4, 8, 16, …), and for n ≥ 3 it is exactly n = 2^k with k ≥ 2.
* "S = {C0} for every cycle C0 with set {0}", together with `Zero_cycle`, is S = {{0}} (finding 1).
* The hypothesis is needed. At n = 1 (a power of two) the first case fails: k* = 0, both cycles {0}, {1} are
  selected. At n = 2 it fails because k_001 = k_011 = k_100 = k_110 = 0: these codes occur in no state, and
  R = sInf ∅ = 0 (`out/theorems.txt`).

**Theorem_3_9.**
* The form `2 ≤ k → n = 2^k` uses the paper's k (as the header of SM says; R154 uses k + 1, as its header says). The
  proof passes `k − 1` to `theorem_3_9_b` (`Main.lean` l. 336, 348).
* (a) Every C ≠ C0 is contained in M: see finding 1 for the missing "{0} is a cycle".
* (b) Both clauses of the paper. `¬ G1 C0 C` for all C includes C = C0, where V(C0, C0) = 0.
* (c) `Reach C C0` for all C (trivial for C = C0). The bound "of length at most μ(C) ≤ n/2" and the definition of
  μ are missing. This is stated in the comment (l. 92) and in README item 6.
* (d) `IsClosedClass {C0}` and every closed class equals {C0}: the paper's "{{0}} is the only closed class".
* (e) γ(C0) = m − 1, γ(C) = m for C ≠ C0, and S = {C0}, with m = `numCycles` and natural subtraction (m ≥ 1). This is
  the paper's (e).
* (f) k_000 = 0, k_v = 1 for the seven others, and k* = 1.

At n = 2 (k = 1), (a)–(e) hold in my model and (f) fails (k_001 = 0, as above), so `2 ≤ k` is needed. At n = 1 (k =
0), (a) already fails.

**Theorem_3_10.** All five claims are present (l. 109–113), and "strongly connected" is formalized correctly. The
hypothesis `3 ≤ n` is redundant (section A).

**Lemma_3_6_in_particular** is exactly the part "In particular", as table B explains, and it is true at n = 1, 2.

**Lemma_3_7, Lemma_3_8_a, Lemma_3_8_b, Lemma_3_5, Lemma_3_4_b_zero:** see table B.

**Vacuous or trivially true statements.**
* No statement is empty on the paper's ring sizes: each hypothesis is satisfiable (n = 6 for Lemma 3.4(b); n = 4 for
  Lemmas 3.5, 3.7, 3.8 and Theorem 3.9; n = 3 for Theorem 3.10).
* `Theorem_3_9` and the S-clause of `Theorem_3_11` rely on `Zero_cycle` (finding 1).
* `Lemma_3_8_a` is vacuous only at n = 2, and `Lemma_3_8_b` is trivial there; that ring size is outside the paper.
* `Reach` is reflexive, so the instances C = C' of `Lemma_3_8_b` and `Theorem_3_10`, and C = C0 of `Theorem_3_9`(c),
  are trivial, as they are in the paper.
* γ is the `sInf` of a non-empty set (the star p ≡ c is an in-tree), and D_v ≠ ∅ for n ≥ 3, so neither `γ` nor
  `kIndex` collapses to 0 by the convention `sInf ∅ = 0` where SM uses them.

## D. Ring sizes

| Statement | Lean | Paper | True on the extra ring sizes? |
|---|---|---|---|
| `Lemma_3_4_b_zero` | even, not a power of two (n ≥ 6) | same | — |
| `Lemma_3_5` | even n ≥ 2 | even n ≥ 4 | n = 2: yes (M = {11}, fixed) |
| `Lemma_3_6_in_particular` | n ≥ 1 | n ≥ 3 | n = 1: yes (identity); n = 2: yes (3 pairs, all in E ∪ O) |
| `Lemma_3_7` | even n ≥ 2 | even n ≥ 4 | n = 2: yes |
| `Lemma_3_8_a`, `Lemma_3_8_b` | even n ≥ 2 | even n ≥ 4 | n = 2: yes (vacuous, respectively trivial) |
| `Theorem_3_9` | n = 2^k, k ≥ 2 | same | — (at k = 1, part (f) would be false) |
| `Theorem_3_10` | n ≥ 3, not a power of two | same | — |
| `Theorem_3_11` | n ≥ 3 | same | — (at n = 1, 2 it would be false) |

README item 5 lists these sizes correctly. The truth at n = 1, 2 rests on the Lean proofs and, independently, on my
model (`out/lemmas.txt`).

## E. README, "Differences from the paper" (l. 548–587)

1. Lemma 3.6: correct. The Lean statement is the part "In particular" (table B).
2. Lemma 3.7: correct as far as it goes; the first clause of the third sentence is not mentioned (finding 2).
3. Lemma 3.8(b): correct, including the remark on `cycle_subset_parM`. The left-out clause is true for even n ≤ 12.
4. Lemma 3.4(b): correct. "The proofs below need only the cell 0": `theorem_3_10` uses `lemma_3_4_b_zero` with `e n 0`
   only (`Main.lean` l. 510–516).
5. Ring sizes: correct (section D).
6. Theorem 3.9(c), checked on paper. Let C ≠ {0}. By (a), C ⊆ M. Let y = 1_E + e_1. It has a one on the even cell 0
   and on the odd cell 1, so y ∈ M and y is periodic (Lemma 3.7). By Lemma 3.8(b) in the Lean form, C reaches the
   cycle C_y of y, either directly or through {1}, as the Lean proof does (`hub_parM`; {1} ⊆ M). The flip of cell 1
   of y is 1_E ∈ E, and F(1_E) = L(1_E) = 0: on odd cells 1 + 1 = 0, on even cells 0 + 0 = 0. So the orbit of
   y + e_1 ends on {0}. C_y ≠ {0} since y ≠ 0, so Lemma 2.3 gives the edge C_y → {0}. The argument is valid for every
   even n ≥ 4. It gives a path and no bound, as the item says. The description matches `exists_edge_to_zero` and the
   proof of `hreach0` (`Main.lean` l. 364–373).
7. Theorem 3.9(e), checked on paper.
   * Upper bound. All cycles other than {0} lie in M and are mutually reachable in G_1. A G_1 path between two of them
     never passes through {0}, because no G_1 edge leaves {0} (b). So they have an in-tree rooted at C ≠ {0} of G_1
     edges, of weight m − 2. Let A = e_2 + e_3: cell 2 is even and cell 3 is odd, so A ∈ M for even n ≥ 4. Add the
     edge {0} → C_A, where C_A is the cycle of A: the path [0, A] has resistance H(F0, A) = 2, and C_A ≠ {0}. The
     result is an in-tree of weight ≤ m. (`gamma_le_card_add` builds a G_1 tree in a graph where the one edge out of
     {0} is set to weight 1, then bounds the true weight by m − 1 + 1. That is the same tree.)
   * Lower bound. (d) gives the unique closed class {C0}. Theorem 2.8, in the form `section_2_4_ECA`, gives S = {C0}
     and γ_min = m − 1. For C ≠ C0, γ(C) ≥ γ_min, and γ(C) ≠ γ_min because C ∉ S; hence γ(C) ≥ m. The hypotheses of
     Theorem 2.8 are those of (d), which are proved before (e).

   Valid. The paper's counting argument (one edge leaves {0}, of weight ≥ 2) is also valid. My model finds that the
   least V({0}, C) is 2 at n = 4, 8, and that γ({0}) = m − 1 and γ(C) = m: 3 and 4 at n = 4, 30 and 31 at n = 8.
8. Theorem 3.9(f), checked on paper, upper bounds.
   * 010: e_1 = 0 + e_1 is a flip of the state 0 of the selected cycle {0}, and it contains 010 at cell 1 (cells 0,
     1, 2 distinct for n ≥ 3). The third clause of Lemma 2.2 gives k_010 ≤ 1.
   * 001, 011, 110, 100: the state with ones at cells 2, 3 contains 001 at cell 1, 011 at cell 2, 110 at cell 3 and
     100 at cell 4. At n = 4 cell 4 is cell 0, and the code there is (x_3, x_0, x_1) = 100.
   * 101: the state with ones at cells 2, 4, 5 contains 101 at cell 3 (x_2 x_3 x_4 = 101). At n = 4 it is the state
     with ones at cells 0, 1, 2, which contains 101 at cell 3 (x_2 x_3 x_0).
   * 111: the state 1 contains it.

   These states lie in M (each has a one on an even and on an odd cell), so they lie on cycles C ≠ {0} with
   γ(C) = m = γ_min + 1 and R(C → D_v) = 0. So k_v ≤ m − (m − 1) = 1. Valid for even n ≥ 4. The lower bound is a
   further route (finding 3).
9. Theorem 3.10: the description matches the Lean proof (`Main.lean` l. 485–569). The only flip of 0 used is cell 0.
   The cycle C' reached is shown to differ from {0} by `lemma_3_4_b_zero`. It is then joined to {1} by a case
   distinction (`hub_parM` when it meets M, `hub_not_parM` otherwise), not by using that it lies in E ∪ O. The code
   states for even n are: ones at 2, 3; at 2, 4, 5; and at 1, 4 (010 at cell 1, which needs n ≥ 5; even n here is
   ≥ 6). For odd n any state containing the code is used. The route to γ = m − 1 is not listed (finding 3).
10. `IsPowTwo`: correct (section A).
11. Theorem 3.11, first case: correct, but incomplete (finding 1).

"No gap or false statement was found in the paper for these statements" (l. 587): I found none either, for the
statements and for the parts of the proofs checked here.

Other README claims checked:
* the table l. 536–546 (each row matches SM);
* "1300 lines of Lean in four new files, of which 131 are statements": 131 + 325 + 249 + 595 = 1300 by `wc -l`;
* "14 theorems": 14 `#check` lines;
* "17 records, n = 4..20, no record for n = 3" (section G).

## F. Computations (my own model)

`out/theorems.txt`, n = 1..12. Here m is the number of cycles, "k_c" lists the k_v in the code order 000, 001, …, 111,
"|S|" is the number of selected cycles, "Closed classes" lists their sizes, and "γ" gives γ({0}) and the set of
values of γ on the other cycles.

| n | m | k_c | k* | \|S\| | Closed classes | γ | Statement whose hypothesis holds | Holds |
|---|---|---|---|---|---|---|---|---|
| 3 | 3 | 0-0-0-0-0-0-0-0 | 0 | 3 | [3] | 2; {2} | 3.10, 3.11 | yes |
| 4 | 4 | 0-1-1-1-1-1-1-1 | 1 | 1 | [1] | 3; {4} | 3.9, 3.11 | yes |
| 5 | 4 | 0-0-0-0-0-0-0-0 | 0 | 4 | [4] | 3; {3} | 3.10, 3.11 | yes |
| 6 | 12 | 0-0-0-0-0-0-0-0 | 0 | 12 | [12] | 11; {11} | 3.10, 3.11 | yes |
| 7 | 8 | 0-0-0-0-0-0-0-0 | 0 | 8 | [8] | 7; {7} | 3.10, 3.11 | yes |
| 8 | 31 | 0-1-1-1-1-1-1-1 | 1 | 1 | [1] | 30; {31} | 3.9, 3.11 | yes |
| 9 | 18 | 0-0-0-0-0-0-0-0 | 0 | 18 | [18] | 17; {17} | 3.10, 3.11 | yes |
| 10 | 62 | 0-0-0-0-0-0-0-0 | 0 | 62 | [62] | 61; {61} | 3.10, 3.11 | yes |
| 11 | 50 | 0-0-0-0-0-0-0-0 | 0 | 50 | [50] | 49; {49} | 3.10, 3.11 | yes |
| 12 | 308 | 0-0-0-0-0-0-0-0 | 0 | 308 | [308] | 307; {307} | 3.10, 3.11 | yes |

* At n = 4 and 8 every one of the eleven conclusions of `Theorem_3_9` holds, including the closed classes (only
  {{0}}) and S = {{0}}. At the other n, every conclusion of `Theorem_3_10` holds: G_1 is strongly connected and γ = m
  − 1 on every cycle.
* All γ values are certified (section "Method", item 4). Edmonds and enumeration agree for m ≤ 6.
* `out/lemmas.txt` (n = 1..12): `Lemma_3_5` holds for every even n ≤ 12. `Lemma_3_6_in_particular` holds for every
  n ≤ 12: 0 colliding pairs for odd n, 2^(n/2) + 1 for even n, all of the paper's three forms. `Lemma_3_7`, together
  with the paper's second sentence and, at n = 4 and 8, the third, holds for even n ≤ 12. So do `Lemma_3_8_a`,
  `Lemma_3_8_b` and the paper's clause "through cycles contained in M".
* G_1 computed from the literal V equals G_1 computed from the criterion of Lemma 2.3, at every even n ≤ 12. The 0-1
  BFS for R equals Dijkstra on all steps for n ≤ 6.
* `out/lemma_3_4_b.txt`: for even n ≤ 24 that are not powers of two (6, 10, 12, 14, 18, 20, 22, 24), the orbit of e_0
  never meets 0, and the same holds for every cell j (the paper's form). For n = 2, 4, 8, 16 the orbit of every e_j
  reaches 0 within n/2 steps (e_0 after exactly n/2), so the hypothesis "not a power of two" is needed.
* `out/n16.txt`: at n = 16, with G_1 from the criterion of Lemma 2.3 and γ pinned by a lower bound and an explicit tree,
  parts (a)–(f) of `Theorem_3_9` hold: m = 4081, k_c = 0-1-1-1-1-1-1-1. The same check at n = 4 and 8 agrees with the
  full computation. This check uses Lemma 2.3, a proved Lean statement, instead of the literal R.

## G. Comparison with `data/fw_sweep.csv` (done last)

`out/sweep_compare.txt`. The file has 17 records of rule 154, n = 4..20, and none for n = 3, as README l. 591–594
says. For every record, the columns `kstar`, `k_c` (code order 4a + 2b + c) and `n_stable` agree with the conclusions
of `Theorem_3_11`: k* = 1, k_c = 0-1-1-1-1-1-1-1 and one selected cycle at n = 4, 8, 16; k* = 0, all k_v = 0 and
`n_stable` = `cycles` otherwise. For n = 4..12 the columns `cycles`, `k_c`, `kstar` and `n_stable` also agree with my
model, and at n = 16 `cycles` = 4081 agrees with `out/n16.txt`. These k_v vectors are symmetric under a ↔ c, so the
comparison cannot detect a mirrored orientation (the earlier report checked orientation separately).

## Not checked

* Lean was not run. I did not check that the proofs compile, the axiom lists, or that the theorems in
  `AxiomCheckRule154.lean` have the claimed types; I read the `#check` lines only.
* Proofs: I read `Main.lean` l. 56–256 and 334–595, and the statements of four lemmas in `Moves.lean`. I did not read
  `Periodic.lean`, the rest of `Moves.lean`, `Main.lean` l. 1–55, the pilot's `pow_two_of_iterate_eq_zero` (used for
  Lemma 3.4(b)), or the proofs of `cycle_subset_parM`, `hub`, `hub_not_parM` and `kIndex_eq_zero_iff`.
  Of `gamma_le_card_add` I read the statement and the outline of the proof.
* The paper's proofs of Lemmas 3.4(b) to 3.8 and of Theorems 3.9 and 3.10, except where sections E.6–E.9 compare
  them with the Lean route.
* Ring sizes beyond the computations:
  * Theorems 3.9 to 3.11 with the literal R: only n ≤ 12;
  * Theorem 3.9 via Lemma 2.3: also n = 16;
  * Lemmas 3.5 to 3.8: n ≤ 12;
  * Lemma 3.4(b): even n ≤ 24.
* γ for n = 11, 12 was taken from breadth-first G_1 trees (optimal because they meet the lower bound), not from
  Edmonds' algorithm.
* Mirror symmetry of the conclusions was not tested: the k_v vectors cannot detect it, and the earlier report covers
  the orientation.
* The definitions of St and R154 again, beyond `git diff` since cf6f77e. The README outside its last section.
  Proposition 2.1, which is not formalized.
* The untracked files of the repository.

No existing file was changed and no commit was made.

Claude
