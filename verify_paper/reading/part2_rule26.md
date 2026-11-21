# Part 2, rule 26: Section 5 and Appendix B of `paper/ring_size_paper.tex` against `proofs_94_26/PROOF_26.md`

Reader: Claude. Date: 20 November 2026. Repository state read: branch `paper-ring-size`, HEAD c926271. Nothing in the
repository was changed (`git status --short` after the reading shows only `PR_BODY.md` and `PR_DRAFT.md` as untracked;
neither was written by me).

## What was read, and how

* Paper: tex lines 1305-1513 (Section 5) and 2047-2226 (Appendix B), every line. Also, because Section 5 depends on
  them: tex 63-79 (abstract), 109-156 (results, status), 158-307 (Section 2: `lem:kzero`, `lem:edge`, `thm:A` with
  their proofs), 349-401 (parity classes, Lemmas 3.3, 3.4), 1249-1297 (mechanism table, row 26), 1632-1638 (open
  cases, rule 26), `numbers.tex` (all 43 lines), `table_kstar.tex` (row 26).
* Source: `proofs_94_26/PROOF_26.md`, all 496 lines (S below). `verify_ring_size/part2_154/PROOF_154.md` lines 30-89
  (P154: Section 1, Lemmas 0 to 4).
* Trace: `paper/trace/trace_26.md` (all 230 lines); `paper/TRACE.md` lines 1-36, rows 93-108 of Part A (Definition 5.1
  to Lemma B.7), Part C and Part D (lines 206-342).
* Comparison: statement and proof of every numbered item were compared sentence by sentence with the source passage
  that TRACE names; the line ranges that TRACE gives for S were checked against S for every row. Every proof was then
  read as a referee, with the small cases written out by hand (n = 4, 6, 8 and n = 10, 12 where they apply).
* One Python check (single process, 0.1 s, even n = 4..12, own code from the definitions; listed at the end). It is
  not a proof; it only confirms the smallest ring sizes.
* Statement numbers (5.1 to 5.9, B.1 to B.7) are those of TRACE.md Part A. The PDF was not opened; the numbers agree
  with the order of the environments in the tex.
* Not opened: `paper/REFEREE_NOTES.md`; any script or script output of the repository.
* Deviations from the task: none in scope (all named passages were read in full on both sides). One shell command
  (a grep for macro names and labels) was not executed by the platform; the same lines were read with the file
  reader instead.

## Result in one paragraph

No false statement was found, and no cited lemma is used outside its range. Every statement of Section 5 and
Appendix B has the hypotheses, ranges of n and quantifiers of its source, apart from the changes that TRACE records.
Every renumbered citation points to the statement that contains what is used. Reading the proofs as a referee, every
step is justified except two one-line steps that are not written (findings 1 and 2; both are also missing in the
source, both are true, and I give the missing sentence). The remaining findings are points of clarity and of form.
The abstract-level claims for rule 26 follow from Theorem 5.7(d) (n = 2^k >= 4, i.e. k >= 2: Sel = {{0}}) and
Proposition 5.8(b), (c) (n = 2^k >= 8, i.e. k >= 3: k* is 1 or 2; k odd: k* = 1) as stated.

## (a) Table of statements

"Confirmed" in the last column means: I read the proof and found every step justified by what stands before it.
"n = ... by hand" names the small cases I wrote out. The Python check is named separately.

