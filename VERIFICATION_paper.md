# Verification of `paper/ring_size_paper.tex`

Branch `paper-ring-size`, HEAD c926271. Verified on 20 November 2026 by Claude (a session that did not write the
paper, the proof documents or any earlier verification). No existing file was changed. New files: this report and
the folder `verify_paper/` (own code and its output).

> **Handling of the findings.** Added on 20 November 2026 by Claude, the reader outside the sessions (not the
> verifying session). The report below is unchanged. The corrections are in the commit that follows 9141d67; none of
> them was verified after it was made. `paper/TRACE.md`, Part F, lists the sentences added to proofs.
>
> * Applied as proposed, or reworded to the same content: D1, D2, D3, D4, D5, D6, D7, D8, D9, D11, D12, D14, D15, D16,
>   D17, D19, D21, D23, D24 (also in Theorem 5.7(c)), D25, D26, D27, D28, D30, D31, D32, D33, D35, D37, D39, D40, D41,
>   D42, D43, D45, D46.
> * Applied with another wording than proposed:
>   D10 (Remark 3.44 now says that Theorem 3.43 is not proved for n = 3 and 4, that at n = 4 no block word has a long
>   block, and that part (i) needs n >= 6; the computed facts follow as before);
>   D13 ("Status of the proofs" is rewritten as proposed and now also reports this verification and says that the
>   corrections made after it are unverified);
>   D20 (both sentences now say "search excerpts of secondary descriptions" and "provisional"; of the two notes in
>   `refs.bib` only that of Freidlin and Wentzell was changed: the edition was seen in search excerpts of Ellison's
>   list of references; the note of Young agrees with `paper/TRACE.md`, Part B, and stays);
>   D29 (the parenthesis says "the leading power of eps in pi_eps(x) is eps^o(x)", the definition of the order in
>   the note, not "has a positive limit", which the note does not state in these words);
>   D44 ("the dependence on the ring size is not studied"; the pointer to the update of 20 November of the addendum;
>   the sentence on the two versions reworded).
> * Applied in part: D18. The clause on chi is added in the proof of Theorem 5.7(a), and Appendix B now says "with
>   the changes listed in `paper/TRACE.md`". Lemma B.6 is not moved before Theorem 5.7: that would renumber Section
>   5, to whose statements this report, `paper/TRACE.md` and `paper/REFEREE_NOTES.md` refer by number. (Reason
>   corrected on 24 November 2026 after finding E9 of `VERIFICATION_corrections.md`: the two files named here
>   before do not name a numbered statement of Section 5.)
> * Not applied: D22 (a letter with two meanings; no sentence is ambiguous); D34, D38 (a letter with two meanings;
>   no sentence is ambiguous, and renaming symbols in proofs that were just verified was judged the larger risk);
>   D36 (no correction proposed). (Reason for D22 corrected on 24 November 2026 after finding E10 of
>   `VERIFICATION_corrections.md`: the rate rho(eps) occurs in no proof.)
> * The statement on the use of AI and "Status of the proofs" now name this report.
> * The PDF was rebuilt with a full TeX installation and BibTeX: 32 pages. The page numbers below refer to the PDF
>   of 31 pages that was verified.

## 1. Summary

**No false statement was found in any theorem, proposition, lemma or corollary of the paper.**

**Verdict.** The mathematics can be released. Before release six sentences of the text should be corrected (D1 to
D6): they say more than is proved or more than the record supports. Three proofs lack one sentence each (D7 to D9);
the missing steps are true, and I recommend adding them in the same pass. Everything else is wording.

**Basis.** Part 1: I read line by line, as a referee, Lemmas 2.2 to 2.7 and Theorem 2.8, Section 3.1, and Lemma
3.32 and Theorem 3.43(i) with every lemma they use; every step is justified and the smallest ring sizes are covered
(one unwritten step, D9). Each of these statements was tested exhaustively with own code. For Theorems 3.9 to 3.11
the potentials, the selected set and all eight k_v were computed from the definitions, with a minimum spanning
in-tree for every root, for every n = 3..20; for Theorem 3.43(i) for n = 6, 9, ..., 21. They agree with the theorems
and with Theorem 2.8. Part 2: all 69 numbered statements were compared with their sources (by reading
sub-sessions, audited by me); each is the same statement or a change recorded in TRACE.md. I read Section 5 and
Appendix B line by line myself. Table 1 was recounted (correct) and 86 of its 95 computed values were recomputed
(no difference). The smallest n of every statement and the sizes below were computed. Part 3: the paper's account of
itself agrees with the records except D3 to D6, D13, D19, D20. Details: Section 6.

**Findings by severity** (Section 2).

| severity | number | findings |
|---|---|---|
| false statement in a theorem, proposition, lemma or corollary | 0 | |
| false or overstated sentence in the abstract, the introduction, Section 6 or the statement on the use of AI | 6 | D1 to D6 |
| gap in a proof (one unwritten step, true in each case) | 3 | D7 to D9 |
| hypothesis or range not met | 0 statements; 3 inexact sentences about ranges | D10 to D12 |
| unclear | 9 | D13 to D21 |
| cosmetic | 24 | D22 to D45 |
| in the record TRACE.md, not in the paper | 1 | D46 |

**Not checked** (in full in Section 6): the literature (by instruction); Proposition 2.1 (quoted, without proof in
the paper); the proofs of Section 3.2 by me (read by a sub-session; I tested every statement by computation);
anything by computation beyond the ranges of Section 4, in particular powers of two above 16 and 9 cells of Table
1; the build of the PDF and the figures; every script of the repository (none was opened or run).

## 2. Findings

Place: LaTeX label or line of `paper/ring_size_paper.tex` (commit c926271) and page of `paper/ring_size_paper.pdf`.
Origin: "own" = found in my own reading or computation; "sub-session" = reported by one of the six reading
sub-sessions (other instances of Claude, see Section 6) and then checked by me at the lines quoted, unless I say
otherwise.

### 2.1 False statements

None in a theorem, proposition, lemma or corollary. Six sentences of the surrounding text say more than is
true or more than the record supports.

**D1. Introduction, l. 93-95, p. 1. False statement (introduction).** Own; also reported by a sub-session.
"Under rules 43 and 142 the state (0011)^(n/4), and under rule 94 the state (011)^(n/3), has a cycle that no single
flip can leave and that every other cycle can reach by single flips; when it exists it is selected, alone or with
its rotations."
(a) For rule 94 "every other cycle can reach" it is false for every n >= 6 with 3 | n: the other two rotations are fixed points that
no single flip leaves (Theorem 3.43(i), Step 1), so they do not reach it. What is proved is a path to *a* crystal
phase. (b) No range is given. At n = 3 the state 011 exists, every single flip of it leads to the zero state (by hand; T04: F^3(x + e_j) != x
for all three cells; Remark 3.44 says that a flip can leave it), and it is not selected: computed from the definitions, the selected set
at n = 3 is {{0}} and k_v = 0, 1, 1, 1, 1, 1, 1, 1 (T05).
Correction: "For 4 | n, n >= 4, the cycle of (0011)^(n/4) under rules 43 and 142, and for 3 | n, n >= 6, each of the
three rotations of (011)^(n/3) under rule 94, is left by no single flip, and every other cycle reaches it, or one of
the three, by single flips; it is selected, alone or with its rotations."

