<!-- TABLE_A -->
| n | periodic states | cycles | G1 edges | out-degree of {0} | every cycle reaches {0} | max G1 distance to {0} | G1 strongly connected | lemma tests run / failed |
|---|---|---|---|---|---|---|---|---|
| 3 | 8 | 3 | 4 | 1 | yes | 2 | yes | 2 / 0 |
| 4 | 10 | 4 | 8 | 0 | yes | 2 | no | 14 / 0 |
| 5 | 32 | 4 | 6 | 1 | yes | 3 | yes | 2 / 0 |
| 6 | 56 | 12 | 77 | 3 | yes | 3 | yes | 11 / 0 |
| 7 | 128 | 8 | 28 | 1 | yes | 4 | yes | 2 / 0 |
| 8 | 226 | 31 | 434 | 0 | yes | 4 | no | 14 / 0 |
| 9 | 512 | 18 | 152 | 1 | yes | 5 | yes | 2 / 0 |
| 10 | 992 | 62 | 1117 | 5 | yes | 5 | yes | 11 / 0 |
| 11 | 2048 | 50 | 884 | 1 | yes | 6 | yes | 2 / 0 |
| 12 | 4000 | 308 | 9824 | 6 | yes | 6 | yes | 11 / 0 |
| 13 | 8192 | 156 | 4190 | 1 | yes | 7 | yes | 2 / 0 |
| 14 | 16256 | 564 | 19149 | 7 | yes | 7 | yes | 11 / 0 |
| 15 | 32768 | 510 | 18098 | 1 | yes | 8 | yes | 2 / 0 |
| 16 | 65026 | 4081 | 221202 | 0 | yes | 8 | no | 14 / 0 |
<!-- END -->

<!-- TABLE_A2 -->
| n | size of M | (2^(n/2)-1)^2 | cycles in M | F^n = id on M | distance histogram (distance: cycles) | distance of the all-ones cycle | distance = min-parity bound for all cycles |
|---|---|---|---|---|---|---|---|
| 4 | 9 | 9 | 3 | yes | 0: 1, 1: 2, 2: 1 | 2 | yes |
| 8 | 225 | 225 | 30 | yes | 0: 1, 1: 16, 2: 11, 3: 2, 4: 1 | 4 | yes |
| 16 | 65025 | 65025 | 4080 | yes | 0: 1, 1: 480, 2: 1384, 3: 1344, 4: 666, 5: 176, 6: 27, 7: 2, 8: 1 | 8 | no |
<!-- END -->

<!-- TABLE_S -->
| n | sampled states of M | F(x) in M | F^n(x) = x | descent: intermediate states tested / periodic | descents ending in 0 within n/2 steps |
|---|---|---|---|---|---|
| 32 | 2000 | 2000 | 2000 | 88 / 88 | 20 of 20 |
| 64 | 1000 | 1000 | 1000 | 220 / 220 | 20 of 20 |
| 128 | 300 | 300 | 300 | 517 / 517 | 20 of 20 |
| 256 | 100 | 100 | 100 | 890 / 890 | 20 of 20 |
| 512 | 30 | 30 | 30 | 3484 / 3484 | 20 of 20 |
| 1024 | 10 | 10 | 10 | 2913 / 2913 | 10 of 10 |
<!-- END -->

<!-- TABLE_B -->
| n | cycles | closed classes: sizes | 0 in closed class | CB in closed class | out-neighbours of {0} | out-degree of CB | smallest out-neighbour of CB (rep) | fate of the defect orbit | cycles with a G1 path to CB | CB has a G1 path to {0} | codes missing on the closed class |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 4 | [4] | yes | yes | CB only | 2 | `0111` | other (transient 0, period 2) | 4 | yes | [1, 4] |
| 6 | 5 | [2] | yes | yes | CB only | 1 | `000000` | zero (transient 3, period 1) | 5 | yes | [1, 3, 4, 6, 7] |
| 8 | 8 | [8] | yes | yes | CB only | 4 | `00000111` | other (transient 2, period 6) | 8 | yes | none |
| 10 | 27 | [25] | no | no | CB only | 5 | `0000011011` | other (transient 3, period 4) | 2 | no | [2] |
| 12 | 21 | [19] | yes | yes | CB only | 6 | `000000000111` | other (transient 4, period 14) | 21 | yes | none |
| 14 | 46 | [2] | yes | yes | CB only | 1 | `00000000000000` | zero (transient 7, period 1) | 46 | yes | [1, 3, 4, 6, 7] |
| 16 | 80 | [38] | yes | yes | CB only | 8 | `0000000000000111` | other (transient 6, period 14) | 80 | yes | none |
| 18 | 167 | [99] | no | no | CB only | 9 | `000000000000011011` | other (transient 7, period 12) | 2 | no | [2] |
| 20 | 289 | [287] | yes | yes | CB only | 10 | `00000000000000000111` | other (transient 8, period 62) | 289 | yes | none |
| 22 | 466 | [365] | yes | yes | CB only | 11 | `0000000000000110000011` | other (transient 9, period 8) | 466 | yes | none |
| 24 | 641 | [132] | yes | yes | CB only | 12 | `000000000000000000000111` | other (transient 10, period 126) | 641 | yes | none |
| 26 | 1506 | [1363] | yes | yes | CB only | 13 | `00000000000000000000011011` | other (transient 11, period 28) | 1506 | yes | none |
<!-- END -->

