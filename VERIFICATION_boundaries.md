# Verification of `report_boundaries.md` (open boundaries)

> **Handling of the findings (25 November 2026).** Written by Claude, the reader outside the sessions, who planned
> the study, applied its patches and then worked these findings into `report_boundaries.md` and
> `literature_boundaries.md`. The report below is unchanged. Its line numbers refer to the report as it stood at
> 57a7208.
>
> * Applied as proposed, or with the proposed content in other words: findings 1 to 4, 6 to 9, 11 to 13, 15, 17 to
>   25.
> * Findings 5 and 26 (the expectations (a) to (c)). Decided by the reader from the planning conversation of
>   24 November 2026, which the reader read again on 25 November: Claude wrote the expectations there, and the
>   checks of their deterministic facts were run there before the task was written (nilpotency of rule 90 and
>   bijectivity of rules 60 and 150 under null walls, the mirror embedding for n = 5, 6, 7, the fixed points of
>   rule 94 for n = 4..14). That conversation is not in the repository, so this rests on the reader's statement. In
>   Section 7 the rows are now marked "chat", (a) for rule 94 is scored "partly correct", the row "(a) facts" is not
>   scored, and the tally reads 3 correct, 1 partly correct. `PREDICTIONS_boundaries.md` is sealed and still says
>   "Frank's expectations".
> * Finding 10: the words that the proposal quotes from Miękisz are given without quotation marks, because the
>   reader did not open the source.
> * Finding 14: the small-n cases are stated separately, with the numbers of the reader's records
>   (`reader_checks/walls/out/null_n04_20.csv`), which agree with those of the finding. For rule 91 the missed code
>   000 at n = 4 is added (finding 25 names n = 5).
> * Finding 16: one paragraph "Names of earlier results" after the tags, instead of a change at each place.
> * Finding 27: the defect is described in Section 4. The data file is unchanged, so it still equals the output of
>   `code/fw/compare_boundaries.py`.
> * Finding 28: a dated note at the top of the report. The status block, open point 9 and Section 9 are unchanged.
> * Not committed: `verify_boundaries/out/wang_table1_crop.png`, a crop of a page of the source, whose licence was
>   not checked. Finding 1 does not rest on it; `verify_boundaries/lit_check.py` and the brute-force check
>   reproduce it.
> * This pass was not verified.

Verified on 25 November 2026, branch `open-boundaries` at 57a7208 (six study commits on b3a73ce plus the reader's
commit). I read the report, the proofs it relies on and the literature it cites as a referee who expects errors. I
recomputed the results with my own code in `verify_boundaries/`, which imports nothing from `code/fw` or
`reader_checks`. No existing file was changed. Line numbers refer to `report_boundaries.md` unless another file is
named.

Committing failed in this environment. A commit made in a workspace copy could not be pulled into the folder,
because the repository has worktrees. This file and `verify_boundaries/` are therefore in the working tree,
uncommitted. Nothing was pushed.

## Verdict

Every proof I was asked to check is correct. Three of them leave a step unwritten: k* = 1 at n = 5 in Theorem 150,
and the two consequences that Section 6 draws from Lemma M′ for rules 90 and 150. The first is closed below for
rule 150 only; for rule 105 the value stays computed. The other two are closed below in one line each. None of the
cited general results uses rotation.

Every number, table entry and count of Sections 4 to 7 that I recomputed agrees with the data file the report names
and with my own solver:

- all 2128 null-wall records;
- all 792 reflecting-wall records;
- all 740 cells of the table in 5.0;
- the table and the counts of Section 6;
- the global counts of Section 4.

The sha256 of the sealed predictions also matches.

The errors are in the prose around the results:

- the "conflict" with Wang et al. comes from misreading their table (rule 195 is in its periodic block);
- the three "undecided" sizes for rule 22 are all decided;
- the plain-words summary contains one false sentence and several overstated ones;
- expectation (a) for rule 94 is scored more generously than the sealed scoring rule and the report's own scoring of
  the same outcome allow.

## Findings, by severity

Classes: **false**, **overstated**, **unclear**, **cosmetic**, **record**. "Own" means computed in
`verify_boundaries/` (output files in `verify_boundaries/out/`, sections of `checks_summary.txt` cited as §k).

### False

