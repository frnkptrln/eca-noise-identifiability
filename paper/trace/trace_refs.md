# trace_refs.md: how each reference of the ring-size paper was seen

Track: literature, references, attributions. Files of this track: `refs.bib`, `related_work.tex`,
`intro_known.tex`, `attributions.md`, this file. Line numbers refer to the repository at branch `paper-ring-size`
(commit d6c6299, merge of `class-94-26`); they were looked up by script from the files, not typed.

The fragment of this track (`related_work.tex` followed by `intro_known.tex`) contains **no theorem, proposition,
lemma or corollary**. The table "paper label | source statement | tag | verification verdict | changes" asked for
in the general deliverables therefore has no rows. Its place is taken by sections 1 (one row per entry of
`refs.bib`) and 9 (one row per sentence of the fragment, with the repository line that covers it).

Reading rule of the repository, used here without change: "read" means that the text itself was opened and read
in a session; abstract-level and excerpt-level knowledge is named as such (`literature_ring_size.md`:5; `literature_addendum.md`:13;
`verify_ring_size/literature/literature_check.md`:8).

Sessions named below, as the repository documents name them:

* **literature session of v0.2**: `literature.md` (note v0.2; November 2026);
* **verification of v0.2**: `VERIFICATION_v02.md` (9 November 2026); it read Bagnoli et al. and nothing else of the
  literature (`VERIFICATION_v02.md`:81);
* **ring-size study session** (literature track): `literature_ring_size.md` Sections 0 to 4;
* **ring-size verification** (literature track, 14 November 2026): `verify_ring_size/literature/literature_check.md`,
  findings A20 to A31 of `VERIFICATION_ring_size.md` (`VERIFICATION_ring_size.md`:260);
* **session of proofs_43_142** (17 November 2026): `literature_addendum.md`;
* **verification of proofs_43_142**, literature sub-task: `VERIFICATION_43_142.md` Section 4,
  `verify_43_142/literature/lit_check_43_142.md`;
* **reader outside both sessions** (18 November 2026): update section of `literature_addendum.md` (`literature_addendum.md`:295);
* **session of proofs_94_26** (17 November 2026): the "Literature" items of `PROOF_26.md` (`proofs_94_26/PROOF_26.md`:337) and
  `PROOF_94_converse.md` (`proofs_94_26/PROOF_94_converse.md`:385); these were **not** checked by the verification of those proofs
  (`VERIFICATION_94_26.md`:263).

## 1. Entries of refs.bib

