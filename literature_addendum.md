# Literature addendum (17 November 2026): sources missing from `literature_ring_size.md`, and prior work on rules 43 and 142

This file adds to `literature_ring_size.md`; that file is not changed. It was written in the session that
produced `proofs_43_142/`. No claim of novelty is made anywhere in this file.

**Occasion.** A novelty search made outside this session reported that it found no prior statement of the
rule-154 theorem, of the class-94 theorem, or of the ring-size dependence of noise selection in ECA, and named
seven sources that `literature_ring_size.md` does not have. This addendum records what this session could read
of each of them (Part A), checks one numerical statement by a script (A1), and reports a search for prior work on
rules 43 and 142 (Part B). The outside search itself was not repeated and is neither confirmed nor contradicted
here.

**Reading rule (as in `literature_ring_size.md`).** "Read" means that the text itself was opened and read in this
session, with the version and pages named. "Search excerpt" means a fragment returned by a web search from the
page named; "abstract" means the abstract only. Statements from excerpts and abstracts are marked as such and
do not count as read. Page numbers are journal pages unless marked "arXiv p.". At most one short phrase is quoted
per source.

**Limits that apply to every "does not cover" below.** (1) The reading was done page by page; no full-text
keyword scan of the PDFs was made, so every negative statement rests on the pages listed under "Read" only.
(2) Several key texts were read in part or not at all. (3) The searches of Part B were 15 queries on one day.
All negative findings are provisional.

## 0. Access (17 November 2026)

| host | result |
|---|---|
| arxiv.org, export.arxiv.org | not reachable from the execution environment (refused at the network layer; this cannot be lifted by an approval). No mirror or cache was used. arXiv texts were reached only when the DOI fetch tool delivered an arXiv copy for a journal DOI, or as search excerpts |
| content.wolfram.com (*Complex Systems*) | reachable: Nordahl (1989), Voorhees and Beauchemin (2004), Fukś (rule 142), Stricker (2023) |
| www.kurims.kyoto-u.ac.jp, repository.kulib.kyoto-u.ac.jp, www.complex-systems.com, atlas.wolfram.com | access approved by the author, then refused at the network layer |
| IOP, World Scientific, APS, Springer, Elsevier | paywalled; not requested |

## Part A. The seven sources

### A1. Zhu and Richard, arXiv:2610.10967

**Reference.** Qingying Zhu, Serge Richard, "Elementary cellular automata: spectral properties of Koopman operator
for finite periodic realizations", arXiv:2610.10967v1 [math.SP], submitted 7 October 2026, 16 pages (data from
the arXiv abstract page as returned by the search).

**Read.** Nothing in full text. Seen: search excerpts of the abstract page and of the HTML version (v1). Search
excerpts are fragments chosen by the search index and are not stored with the session, so they cannot be
re-checked. Two sets were seen: those returned to the literature sub-task of this session (seven queries) and
those returned to one query of the lead.

**Not read.** The PDF and the complete HTML; equation (4); the content of the figures; the reference list.

**What the excerpts say.**

* Seen in both sets: under a heading 2.3 on the Koopman operator, a zero eigenvalue ratio is defined as the
  multiplicity of the eigenvalue 0 of the Koopman matrix of the ring of n cells divided by 2^n, with a pointer to
  an equation (4); for rules 45 and 154 the operator is unitary for every odd n (cited from another paper); for
  rule 154 the ratio

  > "is always below 0.01 for n∈{13,…,27} and seems to decrease with larger n"

  with a pointer to Figure 13 (caption: spectra for rule 154 at n = 22 and n = 24); a list item groups the rules
  60, 90, 105, 150, 154.
* Seen only in the sub-task's set, not by the lead: that these sentences stand in a Section 4.2 (the task names
  the same section) and the list in a Section 4.3, and a sentence that describes the operator of rule 154 at even
  n as close to unitary. These three points are reported second-hand here.

**Not seen.** The two values 0.00048828 (n = 22) and 0.00045776 (n = 24) named in the task, and any wording that
the observation is unexplained. The values are presumably printed in Figure 13. No explanation appears in the
excerpts; whether the paper gives one cannot be stated without the full text. Whether the authors themselves
identify the ratio with the fraction of states that lie on no cycle was not seen either.

