# Reader checks

Written by Claude, the reader outside the sessions (the conversation in which the sessions were planned and their
results were read). 20 November 2026.

## What this folder is

Three scripts that recompute, on small rings and from the definitions only, the statements of the ring-size paper
(`paper/ring_size_paper.tex`) and of the proof documents. They were written in that conversation between 17 and 20 November 2026, when the
proof documents and the paper were read, and rerun on 20 November 2026 to store the output that is in `out/`. They share no code with the scripts of the repository.

What "from the definitions" means here: the step table of the rule on all 2^n states; the cycles; for every cycle
the least resistance to every state (breadth-first search by number of flips, closed under F at each level); V
between cycles; the stochastic potential of every cycle as the weight of a minimum spanning in-tree (Edmonds'
algorithm, `networkx.minimum_spanning_arborescence`, one run per root); the selected set; the indices k_v from
their definition; the one-flip graph G_1 from single flips of the states of each cycle, its strongly connected
components and closed classes. Theorem A is not used to compute anything; where potentials were computed, the
statement S = (union of closed classes) is a result of the comparison.

## What it is not

* Not an independent verification in the sense of the `VERIFICATION_*.md` reports. The reader is the same one who
  did the "second reading" named in `report_ring_size.md`, and who wrote the tasks of the sessions.
* Small rings only; nothing here says anything about all n.
* The three scripts share two functions (`step_table`, `codes_of`, in `check_43_142.py`). An error in them would
  affect all three. Bit i of the integer of a state is cell i.
* The outputs are the raw lines printed by the scripts (Python dictionaries), not a report.

## Runs (20 November 2026)

Python 3.13.18, numpy 2.5.3, networkx 3.7, Linux container with 2 cores, each script a single process. Wall time:
`check_43_142.py 16 12` 40 s; the others below 30 s each.

| command | output file | range | result |
|---|---|---|---|
| `python check_43_142.py 16 12` | `out/check_43_142_n16_p12.txt` | rules 43 and 142; G_1 for n = 4..16; potentials for n = 4..12 | closed classes of G_1 as in Theorem 3.20 and Theorem 3.26 of the paper at all 26 (rule, n); for 4 dividing n the distance to X in G_1 is \|w - n/2\|/2 for every cycle (8 of 8); with potentials: gamma_min = m - 1, S = the claimed set, k* = 1 iff 4 divides n, and the edges of G_1 are exactly the pairs with V = 1 (18 of 18) |
| `python check_94_26.py 94 17 60` | `out/check_94_26_rule94_n17_p60.txt` | rule 94, n = 4..17 with 3 not dividing n (10 ring sizes); potentials where m <= 60 (n = 4, 5, 7, 8) | one closed class K at every n; every cycle with a 101 lies in K and no cycle outside K has a 101 (10 of 10); the states of K contain all eight codes for n >= 5, and the codes 010 and 101 only at n = 4; {0} lies in K at n = 5, 7, 8 and not at n = 4, 10, 11, 13, 14, 16, 17; no edge of G_1 enters {0} at n = 16; with potentials: S = K and gamma_min = m - 1 (4 of 4) |
| `python check_94_26.py 26 18 60` | `out/check_94_26_rule26_n18_p60.txt` | rule 26, even n = 4..18; chi for n <= 16 | one closed class at every n; it is {0} at n = 4, 8, 16; chi(Fx) <= chi(x) for every state, n = 4..16; for even n that is not a power of two every cycle outside the closed class contains 111, and the states of the closed class contain every code other than 111 (n = 6, 10, 12, 18) or all codes (n = 14) |
| `python check_94_26.py 26 14 80` | `out/check_94_26_rule26_n14_p80.txt` | rule 26, even n = 4..14, with potentials | S = the closed class at every n; k_v for the codes 000..111: n = 4: 0,1,1,2,1,1,2,2; n = 8: 0,1,1,1,1,1,1,1; n = 6, 10, 12: 0,0,0,0,0,0,0,1; n = 14: all 0 |
| `python check_154_94.py 14` | `out/check_154_94_n14.txt` | rule 154: n = 3..14 (potentials for n = 3..11, G_1 only for n = 12, 13, 14); rule 94: n = 3, 4, 6, 9, 12 (potentials for n = 3, 4, 6, 9); rules 43 and 142: healing time, n = 4, 8, 12, 16, 20 | rule 154: at n = 4, 8 the only closed class is {0}, S = {{0}}, gamma({0}) = m - 1, gamma = m for every other cycle, k_v = 0,1,1,1,1,1,1,1; at every other n G_1 is strongly connected, and for n <= 11 all cycles are selected with gamma = m - 1 and all k_v = 0 (Theorems 3.9 to 3.11). Rule 94 at n = 6, 9, 12: the closed classes are the three crystal phases and F^3(x + e_j) = x for every crystal phase x and every cell j; at n = 6, 9: S = the three crystal phases and k_v = 1,1,1,0,1,0,0,1 (Lemma 3.32, Theorem 3.43(i)). Rule 94 at n = 4: the closed class and S are the two checkerboards, k* = 1; at n = 3: F^3(x + e_j) = x fails (Remark 3.44). Healing time: 1 and n/2 - 1 as in Proposition 3.22 at all 10 (rule, n) |

No disagreement with a statement of the paper or of a proof document was found in these ranges.

## Not covered

Rule 26 at odd n; rule 26 with potentials at n = 16 and 18; rule 94 with potentials at n >= 10; rule 154 with
potentials at n >= 12; the lemmas of the proofs one by one (the sessions' own scripts and the verification
sessions test those); anything about the literature.
