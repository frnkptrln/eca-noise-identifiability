# Literature check of the ring-size study (branch `ring-size-mechanisms`)

Scope: the literature side of `report_ring_size.md`, `literature_ring_size.md`, `code/ring_size/ellison_remark.md`,
`code/ring_size/literature_section.md`, `PR_DRAFT.md` (and `PREDICTIONS_ring_size.md` where it mentions Ellison).
Nothing in the repository was changed. No statement below asserts novelty; where nothing was located the wording is
"not found in the sources read".

Reading rule. "Read" means the text was in front of me in this session: a text layer I printed, or a page image
rendered to me. Statements taken from a publisher abstract or a search-result fragment are marked as such.
Line numbers refer to the files at commit 1e256cd (`PR_DRAFT.md` is untracked).

Declared limits (details in Section 4).
* Wuensche-Lesser (1992) and the Wolfram Atlas were **not obtained**. The numerical comparison asked for was done
  against substitutes: Martin-Odlyzko-Wolfram Tables 1 and 2, OEIS b-files, and Table 2 of Bagnoli et al.
* Jen (1986, 1988): abstracts only. Samuelson (1994) and Noeldeke-Samuelson (1993): abstract / search fragments only;
  findings L1 and L2 rest partly on Ellison's own description of these papers (read) and on secondary sources, and
  are **provisional** on that point.
* Ellison (2000), published version: 15 of 29 pages read (all pages carrying Definition 1, radius, coradius,
  modified coradius, Theorems 1-3 and Section 6.2); the appendix lemmas were not read.
* The scanned Ellison PDF has no text layer. My first attempt to open it did not display the pages; notes written at
  that stage were discarded unused. Every statement about the published version below comes from page images that were
  displayed afterwards (`ellison2000_published_reading_notes.md`).

---

## 1. Sources and access status

| # | Source | Status | Version and route | What was read |
|---|---|---|---|---|
| 1 | Martin, Odlyzko, Wolfram (1984), Commun. Math. Phys. 93, 219-258 | **read in full** | author scan with text layer, content.wolfram.com (access approved) | all 40 pages (text layer; Table 2 column layout reassembled from the text layer; formulas partly lost in the layer) |
| 2 | Ellison (2000), Rev. Econ. Stud. 67, 17-45 | **read in part** | published version, ProQuest scan hosted at economics.mit.edu, 29 pages, page images | journal pp. 17, 20, 22-26, 28-31, 36-39 |
| 2a | Ellison, working paper January 1999 | read in part | web.mit.edu/gellison/www/basins.pdf, text layer (formulas garbled) + one rendered crop | location of Def. 1, Thms 1-3 by printed page; the sentence on printed p. 30 |
| 3 | Jen (1986), J. Stat. Phys. 43, 219-242 | **abstract only** | abstract as shown in search results (Springer / ADS / OSTI) | abstract |
| 4 | Jen (1988), "Cylindrical cellular automata", Commun. Math. Phys. 118, 569-590 | **abstract only** | abstract as shown in search results; a few disconnected fragments of the Project Euclid PDF in a search result | abstract |
| 5 | Jen (1988), "Linear cellular automata and recurring sequences in finite fields", Commun. Math. Phys. 119, 13-28 | **abstract only** | abstract fragment in search results | abstract fragment |
| 6 | Wuensche and Lesser (1992), atlas | **not obtained** | www.ddlab.org, ddlab.org, users.sussex.ac.uk approved but refused by the sandbox (address resolution) | nothing |
| 7 | Wolfram Atlas of Simple Programs | **not obtained** | atlas.wolfram.com approved but refused by the sandbox | nothing |
| 7a | NKS chapter 6 (PDF excerpt) | not re-read | files.wolframcdn.com, downloaded | only the statements that MOW confirms were cross-checked (L6, Section 3.4) |
| 8 | OEIS A085587, A334504, A334507, A401854, A334508, A070886, A071029 | **read** (entries and b-files) | oeis.org (access approved) | names, comments, links, b-files |
| 9 | Fedoriaka (2025), arXiv:2501.06648 v1 | **read in full** | text extraction via the alphaXiv connector | whole text incl. Table I |
| 10 | Bagnoli, Baia, Matteuzzi, arXiv:2406.15408 (title "Discrete System Phase Space Modification by Vanishing Noise") | read in part | text extraction via the alphaXiv connector | Table 2 (all 88 rows), surrounding text |
| 11 | Bhattacharjee and Das, arXiv:1903.06011, "On Finite 1-Dimensional Cellular Automata: Reversibility and Semi-reversibility" | read in part | text extraction via the alphaXiv connector | abstract, Example 2, Table 3 row lists, theorem statements (keyword scan) |
| 12 | Nobe and Yura (2004), J. Phys. A 37, 5789 | **abstract only** | abstract (fetch tool, IOP page in search results); Proposition 1 seen only as a ResearchGate search fragment | abstract |
| 13 | Samuelson (1994), J. Econ. Theory 64, 35-65 | **abstract only** | ScienceDirect abstract as shown in search results | abstract |
| 14 | Noeldeke and Samuelson (1993), Games Econ. Behav. 5, 425-454 | **not obtained** | closed; www.dklevine.com approved but refused | known only through Ellison (2000) pp. 36-38 (read) and secondary search fragments |
| 15 | Busic, Mairesse, Marcovici (2013) | header and Sect. 5.1 opening only | publisher PDF via fetch tool | citation line, p. 977 opening |
| 16 | Hedlund (1969), Amoroso-Patt (1972), Sutner, Voorhees | **not obtained** | not attempted beyond search | nothing |

