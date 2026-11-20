# Part 3: what the paper says about itself (status, references, AI statement)

Reader: Claude, one reader of the independent verification. Object: `paper/ring_size_paper.tex` on branch
`paper-ring-size` (HEAD c926271), read only. Nothing in the repository was changed.

Deviations from the task: none in scope. Limits of what was done are in section (c).

Abbreviations: VRS = `VERIFICATION_ring_size.md`; V43142 = `VERIFICATION_43_142.md`; V9426 = `VERIFICATION_94_26.md`;
P94 = `verify_ring_size/part2_94/PROOF_94.md`; P154 = `.../part2_154/PROOF_154.md`; C94 = `proofs_94_26/PROOF_94_converse.md`;
C26 = `proofs_94_26/PROOF_26.md`; ADD = `literature_addendum.md`; LRS = `literature_ring_size.md`;
LC = `verify_ring_size/literature/literature_check.md`.

What was read in full: tex 1-330, 1003-1307, 1440-1729 and the passages quoted below; `paper/TRACE.md`; `paper/trace/attributions.md`;
V9426; V43142; VRS; ADD; `reader_checks/README.md`; `refs.bib`; `numbers.tex`. Read in part (the lines quoted):
`literature.md` l.1-150, LRS (l.1-40, 70-175, 205-300), LC (l.1-50, 60-104, 196-213, 396-410),
`ellison2000_published_reading_notes.md` (l.1-12, 50-74), `VERIFICATION.md`, `VERIFICATION_v02.md` (header and grep hits),
`paper/trace/trace_94.md` (l.1-58 and the table rows), `trace_refs.md` (l.1-30 and headings). The git log (dates, commit ids)
was read with `git log`. No script or script output of the repository was opened or run; `paper/REFEREE_NOTES.md` was not opened.

## Answers to the four questions, in short

1. **Status of the proofs.** According to the reports: the proof documents for rules 43/142 (V43142) and for rule 94 with
   3 not dividing n and rule 26 (V9426) were each verified in a separate session with its own code: confirmed. For rule 26
   no statement of the source was excluded: confirmed (V9426 sect. 3 lists Lemmas 1-9, Theorems 1-5, Corollary 5 as correct;
   its sect. 5 excludes none of them). One false sentence, C1, in the source of Lemma 5.4(c), corrected in the paper: confirmed.
   "No other error": V9426 also has two wording findings on rule 26 (C3, C4) and, for rule 94, a gap C2 and a wording point C5
   (finding 5). Theorem A checked by VRS (B5, B7) and not re-proved by V9426 ("I did not re-prove Theorem A"): confirmed;
   V43142 also read its proof ("complete", with wording point B4). Rule 154 and rule 94 with 3 | n without separate
   verification: confirmed (VRS: "checked inside this verification only"; V9426 l.259). Outside both lists without a
   word: Lemmas 2.2-2.4, Lemmas 3.29-3.31, Lemma 3.38(b) (finding 4). "By hand, no computation": no proof step justified
   by a computation or a data file was found by a keyword search of all proof text and by reading Section 2 and the
   proof of Theorem 3.43; the other proofs were not read line by line by me. "Every computed value ... by a script":
   consistent with TRACE Part E; the numbers quoted from Zhu and Richard come from a document, not a data file (Part E says so).
2. **References.** 25 entries; all 25 are cited. On how each text was seen (read in full, in part, abstract only, not
   read) the paper agrees with the records for all 25. For 16 entries there is no reservation at all; for the other 9 a
   sentence or a note says slightly more than the record or is imprecise (findings 2, 8, 9, 10, 12; table in section
   (a2)). Finding 1 concerns where the searches are recorded.
3. **AI statement.** Dates, sessions and the ranges of the reader checks agree with the git log, the report headers and
   the README. Differences: findings 6, 7, 14.
4. **Internal consistency.** Abstract, "Status", AI statement and TRACE do not contradict each other on what is verified.
   They differ in completeness (findings 5, 7, 13). Counts: 25 references (`refs.bib`, TRACE C19) against "five entries"
   in the TRACE header (six were added). Page count (TRACE: 31) not checked.

## (a1) Numbered statements

Part 3 has no proofs of its own. The table gives, for every numbered statement, the source named by TRACE Part A, what
the records say about its verification by a separate session, and whether "Status of the proofs" (tex 146-156) says the
same. "Not compared" and "not read" mean exactly that; these columns belong to the other parts.

