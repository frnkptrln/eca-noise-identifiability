### Table 1. Exhaustive tests of the lemmas (`check_lemmas_94.py` -> `out/check_lemmas_94.json`)

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| L7 | Lemma 7 (windows): boundary cells are frozen ones, width <= n-3, F^t = identity on the frozen set and = phi^t on every window, t = 1..10; every state with non-empty frozen set that is not fully frozen | 5..14 | 26454 | 0 |
| L8 | Lemma 8 (live window orbits): the periodic unfrozen orbits of the window map are {A_w, B_w} for w = 2 mod 3, the 3-cycle 0000, 1001, 1111 for w = 4, and none otherwise; all 2^w window states | w = 1..22 | 8388606 | 0 |
| L7c | Lemma 7(c): a state with non-empty frozen set is periodic iff all its window contents are phi-periodic; every state with non-empty frozen set | 5..16 | 112255 | 0 |
| L9 | Lemma 9: a periodic state with empty frozen set is 0 or has only runs of even length; their number is 1 for odd n and 2(2^(n/2 - 2^e) - 1) + 1 for even n = 2^(e+1) q, q odd (n >= 5); every periodic state | 3..20 | 1230 | 0 |
| T1 | Theorem 1 (periodic states): a state is periodic iff it is 0, or a doubled word with periodic half word, or has non-empty frozen set and only live windows; every state | 3..16 | 131064 | 0 |
| T1b | Theorem 1, direction "periodic implies the description"; every periodic state | 17..20 | 28285 | 0 |
| L10 | Lemma 10 (reversible freezing): in every state of the cycle whose first window is not 1001, the flip named in the lemma gives a periodic state of another cycle with a strictly larger frozen set; every cycle with non-empty frozen set that is not a block word | 5..20 | 11356 | 0 |
| L11 | Lemma 11 (swap, both directions): x + e_(p+2) and x + e_(p+3) form a 2-cycle and x + e_(p+2) + e_(p+3) is the block word with the two blocks exchanged; every block word, every pair of consecutive blocks short, long | 5..24 | 7343 | 0 |
| L12 | Lemma 12 (merge): F(x + e_(p+3)) is the block word with the three short blocks replaced by two long ones; every block word, every triple of consecutive short blocks | 6..24 | 5543 | 0 |
| L13 | Lemma 13 (split): x + e_(p+2) has period 2; five steps after flipping the cell p+6 of its other state the block word with short, long, long replaced by four short blocks is reached; every block word, every occurrence of short, long, long | 8..24 | 3156 | 0 |
| L16 | Lemma 16 (basin of 0): if 8 does not divide n, the states whose orbit ends in 0 are exactly 0, 1^n and the cyclic words over the blocks 001 and 0011 (case = one state of the basin of 0, or one such word) | 5..20 (8 not dividing n) | 544 | 0 |
| LW | Lemma W: every cell outside the window is frozen, F^t = identity outside and = phi^t inside, t = 1..6; every block word, every admissible window of width <= 7, every content (case = one content) | 5..13 | 62082 | 0 |
| L16a | Lemma 16 (i), (ii), (iii): F(x) = 0 iff x is 0 or 1^n; F(x) = 1^n iff x is a word over 001 and 0011; F(z) is such a word only if 8 divides n; every state (case = one state) | 3..16 | 131064 | 0 |

All tests passed: True. CPU time 88.01 s.

Live window orbits found (test L8), by width: w = 2: {00, 11}; w = 4: {0000, 1001, 1111}; w = 5: {00111, 11100}; w = 8: {00111100, 11100111}; w = 11: {00111100111, 11100111100}; w = 14: {00111100111100, 11100111100111}; w = 17: {00111100111100111, 11100111100111100}; w = 20: {00111100111100111100, 11100111100111100111}.

Numbers of periodic states with empty frozen set (test L9), by n: 3: 1, 4: 1, 5: 1, 6: 7, 7: 1, 8: 1, 9: 1, 10: 31, 11: 1, 12: 31, 13: 1, 14: 127, 15: 1, 16: 1, 17: 1, 18: 511, 19: 1, 20: 511.

