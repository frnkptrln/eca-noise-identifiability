# Part 2: the frame of the paper (abstract, introduction, Theorem 3.1, Table 1, Section 4 with Table 2, Section 6.2)

Reader: Claude. Object: `paper/ring_size_paper.tex` on branch `paper-ring-size`, with `paper/numbers.tex` and
`paper/table_kstar.tex`. The summarising parts were checked against the statements of the paper itself; Section 6.2
also against the source documents it names. `paper/REFEREE_NOTES.md` was not opened. No script, program or JSON
file of the repository was opened or run.

## 0. Deviations from the task (declared)

1. The one small machine check that the task allows (rule 94 at n = 3; rule 154 at n = 6) was written but **not
   run**: the tool call was not executed by the environment. The n = 3 case of rule 94 was done by hand instead
   (8 states; see finding 2). The n = 6 question for rule 154 was not settled; finding 4 does not depend on it.
2. Lemma P of `report_ring_size.md` (rule 45 bijective at odd n) was **not read**: the call that would have
   extracted it was not executed either. The paper's sentence on class 45 does not cite Lemma P, so the verdict on
   that sentence does not depend on it.
3. One of the 95 cells of Table 1 (rule 154, n = 22, "computed") was not compared with data: its source is a JSON
   file of a script, which the rules forbid me to open. The count "94 of 95 cells compared with the CSV files" below
   is firm; nothing is said about the 95th beyond its agreement with the table in `report_ring_size.md` l. 276.

## 1. What was read and compared

* Paper, read in full: tex 55-1513 (abstract, Sections 1 to 5 with all statements and all proofs that stand in
  these sections), 1514-1659 (Section 6), 1985-2045 (proof of Lemma 94:lem:000, Proposition 94:prop:periodic), the
  statement of Lemma 26:lem:kinds; `numbers.tex` (43 lines), `table_kstar.tex` (20 lines).
* `paper/TRACE.md`: lines 1-126 (Part A) and 206-356 (Parts C, D, E).
* Sources opened for Section 6.2: `report_ring_size.md` l. 259-608 (Section 5); `proofs_94_26/PROOF_94_converse.md`
  l. 10-95, 286-392, 417-440; `verify_ring_size/part2_154/PROOF_154.md` l. 291-442; `proofs_94_26/PROOF_26.md`
  l. 10-99, 306-393; `note/note_v0.2.tex` l. 206-217 and the lines that contain "biject"; `literature_ring_size.md`
  l. 96-106; `report_ring_size.md` l. 112-120; `verify_ring_size/literature/literature_check.md` l. 326-332;
  `VERIFICATION_94_26.md`, the lines found by a search for "doubled", "0 of 33", "n = 22".
* Data: `data/ring_size/mechanisms.csv` (194 records, 13 rules, n = 8..22) and `data/fw_sweep.csv` (1496 records,
  n = 4..20), read once by a single-process Python CSV read (0.2 s). Output kept in `csv_check.txt` of my working
  directory.

## 2. Table: numbered statements

My part contains one numbered statement, Theorem 3.1. The other rows are the statements I had to read in order to
judge the summaries. "Same statement?" is answered against the source only where I opened the source; otherwise it
says so. The proofs in the last column were read once, in full, as they stand in Sections 2, 3 and 5; the lemmas
they cite were taken as stated unless the row says otherwise.

