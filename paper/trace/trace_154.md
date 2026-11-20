# trace_154.md — track "rule 154" of the ring-size paper

Fragment: `sec_154.tex` (218 lines; one `\section{Rule 154}\label{sec:154}`).
Source: `verify_ring_size/part2_154/PROOF_154.md` (branch paper-ring-size), Sections 0 to 4; line numbers below are lines of that file ("P154 l.").
"F l." are lines of sec_154.tex.

## 0. Not done, cut, not checked; incidents

* **Length: 2.72 pages** of the harness PDF (a4, 10pt) against a budget of 2.25: over by 0.47 page. No step of a
  proof was dropped to save space; what was cut is listed in Section 6 below.
* **Incident in the repository folder (my fault, repaired).** One of my search commands ran with the repository
  as working directory and its output redirect created the untracked file `grep154.txt` (36641 bytes, dated
  20 Nov 11:26) in the repository root. Nothing else was written, no tracked file was touched, no git command
  that changes anything was run. I copied the content to my workspace and removed the file through the approved
  deletion tool (moved to the Trash, not `rm`); `git status --porcelain` afterwards shows only `PR_BODY.md` and
  `PR_DRAFT.md`, as before my session.
* **Observed, not mine, not touched.** At 11:35 `git status` also showed an untracked `lit_grep.txt` (6664 bytes,
  dated 11:34) in the repository root. No command of mine wrote it. At my last status check it was no longer
  there. I did not open more than its first three lines and did not delete it.
* **Not run** (by instruction): the scripts of `verify_ring_size/part2_154/`, any enumeration, any test. All
  checks of this track are by reading; the hand re-check of the source's steps is described in Section 8.
* **Not read:** PROOF_154.md Sections 7 to 10 (rules 122 and 26, summary, scripts, cost), except the section
  headings. The cited literature itself (no network; see Section 4 for how each reference was seen by the repo).
* **Verification documents** were searched by keyword (`154`, `P154`, `PROOF_154`, `rule 90`, `2^k`, `power of
  two`, `Martin`, `nilpoten`) and the hits read in context; they were not read in full.

## 1. Statements

Tag in the source: every statement below is tagged **[proved]** in P154, and Section 0 of P154 (l. 12-15) says
"The proof is elementary and uses no computation."

Verification verdicts that apply to all rows (abbreviations used in the table):

* **V-D2** = `VERIFICATION_ring_size.md`, Part 2, D2 (l. 449-487): heading "Rule 154, all n >= 3 — **proved**";
  "Full text: `part2_154/PROOF_154.md`, sections 1 to 4 (no computer-assisted step)"; checks (l. 477-484): "The
  lead read every step, re-derived the four local cases of Lemma 5, and tested the statements with separate code
  for every n = 3..16 on all states (`audit/audit_154.py`, `audit/out/audit_154.json`)". No finding number records
  an error in P154. Limitation stated by the same document (Summary item 6, l. 62-66): "These proofs were checked
  inside this verification only (line-by-line reading and two separate codes each); they have had no outside
  reader." P154 was produced by a track of that verification session, so V-D2 is a check by the lead of the
  session that produced the proof.
* **R-5.7** = `report_ring_size.md`, Section 5.7 (l. 525-533, Theorem V154 l. 555-574): "(i) the lead of the
  verification read both proofs line by line and re-tested every lemma with separate code
  (`verify_ring_size/audit/`); (ii) a second read outside both sessions checked `PROOF_154.md` and `PROOF_94.md`
  step by step and with separate code (rule 154: all states for n = 3..18 and potentials from the definitions at
  n = 4, 5, 6, 8, 10 ...) and found no error (as reported by the author; that code is not part of this branch).
  Neither proof has a computer-assisted step. They have not been through peer review."
* **V-9426** = `VERIFICATION_94_26.md`: l. 104 "Cited results of P154 used by C26 (Lemma 3, Lemma Q1, the
  conventions of Section 1): correct."; l. 259 (Not checked) "P94 and P154 beyond the results that C94 and C26
  cite." So of this track's statements only Lemma 3 of P154 has a verdict there.
* `VERIFICATION_43_142.md`: **no verification of any statement of P154 is recorded** (the only hit for "154" is
  l. 172, a literature scan of Voorhees and Beauchemin).

