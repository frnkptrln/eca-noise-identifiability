# verify_lean_theorem_a

Scripts for `VERIFICATION_lean_theorem_a.md`: a check of `lean/RingSize/TheoremA/Statement.lean` against Section 2
of `paper/ring_size_paper.tex`. They model the Lean definitions literally in Python and use no code from the
repository. Run each from this directory with `python <script>.py` (Python 3 with networkx; one process).

| Script | Output | What it does |
|---|---|---|
| `lean_defs.py` | — | literal model of the definitions (sInf ∅ = 0, truncated subtraction, parent-map in-trees) |
| `instance.py` | — | all objects for one (rule, n) and the checks of the 17 statements |
| `small_cases.py` | `out/small_cases.txt` | rules 204, 90, 154 at n = 3, 4 |
| `sweep.py [fw_sweep.csv]` | `out/sweep_n1_6.csv`, `out/sweep_summary.txt` | all 256 rules, n = 1..6, and comparison with `data/fw_sweep.csv` (about 90 s) |
| `alternatives.py` | `out/alternatives.txt` | alternative readings of R, IsInTree and the rule numbering |
| `examples.py [fw_sweep.csv]` | `out/examples.txt` | examples quoted in the report (run after `sweep.py`) |
| `rule_tables.py` | `out/rule_tables.txt` | `ruleOfNumber` against the local rules written out in the paper |

Claude
