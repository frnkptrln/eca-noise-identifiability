# Part 2 — Section 3.2 "Rules 43 and 142" (tex lines 579–1002) against `proofs_43_142/PROOF_43_142.md`

Reader: Claude. Read-only. Paper: `paper/ring_size_paper.tex` on branch `paper-ring-size`. Source (called P):
`proofs_43_142/PROOF_43_142.md` (812 lines). Trace: `paper/trace/trace_43_142.md`, `paper/TRACE.md` Part A rows
Lemma 2.2–Theorem 2.8 and Lemma 3.12–Theorem 3.28, Part C.

## 0. What was done, and the result in brief

Read in full, both sides: tex 158–318 (Section 2) and 560–1002; P lines 1–474 (Sections 0–6) and 475–812
(tables, scope, files; the tables only looked through); the trace file (217 lines); TRACE.md lines 33–48, 60–76 and
Part C (206–276). Every proof of Section 3.2 was re-derived by hand while reading (list in the table). No program
was run; no repository script, no `.json`, no `REFEREE_NOTES.md`, no verification report and no literature file was
opened. Scope reductions: none against the task; what was not checked is in Section 4.

Result. In Section 3.2 I found **no false statement (class 1)**, **no step that fails (class 2)** and **no
hypothesis or range that is not met (class 3)**, the smallest rings included (n = 3 for Lemmas 3.12–3.18, n = 4 for
3.19–3.22, n = 5, 6, 7 for 3.23–3.27). All 17 statements are the same statements as in P. Seven findings, all of
class 5 (cosmetic) or 4 (unclear): missing citations of Lemma 2.3, one concluding sentence of P dropped, a fact
used outside the proof in which it is stated, two letters with two meanings. "Confirmed" below means: I read the
proof and re-derived each step by hand; it does not mean confirmed by computation.

Numbering: the 12th numbered environment of Section 3 is `43:lem:R` (line 591) and the 28th is `43:thm:main`
(line 992), counted with grep over `\begin{theorem|lemma|proposition|corollary|remark|definition}`; all share one
counter (lines 21–27). This agrees with "Lemma 3.12 … Theorem 3.28" of TRACE.md. The PDF was not compiled.

## 1. Table: one row per numbered statement

Columns: (S) same statement as the source (hypotheses, ranges, quantifiers)? (P) proof: steps dropped / added /
changed? (X) cross-references correct? (R) read as a referee: every step justified, smallest n covered?