Hosts approved by the user but still refused by the sandbox: projecteuclid.org, www.ddlab.org, ddlab.org,
atlas.wolfram.com, www.osti.gov, www.dklevine.com, link.springer.com, users.sussex.ac.uk, api.crossref.org, arxiv.org.
No mirror or proxy of these hosts was used. The Scite connector was not usable (no plan).

---

## 2. Findings

Severity: **major** = a result the study presents as its own is in the literature it cites or its direct ancestors;
**medium** = missing or imprecise attribution; **minor** = wording or bookkeeping.

### L1 (major). Lemma B is, in substance, a lemma of Samuelson (1994) and Noeldeke-Samuelson (1993, 1997); Ellison says so in the paper the study read.

* Location: `report_ring_size.md:137-153`; `code/ring_size/ellison_remark.md:1-7`; `PR_DRAFT.md:27-28`;
  `PREDICTIONS_ring_size.md:17-24` (G2); `literature_ring_size.md:92-124, 241-250` (Ellison summary, which does not
  mention the passage).
* Evidence (read): Ellison (2000), Sect. 6.2, journal pp. 37-38. In his words the earlier lemma says that a component
  of limit sets gets probability one in the limit if its radius condition holds and it "can be reached from any other
  limit set via a chain of single mutations", and he adds that this condition ensures CR*(Omega) = 1. The relation
  sign is printed "R(Omega) > 2" in both the journal scan and the working paper; with CR* = 1, Theorem 2 itself needs
  only R(Omega) > 1. Footnote 21 (p. 36) states that the Samuelson and Noeldeke-Samuelson lemmas follow from a
  modified-coradius computation.
* The same sentence is on printed p. 30 (PDF page 32) of the January 1999 working paper, i.e. inside the version
  `literature_ring_size.md` reports as read.
* Lemma B's hypotheses (every A_i has radius >= 2; every other cycle reaches A by one-flip edges) are this situation
  with Omega = A. What Lemma B states beyond it: Omega may be a rotation orbit of q cycles joined by two-flip edges,
  and the value gamma_min = m + q - 2. That value was not found in the sources read.
* Primary texts of Samuelson (1994) and Noeldeke-Samuelson (1993, 1997) were not read; the attribution rests on
  Ellison's description. Confidence that the criterion predates the study: high. Confidence about the exact form of
  the original lemma: low.
* Proposed fix: in the report, the remark and the PR text, call Lemma B a restatement, for this model, of the
  single-mutation-chain lemma of Samuelson (1994) / Noeldeke-Samuelson (1993, 1997) as described by Ellison (2000,
  Sect. 6.2, pp. 37-38), keep the short tree-counting proof as a self-contained proof, and claim only the explicit
  potential m + q - 2 as "not found in the sources read". Add these references to `literature_ring_size.md`, marked
  not read.

### L2 (major, provisional). Lemma 1, Lemma 2 and the first sentence of Theorem A correspond to known statements on "mutation-connected" / "locally stable" components.

* Location: `report_ring_size.md:110-111` (Lemma 1), `113-123` (Lemma 2), `125-132` (Theorem A), `:16` (summary);
  `PR_DRAFT.md:26-27`.
* Evidence (abstract, as shown in search results): Samuelson (1994), J. Econ. Theory 64, 35-65: if one element of a
  "mutation-connected component" appears in the stochastically stable distribution, all members appear. This is
  Lemma 1 applied along one-flip edges.
* Evidence (secondary, search fragments only, not read): lecture slides by Oechssler (Heidelberg, 2013) and working
  papers by Huck-Oechssler and by Ania et al. describe Proposition 1 of Noeldeke-Samuelson (1993) as: a state can be
  in the support of the limit distribution only if it belongs to a locally stable component, where a component is a
  set of absorbing sets linked by single-mutation transitions and it is locally stable if at least two mutations are
  needed to reach any other component; the stochastically stable set is then a union of such components. In the
  study's terms a locally stable component is a closed class of G1, so this is Lemma 2 and the first sentence of
  Theorem A.
* Ellison (2000) p. 36 (read) lists Noeldeke-Samuelson (1993, 1997) and Samuelson (1994) among the models covered by
  his theorem, which is consistent with the above.
* Not found in the sources read: the second sentence of Theorem A in its quantitative part (gamma_min = m - 1 for a
  unique closed class) and the computed statement that S equals the union of *all* closed classes.