| paper label | source statement and line | tag | verdict of the verification | changes of wording and notation |
|---|---|---|---|---|
| `154:lem:local` | P154 Lemma 1, l. 58-61 | [proved] | V-D2 l. 478-479: "the formula of Lemma 1" tested n = 3..16. R-5.7 (ii): no error found. | The rule is introduced by its table (f = 1 on 001, 011, 100, 111) instead of "bit (4a+2b+c) of 154" (NOTATION forbids the number of a code); the proof compares the eight values with that table instead of with the binary digits of 154. |
| `154:lem:rule90` | P154 Lemma 2, l. 63-69 | [proved] | V-D2: read; no separate test named for this lemma in D2. R-5.7 (ii): no error found. | "rule 90, L = sigma + sigma^(-1)" moved to the opening paragraph; site -> cell. |
| `154:lem:nilpotent` | P154 Lemma 3, l. 71-80 | [proved] | V-9426 l. 104: "correct". V-D2: read. R-5.7 (ii): no error found. | Exponent 2^j -> 2^s (j is a cell in the paper); e_i -> e_j. |
| `154:lem:invariant` | P154 Lemma 4, l. 84-91 | [proved] | V-D2 l. 480: "F(M) lies in M ... at every even n" (n <= 16). R-5.7 (ii): no error found. | site -> cell. |
| `154:lem:collisions` | P154 Lemma 5, l. 93-113 | [proved] | V-D2 l. 477-480: the lead "re-derived the four local cases of Lemma 5"; "all pairs of states with equal image (257 pairs at n = 16) are of the three kinds of Lemma 5". R-5.7 (ii): no error found. | x' -> y; (*) -> equation (1) of the section; site -> cell. |
| `154:lem:periodic` | P154 Lemma 6, l. 120-128 | [proved] | V-D2 l. 480-481: "every state of M is periodic at every even n; at n = 4, 8, 16 the periodic states are M and 0". R-5.7 (ii): no error found. | The count (2^(n/2) - 1)^2 + 1 is left out (Section 6); "periodic states of rule 90" -> "of L"; F^j(x) = x -> F^t(x) = x. |
| `154:lem:moves` | P154 Lemma 7 (a), (c), l. 130-141 | [proved] | V-D2: read; "symmetry of the edges between cycles in M, connectivity inside M" are tests of P154's own Section 5 (l. 226-228), not of the lead. R-5.7 (ii): no error found. | Part (b) of the source is left out (not used by the theorems); source (c) is (b) of the paper. Flipped cell i -> j. Proof of (a) uses the last sentence of `lem:edge` instead of two applications of Lemma 0. 1^n -> \one. |
| `154:thm:pow2` | P154 Theorem 1 (a)-(f), l. 145-183 | [proved] | V-D2 l. 453-455 (statement), l. 480-484: at n = 4, 8, 16 "{0} has no out-edge, every cycle reaches {0}, and the G1 distance never exceeds the bound of Theorem 1"; "The sealed sample shows the potentials of Theorem 1(e) at n = 8 and 16". R-5.7 (ii): potentials from the definitions at n = 4, 8; no error found. | Codes as words: k_0 -> k_000, "c = 1..7" -> "the seven codes v != 000"; S = {{0}}; G1 -> G_1; "enters/ends in" -> "ends on"; (b) is argued from the statement of `lem:edge` (orbit of 0 + e_j) instead of from the form of a path of resistance 1; "(Proposition prop:order)" added as the reference for k_000 = 0. |
| `154:thm:other` | P154 Theorem 2, l. 194-211 | [proved] | V-D2 l. 456 (statement), l. 482-484: "G1 is strongly connected at n = 6, 10, 12, 14"; "gamma = m - 1 for all cycles at n = 20 and 21" (sealed sample). R-5.7 (ii): potentials at n = 5, 6, 10; no error found. | "k_v = 0 for all eight codes v" moved from the last line of the source's proof into the statement; "The cube graph is connected" -> "Any two states are joined by a sequence of single flips"; states written as words 0^(n-2)11 etc. in \code; "(Proposition prop:order)" added as reference for the last line. |
| `154:thm:main` | P154 Corollary, l. 213-214, with the values of k_v from Theorem 1(f) (l. 152) and the last line of the proof of Theorem 2 (l. 211) | [proved] | V-D2 l. 457: "k* = 1 iff n is a power of two (n >= 4), for all n >= 3". R-5.7 l. 558-559. No separate check beyond those of the two theorems. | "The selected set is {0}" -> S = {{0}} (set of cycles); the values of k_v are added to the statement from the two theorems. Ranges as in the source: every n >= 3; "power of two (n >= 4)". |

## 2. GAPs

None. No `\GAP` in the fragment.

## 3. Errors found in sources

No mathematical error found in P154 Sections 0 to 4 (hand re-check: Section 8). No `\SOURCEERR` in the fragment.

