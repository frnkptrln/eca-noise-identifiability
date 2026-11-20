# Referee notes on `ring_size_paper.pdf`

20 November 2026, by the session that assembled the paper.

## How the paper was read

* The LaTeX source of every section was read in full before the first build: Sections 3.1, 3.2, 3.3, 5 and
  Appendix A as delivered by the sub-sessions, with the proofs followed step by step. Re-derived by hand in that
  reading: the local-rule tables of rules 154, 142, 43, 94 and 26 from the rule numbers; Lemmas 3.2 to 3.6 and
  Theorems 3.9, 3.10 (rule 154); the wall map and the four formulas of Lemma 3.18, the explicit states of
  Corollaries 3.21 and 3.27 and of Lemma 3.25 (rules 43, 142); the six cases of Lemma 3.31, both cases of Lemma
  3.32, Step 6 of part (i) and Step 3 of part (ii) of the proof of Theorem 3.43, and the three cases of Lemma 3.42
  (rule 94); Lemmas 5.2 to 5.6 and Theorem 5.7 (rule 26). Read but not re-derived line by line: the proofs of
  Lemma 3.16 (pairs), Lemma 3.17 (converse direction), Lemma 3.24, Lemma 3.35 (live window orbits), Lemma 3.36
  (the count) and Lemmas 3.37 to 3.41. For these the check rests on the verification reports of the repository.
* The built PDF (27 pages) was then read from the first page to the last as page images (rendered at 110 dpi).
  A first attempt to display the pages failed without my noticing at once, and notes written during it were
  discarded; everything below comes from the second pass, in which the pages were on screen.
* After the fixes the changed pages (1, 2, 5, 16, 17, 20, 21, 22, 23) were looked at again as images. Page 3 (three
  words removed from Proposition 2.1) and the two pages with figures (5 and 11) were looked at in the PDF that is
  committed. The final PDF was not read a second time as a whole.

## Found in the reading and fixed

1. p. 20: "have chi = 6and10": a macro containing the word "and" stood in math mode. Reworded.
2. pp. 22-23: the DOIs were missing from the list of references (the bibliography processor used in the sandbox
   dropped `\href` in the note fields and left an empty link). DOIs are now plain text.
3. p. 1: "where such a state exists and no single flip can leave its cycle, that cycle is selected" read as a
   general fact; it is not (Theorem 2.8 needs that the other cycles reach it). Now stated for the rules treated.
4. p. 2: "Every number in the text ... is taken from a data file" was too wide; now "every computed value".
5. p. 5, Table 1: the row of rule 26 named Proposition 5.8 as "Thm."; it now names Section 5, since the cell n = 4
   follows from Theorem 5.7.
6. p. 5: Section 3.1 said "recall the parity classes" although they are defined there for the first time.
7. p. 8, Theorem 3.10, odd n: cited Lemma 3.8(a), which assumes n even; now cites the last sentence of Lemma 2.3.
8. pp. 16-17: Table 2 stood between the two halves of Remark 3.44, before the heading of the section it belongs to;
   it now follows the text of Section 4.
9. p. 22: very loose word spacing in "Code and data" (long file names); set ragged right. An overfull line in the
   statement on the use of AI was removed before the read.
10. p. 21: "the cycles involved are the zero state and the checkerboard cycle" (class 122) was vague; reworded.
11. Proposition 2.1 said "with a > 0" for the rate; the note does not say this and it is not needed; removed.
12. A page with four lines at the end was removed by making the two figures slightly smaller.

## What a referee would object to, and what was not fixed

Length and form.

* R1. 27 pages against the 12 to 16 asked for. The complete proofs take 2.7 (rule 154), 5.1 (rules 43, 142), 3.0
  plus 4.3 (rule 94) and 2.8 (rule 26) pages. The paper can be brought to about 16 pages only by replacing proofs
  with pointers to the repository documents, which the task excludes. Candidates if the author wants a shorter
  version: the proof of Proposition 3.22 (0.3 page), Proposition A.1 (0.3), the paragraph "Computed values and the
  open case" of Section 5 (0.4), Table 2 (0.3), Section 6.1 (0.9).
* R2. Sections 3.2 and Appendix A are dense: long proofs as running text (Lemmas 3.16, 3.17, 3.35), Definition 5.1
  as one paragraph. Displaying the case distinctions would add about two pages.
