# Verification of the ring-size study, part 1 (steps 2 to 6): findings

Object: branch `ring-size-mechanisms` (commits 8d68e54, 8bcad22, 1e256cd): `report_ring_size.md`, `PREDICTIONS_ring_size.md`, `data/ring_size/`, `code/ring_size/`, `reproduce_ring_size.sh`, and the untracked `PR_DRAFT.md`. Nothing in the study was changed. All code, outputs and logs of this part are in `verify_ring_size/phase2/`; file names below are relative to that folder. The sealed blind sample (`../out/sample.jsonl`, commit a384763) was not changed.

How to read the labels. **Verified by my computation**: recomputed with the verification's own code and compared. **Verified by reading**: checked by reading the text or the study's code, nothing recomputed. **Not verified**: listed in section C. 'Sealed' marks a value taken from the sealed sample; 'supplement' marks a value computed after the seal with the same own solver (`extras.py`, `sweep88.py` and the certificate scripts). Line numbers refer to `report_ring_size.md` unless a file is named.

Conventions reconciled (`out/compare_sample.json`, block `conventions`). The study writes a state as an integer with cell i at bit i and prints the pattern with cell 0 first; the sample uses the bit string with cell 0 as the most significant bit. The printed patterns are directly comparable: all 60355 orbit patterns of `cycle_orbits.csv.gz` are periodic states under the sample's map. The study's orbit representative is the smallest integer (cell i at bit i) over the cycle and its rotations (60355 of 60355 rows confirmed); the sample's is the lexicographically smallest string. The column `drift` is the smallest s with F(x) = x rotated right by s cells, -1 if there is none (60355 of 60355 rows).

Cost of this part (CPU time, 1 process at a time; `out/cpu_total.json`): 1.27 CPU-hours in total. extras.py (out/extras.jsonl) 221 s; sweep88.py (out/sweep88_summary.json) 518 s; seed_orbits.py, seed_orbits_pass3.py (out/seed_compare.json) 933 s; v154_n22.py (out/v154_n22.json) 2894 s; sampled_reach_check.py 8 s. Expected and measured values per batch: `../logs/BATCHES_phase2.md`.

Reductions of scope (declared): the 88-class sweep skipped 20 of 1496 (rule, n) cases with more than 20000 cycles (n = 15..17) or 16000 cycles (n = 18, 19); the atlas comparison covers 1232 of 1327 records (n = 20 and the skipped cases are not covered); potentials per orbit were compared for 23833 of 60355 orbit rows and by the histogram of potentials for all 180 non-bijective cases; 15 seed orbits remain undetermined; the dense Edmonds run for rule 154 at n = 22 was replaced by a level-wise Edmonds on streamed rows of V (validated against the dense one in 1399 sweep cases); the study's pipeline and tests were not executed.

## A. Errors found

Severity classes: wrong result / wrong proof step / overstated tag or wording / bookkeeping. No wrong proof step was found. A 'query' is a point where I am not sure it is an error.

### F1. The list of ring sizes where the seed orbit of rule 22 returns to 0 is incomplete (n = 241 is missing)

* Location: lines 331-332 (sentence tagged [computed]); also line 500, lines 363-365 and 488-489 ('computed up to 256'), mechanism table line 211 ('computed to 256'); `PR_DRAFT.md` lines 37-38
* Severity: wrong result
* Evidence: `out/seed_compare.json`, `out/report_numbers2.json`, `out/rule22_n241_check.json`, `out/seed_orbits_own.csv` (verified by my computation)
* What is wrong: The sentence lists the n not divisible by 4 at which the single-flip orbit of rule 22 returns to 0 'in n <= 256' as 5, 6, 7, 14, 15, 30, 31, 61, 62, 63, 121, 125, 126, 127, 253, 254, 255. In the study's own `seed_orbits.csv` 25 values of n not divisible by 4 (185, 186, 187, 193, 194, 195, 201, 205, 209, 210, 211, 213, 217, 218, 219, 221, 229, 234, 235, 237, 241, 242, 243, 245, 249) are undetermined at the cut-off of 400000 steps, so the list is only the list of the returns found. With own code (Brent cycle detection, up to 6e9 steps) the orbit at n = 241 reaches the zero state after 1303564 steps; this was confirmed with a second implementation (Python integers, `out/rule22_n241_check.json`). Of the 31 n the study left undetermined for rule 22, 27 were settled by own simulation, 2 only by Proposition R22 (4 | n, not a power of two: no return), and n = 242, 243 are still open. The complete list of returns found is 4, 5, 6, 7, 8, 14, 15, 16, 30, 31, 32, 61, 62, 63, 64, 121, 125, 126, 127, 128, 241, 253, 254, 255, 256.
* Proposed fix: Add n = 241; replace 'computed up to 256' by the set of n actually decided and name the open n (242, 243 after this verification); in 7(c) write '121, 125, 241, 253'.

### F2. 'Returns exactly at n = 7, 15, 31, 63, 127, 255' for rule 122 is not supported