| no. | label | source (TRACE Part A / trace files) | same statement? | proof: steps dropped/added/changed? | cross-references correct? | proof read as a referee? | verification according to the records | agreement with 'Status of the proofs' |
|---|---|---|---|---|---|---|---|---|
| Prop. 2.1 | `prop:order` | note v0.2, Theorem 1 (quoted, no proof in paper) | not compared (source not opened; outside part 3) | no proof in the paper | n/a | no proof to read | VERIFICATION_v02.md V11 ("correct in outline, four steps asserted", added in v0.2); V43142 l.143-145 read, "did not re-derive it in full"; TRACE: "No later verification" | not named in 'Status of the proofs' (silent); paper uses it for interpretation only (tex 215) |
| Lemma 2.2 | `lem:kzero` | not a numbered source statement (note v0.2 proof of Thm 1; Cor. 2 of PROOF_43_142; P94 Cor. 2; P154 Thm 1(f)) | not compared (source not opened; outside part 3) | assembled at paper stage (TRACE Part A, C2) | eq:kv correct | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | V_v02 V11(a); V43142 l.63-64 (Cor. 2 confirmed) | silent in 'Status' |
| Lemma 2.3 | `lem:edge` | P154 Lemma 0; PROOF_43_142 l.59-63; last sentence C94 l.41-42, C26 l.44-45 | not compared (source not opened; outside part 3) | last sentence added from two later documents (TRACE) | none | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | V43142 l.50 ("G1 = {V = 1}: confirmed"); V9426 sect. 3 ("the remark on flips between periodic states ... Correct"); VRS D2 (inside producing session) | silent in 'Status' |
| Lemma 2.4 | `lem:sym` | report_ring_size.md l.212-213, 218-219 (part of Lemma B) | not compared (source not opened; outside part 3) | made a lemma; one-line reason written out (TRACE) | none | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | VRS B5, B6 (Lemma B correct; "rotation symmetry gives S = A") | silent in 'Status' |
| Lemma 2.5 | `lem:reroot` | report_ring_size.md l.173-176 | not compared (source not opened; outside part 3) | per TRACE: letter R -> B only | lem:edge correct | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | VRS B5, B7; V43142 sect. 1 and B4 ("complete") | covered only through the words 'Theorem A ... was checked by the verification of the ring-size study' |
| Lemma 2.6 | `lem:closure` | report l.178-179 | not compared (source not opened; outside part 3) | per TRACE: none | lem:reroot correct | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | as 2.5 | as 2.5 |
| Lemma 2.7 | `lem:inclosed` | report l.181-191 | not compared (source not opened; outside part 3) | wording of finding B4 used (TRACE C8) | lem:reroot correct | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | VRS B5; V43142 B4 (wording), with the corrected reading "complete" | as 2.5 |
| Theorem 2.8 | `thm:A` | report l.193-199 | not compared (source not opened; outside part 3) | third sentence of the source moved after the proof (TRACE) | lem:inclosed, lem:closure, lem:edge correct | read in full (tex 218-303); every step justified; case m = 1 covered; not compared with the source lines | VRS B5 ("correct ... including gamma_min = m - 1"), B7 (sweep, 1412 cases); V43142 ("confirmed with remarks (B4)"); V9426: "I did not re-prove Theorem A" | agrees with 'Status' (tex 152-153) |
| Theorem 3.1 | `thm:main` | union of 3.11, 3.28, 3.43 | not compared (source not opened; outside part 3) | n/a | refs at tex 330-333 point to 154:thm:main, 43:thm:main, 94:thm:main: correct | no proof | see rows | - |
| Lemma 3.2 | `154:lem:local` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.3 | `154:lem:rule90` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.4 | `154:lem:nilpotent` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10; Lemma 3 of P154 also "correct" in V9426 l.104 (cited result) | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.5 | `154:lem:invariant` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.6 | `154:lem:collisions` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.7 | `154:lem:periodic` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.8 | `154:lem:moves` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Theorem 3.9 | `154:thm:pow2` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Theorem 3.10 | `154:thm:other` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Theorem 3.11 | `154:thm:main` | PROOF_154.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | no separate session: VRS D2 (lead of the producing session, own code n = 3..16); VRS C10 | agrees: 'Section 3.1 ... not verified by a separate session' |
| Lemma 3.12 | `43:lem:R` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.13 | `43:lem:wall` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.14 | `43:lem:cons` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.15 | `43:lem:flip` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.16 | `43:lem:pairs` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.17 | `43:lem:pww` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.18 | `43:lem:per` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.19 | `43:lem:half` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Theorem 3.20 | `43:thm:crystal` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Corollary 3.21 | `43:cor:div` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed ("confirmed (given Theorem A)"); own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Proposition 3.22 | `43:prop:heal` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.23 | `43:lem:levels` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.24 | `43:lem:slides` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.25 | `43:lem:Z` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Theorem 3.26 | `43:thm:levels` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed; own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Corollary 3.27 | `43:cor:ndiv` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed ("confirmed (given Theorem A)"); own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Theorem 3.28 | `43:thm:main` | PROOF_43_142.md (TRACE Part A) | not compared (source not opened; outside part 3) | not read | not read | not read | V43142 sect. 1: confirmed ("confirmed (given Theorem A)"); own tests n = 3..20; object: proof document at commit 6725208 | agrees ('verified by a separate session'), with the reservation of finding 3 |
| Lemma 3.29 | `94:lem:freeze` | P94 Lemma 1, Cor. 1a, 1b | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 l.85: cited results of P94 "re-checked. Correct." (hand check; no own test of them in its table); VRS D1 (inside producing session) | silent: source is the document the paper calls not verified; see finding 4 |
| Lemma 3.30 | `94:lem:block` | P94 Lemma 2 | not compared (source not opened; outside part 3) | not read | not read | not read | as 3.29 | as 3.29 |
| Lemma 3.31 | `94:lem:growth` | P94 Lemma 3, Cor. 3 | not compared (source not opened; outside part 3) | not read | not read | not read | as 3.29 | as 3.29 |
| Lemma 3.32 | `94:lem:crystal` | P94 Lemma 6 | not compared (source not opened; outside part 3) | not read | not read | not read | none by a separate session (V9426 l.259 excludes it); VRS D1 inside; reader_checks: F^3(x+e_j) = x at n = 6, 9, 12 | agrees (tex 153-155) |
| Lemma 3.33 | `94:lem:windows` | C94 Lemma 7 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.34 | `94:lem:cut` | C94 Lemma W | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.35 | `94:lem:live` | C94 Lemma 8 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.36 | `94:lem:empty` | C94 Lemma 9 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.37 | `94:lem:refreeze` | C94 Lemma 10 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; finding C2 (gap, closed by a citation; the citation is in the paper, tex 1938-1939) | agrees; C2 is not mentioned in 'Status' (finding 5) |
| Lemma 3.38 | `94:lem:swap` | (a) C94 Lemma 11 (= P94 Lemma 4); (b) sorting argument taken out of P94 Thm 1 stage 2 and C94 Lemma 14(i) (trace_94.md rows 70-71) | not compared (source not opened; outside part 3) | (b) is a statement no source numbers (trace_94.md) | not read | not read | (a) V9426 ("recomputed by hand. Correct.", test L11); (b) the argument inside C94 Lemma 14(i) ("(i) sorting ... Correct"), there for 3 not dividing n; P94 Theorem 1 not verified | silent; (b) is used by Theorem 3.43(i) (tex 1182); TRACE Part A has the row for (b) only (finding 13) |
| Lemma 3.39 | `94:lem:merge` | C94 Lemma 12 = P94 Lemma 5 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.40 | `94:lem:split` | C94 Lemma 13 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.41 | `94:lem:component` | C94 Lemma 14 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees |
| Lemma 3.42 | `94:lem:000` | C94 Lemma 15 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; C5 (wording) | agrees |
| Theorem 3.43 | `94:thm:main` | (i) P94 Theorem 1, Cor. 1, 2; (ii) C94 Theorem 2, Cor. 1 (trace_94.md rows 76-80) | not compared (source not opened; outside part 3) | not compared | all refs in the proof (tex 1169-1238) point to the lemmas meant | proof read (tex 1169-1238): steps justified given the lemmas; n = 6 in (i) and n = 5 in (ii) covered at the level of the theorem; proofs of the lemmas not read | (i) none by a separate session; V9426 l.203-209 computed S, k_v at n = 6, 9, 12 only. (ii) V9426 l.81 correct, "given Theorem A" | agrees (tex 149, 153-155); TRACE Part A row is incomplete (finding 13) |
| Remark 3.44 | `94:rem:small` | P94, C94, VRS A10 (computed) | n/a | n/a | lem:growth, lem:crystal correct | no proof | n = 4: V9426 test T2; reader_checks README: n = 4 closed class = two checkerboards, codes 010 and 101 only, k* = 1; n = 3: F^3(x+e_j) = x fails. Same values in numbers.tex | - |
| Definition 5.1 | `26:def` | C26 sect. 1 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (object: source document at commit 67287d7; finding 3) |
| Lemma 5.2 | `26:lem:frame` | C26 Lemma 1 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (object: source document at commit 67287d7; finding 3) |
| Lemma 5.3 | `26:lem:chi` | C26 Lemma 2 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (object: source document at commit 67287d7; finding 3) |
| Lemma 5.4 | `26:lem:domain` | C26 Lemma 3 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; C1 (false first sentence of (c) in the source); the paper has the corrected form (tex 1369-1371; read) | agrees (object: source document at commit 67287d7; finding 3) |
| Lemma 5.5 | `26:lem:singleton` | C26 Lemma 5 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (object: source document at commit 67287d7; finding 3) |
| Lemma 5.6 | `26:lem:parity` | C26 Lemma 6 (uses P154 Lemmas 2, 3) | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; P154 Lemma 3 "correct" (V9426 l.104) | agrees (object: source document at commit 67287d7; finding 3) |
| Theorem 5.7 | `26:thm:main` | C26 Theorems 2, 3(a)-(c) | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (object: source document at commit 67287d7; finding 3) |
| Proposition 5.8 | `26:prop:indices` | C26 Theorem 4 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; k_v at n = 16 exact by a bound, 16 of 552 roots | agrees (object: source document at commit 67287d7; finding 3) |
| Proposition 5.9 | `26:prop:even` | C26 Theorem 5, Corollary 5 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; Theorem A "used as given" | agrees (object: source document at commit 67287d7; finding 3) |
| Proposition A.1 | `94:prop:periodic` | C94 Theorem 1 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 l.70-72 ("every step correct"), tests T1, T1p6, n = 3..20 | agrees (rule 94; holds for every n >= 3, not only 3 not dividing n) |
| Lemma B.1 | `26:lem:ancestors` | C26 Lemma 4 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (source statement not excluded) |
| Lemma B.2 | `26:lem:kinds` | C26 Theorem 1 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; C3 (wording, circular 'iff'); the paper adds a sentence to the statement (TRACE C11(ii)) | agrees (source statement not excluded) |
| Lemma B.3 | `26:lem:carrier` | C26 Lemma 7 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (source statement not excluded) |
| Lemma B.4 | `26:lem:codes` | C26 Lemma 8 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (source statement not excluded) |
| Lemma B.5 | `26:lem:domaingamma` | C26 Theorem 3(d) | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (source statement not excluded) |
| Lemma B.6 | `26:lem:topar` | C26 Theorem 2 (first sentence) | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests; no proof text of its own (TRACE C11(i)) | agrees (source statement not excluded) |
| Lemma B.7 | `26:lem:oneparity` | C26 Lemma 9 | not compared (source not opened; outside part 3) | not read | not read | not read | V9426 sect. 3 correct, own tests | agrees (source statement not excluded) |