| key | how seen | repository lines that say so | where the fields come from | missing fields, remarks |
|---|---|---|---|---|
| MartinOdlyzkoWolfram1984 | read in full (author copy, 40 pp.) by the ring-size verification; not read by the study session (known there second-hand through Powley and Stepney) | `verify_ring_size/literature/literature_check.md`:30, `literature_ring_size.md`:15, `literature_ring_size.md`:234, `VERIFICATION_ring_size.md`:260, `literature_ring_size.md`:210 | all fields: BibTeX block at `literature_ring_size.md`:409 ff.; checked against the first page by the verification (`verify_ring_size/literature/literature_check.md`:375) | none. The note field of the repository's BibTeX block still says 'Not read' (see errors, item 1) |
| Boccara1993 | not obtained by any session; known through the credit in Fuks2005 and Fuks2006 (both print 1992); date and DOI seen on the publisher page by the verification | `literature_addendum.md`:257, `proofs_43_142/PROOF_43_142.md`:757, `literature_addendum.md`:304, `VERIFICATION_43_142.md`:187, `VERIFICATION_43_142.md`:188, `verify_43_142/literature/lit_check_43_142.md`:9 | author (family name), title, journal, volume, pages, year, doi: `literature_addendum.md`:257; number 3-4 and the date 15 October 1993: `VERIFICATION_43_142.md`:188 | given name or initial of the author |
| Fuks2005 | read in full (publisher PDF) by the session of proofs_43_142; statements re-read page by page by the literature sub-task of its verification | `literature_addendum.md`:255, `proofs_43_142/PROOF_43_142.md`:757, `VERIFICATION_43_142.md`:159, `verify_43_142/literature/lit_check_43_142.md`:37 | author (family name), title, journal, volume, pages, year ('footer: 2005'), doi: `literature_addendum.md`:255; year confirmed `verify_43_142/literature/lit_check_43_142.md`:37 | given name or initial; issue number (present only inside the DOI string) |
| Fuks2006 | arXiv:nlin/0502037v1 read in full on 18 November 2026 by the reader outside both sessions; before that a search excerpt only (session of proofs_43_142); not reachable for the verification; journal version (2007, other title) not seen | `literature_addendum.md`:299, `literature_addendum.md`:295, `literature_addendum.md`:256, `proofs_43_142/PROOF_43_142.md`:760, `VERIFICATION_43_142.md`:3, `VERIFICATION_43_142.md`:255 | title of the preprint, arXiv number, date, 15 pages: `literature_addendum.md`:299 ff.; journal title, Fundamenta Informaticae 78 (2007) 329-341: `literature_addendum.md`:256 | given name or initial. KEY/YEAR: no document has a year 2006 for this paper (see section 2) |
| NobeYura2004 | abstract only (study session, via the fetch tool; ring-size verification, publisher page in search results); Proposition 1 seen as a search excerpt only | `literature_ring_size.md`:243, `literature_ring_size.md`:244, `literature_ring_size.md`:245, `literature_ring_size.md`:246, `verify_ring_size/literature/literature_check.md`:43, `verify_ring_size/literature/literature_check.md`:402 | all fields: BibTeX block at `literature_ring_size.md`:453 ff.; journal, volume, issue, first page checked (`verify_ring_size/literature/literature_check.md`:380: 'end page not checked') | none; end page 5804 stands in the repository but was not checked |
| NobeYura2007 | abstract and two search excerpts only (study session: abstract; session of proofs_43_142: abstract and excerpts); full text not reached by the verification | `literature_ring_size.md`:247, `literature_addendum.md`:130, `literature_addendum.md`:135, `VERIFICATION_43_142.md`:175 | author, title, journal, volume, number, first page, year, doi: BibTeX block at `literature_ring_size.md`:465 ff.; page range 7159-7174: `literature_addendum.md`:126 | none |
| Samuelson1994 | abstract only, by the ring-size verification (ScienceDirect abstract as shown in search results); primary text not read by anyone | `verify_ring_size/literature/literature_check.md`:44, `literature_ring_size.md`:26, `VERIFICATION_ring_size.md`:382, `verify_ring_size/literature/literature_check.md`:400 | all fields: BibTeX block at `literature_ring_size.md`:570 ff. | issue number, DOI |
| NoldekeSamuelson1993 | not obtained; known only through Ellison2000, pp. 36-38 (read by the verification) and secondary search fragments | `verify_ring_size/literature/literature_check.md`:45, `literature_ring_size.md`:26, `VERIFICATION_ring_size.md`:382, `verify_ring_size/literature/literature_check.md`:92 | all fields: BibTeX block at `literature_ring_size.md`:580 ff. (key there: NoeldekeSamuelson1993) | issue number, DOI |
| Ellison2000 | read in part. Study session: author working paper of January 1999 (45 pp.): Def. 1, Sects. 2.2, 3.1-3.2, 4.1-4.2, 6.3. Ring-size verification: published version, journal pp. 17, 20, 22-26, 28-31, 36-39 (15 of 29), from page images; appendix lemmas not read | `literature_ring_size.md`:138, `literature_ring_size.md`:74, `literature_ring_size.md`:349, `verify_ring_size/literature/literature_check.md`:31, `verify_ring_size/literature/literature_check.md`:32, `literature_ring_size.md`:15, `verify_ring_size/literature/literature_check.md`:406, `VERIFICATION_ring_size.md`:382 | all fields: BibTeX block at `literature_ring_size.md`:340 ff.; journal, year, volume, pages, title checked against the article header, DOI resolved to the title (`verify_ring_size/literature/literature_check.md`:374; `verify_ring_size/literature/literature_check.md`:136) | none. An earlier document gives the entry without DOI (`literature.md`:13; `literature.md`:88) |
| Young1993 | not read by any session (title via the DOI only); the content is known from the secondary source Newton2018 (read) and from Ellison2000 (pp. 22, 36) | `literature.md`:85, `literature.md`:9, `literature.md`:123, `literature.md`:77, `verify_ring_size/literature/ellison2000_published_reading_notes.md`:70 | all fields: BibTeX block at `literature.md`:241 ff.; also `literature.md`:85 | none |
| FreidlinWentzell2012 | not read by any session (title of chapter 6 only) | `literature.md`:89, `literature.md`:9, `literature.md`:124 | authors, title, edition, publisher, year, doi: BibTeX block at `literature.md`:263 ff.; also `note/note_v0.2.tex`:234 | address, series |
| Bagnoli2024 | the chapter was not read by any session; read was the extended arXiv version (BagnoliBaiaMatteuzzi2025) | `literature_ring_size.md`:76, `literature_ring_size.md`:110, `literature.md`:60, `VERIFICATION_v02.md`:81, `note/note_v0.2.tex`:230 | all fields: BibTeX block at `literature_ring_size.md`:327 ff.; pages 'taken from the authors' own citation of it' (`literature.md`:60); DOI resolved to the title only (`verify_ring_size/literature/literature_check.md`:382) | editors, address |
| Wolfram1983 | no record in the repository that any session read or saw this text | cited at `note/note_v0.2.tex`:39; bibliographic details of the note are listed as not checked by the verification of v0.1 (`VERIFICATION.md`:46) | all fields: bibliography of the note, `note/note_v0.2.tex`:239 | given name (initial only), issue number, DOI |
| LiPackard1990 | search excerpt only (session of proofs_94_26, for the statement that rules 26, 73, 154 are locally chaotic); no record that the text was read | `proofs_94_26/PROOF_26.md`:340; cited at `note/note_v0.2.tex`:78; `VERIFICATION.md`:46 | all fields: bibliography of the note, `note/note_v0.2.tex`:235 | given names (initials only), issue number, DOI |
| PitmanTang2018 | read in the version arXiv:1603.09017v3 (8 February 2018) by the literature session of v0.2 | `literature.md`:33, `literature.md`:34, `literature.md`:125 | authors, title, journal, volume, year, doi: BibTeX block at `literature.md`:174 ff.; also `note/note_v0.2.tex`:237 | pages and issue ('Pages not verified') |
| ZhuRichard2026 | search excerpts only (two sets, session of proofs_43_142; further excerpts seen by the literature sub-task of its verification); the excerpts are not stored | `literature_addendum.md`:41, `literature_addendum.md`:46, `VERIFICATION_43_142.md`:175 | authors, title, arXiv number and class, date, pages: `literature_addendum.md`:37 ff. ('data from the arXiv abstract page as returned by the search') | none |
| PeterleinNote | source document of the paper (note/note_v0.2.tex) | `note/note_v0.2.tex`:24, `note/note_v0.2.tex`:25, `note/note_v0.2.tex`:26 | title: `note/note_v0.2.tex`:24, `CITATION.cff`:3; author: `note/note_v0.2.tex`:25, `CITATION.cff`:5; version and month: `note/note_v0.2.tex`:26; doi of version 0.2: `CITATION.cff`:23-24, `README.md`:15, `report_ring_size.md`:4; 'Zenodo': `README.md`:17 | The note itself does not contain its version DOI: `note/note_v0.2.tex`:227 gives the DOI of v0.1 and the DOI of all versions only (the links in note_v0.2.pdf are the same two). CITATION.cff describes version 0.3 (`CITATION.cff`:8) |
| BagnoliBaiaMatteuzzi2025 | read in full (arXiv v2, 30 April 2025, 16 pp.) by the literature session of v0.2, by the verification of v0.2 and by the ring-size study session; read in part (Table 2 and surrounding text) by the ring-size verification | `literature.md`:60, `VERIFICATION_v02.md`:70, `literature_ring_size.md`:109, `literature_ring_size.md`:110, `verify_ring_size/literature/literature_check.md`:41 | all fields: BibTeX block at `literature_ring_size.md`:318 ff. | none |
| Newton2018 | read (version of record) by the literature session of v0.2; a secondary source | `literature.md`:76, `literature.md`:77 | all fields: BibTeX block at `literature.md`:234 ff. | none |
| Fuks1997 | arXiv:comp-gas/9703001v1 read in full (5 pp.) by the session of proofs_43_142 and by the literature sub-task of its verification; journal version not compared | `literature_addendum.md`:258, `VERIFICATION_43_142.md`:168, `literature_addendum.md`:355 | author (family name), title, journal (as abbreviated there), volume, year, page R2081, arXiv number: `literature_addendum.md`:258 | given name or initial; full journal name; issue; end page |
| HattoriTakesue1991 | not obtained; named in Fuks2006 as the source of the conserved number of blocks 10 | `literature_addendum.md`:265, `literature_addendum.md`:307, `VERIFICATION_43_142.md`:250 | family names, Physica D 49 (1991) 295-322: `literature_addendum.md`:264 | title, given names, DOI |
| BhattacharjeeDas2019 | read in part by the ring-size verification (abstract, Example 2, Table 3 row lists, theorem statements by keyword scan; text extraction); not read by the study | `verify_ring_size/literature/literature_check.md`:42, `verify_ring_size/literature/literature_check.md`:157, `literature_ring_size.md`:15 | all fields: BibTeX block at `literature_ring_size.md`:590 ff. | none |
| Fedoriaka2025 | read in full (v1, text extraction) by the ring-size verification; search excerpt only in the study session | `verify_ring_size/literature/literature_check.md`:40, `verify_ring_size/literature/literature_check.md`:159, `literature_ring_size.md`:248 | all fields: BibTeX block at `literature_ring_size.md`:477 ff.; title and arXiv number checked (`verify_ring_size/literature/literature_check.md`:381) | none |
| Nordahl1989 | read in part (publisher scan: pp. 68-74 and the reference list pp. 76-78) by the session of proofs_43_142; pp. 70, 73, 74 and the references re-read by the literature sub-task of its verification | `literature_addendum.md`:144, `literature_addendum.md`:145, `VERIFICATION_43_142.md`:171 | all fields: `literature_addendum.md`:142 | given names (initials only), issue, DOI |
| Stricker2023 | read in part (publisher PDF: pp. 229-232; the remaining 19 PDF pages not read) by the session of proofs_43_142; pp. 230, 232 re-read by the verification | `literature_addendum.md`:207, `VERIFICATION_43_142.md`:171 | all fields: `literature_addendum.md`:204 ff. | end page ('229 ff.'); given name (initials only) |
| VoorheesBeauchemin2004 | read in part (journal PDF: pp. 41-53 and 66-71) by the session of proofs_43_142; pp. 44, 52, 68-70 re-read and the full text scanned for rule numbers by the verification. Not cited in the fragment (cut for length) | `literature_addendum.md`:225, `VERIFICATION_43_142.md`:171 | all fields: `literature_addendum.md`:219 ff. | given names (initials only), issue, DOI |
| Wuensche2024 | search excerpt only | `literature_ring_size.md`:252, `literature_ring_size.md`:254, `verify_43_142/literature/lit_check_43_142.md`:74 | all fields: BibTeX block at `literature_ring_size.md`:505 ff. | none |
| WuenscheLesser1992 | not obtained by any session (hosts refused); uncited bibliography item of the note | `literature_ring_size.md`:249, `verify_ring_size/literature/literature_check.md`:36, `VERIFICATION_ring_size.md`:380, `literature.md`:101, `VERIFICATION_v02.md`:12 | all fields: BibTeX block at `literature_ring_size.md`:486 ff. ('Publisher data not verified against the book'); series, publisher, year consistent with the author's publication list (`verify_ring_size/literature/literature_check.md`:383) | address |
| Ellison1993 | read (scanned journal pages, via OCR; Theorem 1 checked by eye) by the ring-size study session; not read by the literature session of v0.2. Not cited in the fragment (cut for length) | `literature_ring_size.md`:171, `literature_ring_size.md`:74, `literature.md`:87 | all fields: BibTeX block at `literature_ring_size.md`:352 ff. | none |
| BusicMairesseMarcovici2013 | read in full (publisher PDF) by the literature session of v0.2 and by the ring-size study session. Not cited in the fragment (cut for length) | `literature_ring_size.md`:184, `verify_ring_size/literature/literature_check.md`:46 | all fields: BibTeX block at `literature_ring_size.md`:364 ff. | none |
| MarsanSablik2025 | read in the version arXiv:2403.19932v1 by the literature session of v0.2; read in part by the ring-size study session. Not cited in the fragment (cut for length) | `literature.md`:54, `literature_ring_size.md`:225, `literature_ring_size.md`:78 | all fields: BibTeX block at `literature_ring_size.md`:398 ff. | none |
| PowleyStepney2009 | read in full (author PDF, 12 pp.) by the ring-size study session. Not cited in the fragment (cut for length) | `literature_ring_size.md`:195, `literature_ring_size.md`:202 | all fields: BibTeX block at `literature_ring_size.md`:376 ff. (key there: PowleyStepney2009ECA); data consistent with dblp (`verify_ring_size/literature/literature_check.md`:379) | DOI ('no DOI') |
| AguiarSeverino | abstract and a search excerpt only (session of proofs_94_26); the statement was not checked by the verification of those proofs | `proofs_94_26/PROOF_26.md`:337, `proofs_94_26/PROOF_26.md`:338, `VERIFICATION_94_26.md`:263 | family names, title, journal, volume 24, number 2: `proofs_94_26/PROOF_26.md`:337-338 | given names, year, pages, DOI (BibTeX will warn about the empty year) |
| Krawczyk2015 | abstract and search excerpts only (session of proofs_43_142); journal data from citing reference lists, DOI not verified | `literature_addendum.md`:166, `literature_addendum.md`:170, `VERIFICATION_43_142.md`:175 | all fields: `literature_addendum.md`:166 ff. | given names (initials only), DOI |
| ChuaEtAl2007 | abstract only (session of proofs_43_142); titles and the abstract quotation confirmed through the DOI record by the verification | `literature_addendum.md`:184, `literature_addendum.md`:189, `VERIFICATION_43_142.md`:181 | authors, title, journal (as abbreviated there), year, doi: `literature_addendum.md`:184 ff. | volume and pages ('volume and pages not seen'); the first half of the title is taken from the Part VII entry in the same lines |
| Jen1986 | abstract only (ring-size verification); not read by the study session | `literature_ring_size.md`:241, `verify_ring_size/literature/literature_check.md`:33, `verify_ring_size/literature/literature_check.md`:395 | all fields: BibTeX block at `literature_ring_size.md`:442 ff. | none |
| Jen1988 | abstract only (study session and ring-size verification, as shown in search results) | `literature_ring_size.md`:235, `verify_ring_size/literature/literature_check.md`:34, `verify_ring_size/literature/literature_check.md`:395 | all fields: BibTeX block at `literature_ring_size.md`:420 ff. (key there: Jen1988Cylindrical) | none |
| OEIS | entries and b-files read by the ring-size verification (oeis.org) | `verify_ring_size/literature/literature_check.md`:39, `verify_ring_size/literature/literature_check.md`:200, `verify_ring_size/literature/literature_check.md`:205 | entry numbers and host: `verify_ring_size/literature/literature_check.md`:39 | a title of the database, an author, a year: the repository documents write 'OEIS' only |

