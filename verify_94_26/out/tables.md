### Rule 94 (PROOF_94_converse.md), `test_94.py`

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| L8 | Lemma 8: live window orbits = {A_w,B_w} (w=2 mod 3), 0000->1001->1111 (w=4), none otherwise | w=1..22 | 8388606 | 0 |
| L7ab | Lemma 7(a),(b): window neighbours frozen ones, width <= n-3; F^t = id on W, = phi^t on windows (t<=8) | 5..14 | 26454 | 0 |
| T1 | Theorem 1: x periodic iff x=0, or doubled word D_p(v), v in V_per\{0}, or W nonempty and every window live (A_w/B_w, w=2 mod 3; 0000/1001/1111, w=4); every state | 3..20 | 2097144 | 0 |
| T1p6 | Theorem 1: the period of a case-3 state divides 6 (F^6 x = x) | 3..20 | 2097144 | 0 |
| L9n | Lemma 9 / Theorem 1 case 2: number of periodic states with empty frozen set = 1 (n odd), 2(2^(n/2-2^e)-1)+1 (n = 2^(e+1) q) | 3..20 | 18 | 0 |
| L10 | Lemma 10: in every state of every cycle with W neither empty nor full, every window with content A_w, B_w, 0000, 1111: the named flip gives a periodic state of another cycle, W grows by the named occurrence (2 or 3 cells), the rest of the window is the named live window | 3..20 | 50780 | 0 |
| LW | Lemma W: windows cut out of a block word: cells outside I frozen, F^t = id outside I and phi^t inside (t<=6), every content | 5..12, w<=7 | 40528 | 0 |
| L11 | Lemma 11 (swap): x+e_(p+2), x+e_(p+3) form a 2-cycle, x+e_(p+2)+e_(p+3) = block word with l s; every block word, every s l | 5..20 | 1929 | 0 |
| L12 | Lemma 12 (merge): F(x+e_(p+3)) = x with s s s -> l l; every block word, every s s s followed by a block start | 6..20 | 1454 | 0 |
| L13 | Lemma 13 (split): x+e_(p+2) has period 2, F^5(F(y)+e_(p+6)) = x with s l l -> s s s s; every block word, every s l l | 8..20 | 826 | 0 |
| L15 | Lemma 15 / Prop. 3(i): z = 0100001+block word is periodic with W = complement of {2..5} and contains 000 (n=7, 10..200, 3 not dividing n; periodicity by enumeration for n<=NMAX); chains into {0} for n=5,7,8 | 7..200 | 132 | 0 |
| L16 | Lemma 16 (i) F(x)=0 iff x in {0,1^n}; (ii) F(x)=1^n iff x word over 001,0011; (iii) F(z) such a word => 8|n; basin of 0 described when 8 does not divide n; every state | 3..20 | 2097144 | 0 |
| T2 | Lemma 14, Theorem 2 (a)-(d), Proposition 3 (ii), (iii): unique closed class K, contains every cycle with 101, = reachable from block words, outside K only {0} and doubled-word cycles, 8 codes on K; no edge into {0} for n>=10, 8 not dividing n | 4,5,7,8,10,11,13,14,16,17,19,20 | 12 | 0 |

All passed: True. CPU time 7.69 s.

### Rule 26 (PROOF_26.md), `test_26.py`

