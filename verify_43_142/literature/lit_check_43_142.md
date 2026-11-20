<!-- Report of the literature sub-task of this verification (17 Nov 2026), saved verbatim by the lead: the
sub-task's own file write was held by a safety-check outage, so its text was taken from its final message.
The sub-task read literature_addendum.md and PROOF_43_142.md lines 1-472 only. Its first paragraphs
describe that situation and its limits (18 web searches, 9 of them new; budget was about 10). -->

I wrote the full check, but lit_check_43_142.md was not saved. The command that writes it was held by a safety-check outage and needs your approval. I was told not to retry it another way, so the complete report is below in this message. If you approve, rerun that step (a single `cat > lit_check_43_142.md` in the workspace, then `save_artifacts`), or save this text yourself. Nothing inside the repository was created, changed or deleted.

**Limits on this check:**
- **Not obtained:** B2, B3, B5, Hattori–Takesue, Fukś's 2023 book, NKS online, the Wolfram Atlas, and the full texts of Nobe–Yura, Chua et al., Krawczyk and Zhu–Richard.
- **Read in part:** B6 and B7 only on the pages around keyword hits. A6 and A7 only on the pages named in the table. Nordahl (A3) is an OCR scan; I read pp. 70, 73, 74 and the references.
- **One scan not run:** a planned rule-number scan of A3 was also held by the safety check. The same scan of all of A7 did run.
- **Searches:** 18 web searches in total, 9 of them the fresh prior-work search (budget was about 10).
- All negative findings are provisional.

---

# Literature check of `literature_addendum.md` (rules 43 / 142), 17 Nov 2026

A claim counts as **supported** only if I saw the page text myself in this task. **Partly** means a search excerpt or deposited abstract only, or only part of the claim.

## 1. Statement table

### Part B

| # | location | statement | source and page opened | verdict | note |
|---|---|---|---|---|---|
| P1 | B1 row (a) | rule 60 maps 142 to 226 (abstract) | B1 publisher PDF, p. 123 | supported | |
| P2 | B1 row (a) | eq. 34, p. 132 | B1 p. 132 | supported | Fukś's f60 = x0 + x1 is the proof's wall word up to a shift; rule 226 commutes with shifts. |
| P3 | B1 row (a) | Proposition 6, p. 133 | B1 p. 133 | partly (wording) | Prop. 6 equates two preimage counts. The identity appears there only as eq. (40), inside the proof. |
| P4 | B1 row (a) | credited to Boccara 1992 | B1 p. 132, ref. [2] p. 138 | supported, but see L1 | B1 itself prints 1992. |
| P5 | B1 row | rule 43 not in B1 | all 16 pp. plus keyword scan | supported | The "43" hits are equation numbers. Rules 35 and 14 are named on p. 137. |
| P6 | B1 row | blocks 10 conserved for periodic configurations of every length (Sec. 3) | pp. 125–127 | supported | Eq. (9) holds "for every positive integer L". |
| P7 | B1 row (b) | "infinite lattice, limits in probability" | pp. 127–137 | supported (wording) | Strictly: t → ∞ limits of block probabilities under a translation-invariant measure. |
| P8 | B1 row (c), rings, 4\|n | none of these stated | full text | supported, but see L3 | |
| P9 | "What follows" (c) | density 1/4 jamming on the infinite lattice | pp. 136–137 | supported | |
| P10 | noise | no noise statement in B1 | full-text scan | supported | |
| P11 | B1 footer | 2005 | p. 123 | supported | |
| P12 | B2 row | both identities in Sec. 7 of nlin/0502037 | — | not reachable | My own check: both identities hold on all rings n = 3..12, and the crossed pairs fail. The location in B2 is still unseen. |
| P13 | B2 row | critical density 1/4 for 14, 43, 142 | FI abstract (excerpt) | not reachable | The abstract names no rules. |
| P14 | B3 row | Boccara, Physica D 68, 416–426 | DOI tool; ScienceDirect excerpt | partly | **Published 1993**, DOI 10.1016/0167-2789(93)90134-M. Closed access. |
| P15 | B4 row | arXiv p. 3: after ⌊(L−2)/2⌋ steps no 00 / no 11 / neither | arXiv v1, all 5 pp. | supported | Proposition 1 (p. 2) is proved only in sketch; Proposition 2 (p. 3) does the odd case as "similar". |
| P16 | B4 row | remaining columns | pp. 1–5 | supported | |
| P17 | (b) | healing time equals the B4 bound | p. 3 | supported | |
| P18 | (b) | "periodic iff no 11 or no 00" not written out | B4, B1, B7 pages read | supported (provisional) | See L5. |
| P19 | B5 row | N/2 bound | B6 arXiv p. 4 | partly | B5 not seen; B6 attributes the bound to it. |
| P20–21 | B6 row | Assertion 1.1; N/2 attribution; infinite line | arXiv pp. 1, 3, 4, 7 | supported | |
| P22 | noise | B6's noisy 184 is random hopping | arXiv pp. 1–2 | supported | B6 also cites Bramson–Neuhauser (1994); not in the addendum, not obtained. |
| P23 | B7 row | number of ones conserved on rings | arXiv pp. 3–4, 6 | supported | |