| no. | label | source | same statement? | proof: steps dropped / added / changed | cross-references correct? | proof read as a referee; smallest n |
|---|---|---|---|---|---|---|
| Def. 5.1 | `26:def` | S L54-68, L48-49 | Yes. Added: the name "domain cycle", "a cycle contains a code" (TRACE records both). "even number of sources" includes zero (finding 6). | no proof; the claims inside (U commutes with F; chi even; chi = 0 iff x in E or O; the converse on sources) were checked by hand | `sec:154` for E, O, M: correct (defined tex 353-355) | Confirmed. n = 4: no domain state exists (odd distances >= 3 cannot sum to 4); consistent with S Table 1. |
| Lemma 5.2 | `26:lem:frame` | S Lemma 1, L102-109 | Yes; range narrower (source n >= 3, paper even n >= 4; TRACE records it) | none | none needed | Confirmed (all eight codes evaluated by hand). n = 4: cells j-2 and j+2 coincide, formula unaffected. |
| Lemma 5.3 | `26:lem:chi` | S Lemma 2, L111-122; "constant on every cycle" from S L72, L209 | Yes | added: "if u'_j = 1 and" (explicit case), and the sentence that chi is constant on a cycle; nothing dropped | three refs to Lemma 5.2: correct | Confirmed. I checked in addition that the sets N(p) are disjoint and lie between p and the next one of u (needed for "in cyclic order"; follows from u_(p+1) = u_(p+2) = 0). Python: chi(Fx) <= chi(x) for all states, n = 4..12. |
| Lemma 5.4 | `26:lem:domain` | S Lemma 3, L124-145 | Yes | none; c_k -> z_k applied in statement and proof | Lemma 5.2: correct | (a), (b): confirmed, all four cell types; d = 3 by hand. (c): confirmed except the clause "hence F = sigma^(-1) U permutes the set of all domain states", which has no sentence in the proof (finding 2). Python: domain states periodic, F maps them to domain states, none contains 111, n = 4..12. |
| Lemma 5.5 | `26:lem:singleton` | S Lemma 5, L159-164 | Yes | none | Lemma 5.4(a): correct | Confirmed; states with two and three ones by hand. |
| Lemma 5.6 | `26:lem:parity` | S Lemma 6, L166-173; P154 Lemma 2 (L63-69), Lemma 3 (L71-75) | Yes. n = 2^k under the standing n >= 4 means k >= 2, the range of P154 Lemma 3(a). | changed as TRACE records: the one-line computation of S is written out with the two steps of P154 (F(E) in O from L67-68; L^(2^j) from L74-75). Nothing dropped. | none inside; the note after the proof cites the literature (not checked) | Confirmed. n = 4: L^2 = sigma^2 + sigma^(-2) = 0 because sigma^4 = 1. Exponent letter j: finding 5. |
| Theorem 5.7 | `26:thm:main` | (a): S Theorem 2, L77-79, proof L214-222; (b), (c), (d): S Theorem 3(a), (b), (c), L82-85, proof L224-232 | Yes for n = 2^k >= 4. (a) is the n = 2^k case of S Theorem 2; the clause on the number of drops of c is not taken over (recorded). | added: "so it ends on no other cycle" in (b); the parenthesis on the shortest-path tree in (d) (both recorded in trace_26.md). Nothing dropped. | 5.3, 5.5, 5.5(a), 5.4(c), 5.6, 2.3: each correct | Confirmed, all four parts, including the in-tree of weight m in (d) (no circuit: the cycles outside the path follow a shortest path to {0} until they meet {0} or a D_i). Unstated in (a), Case 2: chi of the last state equals chi(C) (finding 3). n = 4: m = 1, all parts hold trivially. Python: n = 4, 8: {0} has no leaving edge and every cycle reaches it. Potentials were not computed by me. |
| Prop. 5.8 | `26:prop:indices` | S Theorem 4, L88-91; proof S L245-267 | Yes (n = 2^k >= 8; (c) for odd k) | none; codes written as words | 5.7(d) (four times; source "Theorem 3", "3(c)"), B.4 (source Lemma 8), 5.6 (Lemma 6), B.1 (Lemma 4), B.3 (Lemma 7), B.5 (Theorem 3(d)): each contains what is used | Confirmed. n = 8 by hand: e_0 + e_3 (distances 3, 5); e_(-2) + e_1 + e_2, whose image has 111 on the cells -1, 0, 1 (computed by hand from the rule table); (c) with q = 1: x = 10100100, sources 0 and 5. In (c), "gamma(C_y) = m by Theorem 5.7(d)" uses both directions of (d) (C_x is reachable from some C_1 because gamma(C_x) = m); justified. |
| Prop. 5.9 | `26:prop:even` | S Theorem 5, L93-95, and Corollary 5, L97-98; proof S L276-298 | Yes (even n >= 6, not a power of two) | none; R90, L, S renamed consistently | B.7 (Lemma 9), B.6 (Theorem 2), B.2 (Theorem 1), B.4 (Lemma 8), `thm:A`, `lem:kzero`: each correct. `thm:A` needs only "G1 has a unique closed class"; `lem:kzero` has no hypothesis: both met. | Confirmed except one unwritten step: y is shown to be a periodic point of 1 + Sigma, and periodicity under F^2 = Sigma^(-1)(1 + Sigma)^2 is concluded (finding 1). n = 6 (e = 0, domains 3 + 3), n = 10 (3 + 7, 5 + 5), n = 12 (e = 1; 3 + 9, 5 + 7; four domains of length 3) by hand. Python, n = 6, 10, 12: one closed class, it contains every one-parity cycle and every domain cycle, cycles outside contain 111, codes on K are all but 111, y periodic. |
| Lemma B.1 | `26:lem:ancestors` | S Lemma 4, L147-157 | Yes | none | 5.2, 5.4(a): correct | Confirmed, including p = j + 1 (two ones only) and n = 4, r = 1. Python: n = 4..12. |
| Lemma B.2 | `26:lem:kinds` | S Theorem 1, L72-75, proof L209-212 | Yes. The sentence "Hence every cycle is ..." is added (TRACE C.11(ii)); it follows from the proof. | last sentence: source "Lemma 3(c)", paper "Lemma 5.4(c) and Lemma 5.6" (addition not recorded in TRACE; correct) | 5.3, 5.6, B.1, 5.4(c): correct | Confirmed. Python: every cycle is of one of the three kinds, n = 4..12. |
| Lemma B.3 | `26:lem:carrier` | S Lemma 7, L175-182 | Yes ("if p >= 1" -> "if w is a carrier word") | none | none | Confirmed; both image steps recomputed by hand from the rule table. |
| Lemma B.4 | `26:lem:codes` | S Lemma 8, L184-195 | Yes | none | Def. 5.1, 5.4(b), 5.6, B.2: correct | Confirmed; d = 3 (r = 1) by hand. |
| Lemma B.5 | `26:lem:domaingamma` | S Theorem 3(d), L86, L233-241 | Yes (n = 2^k >= 8) | none | 5.7(b) (source "(a)"), 5.4(c), 2.3, 5.7(d) (source "(c)"): correct | Confirmed; even and odd i; g = 1. Not computed (no potentials). |
| Lemma B.6 | `26:lem:topar` | S Theorem 2, first sentence, L77-78; proof L214-222 | Yes (every even n >= 4) | no proof text of its own; refers to tex 1434-1446 | `26:thm:main`(a): points to the right passage | Confirmed for the range claimed: the passage begins "Let n >= 4 be even" and uses only Lemmas 5.3, 5.4(c), 5.5 and 2.3, none of which is restricted to n = 2^k. Form: finding 3. Python: every cycle reaches a one-parity cycle, n = 4..12. |
| Lemma B.7 | `26:lem:oneparity` | S Lemma 9, L197-205 | Yes | none; P -> P_E, pi -> theta applied consistently | 5.6, 2.3: correct | Confirmed. Python: n = 4..12. |

