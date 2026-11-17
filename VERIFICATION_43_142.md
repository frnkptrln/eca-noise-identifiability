# Verification of `proofs_43_142/PROOF_43_142.md` (rules 43 and 142)

Branch `verify-43-142` (from `crystal-43-142` at 6725208). New files only: this report and `verify_43_142/`.
No existing file was changed.

**Order of work (independence).** (1) Read `PROOF_43_142.md` Sections 0 to 6, `report_ring_size.md` Sections 3
and 4, `note/note_v0.2.tex` Sections 1 and 6, and `literature_addendum.md`. (2) Wrote and ran my own code
(`verify_43_142/`) from the rule tables and the definitions only. (3) Only then opened `proofs_43_142/out/` to
compare (Section 5). The scripts in `proofs_43_142/` (`*.py`), the content of `proofs_43_142/review/` and
Section 7 of the proof document (the copy of `out/tables.md`) were not opened at any point. The literature
check (Section 4) was done by a sub-task that was given the addendum and Sections 0 to 6 of the proof and was
not allowed to open the session's scripts or outputs.

Severity scale for findings: **false statement** / **gap in a proof** / **wording**.

## 0. Summary

* No false statement and no gap in a proof was found in Lemmas 1 to 11, Theorems 1 and 2, Propositions 2
  and 3 and Corollaries 1 to 4. Every step was checked by hand for every n in the stated range, including
  n = 4, 5, 6, 7 and the steps where cells of a window coincide (Section 2, end).
* Every lemma and theorem was tested exhaustively for n = 3..20 with independent code (100 statements,
  0 failures). As a negative control the same tests were run with rules 41 and 138 in place of 43 and 142:
  49 of the 94 statements tested in that run fail.
* From the definitions, without Theorem A, I computed V by a BFS on all 2^n states, gamma as minimum in-trees,
  S, gamma_min, k_c and k* for both rules at every n = 3..14. All agree with Corollaries 1 to 4 and
  Proposition 3. In addition the order of nu_c(eps), read off the exact stationary law (GTH) for n = 4..8,
  equals the k_c of the potentials.
* Theorem A (report, Section 4): Lemma 1, Lemma 2 and the proof of Theorem A are complete; one wording point
  (B4). The definition of k_c used in the proof is the note's (v0.2, Section 6) verbatim.
* Comparison with `proofs_43_142/out/`: 0 differences in 324 compared values; 0 disagreements with the 26
  compared records of `mechanisms.csv` (Section 5).