Summary by status (keys of `refs.bib`):

* **read in full** by at least one session: MartinOdlyzkoWolfram1984, Fuks2005, Fuks2006 (arXiv version),
  Fuks1997 (arXiv version), PitmanTang2018 (arXiv version), BagnoliBaiaMatteuzzi2025, Newton2018, Fedoriaka2025,
  Ellison1993 (OCR), BusicMairesseMarcovici2013, MarsanSablik2025 (arXiv version), PowleyStepney2009, OEIS (entries);
* **read in part**: Ellison2000, BhattacharjeeDas2019, Nordahl1989, Stricker2023, VoorheesBeauchemin2004;
* **abstract or search excerpts only**: Samuelson1994, NobeYura2004, NobeYura2007, ZhuRichard2026, AguiarSeverino,
  Wuensche2024, Krawczyk2015, ChuaEtAl2007, Jen1986, Jen1988, LiPackard1990 (one excerpt);
* **not obtained / not read**: Boccara1993, HattoriTakesue1991, NoldekeSamuelson1993, Young1993,
  FreidlinWentzell2012, Bagnoli2024 (the chapter), WuenscheLesser1992;
* **no record of any reading**: Wolfram1983 (and LiPackard1990 apart from the excerpt).

Consequence for the author's rule "cite only what a session has read": of the seventeen keys named in the task,
nine fail the rule when read strictly (Boccara1993, NobeYura2004, NobeYura2007, Samuelson1994,
NoldekeSamuelson1993, Young1993, FreidlinWentzell2012, Wolfram1983, LiPackard1990), one is cited in a version that
was not read (Bagnoli2024) and one was seen in search excerpts only (ZhuRichard2026). The fragment cites these
only with the status written next to them or in the lists at the end of `related_work.tex`, and every entry that
was not read carries a `note` field saying so, which the style prints. Wolfram1983 and LiPackard1990 are in
`refs.bib` because the task asked for them; the fragment does not cite them. Whether such references may be
cited at all is the author's decision.