* Confidence: medium (no primary text read). Marked provisional.
* Proposed fix: obtain Noeldeke-Samuelson (1993), Sect. on the limit distribution, and Samuelson (1994) or Samuelson's
  1997 book, and cite them at Lemma 1, Lemma 2 and Theorem A; until then write "this is the structure known in the
  stochastic-stability literature as locally stable / mutation-connected components (Noeldeke-Samuelson 1993;
  Samuelson 1994; not read)". Remove Theorem A from any list of results presented as the study's own without
  attribution.

### L3 (medium). Ellison's Theorem 2: number, hypotheses and conclusion are correctly described; the hedges and page references can be replaced by the published ones; one conclusion is omitted in two places.

* Location: `report_ring_size.md:73-76, 150`; `code/ring_size/literature_section.md:36-39`;
  `code/ring_size/ellison_remark.md:4`; `literature_ring_size.md:29, 92-124, 241-250, 295-305`.
* Evidence (read, page images): the published article has the same numbering as the working paper. Map:

  | item | working paper (printed page) | published (journal page) |
  |---|---|---|
  | Definition 1 (model of evolution with noise) | 5 | 20 |
  | limit distribution, long-run stochastic stability, W(x, Y, eps) | 7-8 | 22 |
  | Sect. 3.1 basin, path, radius, coradius | 9-10 | 23-24 |
  | Theorem 1 (Sect. 3.2) | 10 | 24 |
  | Example 1 with a cycle as selected set (Sect. 3.3) | 12-13 | 25-26 |
  | Sect. 4.1 modified coradius | 17 | 28-29 |
  | Theorem 2 (Sect. 4.2, "The main theorem") | 19 | 30 |
  | Sect. 6.2, lemma of Samuelson / Noeldeke-Samuelson | 30 | 37-38 |
  | Theorem 3 (Sect. 6.3) | 31 | 38, proof 38-39 |

* Theorem 2 as printed on p. 30: for a model of evolution with noise (Z, P, P(eps)) and a union Omega of limit sets
  with R(Omega) > CR*(Omega): (a) the long-run stochastically stable set is contained in Omega; (b) for every y not in
  Omega, W(y, Omega, eps) = O(eps^(-CR*(Omega))) as eps -> 0.
* Discrepancies found: no wrong theorem number, no wrong hypothesis, no wrong conclusion, no wrong volume, pages or
  DOI. Incomplete: `report_ring_size.md:75-76` and `literature_section.md:38-39` state only conclusion (a) and omit
  the waiting-time bound (b); `literature_ring_size.md:116-118, 246` state both.
* `literature_ring_size.md:29` and `:250` say the numbering is "consistent with later citations" seen only as
  snippets. This is now checked against the journal text.
* The DOI is not printed on the article. 10.1111/1467-937X.00119 resolves to this title in the fetch tool's lookup.
  The remark about a DOI ending in .00121 (`literature_ring_size.md:93`) was not checked.
* Proposed fix: replace "(working-paper numbering)" by "(Theorem 2, Sect. 4.2, p. 30)", give journal pages in
  `literature_ring_size.md` 1.3, add conclusion (b) in the two short summaries, and state that the published version
  was read in part.

### L4 (medium). "it adds equality" overstates the difference to Ellison when the selected set is a single cycle.