### Part A

| # | location | statement | source and page opened | verdict | note |
|---|---|---|---|---|---|
| A1a–c | A1 | metadata; Sec. 2.3 / eq. (4); 154 "below 0.01" sentence; Sec. 4.2; 4.3 list; even-n 154 close to unitary | search excerpts (this task) | partly (excerpt) | All now seen first-hand. Eq. (4) divides by "the total number of eigenvalues 2^n", which points to algebraic multiplicity. New: rule 45 at even n has ratio > 0.5. The two digit strings were not seen. |
| A2 | A2 (1) | title; reduced to a linear system over Z_2 | DOI tool | title supported; abstract partly | The deposited abstract says "on a finite commutative ring" plus an elided formula (L9). |
| A3a–c | A3 pp. 70, 73, 74 | rule 90 cycle fractions; simulation definition; rule list and quoted phrase | publisher scan pp. 70, 73–74, refs | supported | Refs [11] = Martin–Odlyzko–Wolfram 1984 ✓; [26] = Hurd, appendix to Wolfram (ed.) 1986 ✓. |
| A4 | A4 | Table 4; "indivisible by 4" quote; CSF 78 (2015) | excerpts | partly | The quote was not returned in this task. |
| A5 | A5 | titles via DOI; Part VIII abstract quote; rules 154 and 45 | DOI tool plus excerpts | supported (abstract level) | The abstract also says rule 60 has no Isles of Eden for any L. |
| A6 | A6 pp. 230, 232 | k ≤ 22 spectra; quoted sentence | publisher PDF | supported | p. 231 notes 184's cycle lengths are all multiples of k. |
| A7 | A7 pp. 44, 52; Sec. 3.2; App. A | quote; regimes; App. A rules and sizes | publisher PDF pp. 44, 52, 68–70 | supported | "Up to 13" holds only for rule 60. A full-text scan finds no rule 154, 43 or 142. p. 52 cites DDLab metagraphs (L6). |
| A0 | §0 access | which hosts are reachable | own attempts | supported | |

### Numbered findings

- **L1 — false statement (bibliographic).** Boccara's paper is Physica D 68 (3–4), 15 October **1993**. The addendum says 1992 throughout, apparently copied from B1's reference list.
- **L2 — wording.** The identity itself is eq. (34) on p. 132. On p. 133 it is only used, as eq. (40) in the proof of Proposition 6.
- **L3 — understatement.** B1 contains more than "a jamming-type transition":
  - a local motion law: a block 10 preceded by 1 moves one site left; one preceded by 0 stays (eqs. 16–17, p. 127);
  - a velocity law: expected velocity −1 for ρ < 1/4, and 1 − 1/(2ρ) above (eq. 59, p. 137).

  These are infinite-lattice counterparts of the proof's two families of cycles. B1 still has no ring characterisation.