* Findings B1 to B5 (mathematics) are all wording.
* Literature (Section 4): one false bibliographic statement, B6 (Boccara's paper is 1993, not 1992). One
  overstated attribution, B7: "the key lemmas on the wall word are known facts" is stronger than what was read,
  in particular for rule 43. Three wording points, B8 to B10. "The wall map is known (rule 142), the selection
  result was not found" holds as a provisional statement.

## 1. Verdict per statement

| statement | verdict | hand check (beyond reading every step) | own exhaustive test |
|---|---|---|---|
| Section 1: (R), D1 to D3, isolated/interior via P and Q, G1 = {V = 1} | confirmed | all eight table entries; D3 needs n >= 2 | n = 3..20 (G1 = {V = 1}: n = 3..14) |
| Lemma 1 (wall map) | confirmed with remarks (B3) | both cell formulas and both wall rules re-derived | n = 3..20, all states |
| Lemma 2 | confirmed | | n = 3..20, all words |
| Lemma 3 (a), (b), (c) | confirmed | four bracket combinations for each equivalence; n = 3, where cells i-1 and i+2 coincide (A is then empty); P(rho d) = -P(d) - 1 and the reflected equivalences re-derived | n = 3..20, all words |
| Lemma 4 | confirmed | c in {1..n}, t = floor((c-1)/2), both cases, c = n included; reflection | n = 3..20 (periodicity taken from the functional graph of rules 184 and 226) |
| Lemma 5 | confirmed | | n = 3..20 |
| Lemma 6 | confirmed | | n = 3..20, all (state, cell) |
| Lemma 7 (a), (b), (c) | confirmed | the four formulas re-derived; (c) for r of either parity | n = 3..20; (c) for r = 0..2n-1 |
| Description of the cycles | confirmed with remarks (B1) | | n = 3..20 (families, wall bounds, families meet only in X, periods divide 2n) |
| Lemma 8 | confirmed | n = 4 included | n = 3..20 |
| Theorem 1 (1), (2) and the consequence | confirmed | n = 4: w in {0, 2, 4} | n = 4..20 with 4 \| n: all flips of X; G1 distance to X equals abs(w - n/2)/2 for every cycle; every interior (isolated) flip of every state of every cycle |
| Proposition 2 | confirmed | at n = 4 the window j-2..j+1 is the whole ring and t* = n/2 - 2 = 0, checked | n = 4..20, all 4n flips, both rules |
| Proposition 3 | confirmed with remarks (B5) | lower bound valid for arbitrary paths (Lemma 5 holds for all states, not only periodic ones) | V(C, X) by forward BFS for n = 4, 8, 12 and by a backward computation for n = 4..20 (4 \| n) |
| Corollary 1 | confirmed (given Theorem A); without Theorem A confirmed by computation for n = 4, 8, 12 | | Table V2 |
| Corollary 2 | confirmed (given Theorem A and the k_c formula); without Theorem A confirmed by computation for n = 4, 8, 12 | y = x0 + e_2 and y' = x0 + e_1 and their codes at n = 4 (cell 4 = cell 0, cell n-1 = 3) | Table V2; Table V3 (stationary law, n = 4, 8) |
| Lemma 9 (a) to (d) | confirmed | 2 <= w- < n/2 < w+ <= n - 1 for n = 5, 6, 7 and for each residue class | n = 5..19, 4 not dividing n |
| Lemma 10 (first statement, (a), (b)) | confirmed | boundary cases: w = 2 in (a); n - w >= 1 and 2w - n >= 1 in (b) | slides for n = 3..20; both procedures of the proof executed from every eligible periodic state, n = 3..20 |
| Lemma 11 | confirmed | z0, y_s and sigma^2 C z0 written out for n = 5, 6, 7, 9. The case Z = C Z occurs (rule 43, n odd: F^n z0 = C z0) and is covered by the statement | n = 5..19, 4 not dividing n; reachability of C Z from Z in G1 |
| Theorem 2 | confirmed | Steps 1 to 3; x1 = 00101, 001101, 0011001 for n = 5, 6, 7 | unique closed class = K for n = 3 and n = 5..19, 4 not dividing n |
| Corollary 3 | confirmed (given Theorem A); without Theorem A confirmed by computation for n = 5, 6, 7, 9, 10, 11, 13, 14 | codes of z0 also for w- = 2 | Table V2; all eight codes on K, n = 5..19 |
| Corollary 4 | confirmed (given Theorem A); without Theorem A confirmed by computation for n = 4..14 | | Table V2 |
| Remark: n = 3 | confirmed by computation (unique closed class = K, S = K, k* = 0) | | n = 3 |
| Theorem A (report Section 4: re-rooting, Lemma 1, Lemma 2, proof) | confirmed with remarks (B4) | complete | consistent with all 24 records of Table V2 |
| Definition of k_c (note v0.2, Section 6) as used in Corollary 2 | confirmed | the formula agrees with the note verbatim | Table V3: order of nu_c from the stationary law, n = 4..8 |
| `literature_addendum.md`, statements marked "Read" (items B1, B4, B6, B7, A3, A6, A7) | confirmed with remarks (B6, B8, B10) | literature sub-task; B6 re-checked by me | — |
| `literature_addendum.md`, Part B conclusion ("(a) known, (c) and selection not found") | confirmed with remarks (B7, B9) | as above; provisional | — |

## 2. Findings on the mathematics

**B1** (Section 3, "Description of the cycles", sentence "The two families meet exactly in the states with P and
Q both empty, which are the four states of X for 4 | n and do not exist otherwise (Lemma 8)").
*Wording.* Lemma 8 is stated for 4 | n and, in its last sentence, for even n. For odd n the reason is a different
one: P = Q = empty gives 2w = n by Lemma 3(c), which is impossible for odd n. The statement is true and is
confirmed for n = 3..20 ("families meet exactly in X" in Table V1); only the reference is incomplete. No proof
uses the odd case.

**B2** (Section 6, Remarks, third item: "Lemmas 1 to 7, Lemma 9(d) and the slide lemma do not use divisibility").
*Wording.* Lemma 9(d) is formulated with the levels w- and w+, which Section 1 defines only for n not divisible
by 4. Its argument does not use divisibility, but for 4 | n the corresponding statement is Theorem 1(2). The
sentence is a [remark] and no proof depends on it.

**B3** (Lemma 1, proof, rule 43: "delta(F x)_i = d_i + d_(i-1)(1 + d_i) + d_i(1 + d_(i+1))").
*Wording.* The full sum is d_i + [1 + d_(i-1)(1 + d_i)] + [1 + d_i(1 + d_(i+1))]. The two constants 1 cancel
mod 2 and are dropped without comment. The displayed expression and the conclusion (rule 184) are correct.

**B4** (`report_ring_size.md`, Section 4, proof of Lemma 2: "In a finite digraph a closed class K is reachable
from every node"). *Wording.* As written, the sentence can be read as "every closed class is reachable from
every node". That is false when G1 has more than one closed class; the report itself mentions rule 164 at
n = 16, which has two. The proof needs and uses only "some closed class is reachable from every node" (follow
edges to a sink of the condensation). With that reading Lemma 1, Lemma 2 and the proof of Theorem A are
complete. Checked in detail:

* re-rooting yields an in-tree and does not increase the weight when the added edge has weight 1;
* in Lemma 2 the re-rooted nodes D_1, ..., D_k and the nodes of the path inside K are pairwise distinct and
  differ from E until the last step, so e* survives until E is re-rooted;
* gamma_min = m - 1 uses V >= 1 between distinct cycles (report Section 3).

**B5** (Section 2, Proposition 3: "For every cycle C, V(C, X) = ..."). *Wording, minor.* For C = X the formula
gives 0, which is what the note's V(C, C') = R(C -> C') gives. The report uses V only between distinct cycles
(G1, in-trees), so "for every cycle C != X" would avoid the question.

**Checked, nothing found** (beyond B1 to B5):

* all of Section 1;
* Lemmas 2 to 8, and Lemma 1 except for B3;
* the proofs of Theorem 1 and Propositions 2 and 3;
* Corollaries 1 and 2;
* Lemmas 9 to 11, the proof of Theorem 2, Corollaries 3 and 4, and the first remark of Section 6;
* the table of Section 0 against the statements of Section 2.

**Small cases and coinciding cells**, checked one by one:

* Lemma 3 at n = 3 (i-1 = i+2);
* Lemma 4 for c = n;
* Proposition 2 at n = 4 (the window is the whole ring; t* = 0);
* Corollary 2 at n = 4;
* Lemma 10(a) with w = 2 and Lemma 11 with w- = 2 (n = 5, 6, 7);
* Theorem 2 at n = 5, 6, 7;
* the level bounds of Section 6 at n = 5, 6, 7.

## 3. The two places where the document relies on earlier work

**Theorem A** (`report_ring_size.md`, Section 4). Read: re-rooting, Lemma 1, Lemma 2, Theorem A and its proof.
Verdict: complete, apart from the wording point B4. Not checked: the attribution paragraph and Lemmas B, Z, H
and P, which Corollaries 1 and 3 do not use. Independently of Theorem A, Table V2 shows S = (the unique closed
class of G1) and gamma_min = m - 1 in all 24 records (n = 3..14, both rules).

**Definition of k_c** (note v0.2, Section 6, Theorem `thm:order`).

* The note states k_c = min_C [gamma(C) + R(C -> D_c)] - min gamma, with D_c the set of states containing code c,
  and k* = max_c k_c; the theorem asserts nu_c ~ a_c eps^(k_c).
* Corollary 2 of the proof uses exactly this formula and two facts from the note: R(C -> x) = 0 iff x is in C
  (proved in the note), and gamma - min gamma and R are non-negative integers.
* I read the note's proof of the order formula: the tree theorem, censoring onto the cycle states plus x,
  contraction of the cycles, and the redirection argument for a transient x. I found no gap at the level of
  detail given, but I did not re-derive it in full.
* As a numerical check of this instance, Table V3 reads the order of nu_c(eps) off the exact stationary law for
  n = 4..8. It equals the k_c of the formula in all 10 records.

## 4. Literature addendum

Sources are named by the addendum's item labels (item B1, item A3, ...); findings by bold numbers
(**B6** ...). The check was done by a sub-task (report saved verbatim as `verify_43_142/literature/lit_check_43_142.md`).
I re-checked one point myself (finding B6, by web search: the ScienceDirect page of Boccara's paper). I checked the
sub-task's two prior-work points (its L6, L7) against the repository's earlier literature files. Everything else in
this section rests on the sub-task's reading. "Supported" means the sub-task saw the named page itself.

**Statements marked "Read" in the addendum.**

* item B1 (Fukś, Rule 142, publisher PDF, read in full): supported.
  * rule 60 maps rule 142 to rule 226: abstract, p. 123, and eq. (34), p. 132;
  * the credit to Boccara: p. 132, ref. [2];
  * rule 43 does not appear: full text plus a keyword scan;
  * blocks 10 are conserved for periodic configurations of every length: Section 3, pp. 125-127;
  * no ring characterisation, no case 4 | n, no noise statement: full text;
  * jamming-type behaviour at density 1/4 of blocks 10: pp. 136-137.

  Exceptions: findings B6 and B8.
* item B4 (Fukś 1997, arXiv v1, all 5 pp.): supported, including the floor((L-2)/2) statement on arXiv p. 3. The
  remark that the proof there is a sketch is also correct.
* item B6 (Belitsky and Ferrari, arXiv pp. 1-6) and item B7 (Boccara and Fukś, arXiv pp. 1-4): supported.
* item A3 (Nordahl, pp. 70, 73, 74 and the references), item A6 (Stricker, pp. 230, 232) and item A7 (Voorhees
  and Beauchemin, pp. 44, 52, 68-70): supported, with the small wording point B10. A full-text scan of item A7 finds no rule 154, 43
  or 142, which agrees with the addendum's "does not cover".

**Excerpt and abstract statements.** These could not be lifted to "read" (arXiv, IOP, World Scientific and
Elsevier are not reachable or paywalled):

* items B2, B3, B5;
* items A1 (Zhu and Richard), A2 (Nobe and Yura), A4 (Krawczyk), A5 (Chua et al.).

The item A5 titles and the abstract quote were confirmed through the DOI records. For item A1 the sub-task's excerpts
show that eq. (4) divides by the total number 2^n of eigenvalues. That fits the addendum's
algebraic-multiplicity reading, but it is still an excerpt.

**Findings.**

**B6** (addendum, Part B, rows of items B1 and B3: "credited there to Boccara (1992)", "Physica D 68 (1992) 416-426").
*False statement (bibliographic).* Physica D 68, issue 3-4, pp. 416-426 is dated 15 October 1993 (ScienceDirect,
DOI 10.1016/0167-2789(93)90134-M; checked by me). The year 1992 is the one printed in Fukś's reference list, from
which the addendum took it. Correct: Boccara, Physica D 68 (1993) 416-426.

**B7** (`PROOF_43_142.md`, Section 0, line 30: "the key lemmas on the wall word are known facts about rules 142,
43, 226 and 184, see `literature_addendum.md`, Part B"; and the addendum's bullet "(a) is known for both rules").
*Wording: overstated attribution.* By the addendum's own reading rule, what was read is:

* for rule 142, the wall map (Lemma 1) and the conservation law (Lemma 5): read in item B1, and confirmed by
  the sub-task;
* for rule 184, the time bound on rings: item B4.

What was not read:

* for rule 43, the wall map and the conservation law: seen only in a search excerpt of item B2, which neither reader
  could open;
* the "iff" of Lemma 4: "not seen written out" (the addendum's own words);
* Lemma 3, the translation of the pair sets: not attributed to any source.

So "known facts" is stronger than the evidence for Lemma 1 for rule 43 and for Lemmas 3 and 4. The addendum's
bullet qualifies itself in the next sentence; line 30 of the proof does not. A similar sentence stands at line
752 (Section 8, which I did not read; found by a text search). Suggested wording: "Lemma 1 and the conservation
law are known for rule 142 (Fukś 2005, crediting Boccara 1993) and reported for rule 43 (Fukś 2007, seen only as
a search excerpt). Lemmas 3 and 4 in this form, and Lemmas 7 and 8, were not found."

**B8** (addendum, row of item B1: "eq. 34, p. 132; Proposition 6, p. 133"). *Wording.* According to the sub-task,
Proposition 6 is a statement about preimage counts. The identity appears on p. 133 only as eq. (40), inside the
proof of Proposition 6; its statement is eq. (34) on p. 132.

**B9** (addendum, row of item B1 and "What follows", bullet (c): item B1 described as treating density 1/4 "as a
jamming-type transition"). *Understated.* Item B1 also gives a local motion law: a block 10 moves by one site or stays,
depending on the preceding site. The abstract, which I saw in a search result, says this too. According to the
sub-task, item B1 also gives the expected velocity of blocks 10 as a function of density (eq. 59, p. 137). These are
infinite-lattice counterparts of the two families of cycles in Lemma 7. They do not contain the ring
characterisation, so "(c) was not found" stands.

**B10** (addendum, items A7 and A2). *Wording, minor.*

* Item A7: "characteristic equations ... at ring sizes up to 13". According to the sub-task only rule 60 reaches 13;
  the others stop earlier.
* Item A2: "reduced to a linear system over Z_2". The deposited abstract speaks of a finite commutative ring and
  does not confirm "over Z_2".

**Not findings.**

* The sub-task's L5 (item B4 at density 1/2): already in the addendum's row for item B4 ("neither at density 1/2").
* The sub-task's L6 (Wuensche's DDLab jump graph, which tracks where every single flip of an attractor state ends) and L7
  (Marsan and Sablik 2025, strong stochastic stability): both are already cited in `literature.md` and
  `literature_ring_size.md`. They are missing only as cross-references in Part B's "Noise selection" bullet.
  The sub-task also names Hellouin de Menibus and Sablik, J. Stat. Phys. 167 (2017), on the mu-limit set of rule
  184, and Bramson and Neuhauser (1994). Neither is in the repository; both were seen as excerpts only and, as
  far as the excerpts show, neither is on finite rings.

**Part B: how the result may be described.**

* "The wall map is known" is accurate for rule 142: two readers saw it in Fukś (2005), which credits Boccara
  (1993). For rule 43 it is reported, not read.
* "The selection result was not found" is accurate as a provisional negative. Neither the session's 15 queries
  nor the sub-task's 9 new queries found a source that states:
  * the run-length description of the periodic states of rules 43 or 142 on a ring (Lemma 7);
  * the uniqueness of the cycle with n/2 walls, or anything specific to 4 | n (Lemma 8);
  * which cycles small bit-flip noise selects.
* Several likely places are unread: Boccara (1993); Fukś (2007); Hattori and Takesue (1991); NKS p. 1023;
  Fukś's 2023 book, chapter 6. The result may therefore be described as "not found in the sources reached",
  not as new. That is how the proof document itself puts it ("no claim of novelty is made"), apart from the
  attribution point B7.

**Not reached** (by the sub-task or by me):

* Item B2 (Fukś 2007): the arXiv and IOS Press copies are not reachable. The author's page was approved, but it sits
  behind a browser challenge that was not bypassed.
* Items B3 and B5, Hattori and Takesue, and Fukś's 2023 book: closed access.
* NKS online and the Wolfram Atlas: refused.
* The full texts of items A1, A2, A4 and A5.
* The journal versions of items B4, B6 and B7: not compared with the arXiv versions.
* The search excerpts of item A1 seen by the session: they are not stored, so they cannot be re-checked.


## 5. Comparison with `proofs_43_142/out/` (done last)

* `g1_classes.jsonl`: for both rules and n = 3..20 I compared the number of cycles, periodic states, G1 edges,
  strong components and closed classes, the closed class sizes and members, and the codes and wall counts on
  the closed classes: 324 values, **0 differences**. The session goes to n = 24; n = 21..24 was not compared.
* `check_lemmas.json`: the session reports 0 violations in every test. Where both sides count the same objects
  the case counts agree:
  * Lemma 6: 39845880 (state, cell) pairs for n = 3..20;
  * slides of Lemma 10: 497440 per rule;
  * entry costs: 1889 and 1897 cycles for n = 4..20 with 4 | n, which are the sums of my cycle counts
    (3 + 13 + 61 + 283 + 1529 and 5 + 15 + 61 + 285 + 1531).

  For Lemma 7(c) the session counts 1376544 (periodic state, r) pairs. That is the sum over n of p_n (n - 1),
  with p_n my count of periodic states: the session tests r = 1..n-1 and I test r = 0..2n-1, which is
  equivalent because sigma^n = id. This is not a disagreement. The session also tests Theorem 1(1),
  Proposition 2 and Lemma 11 on samples up to n = 400 and 401. I did not repeat those; my tests stop at n = 20.
* `data/ring_size/mechanisms.csv` (study solver; cited after Corollary 2 and in Table 5 of the proof) has 30
  records for rules 43 and 142, n = 8..22. Compared fields: n_selected, gamma_min, k_c, k*, cycles.
  * 14 records (n = 8..14): against my potentials.
  * 12 records (n = 15..20): against my G1 closed class and m - 1. This comparison uses Theorem A.
  * 4 records (n = 21, 22): not compared.

  **0 disagreements.**
* The session's other files (`tables.md`, `crosscheck_data.json`, `constructive_paths.json`) were looked at only
  for their structure. Their numbers were not checked beyond the points above.

## 6. What was not checked

* Sections 7 to 9 of `PROOF_43_142.md` (computations, scope, files); the scripts in `proofs_43_142/`; the file
  `review/second_read.json`.
* Potentials and k_c from the definitions were computed only for n <= 14: gamma by networkx for n = 12..14, and
  by my own Edmonds routine, cross-checked with networkx, for n <= 11. For n = 15..20 only through G1 plus
  Theorem A; for n > 20 not at all.
* The exhaustive tests stop at n = 20; the theorems for larger n rest on the proofs, which were checked by hand.
* The note's proof of the order formula was read, not re-derived (Section 3). The attribution paragraph of the
  report's Section 4 was not checked.
* `report_ring_size.md` Section 5.1, the domain picture referred to in the remark after Proposition 2, was not
  read.
* Literature: see Section 4 for what could not be reached.

## 7. Files (`verify_43_142/`)

| file | content |
|---|---|
| `eca.py` | own core: global map (tested against a cell-by-cell map), functional graph, cycles, attractors, G1 from single flips, BFS for R(C -> x) over all states, own Chu-Liu/Edmonds (tested against networkx and brute force), SCCs |
| `test_lemmas.py` | exhaustive tests of all statements, n = 3..20 -> `out/lemma_tests.json`, `out/lemma_tests.log` |
| `potentials.py` | V, gamma, S, k_c, k*, r(X), G1 = {V = 1}, n = 3..14 -> `out/potentials.jsonl`, `out/potentials.log` |
| `stationary.py` | stationary law by GTH, order of nu_c, n = 4..8 -> `out/stationary.json` |
| `entry_cost.py` | Proposition 3 by a backward computation, 4 \| n, n <= 20 -> `out/entry_cost.json` |
| `compare.py` | comparison with `proofs_43_142/out/` and `mechanisms.csv` -> `out/compare.json` |
| `make_tables.py` | builds `out/tables.md` (copied in Section 8) |
| `literature/lit_check_43_142.md` | report of the literature sub-task |

Cost, one process at a time:

* `test_lemmas.py 20`: 22 s;
* `potentials.py 3 14`: about 19 min, almost all of it at n = 14 (networkx arborescences, about 130 roots);
* every other script: under 1 min.

Reproduce: `cd verify_43_142; python test_lemmas.py 20; python potentials.py 3 14; python stationary.py 8;
python entry_cost.py 20; python compare.py; python make_tables.py`. `potentials.py` appends to its output, so
move `out/potentials.jsonl` away before a rerun.

## 8. Tables (verbatim copy of `verify_43_142/out/tables.md`)

### V1. Exhaustive tests of the statements (`test_lemmas.py` -> `out/lemma_tests.json`)

n = 3..20; 100 statements; total failures: 0; wall time 22 s, one process.

| statement | n tested | cases | failures |
|---|---|---|---|
| (R) form of the tables | tables | 16 | 0 |
| rules agree exactly on codes 1,3,4,6 | tables | 1 | 0 |
| 142 ones on 001,010,011,111; 43 on 000,001,011,101 | tables | 1 | 0 |
| descriptions of rules 184, 226; g226(a,b,c)=g184(c,b,a) | tables | 8 | 0 |
| D1 | 3..20 | 2097144 | 0 |
| D2 (w even) | 3..20 | 2097144 | 0 |
| D3 | 3..20 | 39845880 | 0 |
| isolated/interior via P/Q | 3..20 | 39845880 | 0 |
| Lemma 6 | 3..20 | 39845880 | 0 |
| runs: isolated = run 1, interior iff run >= 3 | 3..12 | 8184 | 0 |
| Lemma 1 (43) cell formula | 3..20 | 2097144 | 0 |
| Lemma 1 (43) delta(Fx)=G184(delta x) | 3..20 | 2097144 | 0 |
| Lemma 5 FC=CF (43) | 3..20 | 2097144 | 0 |
| Lemma 5 w(Fx)=w(x) (43) | 3..20 | 2097144 | 0 |
| Lemma 1 (142) cell formula | 3..20 | 2097144 | 0 |
| Lemma 1 (142) delta(Fx)=G226(delta x) | 3..20 | 2097144 | 0 |
| Lemma 5 FC=CF (142) | 3..20 | 2097144 | 0 |
| Lemma 5 w(Fx)=w(x) (142) | 3..20 | 2097144 | 0 |
| Lemma 2 |G184 d|=|d| | 3..20 | 2097144 | 0 |
| Lemma 2 |G226 d|=|d| | 3..20 | 2097144 | 0 |
| Lemma 3(a) P equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(a) Q equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(a) counts | 3..20 | 2097144 | 0 |
| Lemma 3(a) translation when A empty | 3..20 | 430268 | 0 |
| Lemma 3(b) P equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(b) Q equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(b) counts | 3..20 | 2097144 | 0 |
| Lemma 3(b) translation when A empty | 3..20 | 430268 | 0 |
| Lemma 3(c) | 3..20 | 2097144 | 0 |
| Lemma 4 periodic iff P or Q empty (184) | 3..20 | 2097144 | 0 |
| Lemma 4 action, P empty (184) | 3..20 | 39596 | 0 |
| Lemma 4 action, Q empty (184) | 3..20 | 39596 | 0 |
| Lemma 4 periodic iff P or Q empty (226) | 3..20 | 2097144 | 0 |
| Lemma 4 action, P empty (226) | 3..20 | 39596 | 0 |
| Lemma 4 action, Q empty (226) | 3..20 | 39596 | 0 |
| Lemma 7(a) (43) | 3..20 | 2097144 | 0 |
| Lemma 7(b) no isolated (43) | 3..20 | 39596 | 0 |
| Lemma 7(b) no interior (43) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no isolated' preserved by F, sigma, C (43) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no interior' preserved by F, sigma, C (43) | 3..20 | 39596 | 0 |
| Lemma 7(c) (43) | 3..20 | 2911432 | 0 |
| periods divide 2n (43) | 3..20 | 4025 | 0 |
| family 'no isolated' has w <= n/2 (43) | 3..20 | 39596 | 0 |
| family 'no interior' has w >= n/2 (43) | 3..20 | 39596 | 0 |
| families meet exactly in X (43) | 3..20 | 18 | 0 |
| wall count constant on cycles (43) | 3..20 | 4025 | 0 |
| Theorem 2 unique closed class = K (43) | 3,5,6,7,9,10,11,13,14,15,17,18,19 | 13 | 0 |
| Lemma 10 slides join cycles both ways (43) | 3..20 | 497440 | 0 |
| Lemma 10(a) procedure (43) | 3..20 | 39560 | 0 |
| Lemma 10(b) procedure (43) | 3..20 | 39558 | 0 |
| Lemma 7(a) (142) | 3..20 | 2097144 | 0 |
| Lemma 7(b) no isolated (142) | 3..20 | 39596 | 0 |
| Lemma 7(b) no interior (142) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no isolated' preserved by F, sigma, C (142) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no interior' preserved by F, sigma, C (142) | 3..20 | 39596 | 0 |
| Lemma 7(c) (142) | 3..20 | 2911432 | 0 |
| periods divide 2n (142) | 3..20 | 4043 | 0 |
| family 'no isolated' has w <= n/2 (142) | 3..20 | 39596 | 0 |
| family 'no interior' has w >= n/2 (142) | 3..20 | 39596 | 0 |
| families meet exactly in X (142) | 3..20 | 18 | 0 |
| wall count constant on cycles (142) | 3..20 | 4043 | 0 |
| Theorem 2 unique closed class = K (142) | 3,5,6,7,9,10,11,13,14,15,17,18,19 | 13 | 0 |
| Lemma 10 slides join cycles both ways (142) | 3..20 | 497440 | 0 |
| Lemma 10(a) procedure (142) | 3..20 | 39560 | 0 |
| Lemma 10(b) procedure (142) | 3..20 | 39558 | 0 |
| Lemma 8 neither 11 nor 00 in wall word => X and 4|n (43) | 4,6,8,10,12,14,16,18,20 | 9 | 0 |
| Lemma 8 periodic with w=n/2 are X (43) | 4,8,12,16,20 | 5 | 0 |
| Lemma 8 X one cycle of length 4, F = sigma^-1 (43) | 4,8,12,16,20 | 5 | 0 |
| codes on X are exactly 1,3,4,6 (43) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(1) flips of X return to X (43) | 4,8,12,16,20 | 240 | 0 |
| Theorem 1 only closed class is {X} (43) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(2) G1-distance to X = |w-n/2|/2 (43) | 4,8,12,16,20 | 1889 | 0 |
| Theorem 1(2) interior/isolated cell exists on every state (43) | 4,8,12,16,20 | 35376 | 0 |
| Theorem 1(2) proof step, every interior/isolated flip (43) | 4,8,12,16,20 | 306016 | 0 |
| Proposition 2 healing time (43) | 4,8,12,16,20 | 240 | 0 |
| Lemma 8 neither 11 nor 00 in wall word => X and 4|n (142) | 4,6,8,10,12,14,16,18,20 | 9 | 0 |
| Lemma 8 periodic with w=n/2 are X (142) | 4,8,12,16,20 | 5 | 0 |
| Lemma 8 X one cycle of length 4, F = sigma^-1 (142) | 4,8,12,16,20 | 5 | 0 |
| codes on X are exactly 1,3,4,6 (142) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(1) flips of X return to X (142) | 4,8,12,16,20 | 240 | 0 |
| Theorem 1 only closed class is {X} (142) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(2) G1-distance to X = |w-n/2|/2 (142) | 4,8,12,16,20 | 1897 | 0 |
| Theorem 1(2) interior/isolated cell exists on every state (142) | 4,8,12,16,20 | 35376 | 0 |
| Theorem 1(2) proof step, every interior/isolated flip (142) | 4,8,12,16,20 | 306016 | 0 |
| Proposition 2 healing time (142) | 4,8,12,16,20 | 240 | 0 |
| w- >= 2, w+ <= n-1, eps in {1,2,3} | 5,6,7,9,10,11,13,14,15,17,18,19 | 24 | 0 |
| Lemma 9(a) lower: interior, no isolated (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1404 | 0 |
| Lemma 9(a) upper: isolated, no interior (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1092 | 0 |
| Lemma 9(b) no edge leaves K (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 26261 | 0 |
| Lemma 9(c) edges between the levels (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 144 | 0 |
| Lemma 9(d) every cycle reaches K (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 2133 | 0 |
| Lemma 11 (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |
| Corollary 3 all eight codes on K (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |
| Lemma 9(a) lower: interior, no isolated (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1404 | 0 |
| Lemma 9(a) upper: isolated, no interior (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1092 | 0 |
| Lemma 9(b) no edge leaves K (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 25914 | 0 |
| Lemma 9(c) edges between the levels (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 152 | 0 |
| Lemma 9(d) every cycle reaches K (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 2143 | 0 |
| Lemma 11 (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |
| Corollary 3 all eight codes on K (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |

### V2. Potentials, selected set and k_c from the definitions, without Theorem A (`potentials.py` -> `out/potentials.jsonl`)

| rule | n | cycles m | gamma_min | m - 1 | selected cycles | wall counts of S | k_0..k_7 | k* | closed classes of G1 (sizes) | all document checks | gamma method |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 43 | 3 | 3 | 2 | 2 | 3 | [0, 2] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 142 | 3 | 3 | 2 | 2 | 3 | [0, 2] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 43 | 4 | 3 | 2 | 2 | 1 | [2] | 10100101 | 1 | [1] | True | own Edmonds = networkx = brute force |
| 142 | 4 | 5 | 4 | 4 | 1 | [2] | 10100101 | 1 | [1] | True | own Edmonds = networkx = brute force |
| 43 | 5 | 4 | 3 | 3 | 3 | [2, 4] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 142 | 5 | 5 | 4 | 4 | 3 | [2, 4] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 43 | 6 | 10 | 9 | 9 | 8 | [2, 4] | 00000000 | 0 | [8] | True | own Edmonds = networkx |
| 142 | 6 | 10 | 9 | 9 | 6 | [2, 4] | 00000000 | 0 | [6] | True | own Edmonds = networkx |
| 43 | 7 | 7 | 6 | 6 | 4 | [2, 4] | 00000000 | 0 | [4] | True | own Edmonds = networkx = brute force |
| 142 | 7 | 8 | 7 | 7 | 5 | [2, 4] | 00000000 | 0 | [5] | True | own Edmonds = networkx |
| 43 | 8 | 13 | 12 | 12 | 1 | [4] | 10100101 | 1 | [1] | True | own Edmonds = networkx |
| 142 | 8 | 15 | 14 | 14 | 1 | [4] | 10100101 | 1 | [1] | True | own Edmonds = networkx |
| 43 | 9 | 15 | 14 | 14 | 9 | [4, 6] | 00000000 | 0 | [9] | True | own Edmonds = networkx |
| 142 | 9 | 15 | 14 | 14 | 6 | [4, 6] | 00000000 | 0 | [6] | True | own Edmonds = networkx |
| 43 | 10 | 28 | 27 | 27 | 10 | [4, 6] | 00000000 | 0 | [10] | True | own Edmonds = networkx |
| 142 | 10 | 30 | 29 | 29 | 12 | [4, 6] | 00000000 | 0 | [12] | True | own Edmonds = networkx |
| 43 | 11 | 28 | 27 | 27 | 7 | [4, 6] | 00000000 | 0 | [7] | True | own Edmonds = networkx |
| 142 | 11 | 29 | 28 | 28 | 11 | [4, 6] | 00000000 | 0 | [11] | True | own Edmonds = networkx |
| 43 | 12 | 61 | 60 | 60 | 1 | [6] | 10100101 | 1 | [1] | True | networkx |
| 142 | 12 | 61 | 60 | 60 | 1 | [6] | 10100101 | 1 | [1] | True | networkx |
| 43 | 13 | 61 | 60 | 60 | 15 | [6, 8] | 00000000 | 0 | [15] | True | networkx |
| 142 | 13 | 62 | 61 | 61 | 9 | [6, 8] | 00000000 | 0 | [9] | True | networkx |
| 43 | 14 | 126 | 125 | 125 | 16 | [6, 8] | 00000000 | 0 | [16] | True | networkx |
| 142 | 14 | 128 | 127 | 127 | 14 | [6, 8] | 00000000 | 0 | [14] | True | networkx |

Checks per record (all True in every record): Cor 1: S = {X}; Cor 2: k = (1,0,1,0,0,1,0,1), k* = 1; Cor 3: S = K; Cor 3: k = 0 for all c, k* = 0; G1 (flips) = {V = 1}; Prop 3: V(C,X) = |w-n/2|/2; Prop 3: max V(C,X) = n/4 exactly at w in {0,n}; S = union of closed classes (single class); Thm 1: r(X) >= 2; gamma_min = m - 1.

### V3. Order of nu_c(eps) read off the stationary law (GTH, eps = 1e-4 and 1e-5; `stationary.py` -> `out/stationary.json`)

| rule | n | k_c from pi | k_c from potentials | agree | max rounding error | stationary mass on S at eps = 1e-5 |
|---|---|---|---|---|---|---|
| 43 | 4 | 10100101 | 10100101 | True | 0.0001 | 0.999950 |
| 142 | 4 | 10100101 | 10100101 | True | 0.0001 | 0.999950 |
| 43 | 5 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 142 | 5 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 43 | 6 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 142 | 6 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 43 | 7 | 00000000 | 00000000 | True | 0.0004 | 0.999944 |
| 142 | 7 | 00000000 | 00000000 | True | 0.0004 | 0.999944 |
| 43 | 8 | 10100101 | 10100101 | True | 0.0004 | 0.999780 |
| 142 | 8 | 10100101 | 10100101 | True | 0.0004 | 0.999780 |

### V4. Proposition 3 by a backward computation over all states (`entry_cost.py` -> `out/entry_cost.json`)

| rule | n | cycles | max V(C, X) | n/4 | cycles with V(C, X) != abs(w - n/2)/2 |
|---|---|---|---|---|---|
| 43 | 4 | 3 | 1 | 1 | 0 |
| 142 | 4 | 5 | 1 | 1 | 0 |
| 43 | 8 | 13 | 2 | 2 | 0 |
| 142 | 8 | 15 | 2 | 2 | 0 |
| 43 | 12 | 61 | 3 | 3 | 0 |
| 142 | 12 | 61 | 3 | 3 | 0 |
| 43 | 16 | 283 | 4 | 4 | 0 |
| 142 | 16 | 285 | 4 | 4 | 0 |
| 43 | 20 | 1529 | 5 | 5 | 0 |
| 142 | 20 | 1531 | 5 | 5 | 0 |

### V5. Comparison with `proofs_43_142/out/` and `data/ring_size/mechanisms.csv` (`compare.py` -> `out/compare.json`)

G1 fields of `g1_classes.jsonl` compared for both rules, n = 3..20 (cycles, periodic states, G1 edges, strong components, closed classes, their sizes, members, codes, wall counts): 324 values, 0 differences.

`mechanisms.csv`, rules 43 and 142, n = 8..22: 30 records; compared against 14 records by potentials (definitions), 12 records by G1 closed class + Theorem A (m - 1), 4 records by not computed here (n > 20); disagreements: 0.

Entry costs: the session's test E covers rule 43 n = 4..20 (1889 cycles), rule 142 n = 4..20 (1897 cycles); this verification: rule 43 n = 4: 3 cycles, 0 failures, rule 142 n = 4: 5 cycles, 0 failures, rule 43 n = 8: 13 cycles, 0 failures, rule 142 n = 8: 15 cycles, 0 failures, rule 43 n = 12: 61 cycles, 0 failures, rule 142 n = 12: 61 cycles, 0 failures, rule 43 n = 16: 283 cycles, 0 failures, rule 142 n = 16: 285 cycles, 0 failures, rule 43 n = 20: 1529 cycles, 0 failures, rule 142 n = 20: 1531 cycles, 0 failures.