| no. | label | source (TRACE Part A) | same statement? | proof: steps dropped/added/changed? | cross-references correct? | proof read as a referee: every step justified? smallest n covered? |
|---|---|---|---|---|---|---|
| Thm 2.8 | `thm:A` | report, Section 4, Theorem A | source not opened (not my part) | not compared | refs to `lem:inclosed`, `lem:closure`, `lem:edge` are the ones meant | read with Lemmas 2.5-2.7: every step justified; no dependence on n |
| **Thm 3.1** | `thm:main` | Theorems 3.11, 3.28, 3.43 of the paper | **yes**: (a) = 154:thm:main (n >= 3; powers of two n >= 4); (b) = 43:thm:main (n >= 4); (c) = 94:thm:main (i) n >= 6, 3 divides n, (ii) n >= 5, 3 does not divide n | no proof of its own; paragraph after it: see findings 1 and 3 | `154:thm:main`, `43:thm:main`, `94:thm:main`, `sec:154`, `sec:43`, `sec:94`, `94:rem:small`, `43:lem:R` all point to what is meant | n.a. |
| Thm 3.9 | `154:thm:pow2` | P154 Theorem 1 | first line of source seen only ("Let n = 2^k, k >= 2"): same range | not compared | correct | read: every step justified; n = 4 covered (the codes of e_0, e_0+e_1, F(e_0) checked at n = 4) |
| Thm 3.10 | `154:thm:other` | P154 Theorem 2 | first line of source seen only: same range (n >= 3, not a power of two) | not compared | correct | read: every step justified; n = 3, 5, 6 covered (code lists checked by hand for n = 3 and n = 5) |
| Thm 3.11 | `154:thm:main` | P154 Corollary l. 213 | k* sentence: same (read on both sides); Sel and k_v added from 3.9, 3.10 as TRACE says | none | correct | follows from 3.9, 3.10 |
| Thm 3.20 | `43:thm:crystal` | P43 Theorem 1 | source not opened | not compared | correct | read: justified; n = 4 covered |
| Cor 3.21 | `43:cor:div` | P43 Cor. 1, 2 | source not opened | not compared | correct | read: justified; the codes of x-hat, y, y' checked by hand, n = 4 included |
| Prop 3.22 | `43:prop:heal` | P43 Prop. 2 | source not opened | not compared | correct | read: justified; n = 4 covered (tau = 1) |
| Thm 3.26 | `43:thm:levels` | P43 Theorem 2 | source not opened | not compared | correct | read with Lemma 3.23: justified; n = 5, 6, 7 covered (w- = 2) |
| Cor 3.27 | `43:cor:ndiv` | P43 Cor. 3 | source not opened | not compared | correct | read: justified |
| Thm 3.28 | `43:thm:main` | P43 Cor. 4 | source not opened | not compared | correct | follows from 3.21, 3.27; states k* only (finding 3) |
| Thm 3.43 | `94:thm:main` | (i) P94; (ii) C94 Theorem 2, Corollary 1 | (ii): **yes**, read on both sides (C94 l. 81-90: n >= 5, 3 not dividing n; (a)-(d); S = K, gamma_min = m - 1, k_c = 0). (i): compared with the summary in the report l. 535-537 only: same | (ii): the proof in the paper follows C94 l. 313-327 step by step (read on both sides); (i) not compared | correct | read: justified given the lemmas of Section 3.3 (their proofs, in Appendix A, not read); n = 5, 7, 8 (existence of a block word with a >= 1, b >= 1) and n = 6 covered |
| Rem 3.44 | `94:rem:small` | C94 l. 368-371; data | n = 4 values agree with C94 Table 2 row n = 4 and with `fw_sweep.csv` (k* = 1, k_c = 0 for 010 and 101, 2 selected cycles); n = 3: "a single flip can leave the crystal phase" confirmed by hand | n.a. | correct | n.a. |
| Thm 5.7 | `26:thm:main` | S Theorem 3 (a)-(c), Theorem 2 | **yes**, read on both sides (S l. 77-85) | not compared line by line | correct | read: justified; n = 4 covered (one cycle) |
| Prop 5.8 | `26:prop:indices` | S Theorem 4 | **yes**, read on both sides (S l. 88-91): n = 2^k >= 8; (a), (b), (c) | proof (Appendix B) not read | "(Proof in Appendix B)" correct | not read |
| Prop 5.9 | `26:prop:even` | S Theorem 5, Corollary 5 | **yes**, read on both sides (S l. 93-98): n >= 6 even, not a power of two | proof (Appendix B) not read | correct | not read |
| Prop A.1 | `94:prop:periodic` | C94 Theorem 1 | **yes**, read on both sides (C94 l. 73-79): n >= 3; three cases; count; "period divides 6" | proof identical in its steps to C94 l. 307-311 | correct | read: justified given Lemmas 3.30, 3.33, 3.35, 3.36 (not read) |

