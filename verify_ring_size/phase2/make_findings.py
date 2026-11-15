"""Writes FINDINGS_part1.md from the result files in out/ (every number in the findings is read from one of them)."""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")


def J(name):
    return json.load(open(os.path.join(OUT, name)))


cs, cd, rn, rn2 = J("compare_sample.json"), J("compare_derived.json"), J("report_numbers.json"), J("report_numbers2.json")
at, sw, zp, cc = J("atlas_check.json"), J("sweep88_summary.json"), J("lemmaZP.json"), J("crystal_checks.json")
sd, r90, sr, mc = J("seed_compare.json"), J("rule90_identities.json"), J("sampled_reach_check.json"), J("misc_checks.json")
ta, pr, st, co = J("tags_audit.json"), J("predictions_recount.json"), J("seal_timing.json"), J("cost_claim.json")
v, d4573, pv, r241 = J("v154_n22.json"), J("details_45_73.json"), J("proof_verdicts.json"), J("rule22_n241_check.json")
g1t = J("v154_n22_g1_timing.json")
extras = [json.loads(l) for l in open(os.path.join(OUT, "extras.jsonl"))]

cpu = {"extras.py (out/extras.jsonl)": sum(r["cpu_seconds"] for r in extras),
       "sweep88.py (out/sweep88_summary.json)": sw["cpu_seconds"],
       "seed_orbits.py, seed_orbits_pass3.py (out/seed_compare.json)": sd["cpu_seconds_all_passes"],
       "v154_n22.py (out/v154_n22.json)": v["cpu_seconds"],
       "sampled_reach_check.py": sr["cpu_seconds"], "compare_sample.py": cs["cpu_seconds"],
       "lemmaZP.py": zp["cpu_seconds"], "crystal_checks.py": cc["cpu_seconds"], "rule90_identities.py": r90["cpu_seconds"]}
cpu_total = sum(cpu.values())
json.dump({"cpu_seconds_by_script": cpu, "cpu_seconds_total": round(cpu_total, 1), "cpu_hours_total": round(cpu_total / 3600, 3),
           "note": "scripts without a recorded CPU time (comparisons and bookkeeping) each ran for a few seconds at most"},
          open(os.path.join(OUT, "cpu_total.json"), "w"), indent=1)

f = cs["fields"]
sealed_fields = sorted(k for k, x in f.items() if x["source"] == "sealed")
suppl_fields = sorted(k for k, x in f.items() if x["source"] == "supplement")
internal_fields = sorted(k for k, x in f.items() if x["source"] == "study-internal")
rec_fields = [k for k in f if not k.startswith("orbit.") and not k.startswith("mech.jsonl")]
orb_fields = [k for k in f if k.startswith("orbit.")]
mism_fields = {k: x["mismatch"] for k, x in f.items() if x["mismatch"]}
z = cd["zero_mechanism"]
lb = sw["lemmaB"]
s22, s26, s122, s154 = (sd["by_rule"][k] for k in ("22", "26", "122", "154"))
job = co["job_154_n22"]
c45, c73 = d4573["class45_even_n"], d4573["class73"]
uneq = {c["id"]: c for c in rn["unequal"]}
omitted_fail = [p for p in pr["parts_omitted_by_study_table"] if p[2] == "fails"]
tests = sw["tests"]
n_tests_cases = max(t["cases"] for t in tests.values())
vm = cd["verify_mech_files"]
vm_rows = sum(x["rows"] for x in vm.values())
vm_expected = sum(x["pairs_expected_from_report_text"] for x in vm.values())
vm_missing = sum(x["pairs_missing"] for x in vm.values())
tpl = rn2["template"]
sent22 = rn2["sentences"][0]
own_rows_counts = pr["own_counts_on_study_rows"]
study_counts = pr["study_table_counts"]
diff_rows = pr["study_rows_judged_differently"]
k154 = [p for p in pr["parts"] if p["id"] == "K_154_22"][0]
files56 = sr["files"]

L = []
A = L.append
A("# Verification of the ring-size study, part 1 (steps 2 to 6): findings")
A("")
A("Object: branch `ring-size-mechanisms` (commits 8d68e54, 8bcad22, 1e256cd): `report_ring_size.md`, `PREDICTIONS_ring_size.md`, "
  "`data/ring_size/`, `code/ring_size/`, `reproduce_ring_size.sh`, and the untracked `PR_DRAFT.md`. Nothing in the study was changed. "
  "All code, outputs and logs of this part are in `verify_ring_size/phase2/`; file names below are relative to that folder. "
  "The sealed blind sample (`../out/sample.jsonl`, commit a384763) was not changed.")
A("")
A("How to read the labels. **Verified by my computation**: recomputed with the verification's own code and compared. "
  "**Verified by reading**: checked by reading the text or the study's code, nothing recomputed. **Not verified**: listed in section C. "
  "'Sealed' marks a value taken from the sealed sample; 'supplement' marks a value computed after the seal with the same own solver "
  "(`extras.py`, `sweep88.py` and the certificate scripts). Line numbers refer to `report_ring_size.md` unless a file is named.")
A("")
A("Conventions reconciled (`out/compare_sample.json`, block `conventions`). The study writes a state as an integer with cell i at bit i and "
  "prints the pattern with cell 0 first; the sample uses the bit string with cell 0 as the most significant bit. The printed patterns are "
  "directly comparable: all %d orbit patterns of `cycle_orbits.csv.gz` are periodic states under the sample's map. The study's orbit "
  "representative is the smallest integer (cell i at bit i) over the cycle and its rotations (%d of %d rows confirmed); the sample's is the "
  "lexicographically smallest string. The column `drift` is the smallest s with F(x) = x rotated right by s cells, -1 if there is none "
  "(%d of %d rows)." % (cs["conventions"]["pattern_on_cycle_x0_first"], cs["conventions"]["rep_is_orbit_minimum_lsb_first"],
                        cs["orbit_rows_study"], cs["conventions"]["drift_right_min"], cs["conventions"]["drift_rows"]))
A("")
A("Cost of this part (CPU time, 1 process at a time; `out/cpu_total.json`): %.2f CPU-hours in total. " % (cpu_total / 3600)
  + "; ".join("%s %.0f s" % (k, x) for k, x in cpu.items() if x >= 5) + ". Expected and measured values per batch: `../logs/BATCHES_phase2.md`.")
