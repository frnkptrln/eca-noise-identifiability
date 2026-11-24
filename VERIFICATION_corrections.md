# Verification of the corrections made after `VERIFICATION_paper.md`

> **Handling of the findings (24 November 2026).** Written by Claude, the reader outside the sessions, who made the
> corrections that this report checks and then worked its findings into version 2 of the paper
> (`paper/TRACE.md`, Part G). The report below is unchanged.
>
> * Applied as proposed: E1 (the paper says "a lemma of the proof document for rule 154" and does not give the
>   number 0), E2, E4, E5, E7, E8 in the paper; E9, E10 in the header of `VERIFICATION_paper.md` and in
>   `paper/TRACE.md`, Part F; E11 to E15 in `README.md`.
> * Applied with other wording: E3. The statement on the use of AI names what the pass changed, as proposed, and
>   says "five findings were not applied or were applied in part" where the proposal lists them by number. "Status
>   of the proofs" says that the corrections "were checked afterwards by a further session" and what it found.
> * No change: E6 (none proposed).
> * In the same pass the proposals of the sources session were applied (`literature_addendum.md`, update of
>   24 November 2026). These changes, and the changes listed here, were not checked by a further session. They
>   concern sentences about the paper and its sources, Remark 3.44, the caption of Table 2 and one citation in the
>   proof of Proposition 5.9.
> * The line numbers below refer to the text of commit 20cf1fd (version 1 of the paper, tag v0.4).

**No correction made a true statement false.** One correction added a false clause to "Status of the proofs" (E1). Its wording comes from the report's own proposal under D13.

Repository `~/git/eca-noise-identifiability`, checked out on 24 November 2026: branch `sources-0.5` at 20cf1fd.
That is `main` (2765f7e, the merge of the v0.4 DOI) plus one commit that changes only `literature_addendum.md`. So
`git diff 9141d67 HEAD -- paper/ring_size_paper.tex` is the same from either commit. It holds the corrections
(29d94f7, 20 November) and the DOI commit (51606db, 23 November). Verified by Claude, 24 November 2026. I did not
write the paper, the earlier reports or the corrections. No existing file was changed; this file is the only new one.

## Verdict

The pass is sound in its mathematics. Each of the 49 hunks of the diff answers a finding of `VERIFICATION_paper.md`,
or is the 23 November DOI change described at the end of `paper/TRACE.md`, Part F. No hunk is accounted for by
neither record. I read every sentence that the pass added to a proof or statement in its proof, as a referee. Each
one is correct, follows from what stands before it, and leaves the rest of the proof intact. For D7, D8 and D9 I also
tested the added claims with code of my own: D7 on n = 6, 10, 12, 14, 18, 20, 22; D8 on even n = 4..16; D9 on
n = 6..300 with 3 | n. There were no failures. No theorem, proposition, lemma or corollary changed in content.

The defects are in what the paper says about itself and in the README:

* **E1.** "Status of the proofs" calls Lemma 2.3 new as a lemma. It is Lemma 0 of the proof document for rule 154.
* **E2.** Two sentences say that the verification tested every statement. Proposition 2.1 was not tested.
* **E3.** The statement on the use of AI understates what the last pass changed in statements and proofs.
* **E12, E14.** Two sentences of the README section "In plain words" are false when read literally: the selected
  loops are "a few" and "hard to leave"; and wherever the stripes fit they are selected, while one cell more or less
  makes "other loops win".

Everything else is unclear wording, cosmetic, or a point of the record. I recommend fixing E1 to E3 and E12 to E14
in the next version. Tag v0.4 and its archive already contain the present text. Once this report is committed, the
two sentences that say the last pass "has not been verified" are out of date. They are rewritten in E3.

## Findings

Severity: **false** (a false sentence about the paper or its record), **overstated**, **unclear**, **cosmetic**,
**record** (a file other than the paper). Lines are lines of `paper/ring_size_paper.tex` at HEAD; pages are pages of
the committed 32-page PDF.

### In the paper

**E1. Status of the proofs, l. 159-160, p. 2. False (sources of the paper).**
The paragraph says "Lemmas 2.2, 2.3, 2.4 and 3.38(b) are stated in this paper for the first time as lemmas". Lemma 2.3
(`lem:edge`) is Lemma 0 of `verify_ring_size/part2_154/PROOF_154.md` (l. 48, tagged [proved]). The pass added only its
last sentence. `paper/TRACE.md`, Part A, row of Lemma 2.3, says so, and so does the table in Section 3 of
`VERIFICATION_paper.md`. `paper/REFEREE_NOTES.md`, update 2, item R8, names only Lemmas 2.2 and 2.4. The clause comes
from the correction proposed under D13 ("Lemmas 2.2 to 2.4 and 3.38(b) are stated here for the first time as
lemmas"), which contradicts D13(a) of the same report. The sentence it replaced said nothing about new lemmas, so
no true statement was made false.
Correction: "... and Lemmas 2.2, 2.4 and 3.38(b) are stated in this paper for the first time as lemmas (Lemma 2.3 is
Lemma 0 of the proof document for rule 154, with its last sentence added)."

**E2. Status of the proofs, l. 161-162, p. 2, and statement on the use of AI, l. 1703-1704, p. 23. Overstated.**
The two sentences read "tested every statement of the paper on small rings with code of its own" and "tested every
statement on small rings with its own code". In `VERIFICATION_paper.md`, Proposition 2.1 is "not tested" (Section 3,
first row; Section 6, "What was not checked"). This is the kind of overstatement that D5 and D6 corrected.
Correction at both places: "tested every numbered statement except Proposition 2.1, which is quoted from the note,
on small rings with code of its own".

**E3. Statement on the use of AI, l. 1705-1707, p. 23; Status of the proofs, l. 164-166, p. 2. Unclear (incomplete
account of the last pass).**
The AI statement reads: "Its findings on sentences of the surrounding text and on three proof steps that were not
written were worked into the text by the reader named above ...; this last pass has not been verified." Just before
this, the statement stresses that the sessions were instructed to add no mathematical step. A reader will take the
last pass to be limited to surrounding text and three steps. It was not limited in that way. `paper/TRACE.md`, Part F,
lists further changes:

* it changed the wording of six statements: Proposition 2.1, Theorem 3.9(d), Lemma 3.24, Remark 3.44,
  Definition 5.1 and Theorem 5.7(c);
* it added sentences to further proofs: Lemmas 2.4, 2.5, 3.2, 3.4(b) and 3.23, Theorems 3.9, 3.20, 3.26 and 5.7,
  Corollary 3.27, and Theorem 3.43(i), Step 6;
* it did not apply D22, D34, D36, D38 or part of D18.