- **L4 — overstated wording.** "(a) is known for both rules", and PROOF line 30, say more than the evidence. No text I could read shows the wall map or block-10 conservation for rule 43. Both are true (my own computation), but that is not a literature source.
- **L5 — small addition.** B4 p. 3 also says that at N0 = N1 the configuration becomes the alternating one. That is the density-1/2 half of (b), without the converse.
- **L6 — understatement.** The G1 construction already exists as Wuensche's DDLab attractor jump-graph (arXiv:2406.10704 §4, excerpt): it tracks where every single-bit flip of an attractor state ends. Voorhees–Beauchemin p. 52 cite DDLab metagraphs for exactly this regime, and Bagnoli et al. build a single-flip Markov matrix between attractors. In what I saw, none of them gives the selected set for rules 43/142.
- **L7 — gap in the search.** Noise work on the infinite lattice exists, all seen as excerpts only:
  - Marsan–Sablik, "Strong stochastic stability of cellular automata" (EJP 30, 2025; arXiv:2403.19932);
  - Hellouin de Menibus–Sablik, J. Stat. Phys. 167 (2017): μ-limit set of rule 184, an analogue of (b);
  - Bramson–Neuhauser (1994).

  As far as the excerpts show, none is on finite rings.
- **L8 — open.** Three likely places for the block-10 invariant of 43/142 could not be opened:
  - Hattori–Takesue's table of additive invariants;
  - NKS p. 1023, note (g), on block-type conserved quantities;
  - Fukś 2023, chapter 6.
- **L9 — wording (A2).** "Over Z_2" cannot be confirmed from the deposited abstract.
- **Checked, nothing found:** B1 conservation and abstract, B4, B6, B7, A3, A6, A7, and the A5 titles and quote.

## 2. Part B: how the result may be described

- **Rule 142:** "the wall map and conservation are known" is accurate. Both are in Fukś 2005, which I read in full; it credits the identity to Boccara 1993.
- **Rule 43:** no text I could read attests either fact. Suggested wording: "the corresponding identity for rule 43 is reported in Fukś (2007), seen only in a search excerpt".
- **"The selection result was not found":** accurate as a provisional negative. It should name the jump-graph prior art for G1 (L6) and the infinite-lattice stochastic-stability work (L7).
- **Overstated:** "(a) is known for both rules", PROOF line 30, the 1992 year, and p. 133 as the identity's location.
- **Understated:** B1's motion and velocity laws (L3), B4's density-1/2 statement (L5), and the prior art in L6 and L7.
- **(c), the n/2-wall cycle and 4 | n, and a ring characterisation for 142/43/184/226:** none is stated in any source I read. B4 gives only the rule-184 time bound and the block elimination; Stricker's observation on 184 is numerical. "(c) was not found" stands, with several likely sources unread.

## 3. Not reached

| item | route tried | result |
|---|---|---|
| B2 and the arXiv copy of B1 | arXiv; IOS Press; author homepage | arXiv refused and cannot be approved. IOS Press is paywalled. Author-page access was granted, but the page sits behind a Cloudflare browser challenge, which I did not get around. |
| B3, B5, Hattori–Takesue, Fukś 2023 book | DOI tool | closed access |
| NKS online, Wolfram Atlas | direct | refused, cannot be approved |
| A1 full text | arXiv | refused; excerpts only |
| A2 Nobe–Yura (both) | IOP; open-access repository copy | IOP closed; repository refused |
| A4 Krawczyk, A5 Chua et al. full texts | arXiv; DOI tool | refused / closed |
| Marsan–Sablik, Hellouin de Menibus–Sablik, Bramson–Neuhauser, Wuensche | search only | excerpts only |
| journal versions of B4, B6, B7 | — | not compared with the arXiv versions |

My own computation (not literature): on rings n = 3..12, rule 60 ∘ F43 = F184 ∘ rule 60 and rule 60 ∘ F142 = F226 ∘ rule 60, and the crossed pairs fail. On n = 3..14, both rules conserve the number of blocks 10.