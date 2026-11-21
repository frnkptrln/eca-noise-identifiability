#!/usr/bin/env bash
# Build ring_size_paper.pdf.
#   1. make_numbers.py   numbers.tex, table_kstar.tex, numbers.json from the data files of the repository
#   2. make_figures.py   figures/*.pdf by simulation
#   3. pdflatex, BibTeX (style plain), pdflatex, pdflatex in a temporary folder; only the PDF is copied back
#
# Usage: ./build.sh [OUTDIR]        (default OUTDIR: this folder; test_paper.py passes a temporary folder)
# Environment: PYTHON (default python3), PDFLATEX (default pdflatex).
# BibTeX: bibtex is used if it and plain.bst are installed; otherwise pybtex with its built-in style plain
# (pip install pybtex).  The two differ slightly in the formatting of the list of references.
# The paper needs only: article, fontenc, lmodern, geometry, amsmath, graphicx, array, enumitem, microtype, xcolor,
# theorem, hyperref.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="${1:-$HERE}"
PY="${PYTHON:-python3}"
TEX="${PDFLATEX:-pdflatex}"
export PYTHONDONTWRITEBYTECODE=1
command -v "$TEX" >/dev/null || { echo "build.sh: no $TEX on PATH" >&2; exit 2; }

mkdir -p "$OUT"
B="$(mktemp -d "${TMPDIR:-/tmp}/ring_size_paper.XXXXXX")"
trap 'rm -rf "$B"' EXIT

"$PY" "$HERE/make_numbers.py" --outdir "$B"
if [ "$OUT" = "$HERE" ]; then
  cp "$B/numbers.tex" "$B/table_kstar.tex" "$B/numbers.json" "$HERE/"
  "$PY" "$HERE/make_figures.py"
fi
cp "$HERE/ring_size_paper.tex" "$HERE/refs.bib" "$B/"
cp -R "$HERE/figures" "$B/figures"

cd "$B"
run_tex() { "$TEX" -interaction=nonstopmode -halt-on-error ring_size_paper.tex >"$B/tex.out" 2>&1 \
            || { tail -n 40 "$B/tex.out" >&2; exit 1; }; }
run_tex
if command -v bibtex >/dev/null && kpsewhich plain.bst >/dev/null 2>&1; then
  bibtex ring_size_paper >"$B/bib.out" 2>&1 || { cat "$B/bib.out" >&2; exit 1; }
elif command -v pybtex >/dev/null; then
  pybtex -l python ring_size_paper.aux >"$B/bib.out" 2>&1 || { cat "$B/bib.out" >&2; exit 1; }
else
  echo "build.sh: neither bibtex with plain.bst nor pybtex found" >&2; exit 2
fi
run_tex
run_tex
if grep -a -q "LaTeX Warning: There were undefined references\|LaTeX Warning: Citation .* undefined" ring_size_paper.log; then
  grep -a "undefined" ring_size_paper.log >&2; exit 1
fi
cp ring_size_paper.pdf "$OUT/ring_size_paper.pdf"
if [ "$OUT" != "$HERE" ]; then cp ring_size_paper.log "$OUT/ring_size_paper.log"; fi   # the log only for the test
echo "built $OUT/ring_size_paper.pdf"