Two points that are not errors of mathematics, reported and not corrected:

1. P154 l. 15 and l. 214 write "S = {0}" / "The selected set is {0}" for the set whose only element is the cycle
   {0}; l. 151 writes it correctly as {{0}}. The paper uses {{0}} throughout.
2. `literature_ring_size.md` is not consistent with itself on how the Nobe-Yura (2004) statement was seen:
   l. 35-38 say the bijectivity of rule 154 at odd n is stated "by its abstract in Nobe and Yura (2004)"; l. 244-246
   say the abstract states that exactly 16 ECA rules are reversible for infinitely many cell sizes and that
   "Proposition 1: the rule-154 ECA is reversible for the cell size N = 1 (mod 2)" was seen in a search snippet,
   "**Not read**". The fragment says "known here from its abstract and a search excerpt only".

## 4. Credits given (with the repo line that states the attribution)

1. After `154:lem:nilpotent` (F l. 44-46): `\cite{MartinOdlyzkoWolfram1984}`, Lemma 3.5 for rule 90 on 2^k cells
   and Theorems 3.3, 3.4 with corollaries for the converse for a single one.
   * `literature_ring_size.md` l. 39-40: "**Rule 90 at n = 2^k (A25).** Martin, Odlyzko and Wolfram (1984),
     Lemma 3.5 (p. 230); the "iff" follows from their Theorems 3.3 and 3.4 with corollaries."
   * `report_ring_size.md` l. 113-115: "Martin, Odlyzko and Wolfram (1984), Lemma 3.5 (p. 230): for N = 2^j every
     configuration evolves to the null configuration; with their Theorems 3.3 and 3.4 and corollaries the
     single-seed orbit dies iff N is a power of two (read by the verification)."
   * `VERIFICATION_ring_size.md` A25, l. 297-298. P154 itself (l. 81-82) says only that part (a) and the
     single-seed case "are the study's Proposition R154".
   * How seen: `literature_ring_size.md` l. 15-16, "Martin, Odlyzko and Wolfram (1984) in full (author copy at
     content.wolfram.com)", by the verification session. Not seen by me.
2. After `154:lem:collisions` (F l. 89-90): `\cite{NobeYura2004}` for the bijectivity of rule 154 on rings of
   odd size, with the words "known here from its abstract and a search excerpt only".
   * `literature_ring_size.md` l. 35-38: "**Bijectivity of rules 154 and 45 at odd n (A24)** is stated in
     Bhattacharjee and Das (arXiv:1903.06011, Example 2) and in Fedoriaka (arXiv:2501.06648, Section 3: exhaustive
     computation for N in [4, 20] with explicit circuit constructions, not a proof for all odd N), and by its
     abstract in Nobe and Yura (2004)."
   * `report_ring_size.md` l. 252-255 and l. 103-106; `VERIFICATION_ring_size.md` A24, l. 291-295.
   * How seen: **not read by any session** (`literature_ring_size.md` l. 243-246: abstract through the fetch tool,
     Proposition 1 in a search snippet, "Not read; the green-OA host was refused"). This conflicts with the house
     rule "cite only what a session has read"; see the note for the editor in my report. The two sources the
     verification did read (Bhattacharjee and Das, in part; Fedoriaka, in full) have no key in the list given to
     this track.

Credits considered and not given in the fragment: `NobeYura2007` (whether rule 154 is in its class is "unknown
(not read)", `literature_ring_size.md` l. 247; `literature_addendum.md` A2, l. 124-138); `ZhuRichard2026`
(`literature_addendum.md` A1, l. 35-122: a numerical observation that Lemma 6 of P154 accounts for; not a known
building block of a proof, seen in search excerpts only, and it would need computed values); the "partial
precedents" of the reduction to rule 90 (`literature_ring_size.md` l. 41-45, A26: OEIS A070886 and Section 5 of
Martin, Odlyzko and Wolfram for rule 18; `literature_addendum.md` A3, l. 147-162: Nordahl 1989, no key) — the repo
says of the ring statements for rule 154 "not found in the sources read" (l. 44-45) and that whether Nordahl's
simulation is the one of Lemma 2 "was not checked" (addendum l. 160-162), so no attribution is stated for
`154:lem:rule90`. Theorem A and its credits are not used in this section (the source computes gamma directly;
P154 l. 185-186).

## 5. General facts used beyond the shared statements of Section 2

Each is used by the source at the place named and is not one of `lem:edge`, `prop:order`, `lem:reroot`, `thm:A`,
`lem:sym`.