Cross-references in the texts of part 3 (all checked against the label they point to): tex 150 `sec:26`, `app:26`;
151 `26:lem:domain`(c) (C1 concerns Lemma 3(c) of C26 = this lemma); 152 `thm:A`, `26:prop:even` (its "Consequently"
sentence uses Theorem A); 154 `sec:154`, `94:lem:crystal`, `94:thm:main`(i); 156 `tab:kstar`; 310 `lem:closure`,
`lem:inclosed`, `thm:A`; 317 `sec:related`; 1524 `prop:order`; 1530 `thm:A`; 1555, 1575 `154:lem:periodic`; 1569
`43:prop:heal`; 1573 `thm:A`; 1579 `43:lem:per`; 1581 `43:lem:pww`; 1669 `43:prop:heal`; 1675 `app:26`, `sec:open`; 1685,
1689 `tab:kstar`. All point to the statement meant.

## (a2) Every reference: what the paper says, what the records say

"Paper" = the paragraph "What was read" (tex 1590-1602), the note of the entry in `refs.bib` (printed by the style
`plain`; the list is printed at tex 1697-1698, before the appendices), and the sentences that cite it.

| key | paper says | records say | verdict |
|---|---|---|---|
| MartinOdlyzkoWolfram1984 | read in full by a session; Lemma 3.5 (2^j cells: every configuration evolves to null), Lemma 3.7 (3 \| n: three rotations of 011011...), Section 5 (rule 18), "follows from Theorems 3.3 and 3.4 there with their corollaries" (tex 403-404) | LC row 1: "read in full", 40 pages, by the ring-size verification; LC l.183-186, 203-204, 257-259; VRS A25: "the 'iff' follows from their Theorems 3.3 and 3.4 with corollaries" | agree |
| Boccara1993 | not read; "Not obtained; cited after Fuk\'s (2005)" | ADD l.257 "not obtained"; credited in both texts of Fukś | agree; the note does not say which of the two entries of 2005 (finding 9) |
| Fuks2005 | read in full by a session; rule 142 -> 226, credit to Boccara, blocks 10 conserved for rule 142 | ADD l.255 "read in full (publisher PDF)"; V43142 sect. 4 item B1 "supported" | agree |
| Fuks2005b | read in full by the reader outside the sessions, not by a session; eqs. (28), (29); blocks 10 for both rules, taken from Hattori and Takesue | ADD update of 18 Nov. (l.299-316) | agree |
| Fuks1997 | read in full by a session, as preprint; floor((n-2)/2) steps | ADD l.258 "arXiv version read in full (5 pp.)"; V43142 item B4 "supported" | agree; "this is the healing time" see finding 12 |
| NobeYura2004 | tex 1594 "Abstract or search excerpts only"; tex 1549 "by its abstract and a search excerpt"; **tex 449 "according to its abstract"** | LRS l.244-246: abstract: "exactly 16 ECA rules are reversible for infinitely many cell sizes"; rule 154 at odd N: "A search snippet"; LC row 12 | **differ at tex 448-449** (finding 2) |
| NobeYura2007 | abstract or search excerpts only; "by its abstract ... linearises a class of reversible rules" | ADD A2: "Read. Neither text. Seen for (1): the abstract, and two search excerpts" | agree |
| Samuelson1994 | "Not read; abstract only" | LC row 13 "abstract only ... as shown in search results" | agree |
| NoldekeSamuelson1993 | "Not obtained; cited after Ellison (2000)"; in the text "Proposition 1"; "secondary descriptions" | LC row 14 "not obtained ... known only through Ellison (2000) pp. 36-38 (read) and secondary search fragments"; LC l.92: "secondary, search fragments only, not read" | agree on "not read"; the basis of "Proposition 1" is described more strongly than the record (finding 8) |
| Ellison2000 | read in part: working paper of January 1999 and pp. 17, 20, 22-26, 28-31, 36-39; Theorem 2 p. 30; Section 6.2 pp. 37-38; Section 6.3 | LC rows 2, 2a; reading notes p. 30, 37, 38; LRS l.137-168 (working paper: sections named) | agree |
| Newton2018 | read in full by a session | `literature.md` sect. 1 "Sources read in full text", l.76 "Read: version of record" | agree |
| PitmanTang2018 | read in full by a session, "Read in the version arXiv:1603.09017v3"; Theorem 1.1 | `literature.md` l.33-34 | agree |
| PeterleinNote | own text, v0.2; Theorem 1; Proposition 1 (classes 60, 90); k* = 0 for bijections | note has one proposition (`prop:pow2`); V_v02 header V5; note l.202, 219 | agree (`trace/attributions.md` writes "Proposition 2" for the same statement: an error of that file, not of the paper) |
| PeterleinStudy | own repository, version 0.3, doi ...24275024 | tag `v0.3` exists and contains P94, not `proofs_43_142/` (checked with `git cat-file -e`); the DOI stands in no file of the branch (TRACE D15) | agree as far as checkable; DOI not checked |
| BagnoliBaiaMatteuzzi2025 | read in full by a session (arXiv v2); "on a ring of one size", "the ring size is not varied" | `literature.md` l.60-65; LRS l.109-115: "All ECA results are for L = 17 only ... In §4 they enumerate all attractors for 'small lattice sizes', up to 17" | agree on reading; wording slightly stronger than the record (finding 12) |
| BhattacharjeeDas2019 | "Read in part" | LC row 11 "read in part": abstract, Example 2, Table 3 row lists, theorem statements (keyword scan) | agree |
| Fedoriaka2025 | read in full by a session; "from a computation for small rings, with explicit constructions" | LC row 9 "read in full", l.159-162 | agree |
| Nordahl1989 | "Read in part: pp. 68-74 and the list of references" | ADD A3 | agree |
| Stricker2023 | "Read in part: pp. 229-232" | ADD A6 | agree |
| OEIS | read by a session (entries A070886, A334504; the entry also names A334507) | LC row 8 "read (entries and b-files)" | agree; A334507 is in the entry and not in the text (finding 9) |
| Young1993 | "Not read; cited after Newton (2018) and Ellison (2000)" | `literature.md` l.85 "title via DOI only"; Newton l.77; Ellison notes p. 22, 36 name "Young 1993a" for other statements | agree on "not read"; "and Ellison" not supported for the result cited (finding 9) |
| FreidlinWentzell1984 | "Not read; cited after Ellison (2000), in the edition named in his list of references" | Ellison notes p. 38 ("LRSS states correspond to minimum cost trees (Freidlin-Wentzell)"); LC l.406: journal pp. 40-45 (references) not read; TRACE search S4: edition seen in search result pages | agree on "not read"; the source of the edition is a search excerpt (finding 9) |
| HattoriTakesue1991 | "Not read; cited after Fuk\'s (2005), the preprint" | ADD l.263, 307-308 | agree |
| ZhuRichard2026 | read in full by the reader on 20 November 2026, not by a session; definition, unitarity cited from Nobe-Yura, below 0.01 for n = 13..27, two printed values, no explanation | ADD "Update of 20 November 2026" | agree; the pointer "Section A1 ... records what was read ... and by whom" is imprecise (finding 10) |
| Wolfram2002 | "Read in part: Section 6.4 and the notes for Chapter 6"; p. 963; inference marked as such | LRS l.77, 84-104 | agree |
| (no entry) conference version of Bagnoli et al.; journal version of Fuks2005b; Aguiar and Severino | not read; Aguiar-Severino "seen as a search excerpt only" | TRACE Part B; C26 l.337: "abstract and search excerpt read; the paper was not read" | agree (the paper says less than the record for Aguiar-Severino) |