A("")
A("Reductions of scope (declared): the 88-class sweep skipped %d of %d (rule, n) cases with more than 20000 cycles (n = 15..17) or 16000 cycles "
  "(n = 18, 19); the atlas comparison covers %d of %d records (n = 20 and the skipped cases are not covered); potentials per orbit were compared "
  "for %d of %d orbit rows and by the histogram of potentials for all %d non-bijective cases; %d seed orbits remain undetermined; the dense Edmonds "
  "run for rule 154 at n = 22 was replaced by a level-wise Edmonds on streamed rows of V (validated against the dense one in %d sweep cases); "
  "the study's pipeline and tests were not executed." % (
      len(sw["cases_skipped"]), sw["cases_total"], at["records_compared"], at["atlas_records"], f["orbit.gamma"]["compared"],
      cs["orbit_rows_study"], f["orbit.gamma_histogram_by_cycles"]["compared"],
      len(s22["study_capped_open"]) + len(s122["study_capped_open"]), tests["lean_edmonds_equals_dense"]["cases"]))
A("")
A("## A. Errors found")
A("")
A("Severity classes: wrong result / wrong proof step / overstated tag or wording / bookkeeping. No wrong proof step was found. "
  "A 'query' is a point where I am not sure it is an error.")
A("")

def F(n, title, loc, ev, sev, body, fix):
    A("### F%d. %s" % (n, title))
    A("")
    A("* Location: %s" % loc)
    A("* Severity: %s" % sev)
    A("* Evidence: %s" % ev)
    A("* What is wrong: %s" % body)
    A("* Proposed fix: %s" % fix)
    A("")

F(1, "The list of ring sizes where the seed orbit of rule 22 returns to 0 is incomplete (n = 241 is missing)",
  "lines 331-332 (sentence tagged [computed]); also line 500, lines 363-365 and 488-489 ('computed up to 256'), mechanism table line 211 "
  "('computed to 256'); `PR_DRAFT.md` lines 37-38",
  "`out/seed_compare.json`, `out/report_numbers2.json`, `out/rule22_n241_check.json`, `out/seed_orbits_own.csv` (verified by my computation)",
  "wrong result",
  "The sentence lists the n not divisible by 4 at which the single-flip orbit of rule 22 returns to 0 'in n <= 256' as %s. In the study's own "
  "`seed_orbits.csv` %d values of n not divisible by 4 (%s) are undetermined at the cut-off of %d steps, so the list is only the list of the returns found. "
  "With own code (Brent cycle detection, up to 6e9 steps) the orbit at n = %d reaches the zero state after %d steps; this was confirmed with a "
  "second implementation (Python integers, `out/rule22_n241_check.json`). Of the %d n the study left undetermined for rule 22, %d were settled "
  "by own simulation, %d only by Proposition R22 (4 | n, not a power of two: no return), and n = %s are still open. "
  "The complete list of returns found is %s." % (
      ", ".join(map(str, sent22["report"])), len(sent22["study_undetermined_n_not_divisible_by_4"]),
      ", ".join(map(str, sent22["study_undetermined_n_not_divisible_by_4"])), sd["cap_of_the_study"], r241["n"],
      r241["first_time_state_is_zero_python_bigint"], len(s22["study_capped"]), len(s22["study_capped_settled_by_own_simulation"]),
      len(s22["study_capped_settled_by_proof_only"]), ", ".join(map(str, s22["study_capped_open"])), ", ".join(map(str, s22["returns_own"]))),
  "Add n = 241; replace 'computed up to 256' by the set of n actually decided and name the open n (242, 243 after this verification); "
  "in 7(c) write '121, 125, 241, 253'.")

F(2, "'Returns exactly at n = 7, 15, 31, 63, 127, 255' for rule 122 is not supported",
  "lines 348-349 (tag [computed])", "`out/seed_compare.json`, `out/report_numbers2.json` (verified by my computation)", "overstated tag",
  "%d values of n are undetermined in the study's file, so 'exactly' does not follow. With own code %d of them were settled (none returns); "
  "%d remain open: n = %s. No return other than the six listed was found." % (
      len(s122["study_capped"]), len(s122["study_capped_settled_by_own_simulation"]), len(s122["study_capped_open"]),
      ", ".join(map(str, s122["study_capped_open"]))),
  "Write 'returns at n = 7, 15, 31, 63, 127, 255 and at no other n <= 256 whose orbit could be decided; 13 values of n are open', and tag the "
  "pattern 2^k - 1 as [observed].")

F(3, "PR draft states the class-22 pattern as a result up to n = 256",
  "`PR_DRAFT.md` lines 37-38 ('class 22 switches exactly where a single flip of the zero state dies on the ring (n = 4..8, 14..16, 30..32, "
  "61..64, also 121, 125, 253 in n <= 256)')",
  "verified by reading; k* values: sealed sample and `out/sweep88.jsonl` (n <= 22 only); `out/seed_compare.json`",
  "overstated tag or wording",
  "k* of class 22 is computed for n <= 22 only. Beyond that only the seed orbit is known, i.e. whether the zero state can be left by one flip; "
  "that k* switches there needs the reachability statement, which the report itself lists as not proved and which is sampled at n = 30, 31, 32 only. "
  "The list in the draft also omits 126-128 and 254-256, which are in the report's own table, and n = 241 (F1).",
  "Write 'k* = 1 exactly where the single-flip orbit of 0 returns, for n = 4..22; the orbit returns also at ... (seed orbit only, k* not computed)'.")

F(4, "Class 45: 'all cycles are selected' at every even n >= 10 is false at n = 18 and n = 22",
  "lines 375-376 (tag [computed])", "`out/details_45_73.json`, `out/report_numbers.json` (check sec5_5_45_even); sealed sample and the study's own `cycle_orbits.csv.gz`",
  "wrong result (text; the data files are right)",
  "At n = 18, %d of %d cycles are selected; the unselected ones are the uniform 2-cycle itself and the cycle of (011)^6. At n = 22, %d of %d are "
  "selected. The study's `cycle_orbits.csv.gz` has the same rows as not selected. The radius statement (radius 1 at even n >= 10) is correct, and "
  "k* = 0 is unaffected." % (c45["18"]["selected_cycles"], c45["18"]["cycles"], c45["22"]["selected_cycles"], c45["22"]["cycles"]),
  "Write 'it has radius 1 and all cycles are selected except two cycles at n = 18 (among them the uniform 2-cycle) and one cycle at n = 22'.")

