# Trace file, track "rule 26" (fragment `sec_26.tex`, `\section{Rule 26}\label{sec:26}`)

Sources, read on branch `paper-ring-size` (HEAD d6c6299), nothing changed there:

* **S** = `proofs_94_26/PROOF_26.md` (496 lines; read in full). Line numbers below are lines of this file.
* **P154** = `verify_ring_size/part2_154/PROOF_154.md` (read: L32-82 Section 1 and Lemmas 0 to 3; L150-175 Theorem 1
  (b) to (e); L443-452 and L490-499 Lemma Q1 and the rule-26 remarks. Not read: the rest).
* **V** = `VERIFICATION_94_26.md` (read: L1-130, L150-266. Not read: L131-149, the rule-94 test table, and L267-293,
  file list and reproduction commands).
* Literature: `literature_ring_size.md`, `literature_addendum.md`: searched by keyword (rule 26, rule 90, Martin,
  nilpotent, R154, parity class, Packard, Aguiar) and the passages found were read (L10-48, L280-286, L405-416 of the
  first; L140-165, L205-215, L262-300 of the second). The two files were NOT read in full.
  `report_ring_size.md`: only L107-116, L404-422, L576-580 (Proposition R154, Proposition V26, the attribution lines).
* Data file used for the `\DATA` items: `proofs_94_26/out/g1_26.jsonl` (opened read-only; field names checked).

Length of the fragment in the harness PDF: **2.84 pages** (2 full pages + 583 pt of 697 pt), i.e. 0.59 page over the
budget of 2.25. Parts (i) and (ii) (definitions, Lemmas, Theorem with proof) take about 2.2 pages by themselves.

## 1. Statements of the fragment