## 3. Findings

Severity classes: (1) false statement; (2) gap in a proof; (3) hypothesis or range not met; (4) unclear;
(5) cosmetic.

**Class (2): none found.** My part contains no proof; in the proofs read in passing (table above) I found no
unjustified step.

1. **Abstract l. 68-69; Introduction l. 114-115; paragraph after Theorem 3.1, l. 331. Class (1): the summary is
   stronger than the theorem.** "We determine the selected cycles and k* for four rules, for every ring size from a
   small bound on"; "In each case covered by the theorem the set of noise-selected cycles and the eight indices k_v
   behind k* are determined"; "these theorems also give the noise-selected set". For rule 94 with 3 not dividing n,
   Theorem 3.43(ii) gives Sel = K, "the set of cycles that can be reached in G_1 from a block word", and Section 6.2
   says of this same set (l. 1642-1643): "Not determined is the closed class K of Theorem 3.43(ii) on its cycles
   without 101. For even n with 3 not dividing n it is not known which cycles of doubled words lie in K". So for
   this case the selected set is characterised but, by the paper's own words, not determined. The indices k_v and k*
   are determined in every case. *Correction:* abstract: "We determine k* for four rules, and the selected cycles
   except for rule 94 with 3 not dividing n, where they are determined up to the cycles without 101"; introduction:
   "the eight indices k_v are determined, and the set of noise-selected cycles is given: ... or (rule 94) the unique
   closed class, which contains every cycle with an occurrence of 101 and is not determined on the other cycles
   (Section 6.2)".

2. **Introduction, l. 93-95. Class (1) for one clause, class (3) for the missing range.** "Under rules 43 and 142
   the state (0011)^{n/4}, and under rule 94 the state (011)^{n/3}, has a cycle that no single flip can leave and
   that every other cycle can reach by single flips; when it exists it is selected, alone or with its rotations."
   (a) For rule 94 the cycle of (011)^{n/3} is the fixed point A_1. Theorem 3.43(i) states only "from every other
   cycle there is a directed path in G_1 to a crystal phase" (l. 1157), and by Step 1 of its proof no edge leaves
   A_2 or A_3, so these two cycles cannot reach A_1: the clause "every other cycle can reach" is false as written.
   (b) No range of n is given. At n = 3 the state 011 exists; Remark 3.44 says "At n = 3 a single flip can leave the
   crystal phase" (l. 1245-1246), which contradicts "no single flip can leave"; and "when it exists it is selected"
   fails there: by hand, the cycles at n = 3 are {000}, {011}, {101}, {110} (100 -> 111 -> 000), every flip of a
   crystal phase leads to 000 and no flip leaves 000, so {000} is the only closed class and Sel = {{000}} by
   Theorem 2.8. (Hand calculation; the machine check was not run.) *Correction:* "... has, for n >= 6 in the case
   of rule 94, a cycle that no single flip can leave; every other cycle can reach it or, for rule 94, one of its
   rotations by single flips; then it is selected, alone or with its rotations."

3. **Paragraph after Theorem 3.1, l. 330-331. Class (5).** "Parts (a), (b) and (c) are Theorems 3.11, 3.28 and
   3.43 ...; these theorems also give the noise-selected set and all indices k_v." Theorem 3.28 (`43:thm:main`,
   l. 992-995) states k* only; Sel and the k_v are in Corollaries 3.21 and 3.27. *Correction:* "these theorems and,
   for rules 43 and 142, Corollaries 3.21 and 3.27 also give ...".

