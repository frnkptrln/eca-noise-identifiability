### Table 1. Exhaustive tests of the lemmas (`check_lemmas.py` -> `out/check_lemmas.json`)

Rules 184 and 226 are the wall rules of rules 43 and 142. Every test runs over all objects of the kind named in the column `cases` at every ring size of the column `n`.

| test | statement tested | rule | n | cases | violations |
|---|---|---|---|---|---|
| L1 | Lemma 1: cell-change formula and delta(F x) = G(delta x) | 43 | 3..20 | 2097144 states | 0 |
| L1 | Lemma 1: cell-change formula and delta(F x) = G(delta x) | 142 | 3..20 | 2097144 states | 0 |
| L2 | Lemma 2: the wall rule conserves the number of ones | 184 | 3..20 | 2097144 wall words | 0 |
| L3 | Lemma 3: the sets P and Q after one step; \|P\| and \|Q\| drop by the number of annihilating patterns; \|P\| - \|Q\| = 2\|d\| - n | 184 | 3..20 | 2097144 wall words | 0 |
| L2 | Lemma 2: the wall rule conserves the number of ones | 226 | 3..20 | 2097144 wall words | 0 |
| L3 | Lemma 3: the sets P and Q after one step; \|P\| and \|Q\| drop by the number of annihilating patterns; \|P\| - \|Q\| = 2\|d\| - n | 226 | 3..20 | 2097144 wall words | 0 |
| L4 | Lemma 4: a wall word is periodic iff it has no 11 or no 00; the wall rule is then a shift | 184 | 3..20 | 2097144 wall words | 0 |
| L4 | Lemma 4: a wall word is periodic iff it has no 11 or no 00; the wall rule is then a shift | 226 | 3..20 | 2097144 wall words | 0 |
| L5 | Lemma 5: F commutes with the complement and conserves the wall count; the wall count is even | 43 | 3..20 | 2097144 states | 0 |
| L6 | Lemma 6: a flip changes the wall count by +2 (interior cell), -2 (isolated cell), 0 (otherwise) | 43 | 3..20 | 39845880 (state, cell) pairs | 0 |
| L7 | Lemma 7: a state is periodic iff it has no isolated cell or no interior cell; F is then a shift or a shift followed by the complement | 43 | 3..20 | 2097144 states | 0 |
| L5 | Lemma 5: F commutes with the complement and conserves the wall count; the wall count is even | 142 | 3..20 | 2097144 states | 0 |
| L6 | Lemma 6: a flip changes the wall count by +2 (interior cell), -2 (isolated cell), 0 (otherwise) | 142 | 3..20 | 39845880 (state, cell) pairs | 0 |
| L7 | Lemma 7: a state is periodic iff it has no isolated cell or no interior cell; F is then a shift or a shift followed by the complement | 142 | 3..20 | 2097144 states | 0 |
| L7c | Lemma 7(c): for a periodic state u and every r, sigma^r u lies on the cycle of u or on the cycle of the complement of u | 43 | 3..20 | 1376544 (periodic state, r) pairs | 0 |
| L7c | Lemma 7(c): for a periodic state u and every r, sigma^r u lies on the cycle of u or on the cycle of the complement of u | 142 | 3..20 | 1376544 (periodic state, r) pairs | 0 |
| L8b | Lemma 8, last sentence: a state whose wall word has neither 11 nor 00 exists only for 4 \| n and is then one of the four rotations of (0011)^(n/4) | 43 | 3..20 | 20 such states | 0 |
| L8 | Lemma 8: for 4 \| n the periodic states with n/2 walls are the four rotations of (0011)^(n/4); they form one cycle of length 4 on which F is the left shift | 43 | 4..20 (step 4) | 20 periodic states with n/2 walls | 0 |
| L8b | Lemma 8, last sentence: a state whose wall word has neither 11 nor 00 exists only for 4 \| n and is then one of the four rotations of (0011)^(n/4) | 142 | 3..20 | 20 such states | 0 |
| L8 | Lemma 8: for 4 \| n the periodic states with n/2 walls are the four rotations of (0011)^(n/4); they form one cycle of length 4 on which F is the left shift | 142 | 4..20 (step 4) | 20 periodic states with n/2 walls | 0 |
| T2s | step of Theorem 1(2): a periodic state with w < n/2 has an interior cell and every flip of an interior cell ends on a cycle with w + 2 walls; with w > n/2: isolated cell, w - 2 | 43 | 3..20 | 651148 (periodic state, admissible cell) pairs | 0 |
| T2s | step of Theorem 1(2): a periodic state with w < n/2 has an interior cell and every flip of an interior cell ends on a cycle with w + 2 walls; with w > n/2: isolated cell, w - 2 | 142 | 3..20 | 651148 (periodic state, admissible cell) pairs | 0 |
| T1 | Theorem 1(1) and Proposition 2: every flip of every state of X keeps n/2 walls and is back on X after exactly 1 or n/2 - 1 steps; X has the codes 1, 3, 4, 6; its one-flip neighbours have 0, 2, 5, 7 | 43 | 4..400 (step 4) | 80800 flips | 0 |
| T1 | Theorem 1(1) and Proposition 2: every flip of every state of X keeps n/2 walls and is back on X after exactly 1 or n/2 - 1 steps; X has the codes 1, 3, 4, 6; its one-flip neighbours have 0, 2, 5, 7 | 142 | 4..400 (step 4) | 80800 flips | 0 |
| E | Proposition 3: the least total resistance from a cycle C to X equals \|w(C) - n/2\| / 2 (shortest paths over all states: a step of F costs 0, a flip costs 1) | 43 | 4..20 (step 4) | 1889 cycles | 0 |
| E | Proposition 3: the least total resistance from a cycle C to X equals \|w(C) - n/2\| / 2 (shortest paths over all states: a step of F costs 0, a flip costs 1) | 142 | 4..20 (step 4) | 1897 cycles | 0 |
| L9 | Lemma 9(b): from a periodic state on the lower (upper) level a flip leads to a cycle on the same level or on the upper (lower) level | 43 | 5..19, 12 sizes | 38760 (periodic state, cell) pairs | 0 |
| L10 | consequence of Lemma 10 used in Theorem 2: the cycles of one level are connected by slides (single flips between periodic states of the level) once x is identified with its complement | 43 | 5..19, 12 sizes | 10064 ordered slide pairs | 0 |
| L9 | Lemma 9(b): from a periodic state on the lower (upper) level a flip leads to a cycle on the same level or on the upper (lower) level | 142 | 5..19, 12 sizes | 38760 (periodic state, cell) pairs | 0 |
| L10 | consequence of Lemma 10 used in Theorem 2: the cycles of one level are connected by slides (single flips between periodic states of the level) once x is identified with its complement | 142 | 5..19, 12 sizes | 10064 ordered slide pairs | 0 |
| L9b | Lemma 9 (a), (c), (d): states of the lower (upper) level have an interior (isolated) cell and no isolated (interior) cell; every cycle of a level has a G1 edge to the other level; every cycle has a G1 path into the two levels | 43 | 5..19, 12 sizes | 4773 periodic states of the levels, cycles of the levels and cycles | 0 |
| L9b | Lemma 9 (a), (c), (d): states of the lower (upper) level have an interior (isolated) cell and no isolated (interior) cell; every cycle of a level has a G1 edge to the other level; every cycle has a G1 path into the two levels | 142 | 5..19, 12 sizes | 4791 periodic states of the levels, cycles of the levels and cycles | 0 |
| L10s | Lemma 10, first statement: if a flip leads from a periodic state to a periodic state with the same wall count, their cycles are equal or joined by G1 edges in both directions | 43 | 3..20 | 497440 slides | 0 |
| L10s | Lemma 10, first statement: if a flip leads from a periodic state to a periodic state with the same wall count, their cycles are equal or joined by G1 edges in both directions | 142 | 3..20 | 497440 slides | 0 |
| L10a | Lemma 10(a): the procedure, from every state without isolated cell and with w >= 2 walls, for every cut: every step is a slide and the final run lengths are (n - 2w + 2, 2, ..., 2) | 43 | 3..16 | 22952 (state, cut) pairs | 0 |
| L10b | Lemma 10(b): the procedure, from every state without interior cell and with n/2 < w < n walls, for every cut and two choices of the pair: every step is a slide and lowers the number of inversions by one; the final run lengths are (2, ..., 2, 1, ..., 1) | 43 | 3..16 | 119808 (state, cut, choice) triples | 0 |
| L10a | Lemma 10(a): the procedure, from every state without isolated cell and with w >= 2 walls, for every cut: every step is a slide and the final run lengths are (n - 2w + 2, 2, ..., 2) | 142 | 3..16 | 22952 (state, cut) pairs | 0 |
| L10b | Lemma 10(b): the procedure, from every state without interior cell and with n/2 < w < n walls, for every cut and two choices of the pair: every step is a slide and lowers the number of inversions by one; the final run lengths are (2, ..., 2, 1, ..., 1) | 142 | 3..16 | 119808 (state, cut, choice) triples | 0 |
| L11 | Lemma 11: eps flips lead from z0 = 0^(eps+2) (1100)^((w-2)/2) 11 through periodic states of the lower level to a state on the cycle of the complement of z0; z0 has the codes 0, 1, 3, 4, 6, its complement the code 7 | 43 | 5..401, 298 sizes | 595 flips | 0 |
| L11 | Lemma 11: eps flips lead from z0 = 0^(eps+2) (1100)^((w-2)/2) 11 through periodic states of the lower level to a state on the cycle of the complement of z0; z0 has the codes 0, 1, 3, 4, 6, its complement the code 7 | 142 | 5..401, 298 sizes | 595 flips | 0 |