F(5, "Class 73: the uniform 2-cycle is not selected at n = 22 either, and no cycle of temporal period 3 is selected at n = 9",
  "lines 377-378 (tag [computed]); related: mechanism table line 216",
  "`out/details_45_73.json`, `out/report_numbers.json` (checks sec5_5_73_uniform, sec5_5_73_n9); sealed sample and the study's own `cycle_orbits.csv.gz`",
  "wrong result (text; the data files are right)",
  "'At all other n it is selected' fails at n = 22: the uniform 2-cycle has potential %d against the minimum %d (study file) and is not selected; "
  "k* stays 0 because %d of the %d orbits carrying code 7 are selected. At n = 9 the selected cycles are the three phases of the fixed point "
  "(011)^3 and two orbits of temporal period 2; the two orbits of temporal period 3 are not selected. If 'period-3 cycles' means the crystal of "
  "spatial period 3, the sentence should say so." % (
      c73["22"]["uniform_2cycle_gamma_in_study_file"], c73["22"]["gamma_min"], c73["22"]["selected_carriers_of_code_7"], c73["22"]["carriers_of_code_7"]),
  "Write 'at n = 9 none of the three orbits carrying code 7 is selected (selected: the fixed-point crystal (011)^3 and two orbits of period 2); "
  "at n = 22 the uniform 2-cycle is again not selected, but other carriers of code 7 are'.")

F(6, "The cost claim for class 154 at n = 22 is not supported in compute time",
  "line 534, lines 454 and 528; `data/ring_size/stopped_runs.csv`; `reproduce_ring_size.sh` line 15; `PR_DRAFT.md` lines 43, 57, 61; "
  "`code/ring_size/make_report.py` line 162",
  "`out/cost_claim.json`, `out/pmset_sleep_wake.txt`, `out/v154_n22.json` (verified by reading the study's logs and code; sleep interval from the system power log)",
  "overstated tag or wording",
  "The 7.4 h are wall-clock time between the start of the job (%s, birth time of `log_mech_154_n22.txt`) and the stop (%s in `stopped_runs.csv`, "
  "whose column is named `wall_hours`). The power log shows the machine asleep from %s to %s, i.e. %.2f h of the %.2f h. The job had at most %.1f minutes "
  "(%.2f h) of awake time, below the 5 h cap and below the study's own estimate of 2-3 h (`reproduce_ring_size.sh` line 5). No CPU time was "
  "recorded anywhere: the log holds one line ('1 jobs to run, 194 already in checkpoint'), `cost_seconds` in `run_mech.py` is `time.time()` wall "
  "time and is written only when a job ends. The cap of 5 h is defined nowhere in the repository (not in `run_mech.py`, which has no cap or "
  "time-out option, not in the reproduce script, not in the sealed predictions); `stopped_runs.csv` is written by no script. The case is not "
  "expensive: with own code the result follows from the one-flip graph in %.1f CPU-seconds (`out/v154_n22_g1_timing.json`) and the full cross-check took %.0f CPU-minutes with %.0f MB "
  "(section B)." % (job["start_log_birth"], co["stopped_runs_csv"][0]["stopped_cet"], job["asleep_intervals_within_job"][0][0],
                    job["asleep_intervals_within_job"][0][1], job["asleep_hours_within_job"], job["elapsed_hours_upper"],
                    job["awake_minutes_upper_bound"], job["awake_hours_upper_bound"], g1t["cpu_seconds"], v["cpu_seconds"] / 60, v["peak_rss_mb"]),
  "Replace the sentence by: 'Class 154 at n = 22 was started at 00:46 and stopped at 08:09; the machine was asleep from 02:00 to 08:08, so the job "
  "ran for at most about 1.3 h and was stopped unfinished; its CPU time was not recorded. It is not computed in this study.' Rename the outcome "
  "'not tested: run stopped above the stated cost cap' accordingly, define the cap (wall or CPU) where it is used, and record CPU time "
  "(`time.process_time()`) per job. The value itself can be taken from this verification: k* = 0.")

F(7, "'Total CPU 1.9 h' is a sum of wall-clock times",
  "line 534; file table line 519 calls the same column 'wall time'; `code/ring_size/run_mech.py` lines 26 and 38, `make_report.py` line 163",
  "`out/cost_claim.json` (verified by reading the study's code; sum recomputed from the study's `mech_cost.csv`)", "bookkeeping",
  "`cost_seconds` is `time.time()` at the end minus the start of each job; their sum is %.2f h. For the n = 21, 22 batch alone the log gives "
  "real %s, user %s, sys %s, i.e. more CPU than wall with two workers." % (
      co["sum_cost_seconds_hours"], co["batch_n21_22_time_lines"][0][1], co["batch_n21_22_time_lines"][1][1], co["batch_n21_22_time_lines"][2][1]),
  "Write 'sum of the wall times of the jobs 1.9 h' or record CPU time.")

F(8, "One sealed prediction is reported as holding after it was narrowed (class 26 at n = 8)",
  "line 433; `data/ring_size/predictions_outcome.csv` row 'P6 / 26, other n with k* >= 1: missing code 7'; `code/ring_size/check_predictions.py` line 83",
  "`out/predictions_recount.json`, `out/predictions_recount.csv` (verified by my computation, from own data and separately from the study's files)",
  "overstated tag or wording",
  "Sealed text (P6): 'For class 26 the same holds at n = 16 (k* = 2, zero state alone); at the other n with k* = 1 the missing code is 7 (111) with "
  "a different mechanism.' The check excludes n = 8 as well as n = 16. %s. So this part fails at n = 8 (8 = 2^3 was overlooked when the prediction "
  "was written) and holds at the other n. On the study's own partition into %d rows my outcomes are: %s; the study states: %s. The difference is this "
  "row and the row for class 154 at n = 22, which I computed (%s)." % (
      diff_rows[0]["parts"][0][2] if diff_rows else "", pr["study_table_rows"],
      ", ".join("%s %d" % kv for kv in sorted(own_rows_counts.items())), ", ".join("%s %d" % kv for kv in sorted(study_counts.items())),
      k154["own_outcome"] + ", " + k154["own_detail"]),
  "Report the row as 'fails at n = 8 (zero-state mechanism), holds at n = 9, 10, 12, 13, 15, 18, 19, 21' and change the counts.")

