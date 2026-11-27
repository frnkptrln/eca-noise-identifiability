# Verification: the Lean statements of Section 2 against the paper

> **Handling of the findings (26 November 2026).** Written by Claude, the reader outside the sessions, who wrote
> the Lean files that this report checks and then worked these findings in. The report below is unchanged. Its line
> numbers refer to `Statement.lean` and `lean/README.md` as they stood at 3425cc7.
>
> * Finding 1 (values at n ≤ 2). Stated in the comments of `R` and `kIndex` and in items 4 and 5 of "Differences
>   from the paper" in `lean/README.md`; item 4 now lists every statement of part 3 that holds for all n ≥ 1. The
>   definitions are unchanged.
> * Finding 2: the comment at the top of `Statement.lean` names the files that exist.
> * Finding 3: the comment of `IsInTree` says "for `d ≠ c` and `k = 1`".
> * Finding 4 (orientation untested). Two checks added and proved: `Rule154_local`
>   (`ruleOfNumber 154 a b c = c + a * (1 + b)`, the check the finding proposes) and `Rule170_shift`
>   (`globalMap n (ruleOfNumber 170) x i = x (i + 1)`), which also fixes the orientation of `globalMap`.
> * Finding 5: `Corollary_2_8` is renamed `KStar_unique_class`.
> * Finding 6 (empty graph): stated in the comment of `ClosedClassReachable` and as item 7 of the differences. The
>   paper is not changed.
> * Finding 7: the form for elementary rules is now a statement with a proof, `Section_2_4_ECA` (Lemmas 2.5, 2.6,
>   2.7 and both sentences of Theorem 2.8 for `globalMap n f` and `resistance n f`). The README table says that
>   `Lemma_2_3_general` is not a statement of the paper.
> * Finding 8: `TreeWeight_lower_bound` (every in-tree has weight at least m − 1) is now in `Statement.lean`, with
>   `Gamma_lower_bound` as its consequence; the list "Not formalized" names the noisy chain, ν_v and ρ.
> * Observation on `data/fw_sweep.csv`: the value 0 of `gamma_min` on bijective records is the known placeholder
>   of v0.2 (`code/fw/run_sweep.py`, l. 28; `report_ring_size.md`, l. 153 to 159; `VERIFICATION_ring_size.md`,
>   A17). `paper/make_numbers.py` does not read that column. Nothing changed.
> * After the changes: `lake build` without error or warning, 21 statements, the same three axioms. The reader did
>   not run the scripts in `verify_lean_theorem_a/`; of the report's computations, the reader checked only the
>   codes that occur at n = 1, 2 (by hand) and the local rule of 154 (now a Lean theorem).
> * This pass was not read by a second reader.

Branch `lean-theorem-a`, commit 3425cc7. Checked: `lean/RingSize/TheoremA/Statement.lean` (322 lines) against
Section 2 of `paper/ring_size_paper.tex` (lines 176–338), and the section "Differences from the paper" of
`lean/README.md` (lines 352–376). 26 November 2026.

## Summary

None of the 17 statements in `Statement.lean` claims something different from or weaker than the paper: each is the
paper's statement, an equivalent form of it, or a generalisation that contains it, and the definitions agree with the
paper wherever the paper defines something. The one difference in content is that for n = 1, 2, where the paper
defines nothing, `D`, `R` and `kIndex` give the value 0 to codes that no state contains; the README does not say this
and describes the use of `R` on empty sets incorrectly (finding 1), and findings 2 to 8 concern wording and missing
checks. A literal Python model of the definitions, run on all 256 rules for n = 1, …, 6, found no instance where a
statement fails under its hypotheses, and showed that the hypotheses n ≥ 3 and "unique closed class" are needed and
are satisfied by many instances.

## Method