Paragraph "Computed values and the open case" (tex 1479-1502): every sentence compared with S L269-272, L308-318 and
with `numbers.tex`. The macros agree with S Tables 2 and 3 (n = 4: 1 cycle, k_v = 0, 1, 1, 2, 1, 1, 2, 2, k* = 2;
n = 16: k_111 = 2, k* = 2, 3 cycles with 111, 0 reachable, 2 through a carrier word; n = 22: chi = 6 and 10). The n = 4
vector I confirmed by hand from the definition (m = 1, so k_v = R({0} -> D_v)). The derivation "111 arises only from
10011" is correct. The statements attributed to "the source document" are in S L310-315. One sentence is unclear
(finding 4). Table 1, row 26, agrees with Section 5 (">= 1" at n = 4, 1 at n = 8, 1/2 at n = 16, no statement
elsewhere).

Renamed symbols: chi (for c), z_k (for c_k), calligraphic R (for R90), d (for L), Sigma (for S), theta (for pi), P_E
(for P) are applied at every occurrence in my part; Sigma, theta, calligraphic R and P_E occur nowhere else in the
tex (grep), so they collide with nothing.

## (b) Findings

Severity classes: (1) false statement; (2) gap in a proof; (3) hypothesis or range not met; (4) unclear; (5) cosmetic.