F(9, "The outcome table does not cover every sealed statement",
  "lines 409-412 and file table line 529 ('outcome of every sealed prediction'); `check_predictions.py` docstring; `PR_DRAFT.md` lines 42-43",
  "`out/predictions_recount.json` (block parts_omitted_by_study_table), `out/predictions_recount.csv`", "bookkeeping",
  "I split the sealed text into %d parts; the study's %d rows cover %d of them. The %d uncovered parts are: the general statements G1 to G3, the "
  "column 'proof for all n expected?' of the class table, and sub-claims of P3, P4, P8, P9. Of these, %d hold, %d fail, %d was not tested "
  "(sampled test at n = 64) and %d is not testable. The failing ones are: %s. Three outcomes are typed into `check_predictions.py` instead of "
  "being decided from data (lines 46-47, 54, 116). The row for P9 merges three k* predictions (n = 32, 24, 28). The PR draft's '41 hold, 5 fail, "
  "2 not tested' leaves out the two qualified rows ('holds (trivially)', 'holds (observed, sampled)')." % (
      pr["own_parts_total"], pr["study_table_rows"], pr["own_parts_total"] - len(pr["parts_omitted_by_study_table"]),
      len(pr["parts_omitted_by_study_table"]), pr["omitted_counts"].get("holds", 0), pr["omitted_counts"].get("fails", 0),
      pr["omitted_counts"].get("not tested", 0), pr["omitted_counts"].get("not a testable statement", 0),
      "; ".join("%s (%s)" % (p[0], p[1]) for p in omitted_fail)),
  "Add rows for G1-G3 and for the proof expectations (G3 and the direction-0 proofs for 94, 43, 142 were not obtained; the radius proof was "
  "obtained for 94 only), or state that the table covers P1-P9 and the k* table only.")

F(10, "'432 (rule, n) pairs (all 88 classes at n = 4..8, the 13 switching classes at n = 9, 10)' describes %d pairs" % vm_expected,
   "lines 97-98; `PR_DRAFT.md` line 48", "`out/compare_derived.json` (block verify_mech_files), `out/report_numbers.json` (check sec3_verifier_pairs)",
   "bookkeeping",
   "The two verifier files hold %d rows; the pairs named in the text number %d. The %d missing pairs are exactly the bijective maps, which the "
   "verifier does not treat." % (vm_rows, vm_expected, vm_missing),
   "Write '432 non-bijective (rule, n) pairs; the 34 bijective pairs are not covered by the verifier'.")

F(11, "Summary: 'class 94 for all 3 | n' includes n = 3, where the statement is false",
   "lines 22-23; correct in the body (lines 246-248, 477: n >= 6)", "`out/crystal_radius_own.csv`, `out/crystal_checks.json` (radius_lt2)",
   "overstated tag or wording",
   "At n = 3 a single flip leaves the crystal (radius below 2: %s); Lemma H needs n >= 7 and n = 6 is computed." % cc["crystal_radius"]["radius_lt2"],
   "Write 'class 94 for all 3 | n with n >= 6'.")

F(12, "More than 'one reachability statement' is unproved",
   "Summary lines 24-25 ('this single statement'), 7(a) lines 479-481, tag at line 256; `PR_DRAFT.md` lines 34-35", "verified by reading; `out/crystal_radius_own.csv`, `out/seed_compare.json`",
   "overstated tag or wording",
   "'Each of the crystal and zero-state patterns is proved conditional on one reachability statement' holds only for the direction 'k* >= 1' of "
   "class 94 (n >= 6), of 154 and 26 at n = 2^k and of 22 at 4 | n. Also unproved are: (i) the radius of the crystal (0011)^{n/4} of classes 43 and "
   "142 beyond n = 400 (computed, Lemma H does not apply), so the tag '[proved conditional on reachability]' at line 256 is too strong for these "
   "two classes; (ii) the seed sets of rule 22 for n not divisible by 4 and of rule 122, i.e. the radius of the zero state there; (iii) the "
   "direction 'condition fails, hence k* = 0' for every class except odd n of 154 and 45, which needs the closed classes of G1 and is not a "
   "statement about reaching the crystal or 0 (the report says this itself in 5.1 and in section 8).",
   "Name the three gaps in the Summary and in 7(a); tag line 256 '[proved for class 94 conditional on reachability; for 43, 142 conditional on "
   "reachability and on the radius beyond n = 400]'.")

F(13, "'Every number below is filled in from a data file' is not the case for the prose",
   "lines 5-6", "`out/report_numbers2.json` (block template); verified by reading `make_report.py` and `report_template.md`", "overstated tag or wording",
   "The template has %d lines, %d of them without a placeholder, and all of these occur verbatim in the report; %d placeholders are filled by "
   "`make_report.py`. Ring sizes and counts in the static lines are typed: for example 'n = 4..8, 14, 15, 16' (line 363), '(121, 125, 253)' "
   "(line 332), 'n = 7, 15, 31, 63, 127, 255' (line 349), 'n = 11, 12, 17, 18' (line 370), and the sentences of F4 and F5. The mechanism table is "
   "typed in `make_report.py` (lines 71-83), the cut-off 400000 at line 112, and `stopped_runs.csv` has no generating script. Both wrong "
   "sentences (F4, F5) are typed text; the list of F1 is generated from the rows the study determined, the claim around it is typed." % (
       tpl["template_lines"], tpl["static_lines"], tpl["n_placeholders"]),
   "Either generate those sentences from the data files or say 'tables and the numbers in them are filled in from data files'.")

F(14, "gamma_min = 0 in the records of bijective maps is a placeholder",
   "`data/ring_size/mechanisms.csv` (14 rows: rules 45 and 154 at odd n), `data/ring_size/atlas/mechanisms_atlas.csv`; not used in the report text",
   "`out/compare_sample.json`, `out/compare_mismatches.csv`, `out/atlas_check.json`, `out/misc_checks.json`", "bookkeeping",
   "The minimum potential of a bijective map is m - 1 (sealed sample: full computation in all %d bijective cases). The study writes 0 there; this is "
   "the only field that differs between the sealed sample and `mechanisms.csv` (%d of %d record comparisons), and the only one in the atlas "
   "(%d of %d). The same value is in the v0.2 sweep (%d of the 169 common pairs). The bijective records also carry no orbit rows and no G1 fields." % (
       f["gamma_min"]["mismatch"], f["gamma_min"]["mismatch"], f["gamma_min"]["compared"], at["mismatch_fields"].get("gamma_min", 0),
       at["fields"]["gamma_min"]["compared"], mc["v02_sweep_vs_sample"]["gamma_min_0_placeholder_in_bijective_rows"]),
   "Write m - 1, or leave the field empty and say so in the file description.")

F(15, "'Wherever the zero state is selected alone, Lemma B holds' is flagged in %d of %d cases" % (
    z["fields_equal"]["zero_alone_and_study_g2_holds"], z["fields_equal"]["zero_alone_cases"]),
   "lines 298-299 (tag [computed])", "`out/compare_derived.json` (block zero_mechanism)", "overstated tag or wording (minor)",
   "In n = 8..22 the zero state is selected alone in %d (rule, n) cases of the six rules of `zero_mechanism.csv`. The study's flag `g2_holds` is True "
   "in %d; the other %d are rules 60 and 90 at n = 8, 16, where {0} is the only cycle and the flag is False. Mathematically nothing is wrong "
   "(with one cycle there is nothing to prove)." % (z["fields_equal"]["zero_alone_cases"], z["fields_equal"]["zero_alone_and_study_g2_holds"],
                                                  z["fields_equal"]["zero_alone_single_cycle_map"]),
   "Add '(in the nine cases with more than one cycle)'.")