1. I read `Statement.lean` line by line next to lines 176–338 of the paper and wrote down, for each definition and
   statement, the place in the paper and the comparison (tables A and B below). I also read the import of
   `RingSize/Statement.lean` (the pilot's `State`, `e`, `rule90`) and the axiom check file
   `lean/AxiomCheckTheoremA.lean`, which ascribes each of the 17 theorems to its `Prop`. I did not read the proofs,
   apart from the theorem headers and the lemma names in `Trees.lean` (for README item 7).
2. I wrote a literal Python model of the definitions (`verify_lean_theorem_a/lean_defs.py`). It uses no code from the
   repository and keeps the Lean/Mathlib conventions: `sInf ∅ = 0` on ℕ, truncated subtraction, parent maps with an
   arbitrary value at the root, `IsInTree` exactly as written, and `R` over all non-empty lists, length 0 included.
   Several objects are computed in two independent ways:
   - `R` by Dijkstra and by Floyd–Warshall (n ≤ 4);
   - `gamma` by enumerating all parent maps (m ≤ 6) and by Chu–Liu/Edmonds (networkx);
   - closed classes by enumerating all subsets with `IsClosedClass` (m ≤ 12) and as strongly connected components
     that no edge leaves.
3. On each (rule, n) instance I checked the 17 statements as they are written in Lean (`instance.py`). Lemma 2.5 was
   checked on sampled in-trees: 20 per root, or 5 per root when m > 16. Run for rules 204, 90 and 154 at n = 3 and 4
   (`small_cases.py`) and for all 256 rules at n = 1, …, 6 (`sweep.py`, 1536 instances, 83 s, one process). For
   Lemma 2.2 and the n ≥ 3 corollary, the hypothesis n ≥ 3 was left out on purpose, so that its role is visible.
4. I compared m, k\*, the eight k_v, γ_min and |S| with the data file `data/fw_sweep.csv` (n = 4, …, 6; read as data).
5. I compared `ruleOfNumber` with the local rules written out in the paper for the asymmetric rules 154, 26, 43 and
   142 (`rule_tables.py`). I also evaluated alternative readings of the definitions to find cases where they differ
   (`alternatives.py`, `examples.py`).

## Findings

Severity: **E** = error in a statement; **D** = difference that must be stated; **W** = wording.
No finding has severity E.

1. **D. `kIndex`, `kStar`, `D` and `KIndex_subtraction_exact` at n = 1, 2; README items 4 and 5 are incomplete.**
   Statement.lean l. 110–111 (docstring of `R`), l. 234 (`variable (n : ℕ) [NeZero n]`), l. 250, 263–269, 290–293;
   README l. 364–368. Paper l. 179 ("Fix n ≥ 3"), l. 189, l. 217–220.
   The paper defines D_v, R(C → D_v) and k_v only for n ≥ 3. Lean defines them for every n ≥ 1. For n ≤ 2 some codes
   occur in no state: at n = 1 only 000 and 111 occur, at n = 2 only 000, 010, 101 and 111 (`out/examples.txt`). For
   such a code D_v = ∅, `R … (D n v) = sInf ∅ = 0`, and so `kIndex n f v = 0`. Lean k\* at n ≤ 2 thus counts an
   impossible code as k_v = 0. A literal reading of the paper's formula would give a minimum over an empty set of
   paths, that is +∞.
   Example: rule 204, n = 2, v = 100. D_100 = ∅, Lean k_100 = 0, and no state of a selected cycle contains 100
   (`examples.py`, E1). Part 1 of Lemma 2.2 therefore fails at n = 2: it fails for all 256 rules at n = 1 and at n = 2
   (`out/sweep_summary.txt`). The statements that need n ≥ 3 (`Lemma_2_2`, `Corollary_2_8`) assume it, so nothing
   false is claimed.
   However, the docstring of `R` (l. 110–111) and README item 5 say that "the statements use `R` only for non-empty
   sets (cycles, and `D_v` for n ≥ 3)". `KIndex_subtraction_exact` (l. 290) is stated for every n ≥ 1, so it uses
   `R` on empty sets. It is still true there, since γ_min ≤ min_C γ(C) + 0. README item 4 also lists only
   `Lemma_2_3`, `ResistanceECA` and the general statements as holding for every n ≥ 1. It omits
   `KIndex_subtraction_exact`, `Rule90IsRuleNumber90` and `Rule204_cycles`, which are stated for every n ≥ 1 as well.
   Suggested text: "For n ≤ 2, `kIndex` gives the value 0 to a code that no state contains; the paper does not
   define k_v there."

2. **W. The module docstring names a file that does not exist.** Statement.lean l. 19: "`RingSize/TheoremA/Main.lean`
   proves every statement of this file". There is no `Main.lean`. The 17 theorems are in `Paths.lean`, `ECA.lean`
   and `Checks.lean`, and `lean/AxiomCheckTheoremA.lean` checks their types. Paper: none.

3. **W. The docstring of `IsInTree` claims a little too much.** Statement.lean l. 53–54: "For `k = 1` this says
   `p d ≠ d`". This holds only for d ≠ c: for d = c the hypothesis `∀ j < k, p^[j] d ≠ c` fails at j = 0. The
   definition itself (l. 55–56) is correct, see table A. Paper l. 210 ("edges between distinct cycles").

4. **W. The checks of the rule numbering cannot detect a mirrored neighbourhood.** Statement.lean l. 280–288
   (`Rule90IsRuleNumber90`, `Rule204_cycles`), l. 227–228, l. 238–239. Paper l. 183–187.
   Rules 90 and 204 are their own mirror images (f(a,b,c) = f(c,b,a)). So the two checks would also pass if
   `ruleOfNumber` used the weight 2^(4c+2b+a), or if `globalMap` read (x_{i+1}, x_i, x_{i−1}). Only reversing the
   bit index (7 − (4a+2b+c)) is caught, since it turns 204 into 51 (`out/alternatives.txt`, A3). The definitions as
   written agree with the paper. I checked this on the asymmetric rules: `ruleOfNumber` gives exactly the local rules
   that the paper writes out for rules 154 (l. 371–372 and Lemma 3.2, l. 391: f = c + a(1+b)), 26 (l. 1335–1336),
   142 and 43 (table l. 607–608) (`out/rule_tables.txt`).
   Every statement of Section 2 is invariant under reflection, so a mirrored convention would not change any of them.
   The convention will matter for Stage 4 (rule 154). A check such as
   `ruleOfNumber 154 a b c = c + a * (1 + b)` would close the gap.
   The comparison with `data/fw_sweep.csv` (section D) cannot test orientation either: none of the 1024 instances
   with n = 3, …, 6 has a k_v vector that changes under abc ↦ cba.

5. **W. The name `Corollary_2_8` suggests a numbered result that the paper does not have.** Statement.lean l. 312–320.
   Paper l. 325–326: an unnumbered sentence after the proof of Theorem 2.8. Since theorem-like environments share one
   counter per section, a corollary there would be numbered 2.9. The docstring and the README table describe the
   statement correctly as "the sentence after Theorem 2.8". The content matches (table B).

6. **W. The paper's sentence "Every finite directed graph has a closed class" is false for the empty graph; the Lean
   form is correct.** Statement.lean l. 176–180 (`ClosedClassReachable`). Paper l. 250–251.
   `ClosedClassReachable` says only that from every node there is a path into a closed class. That implies existence
   for every non-empty graph and is true for the empty graph. The paper's first clause fails for the empty graph,
   because a closed class is a component and so is non-empty. This does not matter in the paper, where the graph
   always has at least one cycle as a node. README "Differences" does not mention it. The paper is not changed here.

7. **W. The general statements are not stated for elementary rules in Lean.** Statement.lean l. 155–197; README
   l. 343–345 and item 3. Paper l. 253–323.
   `Lemma_2_5`, `Lemma_2_6`, `Lemma_2_7` and `Theorem_2_8` are stated for every finite `X`, `F` and `r` with
   `IsResistance F r`, which is stronger than the paper. The paper's form, for `globalMap n f` and `resistance n f`,
   follows by applying them to `ResistanceECA`. That is a one-line instantiation, but it is not written down as a Lean
   term, so the claim that they hold "in particular for every elementary rule and every ring size" (README l. 344–345)
   rests on that one step. Similarly, `Lemma_2_3_general` (l. 155–160) is not a statement of the paper. It is the
   content of the converse half of the proof of Lemma 2.3 (paper l. 260–263); README item 3 calls it "Lemma 2.3
   (first form)".

8. **W. Not formalized and not listed in README "Not formalized" (l. 378–382).** Paper l. 191–198 (the noisy chain,
   its kernel, the positivity of the kernel and the uniqueness and full support of π_ε) and l. 222–225 (ν_v and ρ).
   These belong to the context of Proposition 2.1, which is listed, so this concerns completeness of the list only.
   The sentence "every in-tree has weight at least m − 1" (paper l. 322) is formalized only for the minimum:
   `Gamma_lower_bound` (l. 213–216) states `m − 1 ≤ γ(C)`. The statement for every tree,
   `card_sub_one_le_treeWeight`, is proved in `Trees.lean` but is not in `Statement.lean`.

Observation outside `Statement.lean`. In `data/fw_sweep.csv` the column `gamma_min` is 0 on all 18 rows of bijective
rules (n = 4..6). The paper's definition gives γ_min = m − 1 there (for example rule 15, n = 4: m = 6, γ_min = 5;
rule 204, n = 4: m = 16, γ_min = 15; `examples.py`, E3). So that column is not the paper's γ_min for bijective rules.
k\* and k_v in that file agree with the definitions on all rows. I have not checked whether the paper uses that
column anywhere.

