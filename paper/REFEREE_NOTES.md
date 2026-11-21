# Referee notes on `ring_size_paper.pdf`

20 November 2026, by the session that assembled the paper. Updated on the same day by a later session (Claude)
that carried out the author's decisions on the four open points; its additions are the lines "Status (update)"
under R1 to R17 and the sections "Decisions (update)" and "Second reading (update)" at the end. The page numbers of
the first three sections refer to the PDF of commit 72cc2ad (27 pages); those of the update to the PDF built by the
update (31 pages).

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
  Status (update): Decided by the author: the length stays and nothing is cut. With Appendix B the paper has 31 pages.
* R2. Sections 3.2 and Appendix A are dense: long proofs as running text (Lemmas 3.16, 3.17, 3.35), Definition 5.1
  as one paragraph. Displaying the case distinctions would add about two pages.
  Status (update): Not handled. Sections 2 and 3 and Appendix A were not to be changed. Appendix B adds proofs as running
  text of the same kind.
* R3. Section 3.3 states fourteen lemmas without proof in a row. This is the structure asked for (chain of lemmas
  in the main text, proofs in the appendix).
  Status (update): Not handled (structure asked for).
* R4. The paper avoids amssymb and amsthm (not available in the sandbox): "does not divide" is a slashed bar, Z is
  bold, the end-of-proof mark is a filled square that sometimes stands alone on a line after a list (pp. 24, 26).
  Three underfull boxes remain (caption of Table 1).
  Status (update): Not handled. In the PDF of the update the end-of-proof square stands alone on a line after the proofs of
  Lemma 3.31 (p. 25) and Lemma 3.35 (p. 27 in the first build of the update).

Mathematics and its status.

* R5. Proposition 2.1 is quoted from a note that has not been through peer review. It is used only to say what
  k_v means; every theorem is a statement about the integers defined in (1). Not fixable here.
  Status (update): Not handled; not fixable here.
* R6. Proposition 5.8 (the indices k_v of rule 26) and the first half of Proposition 5.9 have no proof in the
  paper; the text points to `proofs_94_26/PROOF_26.md`. A referee will not accept a proposition proved in a
  repository file. Including the proof of 5.8 needs Lemmas 4, 7, 8 and Theorem 3(d) of that file, about one page.
  Status (update): Handled. Propositions 5.8 and 5.9 are proved in Appendix B (Lemmas B.1 to B.7 and two proofs, pp. 29
  to 31), from `proofs_94_26/PROOF_26.md`, with a row for every added statement in `TRACE.md`. No step was added,
  and no gap was found in the source.
* R7. Who checked what. Rules 43, 142, rule 94 with 3 not dividing n, and rule 26: one independent verification
  each. Rule 154 and rule 94 with 3 | n: the proofs were written and checked inside one verification session, and
  a second reading is recorded only "as reported by the author"; no independent verification report exists for
  Lemma 3.32 and for part (i) of Theorem 3.43 (`VERIFICATION_94_26.md` l. 259 excludes them). Nothing has been
  through peer review. The statement at the end says this; a referee will still count it against the paper.
  Status (update): Handled in the wording, not in substance. "Status of the proofs" and the statement on the use of AI
  now say plainly that the proofs for rule 154 and for rule 94 with 3 | n have not been verified by a separate
  session. The clause "as reported by the author" is replaced by sentences that say who read (Claude, in the
  conversation in which the sessions were planned), what was recomputed (`reader_checks/`, with the ranges of its
  README) and that this reader is not independent of the planning. The objection stands until the next
  verification.
* R8. Lemma 2.2 (third clause) and Lemma 2.4 are not numbered statements of a source; they collect arguments that
  the sources repeat in each corollary (TRACE, Part A). No step was added, but they are new as statements.
  Status (update): Not handled. Sections 2 and 3 go to a verification session next.
* R9. Theorem 3.1(c) leaves n = 3 and n = 4 open, rules 43 and 142 leave n = 3 open; Table 1 starts at n = 4.
  At n = 4 rule 94 has k* = 1 by computation, which the theorem does not cover.
  Status (update): Handled for rule 94: the abstract and the introduction now say that n = 3 and n = 4 are not covered and
  that the computed value at n = 4 does not follow the pattern. For rules 43 and 142 the abstract gives the range
  n >= 4 of Theorem 3.1(b); n = 3 is open as before.
* R10. Section 4 fits rule 154 only loosely: its "quantity" is the property of having ones on both parity classes,
  and the number that the flips lower is not constant on a cycle. Table 2 says so in its wording; a referee may
  find the common scheme overstated for this rule. For rule 94 the quantity is a set (said in the caption).
  Status (update): Not handled.
* R11. The remark that rules 43 and 142 are not equivalent under reflection and complementation is stated without
  proof; it rests on the two rules being separate classes in the data files.
  Status (update): Not handled.
* R12. Table 1 compares only up to n = 22, and the value of rule 154 at n = 22 comes from the verification's
  computation, not from the study's data file. The figures illustrate two statements and prove nothing; the
  statements of their panel titles are asserted in the script.
  Status (update): Not handled.