* R3. Section 3.3 states fourteen lemmas without proof in a row. This is the structure asked for (chain of lemmas
  in the main text, proofs in the appendix).
* R4. The paper avoids amssymb and amsthm (not available in the sandbox): "does not divide" is a slashed bar, Z is
  bold, the end-of-proof mark is a filled square that sometimes stands alone on a line after a list (pp. 24, 26).
  Three underfull boxes remain (caption of Table 1).

Mathematics and its status.

* R5. Proposition 2.1 is quoted from a note that has not been through peer review. It is used only to say what
  k_v means; every theorem is a statement about the integers defined in (1). Not fixable here.
* R6. Proposition 5.8 (the indices k_v of rule 26) and the first half of Proposition 5.9 have no proof in the
  paper; the text points to `proofs_94_26/PROOF_26.md`. A referee will not accept a proposition proved in a
  repository file. Including the proof of 5.8 needs Lemmas 4, 7, 8 and Theorem 3(d) of that file, about one page.
* R7. Who checked what. Rules 43, 142, rule 94 with 3 not dividing n, and rule 26: one independent verification
  each. Rule 154 and rule 94 with 3 | n: the proofs were written and checked inside one verification session, and
  a second reading is recorded only "as reported by the author"; no independent verification report exists for
  Lemma 3.32 and for part (i) of Theorem 3.43 (`VERIFICATION_94_26.md` l. 259 excludes them). Nothing has been
  through peer review. The statement at the end says this; a referee will still count it against the paper.
* R8. Lemma 2.2 (third clause) and Lemma 2.4 are not numbered statements of a source; they collect arguments that
  the sources repeat in each corollary (TRACE, Part A). No step was added, but they are new as statements.
* R9. Theorem 3.1(c) leaves n = 3 and n = 4 open, rules 43 and 142 leave n = 3 open; Table 1 starts at n = 4.
  At n = 4 rule 94 has k* = 1 by computation, which the theorem does not cover.
* R10. Section 4 fits rule 154 only loosely: its "quantity" is the property of having ones on both parity classes,
  and the number that the flips lower is not constant on a cycle. Table 2 says so in its wording; a referee may
  find the common scheme overstated for this rule. For rule 94 the quantity is a set (said in the caption).
* R11. The remark that rules 43 and 142 are not equivalent under reflection and complementation is stated without
  proof; it rests on the two rules being separate classes in the data files.
* R12. Table 1 compares only up to n = 22, and the value of rule 154 at n = 22 comes from the verification's
  computation, not from the study's data file. The figures illustrate two statements and prove nothing; the
  statements of their panel titles are asserted in the script.

Literature.

* R13. The attribution of Theorem A rests on Ellison's text, an abstract and secondary descriptions; the papers of
  Samuelson and of Nöldeke and Samuelson were not read. Said in Sections 2.5 and 6.1.
* R14. Young (1993) and Freidlin and Wentzell are named but are not in the list of references, because no session
  read them and the rule of the house is to cite only what was read. A referee will ask for these standard
  references. Entries for both exist in `trace/trace_refs.md`; adding them is a decision for the author.
* R15. Several entries lack data that the repository does not have: given names of Fukś and Boccara ([4], [7],
  [8], [9]), pages of [17], a date for [1]. Nothing was completed from memory.
* R16. The statement of what was not found is provisional: the searches were short, some were not checked by a
  verification, and for rule 154 and rule 94 with 3 | n no session searched after the proofs existed. Zhu and
  Richard (arXiv:2610.10967), the nearest recent text on rule 154 on finite rings, is known from search excerpts
  only and is therefore named but not used.

Build.

* R17. The PDF in this folder was built in a sandbox with a reduced TeX installation and with `pybtex` in place of
  BibTeX (no `plain.bst` there). With a full installation `build.sh` uses BibTeX; the list of references will then
  be formatted slightly differently. That path of `build.sh` was not run.

## For the author to decide

1. Length (R1). 2. Whether Proposition 5.8 gets its proof (R6). 3. Whether Young and Freidlin-Wentzell are added to
the references (R14), and whether the entries without given names are completed from the sources (R15). 4. Whether
the statement on the use of AI, which is new text in the form of the note's statement, says what the author wants
it to say.
