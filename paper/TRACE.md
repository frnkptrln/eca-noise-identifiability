# TRACE of `paper/ring_size_paper.tex`

Written on 20 November 2026 by the session that assembled the paper. Line numbers refer to the repository at branch
`paper-ring-size` after the two merges (commit d6c6299).

Updated on the same day by a later session (Claude), after the author's reader had read the PDF of commit 72cc2ad and
the author had decided the four open points of `REFEREE_NOTES.md`. That session added Appendix B (rule 26), the
classes 60 and 90 in Section 6.2, the report on Zhu and Richard, five entries of the list of references and the new
wording of the abstract, of "Status of the proofs" and of the statement on the use of AI. Its rows and items are
marked "(update)". It worked on `HEAD` dc5ac15; `proofs_94_26/PROOF_26.md` and `VERIFICATION_94_26.md` are
unchanged between d6c6299 and dc5ac15 (`git diff` is empty), so their line numbers hold for both. The statements and
proofs of Sections 2 and 3 and of Appendix A were not changed; their numbers in the PDF are the same as before.

How the paper was put together. Sections 1, 2, 3 (head), 4, 6 and the statements at the end were written by the
assembling session. Sections 3.1 (rule 154), 3.2 (rules 43 and 142), 3.3 with Appendix A (rule 94), 5 (rule 26) and
a draft of Section 6.1 with the bibliography were each written by a sub-session that had one source document as
its task, the instruction to add no mathematical step, and the duty to give for every step of every proof the line
range of the source that contains it. Those line-by-line records are kept in `paper/trace/` as they were delivered (one internal file link in
`trace_154.md` was replaced by the file name):

| file | covers |
|---|---|
| `trace/trace_154.md` | Section 3.1 |
| `trace/trace_43_142.md` | Section 3.2 |
| `trace/trace_94.md` | Section 3.3 and Appendix A |
| `trace/trace_26.md` | Section 5 |
| `trace/trace_refs.md`, `trace/attributions.md` | references and credits (written for a longer list of references than the paper has; see Part B) |

The files of `trace/` name statements by their LaTeX labels (first column of Part A) and were written before the
assembly; what was changed afterwards is listed in Part C. No sub-session reported a gap (a step that is not in the
source). Errors and inconsistencies found in sources are in Part D; none of them is a wrong mathematical step.

## Part A. Every theorem, proposition, lemma and corollary

Columns: number in the PDF; LaTeX label; source document, statement and lines; tag in the source; verdict of the
verification; changes of wording and notation. Rows of Sections 3.1, 3.2, 3.3, 5 and Appendix A are copied from the
tables of the files in `trace/`, where the abbreviations of the verification documents are explained.