**D2. Abstract, l. 68-69, p. 1; Introduction, l. 114-118, p. 2; paragraph after Theorem 3.1, l. 330-331, p. 5.
False as worded (overstatement).** Sub-session; checked.
"We determine the selected cycles and k* for four rules, for every ring size from a small bound on" and "In each
case covered by the theorem the set of noise-selected cycles and the eight indices k_v behind k* are determined".
For rule 94 with 3 not dividing n the paper proves that the selected set is the unique closed class K, that K contains
every cycle with an occurrence of 101, and that a cycle outside K is {0} or a cycle of doubled words. Which of the
cycles without 101 lie in K is not determined: Section 6.2 says so itself (l. 1642-1647: "Not determined is the
closed class K ... on its cycles without 101"; for {0} not determined by a proof when 8 | n, n >= 16). By computation
the answer varies with n (T09: 0 of 5 cycles of doubled words in K at n = 10, 7 of 9 at n = 14, 10 of 45 at n = 20).
The introduction's own description ("one closed class that contains every cycle with an occurrence of 101") is
accurate; the verb "determine" is not. k* and all eight k_v are determined in every case.
Correction: abstract: "We determine k* and the indices k_v, and describe the selected cycles, for four rules ...";
introduction: "... the eight indices k_v are determined, and the set of noise-selected cycles is described: ...; for
rule 94 with 3 not dividing n up to the cycles without 101 (Section 6.2)". In l. 330-331 name Corollaries 3.21 and
3.27, which carry the selected set and the k_v for rules 43 and 142 (Theorem 3.28 states k* only).

**D3. Sentence after Lemma 3.6, l. 448-449, p. 7. False statement about a source.** Two sub-sessions; checked in
`literature_ring_size.md` l. 243-246.
"it is stated in [Bhattacharjee, Das] and in [Fedoriaka] and, according to its abstract, in [Nobe, Yura 2004], which
was not read." The record says: the abstract speaks of 16 rules that are reversible for infinitely many ring sizes;
the statement on rule 154 at odd size was seen as a search excerpt of Proposition 1 only. Section 6.1 (l. 1549) has
it right ("by its abstract and a search excerpt").
Correction: "and, by a search excerpt of its Proposition 1, in [Nobe, Yura 2004], which was not read".

**D4. Section 6.1, l. 1584-1585, p. 21. False statement about the record.** Sub-session; checked.
"The searches were short; they are listed in the files `literature_ring_size.md` and `literature_addendum.md`."
The searches for rule 26 and for rule 94 with 3 not dividing n are recorded only in `proofs_94_26/PROOF_26.md`
(l. 337 ff.) and `proofs_94_26/PROOF_94_converse.md` (l. 385 ff.), each as "short search, two queries, 17 November
2026", without the wording of the queries. Neither of the two files named lists them (no occurrence of the texts
found by them, Aguiar and Severino, Schuele and Stoop).
Correction: "... of the repository; the two short searches for rule 26 and for rule 94 with 3 not dividing n are
recorded in the two proof documents of `proofs_94_26/`, without the wording of the queries."

**D5. Statement on the use of AI, l. 1657-1659, p. 22. Stronger than the record.** Sub-session; checked in
`VERIFICATION_94_26.md`, Section 1.
"... were each written in one session and then verified by a separate session that had not seen the work". The
verification of rule 94 (3 not dividing n) and rule 26 declares an "independence breach": it read the sections of
the two proof documents that reproduce the session's computed tables before it wrote its own tests. It says how it
limited the effect. The paper does not mention it.
Correction: add "(the verification of the second pair read the computed tables of the proof documents before
writing its tests, and says so in its report)".

**D6. Statement on the use of AI, l. 1664-1666, p. 22. Stronger than the record.** Sub-session; checked in
`reader_checks/README.md`, section "Not covered".
"... read the proof documents and this paper and recomputed the statements on small rings with separate code." The
README says: "Not covered: ... the lemmas of the proofs one by one". What was recomputed are the conclusions of the
theorems (closed classes, selected sets, k_v, healing time).
Correction: "recomputed the conclusions of the theorems on small rings".

### 2.2 Gaps in a proof

Three places where one step is not written. In each the step is true (shown below, and confirmed by computation), so
no statement is affected.

**D7. Proof of Proposition 5.9, l. 2206-2213, p. 31. Gap, closed by one sentence.** Sub-session; confirmed by my
reading.
The text shows that y = e_a + e_(a+2^(e+1)) lies in the image of (1 + Sigma)^(2^e), "which is the set of periodic
points of 1 + Sigma", and concludes "So y and y + e_b are periodic". Needed is periodicity under
F^2 = Sigma^(-1) (1 + Sigma)^2, not under 1 + Sigma. The source has the same wording.
Correction: add "Sigma is invertible and commutes with 1 + Sigma, so F^2 = Sigma^(-1)(1 + Sigma)^2 maps this image
onto itself bijectively; hence every state of it is periodic under F^2, and under F." (T07: Proposition 5.9 holds
at n = 6, 10, 12, 14, 18, 20.)

**D8. Lemma 5.4(c), statement l. 1369-1370, proof l. 1388-1392, p. 18. Gap, closed by one sentence.** Sub-session;
confirmed by my reading.
"hence F = sigma^(-1) U permutes the set of all domain states (it moves every source one cell to the left)" has no
sentence in the proof; the proof shows the statement for U only. It needs that a rotation of a domain state is a
domain state (true: n is even, so a rotation by one cell exchanges the two parity classes and keeps all distances).
The clause is used: l. 1489-1490, Lemma B.4, Lemma B.5 and the proofs of Propositions 5.8 and 5.9 take the cycle of
a domain state to be a domain cycle.
Correction: add to the proof of (c): "The set of domain states is invariant under rotation, so F = sigma^(-1) U
maps it bijectively onto itself; in particular the cycle of a domain state is a domain cycle." (T07: all domain
states, even n = 4..18.)

**D9. Proof of Lemma 3.32, parts (a) and (b), l. 1769-1773 and l. 1777-1780, p. 25. One step left to the reader.**
Sub-session; I had read the passage as complete and agree that the step is not written.
The proof treats the cells j-1, j+1, j-2, j+2 and concludes "So in y = x + e_j every cell outside I = {j-1, j, j+1}
is frozen". For n >= 9 there are further cells. They are covered because x is fully frozen and the only occurrence
that contains j is the one centred at j: every other occurrence survives the flip by (O2), and every cell outside I
lies in one of them. This lemma has no separate verification on record.
Correction: say this in one sentence, or cite Lemma 3.34 with I = {j-1, j, j+1} (its hypotheses hold: the cells
j-3, j-2 carry 01 and j+2, j+3 carry 10; l = 3 <= n - 3 because n >= 6). (T04: Lemma 3.32 for every n = 6..300
with 3 | n, every phase, every cell.)

### 2.3 Hypothesis or range

No theorem, proposition, lemma or corollary is used outside its stated range, and the smallest ring sizes of every
statement are covered by its proof (own reading for Sections 2, 3.1, 3.3, 5 and the appendices; sub-session for
Section 3.2) and by computation (Section 4). Three sentences about ranges are inexact.

**D10. Remark 3.44, l. 1241, p. 17. Unclear / reason not the reason.** Own; a sub-session reported the first half.
"For n = 3 and n = 4 nothing is proved (Lemma 3.31 needs n >= 5, Lemma 3.32 needs n >= 6)."
(a) Lemmas 3.29, 3.30, 3.33, 3.36, 3.37 and Proposition A.1 are stated and proved for n >= 3; what is not proved for
n = 3, 4 is Theorem 3.43. (b) Lemma 3.31 holds at n = 4 as stated (T04: all 14 states that are not fully frozen,
and the one cycle; in case (a) of its proof only j-2, j+2 not in {j-1, j, j+1} is used, true for n >= 4). What fails
at n = 4 is Step 3 of part (ii): there is no block word with a long block, the closed class carries only the codes
010 and 101, and Lemma 3.42 fails (T04, T05).
Correction: "Theorem 3.43 is not proved for n = 3 and n = 4: at n = 3 a single flip leaves the crystal phase, and at
n = 4 no block word has a long block, so the codes 011 and 110 are missing (Step 3 of part (ii))."

**D11. Section 5, l. 1480, p. 20. Unclear (range).** Sub-session; confirmed by computation.
"For k even nothing beyond (a) and (b) is proved." Proposition 5.8 assumes n >= 8. For k = 2 (n = 4), (a) and (b)
are not proved either, and (a) is false there: k_011 = k_110 = 2 (T07; the paper quotes these values three lines
below).
Correction: "For even k >= 4 nothing beyond (a) and (b) is proved; for k = 2 the proposition does not apply."

**D12. Section 3.2, l. 868 against Lemma 3.24, l. 899, p. 12. Unclear (range).** Sub-session; checked.
"From here to Corollary 3.27, n >= 5 and 4 does not divide n" is followed inside that range by Lemma 3.24, "Let
n >= 3". The source says that divisibility by 4 plays no role in this lemma; the paper does not. (T06: the lemma
holds for every n = 3..18, (a) and (b) for n = 3..13.)
Correction: "Let n >= 3 (whether or not 4 divides n)."

### 2.4 Unclear