| no. | label (tex line) | source in P | (S) | (P) | (X) | (R) |
|---|---|---|---|---|---|---|
| 3.12 | `43:lem:R` (591) | form (R), l. 44–52 | Same. Both rows of the value table (586–587) checked against the binary expansions 142 = 128+8+4+2 and 43 = 32+8+2+1 and against P 44–45. | Proof written out (P: "compare with the eight table entries"); nothing dropped. | none | Yes. All eight entries checked for both rules. |
| 3.13 | `43:lem:wall` (623) | Lemma 1, 143–161 | Same; `1 - d` written `1 + d` (mod 2; recorded). The two verbal glosses of P 145–148 are not taken over. | Same steps, same order. | 629, 633 → `43:lem:R`: correct. | Yes. Both cell formulas and both wall identities re-derived; g_184, g_226 (618–619) checked against the tables of rules 184 and 226; G_226 = ρ G_184 ρ re-derived. n = 3: only cells i−1, i, i+1 enter, which are distinct. |
| 3.14 | `43:lem:cons` (640) | Lemmas 2 and 5, 163–166, 228–233 | Same (merged). Evenness of w stands in the definition paragraph (603–604) and is recalled in (b). | Same. | 648 → `43:lem:R`, 650 → `43:lem:wall`: correct. | Yes. |
| 3.15 | `43:lem:flip` (659) | Lemma 6, 235–237 | Same. | Same. | 663 → eq. `43:eq:flip`: correct. | Yes. |
| 3.16 | `43:lem:pairs` (666) | Lemma 3, 168–207 | Same; A, A' renamed N, N' (recorded). | Same; the sentence on n = 3 is moved before the counting. | none | Yes. Four bracket combinations for P(d') and for Q(d') re-derived; the counting; (b) index arithmetic incl. P(ρd) = −P(d)−1 and the Q case; (c). n = 3 (cells i−1 and i+2 coincide): the equivalences are propositional in d_{i−1},…,d_{i+2} and stay valid under identification. |
| 3.17 | `43:lem:pww` (704) | Lemma 4, 209–226 | Same (four implications written as one sentence; compared one by one). | Same; T → t_0, c → g (recorded; see finding 6). | 714 → `43:lem:pairs`(a): correct. | Yes. g = n (p = q) is covered by the same argument; n = 3 covered. "Periodic under G" for a word is not defined separately (Section 2 defines it for F); meaning clear. |
| 3.18 | `43:lem:per` (725) | Lemma 7, 239–268 | Same; r → s (recorded). | Same. In (c) "F^t u = C^t σ^t u" is spelled out by parity (recorded). | 739, 749 → `43:lem:wall`; 750 → `43:lem:pww`; 756 → `43:lem:cons`(b): correct. | Yes. Four formulas of (b) re-derived and tried on 00011 and 00101 (n = 5) by hand for both rules. (c) for s of either parity and for u replaced by its complement. |
| 3.19 | `43:lem:half` (763) | Lemma 8, 282–290 | Same content, reordered: the "for even n" sentence first; "only the codes 001, 011, 110, 100" moved from the proof of P (289–290) into the statement (recorded). | Same steps, reordered. | 773 → `43:lem:pairs`(c); 774 → `43:lem:per`(a); 776 → `43:lem:R`: correct. | Yes. n = 4: the four rotations of 0011 are distinct. That the states of X have n/2 walls and are periodic is implicit (alternating wall word; F = σ^{-1} on X). |
| 3.20 | `43:thm:crystal` (780) | Theorem 1, 104–111; proofs 294–311 | Same. "r(X) ≥ 2" written "V(X, C') ≥ 2 for every cycle C' ≠ X"; "returns to" → "ends on"; "Consequently" is item (3) (all recorded). | (1), (2) same. (3): the last sentence of P ("Hence {X} is the only closed class", P 310–311) is dropped — finding 1. | 791, 794, 798, 805 → `43:lem:half`; 793, 799, 802 → `43:lem:cons`; 793, 801 → `43:lem:flip`; 800 → `43:lem:pairs`(c); 796, 803 → `lem:edge`: correct, and the same lemmas as P cites at each step. | Yes. n = 4: w ∈ {0, 2, 4}, one edge. `lem:edge` is used with C ≠ C' in both places. |
| 3.21 | `43:cor:div` (811) | Corollaries 1 and 2, 123–127, 352–366 | Same (merged). | The derivation of "k_c = 0 iff …" (P 355–358) is replaced by a citation of `lem:kzero`; the rest is the same. | 817 → `43:thm:crystal`(3); 818 → `thm:A`, `lem:kzero`; 820 → `43:lem:half`: correct. | Yes. Codes of x̂ at cells 0–3 and of y = x̂+e_2, y' = x̂+e_1 checked for n = 4 (cell 4 = cell 0, cell n−1 = cell 3) and n ≥ 8; F σ x̂ = x̂ from F = σ^{-1} on X. `thm:A` needs a unique closed class: given by (3). |
| 3.22 | `43:prop:heal` (841) | Proposition 2, 113–118, 313–332 | Same; "(For n = 4, n/2 − 1 = 1)" stands in the proof only (recorded). | Same. | 849 → eq. `43:eq:flip`; 850 → `43:lem:half`; 851 → `43:lem:pairs`(c); 856, 862 → `43:lem:pairs`(a), (b): correct. Caption of Figure 2 (834–837) → `43:prop:heal`, and its left/right assignment for rule 43 agrees with the statement. | Yes. P(h), Q(h) for both cell types; the congruence 2t+4 ≡ 0 mod n; n = 4: the window j−2,…,j+1 is the whole ring, N(h) ≠ ∅ at t = 0, τ = 1. |
| 3.23 | `43:lem:levels` (873) | Lemma 9, 377–390; setting 98–100, 373–375 | Same; (b) reworded "a flip of a state of a cycle of K leads to a cycle of K" (recorded; same content). The clause of P 373–374 "no cycle has wall count n/2" is not taken over; no proof uses it. | Same. | 883, 889 → `43:lem:pairs`(c); 884 → `43:lem:per`(a); 885, 890 → `43:lem:flip`; 886, 891 → `43:lem:cons`: correct. `lem:edge` is used and not cited — finding 2. | Yes. Bounds 2 ≤ w_- < n/2 < w_+ ≤ n−1, w_+ − w_- = 2 and η ∈ {1, 2, 3} checked for n = 5, 6, 7 and for each residue mod 4. |
| 3.24 | `43:lem:slides` (898) | Lemma 10, 392–415 | Same (n ≥ 3; the definition of a slide stands before the lemma). | First statement: proved by the last sentence of `lem:edge` instead of P 402–403; same argument (recorded). (a), (b) same; R_k, r_k → I_k, λ_k. | 910 → `lem:edge`; 915 → `43:lem:per`: correct. | Yes. (a): the flipped cells never cross the cut (k ≥ 2); x itself is periodic by `43:lem:per`(a). (b): n − w ≥ 1 and 2w − n ≥ 1 from n/2 < w < n. Range sentence: finding 7. |
| 3.25 | `43:lem:Z` (926) | Lemma 11, 417–433 | Same; z0 → z, y_s → y^{(s)}, eps → η (recorded). | Same. | 936, 940, 941 → `43:lem:per`; 943 → `43:lem:slides`; 944 → `43:lem:cons`: correct. | Yes. Length of z is η + 2w = n; run lengths of y^{(s)}; y^{(η)} = σ² of the complement of z; rule 43 at n = 5 done by hand (F²(11100) = 00111). The complement symmetry of G_1 is proved here in place; see finding 3. |
| 3.26 | `43:thm:levels` (948) | Theorem 2, 129–131, 435–452 | Same (n ≥ 5, 4 ∤ n). | Same three steps; x1 → z^+ etc. (recorded). | 958 → `43:lem:levels`(a), `43:lem:slides`(a); 960, 966 → `43:lem:per`(c); 962 → `43:lem:Z`; 965 → `43:lem:levels`(a), `43:lem:slides`(b); 967, 971 → `43:lem:levels`(c); 973 → (b); 974 → (d): correct, same as P. | Yes. z, z^+ written out for n = 5, 6, 7 (00011/00101, 000011/001101, 0000011/0011001); `43:lem:slides`(a) needs w ≥ 2: w_- ≥ 2 holds; (b) needs n/2 < w < n: holds for w_+. Use of the complement in Step 2: finding 3. |
| 3.27 | `43:cor:ndiv` (978) | Corollary 3, 133–134, 454–458 | Same. | Same; "see the proof of Corollary 2" replaced by `lem:kzero`. | 983 → `43:thm:levels`, `thm:A`; 984 → `43:lem:Z`; 987 → `43:lem:levels`(a); 989 → `lem:kzero`: correct. | Yes, with finding 5 (the upper level is not empty: not said). Codes of z checked also for w_- = 2 (z = 0^{η+2}11). |
| 3.28 | `43:thm:main` (992) | Corollary 4, 136–137, 460 | Same; "In particular k* = 1 iff 4 ∣ n" added (recorded; follows, for n ≥ 4). Agrees with Theorem 3.1(b), line 325. | Same. | 997 → `43:cor:div`, `43:cor:ndiv`: correct. | Yes. n = 4 by 3.21, n = 5, 6, 7 by 3.27; every n ≥ 4 falls in one of the two cases. |