## A. Definitions

| Lean (Statement.lean) | Paper | Verdict | Remarks |
|---|---|---|---|
| `IsInTree` l. 55 | l. 209–211 | same | Parent map. `p c` is free: for d = c the hypothesis fails at j = 0. For d ≠ c, k = 1 gives `p d ≠ d` (distinct cycles). The clause "without passing through the root" excludes exactly the circuits that do not contain c; a circuit through c would need an out-edge of c, which the tree does not have. The maps restricted to ι∖{c} are exactly the paper's trees (one out-edge per D ≠ C, m − 1 edges). Without the clause no map would qualify, γ = sInf ∅ = 0 everywhere (A2: rule 154, n = 4, γ = [3,4,4,4] becomes [0,0,0,0]). If circuits were allowed, S would change (A2c: rule 130, n = 3, S = {C0,C1} becomes {C0,C1,C2}). So the definition carries content, and the content is the paper's. |
| `treeWeight` l. 59 | l. 211–212 | same | Sum over d ≠ c of V(d, p d); does not depend on `p c`. |
| `gamma` l. 63 | l. 209 | same | The set is never empty (the star `fun _ => c` is a tree), so sInf is a minimum. For m = 1 the value is 0, the weight of the empty tree, as in the paper. Brute force over parent maps equals Edmonds on every instance with m ≤ 6. |
| `gammaMin` l. 67 | l. 213 | same | sInf of the range. Empty only when there are no cycles (X = ∅), which never happens for {0,1}^n. In the general part, X = ∅ makes all statements vacuous and none false (no closed class exists). |
| `Sel` l. 71 | l. 213–214 | same | |
| `G1` l. 75 | l. 249 | same | V(C,C) = 0 in both, so there are no loops. |
| `Reach` l. 79 | l. 250 ("directed path") | same | Reflexive–transitive closure; paths of length 0 included. |
| `IsClosedClass` l. 86 | l. 249–250 | equivalent | Non-empty, mutually reachable, closed under G1 edges. Such a set is maximal, because everything reachable from it lies in it, so it is an SCC that no edge leaves; the converse is immediate. `ClosedClass_iff_component` states this. Subset enumeration equals the SCC computation on every instance with m ≤ 12. |
| `IsResistance` l. 99 | l. 204 | same (as a property) | Only this property of r is used in the general part. |
| `pathRes`, `R` l. 104, 112 | l. 203–205 | same for non-empty A, B | Length-0 paths allowed. When the source is a cycle this makes no difference: 0 differences in 20 882 values V(C,C′) and R(C → D_v) at n = 3, 4 (A1). It would differ for other sources: rule 0, n = 3, A = B = {111} gives 0 vs 3 (A1b). The paper uses R only with a cycle as source, R(C → ·), including o(x) in Prop. 2.1. Head ∈ A and last ∈ B, as "from a state of A to a state of B". Empty A or B gives 0, see finding 1. |
| `orbit`, `IsCycle`, `Cyc` l. 116–125 | l. 201 | same | `periodicPts` is "∃ t ≥ 1, F^t x = x". Cycles are sets, so two states of one cycle give one node. |
| `numCycles` l. 134 | l. 202 (m) | same | |
| `EndsOn` l. 138 | l. 202–203 | same | |
| `Vc` l. 142 | l. 207 | same | |
| `ruleOfNumber` l. 227 | l. 183–184 | same | Bit 4a+2b+c, a the left cell. Agrees with the tables of rules 154, 26, 43, 142 in the paper (finding 4). |
| `globalMap` l. 238 | l. 185–187 | same | f(x(i−1), x i, x(i+1)) in `ZMod n`; for n = 1, 2 the three cells coincide partly (finding 1). |
| `resistance` l. 242 | l. 194–196 | same | `hammingDist (F x) y`. |
| `Contains`, `D` l. 246, 250 | l. 188–189 | same for n ≥ 3 | |
| `flip` l. 255 | l. 181 | same | `x + e n j` in ZMod 2. |
| `kIndex` l. 263 | (1), l. 218–221 | same for n ≥ 3 | The minimum is over all cycles, as in the paper. The subtraction in ℕ is exact (`KIndex_subtraction_exact`). For n ≤ 2, see finding 1. |
| `kStar` l. 268 | (1), l. 219 | same | `Finset.sup` over the 8 codes; ⊥ = 0 does not matter, since all k_v ≥ 0. |