### Table 2. G1 and its closed classes computed directly, 3 not dividing n (`g1_classes_94.py` -> `out/g1_classes_94.jsonl`)

| n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | block words | block words in one strong component | cycles with 101 in K | cycles without 101 in K ({0} included) | cycles of doubled words in K | periods of the cycles without 101 in K (period: count) | periods of the cycles without 101 outside K | {0} in K | G1 edges into {0} | codes on K | K = cycles reachable from the block words | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 3 | 3 | 4 | 2 | 1 [2] | 2 | True | 2 of 2 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [2, 5] | True | 0.0 | 53 |
| 5 | 11 | 16 | 55 | 1 | 1 [11] | 5 | True | 10 of 10 | 1 of 1 | 0 of 0 | {'1': 1} | - | True | 5 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 7 | 22 | 43 | 147 | 1 | 1 [22] | 7 | True | 21 of 21 | 1 of 1 | 0 of 0 | {'1': 1} | - | True | 7 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 8 | 27 | 43 | 146 | 1 | 1 [27] | 10 | True | 26 of 26 | 1 of 1 | 0 of 0 | {'1': 1} | - | True | 8 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 10 | 73 | 158 | 610 | 7 | 1 [67] | 17 | True | 67 of 67 | 0 of 6 | 0 of 5 | - | {'1': 1, '6': 5} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.0 | 53 |
| 11 | 78 | 144 | 638 | 2 | 1 [77] | 22 | True | 77 of 77 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.01 | 53 |
| 13 | 209 | 404 | 2145 | 2 | 1 [208] | 39 | True | 208 of 208 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.02 | 54 |
| 14 | 320 | 871 | 4284 | 4 | 1 [317] | 51 | True | 310 of 310 | 7 of 10 | 7 of 9 | {'14': 7} | {'1': 1, '14': 2} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.04 | 54 |
| 16 | 747 | 1723 | 10130 | 2 | 1 [746] | 90 | True | 746 of 746 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.15 | 55 |
| 17 | 1191 | 3112 | 18088 | 2 | 1 [1190] | 119 | True | 1190 of 1190 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.3 | 57 |
| 19 | 2832 | 7677 | 48773 | 2 | 1 [2831] | 209 | True | 2831 of 2831 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 1.14 | 68 |
| 20 | 4513 | 12498 | 86322 | 37 | 1 [4477] | 277 | True | 4467 of 4467 | 10 of 46 | 10 of 45 | {'12': 10} | {'1': 1, '6': 5, '12': 30} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 2.25 | 85 |
| 22 | 10827 | 33388 | 237886 | 35 | 1 [10793] | 486 | True | 10793 of 10793 | 0 of 34 | 0 of 33 | - | {'1': 1, '62': 33} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 0.92 | 182 |
| 23 | 16952 | 48301 | 358846 | 2 | 1 [16951] | 644 | True | 16951 of 16951 | 0 of 1 | 0 of 0 | - | {'1': 1} | False | 0 | [0, 1, 2, 3, 4, 5, 6, 7] | True | 1.73 | 376 |

K denotes the closed class (unique in every row). n = 4 is listed for comparison only; the theorems need n >= 5.

### Table 3. The chains of the proofs, executed step by step (`chains_94.py` -> `out/chains_94.json`)

Part A: every cycle. Growth flip for the cycles without 101, freezing chain to a block word (every flip joins two periodic states), and the digraph of swaps, merges and splits on the block words with every move executed.