* Location: `report_ring_size.md:151-153`; `code/ring_size/ellison_remark.md:5-7`; `PR_DRAFT.md:28` ("with equality
  and the exact potential").
* Evidence (read): Ellison (2000) p. 38, after Theorem 3: when Omega is a single limit set, part (a) of Theorem 2
  gives mu*(Omega) = 1. So for q = 1 (zero state; the travelling crystal of classes 43 and 142) equality S = A is
  already Ellison's conclusion. For q > 1 (class 94) Theorem 2 gives containment and the rotation symmetry gives
  equality; Ellison closes Example 1 (p. 26) with a symmetry step as well (there inside one cyclic limit set).
* Proposed fix: "Ellison's Theorem 2 gives S contained in A, and S = A when A is a single cycle (Ellison p. 38); for
  q > 1 equality follows from rotation symmetry. Lemma B adds the value of gamma_min."

### L5 (medium). Bijectivity of rules 154 and 45 at odd n is in the literature; for rule 45 the study gives no reference.

* Location: `report_ring_size.md:63-64, 168-176, 215, 374, 435, 474`; `code/ring_size/literature_section.md:26-27`;
  `literature_ring_size.md:198-201, 203, 237`; `PR_DRAFT.md:28-29`.
* Evidence (read in part): Bhattacharjee and Das, arXiv:1903.06011, Example 2: rules 45 and 154 "are reversible for
  n = 1, 3, 5, 7, ..., that is, when n is odd".
* Evidence (read in full): Fedoriaka, arXiv:2501.06648 v1, Sect. 3: rules 45, 75, 89, 101, 154, 166, 180, 210 are
  reversible for odd N with periodic boundaries. This list comes from exhaustive computation for N in [4, 20], plus
  explicit circuit constructions for all N; it is not a proof for all odd N. Table I writes U_45 as a global
  complement applied after U_210, and U_210 as the mirror image of U_154.
* Evidence (abstract only): Nobe and Yura (2004): exactly 16 ECA rules are reversible for infinitely many cell sizes,
  shown through a correspondence with the de Bruijn graph. The count 16 equals Fedoriaka's periodic list (6 + 8 + 2),
  which contains 45. Proposition 1 on rule 154 at odd N was seen only as a search fragment, as the study says.
* Consequence for Lemma P: rule 45 is the output complement of rule 210 and 210 is the mirror image of 154 (my check:
  255 - 210 = 45, mirror(154) = 210, F_45 = NOT F_210 for n = 5..9). Bijectivity of F_45 on a ring is therefore
  equivalent to that of F_154; the two certificates of Lemma P are one statement.
* The pair-graph criterion itself (closed walks of length n, periods of off-diagonal components) was not found as
  stated in the sources read; Nobe-Yura's method is a de Bruijn-graph argument according to the abstract. Amoroso-Patt
  (1972), Hedlund (1969) and Sutner were not obtained.
* Confidence that the two bijectivity statements predate the study: high for 154 and 45 as stated facts; medium that
  a proof for all odd n is in Nobe-Yura (not read).
* Proposed fix: at `report_ring_size.md:63-64` and at Lemma P cite Nobe-Yura (2004), Bhattacharjee-Das (2019 preprint)
  and Fedoriaka (2025) for both rules; say that Lemma P re-proves a known fact by a pair-graph certificate; add the
  one-line reduction of rule 45 to rule 154. In `literature_ring_size.md:203` change Fedoriaka to "read" or state the
  evidence type (computation N <= 20 and constructions).

### L6 (medium). Rule 90 at n = 2^k: the primary source is Martin-Odlyzko-Wolfram, Lemma 3.5, and the "iff" follows from their Theorems 3.3 and 3.4.

* Location: `report_ring_size.md:69-71, 311-318, 339-341`; `code/ring_size/literature_section.md:32-34`;
  `literature_ring_size.md:163-178, 189, 239, 364-373`.
* Evidence (read): MOW Lemma 3.5 (p. 230): for N of the form 2^j, Pi_N = 1, with the remark that then any initial
  configuration evolves to the null configuration (one-line proof by squaring x + 1/x). Theorem 3.3 and its corollary
  (p. 228): for N odd half of all configurations lie on cycles. Theorem 3.4 and corollaries (pp. 228-229): for N even
  the trees have height D2(N)/2 and a fraction 2^(-D2(N)) of the configurations lies on cycles. Lemma 3.6 (p. 230):
  Pi_N = 2 Pi_(N/2) for N even, not a power of two. Theorem 3.5 (p. 232): odd N.
* Inference (mine): by additivity the single-seed orbit dies iff every orbit dies, i.e. iff only one configuration is
  on a cycle, i.e. iff 2^(N - D2(N)) = 1 (N even) and never for odd N > 1. So "the rule-90 orbit of e_0 vanishes iff
  n is a power of two", the algebraic core of Proposition R154, is implied by MOW.
* The second-hand MOW numbers quoted from Powley-Stepney in `literature_ring_size.md:166-177` agree with MOW, with
  one exception in L10.
* Proposed fix: cite MOW (1984), Lemma 3.5 and the corollaries to Theorems 3.3 and 3.4, at `report_ring_size.md:69-71`
  and in Proposition R154; move MOW from "not read" to "read" with the author-copy URL.

### L7 (medium). Proposition R154 has partial precedents that the study does not mention.

* Location: `report_ring_size.md:64-65` ("no statement on 154 at n = 2^k, was found"), `311-318`;
  `literature_ring_size.md:238`.
* Evidence (read): OEIS A070886 (rule 90 from a single cell), comment by Havermann: rules 18, 26, 82, 90, 146, 154,
  210 and 218 "all give rise to this sequence". This is the infinite-line form of the first step of Proposition R154
  (single-seed orbits of 154 and 26 coincide with rule 90).
* Evidence (read): MOW Sect. 5 (p. 247) uses the same reduction for rule 18: on configurations with all even or all
  odd sites zero the evolution is that of rule 90.
* Evidence (read): OEIS A334504, eventual period of a single cell under rule 26 on a cyclic universe of width n
  (b-file n = 1..120). Comparing the two OEIS b-files directly (no study data), it equals A085587 (rule 90) at
  30 of the 30 even n in 2..60 (A085587's b-file ends at n = 60), and it is 1 at n = 1, 2, 4, 8, 16, 32, 64.
  This b-file-to-b-file count is separate from the 29 study-versus-OEIS points for rule 26 in Section 3.3, which
  start at n = 4 because `seed_orbits.csv` starts there. OEIS A334507 gives the same kind of data for rule 122
  (value 1 at n = 1, 3, 7, 15, 31, 63).
* Not found in the sources read: the ring statement for rule 154 at even n, the "iff n is a power of two" for 154 and
  26 as a stated result, and anything on rule 22 (Proposition R22). An OEIS search for rule 154 and for rule 22 on
  cyclic rings returned no entry.
* Proposed fix: cite A070886 and MOW Sect. 5 as precedents of the argument, A334504 and A334507 as published data
  that agree with `seed_orbits.csv` (Section 3.3), and keep "not found" for the ring statements of 154 and 22.

### L8 (minor). One sentence infers absence in the literature.

* Location: `literature_ring_size.md:239`: the non-nilpotency of rule 154 at n = 8, 16 is said to be "consistent with
  the absence of any such statement in the literature".
* Evidence: Wuensche-Lesser, the Wolfram Atlas, Jen (1986, 1988), Hedlund, Sutner, Voorhees were not read by the
  study or by me.
* Proposed fix: "no such statement was found in the sources read".

### L9 (minor). The "undetermined" seed orbits of rules 26 and 154 are decided by Proposition R154 and MOW.

* Location: `report_ring_size.md:301-309` (table column undetermined_n: 33 for rules 26 and 154, 31 for rule 22).
* Evidence (file `data/ring_size/seed_orbits.csv`, read): all 33 capped n of rule 26 and of rule 154 are even and not
  powers of two. By Proposition R154 these orbits equal the rule-90 orbit, which by MOW never reaches 0 at such n
  (L6). For rule 22 the capped n divisible by 4 are [188, 196, 212, 220, 236, 244]; Proposition R22 decides them the same way.
* Proposed fix: report these n as "does not return (Proposition R154 / R22)"; only the length of the limit cycle is
  undetermined. The observation at `report_ring_size.md:349-350` (rule 122 shifted by one) matches OEIS: A334507(n) =
  A085587(n + 1) for all 29 odd n in 3..59 (my comparison of the two b-files; an observation, not a statement in a
  source).

### L10 (minor). One second-hand MOW reference does not exist in MOW.

* Location: `literature_ring_size.md:169` ("citing MOW Theorem 3.4 and the corollary to Theorem 3.2").
* Evidence (read): in MOW, Theorem 3.2 (p. 226) has no corollary. The corollaries follow Theorem 3.3 (p. 228) and
  Theorem 3.4 (p. 229, two corollaries). The quoted content (4 predecessors, depth D2(N)/2, 2^(N - D2(N)) cycle
  states) is Theorem 3.2, Theorem 3.4 and the first corollary to Theorem 3.4.
* Proposed fix: check the wording in Powley-Stepney and cite "Theorems 3.2, 3.4 and the corollary to Theorem 3.4".

### L11 (minor). Access statements that are no longer accurate.

* Location: `literature_ring_size.md:13-26, 29, 189, 304, 372` (MOW closed and not read; Ellison's published text not
  read); `report_ring_size.md:40-42`; `PR_DRAFT.md:64-65`.
* Evidence: the author copy of MOW is at content.wolfram.com/sw-publications/2020/07/algebraic-properties-cellular-automata.pdf
  and was reachable after approval. The published Ellison article is served by
  economics.mit.edu/research/publications/basins-attraction-long-run-stochastic-stability-and-speed-step-step-evolution
  (the host the study used for Ellison 1993).
* Proposed fix: update Section 0 and the BibTeX notes.

### L12 (minor). The class-94 crystal is the set of non-null fixed points of rule 90 given by MOW.

* Location: `report_ring_size.md:222-223, 246-248`.
* Evidence (read): MOW Lemma 3.7 (p. 234): for N a multiple of 3 rule 90 has four fixed points, the null
  configuration and the three shifts of 011011...; otherwise only the null one. Rules 94 and 90 agree on the codes
  3, 5, 6 (my check), so the three phases of (011)^(n/3) are fixed under both.
* Not found in the sources read: the one-flip radius of this fixed point under rule 94 (Lemma H with tau = 3), or any
  other statement on period-3 patterns of rule 94 on rings. The study reports NKS p. 951 as silent on finite size;
  not re-checked.
* Proposed fix: add the reference as a remark; no change of status.

### L13. Novelty wording stronger than "not found in the sources read"

| # | Location | Wording | Comment |
|---|---|---|---|
| a | `literature_ring_size.md:239` | "consistent with the absence of any such statement in the literature" | see L8 |
| b | `report_ring_size.md:152`, `ellison_remark.md:6` | "it adds equality (S = A, by rotation symmetry) and the exact value of gamma_min" | see L1, L4 |
| c | `PR_DRAFT.md:26-28` | "Proved for all n: the noise-selected cycles are a union of closed classes ... (Theorem A); a step-by-step criterion ... (Lemma B; the situation of Ellison's 2000 Theorem 2, with equality and the exact potential)" | listed as main results without prior art; see L1, L2 |
| d | `report_ring_size.md:64`, `literature_section.md:27` | "Lemma P below proves bijectivity at odd n independently" | not a novelty claim for 154, but rule 45 is covered by the same sentence without any reference; see L5 |
| e | `report_ring_size.md:146-147` | "It is the step-by-step argument the brief asked for." | presents the criterion without attribution; see L1 |
| f | `PREDICTIONS_ring_size.md:23-24` | "Ellison's modified coradius gives the same conclusion" | Ellison gives containment (and equality for a single limit set), not gamma_min; sealed file, note only |

All other statements about prior work that I checked use "not found" with the scope of the search
(`report_ring_size.md:44-45, 59, 65, 259, 496`; `literature_ring_size.md:225, 233, 238, 257`).

---

## 3. Statements checked and found consistent

### 3.1 Ellison (2000): sentence-by-sentence comparison

| Study sentence | Location | Source (published version, read) | Verdict |
|---|---|---|---|
| Citation Rev. Econ. Stud. 67:17-45, year 2000 | `report:73`, `literature:92, 295-303` | header of p. 17: "Review of Economic Studies (2000) 67, 17-45" | consistent |
| Definition 1: triple (Z, P, P(eps)), ergodic for eps > 0, continuous, cost function with positive limit of P_zz'(eps)/eps^c | `literature:94-98` | p. 20 | consistent |
| mu* = lim mu^eps; z long-run stochastically stable if mu*(z) > 0; limit sets = recurrent classes; W(x, Y, eps) | `literature:98-99` | p. 22 | consistent |
| Basin D(Omega); path = finite sequence of distinct states; radius R(Omega) = min cost of a path from Omega out of D(Omega) | `literature:100-103, 242` | p. 23 | consistent |
| Coradius CR(Omega) = max over x not in Omega of the min path cost to Omega; maximum attained in a limit set; equivalent form with D(Omega) | `literature:104, 243` | p. 24 | consistent |
| Cost of the form min over z with P_xz(0) > 0 of d(z, y), footnotes 8 and 9 | `literature:105` | p. 23 | consistent |
| Theorem 1: R > CR gives (a) containment, (b) W = O(eps^(-CR)) | `literature:107-109, 247` | p. 24 | consistent |
| Modified cost c* = c - sum over i = 2..r-1 of R(L_i); R(L_1) excluded; CR* = max of c*(x, Omega); CR* <= CR | `literature:110-114, 244-245`; `report:75` | pp. 28-29 | consistent |
| Three-state example, W ~ eps^(-CR*) | `literature:115` | pp. 29-30 | consistent |
| Theorem 2: union Omega of limit sets, R > CR*, (a) containment, (b) W(y, Omega, eps) = O(eps^(-CR*)) | `literature:116-118, 246` | p. 30 | consistent |
| Theorem 2, short form with (a) only | `report:75-76`, `literature_section:38-39` | p. 30 | correct but incomplete (L3) |
| Proof uses Lemma 1 and Lemmas 2, 6; Lemmas 2 and 3 give W(l, Z - D(L), eps) ~ eps^(-R(L)) | `literature:120` | pp. 30-31 | consistent |
| "Theorem 2 gives containment ... Uniqueness holds when Omega is a single limit set" | `literature:122` | p. 38 | consistent |
| Theorem 3: single limit set; R(Omega) > c*(x, Omega) gives mu*(x) = 0; equality case; proof by x-trees | `literature:123, 248` | pp. 38-39 | consistent |
| Example with a deterministic cycle as selected set | `literature:124` | pp. 25-26 (Example 1) | consistent |
| "the hypotheses of Lemma B give R(Omega) >= 2" | `report:147-148` | definition p. 23 | consistent (a cost-1 path from A_i stays in D(A_i); my derivation) |
| "modified cost (r - 1) - (r - 2) = 1 ..., i.e. CR*(Omega) <= 1 < R(Omega)" | `report:148-149` | definition pp. 28-29; Ellison's own remark pp. 37-38 (CR* = 1) | consistent |
| "this is the situation of Ellison's Theorem 2 (working-paper numbering), which gives containment" | `report:149-150`, `PR_DRAFT:28` | p. 30 | consistent; numbering identical in the journal |
| "without Ellison's convention that paths consist of distinct states" | `report:151-152` | p. 23 | consistent |
| "it adds equality ... and the exact value of gamma_min" | `report:152` | p. 38 | partly (L4) |

### 3.2 Statements tagged [proved] in `report_ring_size.md` and their status in the sources

| Statement | Location | In a source read? | Reference | Confidence |
|---|---|---|---|---|
| crystal with spatial period p exists only if p divides n | `:91`, `:257` | elementary; not searched as such | Jen (1988) abstract treats limit cycles as shifts on cylinders of any size (abstract only) | - |
| Lemma 1 (closure) | `:110` | yes, as a stated property | Samuelson (1994), abstract | medium (L2) |
| Lemma 2 | `:113` | yes, by secondary description | Noeldeke-Samuelson (1993), Prop. 1, not read | medium (L2) |
| Theorem A, first sentence | `:125` | yes, by secondary description | as above | medium (L2) |
| Theorem A, gamma_min = m - 1 for a unique closed class | `:125-131` | not found in the sources read | - | - |
| Lemma B, selection | `:137` | yes | Ellison (2000) Sect. 6.2 pp. 37-38 and Theorem 2 p. 30 | high (L1) |
| Lemma B, gamma_min = m + q - 2 | `:138-143` | not found in the sources read | - | - |
| Lemma Z | `:155` | not found; elementary | - | - |
| Lemma H (local healing) | `:159` | not found in the sources read | - | - |
| Lemma P, criterion via pair graph | `:168-173` | not found as stated; related de Bruijn method | Nobe-Yura (2004), abstract only | low |
| rules 154 and 45 bijective at every odd n | `:173-176` | yes | Bhattacharjee-Das Example 2; Fedoriaka Sect. 3 and Table I; Nobe-Yura abstract | high (L5) |
| k* = 0 for classes 154 and 45 at odd n | `:176` | k* is the study's notion; follows from bijectivity and v0.2 | - | - |
| class 94: r(crystal) >= 2 for 3 dividing n, n >= 7 | `:245-247` | not found; the fixed point itself is MOW Lemma 3.7 | MOW p. 234 | - (L12) |
| k* >= 1 at p dividing n, conditional on reachability | `:255-256` | conditional statement; see Lemma B | - | - |
| Proposition R154, coincidence of seed orbits with rule 90 | `:311-314` | infinite line: yes; ring: not found | OEIS A070886 comment; MOW Sect. 5 for rule 18 | medium (L7) |
| Proposition R154, rule-90 orbit vanishes iff n = 2^k | `:314-317` | implied | MOW Lemma 3.5, Thms 3.3, 3.4 with corollaries | high (L6) |
| Proposition R154, conclusion for 154 and 26 at even n | `:317-318` | not found as a statement; numerically in OEIS for rule 26 | OEIS A334504 | - |
| Proposition R22 | `:320-330` | not found in the sources read | - | - |
| rules 60, 90: nilpotent at 2^k (v0.2) | `:71, 210` | yes for rule 90 | MOW Lemma 3.5 | high |

### 3.3 Numbers compared with published tables (all agree)

Study values are read from the repository data files; the report itself prints only a few of them.

| Quantity | Published source | Study file | Compared | Agree |
|---|---|---|---|---|
| rule 90, number of cycles, n = 4..20 | MOW Table 2 (p. 235), last column | `data/fw_sweep.csv` | 17 | 17 |
| rule 90, number of cycles, n = 4..22 | MOW Table 2 | `mechanisms.csv` / `atlas/mechanisms_atlas.csv` | 19 | 19 |
| rule 90, maximal cycle length, n = 3..22 | MOW Table 1 (p. 233) vs OEIS A085587 | - | 20 | 20 |
| rule 90, maximal cycle length, n = 8..22 | MOW Table 1 | `cycle_orbits.csv.gz` (max temporal period) | 15 | 15 |
| rule 45, maximal cycle length, even n = 8..22 | OEIS A401854 | `cycle_orbits.csv.gz` | 8 | 8 |
| rule 26, single-seed limit period, n = 4..120 (uncapped) | OEIS A334504 | `seed_orbits.csv` | 112 | 112 |
| rule 122, single-seed limit period, n = 4..120 (uncapped) | OEIS A334507 | `seed_orbits.csv` | 112 | 112 |
| rule 154, single-seed limit period, even n = 4..60 | OEIS A085587 (rule 90) | `seed_orbits.csv` | 29 | 29 |
| rule 26, single-seed limit period, even n = 4..60 | OEIS A085587 (rule 90) | `seed_orbits.csv` | 29 | 29 |
| number of attractors at L = 17, all 88 classes | Bagnoli et al., Table 2 | `data/fw_sweep.csv` and ring-size files | 88 | 88 and 88 |

Numbers printed in the report and covered by these comparisons: 1688 attractors for rule 154 at L = 17
(`report:59-60`); return sets 4, 8, ..., 64 for rule 26 and 7, 15, 31, 63 for rule 122 up to n = 120
(`report:307-308`; OEIS has period 1 exactly there). Rule 45 at odd n has no orbit rows in `cycle_orbits.csv.gz`
(bijective records), so A401854 at odd n was not compared. Tables: `compare_cycles.csv`, `compare_seed.csv`, `compare_bagnoli_L17.csv`.

### 3.4 Other statements about sources that agree with what I read

* `literature_ring_size.md:166-168, 170-177`: the MOW statements quoted through Powley-Stepney (Lemma 3.3 identical
  trees; Lemma 3.4 cycle lengths divide Pi_N; odd N: single arcs, 2^(N-1) cycle states; even N: depth D2(N)/2,
  2^(N-D2(N)) cycle states; Lemma 3.5; Lemma 3.6; Theorem 3.5 with exceptions 37, 95, 101) agree with MOW pp. 227-232.
* `literature_ring_size.md:57-59` and `report_ring_size.md:69-70` (NKS p. 963: cycle fraction 2^(-2^IntegerExponent[n,2])
  for rule 90; depth 2^IntegerExponent[n/2,2]) agree with MOW Theorems 3.3, 3.4 and corollaries. NKS itself was not
  re-read.
* `literature_ring_size.md:45` (NKS p. 260: maximal period of rule 90 is 2^((n-1)/2) - 1) agrees with MOW p. 232.
* `literature_ring_size.md:71-87` (Bagnoli et al., Table 2 rows at L = 17): the 13 rows quoted agree with the table I
  extracted.
* `literature_ring_size.md:203` (Fedoriaka: list of rules reversible for odd N; formula for rule 154) agrees with the
  full text, up to the evidence type (L5).
* `literature_ring_size.md:3` formula: rule 154 = r XOR (l AND NOT c) agrees with Fedoriaka's Table I (the negation
  bar is lost in my text extraction; checked by brute force that this rule is bijective at n = 5, 7, 9 and not at 6, 8).

### 3.5 Bibliographic data verified

| Entry | Verified against | Result |
|---|---|---|
| Ellison (2000) | article header (read); DOI to title via fetch tool | journal, year, volume, pages, title, DOI consistent |
| Martin, Odlyzko, Wolfram (1984) | first page (read); DOI to title | CMP 93, 219-258 (1984) consistent |
| Busic, Mairesse, Marcovici (2013) | first page of publisher PDF; DOI to title | Adv. Appl. Prob. 45, 960-980 (2013) consistent |
| Jen (1986) | publisher page as shown in search results; DOI to title | J. Stat. Phys. 43, 219-242 consistent |
| Jen (1988), Cylindrical | publisher / Project Euclid data in search results; DOI to title | CMP 118, 569-590 consistent |
| Powley and Stepney (2009), both papers | dblp and author page as shown in search results | J. Cell. Autom. 4(2):125-136 and 4(4):293-310 consistent |
| Nobe and Yura (2004) | IOP page in search results; DOI to title | J. Phys. A 37 (22), 5789 consistent (end page not checked) |
| Fedoriaka (2025) | full text | title and arXiv number consistent |
| Ellison (1993); Marsan-Sablik (2025); Bagnoli et al. chapter; Wuensche (2018); Mairesse-Marcovici (2014); Fates (2020); Nobe-Yura (2007); Jen (1988), Linear | DOI to title via fetch tool only | titles consistent; volume and pages not checked |
| Wuensche and Lesser (1992) | Wuensche's publication list as shown in search results | series, publisher and year consistent (Addison-Wesley, Reading, MA) |

No error in authors, year, journal, volume, pages or DOI was found among the entries checked.

---

## 4. Not checked, and why

* Wuensche and Lesser (1992): tabulated cycle counts and basin data. Not obtained (three author hosts refused after
  approval). Whether the atlas confirms or contradicts cycle counts of the report is open.
* Wolfram Atlas finite-size pages for rules 154, 45, 94, 22, 26: not obtained (host refused). The OEIS entries used
  instead are computed sequences, partly attributed to MOW Table 1 and to mailing-list computations, not to the Atlas.
* Jen (1986), Jen (1988, two papers): full texts closed at Springer; Project Euclid, OSTI and Springer pages refused.
  The abstracts mention conditions for homogeneous limits, rules for which inverses exist, and a matrix method that
  counts limit cycles of any period on any cylinder size. Whether they contain statements on rules 154, 45, 94, 22,
  26 at specific ring sizes is unknown. Which 1988 Jen papers are relevant: the two Commun. Math. Phys. papers above;
  no 1988 paper by Jen on invertibility was located (inverses are a topic of the 1986 paper, by its abstract).
* Samuelson (1994), Noeldeke-Samuelson (1993, 1997), Samuelson's 1997 book: primary texts not read (closed; archive
  host refused). L1 and L2 should be confirmed against them.
* Nobe-Yura (2004), full text, including whether rule 45 is treated explicitly and how Proposition 1 is proved; Nobe-
  Yura (2007).
* Hedlund (1969), Amoroso-Patt (1972), Sutner, Voorhees, McIntosh: not obtained; priority of the pair-graph criterion
  of Lemma P is therefore not assessed beyond "not found in the sources read".
* Ellison (2000), journal pp. 18-19, 21, 27, 32-35, 40-45 (examples, Section 5, appendix lemmas, references).
* The statement on a DOI ending in .00121 (`literature_ring_size.md:93`).
* NKS page-level claims of `literature_ring_size.md` 1.1 beyond those implied by MOW; Ellison (1993); Powley-Stepney
  full texts; Marsan-Sablik; the asynchronous-update literature; Kanada (1994); Sethi-Roy-Das (2018).
* Volume, page and year data of the entries listed as "DOI to title only" in 3.5; api.crossref.org was refused.
* The mathematical correctness of the study's proofs. This check concerns sources only.