4. **Section 4, l. 1256-1263, Table 2 row "154, n even", and abstract l. 77-78. Class (4).** The scheme asks for
   "one-flip moves ... that change the quantity by a fixed amount", and the abstract says the proofs "share one
   structure: ... one-flip moves that change the quantity by a fixed amount". For rule 154 the quantity of column
   (1) is the two-valued property "having ones on both parity classes"; column (3) says "deleting a one of the
   parity class with fewer ones: that number drops by 1". "That number" is the number of ones of the state on its
   smaller parity class. It is not the quantity of column (1), and Section 3.1 does not show that it is constant on
   a cycle (mu(C) is defined as a minimum over the states of C, l. 491). The move is used only in the proof of
   Theorem 3.9(c) (n = 2^k), not in the proof of Theorem 3.10. The text says the table "says where the scheme is
   met only in part" (l. 1263); the table and its caption say so for rules 26 and 94, not for rule 154. The
   description of the move itself agrees with the proof of Theorem 3.9(c) (l. 506-514). *Correction:* add to the
   caption of Table 2: "For rule 154 the quantity has two values; the number that drops by 1 is a property of the
   state, used for n = 2^k only"; in the abstract write "one-flip moves that change the quantity in a controlled
   way" or add "in part".

5. **Caption of Table 1, l. 342-345. Class (5).** Recount by hand from `table_kstar.tex`: 19 columns (n = 4..22)
   times 5 rules = 95 cells; second rows without "--": 19 + 19 + 19 + 18 + 3 = 78; in all 78 the computed value is
   admitted. The three macros are correct. Two points of wording: (i) "The theorems give a value in 78 of the 95
   cells": in two of the 78 (rule 26, n = 4: ">=1"; n = 16: "1/2") the entry is a bound or a pair, not a value;
   (ii) "'--' that the paper has no statement": for rule 26 at n = 6, 10, 12, 14, 18, 20, 22 the paper has a
   statement (Proposition 5.9); it fixes no value. *Correction:* "The second rows have an entry in 78 of the 95
   cells"; "'--' that no statement of the paper gives a value or a bound".

6. **Introduction, l. 103-105. Class (5).** "computed k* for the 13 classes ... for n = 8, ..., 22 (data file
   `data/ring_size/mechanisms.csv`)". The file has 13 rules and n = 8..22, but no record for rule 154 at n = 22
   (checked; the caption of Table 1 and TRACE Part D, item 8, say the same). *Correction:* add "(for rule 154 at
   n = 22 the value was computed by the verification of the study)".

7. **Section 6.2, l. 1633, and Table 2, row 26. Class (5).** "The periodic states that contain 111 are not
   described". By Lemma 26:lem:kinds the periodic states that are not described are those whose *cycle* contains
   111; such a state need not contain 111 itself. Section 5, l. 1488, has the exact form ("the cycles that contain
   111 are not described"). *Correction:* use that form in both places.

8. **Section 6.2, l. 1633-1638. Class (4).** "Three things depend on them [the periodic states that contain 111]:
   ...; and all odd n, which the proofs do not treat." No statement of the paper shows that the odd case depends on
   these states; the paper's reason for leaving odd n out is another one (l. 1511-1512: "the parity of a cell is not
   defined and chi has no meaning"), and the source says only "Odd n is not treated" (`PROOF_26.md` l. 319-320).
   *Correction:* "Two things depend on them: ... . Odd n is not treated at all." (The source adds one proved fact
   for odd n, Proposition V26 of the report, tag [proved, verification]: the zero state can be left by one flip. The
   paper does not mention it; that is not an error.)

9. **Introduction l. 136 and Section 2.5 l. 257-258. Class (5).** "Theorem 2.8 restates results of these authors";
   "It restates known results". The attribution paragraph (l. 310-318) limits this to "Lemmas 2.6 and 2.7 and the
   first sentence of Theorem 2.8" and says "The value gamma_min = m - 1 was not found in the sources read".
   *Correction:* "the first sentence of Theorem 2.8 restates ...".

10. **Section 6.2, l. 1614-1615. Class (5).** "rule 45 is a bijection, being the complement of the mirror image of
    rule 154". Checked by hand: the mirror image of rule 154 is rule 210, and 255 - 210 = 45, so rule 45 is rule
    210 with the output negated; with Lemma 3.6 the claim for odd n follows. But l. 333 uses "complementation of the
    rule" for the equivalence of rules (under which the class of 154 is {154, 210, 166, 180} and does not contain
    45). *Correction:* "being the mirror image of rule 154 with the output negated".