* Location: lines 348-349 (tag [computed])
* Severity: overstated tag
* Evidence: `out/seed_compare.json`, `out/report_numbers2.json` (verified by my computation)
* What is wrong: 33 values of n are undetermined in the study's file, so 'exactly' does not follow. With own code 20 of them were settled (none returns); 13 remain open: n = 133, 141, 157, 165, 189, 201, 205, 213, 221, 229, 241, 243, 249. No return other than the six listed was found.
* Proposed fix: Write 'returns at n = 7, 15, 31, 63, 127, 255 and at no other n <= 256 whose orbit could be decided; 13 values of n are open', and tag the pattern 2^k - 1 as [observed].

### F3. PR draft states the class-22 pattern as a result up to n = 256

* Location: `PR_DRAFT.md` lines 37-38 ('class 22 switches exactly where a single flip of the zero state dies on the ring (n = 4..8, 14..16, 30..32, 61..64, also 121, 125, 253 in n <= 256)')
* Severity: overstated tag or wording
* Evidence: verified by reading; k* values: sealed sample and `out/sweep88.jsonl` (n <= 22 only); `out/seed_compare.json`
* What is wrong: k* of class 22 is computed for n <= 22 only. Beyond that only the seed orbit is known, i.e. whether the zero state can be left by one flip; that k* switches there needs the reachability statement, which the report itself lists as not proved and which is sampled at n = 30, 31, 32 only. The list in the draft also omits 126-128 and 254-256, which are in the report's own table, and n = 241 (F1).
* Proposed fix: Write 'k* = 1 exactly where the single-flip orbit of 0 returns, for n = 4..22; the orbit returns also at ... (seed orbit only, k* not computed)'.

### F4. Class 45: 'all cycles are selected' at every even n >= 10 is false at n = 18 and n = 22

* Location: lines 375-376 (tag [computed])
* Severity: wrong result (text; the data files are right)
* Evidence: `out/details_45_73.json`, `out/report_numbers.json` (check sec5_5_45_even); sealed sample and the study's own `cycle_orbits.csv.gz`
* What is wrong: At n = 18, 199 of 201 cycles are selected; the unselected ones are the uniform 2-cycle itself and the cycle of (011)^6. At n = 22, 271 of 272 are selected. The study's `cycle_orbits.csv.gz` has the same rows as not selected. The radius statement (radius 1 at even n >= 10) is correct, and k* = 0 is unaffected.
* Proposed fix: Write 'it has radius 1 and all cycles are selected except two cycles at n = 18 (among them the uniform 2-cycle) and one cycle at n = 22'.

### F5. Class 73: the uniform 2-cycle is not selected at n = 22 either, and no cycle of temporal period 3 is selected at n = 9

* Location: lines 377-378 (tag [computed]); related: mechanism table line 216
* Severity: wrong result (text; the data files are right)
* Evidence: `out/details_45_73.json`, `out/report_numbers.json` (checks sec5_5_73_uniform, sec5_5_73_n9); sealed sample and the study's own `cycle_orbits.csv.gz`
* What is wrong: 'At all other n it is selected' fails at n = 22: the uniform 2-cycle has potential 13304 against the minimum 13303 (study file) and is not selected; k* stays 0 because 462 of the 463 orbits carrying code 7 are selected. At n = 9 the selected cycles are the three phases of the fixed point (011)^3 and two orbits of temporal period 2; the two orbits of temporal period 3 are not selected. If 'period-3 cycles' means the crystal of spatial period 3, the sentence should say so.
* Proposed fix: Write 'at n = 9 none of the three orbits carrying code 7 is selected (selected: the fixed-point crystal (011)^3 and two orbits of period 2); at n = 22 the uniform 2-cycle is again not selected, but other carriers of code 7 are'.

### F6. The cost claim for class 154 at n = 22 is not supported in compute time

