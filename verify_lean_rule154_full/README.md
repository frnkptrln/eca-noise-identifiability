# verify_lean_rule154_full

Scripts for `VERIFICATION_lean_rule154_full.md`. They are an independent Python model of the Lean definitions
(`lean/RingSize/TheoremA/Statement.lean`, `lean/RingSize/Rule154/Statement.lean`,
`lean/RingSize/Rule154/StatementMain.lean`). They use no code from the repository and need only `networkx`. Run each
one from this directory, one at a time and in one process. Set `export PYTHONPATH=.` first.

| Script | Checks | Output | Time |
|---|---|---|---|
| `model.py` | the definitions (module, no output) | — | — |
| `theorems.py` | `Theorem_3_9`, `Theorem_3_10`, `Theorem_3_11`, n = 1..12; writes `out/model_k_values.csv` | `out/theorems.txt` | 14 s |
| `lemmas.py` | `Lemma_3_5` to `Lemma_3_8_b` and the paper's fuller forms, n = 1..12; R and G_1 cross-checks | `out/lemmas.txt` | 2 s |
| `lemma_3_4_b.py` | `Lemma_3_4_b_zero` and the paper's all-cell form, even n ≤ 24 | `out/lemma_3_4_b.txt` | < 1 s |
| `n16.py` | `Theorem_3_9` (a)–(f) at n = 4, 8, 16, with G_1 from the criterion of Lemma 2.3 | `out/n16.txt` | < 1 s |
| `sweep_compare.py <path to data/fw_sweep.csv>` | comparison with the rule-154 records (run after `theorems.py`) | `out/sweep_compare.txt` | < 1 s |

Example: `python theorems.py > out/theorems.txt`.

Claude