| n | cycles | cycles with 101 | growth flips | all chains end on a block word | max freezing flips | mean freezing flips | block words | moves executed | move graph strongly connected | max flips from a block word to l^b0 s^a0 | max flips from l^b0 s^a0 to a block word |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 11 | 10 | 1 | True | 1 | 0.55 | 5 | 10 | True | 4 | 4 |
| 7 | 22 | 21 | 1 | True | 2 | 1.05 | 7 | 14 | True | 6 | 6 |
| 8 | 27 | 26 | 1 | True | 2 | 0.89 | 10 | 32 | True | 5 | 6 |
| 10 | 73 | 67 | 6 | True | 2 | 1.1 | 17 | 60 | True | 7 | 8 |
| 11 | 78 | 77 | 1 | True | 3 | 1.29 | 22 | 77 | True | 7 | 8 |
| 13 | 209 | 208 | 1 | True | 3 | 1.56 | 39 | 169 | True | 8 | 9 |
| 14 | 320 | 310 | 10 | True | 4 | 1.77 | 51 | 224 | True | 8 | 10 |
| 16 | 747 | 746 | 1 | True | 4 | 2.06 | 90 | 464 | True | 10 | 12 |
| 17 | 1191 | 1190 | 1 | True | 5 | 2.16 | 119 | 646 | True | 10 | 12 |
| 19 | 2832 | 2831 | 1 | True | 5 | 2.48 | 209 | 1273 | True | 11 | 14 |
| 20 | 4513 | 4467 | 46 | True | 6 | 2.55 | 277 | 1780 | True | 11 | 14 |
| 22 | 10827 | 10793 | 34 | True | 6 | 2.86 | 486 | 3432 | True | 13 | 16 |
| 23 | 16952 | 16951 | 1 | True | 7 | 3.03 | 644 | 4761 | True | 13 | 16 |

Part B: cycles reached from 200 random states; freezing chain, sorting and merging down to l^b0 s^a0, chain to the cycle with the code 000 (Lemma 15).

| n | start states | all chains end on the cycle with code 000 | max freezing flips | max sorting and merging flips | mean flips |
|---|---|---|---|---|---|
| 25 | 200 | True | 5 | 51 | 28.23 |
| 26 | 200 | True | 5 | 58 | 32.22 |
| 31 | 200 | True | 6 | 78 | 43.55 |
| 40 | 200 | True | 6 | 120 | 72.43 |
| 50 | 200 | True | 7 | 181 | 110.56 |
| 64 | 200 | True | 9 | 283 | 175.55 |
| 100 | 200 | True | 13 | 685 | 421.35 |
| 200 | 200 | True | 23 | 2561 | 1675.88 |
| 301 | 200 | True | 27 | 5128 | 3764.47 |

Part C. Lemma 15, chain from l^b0 s^a0 to the cycle with a width-4 window in the state 0000, executed for n = 7 and 10..300, 3 not dividing n (195 ring sizes): all executed: True; flips: [2] for n = 1 mod 3, [4] for n = 2 mod 3.

Chains into {0} for n = 5, 7, 8 (a periodic state that is joined to a block word by flips between periodic states; one flip; the orbit then reaches 0):

| n | periodic state (cell 0 first) | its period | flipped cell | steps until 0 | orbit after the flip | flips between periodic states from the block word | block word |
|---|---|---|---|---|---|---|---|
| 5 | 01111 | 2 | 0 | 1 | - | 1 | 01101 |
| 7 | 0111111 | 3 | 0 | 1 | - | 2 | 0101101 |
| 8 | 01111010 | 2 | 5 | 4 | 01111110 -> 11000011 -> 01100110 -> 11111111 -> 00000000 | 2 | 01101011 |

CPU time of `chains_94.py`: 171.11 s.

### Table 4. Comparison with data already in the repository (`crosscheck_data.py` -> `out/crosscheck_data.json`)

| compared with | ring sizes n | fields compared | disagreements |
|---|---|---|---|
| data/ring_size/mechanisms.csv | 8, 10, 11, 13, 14, 16, 17, 19, 20, 22 | cycles; selected cycles = size of the closed class; gamma_min = m - 1; k_c = 0 for all c; k* = 0 | 0 |
| verify_ring_size/part2_94/out/g1_classes.jsonl | 5, 7, 8, 10, 11, 13, 14, 16, 17, 19, 20, 22, 23 | cycles; periodic states; G1 edges; strong components; closed-class sizes | 0 |
