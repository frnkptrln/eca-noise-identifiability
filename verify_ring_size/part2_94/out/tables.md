### Table 1. Exhaustive tests of the lemmas (`check_lemmas.py` -> `out/check_lemmas.json`)

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| L1 | Lemma 1 (freezing), every state | 3..20 | 2097144 states | 0 |
| L2 | Lemma 2 (fully frozen = block word, fixed), every state | 3..20 | 1123 fully frozen states among 2097144 | 0 |
| L3a | Lemma 3 (growth move), every state that is not fully frozen | 5..16 | 130685 states | 0 |
| L3b | Corollary 3 (edge of G1 to a cycle with larger frozen set), every periodic state that is not fully frozen; frozen set constant on every cycle | 5..20 | 32176 periodic states (12600 cycles) | 0 |
| L4 | Lemma 4 (swap), every block word, every occurrence | 5..30 | 51068 occurrences | 0 |
| L5 | Lemma 5 (merge), every block word, every occurrence | 6..30 | 38549 occurrences | 0 |
| L6 | Lemma 6 (every flip of the crystal heals; healing time [3]) | 6..99 (step 3) | 1680 flips | 0 |
| C2 | Corollary 2 (one flip of the crystal meets codes 0, 1, 2, 4, 7) | 6..99 (step 3) | 32 ring sizes | 0 |

All tests passed: True. CPU time 3.39 s, peak memory 122 MB.

### Table 2. G1 and its closed classes computed directly, 3 | n (`g1_classes.py` -> `out/g1_classes.jsonl`)

| n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | closed classes = the three crystal phases | cycles with no G1 path to the crystal | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|
| 6 | 9 | 12 | 15 | 9 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 9 | 31 | 58 | 189 | 5 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 12 | 147 | 348 | 1628 | 14 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 15 | 509 | 1189 | 6705 | 5 | 3 [1, 1, 1] | True | 0 | 0.00 | 55 |
| 18 | 1881 | 4998 | 32820 | 44 | 3 [1, 1, 1] | True | 0 | 0.02 | 62 |
| 21 | 6927 | 18988 | 132573 | 5 | 3 [1, 1, 1] | True | 0 | 0.10 | 121 |
| 24 | 26475 | 80116 | 601304 | 74 | 3 [1, 1, 1] | True | 0 | 0.61 | 428 |
| 27 | 101407 | 323383 | 2598588 | 5 | 3 [1, 1, 1] | True | 0 | 3.91 | 2946 |

For comparison, 3 not dividing n (same script): n = 5: 11 cycles, closed classes [11]; n = 7: 22 cycles, closed classes [22]; n = 8: 27 cycles, closed classes [27]; n = 10: 73 cycles, closed classes [67]; n = 11: 78 cycles, closed classes [77]; n = 13: 209 cycles, closed classes [208]; n = 14: 320 cycles, closed classes [317]; n = 16: 747 cycles, closed classes [746]; n = 17: 1191 cycles, closed classes [1190]; n = 19: 2832 cycles, closed classes [2831]; n = 20: 4513 cycles, closed classes [4477]; n = 22: 10827 cycles, closed classes [10793]; n = 23: 16952 cycles, closed classes [16951].

Cross-check with the sealed blind sample (`crosscheck_sample.py` -> `out/crosscheck_sample.json`): numbers of cycles, periodic states, G1 edges and the closed-class sizes compared for n = 8..22 (15 ring sizes); all agree: True.

### Table 3. The chain of the proof, executed and checked step by step (`constructive_paths.py` -> `out/constructive_paths.json`)

| part | n | start cycles | all chains end on a crystal phase | longest chain (flips) | mean | max growth steps | max swap flips | max merges |
|---|---|---|---|---|---|---|---|---|
| A: every cycle | 6 | 9 | True | 1 | 0.67 | 1 | 0 | 1 |
| A: every cycle | 9 | 31 | True | 3 | 1.84 | 2 | 0 | 1 |
| A: every cycle | 12 | 147 | True | 10 | 4.39 | 3 | 6 | 2 |
| A: every cycle | 15 | 509 | True | 14 | 6.58 | 4 | 10 | 2 |
| A: every cycle | 18 | 1881 | True | 19 | 8.53 | 4 | 14 | 3 |
| A: every cycle | 21 | 6927 | True | 25 | 10.80 | 6 | 18 | 3 |
| B: cycles reached from 200 random states | 24 | 200 | True | 26 | 10.54 | 5 | 22 | 4 |
| B: cycles reached from 200 random states | 27 | 200 | True | 31 | 12.21 | 4 | 26 | 4 |
| B: cycles reached from 200 random states | 30 | 200 | True | 35 | 13.49 | 5 | 30 | 4 |
| B: cycles reached from 200 random states | 45 | 200 | True | 57 | 24.20 | 8 | 50 | 6 |
| B: cycles reached from 200 random states | 60 | 200 | True | 67 | 34.58 | 7 | 62 | 7 |
| B: cycles reached from 200 random states | 99 | 200 | True | 108 | 62.27 | 12 | 98 | 12 |
| B: cycles reached from 200 random states | 150 | 200 | True | 153 | 97.05 | 14 | 136 | 19 |
| B: cycles reached from 200 random states | 300 | 200 | True | 283 | 201.20 | 23 | 244 | 32 |
| C: all-zero state and doubled words | 6 | 17 | True | 1 | 1.00 | 1 | 0 | 0 |
| C: all-zero state and doubled words | 18 | 21 | True | 18 | 4.86 | 3 | 14 | 2 |
| C: all-zero state and doubled words | 30 | 21 | True | 26 | 12.81 | 3 | 20 | 4 |
| C: all-zero state and doubled words | 42 | 21 | True | 50 | 24.76 | 2 | 44 | 6 |
| C: all-zero state and doubled words | 54 | 21 | True | 59 | 30.81 | 3 | 50 | 8 |
| C: all-zero state and doubled words | 66 | 21 | True | 75 | 36.48 | 2 | 66 | 10 |
| C: all-zero state and doubled words | 90 | 21 | True | 76 | 47.52 | 3 | 62 | 14 |
| C: all-zero state and doubled words | 150 | 21 | True | 155 | 98.52 | 3 | 136 | 24 |
| C: all-zero state and doubled words | 300 | 1 | True | 51 | 51.00 | 1 | 0 | 50 |

Part A total: 9504 cycles, of which 18 are the crystal phases themselves (chain of length 0). 
Part C start periods (period: count; None = longer than the search bound): n = 6: 1: 1, 2: 16; n = 18: 1: 1, 14: 20; n = 30: 1: 1, 30: 20; n = 42: 1: 1, 126: 20; n = 54: 1: 1, 1022: 20; n = 66: 1: 1, 62: 20; n = 90: 1: 1, 8190: 20; n = 150: 1: 1, None: 20; n = 300: 1: 1.
CPU time 15.38 s, peak memory 185 MB.

Total CPU time of the three scripts as recorded in their output files: 24.0 s.
