### V1. Exhaustive tests of the statements (`test_lemmas.py` -> `out/lemma_tests.json`)

n = 3..20; 100 statements; total failures: 0; wall time 22 s, one process.

| statement | n tested | cases | failures |
|---|---|---|---|
| (R) form of the tables | tables | 16 | 0 |
| rules agree exactly on codes 1,3,4,6 | tables | 1 | 0 |
| 142 ones on 001,010,011,111; 43 on 000,001,011,101 | tables | 1 | 0 |
| descriptions of rules 184, 226; g226(a,b,c)=g184(c,b,a) | tables | 8 | 0 |
| D1 | 3..20 | 2097144 | 0 |
| D2 (w even) | 3..20 | 2097144 | 0 |
| D3 | 3..20 | 39845880 | 0 |
| isolated/interior via P/Q | 3..20 | 39845880 | 0 |
| Lemma 6 | 3..20 | 39845880 | 0 |
| runs: isolated = run 1, interior iff run >= 3 | 3..12 | 8184 | 0 |
| Lemma 1 (43) cell formula | 3..20 | 2097144 | 0 |
| Lemma 1 (43) delta(Fx)=G184(delta x) | 3..20 | 2097144 | 0 |
| Lemma 5 FC=CF (43) | 3..20 | 2097144 | 0 |
| Lemma 5 w(Fx)=w(x) (43) | 3..20 | 2097144 | 0 |
| Lemma 1 (142) cell formula | 3..20 | 2097144 | 0 |
| Lemma 1 (142) delta(Fx)=G226(delta x) | 3..20 | 2097144 | 0 |
| Lemma 5 FC=CF (142) | 3..20 | 2097144 | 0 |
| Lemma 5 w(Fx)=w(x) (142) | 3..20 | 2097144 | 0 |
| Lemma 2 |G184 d|=|d| | 3..20 | 2097144 | 0 |
| Lemma 2 |G226 d|=|d| | 3..20 | 2097144 | 0 |
| Lemma 3(a) P equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(a) Q equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(a) counts | 3..20 | 2097144 | 0 |
| Lemma 3(a) translation when A empty | 3..20 | 430268 | 0 |
| Lemma 3(b) P equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(b) Q equivalence | 3..20 | 2097144 | 0 |
| Lemma 3(b) counts | 3..20 | 2097144 | 0 |
| Lemma 3(b) translation when A empty | 3..20 | 430268 | 0 |
| Lemma 3(c) | 3..20 | 2097144 | 0 |
| Lemma 4 periodic iff P or Q empty (184) | 3..20 | 2097144 | 0 |
| Lemma 4 action, P empty (184) | 3..20 | 39596 | 0 |
| Lemma 4 action, Q empty (184) | 3..20 | 39596 | 0 |
| Lemma 4 periodic iff P or Q empty (226) | 3..20 | 2097144 | 0 |
| Lemma 4 action, P empty (226) | 3..20 | 39596 | 0 |
| Lemma 4 action, Q empty (226) | 3..20 | 39596 | 0 |
| Lemma 7(a) (43) | 3..20 | 2097144 | 0 |
| Lemma 7(b) no isolated (43) | 3..20 | 39596 | 0 |
| Lemma 7(b) no interior (43) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no isolated' preserved by F, sigma, C (43) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no interior' preserved by F, sigma, C (43) | 3..20 | 39596 | 0 |
| Lemma 7(c) (43) | 3..20 | 2911432 | 0 |
| periods divide 2n (43) | 3..20 | 4025 | 0 |
| family 'no isolated' has w <= n/2 (43) | 3..20 | 39596 | 0 |
| family 'no interior' has w >= n/2 (43) | 3..20 | 39596 | 0 |
| families meet exactly in X (43) | 3..20 | 18 | 0 |
| wall count constant on cycles (43) | 3..20 | 4025 | 0 |
| Theorem 2 unique closed class = K (43) | 3,5,6,7,9,10,11,13,14,15,17,18,19 | 13 | 0 |
| Lemma 10 slides join cycles both ways (43) | 3..20 | 497440 | 0 |
| Lemma 10(a) procedure (43) | 3..20 | 39560 | 0 |
| Lemma 10(b) procedure (43) | 3..20 | 39558 | 0 |
| Lemma 7(a) (142) | 3..20 | 2097144 | 0 |
| Lemma 7(b) no isolated (142) | 3..20 | 39596 | 0 |
| Lemma 7(b) no interior (142) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no isolated' preserved by F, sigma, C (142) | 3..20 | 39596 | 0 |
| Lemma 7(b) 'no interior' preserved by F, sigma, C (142) | 3..20 | 39596 | 0 |
| Lemma 7(c) (142) | 3..20 | 2911432 | 0 |
| periods divide 2n (142) | 3..20 | 4043 | 0 |
| family 'no isolated' has w <= n/2 (142) | 3..20 | 39596 | 0 |
| family 'no interior' has w >= n/2 (142) | 3..20 | 39596 | 0 |
| families meet exactly in X (142) | 3..20 | 18 | 0 |
| wall count constant on cycles (142) | 3..20 | 4043 | 0 |
| Theorem 2 unique closed class = K (142) | 3,5,6,7,9,10,11,13,14,15,17,18,19 | 13 | 0 |
| Lemma 10 slides join cycles both ways (142) | 3..20 | 497440 | 0 |
| Lemma 10(a) procedure (142) | 3..20 | 39560 | 0 |
| Lemma 10(b) procedure (142) | 3..20 | 39558 | 0 |
| Lemma 8 neither 11 nor 00 in wall word => X and 4|n (43) | 4,6,8,10,12,14,16,18,20 | 9 | 0 |
| Lemma 8 periodic with w=n/2 are X (43) | 4,8,12,16,20 | 5 | 0 |
| Lemma 8 X one cycle of length 4, F = sigma^-1 (43) | 4,8,12,16,20 | 5 | 0 |
| codes on X are exactly 1,3,4,6 (43) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(1) flips of X return to X (43) | 4,8,12,16,20 | 240 | 0 |
| Theorem 1 only closed class is {X} (43) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(2) G1-distance to X = |w-n/2|/2 (43) | 4,8,12,16,20 | 1889 | 0 |
| Theorem 1(2) interior/isolated cell exists on every state (43) | 4,8,12,16,20 | 35376 | 0 |
| Theorem 1(2) proof step, every interior/isolated flip (43) | 4,8,12,16,20 | 306016 | 0 |
| Proposition 2 healing time (43) | 4,8,12,16,20 | 240 | 0 |
| Lemma 8 neither 11 nor 00 in wall word => X and 4|n (142) | 4,6,8,10,12,14,16,18,20 | 9 | 0 |
| Lemma 8 periodic with w=n/2 are X (142) | 4,8,12,16,20 | 5 | 0 |
| Lemma 8 X one cycle of length 4, F = sigma^-1 (142) | 4,8,12,16,20 | 5 | 0 |
| codes on X are exactly 1,3,4,6 (142) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(1) flips of X return to X (142) | 4,8,12,16,20 | 240 | 0 |
| Theorem 1 only closed class is {X} (142) | 4,8,12,16,20 | 5 | 0 |
| Theorem 1(2) G1-distance to X = |w-n/2|/2 (142) | 4,8,12,16,20 | 1897 | 0 |
| Theorem 1(2) interior/isolated cell exists on every state (142) | 4,8,12,16,20 | 35376 | 0 |
| Theorem 1(2) proof step, every interior/isolated flip (142) | 4,8,12,16,20 | 306016 | 0 |
| Proposition 2 healing time (142) | 4,8,12,16,20 | 240 | 0 |
| w- >= 2, w+ <= n-1, eps in {1,2,3} | 5,6,7,9,10,11,13,14,15,17,18,19 | 24 | 0 |
| Lemma 9(a) lower: interior, no isolated (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1404 | 0 |
| Lemma 9(a) upper: isolated, no interior (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1092 | 0 |
| Lemma 9(b) no edge leaves K (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 26261 | 0 |
| Lemma 9(c) edges between the levels (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 144 | 0 |
| Lemma 9(d) every cycle reaches K (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 2133 | 0 |
| Lemma 11 (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |
| Corollary 3 all eight codes on K (43) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |
| Lemma 9(a) lower: interior, no isolated (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1404 | 0 |
| Lemma 9(a) upper: isolated, no interior (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 1092 | 0 |
| Lemma 9(b) no edge leaves K (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 25914 | 0 |
| Lemma 9(c) edges between the levels (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 152 | 0 |
| Lemma 9(d) every cycle reaches K (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 2143 | 0 |
| Lemma 11 (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |
| Corollary 3 all eight codes on K (142) | 5,6,7,9,10,11,13,14,15,17,18,19 | 12 | 0 |

### V2. Potentials, selected set and k_c from the definitions, without Theorem A (`potentials.py` -> `out/potentials.jsonl`)

| rule | n | cycles m | gamma_min | m - 1 | selected cycles | wall counts of S | k_0..k_7 | k* | closed classes of G1 (sizes) | all document checks | gamma method |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 43 | 3 | 3 | 2 | 2 | 3 | [0, 2] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 142 | 3 | 3 | 2 | 2 | 3 | [0, 2] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 43 | 4 | 3 | 2 | 2 | 1 | [2] | 10100101 | 1 | [1] | True | own Edmonds = networkx = brute force |
| 142 | 4 | 5 | 4 | 4 | 1 | [2] | 10100101 | 1 | [1] | True | own Edmonds = networkx = brute force |
| 43 | 5 | 4 | 3 | 3 | 3 | [2, 4] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 142 | 5 | 5 | 4 | 4 | 3 | [2, 4] | 00000000 | 0 | [3] | True | own Edmonds = networkx = brute force |
| 43 | 6 | 10 | 9 | 9 | 8 | [2, 4] | 00000000 | 0 | [8] | True | own Edmonds = networkx |
| 142 | 6 | 10 | 9 | 9 | 6 | [2, 4] | 00000000 | 0 | [6] | True | own Edmonds = networkx |
| 43 | 7 | 7 | 6 | 6 | 4 | [2, 4] | 00000000 | 0 | [4] | True | own Edmonds = networkx = brute force |
| 142 | 7 | 8 | 7 | 7 | 5 | [2, 4] | 00000000 | 0 | [5] | True | own Edmonds = networkx |
| 43 | 8 | 13 | 12 | 12 | 1 | [4] | 10100101 | 1 | [1] | True | own Edmonds = networkx |
| 142 | 8 | 15 | 14 | 14 | 1 | [4] | 10100101 | 1 | [1] | True | own Edmonds = networkx |
| 43 | 9 | 15 | 14 | 14 | 9 | [4, 6] | 00000000 | 0 | [9] | True | own Edmonds = networkx |
| 142 | 9 | 15 | 14 | 14 | 6 | [4, 6] | 00000000 | 0 | [6] | True | own Edmonds = networkx |
| 43 | 10 | 28 | 27 | 27 | 10 | [4, 6] | 00000000 | 0 | [10] | True | own Edmonds = networkx |
| 142 | 10 | 30 | 29 | 29 | 12 | [4, 6] | 00000000 | 0 | [12] | True | own Edmonds = networkx |
| 43 | 11 | 28 | 27 | 27 | 7 | [4, 6] | 00000000 | 0 | [7] | True | own Edmonds = networkx |
| 142 | 11 | 29 | 28 | 28 | 11 | [4, 6] | 00000000 | 0 | [11] | True | own Edmonds = networkx |
| 43 | 12 | 61 | 60 | 60 | 1 | [6] | 10100101 | 1 | [1] | True | networkx |
| 142 | 12 | 61 | 60 | 60 | 1 | [6] | 10100101 | 1 | [1] | True | networkx |
| 43 | 13 | 61 | 60 | 60 | 15 | [6, 8] | 00000000 | 0 | [15] | True | networkx |
| 142 | 13 | 62 | 61 | 61 | 9 | [6, 8] | 00000000 | 0 | [9] | True | networkx |
| 43 | 14 | 126 | 125 | 125 | 16 | [6, 8] | 00000000 | 0 | [16] | True | networkx |
| 142 | 14 | 128 | 127 | 127 | 14 | [6, 8] | 00000000 | 0 | [14] | True | networkx |

Checks per record (all True in every record): Cor 1: S = {X}; Cor 2: k = (1,0,1,0,0,1,0,1), k* = 1; Cor 3: S = K; Cor 3: k = 0 for all c, k* = 0; G1 (flips) = {V = 1}; Prop 3: V(C,X) = |w-n/2|/2; Prop 3: max V(C,X) = n/4 exactly at w in {0,n}; S = union of closed classes (single class); Thm 1: r(X) >= 2; gamma_min = m - 1.

### V3. Order of nu_c(eps) read off the stationary law (GTH, eps = 1e-4 and 1e-5; `stationary.py` -> `out/stationary.json`)

| rule | n | k_c from pi | k_c from potentials | agree | max rounding error | stationary mass on S at eps = 1e-5 |
|---|---|---|---|---|---|---|
| 43 | 4 | 10100101 | 10100101 | True | 0.0001 | 0.999950 |
| 142 | 4 | 10100101 | 10100101 | True | 0.0001 | 0.999950 |
| 43 | 5 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 142 | 5 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 43 | 6 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 142 | 6 | 00000000 | 00000000 | True | 0.0001 | 0.999978 |
| 43 | 7 | 00000000 | 00000000 | True | 0.0004 | 0.999944 |
| 142 | 7 | 00000000 | 00000000 | True | 0.0004 | 0.999944 |
| 43 | 8 | 10100101 | 10100101 | True | 0.0004 | 0.999780 |
| 142 | 8 | 10100101 | 10100101 | True | 0.0004 | 0.999780 |

### V4. Proposition 3 by a backward computation over all states (`entry_cost.py` -> `out/entry_cost.json`)

| rule | n | cycles | max V(C, X) | n/4 | cycles with V(C, X) != abs(w - n/2)/2 |
|---|---|---|---|---|---|
| 43 | 4 | 3 | 1 | 1 | 0 |
| 142 | 4 | 5 | 1 | 1 | 0 |
| 43 | 8 | 13 | 2 | 2 | 0 |
| 142 | 8 | 15 | 2 | 2 | 0 |
| 43 | 12 | 61 | 3 | 3 | 0 |
| 142 | 12 | 61 | 3 | 3 | 0 |
| 43 | 16 | 283 | 4 | 4 | 0 |
| 142 | 16 | 285 | 4 | 4 | 0 |
| 43 | 20 | 1529 | 5 | 5 | 0 |
| 142 | 20 | 1531 | 5 | 5 | 0 |

### V5. Comparison with `proofs_43_142/out/` and `data/ring_size/mechanisms.csv` (`compare.py` -> `out/compare.json`)

G1 fields of `g1_classes.jsonl` compared for both rules, n = 3..20 (cycles, periodic states, G1 edges, strong components, closed classes, their sizes, members, codes, wall counts): 324 values, 0 differences.

`mechanisms.csv`, rules 43 and 142, n = 8..22: 30 records; compared against 14 records by potentials (definitions), 12 records by G1 closed class + Theorem A (m - 1), 4 records by not computed here (n > 20); disagreements: 0.

Entry costs: the session's test E covers rule 43 n = 4..20 (1889 cycles), rule 142 n = 4..20 (1897 cycles); this verification: rule 43 n = 4: 3 cycles, 0 failures, rule 142 n = 4: 5 cycles, 0 failures, rule 43 n = 8: 13 cycles, 0 failures, rule 142 n = 8: 15 cycles, 0 failures, rule 43 n = 12: 61 cycles, 0 failures, rule 142 n = 12: 61 cycles, 0 failures, rule 43 n = 16: 283 cycles, 0 failures, rule 142 n = 16: 285 cycles, 0 failures, rule 43 n = 20: 1529 cycles, 0 failures, rule 142 n = 20: 1531 cycles, 0 failures.