## (b) Findings

Severity classes: (1) false statement; (2) gap in a proof; (3) hypothesis or range not met; (4) unclear; (5) cosmetic.
No finding of class (2) or (3) arises in part 3.

**1. Section 6.1, "What was not found", tex 1584-1585. Class (1), about the record.**
"The searches were short; they are listed in the files `literature_ring_size.md` and `literature_addendum.md` of the
repository." For items (iii) and (v) (rule 94 with 3 not dividing n; rule 26) the searches are recorded only in the proof
documents: C26 l.337 "Literature (short search, two queries, 17 November 2026)" and C94 l.385, same words. Neither
literature file mentions them (grep of ADD for "rule 26", "rule 94", "domain", "frozen": no hit on these searches), and the
wording of those four queries is recorded nowhere. LRS itself contains no list of queries.
*Correction:* "... they are recorded in `literature_ring_size.md` and `literature_addendum.md` and, for rule 26 and for
rule 94 with 3 not dividing n (two queries each, wording not kept), in Section 7 of `PROOF_26.md` and Section 6 of
`PROOF_94_converse.md`."

**2. Section 3.1, tex 448-449. Class (1), stronger than the record; inconsistent with tex 1549.**
"it is stated in [Bhattacharjee-Das] and in [Fedoriaka] and, according to its abstract, in [Nobe-Yura 2004], which was
not read." Record: the abstract "says exactly 16 ECA rules are reversible for infinitely many cell sizes" (LRS l.244);
the statement on rule 154 at odd N is "A search snippet (ResearchGate)" (LRS l.245; LC row 12: "Proposition 1 seen only
as a ResearchGate search fragment"). Section 6.1 has it right: "by its abstract and a search excerpt" (tex 1549).
TRACE Part D item 3 records this inconsistency of the source; the weaker source wording went into tex 449.
*Correction:* at tex 449 "and, by a search excerpt of its Proposition 1, in [Nobe-Yura 2004], which was not read".

**3. "Status of the proofs", tex 148-151. Class (4).**
"The proofs ... were each verified by a separate session. For rule 26 this covers every statement of Section 5 and of
Appendix B". What was verified are the proof documents, at the commits before the corrections and before the paper
existed (V43142: "from `crystal-43-142` at 6725208"; V9426: "commit 67287d7"). The paper's text was assembled afterwards
with recorded changes of statements (TRACE Part A: Lemma B.2 has a sentence added to its statement; Lemma B.6 has "no
proof text of its own"; Lemma 3.38(b) and Lemma 2.2 are statements no source numbers). No record shows a separate
session verifying the text of the paper.
*Correction:* "The proof documents from which Sections 3.2, 3.3 (3 not dividing n), 5 and Appendix B were assembled
were each verified by a separate session; the text of this paper was not. For rule 26 the verification excluded no
statement of the source of Section 5 and Appendix B."

**4. "Status of the proofs", tex 146-156. Class (4): statements outside both lists.**
The paragraph names as verified "rules 43 and 142", "rule 94 with 3 not dividing n", "rule 26", as checked Theorem A,
and as not verified "Section 3.1, Lemma 3.32 and part (i) of Theorem 3.43". Not placed:
(a) Lemmas 2.2-2.4. By TRACE they are covered (V_v02 V11(a) and V43142 l.63-64; V43142 l.50 and V9426 sect. 3; VRS B5-B6),
but the paper does not say so.
(b) Lemmas 3.29-3.31 (freeze, block, growth). Their source is P94, the document that the paper says has no separate
verification. V9426 l.85: "Cited results of P94 that C94 uses (Lemmas 1, 2, 3, Corollaries 1a, 1b, 3): re-checked.
Correct." This is a hand check; the test table of V9426 names no test of these three lemmas (test L7ab exercises the freezing
property through Lemma 7(b) of C94; the exhaustive tests of P94 Lemmas 1-3 are those of VRS D1, inside the producing
session). So "tested every lemma exhaustively ... with its own code" (tex 1659) is not supported by the record for them.
(c) Lemma 3.38(b): the sorting argument was verified inside C94 Lemma 14(i) ("(i) sorting ... Correct"), a lemma for
3 not dividing n; the paper uses 3.38(b) in part (i) of Theorem 3.43 (tex 1182).
(d) Theorem A is also used by Theorem 3.43(ii) (tex 1235) and Corollaries 3.21, 3.27; V9426 took it "as given" there too;
the paragraph says this for Proposition 5.9 only.
*Correction:* one sentence: "Lemmas 2.2-2.4 and 3.29-3.31 and the swap lemma were checked by these verifications as
results that the verified documents use (3.29-3.31 by reading only); Theorem A is used as given in Theorem 3.43(ii)
and Proposition 5.9, and was read again by the verification for rules 43 and 142."

**5. "Status of the proofs", tex 151-152, against the AI statement, tex 1660-1662. Class (4).**
"It found one false sentence without consequence ... and no other error." V9426 sect. 2 has five findings: C1 (false
sentence, rule 26), C2 "gap in a proof (closed by one citation)" in Lemma 10 of C94 = Lemma 3.37, C3 and C4 (wording, rule
26), C5 (wording, rule 94). The AI statement names C1 and C2; "Status" names C1 only and says nothing about C2, which
concerns a proof for rule 94 that the same paragraph calls verified.
*Correction:* "It found one false sentence without consequence (source of Lemma 5.4(c)) and one step that lacked a
citation (source of Lemma 3.37); both are corrected. Its other three findings are wording."

**6. AI statement, tex 1657-1659. Class (4).**
"verified by a separate session that had not seen the work; it ... tested every lemma exhaustively on small rings with
its own code." V9426 sect. 1 is headed "Independence, and one deviation": "Deviation (independence breach, declared) ...
the session's tables were seen before my own tests existed, contrary to the instruction." The paper does not mention it.
*Correction:* add "(the verification for rule 94 and rule 26 declares that it saw the session's computed tables before
writing its tests)". The statement gives no date for that verification; its commit is of 20 November 2026 (511c310).