**D13. "Status of the proofs", l. 146-156, p. 2.** Sub-session; checked against TRACE Part A and
`VERIFICATION_94_26.md`.
(a) What the separate sessions verified are the proof documents, not the text of the paper, which was assembled
later with recorded changes; some statements of the paper are new as statements (Lemma 2.2, Lemma 2.4, Lemma
3.38(b), the last sentence of Lemma B.2, Lemma B.6). (b) Some statements are in neither of the two lists of the
paragraph: Lemmas 2.2 to 2.4; Lemmas 3.29 to 3.31, which come from the document called unverified and which the
later verification re-checked by reading; Lemma 3.38(b), verified inside a lemma for 3 not dividing n and used in
part (i).
Correction: "The proof documents for ... were each verified by a separate session; the text of this paper was
assembled from them afterwards (TRACE.md lists the changes). Lemmas 2.2 to 2.4 and 3.38(b) are stated here for the
first time as lemmas; Lemmas 3.29 to 3.31, used in both parts of Theorem 3.43, were re-read by the verification
of the case 3 not dividing n." After the present verification the paragraph can be rewritten: Sections 2, 3.1 and
part (i) of Theorem 3.43 with its lemmas now have a separate verification (this report).

**D14. Sentence before Lemma 2.2, l. 215-216, p. 3.** Sub-session; checked.
"the following consequence of the definition is all that is needed to evaluate them." Theorem 3.9(f) (bounds for
101 through F(e_0), lower bound k_v >= 1), Step 6 of Theorem 3.43(i) (codes 111 and 000 in Fy and F^2 y) and the
proof of Proposition 5.8 use equation (1) directly, correctly; Lemma 2.2 does not give these bounds.
Correction: "the following consequences of the definition are used throughout; where they do not suffice, (1) is
used directly."

**D15. l. 136, p. 2, and l. 257-258, p. 4.** Two sub-sessions; checked.
"Theorem 2.8 restates results of these authors" and "It restates known results" are said of the whole theorem. The
attribution paragraph (l. 310-318) limits this to Lemmas 2.6, 2.7 and the first sentence, and says that gamma_min =
m - 1 was not found in the sources read.
Correction: "the first sentence of Theorem 2.8 restates ..." at both places.

**D16. Section 6.2, l. 1633-1638, p. 22.** Sub-session; checked.
"Three things depend on them: ... and all odd n, which the proofs do not treat." Nothing in the paper shows that odd
n depends on the periodic states that contain 111; the reason given for leaving out odd n is another one (l. 1511:
parity of a cell is not defined).
Correction: "Two things depend on them: ... . Odd n is not treated."

**D17. Section 4 and Table 2, row "154, n even", l. 1256-1263, 1282-1286, p. 17-18; abstract l. 77-78, p. 1.**
Sub-session; checked.
For rule 154 the quantity of column (1) is a property with two values (ones on both parity classes or not). The
"number" that "drops by 1" in column (3) is a different thing, the number of ones on the parity class with fewer
ones, a count on one state that is not constant on a cycle (mu(C) is a minimum over the cycle) and that is used only
for n = 2^k. The caption names an exception for rule 94 only; the abstract says "one-flip moves that change the
quantity by a fixed amount".
Correction: add rule 154 to the caption ("for rule 154 the moves lower the number of ones on one parity class,
which is not the conserved quantity"), and in the abstract write "one-flip moves that change it in a controlled
way".

**D18. Lemma B.6, l. 2169-2175, p. 30, and l. 2050-2051, p. 29.** Sub-session; checked.
A lemma for every even n >= 4 is proved by pointing into the proof of a theorem headed "Let n = 2^k >= 4". The
passage pointed to (l. 1434-1446) does begin "Let n >= 4 be even" and uses only Lemmas 5.3, 5.4(c), 5.5 and 2.3, so
the lemma is proved for the range it claims. In Case 2 of that passage it is not said that the flips of free cells
leave chi unchanged (needed for "Case 1 applies to its cycle" with the same chi; true because the sources and
their parities do not change). The sentence "Its statements and proofs are those of the document PROOF_26.md"
(l. 2050) is not exact for Lemmas B.2 and B.6 (TRACE Part C records the changes).
Correction: state Lemma B.6 before Theorem 5.7 with that passage as its proof and cite it in part (a); add the
clause on chi; write "are those of ..., with the changes listed in TRACE.md".

**D19. Statement on the use of AI, l. 1672-1676, p. 22.** Sub-session; checked against the header of TRACE.md.
The list of what the later session added after the reader had read the paper (Appendix B, classes 60 and 90, the
report on Zhu and Richard, entries of the list of references) omits the new wording of the abstract, of "Status of
the proofs" and of this statement, which the TRACE header names.
Correction: add them.

**D20. Attribution, l. 310-317, p. 5; Section 6.1, l. 1533-1534, p. 21; notes in `refs.bib`.** Sub-session; I
checked `literature_ring_size.md` l. 23-26 and the notes of `refs.bib`, not the other records.
"the correspondence rests on Ellison's text, an abstract and secondary descriptions": the record calls the
secondary descriptions search fragments and marks the attribution provisional; "Proposition 1" of Noldeke and
Samuelson rests on those fragments. Notes of `refs.bib`: Freidlin and Wentzell "in the edition named in his list of
references", although the pages of Ellison with the list of references are not among those read; Young "cited
after Newton (2018) and Ellison (2000)". I did not check these two against the reading notes.
Correction: "search excerpts of secondary descriptions; the attribution is provisional"; make the two notes say
what was seen.

**D21. Section 6.1, l. 1568-1569, p. 21.** Sub-session; checked.
"rule 184 has no block 00 or no block 11 after floor((n-2)/2) steps; this is the healing time of Proposition 3.22."
Proposition 3.22 has two healing times, 1 and n/2 - 1; the bound is the larger one.
Correction: "this is the larger of the two healing times".

### 2.5 Cosmetic

| no. | place (label, line, page) | what | proposed correction | origin |
|---|---|---|---|---|
| D22 | Section 2.1, l. 165, and Section 2.3, l. 205, 212, p. 2-3 | rho is the reflection and the rate rho(eps) | another letter for one of them | sub-session |
| D23 | l. 184 against Lemma 2.7 (l. 281), Theorem 3.10 (l. 557), Theorem 5.7 (l. 1429), p. 3-19 | "The cycles are C_1, ..., C_m", and C_1 is later a particular cycle | drop the enumeration at l. 184 or rename | sub-session |
| D24 | Theorem 3.9(d) and proof, l. 492, 516, p. 7 | "{0} is the only closed class": a closed class is a set of cycles, so {{0}}, as in (e) | "{{0}}" | sub-session |
| D25 | Lemma 3.2, proof, l. 374-375, p. 5 | lists the eight values and stops | add "; these are the values of f" | sub-session |
| D26 | Lemma 3.4(b), proof, l. 398-400, p. 6 | "it has degree q - 1 >= 2 and therefore has an irreducible factor different from z + 1": what gives it is that the factor is not constant and not divisible by z + 1 | "it is not constant, so it has an irreducible factor, which is not z + 1" | own |
| D27 | Lemma 2.5, proof, l. 265, p. 4 | "N has no out-edge, so there is no directed circuit" is short | add "(a circuit would consist of cycles that never reach N)" | own |
| D28 | Lemma 2.4, proof, l. 252-253, p. 4 | one verb governs an equation and three objects | two sentences | sub-session |
| D29 | Proposition 2.1, l. 210, p. 3 | "of exact order" is not defined | "(pi_eps(x) / eps^o(x) has a positive limit)" | sub-session |
| D30 | Theorem 3.20, proof of (3), l. 807-808, p. 11 | ends with "a contradiction"; the closing sentence of the source is dropped | add "Hence {X} is the only closed class (one exists, Section 2.4)" | sub-session |
| D31 | Lemma 3.23(b), (c), l. 877-879, 885-888, p. 12 | passes from flips to edges of G1 without citing Lemma 2.3 | cite Lemma 2.3 | sub-session |
| D32 | Theorem 3.26, Step 2, l. 966-968, p. 13 | "Applying the complement" uses a fact stated only inside the proof of Lemma 3.25 | state it once (for example as part (c) of Lemma 3.14) and cite it | sub-session |
| D33 | Corollary 3.27, proof, l. 986-988, p. 14 | assumes that the upper level is not empty | name z+ of Theorem 3.26, or Lemma 3.23(c) | sub-session |
| D34 | Lemma 3.17, l. 716-719, p. 10 | the number g shares its letter with g_184, g_226 | another letter | sub-session |
| D35 | Theorem 3.43(i), Step 6, l. 1204-1206, p. 16 | "k_v <= gamma(A_i) + 1 - gamma_min = 1" without reference | "by (1), since A_i is selected" | sub-session |
| D36 | Section 3.3 and Appendix A | v is a code (k_v) and the half word of a doubled word; q, a, b have several meanings | none needed; no sentence is ambiguous | sub-session |
| D37 | Definition 5.1, l. 1325, p. 17 | "an even number of sources" includes zero | "a positive even number" | sub-session |
| D38 | Section 5 and Appendix B, l. 1416, 1419, 1496, 2206 | exponent j although j is a cell; e is an exponent and e_a a state in one formula | other letters | sub-session |
| D39 | Table 1, caption, l. 339-345, p. 5 | "give a value" counts one bound (">=1") and one pair ("1/2"); "--" is glossed "no statement" although Proposition 5.9 covers rule 26 at n = 6, 10, 12, 14, 18, 20, 22 without fixing k* | "have an entry"; "no statement that gives a value or a bound" | sub-session; counts confirmed by T08 |
| D40 | Introduction, l. 103-105, p. 1 | "computed ... (data file mechanisms.csv)" without the exception for rule 154 at n = 22 that the caption of Table 1 names | add the exception | two sub-sessions |
| D41 | Section 6.2, l. 1614-1615, p. 22 | "the complement of the mirror image of rule 154" is true (255 - 210 = 45, T09) but means the negated output, while l. 333 uses "complementation" for the equivalence of rules | "the mirror image of rule 154 with the output negated" | sub-session |
| D42 | Abstract, l. 67, p. 1 | "records how far the selected cycles are from containing all eight": k_v is a minimum over all cycles | "vanishes iff they contain all of them" (already there) and drop "records how far" | sub-session |
| D43 | Section 6.2, l. 1633, and Table 2, row 26 | "The periodic states that contain 111 are not described": not described are the states whose cycle contains 111 | wording of l. 1488 | sub-session |
| D44 | Section 6.1, l. 1537-1540, 1557-1558, 1599 | "the ring size is not varied" (the record has attractors up to L = 17); the pointer to Section A1 of the addendum should go to its update of 20 November; "Two versions are named in this subsection" | reword | sub-session; not checked by me against the records |
| D45 | Section 5, l. 1500-1501, p. 20 | "at n = 22 the values of chi ... are 6 and 10": the earlier verification recomputed only one of them; l. 1644 has such a remark for rule 94 | add the remark | sub-session; not checked by me |

### 2.6 The record (`paper/TRACE.md`), not the paper

**D46.** Part A keeps only the last sub-row of the trace files for Lemma 3.38, Theorem 3.43 and Theorem 5.7. The row
of Theorem 3.43 names as source only Corollary 1 of the converse document and as verdict "Corollary 1: correct"; the
rows of `trace/trace_94.md` for part (i) ("No independent verification of the proof is recorded") are missing, so
Part A can be read as if the whole theorem had been verified separately. The paper itself says the right thing. The
row of Theorem 5.7 gives the source of part (d) only and a verdict "as (b)" without such a row. The rows of
Theorems 3.9 and 3.10 still say that a reference to Proposition 2.1 was added, where the text cites Lemma 2.2. The
row of Lemma B.2 does not record the added citation of Lemma 5.6. The header says "five entries of the list of
references", Part C item 19 says six. (Own for the row of Theorem 3.43, seen when the list for Part 1 was made;
sub-sessions for the rest.)
Correction: copy the missing rows from `trace/`, update the four others.