## 2. The author's short names against the documents

* **"Boccara 1993"**: matches the documents after the correction B6 (`VERIFICATION_43_142.md`:187-190); the
  reference lists of Fuks print 1992 (`literature_addendum.md`:257). The text was not obtained by anyone.
* **"Fukś 2005"**: matches. Complex Systems 16, 123-138, footer 2005 (`literature_addendum.md`:255; `verify_43_142/literature/lit_check_43_142.md`:37).
* **"Fukś 2006"**: **no repository document has a paper of Fukś dated 2006.** The second paper of Fukś that the
  proofs credit is "Second order additive invariants in elementary cellular automata", arXiv:nlin/0502037v1 of
  17 February 2005 (`literature_addendum.md`:299), whose journal version has another title and is dated 2007 (Fundamenta
  Informaticae 78, 329-341; `literature_addendum.md`:256; not seen). The verification calls it "Fukś 2007" (`VERIFICATION_43_142.md`:192 ff.). The
  key Fuks2006 is kept because the task fixes the key; the entry has year 2005 and describes the preprint that
  was read. Other papers of Fukś in the documents: 1997 (key Fuks1997), 1998 with Boccara (`literature_addendum.md`:261), 1999
  (obtained, not read; `literature_addendum.md`:265), a book of 2023 (not obtained; `literature_addendum.md`:318).
* **"Nobe, Yura 2004, 2007"**: both exist in the documents with full data; **neither was read**
  (`literature_ring_size.md`:246; `literature_addendum.md`:130). A third item, RIMS Kokyuroku 1541 (2007) 178-191, is named with data
  "as given in the task, not verified" (`literature_addendum.md`:127-128); no entry was made for it.
* **"Martin, Odlyzko, Wolfram 1984"**: matches; read in full by the ring-size verification only.
* **"Samuelson 1994", "Nöldeke and Samuelson 1993", "Ellison 2000"**: match; see section 1 for what was read.
  Ellison also names a paper of Nöldeke and Samuelson of 1997 (`verify_ring_size/literature/ellison2000_published_reading_notes.md`:56); the repository has no data for it.

## 3. Sources that the repository documents name as not read or not reachable

From `literature.md` (v0.2): `literature.md`:9 and the table from `literature.md`:81: Young 1993; Kandori, Mailath,
Rob 1993; Ellison 1993 (read later by the ring-size study); Ellison 2000 (read in part later); Freidlin and
Wentzell, ch. 6; Ventcel and Freidlin 1970; Leighton and Rivest 1986; Anantharam and Tsoucas 1989; Chu and Liu
1965; Grassmann, Taksar, Heyman 1985 (abstract); O'Cinneide 1993; Catoni 1992 (abstract), 1999; Trouvé 1996
(abstract); Wicks and Greenwald 2005 and Betz and Le Roux 2016 (search excerpts); Wuensche and Lesser 1992;
Mairesse and Marcovici 2014; Gács 2001; Toom 1980. The ACRI chapter of Bagnoli et al. (`literature.md`:60).
The verification of v0.2 did not check `literature.md` beyond the Bagnoli entry (`VERIFICATION_v02.md`:81).

From `literature_ring_size.md`: hosts refused (`literature_ring_size.md`:61, `literature_ring_size.md`:67, `literature_ring_size.md`:68 and
neighbours); closed access (`literature_ring_size.md`:71); partial readings (`literature_ring_size.md`:74, `literature_ring_size.md`:76,
`literature_ring_size.md`:77, `literature_ring_size.md`:78); Section 2 "located but NOT read": Jen 1988 (two papers; `literature_ring_size.md`:235),
Jen 1986 (`literature_ring_size.md`:241), Jen 1989/1990 (`literature_ring_size.md`:242), Nobe and Yura 2004 and 2007
(`literature_ring_size.md`:243, `literature_ring_size.md`:247), Wuensche and Lesser 1992 (`literature_ring_size.md`:249), Wuensche's jump-graph texts
(`literature_ring_size.md`:251, `literature_ring_size.md`:252, `literature_ring_size.md`:253), Martínez et al. (`literature_ring_size.md`:255), the Wolfram Atlas
(`literature_ring_size.md`:256), Mairesse and Marcovici 2014 (`literature_ring_size.md`:257), the literature on asynchronous updating
(`literature_ring_size.md`:258 ff.), Kanada 1994 (`literature_ring_size.md`:264).

From the ring-size verification: `verify_ring_size/literature/literature_check.md`:33, `verify_ring_size/literature/literature_check.md`:34, `verify_ring_size/literature/literature_check.md`:36, `verify_ring_size/literature/literature_check.md`:37, `verify_ring_size/literature/literature_check.md`:44, `verify_ring_size/literature/literature_check.md`:45,
`verify_ring_size/literature/literature_check.md`:47 (Hedlund 1969, Amoroso and Patt 1972, Sutner, Voorhees: not obtained); hosts refused
(`verify_ring_size/literature/literature_check.md`:49); Section 4 (`verify_ring_size/literature/literature_check.md`:391, `verify_ring_size/literature/literature_check.md`:395, `verify_ring_size/literature/literature_check.md`:400, `verify_ring_size/literature/literature_check.md`:402, `verify_ring_size/literature/literature_check.md`:404,
`verify_ring_size/literature/literature_check.md`:406: Ellison 2000, journal pp. 18-19, 21, 27, 32-35, 40-45); summary in `VERIFICATION_ring_size.md`
(`VERIFICATION_ring_size.md`:380, `VERIFICATION_ring_size.md`:382); no literature search for the two theorems after they were proved (`VERIFICATION_ring_size.md`:400;
`literature_ring_size.md`:48).

From `literature_addendum.md`: access (`literature_addendum.md`:28, `literature_addendum.md`:30, `literature_addendum.md`:31); A1 Zhu and
Richard: PDF, complete HTML, equation (4), figures, reference list (`literature_addendum.md`:46); A2 Nobe and Yura: both texts
(`literature_addendum.md`:133); A3 Nordahl: pp. 63-67 and Section 4 (`literature_addendum.md`:145), and the appendix of Hurd
(`literature_addendum.md`:158); A4 Krawczyk: the body and the entries of Table 4 (`literature_addendum.md`:170); A5 Chua et al.: both full
texts (`literature_addendum.md`:189); A6 Stricker: 19 PDF pages (`literature_addendum.md`:207); A7 Voorhees and Beauchemin: pp. 54-65, 72-78
and the arXiv version (`literature_addendum.md`:225); B2 journal version, B3 Boccara, B5 Capcarrere, Sipper, Tomassini, B6
Belitsky and Ferrari beyond arXiv pp. 1-6, B7 Boccara and Fukś beyond arXiv pp. 1-4 (rows `literature_addendum.md`:256 to
`literature_addendum.md`:261); Hattori and Takesue 1991, Krug and Spohn 1988, Belitsky and Ferrari 1995, Boccara "Eventually
number-conserving cellular automata", the Wolfram Atlas entries for rules 43 and 142, Fukś 1999 (obtained, not
read) (`literature_addendum.md`:263-266); still unread after the update: Boccara 1993, Hattori and Takesue
1991, Fukś 2007 (journal version), Fukś's book of 2023 (`literature_addendum.md`:318 ff.); open items (`literature_addendum.md`:343 ff.).