| test | statement tested | n | cases | violations |
|---|---|---|---|---|
| M1 | Lemma 1: sigma F(u)(j) = u(j) + u(j-2)[1 + u(j-1)(1 + u(j))]; every state | 3..20 | 2097144 | 0 |
| M2 | Lemma 2: c(Fx) <= c(x); every state | 4..20 even | 1398096 | 0 |
| M2f | Lemma 2: a flip changes c by -2, 0, 2; deleting a one does not increase c; every state and cell | 4..20 even | 27029952 | 0 |
| M3a | Lemma 3(a): domain state (sources at distances >= 3) iff no adjacent ones (j, j+1) whose preceding one is at odd distance; every state | 4..18 even | 524288 | 0 |
| M3b | Lemma 3(b): U(u) is a domain state with the same sources, zeros at odd offsets, free cells c_k + c_(k-1); every domain state | 4..18 even | 40364 | 0 |
| M3c | Lemma 3(c): F maps the set of domain states onto itself; no domain state contains 111; flipping a free cell keeps a domain state with the same sources | 4..18 even | 40364 | 0 |
| M3F | Lemma 3(c), wording: does F (not U) preserve the set of sources? (finding C1 expects: no) | 4..18 even | 40364 | 0 |
| M5 | Lemma 5: every state of M that is not a domain state has a singleton group; deleting a singleton group lowers c by 2 | 4..18 even | 524288 | 0 |
| M4 | Lemma 4: u(j)=u(j+1)=1, preceding one at distance 2r+1 => U^r(u) has 111 at j-1, j, j+1; and every non-domain state of M meets 111 within n/2-1 steps | 4..16 even | 223330 | 0 |
| M6 | Lemma 6: on E and O rule 26 = rule 90, E -> O -> E; F^(n/2) = 0 there for n = 2^k (all of E u O for n<=16, single seed for n=32..1024) | 4..16; 32..1024 | 1015 | 0 |
| M7 | Lemma 7: F^2(w) = sigma w for every cyclic word over 11100, 100 with at least one 11100; every rotation | 5..31 | 1444 | 0 |
| T1 | Theorem 1: c constant on cycles; periodic states = rule-90 periodic states in E u O, domain states (all periodic), and states of M (not domain) whose cycle contains 111 | 4..20 even | 9 | 0 |
| L8 | Lemma 8: every domain cycle has codes 1..6; for n = 2^k every cycle other than {0} has codes 3 and 6 | 4..20 even | 9 | 0 |
| L9 | Lemma 9: the cycles contained in E u O lie in one strong component of G1 | 4..20 even | 9 | 0 |
| T2 | Theorem 2: every cycle has a G1 path to a cycle contained in E u O; c rises by at most 2 along a G1 edge | 4..20 even | 9 | 0 |
| T3ab | Theorem 3(a),(b): for n = 2^k no G1 edge leaves {0}, and {0} is the only closed class | 4..20 even | 9 | 0 |
| T5 | Theorem 5: for even n not a power of two one closed class K, containing {0}, all E u O cycles and all domain cycles; cycles outside K contain 111; codes 0..6 on K | 4..20 even | 9 | 0 |
| T2ch | Theorem 2: the chain of the proof (case 1 singleton deletion, case 2 deletion inside a group) executed from every cycle (even n<=NMAX) and from random cycles (n=32, 64, 128) ends on E u O, at {0} for n=2^k | 4..20; 32..128 | 4182 | 0 |
| T34ch | Theorems 3(d), 4(b), 4(c): the chains of the proofs (sources s1, s2, then further sources, then free cells: domain states throughout; the resistance-2 path to 111; 10100(100)^q periodic domain state next to the periodic carrier 11100(100)^q) | 8..1024 | 312 | 0 |
| T5ch | Theorem 5 proof: every domain cycle is joined to the one-parity state e_a + e_(a+2^(e+1)) by flips between periodic domain states (executed for every domain cycle) | even n<=20, not 2^k | 3425 | 0 |
| S7n22 | Section 7: at n = 22 some cycle contains 111 and has c = 6 (periodic flags of all 2^22 states, no G1) | 22 | 1 | 0 |

All passed: True. CPU time 8.07 s.

### Mutation checks (`mutate_94.py`, `mutate_26.py`): deliberately wrong statements, violations found

| rule | wrong statement injected | violations per test |
|---|---|---|
| 94 | T1 without 1001 live | T1: 85, T1p6: 0, L9n: 0 |
| 94 | L8 without 1001 live | L8: 1 |
| 94 | T1 with 11111 live | T1: 41, T1p6: 41, L9n: 0 |
| 94 | T1 without doubled words | T1: 66, T1p6: 0, L9n: 0 |
| 94 | L10 with A replaced by B | L10: 263 |
| 94 | L15 with a wrong z | L15: 15 |
| 94 | L16 with a wrong word set | L16: 13 |
| 26 | domain distance >= 1 instead of >= 3 | M3a: 928, M3b: 736, M3c: 740, M3F: 0, M5: 0 |
| 26 | c = number of ones | M3a: 0, M3b: 0, M3c: 0, M3F: 0, M5: 928 |
| 26 | rule 154 in Lemma 7 and Lemma 1 | M7: 61, M1: 4906 |
| 26 | 12 declared a power of two | T1: 1, L8: 9, L9: 0, T2: 0, T3ab: 1, T5: 0 |

### Potentials from the definitions (`check_potentials.py`; Theorem A not used)

Edmonds (networkx) against brute force over all in-trees: [{'rule': 26, 'n': 6, 'm': 7, 'agree': True}, {'rule': 94, 'n': 4, 'm': 3, 'agree': True}, {'rule': 154, 'n': 5, 'm': 4, 'agree': True}, {'rule': 26, 'n': 5, 'm': 3, 'agree': True}, {'rule': 90, 'n': 5, 'm': 6, 'agree': True}, {'rule': 30, 'n': 5, 'm': 2, 'agree': True}]