Correction (AI statement): "The reader named above then worked its findings into the text: the sentences of the
surrounding text, the three unwritten steps, the wording of six statements and short additions to the proofs of
eleven further statements (`paper/TRACE.md`, Part F). D22, D34, D36, D38 and part of D18 were not applied, as the
header of that report records. That pass was checked in `VERIFICATION_corrections.md`." In "Status of the proofs",
replace "and have not been verified in turn" with "and were checked afterwards (`VERIFICATION_corrections.md`)".

**E4. Status of the proofs, l. 157-163, p. 2. Unclear; and the header of `VERIFICATION_paper.md` is inexact.**
The D13 proposal had a sentence on Lemmas 3.29 to 3.31. These lemmas are used in both parts of Theorem 3.43, come from
the document that the paragraph calls unverified, and were re-read by the verification of the case 3 ∤ n. The
sentence was dropped. The new text covers them only if "these proofs" is read as including the lemmas that part (i)
uses. The header nevertheless says that the paragraph "is rewritten as proposed".
Correction: write "(Section 3.1, Lemma 3.32 and part (i) of Theorem 3.43 with the lemmas it uses)", or restore the
proposed sentence.

**E5. Remark 3.44, l. 1258-1260, p. 17. Unclear (true, but incomplete).**
The remark reads "At n = 4 no block word has a long block (2a + 3b = 4 forces b = 0), so Step 3 of part (ii) does not
give the codes 011 and 110". This is true. But without a long block Step 3 also has no pair "short block followed by
long block". So it does not give the codes 111, 100 and 001 of the cycle D either. The code 000 comes from Lemma
3.42, which is stated for n >= 5 and fails at n = 4 (`VERIFICATION_paper.md`, T04). The remark's own computed sentence
says that only 010 and 101 occur. The first sentence, "is not proved for n = 3 and n = 4", is weaker than what is
known: the conclusions fail at both sizes. At n = 4, k* = 1, as stated in the remark. At n = 3 the selected set is
{{0}}. I computed this here (γ({0}) = 3, γ = 4 for each phase), and T05 of the earlier report agrees.
Correction: "Theorem 3.43 does not extend to n = 3 and n = 4. At n = 4 no block word has a long block (2a + 3b = 4
forces b = 0), so Step 3 of part (ii) gives only the codes 010 and 101, and Lemma 3.42 needs n >= 5; part (i) needs
n >= 6 (Lemma 3.32)."

**E6. Theorem 3.26, Step 2, l. 984-985, p. 14. Cosmetic.**
D32 proposed stating once that the complement maps cycles to cycles and edges of G1 to edges of G1 (for example as
Lemma 3.14(c)), and citing that. The pass cites "(end of the proof of Lemma 3.25)" instead, that is, a fact shown
inside a proof. The fact is correct: F commutes with the complement (Lemma 3.14), and the complement of x + e_j is
the complement of x plus e_j. The header counts D32 among the findings "applied as proposed, or reworded to the same
content". The result is a different remedy, though a defensible one.
Correction: none needed. Optionally, move the sentence into the statement of Lemma 3.25.

**E7. Proof of Proposition 5.9, l. 2252, p. 32. Cosmetic; and `paper/TRACE.md`, Part F, is inexact.**
The clause "and y + e_b is periodic as a domain state" goes beyond the D7 proposal. It is correct: y + e_b has the
sources a and b and the free cell a + 2^(e+1) of the longer domain. My code confirms that it is a domain state and
periodic for every admissible (a, b) on n = 6..22. But it gives no citation. Part F says that every sentence added to
a proof "is the correction proposed in the report, or a rewording of it". This clause is neither, although Part F
does list it.
Correction: "... periodic as a domain state (Lemma 5.4(c))"; in Part F, "..., or a rewording of it; the clause on
y + e_b in D7 is added beyond the proposal".

**E8. Caption of Table 2, l. 1318-1319, p. 18. Cosmetic.**
The caption says that the number of ones on the parity class with fewer ones "is not constant on a cycle". Read
literally, this means "on no cycle". It is constant on many cycles. For rule 154 the number varies on 10 of the 31
cycles at n = 8 and on 193 of the 308 cycles at n = 12 (computed here).
Correction: "need not be constant on a cycle".

### In the records

**E9. Header of `VERIFICATION_paper.md`, item D18. Record (the reason is inexact).**
The header says that moving Lemma B.6 "would renumber Section 5, to which `reader_checks/README.md`,
`literature_addendum.md` and this report refer". Neither of the first two files names any numbered statement of
Section 5. I searched both for "Theorem/Proposition/Lemma/Corollary/Remark/Definition 5.x" and found none. Of the
files I searched, only `VERIFICATION_paper.md` does. `paper/TRACE.md` and `paper/REFEREE_NOTES.md` name Section 5
statements too, by their numbers in the PDF. Part F gives the sound reason ("so that the numbers of Section 5 do not
change"). The decision itself does no harm: see Part 5 below.
Correction: name only the files that do refer to Section 5.

**E10. Header of `VERIFICATION_paper.md`, item "Not applied", and Part F. Record.**
The reason given for D22, D34 and D38 is that renaming symbols in proofs just verified was judged the larger risk.
That does not apply to D22: the rate ρ(ε) occurs in no proof, only in the introduction, Section 2.3 and Proposition
2.1. Not applying D22 is still acceptable, since no sentence is ambiguous (Part 5).
Correction: "D22: no sentence is ambiguous; D34, D38: ...".

### In `README.md`, section "In plain words"

**E11. l. 28. Cosmetic.**
"one pattern, or a short sequence of patterns". The paper says only that there are finitely many cycles. Cycles can
be long. For rule 154 I computed cycles of length 120 at n = 15, 272 at n = 17 and 304 at n = 19. Correction: drop
"short".

**E12. l. 33-34. False when read literally.**
The README says the rarer the errors, "the more of its time it spends in a few loops: those that are hard to leave and
easy to reach". This fails in three of the cases the paper proves:

* For rule 154 with n not a power of two, every cycle is selected (Theorems 3.10 and 3.11). There are 5818 cycles
  at n = 19 (computed here; the same number is in T03 of the earlier report). G1 is strongly connected, so a single
  flip leaves each of them.
* For rules 43 and 142 with 4 ∤ n, the selected set is a whole closed class (Corollary 3.27).
* For rule 94 with 3 ∤ n, the same holds (Theorem 3.43(ii)).

Correction: "The rarer the errors, the more of its time it spends in some of the loops (in the text: the cycles of
least stochastic potential, the noise-selected cycles). Which loops these are, and how many, depends on the rule and
on the number of cells."

**E13. l. 43-44. Overstated.**
"for rule 94 on whether it is divisible by 3". The abstract of the paper names the exception: at n = 4, k* = 1
although 3 ∤ 4. The ring size n = 3 is not covered. The README's closing sentence refers to the paper for the ranges,
but this exception is part of the result, not a range.
Correction: add "(from five or six cells on; on four cells rule 94 is an exception)".

