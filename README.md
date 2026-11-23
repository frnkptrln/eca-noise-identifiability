# Rule identifiability in elementary cellular automata under dynamical noise

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23399100.svg)](https://doi.org/10.5281/zenodo.23399100)

Exact computation (no sampling, no seeds) of how well the rule of an elementary cellular
automaton on a ring of 12 cells can be identified from a trajectory when the dynamics is
corrupted by independent bit flips with probability ε per cell and step.

* `paper/ring_size_paper.pdf` — the ring-size paper (version 0.4; its own record: https://doi.org/10.5281/zenodo.24482170): for which ring sizes small noise selects cycles that leave part of the rule table unused, proved for rules 154, 43, 142 and 94, in part for rule 26
* `note/note_v0.2.pdf` — the note, version 0.2 (English, with all 88 rule classes tabulated in the appendix); `note/note.pdf` is version 0.1
* `code/` — the computation (Python 3, NumPy, SciPy for one sparse matrix, pandas and matplotlib for tables and figures)
* `data/` — every data file the note is built from, with `MANIFEST.sha256`
* `VERIFICATION.md` — report of the independent verification session (its findings A1–A10 are fixed in this version)
* `reproduce.sh` — regenerates `data/`, the figures, `note/numbers.tex`, `note/table_classes.tex` and the PDF

Repository: https://github.com/frnkptrln/eca-noise-identifiability · DOI: https://doi.org/10.5281/zenodo.23399100 (all versions) · https://doi.org/10.5281/zenodo.23399101 (v0.1) · https://doi.org/10.5281/zenodo.24093547 (v0.2) · https://doi.org/10.5281/zenodo.24275024 (v0.3) · https://doi.org/10.5281/zenodo.24482529 (v0.4) · License: CC BY 4.0 (`LICENSE`), covering the note, the data and the code.

Cite as: Peterlein, F. (2026). *Rule identifiability in elementary cellular automata under dynamical noise* (v0.4). Zenodo. https://doi.org/10.5281/zenodo.23399100

Cite the ring-size paper as: Peterlein, F. (2026). *Noise-selected cycles of elementary cellular automata and the arithmetic of the ring size*. Zenodo. https://doi.org/10.5281/zenodo.24482170

## In plain words

An elementary cellular automaton is a row of cells, each 0 or 1. At every step each cell looks at itself and its
two neighbours and takes its new value from a fixed table with eight entries, one for each thing it can see. The
table is the rule. Here the row is closed to a ring: there is no first and no last cell.

Left alone, such a system ends in a loop: one pattern, or a short sequence of patterns, that repeats for ever. A
rule usually has many loops, and where the system starts decides which one it ends in.

Now disturb it a little: at every step each cell is flipped by mistake with a small probability. The system no
longer stays in one loop, because now and then an error throws it into another. But it does not divide its time
evenly. The rarer the errors, the more of its time it spends in a few loops: those that are hard to leave and easy
to reach (in the text: the cycles of least stochastic potential, the noise-selected cycles).

Why this matters here: someone who only watches the patterns can work out the rule, but only those of the eight
table entries that the patterns use. If the selected loops use all eight, the rule can be read off quickly, and the
more quickly the rarer the errors. If they leave an entry unused, the watcher learns it only from the rare
excursions, and more slowly the rarer the errors are. The number k* of the note is 0 in the first case and at least
1 in the second.

The ring-size paper (`paper/ring_size_paper.pdf`) shows that for some rules the outcome depends on the number of
cells, and on its arithmetic rather than its size: for rule 154 on whether the number of cells is a power of two,
for rules 43 and 142 on whether it is divisible by 4, for rule 94 on whether it is divisible by 3. In each case
there is one special pattern: stripes of period 4 or 3, which fit on the ring only when the period divides the
number of cells, or the all-zero pattern, which recovers from every single error exactly when the number of cells
is a power of two. Where the stripes fit, or where the all-zero pattern recovers, the noise selects that pattern,
and it leaves table entries unused. Add or remove one cell, and other loops win.

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
that contains all of them. The paper is also archived as a record of its own, https://doi.org/10.5281/zenodo.24482170,
where it can be read without the repository. The note itself is unchanged: `note/note_v0.2.pdf` is the current text.

* `paper/ring_size_paper.pdf` — *Noise-selected cycles of elementary cellular automata and the arithmetic of the ring size* (32 pages). k* = 1 iff n is a power of two for rule 154 (n ≥ 3); iff 4 divides n for rules 43 and 142 (n ≥ 4); for rule 94, k* = 1 if 3 divides n (n ≥ 6) and k* = 0 if not (n ≥ 5); for rule 26 on 2^k cells the zero state is the only selected cycle, k* is 1 or 2 for k ≥ 3 and 1 for odd k. Not peer reviewed
* `paper/` — source, bibliography, the scripts that write every number and both figures (`build.sh`), `test_paper.py`, `TRACE.md` (every statement mapped to its source), `REFEREE_NOTES.md`
* `proofs_43_142/`, `proofs_94_26/` — the proof documents with their scripts and outputs; `literature_addendum.md` — literature for rules 43, 142 and 154
* `VERIFICATION_43_142.md`, `VERIFICATION_94_26.md`, `VERIFICATION_paper.md` with `verify_43_142/`, `verify_94_26/`, `verify_paper/` — independent verification of each proof document and of the paper; the header of each report says how every finding was handled
* `reader_checks/` — the conclusions of the theorems recomputed on small rings with separate code

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
