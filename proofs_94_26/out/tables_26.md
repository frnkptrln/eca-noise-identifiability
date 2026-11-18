### Table 1. Exhaustive tests of the lemmas (`check_lemmas_26.py` -> `out/check_lemmas_26.json`)

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| M1 | Lemma 1 (moving frame): sigma F (u)(j) = u(j) + u(j-2)[1 + u(j-1)(1 + u(j))]; every state | 4..14 | 32752 | 0 |
| M2 | Lemma 2 (c does not increase): c(F x) <= c(x); every state | 4..20 (even) | 1398096 | 0 |
| M2f | Lemma 2, remark: one flip changes c by -2, 0 or 2, and deleting a one does not raise c; every state, every cell | 4..16 (even) | 1339840 | 0 |
| M3 | Lemma 3 (domain states): the description by sources equals "ones on both parities and no pattern 1 0^(2r) 1 1"; in the moving frame the sources stay, the free cells follow c_k -> c_k + c_(k-1), the other cells stay 0; F permutes the domain states; every state | 4..18 (even) | 349520 | 0 |
| M4 | Lemma 4: if u(j) = u(j+1) = 1 and the preceding one is at distance 2r+1 from j, then after r steps the cells j-1, j, j+1 of the moving frame carry 111; every state, every such pattern | 4..16 (even) | 223330 | 0 |
| M5 | Theorem 1 (periodic states, even n): c is constant on a cycle; a periodic state is 0, or lies on one parity class, or is a domain state, or its orbit contains 111; domain states are periodic; for n = 4, 8, 16 no periodic state other than 0 lies on one parity class; every periodic state | 4..18 (even) | 41267 | 0 |
| M6 | Lemma 5: every state with ones on both parities that is not a domain state has a singleton group, and deleting a singleton group lowers c by 2; every such state | 4..16 (even) | 73843 | 0 |
| M7 | Lemma 7 (carrier words): F^2(w) is w shifted by one cell for every cyclic word over the blocks 11100 and 100 that contains 11100; every such word, every rotation | 5..31 | 1444 | 0 |
| M8 | Lemma 6: on one parity class rule 26 is rule 90 and maps E into O and O into E (every state of E and O, even n = 4..16); F^(n/2) = 0 there for n = 2^k (every state of E and O for n = 4, 8, 16; the two single seeds for n = 32..1024) | 4..16 (even); 32..1024 (powers of two) | 1580 | 0 |
| M9 | Lemma 8: every domain cycle contains the codes 001, 010, 011, 100, 101, 110; for n = 8, 16 every cycle other than {0} contains 011 and 110; every such cycle | 6..18 (even) | 1219 | 0 |

All tests passed: True. CPU time 6.42 s.

Numbers of domain states (test M3), by n: 4: 0, 6: 12, 8: 64, 10: 240, 12: 816, 14: 2688, 16: 8704, 18: 27840.

Periodic states by kind (test M5), n: zero / on one parity class / domain states / orbit with 111: 4: 1 / 0 / 0 / 0; 6: 1 / 6 / 12 / 0; 8: 1 / 0 / 64 / 16; 10: 1 / 30 / 240 / 5; 12: 1 / 30 / 816 / 0; 14: 1 / 126 / 2688 / 56; 16: 1 / 0 / 8704 / 80; 18: 1 / 510 / 27840 / 36.

### Table 2. G1 and its closed classes computed directly, even n (`g1_26.py` -> `out/g1_26.jsonl`)