**E14. l. 47-48. False when read literally (two clauses).**

* "Where the stripes fit, ... the noise selects that pattern". At n = 3 the stripes 011 fit, but the noise selects
  the zero state: γ({0}) = 3 against 4 for each of the three phases (computed here; T05 of the earlier report). The
  paper proves selection of the stripes only for n >= 6 (rule 94) and n >= 4 (rules 43, 142). Remark 3.44 says that
  at n = 3 a single flip can leave the crystal phase.
* "Add or remove one cell, and other loops win". For rule 154 at n = 2^k ± 1, all loops are selected, the all-zero
  pattern among them (Theorem 3.11). That pattern does not lose; every other loop joins it.

Correction: "Where the stripes fit (from four cells on for rules 43 and 142, from six cells on for rule 94), or where
the all-zero pattern recovers, the noise selects that pattern, and it leaves table entries unused. Add or remove one
cell, and this is no longer so: the stripes do not fit, and for rule 154 every loop is selected, the all-zero
pattern included."

**E15. l. 36-40. Unclear (what is proved where).**
The README says the rule "can be read off quickly, and the more quickly the rarer the errors ... and more slowly the
rarer the errors are". This rests on Proposition 2.1, which the paper quotes from the note without proof and uses only
for this interpretation. The earlier verification did not test it. The section ends with "The statements, their
ranges and their proofs are in the paper", which suggests that the paper proves this too.
Correction: add "(this is the result of the note, which the paper quotes; the paper itself proves statements about
k*)".

The other sentences of "In plain words" agree with the paper:

* the description of a rule and of the ring;
* "many loops";
* the role of the eight table entries, and k* = 0 iff the selected cycles contain all eight (Lemma 2.2);
* the dependence on arithmetic for rule 154 (n >= 3) and for rules 43 and 142 (n >= 4);
* "the all-zero pattern, which recovers from every single error exactly when the number of cells is a power of
  two". For rule 154 this is proved: Theorem 3.9(b) for 2^k, and for other n Theorem 3.10 (G1 strongly connected,
  m >= 2) together with the rotation symmetry of the flips.

## Table: every hunk of `git diff 9141d67 HEAD -- paper/ring_size_paper.tex`

"listed in": H = header of `VERIFICATION_paper.md`; F = `paper/TRACE.md`, Part F (including its paragraph of 23
November). "true?" is my judgement after reading the new text against the paper and the records named. "computed"
refers to the checks in the appendix. Hunks 1 and 46 are from 51606db; all others are from 29d94f7. Every hunk is
listed in at least one of the two records.

| # | lines old → new | place | finding | as proposed? | true? | listed in |
|---|---|---|---|---|---|---|
| 1 | 55 → 55 | first page, \date | none: DOI of the paper's own record (23 Nov) | — | DOI not resolved here | F (23 Nov paragraph) |
| 2 | 64 → 64 | abstract, k* sentence | D42; D2 | D42 as proposed; D2 reworded ("determine k* and describe the selected cycles") | true (k* is defined from potentials and resistances; "from the potentials" is short) | H |
| 3 | 75 → 75 | abstract, last sentence | D17 | as proposed | true | H |
| 4 | 90 → 90 | introduction, crystal cycles | D1 | as proposed (verbatim) | true (Thms 3.20(1),(2), 3.43(i)) | H |
| 5 | 102 → 103 | introduction, data file | D40 | as proposed | true (caption of Table 1; OpenNmax = 22) | H |
| 6 | 111 → 113 | introduction, Results | D2 | reworded, same content | true | H |
| 7 | 133 → 136 | introduction, What was known | D15 | as proposed | true | H |
| 8 | 145 → 148 | Status of the proofs | D13; header bullet (name the report) | other wording; the sentence on Lemmas 3.29-3.31 dropped | false clause (E1); overstated (E2); E4 | H |
| 9 | 181 → 192 | Sec. 2.2, number of cycles | D23 | as proposed | true | F |
| 10 | 207 → 218 | Prop. 2.1; sentence before Lemma 2.2 | D29; D14 | D29 other wording (definition of the note); D14 as proposed | true (note: ord = exponent of the leading power) | F; H |
| 11 | 226 → 238 | Sec. 2.4 heading | label for D30 | — | — | F |
| 12 | 249 → 261 | Lemma 2.4 proof; head of Sec. 2.5 | D28; D15 | as proposed | true | F; H |
| 13 | 263 → 275 | Lemma 2.5 proof | D27 | as proposed | true | F |
| 14 | 313 → 325 | Attribution paragraph | D20 | as proposed | true (VERIFICATION_ring_size.md A21: provisional) | H |
| 15 | 328 → 340 | after Theorem 3.1 | D2 (l. 330-331) | as proposed | true | H |
| 16 | 341 → 353 | Table 1 caption | D39 | as proposed | true (counts not recounted by me) | H |
| 17 | 372 → 384 | Lemma 3.2 proof | D25 | as proposed | true (computed) | F |
| 18 | 396 → 409 | Lemma 3.4(b) proof | D26 | as proposed | true | F |
| 19 | 446 → 459 | after Lemma 3.6 | D3 | as proposed | true (literature_ring_size.md l. 243-246) | H |
| 20 | 489 → 502 | Theorem 3.9(d) | D24 | as proposed | true | F |
| 21 | 513 → 526 | Theorem 3.9, proof of (d) | D24 | as proposed | true | F |
| 22 | 805 → 818 | Theorem 3.20, proof of (3) | D30 | as proposed | true | F |
| 23 | 883 → 897 | Lemma 3.23, proofs of (b), (c) | D31 | as proposed | true (computed, n = 5..14) | F |
| 24 | 896 → 912 | Lemma 3.24 statement | D12 | as proposed | true | F |
| 25 | 965 → 981 | Theorem 3.26, Step 2 | D32 | other remedy: pointer into a proof, not a stated fact (E6) | true | F |
| 26 | 983 → 1000 | Corollary 3.27 proof | D33 | as proposed | true (computed, n = 5..14) | F |
| 27 | 1203 → 1220 | Theorem 3.43(i), Step 6 | D35 | as proposed | true | F |
| 28 | 1238 → 1255 | Remark 3.44 | D10 | other wording | true, incomplete (E5) | F; H |
| 29 | 1286 → 1304 | Table 2, row 26 | D43 | as proposed | true | H |
| 30 | 1297 → 1315 | Table 2 caption | D17 | reworded, same content | true; "is not constant" reads as "never constant" (E8) | H |
| 31 | 1322 → 1341 | Definition 5.1 | D37 | as proposed | true | F |
| 32 | 1388 → 1407 | Lemma 5.4(c) proof | D8 | as proposed | true (read; computed n = 4..16) | F |
| 33 | 1424 → 1445 | Theorem 5.7(c) | D24 | as proposed | true | F; H |
| 34 | 1440 → 1461 | Theorem 5.7(a), Case 2 | D18 (clause on chi) | as proposed | true (computed n = 4..16) | F; H |
| 35 | 1477 → 1499 | Sec. 5, computed values | D11 | as proposed | true | H |
| 36 | 1498 → 1520 | Sec. 5, n = 22 values of chi | D45 | as proposed | true (VERIFICATION_94_26.md, test S7n22) | H |
| 37 | 1531 → 1554 | Sec. 6.1, stochastic stability; Bagnoli et al. | D20; D44 | as proposed; reworded | true (records) | H |
| 38 | 1554 → 1578 | Sec. 6.1, Zhu and Richard | D44 | as proposed | true (addendum has the update of 20 Nov) | H |
| 39 | 1566 → 1590 | Sec. 6.1, rule 184 | D21 | as proposed | true | H |
| 40 | 1582 → 1606 | Sec. 6.1, What was not found | D4 | reworded, same content | true (PROOF_26.md l. 337, PROOF_94_converse.md l. 385) | H |
| 41 | 1596 → 1622 | Sec. 6.1, two versions | D44 | reworded | true | H |
| 42 | 1611 → 1637 | Sec. 6.2, class 45 | D41 | as proposed | true | H |
| 43 | 1630 → 1655 | Sec. 6.2, rule 26 | D16; D43 | as proposed | true | H |
| 44 | 1653 → 1677 | Statement on the use of AI (first part) | D5; D6; header bullet | as proposed | true (VERIFICATION_94_26.md Sec. 1; reader_checks/README.md) | H |
| 45 | 1673 → 1698 | Statement on the use of AI (last part) | D19; header bullet | as proposed, plus the account of the verification and of the pass | overstated (E2); incomplete (E3) | H |
| 46 | 1685 → 1717 | Code and data | none: version 0.4 and the paper's DOI (23 Nov) | — | true (tag v0.4 contains paper/, proofs_43_142/, proofs_94_26/); DOI not resolved | F (23 Nov paragraph) |
| 47 | 1769 → 1802 | Lemma 3.32 proof, (a) and (b) | D9 | as proposed | true (read; computed n = 6..300) | F |
| 48 | 2048 → 2085 | Appendix B, first paragraph | D18 (part) | as proposed | true (TRACE rows of Lemmas B.2, B.6) | H |
| 49 | 2209 → 2247 | Prop. 5.9 proof, domain cycles | D7 (+ clause on y + e_b) | as proposed; one clause beyond it (E7) | true (read; computed n = 6..22) | F |