* Location: line 534, lines 454 and 528; `data/ring_size/stopped_runs.csv`; `reproduce_ring_size.sh` line 15; `PR_DRAFT.md` lines 43, 57, 61; `code/ring_size/make_report.py` line 162
* Severity: overstated tag or wording
* Evidence: `out/cost_claim.json`, `out/pmset_sleep_wake.txt`, `out/v154_n22.json` (verified by reading the study's logs and code; sleep interval from the system power log)
* What is wrong: The 7.4 h are wall-clock time between the start of the job (2026-11-14 00:46:21, birth time of `log_mech_154_n22.txt`) and the stop (2026-11-14 08:09 in `stopped_runs.csv`, whose column is named `wall_hours`). The power log shows the machine asleep from 2026-11-14 02:00:31 to 2026-11-14 08:08:00, i.e. 6.12 h of the 7.39 h. The job had at most 76.2 minutes (1.27 h) of awake time, below the 5 h cap and below the study's own estimate of 2-3 h (`reproduce_ring_size.sh` line 5). No CPU time was recorded anywhere: the log holds one line ('1 jobs to run, 194 already in checkpoint'), `cost_seconds` in `run_mech.py` is `time.time()` wall time and is written only when a job ends. The cap of 5 h is defined nowhere in the repository (not in `run_mech.py`, which has no cap or time-out option, not in the reproduce script, not in the sealed predictions); `stopped_runs.csv` is written by no script. The case is not expensive: with own code the result follows from the one-flip graph in 0.4 CPU-seconds (`out/v154_n22_g1_timing.json`) and the full cross-check took 48 CPU-minutes with 2266 MB (section B).
* Proposed fix: Replace the sentence by: 'Class 154 at n = 22 was started at 00:46 and stopped at 08:09; the machine was asleep from 02:00 to 08:08, so the job ran for at most about 1.3 h and was stopped unfinished; its CPU time was not recorded. It is not computed in this study.' Rename the outcome 'not tested: run stopped above the stated cost cap' accordingly, define the cap (wall or CPU) where it is used, and record CPU time (`time.process_time()`) per job. The value itself can be taken from this verification: k* = 0.

### F7. 'Total CPU 1.9 h' is a sum of wall-clock times

* Location: line 534; file table line 519 calls the same column 'wall time'; `code/ring_size/run_mech.py` lines 26 and 38, `make_report.py` line 163
* Severity: bookkeeping
* Evidence: `out/cost_claim.json` (verified by reading the study's code; sum recomputed from the study's `mech_cost.csv`)
* What is wrong: `cost_seconds` is `time.time()` at the end minus the start of each job; their sum is 1.90 h. For the n = 21, 22 batch alone the log gives real 51m1.820s, user 80m42.565s, sys 17m20.328s, i.e. more CPU than wall with two workers.
* Proposed fix: Write 'sum of the wall times of the jobs 1.9 h' or record CPU time.

### F8. One sealed prediction is reported as holding after it was narrowed (class 26 at n = 8)

* Location: line 433; `data/ring_size/predictions_outcome.csv` row 'P6 / 26, other n with k* >= 1: missing code 7'; `code/ring_size/check_predictions.py` line 83
* Severity: overstated tag or wording
* Evidence: `out/predictions_recount.json`, `out/predictions_recount.csv` (verified by my computation, from own data and separately from the study's files)
* What is wrong: Sealed text (P6): 'For class 26 the same holds at n = 16 (k* = 2, zero state alone); at the other n with k* = 1 the missing code is 7 (111) with a different mechanism.' The check excludes n = 8 as well as n = 16. n with k* = 1: [8, 9, 10, 12, 13, 15, 18, 19, 21]; n among them where the missing codes are not exactly {7}: [8] (n = 8: zero state selected alone, codes [1, 2, 3, 4, 5, 6, 7] missing). So this part fails at n = 8 (8 = 2^3 was overlooked when the prediction was written) and holds at the other n. On the study's own partition into 50 rows my outcomes are: fails 6, holds 41, holds (observed, sampled) 1, holds (trivially) 1, not tested 1; the study states: fails 5, holds 41, holds (observed, sampled) 1, holds (trivially) 1, not tested 2. The difference is this row and the row for class 154 at n = 22, which I computed (holds, computed k* = 0).
* Proposed fix: Report the row as 'fails at n = 8 (zero-state mechanism), holds at n = 9, 10, 12, 13, 15, 18, 19, 21' and change the counts.

### F9. The outcome table does not cover every sealed statement

* Location: lines 409-412 and file table line 529 ('outcome of every sealed prediction'); `check_predictions.py` docstring; `PR_DRAFT.md` lines 42-43
* Severity: bookkeeping
* Evidence: `out/predictions_recount.json` (block parts_omitted_by_study_table), `out/predictions_recount.csv`
* What is wrong: I split the sealed text into 92 parts; the study's 50 rows cover 63 of them. The 29 uncovered parts are: the general statements G1 to G3, the column 'proof for all n expected?' of the class table, and sub-claims of P3, P4, P8, P9. Of these, 21 hold, 6 fail, 1 was not tested (sampled test at n = 64) and 1 is not testable. The failing ones are: G3 (incommensurability: expected proved by a finite machine-checked certificate for every class where it applies); T94_dir0 (94: direction 0 (3 does not divide n gives k* = 0): proof for all n expected (G3 + G1)); T43_dir0 (43: as for 94: direction 0 proof expected); T43_radius (43: as for 94: radius proof expected); T142_dir0 (142: as for 94: direction 0 proof expected); T142_radius (142: as for 94: radius proof expected). Three outcomes are typed into `check_predictions.py` instead of being decided from data (lines 46-47, 54, 116). The row for P9 merges three k* predictions (n = 32, 24, 28). The PR draft's '41 hold, 5 fail, 2 not tested' leaves out the two qualified rows ('holds (trivially)', 'holds (observed, sampled)').
* Proposed fix: Add rows for G1-G3 and for the proof expectations (G3 and the direction-0 proofs for 94, 43, 142 were not obtained; the radius proof was obtained for 94 only), or state that the table covers P1-P9 and the k* table only.

### F10. '432 (rule, n) pairs (all 88 classes at n = 4..8, the 13 switching classes at n = 9, 10)' describes 466 pairs

* Location: lines 97-98; `PR_DRAFT.md` line 48
* Severity: bookkeeping
* Evidence: `out/compare_derived.json` (block verify_mech_files), `out/report_numbers.json` (check sec3_verifier_pairs)
* What is wrong: The two verifier files hold 432 rows; the pairs named in the text number 466. The 34 missing pairs are exactly the bijective maps, which the verifier does not treat.
* Proposed fix: Write '432 non-bijective (rule, n) pairs; the 34 bijective pairs are not covered by the verifier'.

### F11. Summary: 'class 94 for all 3 | n' includes n = 3, where the statement is false

* Location: lines 22-23; correct in the body (lines 246-248, 477: n >= 6)
* Severity: overstated tag or wording
* Evidence: `out/crystal_radius_own.csv`, `out/crystal_checks.json` (radius_lt2)
* What is wrong: At n = 3 a single flip leaves the crystal (radius below 2: [[94, 3]]); Lemma H needs n >= 7 and n = 6 is computed.
* Proposed fix: Write 'class 94 for all 3 | n with n >= 6'.

### F12. More than 'one reachability statement' is unproved

* Location: Summary lines 24-25 ('this single statement'), 7(a) lines 479-481, tag at line 256; `PR_DRAFT.md` lines 34-35
* Severity: overstated tag or wording
* Evidence: verified by reading; `out/crystal_radius_own.csv`, `out/seed_compare.json`
* What is wrong: 'Each of the crystal and zero-state patterns is proved conditional on one reachability statement' holds only for the direction 'k* >= 1' of class 94 (n >= 6), of 154 and 26 at n = 2^k and of 22 at 4 | n. Also unproved are: (i) the radius of the crystal (0011)^{n/4} of classes 43 and 142 beyond n = 400 (computed, Lemma H does not apply), so the tag '[proved conditional on reachability]' at line 256 is too strong for these two classes; (ii) the seed sets of rule 22 for n not divisible by 4 and of rule 122, i.e. the radius of the zero state there; (iii) the direction 'condition fails, hence k* = 0' for every class except odd n of 154 and 45, which needs the closed classes of G1 and is not a statement about reaching the crystal or 0 (the report says this itself in 5.1 and in section 8).
* Proposed fix: Name the three gaps in the Summary and in 7(a); tag line 256 '[proved for class 94 conditional on reachability; for 43, 142 conditional on reachability and on the radius beyond n = 400]'.

### F13. 'Every number below is filled in from a data file' is not the case for the prose

* Location: lines 5-6
* Severity: overstated tag or wording
* Evidence: `out/report_numbers2.json` (block template); verified by reading `make_report.py` and `report_template.md`
* What is wrong: The template has 338 lines, 287 of them without a placeholder, and all of these occur verbatim in the report; 41 placeholders are filled by `make_report.py`. Ring sizes and counts in the static lines are typed: for example 'n = 4..8, 14, 15, 16' (line 363), '(121, 125, 253)' (line 332), 'n = 7, 15, 31, 63, 127, 255' (line 349), 'n = 11, 12, 17, 18' (line 370), and the sentences of F4 and F5. The mechanism table is typed in `make_report.py` (lines 71-83), the cut-off 400000 at line 112, and `stopped_runs.csv` has no generating script. Both wrong sentences (F4, F5) are typed text; the list of F1 is generated from the rows the study determined, the claim around it is typed.
* Proposed fix: Either generate those sentences from the data files or say 'tables and the numbers in them are filled in from data files'.

### F14. gamma_min = 0 in the records of bijective maps is a placeholder

* Location: `data/ring_size/mechanisms.csv` (14 rows: rules 45 and 154 at odd n), `data/ring_size/atlas/mechanisms_atlas.csv`; not used in the report text
* Severity: bookkeeping
* Evidence: `out/compare_sample.json`, `out/compare_mismatches.csv`, `out/atlas_check.json`, `out/misc_checks.json`
* What is wrong: The minimum potential of a bijective map is m - 1 (sealed sample: full computation in all 14 bijective cases). The study writes 0 there; this is the only field that differs between the sealed sample and `mechanisms.csv` (14 of 194 record comparisons), and the only one in the atlas (80 of 1232). The same value is in the v0.2 sweep (12 of the 169 common pairs). The bijective records also carry no orbit rows and no G1 fields.
* Proposed fix: Write m - 1, or leave the field empty and say so in the file description.

### F15. 'Wherever the zero state is selected alone, Lemma B holds' is flagged in 9 of 13 cases

* Location: lines 298-299 (tag [computed])
* Severity: overstated tag or wording (minor)
* Evidence: `out/compare_derived.json` (block zero_mechanism)
* What is wrong: In n = 8..22 the zero state is selected alone in 13 (rule, n) cases of the six rules of `zero_mechanism.csv`. The study's flag `g2_holds` is True in 9; the other 4 are rules 60 and 90 at n = 8, 16, where {0} is the only cycle and the flag is False. Mathematically nothing is wrong (with one cycle there is nothing to prove).
* Proposed fix: Add '(in the nine cases with more than one cycle)'.

### F16. Table 5.6: 'distinct_cycles' counts rotation orbits, and the paths are not stored

* Location: lines 386-389; `data/ring_size/sampled_reach/*.csv`
* Severity: bookkeeping
* Evidence: `out/sampled_reach_check.json`, `out/sampled_paths_own.jsonl` (verified by my computation)
* What is wrong: The label of a sampled cycle is the smallest state over the cycle and all rotations (all 3400 labels reproduced under this convention, 1810 under 'smallest state on the cycle'), so the column counts rotation orbits of cycles: for rule 22 at n = 32 the 10 sampled orbits are 55 cycles, for rule 94 at n = 24 125 orbits are 194 cycles. The text calls a found path 'an exact certificate', but the files store only its length. I could therefore not check stored paths; instead an own search found a one-flip path for all 3400 sampled initial states and each path was re-verified step by step (3400 of 3400).
* Proposed fix: Rename the column 'distinct rotation orbits of cycles' and store the paths (state, cell, next cycle).

### F17. 'Checked against v0.2 and an independent verifier' does not apply to n = 21, 22

* Location: lines 504-505
* Severity: overstated tag or wording (minor)
* Evidence: verified by reading; `out/misc_checks.json` (169 pairs), `out/compare_derived.json` (verifier coverage)
* What is wrong: The v0.2 sweep covers n <= 20 (169 pairs) and the verifier n <= 10. The records at n = 21, 22 had no second computation inside the study. They are now confirmed by the sealed sample.
* Proposed fix: Write 'n = 8..20 checked against v0.2; n <= 10 against the verifier'.

### F18. Query: the Summary states the mechanisms without their range

* Location: lines 18-21 ('In the switching classes that cycle is a spatially periodic crystal ... or the zero state ...')
* Severity: query (wording)
* Evidence: verified by reading
* What is wrong: The sentence reads as a general statement; it is computed for n <= 22 and covers 10 of the 13 classes. For class 35 the crystal (100)^{n/3} is not 'selected alone' (almost all cycles are selected); the parenthesis 'within its code-carrying family' hedges this. The following sentences do say what is proved, so I list it as a query.
* Proposed fix: Insert 'for n <= 22' and name classes 37, 45, 73 as not covered.

### F19. Query: `run_mech.py` documents an option that does not exist

* Location: `code/ring_size/run_mech.py` line 11 ('[--max-rss-gb 4]')
* Severity: bookkeeping (minor)
* Evidence: `out/cost_claim.json` (run_mech_has_cap_or_timeout_option, run_mech_docstring_mentions_max_rss_gb)
* What is wrong: The parser has no such argument and no time or memory limit; relevant to F6 because no cap is enforced or defined in code.
* Proposed fix: Remove the option from the usage line or implement it.

## B. Checked and correct

1. **Sealed sample against `mechanisms.csv`** (verified by my computation; `compare_sample.py`, `out/compare_sample.json`, `out/compare_mismatches.csv`). 194 records in the study, 194 in the sample, 194 in common, none on one side only. 23 record fields compared (16 from the sealed sample: bijective, crystal_orbit, crystal_p, cycle_orbits, cycles, g1_closed, g1_sccs, gamma_min, k_c, kstar, n_selected, selected_cover, selected_eq_closed_union, selected_orbits, selected_spatial_periods, selected_temporal_periods; 7 from the supplement: entry_cost_max, g2_holds, gamma_formula_ok, radius_other_max, radius_other_min, radius_selected_max, radius_selected_min). Mismatches: gamma_min 14, all in the bijective records (F14). Where the study has no value (bijective records) the field was not counted.
2. **Orbit table `cycle_orbits.csv.gz`** (verified by my computation; same files). 60355 orbit rows in 180 cases, every own orbit listed exactly once. Equal in all rows: orbit size, temporal period, spatial period, codes, radius (supplement) and the selected flag (sealed lists). Potentials: equal in all 23833 rows where the supplement has them, and the histogram of potentials equals the sealed one in all 180 cases. `mech.jsonl` holds the same 194 records and 60355 orbit rows as the csv tables.
3. **Derived tables** (verified by my computation; `compare_derived.py`, `out/compare_derived.json`): `zero_mechanism.csv` 89 rows, `code_carriers.csv` 165 rows, `rule35_blocks.csv` 13596 rows, `g1_distance_154.csv` 4112 rows; 0 mismatches. The block law of 5.2 holds for n = 8..22 with every state of every family cycle checked. For rule 154 at n = 8 and 16: 31 and 4081 cycles, maximum G1 distance to 0 4 and 8, Spearman 0.94 and 0.96.
4. **Numbers in the report** (verified by my computation; `report_numbers.py`, `out/report_numbers.json`): 590 checks, 585 equal. The 5 unequal ones are findings F4, F5 (two checks), F10 and F15. Equal: the k* table (195 cells for n = 8..22 from the sealed sample, one of them the marker 'not computed' for class 154 at n = 22; 52 cells for n = 4..7 from the own sweep), '180 non-bijective records' and '175 with a single closed class', the tables of 5.1 and 5.2, the statements of 5.3, 5.4 and 5.5 other than F4 and F5, the numbers of the cost line as arithmetic on `mech_cost.csv` (but see F7), the atlas record count. The seed table (lines 304-309) equals the study's file (`out/report_numbers2.json`).
5. **Atlas** (verified by my computation; `atlas_check.py`, `out/atlas_check.json`): 1232 of 1327 records compared, all 88 classes (75 non-switching), n = 4..19; 19 fields; selected orbits compared pattern by pattern in 813 records with n <= 14. Only mismatch: gamma_min in 80 bijective records (F14).
6. **Proofs** (verified by reading, each also tested by computation; `proof_verdicts.py`, `out/proof_verdicts.json`): 16 statements correct, 1 with a gap (the tag at line 256, see F12). Correct: re-rooting, Lemma 1, Lemma 2, Theorem A including gamma_min = m - 1 and the k* consequence, Lemma B including gamma_min = m + q - 2, the internal logic of the Ellison paragraph, Lemma Z, Lemma H with tau = 3 for class 94, Lemma P, Proposition R154, Proposition R22 (every case of the induction), the remark on the spatial period, and the other [proved] tags. Line-by-line reasons are in the file.
7. **Counterexample search** (verified by my computation; `sweep88.py`, `out/sweep88.jsonl`, `out/sweep88_summary.json`): all 88 classes (representatives derived in `p2lib.class_reps`), n = 3..19, 1476 cases solved of 1496 (20 skipped for size, listed in the summary file). Counterexamples: 0 to the re-rooting inequality, Lemma 1, Lemma 2, Theorem A (union of closed classes: 1476 cases; unique closed class gives S = K and gamma_min = m - 1: 1412 cases) and Lemma B. Lemma B: a rotation orbit of radius >= 2 exists in 346 cases (363 orbits, all tested directly); the hypotheses hold in 327 cases (q = 1: 282, q = 2: 40, q = 3: 5) and the conclusion holds in all of them.
8. **Observation on Lemma B** (not an error). The weight-2 edges are needed only for the value gamma_min = m + q - 2. For S = A it suffices that every cycle outside A reaches A by weight-1 edges: then the closed classes of G1 are the singletons {A_i}, Theorem A puts S inside A and rotation symmetry gives S = A. In the sweep this weaker hypothesis holds in 327 cases, the same cases as the full hypothesis (cases where only the weaker one holds: 0).
9. **Observation on Theorem A** (not an error). 'S = union of all closed classes' is tagged [computed] for the 180 records and is not a theorem: in the sweep it fails in 1 case(s): [[164, 16, 2, 1]] (rule, n, closed classes, selected closed classes).
10. **Lemma Z and Lemma P against brute force** (verified by my computation; `lemmaZP.py`, `out/lemmaZP.json`): Lemma Z for the 128 rules with F(0) = 0, n = 3..15: 1664 cases, 0 counterexamples. Lemma P for all 256 rules, same n: 3328 cases; the number of pairs (x, y) with F x = F y equals the trace of the n-th power of the pair-graph matrix in every case; no rule certified by the even-period criterion fails to be bijective at an odd n; certified rules: 15, 45, 51, 75, 85, 89, 101, 154, 166, 170, 180, 204, 210, 240.
11. **Certificate (a), pair graphs** (verified by my computation; `out/pairgraph_all256.csv`): rules 154 and 45 have off-diagonal component periods 2;2 and 2;2; all 13 rows of `injectivity.csv` agree.
12. **Certificate (b), healing and crystal radius** (verified by my computation; `crystal_checks.py`, `out/crystal_checks.json`, `out/lightcone_own.csv`, `out/crystal_radius_own.csv`): all 7 rows of `lightcone.csv` reproduced (class 94 heals after 2, 3, 3 steps, tau = 3; the other 6 words do not heal within 200 steps). Crystal radius: 333 rows, radius >= 2 for class 94 at every 3 | n from 6 to 399 and for classes 43 and 142 at every 4 | n up to 400; the only difference from `crystal_radius.csv` is the return-time entry at n = 3 of class 94, where the radius is below 2 in both files.
13. **Certificate (c), seed orbits** (verified by my computation; `seed_orbits.py`, `seed_orbits_pass3.py`, `seed_compare.py`, `out/seed_compare.json`): on all rows the study determined, returns, transient and limit period agree (rule 22: 222 of 222; 26: 220 of 220; 122: 220 of 220; 154: 220 of 220). For rules 26 and 154 all 33 undetermined n are even and are settled: 12 by own simulation, the rest by Proposition R154; the return sets are the powers of two. Rule 22 and rule 122: see F1, F2.
14. **Certificate (d), orbit identities of R154 and R22** (verified by my computation; `rule90_identities.py`, `out/rule90_identities.json`): for all 127 even n <= 256 the orbits of e_0 under rules 90, 154, 26 coincide step by step, stay on the sites of parity t and equal X^(-t)(1+X)^(2t) (130175 steps checked); they die exactly at the powers of two, at t = n/2. For all 64 n <= 256 with 4 | n the rule-22 orbit equals R_t at even t and R_t united with R_(t-1) at odd t, R_s has no two ones at distance 2 for even s and equals the dilated half-ring orbit (65600 steps checked). The algebraic criterion (X^n - 1 divides a power of 1 + X iff n is a power of two) was checked for n = 2..256.
15. **Certificate (e), table 5.6** (verified by my computation; `sampled_reach_check.py`, `out/sampled_reach_check.json`): all 17 rows of the table reproduced from the study's files; the radius flags re-derived with own code agree in all 17 files; periods of all 3400 sampled limit cycles agree. See F16 for the paths.
16. **Certificate (f), factor search** (verified by my computation; `misc_checks.py`, `out/misc_checks.json`): the 8 counts of `factor_search.csv` reproduced; target rules found: [154, 166]; no additive target.
17. **Tags** (`tags_audit.py`, `out/tags_audit.csv`): 45 tags (17 [proved], 23 [computed], 5 [observed], including the three definitions); 36 match the evidence; 3 overstated and 3 with a wrong statement (lines 256, 299, 332, 349, 376, 378; findings F1, F2, F4, F5, F12, F15). The [proved] tags are at lines 91, 110, 113, 125, 137, 155, 159, 168, 175, 176, 247, 256, 257, 311, 320, 374; each is judged in `out/proof_verdicts.json`.
18. **Patterns classified 'explained, not proved' or 'resists'** (verified by reading): in the mechanism table of Section 5 and in sections 5 to 8 they carry their status; exceptions are F3 (PR draft, class 22), F12 and F18. The commit messages state no result.
19. **Report generation** (verified by reading `make_report.py` and the template; `out/report_numbers2.json`): the report is the template with 41 placeholders filled; 287 static template lines, all verbatim in the report. The two text inputs `literature_section.md` and `ellison_remark.md` are tracked. The manifest lists 48 files, all hashes correct (`out/misc_checks.json`).
20. **Predictions** (`predictions_recount.py`, `out/predictions_recount.json`, `out/predictions_recount.csv`): the sealed file is unchanged since commit 8d68e54. On the study's 50 rows I reach the same outcome in all but two (F8 and class 154 at n = 22, now computed). Outcomes decided from own data and from the study's files agree in 91 of 92 parts (the exception is class 154 at n = 22, which the study's files cannot decide). Sealing before computation (`seal_timing.py`, `out/seal_timing.json`): the seal commit is from 2026-11-13 23:19:23; none of the 76 files and folders under `data/ring_size`, `code/ring_size`, `figures/ring_size` was created or modified before it (earliest: code/ring_size at 2026-11-13 23:21:22). This does not exclude computations that left no file.
21. **Class 154 at n = 22** (verified by my computation; `v154_n22.py`, `out/v154_n22.json`): 76600 cycles in 38328 rotation orbits (4192256 of 4194304 states are periodic; the map is not bijective). G1 has 4756911 edges, one strongly connected component, hence one closed class containing all cycles; no cycle is without an out-edge. V rows were computed for all 38328 orbit representatives (never stored): no row check failed (0 failures), off-diagonal minimum 1, maximum 12, the entries V = 1 number 4756911 and coincide with the G1 edge set. Edmonds' algorithm ends after the first level (one strongly connected component of minimum-weight arcs): gamma = 76599 = m - 1 for every cycle, all 76600 cycles selected, codes 01234567, k_c = 0 for all c, **k* = 0**. This agrees with the sealed prediction (k* = 0) and with Theorem A (unique closed class K, S = K, gamma_min = m - 1). Cost: 48 CPU-minutes, peak memory 2266 MB.
22. **Proposition R154, remark** (verified by my computation for odd n = 3..21, `out/proof_verdicts.json`, and by the seed orbits for all odd n <= 256): for rule 26 at odd n the only preimages of 0 are 0 and 1^n, and 1^n has no preimage, so the zero state has radius 1; with bijectivity of rule 154 at odd n, 'r(0) >= 2 iff n is a power of two' holds for both rules at every n in the computed range and, by these two arguments, for every n >= 3.

## C. Not checked, and why

1. `literature_ring_size.md` and Section 2 of the report: a separate track.
2. The figures in `figures/ring_size/` and `figures_ring_size.py`: not opened; no number in this file depends on them.
3. The study's code was not executed (`reproduce_ring_size.sh`, `test_ring_size.py`, `verify_mech.py`): the task forbids runs that write into existing files. `make_report.py`, `check_predictions.py`, `run_mech.py` and `sample_reach.py` were read; `mech.py`, `ringlang.py`, `lightcone.py`, `run_local.py`, `analyze_mechanisms.py`, `factor_search.py` and `code/fw/` were not read beyond a few lines.
4. The contents of the two verifier files beyond coverage (their `ind_*` columns): not compared; the same (rule, n) pairs with n = 4..10 are covered by the own sweep.
5. v0.2 statements used by the report (Proposition 1 on rules 60 and 90, 'a bijective map has k* = 0'): v0.2 is not under review; the bijective case is confirmed in the 14 bijective sample cases and proved in `../SAMPLE.md`.
6. Structural descriptions in 5.5: 'carriers are (100)-crystals with 111-defects' (class 26), 'carriers built on the period-6 pattern 100000' (class 37), and 'half of the single flips start a domain of another phase' (classes 43, 142, line 249): not checked. For 43 the maximal return time grows linearly with n (`out/crystal_checks.json`), which is consistent with the last one.
7. Atlas: 95 records not compared (all n = 20 records and the cases skipped by the sweep); the atlas log's comparison with v0.2 was not repeated.
8. Sweep: 20 (rule, n) cases skipped for size (rules 5, 29, 51, 76, 108, 170, 200, 204 at n >= 15; list in `out/sweep88_summary.json`); n >= 20 not searched.
9. Seed orbits still undetermined after 6e9 steps: rule 22 at n = 242, 243; rule 122 at n = 133, 141, 157, 165, 189, 201, 205, 213, 221, 229, 241, 243, 249 (their limit periods are expected to exceed the budget).
10. Whether Ellison's theorem is quoted correctly (only the internal logic of the paragraph was checked).
11. The dense all-roots Edmonds computation for rule 154 at n = 22 (5.9 GB): not run. The level-wise variant used instead equals the dense one in all 1399 sweep cases where both were run, and at n = 22 it ends at the first level, where it needs only the minimum of each row of V.
12. Per-orbit potentials of the 17 sample cases whose sealed solve took more than 30 CPU-seconds: compared by histogram only.

## Appendix 1. Summary of the report, sentence by sentence (verified by reading)

| lines | sentence (shortened) | verdict |
|---|---|---|
| 15-16 | selected cycles are a union of closed classes of G1 (Theorem A, proved for all n) | correct |
| 16-18 | a cycle that cannot be left with one flip is selected alone once every other cycle reaches it by one-flip steps (Lemma B) | correct (for a rotation orbit, 'alone' means the orbit) |
| 18-21 | in the switching classes that cycle is a crystal (94, 43, 142, 35 within its family) or the zero state (154, 26, 22, 60, 90, 122) | query F18: range n <= 22 not stated; 37, 45, 73 not covered |
| 21 | inherited from rule 90's nilpotency at n = 2^k for 154 and 26, proved | correct (Proposition R154) |
| 21-23 | proved for all n: general statements; k* = 0 for 154 and 45 at odd n; radius for class 94 for all 3 / n; zero state of 154, 26 for even n and of 22 for 4 / n | F11: n = 3 must be excluded for class 94; the rest correct |
| 24-25 | not proved: reachability; 'this single statement' computed for n <= 22 and sampled up to 32 | F12: not the only gap |
| 26 | class 122 at even n, class 26 away from powers of two, single switches of 45 and 73 resist | consistent with 7(c) |

## Appendix 2. Recount of the sealed predictions (`out/predictions_recount.csv` has all 92 parts)

| count | study's table (50 rows) | own outcome on the same rows | all 92 own parts |
|---|---|---|---|
| holds | 41 | 41 | 71 |
| fails | 5 | 6 | 14 |
| not tested | 2 | 1 | 4 |
| holds (trivially) | 1 | 1 | 1 |
| holds (observed, sampled) | 1 | 1 | 1 |
| not a testable statement | 0 | 0 | 1 |

Rows judged differently from the study: '26, other n with k* >= 1: missing code 7': study holds, own fails; 'class 154, n = 22: k* = 0': study not tested, own holds.

## Appendix 3. Files of this part

Scripts: `p2lib.py`, `p2core.c`, `lean_edmonds.py`, `extras.py`, `compare_sample.py`, `compare_derived.py`, `report_numbers.py`, `report_numbers2.py`, `atlas_check.py`, `sweep88.py`, `sweep_summary.py`, `lemmaZP.py`, `proof_verdicts.py`, `orbitlib.py`, `p2orbit.c`, `seed_orbits.py`, `seed_orbits_pass3.py`, `seed_compare.py`, `crystal_checks.py`, `rule90_identities.py`, `p2reach.c`, `sampled_reach_check.py`, `misc_checks.py`, `details_45_73.py`, `tags_audit.py`, `predictions_recount.py`, `seal_timing.py`, `cost_claim.py`, `v154_n22.py`, `g1_timing.py`, `make_findings.py`. Outputs: `out/`. Logs: `logs/`, `../logs/BATCHES_phase2.md`.