From `VERIFICATION_43_142.md`: `VERIFICATION_43_142.md`:175 ff. (items B2, B3, B5, A1, A2, A4, A5 could not be lifted to "read");
`VERIFICATION_43_142.md`:250 (also NKS p. 1023); `VERIFICATION_43_142.md`:237 (Hellouin de Menibus and Sablik 2017, Bramson and Neuhauser
1994: excerpts only); `VERIFICATION_43_142.md`:255 ff.

From `proofs_94_26/`: Aguiar and Severino (abstract and excerpt), Li and Packard (excerpt) (`proofs_94_26/PROOF_26.md`:337 ff.);
Schuele and Stoop, Flocchini and Cezar (excerpts); the relation of the walls of rule 94 to rule 18 "was not
searched for" (`proofs_94_26/PROOF_94_converse.md`:385 ff., `proofs_94_26/PROOF_94_converse.md`:390).

## 4. Errors and inconsistencies found in the sources (reported, not corrected)

1. **Stale notes in the BibTeX section of `literature_ring_size.md`.** `literature_ring_size.md`:417: "Not read ... Statement
   numbers known only via PowleyStepney2009Linear"; `literature_ring_size.md`:483: "Not read (search snippet only)";
   `literature_ring_size.md`:349: "Published journal text not read". The update section of the same file says that the
   verification read Martin, Odlyzko and Wolfram in full, Fedoriaka in full and the published Ellison in part
   (`literature_ring_size.md`:15 ff.). The BibTeX notes were not updated. `refs.bib` follows the update section.
2. **Page range of Nobe and Yura (2007).** `literature_ring_size.md`:471 has the first page only; `literature_addendum.md`:126 has
   7159-7174. `refs.bib` uses the range.
3. **The short description of the chain lemma omits its radius condition.** `report_ring_size.md`:95
   (same text in `code/ring_size/literature_section.md`:30-32): "the lemma that a set reachable from every other
   limit set by a chain of single mutations is selected". Ellison's sentence, as the verification read it, has the
   additional hypothesis on the radius (`verify_ring_size/literature/ellison2000_published_reading_notes.md`:56; `verify_ring_size/literature/ellison2000_published_reading_notes.md`:58). `related_work.tex` states the condition.
4. **The note v0.2 cites texts that no session read.** Young 1993 (`note/note_v0.2.tex`:193) and Freidlin and Wentzell
   (`note/note_v0.2.tex`:98) are recorded as not read (`literature.md`:85, `literature.md`:89); for Wolfram 1983 and Li and
   Packard 1990 (`note/note_v0.2.tex`:39, `note/note_v0.2.tex`:78) the repository has no record of a reading; the note's entry for
   Bagnoli et al. is the LNCS chapter (`note/note_v0.2.tex`:230), while only the arXiv version was read (`literature.md`:60).
   This is the state of a source that the task says is to be used as it stands; it conflicts with the rule "cite
   only what a session has read" and is reported for the author's decision.
5. **The note does not contain its own version DOI.** The task says "its Zenodo DOI as given in the note and the
   repo's CITATION.cff". `note/note_v0.2.tex`:227 gives 10.5281/zenodo.23399101 (version 0.1) and 10.5281/zenodo.23399100
   (all versions); the links of `note/note_v0.2.pdf` are these two (checked by scanning the PDF). The version DOI
   10.5281/zenodo.24093547 stands in `CITATION.cff`:23-24, `README.md`:15 and `report_ring_size.md`:4.
   `CITATION.cff` itself describes version 0.3 (`CITATION.cff`:8).
6. **Task text against the documents: what Theorem A restates.** See the first note of `attributions.md`.
7. Known and already recorded in the repository, repeated here because the paper depends on it: the wording
   point B4 in the report's proof of Lemma 2 (`VERIFICATION_43_142.md`:95), which the repository lists "for its next revision"
   (`VERIFICATION_43_142.md`:3 ff.). It concerns the track that writes Theorem A.

No mathematical error was looked for or found by this track.

## 5. Credits given in the fragment, with the repository line that states the attribution

| credit in the fragment | key(s) | repository line |
|---|---|---|
| stochastic potential | Young1993 | `note/note_v0.2.tex`:193; not read: `literature.md`:85 |
| minimum-cost trees | FreidlinWentzell2012 via Ellison2000, Section 6.3 | `verify_ring_size/literature/ellison2000_published_reading_notes.md`:64; `note/note_v0.2.tex`:98; not read: `literature.md`:89 |
| least stochastic potential = stochastically stable | Newton2018 | `literature.md`:77 |
| Markov chain tree theorem | PitmanTang2018 | `note/note_v0.2.tex`:199; `literature.md`:34 |
| order formula, reduction to cycles | PeterleinNote | `note/note_v0.2.tex`:195; `literature.md`:133 |
| Theorem 2 of Ellison | Ellison2000 | `verify_ring_size/literature/literature_check.md`:128; `literature_ring_size.md`:30 |
| chain lemma | Ellison2000 attributing to Samuelson1994, NoldekeSamuelson1993 | `verify_ring_size/literature/ellison2000_published_reading_notes.md`:56; `VERIFICATION_ring_size.md`:267; `literature_ring_size.md`:21 |
| mutation-connected and locally stable components | Samuelson1994, NoldekeSamuelson1993 | `VERIFICATION_ring_size.md`:274; `report_ring_size.md`:163 |
| single-flip chain between attractors | Bagnoli2024, BagnoliBaiaMatteuzzi2025 | `literature_ring_size.md`:111; `note/note_v0.2.tex`:193 |
| jump graph | Wuensche2024 | `literature_ring_size.md`:252; `verify_43_142/literature/lit_check_43_142.md`:74 |
| rule 90 on 2^j cells; fixed points for 3 dividing n | MartinOdlyzkoWolfram1984 | `verify_ring_size/literature/literature_check.md`:183; `verify_ring_size/literature/literature_check.md`:257; `report_ring_size.md`:113; `report_ring_size.md`:119 |
| rule 154 reversible on odd rings | BhattacharjeeDas2019, Fedoriaka2025, NobeYura2004 | `verify_ring_size/literature/literature_check.md`:157; `verify_ring_size/literature/literature_check.md`:159; `verify_ring_size/literature/literature_check.md`:163; `report_ring_size.md`:253 |
| linearisable reversible rules | NobeYura2007 | `literature_addendum.md`:135 |
| rule-90 pattern of rules 26, 154; reduction for rule 18 | OEIS; MartinOdlyzkoWolfram1984, Section 5 | `verify_ring_size/literature/literature_check.md`:200; `verify_ring_size/literature/literature_check.md`:203; `report_ring_size.md`:416 ff. |
| rules simulating rule 90 | Nordahl1989 | `literature_addendum.md`:147 ff.; `literature_addendum.md`:153 |
| rules 26, 154 on finite rings, further | OEIS (A334504), Stricker2023, ZhuRichard2026, AguiarSeverino | `verify_ring_size/literature/literature_check.md`:205; `literature_addendum.md`:212; `literature_addendum.md`:50; `proofs_94_26/PROOF_26.md`:337 |
| wall map | Boccara1993 via Fuks2005; Fuks2006 | `proofs_43_142/PROOF_43_142.md`:755 ff.; `literature_addendum.md`:255; `literature_addendum.md`:304 |
| conserved number of blocks 10 | Fuks2005; Fuks2006; HattoriTakesue1991 | `literature_addendum.md`:255; `literature_addendum.md`:307; `literature_addendum.md`:272 |
| rule 184 on rings | Fuks1997 | `proofs_43_142/PROOF_43_142.md`:765; `literature_addendum.md`:258 |