**7. AI statement, tex 1664-1676, against the README and the TRACE header. Class (4).**
(a) "read the proof documents and this paper and recomputed the statements on small rings". README, "Not covered":
"the lemmas of the proofs one by one". What was recomputed are the conclusions of the theorems (closed classes, selected
set, k_v, gamma_min, healing time, F^3(x+e_j) = x).
(b) By the TRACE header the reader "had read the PDF of commit 72cc2ad". Appendix B, the classes 60 and 90, the report on
Zhu and Richard and "the new wording of the abstract, of 'Status of the proofs' and of the statement on the use of AI"
were written after that. The AI statement lists the first three and the reference entries, not the rewritten abstract and
the two statements. By the records, no one but the writing session has read these parts.
*Correction:* (a) "recomputed the conclusions of the theorems on small rings"; (b) add "and rewrote the abstract, the
paragraph 'Status of the proofs' and this statement; these parts and Appendix B were written after that reader's reading".

**8. Attribution paragraph, tex 310-317, and tex 136, 258, 1530-1534. Class (4): stronger than the record.**
"the correspondence rests on Ellison's text, an abstract and secondary descriptions". LC l.92: "Evidence (secondary,
search fragments only, not read)"; VRS A21: "(L2, attribution; provisional)", "known here only through secondary
descriptions". So the secondary texts were not read either, and the pinpoint "Proposition 1" of Nöldeke and Samuelson
(tex 313) rests on search fragments of them. The words "restates" (tex 136, 258, 310, 1530) carry no "provisional".
*Correction:* "... an abstract and search excerpts of secondary descriptions; the correspondence is provisional."

