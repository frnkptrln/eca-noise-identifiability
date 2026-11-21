# verify_paper/

Code and output of the verification of `paper/ring_size_paper.tex` (branch `paper-ring-size`, HEAD c926271),
20 November 2026. The report is `VERIFICATION_paper.md` at the root of the repository. Everything here was written
for that verification, from the definitions and statements of the paper, without reading any script of the
repository. Text files only.

## Run

    python3 verify_paper/run_all.py

from the root of the repository. Needs Python 3 with numpy and scipy, and a C compiler reachable as `cc`. About
15 minutes on a laptop, at most 2 threads, about 9 GB of memory at the largest system (rule 154, n = 20; lower the
first argument of T03 in `run_all.py` to 18 to stay below 1 GB). One test alone: `python3 verify_paper/run_all.py
paper T05`, or `python3 verify_paper/T05_rule94_theorem.py 12` with the arguments named in the head of each file.
Nothing is written outside `verify_paper/out/` and the system's temporary directory.

## Files

| file | content |
|---|---|
| `vp_core.py` | the engine: map F, cycles, V(C, C'), R(C -> D_v), gamma for every root, k_v, G1, closed classes. The inner loops are C; the C source is a string in this file, compiled at run time into the temporary directory and run as a separate program. A pure Python/numpy version of every routine is in the same file |
| `T00_engine.py` | C against numpy; in-tree weights against enumeration and against a per-root Chu-Liu/Edmonds |
| `T01_section2.py` | Lemmas 2.2 to 2.7 and Theorem 2.8 on all 256 rules, n = 3..12 |
| `T02_rule154_lemmas.py` | Lemmas 3.2 to 3.8 |
| `T03_rule154_theorems.py` | Theorems 3.9 to 3.11 from the definitions, n = 3..20 |
| `T04_rule94_lemmas.py` | Lemmas 3.29 to 3.42, Proposition A.1 |
| `T05_rule94_theorem.py` | Theorem 3.43 and Remark 3.44 from the definitions, n = 3..21 |
| `T06_rules43_142.py` | Section 3.2, every statement |
| `T07_rule26.py` | Section 5 and Appendix B, every statement |
| `T08_table1.py` | Table 1 recounted and recomputed (reads `paper/table_kstar.tex`, `paper/numbers.tex` and the csv files of T03, T05, T06, T07) |
| `T09_section6.py` | computed and proved statements of Section 6 on small rings |
| `T10_mutation.py` | the tests run with wrong rules and wrong statements; each must fail |
| `T11_certificates.py` | the potentials without Edmonds' algorithm (explicit in-trees and a lower bound) |
| `run_all.py` | runs T00 to T11 and writes `out/run_all.txt` |
| `out/T??.txt` | summary of each test; `out/T??_stdout.txt` every line; `out/*.csv` tables (one row per ring size or system); `out/run_all.txt` exit codes and times of the final run |
| `own_findings_before_comparison.md` | my findings as written down before the reports of the reading sub-sessions were collected and before `paper/REFEREE_NOTES.md` was opened |
| `reading/*.md` | the reports of the six reading sub-sessions (other instances of Claude), unchanged: paper against sources, statement by statement, and the paper's statements about itself. Their findings were audited before they went into the report; where they and the report differ, the report holds |

Claude
