#!/usr/bin/env bash
# Regenerates every data file, figure, number and the PDF of the note. ~1 h on 2 cores.
set -euo pipefail
cd "$(dirname "$0")"
python3 code/run_zero_noise.py
python3 code/run_finite_horizon.py
python3 code/run_radius2.py
python3 code/check_additive.py
python3 code/run_stationary.py --rules reps --check yes
python3 code/run_refine.py
python3 code/run_stationary.py --rules rest --check no      # symmetry check: all 256 rules
python3 code/make_numbers.py
python3 code/make_figures.py
cd note && pdflatex -interaction=nonstopmode note.tex >/dev/null && pdflatex -interaction=nonstopmode note.tex >/dev/null
echo "done: note/note.pdf"
