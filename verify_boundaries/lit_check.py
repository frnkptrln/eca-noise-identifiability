"""Download the open copies of the sources of Section 1 of report_boundaries.md and print where each cited
statement is (PDF page; arXiv/journal page in brackets). PDFs are kept in ./lit (not committed).
    python3 verify_boundaries/lit_check.py > verify_boundaries/out/lit_locations.txt"""
import os, re, subprocess, pypdf
SRC = {
 'MdR2015': ('https://inmabb.criba.edu.ar/revuma/pdf/v56n1/v56n1a06.pdf', 106),   # pdf page k = journal page 106+k
 'VT2026': ('https://arxiv.org/pdf/2502.10898v2', 0),
 'Tadaki1994': ('https://arxiv.org/pdf/cond-mat/9305012v1', 0),
 'Bhattacharjee2020': ('https://arxiv.org/pdf/1607.02291', 0),
 'Wang2025': ('https://arxiv.org/pdf/2402.05404v2', 0),
 'Miekisz2008': ('https://arxiv.org/pdf/q-bio/0703062v1', 0)}
CHECKS = [
 ('MdR2015', r'Proposition 3\.1\. The elementary'), ('MdR2015', r'if and only if the\s*number of cells'),
 ('MdR2015', r'4\. The reversibility of linear'), ('MdR2015', r'Reversibility of ECA 60'), ('MdR2015', r'Reversibility of ECA 102'),
 ('MdR2015', r'ECA 150 is reversible if n'),
 ('VT2026', r'Theorem 3\.4\.If'), ('VT2026', r'Theorem 3\.6\.For'), ('VT2026', r'Theorem 5\.1\.If'), ('VT2026', r'Theorem 6\.2\.Consider'),
 ('VT2026', r'Lemma B\.3\.For'), ('VT2026', r'usually\s*does not work'),
 ('Tadaki1994', r'\(2\.4c\)'), ('Tadaki1994', r'N = 3n \+ 2 there appear'), ('Tadaki1994', r'TABLE I\. Periodicity'), ('Tadaki1994', r'\n32 U'),
 ('Bhattacharjee2020', r'3\.3 Reachability tree'), ('Bhattacharjee2020', r'Fig\. 6: Reachability Tree'),
 ('Wang2025', r'Theorem 1\. FCA'), ('Wang2025', r'Theorem 2\. If'), ('Wang2025', r'Theorem 3\. If'), ('Wang2025', r'Theorem 4\. If'), ('Wang2025', r'Theorem 5\. The'),
 ('Wang2025', r'Wolfram number 11110000'), ('Wang2025', r'Table 1\. List of reversibility'),
 ('Miekisz2008', r'7 Stochastic dynamics of ﬁnite populations'), ('Miekisz2008', r'or any other inﬁnite graph'), ('Miekisz2008', r'only absorbing states can be stochastically'),
 ('Miekisz2008', r'Example\s*6\s*Players'), ('Miekisz2008', r'located\s+on\s+the\s+circle'), ('Miekisz2008', r'Example\s*9\s*Players')]
os.makedirs('lit', exist_ok=True); T = {}
for k, (u, off) in SRC.items():
    f = f'lit/{k}.pdf'
    if not os.path.exists(f): subprocess.run(['curl', '-sSL', '-o', f, u], check=True)
    T[k] = [p.extract_text() or '' for p in pypdf.PdfReader(f).pages]
for k, pat in CHECKS:
    hits = [i + 1 for i, t in enumerate(T[k]) if re.search(pat, t)]
    off = SRC[k][1]
    print(f'{k:18s} {pat!r:45s} pdf page(s) {hits}' + (f'  (journal pages {[h + off for h in hits]})' if off else ''))