11. **Abstract, l. 67-68. Class (5).** "An integer k* >= 0 records how far the selected cycles are from containing
    all eight neighbourhood configurations". By (1) of Section 2.3, k_v is a minimum over all cycles C of
    gamma(C) - gamma_min + R(C -> D_v), not a distance from the selected cycles: in Theorem 3.9(f), k_011 = 1 is
    reached through a cycle that is not selected. The second half of the sentence ("k* = 0 iff they contain all of
    them") is exact (Lemma 2.2). *Correction:* "An integer k* >= 0, defined from the potentials, vanishes iff the
    selected cycles contain all eight neighbourhood configurations."

## 4. Part (a) sentence by sentence: what agrees

Every other claim of the abstract, of the paragraphs "The question" and "Results" and of Theorem 3.1 was compared
with the statement named and has the same range and quantifiers:

* rule 154, n >= 3 (Thm 3.11); rules 43, 142, n >= 4 (Thm 3.28); rule 94, k* = 1 for n >= 6 with 3 | n and
  k* = 0 for n >= 5 with 3 not dividing n (Thm 3.43); n = 3, 4 not covered; computed k* = 1 at n = 4
  (Remark 3.44; `fw_sweep.csv`, record rule 94, n = 4: kstar = 1).
* "the zero state alone, or all cycles" (Thm 3.11); "the cycle of (0011)^{n/4}, or the cycles on the two levels"
  (Cor. 3.21, 3.27); "the three rotations of (011)^{n/3}" (Thm 3.43(i)); "one closed class that contains every
  cycle with an occurrence of 101" (Thm 3.43(ii): "contains every cycle with a non-empty frozen set").
* rule 26: zero state the only selected cycle for n = 2^k, k >= 2 (Thm 5.7); k* is 1 or 2 for k >= 3 and k* = 1
  for odd k >= 3 (Prop. 5.8, n = 2^k >= 8); computed k* = 2 at n = 4 and n = 16 (`fw_sweep.csv` and
  `mechanisms.csv`); even k >= 6 open (Section 5, l. 1486-1488); even n not a power of two: one closed class and
  k* = 0 iff it contains a cycle with 111 (Prop. 5.9, n >= 6); "computed for n <= 22": the seven even n in 6..22
  that are not powers of two have computed values in Table 1; odd n not treated.
* What is called "computed" (rule 94 at n = 4; rule 26 at n = 4, 16; the question of Prop. 5.9 for n <= 22) is
  nowhere called proved, and conversely.
* "rule 90 ... sends every state to the zero state exactly when n is a power of two" (l. 96-97): the paper proves
  this for even n (Lemma 3.4); for odd n it is not proved in the paper and is not needed there.
* "Rule 43 and rule 142 are not equivalent under reflection and complementation" (l. 333): checked by hand from the
  rule tables of l. 585-587 (classes {43, 113} and {142, 212}).

## 5. Part (b): Table 1

* Recount: finding 5. `TableCells` = 95, `TableCompared` = 78, `TableAgree` = 78 are correct.
* "Theorem" rows against the theorems, every n = 4..22: rule 154: 1 at n = 4, 8, 16, else 0 (Thm 3.11): correct.
  Rules 43, 142: 1 at n = 4, 8, 12, 16, 20, else 0 (Thm 3.28): correct. Rule 94: "--" at n = 4; 1 at n = 6, 9, 12,
  15, 18, 21; 0 at the other n >= 5 (Thm 3.43): correct. Rule 26: ">=1" at n = 4 (Thm 5.7 and Lemma 2.2), "1" at
  n = 8 (Prop. 5.8(c), k = 3), "1/2" at n = 16 (Prop. 5.8(b)), "--" elsewhere: correct, with the remark on "--" in
  finding 5.
* "Computed" rows against the data: all five rows, n = 4..7 against `data/fw_sweep.csv` (columns n, rule, kstar)
  and n = 8..22 against `data/ring_size/mechanisms.csv` (columns rule, n, kstar): 94 cells, no difference. The
  95th cell (rule 154, n = 22) has no record in `mechanisms.csv`, as the caption says; not compared (deviation 3).
  For n = 8..20 the two files have 169 common (rule, n) pairs among the 13 rules, with equal kstar.

## 6. Part (c): Section 4 and Table 2

| row / sentence | lemma cited | what the lemma states | verdict |
|---|---|---|---|
| 43, 142 (1) "number of walls; conserved" | 43:lem:cons(b) | "w(Fx) = w(x)" | agrees |
| 43, 142 (2) "all: the states without isolated cell or without interior cell" | 43:lem:per(a) | "a state is periodic iff it has no isolated cell or no interior cell" | agrees |
| 43, 142 (3) "flip of an interior cell: w+2; of an isolated cell: w-2; slides: w unchanged" | 43:lem:flip, 43:lem:slides | "+2 if cell j of x is interior, -2 if it is isolated, and 0 otherwise"; slide = flip between periodic states with the same wall count | agrees |
| text: "the value n/2 ... is taken by a periodic state iff 4 divides n, and then by the four states of one cycle only" | 43:lem:half | "If 4 divides n, the periodic states with wall count n/2 are exactly the four states of X; they form one cycle" | agrees; the "only if" for n = 2 mod 4 is not a sentence of the lemma but follows from it with Lemmas 3.16(c), 3.18(a), or from w being even |
| text: "otherwise the two even numbers next to n/2 are joined by flips in both directions" | 43:lem:levels(c) | "Every cycle of the lower level has an edge of G_1 to a cycle of the upper level, and conversely" (n >= 5) | agrees for n >= 5; Section 4 gives no range |
| 154 (1) | 154:lem:rule90, 154:lem:invariant | F(E) in O, F(O) in E; F(M) in M | agrees |
| 154 (2) | 154:lem:periodic | "The periodic states of F are the states of M and the periodic states of L in E u O" | agrees |
| 154 (3) "deleting a one of the parity class with fewer ones" | proof of 154:thm:pow2(c); 154:lem:moves | l. 506-514; moves(a): C_y = C or edges in both directions | the move is the one of the proof; see finding 4 |
| 26 (1) | 26:lem:chi | "chi(Fx) <= chi(x)" | agrees |
| 26 (2) | 26:lem:parity, 26:lem:domain(c) | rule 90 on E u O; "every domain state is periodic" | agrees; wording of the last clause: finding 7 |
| 26 (3) "deleting a singleton group: chi - 2; flips of free cells of domain states: chi unchanged" | 26:lem:singleton(b), 26:lem:domain(c) | "chi(x+e_j) = chi(x) - 2"; "gives a domain state with the same sources" | agrees (chi is the number of groups, hence of sources) |
| 94 (1) | 94:lem:freeze | Fz(x) in Fz(F^t x); constant on a cycle | agrees |
| 94 (2) "all (Prop. A.1); for 3 dividing n only the block words are needed" | 94:prop:periodic; proof of 94:thm:main(i) | three cases; part (i) uses Lemmas 3.30, 3.31, 3.32, 3.38, 3.39 | agrees |
| 94 (3) "growth and freezing flips: the frozen set grows; swap, a unchanged; merge, a-3; split, a+3" | 94:lem:growth, refreeze, swap, merge, split | growth: Fz grows properly (n >= 5); refreeze: periodic to periodic, Fz grows; swap sl -> ls; merge sss -> ll; split sll -> ssss | agrees |
| text: "rule 90, which is nilpotent iff n is a power of two" | 154:lem:nilpotent, 26:lem:parity | (a) n = 2^k; (b) n even, not a power of two; 26:lem:parity has the "if" half only | agrees for even n |
| text: "a = 0 is possible iff 3 divides n, and merging reaches it" | proof of 94:thm:main(i), Step 3 | n >= 6 | agrees |

All `\ref` of Section 4 and Table 2 point to the statements meant.

## 7. Part (d): Section 6.2, sentence by sentence

| sentence (tex line) | named proof or source | what I compared | verdict |
|---|---|---|---|
| "k* changes with n for 8 further classes" (1607) | `mechanisms.csv` | 13 rules in the file; each of 35, 37, 45, 73, 122, 22, 60, 90 has both k* = 0 and k* >= 1 in n = 8..22 | agrees |
| Class 35: k* >= 1 at 9, 12, 15, 18, 21; "the selected cycles do not contain the code 101" (1612) | CSV; report 5.2 | CSV values; report l. 357-358, tag [computed] | agrees; computed |
| Class 37: k* = 0 at 11, 12, 17, 18 (1613) | CSV | values | agrees |
| Class 45: k* >= 1 at n = 8 only; "for odd n rule 45 is a bijection ... and for a bijection k* = 0 [note]" (1614-1616) | Lemma 3.6 of the paper; note v0.2 | arithmetic of the rule numbers by hand; note l. 151 ("the map is a bijection of S and the uniform law is stationary") and l. 219 ("Proved for all n: ... k* = 0 for bijective rules") | agrees; wording: finding 10. Lemma P of the report not read |
| Class 73: k* >= 1 at n = 9 only (1616) | CSV | values | agrees |
| Class 122: k* = 0 at 8, 12, 16, 20, 22; "partial results on these two cycles are proved in PROOF_154.md, Section 7" (1616-1620) | PROOF_154.md 7.1 | Lemmas R1 to R4 tagged [proved], Corollary R5 [proved, using Theorem A], all for even n >= 4; what decides the selection is tagged [computed] and [attempted (gap ...)] | agrees: "partial results ... are proved" is what the source has; the paper does not say that they are for even n. Proofs R1-R4 not refereed |
| Class 22: k* >= 1 at 8, 14, 15, 16, "where the zero state is selected alone"; "for 4 dividing n it is proved in the report (Proposition R22) that no single flip leaves the zero state iff n is a power of two" (1620-1622) | report l. 424-434, 473-474 | CSV values; R22: "for 4 | n, r(0) >= 2 under rule 22 iff n is a power of two", tag [proved]; "0 is selected alone [computed]" | agrees: statement, range and tag. The proof of R22 was read once; checked by hand at n = 4 only |
| Classes 60, 90: k* >= 1 at 8, 16 only, k* = 1 resp. 2, one cycle (1622-1625) | CSV | kstar and cycles at n = 8, 16 in both files | agrees |
| "For rule 90 on 2^j cells this is Lemma 3.5 of [MOW]" (1625) | literature | repository record only (report l. 113-114) | not checked against the text of the reference |
| rule 60: Wolfram p. 963, "an inference recorded in the study, not a statement read in that note" (1625-1628) | `literature_ring_size.md` l. 100-104 | "Inference (mine, not stated in NKS)" | agrees with the record |
| "A proof that k* >= 1 iff n is a power of two, for both classes and every n >= 4, is Proposition 1 of [note]" (1628-1630) | `note_v0.2.tex` l. 210-216 | statement: "For the classes of rules 60 and 90 and every n >= 4, k* >= 1 iff n is a power of two"; it is the first proposition of the note; l. 219: "Proved for all n >= 4" | agrees: statement, range, tag. Proof read once, not refereed (it uses results of the note's Section on results) |
| Rule 26: "computed: k* = 0 at n = 14, 20, 22 and k* >= 1 at n = 10, 12, 18" (1636-1637) | CSV; PROOF_26.md Table 2 | CSV values; Table 2 column "cycles with 111 in K": 0 of 1, 0 of 0, 2 of 2, 0 of 1, 3 of 4, 2 of 13 | agrees; tag in source [computed for even n <= 22] |
| Rule 26: "the value of k* for n = 2^k with even k >= 6" open (1634) | PROOF_26.md l. 308-315 | tag [attempted (gap: no description of the cycles that contain 111)] | agrees |
| Rule 26: "and all odd n" (1637) | PROOF_26.md l. 319-320 | "Odd n is not treated" | agrees as to "not treated"; "depend on them": finding 8 |
| Rule 94: "All periodic states are described (Prop. A.1), and k* is determined for every n >= 5" (1641) | Prop. A.1; Thm 3.43 | statements | agrees |
| Rule 94: doubled words "computed: 0 of 5 at n = 10, 7 of 9 at n = 14, 10 of 45 at n = 20 and 0 of 33 at n = 22 (the last ... not recomputed by the independent verification)" (1643-1644) | C94 Table 2; l. 361-364; VERIFICATION_94_26.md l. 254-255 | the four values; tag [computed]; "'0 of 33 for n = 22' ... is not checked" | agrees |
| Rule 94: "{0} ... is proved in PROOF_94_converse.md (Proposition 3) that it lies in K for n = 5, 7, 8 and not for n >= 10 with 8 not dividing n and 3 not dividing n" (1644-1646) | C94 l. 92-94, proof l. 329-348, Lemma 16 l. 288-303 | statement (i), (ii); tag [proved]; proof of (ii) and of Lemma 16 read as a referee: the four cases for y + e_j are complete and each is justified, given Theorem 1 and Lemma 9 of C94 | agrees: statement, range, tag |
| Rule 94: "when 8 divides n and n >= 16 this is not determined by a proof (computed: not in K at n = 16)" (1646-1647) | C94 l. 365-367, Table 2 row n = 16 | "{0} in K: False"; tag [computed] | agrees (the source's own "n >= 24" is the point of TRACE Part D, item 7) |

The paragraph "Computed values and the open case" of Section 5 (l. 1479-1502), which quotes sections 7 and 8 of
`PROOF_26.md`, was compared as well: the values at n = 4 and n = 16 (Table 3), "2 of the 3 cycles ... pass through
a carrier word" (Table 2), the bound (n + 8)/3 and the values 6 and 10 of chi at n = 22 (l. 311-314, Table 2), and
the list of what is proved about a cycle with 111 (l. 315-318) agree with the source. The sentence "in one step 111
arises only from 10011" was checked by hand.

## 8. Macros of `numbers.tex` seen against a source

Agree: the three table macros; `KstarNinetyFourAtFour`, `NinetyFourFourClosed`, `NinetyFourFourClassSize`,
`NinetyFourFourCodes` (CSV record rule 94, n = 4, and C94 Table 2); `TwentySixFourCycles`, `TwentySixFourKv`,
`KstarTwentySixAtFour`, `KsevenTwentySixAtSixteen`, `KstarTwentySixAtSixteen` (CSV); `TwentySixSixteenWith`,
`TwentySixSixteenReach`, `TwentySixSixteenCarrier`, `TwentySixTwentyTwoChi` (PROOF_26.md Tables 2, 3);
`TwentySixEvenZero`, `TwentySixEvenPos`, all `Kpos...`, `Kzero...`, `KstarSixtyPos`, `KstarNinetyPos`,
`CyclesSixtyNinetyPos`, `NumSwitching`, `NumOtherSwitching`, `OpenNmin`, `OpenNmax` (CSV);
`NinetyFourDoubledInK` (C94 Table 2). Not compared: `ZRValues`, `ZRBound`, `ZRNmin`, `ZRNmax` (Section 6.1, not
my part).

## 9. What I did not check

* The one cell of Table 1 with the dagger (rule 154, n = 22), whose source is a JSON file.
* The machine check of rule 94 at n = 3 and of rule 154 at n = 6 (not run; n = 3 done by hand).
* Lemma P of the report.
* The proofs in Appendices A and B (all lemmas of Section 3.3, Propositions 5.8 and 5.9), and the proofs of the
  lemmas of Sections 3.1 and 3.2 as a referee (they were read once while reading the sections; no verdict is
  given on them here).
* Statements against their sources, except where the table of section 2 says "read on both sides".
* The proofs of Lemmas R1 to R4 and Proposition R22 of the sources and of Proposition 1 of the note beyond one
  reading; whether these were verified independently.
* Anything in the literature: Lemma 3.5 of Martin, Odlyzko and Wolfram, Wolfram p. 963, and the paragraph "What was
  known" beyond its description of the paper's own results. The paragraph "Status of the proofs", Section 6.1 and
  the statement on the use of AI.
* That the eight classes of Section 6.2 are named by their smallest rule number (believed, not computed).
* The descriptions "the zero state is selected alone" (class 22) and "the selected cycles do not contain 101"
  (class 35) against the data; they were compared with the report only.
* `paper/REFEREE_NOTES.md` (not opened, as instructed), `numbers.json`, the figures, the PDF.

Claude