**9. Notes of the reference list (`refs.bib`). Class (4)/(5).**
(a) FreidlinWentzell1984: "in the edition named in his list of references". Ellison's pp. 40-45 were not read (LC l.406:
"journal pp. 18-19, 21, 27, 32-35, 40-45 (examples, Section 5, appendix lemmas, references)"); the edition comes from search result pages (TRACE, search S4). Say "edition as shown in a search excerpt of his
list of references".
(b) Young1993: "cited after Newton (2018) and Ellison (2000)". The record gives Newton for the stochastic potential;
Ellison's read pages (22, 36) name "Young 1993a" for other statements. Either drop "and Ellison (2000)" or name the page.
(c) Boccara1993: "cited after Fuk\'s (2005)": two entries of that author and year; write "after both texts of Fuk\'s (2005)".
(d) OEIS: the entry names A334507, which the text does not cite.

**10. Section 6.1, tex 1557-1558. Class (4).**
"the table of Section A1 of `literature_addendum.md`, which also records what was read of [Zhu-Richard] and by whom."
Section A1 says "Read. Nothing in full text" (ADD l.41); the reading in full is in the section "Update of 20 November
2026" at the end of that file (TRACE Part D item 13 knows the stale text).
*Correction:* "...; what was read of it and by whom is in the update of 20 November 2026 of that file."