All tests passed: True. Return times in test T1 are exactly 1 and n/2 - 1 at every ring size: True. CPU time 43.62 s, peak memory 625 MB.

### Table 2. G1 and its closed classes computed directly, 4 | n (`g1_classes.py` -> `out/g1_classes.jsonl`)

| rule | n | cycles | periodic states | G1 edges | strong components | closed classes (sizes) | closed classes = {X} | cycles without G1 path to X | longest shortest G1 path to X | G1 distance to X = \|w - n/2\| / 2 for every cycle | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 43 | 4 | 3 | 8 | 2 | 3 | 1 [1] | True | 0 | 1 | True | 0.00 | 55 |
| 43 | 8 | 13 | 88 | 42 | 5 | 1 [1] | True | 0 | 2 | True | 0.00 | 55 |
| 43 | 12 | 61 | 644 | 400 | 7 | 1 [1] | True | 0 | 3 | True | 0.00 | 55 |
| 43 | 16 | 283 | 4408 | 3160 | 9 | 1 [1] | True | 0 | 4 | True | 0.01 | 60 |
| 43 | 20 | 1529 | 30248 | 23118 | 11 | 1 [1] | True | 0 | 5 | True | 0.08 | 124 |
| 43 | 24 | 8681 | 207364 | 161998 | 13 | 1 [1] | True | 0 | 6 | True | 0.97 | 1267 |
| 142 | 4 | 5 | 8 | 4 | 5 | 1 [1] | True | 0 | 1 | True | 0.00 | 55 |
| 142 | 8 | 15 | 88 | 30 | 7 | 1 [1] | True | 0 | 2 | True | 0.00 | 55 |
| 142 | 12 | 61 | 644 | 362 | 9 | 1 [1] | True | 0 | 3 | True | 0.00 | 56 |
| 142 | 16 | 285 | 4408 | 3060 | 11 | 1 [1] | True | 0 | 4 | True | 0.00 | 60 |
| 142 | 20 | 1531 | 30248 | 22936 | 13 | 1 [1] | True | 0 | 5 | True | 0.08 | 136 |
| 142 | 24 | 8681 | 207364 | 161858 | 15 | 1 [1] | True | 0 | 6 | True | 0.94 | 1272 |