| no. | label | source | tag | verification | changes |
|---|---|---|---|---|---|
| Proposition 2.1 | `prop:order` | `note/note_v0.2.tex`, Theorem 1 (label `thm:order`, line 195), with its proof there | proved (note v0.2: "Proved for all n: ... Theorem 1") | `VERIFICATION_v02.md`, finding V11 and the paragraph "Proofs (task 4)": order formula and reduction to cycles "correct"; V11: "correct in outline, four steps asserted rather than shown", added to the proof in v0.2 (header of that file). No later verification. | Quoted, not proved in the paper. Only three statements are taken over: the order of pi(x), nu_v ~ a_v eps^(k_v), rho ~ a eps^(k*) log(1/eps). Code index c in 0..7 -> code word v; D_c -> calligraphic D_v; ord pi(x) -> "of exact order eps^(o(x))"; R(C -> x) -> R(C -> {x}). The paper uses it only for the interpretation of k_v. |
| Lemma 2.2 | `lem:kzero` | Not a numbered statement of a source. First two sentences: `note/note_v0.2.tex`, last lines of the proof of Theorem 1 ("Since a move of resistance 0 from a cycle state stays on its cycle, R(C -> x) = 0 iff x in C; hence ... k_c = 0 for every c iff the noise-selected cycles jointly contain all eight codes"). Third clause (k_v <= 1): the argument of `proofs_43_142/PROOF_43_142.md` l. 356-366 (Corollary 2), of `verify_ring_size/part2_94/PROOF_94.md` Corollary 2 and of `verify_ring_size/part2_154/PROOF_154.md` Theorem 1(f). | proved (inside the proofs named) | `VERIFICATION_v02.md` V11(a) (the step "R(C -> x) = 0 iff x in C" was asked for and added). `VERIFICATION_43_142.md` l. 63-64 (Corollary 2 "confirmed (given Theorem A) and the k_c formula"). | Stated once as a lemma about the integers k_v, so that the sections can cite it; the sources repeat the argument in each corollary. The tracks' sections cited `prop:order` for it; changed to this lemma at assembly. |
| Lemma 2.3 | `lem:edge` | `verify_ring_size/part2_154/PROOF_154.md`, Lemma 0, l. 48-54. Also `proofs_43_142/PROOF_43_142.md` l. 59-63. Last sentence ("a flip between periodic states"): `proofs_94_26/PROOF_94_converse.md` l. 41-42, `proofs_94_26/PROOF_26.md` l. 44-45. | [proved] | `VERIFICATION_ring_size.md` D2 (lead read every step of PROOF_154.md); `VERIFICATION_43_142.md` l. 50: "G1 = {V = 1}: confirmed". | Site -> cell; "enters C'" -> "ends on C'"; the "in particular" sentence is added from the two later documents and proved by applying the first statement twice. |
| Lemma 2.4 | `lem:sym` | `report_ring_size.md`, Section 4, last sentence of the proof of Lemma B (l. 212-213: "gamma is constant on a rotation orbit because F commutes with rotations") and l. 218-219 ("rotation symmetry gives S = A"). | [proved] (as part of Lemma B) | `VERIFICATION_ring_size.md` l. 334-342: Lemma B correct; "Theorem A then puts S inside A and rotation symmetry gives S = A". | Made a numbered lemma. The one-line reason of the source is written out (sigma maps cycles to cycles, preserves resistances, paths and in-trees). Stated for the rotation only. For the complement, Lemma 43:lem:Z proves what it needs in place, as its source does. |
| Lemma 2.5 | `lem:reroot` | `report_ring_size.md`, Section 4, paragraph "Re-rooting", l. 173-176. | [proved] | `VERIFICATION_ring_size.md` l. 334-335: "correct are the re-rooting statement, Lemma 1, Lemma 2, Theorem A including gamma_min = m - 1 and the k* consequence"; sweep without counterexample (l. 344-345). | Root R -> B (R is the path resistance in the paper). |
| Lemma 2.6 | `lem:closure` | `report_ring_size.md`, Section 4, Lemma 1 (closure), l. 178-179. | [proved] | as for Lemma 2.5 (`VERIFICATION_ring_size.md` l. 334-336, 344-345). | S -> calligraphic S. |
| Lemma 2.7 | `lem:inclosed` | `report_ring_size.md`, Section 4, Lemma 2, l. 181-191. | [proved] | `VERIFICATION_ring_size.md` l. 334-336 (correct). `VERIFICATION_43_142.md`, finding B4 (wording): "a closed class K is reachable from every node" must read "some closed class is reachable from every node"; the header of that file says B4 is not applied in the report (the file belongs to v0.3). | The corrected reading of finding B4 is used: "Some closed class K is reachable from C". This is the one place where the paper departs from the wording of a source because of a recorded finding; the source file is not changed. Nodes D_0..D_k -> C_0..C_k; the edge e* = (E -> X) -> (D -> D') (E and X have other meanings in the paper); "simple path" -> "path without repeated node". |
| Theorem 2.8 | `thm:A` | `report_ring_size.md`, Section 4, Theorem A, l. 193-199. | [proved] | `VERIFICATION_ring_size.md` l. 334-336 (correct, "including gamma_min = m - 1 and the k* consequence"); findings A20, A21 (attribution, provisional on the primary texts). | The third sentence of the source's statement ("Hence k* = 0 iff the selected closed classes jointly contain all eight codes") is not in the theorem; its special case for a unique closed class stands as a sentence after the proof, with Lemma 2.2. The attribution paragraph follows `report_ring_size.md` l. 163-171. |
| Theorem 3.1 | `thm:main` | Parts (a), (b), (c) are the theorems 154:thm:main, 43:thm:main, 94:thm:main of the paper (rows below). | - | see the three rows | Statement of the three results in one theorem, with the ranges of each part as in its section. (c) is written as two implications because the two directions have different ranges. |
| Lemma 3.2 | `154:lem:local` | P154 Lemma 1, l. 58-61 | [proved] | V-D2 l. 478-479: "the formula of Lemma 1" tested n = 3..16. R-5.7 (ii): no error found. | The rule is introduced by its table (f = 1 on 001, 011, 100, 111) instead of "bit (4a+2b+c) of 154" (NOTATION forbids the number of a code); the proof compares the eight values with that table instead of with the binary digits of 154. |
| Lemma 3.3 | `154:lem:rule90` | P154 Lemma 2, l. 63-69 | [proved] | V-D2: read; no separate test named for this lemma in D2. R-5.7 (ii): no error found. | "rule 90, L = sigma + sigma^(-1)" moved to the opening paragraph; site -> cell. |
| Lemma 3.4 | `154:lem:nilpotent` | P154 Lemma 3, l. 71-80 | [proved] | V-9426 l. 104: "correct". V-D2: read. R-5.7 (ii): no error found. | Exponent 2^j -> 2^s (j is a cell in the paper); e_i -> e_j. |
| Lemma 3.5 | `154:lem:invariant` | P154 Lemma 4, l. 84-91 | [proved] | V-D2 l. 480: "F(M) lies in M ... at every even n" (n <= 16). R-5.7 (ii): no error found. | site -> cell. |
| Lemma 3.6 | `154:lem:collisions` | P154 Lemma 5, l. 93-113 | [proved] | V-D2 l. 477-480: the lead "re-derived the four local cases of Lemma 5"; "all pairs of states with equal image (257 pairs at n = 16) are of the three kinds of Lemma 5". R-5.7 (ii): no error found. | x' -> y; (*) -> equation (1) of the section; site -> cell. |
| Lemma 3.7 | `154:lem:periodic` | P154 Lemma 6, l. 120-128 | [proved] | V-D2 l. 480-481: "every state of M is periodic at every even n; at n = 4, 8, 16 the periodic states are M and 0". R-5.7 (ii): no error found. | The count (2^(n/2) - 1)^2 + 1 is left out (Section 6); "periodic states of rule 90" -> "of L"; F^j(x) = x -> F^t(x) = x. |
| Lemma 3.8 | `154:lem:moves` | P154 Lemma 7 (a), (c), l. 130-141 | [proved] | V-D2: read; "symmetry of the edges between cycles in M, connectivity inside M" are tests of P154's own Section 5 (l. 226-228), not of the lead. R-5.7 (ii): no error found. | Part (b) of the source is left out (not used by the theorems); source (c) is (b) of the paper. Flipped cell i -> j. Proof of (a) uses the last sentence of `lem:edge` instead of two applications of Lemma 0. 1^n -> \one. |
| Theorem 3.9 | `154:thm:pow2` | P154 Theorem 1 (a)-(f), l. 145-183 | [proved] | V-D2 l. 453-455 (statement), l. 480-484: at n = 4, 8, 16 "{0} has no out-edge, every cycle reaches {0}, and the G1 distance never exceeds the bound of Theorem 1"; "The sealed sample shows the potentials of Theorem 1(e) at n = 8 and 16". R-5.7 (ii): potentials from the definitions at n = 4, 8; no error found. | Codes as words: k_0 -> k_000, "c = 1..7" -> "the seven codes v != 000"; S = {{0}}; G1 -> G_1; "enters/ends in" -> "ends on"; (b) is argued from the statement of `lem:edge` (orbit of 0 + e_j) instead of from the form of a path of resistance 1; "(Proposition prop:order)" added as the reference for k_000 = 0. |
| Theorem 3.10 | `154:thm:other` | P154 Theorem 2, l. 194-211 | [proved] | V-D2 l. 456 (statement), l. 482-484: "G1 is strongly connected at n = 6, 10, 12, 14"; "gamma = m - 1 for all cycles at n = 20 and 21" (sealed sample). R-5.7 (ii): potentials at n = 5, 6, 10; no error found. | "k_v = 0 for all eight codes v" moved from the last line of the source's proof into the statement; "The cube graph is connected" -> "Any two states are joined by a sequence of single flips"; states written as words 0^(n-2)11 etc. in \code; "(Proposition prop:order)" added as reference for the last line. |
| Theorem 3.11 | `154:thm:main` | P154 Corollary, l. 213-214, with the values of k_v from Theorem 1(f) (l. 152) and the last line of the proof of Theorem 2 (l. 211) | [proved] | V-D2 l. 457: "k* = 1 iff n is a power of two (n >= 4), for all n >= 3". R-5.7 l. 558-559. No separate check beyond those of the two theorems. | "The selected set is {0}" -> S = {{0}} (set of cycles); the values of k_v are added to the statement from the two theorems. Ranges as in the source: every n >= 3; "power of two (n >= 4)". |
| Lemma 3.12 | `43:lem:R` | Section 1, form (R); rule tables 44-45, form 47-52 | [proved: compare with the eight table entries] | V line 50: "Section 1: (R), D1 to D3, isolated/interior via P and Q, G1 = {V = 1}: confirmed", hand check "all eight table entries", own test n = 3..20 | made a numbered lemma; the two rule tables are printed as a table of values; codes as words, not numbers |
| Lemma 3.13 | `43:lem:wall` | Lemma 1; statement 143-148, proof 150-161 | [proved] | V line 51: confirmed with remarks (B3). B3 (V 91-93) is wording: the two constants 1 were dropped without comment. Applied in P line 159. Own test n = 3..20, all states | 1 - d written as 1 + d (sums mod 2, as in the proof of P); "rule 226", "rule 184" written as the local maps g_226, g_184 |
| Lemma 3.14 | `43:lem:cons` | Lemma 2 (163-166) and Lemma 5 (228-233), merged | [proved], [proved] | V lines 52, 55: both confirmed; n = 3..20 | merged into one lemma with parts (a), (b); "F C = C F" written F(cpl x) = cpl F(x); the parity statement (D2, line 74) is in the definition paragraph and recalled in (b) |
| Lemma 3.15 | `43:lem:flip` | Lemma 6, 235-237 | [proved] | V line 56: confirmed; all (state, cell), n = 3..20 | (D3) is equation (43:eq:flip) |
| Lemma 3.16 | `43:lem:pairs` | Lemma 3; statement 168-184, proof 186-207 | [proved] | V line 53: confirmed; hand check of the four bracket combinations for each equivalence, of n = 3 (cells i-1 and i+2 coincide), of P(rho d) = -P(d) - 1; n = 3..20 | A(d), A'(d) renamed N(d), N'(d) (the letter A is reserved for rule 94) |
| Lemma 3.17 | `43:lem:pww` | Lemma 4; statement 209-213, proof 215-226 | [proved] | V line 54: confirmed; c in {1..n}, c = n included; reflection; n = 3..20 | period T renamed t_0; the number c renamed g; the four implications of the display 212-213 written as one sentence |
| Lemma 3.18 | `43:lem:per` | Lemma 7; statement 239-252, proof 254-268 | [proved] | V line 57: confirmed; four formulas re-derived; (c) for r of either parity; n = 3..20 | "C sigma x" written cpl(sigma x); exponent r renamed s (r is the resistance in the paper); in (c) "F^t u = C^t sigma^t u" spelled out by the parity of t |
| Lemma 3.19 | `43:lem:half` | Lemma 8; statement 282-284, proof 286-290 | [proved] | V line 59: confirmed, n = 4 included; n = 3..20 | x0 renamed \hat x; the sentence "More generally, for even n ..." is put first; "they contain only the codes 001, 011, 110, 100" moved from the proof (P 289-290) into the statement, because Corollary 43:cor:div cites it |
| Theorem 3.20 | `43:thm:crystal` | Theorem 1; statement 104-111, proofs 294-311 | [proved] | V line 60: confirmed; n = 4: w in {0, 2, 4}; n = 4..20 with 4 dividing n | "r(X) >= 2" written "V(X, C') >= 2 for every cycle C' != X" (notation sheet); "returns to X" written "ends on X"; the "Consequently" sentence is item (3) |
| Corollary 3.21 | `43:cor:div` | Corollary 1 (123-124, proof 352-353) and Corollary 2 (126-127, proof 355-366), merged | [proved, given Theorem A] both | V lines 63-64: "confirmed (given Theorem A)", Corollary 2 also "and the k_c formula"; "without Theorem A confirmed by computation for n = 4, 8, 12"; y, y' and their codes checked at n = 4 | merged; k_c -> k_v with code words; S -> \Sel; D_c -> \Dc{v}; the definition of k_c is not repeated (prop:order of Section 2 is cited for "k_v = 0 iff v occurs in a state of a selected cycle"); the description of y, y' is written as lists of cell values |
| Proposition 3.22 | `43:prop:heal` | Proposition 2; statement 113-118, proof 313-332 | [proved] | V line 61: confirmed; "at n = 4 the window j-2..j+1 is the whole ring and t* = n/2 - 2 = 0, checked"; n = 4..20, all 4n flips | A, A' -> N, N'; "(For n = 4, n/2 - 1 = 1)" appears in the proof only |
| Lemma 3.23 | `43:lem:levels` | Lemma 9; statement 377-381, proof 383-390; setting 98-100, 373-375 | [proved] | V line 65: confirmed; bounds 2 <= w- < n/2 < w+ <= n-1 checked for n = 5, 6, 7 and each residue class; n = 5..19 | eps renamed \eta (\eps is taken in the paper); (b) "lower -> lower or upper; likewise for the upper level" written "a flip of a state of a cycle of K leads to a cycle of K" |
| Lemma 3.24 | `43:lem:slides` | Lemma 10; statement 392-400, proof 402-415 | [proved] | V line 66: confirmed; boundary cases w = 2 in (a), n - w >= 1 and 2w - n >= 1 in (b); procedures executed n = 3..20 | runs R_k renamed I_k and lengths r_k renamed \lambda_k (R, r are resistances in the paper); the first statement is proved by citing the last sentence of lem:edge, which is the argument of P 402-403 |
| Lemma 3.25 | `43:lem:Z` | Lemma 11; statement 417-422, proof 424-433 | [proved] | V line 67: confirmed; "The case Z = C Z occurs (rule 43, n odd ...) and is covered by the statement"; n = 5..19 | z0 -> z; y_s -> y^{(s)}; eps -> \eta; C Z -> cpl Z |
| Theorem 3.26 | `43:thm:levels` | Theorem 2; statement 129-131, proof 435-452 | [proved] | V line 68: confirmed; Steps 1 to 3; n = 5, 6, 7 written out; n = 3 and n = 5..19 by computation | x1 -> z^+; Z+ -> Z^+; D+ -> D^+; Z'+ -> Z''; K0 -> K_0; exponent r -> s |
| Corollary 3.27 | `43:cor:ndiv` | Corollary 3; statement 133-134, proof 454-458 | [proved, given Theorem A] | V line 69: "confirmed (given Theorem A); without Theorem A confirmed by computation for n = 5, 6, 7, 9, 10, 11, 13, 14"; codes of z0 also for w- = 2 | k_c -> k_v; S -> \Sel; "on a state" -> "in a state" |
| Theorem 3.28 | `43:thm:main` | Corollary 4; statement 136-137, proof 460 | [proved, given Theorem A] | V line 70: "confirmed (given Theorem A); without Theorem A confirmed by computation for n = 4..14" | called Theorem (task); added the sentence "In particular k* = 1 iff 4 divides n", which is the same statement because k* is 0 or 1 in the two cases |
| Lemma 3.29 | `94:lem:freeze` | P94 Lemma 1 (75-80), Corollary 1a (82-83), Corollary 1b (85-87) | [proved] each | V9426 line 85: re-checked, correct. VRS D1 436-437 (lead's test). REP 527-531 (second read). | three source statements merged into one lemma; W -> Fz; "by induction the same holds for F^t" moved into (i) |
| Lemma 3.30 | `94:lem:block` | P94 Lemma 2 (89-97) | [proved] | V9426 line 85; VRS D1 436-437; REP 527-531 | W -> Fz; 1^n -> \one |
| Lemma 3.31 | `94:lem:growth` | P94 Lemma 3 (99-129) and Corollary 3 (131-135) | [proved] each | V9426 line 85 (Lemma 3, Corollary 3: correct); VRS D1 437-438; REP 527-531 | Lemma 3 and Corollary 3 merged; the first "more precisely" bullet of Lemma 3 (W(y) contains W(x) and j) is not in the statement, only in the proof; the second bullet (x = 0) is kept |
| Lemma 3.32 | `94:lem:crystal` | P94 Lemma 6 (171-190); second sentence = proof part (b), lines 182-187, as used in Corollary 2 (229-233) | [proved] | **No independent verification of this statement is recorded in the repository** (V9426 line 259 excludes it). Inside the producing session: VRS D1 436-439 (lead read every step; Lemma 6 on 627 flips, n = 6..60). REP 527-531: second read of PROOF_94.md "step by step ... found no error (as reported by the author)". | the orbit y, Fy, F^2 y of the flip of part (b) is moved from the proof into the statement (the theorem needs it); tuples written as words |
| Lemma 3.33 | `94:lem:windows` | C94 Lemma 7 (98-110) | [proved] | V9426 70-72: "every step correct"; test L7ab (137); part (c) is exercised by test T1 (138) | w -> \ell; phi of width \\|I\\| written \varphi_{\\|I\\|} |
| Lemma 3.34 | `94:lem:cut` | C94 Lemma W (112-121) | [proved] | V9426 70-72; test LW (142) | w -> \ell |
| Lemma 3.35 | `94:lem:live` | C94 Lemma 8 (123-184) | [proved] | V9426 70-72: "In Lemma 8 the cases (1) to (7) were followed for an arbitrary orbit state, including the induction on m with c+ and the final condition 3 \\| w + 1. Nothing found."; test L8, w = 1..22 (136) | w -> \ell; A_w, B_w -> \alpha_\ell, \beta_\ell; infinite words A, B with letters A(i), B(i) -> \alpha, \beta with \alpha(i), \beta(i); "state" of the orbit -> "(padded) word"; runs R_1..R_r -> J_1..J_r; induction index m -> d; c+ -> c^{+} |
| Lemma 3.36 | `94:lem:empty` | C94 Lemma 9 (186-202) | [proved] | V9426 70-72 ("including the GF(2)[S] count ... and D_0(v) != D_1(v')"); test L9n (140) | D_p(v) -> \Delta_p(v); shift S -> \tau (S is the selected set in the paper); V_per -> P_h; 0 -> \zero, 1^n -> \one |
| Lemma 3.37 | `94:lem:refreeze` | C94 Lemma 10 (204-228) | [proved] | V9426 73-74: "correct apart from C2"; C2 (line 56) is corrected in C94 lines 226-227 and the correction is in the fragment; test L10 (141) | name "reversible freezing" -> "freezing flips between periodic states"; letters as in Lemma live |
| Lemma 3.38 | `94:lem:swap` | sorting argument: P94 proof of Theorem 1, stage 2, lines 205-210; C94 proof of Lemma 14 (i), lines 259-261 ("The swaps are edges in both directions") | part of [proved] statements, not a numbered statement in either source | as for Theorem 1 of P94 and Lemma 14 of C94 (rows below) | **numbered sub-statement made by taking an argument out of two proofs**; X_c -> X (statement), X_q (proof of Lemma component); positions k < k' -> i < i'; linear word w kept (w is no longer the window width) |
| Lemma 3.39 | `94:lem:merge` | C94 Lemma 12 (239-242) = P94 Lemma 5 (156-169) | [proved] (both) | C94 Lemma 12: V9426 75-76, test L12 (144). P94 Lemma 5: VRS D1 438-441 | statement in the form of P94 ("x'' is a block word", edge) with the clause "the next block starts at p+6" of C94 |
| Lemma 3.40 | `94:lem:split` | C94 Lemma 13 (244-253) | [proved] | V9426 75-76 ("including the five steps 00100 -> ... -> 01010"), test L13 (145) | C -> D |
| Lemma 3.41 | `94:lem:component` | C94 Lemma 14 (255-270) | [proved] | V9426 77-78 ("(i) sorting, X_c ~ X_(c+3), gcd(3, n) = 1; (ii) ...; (iii) b = 0. Correct."), test T2 (148) | X_c -> X_q; "class (a, b)" given one defining sentence |
| Lemma 3.42 | `94:lem:000` | C94 Lemma 15 (272-286) | [proved] | V9426 79-80 ("Lemma 15 (C5 only)"; orbit at n = 8 recomputed by hand); C5 (line 59) corrected in C94 275-277; test L15 (146) | A_2, B_5 -> \alpha_2, \beta_5 |
| Theorem 3.43 | `94:thm:main` | C94 Corollary 1 (89-90), proof 352-355 | [proved, given Theorem A] | V9426 81 ("Corollary 1: correct"); 202-208: potentials from the definitions at n = 5, 7, 8, 10, 11 agree | as above |
| Remark 3.44 | `94:rem:small` | P94 247-248 (n = 3 excluded, not examined); C94 356-357, 368-371 (n = 3 not covered; n = 4 [computed]); VRS A10, 212-213 and REP 330-331 (n = 3: one flip leaves the crystal, computed) | not a theorem; [computed for n = 4]; n = 3 computed | n = 4: V9426 test T2 includes n = 4 (line 148) | computed facts written as `\DATA` |
| Definition 5.1 | `26:def` | S section 1, L54-68 (moving frame L54-56, c L57-58, groups and sources L59-61, domain states L62-67, carrier words L68); "contained in E ∪ O" L48-49 | none (definitions) | V L89-90: "the definitions of c, groups, sources, domain states, carrier words. Correct." | c(x) -> chi(x). Added: the name "domain cycle" (a cycle that consists of domain states); the source uses the term (L86, L94, L184) without a definition; it rests on L129-131. Added: "a cycle contains a code if one of its states does" (the source's usage, e.g. L74, L95). "distance d = s' - s" written into the definition (source: L63-64). |
| Lemma 5.2 | `26:lem:frame` | S Lemma 1, statement L102-106, proof L108-109 | [proved] | V L91 (hand check, "all eight codes": correct); test M1, V L156 (n = 3..20, 0 violations). No finding. | u(j) -> u_j; U(u)(j) -> (Uu)_j. Range: the source has "every n >= 3"; the fragment states it inside the section's standing assumption (n even, n >= 4), i.e. for fewer n. The word "attacker" is introduced in the statement (the source uses it from L136 on without introducing it). |
| Lemma 5.3 | `26:lem:chi` | S Lemma 2, statement L111-112, proof L114-122; "constant on every cycle": S Theorem 1, L72, proof L209 (also row L14) | [proved] | V L91 ("the sets N(p), order and parity of the ones of u'; the flip remark": correct); tests M2, M2f, V L157-158 (even n = 4..20, 0 violations). No finding. | c -> chi; u'(p) -> u'_p. The sentence "chi is constant on every cycle" is moved from Theorem 1 of the source into this lemma. |
| Lemma 5.4 | `26:lem:domain` | S Lemma 3, statement L124-131, proof L133-145 | [proved] | V L91-92 ("(a), (b) (all cell types of a domain, with d >= 3 used where stated) and (c) (apart from C1)": correct). Finding C1 (V L55): the first sentence of (c) was false for F in the verified version; corrected in S (L129-131 now has the form the verification proposes; checked). Tests M3a, M3b, M3c, M3F, V L159-162 (even n = 4..18, 0 violations). | free-cell values c_k -> z_k (the letter c is not free in the paper); GF(2)^((d-1)/2) -> "{0,1}^((d-1)/2) over the field with two elements" (no \mathbb); "contains no 111" -> "does not contain the code 111"; "Flipping a free cell" -> "The flip of a free cell". |
| Lemma 5.5 | `26:lem:singleton` | S Lemma 5, statement L159-160, proof L162-164 | [proved] | V L93 (correct); test M5, V L163 (even n = 4..18, 0 violations). No finding. | c -> chi. |
| Lemma 5.6 | `26:lem:parity` | S Lemma 6, statement L166-169, proof L171-173, which refers to P154 Lemma 3 (P154 L71-75); the step F(E) in O is written out in P154 Lemma 2, L63-69 | [proved] (S); P154 Lemmas 2, 3: [proved] | V L93 (Lemma 6: correct); V L104: "Cited results of P154 used by C26 (Lemma 3, Lemma Q1, the conventions of Section 1): correct."; test M6, V L165. No finding. An independent verification of P154 as a whole was not looked up by this track. | "x in E or O" -> "x in E ∪ O"; 0 -> \zero. The algebraic step, which S gives in one line with "(as in P154, Lemma 3)", is written with the wording of P154 L74-75. See section 4 (credit) and section 8, Lemma parity, steps 2 to 4. |
| Theorem 5.7 | `26:thm:main` | S Theorem 3(c), L84-85, proof L226-232 | [proved] | as (b); V L95-96 names "the in-tree of weight m in (c)" as checked | re-lettered: source 3(c) -> paper (d); wording of the statement as in the source (S -> \Sel, G1 -> \Gone, 0 -> \zero). Theorem 3(d) of the source is NOT part of the theorem; (update) it is Lemma B.5 of Appendix B. |
| Proposition 5.8 | `26:prop:indices` | S Theorem 4, statement L88-91 (rows L18-20). Proof (update): Appendix B, "Proof of Proposition 5.8" = S section 5, L245-267: the formula for k_c L245-249, (a) L251-254, (b) L256-260, (c) L262-267 | [proved] | V L96-97 ("Theorem 4 (a), (b), (c) (the sources 0, 5, 8, ..., n - 3 of 10100(100)^q, q odd)": correct); test T34ch, V L174; k_c from the definitions at n = 8 and n = 16 (V L212, L222). No finding. Not excluded by V. | codes c = 0..7 -> code words; k_c -> k_v, k_7 -> k_{111}; k_0 -> k_{000}; "c = 1, ..., 6" -> the six words. (update) In the proof: D_c -> \Dc{v}; "k_1 = k_2 = k_4 = k_5 = 1" -> "k_v = 1 for v in {001, 010, 100, 101}"; "for c = 3, 6" -> "for v in {011, 110}"; Theorem 3(c) -> Theorem 5.7(d); Theorem 3(d) -> Lemma B.5; Lemma 4, 6, 7, 8 -> Lemma B.1, 5.6, B.3, B.4; The sentence after the statement that named the source's Lemmas 4, 7, 8, Theorem 3(d) and Theorem 1 is replaced by "(Proof in Appendix B.)". |
| Proposition 5.9 | `26:prop:even` | Statements before "Consequently": S Theorem 5, L93-95. Last sentence: S Corollary 5, L97-98. Proof (update): Appendix B, "Proof of Proposition 5.9" = S section 6: first paragraph L276-280, "Domain cycles" L281-292, "Outside K" L293, "Codes" L294-295, Corollary 5 L297-298 | Theorem 5: [proved]; Corollary 5: [proved, given Theorem A] | V L97-98 ("Theorem 5 (reduction to two domains, L >= 2^(e+1) + 1, y in the image of (1 + S)^(2^e)), Corollary 5: correct"); tests T5 (V L172) and T5ch (V L175), even n <= 20; potentials from the definitions, n = 6..14, agree (V L28, L211-215). Theorem A itself: "used as given", not re-proved by V (V L106-108, L257); in the paper it is Theorem 2.8, whose verdict is in its own row. Not excluded by V. | k_c = 0 for c = 0..6 -> k_v = 0 for every code v != 111; "Theorem A" -> `thm:A`; the step "k_c = 0 iff a state of a selected cycle contains c" -> `lem:kzero`. (update) In the proof: R90 -> calligraphic R (R is a resistance in the paper); the domain lengths L_1, L_2, L -> d_1, d_2, d (L is the map of rule 90 in the paper); the shift S -> \Sigma = sigma^2 (S is the selected set); Theorem 2 -> Lemma B.6; Lemma 9 -> Lemma B.7; Theorem 1 -> Lemma B.2; Lemma 8 -> Lemma B.4. The proof of Corollary 5 is the paragraph "The last sentence of the proposition"; nothing is added to its two clauses. |
| Lemma B.1 (update) | `26:lem:ancestors` | S Lemma 4, statement L147-149, proof L151-157 | [proved] | V L92-93 ("Lemma 4 (induction, the case p = j + 1)": correct); test M4, V L164 (even n = 4..16, 223330 cases, 0 violations). No finding. Not excluded by V. | u(j) -> u_j; U^r(u) -> U^r u; "Let n be even" is the standing assumption of the appendix; Lemma 1 -> Lemma 5.2; Lemma 3(a) -> Lemma 5.4(a); "the block 111" -> "the code 111"; last sentence: "the F-orbit of every state ... contains 111" -> "a state of its orbit under F contains 111". |
| Lemma B.2 (update) | `26:lem:kinds` | S Theorem 1, statement L72-75 (in the wording after finding C3), proof L209-212 | [proved] | V L95 ("Theorem 1 (C3 only)": correct; C3, V L57, is a wording point, applied in S L72-75); tests M5 of S and T1 of V (V L167, even n = 4..20, 0 violations). Not excluded by V. | Called a lemma. c -> chi. The first sentence of the source's statement ("c is constant on every cycle") is Lemma 5.3 of the paper and is not repeated; its last sentence ("F permutes the domain states, and no domain state contains 111") is Lemma 5.4(c) and is not repeated. The labels "kind (i), (ii), (iii)" are dropped. Added as a sentence of the statement, from the source's proof (L210-212: "the whole cycle lies in M ... If every state of the cycle is a domain state ... If not ... the cycle contains 111") and from the way Lemma 8 and Theorem 5 of the source cite Theorem 1 (L193, L293): "Hence every cycle is contained in E ∪ O, or is a domain cycle, or contains 111; for n = 2^k the only cycle contained in E ∪ O is {0}". No step is added; the sentence states for cycles what the proof shows. |
| Lemma B.3 (update) | `26:lem:carrier` | S Lemma 7, statement L175-176, proof L178-182 | [proved] | V L93 ("Lemma 7 (both image steps block by block)": correct); test M7, V L166 (n = 5..31, 1444 cases, 0 violations). No finding. Not excluded by V. | "(n = 5p + 3q)" is left out and "if p >= 1" is written "if w is a carrier word" (Definition 5.1: at least one block 11100); the images are written with \code. |
| Lemma B.4 (update) | `26:lem:codes` | S Lemma 8, statement L184-185, proof L187-195 | [proved] | V L93-94 ("Lemma 8 (both values of c_1 and c_r; the run argument at 2^k)": correct); test L8 of V, V L168 (even n = 4..20, 0 violations). No finding. Not excluded by V. | Title "codes 011 and 110" -> "codes on the cycles". Free cells c_k -> z_k (as in Lemma 5.4); 1^n -> \one; Lemma 3(b) -> Lemma 5.4(b); Lemma 6 -> Lemma 5.6; Theorem 1 -> Lemma B.2; "(codes are invariant under rotation)" refers to Definition 5.1. |
| Lemma B.5 (update) | `26:lem:domaingamma` | S Theorem 3(d), statement L86, proof L233-241 | [proved] | V L95-96 ("Theorem 3 (a) to (d) (in particular ... the intermediate states of (d) for even and odd i)": correct); test T34ch, V L174 (n = 8..1024). No finding. Not excluded by V. | Made a lemma of its own (Theorem 5.7 of the paper has the parts (a) to (c) of the source's Theorem 3 and its Theorem 2). "(a)" -> Theorem 5.7(b); "(c)" -> Theorem 5.7(d); Lemma 3 -> Lemma 5.4(c); "equal or G1-adjacent cycles" -> "equal cycles or cycles joined by an edge of G_1 (Lemma 2.3)". |
| Lemma B.6 (update) | `26:lem:topar` | S Theorem 2, statement L77-79 (first sentence), proof L214-222 | [proved] | V L95 ("Theorem 2 (both cases, the induction)": correct); tests T2 and T2ch, V L170, L173. No finding. Not excluded by V. | The paper has the proof of S Theorem 2 inside the proof of Theorem 5.7(a), written there for every even n >= 4; the lemma states its conclusion for even n and refers to that proof. The second half of the source's statement (the number of drops of c) is not taken over. |
| Lemma B.7 (update) | `26:lem:oneparity` | S Lemma 9, statement L197-198, proof L200-205 | [proved] | V L94 ("Lemma 9 (the projection pi = F^T)": correct); test L9, V L169 (even n = 4..20, 0 violations). No finding. Not excluded by V. | P -> P_E (P(d) and P_h have other meanings in Section 3); pi -> theta (pi_eps is the stationary law); "is its G1 successor" -> "G_1 has an edge from the cycle of x to it (Lemma 2.3)"; Lemma 6 -> Lemma 5.6. |
| Proposition A.1 | `94:prop:periodic` | `proofs_94_26/PROOF_94_converse.md`, Theorem 1 (l. 73-79), proof l. 307-311 | [proved] | `VERIFICATION_94_26.md` l. 70-72; tests T1, T1p6 (l. 138-139), n = 3..20 (row "optional block" of `trace/trace_94.md`) | Called a proposition and placed at the end of Appendix A; notation as in Lemmas 94:lem:empty and 94:lem:live. The other two statements of the sub-session's optional block (basin of the zero state; Proposition 3 of the source) were not taken into the paper. |

Statements of the paper that have no proof in the paper: Proposition 2.1 (quoted from the note v0.2). (update)
Propositions `26:prop:indices` and `26:prop:even`, which were without proof in the PDF of commit 72cc2ad, are proved
in Appendix B. The verification `VERIFICATION_94_26.md` excluded no statement of Section 5 or of Appendix B; what it
did not check is listed in its section 5 (V L252-266) and concerns, for rule 26: the row n = 22 of the source's
Table 2 apart from one claim, the potentials at n = 16 for 536 of the 552 roots, Theorem A (used as given), and the
literature and process statements of the source. "Status of the proofs" in the paper says that Theorem A was not
re-proved by that verification.

Statements of the sources that the paper does not contain: Lemma B, Lemma Z, Lemma H, Lemma P of
`report_ring_size.md`; Proposition 3 (entry cost) and the paragraph "Description of the cycles" of
`PROOF_43_142.md`; Lemma 7(b) and the counts of Lemma 6 of `PROOF_154.md`, and its Section 7 (rules 122, 26);
Lemma 16 and Proposition 3 of `PROOF_94_converse.md` (quoted in Section 6.2 without proof); gamma_min for rule 94 at
3 | n (not stated in `PROOF_94.md`). (update) Of `PROOF_26.md` the paper now contains every lemma and theorem; not
taken over are the second half of the statement of its Theorem 2 (the number of drops of c) and its sections 7
(scope) and 8 (computations), which the paragraph "Computed values and the open case" quotes in part.

## Part B. Every reference: how it was seen

"Read" means that the text itself was opened and read in a session; knowledge from an abstract or from search
excerpts is named as such. The rows are taken from `trace/trace_refs.md`, Section 1, which also says where each
bibliographic field comes from (always a repository document; nothing was completed from memory, which is why some
entries have a family name only or lack pages). No reference was opened in the session that assembled the paper:
the sandbox had no network access to the literature (only package registries were reachable).

| key in `refs.bib` | how seen | repository lines that say so | missing fields, remarks |
|---|---|---|---|
| `BagnoliBaiaMatteuzzi2025` | read in full (arXiv v2, 30 April 2025, 16 pp.) by the literature session of v0.2, by the verification of v0.2 and by the ring-size study session; read in part (Table 2 and surrounding text) by the ring-size verification | `literature.md`:60, `VERIFICATION_v02.md`:70, `literature_ring_size.md`:109, `literature_ring_size.md`:110, `verify_ring_size/literature/literature_check.md`:41 | none |
| `BhattacharjeeDas2019` | read in part by the ring-size verification (abstract, Example 2, Table 3 row lists, theorem statements by keyword scan; text extraction); not read by the study | `verify_ring_size/literature/literature_check.md`:42, `verify_ring_size/literature/literature_check.md`:157, `literature_ring_size.md`:15 | none |
| `Boccara1993` | not obtained by any session; known through the credit in Fuks2005 and Fuks2005b (both print 1992); date and DOI seen on the publisher page by the verification | `literature_addendum.md`:257, `proofs_43_142/PROOF_43_142.md`:757, `literature_addendum.md`:304, `VERIFICATION_43_142.md`:187, `VERIFICATION_43_142.md`:188, `verify_43_142/literature/lit_check_43_142.md`:9 | (update) given name Nino: `literature_addendum.md`, "Bibliographic data seen on 20 November 2026" (result page of a web search, not the paper) |
| `Ellison2000` | read in part. Study session: author working paper of January 1999 (45 pp.): Def. 1, Sects. 2.2, 3.1-3.2, 4.1-4.2, 6.3. Ring-size verification: published version, journal pp. 17, 20, 22-26, 28-31, 36-39 (15 of 29), from page images; appendix lemmas not read | `literature_ring_size.md`:138, `literature_ring_size.md`:74, `literature_ring_size.md`:349, `verify_ring_size/literature/literature_check.md`:31, `verify_ring_size/literature/literature_check.md`:32, `literature_ring_size.md`:15, `verify_ring_size/literature/literature_check.md`:406, `VERIFICATION_ring_size.md`:382 | none. An earlier document gives the entry without DOI (`literature.md`:13; `literature.md`:88) |
| `Fedoriaka2025` | read in full (v1, text extraction) by the ring-size verification; search excerpt only in the study session | `verify_ring_size/literature/literature_check.md`:40, `verify_ring_size/literature/literature_check.md`:159, `literature_ring_size.md`:248 | none |
| `Fuks1997` | arXiv:comp-gas/9703001v1 read in full (5 pp.) by the session of proofs_43_142 and by the literature sub-task of its verification; journal version not compared | `literature_addendum.md`:258, `VERIFICATION_43_142.md`:168, `literature_addendum.md`:355 | (update) given name Henryk: `literature_addendum.md`, update of 20 November 2026 (author line of arXiv:nlin/0502037v1). Journal name in full, issue 3 and pages R2081-R2084: search S2 below (not the paper itself) |
| `Fuks2005` | read in full (publisher PDF) by the session of proofs_43_142; statements re-read page by page by the literature sub-task of its verification | `literature_addendum.md`:255, `proofs_43_142/PROOF_43_142.md`:757, `VERIFICATION_43_142.md`:159, `verify_43_142/literature/lit_check_43_142.md`:37 | (update) given name Henryk: as for `Fuks1997`. Still missing: issue number (present only inside the DOI string) |
| `Fuks2005b` | arXiv:nlin/0502037v1 read in full on 18 November 2026 by the reader outside both sessions; before that a search excerpt only (session of proofs_43_142); not reachable for the verification; journal version (2007, other title) not seen | `literature_addendum.md`:299, `literature_addendum.md`:295, `literature_addendum.md`:256, `proofs_43_142/PROOF_43_142.md`:760, `VERIFICATION_43_142.md`:3, `VERIFICATION_43_142.md`:255 | (update) given name Henryk: author line of this preprint (`literature_addendum.md`, update of 20 November 2026). The entry now says that the text was read by the reader outside the sessions, not by a session. KEY/YEAR: no document has a year 2006 for this paper (this key was `Fuks2006` in the sub-session's file) |
| `MartinOdlyzkoWolfram1984` | read in full (author copy, 40 pp.) by the ring-size verification; not read by the study session (known there second-hand through Powley and Stepney) | `verify_ring_size/literature/literature_check.md`:30, `literature_ring_size.md`:15, `literature_ring_size.md`:234, `VERIFICATION_ring_size.md`:260, `literature_ring_size.md`:210 | none. The note field of the repository's BibTeX block still says 'Not read' (see errors, item 1) |
| `Newton2018` | read (version of record) by the literature session of v0.2; a secondary source | `literature.md`:76, `literature.md`:77 | none |
| `NobeYura2004` | abstract only (study session, via the fetch tool; ring-size verification, publisher page in search results); Proposition 1 seen as a search excerpt only | `literature_ring_size.md`:243, `literature_ring_size.md`:244, `literature_ring_size.md`:245, `literature_ring_size.md`:246, `verify_ring_size/literature/literature_check.md`:43, `verify_ring_size/literature/literature_check.md`:402 | none; end page 5804 stands in the repository but was not checked |
| `NobeYura2007` | abstract and two search excerpts only (study session: abstract; session of proofs_43_142: abstract and excerpts); full text not reached by the verification | `literature_ring_size.md`:247, `literature_addendum.md`:130, `literature_addendum.md`:135, `VERIFICATION_43_142.md`:175 | none |
| `NoldekeSamuelson1993` | not obtained; known only through Ellison2000, pp. 36-38 (read by the verification) and secondary search fragments | `verify_ring_size/literature/literature_check.md`:45, `literature_ring_size.md`:26, `VERIFICATION_ring_size.md`:382, `verify_ring_size/literature/literature_check.md`:92 | issue number, DOI |
| `Nordahl1989` | read in part (publisher scan: pp. 68-74 and the reference list pp. 76-78) by the session of proofs_43_142; pp. 70, 73, 74 and the references re-read by the literature sub-task of its verification | `literature_addendum.md`:144, `literature_addendum.md`:145, `VERIFICATION_43_142.md`:171 | given names (initials only), issue, DOI |
| `OEIS` | entries and b-files read by the ring-size verification (oeis.org) | `verify_ring_size/literature/literature_check.md`:39, `verify_ring_size/literature/literature_check.md`:200, `verify_ring_size/literature/literature_check.md`:205 | a title of the database, an author, a year: the repository documents write 'OEIS' only |
| `PeterleinNote` | source document of the paper (note/note_v0.2.tex) | `note/note_v0.2.tex`:24, `note/note_v0.2.tex`:25, `note/note_v0.2.tex`:26 | The note itself does not contain its version DOI: `note/note_v0.2.tex`:227 gives the DOI of v0.1 and the DOI of all versions only (the links in note_v0.2.pdf are the same two). CITATION.cff describes version 0.3 (`CITATION.cff`:8). (update) Cited where the paper uses the note: the model, Proposition 2.1, the rate, k* = 0 for bijections, Proposition 1 of the note (classes 60 and 90) |
| `PitmanTang2018` | read in the version arXiv:1603.09017v3 (8 February 2018) by the literature session of v0.2 | `literature.md`:33, `literature.md`:34, `literature.md`:125 | (update) issue 3: `literature_addendum.md`, update of 20 November 2026 (address of the paper at Project Euclid, in a search result). Pages 1942-1972: search S1 below (not the paper itself) |
| `Samuelson1994` | abstract only, by the ring-size verification (ScienceDirect abstract as shown in search results); primary text not read by anyone | `verify_ring_size/literature/literature_check.md`:44, `literature_ring_size.md`:26, `VERIFICATION_ring_size.md`:382, `verify_ring_size/literature/literature_check.md`:400 | issue number, DOI |
| `Stricker2023` | read in part (publisher PDF: pp. 229-232; the remaining 19 PDF pages not read) by the session of proofs_43_142; pp. 230, 232 re-read by the verification | `literature_addendum.md`:207, `VERIFICATION_43_142.md`:171 | (update) pages 229-251: `literature_addendum.md`, update of 20 November 2026 (reference list of Zhu and Richard). Still missing: given name (initials only) |

Rows added by the update of 20 November 2026 (same columns):

| key in `refs.bib` | how seen | repository lines that say so | fields, remarks |
|---|---|---|---|
| `PeterleinStudy` | source documents of the paper: the repository at tag `v0.3` (commit 0849cd8), which contains `report_ring_size.md`, `data/ring_size/mechanisms.csv`, `data/fw_sweep.csv`, `data/ring_size/crystal_radius.csv`, `verify_ring_size/` (with `PROOF_154.md`, `PROOF_94.md` and `phase2/out/v154_n22.json`) and `VERIFICATION_ring_size.md` (checked with `git cat-file -e v0.3:<path>`); it does not contain `proofs_43_142/`, `proofs_94_26/`, `literature_addendum.md` or `paper/` | `CITATION.cff`:3 (title), :8 (version 0.3), :9 (date 2026-11-16) | The DOI 10.5281/zenodo.24275024 of version 0.3 was given by the author in the task of this session; no file of the branch contains it (`CITATION.cff` lists the DOIs of versions 0.1 and 0.2 and the DOI of all versions). Cited where the paper refers to the ring-size study, its report or its data files: introduction, caption of Table 1, Section 6.2, statement on the use of AI, "Code and data" |
| `Young1993` | not read by any session and not by the reader (title via the DOI only); the content is known from Newton2018 (read: stochastic potential, stochastically stable = least stochastic potential, with reference to Young 1993) and from Ellison2000 (pp. 22, 36) | `literature.md`:85, :77, :123; `verify_ring_size/literature/ellison2000_published_reading_notes.md`:70 | all fields: BibTeX block at `literature.md`:241 ff. Note in the entry: "Not read; cited after Newton (2018) and Ellison (2000)" |
| `FreidlinWentzell1984` | not read by any session and not by the reader | `verify_ring_size/literature/ellison2000_published_reading_notes.md`:62, :64 (Ellison, Section 6.3, refers the minimum-cost trees to Freidlin and Wentzell); `literature.md`:89 (chapter title of the third edition only) | The repository does not record which edition Ellison cites (`trace/trace_refs.md`, row RW:6). Year 1984, publisher Springer-Verlag, New York: search S4 below (Ellison's list of references as shown in search results). Given names: `literature.md`:264 (entry of the third edition, 2012, which the note v0.2 cites). Note in the entry: "Not read; cited after Ellison (2000), in the edition named in his list of references" |
| `HattoriTakesue1991` | not obtained; named in Fuks2005b (read by the reader outside the sessions) as the source of the conserved number of blocks 10 | `literature_addendum.md`:263, :307-308 | journal, volume, year, pages: `literature_addendum.md`:263. Title, given names, issue 3, DOI: search S3 below. Note in the entry: "Not read; cited after Fukś (2005), the preprint" |
| `ZhuRichard2026` | read in full (v1, 16 pages; the figures only as the text printed in them) on 20 November 2026 by Claude, the reader outside the sessions, through an arXiv reader that the sessions could not reach; before that, search excerpts only (session of proofs_43_142 and its verification). No session read it; this session did not open it | `literature_addendum.md`, section "Update of 20 November 2026 (A1 read in full)"; section A1 (`literature_addendum.md`:37 ff.) | authors, title, arXiv number, version: `literature_addendum.md`:37-39. What the paper says about the text is taken from the update and from section A1 only: the definition of the ratio (equation (4) and Proposition 2.2 there), unitarity at odd n cited from Nobe and Yura (2004), "below 0.01 for n in {13, ..., 27}", the two values printed in Figure 13, no explanation given, and what is not in the text. The numbers enter through `make_numbers.py` (macros `ZRBound`, `ZRNmin`, `ZRNmax`, `ZRValues`) |
| `Wolfram2002` | read in part by the ring-size study session: Section 6.4 (pp. 255-260) and the notes for Chapter 6 (pp. 947-965), from PDF excerpts; the note "Additive rules" (p. 963) checked by eye; not re-read by the verification of the study | `literature_ring_size.md`:77, :84-85, :100-104; `verify_ring_size/literature/literature_check.md`:38 | all fields: BibTeX block at `literature_ring_size.md`:309 ff. Cited once, for rule 60 in Section 6.2: p. 963 gives the fraction of states on cycles for rules 60 and 90; that only the zero state is left at n = 2^j is the study's inference (`literature_ring_size.md`:104, `report_ring_size.md`:116-118), and the paper says so |

Web searches of 20 November 2026 (update), made by this session with the web search tool; only result pages were
seen, no paper was opened. Each was made once.

| no. | query | what was seen, and where |
|---|---|---|
| S1 | `Pitman Tang "Tree formulas, mean first passage times and Kemeny's constant of a Markov chain" Bernoulli 24(3) pages` | "Bernoulli 24(3): 1942-1972 (August 2018)" on the page of the paper at projecteuclid.org; the same pages in three reference lists and on the home page of W. Tang |
| S2 | `Fukś "Solution of the density classification problem with two cellular automata rules" Phys. Rev. E 55 R2081 pages` | "Physical Review E, 55(3):R2081-R2084" in two reference lists (arXiv:1409.3588; LIPIcs.STACS.2011.284) and in the Wikidata record of the paper (volume 55, issue 3, pages R2081-R2084) |
| S3 | `Hattori Takesue 1991 Physica D 49 295-322 "Additive conserved quantities in discrete-time lattice dynamical systems"` | authors Tetsuya Hattori and Shinji Takesue, the title, "Physica D, Volume 49, Issue 3, Pages 295-322", doi 10.1016/0167-2789(91)90150-8 (ACM Digital Library record; record of Keio University) |
| S4 | `Ellison 2000 "Basins of Attraction, Long-Run Stochastic Stability" references Freidlin Wentzell 1984 "Random Perturbations of Dynamical Systems" Springer-Verlag` | in excerpts of the published paper (copy at dklevine.com) and of the working paper of January 1999 (web.mit.edu): the entry "Freidlin, M. and Wentzell, A. (1984) Random Perturbations of Dynamical Systems (New York: Springer Verlag)", and the phrase "Lemma 3.1 of Chapter 6 of Freidlin and Wentzell (1984)" |

Entries that are still incomplete after the update (no repository record, and not asked for): `OEIS` (no year);
`Nordahl1989` (initials only, no issue, no DOI); `NoldekeSamuelson1993` and `Samuelson1994` (no issue, no DOI);
`Stricker2023` (initials only); `Fuks2005` (no issue).

The author's list of credits against the documents. "Boccara 1993": not obtained by any session; cited after the
two papers of Fukś, with a note in the entry. "Fukś 2005, 2006": the documents have the Complex Systems paper
(2005) and the preprint arXiv:nlin/0502037v1 (2005; journal version 2007 under another title, not seen); there is
no paper of 2006. "Nobe, Yura 2004, 2007": abstracts and search excerpts only; cited with that statement in the text
and in the entries. "Samuelson 1994": abstract only. "Nöldeke and Samuelson 1993": not obtained; cited after
Ellison (2000). "Ellison 2000": read in part. "Martin, Odlyzko, Wolfram 1984": read in full by the ring-size
verification.

Named in the text of Section 6.1 without an entry in the list of references. (update) By the author's decision of
20 November 2026, Young (1993), Freidlin and Wentzell and Hattori and Takesue (1991) now have entries, each with the
note "Not read; cited after ..." that names the read source; Zhu and Richard has an entry as read in full by the
reader outside the sessions. Still named without an entry:

| text | how seen (rows `Bagnoli2024`, `AguiarSeverino` of `trace/trace_refs.md`) |
|---|---|
| Bagnoli, Baia, Matteuzzi, conference chapter (ACRI 2024) | the chapter was not read by any session; read was the extended arXiv version (BagnoliBaiaMatteuzzi2025) |
| Fukś, Fundamenta Informaticae 78 (2007), the journal version of Fuks2005b | not seen |
| Aguiar and Severino, Complex Systems 24 | abstract and a search excerpt only (session of proofs_94_26); the statement was not checked by the verification of those proofs |

Entries of the sub-session's bibliography that the paper does not use (their rows are in `trace/trace_refs.md`):
`Wolfram1983`, `LiPackard1990`, `VoorheesBeauchemin2004`, `Wuensche2024`, `WuenscheLesser1992`, `Ellison1993`, `BusicMairesseMarcovici2013`, `MarsanSablik2025`, `PowleyStepney2009`, `Krawczyk2015`, `ChuaEtAl2007`, `Jen1986`, `Jen1988`. `Wolfram1983` and `LiPackard1990` are cited by the note v0.2, but the
repository has no record that a session read them; the paper therefore defines rule numbers and classes without
citing them.

## Part C. Changes made at assembly, after the sub-sessions

1. Sections 3.1 to 3.3 are subsections of Section 3; Theorem 3.1 states the three results together.
2. The sub-sessions cited `prop:order` for "k_v = 0 iff v occurs in a state of a noise-selected cycle". In the paper
   this is Lemma 2.2 (`lem:kzero`); the eight references were changed. No argument changed.
3. Section 3.1, opening: "For even n recall the parity classes" -> "the parity classes are defined as follows"
   (they are not defined earlier). The sentence on the bijectivity of rule 154 on odd rings now cites
   Bhattacharjee and Das and Fedoriaka (read) and names Nobe and Yura (2004) as known from its abstract; source of
   the attribution: `report_ring_size.md` l. 252-254. Theorem 154:thm:other, odd n: "as in Lemma 154:lem:moves(a)"
   -> "by the last sentence of Lemma 2.3" (Lemma 154:lem:moves assumes n even; the argument, two periodic states that
   differ in one cell, is the same; `PROOF_154.md` l. 197-198 writes "as in Lemma 7(a)").
4. Section 3.2: key `Fuks2006` -> `Fuks2005b`; Figure 2 inserted before Proposition 43:prop:heal.
5. Section 3.3 and Appendix A: the block word called X by the sub-session is written x-tilde (X is the crystal cycle
   of Section 3.2). Remark 94:rem:small: the computed facts enter through macros of `numbers.tex`; the value of k* at
   n = 4 (file `data/fw_sweep.csv`) was added. Of the sub-session's optional block only the proposition on the
   periodic states was kept.
6. Section 5: the computed facts enter through macros of `numbers.tex`; "parity classes of Section 2" -> "of
   Section 3.1".
7. Section 6.1: the sub-session's draft cited twelve texts that no session read; the paper keeps the citations the
   author asked for and names the others in words (Part B). Counts of search queries and the ring size and number
   of classes of Bagnoli et al. were replaced by words, because they are numbers that do not come from a data file.
8. Lemma 2.7: wording of finding B4 (row `lem:inclosed` of Part A).
9. The statement on the use of AI is not the text of the note: that text describes how the note was made. The
   paper's statement has the same form and says how this paper was made; its dates are those of the git log and of
   the headers of the verification reports.
10. Layout: the paper is written for a TeX installation without amssymb, amsthm, natbib and booktabs (the only one
    available in the sandbox); "does not divide" is typeset with a slashed bar, Z/nZ in bold.

Changes of the update of 20 November 2026 (second session of that day):

11. Appendix B is new. It contains Lemmas B.1 to B.7 and the proofs of Propositions 5.8 and 5.9, from
    `proofs_94_26/PROOF_26.md` (rows of Part A). No mathematical step was added, and the session found no gap in
    the source that would have stopped the task. Three things are not literal: (i) Lemma B.6 has no proof text of
    its own; it refers to the proof of Theorem 5.7(a), which is the proof of the source's Theorem 2 and is written
    there for every even n. (ii) Lemma B.2 states for cycles what the source's proof of Theorem 1 shows for states
    (row of Part A). (iii) Letters: R90, L, S, P, pi of the source are calligraphic R, d, Sigma, P_E, theta, because
    R, L, S, P, pi have other meanings in the paper.
12. Section 5: the two paragraphs that said the proofs were not reproduced are replaced by "(Proof in Appendix B.)"
    inside the two propositions. The sentence "Odd n is not treated ..." is kept.
13. Abstract: "for four rules and all ring sizes" -> "for four rules, for every ring size from a small bound on";
    for rule 94 the abstract now says that n = 3 and n = 4 are not covered and that the computed value at n = 4
    (macro `KstarNinetyFourAtFour`, file `data/fw_sweep.csv`) does not follow the pattern; for rule 26 it gives the
    ranges of Theorem 5.7 and Proposition 5.8 (k >= 2; k >= 3; odd k >= 3) and says that for even k the value is
    computed for k = 2 and k = 4 only. Introduction, "Results": the same, with the two computed values as macros,
    and what Proposition 5.9 proves and leaves open; "for all n" -> "for every n from the bounds stated in Theorem
    3.1 on".
14. "Status of the proofs": says which proofs were verified by a separate session, that the verification of the
    proofs for rule 26 excluded no statement of Section 5 or Appendix B, found one false sentence in the source of
    Lemma 5.4(c) (finding C1, corrected) and did not re-prove Theorem A, and that the proofs for rule 154 and for
    rule 94 with 3 | n have not been verified by a separate session.
15. Section 6.1: Young, Freidlin and Wentzell, Hattori and Takesue are cited (entries with "Not read; cited after
    ..."). The report on Zhu and Richard is new (Part B, row `ZhuRichard2026`); the sentence after it states what
    Lemma 3.7 gives, with the count 2^(n/2+1) - 1 of the states of E ∪ O and a pointer to the table of section A1
    of `literature_addendum.md`; no other arithmetic was added. "What was read" is rewritten accordingly. The
    sentence on Aguiar and Severino keeps its wording; it had named two texts ("Two further texts ... were seen as
    search excerpts only"), so its subject and verb are now singular.
16. Section 6.2: the count of the other classes is the macro `NumOtherSwitching` (file `mechanisms.csv`), not a
    word; classes 60 and 90 are added with computed values (macros `KposSixty`, `KposNinety`, `KstarSixtyPos`,
    `KstarNinetyPos`, `CyclesSixtyNinetyPos`). No proof is given for either class. Cited: Martin, Odlyzko and
    Wolfram, Lemma 3.5, for rule 90; for rule 60 the note of Wolfram (2002), p. 963, which is the only text the
    repository records as read for it, with the remark that the conclusion for n = 2^j is the study's inference;
    Proposition 1 of the note v0.2 as the place of a proof for both classes (its proof is the one of finding V5 of
    `VERIFICATION_v02.md`; the header of that file says so).
17. Statement on the use of AI: the clause "as reported by the author, by a second reading outside the sessions"
    is replaced by sentences that name the reader (Claude, in the conversation in which the sessions were
    planned), the folder `reader_checks/` and the ranges of its README, and that say that this reader is not
    independent of the planning; the sentence that the two proofs have not been verified by a separate session;
    this session and its date. `test_paper.py` compares the quoted ranges with the README.
18. "Code and data" and five other places name version 0.3 of the repository (key `PeterleinStudy`).
19. References: 19 entries -> 25. With the six new entries the numbers in the PDF change: the note v0.2 is [18]
    (it was [16]), the study [19].

## Part D. Errors and inconsistencies found in sources (reported, not corrected)

No wrong mathematical step was found in a proof document. Found and left as they are:

1. `report_ring_size.md`, Section 4, proof of Lemma 2: "a closed class K is reachable from every node" should read
   "some closed class is reachable from every node". Already recorded as finding B4 of `VERIFICATION_43_142.md`,
   not applied there. The paper uses the corrected reading.
2. `verify_ring_size/part2_154/PROOF_154.md` l. 15 and l. 214 write the selected set as {0}; the set {{0}} of
   cycles is meant (l. 151 has it). Notation only.
3. `literature_ring_size.md` is inconsistent on how Nobe and Yura (2004) was seen (l. 35-38: bijectivity of rule 154
   "by its abstract"; l. 244-246: the abstract speaks of 16 reversible rules, Proposition 1 on rule 154 seen in a
   search excerpt only). Its BibTeX section has stale notes that its own update section contradicts (l. 417
   Martin-Odlyzko-Wolfram "Not read"; l. 483 Fedoriaka "Not read"; l. 349 Ellison "Published journal text not
   read"); the entry of Nobe and Yura (2007) has the first page only.
4. `literature_addendum.md` still has lines superseded by its update of 18 November 2026 (l. 256, l. 272-273,
   open item 4 at l. 351).
5. `report_ring_size.md` l. 94-96 (and `code/ring_size/literature_section.md` l. 30-32): the short description of
   the lemma that Ellison attributes to Samuelson and to Nöldeke and Samuelson omits its radius condition.
6. `note/note_v0.2.tex` cites texts that no session read (Young 1993; Freidlin and Wentzell) or for which there is
   no record of a reading (Wolfram 1983; Li and Packard 1990), and cites the conference chapter of Bagnoli et al.
   while the arXiv version was read.
7. `proofs_94_26/PROOF_94_converse.md` l. 365-367 writes "for 8 | n, n >= 24 this is not determined"; with 3 not
   dividing n the first such ring size is 32 (n = 16 is computed). Not wrong, but the bound reads as if n = 24 were
   a case.

Differences between the task and the repository:

8. The table was to take k* for n = 4..22 from `data/ring_size/mechanisms.csv`. That file has n = 8..22 and no
   record for rule 154 at n = 22. The script takes n = 4..7 from `data/fw_sweep.csv` and rule 154 at n = 22 from
   `verify_ring_size/phase2/out/v154_n22.json`; the caption of Table 1 says so.
9. "Fukś 2005, 2006": see Part B. The version DOI of the note v0.2 (10.5281/zenodo.24093547) is not in the note
   itself; it is taken from `CITATION.cff`, `README.md` and `report_ring_size.md`.
10. The task names "the single-mutation-chain lemma" as what Theorem A restates. The documents say: Lemmas 1, 2 and
    the first sentence of Theorem A correspond to the results on mutation-connected and locally stable components
    (finding A21); the chain lemma corresponds to Lemma B (finding A20). Section 2.5 and Section 6.1 follow the
    documents.
11. Length: the task asks for 12 to 16 pages; the paper has 27, because the complete proofs asked for do not fit
    (see `REFEREE_NOTES.md`). (update) The author decided that the length stays; with Appendix B the paper has 31
    pages.

Found by the update of 20 November 2026:

12. `proofs_94_26/PROOF_26.md`: no gap and no wrong step was found in Lemmas 4, 7, 8, 9, Theorems 1, 2, 3(d), 4, 5
    and Corollary 5 when they were written into Appendix B. Points of form only: Theorem 2 is titled "paths to the
    zero state" although its statement is about paths to a cycle contained in E ∪ O (the zero state for n = 2^k
    only); Theorem 3(d) is restricted to n >= 8 although at n = 4 there is no domain state (its Table 1), so the
    restriction excludes nothing; the proof of Theorem 5 writes the reduction to two domains for one group and
    leaves the repetition to the reader ("So we may assume ...").
13. `literature_addendum.md`, section A1, still says "Read. Nothing in full text" and "Not seen. The two values
    ..."; both are superseded by its update of 20 November 2026, which says so for open item 1 only. The update
    gives two dates for the text (arXiv stamp 7 October 2026, first page 9 October 2026). Its remark on rule 90 and
    Martin, Odlyzko and Wolfram is marked there as recalled and not looked up; the paper does not use it.
14. `literature_ring_size.md` l. 100-104 and `report_ring_size.md` l. 116-118: for rules 60 and 90 at n = 2^k the
    statement "only the null state lies on a cycle" is an inference of the study session from a formula read in
    Wolfram (2002), p. 963; the report words it as if the book gave it for both rules. For rule 60 no session read
    a text that states it (`verify_ring_size/literature/literature_check.md` l. 330: "yes for rule 90").
15. `CITATION.cff` describes version 0.3 but has no DOI of that version; the DOI used in the paper was given by the
    author.
16. `paper/trace/trace_refs.md`, row RW:6, had recorded that the edition of Freidlin and Wentzell in the
    sub-session's bibliography (third edition, 2012) is the one the note v0.2 cites, not one that Ellison cites.
    The paper now cites the edition of 1984 (search S4, Part B).
17. `reader_checks/README.md` and `literature_addendum.md` refer to statements of the paper by their numbers in the
    PDF of commit 72cc2ad (Lemma 3.7, Theorems 3.9 to 3.11, 3.20, 3.26, Proposition 3.22, Lemma 3.32, Theorem
    3.43(i), Remark 3.44). These numbers are unchanged; numbers of references in the PDF have changed (Part C, 19).

## Part E. Numbers

Every computed value in the text enters through a macro of `numbers.tex` or through `table_kstar.tex`; both are
written by `make_numbers.py`, and `numbers.json` lists for each value the data file, the record and the field.
`test_paper.py` recomputes every value with separate code and compares. Statements taken from data files without a
number ("claims" in `numbers.json`) are checked the same way. Numerals that are not data (rule numbers, ring sizes
in statements and in the simulated figures, numbers inside citations, dates of the sessions) are listed with their
reason in the allowlist of `test_paper.py`; the test fails if a numeral outside the macros and outside this list
appears in the text. (update) 42 macros and 11 claims. Three further tests: the numbers quoted from Zhu and Richard
against the record of the reading (`literature_addendum.md`, and `proofs_43_142/out/zhu_richard_154.json`; the
record is a document, not a data file, and is the only place where these numbers stand); the classes named in the
paragraph "Other classes that change with n" against the classes of `mechanisms.csv` minus the five treated ones;
the ring sizes that the statement on the use of AI quotes from `reader_checks/README.md` against that file. The figures are simulated by `make_figures.py` from the definition of the rules; the
statements of their panel titles are asserted in the script.