1. **False. Section 1, l. 60–64; Section 8 item 8, l. 634; also `literature_boundaries.md` l. 148–153.** The text
   says Wang et al., Table 1, lists rule 195 as never reversible under null walls. It does not. The extracted text
   layer of the arXiv copy (2402.05404v2, p. 10) loses the table's layout. In the typeset page a horizontal rule
   (y = 202.0 in the PDF drawing list) closes the block labelled "2, 3, 'n'" after five rows:
   10101010, 10101001, 10100110, 10100101, 10010110 (rules 170, 169, 166, 165, 150). The rows 11100001, 11010010
   and 11000011 (rules 225, 210, 195) open the block "2, 3, 'p'", together with 10101001, 10100110 and 10010110
   (crop saved as `verify_boundaries/out/wang_table1_crop.png`). I brute-forced all eleven sequences for
   n = 1..12 with the paper's convention (string f(111)…f(000), Eq. (1), p. 3; symmetric neighbourhood). Each null
   row equals my null sequence and each periodic row equals my periodic sequence. Rule 195 under null walls is
   bijective at every n = 1..12 (my sequence 111111111111); on the ring it is never bijective (000000000000), as the
   table says. There is no conflict (§14).
   *Proposed wording (l. 60–64):* "Wang et al., Table 1 (p. 10 of arXiv v2), gives reversibility sequences for
   n = 1..12. Its null-boundary entries (rules 170, 169, 166, 165, 150) and its periodic entries (225, 210, 195,
   169, 166, 150) agree with brute force; rule 195 appears only in the periodic block." Delete open point 8 and the
   [our remark] in `literature_boundaries.md` l. 153.

2. **False. Section 5.3, l. 451; Section 8 item 3, l. 623.** The report says that for rule 22 the sizes
   n = 55, 56, 57 are "undecided at 2·10^4 steps". At the same budget the seed e₁ (n = 55) ends on a cycle of
   period 112, and e₀ (n = 57) on a cycle of period 120. Neither cycle contains 0. At n = 56 the seed e₀ ends on a
   cycle of period 65532 not containing 0 (found with a budget of 4·10^5 steps). So the set of n in 4..62 at which
   all single flips of 0 die is exactly {6, 14, 30, 62}, with no undecided size (§11). This confirms the reader's
   finding 3 and extends it to n = 56.
   *Proposed wording:* "all n single flips die exactly at n = 6, 14, 30, 62 among n = 4..62 (n = 56 needs more
   than 2·10^4 steps: a seed reaches a cycle of period 65532)".

3. **False. Plain-words summary, l. 652–653.** The sentence "under walls their long-run patterns never show some
   neighbourhoods at all, whatever the noise, so part of their rule table stays unobserved at every size" is false
   as written. For ε > 0 every state has positive stationary probability, so every neighbourhood is observed at a
   positive rate. What holds is weaker: no cycle contains those neighbourhoods, so their frequency is O(ε) and the
   rate tends to 0 as ε → 0 (note v0.2, Lemma 3). Also, "at every size" is computed only for n = 4..16 (§10).
   *Proposed wording:* "under walls none of their cycles contains some neighbourhoods, so as the noise vanishes
   those entries of the rule table are seen ever more rarely; this holds at every size computed (4 to 16 cells)".

4. **False. Section 5.5, l. 491 (class 137).** The report says that at even n "all cycles carry all codes". At
   n = 8 one of the three cycles carries only the codes 0, 1, 2, 3, 4, 6. At n = 14 one of the seven cycles carries
   only those six codes (§10). The selected cycles jointly carry all codes (k* = 0 at even n).
   *Proposed wording:* "At even n the selected cycles jointly carry all codes."

### Overstated

5. **Overstated. Section 7, l. 581 and l. 613.** Expectation (a) for rule 94 fails at n = 4 and 7 (k* = 1 there,
   missed 000; own: §10) and is scored "correct for n >= 8". By the sealed scoring rule
   (`PREDICTIONS_boundaries.md`, "What would count as confirming or refuting": scored on n = 4..14; "partly correct
   (right pattern with exceptions …)") this is "partly correct". The report scores its own rule-94 item "partly"
   for the same outcome (l. 598). "Frank's: 5 items, all correct" should therefore read "4 correct, 1 partly
   correct". On who wrote these expectations, see finding 26.

6. **Overstated. Short form l. 276; Section 7 l. 588.** The text tags "165: k* = 1 iff n + 1 = 2^k, else 0" as
   [proved] and says "(k* = 1), proved". Theorem 90 proves k* ≥ 1 iff n + 1 = 2^k (l. 344). The value 1 is
   computed at n = 7 and 15 only (l. 345). My own exact values agree (k* = 1 at n = 7, 15). The one-flip
   neighbours of the fixed point carry the codes 0..6 but not 7 at n = 7, 15, 31, 63, 127. So the value does not
   follow from Lemma 2.2 of the paper (`lem:kzero`: a code one flip away from a state of a selected cycle has
   k_v ≤ 1) and is not proved.
   *Proposed wording:* "165: k* ≥ 1 iff n + 1 = 2^k, else 0 [proved]; k* = 1 at n = 7, 15 [computed]".

7. **Overstated. Theorem 150, l. 366–367 and l. 376–378.** The statement under [proved] includes "k* = 1 at n = 5,
   the same for rule 105", but the proof gives k* ≥ 1 and then "k* = 1 [computed]". The gap closes for rule 150:
   a single flip of 00000 or of 10101 yields every code (codes after one flip 01234567, §4). With Lemma 2.2 of the
   paper (`lem:kzero`) this gives k_v ≤ 1 for all v, hence k* = 1. For rule 105 the periodic states 00100 and 10001
   reach only codes 0..6 by one flip, so its k* = 1 stays computed.
   *Proposed wording:* add to the proof "every code occurs in a single flip of 00000 or 10101, so k* = 1 (paper,
   Lemma 2.2)", and change "(k* = 1 at n = 5 computed)" for rule 105.