In every row the codes on the closed class are 1, 3, 4, 6 and X is the only cycle that no single flip leaves: True. The number of strong components equals n/2 + 1 (rule 43) and n/2 + 3 (rule 142) in every row: True (an observation; not used and not proved).

### Table 3. G1 and its closed classes computed directly, 4 not dividing n (same script)

w- and w+ are the largest even number below n/2 and the smallest even number above n/2.

| rule | n | w- | w+ | cycles | cycles with w- or w+ walls | strong components | closed classes (sizes) | closed class = the cycles with w- or w+ walls, all eight codes | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|
| 43 | 3 | 0 | 2 | 3 | 3 | 1 | 1 [3] | True | 0.00 | 55 |
| 43 | 5 | 2 | 4 | 4 | 3 | 2 | 1 [3] | True | 0.00 | 55 |
| 43 | 6 | 2 | 4 | 10 | 8 | 3 | 1 [8] | True | 0.00 | 55 |
| 43 | 7 | 2 | 4 | 7 | 4 | 3 | 1 [4] | True | 0.00 | 55 |
| 43 | 9 | 4 | 6 | 15 | 9 | 4 | 1 [9] | True | 0.00 | 55 |
| 43 | 10 | 4 | 6 | 28 | 10 | 5 | 1 [10] | True | 0.00 | 55 |
| 43 | 11 | 4 | 6 | 28 | 7 | 5 | 1 [7] | True | 0.00 | 55 |
| 43 | 13 | 6 | 8 | 61 | 15 | 6 | 1 [15] | True | 0.00 | 56 |
| 43 | 14 | 6 | 8 | 126 | 16 | 7 | 1 [16] | True | 0.00 | 56 |
| 43 | 15 | 6 | 8 | 141 | 12 | 7 | 1 [12] | True | 0.00 | 57 |
| 43 | 17 | 8 | 10 | 316 | 25 | 8 | 1 [25] | True | 0.01 | 62 |
| 43 | 18 | 8 | 10 | 658 | 18 | 9 | 1 [18] | True | 0.02 | 69 |
| 43 | 19 | 8 | 10 | 739 | 17 | 9 | 1 [17] | True | 0.03 | 78 |
| 43 | 21 | 10 | 12 | 1755 | 39 | 10 | 1 [39] | True | 0.13 | 178 |
| 43 | 22 | 10 | 12 | 3620 | 24 | 11 | 1 [24] | True | 0.26 | 350 |
| 43 | 23 | 10 | 12 | 4180 | 24 | 11 | 1 [24] | True | 0.44 | 535 |
| 142 | 3 | 0 | 2 | 3 | 3 | 1 | 1 [3] | True | 0.00 | 55 |
| 142 | 5 | 2 | 4 | 5 | 3 | 3 | 1 [3] | True | 0.00 | 55 |
| 142 | 6 | 2 | 4 | 10 | 6 | 5 | 1 [6] | True | 0.00 | 55 |
| 142 | 7 | 2 | 4 | 8 | 5 | 4 | 1 [5] | True | 0.00 | 55 |
| 142 | 9 | 4 | 6 | 15 | 6 | 5 | 1 [6] | True | 0.00 | 55 |
| 142 | 10 | 4 | 6 | 30 | 12 | 7 | 1 [12] | True | 0.00 | 55 |
| 142 | 11 | 4 | 6 | 29 | 11 | 6 | 1 [11] | True | 0.00 | 55 |
| 142 | 13 | 6 | 8 | 62 | 9 | 7 | 1 [9] | True | 0.00 | 56 |
| 142 | 14 | 6 | 8 | 128 | 14 | 9 | 1 [14] | True | 0.00 | 56 |
| 142 | 15 | 6 | 8 | 141 | 21 | 8 | 1 [21] | True | 0.00 | 57 |
| 142 | 17 | 8 | 10 | 317 | 14 | 9 | 1 [14] | True | 0.01 | 62 |
| 142 | 18 | 8 | 10 | 658 | 20 | 11 | 1 [20] | True | 0.02 | 69 |
| 142 | 19 | 8 | 10 | 740 | 31 | 10 | 1 [31] | True | 0.03 | 78 |
| 142 | 21 | 10 | 12 | 1755 | 21 | 11 | 1 [21] | True | 0.12 | 178 |
| 142 | 22 | 10 | 12 | 3622 | 22 | 13 | 1 [22] | True | 0.26 | 350 |
| 142 | 23 | 10 | 12 | 4181 | 45 | 12 | 1 [45] | True | 0.47 | 538 |