## B. Statements

| Lean | Paper | Verdict | Hypotheses |
|---|---|---|---|
| `EndsOnExactlyOneCycle` l. 150 | l. 202 | same | none; holds on all 1536 instances |
| `Lemma_2_3_general` l. 155 | proof of Lemma 2.3, l. 259–263 | not a paper statement; equivalent to Lemma 2.3 for r = H(Fx, y) | `IsResistance` (satisfiable: `ResistanceECA`) |
| `Lemma_2_5` l. 165 | Lemma 2.5, l. 280–283 | same, for every X, F, r (stronger) | `IsInTree B p`, `N ≠ B`; the new tree is `update p B N` with root N: the out-edge of N is dropped because the root's value is ignored, and B → N is added |
| `Lemma_2_6` l. 172 | Lemma 2.6, l. 289–291 | same, general | |
| `ClosedClassReachable` l. 178 | l. 250–251 | same for non-empty graphs; see finding 6 | any finite ι and V; every finite digraph is G1 of some V |
| `Lemma_2_7` l. 183 | Lemma 2.7, l. 296–298 | same, general | |
| `Theorem_2_8` l. 190 | Theorem 2.8, l. 312–315 | equivalent, general | First part: "each C ∈ S lies in a closed class K ⊆ S", which is equivalent to "S is a union of closed classes". Second part: K closed and every closed class equals K, hence unique (satisfied on 988 of the instances with n ≥ 3). The uniqueness hypothesis is needed: rule 232, n = 3 has two closed classes and γ_min = 2 ≠ m − 1 = 1 (E4). In ℕ, m − 1 is exact because K ≠ ∅ gives m ≥ 1. |
| `InTree_iff_reaches` l. 202 | — (check) | correct check | |
| `ClosedClass_iff_component` l. 207 | — (check of l. 249–250) | correct check | no finiteness assumed |
| `Gamma_lower_bound` l. 213 | proof of Thm 2.8, l. 322 | weaker than the sentence (finding 8) | |
| `ResistanceECA` l. 276 | l. 204 for r = H(Fx, y) | same, every n ≥ 1 | |
| `Rule90IsRuleNumber90` l. 280 | — (check) | correct; orientation-blind (finding 4) | |
| `Rule204_cycles` l. 285 | — (check) | correct; orientation-blind (finding 4) | |
| `KIndex_subtraction_exact` l. 290 | — (check) | correct, every n ≥ 1 (finding 1) | |
| `Lemma_2_2` l. 298 | Lemma 2.2, l. 237–240 | same, all three parts | `3 ≤ n`, needed (finding 1); `[NeZero n]` is redundant with it but harmless. "Jointly contain all eight codes" = ∀ v ∃ C ∈ S ∃ x ∈ C, x contains v. |
| `Lemma_2_3` l. 307 | Lemma 2.3, l. 253–257 | same; stronger (every n ≥ 1) | `C ≠ C′`; the third part takes x ∈ C, x + e_j ∈ C′, which is the paper's "periodic and on different cycles C and C′" |
| `Corollary_2_8` l. 315 | sentence l. 325–326 | same | `3 ≤ n` (needed: at n = 1, 2 it fails for 128 and 64 rules); unique closed class |

