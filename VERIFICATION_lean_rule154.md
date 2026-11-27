# Verification: the Lean statements of Lemma 2.4 and of rule 154 (Section 3.1) against the paper

> **Handling of the findings (27 November 2026).** Written by Claude, the reader outside the sessions, who wrote
> the Lean files that this report checks and then worked these findings in. The report below is unchanged. Its line
> numbers refer to the Lean files and `lean/README.md` as they stood at cf6f77e.
>
> * Finding 1 (ring sizes not listed): item 4 of the differences in `lean/README.md` now names `GlobalMap_rot`,
>   `Resistance_rot`, `Lemma_2_4`, `Zero_cycle` (every n ≥ 1) and `Single_mem` (every n).
> * Finding 2 (the exponent k): stated in the comment at the top of `Rule154/Statement.lean`, in the comments of
>   `Lemma_3_4_a` and `Theorem_3_9_b`, and in item 4. The statements are unchanged.
> * Finding 3 (`Rule170_shift`): its comment now says that it fixes the orientation of `globalMap` given the rule
>   numbering, and that the case "both mirrored" is excluded by `Rule154_local`. The README says the same and adds
>   the observation of the finding that no statement depends on the orientation.
> * Finding 4 (invariance stated pointwise): a clause was added to `Lemma_2_4_general` and `Lemma_2_4`, "every
>   cycle is the image of a cycle", and proved. With the injectivity of `σ` this makes `C ↦ σC` a bijection of
>   the cycles, so `σ(S) = S` and the automorphism of `G_1` follow; the comments and item 2 say so. The clause on
>   injectivity itself is not stated (it is the injectivity of `σ` on sets of states).
> * Finding 5 (dependencies of Theorem 3.9(b)): item 5 lists what the Lean proof uses, in the words the finding
>   proposes.
> * Finding 6: the comment at the top of `Rule154/Statement.lean` names Theorem 3.11.
> * After the changes: `lake build` without error or warning, the same 30 theorems checked against their
>   statements, the same three axioms. The reader did not run the scripts in `verify_lean_rule154/`. The new
>   clause of finding 4 was checked by Lean and not read by a second reader.

Branch `lean-rule-154`, commit cf6f77e. Checked: `lean/RingSize/TheoremA/StatementRotation.lean` (72 lines),
`lean/RingSize/Rule154/Statement.lean` (77 lines), the statements `Rule154_local`, `Rule170_shift`,
`Section_2_4_ECA`, `TreeWeight_lower_bound` and the renamed `KStar_unique_class` in
`lean/RingSize/TheoremA/Statement.lean`, and the last section of `lean/README.md` (lines 429–501), against
`paper/ring_size_paper.tex` (Section 2, lines 176–338; Section 3.1, lines 369–598). 27 November 2026.

In this report "SR" is `StatementRotation.lean`, "R154" is `Rule154/Statement.lean`, "St" is
`TheoremA/Statement.lean`, and "l." without a file name is a line of the paper.

## Summary

None of the 14 statements checked here claims something different from or weaker than the paper: each is the
paper's statement, an equivalent form, the written-out instance (`Section_2_4_ECA`), or a form that also covers
n = 1, 2 (or n = 2) and is true there, so there is no finding of severity E or D. The six findings are wording: ring
sizes the README does not list, the shifted exponent k, what `Rule170_shift` alone detects, the pointwise form of
"invariant", the dependencies named in README item 5 (whose argument is valid), and a missing theorem number. An
independent Python model of the Lean definitions reproduces every statement on the cases computed (rule 154 for
n = 1..8, all of E ∪ O for even n ≤ 16, ten asymmetric rules for n = 3..6), and shows that `Lemma_3_3`,
`Lemma_3_4_a` and `Theorem_3_9_b` fail outside the ring sizes they assume.

## Method

1. I read the two statement files and the five statements of St line by line next to the paper. I wrote down, for
   each definition and statement, its place in the paper and the comparison (tables A and B). I read the imports from
   St and from the pilot's `RingSize/Statement.lean` (`State`, `rule90`, `e`) and the two axiom check files, which
   assign to each theorem its `Prop`. Of the proofs, I read `Rule154/Pow2.lean` in full, for README items 5 and 6.
   I also read lines 130–205 of `Rotation.lean`, where `lemma_2_4` is derived from `lemma_2_4_general`.
