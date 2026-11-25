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

## Open boundaries (25 November 2026)

Written by Claude, the reader outside the sessions, on 25 November 2026, after reading `report_boundaries.md`
(the study of the night of 24 to 25 November 2026: the same noise question on a row with walls instead of a ring).
When this was written no verification session had read that study. The session could not commit; its six patches
were applied here to `main` at version 0.5 (b3a73ce) as six commits, without change. The session had worked on the
tree of version 0.4 (2765f7e), and the status block and Section 9 of the report still describe that situation.

### What `walls/` is

Five scripts that share no code with the repository or with the three scripts above. `walls.py` builds the step
table for ring, null, fixed-1 and reflecting walls from the definition, finds the cycles, the one-flip graph G_1
from single flips of the states of each cycle, and, up to a cap on the number of cycles, the least resistance from
every cycle to every state, V, the potential of every cycle (own implementation of Edmonds' algorithm, one run per
root) and every k_c. Above the cap it computes G_1 only; if G_1 has one closed class K, then K is the selected set
and gamma_min = m - 1 (an in-tree of m - 1 edges of weight 1 exists exactly for the roots in K). Below the cap that
statement is asserted against the potentials wherever G_1 has one closed class, not used. On the ring the script
reproduces the values of k* in the ring rows of the table in Section 5.0 of the report (from `data/fw_sweep.csv`)
for rules 154, 94, 43, 90, 26 and 22 at n = 4..9.

### Runs (25 November 2026)

Python 3.13.18, numpy 2.5.3, scipy 1.18.1, Linux container with 2 cores, two processes; a few minutes in all.
The records are in `walls/out/`; `walls/out/summary.txt` holds the printed output of the other four scripts. The
comparison scripts were run again on the author's machine against the committed data files.

| script | range | compared with | result |
|---|---|---|---|
| `walls.py null` | all 256 rules, n = 4..9; the 160 class representatives, n = 10..16; the 12 classes that change side, n = 17..20 (2704 records; cap 70, 120 for n = 10..14, 60 for n = 15, 16, 40 for n = 17..20; rule 218 at n = 15 without cap) | `data/boundaries/null_sweep.csv` (2128 records): number of cycles, number of selected cycles, gamma_min, missed codes, whether the cycles jointly miss a code; for the records marked bijective, which the study did not solve: all cycles selected and no code missed | no difference; every k_c compared in 1736 records, no difference |
| the same records | | `data/boundaries/ring_vs_null.csv` (2704 records): side, missed codes, k* | no difference in side or k* (k* compared in 2351 records); finding 2 below |
| `walls.py reflect` | the 88 class representatives, n = 4..12 (792 records; cap 120, 100 for n = 11, 12; rule 77 at n = 11, 12 without cap) | `data/boundaries/reflect_sweep.csv` (792 records), same fields | no difference; every k_c compared in 723 records |
| `affine.py` | the 16 affine rules, n = 3..128, own linear algebra over GF(2) | `data/boundaries/affine_null.csv` (2016 records): dimension of the periodic subspace, bijectivity, missed codes | no difference; rules 90 and 165 miss a code exactly at n = 3, 7, 15, 31, 63, 127; rules 150 and 105 only at n = 5 |
| `local.py` | own simulation | Sections 5.2, 5.3, 5.5 and Lemmas M, M' of the report | rule 94: the crystal 110...11 is fixed with radius 2 at every n = 2 mod 3, 5..62; rule 133: (010)^k at every 3 \| n, 6..60; rule 75: radius 2 for n <= 41 and radius 1 at n = 44, 47, ..., 62; rule 22: every single flip of 0 dies exactly at n = 6, 14, 30, 62 (finding 3); rules 154 and 26: the orbit of every single flip equals the rule-90 orbit (n = 3..69), all die at n = 3, 7, 15, 31, 63; rule 122: the checkerboard 2-cycle has radius 2 at n = 7 and 15 only (4..61); rule 137: the 2-cycle has radius 2 at n = 7 and every odd n from 11 to 61; Lemma M holds (n = 1..7) for exactly the 16 rules named in the report, Lemma M' for exactly the 64 reflection-symmetric rules |
| `counts.py` | from `walls/out/null_n04_20.csv` and own step tables | global counts of Section 4 | 110, 38 and 12 classes; 31 and 9 classes change side in n = 4..14 and 8..14; 186, 187, 189, 187 rules with k* >= 1 at n = 12, 13, 14, 16; 181 and 180 rules whose cycles jointly miss a code at n = 12 and 16 (ring at n = 12: 138); 562 records with a single cycle; more than one closed class of G_1 only for rule 218 at n = 7 and 15; the list of bijective classes: all as in the report |

I also read the proofs of Section 5.1 (Proposition L, Lemmas F, W and M, Theorems 90 and 150) and of
Proposition N, and found no gap. That is one reading by the reader who planned the session, not a verification.

### Findings

1. Attribution. `PREDICTIONS_boundaries.md` and Section 7 of the report call the expectations (a), (b), (c)
   "Frank's expectations". They are not his. Claude wrote them on 24 November 2026 in the conversation in which the
   session was planned, and the task passed them on as "expectations from Frank's chat with Claude". Their
   deterministic facts (the mirror embedding for n = 5, 6, 7, the fixed point of rule 94, nilpotency of rule 90,
   bijectivity of rules 60 and 150) had been computed in that conversation before the session started; only the
   statements about k* were predictions. The sealed file is not to be edited; the label in Section 7 of the report
   and its sentence "Frank's: 5 items, all correct" should be corrected when the findings of a verification are
   handled.
2. `data/boundaries/ring_vs_null.csv`, column `null_missed`. For a rule that is not the representative of its
   null class the column gives the missed codes of the representative, not those of the rule in the row, which are
   their mirror image (codes 1 and 4 exchanged, 3 and 6 exchanged). This concerns 142 of the 2704 records
   compared. The values of k* in the file and the tables of the report are not affected.
3. Section 5.3 and open point 3 of the report say that for rule 22 the sizes n = 55, 56, 57 are undecided. At
   n = 55 and n = 57 some single flip of 0 runs into a cycle other than {0} within 20000 steps, so not every flip
   dies there. Only n = 56 is undecided at 20000 steps.

No disagreement with a computed or proved statement of the report was found in these ranges.

### Not covered

The literature review (`literature_boundaries.md`) and the conflict with a table of Wang et al. that the report
names; the certificates and the study's own check of stationary laws; null walls for n >= 17 except the 12 classes;
which cycles are selected in the descriptions of Sections 5.2 to 5.5, beyond their number and the codes they miss;
the proofs as a verification.