## Part 2: the sentences added in statements and proofs

I read each sentence in its proof and checked three things: is the step correct, is it justified by what precedes
it, and does the rest of the proof still stand.

* **D7 (Proposition 5.9, domain cycles).** On one parity class, with Σ = σ², F² = L² = σ² + σ⁻² = Σ⁻¹(1 + Σ)²
  (Lemma 5.6). Σ commutes with (1 + Σ)^(2^e), so Σ and Σ⁻¹ map its image into itself. They are injective, so they
  are bijections of the finite image. 1 + Σ is invertible on the image, by the sentence before. So F² permutes the
  image, every state of the image is F²-periodic, and so it is F-periodic. y lies in the image, and its cycle lies in
  E ∪ O because F exchanges E and O. y + e_b is a domain state (E7). The step is correct and complete, and the
  argument before and after is unchanged.
  Computed for n = 6, 10, 12, 14, 18, 20, 22:
  * F² = Σ⁻¹(1 + Σ)² on all of E and all of O;
  * the image of (1 + Σ)^(2^e) equals the set of periodic points of 1 + Σ, and F² permutes it;
  * every state of the image is F-periodic;
  * for every admissible pair of sources (a, b): the longer domain has length >= 2^(e+1) + 1, y is periodic with
    its cycle in E ∪ O, and y + e_b is a domain state and periodic;
  * the conclusion of the paragraph (every domain cycle and every cycle in E ∪ O lies in the one closed class) holds
    at n = 6, 10, 12, 14.
* **D8 (Lemma 5.4(c)).** Rotation by one cell exchanges E and O, so it keeps M. It also keeps the cyclic order of
  the ones, the groups, the sources and their distances. So it maps domain states to domain states, and σ⁻¹ is a
  bijection of that set. U is a bijection on each set with given sources, so U and F = σ⁻¹U are bijections of the
  union. Every domain state is periodic, and its orbit stays in the set, so its cycle is a domain cycle. The clause is
  now proved; the following sentences are unchanged.
  Computed for even n = 4..16:
  * the set defined by source distances equals the set built by the converse in Definition 5.1 (0, 12, 64, 240,
    816, 2688, 8704 domain states; at n = 4 none exist, since a positive even number of odd distances >= 3 cannot add up to 4);
  * the set is invariant under rotation, and F maps it onto itself;
  * every domain state is periodic, and its whole cycle consists of domain states;
  * U keeps the sources.
* **D9 (Lemma 3.32, (a) and (b)).** (O2) says that a flip of j removes from Occ only centres in {j-1, j, j+1}.
  * In (a), the only centre of x there is j. The occurrence centred at j covers exactly I. Since x is fully frozen,
    every cell outside I lies in another occurrence, and that occurrence survives.
  * In (b), the flipped cell is p + 1, and the only centre among p, p + 1, p + 2 is p. The same argument works with
    I = {p-1, p, p+1}.

  Both sentences are correct and use only (O2) and Lemma 3.30 ("fully frozen"). The earlier sentences on j ± 2 are
  now redundant but harmless. Lemma 3.29(iii) is then applicable as before.
  Computed for every n = 6..300 with 3 | n, every phase and every cell (45,441 flips), in the cases (a), (b) and
  (c):
  * the only centre near the flipped cell is the one named;
  * the other occurrences survive, cover every cell outside I, and make those cells frozen in y;
  * y agrees with x outside I for t = 0..3, and F³y = x.

  (O2) itself was checked on all states for n = 3..12.
* **D18 (Theorem 5.7(a), Case 2).** χ is the number of groups, which is the number of sources. The intermediate
  states are domain states with the same sources (Lemma 5.4(c)), so they have the same χ. This is what "Case 1
  applies to its cycle" needs for the induction on χ. Correct. Computed: for every domain state at even n = 4..16,
  the flip of a one on a free cell gives a domain state with the same sources and the same χ.
* **D23.** Dropping C_1, ..., C_m leaves no later use of an enumeration. I searched for C_m and C_i: the remaining
  C_0, C_1, ... are paths, defined where they are used.