| paper label | source (S = PROOF_26.md) | tag in the source | independent verification (V = VERIFICATION_94_26.md) | changes of wording and notation |
|---|---|---|---|---|
| `26:def` (definition) | S section 1, L54-68 (moving frame L54-56, c L57-58, groups and sources L59-61, domain states L62-67, carrier words L68); "contained in E ∪ O" L48-49 | none (definitions) | V L89-90: "the definitions of c, groups, sources, domain states, carrier words. Correct." | c(x) -> chi(x). Added: the name "domain cycle" (a cycle that consists of domain states); the source uses the term (L86, L94, L184) without a definition; it rests on L129-131. Added: "a cycle contains a code if one of its states does" (the source's usage, e.g. L74, L95). "distance d = s' - s" written into the definition (source: L63-64). |
| `26:lem:frame` | S Lemma 1, statement L102-106, proof L108-109 | [proved] | V L91 (hand check, "all eight codes": correct); test M1, V L156 (n = 3..20, 0 violations). No finding. | u(j) -> u_j; U(u)(j) -> (Uu)_j. Range: the source has "every n >= 3"; the fragment states it inside the section's standing assumption (n even, n >= 4), i.e. for fewer n. The word "attacker" is introduced in the statement (the source uses it from L136 on without introducing it). |
| `26:lem:chi` | S Lemma 2, statement L111-112, proof L114-122; "constant on every cycle": S Theorem 1, L72, proof L209 (also row L14) | [proved] | V L91 ("the sets N(p), order and parity of the ones of u'; the flip remark": correct); tests M2, M2f, V L157-158 (even n = 4..20, 0 violations). No finding. | c -> chi; u'(p) -> u'_p. The sentence "chi is constant on every cycle" is moved from Theorem 1 of the source into this lemma. |
| `26:lem:domain` | S Lemma 3, statement L124-131, proof L133-145 | [proved] | V L91-92 ("(a), (b) (all cell types of a domain, with d >= 3 used where stated) and (c) (apart from C1)": correct). Finding C1 (V L55): the first sentence of (c) was false for F in the verified version; corrected in S (L129-131 now has the form the verification proposes; checked). Tests M3a, M3b, M3c, M3F, V L159-162 (even n = 4..18, 0 violations). | free-cell values c_k -> z_k (the letter c is not free in the paper); GF(2)^((d-1)/2) -> "{0,1}^((d-1)/2) over the field with two elements" (no \mathbb); "contains no 111" -> "does not contain the code 111"; "Flipping a free cell" -> "The flip of a free cell". |
| `26:lem:singleton` | S Lemma 5, statement L159-160, proof L162-164 | [proved] | V L93 (correct); test M5, V L163 (even n = 4..18, 0 violations). No finding. | c -> chi. |
| `26:lem:parity` | S Lemma 6, statement L166-169, proof L171-173, which refers to P154 Lemma 3 (P154 L71-75); the step F(E) in O is written out in P154 Lemma 2, L63-69 | [proved] (S); P154 Lemmas 2, 3: [proved] | V L93 (Lemma 6: correct); V L104: "Cited results of P154 used by C26 (Lemma 3, Lemma Q1, the conventions of Section 1): correct."; test M6, V L165. No finding. An independent verification of P154 as a whole was not looked up by this track. | "x in E or O" -> "x in E ∪ O"; 0 -> \zero. The algebraic step, which S gives in one line with "(as in P154, Lemma 3)", is written with the wording of P154 L74-75. See section 4 (credit) and section 8, Lemma parity, steps 2 to 4. |
| `26:thm:main` (a) | S Theorem 2, statement L77-79 (and row L16), proof L214-222 | [proved] | V L95 ("Theorem 2 (both cases, the induction)": correct); tests T2, T2ch, V L170, L173. No finding. | Statement restricted to what the task names (n = 2^k: every cycle other than {0} has a directed path to {0}). The source's statement for every even n >= 4 (path to a cycle contained in E ∪ O) is kept inside the proof, which is written for every even n as in the source. Not stated: the clause of the source on the number of drops of c ("c drops at most c(C)/2 times, ...", L78-79). c -> chi. |
| `26:thm:main` (b) | S Theorem 3(a), L82, proof L224 | [proved] ("Theorem A is not needed", L17) | V L95-96 (Theorem 3 (a) to (d): correct); test T3ab, V L171; potentials from the definitions at n = 4, 8 for every root (V L217-220) and at n = 16 for 16 of 552 roots (V L222); V L256: not checked for the other 536 roots at n = 16. No finding. | re-lettered: source 3(a) -> paper (b). |
| `26:thm:main` (c) | S Theorem 3(b), L83, proof L225 | [proved] | as (b) | re-lettered: source 3(b) -> paper (c). |
| `26:thm:main` (d) | S Theorem 3(c), L84-85, proof L226-232 | [proved] | as (b); V L95-96 names "the in-tree of weight m in (c)" as checked | re-lettered: source 3(c) -> paper (d); wording of the statement as in the source (S -> \Sel, G1 -> \Gone, 0 -> \zero). Theorem 3(d) of the source is NOT part of the theorem; it is quoted after Proposition `26:prop:indices` as "Theorem 3(d) of that document". |
| `26:prop:indices` (a), (b), (c) | S Theorem 4, statement L88-91 (rows L18-20), proof L245-267 (not reproduced) | [proved] | V L96-97 ("Theorem 4 (a), (b), (c) (the sources 0, 5, 8, ..., n - 3 of 10100(100)^q, q odd)": correct); test T34ch, V L174; k_c from the definitions at n = 8 and n = 16 (V L212, L222). No finding. | codes c = 0..7 -> code words; k_c -> k_v, k_7 -> k_{111}; k_0 -> k_{000}; "c = 1, ..., 6" -> the six words. |
| `26:prop:even` (first four sentences) | S Theorem 5, statement L93-95, proof L276-295 (not reproduced) | [proved] | V L97-98 ("Theorem 5 (reduction to two domains, L >= 2^(e+1) + 1, y in the image of (1 + S)^(2^e))": correct); tests T5, T5ch, V L172, L175. No finding. | "the codes 0, ..., 6" -> "every code other than 111 occurs in a state of a cycle of K". |
| `26:prop:even` (sentence "Consequently ...") | S Corollary 5, statement L97-98, proof L297-298 | [proved, given Theorem A] | V L98 (Corollary 5: correct); potentials from the definitions, n = 6..14, agree (V L28, L211-215). Theorem A itself: "used as given", not re-proved by V (V L106-108, L257). | k_c = 0 for c = 0..6 -> k_v = 0 for every code v != 111; "Theorem A" -> `thm:A`; the step "k_c = 0 iff a state of a selected cycle contains c" -> `prop:order`. |

Not stated in the fragment as numbered statements: S Theorem 1 as a whole (only its parts "chi constant on cycles", "F
permutes the domain states", "no domain state contains 111" are in the lemmas; its classification "every other
periodic state has 111 on its cycle" is quoted once, with attribution, after `26:prop:indices`); S Lemmas 4, 7, 8, 9;
S Theorem 3(d).

## 2. GAPs

None marked. No `\GAP` in the fragment. Three places where the wording is not a sentence-by-sentence image of S are
listed in section 8 with their line ranges (Lemma parity steps 2 to 4; Theorem (b) last clause; Theorem (d),
parenthesis) and in the notes for the editor, so that the editor can decide whether to treat any of them as a GAP.

## 3. Errors found in sources

None. No `\SOURCEERR` in the fragment. Checked: the three findings of V that concern PROOF_26.md are applied in S:
C1 (V L55) -> S L129-131; C3 (V L57) -> S L72-75; C4 (V L58) -> S L22.

Observations that are not errors (nothing was corrected):

* S L65-67: "any choice of an even number of sources ..." formally includes zero sources; copied as it stands.
* S L171-173 (proof of Lemma 6) does not write out why F maps E into O; the statement (L167) asserts it and P154
  L67-69 gives the reason for rule 154. See section 8.
* S L129-130: "hence F = sigma^(-1) U permutes the set of all domain states" stands in the statement; the proof
  (L142-145) has no separate sentence for the "hence". Copied as it stands. The main theorem does not use it.
* S L316: "(Lemma 3(c), Lemma 6 for n = 2^k)"; the fragment restricts that sentence to n = 2^k.
* P154 L445: Lemma Q1 carries the tag [proved (computer-assisted ...)] together with a derivation by hand (L446-447);
  V L103 says it was re-derived by hand. The fragment gives the derivation by hand.

## 4. Credits given

| place | sentence | key | repo lines that state the attribution |
|---|---|---|---|
| after the proof of `26:lem:parity` | "That rule 90 sends every state of a ring of 2^j cells to 0 is Lemma 3.5 of [MOW]; Section 5 there makes the same reduction to rule 90 for rule 18." | `MartinOdlyzkoWolfram1984` | `literature_ring_size.md` L39-40: "**Rule 90 at n = 2^k (A25).** Martin, Odlyzko and Wolfram (1984), Lemma 3.5 (p. 230)"; L41-43: "Martin, Odlyzko and Wolfram, Section 5 (p. 247): the same reduction for rule 18". `report_ring_size.md` L113-114: "Martin, Odlyzko and Wolfram (1984), Lemma 3.5 (p. 230): for N = 2^j every configuration evolves to the null configuration"; L416-420: "The algebraic step is in Martin, Odlyzko and Wolfram (1984): Lemma 3.5 (p. 230) gives the nilpotency of rule 90 at n = 2^j ... Section 5 of Martin, Odlyzko and Wolfram (the same reduction for rule 18)". S L341-342: "The reduction of rule 26 to rule 90 on one parity class is the report's Proposition R154, with the sources named there." |

How the reference was seen: not by me (no network, and I opened no copy). According to `literature_ring_size.md`
L15-16 it was "read in full (author copy at content.wolfram.com)" by the verification of the ring-size study; the
study session itself had not read it (L210, L234).

No other credit sentence. Not cited, although S mentions them: Li and Packard (S L340: "search excerpt only"; not in
the two literature files; the house rule allows only what a session has read), Aguiar and Severino (S L337-339:
abstract only; no key in the list). Mentions of rule 26 in the literature files that have no key in the list and are
not used: OEIS A070886, A334504, A334507 (`literature_ring_size.md` L41-45); Nordahl 1989, rule 26 among the rules
"known to be capable of simulating rule 90" (`literature_addendum.md` L147-155); the numerical remark on cycle
lengths 4k of rules 26 and 154 (`literature_addendum.md` L212). S L342-343: "No source was found for the quantity c,
for the domain states, or for the path to {0}; the search was short, and no claim of novelty is made".

Theorem A and Proposition `prop:order` are cited by label only (`26:prop:even`); their credits belong to Section 2.

## 5. General facts used beyond the shared statements of Section 2

1. The rotation sigma commutes with F, hence U = sigma F commutes with F (S L54; needed for "periodic under F iff
   periodic under U").
2. A bijection of a finite set has only periodic points (S L143-144).
3. Over the field with two elements, identity + nilpotent linear map is invertible (S L142-143).
4. For commuting linear maps A, B over the field with two elements, (A + B)^(2^j) = A^(2^j) + B^(2^j) (S L172,
   P154 L74-75).
5. Definitions of Section 2 used directly, not through a cited statement: closed class (Theorem (c)); spanning in-tree
   and potential (Theorem (d)); "the orbit of x ends on C".
6. `lem:edge` is used in both forms (V = 1 iff ...; the "in particular" on two periodic states).

## 6. \DATA items (all from `proofs_94_26/out/g1_26.jsonl`, one JSON object per ring size)

| # | what | row, fields | tag in S |
|---|---|---|---|
| D1 | n = 4: the only cycle is {0}; the eight k_v and k* | row n = 4: `cycles`, `k_c_from_the_definition` (k* = max) | [computed for n = 4], S L21, L271-272 |
| D2 | n = 16: k_{111} and k*; no cycle that contains 111 is reachable in G1 from a cycle C_1 with V({0}, C_1) = 2 | row n = 16: `k_c_from_the_definition`, `cycles_with_111_reachable_from_T2`, `gamma_by_kind` | [computed for n = 16], S L21, L269-271 |
| D3 | n = 16: a cycle that contains 111 and does not pass through a carrier word | row n = 16: `cycles_by_kind` (entry `with_111`), `cycles_with_111_through_a_carrier_word` | computed (Table 2), S L313-314 |
| D4 | n = 22: the values of chi on the cycles that contain 111 (one is below n/3) | row n = 22: `c_of_cycles_with_111` | computed (Table 2), S L314; V test S7n22, L176 |

Verification of these data by V: n = 4 and n = 16 recomputed (V L219, L222; at n = 16 gamma for 16 of 552 roots and
k_c "exact by the bound"); the n = 22 claim checked (V L120, L176); the rest of the row n = 22 was not checked by V
(V L254). No number from these files is typed in the fragment; the ring sizes 4, 16, 22, 64, 256 appear as
parameters.

Left out of the fragment (computed in S, not needed): which even n <= 22 have a cycle with 111 in K (S L300-301,
Table 2); the numbers of cycles by kind; the chain tables.

## 7. Which cycles of rule 26 the source leaves undescribed (for the section on open cases)

* The source describes (Theorem 1, S L72-75; proof L209-212), for every even n >= 4, three kinds of periodic states:
  (i) states of E or O that are periodic under rule 90 (for n = 2^k: the zero state only, Lemma 6, L166-169);
  (ii) the domain states, an explicit set permuted by F (Lemma 3, L124-131);
  (iii) "Every other periodic state lies in M, is not a domain state, and its cycle contains the block 111".
* **Kind (iii) is not described**: S L36-37 "The cycles that contain 111 are not described; the path to {0} does not
  need their description"; S L22 and L308 "[attempted (gap: no description of the cycles that contain 111 ...)]".
  For n = 2^k every cycle other than {0} is a domain cycle or contains 111 (S L193-194), so the undescribed cycles are
  exactly the cycles other than {0} that are not domain cycles.
* What is proved about them (S L315-318): chi is constant on them; every state of such a cycle lies in M and is not a
  domain state, contains a pattern of Lemma 4 (adjacent ones whose preceding one is at odd distance, Lemma 3(a)) and
  has a singleton group (Lemma 5); in one step 111 arises only from 10011 (P154 Lemma Q1, L445-449). Not shown
  (S L318): "how an occurrence of 111 is related to patterns at earlier times".
* One explicit family inside kind (iii): the carrier words (S L68; Lemma 7, L175-182: F^2 w = sigma w, period dividing
  2n, every second state contains 111 if there is a block 11100). They are not all of kind (iii): S L313-314 (computed:
  at n = 16 one of the three cycles with 111 does not pass through a carrier word; at n = 22 a cycle with 111 has
  c = 6 < n/3), data fields D3, D4 above.
* Consequences left open, with the source's own wording of the gap:
  - n = 2^k, k even, k >= 6: whether a cycle with 111 is reachable in G1 from a cycle at resistance 2 from {0}, i.e.
    whether k_{111} (= k*) is 1 or 2 (S L22, L308-315). The conditional statement of S L311-312 (a bound
    chi >= (n + 8)/3 for every cycle with 111 at n = 4^j would give k* = 2) is not proved in S as a lemma; V L99-101
    says it is correct and adds that domain cycles have c <= (n - 4)/3 there. The formula c = (n + 4p)/3 for carrier
    words (S L312) is stated in S without proof; V L101, L246: confirmed by computation for even n = 6..30.
  - even n not a power of two: which of these n have a cycle with 111 inside K, i.e. where k* = 0 (S L24: "[computed
    for even n <= 22]", L300-301); proved is only the equivalence of Corollary 5.
  - odd n: not treated (S L25, L319-320: "c is not defined on an odd ring"; "For odd n only Proposition V26 of the
    report is known (0 can be left by one flip)").
  - G1 distance to {0}: the number of G1 edges between two drops of c is not bounded (S L321-322).

## 8. Second pass: source line ranges, step by step (S = PROOF_26.md unless marked)

Opening paragraph (fragment L3-6): rule table S L41-42; rule 90 differs on 110 only S L42, rule 90 as x_(i-1) +
x_(i+1) S L167; "contained in E ∪ O" S L48.

**`26:def`** (fragment L8-26): moving frame S L54-56; chi S L57-58; groups, sources, singleton group S L59-61; domain
states, domains, free cells, converse S L62-67; carrier words S L68; "domain cycle": term of S L86, L94, L184, resting
on L129-131.

**`26:lem:frame`** (L28-38): statement S L102-106; proof: (Uu)_j = (Fu)_(j-1) S L108; the two cases of f S L108-109.

**`26:lem:chi`** (L40-56):
1. chi invariant under rotation, chi(Fx) = chi(Ux), u, u': S L114.
2. the sets N(p); u'_(p+2) = 1: S L114-115.
3. every one of u' lies in some N(p): S L115-117.
4. if p + 2 in N(p): no one of u on p + 1, p + 2, and u'_(p+1) = 0: S L117-118.
5. the ones of u' in cyclic order; 0, 1 or 2 cells of the parity of p: S L118-119.
6. deleting and doubling letters; neither increases the number of cyclic changes: S L119-121.
7. chi constant on a cycle: S L209 (and L72).
8. flips: S L121-122.

**`26:lem:domain`** (L58-89):
(a) S L133-135 (three sentences, same order).
(b) cells s + 2k: S L136-137; cells s + 2k + 1: S L137-138; cell s + 1: S L138-139; source s' (d >= 3): S L139-140;
conclusion: S L140-141.
(c) affine map, invertible, shift nilpotent: S L142-143; bijection of the finite set, U-periodic hence F-periodic:
S L143-144; adjacent ones only as free cell + next source, next cell 0: S L144-145; last statement by definition:
S L145. The clause "hence F permutes the set of all domain states (it moves every source one cell to the left)" is
in the statement only, as in S L129-130.

**`26:lem:singleton`** (L91-100): (a) S L162-163; (b) S L163-164.

**`26:lem:parity`** (L102-114):
1. no two adjacent ones, 110 does not occur, Fx = Lx, L = sigma + sigma^(-1): S L171-172 (with L42).
2. "For x in E and even i, x_(i-1) = x_(i+1) = 0, so (Fx)_i = 0 and Fx in O; the same with the parities exchanged":
   asserted in the statement S L167; the sentence itself is P154 L67-69 (proof of Lemma 2 there, written for rule 154,
   where the formula is the same once Fx = Lx).
3. "Hence F^t x = L^t x for all t >= 0": P154 L65 and L69 ("by induction on t"), L74.
4. L^(2^j) = sigma^(2^j) + sigma^(-2^j) and L^(n/2) = sigma^(-n/2)(sigma^n + 1) = 0: P154 L74-75; S L172 has the
   result "L^(n/2) = sigma^(n/2) + sigma^(-n/2) = 0 for n/2 a power of two (as in P154, Lemma 3)".
5. a periodic state other than 0 cannot lie in E or O: S L172-173.
6. the consequences in the statement (every cycle other than {0} lies in M; a single flip of 0 returns to 0):
   S L167-169.
The paper label `154:lem:nilpotent` is NOT cited. S does not reduce to the P154 lemma by a bare citation: it gives
the computation in one line and adds "(as in P154, Lemma 3)". The fragment therefore proves the statement for rule 26
with the two lines of P154 L74-75.

**`26:thm:main`** (L118-160):
(a) "C not contained in E ∪ O, i.e. chi(C) >= 2": S L48-49, L77, L214, with L209. Induction on chi(C): S L214.
Case 1: S L215-216 (edge by `lem:edge` = S L51-52, P154 L48-54). Case 2: S L217-220 ("joined by an edge": S L44-45).
"In both cases ...", induction, n = 2^k: S L221-222.
(b) S L224 (with S L51-52). The closing clause "so it ends on no other cycle" is the statement S L82 in the words of
P154 L158.
(c) S L225 (both clauses; nothing added).
(d) m - 1 edges of weight at least 1: S L226. In-tree of weight m - 1 rooted at {0} from the edges of (a): S L226-227;
the parenthesis "(give every cycle other than {0} its first edge on a shortest path to {0} in G1)" is the choice that
S makes at L230-231 for the second tree and that P154 L170-171 makes for this tree; S L226-227 itself only says "The
edges of Theorem 2 towards {0} contain an in-tree". gamma(C) >= m > gamma({0}), S = {{0}}: S L227-228. "If
gamma(C) = m ...": S L228-229. Converse (path D_0, ..., D_l; {0} none of the D_i; the edges; in-tree of weight m):
S L229-232.

**`26:prop:indices`** (L162-176): statement S L88-91. Proof not reproduced (S L245-267: (a) L251-254, (b) L256-260,
(c) L262-267). It would need, beyond the fragment: Lemma 4 (S L147-157), Lemma 7 (L175-182), Lemma 8 (L184-195),
Theorem 3(d) (L86, L233-241), i.e. about 40 further lines of the source in addition to the 23 lines of the proof.
"for n >= 8 every domain cycle has gamma = m": S L86. "every cycle other than {0} is a domain cycle or contains 111":
S L193-194 (Theorem 1, L72-75).

**Paragraph "Computed values and the open case"** (L178-202): "For k even nothing beyond (a), (b) is proved": S L269.
D1: S L271-272, L21. D2: S L269-271, L21. "For even k >= 6 ... not determined": S L22, L31-32, L315. "k* = 2 iff no
cycle that contains 111 is reachable ...": S L308-309 (with Theorem 3(c), L84-85). "The gap is ...": S L22, L308.
"What is proved about such a cycle": S L315-318. "111 arises only from 10011" and its reason: P154 L445-447.
"It is not shown how ...": S L318. "An edge of G1 raises chi by at most 2 (Lemma 2)": S L310-311. Conditional
statement with (n + 8)/3 at n = 4^j: S L311-312. Carrier words satisfy the bound, are not the only cycles: S L312-313.
D3: S L313-314. D4: S L314. "So a lower bound ... is not available": S L315.

**`26:prop:even`** (L204-213): statement S L93-95 and L97-98. "Theorem 5 ... proof not reproduced": S L276-295.
"The last sentence follows by Theorem A and Proposition order": S L297-298. "Odd n is not treated ...": S L319
(also L25). The source's sentence on Proposition V26 (S L320) is not in the fragment.

## 9. Notation changes against the source (complete list)

c(x) -> \chi(x); code numbers 0..7 -> code words (\code{...}); k_c, k_7, k_0 -> k_v, k_{\code{111}}, k_{\code{000}};
D_c not used; u(j) -> u_j; U(u) -> Uu; free-cell values c_k -> z_k; 0 -> \zero; G1 -> \Gone; S -> \Sel;
gamma_min -> \gmin; "E or O" (for states) -> "E ∪ O"; GF(2) -> "the field with two elements"; "T2" (cycles at
resistance 2 from {0}) -> "a cycle C_1 with V({0}, C_1) = 2"; "cycle with 111" -> "cycle that contains 111";
Theorem 2 + Theorem 3(a), (b), (c) of S -> Theorem `26:thm:main` (a), (b), (c), (d); Theorem 4 -> Proposition
`26:prop:indices`; Theorem 5 + Corollary 5 -> Proposition `26:prop:even`; Lemmas 1, 2, 3, 5, 6 of S -> `26:lem:frame`,
`26:lem:chi`, `26:lem:domain`, `26:lem:singleton`, `26:lem:parity`. "site" does not occur (S says "cell").