**11. Introduction, tex 103-105, and Section 5, tex 1500-1501. Class (4).**
(a) "[the study] computed k* for the 13 classes ... for n = 8,...,22 (data file `data/ring_size/mechanisms.csv`)". That
file "has n = 8..22 and no record for rule 154 at n = 22" (TRACE D8; caption of Table 1, tex 341-342); the value was
computed by the verification of the study (VRS B12). Add "except rule 154 at n = 22".
(b) "at n = 22 the values of chi on the cycles that contain 111 are 6 and 10": V9426 checked "at n = 22 some cycle
contains 111 and has c = 6" only and lists the row n = 22 of the table of C26 as not checked. The paper marks the
analogous value for rule 94 (tex 1644) and not this one. Add the same remark.

**12. Section 6.1, small wording points. Class (4)/(5).**
(a) tex 1568-1569: "this is the healing time of Proposition 3.22". The proposition has two times, 1 and n/2 - 1; the
record says "the healing time n/2 - 1 ... equals the bound" (ADD l.276-277, about Proposition 2 of the proof document = Proposition 3.22). Write "the larger of the two healing times".
(b) tex 1537-1540: "on a ring of one size ... the ring size is not varied". Record: results under noise for L = 17 only;
attractors enumerated "for 'small lattice sizes', up to 17". Write "the results under noise are for one ring size".
(c) tex 1599-1600: "Two versions are named in this subsection": they are named only in that sentence.
(d) tex 2050-2051 (Appendix B): "Its statements and proofs are those of the document": TRACE C11 lists three things
that are "not literal".