## 6. Changes of notation and wording against the sources

* Ring size: the references' N and L are written n; "site" becomes "cell" (NOTATION.md).
* Codes: the report's "codes 3, 5, 6" (`report_ring_size.md`:119 ff.) are written as the words 011, 101, 110 (code number
  4a + 2b + c). Blocks of two cells ("blocks 10", "00", "11") are typeset with `\code`.
* G1 is `\Gone`, S is `\Sel`, gamma_min is `\gmin`, k* is `\kst`; the quantity c of PROOF_26.md is chi; the frozen
  set W(x) of PROOF_94.md is described in words ("the frozen occurrences of 101"); the wall word d is delta.
* Ellison's symbols R(Omega) and CR*(Omega) are not used, because R is the path resistance in the paper; the text
  says "radius" and "modified coradius c". Ellison's "limit set", "long-run stochastically stable set" and "single
  mutation" are kept as words; the "long-run stochastically stable set" is shortened to "stochastically stable
  set"; "single mutation" corresponds to a single flip, that is, to an edge of G1 (`verify_ring_size/literature/literature_check.md`:73).
* "Reversible" (the references) and "bijective" (the proofs) are used for the same property of the global map.
* "Null configuration" (Martin, Odlyzko and Wolfram) is kept in the sentence that reports their lemma; elsewhere
  the paper says zero state.
* The report's "radius r(C) >= 2" is written "no single flip leaves" (NOTATION.md).
* "Not found in the sources read" (the documents) is written "not found in the sources reached" (the form
  fixed by the task and by `VERIFICATION_43_142.md`:250 ff.).

## 7. General facts used beyond the shared statements of Section 2

None. The fragment contains no proof. It refers to `prop:order` and `thm:A` only.

## 8. \DATA items and numbers in the fragment

No `\DATA`, `\GAP` or `\SOURCEERR` marker is used. No number of the fragment comes from an enumeration or a data
file of the repository. The numbers that are typed describe the literature or the searches and stand in the
documents: 88 classes and 17 cells (`literature_ring_size.md`:270 ff.; `literature_ring_size.md`:113); 4 <= n <= 20 (`verify_ring_size/literature/literature_check.md`:159 ff.);
equations (28), (29) (`literature_addendum.md`:304); floor((n - 2)/2) (`literature_addendum.md`:258); 15 queries (`literature_addendum.md`:19 ff.) and 9
queries (`VERIFICATION_43_142.md`:241 ff.); two queries (`proofs_94_26/PROOF_26.md`:337; `proofs_94_26/PROOF_94_converse.md`:385); seven sources (`literature_addendum.md`:6 ff.);
pages, sections and lemma numbers of the references as in section 9. In the note the two values 88 and 17 are the
macros `\NumClasses` and `\BBMLattice` (`note/note_v0.2.tex`:193); if the editor wants them through a script, they can be
taken from `note/numbers_v02.tex`.

## 9. Second pass: every sentence of the fragment against the repository

RW = `related_work.tex`, IK = `intro_known.tex`; the number is the line of the .tex file on which the sentence
(or its marked part) starts.