Unnumbered text. Definitions 601–621 against P 65–100: same; not taken over are (D1) in its "only if" direction
and "In a constant state every cell is interior" (P 80); neither is used (the interior cell of a constant state is
obtained from Lemma 3.16(c) in 800 and 889). Credit paragraph 653–657 against P 755–762: agrees with P; "up to a
shift of the indices, δ is the local map of rule 60" is correct (δ(x)_i = x_i + x_{i+1} is rule 60 read at cell
i+1). Closing sentence 1000–1001 against P 464–466: same, without the computed part; correct (at n = 3, w_- = 0).
Sentences 868–871 against P 98–100, 373–375: same.

Uses of Section 2 in Section 3.2.

| cited | where (tex line) | hypotheses met? |
|---|---|---|
| `lem:kzero` | 818 (3.21), 989 (3.27) | Yes; first sentence of the lemma, no hypothesis. The third clause (k_v ≤ 1) is not cited; 823–828 argue from the definition, as P does. |
| `lem:edge` | 796, 803 (3.20), 910 (3.24) | Yes; C ≠ C' in each place (different wall counts, or "equal or joined"). Used without citation in 3.23(b)–(d) and inside "edges to edges" of 3.25 (findings 2, 3). |
| `lem:sym` | not cited in Section 3.2 | — . The section needs the complement, not the rotation; proved in place in 3.25 (TRACE.md row `lem:sym` says so). |
| `thm:A` | 818 (3.21), 983 (3.27) | Yes; in both places a unique closed class is established first (3.20(3), 3.26). |