Classes (1) and (3): nothing found.

1. **Proof of Proposition 5.9 (`26:prop:even`), tex 2206-2213; S L281-292 (paragraph "Domain cycles"). Class (2), minor, inherited from the
   source.** The text shows that y "lies in the image of $(1+\Sigma)^{2^e}$, which is the set of periodic points of
   $1+\Sigma$" and continues "So $y$ and $y+e_b$ are periodic". What is needed is that y is periodic under F, i.e.
   under $F^2=\Sigma^{-1}(1+\Sigma)^2$; a periodic point of $1+\Sigma$ is not by that fact alone a periodic point of
   $\Sigma^{-1}(1+\Sigma)^2$. The step is true and takes one sentence. Proposed: after "and $1+\Sigma$ is invertible
   on the image" add "$\Sigma$ commutes with $1+\Sigma$ and is invertible, so it maps the image onto itself; hence
   $F^2=\Sigma^{-1}(1+\Sigma)^2$ is a bijection of the image, and every state of the image is periodic under $F^2$,
   hence under $F$." (Evidence: the argument above, by hand; y periodic at n = 6, 10, 12 in the Python check.)

2. **Lemma 5.4(c) (`26:lem:domain`), statement tex 1369-1370, proof tex 1388-1392; S L129-130, L142-145. Class (2),
   minor, inherited.** The statement has "hence $F=\sigma^{-1}U$ permutes the set of all domain states"; the proof
   shows only that U permutes the domain states with given sources. Missing: a rotation of a domain state is a domain
   state. Definition 5.1 lists "codes, $\chi$ and the existence of flips" as invariant under rotation, not the
   property of being a domain state. `trace_26.md` (section 3) saw this and wrote "The main theorem does not use
   it". Appendix B and the open-case paragraph do use it: "on a domain cycle $C_x$" (tex 2163-2164), the cycle of
   $e_0+e_3$ as a domain cycle (tex 2146-2148 and 2219), and "each of its states ... is not a domain state" (tex
   1489-1490). Proposed: add to the proof of (c) "The definition of a domain state is invariant under rotation
   ($n$ is even), so $\sigma^{-1}$ maps domain states to domain states and $F=\sigma^{-1}U$ permutes them; in
   particular the cycle of a domain state is a domain cycle."

3. **Lemma B.6 (`26:lem:topar`), tex 2169-2175, with the proof of Theorem 5.7(a), tex 1434-1447. Class (4).** The
   lemma is proved for the range it claims (see the table). But a statement for every even n >= 4 is proved by
   pointing into the proof of a theorem whose hypothesis is "Let $n=2^k\ge4$" (tex 1423); the reader has to check
   that the proof resets the hypothesis ("Let $n\ge4$ be even", tex 1434). Proposed: state B.6 as a lemma of
   Section 5 before Theorem 5.7, with tex 1434-1446 as its proof, and let the proof of 5.7(a) be "Lemma ... and
   Lemma 5.6". In the same passage (tex 1444-1445), "Case 1 applies to its cycle" followed by "a cycle with a
   smaller $\chi$" uses that the flips of free cells leave $\chi$ unchanged; add "(the sources, hence $\chi$, are
   the same)". The notation $\chi(C)$ for a cycle is used without being introduced.