**The quantity.** For a map F on a finite set of N states, the Koopman matrix in the basis of indicator functions
is the 0-1 matrix of the graph of F; the rank of its t-th power is the number of states in F^t of the whole set,
which for large t is the number of periodic states. So the algebraic multiplicity of the eigenvalue 0 is the
number of non-periodic states [proved, this paragraph]. The dimension of the kernel, in contrast, is the number
of states without preimage. Which of the two the paper's "multiplicity" means was not seen; the script below
computes both.

**Check by script** (`proofs_43_142/zhu_richard_154.py`; table copied verbatim from
`proofs_43_142/out/tables_154.md`). Lemma 6 of `verify_ring_size/part2_154/PROOF_154.md` says: on an even ring the
periodic states of rule 154 are the (2^(n/2) - 1)^2 states of M together with the periodic states inside E ∪ O
(states supported on one parity class of sites). The lemma gives the number of the latter only for n = 2^k. The
script counts them by iterating rule 154 on the 2^(n/2+1) - 1 states of E ∪ O alone, and compares with a direct
enumeration of all 2^n states for n <= 24.

<!-- TABLE 154 BEGIN -->
| n | periodic states in E ∪ O | periodic states by Lemma 6 | periodic states, direct enumeration | equal | fraction of states not on a cycle | decimal | 2^(1 - n/2) (1 - 2^(-2^j)) equal | value quoted from arXiv:2610.10967 | agrees at the quoted precision | states without preimage (fraction) |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 | 10 | 10 | True | 3/8 | 0.375000000000 | True |  |  | 4 (0.250000000000) |
| 6 | 7 | 56 | 56 | True | 1/8 | 0.125000000000 | True |  |  | 8 (0.125000000000) |
| 8 | 1 | 226 | 226 | True | 15/128 | 0.117187500000 | True |  |  | 16 (0.062500000000) |
| 10 | 31 | 992 | 992 | True | 1/32 | 0.031250000000 | True |  |  | 32 (0.031250000000) |
| 12 | 31 | 4000 | 4000 | True | 3/128 | 0.023437500000 | True |  |  | 64 (0.015625000000) |
| 14 | 127 | 16256 | 16256 | True | 1/128 | 0.007812500000 | True |  |  | 128 (0.007812500000) |
| 16 | 1 | 65026 | 65026 | True | 255/32768 | 0.007781982422 | True |  |  | 256 (0.003906250000) |
| 18 | 511 | 261632 | 261632 | True | 1/512 | 0.001953125000 | True |  |  | 512 (0.001953125000) |
| 20 | 511 | 1047040 | 1047040 | True | 3/2048 | 0.001464843750 | True |  |  | 1024 (0.000976562500) |
| 22 | 2047 | 4192256 | 4192256 | True | 1/2048 | 0.000488281250 | True | 0.00048828 | True | 2048 (0.000488281250) |
| 24 | 511 | 16769536 | 16769536 | True | 15/32768 | 0.000457763672 | True | 0.00045776 | True | 4096 (0.000244140625) |
| 26 | 8191 | 67100672 | not computed |  | 1/8192 | 0.000122070312 | True |  |  | not computed |

Lemma 6 count equals the direct count at every even n = 4..24: True. The closed form agrees at every even n = 4..26: True. Both quoted values agree: True. Within n = 4..26 the fraction is below 0.01 for every even n >= 14 and not for smaller even n. CPU time 1.39 s, peak memory 1035 MB (`proofs_43_142/zhu_richard_154.py` -> `proofs_43_142/out/zhu_richard_154.json`).
<!-- TABLE 154 END -->

Reading of the table.

* **The two quoted values are exactly what Lemma 6 gives**, at the quoted precision: 1/2048 at n = 22 and
  15/32768 at n = 24, when the ratio is the fraction of non-periodic states (algebraic multiplicity). The number of
  states without preimage gives the same value at n = 22 and a different one at n = 24, so the quoted pair fits
  the first reading and not the second. The comparison is with the values as given in the task; the digits were
  not seen in the paper.
* **"Below 0.01 for n in {13, ..., 27}"** agrees with the table for the even n in that range (14 to 26); for odd n
  the map is a bijection and the fraction is 0. For even n <= 12 the fraction is above 0.01.
* **Closed form** [computed for even n = 4..26]: the fraction equals 2^(1 - n/2) (1 - 2^(-2^j)), where n/2 = 2^j q
  with q odd. Sketch of a derivation, not checked against the primary source: by Lemma 2 of `PROOF_154.md` rule 154
  acts on E ∪ O as rule 90, whose square on one parity class is rule 90 on a ring of n/2 cells; the fraction of
  periodic states of rule 90 on a ring of N cells is 2^(-D2(N)), D2(N) the largest power of two dividing N (and 1/2
  for odd N), a result of Martin, Odlyzko and Wolfram (1984) as quoted by Nordahl (A3, p. 70). The closed form is
  strictly decreasing in even n.