## 2. Findings

None of class 1 (false statement). None of class 3 (hypothesis or range not met). Class 2: none in the sense of a
step that fails; finding 1 is a sentence dropped relative to the source, which I put in class 5 because what is
missing follows in one line from what stands in the paper.

1. **`43:thm:crystal`, proof of (3), tex 807–808. Class 5 (sentence of the source dropped).** The proof ends
   "so $K=\{X\}$, a contradiction." P 309–311 goes on: "Hence {X} is the only closed class." The paper stops at the
   contradiction; that a closed class exists (tex 231–232) or that {X} is one (no edge leaves X, by (1)) is not
   said either. Correction: add "Hence a closed class contains no cycle other than $X$; a closed class exists
   (Section 2.4), so $\{X\}$ is the only one."

2. **`43:lem:levels` (b), (c), (d), tex 877–879 and 885–893. Class 5 (citation missing).** "A single flip of a
   state of a cycle of $K$ leads to a cycle of $K$. So no edge of $\Gone$ leaves $K$" (877); "has an edge of
   $\Gone$" (878); "after finitely many edges" (892). In the paper an edge of G_1 is defined by V = 1 (tex 230), so
   the passage from flips to edges is Lemma 2.3 (`lem:edge`); the proof cites only `43:lem:pairs`, `43:lem:per`,
   `43:lem:flip`, `43:lem:cons`. In P no citation is needed because G1 is defined by flips (P 55–56); in the
   same step of `43:thm:crystal` the paper does cite `lem:edge` (796, 803). Correction: add
   "(Lemma~\ref{lem:edge})" in (b) and (c).

