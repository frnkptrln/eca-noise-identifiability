# Reader report: Section 2 "Setting" and Section 3.1 "Rule 154" of `paper/ring_size_paper.tex`

Reader: Claude. Date: 20 November 2026. Branch `paper-ring-size`. Read only; no file of the repository was changed.

## 0. Deviations and limits (read first)

1. **One step was not run.** A single text-extraction command (grep/sed) was refused by the platform ("safety
   check could not run, needs the user's approval"). I did not obtain the same lines by another route. It would
   have shown: the `\newtheorem` set-up of the paper and of the note (theorem numbers), all uses of `\rho` and of
   `\ref{lem:sym}`, `\ref{lem:kzero}`, `\ref{prop:order}` outside my part, `proofs_43_142/PROOF_43_142.md`
   l. 57-64 and 352-366, Corollary 2 of `verify_ring_size/part2_94/PROOF_94.md`,
   `proofs_94_26/PROOF_94_converse.md` l. 38-43, `proofs_94_26/PROOF_26.md` l. 42-46, and
   `literature_ring_size.md` l. 33-40 and 240-248. Everything that depends on these is marked "not checked" or
   "provisional" below.
2. **No computation was run**, not even the permitted small check. Every verdict is from reading and from
   re-deriving the steps by hand.
3. Statement numbers (2.1 to 2.8, 3.2 to 3.11) are those of TRACE.md Part A. I matched statements by LaTeX label;
   I did not check the numbers against the PDF or the preamble (item 1).

What I read in full: tex l. 120-349 and l. 349-580; `PROOF_154.md` l. 1-260; `note_v0.2.tex` l. 28-253;
`report_ring_size.md` l. 84-259; `paper/trace/trace_154.md` (all); `paper/TRACE.md` l. 1-126 and l. 206-356.

## 1. Definitions of Section 2 against the note and the report

| object | paper (tex line) | source | verdict |
|---|---|---|---|
| kernel, resistance r(x,y) = H(Fx,y) | l. 173-179 | note l. 42-46, l. 193 | same |
| R | l. 186-187: "the least resistance of a path from a state of $A$ to a state of $B$" | note l. 193: "$R(u\to v)$ the minimum total resistance of a path from $u$ to $v$"; PROOF_154 l. 40 | same; the paper states the set version, which the note uses without stating it |
| V(C,C') = R(C -> C') | l. 188-190 | note l. 193 | same |
| gamma | l. 191-194: least weight of a spanning in-tree on the cycles rooted at C, edge weights V | note l. 193; report l. 134-135 | same (minimum over in-trees on cycles, weights V) |
| noise-selected, S | l. 195-196 | note l. 193; report l. 135-136 | same |
| k_v, k* | l. 199-202: k_v = min_C [gamma(C) + R(C -> D_v)] - gamma_min, k* = max_v k_v | note l. 196 | same; R(C -> D_v) is over paths from a state of C (l. 186-187) |
| nu_v | l. 204 | note l. 81: "$\nu_c(f;\eps)=\E_{\pi_{f,\eps}}[n_c]$", n_c at l. 39 | same |
| rho | l. 205: (1-2 eps) log((1-eps)/eps) min_v nu_v | note l. 65 (lambda), l. 76 (definition as min over g), l. 83 (Lemma "one-bit neighbour": rho = lambda min_c nu_c) | same quantity. The paper takes as definition what the note proves as a lemma and says so ("by \cite{PeterleinNote} this is the rate ..."). |
| G_1, closed class | l. 230-232 | report l. 139-142 | same |

## 2. Table of the numbered statements

"Referee" = I followed every step of the paper's proof by hand, including the smallest ring sizes the statement
allows. "Source" lines are lines of the file named.

| no. | label (tex lines) | source | same statement? | proof: steps dropped / added / changed | cross-references | referee: every step justified? smallest n? |
|---|---|---|---|---|---|---|
| Prop. 2.1 | `prop:order` (209-213) | note l. 195-197 (statement), proof l. 198-200 | Yes for the three sentences taken over: order of pi(x); nu_v ~ a_v eps^(k_v), a_v > 0; rho ~ a eps^(k*) log(1/eps). Not taken over: "In particular $\rho\to\infty$ iff $k^*=0$ ..." (recorded in TRACE). "of exact order" replaces the note's ord (finding 8). That the statement is "Theorem 1" of the note: not checked (Section 0, item 1). | No proof in the paper (quoted). | none inside | Not refereed: the note's proof was read once, not checked. The paper uses the proposition only for interpretation (l. 215). |
| Lemma 2.2 | `lem:kzero` (218-227) | see Section 3 below | New as a statement. | Proof is the paper's own. | `\eqref{eq:kv}` correct | Yes, complete on its own (Section 3). All n >= 3. |
| Lemma 2.3 | `lem:edge` (234-245) | PROOF_154 Lemma 0, l. 48-54 | First two statements: same. "In particular" sentence: added (TRACE names two other sources; not read, item 1). | First part word for word. Added: "The last statement applies the first to $x$ and to $x+e_j$." | none | Yes. The added sentence follows from the first statement applied twice (a periodic state's orbit ends on its own cycle). All n >= 3. |
| Lemma 2.4 | `lem:sym` (247-254) | see Section 3 below | New as a statement; says more than the source sentences. | Proof is the paper's own. | none | Yes, complete, but one compressed sentence (finding 9). |
| Lemma 2.5 | `lem:reroot` (260-267) | report l. 173-176 | Same ("If the added edge has weight 1" = "If $V(B,N)=1$"). | Added: "and $B$ reaches $N$"; the reference to Lemma 2.3 for "weighs at least 1". Nothing dropped. | `lem:edge` correct | Yes. |
| Lemma 2.6 | `lem:closure` (269-274) | report l. 178-179 | Same. | Same. | `lem:reroot` correct | Yes. |
| Lemma 2.7 | `lem:inclosed` (276-290) | report l. 181-191 | Same. | Changed as recorded: "Some closed class $K$ is reachable from $C$" (finding B4). Added: "and adds an edge of weight $1$" in the second case. Nothing dropped. | `lem:reroot` (twice) correct | Yes. Checked: D is not a new root before the last step, so e* stays; weight falls by at least 1. Uses l. 231-232 ("from every node there is a directed path into some closed class"), stated without proof, standard. |
| Thm. 2.8 | `thm:A` (292-303) | report l. 193-199 | First two sentences same. Third sentence of the source moved after the proof, for a unique closed class only (l. 305-306), as recorded. | Added: "every in-tree has weight at least $m-1$ by Lemma 2.3" for the source's "the trivial lower bound". Nothing dropped. | `lem:inclosed`, `lem:closure`, `lem:edge` correct; l. 305 `lem:kzero` correct; l. 307 `lem:sym`, `sec:94`: target not checked (item 1) | Yes. m = 1 is covered (empty tree). |
| - | attribution (309-318) | report l. 163-171 | Same content, restricted to what the paper contains (no Lemma B). See finding 6. | - | `sec:related` not checked | - |
| Lemma 3.2 | `154:lem:local` (370-376) | PROOF_154 l. 58-61 | Same. | Changed: the proof no longer says what the eight values are compared with (finding 4). | none | Yes; I evaluated c + a(1+b) on the eight codes: 0,1,0,1,1,0,0,1, which is the table of l. 351-352 and the bits of 154. |
| Lemma 3.3 | `154:lem:rule90` (378-386) | l. 63-69 | Same (n even, n >= 4). | Same. | `154:lem:local` correct | Yes; n = 4 followed. |
| Lemma 3.4 | `154:lem:nilpotent` (388-401) | l. 71-80 | Same ((a) n = 2^k, k >= 2; (b) n even, not a power of two). | Same; 2^j -> 2^s, e_i -> e_j applied consistently. | `154:lem:rule90` correct | Yes. (a) s = k-1 >= 1. (b) t = 0 included; q >= 3 gives degree q-1 >= 2. |
| Lemma 3.5 | `154:lem:invariant` (407-417) | l. 84-91 | Same. | Same. | `154:lem:local` correct | Yes; n = 4 followed (odd cells 1, 3 are one orbit of j -> j-2). |
| Lemma 3.6 | `154:lem:collisions` (419-446) | l. 93-113 | Same (n >= 3). | Same; x' -> y applied at every place. | `154:lem:local`, `\eqref{154:eq:star}` (three times) correct | Yes. (i) to (iv) re-derived. n = 3: cells i-1, i, i+1 are distinct; Case A then contradicts itself (d_(i+2) = d_(i-1)), which the "n odd" argument covers. |
| Lemma 3.7 | `154:lem:periodic` (451-464) | l. 120-128 | Same without the count (2^(n/2) - 1)^2 + 1 (recorded). | Same. | `154:lem:invariant` (twice), `154:lem:collisions`, `154:lem:rule90`, `154:lem:nilpotent`(a) correct (source: Lemmas 4, 5, 2, 3a, 4) | Yes. |
| Lemma 3.8 | `154:lem:moves` (466-483) | l. 130-141, parts (a), (c) | Same; source (b) left out, source (c) is (b) (recorded). | (a) changed as recorded: the last sentence of Lemma 2.3 in place of two uses of Lemma 0. Same content. | `154:lem:periodic`, `lem:edge` correct | Yes. \one is in M and F(\one) = \one. |
| Thm. 3.9 | `154:thm:pow2` (485-538) | l. 145-183 | Same (n = 2^k, k >= 2), parts (a) to (f). | (b) reworded as recorded (from the statement of Lemma 2.3). (f): reference `lem:kzero` added. Nothing dropped. | (a) `154:lem:periodic`; (b) `lem:edge`, `154:lem:rule90`, `154:lem:nilpotent`(a); (c) `154:lem:periodic`, `154:lem:moves`(a), `154:lem:nilpotent`(a), `lem:edge`; (e) `lem:edge`, `154:lem:moves`(b); (f) `lem:kzero`, `154:lem:rule90`: all correct and the same as the source's Lemma 6; 0, 2, 3a; 6, 7(a), 3a, 0; 0, 7(c); 2 | Yes. mu = 1 followed (the range s < mu - 1 is empty). n = 4 followed for the codes of (f): e_0 = 1000, F(e_0) = 0101, e_0 + e_1 = 1100. See findings 2, 3. |
| Thm. 3.10 | `154:thm:other` (540-568) | l. 194-211 | Same range (n >= 3, not a power of two). "k_v = 0 for all eight codes" moved from the proof into the statement (recorded). | Odd n: "as in Lemma 7(a)" -> "by the last sentence of Lemma 2.3" (recorded; correct, because `154:lem:moves` assumes n even). Nothing dropped. | `154:lem:collisions`; `lem:edge`; `154:lem:periodic`; `154:lem:moves`(b); `lem:edge`; `154:lem:rule90`; `154:lem:nilpotent`(b); `lem:kzero`: all correct (source: 5; 7(a); 6; 7(c); 0; 2; 3b) | Yes. n = 3 (states 001, 011), n = 5 (00011, 01011), n = 6 followed. Odd n >= 3 and even n >= 6 exhaust the range. L \one_E = \zero checked. |
| Thm. 3.11 | `154:thm:main` (570-577) | l. 213-214, with l. 152 and l. 211 | Same; values of k_v added from the two theorems (recorded). | - | `154:thm:pow2`, `154:thm:other` correct | Yes: powers of two >= 4 and all other n >= 3 exhaust n >= 3. |

Figure 1 caption (l. 362-366): `154:lem:rule90`, `154:lem:nilpotent`(a), (b) point to the statements meant. I did
not look at the figure.

## 3. Lemmas 2.2 and 2.4: what they rest on, and whether the proofs stand alone

**Lemma 2.2 (`lem:kzero`).**

* First sentence ("$k_v=0$ iff $v$ is contained in a state of a noise-selected cycle"). The note has, in the proof
  of its theorem (l. 199): "Since a move of resistance $0$ from a cycle state stays on its cycle, $R(C\to x)=0$ iff
  $x\in C$; hence ... $k_c=0$ for every $c$ iff the noise-selected cycles jointly contain all eight codes." The
  note states the conclusion for all codes jointly, and the zero-resistance step for a single state x. The
  per-code sentence of the paper is not written in the note. It is the same argument with D_v in place of {x}.
  TRACE Part A ("First two sentences: note ...") is therefore exact for the second sentence only.
* Second sentence ("Hence $\kst=0$ iff ..."): the note's sentence quoted above, and the last sentence of the
  note's theorem (l. 196).
* Third clause ("$k_v\le1$ if some flip ..."): `PROOF_154.md` l. 179-181 ("both are reached from {0} with
  resistance 1, so k_c <= 1"), read. The two other sources TRACE names (`PROOF_43_142.md` l. 356-366,
  `PROOF_94.md` Corollary 2) were not read (Section 0, item 1).
* The paper's proof (l. 223-226) is complete on its own. Checked: k_v is the minimum over C of
  [gamma(C) - gamma_min] + R(C -> D_v), both terms non-negative integers, so it is 0 iff both vanish for one C; a
  path of resistance 0 stays on C; for the third clause the state y of C with Fy = x exists because F permutes C,
  and the bound gives k_v <= gamma(C) - gamma_min + 1 = 1 (the last equation is left to the reader).

**Lemma 2.4 (`lem:sym`).**

* Source sentences: report l. 212-213, "gamma is constant on a rotation orbit because F commutes with
  rotations", and l. 217-219, "Theorem A puts S inside A, and rotation symmetry gives S = A".
* The paper's statement says more than these: V(sigma C, sigma C') = V(C, C') and the invariance of G_1 are not in
  the source sentences. They are proved by the paper's own line (l. 252-253).
* The proof is complete: sigma is a bijection of the states that commutes with F, so it permutes the cycles;
  H(sigma u, sigma v) = H(u, v) gives r(sigma x, sigma y) = r(x, y); hence paths, V, in-trees and gamma are
  carried over, and equality (not only an inequality) holds because sigma is invertible. The last point is not
  said. See finding 9 for the wording.

## 4. Findings

No false statement (class 1) was found. No gap in a proof (class 2) was found. No hypothesis or range not met
(class 3) was found; the smallest ring sizes (n = 3 for Lemma 3.6 and Theorem 3.10, n = 4 for Lemmas 3.3 to 3.8
and Theorem 3.9, n = 6 for the even case of Theorem 3.10) are covered by the arguments as written. All findings
are of class 4 (unclear) or 5 (cosmetic).

1. **Section 2.1 and 2.3, l. 165 and l. 205, 212. Class 5.** The letter rho has two meanings in Section 2:
   "$\rho$ the reflection, $(\rho x)_i=x_{-i}$" (l. 164-165) and "$\rho(\eps)=(1-2\eps)\log\frac{1-\eps}{\eps}\,
   \min_v\nu_v(\eps)$" (l. 205; also l. 212). Not recorded in TRACE. Correction: another letter for one of them,
   or one sentence at l. 205 that rho(eps) is not the reflection. (Uses of rho elsewhere: not checked.)

2. **Sentence before Lemma 2.2, l. 215-216. Class 4.** "the following consequence of the definition is all that
   is needed to evaluate them." This is not so in Theorem 3.9(f): the bound k_101 <= 1 (l. 532-535) uses the state
   F(e_0) = e_(-1) + e_1, "reached from $\{\zero\}$ with resistance $1$". F(e_0) is not a flip of a state of a
   selected cycle, so the third clause of Lemma 2.2 does not give it; the proof uses definition (1) directly, and
   correctly. The lower bound k_v >= 1 (l. 531-532) is also argued from the definition. Correction: replace by
   "the following consequences of the definition are used throughout; where they do not suffice, (1) is used
   directly", or leave the sentence out. No change of mathematics.

3. **`154:thm:pow2`(d) and its proof, l. 492 and l. 516. Class 5.** "$\{\zero\}$ is the only closed class of
   $\Gone$" and "every strongly connected component other than $\{\zero\}$". A closed class is a set of cycles
   (l. 230-231), so the class is {{0}}; part (e), l. 493, writes "$\Sel=\{\{\zero\}\}$". The source has the same
   (PROOF_154 l. 150, l. 168). TRACE Part D item 2 records this slip for S only. Correction: "$\{\{\zero\}\}$ is
   the only closed class", "other than $\{\{\zero\}\}$".

4. **`154:lem:local`, proof, l. 374-375. Class 5.** The proof lists the eight values of the right-hand side and
   stops. The source ends "which are the bits 0..7 of 154" (PROOF_154 l. 60-61). The comparison with the table of
   l. 351-352 is left unsaid. Correction: add "; these are the values of $f$".

5. **`lem:inclosed`, l. 281, and `154:thm:other`, l. 557. Class 5.** "$C=C_0\to C_1\to\dots\to C_k$" and "a cycle
   $C_1\subseteq E\cup O$" use the names that l. 184 gives to the list of all cycles ("The cycles are
   $C_1,\dots,C_m$"). In `lem:inclosed` the collision comes from the renaming D_0..D_k -> C_0..C_k that TRACE
   records. No step is affected. Correction: other names (for instance $B_0,\dots,B_k$; $C'$ at l. 557), or drop
   the enumeration at l. 184, which my part does not use.

6. **Opening of Section 2.5, l. 257-258, against the attribution, l. 310 and l. 317-318. Class 4.** "It restates
   known results" is said of the whole theorem. The attribution says "the first sentence of
   Theorem~\ref{thm:A} restate[s]" and "The value $\gmin=m-1$ was not found in the sources read", as the source
   does (report l. 163-171). Correction at l. 258: "Its first sentence restates known results". (The same
   wording at l. 136 of the introduction is outside my part.)

7. **Sentence after Lemma 3.6, l. 448-449. Class 4, provisional.** "according to its abstract, in
   \cite{NobeYura2004}, which was not read". The sub-session's wording was "known here from its abstract and a
   search excerpt only" (trace_154.md, section 3 item 2 and section 4 item 2), and TRACE Part D item 3 records
   that `literature_ring_size.md` is inconsistent: at one place the abstract is the source, at another "the
   abstract speaks of 16 reversible rules, Proposition 1 on rule 154 seen in a search excerpt only". The paper's
   wording is then stronger than the record. I did not read `literature_ring_size.md` (Section 0, item 1) nor any
   cited text; this rests on the two trace files only. Correction: "according to its abstract and a search
   excerpt". The same record says of Fedoriaka: computation for N <= 20 with explicit constructions, "not a proof
   for all odd N"; "stated in" (l. 448) is compatible with that, "is known" is carried by Bhattacharjee and Das.

8. **`prop:order`, l. 210-212. Class 5.** "of exact order $\eps^{\,o(x)}$" is not defined in the paper. The note
   defines "$\operatorname{ord}g$ for the exponent of the leading power of $\eps$ in $g(\eps)$" (l. 193). For the
   rational function pi_eps(x) the two agree. Correction: a clause "(that is, $\pi_\eps(x)/\eps^{o(x)}$ has a
   positive limit)". The constant a in "$\rho(\eps)\sim a\,\eps^{\kst}\log\frac1\eps$" has no "a > 0" in the note
   either; the quote is faithful.

9. **`lem:sym`, proof, l. 252-253. Class 5.** One sentence carries four objects under one verb: "$\sigma$ maps
   cycles to cycles, $r(\sigma x,\sigma y)=H(\sigma Fx,\sigma y)=r(x,y)$, paths to paths ..., and in-trees to
   in-trees". The middle member is an equation, not an object that sigma maps. Correction: "so $\sigma$ permutes
   the cycles and $r(\sigma x,\sigma y)=H(\sigma Fx,\sigma y)=r(x,y)$; hence $\sigma$ maps paths to paths of the
   same resistance and in-trees to in-trees of the same weight, and so does $\sigma^{-1}$."

10. **TRACE.md, not the paper. Class 5.** (a) Part A, rows Theorem 3.9 and 3.10: "'(Proposition prop:order)' added
    as the reference", while the tex has `lem:kzero` at l. 530 and l. 567; Part C item 2 explains the change, the
    rows were not updated. (b) Part A, row Lemma 2.2: "First two sentences: note"; the per-code first sentence is
    not in the note (Section 3 above).

## 5. What I did not check

* Everything under Section 0, item 1: theorem numbers in the PDF and in the note ("Theorem 1"); uses of rho,
  `lem:sym`, `lem:kzero`, `prop:order` outside tex l. 158-577; the sources of the third clause of Lemma 2.2 other
  than PROOF_154; the two sources TRACE names for the last sentence of Lemma 2.3; `literature_ring_size.md`.
* The targets of three references that point outside my part: `\ref{sec:related}` at l. 195 and l. 317, and
  `\ref{sec:94}` with `\ref{lem:sym}` at l. 307 (whether Section 3.3 uses Lemma 2.4 as the sentence says). Every
  other `\ref` / `\eqref` in tex l. 158-318 and l. 349-577 points to a statement inside my part and was compared
  with what the source cites at that step (table of Section 2).
* The proof of the note's theorem behind Proposition 2.1 (read, not refereed).
* Any cited literature (Martin, Odlyzko and Wolfram; Bhattacharjee and Das; Fedoriaka; Nobe and Yura; Ellison;
  Samuelson; Nöldeke and Samuelson). The sentences at l. 403-405 and l. 448-449 were compared with the repository's
  records only (report l. 113-115, l. 252-254; trace_154.md).
* The verification documents quoted in the "verification" column of TRACE Part A.
* PROOF_154.md from l. 261 on (tests, rules 122 and 26); Figure 1 itself; `numbers.tex`, `table_kstar.tex`.
* No statement was tested by computation. `paper/REFEREE_NOTES.md` and all scripts were not opened.