1. An injective map of a finite set into itself is a bijection (`154:lem:collisions` "in particular";
   `154:lem:periodic`).
2. Algebra over GF(2): in a commutative algebra of characteristic 2, (a + b)^(2^s) = a^(2^s) + b^(2^s); the
   identification of the states with GF(2)[z]/(z^n + 1), the rotation being multiplication by z; unique
   factorisation in GF(2)[z] (`154:lem:nilpotent`).
3. Graphs: in a strongly connected directed graph every vertex is the root of a spanning in-tree; if every vertex
   other than the root has an edge to a vertex closer to the root, these edges form a spanning in-tree; an in-tree
   rooted at C contains exactly one edge leaving each other vertex (`154:thm:pow2`(d), (e); `154:thm:other`).
4. V is integer-valued (a sum of Hamming distances), so "no edge of G_1" together with V >= 1 (`lem:edge`) gives
   V >= 2 (`154:thm:pow2`(b), (e)). The fragment states this as the source does (P154 l. 147), without the reason.
5. The definition of k_v itself (not only the consequences listed with `prop:order`): the lower bound k_v >= 1 in
   `154:thm:pow2`(f) uses k_v = min_C [gamma(C) + R(C -> D_v)] - gamma_min, R >= 0, and R({0} -> D_v) >= 1 because
   the state 0 does not contain v. The upper bounds use that a path 0 -> e_0 -> F(e_0) has resistance 1.
6. Any two states are joined by a sequence of single flips (`154:lem:moves`(b), `154:thm:other`, odd n).
7. gamma(C) >= m - 1 for every cycle because an in-tree has m - 1 edges of weight >= 1 (`lem:edge`); used for
   gamma = m - 1 in both theorems.

## 6. \DATA items; what of the source is not in the fragment

`\DATA` items: none. No number from an enumeration or a data file is in the fragment.

Left out of the fragment:

* P154 Lemma 0 (l. 48-54): replaced by `lem:edge`, as instructed.
* P154 Lemma 7(b) (l. 133, proof l. 138 "(b) Lemma 2"): [proved], not used by Theorems 1 and 2.
* The counts |M| = (2^(n/2) - 1)^2 (l. 45) and "their number is (2^(n/2) - 1)^2 + 1" (l. 122): [proved] in the
  source (no proof text is given for the count), not needed by the theorems.
* Remarks (1) to (3) after Theorem 1 (l. 185-190); the sentences on agreement with computations (l. 216-218);
  the mechanical re-check of Lemma 5 by `check_pair_graph.py` (l. 115-118), which is a script output.
* Everything tagged [computed]: Section 5 (l. 220-282), including O1 (cycle lengths divide n) and O2 (maximum
  distance n/2); Section 6 (l. 284-289).

## 7. Changes of notation against the source (complete list)

site -> cell; 0 -> \zero; 1^n -> \one; 1_E, 1_O -> \one_E, \one_O; code number c in {0..7} -> code word v
(000, ..., 111); k_c -> k_v, k_0 -> k_000; D_c -> \Dc{v}; S -> \Sel, and {0} -> {{0}} where the set of cycles is
meant; G1 -> \Gone; k* -> \kst; "enters C'" / "ends in 0" -> "ends on"; Lemma 0 -> Lemma `lem:edge`; flipped cell
i -> j in Lemma 7, Theorem 1(b), Theorem 2(3) and e_i -> e_j in Lemma 3 (as in `lem:edge`); x' -> y in Lemma 5;
(*) -> numbered equation; exponent 2^j -> 2^s in Lemma 3; F^j(x) = x -> F^t(x) = x in Lemma 6; Lemma 7(c) ->
`154:lem:moves`(b); Theorems 1, 2 and the Corollary -> `154:thm:pow2`, `154:thm:other`, `154:thm:main`. Unchanged:
E, O, M, L, sigma, m, mu(C), |x|_E, |x|_O, C_y, C_*, C_s, C_1, x^(s), j_s, d, b, z, a, q, n = 2^k.

## 8. Second pass: source line range of every step

All ranges are lines of `verify_ring_size/part2_154/PROOF_154.md`. Each step was also re-checked by hand against the local rule (the eight values of
Lemma 1; the identities (i)-(iv) of Lemma 5; L 1_E = 0; the codes named in Theorem 1(f) and in the last paragraph
of Theorem 2, for n = 3, n = 5 and general n).

**Opening paragraph (F l. 3-9).** Rule, n >= 3, m: l. 34-41. E, O, M, 1_E, 1_O, |x|_E, |x|_O: l. 43-46.
L = sigma + sigma^(-1): l. 64. The table of the rule: l. 60.