| n | 2^k | cycles | periodic states | G1 edges | closed classes (sizes) | {0} in the closed class | cycles on one parity class (not {0}) | domain cycles | cycles with 111 | one-parity cycles in K | domain cycles in K | cycles with 111 in K | codes on K | c of the domain cycles | c of the cycles with 111 | cycles with 111 through a carrier word | largest increase of c along a G1 edge | cycles with a G1 path to {0} | max G1 distance to {0} | CPU s | peak MB |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | yes | 1 | 1 | 0 | 1 [1] | True | 0 | 0 | 0 | 0 of 0 | 0 of 0 | 0 of 0 | [0] | - | - | 0 | None | 1 of 1 | 0 | 0.0 | 54 |
| 6 | no | 7 | 19 | 33 | 1 [7] | True | 3 | 3 | 0 | 3 of 3 | 3 of 3 | 0 of 0 | [0, 1, 2, 3, 4, 5, 6] | [2] | - | 0 | 2 | 7 of 7 | 2 | 0.0 | 54 |
| 8 | yes | 10 | 81 | 73 | 1 [1] | True | 0 | 8 | 1 | 0 of 0 | 0 of 8 | 0 of 1 | [0] | [2] | [4] | 1 | 2 | 10 of 10 | 1 | 0.01 | 54 |
| 10 | no | 19 | 276 | 259 | 1 [18] | True | 5 | 12 | 1 | 5 of 5 | 12 of 12 | 0 of 1 | [0, 1, 2, 3, 4, 5, 6] | [2] | [6] | 1 | 2 | 19 of 19 | 3 | 0.0 | 54 |
| 12 | no | 64 | 847 | 1665 | 1 [64] | True | 9 | 54 | 0 | 9 of 9 | 54 of 54 | 0 of 0 | [0, 1, 2, 3, 4, 5, 6] | [2, 4] | - | 0 | 2 | 64 of 64 | 3 | 0.01 | 54 |
| 14 | no | 76 | 2871 | 2493 | 1 [76] | True | 9 | 64 | 2 | 9 of 9 | 64 of 64 | 2 of 2 | [0, 1, 2, 3, 4, 5, 6, 7] | [2, 4] | [6] | 1 | 2 | 76 of 76 | 3 | 0.03 | 54 |
| 16 | yes | 552 | 8785 | 32240 | 1 [1] | True | 0 | 548 | 3 | 0 of 0 | 0 of 548 | 0 of 3 | [0] | [2, 4] | [8] | 2 | 2 | 552 of 552 | 3 | 245.24 | 192 |
| 18 | no | 567 | 28387 | 33364 | 1 [566] | True | 39 | 526 | 1 | 39 of 39 | 526 of 526 | 0 of 1 | [0, 1, 2, 3, 4, 5, 6] | [2, 4, 6] | [10] | 1 | 2 | 567 of 567 | 4 | 0.38 | 193 |
| 20 | no | 2816 | 88956 | 191625 | 1 [2815] | True | 45 | 2766 | 4 | 45 of 45 | 2766 of 2766 | 3 of 4 | [0, 1, 2, 3, 4, 5, 6, 7] | [2, 4, 6] | [8, 12] | 2 | 2 | 2816 of 2816 | 5 | 1.37 | 231 |
| 22 | no | 3695 | 281315 | 292094 | 1 [3684] | True | 33 | 3648 | 13 | 33 of 33 | 3648 of 3648 | 2 of 13 | [0, 1, 2, 3, 4, 5, 6, 7] | [2, 4, 6] | [6, 10] | 3 | 2 | 3695 of 3695 | 5 | 4.68 | 407 |

K denotes the closed class that contains {0} (the only closed class in every row). For n = 4, 8, 16, K = {0}.

### Table 3. n = 4, 8, 16: resistances, potentials and k_c from the definitions (`g1_26.py`)

| n | m | V({0}, C): value: number of cycles | cycles with V({0}, C) = 2 (T2) | cycles reachable from T2 in G1 | domain cycles reachable from T2 | cycles with 111 reachable from T2 | gamma({0}) | gamma by kind of cycle (roots computed by Edmonds) | gamma agrees with Theorem 3 | G1 edges = pairs with V = 1 | R({0} -> D_c), c = 0..7 | k_c, c = 0..7 | k* | how gamma was obtained |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 1 | {'0': 1} | 0 | 0 | 0 of 0 | 0 of 0 | 0 | {'zero': [0]} | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | [0, 1, 1, 2, 1, 1, 2, 2] | 2 | Edmonds, all roots |
| 8 | 10 | {'0': 1, '2': 8, '3': 1} | 8 | 10 | 8 of 8 | 1 of 1 | 9 | {'domain': [10], 'with_111': [10], 'zero': [9]} | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | [0, 1, 1, 1, 1, 1, 1, 1] | 1 | Edmonds, all roots |
| 16 | 552 | {'0': 1, '2': 88, '3': 392, '4': 68, '5': 3} | 88 | 549 | 548 of 548 | 0 of 3 | 551 | {'domain': [552], 'with_111': [553], 'zero': [551]} | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | [0, 1, 1, 1, 1, 1, 1, 2] | 2 | Edmonds, all roots |

### Table 4. The chains of the proofs, executed step by step (`chains_26.py` -> `out/chains_26.json`)

Part A: every cycle, chain of Theorem 2 down to a cycle on one parity class.