Records in `out/g1_classes.jsonl`: 44 (rules 43 and 142, n = 3..24); records in which the computed closed classes are the ones stated in Theorem 1 (4 | n) or Theorem 2 (otherwise): 44. Sum of the recorded CPU times: 3.88 s; largest peak memory 1272 MB (n = 24).

### Table 4. The chains of the proofs, executed and checked step by step (`constructive_paths.py` -> `out/constructive_paths.json`)

| part | rule | n | start cycles | all chains end on the target | longest chain (flips) | mean | chains of length 0 | remarks |
|---|---|---|---|---|---|---|---|---|
| A: Theorem 1(2), every cycle | 43 | 4 | 3 | True | 1 | 0.67 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 43 | 8 | 13 | True | 2 | 1.08 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 43 | 12 | 61 | True | 3 | 1.34 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 43 | 16 | 283 | True | 4 | 1.80 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 43 | 20 | 1529 | True | 5 | 2.24 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 142 | 4 | 5 | True | 1 | 0.80 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 142 | 8 | 15 | True | 2 | 1.20 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 142 | 12 | 61 | True | 3 | 1.41 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 142 | 16 | 285 | True | 4 | 1.82 | 1 | every cycle; two choices of the flipped cell |
| A: Theorem 1(2), every cycle | 142 | 20 | 1531 | True | 5 | 2.24 | 1 | every cycle; two choices of the flipped cell |
| B: Theorem 1(2), samples | 43 | 24 | 223 | True | 6 | 1.29 | 64 | 200 random initial states and 23 structured states; 122 distinct cycles |
| B: Theorem 1(2), samples | 43 | 28 | 223 | True | 7 | 1.38 | 55 | 200 random initial states and 23 structured states; 133 distinct cycles |
| B: Theorem 1(2), samples | 43 | 32 | 223 | True | 8 | 1.63 | 50 | 200 random initial states and 23 structured states; 155 distinct cycles |
| B: Theorem 1(2), samples | 43 | 48 | 223 | True | 12 | 2.02 | 56 | 200 random initial states and 23 structured states; 156 distinct cycles |
| B: Theorem 1(2), samples | 43 | 64 | 223 | True | 16 | 2.72 | 34 | 200 random initial states and 23 structured states; 172 distinct cycles |
| B: Theorem 1(2), samples | 43 | 100 | 223 | True | 25 | 3.66 | 32 | 200 random initial states and 23 structured states; 182 distinct cycles |
| B: Theorem 1(2), samples | 43 | 200 | 223 | True | 50 | 6.34 | 24 | 200 random initial states and 23 structured states; 195 distinct cycles |
| B: Theorem 1(2), samples | 43 | 400 | 223 | True | 100 | 11.26 | 12 | 200 random initial states and 23 structured states; 211 distinct cycles |
| B: Theorem 1(2), samples | 142 | 24 | 223 | True | 6 | 1.33 | 66 | 200 random initial states and 23 structured states; 131 distinct cycles |
| B: Theorem 1(2), samples | 142 | 28 | 223 | True | 7 | 1.38 | 61 | 200 random initial states and 23 structured states; 127 distinct cycles |
| B: Theorem 1(2), samples | 142 | 32 | 223 | True | 8 | 1.53 | 50 | 200 random initial states and 23 structured states; 140 distinct cycles |
| B: Theorem 1(2), samples | 142 | 48 | 223 | True | 12 | 2.14 | 47 | 200 random initial states and 23 structured states; 165 distinct cycles |
| B: Theorem 1(2), samples | 142 | 64 | 223 | True | 16 | 2.67 | 34 | 200 random initial states and 23 structured states; 181 distinct cycles |
| B: Theorem 1(2), samples | 142 | 100 | 223 | True | 25 | 3.87 | 28 | 200 random initial states and 23 structured states; 184 distinct cycles |
| B: Theorem 1(2), samples | 142 | 200 | 223 | True | 50 | 6.32 | 24 | 200 random initial states and 23 structured states; 194 distinct cycles |
| B: Theorem 1(2), samples | 142 | 400 | 223 | True | 100 | 11.39 | 16 | 200 random initial states and 23 structured states; 207 distinct cycles |
| C: Theorem 1(2), stored initial states of `sampled_reach` | 43 | 24 | 200 | True | 3 | 0.90 | 64 | cycles of the stored initial states x0; stored path length equal / longer / shorter than the chain: 200 / 0 / 0 |
| C: Theorem 1(2), stored initial states of `sampled_reach` | 43 | 28 | 200 | True | 4 | 0.97 | 63 | cycles of the stored initial states x0; stored path length equal / longer / shorter than the chain: 200 / 0 / 0 |
| C: Theorem 1(2), stored initial states of `sampled_reach` | 43 | 32 | 200 | True | 4 | 1.05 | 51 | cycles of the stored initial states x0; stored path length equal / longer / shorter than the chain: 200 / 0 / 0 |
| C: Theorem 1(2), stored initial states of `sampled_reach` | 142 | 24 | 200 | True | 3 | 0.90 | 64 | cycles of the stored initial states x0; stored path length equal / longer / shorter than the chain: 200 / 0 / 0 |
| C: Theorem 1(2), stored initial states of `sampled_reach` | 142 | 28 | 200 | True | 4 | 0.97 | 63 | cycles of the stored initial states x0; stored path length equal / longer / shorter than the chain: 200 / 0 / 0 |
| C: Theorem 1(2), stored initial states of `sampled_reach` | 142 | 32 | 200 | True | 4 | 1.05 | 51 | cycles of the stored initial states x0; stored path length equal / longer / shorter than the chain: 200 / 0 / 0 |
| D: Theorem 2 | 43 | 5 | 4 | True | 2 | 1.50 | 0 | every cycle; most flips towards the levels 1, most slides 1, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 6 | 10 | True | 5 | 3.30 | 0 | every cycle; most flips towards the levels 1, most slides 2, chains using Lemma 11: 7 |
| D: Theorem 2 | 43 | 7 | 7 | True | 5 | 3.00 | 0 | every cycle; most flips towards the levels 1, most slides 3, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 9 | 15 | True | 5 | 2.47 | 0 | every cycle; most flips towards the levels 2, most slides 3, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 10 | 28 | True | 9 | 5.50 | 0 | every cycle; most flips towards the levels 2, most slides 6, chains using Lemma 11: 11 |
| D: Theorem 2 | 43 | 11 | 28 | True | 11 | 6.75 | 0 | every cycle; most flips towards the levels 2, most slides 9, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 13 | 61 | True | 7 | 3.77 | 0 | every cycle; most flips towards the levels 3, most slides 5, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 14 | 126 | True | 14 | 8.47 | 0 | every cycle; most flips towards the levels 3, most slides 10, chains using Lemma 11: 76 |
| D: Theorem 2 | 43 | 15 | 141 | True | 18 | 10.96 | 0 | every cycle; most flips towards the levels 3, most slides 15, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 17 | 316 | True | 10 | 5.37 | 0 | every cycle; most flips towards the levels 4, most slides 7, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 18 | 658 | True | 19 | 10.76 | 0 | every cycle; most flips towards the levels 4, most slides 14, chains using Lemma 11: 288 |
| D: Theorem 2 | 43 | 19 | 739 | True | 24 | 14.86 | 0 | every cycle; most flips towards the levels 4, most slides 21, chains using Lemma 11: 0 |
| D: Theorem 2 | 43 | 21 | 223 | True | 14 | 5.61 | 10 | 200 random initial states and 23 structured states; most flips towards the levels 5, most slides 9, chains using Lemma 11: 0; 92 distinct cycles |
| D: Theorem 2 | 43 | 22 | 223 | True | 25 | 11.73 | 3 | 200 random initial states and 23 structured states; most flips towards the levels 5, most slides 18, chains using Lemma 11: 111; 116 distinct cycles |
| D: Theorem 2 | 43 | 23 | 223 | True | 32 | 17.39 | 1 | 200 random initial states and 23 structured states; most flips towards the levels 5, most slides 27, chains using Lemma 11: 0; 104 distinct cycles |
| D: Theorem 2 | 43 | 25 | 223 | True | 16 | 6.79 | 7 | 200 random initial states and 23 structured states; most flips towards the levels 6, most slides 11, chains using Lemma 11: 0; 131 distinct cycles |
| D: Theorem 2 | 43 | 26 | 223 | True | 29 | 14.35 | 1 | 200 random initial states and 23 structured states; most flips towards the levels 6, most slides 22, chains using Lemma 11: 119; 122 distinct cycles |
| D: Theorem 2 | 43 | 27 | 223 | True | 38 | 19.33 | 3 | 200 random initial states and 23 structured states; most flips towards the levels 6, most slides 33, chains using Lemma 11: 0; 110 distinct cycles |
| D: Theorem 2 | 43 | 50 | 73 | True | 49 | 27.85 | 0 | 50 random initial states and 23 structured states; most flips towards the levels 12, most slides 46, chains using Lemma 11: 40; 55 distinct cycles |
| D: Theorem 2 | 43 | 101 | 73 | True | 73 | 33.85 | 0 | 50 random initial states and 23 structured states; most flips towards the levels 25, most slides 49, chains using Lemma 11: 0; 68 distinct cycles |
| D: Theorem 2 | 43 | 202 | 73 | True | 202 | 115.34 | 0 | 50 random initial states and 23 structured states; most flips towards the levels 50, most slides 198, chains using Lemma 11: 29; 69 distinct cycles |
| D: Theorem 2 | 142 | 5 | 5 | True | 3 | 1.80 | 0 | every cycle; most flips towards the levels 1, most slides 1, chains using Lemma 11: 4 |
| D: Theorem 2 | 142 | 6 | 10 | True | 5 | 3.20 | 0 | every cycle; most flips towards the levels 1, most slides 2, chains using Lemma 11: 8 |
| D: Theorem 2 | 142 | 7 | 8 | True | 8 | 4.75 | 0 | every cycle; most flips towards the levels 1, most slides 3, chains using Lemma 11: 7 |
| D: Theorem 2 | 142 | 9 | 15 | True | 5 | 3.07 | 0 | every cycle; most flips towards the levels 2, most slides 3, chains using Lemma 11: 8 |
| D: Theorem 2 | 142 | 10 | 30 | True | 11 | 5.80 | 0 | every cycle; most flips towards the levels 2, most slides 6, chains using Lemma 11: 18 |
| D: Theorem 2 | 142 | 11 | 29 | True | 15 | 8.38 | 0 | every cycle; most flips towards the levels 2, most slides 9, chains using Lemma 11: 18 |
| D: Theorem 2 | 142 | 13 | 62 | True | 7 | 4.15 | 0 | every cycle; most flips towards the levels 3, most slides 5, chains using Lemma 11: 29 |
| D: Theorem 2 | 142 | 14 | 128 | True | 16 | 8.27 | 0 | every cycle; most flips towards the levels 3, most slides 10, chains using Lemma 11: 63 |
| D: Theorem 2 | 142 | 15 | 141 | True | 21 | 12.79 | 0 | every cycle; most flips towards the levels 3, most slides 15, chains using Lemma 11: 85 |
| D: Theorem 2 | 142 | 17 | 317 | True | 11 | 5.68 | 0 | every cycle; most flips towards the levels 4, most slides 7, chains using Lemma 11: 158 |
| D: Theorem 2 | 142 | 18 | 658 | True | 20 | 11.31 | 0 | every cycle; most flips towards the levels 4, most slides 14, chains using Lemma 11: 339 |
| D: Theorem 2 | 142 | 19 | 740 | True | 28 | 16.19 | 0 | every cycle; most flips towards the levels 4, most slides 21, chains using Lemma 11: 364 |
| D: Theorem 2 | 142 | 21 | 223 | True | 13 | 6.17 | 4 | 200 random initial states and 23 structured states; most flips towards the levels 5, most slides 9, chains using Lemma 11: 117; 107 distinct cycles |
| D: Theorem 2 | 142 | 22 | 223 | True | 24 | 12.31 | 0 | 200 random initial states and 23 structured states; most flips towards the levels 5, most slides 18, chains using Lemma 11: 91; 121 distinct cycles |
| D: Theorem 2 | 142 | 23 | 223 | True | 35 | 19.39 | 0 | 200 random initial states and 23 structured states; most flips towards the levels 5, most slides 27, chains using Lemma 11: 122; 114 distinct cycles |
| D: Theorem 2 | 142 | 25 | 223 | True | 15 | 7.40 | 2 | 200 random initial states and 23 structured states; most flips towards the levels 6, most slides 11, chains using Lemma 11: 115; 125 distinct cycles |
| D: Theorem 2 | 142 | 26 | 223 | True | 27 | 14.16 | 0 | 200 random initial states and 23 structured states; most flips towards the levels 6, most slides 22, chains using Lemma 11: 101; 129 distinct cycles |
| D: Theorem 2 | 142 | 27 | 223 | True | 41 | 22.49 | 0 | 200 random initial states and 23 structured states; most flips towards the levels 6, most slides 33, chains using Lemma 11: 107; 129 distinct cycles |
| D: Theorem 2 | 142 | 50 | 73 | True | 59 | 31.51 | 0 | 50 random initial states and 23 structured states; most flips towards the levels 12, most slides 46, chains using Lemma 11: 28; 58 distinct cycles |
| D: Theorem 2 | 142 | 101 | 73 | True | 72 | 32.08 | 0 | 50 random initial states and 23 structured states; most flips towards the levels 25, most slides 49, chains using Lemma 11: 29; 61 distinct cycles |
| D: Theorem 2 | 142 | 202 | 73 | True | 237 | 110.89 | 0 | 50 random initial states and 23 structured states; most flips towards the levels 50, most slides 198, chains using Lemma 11: 30; 68 distinct cycles |
| E: Lemma 10(b), upper level | 43 | 5 | 2 | True | 3 | 1.50 | 1 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 6 | 4 | True | 4 | 2.50 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 7 | 2 | True | 2 | 1.50 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 9 | 8 | True | 8 | 5.25 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 10 | 5 | True | 8 | 4.40 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 11 | 2 | True | 4 | 2.50 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 13 | 14 | True | 14 | 7.79 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 14 | 8 | True | 12 | 6.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 15 | 2 | True | 6 | 3.50 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 17 | 24 | True | 20 | 10.42 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 18 | 9 | True | 16 | 7.56 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 19 | 2 | True | 8 | 4.50 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 21 | 100 | True | 27 | 14.07 | 0 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 22 | 100 | True | 20 | 10.35 | 2 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 23 | 100 | True | 11 | 5.21 | 4 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 25 | 100 | True | 32 | 17.83 | 0 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 26 | 100 | True | 24 | 12.04 | 1 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 27 | 100 | True | 13 | 7.32 | 4 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 50 | 50 | True | 44 | 24.28 | 1 | 50 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 101 | 50 | True | 120 | 81.06 | 0 | 50 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 43 | 202 | 20 | True | 170 | 98.45 | 0 | 20 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 5 | 1 | True | 3 | 3.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 6 | 3 | True | 4 | 3.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 7 | 1 | True | 1 | 1.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 9 | 4 | True | 7 | 5.25 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 10 | 6 | True | 8 | 4.67 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 11 | 1 | True | 1 | 1.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 13 | 7 | True | 11 | 6.86 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 14 | 7 | True | 12 | 6.43 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 15 | 1 | True | 1 | 1.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 17 | 12 | True | 15 | 8.67 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 18 | 10 | True | 16 | 8.20 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 19 | 1 | True | 1 | 1.00 | 0 | every cycle of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 21 | 100 | True | 27 | 13.92 | 0 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 22 | 100 | True | 20 | 10.42 | 1 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 23 | 100 | True | 11 | 6.13 | 6 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 25 | 100 | True | 32 | 17.22 | 0 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 26 | 100 | True | 24 | 12.44 | 1 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 27 | 100 | True | 13 | 7.35 | 3 | 100 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 50 | 50 | True | 46 | 23.14 | 0 | 50 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 101 | 50 | True | 118 | 68.44 | 0 | 50 random states of the upper level; chain length = number of slides |
| E: Lemma 10(b), upper level | 142 | 202 | 20 | True | 169 | 107.20 | 0 | 20 random states of the upper level; chain length = number of slides |