No statement is empty or trivially true: every hypothesis is satisfied by some instance, and no definition makes a
conclusion automatic. The two places where an empty set could make a statement trivial (`sInf ∅ = 0` in `gamma` and
in `R`) do not apply: the set in `gamma` is never empty, and `R` is applied to empty sets only at n ≤ 2 (finding 1).

## C. The seven "Differences from the paper" in lean/README.md

1. In-trees: correct. The parent map is many-to-one onto trees (|ι| choices of `p c`), which does not affect any
   statement. Only the docstring needs care (finding 3).
2. Closed classes: correct.
3. Generality: correct. See finding 7 for the missing explicit instantiation.
4. Ring size: correct but incomplete (finding 1). The reason given for n ≥ 3 ("some codes occur in no state") is
   correct; my computation shows which codes.
5. R of an empty set: inaccurate for `KIndex_subtraction_exact` and for the definitions at n ≤ 2 (finding 1).
6. Subtraction: correct.
7. Proofs: consistent with the lemma names in `Trees.lean` (`reroot_path_strict`: "re-rooting along a path of G_1";
   `lev`: "the nodes from which c is reached in at most k steps"). I did not read the proofs.

Missing from the list: finding 1 (values at n ≤ 2), finding 4 (orientation untested), finding 6 (empty graph), and
the fact that `Lemma_2_3_general` and the general statements need `IsResistance`, which `ResistanceECA` supplies.

