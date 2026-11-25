# Rule identifiability in elementary cellular automata under dynamical noise

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23399100.svg)](https://doi.org/10.5281/zenodo.23399100)

Exact computation (no sampling, no seeds) of how well the rule of an elementary cellular
automaton on a ring of 12 cells can be identified from a trajectory when the dynamics is
corrupted by independent bit flips with probability ε per cell and step.

* `paper/ring_size_paper.pdf` — the ring-size paper (version 2; its own record: https://doi.org/10.5281/zenodo.24482169): for which ring sizes small noise selects cycles that leave part of the rule table unused, proved for rules 154, 43, 142 and 94, in part for rule 26
* `report_boundaries.md` — the same question on a row with walls instead of a ring (version 0.6): computed for rows up to 20 cells, proved for the additive rules 60, 90 and 150
* `note/note_v0.2.pdf` — the note, version 0.2 (English, with all 88 rule classes tabulated in the appendix); `note/note.pdf` is version 0.1
* `code/` — the computation (Python 3, NumPy, SciPy for one sparse matrix, pandas and matplotlib for tables and figures)
* `data/` — every data file the note is built from, with `MANIFEST.sha256`
* `VERIFICATION.md` — report of the independent verification session (its findings A1–A10 are fixed in this version)
* `reproduce.sh` — regenerates `data/`, the figures, `note/numbers.tex`, `note/table_classes.tex` and the PDF

Repository: https://github.com/frnkptrln/eca-noise-identifiability · DOI: https://doi.org/10.5281/zenodo.23399100 (all versions; the single versions are listed there) · License: CC BY 4.0 (`LICENSE`), covering the note, the data and the code.

Cite as: Peterlein, F. (2026). *Rule identifiability in elementary cellular automata under dynamical noise* (v0.6). Zenodo. https://doi.org/10.5281/zenodo.23399100

Cite the ring-size paper as: Peterlein, F. (2026). *Noise-selected cycles of elementary cellular automata and the arithmetic of the ring size*. Zenodo. https://doi.org/10.5281/zenodo.24482169

## In plain words

An elementary cellular automaton is a row of cells, each 0 or 1. At every step each cell looks at itself and its
two neighbours and takes its new value from a fixed table with eight entries, one for each thing it can see. The
table is the rule. Here the row is closed to a ring: there is no first and no last cell.

Left alone, such a system ends in a loop: one pattern, or a sequence of patterns, that repeats for ever. A
rule usually has many loops, and where the system starts decides which one it ends in.

Now disturb it a little: at every step each cell is flipped by mistake with a small probability. The system no
longer stays in one loop, because now and then an error throws it into another. But it does not divide its time
evenly. The rarer the errors, the more of its time it spends in some of the loops (in the text: the cycles of least
stochastic potential, the noise-selected cycles). Which loops these are, and how many, depends on the rule and on
the number of cells.

Why this matters here: someone who only watches the patterns can work out the rule, but only those of the eight
table entries that the patterns use. If the selected loops use all eight, the rule can be read off quickly, and the
more quickly the rarer the errors. If they leave an entry unused, the watcher learns it only from the rare
excursions, and more slowly the rarer the errors are. The number k* of the note is 0 in the first case and at least
1 in the second. (This is the result of the note, which the paper quotes; the paper itself proves statements about
k*.)

The ring-size paper (`paper/ring_size_paper.pdf`) shows that for some rules the outcome depends on the number of
cells, and on its arithmetic rather than its size: for rule 154 on whether the number of cells is a power of two,
for rules 43 and 142 on whether it is divisible by 4, for rule 94 on whether it is divisible by 3 (from five or
six cells on; on four cells rule 94 is an exception). In each case
there is one special pattern: stripes of period 4 or 3, which fit on the ring only when the period divides the
number of cells, or the all-zero pattern, which recovers from every single error exactly when the number of cells
is a power of two. Where the stripes fit (from four cells on for rules 43 and 142, from six cells on for rule 94),
or where the all-zero pattern recovers, the noise selects that pattern, and it leaves table entries unused. Add or
remove one cell, and this is no longer so: the stripes do not fit, and for rule 154 every loop is selected, the
all-zero pattern included.

This section is a summary without formulas. The statements, their ranges and their proofs are in the paper.

## What is computed

* **ε = 0:** for all 256 rules × 4096 initial states the orbit is followed until it closes;
  this gives the closure time τ, the set of neighbourhood codes seen, and the consistent class
  of rules (`zero_noise_per_state.csv.gz`, `zero_noise_per_rule.csv`).
* **ε > 0, stationary:** for every rule and every ε on a 17-point grid, the stationary law of the
  4096-state chain by a dense linear solve, verified by power iteration from three initial laws;
  the expected neighbourhood counts ν_c and the identifiability rate ρ = λ(ε)·min_c ν_c
  (`stationary_rates.csv`). The best noise level ε* per class by golden-section search
  (`epsilon_star.csv`).
* **ε > 0, finite horizon:** the exact evidence margin against the hardest alternative from every
  initial state for T ∈ {8,16,32,64} and six noise levels (`finite_horizon_per_rule.csv`,
  `finite_horizon_per_state.csv.gz`).
* **Boundary check:** three radius-2 generators scored by the radius-1 observer
  (`radius2_boundary.csv`, `radius2_zero_noise.csv`).
* **Affine rules:** bijectivity, GF(2) rank and the Walsh-basis check of uniform three-cell marginals
  for the 16 affine rules (`additive_rules.csv`).

## Reproduce

    ./reproduce.sh

About two hours on two CPU cores; `pdflatex` is needed for the PDF. Every number in the note
is a LaTeX macro written by `code/make_numbers.py` from the CSV files — nothing is typed by hand.

## Version 0.2: noise-selected cycles

<!-- v02:begin (generated by code/fw/make_report.py) -->
* `report.md` — exact small-noise orders: noise-selected cycles, k_c and k* for all 88 classes at n = 4..20; checked certificates for n = 12 and n = 4..14, none for n = 15..20; for n ≥ 8, 13 classes change side with n; verification and the comparison with v0.1
* `PREDICTIONS.md` — predictions sealed before the solver was written (first commit of the branch)
* `literature.md` — literature note with read/not-read status per source
* `note/note_v0.2.tex`, `note/note_v0.2.diff`, `note/numbers_v02.tex`, `note/table_classes_v02.tex` — v0.2 of the note, built as `note/note_v0.2.pdf` (v0.1 files unchanged)
* `code/fw/` — solver, verifiers, certificate checker, tests; `reproduce_v02.sh` regenerates the v0.2 data and report from scratch (run after `reproduce.sh`; `REUSE_CHECKPOINTS=1` resumes from the committed sweep checkpoint and the GTH caches instead)
* `VERIFICATION_v02.md`, `verify_v02/` — independent verification of v0.2 (own code, sealed sample, outputs, logs) and how each finding was handled
<!-- v02:end -->

## Version 0.3: ring-size study

Version 0.2 found 13 classes whose small-noise order k* changes side with the ring size n. Version 0.3
adds a study of why. The note itself is unchanged: `note/note_v0.2.pdf` is the current text.

* `report_ring_size.md` — the report. Mechanisms computed for n ≤ 22: in ten of the 13 classes the selected cycle at the switching sizes is a spatially periodic crystal that exists only when its period divides n, or the zero state, which cannot be left with one flip exactly when a single flip dies out on the ring; classes 37, 45 and 73 are not covered. Proved for all n by the independent verification: for rule 154, k* = 1 iff n is a power of two (n ≥ 3); for class 94, k* = 1 at every n ≥ 6 divisible by 3. The proofs are not peer reviewed; what is not proved is listed in the report
* `PREDICTIONS_ring_size.md` — predictions sealed before any new computation (first commit of the branch)
* `literature_ring_size.md` — literature review with read/not-read status per source
* `code/ring_size/`, `data/ring_size/` (with its own `MANIFEST.sha256`), `figures/ring_size/` — mechanism analysis, data and figures; `reproduce_ring_size.sh` regenerates them and the report
* `VERIFICATION_ring_size.md`, `verify_ring_size/` — independent verification (sealed blind sample, own solver, 31 findings, the two proofs) and how each finding was handled

## Version 0.4: the ring-size paper

Version 0.3 proved the dependence on the ring size for rule 154 and, in one direction, for class 94. Version 0.4
adds the proofs for rules 43 and 142, the other direction for rule 94, a partial result for rule 26, and a paper
that contains all of them. The paper is also archived as a record of its own, https://doi.org/10.5281/zenodo.24482169,
where it can be read without the repository. The note itself is unchanged: `note/note_v0.2.pdf` is the current text.

* `paper/ring_size_paper.pdf` — *Noise-selected cycles of elementary cellular automata and the arithmetic of the ring size* (32 pages). k* = 1 iff n is a power of two for rule 154 (n ≥ 3); iff 4 divides n for rules 43 and 142 (n ≥ 4); for rule 94, k* = 1 if 3 divides n (n ≥ 6) and k* = 0 if not (n ≥ 5); for rule 26 on 2^k cells the zero state is the only selected cycle, k* is 1 or 2 for k ≥ 3 and 1 for odd k. Not peer reviewed
* `paper/` — source, bibliography, the scripts that write every number and both figures (`build.sh`), `test_paper.py`, `TRACE.md` (every statement mapped to its source), `REFEREE_NOTES.md`
* `proofs_43_142/`, `proofs_94_26/` — the proof documents with their scripts and outputs; `literature_addendum.md` — literature for rules 43, 142 and 154
* `VERIFICATION_43_142.md`, `VERIFICATION_94_26.md`, `VERIFICATION_paper.md` with `verify_43_142/`, `verify_94_26/`, `verify_paper/` — independent verification of each proof document and of the paper; the header of each report says how every finding was handled
* `reader_checks/` — the conclusions of the theorems recomputed on small rings with separate code

## Version 0.5: sources and corrections

No new mathematics. Version 0.5 contains version 2 of the ring-size paper.

* The corrections made after the verification of the paper were checked by a separate session
  (`VERIFICATION_corrections.md`). It found no false statement in a proof. It found one false clause and several
  inexact sentences in what the paper says about itself, and two sentences of the section "In plain words" above
  that are false when read literally; these are corrected.
* Young (1993), which the paper cited as not read, was read in full by a session (`literature_addendum.md`, update
  of 24 November 2026). Seven texts could not be obtained; the paper cites them after a source that was read, and
  it no longer says that Theorem 2.8 restates results of Samuelson and of Nöldeke and Samuelson, only that
  secondary descriptions say so.
* `paper/TRACE.md`, Part G, lists every change of version 2.

## Version 0.6: open boundaries

Everything before this version is computed on a ring. Version 0.6 adds a study of the same question on a row of n
cells whose two outer neighbours are held at 0 (null walls) and, more briefly, on a row with reflecting walls. The
note and the ring-size paper are unchanged.

In plain words: on the ring, the answer for some rules depends on the arithmetic of the ring size. With walls none
of those conditions survives unchanged. Two survive shifted by one. The period-3 pattern of rule 94 is selected
when 3 divides n + 1 (computed for rows of 8 to 20 cells, not proved), and the power-of-two effect of rule 90
appears exactly when n + 1 is a power of two (proved for every row of at least 4 cells). For the rules whose
selected patterns travel around the ring (43, 142, 35) the dependence on the size disappears: at every size
computed (4 to 16 cells) none of their cycles contains some neighbourhoods, so as the noise vanishes those entries
of the rule table are seen ever more rarely. The walls also create dependences on the size that the ring does not
have, for instance on n mod 3 (rules 37, 91, 75) or on the parity of n (rules 135, 137); these are computed for
rows up to 20 cells and not proved. Holding the walls at 1 instead of 0 is the same as exchanging 0 and 1 in the
rule, in its inputs and in its output.

* `report_boundaries.md` — the report. Under null walls only reflection remains a symmetry, so the 256 rules form 160 classes. Computed: all 160 classes for n = 4..16, the 12 classes that change side for n = 17..20, reflecting walls for n = 4..12, each compared with the ring. Proved for every row of at least 4 cells: the additive rules 60, 90 and 150 and their complements (rule 60: k* = 0; rule 90: k* ≥ 1 exactly when n + 1 is a power of two; rule 150: k* ≥ 1 only at n = 5). Every other statement is tagged as computed or observed
* `PREDICTIONS_boundaries.md` — predictions sealed before the first computation under walls (sha256 in the report); of the session's own 28 items 17 were correct, 5 partly correct and 6 wrong
* `literature_boundaries.md` — literature on elementary cellular automata with fixed boundaries; only sources read in that session
* `code/fw/*boundaries*.py` and the boundary option in `code/fw/fwlib.py` (the ring is the default and is guarded by `code/fw/test_boundaries.py`), `data/boundaries/` (with its own `MANIFEST.sha256`) — computation, data and certificates; Section 9 of the report lists the commands
* `VERIFICATION_boundaries.md`, `verify_boundaries/` — independent verification with own code: every proof it checked is correct, every number it recomputed agrees, 28 findings on the text around the results; its header says how each was handled
* `reader_checks/walls/` — a further recomputation with separate code (all records of the null and reflecting tables), described in `reader_checks/README.md`

The changes made to the report after the verification were not verified in turn.

## Conventions

States are integers 0..4095, bit i is cell i (indices mod 12). A rule is its Wolfram number:
the successor of cell i is bit 4·x_{i−1}+2·x_i+x_{i+1} of the rule. Noise: X_{t+1} = F(X_t) XOR Z_t
with Z_t i.i.d. Bernoulli(ε) per cell. Natural logarithms throughout (rates in nats per step).

## Statement on the use of AI

Definitions, code, computation, figures and text were produced by Claude (Anthropic) in
sessions directed by Frank Peterlein on 4 and 15 October 2026. A separate Claude session that had
not seen the work recomputed samples of every quantity from the definitions, checked every number
in the text against the data files and read the proofs; its report is `VERIFICATION.md`, and its
findings were corrected before release. The author selected the question, set the scope, and is
responsible for the content.

Versions 0.2 (8 and 9 November 2026) and 0.3 (13 to 15 November 2026) were produced in the same way,
each with its own independent verification session (`VERIFICATION_v02.md`, `VERIFICATION_ring_size.md`).
For version 0.3 the verification session also proved the two statements that hold for all n; its proofs
were read a second time, with separate code, in a further Claude session.

Version 0.4 (17 to 23 November 2026) was produced in the same way: the proofs and the paper in sessions directed
by the author, each proof document and then the paper verified by a separate session that had not seen the work.
Claude, in the conversation in which the sessions were planned, read the proof documents and the paper, recomputed
the conclusions on small rings (`reader_checks/`) and worked the findings of the verifications into the texts; the
corrections made after the last verification were not verified in turn. The paper has its own statement with the
detail.

Version 0.5 (24 November 2026): one separate session checked those corrections, another read sources; Claude, in
the conversation named above, worked the findings of both into the paper and this file. These last changes were
not checked again.

Version 0.6 (24 and 25 November 2026) was produced in the same way: the study of open boundaries in one session,
its verification in a separate session that had not seen the work. Claude, in the conversation named above, had
written the task, recomputed the tables with separate code (`reader_checks/walls/`), applied the patches of the
session as commits and worked the findings of the verification into the report; that last pass was not verified.