8. **Overstated. Plain-words summary, l. 660.** "Reflecting walls behave much more like the ring" is not supported
   by the data.
   - B-type rules at n = 12: ring 138, null walls 181, reflecting walls 180 (§9, §7).
   - Classes on the same side as the ring at every n = 8..12: 65 of 88 under reflecting walls; 58 of 88 under null
     walls, counting both null classes of a ring class (§9).
   - Classes changing side in n = 8..12: ring 13, reflecting walls 1.

   The one property that clearly carries over is the power-of-two arithmetic of rule 90 (Lemma M′).
   *Proposed wording:* "reflecting walls keep the ring's power-of-two arithmetic for rule 90, but otherwise remove
   the size dependence much as null walls do (one class changes side in n = 8..12 against 13 on the ring)".

9. **Overstated. Plain-words summary, l. 647–648.** "For the additive rules 60, 90 and 150 this is proved for every
   row length." Theorems 90 and 150 assume n ≥ 4. At n ≤ 2 the codes 101 and 111 cannot occur at all, because the
   edge cells read wall values.
   *Proposed wording:* "proved for every row of at least 4 cells".

10. **Overstated. Section 1, l. 65–66.** The phrase "only noise-free recurrent classes can be stochastically stable"
    is set in quotation marks but is not in the source. Miękisz (arXiv q-bio/0703062v1, p. 23) assumes that the
    noise-free dynamics has no recurrent class with more than one state, and concludes that only absorbing states
    can be stochastically stable. The tree representation, eqs. (49)–(50), p. 23, is general, and the source allows
    Λ to be a finite subset of "Z, Z², or any other infinite graph" (p. 22).
    *Proposed wording:* "the tree representation (eqs. (49)–(50), p. 23) holds for any finite state space; the
    source states the consequence only for dynamics whose recurrent classes are single states ('only absorbing
    states can be stochastically stable', p. 23)".

11. **Overstated. Section 5.6, l. 501 (class 22).** The row reads "carries over partly: only at n = 2^k − 2 (to
    n = 62)". Up to n = 62 only the seed deaths (r(0) ≥ 2) are computed. The value k* ≥ 1 is computed only for
    n ≤ 20 (at n = 4, 5, 6, 14).
    *Proposed wording:* "the zero state has radius 2 exactly at n = 6, 14, 30, 62 in 4..62; k* = 1 there is
    computed for n = 6, 14".

12. **Overstated. Section 5.0, l. 292.** The text says these classes become B-type, "so k* >= 1 at every n". This
    is computed for n = 4..16 (5.4).
    *Proposed wording:* "at every computed n (4..16)".

13. **Overstated (true, but the evidence cited does not establish it). Section 5.3, l. 460–461.** The report says
    the checkerboard of 122 has radius 2 "only at n = 7 and 15 among n = 4..61 (`local_radius2.csv`)". The cited file
    leaves 56 of the 112 flips undecided at n = 56. My own run at 4·10^5 steps decides n = 56 (radius 1), so the
    statement is true (§11).
    *Proposed wording:* add "(n = 56 needs more than 2·10^4 steps)".

### Unclear

14. **Unclear. Section 5.3, l. 449 (22), l. 458 (122), l. 489 (137), l. 464 (126).** The parentheses "(and 4, 5, 6)",
    "(and 4, 5, 7)" and "(also 4, 5, 7)" can be read as carrying the description that follows. Read that way the
    text is false:
    - 22 at n = 4: three cycles are selected; at n = 5, two (missed code 5). The zero state is selected alone only
      at n = 6 and 14.
    - 122 at n = 4 and 5: three and two cycles are selected (missed 000). The checkerboard is selected alone only at
      n = 7 and 15.
    - 137 at n = 4 there is a single cycle missing code 5; at n = 5 two cycles are selected (missed 5, 7). A cycle selected
      alone with k* = 1 occurs at n = 7, 11, 13, 15, 17, 19.
    - 126 also has k* = 1 at n = 4 (missed 0, 5), which l. 464 omits (the table, l. 264, has it).

    Records are in §10. *Proposed wording:* state the small-n cases separately, e.g. "k* = 1 at n = 14 and 6 with
    the zero state selected alone; also at n = 4, 5, where 3 and 2 cycles are selected and code 101 is missed".

15. **Unclear (internal inconsistency). l. 293 against l. 503; G1 score l. 574.** Section 5.0 counts "37 … mod 3" among
    the "new dependences on n … that have no ring counterpart". Table 5.6 says the period-6 family of 37 "carries
    over as a mod-3 condition". If it carries over, G1 ("where a ring mechanism survives, the arithmetic moves to
    n + 1") fails for 37, because k* = 0 iff n ≡ 1 mod 3 is not the ring condition n mod 6 ∈ {0, 5} shifted. Then
    G1 is only partly correct. The carriers are the ring's period-6 pattern, but the arithmetic is new.
    *Proposed wording (5.6):* "37: **replaced** by a mod-3 condition (n ≡ 1 mod 3) carried by the period-6 pattern
    between walls; the ring's n mod 6 ∈ {0, 5} does not survive".