| place | statement | covered by | remark |
|---|---|---|---|
| RW:4 | gamma is the stochastic potential of Young | `note/note_v0.2.tex`:193 | Young not read: `literature.md`:85 |
| RW:5 | stochastically stable = least stochastic potential, stated with reference to Young in the survey of Newton | `literature.md`:77 | the survey also cites Kandori, Mailath and Rob; left out for length |
| RW:6 | Ellison, Section 6.3, refers the description by minimum-cost trees to Freidlin and Wentzell | `verify_ring_size/literature/ellison2000_published_reading_notes.md`:62, `verify_ring_size/literature/ellison2000_published_reading_notes.md`:64 | "(see [FreidlinWentzell2012])": the edition is the one the note cites (`note/note_v0.2.tex`:234), not one that Ellison cites; not read: `literature.md`:89 |
| RW:8 | the note takes the Markov chain tree theorem from Pitman and Tang, Theorem 1.1, and proves the reduction to cycles itself | `note/note_v0.2.tex`:199, `literature.md`:34, `literature.md`:144 |  |
| RW:9 | the cycle-reduced formula was not found in the sources read for the note | `literature.md`:133 |  |
| RW:11 | Theorem 2 of Ellison, p. 30: radius > modified coradius implies containment and the waiting-time bound | `verify_ring_size/literature/literature_check.md`:128, `verify_ring_size/literature/ellison2000_published_reading_notes.md`:9, `literature_ring_size.md`:30 | radius and modified coradius are not defined in the fragment (cut for length); definitions: `literature_ring_size.md`:148, `literature_ring_size.md`:155 |
| RW:14 | the chain lemma, in Ellison's words, attributed to Samuelson (1994) and Noeldeke and Samuelson (1993, 1997) | `verify_ring_size/literature/ellison2000_published_reading_notes.md`:56, `verify_ring_size/literature/ellison2000_published_reading_notes.md`:58, `verify_ring_size/literature/ellison2000_published_reading_notes.md`:60, `verify_ring_size/literature/literature_check.md`:65 |  |
| RW:18 | Theorem A restates these results: first sentence and the two steps (Lemmas 1, 2 of the report) correspond to the component results | `report_ring_size.md`:163, `VERIFICATION_ring_size.md`:274, `verify_ring_size/literature/literature_check.md`:89, `verify_ring_size/literature/literature_check.md`:92 |  |
| RW:21 | the use of Theorem A for a set that no single flip leaves and that every other cycle reaches by edges of G1 is in substance the chain lemma | `VERIFICATION_ring_size.md`:267, `verify_ring_size/literature/literature_check.md`:73, `report_ring_size.md`:217, `VERIFICATION_ring_size.md`:340 |  |
| RW:22 | primary texts not read; the correspondence rests on Ellison's text, the abstract of Samuelson (1994) and secondary descriptions | `literature_ring_size.md`:26, `report_ring_size.md`:163, `VERIFICATION_ring_size.md`:382 |  |
| RW:26 | Bagnoli et al.: 88 classes, 17 cells, at most one flip applied to attractor states; count over states of a cycle and single flips; normalise; iterate | `literature_ring_size.md`:111, `literature_ring_size.md`:113, `literature_ring_size.md`:270, `literature_ring_size.md`:110 | both keys are cited: the chapter (not read) and the extended version (read) |
| RW:30 | no costs above one, no potentials, ring size not varied | `literature_ring_size.md`:111, `literature_ring_size.md`:115, `literature.md`:65 |  |
| RW:31 | by the note: correct leading-order law when G1 has a single closed class, which is then the selected set; their table determines the selected cycles of all classes at 17 cells | `note/note_v0.2.tex`:193, `VERIFICATION_v02.md`:44 |  |
| RW:33 | jump graph of Wuensche: jumps between basins under single flips of attractor states (search excerpt) | `literature_ring_size.md`:252, `literature_ring_size.md`:254, `verify_43_142/literature/lit_check_43_142.md`:74 | status given in the list at the end |
| RW:36 | rule 90 on 2^j cells: every configuration evolves to the null configuration (MOW Lemma 3.5) | `verify_ring_size/literature/literature_check.md`:183, `VERIFICATION_ring_size.md`:297, `report_ring_size.md`:113 |  |
| RW:38 | for 3 \| n the non-null fixed points of rule 90 are the three shifts of 011011... (MOW Lemma 3.7); rules 94 and 90 agree on the codes 011, 101, 110 | `verify_ring_size/literature/literature_check.md`:257, `VERIFICATION_ring_size.md`:316, `report_ring_size.md`:119 |  |
| RW:40 | rule 154 reversible at odd size: Bhattacharjee and Das; Fedoriaka (computation for N in [4, 20] with constructions); Nobe and Yura 2004 by abstract and a search excerpt | `verify_ring_size/literature/literature_check.md`:157, `verify_ring_size/literature/literature_check.md`:159, `verify_ring_size/literature/literature_check.md`:163, `literature_ring_size.md`:245, `VERIFICATION_ring_size.md`:291 |  |
| RW:42 | Nobe and Yura 2007, by its abstract, linearises a class of reversible rules | `literature_addendum.md`:135, `literature_ring_size.md`:247 |  |
| RW:43 | rules 26 and 154 give the rule-90 pattern from a single cell on the line: comment in OEIS A070886 | `verify_ring_size/literature/literature_check.md`:200, `VERIFICATION_ring_size.md`:300 |  |
| RW:44 | MOW Section 5 uses the reduction for rule 18; Nordahl lists rules 26, 94, 154 among those "known to be capable of simulating rule 90" | `verify_ring_size/literature/literature_check.md`:203, `literature_addendum.md`:147, `literature_addendum.md`:153 | one phrase of Nordahl is quoted, as the addendum quotes it |
| RW:46 | rule 26 on rings in OEIS A334504; rules 26 and 154 in Stricker; rule 154 in Zhu and Richard; both in Aguiar and Severino | `verify_ring_size/literature/literature_check.md`:205, `literature_addendum.md`:209, `literature_addendum.md`:212, `literature_addendum.md`:50, `proofs_94_26/PROOF_26.md`:337 | contents not described in the fragment (cut for length); see attributions.md |
| RW:48 | wall map (rule 60) transforms rule 142 into rule 226: Fuks 2005, credited to Boccara; both identities: eqs. (28), (29) of the arXiv text of Fuks, same credit | `literature_addendum.md`:255, `proofs_43_142/PROOF_43_142.md`:757, `literature_addendum.md`:304, `proofs_43_142/PROOF_43_142.md`:759 |  |
| RW:51 | number of blocks 10 conserved (half the number of walls): Fuks 2005 for rule 142; Fuks arXiv text for both rules, from Hattori and Takesue | `literature_addendum.md`:255, `literature_addendum.md`:272, `literature_addendum.md`:307 |  |
| RW:53 | rule 184 on a ring: no block 00 or no block 11 after floor((n - 2)/2) steps (Fuks 1997) | `proofs_43_142/PROOF_43_142.md`:765, `literature_addendum.md`:258, `VERIFICATION_43_142.md`:168 | "proof sketched there" and the case of density 1/2 were cut for length |
| RW:57 | no claim of novelty | `verify_ring_size/part2_154/PROOF_154.md`:8, `verify_ring_size/part2_94/PROOF_94.md`:20, `proofs_43_142/PROOF_43_142.md`:755, `proofs_94_26/PROOF_26.md`:342, `proofs_94_26/PROOF_94_converse.md`:385 |  |
| RW:59 | (i) gamma_min = m - 1 not found | `verify_ring_size/literature/literature_check.md`:101, `report_ring_size.md`:163, `literature_ring_size.md`:21 |  |
| RW:60 | (ii) rule 154: no statement on rings of 2^k cells, no conjugacy or factor map onto rule 90; nothing on the permutation of M | `report_ring_size.md`:99, `literature_ring_size.md`:283, `verify_ring_size/literature/literature_check.md`:211, `literature_addendum.md`:158, `literature_addendum.md`:120 | WEAKEST ITEM: for the permutation of M the only explicit negatives are for Nordahl (pages read) and for the excerpts of Zhu and Richard; no session searched for it (`VERIFICATION_ring_size.md`:400); the fragment says so two sentences later |
| RW:62 | (iii) rule 94: one-flip stability of the crystal, frozen word 101, classification of periodic states (window classification), closed class | `report_ring_size.md`:119, `verify_ring_size/literature/literature_check.md`:260, `proofs_94_26/PROOF_94_converse.md`:388 |  |
| RW:64 | (iv) rules 43, 142: run-length description, unique cycle with n/2 walls, case 4 \| n; Lemmas 3, 4 in the form used | `literature_addendum.md`:278, `proofs_43_142/PROOF_43_142.md`:768, `proofs_43_142/PROOF_43_142.md`:763, `VERIFICATION_43_142.md`:241 |  |
| RW:66 | (v) rule 26: the quantity c (chi), the domain states, the path to the zero state | `proofs_94_26/PROOF_26.md`:342 |  |
| RW:67 | (vi) which cycles small noise selects as a function of n | `literature_ring_size.md`:270, `literature_ring_size.md`:278, `literature_addendum.md`:284, `literature.md`:110 | for one ring size, 17, the table of Bagnoli et al. determines the selected cycles (sentence above) |
| RW:68 | provisional; 15 queries and 9 in the verification (43, 142); two queries each (26; 94 with 3 not dividing n), not checked by the verification | `literature_addendum.md`:19, `literature_addendum.md`:290, `VERIFICATION_43_142.md`:241, `proofs_94_26/PROOF_26.md`:337, `proofs_94_26/PROOF_94_converse.md`:385, `VERIFICATION_94_26.md`:263 |  |
| RW:70 | rule 154 and rule 94 with 3 \| n: no search after the proofs; seven sources named by an outside search were looked up; the outside search was not repeated | `VERIFICATION_ring_size.md`:400, `literature_ring_size.md`:48, `literature_addendum.md`:6 |  |
| RW:73 | list of what was not obtained or not read | `literature_addendum.md`:257, `literature_addendum.md`:263, `verify_ring_size/literature/literature_check.md`:45, `literature.md`:85, `literature.md`:89, `literature_ring_size.md`:249, `literature_ring_size.md`:76, `literature_addendum.md`:299, `literature_addendum.md`:318, `literature_ring_size.md`:256, `literature_addendum.md`:158 |  |
| RW:77 | list of abstract-only and excerpt-only references | `verify_ring_size/literature/literature_check.md`:44, `literature_ring_size.md`:243, `literature_addendum.md`:130, `literature_addendum.md`:41, `proofs_94_26/PROOF_26.md`:337, `literature_ring_size.md`:252, `literature_addendum.md`:170, `literature_addendum.md`:189, `verify_ring_size/literature/literature_check.md`:33, `verify_ring_size/literature/literature_check.md`:34 |  |
| RW:79 | list of references read in part | `verify_ring_size/literature/literature_check.md`:31, `verify_ring_size/literature/literature_check.md`:42, `literature_addendum.md`:144, `literature_addendum.md`:207 |  |
| RW:80 | the remaining cited references were read, some as preprints: Newton2018, PitmanTang2018 (arXiv), BagnoliBaiaMatteuzzi2025 (arXiv), MartinOdlyzkoWolfram1984, Fedoriaka2025, OEIS, Fuks2005, Fuks2006 (arXiv), Fuks1997 (arXiv); PeterleinNote is a source document | `literature.md`:76, `literature.md`:33, `literature_ring_size.md`:110, `verify_ring_size/literature/literature_check.md`:30, `verify_ring_size/literature/literature_check.md`:40, `verify_ring_size/literature/literature_check.md`:39, `literature_addendum.md`:255, `literature_addendum.md`:299, `literature_addendum.md`:258 |  |
| IK:2 | selection described by the stochastic potential of Young within the theory of Freidlin and Wentzell; orders determined in the note | `note/note_v0.2.tex`:193, `note/note_v0.2.tex`:98, `note/note_v0.2.tex`:195 | neither Young nor Freidlin and Wentzell was read; the paragraph points to the subsection for that |
| IK:5 | selection from steps of cost one is known: Ellison attributes a lemma of this kind to Samuelson and to Noeldeke and Samuelson; Theorem A restates results of these authors | `report_ring_size.md`:91, `report_ring_size.md`:163, `VERIFICATION_ring_size.md`:267, `VERIFICATION_ring_size.md`:274 |  |
| IK:8 | Bagnoli et al.: chain of single-flip jumps between attractors, 88 classes, one ring size, 17 | `literature_ring_size.md`:270, `literature_ring_size.md`:113, `note/note_v0.2.tex`:193 | cites the chapter key only; the version read is named in the subsection |
| IK:10 | rule 90 nilpotent on 2^k cells; fixed points for 3 \| n (MOW) | `verify_ring_size/literature/literature_check.md`:183, `verify_ring_size/literature/literature_check.md`:257 |  |
| IK:12 | rule 154 reversible on rings of odd size | `verify_ring_size/literature/literature_check.md`:157, `verify_ring_size/literature/literature_check.md`:159, `verify_ring_size/literature/literature_check.md`:163 |  |
| IK:13 | wall map carries rules 142 and 43 onto rules 226 and 184; both conserve the number of walls | `proofs_43_142/PROOF_43_142.md`:755, `literature_addendum.md`:318 |  |
| IK:15 | selection as a function of n not found in the sources reached; pointer to the subsection | `literature_ring_size.md`:270, `literature_addendum.md`:284 |  |