* **D24.** "{{0}} is the only closed class" in Theorems 3.9(d) and 5.7(c), and "the cycle {0} has none" in the proof
  of 3.9(d). These match the definition (a closed class is a set of cycles) and the use of {X} and {A_i} in
  Theorems 3.20 and 3.43. Correct.
* **D25.** The listed values 0, 1, 0, 1, 1, 0, 0, 1 are the bits of 154, and they equal c + a(1 + b) (computed).
  Correct.
* **D26.** For odd q >= 3, the polynomial 1 + z + ... + z^(q-1) is not constant, so it has an irreducible factor.
  That factor is not z + 1, because the value at 1 is 1. By unique factorisation it divides no power of 1 + z.
  Correct.
* **D27.** In the new edge set every node reaches N, and N has no out-edge. A circuit cannot contain N, and from a
  circuit one never leaves it, so its nodes would never reach N. Correct. ("cycles" here means nodes of the graph,
  as elsewhere in the paper.)
* **D28.** The same content in two sentences. Correct.
* **D29.** The parenthesis matches the definition in `note/note_v0.2.tex` (ord g is the exponent of the leading
  power of ε, used in its Theorem 1). Correct as a gloss.
* **D30.** With "a contradiction", every closed class is {X}, and one exists (Section 2.4, "Every finite directed
  graph has a closed class"). Correct; the label `sec:g1` resolves to 2.4 in the PDF.
* **D31.** (b): a flip of a state of a cycle of K ends on a cycle of K. By Lemma 2.3 an edge of G1 is exactly such
  an orbit, so no edge leaves K. (c): the edge comes from Lemma 2.3. Correct. Computed for rules 43 and 142,
  n = 5..14 with 4 ∤ n: no flip of a state of a cycle of K leaves K.
* **D32.** See E6. Correct.
* **D33.** The lower level is not empty (z of Lemma 3.25 is periodic with w_- walls, as stated just before), so by
  Lemma 3.23(c) the upper level is not empty. Correct. Computed for the same rings: the upper level is not empty.
* **D35.** In (1) take C = A_i, which has γ(A_i) = γ_min because it is selected, and R <= 1. Correct.
* **D37.** Zero sources would give 0, which is in E ∪ O, not in M. So "positive" is needed, and with it the
  converse is exact (computed, see D8).
* **D10.** See E5. True. The cited facts were checked: at n = 4 the only block words are 0101 and 1010 (computed),
  and Lemma 3.32 needs n >= 6.
* **D12.** "(whether or not 4 divides n)" agrees with the proof: it uses no divisibility.

## Part 3: what the paper says about itself

I compared each sentence of "Status of the proofs" and of the statement on the use of AI with
`VERIFICATION_paper.md`, `VERIFICATION_ring_size.md`, `VERIFICATION_43_142.md`, `VERIFICATION_94_26.md`,
`reader_checks/README.md` and the git log. Findings: E1 to E4. The other sentences agree with the records:

* The dates 13/14, 14, 17, 18 and 20 November match commits 1e256cd, 78ba600, c5dd793, 67287d7, f57f2a0, bdf477b,
  9141d67 and 29d94f7.
* "The verification of the second pair read the computed tables of the proof documents before it wrote its tests,
  and says so" agrees with `VERIFICATION_94_26.md`, Section 1.
* "one false sentence without consequence in a lemma and one step that lacked a citation" corresponds to C1 and C2.
* The reader's ranges, and "recomputed the conclusions of the theorems", agree with `reader_checks/README.md`.
* "Code and data": tag v0.4 contains `paper/`, `proofs_43_142/` and `proofs_94_26/`.

I could not check the DOI 10.5281/zenodo.24482170 (no network access to Zenodo).

## Part 5: the findings that were not applied

* **D22** (ρ the reflection and ρ(ε) the rate). Each use is explicit: "the reflection ρ" in Sections 2.1 and 3.3
  and in the proof of Lemma 3.17; ρ(ε) in the introduction, Section 2.3 and Proposition 2.1. No sentence can be
  misread. Not applying it is sound, though the reason given is not (E10).
* **D34** (g and G_184, G_226). Different cases of the letter, in one proof; no sentence is ambiguous. Sound.
* **D36.** No correction was proposed, and I found no ambiguous sentence in Section 3.3 or Appendix A in the places I
  read (Lemmas 3.29 to 3.32, Theorem 3.43). Sound.
* **D38** (j as exponent and as cell; e as exponent next to e_a). In the proof of Proposition 5.9, "the kernels of
  (1 + Σ)^j stop growing at j = 2^e" and "e_{a+2^{e+1}}" can each be parsed in only one way. The D7 sentence adds no
  new clash. Sound.
* **D18 in part.** Lemma B.6 stays in Appendix B and points into the proof of Theorem 5.7(a). That passage begins
  "Let n >= 4 be even", uses only Lemmas 5.3, 5.4(c), 5.5 and 2.3, and is now complete (the clause on χ). So the
  lemma is proved for its range, and nothing is misread, provided the reader follows the pointer. The decision is
  sound; the reason given in the header is inexact (E9).

## What I did not check

* The literature, and whether the records of `literature_*.md` are right. For D3, D4, D20 and D44 I checked only the
  record lines the new text relies on (`literature_ring_size.md` l. 20-28 and 240-246; `VERIFICATION_ring_size.md`
  l. 274-279 and 382-383; `PROOF_26.md` l. 337; `PROOF_94_converse.md` l. 385; the section headings of
  `literature_addendum.md`). I did not compare the note field of `refs.bib` for Freidlin and Wentzell with any list
  of references.
* The text that the diff does not touch, except the context needed to read the hunks: the abstract, the
  introduction, Sections 2, 4 and 5, Section 3.2 from Theorem 3.20 to Corollary 3.27, Section 3.3 except the
  statements of Lemmas 3.33 to 3.37, Appendix A up to the proof of Lemma 3.32, Appendix B, the statement on the use
  of AI and "Code and data". The statements of the paper were not verified again.
* The build: no TeX here. I only extracted the text of the committed PDF: 32 pages, 18 of the new phrases found, and
  the cross-references Section 2.4, Lemma 3.25, Lemma 3.23(c), Corollaries 3.21 and 3.27, Remark 3.44 and Lemma 3.24
  resolve as intended; no "??". The figures were not looked at.
* No script of the repository was opened or run (`make_numbers.py`, `make_figures.py`, `test_paper.py`, `build.sh`,
  `verify_paper/`). The claim "test_paper.py: 12 passed" is unchecked. Of `numbers.tex` I read only the macros
  quoted above.
* The changes the pass made in `paper/TRACE.md` (D46, the rows of Part A) and in `paper/REFEREE_NOTES.md` (update 2),
  beyond the lines quoted. The other sections of `README.md`, `CITATION.cff` and `.zenodo.json`. Commit 20cf1fd
  (literature addendum of 23 November).
* Computation proves nothing beyond the rings computed. The ranges are given in Part 2. The engine counts the cycles
  of rule 154 as 510, 1688 and 5818 at n = 15, 17 and 19, which agrees with T03 of `VERIFICATION_paper.md`.
  Mutations (appendix): four wrong inputs were all detected. A first choice of mutation, rule 154 in place of rule 26
  for D8, was not a mutation: the two rules differ only on 111, which no domain state contains. It was replaced by
  rule 90.

## Appendix: code and output

The repository may receive only this file, so the code is given here. It is written from the definitions of the
paper and shares nothing with the scripts of the repository. Run on the author's laptop, one process: 21 s for the
checks and 12 s for the mutations. To run it (macOS):

```
python3 -c "import re; s = open('VERIFICATION_corrections.md').read(); b = re.findall(r'~~~python\n(.*?)~~~', s, re.S); open('/tmp/check_corrections.py', 'w').write(b[0]); open('/tmp/mutations.py', 'w').write(b[1])"
cd /tmp && python3 check_corrections.py && python3 mutations.py
```

(numpy is needed.)

~~~python
"""Own checks of the sentences added for D7, D8, D9 (and a few others) in paper/ring_size_paper.tex.
Written from the definitions of the paper; no script of the repository is used.  Cell i = bit i of an integer.
(F x)_i = f(x_{i-1}, x_i, x_{i+1}),  f(a,b,c) = bit (4a+2b+c) of the rule number;  (sigma x)_i = x_{i-1}."""
import sys, itertools
import numpy as np

def bit(x, i, n): return (x >> (i % n)) & 1
def F_int(x, n, rule):
    y = 0
    for i in range(n):
        a, b, c = bit(x, i-1, n), bit(x, i, n), bit(x, i+1, n)
        if (rule >> (4*a+2*b+c)) & 1: y |= 1 << i
    return y
def F_table(n, rule):
    s = np.arange(1 << n, dtype=np.int64); full = (1 << n) - 1
    left = ((s << 1) | (s >> (n-1))) & full      # bit i = x_{i-1}
    right = ((s >> 1) | (s << (n-1))) & full     # bit i = x_{i+1}
    out = np.zeros_like(s)
    for a, b, c in itertools.product((0, 1), repeat=3):
        if (rule >> (4*a+2*b+c)) & 1:
            ma = left if a else (~left & full); mb = s if b else (~s & full); mc = right if c else (~right & full)
            out |= ma & mb & mc
    return out
def sigma(x, n, k=1):
    k %= n; full = (1 << n) - 1
    return ((x << k) | (x >> (n-k))) & full
def cycles_of(T):
    """cycle id for every state (id of the cycle its orbit ends on) and the set of periodic states"""
    N = len(T)
    # periodic states = image of T^N; compute T^(2^k) by repeated squaring until 2^k >= N
    P = T.copy(); k = 1
    while k < N: P = P[P]; k *= 2
    per = np.zeros(N, bool); per[np.unique(P)] = True
    cid = -np.ones(N, np.int64); c = 0
    for s in np.nonzero(per)[0]:
        if cid[s] >= 0: continue
        x = s
        while cid[x] < 0: cid[x] = c; x = T[x]
        c += 1
    endon = cid[P]                              # P maps every state onto a periodic state of its own orbit
    return per, cid, endon, c

fails = []
def check(cond, msg):
    if not cond: fails.append(msg)

# ------------------------------------------------------------------ D9: rule 94, Lemma 3.32 (a), (b), (c)
def occ(x, n): return {i for i in range(n) if bit(x, i-1, n) == 1 and bit(x, i, n) == 0 and bit(x, i+1, n) == 1}
def fz(x, n): return {(c+d) % n for c in occ(x, n) for d in (-1, 0, 1)}
d9_cases = 0
for n in range(6, 301, 3):
    base = sum(1 << i for i in range(n) if i % 3 != 0)      # (011)^(n/3) with 0 at cells 0 mod 3
    for ph in range(3):
        x = sigma(base, n, ph); Ox = occ(x, n)
        check(F_int(x, n, 94) == x, f"D9 n={n}: phase not fixed")
        for j in range(n):
            y = x ^ (1 << j); Oy = occ(y, n)
            if bit(x, j, n) == 0: cen = j; I = {(j-1) % n, j, (j+1) % n}                       # case (a)
            elif bit(x, j-1, n) == 0: cen = (j-1) % n; I = {(cen-1) % n, cen, (cen+1) % n}      # case (b), p = j-1
            else: cen = (j+1) % n; I = {(cen-1) % n, cen, (cen+1) % n}                          # case (c), mirror
            # only centre of x among {j-1, j, j+1} is cen
            check(Ox & {(j-1) % n, j, (j+1) % n} == {cen}, f"D9 n={n} j={j}: centres near j")
            # (O2): flipping j removes only centres in {j-1,j,j+1}
            check((Ox - Oy) <= {(j-1) % n, j, (j+1) % n}, f"D9 n={n} j={j}: O2")
            kept = Ox - {cen}
            check(kept <= Oy, f"D9 n={n} j={j}: occurrences with centre != cen do not survive")
            cover = {(c+d) % n for c in kept for d in (-1, 0, 1)}
            check(set(range(n)) - I <= cover, f"D9 n={n} j={j}: a cell outside I not covered by surviving occurrences")
            check(set(range(n)) - I <= fz(y, n), f"D9 n={n} j={j}: cell outside I not frozen in y")
            z = y
            for t in range(4):
                for i in set(range(n)) - I: check(bit(z, i, n) == bit(y, i, n), f"D9 n={n} j={j}: outside I changes")
                z = F_int(z, n, 94)
            z = y
            for _ in range(3): z = F_int(z, n, 94)
            check(z == x, f"D9 n={n} j={j}: F^3 y != x")
            d9_cases += 1
# (O2) on all states, n = 3..12
for n in range(3, 13):
    for x in range(1 << n):
        Ox = occ(x, n)
        for j in range(n):
            check((Ox - occ(x ^ (1 << j), n)) <= {(j-1) % n, j, (j+1) % n}, f"O2 n={n} x={x} j={j}")
print("D9: crystal flips checked:", d9_cases, "(n = 6..300, 3 | n, all phases and cells); O2 on all states n = 3..12")

# ------------------------------------------------------------------ rule 26 helpers
def ones(x, n): return [i for i in range(n) if bit(x, i, n)]
def in_EO(x, n):
    o = ones(x, n); return len({i % 2 for i in o}) <= 1
def chi(x, n):
    o = ones(x, n)
    if len(o) < 2: return 0
    return sum(1 for k in range(len(o)) if (o[k] - o[k-1]) % 2 == 1)   # n even: parity of a difference is defined
def sources(x, n):
    o = ones(x, n)
    return [o[k] for k in range(len(o)) if (o[k] - o[k-1]) % 2 == 1]
def is_domain(x, n):
    if in_EO(x, n): return False
    s = sources(x, n)
    return all(((s[(k+1) % len(s)] - s[k]) % n) >= 3 for k in range(len(s)))
def domain_by_construction(n):
    """positive even number of sources of alternating parity at distances >= 3, free cells arbitrary"""
    out = set()
    for r in range(2, n+1, 2):
        for S in itertools.combinations(range(n), r):
            d = [(S[(k+1) % r] - S[k]) % n for k in range(r)]
            if any(dd < 3 or dd % 2 == 0 for dd in d): continue      # alternating parity <=> odd distances (n even)
            free = [S[k] + 2*t for k in range(r) for t in range(1, (d[k]-1)//2 + 1)]
            for bits_ in itertools.product((0, 1), repeat=len(free)):
                x = sum(1 << s for s in S) + sum(1 << (f % n) for f, b in zip(free, bits_) if b)
                out.add(x)
    return out

# ------------------------------------------------------------------ D8 (and D18): rule 26, Lemma 5.4(c), Theorem 5.7(a) Case 2
for n in range(4, 17, 2):
    T = F_table(n, 26); per, cid, endon, m = cycles_of(T)
    D = {x for x in range(1 << n) if is_domain(x, n)}
    check(D == domain_by_construction(n), f"D8 n={n}: definition and construction disagree")
    check({sigma(x, n) for x in D} == D, f"D8 n={n}: not rotation invariant")
    img = {int(T[x]) for x in D}
    check(img == D, f"D8 n={n}: F does not map D onto D")
    check(all(per[x] for x in D), f"D8 n={n}: a domain state is not periodic")
    for x in D:   # the cycle of a domain state consists of domain states
        z = int(T[x])
        while z != x:
            if z not in D: check(False, f"D8 n={n}: cycle of {x} leaves D"); break
            z = int(T[z])
        U = sigma(int(T[x]), n)
        check(sorted(sources(U, n)) == sorted(sources(x, n)), f"D8 n={n}: U changes the sources")
        # D18: flipping a one on a free cell keeps sources and chi, and gives a domain state
        s = set(sources(x, n))
        for j in ones(x, n):
            if j in s: continue
            y = x ^ (1 << j)
            check(y in D and set(sources(y, n)) == s and chi(y, n) == chi(x, n), f"D18 n={n}: free-cell flip")
    print(f"D8/D18 n={n}: {len(D)} domain states, m={m}")

# ------------------------------------------------------------------ D7: rule 26, proof of Proposition 5.9
def is_pow2(k): return k & (k-1) == 0
for n in [k for k in range(6, 23, 2) if not is_pow2(k)]:
    h = n // 2; e = 0; q = h
    while q % 2 == 0: q //= 2; e += 1
    check(n == 2**(e+1) * q and q >= 3, f"D7 n={n}: decomposition")
    def emb(v, par): return sum(1 << (2*k + par) for k in range(h) if (v >> k) & 1)
    # F^2 = Sigma^{-1}(1+Sigma)^2 on E and on O, Sigma = shift by two cells (= sigma^2)
    for par in (0, 1):
        for v in range(1 << h):
            x = emb(v, par)
            F2 = F_int(F_int(x, n, 26), n, 26)
            S = lambda z, k=1: sigma(z, n, 2*k)
            rhs = S(x, -1) ^ S(x, 1)          # Sigma^{-1}(1 + Sigma^2) = Sigma^{-1} + Sigma
            check(F2 == rhs, f"D7 n={n}: F^2 != Sigma^-1 (1+Sigma)^2 on parity class {par}")
    # image of (1+Sigma)^(2^e) on the h-ring  = set of periodic points of 1+Sigma = periodic states of F in E
    def tau(v, k=1): k %= h; return ((v >> k) | (v << (h-k))) & ((1 << h) - 1) if k else v
    def one_plus_S_pow(v, p):   # (1+Sigma)^p v ;  Sigma = cell k -> k+1 on the h-ring
        for _ in range(p): v = v ^ (((v << 1) | (v >> (h-1))) & ((1 << h) - 1))
        return v
    image = {one_plus_S_pow(v, 2**e) for v in range(1 << h)}
    A = [one_plus_S_pow(v, 1) for v in range(1 << h)]
    # periodic points of 1+Sigma
    perA = set(range(1 << h))
    for _ in range(h + 2): perA = {A[v] for v in perA}
    check(image == perA, f"D7 n={n}: image != periodic points of 1+Sigma")
    # F-periodicity of every state of the image (embedded in E), by following F
    for v in image:
        x = emb(v, 0); z = F_int(x, n, 26); steps = 1
        while z != x and steps <= 4 * (1 << h):
            z = F_int(z, n, 26); steps += 1
        check(z == x, f"D7 n={n}: a state of the image is not F-periodic")
    # F^2 restricted to the image is a bijection of the image
    F2img = {emb(v, 0) for v in image}
    check({F_int(F_int(x, n, 26), n, 26) for x in F2img} == F2img, f"D7 n={n}: F^2 not a bijection of the image")
    # the states of the proof: two domains, sources a, b, longer domain at a; y = e_a + e_{a+2^{e+1}}, y + e_b
    cnt = 0
    for a in range(n):
        for b in range(n):
            d1 = (b - a) % n; d2 = n - d1
            if d1 % 2 == 0 or d1 < 3 or d2 < 3 or d1 < d2: continue   # domain of a is the longer one
            check(d1 >= 2**(e+1) + 1, f"D7 n={n}: longer domain too short")
            y = (1 << a) | (1 << ((a + 2**(e+1)) % n)); yb = y | (1 << b)
            check(in_EO(y, n), f"D7 n={n}: y not on one parity class")
            for z0 in (y, yb):
                z = F_int(z0, n, 26); steps = 1
                while z != z0 and steps <= 4 * (1 << n): z = F_int(z, n, 26); steps += 1
                check(z == z0, f"D7 n={n}: state of the proof not periodic")
            check(is_domain(yb, n), f"D7 n={n}: y + e_b is not a domain state")
            # cycle of y contained in E u O
            z = F_int(y, n, 26)
            while z != y: check(in_EO(z, n), f"D7 n={n}: cycle of y leaves E u O"); z = F_int(z, n, 26)
            cnt += 1
    print(f"D7 n={n}: e={e}, q={q}, |image|={len(image)}, (a,b) pairs={cnt}")
# Proposition 5.9 itself on small rings: unique closed class K, every domain cycle and every cycle in E u O in K
for n in (6, 10, 12, 14):
    T = F_table(n, 26); per, cid, endon, m = cycles_of(T)
    adj = [set() for _ in range(m)]
    for x in np.nonzero(per)[0]:
        for j in range(n):
            c2 = endon[x ^ (1 << j)]
            if c2 != cid[x]: adj[cid[x]].add(int(c2))
    # strongly connected components (Kosaraju)
    order, seen = [], [False]*m
    for s in range(m):
        if seen[s]: continue
        stack = [(s, iter(adj[s]))]; seen[s] = True
        while stack:
            u, it = stack[-1]
            for w in it:
                if not seen[w]: seen[w] = True; stack.append((w, iter(adj[w]))); break
            else: order.append(u); stack.pop()
    radj = [set() for _ in range(m)]
    for u in range(m):
        for w in adj[u]: radj[w].add(u)
    comp = [-1]*m; c = 0
    for s in reversed(order):
        if comp[s] >= 0: continue
        st = [s]; comp[s] = c
        while st:
            u = st.pop()
            for w in radj[u]:
                if comp[w] < 0: comp[w] = c; st.append(w)
        c += 1
    closed = {comp[u] for u in range(m)} - {comp[u] for u in range(m) for w in adj[u] if comp[w] != comp[u]}
    check(len(closed) == 1, f"P5.9 n={n}: number of closed classes {len(closed)}")
    K = closed.pop()
    D = {x for x in range(1 << n) if is_domain(x, n)}
    for x in np.nonzero(per)[0]:
        x = int(x)
        if x in D or in_EO(x, n): check(comp[cid[x]] == K, f"P5.9 n={n}: domain/EO cycle outside K")
    print(f"P5.9 n={n}: m={m}, one closed class, all domain and E u O cycles in it")

# ------------------------------------------------------------------ small items
vals = [((154 >> c) & 1) for c in range(8)]
check(vals == [0, 1, 0, 1, 1, 0, 0, 1], "D25: listed values are not those of rule 154")
check(all((c & 1) ^ ((c >> 2) & 1) * (1 ^ ((c >> 1) & 1)) == vals[c] for c in range(8)), "D25: c + a(1+b) != f")
n = 4; bw = [x for x in range(16) if fz(x, 4) == set(range(4))]
check(sorted(bw) == [5, 10], "D10: block words at n = 4")
# D31, D33: rules 43, 142, n = 5..14, 4 does not divide n
def walls(x, n): return sum(bit(x, i, n) != bit(x, i+1, n) for i in range(n))
for rule in (43, 142):
    for n in [k for k in range(5, 15) if k % 4]:
        T = F_table(n, rule); per, cid, endon, m = cycles_of(T)
        wm = max(w for w in range(0, n) if w % 2 == 0 and 2*w < n); wp = wm + 2
        Kc = {int(cid[x]) for x in np.nonzero(per)[0] if walls(int(x), n) in (wm, wp)}
        up = {int(cid[x]) for x in np.nonzero(per)[0] if walls(int(x), n) == wp}
        check(len(up) > 0, f"D33 rule {rule} n={n}: upper level empty")
        for x in np.nonzero(per)[0]:
            if int(cid[x]) in Kc:
                for j in range(n): check(int(endon[x ^ (1 << j)]) in Kc, f"D31 rule {rule} n={n}: flip leaves K")
print("small items done")
print("FAILURES:", len(fails))
for f_ in fails[:20]: print("  ", f_)
~~~

Output:

```
D9: crystal flips checked: 45441 (n = 6..300, 3 | n, all phases and cells); O2 on all states n = 3..12
D8/D18 n=4: 0 domain states, m=1
D8/D18 n=6: 12 domain states, m=7
D8/D18 n=8: 64 domain states, m=10
D8/D18 n=10: 240 domain states, m=19
D8/D18 n=12: 816 domain states, m=64
D8/D18 n=14: 2688 domain states, m=76
D8/D18 n=16: 8704 domain states, m=552
D7 n=6: e=0, q=3, |image|=4, (a,b) pairs=6
D7 n=10: e=0, q=5, |image|=16, (a,b) pairs=20
D7 n=12: e=1, q=3, |image|=16, (a,b) pairs=24
D7 n=14: e=0, q=7, |image|=64, (a,b) pairs=42
D7 n=18: e=0, q=9, |image|=256, (a,b) pairs=72
D7 n=20: e=1, q=5, |image|=256, (a,b) pairs=80
D7 n=22: e=0, q=11, |image|=1024, (a,b) pairs=110
P5.9 n=6: m=7, one closed class, all domain and E u O cycles in it
P5.9 n=10: m=19, one closed class, all domain and E u O cycles in it
P5.9 n=12: m=64, one closed class, all domain and E u O cycles in it
P5.9 n=14: m=76, one closed class, all domain and E u O cycles in it
small items done
FAILURES: 0
real 21.24
user 20.96
sys 0.09
```

~~~python
"""Mutations: each must be caught (expected result False for every line)."""
src = open('check_corrections.py').read()
exec(src[:src.index('d9_cases = 0')])                                     # engine, occ, fz
exec(src[src.index('# ------------------------------------------------------------------ rule 26 helpers'):
         src.index('# ------------------------------------------------------------------ D8')])  # rule 26 helpers
res = {}
n = 9; base = sum(1 << i for i in range(n) if i % 3); ok = True
for j in range(n):
    if bit(base, j, n) == 0:
        ok &= occ(base, n) <= occ(base ^ (1 << j), n)
res['M1 D9: occurrence at the removed centre survives'] = ok
n = 10; T = F_table(n, 90); D = {x for x in range(1 << n) if is_domain(x, n)}
res['M2 D8: F(D) = D under rule 90 (rule 154 agrees with 26 off 111, so it is no mutation here)'] = {int(T[x]) for x in D} == D
for n, e in ((12, 1), (20, 1)):
    y = 1 | (1 << (2**e)); z = F_int(y, n, 26); s = 1
    while z != y and s < 4 * (1 << n):
        z = F_int(z, n, 26); s += 1
    res[f'M3 D7 n={n}: e_0 + e_(2^e) periodic'] = (z == y)
n = 10; x = 0b11
res['M4 D7: F^2 = Sigma + Sigma^-1 on a state of M'] = F_int(F_int(x, n, 26), n, 26) == (sigma(x, n, 2) ^ sigma(x, n, -2))
for k, v in res.items():
    print(k, '->', v)
~~~

Output (each line must be False):

```
M1 D9: occurrence at the removed centre survives -> False
M2 D8: F(D) = D under rule 90 (rule 154 agrees with 26 off 111, so it is no mutation here) -> False
M3 D7 n=12: e_0 + e_(2^e) periodic -> False
M3 D7 n=20: e_0 + e_(2^e) periodic -> False
M4 D7: F^2 = Sigma + Sigma^-1 on a state of M -> False
```

Claude
