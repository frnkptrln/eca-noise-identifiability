# Reader report, part 2: rule 94 (Section 3.3 and Appendix A)

Reader: Claude. Paper: `paper/ring_size_paper.tex`, branch `paper-ring-size`, tex lines 1003-1247 (Lemma 3.29 to
Remark 3.44) and 1700-2045 (Appendix A, Proposition A.1). Sources: P94 = `verify_ring_size/part2_94/PROOF_94.md`,
C94 = `proofs_94_26/PROOF_94_converse.md`. Records: `paper/trace/trace_94.md`, `paper/TRACE.md`.

## 0. What was read, and reductions of scope

* Read in full, both sides: tex 1003-1247 and 1700-2045; P94 complete (376 lines); C94 lines 1-410 (statements,
  all lemmas and proofs, sections 4-6, start of the tables); `trace_94.md` complete; tex 158-307 (definitions and
  the shared lemmas `lem:kzero`, `lem:edge`, `lem:sym`, `thm:A` that the part cites); `numbers.tex` complete.
* **Not read:** C94 lines 411-523 (rest of the computation tables and the file list). `TRACE.md`: only the
  Part A rows of lines 77-92 and 109 (rows 80, 86, 91, 92, 109 in full, the others in their first 260 characters),
  Part C items 5, 13, 14, and the first lines of Part E. `REFEREE_NOTES.md`, the scripts, the `.json`/`.jsonl`
  files and the `.csv` data files were not opened.
* P94 was read without line numbers; line numbers of P94 given below are those of its statement headers (from
  grep) or the ranges recorded in `trace_94.md`.
* One Python check was run (single process, 0.31 s CPU, ring sizes 3 to 12, window widths 1 to 12). It is my own
  code written from the definitions in the paper; its output is in section 4. It covers more than one small case
  in one run; I say so because the rule allowed one short check. Everything called "comp." below refers to this
  run and to n <= 12 only.
* One last text search (a grep to re-confirm finding 3) was refused by the tool's safety check and was not
  repeated; finding 3 rests on the lines of `TRACE.md` that I had already read in full (86, 91).

## 1. Table: one row per numbered statement

"yes" in the last column = I followed every step by hand from the rule table (f = 0 on 000, 101, 111; f = 1
otherwise). "comp." = the conclusion was also confirmed by the check of section 4 for the n named.