2. `git diff 3425cc7 cf6f77e` shows that the paper is unchanged since the earlier verification. In St only comments
   changed, four statements were added, and `Corollary_2_8` was renamed to `KStar_unique_class` with the same
   body. In `ECA.lean` only the theorem name changed. So the definitions checked in `VERIFICATION_lean_theorem_a.md`
   are the ones used here.
3. I wrote a literal Python model of the Lean definitions, `verify_lean_rule154/model.py`. It uses no code from the
   repository. It keeps the conventions of the Lean files: cells are `ZMod n` with `i.val` = i, `parE`/`parO` go
   through `i.val`, `IsCycle` means "the orbit of a periodic point", `R` ranges over all non-empty lists (length 1
   included) and is computed by Dijkstra, and `sInf ∅ = 0`. `IsInTree` is coded exactly as written. `gamma` is
   computed by enumerating all parent maps when m ≤ 6 and by Edmonds' algorithm (networkx) otherwise; the two methods
   agree wherever both were run. Scripts and outputs (in `verify_lean_rule154/out/`):
   - `rule154_small.py`: rule 154 at n = 1..8. It lists the cycles, V({0}, C) for every cycle C and the edges of G_1
     out of {0}, and checks both clauses of `Theorem_3_9_b`. As a cross-check, the edges out of {0} are compared
     with the cycles on which the orbit of some e_j ends (Lemma 2.3). Run time 5 s.
   - `parity_checks.py`: `Lemma_3_3` (all three clauses) on every state of E and of O for even n = 2..16, and
     `Lemma_3_4_a` on every state of E ∪ O. For each even n it also records whether F^(n/2) x = 0 holds on all of
     E ∪ O, and the largest time to reach 0. It checks `Single_mem` for n = 1..16, and what `parE`, `parO` and
     Lemma 3.3 give at odd n. For "∀ t", F^t x and L^t x are compared until the F-orbit of x repeats. From then on both
     sequences repeat with the same period, so equality holds for all t. Run time under 1 s.
   - `rotation_checks.py`: `GlobalMap_rot` and `Resistance_rot` for all 256 rules at n = 1..6 (all states and all
     pairs). Then `Lemma_2_4` in full (images of cycles are cycles under the literal `IsCycle`; C ↦ σC is a
     bijection; V, γ, S and G_1 are preserved) for the asymmetric rules 154, 26, 43, 142, 30, 110, 14, 2, 184 and 106
     at n = 3..6. Then `Lemma_2_4_general` with s = complement for rules 150 and 105, and with the reflection, which
     does not commute with F, for rule 154. Run time 14 s.
   - `section_2_4_check.py`: closed classes, S, γ_min and m − 1 for rule 154 at n = 2, 4, 6, 8, as a sanity check
     of the instance `Section_2_4_ECA` against Theorems 3.9(d), (e) and 3.10. Run time 5 s.
   - `orientation.py`: `Rule154_local` and `Rule170_shift` under the four combinations of a mirrored or unmirrored
     `ruleOfNumber` and `globalMap`. It also checks Lemmas 3.3, 3.4(a) and Theorem 3.9(b) for the mirror image of
     rule 154 (rule 210). Run time 2 s.

   All scripts ran in one process, one after the other. Run each from `verify_lean_rule154/` with
   `export PYTHONPATH=. && python <script>.py`; only networkx is needed.
4. Only at the end did I compare my numbers with `reader_checks/lean_rule154/out.txt`, the author's check (section D).
   I did not use its code.

## Findings

Severity: **E** = error in a statement; **D** = difference that must be stated; **W** = wording.
No finding has severity E or D.