| rule | n | m | gamma_min | gamma_min = m-1 | selected | closed classes (sizes) | S = union of closed classes | G1 = pairs with V = 1 | k_c, c = 0..7 | k* |
|---|---|---|---|---|---|---|---|---|---|---|
| 94 | 5 | 11 | 10 | True | 11 | [11] | True | True | [0, 0, 0, 0, 0, 0, 0, 0] | 0 |
| 94 | 6 | 9 | 10 | False | 3 | [1, 1, 1] | True | True | [1, 1, 1, 0, 1, 0, 0, 1] | 1 |
| 94 | 7 | 22 | 21 | True | 22 | [22] | True | True | [0, 0, 0, 0, 0, 0, 0, 0] | 0 |
| 94 | 8 | 27 | 26 | True | 27 | [27] | True | True | [0, 0, 0, 0, 0, 0, 0, 0] | 0 |
| 94 | 9 | 31 | 32 | False | 3 | [1, 1, 1] | True | True | [1, 1, 1, 0, 1, 0, 0, 1] | 1 |
| 94 | 10 | 73 | 72 | True | 67 | [67] | True | True | [0, 0, 0, 0, 0, 0, 0, 0] | 0 |
| 94 | 11 | 78 | 77 | True | 77 | [77] | True | True | [0, 0, 0, 0, 0, 0, 0, 0] | 0 |
| 94 | 12 | 147 | 148 | False | 3 | [1, 1, 1] | True | True | [1, 1, 1, 0, 1, 0, 0, 1] | 1 |
| 26 | 4 | 1 | 0 | True | 1 | [1] | True | True | [0, 1, 1, 2, 1, 1, 2, 2] | 2 |
| 26 | 6 | 7 | 6 | True | 7 | [7] | True | True | [0, 0, 0, 0, 0, 0, 0, 1] | 1 |
| 26 | 8 | 10 | 9 | True | 1 | [1] | True | True | [0, 1, 1, 1, 1, 1, 1, 1] | 1 |
| 26 | 10 | 19 | 18 | True | 18 | [18] | True | True | [0, 0, 0, 0, 0, 0, 0, 1] | 1 |
| 26 | 12 | 64 | 63 | True | 64 | [64] | True | True | [0, 0, 0, 0, 0, 0, 0, 1] | 1 |
| 26 | 14 | 76 | 75 | True | 76 | [76] | True | True | [0, 0, 0, 0, 0, 0, 0, 0] | 0 |

Rule 26, n = 4, 8 (every root):

* n = 4: V({0}, C) histogram {'0': 1}; gamma by kind {'zero': [0]}; Theorem 3(c) holds for every root: True; R({0} -> D_c) = [0, 1, 1, 2, 1, 1, 2, 2]
* n = 8: V({0}, C) histogram {'0': 1, '2': 8, '3': 1}; gamma by kind {'zero': [9], 'domain': [10], 'with_111': [10]}; Theorem 3(c) holds for every root: True; R({0} -> D_c) = [0, 1, 1, 2, 1, 1, 2, 2]

Rule 26, n = 16 (`check_potentials_16.py`, 16 of 552 roots by Edmonds, wall 3510.2 s): m = 552; min V({0}, C) = 2, hence gamma(C) >= 552 for every C != {0}; gamma({0}) = 551; V({0}, C) histogram {'0': 1, '2': 88, '3': 392, '4': 68, '5': 3}; cycles at resistance 2: 88 (kinds ['domain']); reachable from them in G1: 549; the three cycles with 111: V from {0} = [5, 5, 5], reachable from T2: [False, False, False]; Theorem 3(c) on the computed roots: True; k_c = [0, 1, 1, 1, 1, 1, 1, 2] (exact by the bound: [True, True, True, True, True, True, True, True]).

| root | kind | in T2 | reachable from T2 | gamma | seconds |
|---|---|---|---|---|---|
| 0 | zero | False | True | 551 | 0.8 |
| 537 | with_111 | False | False | 553 | 291.4 |
| 549 | with_111 | False | False | 553 | 246.8 |
| 550 | with_111 | False | False | 553 | 257.5 |
| 371 | domain | True | True | 552 | 248.0 |
| 481 | domain | False | True | 552 | 259.9 |
| 493 | domain | False | True | 552 | 252.8 |
| 292 | domain | False | True | 552 | 253.9 |
| 427 | domain | False | True | 552 | 236.1 |
| 233 | domain | False | True | 552 | 238.8 |
| 458 | domain | False | True | 552 | 259.5 |
| 6 | domain | False | True | 552 | 1.1 |
| 420 | domain | False | True | 552 | 233.6 |
| 266 | domain | True | True | 552 | 232.1 |
| 244 | domain | False | True | 552 | 256.7 |
| 228 | domain | False | True | 552 | 240.5 |

### Side remarks (`check_remarks.py`)

* rule 94, states without 101: walls evolve one step by rule 18: {'n': '4..16', 'cases': 18795, 'violations': 0}
* rule 26, carrier words: c = (n + 4p)/3: {'n': '6..30 even', 'cases': 55, 'violations': 0}

### Comparison with `proofs_94_26/out/` (`compare.py`, run last)

fields compared: 331; disagreements: 0. Field list: `verify_94_26/out/compare.md`.