### 2.7 Observations that are not findings

* Theorem 3.43(i) states no value of gamma_min. Computed: gamma(A_i) = m + 1 at n = 6, 9, 12, 15, 18, 21 (T05), and
  every other cycle has gamma >= m + 2 (T11).
* For rule 94 at n = 3 the selected set is {{0}}, k* = 1; at n = 4 everything in Remark 3.44 is confirmed (T05).
* For rules 43 and 142 at n = 3, below the range of Theorem 3.28, k* = 0 (T06), which is the value of the pattern.
* Lemma 3.41 holds at n = 4 (T04); it is stated for n >= 5.
* The two values that the paper quotes from Zhu and Richard for rule 154 (n = 22 and 24) are the fractions that
  Lemma 3.7 gives, to the eight digits printed, and the fraction stays below 0.01 for n = 13..27 (T09).

## 3. Every numbered statement

"confirmed (read by me)" means: I followed every step of the proof in the paper, checked the hypotheses of every
lemma it cites including the range of n, and followed the smallest ring sizes by hand. The column "computation" gives
the test and the range on which the statement was tested exhaustively with own code; it is a confirmation for that
range only. The last column is the result of Part 2; "same" means same hypotheses, ranges and quantifiers, with the
renamings that TRACE.md records. Pages are those of the committed PDF.