* So Lemma 6 accounts for the observation as far as its content is known here: the non-periodic states of rule
  154 on an even ring are exactly the non-periodic states of the embedded rule 90 on the two parity classes, a
  set of at most 2^(n/2+1) states among 2^n.

**Covers.** A numerical observation on rule 154 for n up to 27 (excerpt). **Does not cover (as far as the
excerpts show).** One-flip graphs between attractors; noise; a relation of the observation to parity classes or to
rule 90.

### A2. Nobe and Yura

**Reference.** (1) A. Nobe, F. Yura, "Linearizable cellular automata", J. Phys. A: Math. Theor. 40 (2007) 7159-7174,
DOI 10.1088/1751-8113/40/26/004 (DOI verified by title). (2) Nobe and Yura, RIMS Kokyuroku 1541 (2007) 178-191:
data as given in the task, not verified.

**Read.** Neither text. Seen for (1): the abstract, and two search excerpts (a table caption on the reversible
ECA rules with periodic boundaries; a sentence that the transitions of rules 45, 75, 89, 101 are compositions of
those of the linearizable rules 210, 180, 166, 154 with the exchange of 0 and 1).
**Not read.** Both full texts ((1) paywalled; (2) host not reachable).

**Covers (abstract only).** The initial value problem of a class of reversible ECA with periodic boundaries is
reduced to a linear system over a finite commutative ring (the deposited abstract does not confirm "over Z_2"). **Unknown.** What is said for even N. The statement "even N not treated" is
neither confirmed nor contradicted; the abstract speaks only of reversible automata, and rule 154 is reversible
only at odd N.

### A3. Nordahl (1989)

**Reference.** M. G. Nordahl, "Formal languages and finite cellular automata", Complex Systems 3 (1989) 63-78.

**Read.** Publisher scan (content.wolfram.com): pp. 68-74 (Section 3) and the reference list pp. 76-78.
**Not read.** pp. 63-67 and Section 4 (displayed, not studied).

**Covers.** p. 70: for rule 90 with periodic boundary, citing Martin, Odlyzko and Wolfram: the fraction of states
on cycles is 1/2 for odd n and 2^(-D2(n)) for even n; at n = 2^k the zero configuration is the only periodic
state. p. 73: definition of simulation by a finite blocking transformation. p. 74: every rule that can simulate
rule 60, 90 or 150 has a periodic set that is neither regular nor unambiguous context-free, and this applies to
the rules 18, 22, 26, 94, 122, 146, 154 and 164,

> "which are known to be capable of simulating rule 90"

with a reference to an appendix by L. P. Hurd in Wolfram (ed.), *Theory and Applications of Cellular Automata*
(1986), and to rule 105 (simulating rule 150).