16. **Unclear. l. 80–83, 200, 316, 402, 454, 482 ("the ring paper"); l. 79, 196, 318, 356 ("the note"); l. 301
    (PROOF_154.md).** The names Lemma 1, Lemma 2, Lemma B, Lemma Z, Lemma H and the sections "5.3", "5.5" are those
    of `report_ring_size.md`, Section 4 and Section 5. They are not those of `paper/ring_size_paper.tex`, where the
    same results are Lemmas `lem:closure`, `lem:inclosed` and Theorem `thm:A`. "Theorem 1" and "Lemma 3" of the note
    are those of `note/note_v0.2.tex` (`thm:order`, `lem:ends`). `note/note.tex` has no theorem. PROOF_154.md is
    `verify_ring_size/part2_154/PROOF_154.md`.
    *Proposed wording:* name the files at first use.

17. **Unclear. Plain-words summary, l. 643–645.** "the all-zero state shakes off any single error only when the size
    is a power of two" holds for rules 60, 90, 154 and 26. For rule 22 the ring's zero state shakes off every single
    error at n = 4..8, 14, 15, 16, 30, … (`report_ring_size.md`, 5.3 table).
    *Proposed wording:* "for rules 60, 90, 154 and 26 the all-zero state …".

18. **Unclear. Plain-words summary, l. 657–658.** In "new size effects that the ring does not have, for instance
    patterns that fit only when n is a multiple of 3", the only multiple-of-3 fit under null walls is the 133 crystal
    (010)^k. That is the ring crystal of class {94, 133} with the ring's own arithmetic, which 5.0 (l. 290–291)
    itself presents as a survival.
    *Proposed wording:* "for instance dependences on n mod 3 (rules 37, 91, 75) or on the parity of n
    (rules 135, 137)".

19. **Unclear. Short form l. 278 (ring column for 26).** "2^k: zero state; else code 7" does not say that ring k* = 0
    at n = 11, 14, 17, 20 (table l. 228).
    *Proposed wording:* "k* ≥ 1 at 2^k (zero state) and at most other n (code 7 missing); k* = 0 at n = 11, 14, 17,
    20".

20. **Unclear. l. 199 and l. 168.** The 2040 non-bijective records of l. 199 cover all 160 classes at n = 4..16 plus
    the 12 classes at n = 17..20; the range is not stated (counts confirmed, §7). "The largest job was class 76 at
    n = 16 (52 s, 531 MB)" is right for memory, but by time the largest job was class 133 at n = 20 (224 s,
    480 MB; `null_sweep_cost.csv`).

21. **Unclear (gap, statement true). Section 6, l. 518–519 and l. 564–566.** Lemma M′ gives only one direction of
    each "consequently":
    - **Rule 90.** If 2n is a power of two, the ring of 2n is nilpotent, so the row is. For the converse: the lift
      of e₀ is 1 + z^(2n−1) = z^(−1)(1 + z). Write 2n = 2^s q with q odd and q > 1. The generalised kernel then
      consists of the multiples of ((z^q − 1)/(z − 1))^(2^s), which is coprime to 1 + z, so e₀ does not die.
    - **Rule 150.** For 3 ∤ n the ring of 2n is bijective, hence so is the row. For 3 | n the row has the kernel
      vector (101)^(n/3) (checked n = 3..18, §4).

    *Proposed wording:* add these two lines.

### Cosmetic

22. **Cosmetic. Lemma M proof, l. 333–334.** "the two reflections j → −2 − j and j → 2n − j" are one map
    (−2 − j ≡ 2n − j mod 2n + 2), which fixes both cells N − 1 and n. The proof is otherwise correct.
    *Proposed wording:* "the reflection j → −2 − j of Z/NZ, which fixes the cells N − 1 and n".

23. **Cosmetic. Lemma Z′, l. 423.** For reflection-symmetric rules ⌈n/2⌉ seeds are needed, not n/2.

24. **Cosmetic. l. 438.** The inclusion F(M) ⊆ M whose proof "goes once around the ring" is Lemma 4 of
    PROOF_154.md; Lemma 6 only quotes it.

25. **Cosmetic. Section 1, l. 56–57, 59–60, 66–67; Section 5.5, l. 480, 483.** Five small slips:
    - Vadali and Turner's Lemma B.3 (p. 20) is the equality CL[σ1(n)] = CL[σ̄1(2n+2)], not the embedding, which is
      Thm. 6.2.
    - The page numbers of Bhattacharjee et al. and Wang et al. are those of the arXiv copies (the literature file
      says so; the report does not).
    - "All spatial examples read there use rings": Example 6 (p. 36) is on Z² with periodic boundary, a torus.
    - 37, l. 480: at n ≢ 0 mod 3 the period-3 fixed points are not (010)^k (e.g. 1001001001 at n = 10).
    - 91, l. 483: at n = 5 the missed code is 000, not 101.