1. **W. Statements that hold for every n ≥ 1 and that the README does not list.** SR l. 49–50 (`GlobalMap_rot`),
   l. 53–55 (`Resistance_rot`), l. 61–68 (`Lemma_2_4`); R154 l. 42–43 (`Zero_cycle`), l. 62–63 (`Single_mem`, which
   holds for every n : ℕ, n = 0 included); README l. 466–468 (item 4) and l. 377–384 (item 4 of the Section 2
   part). Paper l. 179 ("Fix n ≥ 3").
   README item 4 of the new section names only `Lemma_3_3`, `Lemma_3_4_a` and `Theorem_3_9_b` as covering ring sizes
   outside the paper. The list in item 4 of the Section 2 part ("All other statements of part 3 are stated and
   proved for every n ≥ 1") names statements of St only. The rotation statements are stated for every n ≥ 1
   (`[NeZero n]`), and the paper fixes n ≥ 3. They are true there: `rotation_checks.py` (1) checks commutation and
   resistance for all 256 rules at n = 1, 2. Nothing false is claimed. Suggested sentence for item 4: "`GlobalMap_rot`,
   `Resistance_rot`, `Lemma_2_4` and `Zero_cycle` are stated for every n ≥ 1, `Single_mem` for every n."

2. **W. The exponent k in Lean is the paper's k − 1.** R154 l. 57–59 (`Lemma_3_4_a`), l. 69–73 (`Theorem_3_9_b`);
   README table l. 448, 450. Paper l. 410 and l. 507 ("n = 2^k, k ≥ 2").
   Lean writes n = 2^(k+1) with k ≥ 0, so Lean's k = 1 is the paper's k = 2, which is n = 4. The docstrings and the
   README say "that is, for every power of two n ≥ 2", which is correct. The range of n is the paper's range with n = 2
   added. The variable k, however, does not mean what it means in the paper: with k = 2, the paper's case is n = 4
   and Lean's is n = 8. Anyone who later states Theorem 3.9(c) (path length ≤ n/2) or other parts in terms of k
   should not mix the two. Suggestion: a sentence in the docstrings, "the `k` here is the paper's `k − 1`".

3. **W. `Rule170_shift` alone does not fix the orientation of `globalMap`; together with `Rule154_local` it does.**
   St l. 305–309; README l. 359–361. Paper l. 183–187.
   The docstring says that rule 170 checks "the orientation of rule numbering and global map together" and that a
   mirrored neighbourhood in `globalMap` "would give x_{i−1}". That is true only if `ruleOfNumber` stays as it is.
   If both are mirrored (bit 4c+2b+a and (x_{i+1}, x_i, x_{i−1})), `Rule170_shift` still holds
   (`out/orientation.txt`, last of the four rows). `Rule154_local` fails in exactly the two rows where `ruleOfNumber`
   is mirrored. So the pair catches every wrong combination, as README l. 360–361 says ("These two fail if …"). The
   docstring of `Rule170_shift` should say that it does so given `Rule154_local`.
   Related observation: the statements on rule 154 do not depend on the orientation at all. Lemma 3.3, Lemma 3.4(a)
   and Theorem 3.9(b) hold equally for the mirror image of rule 154, rule 210 (`out/orientation.txt`), and
   `GlobalMap_rot` and `Lemma_2_4` hold for both directions of rotation (`out/rotation_checks.txt`, (1)). The
   orientation checks therefore ensure that "154" in Lean names the rule of the paper (l. 371–372). They do not
   protect any truth value in these files. The direction of `rot`, (σx)_i = x_{i−1} (SR l. 45–46, paper l. 182),
   agrees with the paper; that was checked by reading only, since no statement could detect the other direction.

4. **W. "S and G_1 are invariant under rotation" is stated pointwise; σ(S) = S as sets needs one more step that is
   not stated.** SR l. 61–68 (and l. 34–42); README l. 461–462 (item 2). Paper l. 267–268.
   Lean states: σC ∈ S iff C ∈ S, and σC → σC′ is an edge of G_1 iff C → C′ is. For the paper's sentence read as
   σ(S) = S, and as "σ is an automorphism of G_1", one also needs that C ↦ σC is a bijection of the set of cycles.
   It is: σ is injective on sets of states and there are finitely many cycles. `rotation_checks.py` confirms it on
   every instance. The proof builds this bijection as `τ : Cyc F ≃ Cyc F` (Rotation.lean l. 147–151), but the
   statement does not contain it. Nothing in the two readings can disagree, since the Lean form together with this
   bijection gives σ(S) = S. README item 2 says exactly what is stated, so this is wording only. Possible addition: a
   clause "`C ↦ σC` is a bijection of the cycles", or a remark in the docstring.
   On the hypotheses `D.1 = s '' C.1`: they cannot make the second clause vacuous. The first clause gives, for every
   C, a cycle D = ⟨s '' C.1, _⟩, and D is unique by `Subtype.ext`. Without the first clause the second could be
   empty for some C: for the reflection and rule 154, which do not commute, the image of a cycle is not a cycle at
   n = 4 (cycle {0011, 1011, 1100, 1110}) and at n = 6 (`out/rotation_checks.txt`, (3)).

5. **W. README item 5: the argument is correct, and the list of what it uses is incomplete.** README l. 469–472;
   Pow2.lean l. 158–192. Paper l. 521–525 (proof of Theorem 3.9(b)), l. 509 (part (a)), l. 472–485 (Lemma 3.7),
   l. 201–203.
   The paper uses part (a), the list of the cycles (from Lemma 3.7, which rests on Lemmas 3.5 and 3.6), to conclude
   that no state of the orbit of e_j lies on a cycle other than {0}. The Lean argument is as follows. If the orbit of
   e_j ends on a cycle C, say F^t(e_j) ∈ C, then F^(t+n/2)(e_j) ∈ C, since cycles are invariant under F. Also
   F^(t+n/2)(e_j) = F^t(F^(n/2) e_j) = F^t(0) = 0 by Lemma 3.4(a) and F(0) = 0. So 0 ∈ C, and two cycles with a
   common state are equal, so C = {0}. I checked this on paper and it is valid. It is the paper's own sentence of
   2.2, "the orbit of every state enters exactly one cycle" (l. 202), applied to e_j, whose orbit enters {0}. It
   needs neither part (a) nor Lemmas 3.5–3.7. The paper's proof is also correct; it uses more than it needs.
   README item 5 says (b) "depends only on Lemmas 2.3, 3.2, 3.3 and 3.4(a)". The Lean proof also uses
   `Single_mem` (e_j ∈ E ∪ O), F(0) = 0 (`F154_zero`), and the two facts about cycles above (`Cyc.iterate_mem`,
   `Cyc.eq_of_mem`). Lemma 3.3 enters only through Lemma 3.4(a). These additions are elementary and are not
   statements of the paper. Suggested wording: "… only on Lemmas 2.3, 3.2 and 3.4(a) (with 3.3), on e_j ∈ E ∪ O, on
   F(0) = 0 and on the fact that cycles are invariant and disjoint."

6. **W. The module docstring of R154 omits Theorem 3.11.** R154 l. 17: "Not in this file: Lemma 3.4(b), Lemmas 3.5 to
   3.8, the other parts of Theorem 3.9, and Theorem 3.10." Theorem 3.11 (l. 591–598, `154:thm:main`) is not in the
   file either. README l. 487–488 lists it correctly.

No statement is empty or trivially true because of a definition. Every hypothesis is satisfiable: `Zero_cycle` gives
the cycle C0 of `Theorem_3_9_b`, E and O have 2^(n/2) states, and there are cycles other than {0} at every
n = 2^(k+1), for instance {1}. The only clause that holds for a trivial reason is the case C = C0 of the second
clause of `Theorem_3_9_b`: V(C0, C0) = 0 through the list [0], and Pow2.lean l. 186–191 proves it so. The paper has
the same convention (G_1 has no loops, since V(C, C) = 0), so this is not a difference.

## A. Definitions

| Lean | Paper | Verdict | Remarks |
|---|---|---|---|
| `rot` SR l. 45–46 | l. 182 | same | `fun i => x (i - 1)` = (σx)_i = x_{i−1}. The direction was checked by reading; no statement detects it (finding 3). |
| `F154` R154 l. 27–28 | l. 371–372 | same | `globalMap n (ruleOfNumber 154)`; bits 1, 3, 4, 7 of 154 are set, so f = 1 exactly on 001, 011, 100, 111. |
| `parE` R154 l. 33–34 | l. 373–374 | same for even n | Zero on cells with odd `i.val`. For even n the parity of `i.val` is the parity of i mod n, so the neighbours i ± 1 have the other parity, also across the cell 0. E ∩ O = {0} (checked n = 2..16). |
| `parO` R154 l. 37–38 | l. 373–374 | same for even n | Zero on cells with even `i.val`. |
| `parE`, `parO` at odd n | not defined | not used | At odd n the cells 0 and n − 1 are both "even", and Lemma 3.3 would fail. Example n = 3, x = 001 (x_2 = 1) ∈ parE: F x = 110 = L x, but F x ∉ parO, since cell 0 carries 1. Every statement that uses the classes assumes n even, except `Single_mem`, which is true for every n (`out/parity_checks.txt`). README item 3 is correct. |
| `rule90 n` (pilot) as L | l. 376–377 | same | x_{i−1} + x_{i+1} = (σ + σ^{−1})x with σ as above. |
| `e n j` (pilot) | l. 181 | same | |

## B. Statements

| Lean | Paper | Verdict | Remarks and computation |
|---|---|---|---|
| `Lemma_2_4_general` SR l. 34–42 | Lemma 2.4, l. 266–273 | stronger (generalisation) | Any `s : X ≃ X` with F∘s = s∘F and r(sx, sy) = r(x, y), the two properties named in the proof (l. 271). No `IsResistance` is needed. Checked with s = complement for rules 150 and 105 at n = 3..6. Hypotheses matter: finding 4. |
| `GlobalMap_rot` SR l. 49–50 | l. 188 ("Fσ = σF") | same, every n ≥ 1 | All 256 rules, n = 1..6. Holds for both directions of rotation. Finding 1. |
| `Resistance_rot` SR l. 53–55 | proof of Lemma 2.4, l. 271 | same, every n ≥ 1 | All 256 rules, n = 1..6, all pairs. |
| `Lemma_2_4` SR l. 61–68 | Lemma 2.4, l. 266–268 | same; every n ≥ 1 | Clause 1 = "σ maps cycles to cycles" (l. 271). Clause 2: V, γ, S, G_1. Ten asymmetric rules, n = 3..6, 40 instances, all clauses hold; on 13 of them the rotation moves at least one cycle. Findings 1, 4. |
| `Zero_cycle` R154 l. 42–43 | l. 475, 509 ({0} is a cycle) | true, every n ≥ 1 | Auxiliary; f(0,0,0) = 0. Ensures that C0 in `Theorem_3_9_b` exists. |
| `Lemma_3_3` R154 l. 49–53 | Lemma 3.3, l. 399–402 | same; also n = 2 | All three clauses on every state of E and O, even n = 2..16. At n = 2, L = 0 and F = 0 on E ∪ O (F: 00, 01, 10 ↦ 00, 11 ↦ 11), so the lemma holds there trivially but truly. |
| `Lemma_3_4_a` R154 l. 57–59 | Lemma 3.4(a), l. 410 | same; also n = 2 | `n / 2` = 2^k exactly. Every state of E ∪ O at n = 2, 4, 8, 16. The time n/2 is attained (largest times 1, 2, 4, 8). At even n that is not a power of two (6, 10, 12, 14) the conclusion fails, so the hypothesis is needed. Finding 2. |
| `Single_mem` R154 l. 62–63 | proof of Theorem 3.9(b), l. 522 | same; every n | n = 1..16. |
| `Theorem_3_9_b` R154 l. 69–73 | Theorem 3.9(b), l. 507, 510 | same; also n = 2 | Both clauses at n = 2, 4, 8 (least V({0}, C) = 2, no G_1 edge out of {0}). False at n = 1, 3, 5, 6, 7 (least V = 1), which are excluded by the form n = 2^(k+1). Clause 1 with C ≠ C0 is "V({0}, C) ≥ 2 for every cycle C ≠ {0}"; clause 2 is "no edge of G_1 leaves {0}". Finding 2. |
| `Rule154_local` St l. 302–303 | Lemma 3.2, l. 390–392 | same | The eight values agree with l. 394–396. |
| `Rule170_shift` St l. 308–309 | — (check of l. 183–187) | correct check | Rule 170 is not in the paper. Finding 3. |
| `Section_2_4_ECA` St l. 340–349 | Lemmas 2.5, 2.6, 2.7, Theorem 2.8, l. 280–315 | exactly the instance | Compared part by part with `Lemma_2_5` (St l. 166–170), `Lemma_2_6` (l. 173–175), `Lemma_2_7` (l. 185–187) and `Theorem_2_8` (l. 192–196), with X = `State n`, F = `globalMap n f`, r = `resistance n f`, `Vc F r` = `VE n f`. The texts agree symbol for symbol. The only change is that the hypothesis `IsResistance F r` is dropped, which `ResistanceECA` provides. The order of the five parts is as in its docstring. Every n ≥ 1 (README l. 383). Sanity check for rule 154: one closed class {{0}}, S = {{0}}, γ_min = m − 1 at n = 2 (m = 2), 4 (m = 4), 8 (m = 31), with γ = m for every other cycle. At n = 6, all 12 cycles are selected with γ = 11. This agrees with Theorem 3.9(d), (e) and Theorem 3.10. |
| `TreeWeight_lower_bound` St l. 215–217 | proof of Theorem 2.8, l. 321–322 | same, general | For every parent map p with `IsInTree C p`. Each of the m − 1 edges d → p d, d ≠ C, joins distinct cycles (k = 1 in `IsInTree`), so it weighs ≥ 1 by Lemma 2.3. This closes finding 8 of the earlier report. |
| `KStar_unique_class` St l. 354–357 | sentence l. 325–326 | same | The body is identical to that of `Corollary_2_8` at 3425cc7 (git diff), which the earlier report checked. The new docstring correctly says that the sentence has no number. |

## C. README, "Differences from the paper" (l. 456–476)

1. **`σC` as a cycle** (l. 458–460): correct. See finding 4 for why the hypotheses cannot make the second clause
   vacuous.
2. **Invariance of S and G_1** (l. 461–462): correct description of what is stated. Finding 4.
3. **Parity of a cell** (l. 463–465): correct. `Single_mem` is the only statement that uses `parE`/`parO` without
   assuming n even, and it is true for every n. The odd-n example is in table A.
4. **Ring sizes** (l. 466–468): correct as far as it goes. At n = 2 the cycles are {00} and {11} and
   V({00}, {11}) = 2, and `Lemma_3_3`, `Lemma_3_4_a` and `Theorem_3_9_b` hold there. `Theorem_3_9_b` is false at
   n = 1 (V({0}, {1}) = 1), which the form n = 2^(k+1) excludes. Incomplete for the rotation statements (finding 1);
   the meaning of k is not stated (finding 2).
5. **Proof of Theorem 3.9(b)** (l. 469–472): the argument is valid and does not use part (a). The list of
   dependencies is incomplete (finding 5).
6. **Proof of Lemma 3.3** (l. 473–474): agrees with Pow2.lean l. 62–81 (`step_aux` with a parity c ∈ ZMod 2) and with
   the structure of the paper's proof (l. 404–406). Here x ∈ E is the case c = 1 and x ∈ O the case c = 0.

Differences missing from the list: findings 1 and 2. I found no other difference between the statements and the
paper. The claim "No gap or false statement was found in the paper for these statements" (l. 476) agrees with what I
saw. In the paper's proof of 3.9(b) the appeal to (a) is valid, only more than is needed.

## D. Comparison with the author's check (done last)

`reader_checks/lean_rule154/out.txt` prints, for n = 1..6 and 8, the number of cycles and the six smallest values of
V({0}, C), C ≠ {0}. My values agree at every n: m = 2, 2, 3, 4, 4, 12, 31; for example, at n = 6 the six smallest are
1, 1, 1, 2, 2, 2, and at n = 8 all six are 2. The author's file covers Lemma 3.3 at n = 2, 4, 6, 8, 16 and
Lemma 3.4(a) at n = 2, 4, 8, 16, all True; mine covers all even n ≤ 16 and gives the same results. The author did not
compute n = 7. There my model gives m = 8 and least V({0}, C) = 1. README l. 480–483 reports the author's values
correctly.

## Not checked

* Lean was not run. I did not check that the proofs compile, the axiom lists, or that the theorems in
  `AxiomCheckTheoremA.lean` and `AxiomCheckRule154.lean` have the claimed types (I read the `#check` lines only).
* Proofs: I read `Pow2.lean` and lines 130–205 of `Rotation.lean`; I did not read lines 1–129 of `Rotation.lean`,
  the proof of `section_2_4_ECA` in `Checks.lean`, or the pilot's `iterate_half_eq_zero`, on which `Lemma_3_4_a`
  rests.
* `Lemma_2_4` in full was computed only for ten asymmetric rules at n = 3..6 (commutation and resistance for all 256
  rules at n = 1..6). `Theorem_3_9_b` was computed for n ≤ 8, `Lemma_3_3` and `Lemma_3_4_a` for n ≤ 16.
* The paper's proofs of Lemma 3.4(a) and of Theorem 3.9(b), except the step discussed in finding 5; the other parts
  of Section 3.1.
* The definitions of St again (only that they are unchanged since 3425cc7, by `git diff`). The README outside its
  last section, except item 4 and l. 359–361 of the Section 2 part. The build and cost figures in the README; of
  these I checked only the line counts: 72 + 77 = 149 statement lines, and 72 + 77 + 205 + 196 = 550 lines in
  four files.
* The untracked files `PR_BODY.md` and `PR_BODY_154.md`.

No existing file was changed and no commit was made.

Claude
