Full review with access status, what was read (version, pages) and BibTeX: `literature_ring_size.md`
(prepared in this session by a separate literature track; nothing is marked as read that was not read).
Several hosts were refused by the sandbox even after access was approved (Wolfram Atlas, wolframscience.com,
projecteuclid.org, direct arxiv.org, ddlab.org); Martin–Odlyzko–Wolfram (1984), Jen (1986, 1988),
Wuensche–Lesser (1992) and Mairesse–Marcovici (2014) were not read.

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

**Rule 154 under noise:** *not found*, apart from one row of Bagnoli et al.'s Table 2 at L = 17 (1688
attractors, S = S* = 1, no discussion). Powley and Stepney (2009, J. Cellular Automata 4:125–136, §5.2,
read) place 154 as the only nonlinear rule in the group of the linear rules by the even/odd alternation of
the automorphism count of its transition graph, and name the shared Sierpiński pattern from a single seed.
That rule 154 is reversible for odd N is stated by Nobe and Yura (2004, Proposition 1) according to a search
snippet only (not read); Lemma P below proves bijectivity at odd n independently. No conjugacy or factor map
between 154 and rule 90, and no statement on 154 at n = 2^k, was found (in this study, every block map of width at most 4
that intertwines rule 154 with a radius-1 rule maps it onto rule 154 or 166, its own symmetry class;
no factor onto an additive rule exists at these widths [computed, `factor_search.csv`]).

**Rule 90 at n = 2^k** (used in Proposition R154): NKS p. 963 (read) gives the fraction of states on cycles
for rules 60 and 90 as 2^(−2^IntegerExponent[n,2]), which for n = 2^k leaves only the null state; the
nilpotency is also proved directly in v0.2 (Proposition 1) and here.

**Radius and modified coradius.** Ellison (2000, Rev. Econ. Stud. 67:17–45, doi 10.1111/1467-937X.00119),
read in the January 1999 working-paper version (theorem numbers of that version): radius R(Ω), coradius,
modified coradius CR*(Ω) (path cost minus the radii of the intermediate limit sets), and Theorem 2: if
R(Ω) > CR*(Ω) for a union Ω of limit sets, the long-run stochastically stable set is contained in Ω.