<!-- TABLE_B2 -->
- defect orbit ends on **zero**: n = 6, 14, 30, 62
- defect orbit ends on **checkerboard**: n = (none)
- defect orbit ends on **other**: n = 4, 8, 10, 12, 16, 18, 20, 22, 24, 26, 28, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 64, 66, 68, 70, 74, 76, 78, 80, 82, 84, 86, 88, 90, 94, 98, 100
- defect orbit ends on **undetermined**: n = 72, 92, 96
- undetermined cases: cycle not closed within 400000 steps; 0 or CB met within these steps: n = 72: no, n = 92: no, n = 96: no
<!-- END -->

<!-- TABLE_B3 -->
| n (odd) | cycles | closed classes: sizes | 0 in closed class | out-degree of {0} | codes missing on the closed class |
|---|---|---|---|---|---|
| 5 | 6 | [6] | yes | 5 | [2] |
| 7 | 1 | [1] | yes | 0 | [1, 2, 3, 4, 5, 6, 7] |
| 9 | 19 | [19] | yes | 9 | [2] |
| 11 | 25 | [24] | no | 11 | [2] |
| 13 | 29 | [16] | yes | 13 | [2] |
| 15 | 51 | [1] | yes | 0 | [1, 2, 3, 4, 5, 6, 7] |
| 17 | 120 | [86] | yes | 17 | [2] |
| 19 | 229 | [95] | no | 19 | [2] |
| 21 | 379 | [358] | yes | 21 | [2] |
| 23 | 509 | [230] | no | 23 | [2] |
| 25 | 899 | [244] | yes | 25 | [2] |
<!-- END -->

<!-- TABLE_C -->
| n | n mod 3 | cycles | closed classes: sizes | transient cycles | cycles carrying 111 | of these in the closed class | transient cycles = 111-carriers outside the closed class | codes missing on the closed class | smallest 111-carrier in the closed class (rep) |
|---|---|---|---|---|---|---|---|---|---|
| 4 (2^k) | 1 | 1 | [1] | 0 | 0 | 0 | yes | [1, 2, 3, 4, 5, 6, 7] | - |
| 5 | 2 | 3 | [3] | 0 | 1 | 1 | yes | none | `00111` |
| 6 | 0 | 7 | [7] | 0 | 0 | 0 | yes | [7] | - |
| 7 | 1 | 3 | [3] | 0 | 0 | 0 | yes | [7] | - |
| 8 (2^k) | 2 | 10 | [1] | 9 | 1 | 0 | no | [1, 2, 3, 4, 5, 6, 7] | - |
| 9 | 0 | 5 | [5] | 0 | 0 | 0 | yes | [7] | - |
| 10 | 1 | 19 | [18] | 1 | 1 | 0 | yes | [7] | - |
| 11 | 2 | 12 | [12] | 0 | 3 | 3 | yes | none | `00001010011` |
| 12 | 0 | 64 | [64] | 0 | 0 | 0 | yes | [7] | - |
| 13 | 1 | 27 | [25] | 2 | 2 | 0 | yes | [7] | - |
| 14 | 2 | 76 | [76] | 0 | 2 | 2 | yes | none | `00100100100111` |
| 15 | 0 | 68 | [67] | 1 | 1 | 0 | yes | [7] | - |
| 16 (2^k) | 1 | 552 | [1] | 551 | 3 | 0 | no | [1, 2, 3, 4, 5, 6, 7] | - |
| 17 | 2 | 148 | [148] | 0 | 3 | 3 | yes | none | `00100100100100111` |
| 18 | 0 | 567 | [566] | 1 | 1 | 0 | yes | [7] | - |
| 19 | 1 | 390 | [385] | 5 | 5 | 0 | yes | [7] | - |
| 20 | 2 | 2816 | [2815] | 1 | 4 | 3 | yes | none | `00100100100100100111` |
| 21 | 0 | 1115 | [1111] | 4 | 4 | 0 | yes | [7] | - |
| 22 | 1 | 3695 | [3684] | 11 | 13 | 2 | yes | none | `0000101001000111010011` |
| 23 | 2 | 3142 | [3141] | 1 | 5 | 4 | yes | none | `00100100100100100100111` |
| 24 | 0 | 33606 | [33594] | 12 | 12 | 0 | yes | [7] | - |
| 25 | 1 | 8772 | [8757] | 15 | 15 | 0 | yes | [7] | - |
| 26 | 2 | 28748 | [28742] | 6 | 10 | 4 | yes | none | `00100100100100100100100111` |
<!-- END -->

<!-- TABLE_C2 -->
- for every n in 4..26 that is not a power of two, the transient cycles are exactly the 111-carrying cycles outside the closed class: True
- n in 4..26 with a 111-carrying cycle in the closed class (k* = 0): [5, 11, 14, 17, 20, 22, 23, 26]
- rule 26, 5-blocks x_(i-2..i+2) whose image has 111 at i-1..i+1: ['10011']
<!-- END -->

<!-- TABLE_COST -->
| script | CPU seconds | source of the figure |
|---|---|---|
| check_lemmas.py (n = 3..16) | 0.50 | out/check_lemmas.txt |
| cross_check.py (solver for n = 4..7 and comparison) | 0.01 | out/cross_check.txt |
| sample_large_n.py (n = 32..1024) | 1.28 | out/sample_large_n.jsonl (cumulative, last record) |
| cb_defect_122.py (even n = 4..256, fate up to 100) | 2.2 | out/cb_defect_122.txt |
| explore_122_26.py, n = 4..20 (sum of the per-case figures) | 0.3 | out/explore_122_26.jsonl |
| explore_122_26.py, n = 21..24 (sum of the per-case figures) | 4.8 | out/explore_122_26.jsonl |
| explore_122_26.py, n = 25..26 (sum of the per-case figures) | 14.3 | out/explore_122_26.jsonl |
<!-- END -->