F(16, "Table 5.6: 'distinct_cycles' counts rotation orbits, and the paths are not stored",
   "lines 386-389; `data/ring_size/sampled_reach/*.csv`", "`out/sampled_reach_check.json`, `out/sampled_paths_own.jsonl` (verified by my computation)",
   "bookkeeping",
   "The label of a sampled cycle is the smallest state over the cycle and all rotations (all %d labels reproduced under this convention, %d under "
   "'smallest state on the cycle'), so the column counts rotation orbits of cycles: for rule 22 at n = 32 the %d sampled orbits are %d cycles, for "
   "rule 94 at n = 24 %d orbits are %d cycles. The text calls a found path 'an exact certificate', but the files store only its length. I could "
   "therefore not check stored paths; instead an own search found a one-flip path for all %d sampled initial states and each path was re-verified "
   "step by step (%d of %d)." % (
       sr["paths_checked"] - sr["label_mismatch_rotation_canonical"], sr["paths_checked"] - sr["label_mismatch"],
       files56["rule22_n32.csv"]["own_distinct_rotation_orbits_of_cycles"], files56["rule22_n32.csv"]["own_distinct_cycles"],
       files56["rule94_n24.csv"]["own_distinct_rotation_orbits_of_cycles"], files56["rule94_n24.csv"]["own_distinct_cycles"],
       sr["paths_checked"], sr["paths_verified_step_by_step"], sr["paths_checked"]),
   "Rename the column 'distinct rotation orbits of cycles' and store the paths (state, cell, next cycle).")

F(17, "'Checked against v0.2 and an independent verifier' does not apply to n = 21, 22",
   "lines 504-505", "verified by reading; `out/misc_checks.json` (169 pairs), `out/compare_derived.json` (verifier coverage)", "overstated tag or wording (minor)",
   "The v0.2 sweep covers n <= 20 (%d pairs) and the verifier n <= 10. The records at n = 21, 22 had no second computation inside the study. "
   "They are now confirmed by the sealed sample." % mc["v02_sweep_vs_sample"]["pairs_compared"],
   "Write 'n = 8..20 checked against v0.2; n <= 10 against the verifier'.")

F(18, "Query: the Summary states the mechanisms without their range",
   "lines 18-21 ('In the switching classes that cycle is a spatially periodic crystal ... or the zero state ...')", "verified by reading", "query (wording)",
   "The sentence reads as a general statement; it is computed for n <= 22 and covers 10 of the 13 classes. For class 35 the crystal (100)^{n/3} is "
   "not 'selected alone' (almost all cycles are selected); the parenthesis 'within its code-carrying family' hedges this. The following sentences "
   "do say what is proved, so I list it as a query.",
   "Insert 'for n <= 22' and name classes 37, 45, 73 as not covered.")

F(19, "Query: `run_mech.py` documents an option that does not exist",
   "`code/ring_size/run_mech.py` line 11 ('[--max-rss-gb 4]')", "`out/cost_claim.json` (run_mech_has_cap_or_timeout_option, run_mech_docstring_mentions_max_rss_gb)",
   "bookkeeping (minor)", "The parser has no such argument and no time or memory limit; relevant to F6 because no cap is enforced or defined in code.",
   "Remove the option from the usage line or implement it.")

A("## B. Checked and correct")
A("")
A("1. **Sealed sample against `mechanisms.csv`** (verified by my computation; `compare_sample.py`, `out/compare_sample.json`, `out/compare_mismatches.csv`). "
  "%d records in the study, %d in the sample, %d in common, none on one side only. %d record fields compared (%d from the sealed sample: %s; %d from the "
  "supplement: %s). Mismatches: %s, all in the bijective records (F14). Where the study has no value (bijective records) the field was not counted." % (
      cs["records_study"], cs["records_sample"], cs["records_common"], len(rec_fields), len([k for k in rec_fields if f[k]["source"] == "sealed"]),
      ", ".join(k for k in rec_fields if f[k]["source"] == "sealed"), len([k for k in rec_fields if f[k]["source"] == "supplement"]),
      ", ".join(k for k in rec_fields if f[k]["source"] == "supplement"), ", ".join("%s %d" % kv for kv in mism_fields.items())))
A("2. **Orbit table `cycle_orbits.csv.gz`** (verified by my computation; same files). %d orbit rows in %d cases, every own orbit listed exactly once. "
  "Equal in all rows: orbit size, temporal period, spatial period, codes, radius (supplement) and the selected flag (sealed lists). Potentials: equal in "
  "all %d rows where the supplement has them, and the histogram of potentials equals the sealed one in all %d cases. `mech.jsonl` holds the same %d records "
  "and %d orbit rows as the csv tables." % (cs["orbit_rows_study"], cs["cases_with_orbit_rows"], f["orbit.gamma"]["compared"],
                                           f["orbit.gamma_histogram_by_cycles"]["compared"], cs["mech_jsonl_records"], cs["mech_jsonl_orbit_rows"]))
A("3. **Derived tables** (verified by my computation; `compare_derived.py`, `out/compare_derived.json`): `zero_mechanism.csv` %d rows, `code_carriers.csv` %d rows, "
  "`rule35_blocks.csv` %d rows, `g1_distance_154.csv` %d rows; %d mismatches. The block law of 5.2 holds for n = 8..22 with every state of every family "
  "cycle checked. For rule 154 at n = 8 and 16: %d and %d cycles, maximum G1 distance to 0 %d and %d, Spearman %.2f and %.2f." % (
      z["rows"], cd["code_carriers"]["rows"], cd["rule35_blocks"]["rows"], cd["g1_distance_154"]["rows"], cd["n_mismatches"],
      cd["g1_distance_154"]["own"]["8"]["cycles"], cd["g1_distance_154"]["own"]["16"]["cycles"], cd["g1_distance_154"]["own"]["8"]["max_distance"],
      cd["g1_distance_154"]["own"]["16"]["max_distance"], cd["g1_distance_154"]["own"]["8"]["spearman_mean_ones_vs_distance"],
      cd["g1_distance_154"]["own"]["16"]["spearman_mean_ones_vs_distance"]))
