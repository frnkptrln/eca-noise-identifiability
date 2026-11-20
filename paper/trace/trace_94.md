# Trace file, track "rule 94 (both directions)"

Fragments: `sec_94_main.tex` (`\section{Rule 94}\label{sec:94}`) and `app_94.tex`
(`\section{Proofs of the lemmas for rule 94}\label{app:94}`).

Abbreviations of the sources (line numbers are those of the files on branch `paper-ring-size`, commit d6c6299):

* **P94** = `verify_ring_size/part2_94/PROOF_94.md` (3 | n, n >= 6)
* **C94** = `proofs_94_26/PROOF_94_converse.md` (3 not dividing n, n >= 5)
* **V9426** = `VERIFICATION_94_26.md`; **VRS** = `VERIFICATION_ring_size.md`; **REP** = `report_ring_size.md`;
  **V43142** = `VERIFICATION_43_142.md`; **LIT** = `literature_ring_size.md`; **ADD** = `literature_addendum.md`

## 0. Not done, cut, not checked

* No script, test or enumeration of the repository was run. Data files were only read (two files, for the field
  names of the `\DATA` items).
* The main-text fragment is **2.97 pages** against a budget of 1.5 (overrun 1.47 pages); the appendix is **4.01
  pages** without the optional block (budget 4.5) and **5.06 pages** with it. Nothing was dropped to meet the
  budget. Section 9 lists what can be moved.
* Not included in the fragments: all tables and computed facts of P94 section 7 and C94 section 7; the remarks of
  P94 section 6 and C94 section 6 on literature, code and process; the gamma_min of the case 3 | n (not stated in
  P94; see section 9).
* I did not read Martin, Odlyzko and Wolfram (1984); the one citation rests on three repository lines (section 5).
* Every proof step was re-derived by hand from the rule table while writing (in particular all window-map
  evaluations of Lemmas swap, merge, split, crystal, 000 and the image rules of alpha and beta). No code was run
  for this. No error was found in P94 or C94.
* The compiled PDF was checked through its text layer and the LaTeX log (no error, no overfull box, no undefined
  reference except the one `\cite` key). The page images were not inspected by eye.

## 1. Statements of the fragment

Verification documents, and what they say (used in the column "verification" below):

* **V9426** (independent verification of `proofs_94_26/`, 20 November 2026). Verdict, lines 17-20: "No false
  mathematical statement in a theorem, and no gap that affects a result. Every theorem, proposition and corollary of
  C94 (Theorems 1, 2, Proposition 3, Corollary 1) ... was re-derived line by line from the rule table and found
  correct". Findings on C94: **C2** (line 56; Lemma 10: the fully frozen case needs Lemma 2 of P94; "gap in a proof
  (closed by one citation)") and **C5** (line 59; Lemma 15: redundant condition; wording). Header lines 3-7: C2 and
  C5 are corrected in the proof document. **Checked here: both are reflected in C94** (C2: lines 226-227, "if the
  flip leaves no window ... fully frozen, hence a block word and a fixed point by Lemma 2 of P94"; C5: lines 275-277,
  "n - 7 = 2a + 3b has a solution for every n - 7 >= 2"). Hand checks: lines 67-85. Own exhaustive tests: lines
  132-148 (n <= 20, no violation). Not checked by V9426 (lines 252-266): rows n = 22, 23 of C94 Table 2 (in
  particular "0 of 33 for n = 22"); potentials of rule 94 for n >= 13; Theorem A, the definition of k_c, Theorem V94;
  "P94 and P154 beyond the results that C94 and C26 cite"; n = 3.
* **V9426 on P94**: line 85: "Cited results of P94 that C94 uses (Lemmas 1, 2, 3, Corollaries 1a, 1b, 3):
  re-checked. Correct." Lines 26-28 and 203-209: potentials, S and k_c computed from the definitions without
  Theorem A agree with P94 Corollary 2 at n = 6, 9, 12. Line 259: the rest of P94 (Lemmas 4, 5, 6, Theorem 1,
  Corollaries 1, 2 as proofs) was **not** checked by V9426.