Literature.

* R13. The attribution of Theorem A rests on Ellison's text, an abstract and secondary descriptions; the papers of
  Samuelson and of Nöldeke and Samuelson were not read. Said in Sections 2.5 and 6.1.
  Status (update): Not handled; said in Sections 2.5 and 6.1 as before.
* R14. Young (1993) and Freidlin and Wentzell are named but are not in the list of references, because no session
  read them and the rule of the house is to cite only what was read. A referee will ask for these standard
  references. Entries for both exist in `trace/trace_refs.md`; adding them is a decision for the author.
  Status (update): Handled by the decision of the author: Young (1993), Freidlin and Wentzell (the edition of 1984 that
  Ellison cites) and Hattori and Takesue (1991) are in the list of references, each with the note "Not read; cited
  after ..." that names the read source. The sentence of Section 6.1 that said they are not in the list is removed.
* R15. Several entries lack data that the repository does not have: given names of Fukś and Boccara ([4], [7],
  [8], [9]), pages of [17], a date for [1]. Nothing was completed from memory.
  Status (update): Handled in part. Completed: Nino Boccara; Henryk Fukś (three entries); Pitman and Tang, Bernoulli
  24(3), 1942-1972; Stricker, 229-251; Fukś (1997), Physical Review E 55(3), R2081-R2084. The data come from the
  update of 20 November of `literature_addendum.md` and from four web searches recorded in `TRACE.md`, Part B
  (result pages only; no paper was opened). Still incomplete: the OEIS entry has no year; Nordahl and Stricker have
  initials only; Nöldeke and Samuelson (1993) and Samuelson (1994) have no issue and no DOI.
* R16. The statement of what was not found is provisional: the searches were short, some were not checked by a
  verification, and for rule 154 and rule 94 with 3 | n no session searched after the proofs existed. Zhu and
  Richard (arXiv:2610.10967), the nearest recent text on rule 154 on finite rings, is known from search excerpts
  only and is therefore named but not used.
  Status (update): Handled for Zhu and Richard: the text was read in full on 20 November 2026 by the reader outside the
  sessions, has an entry that says so, and Section 6.1 reports what it says about rule 154 and what Lemma 3.7
  gives. No session opened the text; the report rests on the record of that reader in `literature_addendum.md`. The
  rest of R16 stands (short searches; no search by a session after the proofs for rule 154 and for rule 94 with
  3 | n existed).

Build.

* R17. The PDF in this folder was built in a sandbox with a reduced TeX installation and with `pybtex` in place of
  BibTeX (no `plain.bst` there). With a full installation `build.sh` uses BibTeX; the list of references will then
  be formatted slightly differently. That path of `build.sh` was not run.
  Status (update): Not handled. The PDF of the update was again built with the reduced pdflatex of the sandbox and with
  `pybtex`; `plain.bst` is not installed there, so the BibTeX path of `build.sh` is still not run.

## For the author to decide

1. Length (R1). 2. Whether Proposition 5.8 gets its proof (R6). 3. Whether Young and Freidlin-Wentzell are added to
the references (R14), and whether the entries without given names are completed from the sources (R15). 4. Whether
the statement on the use of AI, which is new text in the form of the note's statement, says what the author wants
it to say.

## Decisions (update)

Decided by the author on 20 November 2026 and carried out by the update: (1) the length stays; (2) Propositions 5.8
and 5.9 get their proofs in the paper; (3) Young and Freidlin-Wentzell (and Hattori-Takesue) go into the list of
references as texts not read; (4) the statement on the use of AI is changed.

## Second reading (update)

### How the paper was read

* The LaTeX source of the paper of commit 72cc2ad was read in full (all 1995 lines) before any change, together
  with `proofs_94_26/PROOF_26.md` (all sections), `VERIFICATION_94_26.md` and `literature_addendum.md`. While
  Appendix B was written, every step of Lemmas 4, 7, 8, 9, of Theorems 1, 3(d), 4 and 5 and of Corollary 5 of the
  source was followed by hand against the rule table and the lemmas of Section 5. Re-derived in that reading: the
  induction of Lemma B.1, both image steps of Lemma B.3, the four cell patterns of Lemma B.4, the groups and
  sources of the intermediate states of Lemma B.5 for even and odd i, the sources 0, 5, 8, ..., n - 3 in part (c)
  of the proof of Proposition 5.8, and the bound on the longer domain in the proof of Proposition 5.9. Read but not
  re-derived: the decomposition into kernel and image over GF(2) in the proof of Proposition 5.9 (the same argument
  as in the proof of Lemma 3.36).
* The first PDF built by the update (31 pages) was then read from the first page to the last as page images
  (110 dpi), one page per image. The first requests for pages returned no content, and the notes written after them
  were discarded; one of those notes had listed pages as seen that had not been displayed. After that every one of
  the 31 pages was displayed once.
