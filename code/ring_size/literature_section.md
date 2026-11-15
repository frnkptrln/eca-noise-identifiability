Full review with access status, what was read (version, pages) and BibTeX: `literature_ring_size.md`
(prepared in the study session by a separate literature track; nothing is marked as read that was not read).
Several hosts were refused by the sandbox even after access was approved (Wolfram Atlas, wolframscience.com,
projecteuclid.org, direct arxiv.org, ddlab.org); in the study session Martin–Odlyzko–Wolfram (1984), Jen
(1986, 1988), Wuensche–Lesser (1992) and Mairesse–Marcovici (2014) were not read. The independent
verification then read Martin–Odlyzko–Wolfram (1984) in full and the published version of Ellison (2000) in
part (15 of 29 pages: all definitions, Theorems 1 to 3, Section 6.2), and Jen (1986, 1988) as abstracts only;
Wuensche–Lesser (1992) and the Wolfram Atlas remained unobtainable
(`verify_ring_size/literature/literature_check.md`). Statements below that rest on the verification's
reading say so.

**Has the dependence of noise-selected attractors on the ring size been studied?** *Not found* in the
searched sources for ECA with i.i.d. bit-flip noise and minimum-stochastic-potential selection. Closest:

* Bagnoli, Baia and Matteuzzi (arXiv:2406.15408 v2, the extended version of the ACRI 2024 chapter; the
  chapter itself not read) treat all 88 classes under a single-flip "vanishing" noise, but only at L = 17
  (Table 2) and with a single-flip chain between attractors, not stochastic potentials; they do not vary L.
* Ellison (1993, Econometrica 61, Theorem 1(b), p. 1055): coordination on a circle; the parity of N changes
  the order of the non-selected state through a 2-cycle that exists only for even N; the selected state does
  not change with N.
* Bušić, Mairesse and Marcovici (2013, Adv. Appl. Probab. 45, §5.1, p. 977): a majority-flip PCA on Z/nZ
  puts its invariant measure on the two alternating configurations exactly when n is even. Fixed noise, not
  a small-noise limit; the closest published analogue of crystal capture found.
* Studies of asynchronous updating report ring-size conditions (n even, 3 | n, 4 | n) for convergence;
  different noise model, not read.

**Selection by one-mutation steps (Theorem A, Lemma B).** The structure used in Section 4 is known in the
stochastic-stability literature: Samuelson (1994) and Nöldeke and Samuelson (1993, Proposition 1) on
mutation-connected and locally stable components (primary texts not read; known here from the abstract of
Samuelson 1994, from secondary descriptions, and from Ellison), and Ellison (2000, Section 6.2, pp. 37-38),
who attributes to them the lemma that a set reachable from every other limit set by a chain of single
mutations is selected. Not found in the sources read: the explicit potentials gamma_min = m - 1 and
gamma_min = m + q - 2.

**Rule 154 under noise:** *not found*, apart from one row of Bagnoli et al.'s Table 2 at L = 17 (1688
attractors, S = S* = 1, no discussion). Powley and Stepney (2009, J. Cellular Automata 4:125–136, §5.2,
read) place 154 as the only nonlinear rule in the group of the linear rules by the even/odd alternation of
the automorphism count of its transition graph, and name the shared Sierpiński pattern from a single seed.
That rules 154 and 45 are reversible for odd N is in the literature: Bhattacharjee and Das
(arXiv:1903.06011, Example 2; read in part by the verification), Fedoriaka (arXiv:2501.06648; a computation
for N <= 20 with explicit constructions; read by the verification), and Nobe and Yura (2004; abstract and a
search snippet only). Lemma P below re-proves this known fact by a pair-graph certificate. No conjugacy or
factor map between 154 and rule 90, and no statement on 154 at n = 2^k on a ring, was found in the sources
read; partial precedents of the reduction to rule 90 are a comment in OEIS A070886 and Section 5 of
Martin–Odlyzko–Wolfram for rule 18 (see Proposition R154). In this study, every block map of width at most 4
that intertwines rule 154 with a radius-1 rule maps it onto rule 154 or 166, its own symmetry class;
no factor onto an additive rule exists at these widths [computed, `factor_search.csv`].

**Rule 90 at n = 2^k** (used in Proposition R154): Martin, Odlyzko and Wolfram (1984), Lemma 3.5 (p. 230):
for N = 2^j every configuration evolves to the null configuration; with their Theorems 3.3 and 3.4 and
corollaries the single-seed orbit dies iff N is a power of two (read by the verification). NKS p. 963 (read)
gives the fraction of states on cycles for rules 60 and 90 as 2^(−2^IntegerExponent[n,2]), which for n = 2^k
leaves only the null state; the nilpotency is also proved directly in v0.2 (Proposition 1) and here.

**The crystal of class 94.** The three phases of (011)^{n/3} are the non-null fixed points of rule 90 for
3 | N given by Martin, Odlyzko and Wolfram (1984), Lemma 3.7 (p. 234; read by the verification); rules 94
and 90 agree on the codes 3, 5, 6. Its one-flip radius under rule 94 was not found in the sources read.

**Radius and modified coradius.** Ellison (2000, Rev. Econ. Stud. 67:17–45, doi 10.1111/1467-937X.00119):
radius R(Ω), coradius, modified coradius CR*(Ω) (path cost minus the radii of the intermediate limit sets),
and Theorem 2 (Section 4.2, p. 30): if R(Ω) > CR*(Ω) for a union Ω of limit sets, then (a) the long-run
stochastically stable set is contained in Ω and (b) W(y, Ω, ε) = O(ε^(−CR*(Ω))) for every y outside Ω. The
study session read the January 1999 working paper, which has the same theorem numbers; the journal pages
were read by the verification.