4. **Paragraph after Proposition 5.8, tex 1480: "For $k$ even nothing beyond (a) and (b) is proved." Class (4).**
   Proposition 5.8 assumes n >= 8. For k = 2 (n = 4), which the same paragraph treats, (a) and (b) are not proved,
   and (a) does not hold there: the computed values quoted three lines below are $k_{011}=k_{110}=2$. Proposed:
   "For even $k\ge4$ nothing beyond (a) and (b) is proved; for $k=2$ the proposition does not apply."

5. **Letters. Class (5).** (i) The exponent j in tex 1416 ("$L^{2^j}=\sigma^{2^j}+\sigma^{-2^j}$, and for
   $2^j=n/2$"), tex 1419 ("$2^j$ cells") and tex 1496 ("$n=4^j$"), while j is a cell everywhere else in Section 5 and
   Lemma 3.4 was changed to $2^s$ for that reason (tex 394-395; TRACE row of Lemma 3.4). (ii) e is an exponent and a
   unit state in one formula: "$e_a+e_{a+2^{e+1}}+e_b$" (tex 2206; as in S, paragraph "Domain cycles", L281-292). (iii) k is the index of a free cell
   and the exponent of n in one proof: "$z_{k-1}$" (tex 2107) and "$n=2^k$" (tex 2113); also tex 1368. (iv) r is an
   integer in tex 1441, 2054, 2106, and $r(x,y)$ is the resistance (tex 176). (v) "$C_1$" in Theorem 5.7(d) (tex
   1429) and "The cycles are $C_1,\dots,C_m$" (tex 184). TRACE C.11(iii) renames R, L, S, P, pi for this kind of
   reason; these five were left. None of them makes a statement ambiguous. Proposed: $2^s$, $4^s$ in (i); another
   letter for the exponent in (ii) (e.g. $n=2^{a+1}q$ with sources named differently) and for the free-cell index in
   (iii).

6. **Definition 5.1, tex 1325: "any choice of an even number of sources". Class (5).** Zero sources give the zero
   state, which is not in M. Proposed: "a positive even number". (Noted in `trace_26.md`, section 3; as in S L65-67.)

7. **TRACE.md, Part A, row "Theorem 5.7" (TRACE.md line 99). Class (5), documentation.** The row gives the source
   of part (d) only ("S Theorem 3(c), L84-85, proof L226-232") and its verdict cell begins "as (b);", which refers
   to a row that is not there. The four rows of `trace_26.md` for (a), (b), (c), (d) were reduced to the last one.
   Missing in Part A: (a) = S Theorem 2, L77-79, proof L214-222; (b) = S Theorem 3(a), L82, proof L224; (c) =
   S Theorem 3(b), L83, proof L225. Also: the row of Lemma B.2 does not record that the last sentence of the proof
   reads "Lemma 5.4(c) and Lemma 5.6" (tex 2080-2081) where the source has "Lemma 3(c)" (S L212). Both additions
   are correct.

## (c) Not checked

* The PDF (numbering, layout); numbers are those of TRACE.md.
* The literature: Lemma 3.5 and Section 5 of Martin, Odlyzko and Wolfram (note after Lemma 5.6); no search was made.
* The data files and the scripts: the macros of `numbers.tex` were compared with the tables printed in S (section 8),
  not with `g1_26.jsonl` or the csv files; "the same values are in the data files of Table 1" (tex 1480-1481) was
  not checked. Of the computed values only the n = 4 vector was re-derived (by hand); n = 16 and n = 22 were not.
* The potentials gamma and the indices k_v at n = 8 and n = 16 were not computed by me; Theorem 5.7(d), Lemma B.5
  and Proposition 5.8 are confirmed by reading the proofs only.
* The conditional remark of the source on chi >= (n + 8)/3 and the formula chi = (n + 4p)/3 for carrier words: the
  paper attributes both to the source; I checked that the conditional remark is correct by hand (domain cycles at
  n = 4^j have chi <= (n - 4)/3, one edge adds at most 2), the formula not.
* `VERIFICATION_94_26.md` was not opened; the verdict columns of TRACE were not compared with it. Whether "the
  verification excluded none of them" (tex 150-151) is true was not checked.
* P154 beyond lines 30-89 (in particular Lemma Q1, L443-452).
* Theorem 2.8 (`thm:A`) and Lemmas 2.2, 2.3 were read for their hypotheses only; their proofs were read but are not
  judged here.
* The Python check covers even n <= 12 only and no potentials.

## Appendix: the Python check (own code, single process, 0.1 s)

For even n = 4, 6, 8, 10, 12, from the rule table: all states, periodic states, cycles, one-flip edges between
cycles, reachability. Output (True = holds for every case):

| n | m | chi(Fx) <= chi(x) | domain states periodic, mapped to domain states, no 111 | B.1 (111 within n/2 - 1 steps) | cycles by kind (one-parity / domain / with 111 / other) | every cycle reaches a one-parity cycle | one-parity cycles in one component | cycles reachable from {0} (K) | K strongly connected | domain cycles in K | cycles outside K contain 111 | codes on K | y periodic |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 | True | True | True | 1 / 0 / 0 / 0 | True | True | 1 | True | (none) | (none) | 000 | n/a |
| 6 | 7 | True | True | True | 4 / 3 / 0 / 0 | True | True | 7 | True | True | True (none outside) | all but 111 | True (e = 0) |
| 8 | 10 | True | True | True | 1 / 8 / 1 / 0 | True | True | 1 | True | False, as expected (K = {0}) | False, as expected (the 8 domain cycles are outside) | 000 | n/a |
| 10 | 19 | True | True | True | 6 / 12 / 1 / 0 | True | True | 18 | True | True | True | all but 111 | True (e = 0) |
| 12 | 64 | True | True | True | 10 / 54 / 0 / 0 | True | True | 64 | True | True | True (none outside) | all but 111 | True (e = 1) |

The numbers of cycles and of cycles by kind agree with S Table 2 (which counts {0} separately from the other
one-parity cycles).

```python
def run(n):
    N=1<<n; R={1,3,4}                       # rule 26: f = 1 on 001, 011, 100
    bit=lambda x,i:(x>>(i%n))&1
    code=lambda x,i:4*bit(x,i-1)+2*bit(x,i)+bit(x,i+1)
    Ft=[sum((code(x,i) in R)<<i for i in range(n)) for x in range(N)]
    has7=[any(code(x,i)==7 for i in range(n)) for x in range(N)]
    def chi(x):
        o=[i for i in range(n) if bit(x,i)]
        return 0 if len(o)<2 else sum((o[k]-o[k-1])%2 for k in range(len(o)))
    def dom(x):                             # sources: ones whose preceding one has the other parity
        o=[i for i in range(n) if bit(x,i)]
        s=[o[k] for k in range(len(o)) if (o[k]-o[k-1])%2]
        return len(s)>=2 and all(((s[k]-s[k-1])%n)>=3 for k in range(len(s)))
    CH=[chi(x) for x in range(N)]; DM=[dom(x) for x in range(N)]
    S=set(range(N))
    while True:
        S2={Ft[x] for x in S}
        if len(S2)==len(S): break
        S=S2
    per=S; cyc={}; cycles=[]
    for x in sorted(per):
        if x not in cyc:
            c=[];y=x
            while y not in cyc: cyc[y]=len(cycles); c.append(y); y=Ft[y]
            cycles.append(c)
    m=len(cycles)
    def end(x):
        while x not in per: x=Ft[x]
        return cyc[x]
    A=[[False]*m for _ in range(m)]
    for x in per:
        for j in range(n):
            c2=end(x^(1<<j))
            if c2!=cyc[x]: A[cyc[x]][c2]=True
    Rch=[[A[i][j] or i==j for j in range(m)] for i in range(m)]
    for k in range(m):
        for i in range(m):
            if Rch[i][k]:
                for j in range(m):
                    if Rch[k][j]: Rch[i][j]=True
    # then: the tests of the table above, read off CH, DM, has7, per, cycles, Rch
for n in (4,6,8,10,12): run(n)
```

Signed: Claude.