Part A: 3786 cycles in total (both rules, n = 4, 8, 12, 16, 20), each with two choices of the flipped cells. Part D, every cycle: 4276 cycles (both rules, n = 5..19, 4 not dividing n). Part E, every cycle of the upper level: 136 cycles. Random choices use the seed 43142. CPU time 25.70 s, peak memory 118 MB.

### Table 5. Comparison with the data of the study (`crosscheck_data.py` -> `out/crosscheck_data.json`)

| data of the study | compared with | compared | disagreements |
|---|---|---|---|
| `data/ring_size/mechanisms.csv`, rules 43 and 142, n = 8..22 (30 records), fields cycles, g1_closed, g1_sccs, n_selected, gamma_min, kstar, k_c, selected_cover, entry_cost_max, radius_selected_min | Table 2, Table 3 and the values given by Theorems 1 and 2 (one selected cycle or the cycles of the two levels; gamma_min = m - 1; k_c; k*; largest entry cost n/4) | 300 values | 0 |
| `data/ring_size/crystal_radius.csv`, rules 43 and 142, n = 4..400 (200 rows): radius >= 2 and largest return time | Theorem 1(1) and the return time max(1, n/2 - 1) of Proposition 2; test T1 of Table 1 | 200 rows | 0 |
| `data/ring_size/sampled_reach/rule{43,142}_n{24,28,32}.csv` (6 files): stored length of a one-flip path into X | length \|w - n/2\| / 2 of the chain of Theorem 1(2) from the same cycle (Table 4, part C) | 1200 initial states | 0 (stored path longer: 0, shorter: 0) |
| largest direct entry cost in `mechanisms.csv`, 4 \| n | exhaustive shortest-path search of test E | 8 (rule, n) pairs | 0 |

All comparisons agree: True.

Total CPU time of the computing scripts of this folder as recorded in their output files (`check_lemmas.py`, `g1_classes.py`, `constructive_paths.py`, `zhu_richard_154.py`): 74.6 s. Every script ran as a single process.