* After the fixes the pages whose content changed were looked at again as images: pp. 2 and 21 in the build before
  the last change; pp. 22, 24, 25, 30 and 31 in the final build. The final PDF was not read a second time as a
  whole; from p. 2 on its line breaks differ by a few lines from the PDF that was read, and Lemma B.7 moved from
  p. 30 to p. 31.

### Found in this reading and fixed

1. p. 2: "(k* = 2 and k* = 2)" for rule 26 at k = 2 and k = 4; the ring sizes are now named.
2. p. 21: "for even n they print the values ... at n = 22 and ... at n = 24" read as a statement on every even n;
   now "the two values that they print for even n".
3. p. 2, "Status of the proofs": a first wording said that the verification found every statement on rule 26
   correct. It found one false sentence in the source of Lemma 5.4(c) (finding C1, corrected in the source). The
   paragraph now says so.
4. p. 22, classes 60 and 90: a first wording said that the repository records no text as read for rule 60 on 2^j
   cells. It records one: a note in Wolfram (2002), p. 963, read by the study session, from which the statement
   was inferred there. The paper now cites it and says that the conclusion is an inference of the study.
5. p. 23, "Code and data": a first wording placed "the data files used here" in version 0.3. The output files of
   `proofs_94_26/` and `proofs_43_142/` are not in the tag v0.3; the sentence now names the data files of Table 1.

### What a referee would object to, new or changed (not fixed)

* R18. Lemma B.6 has no proof text of its own: it refers to the first part of the proof of Theorem 5.7(a), which
  is written for every even n. A referee will ask that the statement for even n stand before Theorem 5.7. That
  changes a statement of Section 5 and was left as it is.
* R19. The proof of Proposition 5.9 repeats, with the letter Sigma, the algebra over GF(2) that the proof of
  Lemma 3.36 gives with the letter tau. One lemma would serve both; Appendix A was not to be changed.
* R20. Lemma B.2 ends with a sentence about cycles ("Hence every cycle is contained in E ∪ O, or is a domain
  cycle, or contains 111") that is not a sentence of Theorem 1 of the source; it states what the proof there shows
  and how the source uses that theorem (`TRACE.md`, row of Lemma B.2).
* R21. Section 6.2 cites Proposition 1 of the note [18] for classes 60 and 90. The note has not been through peer
  review; its proof is the one given in finding V5 of `VERIFICATION_v02.md`, and no later session checked it.
* R22. The report on Zhu and Richard rests on the record of the reader outside the sessions; no session opened the
  text, and that reader had the figures only as the text printed in them. The four numbers quoted from the text are
  taken from that record and from the file that stores the two quoted values, through `make_numbers.py`.
* R23. The DOI of version 0.3 is not in any file of the branch (it was given by the author). What "Code and data"
  says about the content of version 0.3 was checked against the git tag v0.3, not against the Zenodo record.
* R24. Bibliographic data of five entries come from result pages of web searches (pages of Pitman and Tang and of
  Fukś 1997; title, given names and DOI of Hattori and Takesue; edition of Freidlin and Wentzell), not from the
  texts.
* R25. The abstract is longer; it now carries the ranges and the exception at n = 4.
* R26. Table 2 floats to the top of p. 18, between the two halves of Definition 5.1.
* R27. p. 31 is half empty; the paper ends with the proof of Proposition 5.9.
* R28. `reader_checks/README.md` and the update of `literature_addendum.md` refer to statements of the paper by
  number. The numbers of Sections 2, 3 and 5 are unchanged; the numbers of the references are not (the note is
  [18], it was [16]).

## After the verification of the paper (update 2)

Written on 20 November 2026 by Claude, the reader outside the sessions, after `VERIFICATION_paper.md` and after its
findings were worked into the paper (`paper/TRACE.md`, Part F; header of the report).

* R7 (who checked what): handled in substance. Section 2, Section 3.1, Lemma 3.32 and part (i) of Theorem 3.43
  with the lemmas it uses were verified by a separate session; it found no false statement. What remains: the
  corrections made after that verification (some of them sentences in proofs) are unverified, and nothing has been
  through peer review.
* R8 (Lemmas 2.2 and 2.4 new as statements): verified by that session; "Status of the proofs" names them.
* R9: Remark 3.44 now says what fails at n = 4. n = 3 for rules 43 and 142 is open as before (computed in the
  verification: k* = 0).
* R10: the caption of Table 2 and the abstract now say that the scheme fits rule 154 only in part.
* R17: handled. The PDF is now built with a full TeX installation and BibTeX (`plain.bst`); 32 pages.
* R18: handled in part (clause on chi added; Lemma B.6 not moved, see the header of the report, D18).
* R26, R27: the page breaks changed with the new build; not looked at again one by one.
* Still open and not touched: R2, R3, R4 (no amssymb, no amsthm), R5, R11, R12, R13, the rest of R16, R19, R21 to
  R24, R28.
* New: the page numbers in this file and in `VERIFICATION_paper.md` refer to earlier PDFs (27 and 31 pages).

Claude