**Does not cover.** The blocks for rule 154 are not given (Hurd's appendix was not obtained). Nothing specific to
rule 154 at even N beyond membership in the list; nothing on the set M or on the permutation property of
`PROOF_154.md`; nothing on one-flip graphs or noise. Relation to the repository: `PROOF_154.md` (Lemma 2) uses
that rule 154 acts as rule 90 on the states supported on one parity class of sites; whether this is the simulation
meant by Nordahl and Hurd was not checked.

### A4. Krawczyk, arXiv:1304.5771

**Reference.** M. J. Krawczyk, "New aspects of symmetry of elementary cellular automata", arXiv:1304.5771 (version
not seen); journal version Chaos, Solitons and Fractals 78 (2015) 86-94 (from citing reference lists; DOI not
verified).

**Read.** Nothing in full text. Seen: abstract and search excerpts of the arXiv PDF.
**Not read.** The body; **the entries of Table 4**.

**Covers (excerpts).** States on N cells are grouped into classes by a symmetry of the state-transition network;
the number of classes is tabulated against N. For the automata 154, 166, 180, 210: one class for odd N; for
even N the numbers are in Table 4, with the remark

> "for every second even value (indivisible by 4) the number of classes is equal to 5"

The journal version describes the method as numerical. **Does not cover (as far as seen).** An explanation of the
N-dependence; which N are tabulated; one-flip graphs; noise.

### A5. Chua et al., Parts VII and VIII

**Reference.** L. O. Chua, J. Guan, V. I. Sbitnev, J. Shin, "A nonlinear dynamics perspective of Wolfram's new kind
of science. Part VII: Isles of Eden", Int. J. Bifurcation Chaos (2007), DOI 10.1142/S0218127407019068; L. O. Chua,
K. Karacs, V. I. Sbitnev, J. Guan, J. Shin, "... Part VIII: More Isles of Eden", DOI 10.1142/S0218127407019901
(titles verified through the DOI; volume and pages not seen).

**Read.** Abstracts only. **Not read.** Both full texts (paywalled).

**Covers (abstracts).** Part VIII: basin tree diagrams of the hyper Bernoulli shift rules for L = 3..8; stated as
proved for all L: rules 154 and 45 are

> "inhabited by a dense set (continuum) of Isles of Eden if, and only if, L is an odd integer"

An Isle of Eden is a periodic orbit with empty basin. For a bijection every orbit is one, so this agrees at odd L
with the wording of the task ("only Isles of Eden for odd L"); the exact theorem was not read, nor what is said
about even L beyond the "only if". Secondary lists (search excerpts of two later arXiv surveys) place rules 14,
35, 43, 142 and 184 in one class of this series (Bernoulli shift rules). **Does not cover (as far as seen).**
One-flip graphs; noise; ring sizes above 8 in the diagrams.

### A6. Stricker (2023)

**Reference.** H.-P. Stricker, "Classification of elementary cellular automata based on their limit cycle lengths
in Z/k", Complex Systems 32(3) (2023) 229 ff., DOI 10.25088/ComplexSystems.32.3.229.

**Read.** Publisher PDF: pp. 229-232. **Not read.** The remaining 19 PDF pages (tables and text).

**Covers.** p. 230: complete cycle-length spectra of all 88 classes up to ring size k = 22 (rule 45 up to 18);
partial spectra from random initial configurations for larger k. p. 232, among numerical findings:

> "Rules 26 and 154 are the only rules with linear growth that have cycle lengths L = 4·k."

**Does not cover (pages read).** A proof; the k at which the length 4k occurs; an even/odd analysis of rule 154;
one-flip graphs; noise.

### A7. Voorhees and Beauchemin

**Reference.** B. Voorhees, C. Beauchemin, "Point mutations and transitions between cellular automata attractor
basins", Complex Systems 15 (2004) 41-78; preprint arXiv:nlin/0306033.

**In the repository so far.** Listed among the sources not obtained in
`verify_ring_size/literature/literature_check.md`; no mention in `VERIFICATION_ring_size.md`.

**Read.** Journal PDF: pp. 41-53 and 66-71. **Not read.** pp. 54-65 (theorems for additive rules), 72-78; the arXiv
version.

**Covers.** Binary CA on a ring (left-justified neighbourhoods); a tau-point mutation toggles tau sites. The
matrix of all tau-site toggles on the 2^n states, normalised, has the uniform steady state. The paper assumes
that mutations are much faster than the rule iterations (pp. 44, 52). It names the opposite regime, mutations
much slower than the dynamics, in which

> "then only the attractors are relevant"

and does not treat it. That regime is the one of the graph G1 of this repository. Section 3.2 groups states by
attractor and height and counts mutations between the groups. Appendix A tabulates characteristic equations of
one-point-mutation matrices for rules 60, 90, 150, 18, 22, 30, 54, 110 at small ring sizes (up to 13 for rule 60 only, according to the verification's literature check).

**Does not cover.** Costs, stochastic potential, a small-noise limit, a selection of attractors; rules 154, 43,
142 (pages read).

## Part B. Prior work on rules 43 and 142

Three facts carry the proofs of `proofs_43_142/PROOF_43_142.md`:

* (a) the wall word d_i = x_i + x_(i+1) mod 2 turns rule 142 into rule 226 and rule 43 into rule 184, and the
  number of walls is conserved (Lemmas 1, 2, 5 there);
* (b) for rules 184 and 226 on a ring, a configuration is periodic iff it has no block 11 or no block 00; at
  density 1/2 the periodic configurations are the alternating ones (Lemmas 3, 4);
* (c) the periodic configurations of rules 43 and 142 are those whose runs all have length >= 2 or all have
  length <= 2; for 4 | n the travelling configuration (0011)^(n/4) is the only cycle with n/2 walls (Lemmas 7, 8).

| source | how seen | (a) | conservation | (b) | (c) | finite rings | case 4 \| n |
|---|---|---|---|---|---|---|---|
| B1 Fukś, "Dynamics of the cellular automaton Rule 142", Complex Systems 16, 123-138 (footer: 2005), DOI 10.25088/ComplexSystems.16.2.123 | read in full (publisher PDF) | rule 142 -> rule 226 under rule 60: yes (abstract; eq. 34, p. 132; again as eq. 40, p. 133, inside the proof of Proposition 6, which itself is a statement on preimage counts), credited there to Boccara (printed there as 1992; the volume is dated 1993). Rule 43: not in the pages | yes: rule 142 conserves the number of blocks 10, for periodic configurations of every length (Section 3) | no (infinite lattice, limits in probability) | no | conservation only | no |
| B2 Fukś, "Remarks on the critical behavior of second order additive invariants in elementary cellular automata", Fundamenta Informaticae 78 (2007) 329-341; arXiv:nlin/0502037 | search excerpts only | both identities, f60 ∘ f43 = f184 ∘ f60 and f60 ∘ f142 = f226 ∘ f60 (Section 7 of the arXiv text; location to be checked) | critical density of the invariant 1/4 for rules 14, 43, 142 (figure caption) | ballistic-annihilation picture of rule 184 | not seen | not seen | not seen |
| B3 Boccara, "Transformations of one-dimensional cellular automaton rules by translation-invariant local surjective mappings", Physica D 68 (1993) 416-426, DOI 10.1016/0167-2789(93)90134-M (Fukś's reference lists print 1992) | not obtained | per B1: source of the identity for rule 142 | ? | ? | ? | ? | ? |
| B4 Fukś, "Solution of the density classification problem with two cellular automata rules", Phys. Rev. E 55 (1997) R2081; arXiv:comp-gas/9703001v1 | arXiv version read in full (5 pp.) | no | number of ones (implicit) | yes (arXiv p. 3): on a ring of length L, after floor((L - 2)/2) steps of rule 184 there is no block 00 if the density exceeds 1/2, no block 11 if it is below 1/2, and neither at density 1/2; the underlying proposition is proved in sketch | no | yes | no |
| B5 Capcarrere, Sipper, Tomassini, Phys. Rev. Lett. 77 (1996) 4969-4971 | not obtained | ? | ? | per B6 (p. 4): rule 184 on a ring of size N reaches its invariant state within N/2 steps | ? | yes (second-hand) | ? |
| B6 Belitsky and Ferrari, "Invariant measures and convergence properties for cellular automaton 184 and related processes", J. Stat. Phys., DOI 10.1007/s10955-004-8822-4; arXiv:math/9811103v1 | arXiv pp. 1-6 of 18 | no (a related map to ballistic annihilation, Assertion 1.1) | n/a | attributes the N/2 bound on a ring to B5; own results on the infinite line | no | no | no |
| B7 Boccara and Fukś, "Cellular automaton rules conserving the number of active sites", J. Phys. A 31 (1998) 6007-6018; arXiv:adap-org/9712003v2 | arXiv pp. 1-4 of 14 | no | number of ones, on rings | no | no | yes | no |

Not obtained or not located, so nothing can be said about them: Hattori and Takesue, Physica D 49 (1991) 295-322
(additive conserved quantities; cited in B2); Krug and Spohn, Phys. Rev. A 38 (1988) 4271-4283; Belitsky and
Ferrari (1995) on ballistic annihilation; Boccara, "Eventually number-conserving cellular automata"; the Wolfram
Atlas entries for rules 43 and 142. Fukś, Phys. Rev. E 60 (1999) 197-202 was obtained and not read.

**What follows for `PROOF_43_142.md`.**

* (a) is known for both rules. For rule 142 it was read (B1, which credits Boccara 1993, not read); for rule 43 it
  was seen by the session in a search excerpt of B2 only and was read in B2 on 18 November 2026 (update below). Lemma 1 of the proof re-derives both identities from the rule tables.
* The conservation law is known for rule 142 (B1, read). The number of blocks 10 is half the number of walls. For
  rule 43 a conserved block-10 count was seen only in excerpts.
* (b) is known for rule 184 on rings in the form "after floor((L - 2)/2) steps" (B4, read; proof sketched there).
  The statement "periodic iff no 11 or no 00" follows from it with number conservation but was not seen written
  out. Lemmas 3 and 4 give a different, complete argument (translation of the two sets of pairs); the healing time
  n/2 - 1 of Proposition 2 equals the bound of B4 at L = n.
* (c) was **not found**: no source seen states the run-length description of the periodic configurations of rules
  142 or 43 on a ring, the uniqueness of the cycle with n/2 walls, or the case 4 | n. B1 treats the density 1/4 of
  blocks 10 (which corresponds to n/2 walls) on the infinite lattice as a jamming-type transition. According to
  the verification's literature check, B1 also gives a local motion law for the blocks 10 (a block moves by one
  site or stays, depending on the preceding site) and their expected velocity as a function of density (eq. 59,
  p. 137): infinite-lattice counterparts of the two families of cycles of Lemma 7, without the ring statement.
* **Noise selection.** No source was found that states which cycles of rules 43 or 142 are selected by small
  bit-flip noise, on any ring. The only related datum found is the table row of Bagnoli, Baia and Matteuzzi
  (arXiv:2406.15408, already Section 1.2 of `literature_ring_size.md`) for rules 43 and 142 at ring size 17, an odd
  size, without discussion of these rules. The noisy rule 184 of B6 and of the density-classification literature is
  a random hopping of particles, not bit-flip noise.

These are statements about a short search with several key texts unread. They do not show that (c) or the
selection statement is absent from the literature.

## Update of 18 November 2026 (after the verification)

Written by Claude, the reader outside both sessions, after `VERIFICATION_43_142.md`. Findings B6 and B8 to B10 of
the verification are applied in the text above (Boccara's paper is dated 1993; location of the identity in B1; the
motion law of B1; A7 and A2).

**B2 read in full.** Fukś, "Second order additive invariants in elementary cellular automata",
arXiv:nlin/0502037v1 (17 February 2005), 15 pages, read in full through an arXiv reader that the two sessions
could not reach. The journal version (Fundamenta Informaticae 78 (2007) 329-341, different title) was not seen and
not compared.

* Section 7, p. 12, eqs. (28) and (29): f60 ∘ f43 = f184 ∘ f60 and f60 ∘ f142 = f226 ∘ f60, with the words
  "there exists a local mapping (rule 60) which transforms rule 43 into rule 184, and rule 142 into rule 226";
  credited to its reference [19], Boccara (printed as 1992).
* Section 5, p. 7, and Table 1, p. 6: rules 12, 14, 15, 34, 35, 42, 43, 51, 140 and 142 "conserve the number of
  blocks 10"; the result is taken from Hattori and Takesue (1991, not read). Setting: a lattice of length L with
  periodic boundary conditions (Section 2).
* Table 2, p. 10, and Figures 1 and 5: for rules 43 and 142 the fundamental diagram has its singularity at density
  1/4 of the invariant, i.e. at n/2 walls (simulations on 50000 sites); the space-time patterns at that density
  show localized structures that move in opposite directions and annihilate upon collision (Figure 5; for rule 184
  the paper states that the two kinds of defects are equally frequent at the critical point). This is the level of
  the crystal X of `PROOF_43_142.md`, seen there on a very large lattice.
* Not in the text: the periodic configurations on a ring of given length, the uniqueness of the cycle at density
  1/4, any role of 4 | L, noise.

**Consequence for Part B.** Fact (a) and the conservation law are known and were read for both rules (rule 142: B1;
rules 43 and 142: B2). Fact (b) in the form of Lemmas 3 and 4 and fact (c) remain "not found in the sources
reached"; Boccara (1993), Hattori and Takesue (1991), Fukś (2007, journal version) and Fukś's 2023 book are still
unread.

## Update of 20 November 2026 (A1 read in full)

Written by Claude, the reader outside the sessions.

**A1 read in full.** Zhu and Richard, arXiv:2610.10967v1 (arXiv stamp 7 October 2026, first page dated 9 October
2026), 16 pages, read in full on 20 November 2026 through an arXiv reader that returns the text of every page and
that the sessions could not reach. The figures were available only as the text printed in them (titles, axis
labels, the printed ratio), not as images.

* Definition. Equation (4), p. 13: the zero eigenvalue ratio is the number of eigenvalues 0 of the Koopman matrix
  divided by 2^n. Proposition 2.2, p. 6 (given there as a summary of Lemmas 1 to 6 of Taga et al., Chaos 31, 2021,
  not read): a cycle of length m contributes the m-th roots of unity, and every state that is a Garden of Eden or
  transient contributes one eigenvalue 0; the text below it says that the multiplicity of 0 is the number of
  states that lie on no periodic orbit. So the ratio is the algebraic multiplicity divided by 2^n, the fraction of
  states on no cycle: the first of the two quantities of the paragraph "The quantity" above.
* Rule 154. Section 4.2 ("Unitarity"), pp. 13-14: for rules 45 and 154 the operator is unitary for every odd n,
  cited from Table 1 of Nobe and Yura (2004); for even n the operator of rule 154 is called "not far from being
  unitary"; the sentence quoted above ("is always below 0.01 ...") is on p. 14, followed by the comparison that
  for rule 45 the ratio at even n is above 0.5 in the range computed. Figure 13, p. 14, prints "Zero eigenvalue
  ratio: 0.00048828" for n = 22 and "0.00045776" for n = 24. These are the two values named in the task, and they
  agree with the table above.
* No explanation is given. Section 1, p. 2, says of the observations of Section 4 that the authors could not find
  them in the literature and that for now they are "only observations"; Section 5, p. 15, leaves the properties
  that depend on n to future work.
* Rules 60 and 90. Section 4.3, p. 14, groups rules 60, 90, 105, 150 and 154 as one family (IV_2 in Table 1,
  p. 12). For rules 60 and 90 the ratio is reported as 0.5 for odd n, 0.75 for n = 14, 18, 22, and above 0.93 for
  n = 16, 20, 24, with the words "We do not have an explanation for this surprising pattern." (For rule 90 the
  fraction of states on cycles as a function of the power of 2 in n is, as far as the reader recalls, in Martin,
  Odlyzko and Wolfram (1984); this was not looked up for this note.)
* Classification, Section 3 and Table 1: rules 26 and 94 are in family IV_0; rules 43 and 142 in family III_1/2
  (many cycles of length n for even n and of length 2n for odd n); rule 184 in III_1.
* Not in the text: noise or any other perturbation of the dynamics; the parity classes of rule 154, a relation of
  rule 154 to rule 90, or rings of 2^k cells; which cycles carry weight under small noise; any statement on rules
  26, 43, 94 or 142 beyond the classification.

**Consequence.** Open item 1 is settled: the multiplicity of equation (4) is the algebraic one, both digit strings
are printed in Figure 13, and the paper offers no explanation of the observation for rule 154. The description of
the periodic states of rule 154 on even rings ("Lemma 6" in the table above; Lemma 3.7 of
`paper/ring_size_paper.tex`) explains it: the states on no cycle are the states with ones on one parity class
only that are not periodic under rule 90, at most 2^(n/2+1) - 1 of the 2^n states. Zhu and Richard can now be
cited as read in full.

**Bibliographic data seen on 20 November 2026.** In the reference list of Zhu and Richard: Stricker, Complex
Systems 32 (3), 229-251, 2023; Nobe and Yura, J. Phys. A: Math. Gen. 37, 5789-5804, 2004. In the results of a web
search (result pages, not the papers themselves): Pitman and Tang is in Bernoulli, volume 24, issue 3 (the address
of the paper at Project Euclid); the author of Physica D 68 (1993) 416-426 is Nino Boccara. The given name of
Fukś is Henryk (author line of arXiv:nlin/0502037v1, read on 18 November).

## Update of 23 November 2026 (attempt to reach the texts marked "not read")

Written by Claude, the reader outside the sessions. Aim: to read the texts that the paper cites as not read or as
seen through an abstract or excerpt only. Result: one related text reached through a tool, none of the texts
themselves.

**Reached, through a tool only.** Nobe and Yura, "On the integrability of reversible elementary cellular automata"
(in Japanese), RIMS Kôkyûroku 1541 (2007), pp. 178-191, open at
https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/1541-13.pdf. This is not one of the two texts of
Nobe and Yura in the list of references (J. Phys. A 37, 2004, and J. Phys. A 40, 2007); it is a proceedings text by
the same authors on the subject of the second. How it was seen: a fetch tool answered four questions against the
text of the PDF (extracted by character recognition). I did not see the pages; what follows is the tool's report,
and the layout of the table was reported as approximate.

* Theorem 2, p. 180: there are 16 reversible elementary rules with periodic boundary; attributed there to their
  reference [13], which is the paper of 2004.
* Table 1, p. 180: rules 150 and 105 for N = 1, 2 (mod 3); rules 154, 166, 180, 210 and 45, 75, 89, 101 for odd N;
  rules 170, 240, 15, 85 for all N (one further row was garbled in the extraction).
* Rule 154, pp. 180-183: analysed for odd N only. The configuration is cut into blocks; inside a block the evolution
  is linear, written with the polynomial 1 + x^2 over the field with two elements; the positions of the cells are
  separated by parity. Proposition 1, p. 183: the period of a configuration divides 2^(s+1) N, with s the integer
  part of the binary logarithm of the largest block length. Rule 90 is not named.
* Even N for rule 154 is not analysed; nothing on states that lie on no cycle.
* Table 2, p. 189: the rules are classed as trivial, additive, linearizable or unknown; 45, 75, 89, 101 are
  "unknown".

Consequence: that rule 154 is reversible for odd N is now seen in a text of Nobe and Yura themselves (through a
tool), with the attribution to their paper of 2004; it was an abstract and a search excerpt before. What Lemma 3.7
of the paper says for even N is not in this text. The paper's entries for Nobe and Yura stay "not read".

**Not reached** (23 November 2026, tools of this conversation):

| text | why |
|---|---|
| Young, Econometrica 61 (1993) | JSTOR; a copy on a third-party archive was not readable by the fetch tool (the site's rules for automated access could not be read) and was not fetched in another way |
| Nöldeke and Samuelson, Games Econ. Behav. 5 (1993) | as for Young (same archive) |
| Samuelson, J. Econ. Theory 64 (1994) | publisher's paywall |
| Nobe and Yura, J. Phys. A 37 (2004) and 40 (2007) | publisher's paywall; not found on arXiv |
| Boccara, Physica D 68 (1993) | publisher's paywall |
| Hattori and Takesue, Physica D 49 (1991) | publisher's paywall |
| Freidlin and Wentzell (book) | not available online |

Search results seen on the way (result pages, not the texts): the abstract of Young (1993) names "a general theorem
on perturbed Markov processes that characterizes their stochastically stable states graph-theoretically"; the
abstract of Hattori and Takesue (1991) says that the condition is applied to "Wolfram's elementary CA".

Claude

## Search queries (17 November 2026, web search)

Part A: `arXiv 2610.10967 Zhu Richard elementary cellular automata`; `Zhu Richard 2026 elementary cellular automata
finite rings rule 154 fraction of states not on cycles`; `"2610.10967"`; four further queries with the title words,
"zero eigenvalue ratio", Figure 13 and the two digit strings; `Krawczyk "New aspects of symmetry of elementary
cellular automata" Table 4 automata 154, 166, 180, 210 number of classes even N`; `Nobe Yura "Linearizable cellular
automata" rule 154 odd N even N periodic boundary RIMS Kokyuroku 1541`; `Chua "Isles of Eden" rules 45 and 154 odd
L ... Part VIII hyper Bernoulli shift`.

Part B: `Fuks "Second order additive invariants in elementary cellular automata" rule 142 rule 43 rule 14 rule 35
number of blocks 10 conserved`; `rule 184 cellular automaton bit-flip noise small-noise limit stochastic stability
stationary distribution finite ring rule 142 OR rule 43`; `Capcarrere Sipper Tomassini "Two-state, r=1 cellular
automaton that classifies density" rule 184 N/2 time steps background 01 blocks 00 11`; `elementary cellular
automaton "rule 43" "rule 184" "rule 60" OR "rule 102" transformation semi-conjugacy factor periodic configurations
ring`; `"rule 142" OR "rule 43" elementary cellular automaton noise "stochastically stable" OR "zero-noise limit" OR
"vanishing noise" attractor selected ring`.

One further query was made by the lead of the session for A1 (title words, "rule 154", "zero eigenvalue ratio");
it returned the same excerpts.

## Open items

1. A1: Figure 13 and Section 4.2 of arXiv:2610.10967v1 need to be looked at by someone with arXiv access: the two
   digit strings, the definition in equation (4) (algebraic multiplicity or kernel dimension), and whether an
   explanation is offered.
   Settled on 20 November 2026, see the update of that date.
2. A2: both Nobe-Yura texts; what is said for even N.
3. A3: Hurd's appendix (the blocks for rule 154). A4: the entries of Krawczyk's Table 4. A5: the theorems of Chua
   et al., Part VIII. A6, A7: the pages not read.
4. B2: the location and wording of the identity for rule 43 (seen as an excerpt). B3 (Boccara 1993) and B5
   (Capcarrere et al. 1996) are the apparent primary sources of (a) and of the N/2 bound in (b); both
   attributions are second-hand.
5. Hattori and Takesue (1991): whether its tables list the block-10 invariant for rules 43 and 142.
6. The journal versions of B4, B6, B7 were not compared with the arXiv versions read.