**154:lem:local (F l. 11-17).** Statement l. 58. The eight values: l. 60-61.

**154:lem:rule90 (F l. 19-27).** Statement l. 63-65. Odd i: l. 67. Even i: l. 67-68. F(x) = Lx in O: l. 68.
x in O and induction on t: l. 68-69.

**154:lem:nilpotent (F l. 29-42).** Statement l. 71-72. F^t = L^t on E u O; commutative algebra,
L^(2^s) = sigma^(2^s) + sigma^(-2^s): l. 74-75. (a) L^(n/2) = sigma^(-n/2)(sigma^n + 1) = 0: l. 75.
(b) identification, L^t e_0 = z^(-t)(1 + z)^(2t), divisibility criterion: l. 76-77. n = 2^a q, the two
factorisations: l. 77-78. Value q at z = 1, degree q - 1 >= 2, irreducible factor: l. 78-80. Rotation: l. 80.

**154:lem:invariant (F l. 48-58).** Statement l. 84. F(x) in O, x_(i+1) = x_(i-1)(1 + x_i), j = i + 1,
inequality: l. 86-87. One orbit of j -> j - 2, all odd cells equal: l. 88-89. All odd cells 1, even cells 0,
contradiction: l. 89-90. Case F(x) in E: l. 90-91.

**154:lem:collisions (F l. 60-87).** Statement l. 93-96. d and (*): l. 98-99. (i): l. 100-101. (ii): l. 102-103.
(iii): l. 104. (iv): l. 105-106. Case A: l. 107-111. Case B: l. 112-113.

**154:lem:periodic (F l. 92-105).** Statement l. 120-123 (without the count). F(M) in M and injective on M:
l. 125-126. Injective self-map of a finite set, F^t(x) = x: l. 126-127. E u O mapped into itself, F = L: l. 127.
n = 2^k, 0 the only periodic state outside M: l. 127-128. A cycle that meets M stays in M: l. 128.

**154:lem:moves (F l. 107-124).** Statement l. 130-132, 134-135. (a) y periodic, on a cycle in M: l. 137 with
l. 128; both edges: l. 137-138 (through the last sentence of `lem:edge`, whose content is l. 51-52). (b) path to
1^n through M: l. 138-140; consecutive states by (a): l. 140; joined to {1^n}, F(1^n) = 1^n: l. 141.

**154:thm:pow2 (F l. 126-179).** Statement l. 145-152.
(a) l. 154.
(b) the orbit of a single flip of 0; e_j in E u O; stays there and reaches 0 within n/2 steps; no state on another
cycle: l. 156-158 (the reduction to the orbit of 0 + e_j is `lem:edge`, source l. 48-49 and 156).
(c) choice of x, mu >= 1: l. 160. Parity assumption, j_1..j_mu, x^(s): l. 160-162. x^(s) in M on C_s, C_0 = C:
l. 162-163. s < mu - 1 and Lemma 7(a): l. 163-164. x^(mu) in E \ {0}, orbit ends in 0, edge to {0}: l. 164-165.
Deleting repetitions, length <= mu <= n/2: l. 165-166.
(d) l. 168.
(e) m - 1 edges of weight >= 1: l. 170. In-tree rooted at {0} of weight m - 1: l. 170-172. Lower bound m for
C != {0}: l. 172-173. C_*, the step of resistance 2: l. 173-174. In-tree in M by Lemma 7(c), added edge, weight m:
l. 174-176. gamma(C) = m > gamma({0}): l. 176; S = {{0}}: l. 151.
(f) k_000 = 0: l. 178. Lower bound: l. 178-179. e_0 and its three codes, F(e_0) = e_(-1) + e_1 and code 101,
resistance 1: l. 179-181. e_0 + e_1 in M, codes 011 and 110; {1^n} and code 111: l. 181-183.

**154:thm:other (F l. 181-209).** Statement l. 194-195 (k_v = 0 for all v: l. 211).
Odd n: l. 197-199.
Even n: n >= 6, the cycles: l. 200. (1): l. 201. (2): l. 202-203. (3) forward: l. 204-205; backward,
y = 1_E + e_1, F(1_E) = L 1_E = 0: l. 206. Conclusion: l. 207.
Both cases, gamma = m - 1, all selected: l. 208. The codes on periodic states, n >= 5 and n = 3: l. 209-211.
k_v = 0: l. 211.

**154:thm:main (F l. 211-218).** l. 213-214; values of k_v: l. 152 and l. 211.

No step of the fragment is without a source line range.
