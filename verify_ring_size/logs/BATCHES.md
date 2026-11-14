# Batches

Load budget: at most 2 worker processes at any moment, one batch at a time. Costs are CPU time
(time.process_time / resource.getrusage), not wall time. Each entry is written before launch
(expected values) and completed after the run (measured values).

## Batch 0 - solver validation (validate.py, parts A and B)

- What: part A = all 256 rules, n = 3..8, dense Dijkstra / per-root Edmonds / exhaustive in-trees
  against the solver; part B = exact stationary laws at n = 3..6 (256 rules at n = 3, 4; 25 rules
  at n = 5, 6) at eps = 1e-8, 1e-16, 1e-24.
- Workers: 1 process.
- Expected: about 15 CPU-minutes (timed: part B about 15 s per rule at n = 6, 0.5 s at n = 5; part A
  below 0.1 s per case in spot checks), peak memory below 0.3 GB.
- Measured: part A 25.4 CPU-s (1536 cases, 0 failures), part B 437.2 CPU-s (562 cases, 0 failures),
  total 462.6 CPU-s = 7.7 CPU-minutes (logs/validation_summary.json). Peak memory was not recorded
  for this batch.

## Batch 0b - validation part C (rotation shortcut and all-roots potentials at n = 9..12) and cycle census

- What: (C) the 13 sample rules at n = 9..12 solved twice, with one search per rotation orbit and
  with one search per cycle; V, gamma and code distances compared; per-root Python Edmonds on up to
  8 sampled roots when there are at most 400 cycles. (census) cycle counts, bijectivity and the time
  of one search for the 13 rules at n = 8..22, used only to choose the larger n.
- Workers: 1 process, the two scripts one after the other.
- Expected: below 3 CPU-minutes in total, peak memory below 0.5 GB.
- Measured: part C 0.4 CPU-s, 52 cases, 0 failures, peak 196.9 MB (logs/validation_summary.json);
  census 2.6 CPU-s (out/census.jsonl), peak memory not recorded.

## Batch 1 - sample, 13 rules x n = 8..14 (91 cases)

- What: full computation (V by one 0-1 search per rotation orbit, all-roots minimum in-trees, k_c, G1).
- Workers: 2 processes (one case per process).
- Expected: about 1 CPU-minute in total (largest case has 564 cycles; each case is dominated by
  interpreter start-up, about 0.3 CPU-s), peak memory below 0.2 GB per worker.
- Measured: 91 cases, 0 failed, 14.2 CPU-s in total (sum of per-case process CPU time), largest
  single-case peak 56.9 MB (logs/batch_n08_14_measured.json).

## Choice of the larger n (made from out/census.jsonl and logs/estimates_larger_n.json, before any larger case was solved)

The census shows at most 76600 cycles (rule 154, n = 22) and one 0-1 search costs 0.08 CPU-s at
n = 22, so the full computation (dense V, all-roots in-trees) is affordable for every rule at every
n = 15..22 with one exception: rule 154 at n = 22 needs a dense 76600 x 76600 byte matrix (5.9 GB)
and about 1.1 CPU-hours; the machine showed about 13 GB of active memory at that moment, so this
single case is NOT run (it could be noticed).

- Designated three larger n per rule: n = 16 (power of two, multiple of 4), n = 21 (odd, multiple
  of 3) and n = 22 (largest; even, neither multiple of 3 nor of 4) for the twelve rules 22, 26, 35,
  37, 43, 45, 60, 73, 90, 94, 122, 142; for rule 154: n = 16, n = 20 (multiple of 4, largest even n
  that fits in memory) and n = 21 (odd, multiple of 3, F bijective).
- Because the estimated total is only about 1 CPU-hour, all remaining n in 15..22 are computed as
  well (extras: n = 15, 17, 18, 19, 20 for the twelve rules; n = 15, 17, 18, 19 for rule 154), so
  that primes (17, 19) and further multiples of 3 (15, 18) are covered. Estimated CPU per n
  (sum over rules): n = 15..19 about 3 CPU-min, n = 20 about 6 CPU-min, n = 21 about 23 CPU-min,
  n = 22 without rule 154 about 25 CPU-min.
- Every case uses the full computation, including those where F is a bijection (rule 45 and rule 154
  at odd n), so the bijection shortcut is not needed anywhere and is confirmed wherever it applies.

## Batch 2 - sample, 13 rules x n = 15..19 (65 cases)

- Workers: 2 processes.
- Expected: about 3.5 CPU-minutes in total, peak memory below 0.2 GB per worker (largest dense V:
  6314 cycles = 40 MB).
- Measured: 65 cases, 0 failed, 100.8 CPU-s in total, largest single-case peak 190.1 MB
  (logs/batch_n15_19_measured.json).

## Batch 3 - sample, 13 rules x n = 20, 21 (26 cases)

- Workers: 2 processes.
- Expected: about 20 to 30 CPU-minutes in total (census estimate 30 CPU-min; batch 2 came in at 0.63
  of its estimate), of which rule 154 takes about 3 CPU-min at n = 20 and 11 to 16 CPU-min at n = 21.
  Peak memory: about 2.2 GB for rule 154 at n = 20 (dense V of 41626 cycles = 1.65 GB), below 0.8 GB
  for every other case.
- Note: the first launch of batch 3 was stopped by me after 34 s of wall time (8 cases finished and
  kept, 60.4 CPU-s; two cases in flight were discarded) in order to add one output to solve.py: the
  complete list of selected orbits is now written to out/selected/sel_r<RULE>_n<N>.tsv whenever it is
  too long for the JSON record (more than 60 orbits). No computed quantity changed. The batch was then
  resumed from the checkpoint with the same expected cost (remaining 18 cases). Earlier cases with
  partial lists are re-solved in batch 3b, which also checks that their records are reproduced
  identically.
- Measured: 26 cases, 0 failed; 60.4 CPU-s (first launch, 8 cases) + 1169.5 CPU-s (resumed launch,
  18 cases) = 1229.9 CPU-s = 20.5 CPU-minutes; largest single-case peak 1888.8 MB (rule 154, n = 20).
  (logs/batch_n20_21.log; batch_n20_21_measured.json covers the resumed launch only.)

## Batch 3b - complete selected-orbit lists for earlier cases (supplement_lists.py)

- What: the 35 cases with n <= 20 that were solved before the list files existed and have more than
  60 selected orbits are solved again; the new record must equal the stored one.
- Workers: 1 process.
- Expected: about 2.5 CPU-minutes (their first solve took 124 CPU-s), peak memory below 0.3 GB.
- Measured: 35 cases, all 35 records reproduced identically, 115.7 CPU-s, peak 284.1 MB
  (logs/supplement_lists.jsonl).

## Batch 4 - sample, 12 rules x n = 22 (rule 154 excluded, see the choice above)

- Workers: 2 processes.
- Expected: about 17 to 25 CPU-minutes in total (census estimate 24 CPU-min; batch 3 came in at 0.69
  of its estimate), of which rule 35 takes about 5 to 7 CPU-min. Peak memory below 0.9 GB per worker
  (largest dense V: 16930 cycles = 0.29 GB, plus about 0.3 GB of per-state arrays at n = 22).
- Measured: 12 cases, 0 failed, 1423.3 CPU-s = 23.7 CPU-minutes in total; largest single-case peak
  1082.8 MB (logs/batch_n22_measured.json), i.e. above the 0.9 GB stated before launch.

## Not run

- Rule 154 at n = 22 (76600 cycles; dense V of 5.9 GB, about 1 CPU-hour): not attempted, see the
  choice above. The designated larger n for rule 154 are 16, 20, 21.