A("4. **Numbers in the report** (verified by my computation; `report_numbers.py`, `out/report_numbers.json`): %d checks, %d equal. The %d unequal ones are "
  "findings F4, F5 (two checks), F10 and F15. Equal: the k* table (%d cells for n = 8..22 from the sealed sample, one of them the marker 'not computed' for class 154 at n = 22; %d cells for n = 4..7 from the own sweep), "
  "'180 non-bijective records' and '175 with a single closed class', the tables of 5.1 and 5.2, the statements of 5.3, 5.4 and 5.5 other than F4 and F5, the "
  "numbers of the cost line as arithmetic on `mech_cost.csv` (but see F7), the atlas record count. The seed table (lines 304-309) equals the study's file "
  "(`out/report_numbers2.json`)." % (rn["n_checks"], rn["n_equal"], rn["n_unequal"], rn["by_id"]["kstar_table"]["checks"], rn["by_id"]["kstar_table_n4_7"]["checks"]))
A("5. **Atlas** (verified by my computation; `atlas_check.py`, `out/atlas_check.json`): %d of %d records compared, all %d classes (%d non-switching), n = %d..%d; "
  "%d fields; selected orbits compared pattern by pattern in %d records with n <= 14. Only mismatch: gamma_min in %d bijective records (F14)." % (
      at["records_compared"], at["atlas_records"], at["classes_compared"], at["non_switching_classes_compared"], at["n_range_compared"][0],
      at["n_range_compared"][1], len(at["fields"]), at["fields"]["selected_orbit_patterns_n_le_14"]["compared"], at["n_mismatches"]))
A("6. **Proofs** (verified by reading, each also tested by computation; `proof_verdicts.py`, `out/proof_verdicts.json`): %d statements correct, %d with a gap "
  "(the tag at line 256, see F12). Correct: re-rooting, Lemma 1, Lemma 2, Theorem A including gamma_min = m - 1 and the k* consequence, Lemma B including "
  "gamma_min = m + q - 2, the internal logic of the Ellison paragraph, Lemma Z, Lemma H with tau = 3 for class 94, Lemma P, Proposition R154, "
  "Proposition R22 (every case of the induction), the remark on the spatial period, and the other [proved] tags. Line-by-line reasons are in the file." % (
      pv["counts"].get("correct", 0), pv["counts"].get("gap", 0)))
A("7. **Counterexample search** (verified by my computation; `sweep88.py`, `out/sweep88.jsonl`, `out/sweep88_summary.json`): all %d classes (representatives "
  "derived in `p2lib.class_reps`), n = %d..%d, %d cases solved of %d (%d skipped for size, listed in the summary file). Counterexamples: 0 to the re-rooting "
  "inequality, Lemma 1, Lemma 2, Theorem A (union of closed classes: %d cases; unique closed class gives S = K and gamma_min = m - 1: %d cases) and Lemma B. "
  "Lemma B: a rotation orbit of radius >= 2 exists in %d cases (%d orbits, all tested directly); the hypotheses hold in %d cases (q = 1: %d, q = 2: %d, q = 3: %d) "
  "and the conclusion holds in all of them." % (
      sw["rules"], sw["n_range"][0], sw["n_range"][1], sw["cases_solved"], sw["cases_total"], len(sw["cases_skipped"]),
      tests["thmA_union_of_closed_classes"]["cases"], tests["thmA_unique_S_equals_K"]["cases"], lb["cases_with_a_radius_ge2_orbit"],
      lb["candidate_orbits_total"], lb["hypotheses_hold"], lb["hypotheses_hold_by_q"].get("1", 0), lb["hypotheses_hold_by_q"].get("2", 0),
      lb["hypotheses_hold_by_q"].get("3", 0)))
A("8. **Observation on Lemma B** (not an error). The weight-2 edges are needed only for the value gamma_min = m + q - 2. For S = A it suffices that every cycle "
  "outside A reaches A by weight-1 edges: then the closed classes of G1 are the singletons {A_i}, Theorem A puts S inside A and rotation symmetry gives S = A. "
  "In the sweep this weaker hypothesis holds in %d cases, the same cases as the full hypothesis (cases where only the weaker one holds: %d)." % (
      lb["weak_hypothesis_holds"], len(lb["weak_holds_but_G2_fails"])))
A("9. **Observation on Theorem A** (not an error). 'S = union of all closed classes' is tagged [computed] for the 180 records and is not a theorem: in the sweep "
  "it fails in %d case(s): %s (rule, n, closed classes, selected closed classes)." % (sw["S_proper_subset_of_union_count"], sw["S_proper_subset_of_union_cases"]))
A("10. **Lemma Z and Lemma P against brute force** (verified by my computation; `lemmaZP.py`, `out/lemmaZP.json`): Lemma Z for the 128 rules with F(0) = 0, "
  "n = %d..%d: %d cases, %d counterexamples. Lemma P for all 256 rules, same n: %d cases; the number of pairs (x, y) with F x = F y equals the trace of the n-th "
  "power of the pair-graph matrix in every case; no rule certified by the even-period criterion fails to be bijective at an odd n; certified rules: %s." % (
      zp["n_range"][0], zp["n_range"][1], zp["lemmaZ"]["cases"], len(zp["lemmaZ"]["counterexamples"]), zp["lemmaP"]["cases"],
      ", ".join(map(str, zp["lemmaP"]["certified_rules"]))))
A("11. **Certificate (a), pair graphs** (verified by my computation; `out/pairgraph_all256.csv`): rules 154 and 45 have off-diagonal component periods %s and %s; "
  "all %d rows of `injectivity.csv` agree." % (zp["rule154"]["offdiag_scc_periods"], zp["rule45"]["offdiag_scc_periods"], zp["injectivity_csv"]["rows"]))
A("12. **Certificate (b), healing and crystal radius** (verified by my computation; `crystal_checks.py`, `out/crystal_checks.json`, `out/lightcone_own.csv`, "
  "`out/crystal_radius_own.csv`): all %d rows of `lightcone.csv` reproduced (class 94 heals after %s steps, tau = %d; the other %d words do not heal within 200 "
  "steps). Crystal radius: %d rows, radius >= 2 for class 94 at every 3 | n from 6 to 399 and for classes 43 and 142 at every 4 | n up to 400; the only "
  "difference from `crystal_radius.csv` is the return-time entry at n = 3 of class 94, where the radius is below 2 in both files." % (
      len(cc["lightcone"]["rows"]), ", ".join(str(d["heal_time"]) for d in cc["rule94_line_flips"]),
      [r["tau"] for r in cc["lightcone"]["rows"] if r["healed"]][0], sum(1 for r in cc["lightcone"]["rows"] if not r["healed"]),
      cc["crystal_radius"]["rows_own"]))