| statement | label | page | proof | computation (own code) | paper against its source |
|---|---|---|---|---|---|
| Proposition 2.1 | `prop:order` | 3 | no proof in the paper (quoted from the note v0.2, Theorem 1); not refereed | not tested | quotation agrees with the note (statement and definitions of nu_v, rho) |
| Lemma 2.2 | `lem:kzero` | 3 | confirmed (read by me) | T01: all 256 rules, n = 3..12 | new as a numbered statement; rests on the last lines of the proof of Theorem 1 of the note and on the corollaries of the proof documents; the proof in the paper is complete on its own |
| Lemma 2.3 | `lem:edge` | 3 | confirmed (read by me) | T01: all 256 rules, n = 3..12 | same as PROOF_154 Lemma 0; last sentence added (recorded in TRACE), proved in the paper |
| Lemma 2.4 | `lem:sym` | 4 | confirmed (read by me) | T01: all 256 rules, n = 3..12 | new as a numbered statement (two sentences of the report, Section 4); the proof in the paper is complete on its own |
| Lemma 2.5 | `lem:reroot` | 4 | confirmed (read by me) | T01: 48,080 random in-trees on the cycle sets, n = 3..12 | same |
| Lemma 2.6 | `lem:closure` | 4 | confirmed (read by me) | T01: all 256 rules, n = 3..12 | same |
| Lemma 2.7 | `lem:inclosed` | 4 | confirmed (read by me) | T01: all 256 rules, n = 3..12 | same, with the corrected wording of the earlier finding B4 (recorded) |
| Theorem 2.8 | `thm:A` | 4 | confirmed (read by me) | T01: all 256 rules, n = 3..12; T03, T05, T06, T07 on every system computed | same; third sentence of the source moved after the proof (recorded) |
| Theorem 3.1 | `thm:main` | 5 | summary of Theorems 3.11, 3.28, 3.43; ranges and quantifiers identical to these | T03 (n = 3..20), T06 (n = 4..18), T05 (n = 5..21) | agrees with the three theorems |
| Lemma 3.2 | `154:lem:local` | 5 | confirmed (read by me and by a reading sub-session) | T02: 8 codes; all states, n = 3..22 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.3 | `154:lem:rule90` | 5 | confirmed (read by me and by a reading sub-session) | T02: all states of E u O, even n = 4..22 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.4 | `154:lem:nilpotent` | 6 | confirmed (read by me and by a reading sub-session) | T02: (a) all of E u O for n = 4, 8, 16, 32, e_0 for n = 64..4096; (b) every e_j for even n <= 22, e_0 for even n <= 4096 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.5 | `154:lem:invariant` | 6 | confirmed (read by me and by a reading sub-session) | T02: all states of M, even n = 4..22 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.6 | `154:lem:collisions` | 6 | confirmed (read by me and by a reading sub-session) | T02: all colliding pairs, n = 3..22 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.7 | `154:lem:periodic` | 7 | confirmed (read by me and by a reading sub-session) | T02: all states, even n = 4..22 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.8 | `154:lem:moves` | 7 | confirmed (read by me and by a reading sub-session) | T02: all flips inside M and G1 on the cycles in M, even n = 4..16 | same as PROOF_154 (recorded changes of wording only) |
| Theorem 3.9 | `154:thm:pow2` | 7 | confirmed (read by me and by a reading sub-session) | T03: n = 4, 8, 16, from the definitions, in-tree for every root; T11 | same as PROOF_154 (recorded changes of wording only) |
| Theorem 3.10 | `154:thm:other` | 8 | confirmed (read by me and by a reading sub-session) | T03: every n = 3..20 that is not a power of two; T11 (n <= 18) | same as PROOF_154 (recorded changes of wording only) |
| Theorem 3.11 | `154:thm:main` | 8 | confirmed (read by me and by a reading sub-session) | T03: n = 3..20 | same as PROOF_154 (recorded changes of wording only) |
| Lemma 3.12 | `43:lem:R` | 8 | read by a reading sub-session, every step followed; not re-read by me | T06: 8 codes, both rules | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.13 | `43:lem:wall` | 9 | read by a reading sub-session, every step followed; not re-read by me | T06: all states, n = 3..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.14 | `43:lem:cons` | 9 | read by a reading sub-session, every step followed; not re-read by me | T06: all words and states, n = 3..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.15 | `43:lem:flip` | 9 | read by a reading sub-session, every step followed; not re-read by me | T06: all states and cells, n = 3..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.16 | `43:lem:pairs` | 9 | read by a reading sub-session, every step followed; not re-read by me | T06: all words, n = 3..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.17 | `43:lem:pww` | 10 | read by a reading sub-session, every step followed; not re-read by me | T06: all words, n = 3..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.18 | `43:lem:per` | 10 | read by a reading sub-session, every step followed; not re-read by me | T06: all states, n = 3..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.19 | `43:lem:half` | 11 | read by a reading sub-session, every step followed; not re-read by me | T06: even n = 4..16 | same as PROOF_43_142 (merges and renamings recorded) |
| Theorem 3.20 | `43:thm:crystal` | 11 | read by a reading sub-session, every step followed; not re-read by me | T06: n = 4, 8, 12, 16, from the definitions | same as PROOF_43_142 (merges and renamings recorded) |
| Corollary 3.21 | `43:cor:div` | 11 | read by a reading sub-session, every step followed; not re-read by me | T06: n = 4, 8, 12, 16, in-tree for every root | same as PROOF_43_142 (merges and renamings recorded) |
| Proposition 3.22 | `43:prop:heal` | 11 | read by a reading sub-session, every step followed; not re-read by me | T06: 4 | n, n = 4..64, by simulation | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.23 | `43:lem:levels` | 12 | read by a reading sub-session, every step followed; not re-read by me | T06: n = 5..18, 4 not dividing n | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.24 | `43:lem:slides` | 12 | read by a reading sub-session, every step followed; not re-read by me | T06: first statement n = 3..18; (a), (b) n = 3..13 | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.25 | `43:lem:Z` | 13 | read by a reading sub-session, every step followed; not re-read by me | T06: n = 5..18, 4 not dividing n | same as PROOF_43_142 (merges and renamings recorded) |
| Theorem 3.26 | `43:thm:levels` | 13 | confirmed (proof read by me and by a reading sub-session), given the lemmas it cites | T06: n = 5..18, 4 not dividing n | same as PROOF_43_142 (merges and renamings recorded) |
| Corollary 3.27 | `43:cor:ndiv` | 13 | confirmed (proof read by me and by a reading sub-session), given the lemmas it cites | T06: n = 5..18, 4 not dividing n, in-tree for every root | same as PROOF_43_142 (merges and renamings recorded) |
| Theorem 3.28 | `43:thm:main` | 14 | read by a reading sub-session, every step followed; not re-read by me | T06: n = 4..18 (and n = 19, 20 in T08) | same as PROOF_43_142 (merges and renamings recorded) |
| Lemma 3.29 | `94:lem:freeze` | 14 | confirmed (read by me and by a reading sub-session) | T04: all states and cycles, n = 3..20 | same as PROOF_94 Lemma 1, Corollaries 1a, 1b (merged) |
| Lemma 3.30 | `94:lem:block` | 15 | confirmed (read by me and by a reading sub-session) | T04: all states, n = 3..20 | same as PROOF_94 Lemma 2 |
| Lemma 3.31 | `94:lem:growth` | 15 | confirmed (read by me and by a reading sub-session) | T04: all states and cycles, n = 5..20; the six cases of the proof for n <= 14; holds also at n = 4, fails at n = 3 | same as PROOF_94 Lemma 3, Corollary 3 (merged) |
| Lemma 3.32 | `94:lem:crystal` | 15 | confirmed (read by me and by a reading sub-session); one step left to the reader (D9) | T04: 3 | n, n = 6..300, every phase and cell; fails at n = 3 | same as PROOF_94 Lemma 6; second sentence moved from the proof (recorded) |
| Lemma 3.33 | `94:lem:windows` | 15 | confirmed by a reading sub-session; read by me once, not every case re-derived | T04: all states, n = 3..13 | same as PROOF_94_converse Lemma 7 |
| Lemma 3.34 | `94:lem:cut` | 15 | confirmed (read by me and by a reading sub-session) | T04: all block words, windows and fillings, n = 4..13 | same as PROOF_94_converse Lemma W |
| Lemma 3.35 | `94:lem:live` | 15 | confirmed by a reading sub-session; read by me once, not every case re-derived | T04: all words of width 1..18 | same as PROOF_94_converse Lemma 8 |
| Lemma 3.36 | `94:lem:empty` | 15 | confirmed by a reading sub-session; read by me once, not every case re-derived | T04: all states, n = 3..20 | same as PROOF_94_converse Lemma 9 |
| Lemma 3.37 | `94:lem:refreeze` | 15 | confirmed by a reading sub-session; read by me once, not every case re-derived | T04: all cycles, n = 4..18 | same as PROOF_94_converse Lemma 10 (with the correction of the earlier finding C2) |
| Lemma 3.38 | `94:lem:swap` | 15 | confirmed (read by me and by a reading sub-session) | T04: all block words, n = 5..18 | (a) same as PROOF_94_converse Lemma 11; (b) new as a statement, made from two proofs (recorded); correct for every n >= 5 |
| Lemma 3.39 | `94:lem:merge` | 15 | confirmed (read by me and by a reading sub-session) | T04: all block words, n = 6..18 | same (statement in the form of PROOF_94 Lemma 5, proof of PROOF_94_converse Lemma 12) |
| Lemma 3.40 | `94:lem:split` | 15 | confirmed by a reading sub-session; read by me once, not every case re-derived | T04: all block words, n = 8..18 | same as PROOF_94_converse Lemma 13 |
| Lemma 3.41 | `94:lem:component` | 15 | confirmed (read by me and by a reading sub-session) | T04: n = 5..17, 3 not dividing n; holds also at n = 4 | same as PROOF_94_converse Lemma 14 |
| Lemma 3.42 | `94:lem:000` | 16 | confirmed (read by me and by a reading sub-session) | T04: n = 5..17, 3 not dividing n; fails at n = 4 | same as PROOF_94_converse Lemma 15 |
| Theorem 3.43 | `94:thm:main` | 16 | (i) confirmed (read by me and by a reading sub-session); (ii) confirmed (read by me and by a reading sub-session), given the lemmas it cites | T05, from the definitions, in-tree for every root: (i) n = 6, 9, 12, 15, 18, 21; (ii) every n = 5..20 with 3 not dividing n; T11 | (i) same as PROOF_94 Theorem 1, Corollaries 1, 2 (Step 3 uses Lemma 3.38(b), recorded); (ii) same as PROOF_94_converse Theorem 2, Corollary 1 |
| Remark 3.44 | `94:rem:small` | 17 | not a proof; wording: D10 | T05: n = 3 and n = 4, all values quoted | values agree with the source; k* = 1 at n = 4 added at assembly (recorded) |
| Definition 5.1 | `26:def` | 17 | definition; the claims inside it checked (sub-session by hand, T07 by computation) | T07: even n = 4..18 | same as PROOF_26 section 1 (two names added, recorded) |
| Lemma 5.2 | `26:lem:frame` | 18 | confirmed (read by me and by a reading sub-session) | T07: all states, n = 3..18 | same as PROOF_26 Lemma 1 (stated for fewer n than the source) |
| Lemma 5.3 | `26:lem:chi` | 18 | confirmed (read by me and by a reading sub-session) | T07: all states, even n = 4..18 | same as PROOF_26 Lemma 2 (one sentence moved in, recorded) |
| Lemma 5.4 | `26:lem:domain` | 18 | confirmed (read by me and by a reading sub-session); one clause of (c) without a sentence in the proof (D8) | T07: all states, even n = 4..18 | same as PROOF_26 Lemma 3 in its corrected form |
| Lemma 5.5 | `26:lem:singleton` | 19 | confirmed (read by me and by a reading sub-session) | T07: all states, even n = 4..18 | same as PROOF_26 Lemma 5 |
| Lemma 5.6 | `26:lem:parity` | 19 | confirmed (read by me and by a reading sub-session) | T07: all states of E u O, even n = 4..18 | same as PROOF_26 Lemma 6, written out with PROOF_154 Lemmas 2, 3 (recorded) |
| Theorem 5.7 | `26:thm:main` | 19 | confirmed (read by me and by a reading sub-session) | T07: n = 4, 8, 16, from the definitions, in-tree for every root; T11 | same as PROOF_26 Theorems 2, 3(a)-(c) (re-lettered, recorded) |
| Proposition 5.8 | `26:prop:indices` | 20 | confirmed (read by me and by a reading sub-session) | T07: n = 8, 16 ((c): n = 8 only; n = 32 is out of reach) | same as PROOF_26 Theorem 4 |
| Proposition 5.9 | `26:prop:even` | 20 | confirmed (read by me and by a reading sub-session); one step not written (D7) | T07: n = 6, 10, 12, 14, 18, 20, in-tree for every root | same as PROOF_26 Theorem 5, Corollary 5 |
| Proposition A.1 | `94:prop:periodic` | 28 | confirmed by a reading sub-session; read by me once, not every case re-derived | T04: all states, n = 3..18 | same as PROOF_94_converse Theorem 1 |
| Lemma B.1 | `26:lem:ancestors` | 29 | confirmed (read by me and by a reading sub-session) | T07: all states, even n = 4..18 | same as PROOF_26 Lemma 4 |
| Lemma B.2 | `26:lem:kinds` | 29 | confirmed (read by me and by a reading sub-session) | T07: all cycles, even n = 4..18 | same as PROOF_26 Theorem 1 (last sentence added from its proof, recorded; the added citation of Lemma 5.6 is not recorded) |
| Lemma B.3 | `26:lem:carrier` | 29 | confirmed (read by me and by a reading sub-session) | T07: all words over the two blocks, all rotations, n = 3..40 | same as PROOF_26 Lemma 7 |
| Lemma B.4 | `26:lem:codes` | 30 | confirmed (read by me and by a reading sub-session) | T07: all cycles, even n = 4..18 | same as PROOF_26 Lemma 8 |
| Lemma B.5 | `26:lem:domaingamma` | 30 | confirmed (read by me and by a reading sub-session) | T07: n = 8, 16 (all domain cycles) | same as PROOF_26 Theorem 3(d) |
| Lemma B.6 | `26:lem:topar` | 30 | confirmed (read by me and by a reading sub-session); form: D18 | T07: even n = 4..20 | first sentence of PROOF_26 Theorem 2; no proof text of its own |
| Lemma B.7 | `26:lem:oneparity` | 31 | confirmed (read by me and by a reading sub-session) | T07: even n = 4..20 | same as PROOF_26 Lemma 9 |