### Record

26. **Record (reader's finding 1). l. 581–583, l. 613.** Authorship of expectations (a)–(c) cannot be decided from
    the repository. The sealed file calls them "Frank's expectations (from his chat with Claude; scored like mine)".
    The reader states they were written by Claude in the planning conversation, and that their deterministic facts
    had been computed before the session. I can neither confirm nor refute either claim. If the second is right,
    item "(a) facts" is not a prediction and should not be scored.

27. **Record (reader's finding 2), `data/boundaries/ring_vs_null.csv`.** Confirmed. For a rule that is not the
    representative of its null class, the column `null_missed` holds the representative's missed codes instead of
    their mirror image. That affects 142 rows at n ≤ 9 (the reader's count for the reader's subset) and 312 of the
    3388 rows with null data in the whole file. k* is unaffected (0 differences; §12).

28. **Record. Status block l. 5–11 and l. 24; Section 8 item 9, l. 635; Section 9.** These parts still describe the
    session's situation: base 2765f7e (version 0.4), nothing committed. The six step commits are now in the
    repository on b3a73ce (version 0.5), applied by the reader (`reader_checks/README.md`, "Open boundaries").
    *Proposed wording:* a dated note at the top of the status block.

## What I did not check

- **Stationary laws.** I computed none. I neither reran nor reimplemented the study's GTH check (`verify_null_gth.csv`
  1536 of 1536 ok, maximal deviation 7e-06; `verify_reflect_gth.csv` 1280 of 1280, 4e-06; I read the files only).
  The link between the integers k_c and the orders of π rests on the note's Theorem 1, whose proof I read (item 2).
- **The study's certificates, tests and scripts.** I did not run `check_cert.py` or my own checker on the
  certificates; I counted the files (1850 null, 792 reflecting) and read the logs. I did not run the study's tests,
  because of the own-code rule (logs: 24, 21 and 16 passed).
- **Timings.** I did not reproduce the estimates and measured times in the table of Section 4.
- **Two cells of the table in 5.0.** 94 at n = 20 and 133 at n = 18 have more cycles (1903, 1902) than my cap for
  exact potentials. I confirmed the side and the selected set (single closed class = the crystal), not the value 1.
- **Sizes not computed.** Null walls at n ≥ 17 for classes other than the twelve; reflecting walls at n ≥ 13.
- **Descriptions.** Some were not checked: "flips next to a wall heal like interior ones" (l. 404); the placements of
  the 133 crystal against one-walls (l. 410); the 37 "domain-wall 2-cycles" beyond the selected set at
  n = 5, 8, 11 and the carriers of 010/101 at n = 9..13; "a single flip at an edge leaves it" for reflecting 94
  (I checked radius 1, not which flip).
- **Literature.** The counts "nine sources … nineteen further candidates" (l. 44–45). The published (non-arXiv)
  versions and their page numbers. Martín del Rey's source [14] for Prop. 4.1. The parts of
  `literature_boundaries.md` that Section 1 does not use, apart from the Wang entry.
- **Reader's finding 1 (authorship).** Not decidable here (finding 26).
- **Section 9.** I did not execute the commands.

---

## Appendix A. Proofs (task 1)

Tests: `verify_boundaries/proof_tests.py` (output `out/proof_tests.txt`) and `checks.py` §1–§5, §10.

| proof | verdict | small-n test (own code) |
|---|---|---|
| Section 2, symmetries (i), (ii) | correct as written. phi preserves H, conjugates F, maps D_c to D_pi(c); reflection works for all four boundaries; complement maps null to one and preserves ring and reflect | conjugation of maps and code masks, 256 rules, n = 1..10, four boundaries: no failure (negative controls fail as expected); reflection partners have equal m, k* and mirrored k_c for all 256 rules, n = 4..11; 160 / 64 / 16 classes and the table l. 107–122 reproduced |
| Lemma 0 as used (l. 301) | correct (PROOF_154.md l. 48; the paper's Lemma 2.3 (`lem:edge`) is the same) | resistances by own 0-1 BFS equal brute-force Dijkstra on the full resistance graph (rules 22, 26, 30, 37, 90, 94, 110, 122, 154, 218; n = 4, 5) |
| Proposition L | correct as written (Fitting decomposition; F^T(y + e_i) = y + M^T e_i; the reverse flip; g_i span V_inv) | 16 affine rules, n = 3..14: one closed class containing all cycles in all 192 records; all gamma = m − 1 where computed (n ≤ 9) |
| Lemma F | correct | used in the checks of 165 and 15 (the fixed points carry the codes {1, 2, 4} for 165 at n = 7, 15, and {2, 4, 5} or {2, 5} for 15, within the sets {1, 2, 4, 7} and {2, 3, 4, 5} that Lemma F allows) |
| Lemma W | correct as written ((im M^K)^⊥ = ker M^K for symmetric M over GF(2); projection onto three coordinates) | rules 90, 150, 165, 105, 204, 51, n = 3..14: hypothesis true in 66 cases, all with eight codes at cell 1 |
| Lemma M | correct; cosmetic slip (finding 22) | holds for exactly the 16 rules named, n = 1..10 (all 256 rules tested) |
| Theorem 90 | correct. One unwritten step: z^4 · lift(u) lies in the generalised kernel because M_ring commutes with rotation; trivially closed | own GF(2) linear algebra n = 3..128: 90 and 165 miss a code exactly at n = 3, 7, 15, 31, 63, 127; exact k* = 2 (90) and 1 (165) at n = 7, 15, 0 elsewhere to n = 20 |
| Theorem 150 | correct with a gap (finding 7): "k* = 1 at n = 5" is computed in a [proved] theorem; closed for 150, not for 105. The order "also V_nil ≠ 0" before its justification (the kernel vector, l. 376–377) is only a matter of order | char. polynomial case n = 5: periodic states {00000, 10101}; kernel (110)^k 11 at n ≡ 2 mod 3, n = 2..20; linear algebra to 128: a code is missed only at n = 5 |
| Classes 60, 153 and the shifts | correct | 60, 102, 153, 195 bijective at every n = 3..128; k* = 3 for 170, 1 for 15 at n = 4..16 |
| Bijective rules | correct; uses no ring | 32 bijective records n ≤ 8 solved with full potentials: all cycles selected, k* = 0 |
| Lemma Z′ | correct; cosmetic (finding 23) | — |
| Proposition N | correct as written (both rules equal A on one-parity states; walls 0 needed at the edge cells) | orbits of every e_i under 154 and 26 equal the rule-90 orbits for n = 3..40 (3n steps); all e_i die exactly at n = 3, 7, 15, 31 in 3..40 |
| Lemma M′ | the lemma is correct; its two "consequently" statements have a gap, closed in finding 21 | holds for exactly the 64 symmetric rules, n = 1..10; reflecting rule 90 nilpotent exactly at n = 1, 2, 4, 8, 16; reflecting 150 bijective exactly at 3 ∤ n (n ≤ 16); reflecting 60 never bijective |

## Appendix B. "Uses no ring" (task 2)

- **Note, Theorem 1** (`note/note_v0.2.tex`, `thm:order`). Correct: the claim holds. The proof uses the Markov chain
  tree theorem, censoring on cycle states plus x, contraction of cycles, and Lemma 3 (π of the cycle states → 1).
  Lemma 3's proof uses only (1 − ε)^n and the longest transient. No step uses rotation. The note's setting is
  written for a ring (§1.1, "indices mod n"), but the proof carries over word for word.
- **Ring paper, Lemma 1, Lemma 2, Theorem A** (`report_ring_size.md`, Section 4; in `paper/ring_size_paper.tex`
  `lem:closure`, `lem:inclosed`, `thm:A`). Correct: the claim holds. Re-rooting, closed classes and the
  breadth-first in-tree use only V ≥ 1 between distinct cycles. Lemma B for q = 1 also uses no rotation; the step
  "gamma is constant on a rotation orbit" is needed only for q > 1, as the report says (l. 81–82).
- **PROOF_154.md, Lemma 0.** Correct: the claim holds; the proof uses only that a cycle state has a predecessor on
  its cycle.
- **Theorem A against the data.** In all 2797 exact null records with one closed class, S equals that class and
  gamma_min = m − 1. The two records with two closed classes are 218 at n = 7 (both classes selected) and at n = 15
  (88 of 89 selected) (§6).

## Appendix C. Numbers (task 3)

Own solver: `vb.py` (numba). It builds the step table for ring, null, one and reflect from the definition, finds
the cycles and the one-flip graph, runs a 0-1 BFS from every cycle for V and R(C → D_c), and computes every gamma
by root-free Edmonds contraction. That contraction was checked against per-root `networkx` arborescences on 300
random matrices with no difference. Records whose cycle count is above the cap are decided by the one-flip graph
and Theorem A (side only).

- **`null_sweep.csv`.** All 2128 records agree in every field: m, bijectivity, codes on cycles, number selected,
  gamma_min, missed codes, every k_c, k*. 2005 records have exact potentials, 88 are bijective, and 35 are decided
  on the one-flip graph (side compared). Own data: all 256 rules for n = 4..11, the 160 representatives for
  n = 12..16, the twelve classes for n = 17..20 (§6).
- **Section 4 counts.** All reproduced (§7):
  - 110 / 38 / 12 classes and the list of twelve;
  - 31 classes change side in n = 4..14;
  - 186, 187, 189, 187 rules with k* ≥ 1 at n = 12, 13, 14, 16;
  - 181 and 180 B-type rules at n = 12 and 16;
  - 2038 of 2040 non-bijective records with one closed class, and 562 single-cycle records;
  - the bijective classes.
- **Ring side.** Ring values 180, 174, 172, 188 and B-type counts 138, 142 agree with `data/fw_sweep.csv`. My own
  ring recomputation, 88 classes, n = 4..12, agrees with `fw_sweep.csv` at every (class, n).
- **Table of 5.0.** All 740 cells agree: null and fixed-1 rows against my records, ring rows against
  `fw_sweep.csv`. For two cells only the side is confirmed (see "What I did not check") (§8).
- **Section 6.** All 792 records of `reflect_sweep.csv` agree. So do the table l. 528–557 and the counts
  60 / 62, 42 / 59, 13 / 1 (class 90) and 65 of 88 (§9).
- **`affine_null.csv`.** All 2016 records agree (§5).

## Appendix D. Observed patterns (task 4)

Checked against my records (§10, §11). Where the wording says more than the data, the finding is given.

| claim | verdict |
|---|---|
| short form "iff" rows, "n ≥ 8, n ≤ 20 where computed" (l. 268–287) | supported over the stated range, except the issues in findings 6 and 19 |
| 94: crystal selected alone at n ≡ 2 mod 3, 8..20; radius 2 to 62; m − 1 of m selected at n = 9..19, n ≢ 2; exceptions 4 and 7 (3 of 4, 7 of 8, missed 000) | supported |
| 133: (010)^k alone at 3 \| n, 6..18; all selected at n = 1, 2 mod 3, n ≥ 7 (also n = 4); radius 2 to 60 | supported |
| 75: crystal alone at n ≡ 2; 2-cycle alone at n ≡ 1 (missed 001, 111); k* = 0 at 3 \| n; 7 of 7 at n = 12; radius 2 to 41, 1 at 44, …, 62 | supported |
| 154, 26: periodic states on one parity class; union {0, 1, 2, 4, 5}; equal cycle counts 2, 3, 2, 1, 4, 4, 2, 6, 2, 6, 12, 1, 20 | supported (n = 4..16); the observed "every orbit enters the one-parity set" is tagged correctly |
| 166: codes {0, 2, 4}, two fixed points, both selected | supported at every n = 4..16 (not only n = 10) |
| 22 seed set; 122 and 137 radii; 122 zero state never radius 2 | findings 2, 13; otherwise supported |
| 43: ⌊n/2⌋ cycles, 101 absent; 142: ⌈n/2⌉ + 1 cycles; 35: one cycle {0, 3, 6, 7}; 59 | supported n = 4..16 |
| 37 (k* = 0 iff n ≡ 1 mod 3, n = 4..20), 91, 135, 137 | supported; findings 4, 14, 25 |

## Appendix E. Literature (task 5)

Opened in this session: open copies downloaded by `verify_boundaries/lit_check.py`. Locations are in
`out/lit_locations.txt`; PDF page = arXiv page, and for Martín del Rey journal page = PDF page + 106.

| attribution (Section 1) | found at | verdict |
|---|---|---|
| Martín del Rey, Prop. 3.1(a), pp. 113–114 (rule 90 null reversible iff n even) | statement p. 113, proof pp. 113–114 | correct |
| Martín del Rey, Section 4, pp. 120–121 (60, 102 reversible every n) | Section 4 starts p. 119; ECA 60 p. 120, ECA 102 p. 121 | correct |
| Martín del Rey, p. 121 (150 reversible if n ≡ 0, 1 mod 3, stated) | p. 121, "(see [14])" | correct |
| Vadali–Turner, Thm. 3.4 p. 6; Thms. 3.4, 3.6 (converse); Thm. 5.1 p. 9 | p. 6, p. 7, p. 9 | correct; the converse follows as stated |
| Vadali–Turner, Thm. 6.2 p. 12 and Lemma B.3 p. 20; "usually does not work" pp. 12–13 | p. 12; p. 20; sentence begins p. 12, ends p. 13 | correct, except the role of Lemma B.3 (finding 25) |
| Tadaki, eq. (2.4), p. 3; numerical, N ≤ 32 | (2.4c) p. 3, results of the author's paper I; Table I N = 3..32, pp. 11–12 | correct |
| Tadaki, 150 transients exactly at N = 3m + 2, p. 4 and Table I | p. 4; Table I (N = 5, 8, …, 32) | correct |
| Bhattacharjee et al., Section 3.3, pp. 13–14 | Section 3.3 p. 13, Fig. 6 p. 14 (arXiv draft) | correct (finding 25) |
| Wang et al., Thms. 1–5, pp. 5–8 | Thm. 1 p. 5; 2, 3 p. 6; 4 p. 7; 5 p. 8 | correct |
| Wang et al., Table 1, p. 10, rule 195 | rule 195 is in the periodic block | **false** (finding 1; conflict resolved) |
| Miękisz, Section 7, pp. 22–24 | Section 7 starts p. 22; (49)–(50) and the absorbing-state statement p. 23; (51) p. 24 | overstated (finding 10); examples (finding 25) |

## Appendix F. Predictions (task 6)

`shasum -a 256 PREDICTIONS_boundaries.md` gives d5e5b52061bb5434b128bb5c0e8a1eef4ab17b13545742d386b5a4e4217ec33d,
equal to l. 15. The file was added in 20b582c ("step 2"), before the commit with the sweep (24ff6a9). The
commits' dates are those of the reader's application (25 Nov 2026); the time order of sealing and computation rests
on the report's statement and the artifact named in l. 687–689, which I did not see.

Item by item against the data (§7, §10, §13): every "outcome" column agrees with the data. That includes G4 (k* = 3,
1), G5 (186 / 187 / 189 vs 180 / 174 / 172; 187 vs 188 at 16), G6 (153 of the 166 rules at each of n = 12, 13, 14)
and G7 (9 classes). The tally of the report's own items (28: 17 correct, 5 partly, 6 wrong; all wrong items marked L;
all H statements held) is reproduced from the table.

Two scores are not consistent with the sealed rule:
- (a) for 94 (finding 5);
- G1, if 5.6's reading of class 37 is kept (finding 15).

The other scores follow the rule. Some calls are generous but defensible: "37 partly" could be "correct", since
k* ≥ 1 at two thirds of the n; "154 partly" with its radius part proved.

## Appendix G. The reader's three findings (task 7)

1. Attribution of (a)–(c): not decidable from the repository (finding 26).
2. `ring_vs_null.csv`, `null_missed`: confirmed; 142 in the reader's records, 312 in the whole file; k* not
   affected (finding 27).
3. Rule 22 at n = 55, 57: confirmed (periods 112 and 120 at 2·10^4 steps). In addition, n = 56 is decided at
   4·10^5 steps (finding 2).

## Appendix H. Plain-words summary, sentence by sentence (task 8)

1. "The earlier results … neighbour of the first." Correct.
2. "This study cuts the ring open … whole rule table." Correct.
3. "On the ring … power of two." Unclear (finding 17).
4. "With walls, two of these effects survive in shifted form." Correct as a summary of 5.0. 5.6 lists more partial
   survivals (22; 37 as worded there).
5. "The period-3 pattern of rule 94 now fits when the period divides n + 1, because the walls act as two of its
   cells;" Correct (fixed point exists iff 3 | (n+1), n = 3..20).
6. "and the power-of-two effect of rule 90 now appears when n + 1 is a power of two." Correct (proved for n ≥ 4).
7. "For the additive rules 60, 90 and 150 this is proved for every row length: …" Overstated (finding 9). The three
   clauses are otherwise correct (60: k* = 0; 90: k* ≥ 1 iff n + 1 = 2^k; 150: only n = 5).
8. "The patterns that travel around the ring (rules 43, 142, 35) cannot travel between walls." Supported by the
   data for n = 4..16; not proved.
9. "These rules no longer depend on the size: …" False (finding 3).
10. "This is the most common effect of the walls: … (181 of 256 rules at 12 cells, against 138 on the ring)."
    Numbers correct; "the most common effect" is an interpretation.
11. "The walls also create new size effects …" Unclear (finding 18).
12. "These are computed for rows up to 20 cells and described, but not proved." Correct.
13. "Holding the walls at 1 instead of 0 is the same as complementing the rule, so it needs no separate computation;"
    Correct if "complementing" means the complement conjugate R*.
14. "reflecting walls behave much more like the ring." Overstated (finding 8).

## Appendix I. Reproduction

Python 3.11.18, numpy 2.4.6, numba 0.68.1, scipy 1.17.1, pandas 3.1.1, networkx 3.6.1, pypdf 7.0.0 (for
`lit_check.py`). macOS laptop, at most 2 worker processes. From the repository root:

```sh
cd verify_boundaries
python3 sweep.py null 4 11 all 100000 out/null_all_n04_11.csv              #   4 s
python3 sweep.py null 12 16 nullreps 2500 out/null_reps_n12_16.csv         # 4.2 min
python3 sweep.py null 17 20 22,37,75,90,91,94,122,126,133,135,137,165 1000 out/null_12cls_n17_20.csv   # 52 s
python3 sweep.py reflect 4 12 ringreps 2500 out/reflect_reps_n04_12.csv    #   8 s
python3 sweep.py ring 4 12 ringreps 2500 out/ring_reps_n04_12.csv          #  12 s
cd ..
python3 verify_boundaries/checks.py      > verify_boundaries/out/checks_summary.txt   # about 2 min, one process
python3 verify_boundaries/proof_tests.py > verify_boundaries/out/proof_tests.txt
python3 verify_boundaries/lit_check.py   > verify_boundaries/out/lit_locations.txt    # downloads the open PDFs to ./lit
```

The sweep columns are: m, bijectivity, codes on cycles, B-type, closed classes (sizes, codes), and whether the
potentials are exact. Where they are, the sweep also gives gamma_min, the number selected, the codes covered and
missed, k_c, k*, whether S equals the union of the closed classes, and the smallest states of up to 20 selected
cycles.
