# Rule identifiability in elementary cellular automata under dynamical noise

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23399101.svg)](https://doi.org/10.5281/zenodo.23399101)

Exact computation (no sampling, no seeds) of how well the rule of an elementary cellular
automaton on a ring of 12 cells can be identified from a trajectory when the dynamics is
corrupted by independent bit flips with probability ε per cell and step.

* `note/note.pdf` — the note (English, with all 88 rule classes tabulated in the appendix)
* `code/` — the computation (Python 3, NumPy, SciPy for one sparse matrix, pandas and matplotlib for tables and figures)
* `data/` — every data file the note is built from, with `MANIFEST.sha256`
* `VERIFICATION.md` — report of the independent verification session (its findings A1–A10 are fixed in this version)
* `reproduce.sh` — regenerates `data/`, the figures, `note/numbers.tex`, `note/table_classes.tex` and the PDF

Repository: https://github.com/frnkptrln/eca-noise-identifiability · DOI: https://doi.org/10.5281/zenodo.23399100 (all versions) · https://doi.org/10.5281/zenodo.23399101 (v0.1) · License: CC BY 4.0 (`LICENSE`), covering the note, the data and the code.

Cite as: Peterlein, F. (2026). *Rule identifiability in elementary cellular automata under dynamical noise* (v0.1). Zenodo. https://doi.org/10.5281/zenodo.23399100

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
