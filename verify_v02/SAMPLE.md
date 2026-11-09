# Sealed sample for the independent verification of v0.2

Sealed before reading `report.md`, `note/note_v0.2.tex`, `literature.md`, `PREDICTIONS.md` or any `data/fw_*` file,
and before computing any order k_c in the sample (one exception, see "Seen before sealing").
The selection is made by `make_sample.py` from the class representatives and from
`out/cycle_counts_n17_n20.jsonl` (cycle counts of the noiseless map, produced by `count_cycles.py`);
its output is `SAMPLE.json`. Nothing else enters the selection.

## Pairs (rule, n)

| n | classes | how chosen |
|---|---|---|
| 4 | all 88 representatives (smallest rule number in the orbit under reflection and complementation) | fixed by the brief |
| 5 | all 88 representatives | fixed by the brief |
| 12 | 7, 19, 22, 23, 30, 41, 106, 108, 200, 232 | fixed by the brief |
| 12 | 29, 40, 43, 46, 62, 90, 105, 122, 140, 170 | `numpy.random.default_rng(20261109).choice(remaining 78 classes in increasing order, 10, replace=False)`, sorted |
| 17 | 4, 22, 37, 72 and 29 | 4 drawn by `default_rng(20262829).choice(pool, 4, replace=False)`, pool = classes with at most 20000 cycles at n = 17 and at n = 20, minus the two max-cycle classes below; 29 = the class with most cycles within the cap at n = 17 (15777 cycles) |
| 20 | 4, 22, 37, 72 and 132 | the same 4 drawn classes; 132 = the class with most cycles within the cap at n = 20 (15128 cycles; tie with 140 broken towards the smaller rule number) |

Cycle counts of the sample at n = 17: 4: 3571, 22: 52, 37: 349, 72: 664, 29: 15777.
At n = 20: 4: 15127, 22: 170, 37: 1046, 72: 2090, 132: 15128.

Affordability cap: at most 20000 cycles per class. Route (b) needs one 0-1 breadth-first search per cycle
(pilot, `logs/pilot_timing.txt`: about 0.02-0.05 s per cycle at n = 20) and a tropical GTH elimination on the
m x m cycle-cost matrix (O(m^3); about 2 s at m = 3000, about 5 min and 2 x 1.8 GB at m = 15000).
The next classes above the cap (n = 17: class 76 with 31553 cycles; n = 20: class 5 with 38503) would need
about 40 min / 16 GB and 70 min / 24 GB for the elimination alone, beyond a laptop run that should go unnoticed.

## Routes

(a) Exact stationary laws: at n = 4 and n = 5 all 88 classes, as exact rational functions of eps
(Markov chain tree theorem: unnormalised pi(x) = principal minor of I - P, an integer polynomial in eps,
obtained by exact evaluation at integer points and exact interpolation, checked at an extra rational point
against an exact linear solve). At n = 12 the 20 classes above: own subtraction-free GTH elimination in
float64 at eps = 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9; k_c read off as the local slope of log nu_c
against log eps.

(b) Minimum resistances and minimum in-trees: cycle-to-cycle minimum resistances by 0-1 breadth-first
search (edges u -> F(u) cost 0, u -> u xor e_i cost 1), minimum in-tree weights on the cycles by
tropical (min-plus) GTH, orders of all other states from ord pi(x) = min_y [ord pi(y) + Hamming(F(y), x)],
k_c = min of ord pi(x) over states containing code c. Applied to every pair in the table. As a validation of the
reduction, the full 2^n-state tropical GTH (no reduction to cycles) is compared state by state at
n = 4..12 (all 88 classes; added here before any comparison with the claims).

Extensions that are cheap with route (b) (all 88 classes at n = 12, and any pair needed later for the
certificate sample of step 3 or the comparison of step 6) are run after this seal and are reported as
post-seal additions, never as part of the blind sample.

## Seen before sealing

- The file list of the branch (names only), `VERIFICATION.md` of v0.1, and the git log subjects.
- A memory note from an earlier session of this project, truncated, stating that v0.2 classified all 88
  classes at n = 12 with certificates and that 87 of 88 agree with the v0.1 trend. No class-level values.
- A smoke test of route (b) printed k_c = 0 for all eight codes for rule 30 at n = 12 (a pair fixed by the
  brief, so the selection was not affected).