| n | cycles | all chains end on one parity class | chains ending at {0} | max flips | max number of drops of c |
|---|---|---|---|---|---|
| 4 | 1 | True | 1 | 0 | 0 |
| 6 | 7 | True | 1 | 1 | 1 |
| 8 | 10 | True | 10 | 2 | 2 |
| 10 | 19 | True | 1 | 2 | 2 |
| 12 | 64 | True | 1 | 3 | 2 |
| 14 | 76 | True | 1 | 4 | 3 |
| 16 | 552 | True | 552 | 4 | 3 |
| 18 | 567 | True | 1 | 5 | 4 |
| 20 | 2816 | True | 1 | 7 | 5 |

Part B: cycles reached from random states, n = 2^k, chain of Theorem 2 to {0}.

| n | start states | all chains end at {0} | max c of the start cycle | max flips | max number of drops of c |
|---|---|---|---|---|---|
| 32 | 100 | True | 10 | 9 | 5 |
| 64 | 100 | True | 16 | 20 | 8 |
| 128 | 50 | True | 30 | 39 | 15 |
| 256 | 50 | True | 58 | 79 | 29 |
| 512 | 20 | True | 112 | 160 | 56 |
| 1024 | 10 | True | 218 | 302 | 109 |

Part C: chain of Theorem 4(c): 0, e_0 + e_5 (resistance 2), then single flips between periodic domain states up to 10100 (100)^q, then one flip to the carrier word 11100 (100)^q.

| n | q | flips between domain states after e_0 + e_5 | all intermediate states periodic domain states | last flip gives the carrier word, periodic, with 111 | period of the carrier cycle | c of the last domain state | c of the carrier |
|---|---|---|---|---|---|---|---|
| 8 | 1 | 2 | True | True | 16 | 2 | 4 |
| 32 | 9 | 10 | True | True | 64 | 10 | 12 |
| 128 | 41 | 42 | True | True | 256 | 42 | 44 |
| 512 | 169 | 170 | True | True | 1024 | 170 | 172 |

Part D: even n that are not powers of two. Every cycle on one parity class is joined to {0} in both directions (Lemma 9), and every domain cycle is joined to a cycle on one parity class by flips between periodic states (Theorem 5).

| n | one-parity cycles joined to {0} both ways | domain cycles joined to a one-parity cycle |
|---|---|---|
| 6 | 3 | 3 |
| 10 | 5 | 12 |
| 12 | 9 | 54 |
| 14 | 9 | 64 |
| 18 | 39 | 526 |
| 20 | 45 | 2766 |

Part E: Theorem 3(d). From e_(s1) + e_(s2) (resistance 2 from 0; s1, s2 two consecutive sources) to a given domain state by single flips; every intermediate state is asserted to be a periodic domain state.

| n | target domain states | which | all intermediate states periodic domain states | max flips |
|---|---|---|---|---|
| 8 | 8 | every domain cycle | True | 2 |
| 16 | 548 | every domain cycle | True | 6 |
| 32 | 200 | cycles reached from random states | True | 15 |
| 64 | 200 | cycles reached from random states | True | 30 |

Part F: Theorem 4(b). The path 0, e_0, F(e_0), F^2(e_0) + e_1, whose next state contains 111, and the orbit of a single flip of 0 (no two adjacent ones, returns to 0): executed for n = 8, 16, 32, 64, 128, 256, 512, 1024; all as stated: True.

CPU time of `chains_26.py`: 36.61 s.

### Table 5. Comparison with data already in the repository (`crosscheck_data.py` -> `out/crosscheck_data.json`)

| compared with | ring sizes n | fields compared | disagreements |
|---|---|---|---|
| data/ring_size/mechanisms.csv | 8, 10, 12, 14, 16, 18, 20, 22 | cycles; selected cycles = size of the closed class; gamma_min = m - 1; k_c and k* (n = 8, 16: all values; other n: the codes with k_c = 0 are the codes on the closed class) | 0 |
| verify_ring_size/part2_154/out/explore_122_26.jsonl | 4, 6, 8, 10, 12, 14, 16, 18, 20, 22 | closed-class sizes; cycles; cycles that contain 111 (where recorded) | 0 |

k_c of the study and of this folder at the powers of two in the study: n = 8: study [0, 1, 1, 1, 1, 1, 1, 1], here [0, 1, 1, 1, 1, 1, 1, 1]; n = 16: study [0, 1, 1, 1, 1, 1, 1, 2], here [0, 1, 1, 1, 1, 1, 1, 2].