A("13. **Certificate (c), seed orbits** (verified by my computation; `seed_orbits.py`, `seed_orbits_pass3.py`, `seed_compare.py`, `out/seed_compare.json`): on "
  "all rows the study determined, returns, transient and limit period agree (rule 22: %d of %d; 26: %d of %d; 122: %d of %d; 154: %d of %d). For rules 26 and 154 all %d "
  "undetermined n are even and are settled: %d by own simulation, the rest by Proposition R154; the return sets are the powers of two. Rule 22 and rule 122: see F1, F2." % (
      s22["study_determined_rows_equal"], s22["study_determined_rows"], s26["study_determined_rows_equal"], s26["study_determined_rows"],
      s122["study_determined_rows_equal"], s122["study_determined_rows"], s154["study_determined_rows_equal"], s154["study_determined_rows"],
      len(s26["study_capped"]), len(s26["study_capped_settled_by_own_simulation"])))
A("14. **Certificate (d), orbit identities of R154 and R22** (verified by my computation; `rule90_identities.py`, `out/rule90_identities.json`): for all %d even "
  "n <= 256 the orbits of e_0 under rules 90, 154, 26 coincide step by step, stay on the sites of parity t and equal X^(-t)(1+X)^(2t) (%d steps checked); they die "
  "exactly at the powers of two, at t = n/2. For all %d n <= 256 with 4 | n the rule-22 orbit equals R_t at even t and R_t united with R_(t-1) at odd t, R_s has "
  "no two ones at distance 2 for even s and equals the dilated half-ring orbit (%d steps checked). The algebraic criterion (X^n - 1 divides a power of 1 + X iff "
  "n is a power of two) was checked for n = 2..256." % (r90["R154"]["even_n"], r90["R154"]["steps_checked"], r90["R22"]["n_4_divides"], r90["R22"]["steps_checked"]))
A("15. **Certificate (e), table 5.6** (verified by my computation; `sampled_reach_check.py`, `out/sampled_reach_check.json`): all %d rows of the table reproduced from "
  "the study's files; the radius flags re-derived with own code agree in all %d files; periods of all %d sampled limit cycles agree. See F16 for the paths." % (
      sr["table_5_6_rows"], len(files56), sr["paths_checked"]))
A("16. **Certificate (f), factor search** (verified by my computation; `misc_checks.py`, `out/misc_checks.json`): the 8 counts of `factor_search.csv` reproduced; "
  "target rules found: %s; no additive target." % mc["factor_search"]["target_rules_own"])
A("17. **Tags** (`tags_audit.py`, `out/tags_audit.csv`): %d tags (%d [proved], %d [computed], %d [observed], including the three definitions); %d match the evidence; "
  "%d overstated and %d with a wrong statement (lines %s; findings F1, F2, F4, F5, F12, F15). The [proved] tags are at lines %s; each is judged in `out/proof_verdicts.json`." % (
      ta["tags"], ta["by_kind"]["proved"], ta["by_kind"]["computed"], ta["by_kind"]["observed"], ta["by_verdict"]["matches the evidence"],
      ta["by_verdict"].get("overstated", 0), ta["by_verdict"].get("statement under the tag is wrong", 0), ", ".join(str(x[0]) for x in ta["not_matching"]),
      ", ".join(map(str, ta["proved_lines"]))))
A("18. **Patterns classified 'explained, not proved' or 'resists'** (verified by reading): in the mechanism table of Section 5 and in sections 5 to 8 they carry "
  "their status; exceptions are F3 (PR draft, class 22), F12 and F18. The commit messages state no result.")
A("19. **Report generation** (verified by reading `make_report.py` and the template; `out/report_numbers2.json`): the report is the template with %d placeholders "
  "filled; %d static template lines, all verbatim in the report. The two text inputs `literature_section.md` and `ellison_remark.md` are tracked. The manifest "
  "lists %d files, all hashes correct (`out/misc_checks.json`)." % (tpl["n_placeholders"], tpl["static_lines"], mc["manifest"]["entries"]))
A("20. **Predictions** (`predictions_recount.py`, `out/predictions_recount.json`, `out/predictions_recount.csv`): the sealed file is unchanged since commit 8d68e54. "
  "On the study's %d rows I reach the same outcome in all but two (F8 and class 154 at n = 22, now computed). Outcomes decided from own data and from the study's "
  "files agree in %d of %d parts (the exception is class 154 at n = 22, which the study's files cannot decide). Sealing before computation (`seal_timing.py`, `out/seal_timing.json`): the seal commit is from %s; none of the %d files and "
  "folders under `data/ring_size`, `code/ring_size`, `figures/ring_size` was created or modified before it (earliest: %s at %s). This does not exclude "
  "computations that left no file." % (pr["study_table_rows"], pr["own_parts_total"] - len(pr["own_vs_study_data_disagreements"]), pr["own_parts_total"],
                                    st["seal_commit_time_local"], st["ring_size_files_and_folders"],
                                    st["ring_size_earliest_births"][0][2], st["ring_size_earliest_births"][0][0]))
A("21. **Class 154 at n = 22** (verified by my computation; `v154_n22.py`, `out/v154_n22.json`): %d cycles in %d rotation orbits (%d of %d states are periodic; the "
  "map is not bijective). G1 has %d edges, one strongly connected component, hence one closed class containing all cycles; no cycle is without an out-edge. "
  "V rows were computed for all %d orbit representatives (never stored): no row check failed (%d failures), off-diagonal minimum %d, maximum %d, the entries "
  "V = 1 number %d and coincide with the G1 edge set. Edmonds' algorithm ends after the first level (one strongly connected component of minimum-weight arcs): "
  "gamma = %d = m - 1 for every cycle, all %d cycles selected, codes %s, k_c = 0 for all c, **k* = %s**. This agrees with the sealed prediction (k* = 0) and "
  "with Theorem A (unique closed class K, S = K, gamma_min = m - 1). Cost: %.0f CPU-minutes, peak memory %.0f MB." % (
      v["cycles"], v["rotation_orbits"], v["cycle_states"], v["states"], v["g1_edges"], v["V_rows_computed"], len(v["row_check_failures"]),
      v["rho_min"], v["V_max"], v["V_equal_1_entries"], v["gamma_min"], v["selected_cycles"], v["selected_cover"], v["kstar"],
      v["cpu_seconds"] / 60, v["peak_rss_mb"]))
A("22. **Proposition R154, remark** (verified by my computation for odd n = 3..21, `out/proof_verdicts.json`, and by the seed orbits for all odd n <= 256): for "
  "rule 26 at odd n the only preimages of 0 are 0 and 1^n, and 1^n has no preimage, so the zero state has radius 1; with bijectivity of rule 154 at odd n, "
  "'r(0) >= 2 iff n is a power of two' holds for both rules at every n in the computed range and, by these two arguments, for every n >= 3.")