## 4. Tests

All code is in `verify_paper/`, written from the definitions of Section 2 of the paper and from the statements,
without reading any script of the repository. `python3 verify_paper/run_all.py` runs everything (needs numpy, scipy
and a C compiler `cc`); the outputs are in `verify_paper/out/` (`T??.txt` the summary of each test, `T??_stdout.txt`
every line, `*.csv` the tables, `run_all.txt` the times). Times are from the final run on the author's laptop
(12 cores, at most 2 threads used): wall time, and CPU time including the C program. Total: 911 s wall, 1667 s CPU. Result of the final run: all tests pass.

How the quantities are computed. States are integers (cell i = bit i). F and the codes of every state are tabulated.
Cycles are found by following F. V(C, C') and R(C -> D_v) come from a 0-1 breadth-first search over all 2^n states
from each cycle, with the moves "apply F" (cost 0) and "flip one cell" (cost 1); `vp_core.py` says why this is the
resistance of the paper. gamma(C) is the weight of a minimum spanning in-tree for every root C (Edmonds'
contraction carried out once without a root, which gives all roots); Theorem 2.8 is never used to compute anything.
G1 is the set of pairs with V = 1; closed classes are the strongly connected components without leaving edge.

| test | what it computes | rings | result | wall / CPU (s) |
|---|---|---|---|---|
| T00 engine | (a) the C routines against the numpy reference: F, codes, cycles, V, R(C -> D_v). (b) in-tree weights for every root: C routine against enumeration of all in-trees, and against a per-root Chu-Liu/Edmonds in Python | (a) all 256 rules, n = 3..7; rules 154, 43, 142, 94, 26 at n = 8, 9, 10: 1,295 systems. (b) 1,545 roots in 400 random matrices (m <= 6) by enumeration; 1,908 roots in 60 random matrices (m <= 60) and 7,079 roots in 1,284 systems of (a) per root | 0 differences | 10.2 / 9.7 |
| T01 Section 2 | Lemmas 2.2, 2.3, 2.4, 2.6, 2.7 and Theorem 2.8 on every cycle; Lemma 2.5 on random in-trees (20 per system) | all 256 rules, n = 3..12 (2,560 systems, 79,257 cycles, 48,080 in-trees) | 0 failures | 18.6 / 17.6 |
| T02 rule 154, lemmas | Lemmas 3.2 to 3.7 on every state; all pairs of states with equal image (3.6); 3.4 also with rule 90 alone on large rings; 3.8 with G1 from the matrix V | all states, n = 3..22; 3.4(a): all of E u O at n = 4, 8, 16, 32 and e_0 at n = 64..4096; 3.4(b): every e_j for even n <= 22, and L^n e_0 != 0 for the 2,036 even n <= 4096 that are not powers of two; 3.8: even n = 4..16 (n = 16: 1,036,320 flips, 4,080 cycles in M) | 0 failures. The converse of Lemma 3.6 (every pair of the three kinds collides), which the lemma does not claim, also holds | 5.0 / 6.6 |
| T03 rule 154, theorems | Theorems 3.9, 3.10, 3.11 from the definitions: all cycles, V, gamma for every root, selected set, k_v for the eight codes, G1, closed classes; every item (a) to (f) of Theorem 3.9; the states named in the proof of Theorem 3.10; Theorem 2.8 against the in-trees | n = 3..20 (m = 3, 4, 4, 12, 8, 31, 18, 62, 50, 308, 156, 564, 510, 4081, 1688, 6314, 5818, 41626 cycles). Per-root recheck in Python for m <= 320 (n <= 13) | all as stated: k* = 1 and k_v = 0,1,1,1,1,1,1,1 at n = 4, 8, 16, with gamma({0}) = m - 1, gamma = m elsewhere, min V({0}, C) = 2 and largest G1 distance to {0} equal to the largest mu (2, 4, 8); k* = 0, G1 strongly connected and gamma = m - 1 for every cycle at the 15 other n | 397.0 / 751.0 |
| T04 rule 94, lemmas | Group A (used by Theorem 3.43(i)): Lemmas 3.29, 3.30, 3.31 (existence and the six cases of the proof), 3.32, 3.34, 3.38, 3.39. Group B: Lemmas 3.33, 3.35, 3.36, 3.37, 3.40, 3.41, 3.42, Proposition A.1 | all states n = 3..20 (3.29, 3.30, 3.31, 3.36); proof cases of 3.31 n <= 14; 3.32: every n = 6..300 with 3 dividing n, three phases, every cell; 3.34: n = 4..13, every filling (264,498 states at n = 13); 3.35: all words of width 1..18; 3.33: n = 3..13; A.1: n = 3..18; G1 statements: n = 4..18 | 0 failures inside the stated ranges. Outside: 3.31 holds at n = 4 and fails at n = 3; 3.32 fails at n = 3; 3.41 holds at n = 4; 3.42 fails at n = 4 | 9.9 / 13.2 |
| T05 rule 94, theorem | Theorem 3.43 and Remark 3.44 from the definitions, as T03. (i): closed classes, paths to the phases, selected set, k_v, the words of Step 6. (ii): every clause of the statement | n = 3..21 (m up to 6,927). Per-root recheck for m <= 320 (n <= 14) | (i) n = 6, 9, 12, 15, 18, 21: closed classes exactly the three phases, S = {A_1, A_2, A_3}, k_v = 1,1,1,0,1,0,0,1, k* = 1, gamma(A_i) = m + 1. (ii) every n = 5..20 not divisible by 3: one closed class with all clauses, k* = 0. n = 4: one closed class, the two checkerboards, codes 010 and 101, k* = 1. n = 3: selected set {{0}}, k* = 1, a flip leaves the phase | 170.7 / 308.1 |
| T06 rules 43, 142 | every numbered statement of Section 3.2: Lemmas 3.12 to 3.19 on all states and words; Theorems 3.20, 3.26, Corollaries 3.21, 3.27, Lemmas 3.23 to 3.25, Theorem 3.28 from the definitions; Proposition 3.22 by simulation | all states n = 3..16; from the definitions n = 3..18, both rules; slides search n <= 13; healing time for 4 dividing n, n = 4..64 | 0 failures for n >= the stated bounds; k* = 1 iff 4 divides n for n = 4..18. n = 3 (below the range): k* = 0 for both rules | 3.7 / 6.1 |
| T07 rule 26 | every numbered statement of Section 5 and Appendix B: Lemmas 5.2 to 5.6, B.1, B.2, B.4 on all states; B.3 on all words over the two blocks; Theorem 5.7, Propositions 5.8, 5.9, Lemmas B.5, B.6, B.7 from the definitions; the computed values quoted for n = 4 and n = 16 | all states, even n = 4..18 (5.2: n = 3..18); B.3: n = 3..40 (67,187 rotated words); from the definitions: even n = 4..20 | 0 failures. n = 4: one cycle, k_v = 0,1,1,2,1,1,2,2. n = 8: k* = 1. n = 16: k_111 = 2, k* = 2, 3 cycles with 111, none reachable, 2 through a carrier word. Even n that are not powers of two: k* = 0 at n = 14, 20 and k* > 0 at n = 6, 10, 12, 18 | 24.5 / 46.0 |
| T08 Table 1 | recount of the table; its "theorem" rows against the statements of the theorems; its "computed" rows against own k* | 95 cells; own k* for 86 of them (rule 154 n <= 20; rules 43, 142, 26 n <= 20; rule 94 n <= 21) | counts 95 / 78 / 78 as in the paper; theorem rows 95 of 95 equal; computed rows 86 of 86 equal. Not recomputed: n = 21, 22 for rules 154, 43, 142, 26; n = 22 for rule 94 | 26.6 / 52.5 |
| T09 Section 6 | (1) fraction of states of rule 154 on no cycle, from Lemma 3.7 and directly, against the values quoted from Zhu and Richard; (2) classes 60, 90; (3) rule 45 as the negated mirror image of rule 154 and a bijection for odd n; (4) the lists of n for classes 35, 37, 45, 73, 122, 22; (5) rule 94: is {0} in K, how many cycles of doubled words are in K; (6) the classes of rules 43 and 142 under reflection and complementation | (1) n = 13..27 (directly for n <= 24); (2) n = 4..16; (3) odd n <= 21; (4) n = 8..16; (5) n = 5..20 | all agree with the paper on these ranges: (1) 0.00048828 at n = 22, 0.00045776 at n = 24, largest value 0.0078 at n = 14; (2) k* >= 1 exactly at powers of two, k* = 1 (rule 60) and 2 (rule 90), one cycle; (5) {0} in K exactly at n = 5, 7, 8; 0 of 5, 7 of 9, 10 of 45; (6) {43, 113} and {142, 212}: not equivalent | 46.1 / 83.7 |
| T10 mutations | the tests run again with something wrong: another rule delivered by the engine (26 for 154, 90 for 94, 43 and 142 exchanged, 154 for 26); a wrong list of live words; a wrong definition of domain states; a wrong entry of Table 1; perturbed potentials | short ranges | 10 of 10 mutations caught | 8.4 / 7.9 |
| T11 certificates | the potentials without Edmonds' algorithm: lower bound by the cheapest edge out of every cycle, explicit breadth-first in-trees in the graph of cheapest edges; gives gamma exactly on one component, gamma_min, the selected set and bounds for k_v | rule 154 n = 3..18; rule 94 n = 5..21; rules 43, 142 n = 4..18; rule 26 even n = 4..20: 72 systems | in all 72 systems gamma_min, the selected set and all eight k_v are fixed by the certificate and equal the values of the C routine | 189.9 / 364.8 |

What the tests do not show. A test on rings up to n = N says nothing about n > N; the proofs do. The matrix V and
R(C -> D_v) come from one search routine (C), compared with a numpy version only for n <= 10 (T00). The tests of the
lemmas use the same tabulated map F as the engine; a wrong map would be caught by the local forms (Lemmas 3.2,
3.12, 5.2, and the three-line definition of rule 94 in T04), which are checked against it.

## 5. After reading `paper/REFEREE_NOTES.md`

Read after Sections 1 to 4 and 6 were written (a copy of that state is `verify_paper/own_findings_before_comparison.md`
for the first findings; the numbering D1 to D46 was fixed before the notes were opened). The notes list what was
fixed in two readings (12 and 5 items) and 28 objections R1 to R28 that were not fixed or were handled by a decision
of the author.

### 5.1 Objections that I confirm

* **R5** (Proposition 2.1 is quoted from a note without peer review). Confirmed: it has no proof in the paper, and
  it is used only for the interpretation of k_v; every theorem is a statement about the integers of equation (1).
  I did not test it.
* **R6** (Propositions 5.8, 5.9 need proofs in the paper). Confirmed as handled: Appendix B proves both, and I
  found no error in it. The status line "no gap was found in the source" needs a qualification: two steps are not
  written, in the paper as in the source (D7, D8).
* **R7** (rule 154 and rule 94 with 3 | n have no separate verification). Confirmed for the state of the paper.
  This report is such a verification for Section 3.1, Lemma 3.32 and Theorem 3.43(i): proofs read line by line,
  every statement tested with own code, potentials from the definitions for n <= 20 and n <= 21. Result: correct.
* **R8** (Lemma 2.2, third clause, and Lemma 2.4 are new as statements). Confirmed; the whole of Lemma 2.2 and of
  Lemma 2.4 is new as a numbered statement, and so is Lemma 3.38(b). Their proofs in the paper are complete and
  correct (own reading). Lemmas 2.2 and 2.4 hold on all 256 rules for n = 3..12 (T01), Lemma 3.38(b) on all block
  words for n = 5..18 (T04).
* **R9** (n = 3, 4 for rule 94 and n = 3 for rules 43, 142 are not covered). Confirmed. Computed: rule 94 at n = 3
  has S = {{0}}, k* = 1; at n = 4, k* = 1 with the values of Remark 3.44; rules 43 and 142 at n = 3 have k* = 0.
* **R10** (Section 4 fits rule 154 only loosely). Confirmed; this is D17.
* **R11** (rules 43 and 142 not equivalent, stated without proof). Confirmed that no proof is given; the statement
  is true: the classes under reflection and complementation are {43, 113} and {142, 212} (T09, item 6).
* **R12** (Table 1 only up to n = 22; rule 154 at n = 22 from another file). Confirmed; D40 adds that the
  introduction omits the exception. I did not look at the figures.
* **R13** (the attribution of Theorem 2.8 rests on Ellison's text, an abstract and secondary descriptions).
  Confirmed against the records; D15 and D20 add that two sentences say more than the attribution paragraph and
  the records.
* **R16** (the negatives are provisional). Confirmed; D4 adds that the sentence on where the searches are listed is
  not exact.
* **R18** (Lemma B.6 has no proof text of its own). Confirmed; this is D18. The lemma is proved for the range it
  claims.
* **R19** (the GF(2) algebra stands twice, in Lemma 3.36 and in the proof of Proposition 5.9). Confirmed. The
  passage in the proof of Proposition 5.9 is the place of D7.
* **R20** (the last sentence of Lemma B.2 is not a sentence of the source). Confirmed; it is recorded in TRACE.md
  and it follows from the proof given.
* **R21** (Section 6.2 cites Proposition 1 of the note for classes 60 and 90). Confirmed that the citation is the
  only support. Computed: for rules 60 and 90, k* >= 1 exactly at n = 4, 8, 16 among n = 4..16 (T09). The proof in
  the note was not checked.
* **R22** (the report on Zhu and Richard rests on the record of the outside reader). Confirmed. Computed: the two
  values quoted are what Lemma 3.7 gives (T09).

Of the items "found and fixed": item 7 of the first reading (Theorem 3.10 for odd n now cites the last sentence of
Lemma 2.3) is in the text and is right. Item 3 of the first reading (the sentence on p. 1 about a cycle that no
single flip can leave) was fixed by stating it "for the rules treated"; the sentence that resulted is D1, which is
still not true for rule 94 as worded.

### 5.2 Objections on which I have no judgement

R1 (length) is decided by the author and is not a finding. R2, R3, R4, R25, R26, R27 (density, structure,
typography, layout): I did not read the PDF as page images. R14, R15, R24 (which references are listed, and where
their data come from): decided by the author, or not checked by me. R17 (build with a reduced TeX installation):
not checked; I could not build. R23 (the DOI of version 0.3): not checked. R28: not about the paper.

### 5.3 Findings of this report that the notes do not have

* D1 (the introduction's sentence on the crystal cycles: false for the other two phases of rule 94, and at n = 3),
  D2 ("We determine the selected cycles" against Section 6.2), D3 (Nobe and Yura "according to its abstract"),
  D4 (where the searches are listed), D5 and D6 (two sentences of the statement on the use of AI).
* D7, D8, D9 (three unwritten steps in the proofs of Proposition 5.9, Lemma 5.4(c) and Lemma 3.32).
* D10 (Remark 3.44: the reason given for n = 4 is not the reason; Lemma 3.31 holds at n = 4), D11 ("For k even"),
  D12 (range of Lemma 3.24).
* D13 (what "Status of the proofs" leaves out; R7 and R8 touch it, without the point that the proof documents and
  not the text were verified, and without Lemmas 3.29 to 3.31 and 3.38(b)), D14, D15, D16, D19, D20 (the wording
  beyond R13), D21.
* D22 to D45 (cosmetic), except that D40 is the other side of R12.
* D46 (rows of TRACE.md).
* The observations of Section 2.7 (gamma(A_i) = m + 1 for rule 94 with 3 | n; Lemma 3.41 at n = 4).

The notes have, and this report does not: R2 to R4 and R25 to R27 (form and layout), R15, R23, R24, R28.

## 6. How the work was done, and what was not checked

Order: (1) the paper was read (Sections 1 to 3.1, 3.3, 4, Appendix A) and TRACE.md Part A; (2) own code was written
from the definitions of Section 2 and the statements, and run (T00 to T04 in full, T05 up to n = 19, T06 and T07 on short ranges; the full runs followed and changed nothing); (3) own findings were written down
(`verify_paper/own_findings_before_comparison.md`); (4) the reports of the reading sub-sessions were collected and
audited, Sections 5, 6 and Appendix B were read; (5) T08 to T11 were written, and all tests were run once more in
one pass (`run_all.py`); (6) Sections 1 to 4 of this report were written; (7) `paper/REFEREE_NOTES.md` was read and
Section 5 written.

Independence. No script of the repository (`proofs_*/`, `verify_*/`, `code/`, `reader_checks/`, `paper/*.py`) was
opened or run at any time. Read from those folders: the proof documents (`PROOF_*.md`), which TRACE.md names as the
sources of the paper, and, after my tests were written and run, a few lines of `reader_checks/README.md`. The proof
documents were read by the reading sub-sessions while I wrote my tests; I saw their reports only at step (4).

Sub-sessions. Six other instances of Claude each compared one part of the paper with its sources and read its
proofs (rules 43/142; rule 94; rule 26; rule 154 with Section 2; abstract, introduction, tables, Sections 4 and
6.2; the statements of the paper about itself). They were told to read only, to open no script and not to open
`REFEREE_NOTES.md`. Their findings are marked "sub-session" in Section 2; I checked each at the lines quoted unless
I say otherwise. One of them (rule 94) ran a short check of its own on rings up to n = 12; its code was not kept
and nothing in this report rests on it. Their reports are in `verify_paper/reading/`, unchanged.

Code. `verify_paper/vp_core.py` holds the engine. Its inner loops are C; the C source is a string inside the
Python file and is compiled at run time into the system's temporary directory, so the folder contains text files
only. A pure Python/numpy version of every routine is in the same file and is compared with the C version in T00.
At most 2 threads were used.

Deviations. (a) The sandbox in which I worked cannot write into the repository; the new files were placed there
through its file-saving channel and are not committed (commands in my closing message). (b) The first versions of
T02 and T03 had a loop that did not end in reasonable time (an orbit of rule 90 followed until it repeats; a
per-root Python routine at m = 4081); both were replaced before any result was used.


### What was confirmed, in full

* *Part 1 (statements without a separate verification).* I read line by line, as a referee: Lemmas 2.2 to 2.7 and
  Theorem 2.8; Section 3.1 (Lemmas 3.2 to 3.8, Theorems 3.9 to 3.11); Lemma 3.32 and part (i) of Theorem 3.43 with
  every lemma it uses (3.29, 3.30, 3.31, 3.34, 3.38, 3.39). Every step is justified, the hypotheses of every cited
  lemma are met, and the smallest ring sizes are covered, with the one unwritten step of D9. Each of these
  statements was also tested exhaustively with own code (every state, every cell, every cycle; ranges in Sections 3
  and 4). For Theorems 3.9 to 3.11 the potentials, the selected set and all eight k_v were computed from the
  definitions of Section 2 with a minimum spanning in-tree for every root, for every n = 3..20; for Theorem 3.43(i)
  for n = 6, 9, 12, 15, 18, 21. They agree with the theorems and with Theorem 2.8 in every case.
* *Part 2 (paper against sources).* All 69 numbered statements were compared with the source named in TRACE.md
  (by six reading sub-sessions, audited by me). Every statement is the same statement as its source in hypotheses,
  ranges and quantifiers, or is recorded in TRACE.md as new or changed; no proof step was dropped except the
  closing sentence of D30; every cross-reference points to the statement meant. I read Section 5 and Appendix B
  (written on 20 November) line by line myself: no error, two unwritten steps (D7, D8). Table 1 was recounted (95
  cells, 78 with an entry of a theorem, 78 agree: correct) and 86 of its 95 computed values were recomputed from the
  definitions: no difference. The edges of every range were computed: rule 154 n = 3, 4; rules 43, 142 n = 3..8;
  rule 94 n = 3..8; rule 26 n = 4, 6, 8, 16.
* *Part 3 (what the paper says about itself).* The lists of what was verified by a separate session and what was
  not are correct as far as they go (D13 for what they leave out). How each of the 25 references was seen agrees
  with the records, with the exceptions D3, D4, D20. The statement on the use of AI agrees with the records except
  D5, D6, D19.


### What was not checked, in full

* The literature, by instruction: whether a result is known elsewhere, and whether an attribution is right.
* Proposition 2.1: it is quoted from the note, has no proof in the paper, and was not tested.
* Section 3.2 (rules 43 and 142): the proofs were read line by line by a reading sub-session, not by me, apart from
  the proofs of Theorem 3.26 and Corollary 3.27. I tested every statement of the section by computation (n <= 18).
* Lemmas 3.33, 3.35, 3.36, 3.37, 3.40 and Proposition A.1: read line by line by a reading sub-session; by me once,
  without re-deriving every case of Lemma 3.35. All were tested by computation.
* A computation on small rings confirms a statement for those rings only. Not reached: n = 32 for the theorems on
  powers of two (rules 154 and 26; the largest power of two computed in full is 16); Proposition 5.8(c) beyond
  n = 8; 9 cells of Table 1 (n = 21, 22 for rules 154, 43, 142, 26 and n = 22 for rule 94); the computed values
  of Section 6.2 beyond n = 16 (classes 35 to 122) and n = 20 (rule 94).
* Potentials: every value comes from one C routine (minimum in-tree for all roots). It is validated against
  enumeration of all in-trees and against a per-root Chu-Liu/Edmonds (T00), rechecked per root for m <= 320 (rule
  154: n <= 13; rule 94: n <= 14), and confirmed without Edmonds' algorithm by explicit in-trees and a lower bound
  for 72 systems (T11). For rule 154 at n = 19 and 20 there is no second check.
* The PDF was not rebuilt (no TeX here). Page numbers are from the text of the committed PDF. The figures, and
  whether the committed PDF is the build of the committed source, were not checked.
* No script of the repository was opened or run, before or after my tests (so `make_numbers.py`, `test_paper.py`
  and the scripts of the proof documents are unchecked); `numbers.json` was not opened. Results were compared
  through `paper/table_kstar.tex` and `paper/numbers.tex` only.
* Three items reported by sub-sessions were not re-checked by me against the records: D20 in part, D44, D45.

Claude