## D. Small cases (from the literal model; `out/small_cases.txt`)

| rule, n | m | γ | γ_min | S | closed classes | k_v (000 … 111) | k\* |
|---|---|---|---|---|---|---|---|
| 204, 3 | 8 (every state) | all 7 | 7 = m − 1 | all | one (all) | 0 0 0 0 0 0 0 0 | 0 |
| 204, 4 | 16 | all 15 | 15 = m − 1 | all | one (all) | 0 0 0 0 0 0 0 0 | 0 |
| 90, 3 | 4: {000}, {011}, {101}, {110} | all 3 | 3 | all | one (all) | 0 1 1 0 1 0 0 1 | 1 |
| 90, 4 | 1: {0000} | 0 | 0 | {0000} | one | 0 1 1 2 1 1 2 2 | 2 |
| 154, 3 | 3: {000}, the six states with one or two ones, {111} | all 2 | 2 | all | one (all) | 0 0 0 0 0 0 0 0 | 0 |
| 154, 4 | 4: {0000}, two cycles of length 4, {1111} | 3, 4, 4, 4 | 3 | {0000} | one: {{0000}} | 0 1 1 1 1 1 1 1 | 1 |

Comparison with the paper:
- Rule 154: Theorem 3.1(a) (l. 344) gives k\* = 0 at n = 3 and k\* = 1 at n = 4 = 2². Both agree. At n = 4 the
  values are those of Section 3.1 for powers of two: no edge of G1 leaves {0}, V({0}, C) ≥ 2 (l. 510);
  γ({0}) = m − 1 = 3 and γ(C) = m = 4 otherwise, S = {{0}} (l. 514); k_000 = 0 and k_v = 1 for the seven other
  codes (l. 593).
- Rule 90: at n = 4 the zero state is the only cycle, as l. 1666–1668 state for powers of two. At n = 3 the non-zero
  periodic states are the three rotations of 011 (l. 1044). Both agree.
- Rule 204: every state is a cycle (`Rule204_cycles`), and k\* = 0, as the paper states for bijections (l. 1658).
  Agrees.
- In all six cases G1 has one closed class, and S = K and γ_min = m − 1, as Theorem 2.8 says.

Sweep (`out/sweep_summary.txt`, `out/sweep_n1_6.csv`): for n ≥ 3, every statement check passes on all 1024
instances. The two computations of R, of γ and of the closed classes agree wherever both were run. The data file
agrees on m (264 of 264 rows), k\* (264 of 264), k_v (264 of 264), and γ_min and |S| (246 of 246 non-bijective rows).
The only failures are `Lemma_2_2` and `Corollary_2_8` at n = 1, 2, where the checker deliberately leaves out n ≥ 3.

## What I did not check

- The Lean proofs themselves, and whether `lake build` succeeds. Lean was not run, as instructed. I rely on the README
  for the build and on `AxiomCheckTheoremA.lean` for the type ascriptions.
- That the Lean elaborator reads the statements as I read them: implicit arguments, the choice of the noncomputable
  `Fintype`/`DecidableEq` instances on `Cyc F` (any instance gives the same `Finset.univ` and the same `update`), and
  universe levels.
- Lemma 2.5 on all in-trees: only on sampled trees (20 per root, or 5 per root when m > 16).
- Instances with n ≥ 7. Between n = 3 and 6, S always equals the union of all closed classes (36 instances with
  two or more closed classes). So the small cases do not separate "S is a union of closed classes" from the stronger
  "S is the union of all closed classes". The paper's rule 94 (Section 3.3, l. 1028 ff.) is where they separate.
- Proposition 2.1, Lemma 2.4, rule 154 (Stage 4) and Sections 3–6 of the paper, beyond the comparisons in D and
  finding 4.
- Whether the paper uses the `gamma_min` column of `data/fw_sweep.csv` anywhere.

## Files

`verify_lean_theorem_a/`: `lean_defs.py` (literal model of the definitions), `instance.py` (objects and statement
checks per instance), `small_cases.py`, `sweep.py`, `alternatives.py`, `examples.py`, `rule_tables.py`, `README.md`.
Their outputs are in `out/`. Run each from that directory with `python <script>.py`; this needs networkx.
`sweep.py` and `examples.py` take the path of `data/fw_sweep.csv` as their argument (default
`../data/fw_sweep.csv`); `sweep.py` must run before `examples.py`. No existing file was changed, and nothing was committed.

Claude