Result of the pass: no sentence without a repository line. One item is covered only weakly and is marked above
(item (ii), the permutation of the set M of rule 154).

## 10. Compile check and length

* `harness.tex` (the copy with the three marker macros added) with `fragment.tex` = `related_work.tex` followed by
  `intro_known.tex`, pdflatex twice in the conda environment `latex`: **0 errors**, no undefined `\ref`, no
  multiply defined label, no overfull box; the only warnings are the undefined `\cite` keys (the harness has no
  bibliography).
* Length. In `harness.pdf` (citations print as "[?]") the fragment takes 1.11 page
  (771.1 pt of a text height of 697.1 pt). With numeric citation labels, as the style "plain"
  will print them (measured in a copy of the harness with a stand-in list of numbered `\bibitem`s):
  `related_work.tex` takes **0.905 page** (631.0 pt, heading included), against a budget of
  0.9; `intro_known.tex` takes **11 lines** of text, against a budget of 12.
* The subsection is one line over the budget (0.905 against 0.9). A trim of about a third of a line in the first
  paragraph, which removes that line, was prepared and could not be applied in this session; it is listed in
  section 11.
* **BibTeX.** The TeX installation of the environment `latex` contains no `.bst` file at all (`kpsewhich plain.bst`
  finds nothing), so `refs.bib` could **not** be processed with the style "plain" here. It was parsed by the
  BibTeX program of the same installation with a minimal style that only reads the database: no error and no
  warning from the parser. What "plain" will warn about, by its rules: AguiarSeverino has no year;
  several entries have a single-word author (Fuks, Boccara, Hattori and Takesue, Aguiar and Severino: family
  names only). The `doi` fields are not printed by "plain".
* **Field check by script.** Every field value of every entry of `refs.bib` (the `note` fields apart) was searched,
  after removal of TeX accents and braces, in the repository documents named in section 1. All were found
  verbatim except three values that are composed from data of one line each: the `howpublished` of
  HattoriTakesue1991 ("Physica D 49 (1991) 295-322" in the document), the title of ChuaEtAl2007 (the document
  abbreviates the common first half of the title of Part VIII by "..." after giving it for Part VII), and the title
  of the OEIS entry (the three entry numbers).

## 11. Not done, cut, or not checked

* **Not applied:** the last trim of `related_work.tex`. The edit was held by the platform's safety check
  ("could not run"), and the instruction in that case is not to repeat it by another route. The four changes, all
  in the first paragraph: "is stated, with reference to Young, in the survey [..], and Ellison" -> "...; Ellison";
  "that formula" -> "this formula"; "correspond to the results of these authors on" -> "correspond to their
  results on"; "the correspondence rests on" -> "this rests on". Before the sentence on the seven
  looked-up sources was added the subsection measured 0.888 page; that sentence added one line. The last line of
  the first paragraph is about one third full, and the four changes remove more than that; the result was not
  measured.
* **Cut for length** from `related_work.tex` (entries stay in `refs.bib`, the facts in `attributions.md`):
  the definitions of radius and modified coradius; Kandori, Mailath and Rob; Voorhees and Beauchemin (point
  mutations between basins; the regime of slow mutations named and not treated, `literature_addendum.md`:228 ff.); Marsan and
  Sablik (infinite lattices, `literature_ring_size.md`:228); the two parity effects nearest to a ring-size dependence, Ellison
  1993 and Busic, Mairesse, Marcovici 2013 (`literature_ring_size.md`:270 ff.); Powley and Stepney (rule 154 grouped with the linear
  rules, `literature_ring_size.md`:202); the contents of the observations of Stricker, of Zhu and Richard and of Aguiar and
  Severino; the fractions of periodic states of rule 90 at other n; "proof sketched there" for Fuks 1997;
  Krawczyk, Chua et al. and Jen appear only in the list of what was seen as abstracts.
* **Not checked:** no reference was opened by this track (no network); every statement about a reference rests
  on the repository documents. The bibliographic data were not compared with any external record. `refs.bib`
  was not run through "plain" (see section 10). The labels of the rule-specific theorems of the other tracks
  are unknown to this track, so the list "what was not found" names the statements in words and has no `\ref`
  to them.
* **Not searched:** no new literature search was made. In particular the gap recorded in the repository stays
  open: no session searched for prior statements of the theorems on rule 154 and on rule 94 with 3 | n after
  they were proved (`VERIFICATION_ring_size.md`:400).