3. **`43:thm:levels`, Step 2, tex 966–968, with `43:lem:Z`, tex 944–945. Class 4/5.** Step 2 says "Applying the
   complement, $\cpl{Z}$ has a path to the other one" and uses $\cpl{Z^+}$. The fact used ("the complement maps
   cycles to cycles and edges of $\Gone$ to edges of $\Gone$") stands only inside the proof of `43:lem:Z`, is not
   referred to in Step 2, and $\cpl{D}$ for a cycle D is defined only for D = Z (930). Same in P (447, 433); the
   argument is correct. Correction: state the fact once as a numbered sentence (for instance as part (c) of
   `43:lem:cons`: "the complement of a cycle is a cycle, and $C\to C'$ is an edge of $\Gone$ iff
   $\cpl{C}\to\cpl{C'}$ is", by Lemma 2.3) and cite it in 945 and 968.

4. **Definition of $\rho$, tex 164–165 and 205, used in 621, 694–695, 721–722. Class 5 (one letter, two
   meanings).** $\rho$ is "the reflection, $(\rho x)_i=x_{-i}$" (165) and "$\rho(\eps)=(1-2\eps)\log\dots$" (205,
   also 102, 212). Section 3.2 uses the reflection. The collision is in Section 2, not introduced by Section 3.2.
   Correction: another letter for the rate, or a remark.

5. **`43:cor:ndiv`, tex 986–988. Class 5.** "A state of a cycle of the upper level has an isolated cell …" assumes
   that the upper level is not empty; this is not said in the corollary. It holds (Lemma 3.23(c) applied to Z, or
   the state $z^+$ of the proof of Theorem 3.26). Same in P 455–457. Correction: "the state $z^+$ of the proof of
   Theorem~\ref{43:thm:levels} lies on a cycle of the upper level and has an isolated cell …".

6. **`43:lem:pww`, tex 716–719. Class 5 (renaming recorded in TRACE.md, mild collision).** "Let
   $g\in\{1,\dots,n\}$ with $g=p-q$ mod $n$": g is also the letter of the local rules $g_{184}$, $g_{226}$
   (618–621) of the same lemma. TRACE.md records "the number c renamed g". No ambiguity arises because the rules
   carry subscripts. Correction: a letter not otherwise used in the section (for instance $\ell$).

7. **Range sentence, tex 868 against `43:lem:slides`, tex 899. Class 4.** "From here to
   Corollary~\ref{43:cor:ndiv}, $n\ge 5$ and $4\ndiv n$" (868), and inside this range "Let $n\ge 3$" (899). The
   lemma is meant for every n ≥ 3 with or without 4 ∣ n (P 392: "divisibility by 4 plays no role"; the table at tex
   1281 cites it without a restriction on n), but the paper does not say that the standing assumption 4 ∤ n is lifted.
   Correction: "Let $n\ge 3$ (whether or not $4\mid n$)."

Observations outside tex 579–1002 that concern statements of this section (read once, not part of the task):

* tex 1265–1266: "the value $n/2$ … is taken by a periodic state iff $4\mid n$ … (Lemma~\ref{43:lem:half})". The
  "only if" for n ≡ 2 mod 4 is the evenness of w (tex 603), not Lemma 3.19 as stated; true, citation incomplete.
* tex 1562: "the wall map $\delta$, which is rule 60" against tex 654 "Up to a shift of the indices, $\delta$ is
  the local map of rule 60". The second is the exact one.
* tex 333–334: "Rule 43 and rule 142 are not equivalent under reflection and complementation of the rule".
  Checked by hand: both rules are invariant under complementation, the reflections are rules 113 and 212. Correct.
* tex 1567–1569: ⌊(n−2)/2⌋ = n/2 − 1 for even n, the value of Proposition 3.22. Consistent.

Trace records (not findings on the paper): the TRACE.md row of `43:cor:div` and `trace_43_142.md` §6 still say
that `prop:order` is cited, and §5 of the trace quotes the key `Fuks2006`; the paper has `lem:kzero` (818, 989)
and `Fuks2005b` (656). Part C items 2 and 4 of TRACE.md record both changes, so the records are consistent when
read together.

## 3. Renamings checked for consistency

A, A' → N, N' (669–676, 691–692, 715, 719, 856–864: consistent). T → t_0; c → g; r → s (732, 752–755, 959);
R_k, r_k → I_k, λ_k (911–923); eps → η (869–985; η occurs nowhere else in the paper, by grep); x0 → x̂ (760–827);
z0 → z; y_s → y^{(s)}; x1 → z^+; K0 → K_0; Z'+ → Z''; "C x" → overline (no complement written with C is left in
579–1002); code numbers → code words ({1,3,4,6} = 001, 011, 100, 110; {0,2,5,7} = 000, 010, 101, 111: checked in
813–814). No inconsistent application found. Other letters with a second meaning in the paper, harmless here:
K (closed class in 807; union of the two levels from 871; the unique closed class in Section 2), X (the cycle;
X_t the chain, tex 173), N (rule number 165, a cycle in Lemma 2.5, N(d) here).

## 4. Not checked

* No computation: nothing in this report is confirmed by enumeration. All checks are by hand; the worked cases are
  n = 4 (Corollary 3.21, Proposition 3.22), n = 5 (Lemmas 3.18, 3.25), n = 5, 6, 7 (words z, z^+, bounds).
* The PDF (numbers 3.12–3.28 are counted from the source, not read off a compiled file); Figure 2 itself
  (`figures/fig_crystal_43.pdf`) and the script that draws it; only the caption was compared with Proposition 3.22.
* The cited papers (Fukś, Boccara) and `literature_addendum.md`: the credit paragraph 653–657 was compared with
  P 755–762 and with the quotations in `trace_43_142.md` §5 only. The bibliography entries were not read.
* `VERIFICATION_43_142.md`, `review/second_read.json`, all scripts and their outputs, `REFEREE_NOTES.md`: not
  opened. The verdicts quoted in the trace ("V: confirmed") were not compared with that report.
* Section 2 was read for the hypotheses of `lem:kzero`, `lem:edge`, `lem:sym`, `thm:A` as used in Section 3.2; I
  did not referee the proofs of Lemmas 2.5–2.7 and Theorem 2.8, and did not compare Section 2 with its sources.
* Proposition 3 of P (entry cost) and the paragraph "Description of the cycles" (P 270–280) are not in the paper
  (recorded in the trace); I did not check them. Tables 1–5 of P were not checked.
* Passages outside 579–1002 that cite this section were read once (list in Section 2), not compared with sources.