* **VRS**, D1 (lines 415-448): P94 was written by a proof track of the verification session of 14 November 2026;
  "The lead read every step and re-tested the lemmas with separate code" (lines 436-441: Lemmas 1, 2 on all states
  n = 3..14, Lemma 3, Lemmas 4 and 5 for n = 6..18, Lemma 6 for n = 6..60, closed classes at n = 6, 9, 12, 15; no
  violation). This is a check inside the session that produced P94, not an independent verification.
* **REP**, Section 5.7 (lines 525-533): "(ii) a second read outside both sessions checked PROOF_154.md and
  PROOF_94.md step by step and with separate code (... class 94: Lemmas 1 to 3 on all states and the closed classes
  for n = 6..21, potentials at n = 6, 9) and found no error (as reported by the author; that code is not part of
  this branch)". "They have not been through peer review."
* **V43142**: contains no statement about P94 or rule 94 (searched for "94", "P94", "part2_94").

| paper label | source statement and lines | tag in the source | verification | changes of wording and notation |
|---|---|---|---|---|
| `94:lem:freeze` (i), (ii), (iii) | P94 Lemma 1 (75-80), Corollary 1a (82-83), Corollary 1b (85-87) | [proved] each | V9426 line 85: re-checked, correct. VRS D1 436-437 (lead's test). REP 527-531 (second read). | three source statements merged into one lemma; W -> Fz; "by induction the same holds for F^t" moved into (i) |
| `94:lem:block` | P94 Lemma 2 (89-97) | [proved] | V9426 line 85; VRS D1 436-437; REP 527-531 | W -> Fz; 1^n -> \one |
| `94:lem:growth` | P94 Lemma 3 (99-129) and Corollary 3 (131-135) | [proved] each | V9426 line 85 (Lemma 3, Corollary 3: correct); VRS D1 437-438; REP 527-531 | Lemma 3 and Corollary 3 merged; the first "more precisely" bullet of Lemma 3 (W(y) contains W(x) and j) is not in the statement, only in the proof; the second bullet (x = 0) is kept |
| `94:lem:crystal` | P94 Lemma 6 (171-190); second sentence = proof part (b), lines 182-187, as used in Corollary 2 (229-233) | [proved] | **No independent verification of this statement is recorded in the repository** (V9426 line 259 excludes it). Inside the producing session: VRS D1 436-439 (lead read every step; Lemma 6 on 627 flips, n = 6..60). REP 527-531: second read of PROOF_94.md "step by step ... found no error (as reported by the author)". | the orbit y, Fy, F^2 y of the flip of part (b) is moved from the proof into the statement (the theorem needs it); tuples written as words |
| `94:lem:windows` | C94 Lemma 7 (98-110) | [proved] | V9426 70-72: "every step correct"; test L7ab (137); part (c) is exercised by test T1 (138) | w -> \ell; phi of width \|I\| written \varphi_{\|I\|} |
| `94:lem:cut` | C94 Lemma W (112-121) | [proved] | V9426 70-72; test LW (142) | w -> \ell |
| `94:lem:live` | C94 Lemma 8 (123-184) | [proved] | V9426 70-72: "In Lemma 8 the cases (1) to (7) were followed for an arbitrary orbit state, including the induction on m with c+ and the final condition 3 \| w + 1. Nothing found."; test L8, w = 1..22 (136) | w -> \ell; A_w, B_w -> \alpha_\ell, \beta_\ell; infinite words A, B with letters A(i), B(i) -> \alpha, \beta with \alpha(i), \beta(i); "state" of the orbit -> "(padded) word"; runs R_1..R_r -> J_1..J_r; induction index m -> d; c+ -> c^{+} |
| `94:lem:empty` | C94 Lemma 9 (186-202) | [proved] | V9426 70-72 ("including the GF(2)[S] count ... and D_0(v) != D_1(v')"); test L9n (140) | D_p(v) -> \Delta_p(v); shift S -> \tau (S is the selected set in the paper); V_per -> P_h; 0 -> \zero, 1^n -> \one |
| `94:lem:refreeze` | C94 Lemma 10 (204-228) | [proved] | V9426 73-74: "correct apart from C2"; C2 (line 56) is corrected in C94 lines 226-227 and the correction is in the fragment; test L10 (141) | name "reversible freezing" -> "freezing flips between periodic states"; letters as in Lemma live |
| `94:lem:swap` (a) | C94 Lemma 11 (230-237). It contains P94 Lemma 4 (137-154): same conclusion {x} -> C2 -> {x'}, hypothesis n >= 5 instead of "at least three blocks" | [proved] (both) | C94 Lemma 11: V9426 75-76 ("recomputed by hand. Correct."), test L11 (143). P94 Lemma 4: not independently verified (V9426 259); VRS D1 438 | C2 -> D (cycle letters of the paper); tuples as words |
| `94:lem:swap` (b) | sorting argument: P94 proof of Theorem 1, stage 2, lines 205-210; C94 proof of Lemma 14 (i), lines 259-261 ("The swaps are edges in both directions") | part of [proved] statements, not a numbered statement in either source | as for Theorem 1 of P94 and Lemma 14 of C94 (rows below) | **numbered sub-statement made by taking an argument out of two proofs**; X_c -> X (statement), X_q (proof of Lemma component); positions k < k' -> i < i'; linear word w kept (w is no longer the window width) |
| `94:lem:merge` | C94 Lemma 12 (239-242) = P94 Lemma 5 (156-169) | [proved] (both) | C94 Lemma 12: V9426 75-76, test L12 (144). P94 Lemma 5: VRS D1 438-441 | statement in the form of P94 ("x'' is a block word", edge) with the clause "the next block starts at p+6" of C94 |
| `94:lem:split` | C94 Lemma 13 (244-253) | [proved] | V9426 75-76 ("including the five steps 00100 -> ... -> 01010"), test L13 (145) | C -> D |
| `94:lem:component` | C94 Lemma 14 (255-270) | [proved] | V9426 77-78 ("(i) sorting, X_c ~ X_(c+3), gcd(3, n) = 1; (ii) ...; (iii) b = 0. Correct."), test T2 (148) | X_c -> X_q; "class (a, b)" given one defining sentence |
| `94:lem:000` | C94 Lemma 15 (272-286) | [proved] | V9426 79-80 ("Lemma 15 (C5 only)"; orbit at n = 8 recomputed by hand); C5 (line 59) corrected in C94 275-277; test L15 (146) | A_2, B_5 -> \alpha_2, \beta_5 |
| `94:thm:main` (i), closed classes and paths | P94 Theorem 1 (57-63), proof 194-218 | [proved] | **No independent verification of the proof is recorded in the repository** (V9426 259). VRS D1 436-441 (lead; closed classes n = 6, 9, 12, 15). REP 527-531 (second read; closed classes n = 6..21). V9426 203-209: closed classes [1, 1, 1] recomputed at n = 6, 9, 12 | stage 2 uses `94:lem:swap` (b) instead of Lemma 4 of P94 plus the inversion count (same steps, see section 9) |
| `94:thm:main` (i), S = A | P94 Corollary 1 (65), proof 222-224 | [proved, given Theorem A] | V9426 203-209: S computed from the definitions at n = 6, 9, 12 agrees. Otherwise as the previous row | "resistances are invariant under rotation" -> `lem:sym`; Theorem A -> `thm:A` |
| `94:thm:main` (i), k_v, k* = 1 | P94 Corollary 2 (67-68), proof 226-233 | [proved, given Theorem A] | V9426 26-28, 203-209: k_c and k* computed from the definitions at n = 6, 9, 12 agree. Otherwise as above | codes 3, 5, 6 -> 011, 101, 110; 0, 1, 2, 4, 7 -> 000, 001, 010, 100, 111; D_c -> \Dc{v}; definition of k_c -> `prop:order` |
| `94:thm:main` (ii), K | C94 Theorem 2 (a), (b), (c), (d) (81-87), proof 313-327 | [proved] | V9426 81: "Theorem 2 (a) to (d) ... correct"; test T2 (148), n up to 20 | BW -> K from the start (the source sets K := BW in line 319) |
| `94:thm:main` (ii), S = K, gamma_min, k_v, k* = 0 | C94 Corollary 1 (89-90), proof 352-355 | [proved, given Theorem A] | V9426 81 ("Corollary 1: correct"); 202-208: potentials from the definitions at n = 5, 7, 8, 10, 11 agree | as above |
| `94:rem:small` | P94 247-248 (n = 3 excluded, not examined); C94 356-357, 368-371 (n = 3 not covered; n = 4 [computed]); VRS A10, 212-213 and REP 330-331 (n = 3: one flip leaves the crystal, computed) | not a theorem; [computed for n = 4]; n = 3 computed | n = 4: V9426 test T2 includes n = 4 (line 148) | computed facts written as `\DATA` |
| optional block: `94:prop:periodic` | C94 Theorem 1 (73-79), proof 307-311 | [proved] | V9426 70-72; tests T1, T1p6 (138-139), n = 3..20 | as Lemma empty / live |
| optional block: `94:lem:basin` | C94 Lemma 16 (288-303) | [proved] | V9426 79 ("Lemma 16 (i), (ii), (iii) and the description of the basin of 0: correct"); test L16 (147) | 1^n -> \one |
| optional block: `94:prop:zero` | C94 Proposition 3 (92-94), proof 329-348 | [proved] | V9426 81 ("Proposition 3 (i) to (iii) (the four cases of an edge into {0})": correct); tests L15, T2 (146, 148) | K introduced by reference to `94:thm:main` (ii) |

## 2. GAPs

None. There is no `\GAP` in either fragment.

## 3. Errors found in sources

None. There is no `\SOURCEERR` in either fragment. (Both findings of V9426 on C94, C2 and C5, are already corrected
in C94.)

Points that are not errors but that the editor should know:

* P94 Lemma 6, case (a) ends with "(1,1,1) -> (0,0,0) -> (1,0,1) on I, which is x": this shows F^2(x + e_j) = x; the
  statement F^3(x + e_j) = x then uses that x is a fixed point (first line of the proof: "x is a block word"). The
  fragment writes this out ("so F^2 y = x and F^3 y = x").
* C94 Theorem 2 (b) says "Equivalently: a cycle outside K consists of states without 101"; the fragment states the
  two halves as separate sentences, without "equivalently".
* C94 line 367 says "for 8 | n, n >= 24 this is not determined" inside a document whose range is 3 not dividing n;
  the smallest such n is 32.

## 4. Unified notation: all changes of letter against the sources

W(x) -> Fz(x); A_w, B_w -> alpha_ell, beta_ell; A, B (infinite words), A(i), B(i) -> alpha, beta, alpha(i), beta(i);
w (window width) -> ell; phi_w -> varphi_ell; D_p(v) -> Delta_p(v); S (shift on half words) -> tau; V_per -> P_h
(not on the notation sheet; chosen here); C2 and the 2-cycle C of Lemma 13 -> D; code numbers -> code words;
D_c -> \Dc{v}; k_c -> k_v; 0 -> \zero; 1^n -> \one; BW -> K; a generic closed class in the 3 | n part -> K'
(K is kept for the class of part (ii)); runs R_i -> J_i; induction index m (Lemma 8 (7)) -> d (m is the
number of cycles); positions k < k' -> i < i'; X_c -> X_q; "cell c" in (O1) -> cell q; tuples such as (0,1,0,1,1) ->
words `\code{01011}`; "state of the phi-orbit" -> "word of the orbit"; "type alpha / type beta" kept.
Term taken from C94 line 42 and defined once: "flip between periodic states". "class (a, b)" is defined in one
sentence in the proof of Lemma component (C94 uses it without a definition).

## 5. Credits given

One sentence, in the definitions of `sec_94_main.tex`: "By Lemma 3.7 of \cite{MartinOdlyzkoWolfram1984} these three
states are the non-zero fixed points of rule 90 on rings with 3 | n; rules 90 and 94 agree on the codes 011, 101,
110." Repository lines that state the attribution:

* LIT lines 46-47: "**The class-94 crystal (A30).** The three shifts of 011011... are the non-null fixed points of
  rule 90 for N a multiple of 3 (Martin, Odlyzko and Wolfram, Lemma 3.7, p. 234)."
* REP lines 119-121: "The three phases of (011)^{n/3} are the non-null fixed points of rule 90 for 3 | N given by
  Martin, Odlyzko and Wolfram (1984), Lemma 3.7 (p. 234; read by the verification); rules 94 and 90 agree on the
  codes 3, 5, 6."
* VRS lines 316-317 (finding A30): "The class-94 crystal is the set of non-null fixed points of rule 90 given in
  MOW, Lemma 3.7 (p. 234). A reference to add".
* How the reference was seen: LIT line 15, "Sources now read (by the verification). Martin, Odlyzko and Wolfram
  (1984) in full (author copy at content.wolfram.com)". **Not read by this session.**

No other credit is given in the fragments. Not cited, because the key is not on the list, the text was not read by
any session, or the credit belongs to Section 2:

* Theorem A (`thm:A`) is used in Step 5 of part (i) and Step 4 of part (ii); its credit (Samuelson 1994, Noeldeke
  and Samuelson 1993, Ellison 2000; REP 163-171, LIT 21-29) belongs to its statement in Section 2 and is not
  repeated in this section.
* The definition of k_v (note v0.2, Section 6; P94 226, C94 353) is used through `prop:order`; `PeterleinNote` is
  not cited in the fragment.
* ADD lines 149-156 (Nordahl 1989, read pp. 68-74): rule 94 is among the rules "which are known to be capable of
  simulating rule 90". No key on the list.
* C94 lines 385-391: Schuele and Stoop (arXiv:1107.2080) and Flocchini and Cezar, "search excerpt only", "Neither
  text was read; no source was found for the frozen word 101, the window classification of Lemma 8, or the closed
  class". No key on the list; not cited.
* LIT line 302: "For rules 94, 43, 142, 35 and 122, no source read here states how their cycle structure depends
  on n." LIT 48-50: "No search for these two statements was made after they were proved."

## 6. General facts used beyond the shared statements of Section 2

1. Every integer >= 2 is of the form 2a + 3b with a, b >= 0 (Lemma 000; C94 276-277).
2. Linear algebra over GF(2) in the count of Lemma empty (C94 199-202): in GF(2)[tau]/(tau^h - 1), h = 2^e q,
   q odd, tau^h - 1 = (tau^q - 1)^(2^e); 1 + tau divides tau^q - 1 exactly once; hence dim ker (1 + tau)^j =
   min(j, 2^e); the periodic points of a linear map of a finite vector space form the image of a high power. The
   count is not used by Theorem `94:thm:main`; it is used for the number of states in `94:prop:periodic`, case 2.
3. On doubled words F^2 is conjugate to an invertible shift composed with (1 + tau)^2, so periodicity under F is
   periodicity of v under 1 + tau (C94 197-198; one sentence there, one sentence in the fragment).
4. An adjacent transposition "s l -> l s" lowers the number of inversions by one (P94 209-210).
5. 3 and n coprime: the cells q, q + 3, q + 6, ... exhaust Z/nZ (C94 263).
6. Elementary facts on digraphs: a closed class contains everything reachable from it; a strongly connected
   component that no edge leaves is a closed class (P94 216-218, C94 317-322).
7. F commutes with the reflection rho for rule 94 (f(a,b,c) = f(c,b,a); P94 29-30), used in Lemma crystal (c).
8. Definitions of Section 2 used directly: the step from a fixed point x to x + e_j has resistance 1 and the steps
   along an orbit have resistance 0 (Step 6 of part (i); P94 229-231); S is not empty (Step 5; P94 223); the
   definition of k_v as min_C [gamma(C) + R(C -> D_v)] - gamma_min for the bound k_v <= 1 (P94 226, 233).
9. `lem:sym` is used for the rotation only; `lem:reroot` is not used.

## 7. \DATA items

In the fragment (`94:rem:small`), two items:

1. n = 4: one closed class, the two block words (checkerboards), codes 010 and 101 only.
   File `proofs_94_26/out/g1_classes_94.jsonl`, record `n = 4`, fields `closed_classes`, `block_words`,
   `block_words_all_in_K`, `codes_on_K` (also `cycles_with_101_in_K`, `K_equals_cycles_reachable_from_block_words`
   for "(a), (b), (c) hold"). Source text: C94 21, 368-371, Table 2 row n = 4 (line 423).
2. n = 3: one flip leaves the crystal phase. File `data/ring_size/crystal_radius.csv`, row `rule = 94, n = 3`,
   field `radius_ge2`. Source text: VRS 212-213 (A10; it names `verify_ring_size/phase2/out/crystal_checks.json`),
   REP 330-331.

Both files were opened and the fields exist with the content described. Section 8 names further `\DATA` items for
the section on open cases; they are not in the fragments.

## 8. Which cycles of rule 94 the sources leave undescribed or undecided

Described for every n >= 3 [proved]: all periodic states (C94 Theorem 1, lines 73-79; `94:prop:periodic` in the
optional block). So no cycle is undescribed as a set of states. Not given: the periods of the cycles of doubled
words in closed form (they are the periods of v under 1 + tau; P94 252-256 notes "periods growing irregularly
with n" for these cycles, with the tag "not needed for the proof, not proved").

Decided [proved]:

* 3 | n, n >= 6: S is exactly the three crystal phases; every other cycle is outside S (P94 Theorem 1, Corollary 1).
* 3 not dividing n, n >= 5: every cycle with a 101 is in K = S (C94 Theorem 2 (b), Corollary 1). k* does not
  depend on the open points below (C94 364: "This does not affect Theorem 2 or Corollary 1").
* {0}: in K for n = 5, 7, 8; without incoming edge for n >= 10 with 8 not dividing n, hence not in K if moreover 3
  does not divide n (C94 Proposition 3, lines 92-94; `94:prop:zero`). So for odd n >= 11 with 3 not dividing n,
  K = all cycles except {0}; for n = 5, 7, K = all cycles.

Undecided (the sources say so):

1. **Cycles of doubled words on even rings with 3 not dividing n** (they exist unless n is a power of two): which of
   them lie in K. C94 20 and 361-364: "[computed for n = 10, 14, 16, 20, 22]; no rule was found", "nothing claimed
   for larger n". `\DATA{numbers of cycles of doubled words in K and outside K for n = 10, 14, 20, 22}
   {proofs_94_26/out/g1_classes_94.jsonl, fields cycles_without_101, cycles_without_101_in_K, zero_state_in_K,
   periods_without_101_in_K, periods_without_101_outside_K}` (the number of doubled-word cycles is
   `cycles_without_101` minus one for {0}; C94 Table 2, lines 421-436, column "cycles of doubled words in K").
   V9426 254-255: the rows n = 22, 23 of this table, "in particular '0 of 33 for n = 22'", were **not** checked by
   the independent verification; the values for n = 10, 14, 20 were recomputed there (V9426 42-44).
2. **{0} when 8 | n and 3 does not divide n, n >= 32** (C94 365-367 writes "for 8 | n, n >= 24 this is not
   determined"; Lemma 16 describes the basin of 0 only for 8 not dividing n; for 8 | n the basin has further
   levels, e.g. (00001111)^(n/8)). n = 8: in K [proved, Lemma 15]. n = 16: `\DATA{the cycle of the zero state is
   not in K and has no incoming edge at n = 16}{proofs_94_26/out/g1_classes_94.jsonl, record n = 16, fields
   zero_state_in_K, zero_state_in_degree}` (C94 366-367, [computed]).
3. **n = 4** ([computed] only; C94 368-371) and **n = 3** (not examined in P94, lines 247-248; not covered in C94,
   line 357; one computed fact, item 2 of section 7).
4. **3 | n**: nothing is undecided about S. Not stated in the sources of this track: gamma_min for 3 | n (section 9).

Computed facts of P94 that a section on open cases might quote, with their file: closed classes of G1 computed
directly for 3 | n up to n = 27, `verify_ring_size/part2_94/out/g1_classes.jsonl`, fields `closed_classes`,
`closed_class_sizes`, `cycles`, `period_hist` (P94 Table 2, lines 285-296; periods of the cycles: P94 252-254).

## 9. Notes for the editor

* Length (compiled with the harness: 10pt, a4, margins 2.6 cm; measured with \pdfsavepos from the first to the
  last line of each fragment): main 2.97 pages = definitions 0.4 + idea 0.2 + fourteen lemma statements 1.2 +
  theorem 0.2 + proof of the theorem 0.9 + remark 0.1. Appendix 4.01 pages; with the optional block 5.06.
  Ways to shorten the main text without losing a step: (1) move the statements of Lemmas windows, cut, live,
  split and the definitions of the window map, padded word, live, alpha, beta to the appendix (about 0.5 page);
  (2) move Steps 1 to 4 of part (i) and Steps 1 to 3 of part (ii) of the proof into the appendix as two
  propositions (about 0.6 page). Both together give about 1.9 pages. 1.5 pages is not reachable with all fourteen
  statements and the proof of the theorem in the main text.
* P94 Lemma 4 (swap, one direction, "at least three blocks") does not appear as a statement: C94 Lemma 11 has the
  same conclusion under n >= 5 and in both directions, and the paper uses it in both parts. P94 Lemma 5 (merge) is
  proved in the form of C94 Lemma 12 (through Lemma W), with the hypothesis checks of P94 lines 161-162, 168-169.
* `94:lem:swap` (b) is a statement that neither source numbers; it is the sorting argument of P94 stage 2 and of
  C94 Lemma 14 (i), stated once. For 3 | n the source sorts with Lemma 4 of P94; the paper sorts with Lemma 11 of
  C94, which C94 states for every n >= 5 without a condition on n mod 3. If this recombination is not wanted, P94
  Lemma 4 with its proof (lines 137-154) has to be added and Step 3 of part (i) reverted to P94 204-212.
* gamma_min for 3 | n is not in P94 and not in the theorem. Lemma B of the report (REP 207-213) would give
  m + q - 2 with q = 3 from part (i), but Lemma B is not among the shared statements of Section 2 and the inference
  is not made in P94; nothing is claimed. (Computed values exist: V9426 lines 203, 206, 209, columns m and
  gamma_min for n = 6, 9, 12.)
* The optional block at the end of `app_94.tex` (between two comment lines) holds C94 Theorem 1, Lemma 16 and
  Proposition 3 with complete proofs. Theorem `94:thm:main` does not need it; the section on open cases can cite it.
  `94:prop:zero` refers to `94:thm:main` and to Lemmas growth, empty, 000.
* Symbols not on the notation sheet: P_h, tau, D (2-cycles), K' (generic closed class in part (i)), J_i (runs).
* The fragments use `enumitem` options (`label=`, `leftmargin=*`, `nosep`), `\mathrm{GF}`, `\mathbf{Z}`,
  `\paragraph`; all compile with the preamble. Labels: `sec:94`, `app:94`, `app:94:further`, and `94:...`.

## 10. Second pass: source lines of every step

### Definitions and facts (sec_94_main.tex, head of app_94.tex)

| item | source lines |
|---|---|
| rule table, verbal form, f(a,b,c) = f(c,b,a) | P94 24-30; C94 38-39 |
| Occ, frozen set, fully frozen | P94 39-44 |
| block words, 2a + 3b = n | P94 51-53 |
| crystal phases, A | P94 36-37, 53 |
| sentence on rule 90 | LIT 46-47; REP 119-121 |
| windows | C94 66-67 |
| window map, padded word, unfrozen, live | C94 58-61 |
| alpha, beta, alpha_ell, beta_ell | C94 62-65 |
| doubled words, P_h | C94 68-69 |
| idea paragraph | REP 537-550; VRS 421-434; P94 240-243; C94 32-34 |
| (O1), (O2) | P94 46-49; C94 46-47 |
| flip between periodic states | C94 40-42 (with `lem:edge`) |

### Lemma freeze
(i) evaluation at i, i-1, i+1: P94 78-80; consequences and induction: P94 75-76. (ii) P94 82-83. (iii) P94 87.

### Lemma block
P94 92-97, sentence by sentence.

### Lemma growth
Occ(y) contains Occ(x), W(F^t y) contains W(x): P94 105-106. (a): P94 108-111. (b) reduction: P94 113-114; "so
does Fz(F^t y) for all t >= 0": P94 102, 105-106. Case 1: P94 116. Case 2: 117-119. Case 3: 120. Case 4: 122-123.
Case 5: 124. Case 6: 125-127. Exhaustiveness for x_i = 0: P94 121. Distinct cells: P94 129. Edge of G1: P94
134-135, with `lem:edge` (P94 32-34).

### Lemma crystal
First line: P94 174, 89-90. (a): P94 176-180; "F^2 y = x and F^3 y = x": P94 171-172, 174, 180 (see section 3).
(b): P94 182-187; second statement of the lemma: P94 186-187 (the three words on I, and "every cell outside I is
frozen"). (c): P94 189-190.

### Lemma windows
(a) C94 104-105. (b) C94 106-107. (c) C94 108-110.

### Lemma cut
C94 116-121.

### Lemma live
Set-up: C94 128-131. (1): 133-134. (2): 136-139. (3): 141-143. (4)(i): 145-147; (ii): 147-149; (iii): 149-151;
(iv): 151. (5): 153-158. (6): 160-163. (7) first paragraph: 165-167; type beta: 168-170; type alpha: 171-173;
induction: 173-179; conclusion: 180-181; converse: 182-184.

### Lemma empty
First paragraph: C94 190-195. Doubled words under F: 196-198. Count: 199-202.

### Lemma refreeze
Choice of y, I, c: C94 208-210. Four cases: 211-213, 214-215, 216-217, 218-219. j not frozen, exactly one new
centre, two or three new cells: 220-223. Remaining window and other windows: 223-226. Periodicity, and the fully
frozen case (finding C2): 226-227. Another cycle: 227-228. "flip between periodic states": 205-206, 40-42.

### Lemma swap
(a) Lemma cut applies, hypotheses: C94 235-236 (ell <= n - 3: C94 112, 230). phi_2: 236. Contents after one and two
flips: 236-237. "All four states are periodic": 237; x' a block word: P94 152-153; x, x' fixed: P94 89-90; the
2-cycle: C94 232. Edges: C94 233, 40-42.
(b) Cut at a block start, linear word: P94 205-206; C94 259. Swap of an adjacent pair, consecutive on the ring:
P94 207-209. Edges in both directions: C94 260-261 (with (a)). Inversions, at most ab swaps: P94 209-210.

### Lemma merge
Lemma cut with I = {p+2, p+3, p+4}, contents 010, 000, phi_3(000) = 101: C94 241-242. Hypotheses of Lemma cut
(x_p x_(p+1) = 01, x_(p+5) = 1, x_(p+6) = 0, the case n = 6): P94 157, 161-162; C94 239-240. x'' a block word,
fixed, different from x: P94 168-169. Edge: P94 158-159, `lem:edge`.

### Lemma split
C94 249-253. Closing sentence (period 2, flip of p+6, F^5, edges): C94 246-247.

### Lemma component
a >= 1: C94 258. (i): 259-263 (sorting through Lemma swap (b)). (ii): 264-267. (iii): 268-270.

### Lemma 000
n = 7 or n >= 10: C94 275-280. n = 5: 281-283. n = 8: 284-286.

### Theorem 94:thm:main
Statement (i): P94 57-68. Statement (ii): C94 81-90. Last sentence (n = 3, 4): P94 247-248; C94 357, 368-371.
Proof, part (i). Step 1: P94 194-196. Step 2: 198-202. Step 3: 204-205 and 210-214, with Lemma swap (b) for
205-210. Step 4: 216-218. Step 5: 222-224. Step 6: 226-233.
Proof, part (ii). K: C94 313, 319. Step 1: 314-316. Step 2: 317-323. Step 3: 324-327 (a_0, b_0: 267, 324).
Step 4: 352-355.

### Optional block
Proposition periodic: statement C94 73-79; proof 307-311. Lemma basin: statement 288-292; proof (i) 294-295, (ii)
295-297, (iii) 297-303. Proposition zero: statement 92-94; (i) 329-331 (the last clause "as for n = 5": 282-283);
(ii) 332-346; (iii) 347-348.

Every step of every proof in the two fragments has a line range above.