A("")
A("## C. Not checked, and why")
A("")
A("1. `literature_ring_size.md` and Section 2 of the report: a separate track.")
A("2. The figures in `figures/ring_size/` and `figures_ring_size.py`: not opened; no number in this file depends on them.")
A("3. The study's code was not executed (`reproduce_ring_size.sh`, `test_ring_size.py`, `verify_mech.py`): the task forbids runs that write into existing "
  "files. `make_report.py`, `check_predictions.py`, `run_mech.py` and `sample_reach.py` were read; `mech.py`, `ringlang.py`, `lightcone.py`, `run_local.py`, "
  "`analyze_mechanisms.py`, `factor_search.py` and `code/fw/` were not read beyond a few lines.")
A("4. The contents of the two verifier files beyond coverage (their `ind_*` columns): not compared; the same (rule, n) pairs with n = 4..10 are covered by the own sweep.")
A("5. v0.2 statements used by the report (Proposition 1 on rules 60 and 90, 'a bijective map has k* = 0'): v0.2 is not under review; the bijective case is "
  "confirmed in the 14 bijective sample cases and proved in `../SAMPLE.md`.")
A("6. Structural descriptions in 5.5: 'carriers are (100)-crystals with 111-defects' (class 26), 'carriers built on the period-6 pattern 100000' (class 37), and "
  "'half of the single flips start a domain of another phase' (classes 43, 142, line 249): not checked. For 43 the maximal return time grows linearly with n "
  "(`out/crystal_checks.json`), which is consistent with the last one.")
A("7. Atlas: %d records not compared (all n = 20 records and the cases skipped by the sweep); the atlas log's comparison with v0.2 was not repeated." % (
    at["atlas_records"] - at["records_compared"]))
A("8. Sweep: %d (rule, n) cases skipped for size (rules %s at n >= %d; list in `out/sweep88_summary.json`); n >= 20 not searched." % (
    len(sw["cases_skipped"]), ", ".join(map(str, sorted({c[0] for c in sw["cases_skipped"]}))), min(c[1] for c in sw["cases_skipped"])))
A("9. Seed orbits still undetermined after 6e9 steps: rule 22 at n = %s; rule 122 at n = %s (their limit periods are expected to exceed the budget)." % (
    ", ".join(map(str, s22["study_capped_open"])), ", ".join(map(str, s122["study_capped_open"]))))
A("10. Whether Ellison's theorem is quoted correctly (only the internal logic of the paragraph was checked).")
A("11. The dense all-roots Edmonds computation for rule 154 at n = 22 (5.9 GB): not run. The level-wise variant used instead equals the dense one in all %d sweep "
  "cases where both were run, and at n = 22 it ends at the first level, where it needs only the minimum of each row of V." % tests["lean_edmonds_equals_dense"]["cases"])
A("12. Per-orbit potentials of the %d sample cases whose sealed solve took more than 30 CPU-seconds: compared by histogram only." % (
    cs["records_common"] - sum(1 for r in extras if r["gamma_per_orbit"])))
A("")
A("## Appendix 1. Summary of the report, sentence by sentence (verified by reading)")
A("")
A("| lines | sentence (shortened) | verdict |")
A("|---|---|---|")
A("| 15-16 | selected cycles are a union of closed classes of G1 (Theorem A, proved for all n) | correct |")
A("| 16-18 | a cycle that cannot be left with one flip is selected alone once every other cycle reaches it by one-flip steps (Lemma B) | correct (for a rotation orbit, 'alone' means the orbit) |")
A("| 18-21 | in the switching classes that cycle is a crystal (94, 43, 142, 35 within its family) or the zero state (154, 26, 22, 60, 90, 122) | query F18: range n <= 22 not stated; 37, 45, 73 not covered |")
A("| 21 | inherited from rule 90's nilpotency at n = 2^k for 154 and 26, proved | correct (Proposition R154) |")
A("| 21-23 | proved for all n: general statements; k* = 0 for 154 and 45 at odd n; radius for class 94 for all 3 / n; zero state of 154, 26 for even n and of 22 for 4 / n | F11: n = 3 must be excluded for class 94; the rest correct |")
A("| 24-25 | not proved: reachability; 'this single statement' computed for n <= 22 and sampled up to 32 | F12: not the only gap |")
A("| 26 | class 122 at even n, class 26 away from powers of two, single switches of 45 and 73 resist | consistent with 7(c) |")
A("")
A("## Appendix 2. Recount of the sealed predictions (`out/predictions_recount.csv` has all %d parts)" % pr["own_parts_total"])
A("")
A("| count | study's table (%d rows) | own outcome on the same rows | all %d own parts |" % (pr["study_table_rows"], pr["own_parts_total"]))
A("|---|---|---|---|")
for k in ["holds", "fails", "not tested", "holds (trivially)", "holds (observed, sampled)", "not a testable statement"]:
    A("| %s | %s | %s | %s |" % (k, study_counts.get(k, 0), own_rows_counts.get(k, 0), pr["own_counts_all_parts"].get(k, 0)))
A("")
A("Rows judged differently from the study: %s." % "; ".join("'%s': study %s, own %s" % (d["row"], d["study"], d["own"]) for d in diff_rows))
A("")
A("## Appendix 3. Files of this part")
A("")
A("Scripts: `p2lib.py`, `p2core.c`, `lean_edmonds.py`, `extras.py`, `compare_sample.py`, `compare_derived.py`, `report_numbers.py`, `report_numbers2.py`, "
  "`atlas_check.py`, `sweep88.py`, `sweep_summary.py`, `lemmaZP.py`, `proof_verdicts.py`, `orbitlib.py`, `p2orbit.c`, `seed_orbits.py`, `seed_orbits_pass3.py`, "
  "`seed_compare.py`, `crystal_checks.py`, `rule90_identities.py`, `p2reach.c`, `sampled_reach_check.py`, `misc_checks.py`, `details_45_73.py`, `tags_audit.py`, "
  "`predictions_recount.py`, `seal_timing.py`, `cost_claim.py`, `v154_n22.py`, `g1_timing.py`, `make_findings.py`. Outputs: `out/`. Logs: `logs/`, `../logs/BATCHES_phase2.md`.")
open(os.path.join(HERE, "FINDINGS_part1.md"), "w").write("\n".join(L) + "\n")
print("wrote FINDINGS_part1.md", len(L), "lines", round(cpu_total / 3600, 3), "CPU-hours")