**13. `paper/TRACE.md` against tex 1676-1678 ("maps every statement of the paper to its source"). Class (5) for the paper,
but the rows concern verification.**
Part A keeps only the last sub-row of `trace/trace_94.md` and `trace/trace_26.md` for three statements. Row 3.43 has
the source "C94 Corollary 1" and the verdict "V9426 81 ('Corollary 1: correct')" and the change "as above" with nothing
above; the rows for part (i) ("No independent verification of the proof is recorded in the repository") and for (ii) K
are missing. Row 3.38 has (b) only; row 5.7 has (d) only ("as (b)"). Read alone, Part A says Theorem 3.43 is verified;
the paper's "Status" is right. Also: the TRACE header says "five entries of the list of references", Part C item 19
"19 entries -> 25 ... six new entries"; `trace/attributions.md` writes "note v0.2, Proposition 2" where the note has
one proposition.
*Correction:* restore the sub-rows in Part A; "six entries" in the header.

**14. Dates. Class (5).**
AI statement: proofs for rule 94 (3 not dividing n) and rule 26 "(18 November 2026)" = date of commit 67287d7. The proof
documents date their literature search "17 November 2026", and `trace/trace_refs.md` l.28 writes "session of
proofs_94_26 (17 November 2026)". All other dates of the statement agree with the git log (13/14 November study and
proofs; 17 November proofs and verification of 43/142; 20 November assembly, update, reader checks) and with the TRACE
header (commits d6c6299, 72cc2ad, dc5ac15 exist).

**15. "Code and data", tex 1683-1694. Class (4), remark.**
The files added after version 0.3, on which the statements of the paper rest (`proofs_43_142/`, `proofs_94_26/`,
`VERIFICATION_43_142.md`, `VERIFICATION_94_26.md`, `reader_checks/`, `literature_addendum.md`, `paper/`), are in no
archived version, and the paper names no tag or commit for them. This is said ("added to the repository after that
version"), so it is not an error; a tag or commit id would make the references checkable.

Nothing found in class (2) (gap in a proof) and class (3) (range not met): the texts of part 3 contain no proof, and the
proofs of Section 2 and of Theorem 3.43, which I read, gave no finding.

## (c) Not checked

* Whether an attribution is right in the literature; no reference was opened, nothing was searched.
* The statements of the paper against their source documents, and the proofs other than Section 2 (tex 218-303) and
  the proof of Theorem 3.43 (tex 1169-1238). "By hand, no computation" for the other proofs rests on a keyword search
  (comput, enumerat, exhaust, check, verif, table, data, script, inspection, one finds, rule table, ...) and the hits read in
  context, not on a full reading.
* `paper/numbers.json`, `paper/test_paper.py`, `make_numbers.py`, every script and output file: not opened. So "taken from a
  data file by a script" was compared with TRACE Part E and `numbers.tex` only, not with the data.
* The printed PDF (page count 31, numbers of the references [18], [19], how the notes print).
* The DOIs (zenodo 23399100, 24093547, 24275024), the ORCID, the URL. 23399100 and 24093547 stand in `CITATION.cff`;
  24275024 stands in no file of the branch (TRACE D15).
* `literature.md` l.151-354, LRS l.300-597 (BibTeX blocks), `trace_refs.md` beyond l.1-30, `trace_154.md`, `trace_43_142.md`,
  `trace_26.md` beyond their row labels, `report_ring_size.md` (two greps only), `verify_43_142/literature/lit_check_43_142.md`.
* Whether the reader's reading of Zhu and Richard and of Fukś (preprint) is accurate: the record of the reader is the only source.
* `paper/REFEREE_NOTES.md` (not opened, as instructed).

Claude