| no. | label | source | same statement? (hypotheses, range of n, quantifiers) | proof: steps dropped / added / changed | cross-references correct? | proof read as a referee: every step justified? smallest n covered? |
|---|---|---|---|---|---|---|
| Lemma 3.29 | `94:lem:freeze` | P94 Lemma 1, Cor. 1a, Cor. 1b | yes (n >= 3; three statements merged, recorded) | none; "(iii) is immediate from (i)" as in the source | yes (none inside) | yes. n = 3 (cells i-2 and i+1 coincide): f(a,1,0) = f(0,1,a) = 1 for both a, so the step holds. |
| Lemma 3.30 | `94:lem:block` | P94 Lemma 2 | yes (n >= 3) | none | yes (`94:lem:freeze`(i)) | yes; n = 3, 4 checked by hand; comp. n = 3..12 |
| Lemma 3.31 | `94:lem:growth` | P94 Lemma 3 and Cor. 3 | yes (n >= 5). First "more precisely" bullet of the source is in the proof only (recorded) | nested cases of the source written as six numbered cases; sentence "and so does Fz(F^t y) for all t >= 0" added; nothing dropped | yes (`94:lem:freeze`(i), (ii); `lem:edge`) | yes. Cases 1-6 are exhaustive; in each case j is shown not frozen. Part (a) at n = 5: j-2 and j+2 are distinct from j-1, j, j+1 and adjacent to each other; values still as stated. comp. n = 5..12, all states |
| Lemma 3.32 | `94:lem:crystal` | P94 Lemma 6 (header line 171) | yes (n >= 6, 3 \| n). Second sentence is taken from proof part (b) of the source (recorded) | added: "so F^2 y = x and F^3 y = x"; "This also gives the second statement" | yes (`94:lem:block`, `94:lem:freeze`(iii)) | one step not written out (finding 1); otherwise yes. n = 6 (occurrences at j-3 and j+3 coincide; in (b) the cells p-2 and p+2 lie in the same occurrence) checked by hand, cell by cell. comp. n = 6, 9, 12 |
| Lemma 3.33 | `94:lem:windows` | C94 Lemma 7 (98-110) | yes (n >= 3) | none | yes (`94:lem:freeze`(i), (ii) for the source's Lemma 1, Cor. 1a) | yes |
| Lemma 3.34 | `94:lem:cut` | C94 Lemma W (112-121) | yes (1 <= l <= n-3); "for all t >= 0" added | none | yes (`94:lem:freeze`(iii) for Cor. 1b) | yes; the case l = n-3 (three cells outside I) checked for n = 5 (swap), 6 (merge), 8 (split) |
| Lemma 3.35 | `94:lem:live` | C94 Lemma 8 (123-184) | yes | none; "state" -> "padded word", "the image has c_1 = 1" -> "the image is 1 at the cell 1" | yes (none) | yes, steps (1)-(7) including the induction on d and the converse. comp. widths 1..12 (all words) |
| Lemma 3.36 | `94:lem:empty` | C94 Lemma 9 (186-202) | yes (n >= 3) | none | yes (`94:lem:freeze`(ii); steps (2), (4) of `94:lem:live`) | yes, including F(Delta_0(v)), F(Delta_1(v)), the dimension count and Delta_0(v) != Delta_1(v'). comp. n = 3..12 (count of P_h for even n, set of periodic states) |
| Lemma 3.37 | `94:lem:refreeze` | C94 Lemma 10 (204-228) | yes (n >= 3) | last clause "so y, y + e_j is a flip between periodic states" added | yes (`94:lem:windows`(b), (c), `94:lem:live`, (O2), `94:lem:block`) | yes, four cases, widths 2, 4 and >= 5 separately. comp. n = 5..12, all cycles |
| Lemma 3.38 | `94:lem:swap` | (a) C94 Lemma 11 (230-237); (b) not a numbered statement: P94 stage 2 (from line 204), C94 Lemma 14(i) (259-261) | (a) yes (n >= 5). (b) new statement; it says what the two source arguments prove (both directions, any block start q) | (a) added: why x' is a block word and which four flips are meant. (b) composed from the two sources; P94 Lemma 4 ("at least three blocks", line 137) is replaced by (a) | yes (`94:lem:cut`) | yes. (a): `94:lem:cut` with l = 2 <= n-3 needs n >= 5, met; n = 5 (x_(p+5) is the cell p) checked; phi_2 values checked. (b): the swap stays inside the linear word, keeps the cut q, lowers the inversions by one; a = 0 or b = 0 gives the empty path. comp. (a) n = 5..12 |
| Lemma 3.39 | `94:lem:merge` | C94 Lemma 12 (239-242) = P94 Lemma 5 (line 156) | yes (n >= 6) | proof is that of C94 (through `94:lem:cut`), with the hypothesis check written out; P94's direct argument is not used | yes (`94:lem:cut`, `lem:edge`) | yes; l = 3 <= n-3 needs n >= 6; n = 6 checked. comp. n = 6..12 |
| Lemma 3.40 | `94:lem:split` | C94 Lemma 13 (244-253) | yes (n >= 8) | closing sentence (period 2, flip of p+6, edges) added from the statement | yes (`94:lem:cut`, `lem:edge`) | yes; all phi_5 evaluations recomputed; l = 5 <= n-3 needs n >= 8; n = 8 checked. comp. n = 8..12 |
| Lemma 3.41 | `94:lem:component` | C94 Lemma 14 (255-270) | yes (n >= 5, 3 not dividing n) | (i) uses `94:lem:swap`(b) for the sorting; one sentence defines "class (a, b)" | yes (`94:lem:swap`(b), `94:lem:merge`, `94:lem:split`) | yes. Ranges of the cited lemmas: merge is used with a >= 3, so n >= 6; split with a >= 1, b >= 2, so n >= 8. n = 5: class (1,1) only; n = 7: (2,1) only; n = 8: (1,2), (4,0); n = 10: (2,2), (5,0); n = 11: (1,3), (4,1); each followed by hand, including both checkerboards in (iii). comp. n = 5, 7, 8, 10, 11 (all block words in the one closed class) |
| Lemma 3.42 | `94:lem:000` | C94 Lemma 15 (272-286) | yes | parenthesis on Table 3 dropped (not a proof step) | yes (`94:lem:live`, `94:lem:windows`(c)) | yes. Every n >= 5 with 3 not dividing n is 5, 7, 8 or >= 10: covered. z checked for n = 7 and for n >= 10 (the cell 6 is next to the centre 7, or 0 if n = 7); the orbit at n = 8 recomputed by hand |
| Theorem 3.43 (i) | `94:thm:main` | P94 Theorem 1 (line 57), Cor. 1 (65), Cor. 2 (67); proofs from line 194 | yes (n >= 6, 3 \| n) | Step 3 uses `94:lem:swap`(b) instead of P94 Lemma 4 plus the inversion count; parenthesis "(the cell p+2 is a 1 between ...)" dropped (the six cells are written out instead) | yes (`94:lem:crystal`, `lem:edge`, `94:lem:growth`, `94:lem:block`, `94:lem:swap`(b), `94:lem:merge`, `thm:A`, `lem:sym`, `lem:kzero`) | yes, Steps 1-6. n = 6: the block words are the crystal phases and the two checkerboards; merge applies with l = n-3. Step 6: the six-cell words 110010, 111110, 100010 and the five codes checked. Cosmetic: finding 4. comp. n = 6, 9, 12 |
| Theorem 3.43 (ii) | `94:thm:main` | C94 Theorem 2 (81-87), Cor. 1 (89-90); proofs 313-327, 352-355 | yes (n >= 5, 3 not dividing n) | Step 2 cites `94:lem:empty` where the source cites its Theorem 1 (C94 323); it is the statement that is needed | yes (`94:lem:component`, `94:lem:refreeze`, `94:lem:block`, `94:lem:growth`, `94:lem:empty`, `94:lem:swap`(a), `94:lem:000`, `thm:A`, `lem:kzero`) | yes, Steps 1-4. Step 3: b_0 >= 1 for n >= 5 checked (n = 1 mod 3: a_0 = 2, b_0 = (n-4)/3; n = 2 mod 3: a_0 = 1, b_0 = (n-2)/3); the eight codes checked on the named cells. comp. n = 5, 7, 8, 10, 11 |
| Remark 3.44 | `94:rem:small` | P94 line 247; C94 356-357, 368-371; macros of `numbers.tex` lines 20-23 | values agree with C94 lines 21 and 368-371 (one closed class, two checkerboards, codes 2 and 5 = 010 and 101). k* = 1 at n = 4 is not in C94 (added at assembly, TRACE Part C item 5) | not a proof | yes (`94:lem:growth`, `94:lem:crystal`) | n = 4 and n = 3 computed by hand and in the check: all four macro values confirmed; wording: finding 2 |
| Proposition A.1 | `94:prop:periodic` | C94 Theorem 1 (73-79), proof 307-311 | yes (n >= 3) | none | yes (`94:lem:empty`, `94:lem:block`, `94:lem:windows`(c), `94:lem:live`) | yes. comp. n = 3..12: the set of periodic states equals the described set |

Definitions (tex 1009-1033), (O1), (O2), "flip between periodic states" (tex 1706-1712): same as P94 (section 1)
and C94 lines 40-69. The sentence alpha(i) = 0 iff i mod 6 in {4, 5}, beta(i) = 0 iff i mod 6 in {1, 2} of C94 63
is not in the definition but appears, in the form "= 1 iff", in the proof (tex 1877-1878). The rule table of tex
1005-1007 was checked against 94 = 01011110 in binary.

## 2. Findings

**False statements (class 1):** none found.

**Hypothesis or range not met (class 3):** none found. Checked: every use of `94:lem:growth` (n >= 5),
`94:lem:crystal` (n >= 6), `94:lem:swap` (n >= 5), `94:lem:merge` (n >= 6), `94:lem:split` (n >= 8),
`94:lem:cut` (l <= n-3) lies inside the stated range, including inside `94:lem:component` for n = 5, 7, 8, 10, 11
and inside part (i) for n = 6. `94:lem:000` covers every n >= 5 with 3 not dividing n.

**Gap in a proof (class 2):**

1. **`94:lem:crystal`, proof parts (a) and (b), tex 1769-1773 and 1777-1780.** The text discusses the cells
   j-1, j+1, j-2, j+2 (in (b): p-1, p-2, p+2) and then says "So in $y=x+e_j$ every cell outside
   $I=\{j-1,j,j+1\}$ is frozen". For n >= 9 there are further cells, and nothing is said about them. The source
   has the same wording (P94 Lemma 6, proof (a) and (b); `trace_94.md` gives lines 176-187). The statement is true:
   every other cell lies in an occurrence of x centred at a zero other than j (resp. p), which does not contain
   the flipped cell. This is the lemma for which no separate verification is recorded. Small, without effect on the
   result. *Proposed correction:* replace the sentence by a citation of Lemma `94:lem:cut`, which gives exactly
   this: in (a) with I = {j-1, j, j+1} (x_(j-3) x_(j-2) = 01, x_(j+2) x_(j+3) = 10, l = 3 <= n-3 because n >= 6);
   in (b) with I = {p-1, p, p+1} (x_(p-3) x_(p-2) = 01, x_(p+2) x_(p+3) = 10). I checked that the hypotheses of
   `94:lem:cut` hold in both cases, also for n = 6.

**Unclear (class 4):**

2. **`94:rem:small`, tex 1241.** "For $n=3$ and $n=4$ nothing is proved". Lemmas `94:lem:freeze`, `94:lem:block`,
   `94:lem:windows`, `94:lem:empty`, `94:lem:refreeze` and Proposition `94:prop:periodic` are stated and proved for
   n >= 3. *Proposed:* "Theorem `94:thm:main` is not proved for n = 3 and n = 4".
   Cosmetic, same place: the reason given for n = 4 is only "Lemma `94:lem:growth` needs $n\ge5$"; the source gives
   a second reason (C94 368: "a long block for the codes 011 and 110"), which is why the statement on the codes
   fails at n = 4. The computed sentence "At $n=3$ a single flip can leave the crystal phase" (tex 1245-1246) is
   true; by hand, every flip of 011 leads to 000 (111 -> 000; 001 -> 111 -> 000).

3. **`TRACE.md` Part A, rows of Theorem 3.43 and Lemma 3.38 (record, not the paper).** Row "Theorem 3.43"
   (`TRACE.md` line 91) names as source only "C94 Corollary 1 (89-90), proof 352-355" and as verification
   "V9426 81 (\"Corollary 1: correct\")", with "as above" in the last column. `trace_94.md` has four rows for
   `94:thm:main`; the three for part (i) (P94 Theorem 1, Corollaries 1, 2; "No independent verification of the
   proof is recorded in the repository") and for the class K of part (ii) (C94 Theorem 2) are not in Part A. Row
   "Lemma 3.38" (line 86) is the row of part (b) only; the row for part (a) (C94 Lemma 11, 230-237) is missing. So
   Part A does not give the source of part (i) of the theorem, and its verification column can be read as if the
   whole theorem had been verified separately. The paper itself says the right thing (tex 153-154). *Proposed:*
   copy the missing rows from `trace_94.md`. (Basis: lines 86 and 91 read in full; lines 77-92 are one row per
   label.)

**Cosmetic (class 5):**

4. **`94:thm:main`, proof of (i), Step 6, tex 1204-1206.** "$k_v\le\gamma(A_i)+1-\gmin=1$" uses the definition
   (eq. `eq:kv`) and gamma(A_i) = gamma_min (Step 5); neither is named. (The third clause of `lem:kzero` would not
   do: the codes 111 and 000 occur in Fy and F^2 y, not in a flip of a state of the cycle. The step as written is
   correct.) *Proposed:* "by \eqref{eq:kv}, since $A_i\in\Sel$".

5. **Letters.** The paper-wide renaming of a code from c to v (k_v, D_v; tex 1158-1163) meets the half word v of
   the doubled words (tex 1031-1033, 1106-1107, 2028), which the source keeps apart (C94: code c, half word v).
   They never stand in one sentence. Also q is a cell ((O1), `94:lem:cut`, `94:lem:swap`(b)), an index of runs
   (tex 1842) and the odd factor of n (tex 1108); a, b are numbers of blocks, end points of runs (tex 1828) and bits
   (tex 1899); the last two are as in the sources. No statement becomes ambiguous.

Recorded changes that I checked and that are **not** findings: Step 3 of part (i) sorts with `94:lem:swap`(b)
(built on C94 Lemma 11, n >= 5, no condition on n mod 3) instead of P94 Lemma 4 ("at least three blocks"); part
(i) has n >= 6, so the hypothesis is met. `TRACE.md` row 3.38 says "X_c -> X", the paper writes x-tilde (Part C
item 5 records this).

## 3. Verdict per statement

* Proof confirmed by reading (every step followed by hand): Lemmas 3.29-3.42 (3.32 with the one unwritten step
  of finding 1, which I supplied), Theorem 3.43 (i) and (ii), Proposition A.1. Lemma 3.38(b) was read as a new
  statement: correct for every n >= 5.
* In addition confirmed by computation, n <= 12 only, as listed in section 4: 3.30, 3.31, 3.32, 3.35, 3.36 (count
  of P_h and, through A.1, the set of periodic states), 3.37, 3.38(a), 3.39, 3.40, Theorem 3.43 (i) and (ii),
  A.1. Tested only in part or only through the theorem: 3.29 (frozen set constant on cycles), 3.38(b) and 3.41
  (all block words in the one closed class), 3.42 (the code 000 on K). Not tested by computation: 3.33, 3.34.
* Theorem 3.43 uses `thm:A`, `lem:kzero`, `lem:edge`, `lem:sym` as given; I read their statements, not their
  proofs (not my part).
* Remark 3.44: the four macro values (1 closed class; 2 block words; codes 010 and 101; k* = 1) and the sentence on
  n = 3 confirmed by hand and by the check (k* = 1 at n = 4 uses Theorem A for Sel = K).

## 4. The check (own code, ring sizes 3..12; output)

```
Lemma live, widths 1..12: OK
n=3 Prop periodic (set equality, 4 states): OK
n=3 period of states with Fz nonempty divides 6: OK
n=3 block words fixed, Fz const on cycles: OK
n=3: flips of 011 (bit i = cell i) end on cycles [0, 0, 0]; closed classes [[0]]
n=4 |P_h|=2^(n/2-2^e): OK
n=4 Prop periodic (set equality, 3 states): OK
n=4 period of states with Fz nonempty divides 6: OK
n=4 block words fixed, Fz const on cycles: OK
n=4: closed classes 1; members ['0101', '1010']; block words ['0101', '1010']; codes on K ['010', '101']; codes within one flip ['000', '001', '010', '011', '100', '101', '110', '111']; cycles 3
n=5 Prop periodic (set equality, 16 states): OK
n=5 period of states with Fz nonempty divides 6: OK
n=5 block words fixed, Fz const on cycles: OK
n=5 Lemma growth (all states): OK
n=5 Lemma refreeze (all cycles): OK
n=5 swap(a)/merge/split on all block words (5/0/0 places): OK
n=5 one closed class; all cycles with Fz nonempty in K; K=reach(block words); 8 codes (m=11, |K|=11, zero in K: True): OK
n=6 |P_h|=2^(n/2-2^e): OK
n=6 Prop periodic (set equality, 12 states): OK
n=6 period of states with Fz nonempty divides 6: OK
n=6 block words fixed, Fz const on cycles: OK
n=6 Lemma growth (all states): OK
n=6 Lemma refreeze (all cycles): OK
n=6 swap(a)/merge/split on all block words (0/6/0 places): OK
n=6 closed classes = 3 crystal singletons (m=9): OK
n=6 Lemma crystal F^3(x+e_j)=x: OK
n=6 crystal codes {011,101,110}, one flip gives the other five: OK
n=7 Prop periodic (set equality, 43 states): OK
n=7 period of states with Fz nonempty divides 6: OK
n=7 block words fixed, Fz const on cycles: OK
n=7 Lemma growth (all states): OK
n=7 Lemma refreeze (all cycles): OK
n=7 swap(a)/merge/split on all block words (7/0/0 places): OK
n=7 one closed class; all cycles with Fz nonempty in K; K=reach(block words); 8 codes (m=22, |K|=22, zero in K: True): OK
n=8 |P_h|=2^(n/2-2^e): OK
n=8 Prop periodic (set equality, 43 states): OK
n=8 period of states with Fz nonempty divides 6: OK
n=8 block words fixed, Fz const on cycles: OK
n=8 Lemma growth (all states): OK
n=8 Lemma refreeze (all cycles): OK
n=8 swap(a)/merge/split on all block words (8/8/8 places): OK
n=8 one closed class; all cycles with Fz nonempty in K; K=reach(block words); 8 codes (m=27, |K|=27, zero in K: True): OK
n=9 Prop periodic (set equality, 58 states): OK
n=9 period of states with Fz nonempty divides 6: OK
n=9 block words fixed, Fz const on cycles: OK
n=9 Lemma growth (all states): OK
n=9 Lemma refreeze (all cycles): OK
n=9 swap(a)/merge/split on all block words (9/9/0 places): OK
n=9 closed classes = 3 crystal singletons (m=31): OK
n=9 Lemma crystal F^3(x+e_j)=x: OK
n=9 crystal codes {011,101,110}, one flip gives the other five: OK
n=10 |P_h|=2^(n/2-2^e): OK
n=10 Prop periodic (set equality, 158 states): OK
n=10 period of states with Fz nonempty divides 6: OK
n=10 block words fixed, Fz const on cycles: OK
n=10 Lemma growth (all states): OK
n=10 Lemma refreeze (all cycles): OK
n=10 swap(a)/merge/split on all block words (20/10/10 places): OK
n=10 one closed class; all cycles with Fz nonempty in K; K=reach(block words); 8 codes (m=73, |K|=67, zero in K: False): OK
n=11 Prop periodic (set equality, 144 states): OK
n=11 period of states with Fz nonempty divides 6: OK
n=11 block words fixed, Fz const on cycles: OK
n=11 Lemma growth (all states): OK
n=11 Lemma refreeze (all cycles): OK
n=11 swap(a)/merge/split on all block words (22/22/11 places): OK
n=11 one closed class; all cycles with Fz nonempty in K; K=reach(block words); 8 codes (m=78, |K|=77, zero in K: False): OK
n=12 |P_h|=2^(n/2-2^e): OK
n=12 Prop periodic (set equality, 348 states): OK
n=12 period of states with Fz nonempty divides 6: OK
n=12 block words fixed, Fz const on cycles: OK
n=12 Lemma growth (all states): OK
n=12 Lemma refreeze (all cycles): OK
n=12 swap(a)/merge/split on all block words (36/24/12 places): OK
n=12 closed classes = 3 crystal singletons (m=147): OK
n=12 Lemma crystal F^3(x+e_j)=x: OK
n=12 crystal codes {011,101,110}, one flip gives the other five: OK
CPU time 0.31 s
```

What the lines mean: for n = 3..12, all 2^n states were tabulated from the rule table; periodic states, cycles,
G1 (edge C -> C' iff some flip of a state of C ends on C' != C), strong components and closed classes were
computed; the statements named in each line were tested on all states, cycles or block words of that n.
"closed classes = 3 crystal singletons" is part (i); "one closed class ..." is part (ii) (K contains every cycle
with non-empty frozen set, K = cycles reachable from block words, all 8 codes on K). In the lines for n = 3 and
n = 4 the states are printed as binary numbers.

(The code of the check is not reproduced in this file: it could not be read back from the kernel, and I did not
re-type it. It stands in the session record of the tool call that produced the output above.)

## 5. What I did not check

* The citation of Martin, Odlyzko and Wolfram, Lemma 3.7 (tex 1019); only that rules 90 and 94 agree on 011,
  101, 110.
* That the macros of `numbers.tex` are what the data files contain (`g1_classes_94.jsonl`, `fw_sweep.csv`,
  `crystal_radius.csv` were not opened); I confirmed the values themselves by my own computation.
* The proofs of `thm:A`, `lem:kzero`, `lem:edge`, `lem:sym` and Proposition 2.1.
* C94 lines 411-523 and the tables of P94 section 7 as data (I read the P94 tables as text only and compared
  nothing with them except the cycle counts m, which agree with my check for n = 5..12).
* `TRACE.md` outside the lines named in section 0; the verification documents cited in the trace (V9426, VRS,
  REP); the compiled PDF and the statement numbers 3.29-3.44 in it (taken from `TRACE.md`).
* References to this part from other sections (abstract, Theorem 3.1(c), Section 6).
* Anything by computation beyond n = 12.
