# Verification of the ring-size study

Object: branch `ring-size-mechanisms` (commits 8d68e54, 8bcad22, 1e256cd after main at 2ef9d00):
`report_ring_size.md`, `literature_ring_size.md`, `PREDICTIONS_ring_size.md`, `code/ring_size/`,
`data/ring_size/`, `figures/ring_size/`, `reproduce_ring_size.sh`, and the untracked `PR_DRAFT.md`.
Version 0.2 itself is not under review. Nothing in the study was changed. Date: 2026-11-14.

Question: are the results and proofs correct, are the claims no stronger than the evidence, and can the
central open statement be proved?

Everything written by this verification is in `verify_ring_size/` on branch `verify-ring-size`. Each
section below names the file its numbers come from; paths are relative to `verify_ring_size/` unless a
study file is named. Line numbers refer to `report_ring_size.md` at commit 1e256cd unless a file is named.

## Answer in brief

1. **Results.** The data are right. All 194 common (rule, n) records agree with a blind sample computed
   with separate code, except a placeholder value in the bijective records (A17). Three sentences of the
   report contradict the study's own data (A1 to A3), and one list is incomplete because undetermined runs
   were read as "no return" (A1, A8).
2. **Proofs.** No wrong proof step was found. Every statement tagged [proved] is correct; one tag is too
   strong for two of the three classes it covers (A11). No counterexample to Theorem A or Lemma B in
   1476 cases over all 88 classes (B7).
3. **Claims versus evidence.** Several sentences are stronger than their evidence (A8 to A15). The cost
   claim for class 154 at n = 22 is not supported in compute time (A4): the job had at most about 76
   minutes of awake time. The case is now computed: k* = 0 (B12).
4. **Predictions.** On the study's 50 rows the recount is 41 hold, 6 fail, 1 not tested, plus the two
   qualified rows (A6, A7); the study states 41, 5 and 2.
5. **Literature.** Lemma B and the first sentence of Theorem A correspond to known results in the
   stochastic-stability literature (A20, A21; provisional, primary texts not read). Ellison's Theorem 2 is
   described correctly (A22).
6. **The open statement (Part 2).** It is proved for class 94 at every n >= 6 with 3 | n (D1) and for
   rule 154 at every n = 2^k >= 4 (D2). For rule 154 the converse is proved as well, so k* = 1 iff n is a
   power of two, for all n >= 3. Classes 122 and 26 are settled only in part (D3, D4). These proofs were
   checked inside this verification only (line-by-line reading and two separate codes each); they have had
   no outside reader.

## How the verification was done

* **Sealed blind sample (step 1).** Own solver written from the definitions (`core.c`, `eca_core.py`,
  `solve.py`), validated against brute force before use (`logs/validation_summary.json`), then run on the
  13 switching classes at n = 8..22 except class 154 at n = 22: 194 cases. Sealed in `SAMPLE.md` and
  committed as a384763 before any claim file was opened by the track that computed it.
* **Comparison, proofs, tags, predictions, cost (steps 2 to 6).** `phase2/FINDINGS_part1.md` with scripts
  and outputs in `phase2/`.
* **Literature (step 7).** `literature/literature_check.md`.
* **Own proof attempts (steps 8, 9).** `part2_94/PROOF_94.md`, `part2_154/PROOF_154.md`; the lead's
  re-tests of their lemmas are in `audit/`.

Disclosures on independence and on departures from the task.

* Before the sample was computed, the lead saw truncated one-line memory summaries of the study
  (mentioning crystal patterns for classes 94 and 43/142 and a defect family for class 35). None of this
  was passed to the code or to the track that computed the sample (recorded in `SAMPLE.md`).
* The literature track read `report_ring_size.md` before the seal, in a separate context with no channel
  to the sample track. Its result was read by the lead only after the seal commit.
* The sample track took the definitions from the task text and did not open `note/note_v0.2.tex`; the
  lead had checked that text against Sections 1 and 6 of the note.
* Class 154 at n = 22 is not in the sealed sample; its three larger n are 16, 20, 21. It was computed
  after the seal with a memory-lean method (B12).
* In the validation of the solver, the per-root cross-check of gamma used 16 sampled roots instead of all
  roots in 15 of 1536 cases (those with more than 64 cycles).
* Load. The sample ran with 2 worker processes. In the second phase one sustained process ran the
  verification batches; the two proof tracks ran short single-process experiments at the same time, so
  three processes were briefly active. Memory estimates stated before launch were exceeded four times
  (2.4 GB against 2.0 GB; 2.27 GB against 0.6 GB; 4.3 GB against 1.5 GB for about 15 CPU-seconds; 1.08 GB
  against 0.9 GB); all are recorded in `logs/BATCHES.md` and `logs/BATCHES_phase2.md`.
* Cost in CPU time: sealed sample and its validation 0.93 CPU-hours (total as reported by the sample
  track; per-batch figures in `logs/BATCHES.md`); steps 2 to 6
  1.27 CPU-hours (`phase2/out/cpu_total.json`), of which class 154 at n = 22 took 48.2 CPU-minutes; the
  proof tracks and the lead's audits under one CPU-minute each (`part2_94/PROOF_94.md` section 7,
  `part2_154/PROOF_154.md` section 10, `audit/out/*.json`).

---

# Part 1: verification

## A. Errors found

Severity: **result** (a stated result is wrong), **wording** (a tag or sentence is stronger than its
evidence), **bookkeeping**, **attribution** (literature). Items A1 to A19 are findings F1 to F19 of
`phase2/FINDINGS_part1.md`, which gives the full evidence; A20 to A31 are findings L1 to L13 of
`literature/literature_check.md`. The lead re-checked A1, A2, A3, A4 and A6 with separate code
(`audit/audit_findings.py`, `audit/out/audit_findings.json`).

### Wrong results in the text (the data files are right)

**A1 (F1). Rule 22: the list of ring sizes where the seed orbit returns to 0 omits n = 241.**
Location: lines 331-332 ([computed]), also lines 211, 363-365, 488-489, 500; `PR_DRAFT.md` lines 37-38.
Evidence: in the study's `seed_orbits.csv`, 25 values of n not divisible by 4 are undetermined at the
400000-step cut-off, so the list is the list of returns found, not of returns. At n = 241 the orbit
reaches 0 after 1303564 steps (`phase2/out/rule22_n241_check.json`; same step count in the lead's
simulation, `audit/out/audit_findings.json`). After this verification n = 242 and 243 remain open
(`phase2/out/seed_compare.json`).
Fix: add 241; replace "computed up to 256" by the set of n decided and name the open n; in 7(c) write
"121, 125, 241, 253".

**A2 (F4). Class 45: "all cycles are selected" at every even n >= 10 is false at n = 18 and n = 22.**
Location: lines 375-376 ([computed]).
Evidence: 199 of 201 cycles are selected at n = 18 and 271 of 272 at n = 22 (sealed sample, histogram of
potentials; `audit/out/audit_findings.json`, `phase2/out/details_45_73.json`). The study's own
`cycle_orbits.csv.gz` marks the uniform 2-cycle as not selected at n = 18. The radius statement and
k* = 0 are unaffected.
Fix: "it has radius 1 and all cycles are selected except two at n = 18 (among them the uniform 2-cycle)
and one at n = 22".

**A3 (F5). Class 73: the uniform 2-cycle is not selected at n = 22 either; no cycle of temporal period 3
is selected at n = 9.**
Location: lines 377-378 ([computed]); mechanism table line 216.
Evidence: at n = 22, 13303 of 13304 cycles are selected and the uniform 2-cycle has potential 13304
against the minimum 13303 (sealed sample and the study's own orbit table; `audit/out/audit_findings.json`).
k* stays 0 there. At n = 9 the selected cycles are the three phases of (011)^3 and two orbits of temporal
period 2 (`phase2/out/details_45_73.json`).
Fix: say so; if "period-3 cycles" means spatial period 3, write that.

### Cost claim

**A4 (F6). The cap was not exceeded in compute time.**
Location: line 534, lines 454 and 528; `data/ring_size/stopped_runs.csv`; `reproduce_ring_size.sh`
line 15; `PR_DRAFT.md` lines 43, 57, 61.
Evidence (`phase2/out/cost_claim.json`, `phase2/out/pmset_sleep_wake.txt`): the 7.4 h are wall time
between the creation of `log_mech_154_n22.txt` (2026-11-14 00:46:21) and the stop at 08:09
(`stopped_runs.csv`, column `wall_hours`). The system power log shows the machine asleep from 02:00:31 to
08:08:00, i.e. 6.12 h of the 7.39 h. The job had at most 76.2 minutes of awake time. No CPU time was
recorded: the log holds one line, and `cost_seconds` in `run_mech.py` is `time.time()` wall time written
only when a job ends. The 5 h cap is defined nowhere in the repository, and `run_mech.py` has no cap or
time-out option.
Fix (corrected wording): "Class 154 at n = 22 was started at 00:46 and stopped at 08:09; the machine was
asleep from 02:00 to 08:08, so the job ran for at most about 1.3 h and was stopped unfinished; its CPU
time was not recorded. It is not computed in this study." Change the outcome text "run stopped above the
stated cost cap" accordingly, define the cap as CPU time, and record `time.process_time()` per job. The
value is available from this verification: k* = 0 (B12, D2).

**A5 (F7). "Total CPU 1.9 h" is a sum of wall-clock times.** Location: line 534; `run_mech.py` lines 26,
38. Evidence: `phase2/out/cost_claim.json`; for the n = 21, 22 batch the study's log shows more CPU than
wall time (real 51m, user 80m, sys 17m). Fix: "sum of the wall times of the jobs", or record CPU time.

### Predictions

**A6 (F8). One sealed part is reported as holding after it was narrowed.**
Location: line 433; `predictions_outcome.csv` row "26, other n with k* >= 1: missing code 7";
`check_predictions.py` line 83.
Evidence: sealed text of P6: "at the other n with k* = 1 the missing code is 7". At n = 8 class 26 has
k* = 1 with the zero state selected alone and codes 1 to 7 missing (sealed sample;
`audit/out/audit_findings.json`); the study's check excludes n = 8 together with n = 16.
Fix: report the row as "fails at n = 8, holds at n = 9, 10, 12, 13, 15, 18, 19, 21".

**A7 (F9). The outcome table does not cover every sealed statement, and the counts change.**
Location: lines 409-412, 529; `PR_DRAFT.md` lines 42-43.
Evidence (`phase2/out/predictions_recount.json`, `.csv`; Appendix 2 of the findings file): the sealed
file is unchanged since 8d68e54 and no ring-size file predates the seal commit. On the study's 50 rows:

| outcome | study | recount |
|---|---|---|
| holds | 41 | 41 |
| fails | 5 | 6 |
| not tested | 2 | 1 |
| holds (trivially) | 1 | 1 |
| holds (observed, sampled) | 1 | 1 |

The two rows judged differently are A6 and class 154 at n = 22 (now computed: holds). "41 hold, 5 fail,
2 not tested" in the PR draft also leaves out the two qualified rows. Splitting the sealed text into
single statements gives 92 parts, of which the 50 rows cover 63; among the 29 uncovered parts 6 fail (the
expectation G3 and the expected proofs for the direction "p does not divide n" of classes 94, 43, 142 and
for the radius of 43, 142). Three outcomes are typed into `check_predictions.py` rather than decided from
data. The remaining "not tested" row (P9: k* of class 154 at n = 32, 24, 28) holds by the proof in D2.
Fix: correct the counts; add rows for G1 to G3 and the proof expectations, or state the table's scope.

### Tags and wording stronger than the evidence

**A8 (F2). Rule 122: "returns exactly at n = 7, 15, 31, 63, 127, 255" ([computed], lines 348-349).**
33 values of n are undetermined in the study's file. This verification settled 20 (none returns); 13
remain open: 133, 141, 157, 165, 189, 201, 205, 213, 221, 229, 241, 243, 249
(`phase2/out/seed_compare.json`). Fix: "at no other n <= 256 whose orbit could be decided; 13 n open";
tag the pattern 2^k - 1 as [observed]. For rules 26 and 154 all 33 undetermined n are even and are decided
by Proposition R154 (no return); the report should say so (also L9).

**A9 (F3). `PR_DRAFT.md` lines 37-38 state the class-22 pattern as a result up to n = 256.** k* of class
22 is computed for n <= 22; beyond that only the seed orbit is known. The list there also omits 126-128,
254-256 and 241. Fix: separate "k* computed, n = 4..22" from "seed orbit only".

**A10 (F11). Summary, lines 22-23: "class 94 for all 3 | n" includes n = 3,** where one flip leaves the
crystal (`phase2/out/crystal_checks.json`). The body is correct (n >= 6). Fix: add "n >= 6".

**A11 (F12). More than one statement is unproved.** Location: lines 24-25 ("this single statement"),
479-481, tag at line 256; `PR_DRAFT.md` lines 34-35. Also unproved in the study: (i) the radius of the
crystal of classes 43 and 142 beyond n = 400, so "[proved conditional on reachability]" at line 256 is too
strong for these two classes; (ii) the seed sets of rule 22 at n not divisible by 4 and of rule 122;
(iii) the direction "condition fails, hence k* = 0" for every class except odd n of 154 and 45.
Fix: name the three gaps; tag line 256 per class.

**A12 (F13). Lines 5-6: "every number below is filled in from a data file".** 287 of the 338 template
lines have no placeholder and are copied verbatim; ring sizes and counts in them are typed, among them
the sentences of A2, A3 and the claim around A1 (`phase2/out/report_numbers2.json`). Fix: generate those
sentences, or restrict the statement to the tables.

**A13 (F15). Lines 298-299: "wherever the zero state is selected alone, Lemma B holds".** The study's flag
is true in 9 of 13 such cases; the other 4 are rules 60 and 90 at n = 8, 16, where {0} is the only cycle
(`phase2/out/compare_derived.json`). Nothing is wrong mathematically. Fix: add "(in the nine cases with
more than one cycle)".

**A14 (F17). Lines 504-505: "checked against v0.2 and an independent verifier"** does not apply to
n = 21, 22 (v0.2 covers n <= 20, the verifier n <= 10). Those records are now confirmed by the sealed
sample. Fix: state the ranges.

**A15 (F18, query). Summary lines 18-21** state the mechanisms without the range n <= 22 and without
naming classes 37, 45, 73 as not covered. Fix: insert both.

### Bookkeeping

**A16 (F10). Lines 97-98; `PR_DRAFT.md` line 48: "432 (rule, n) pairs (all 88 classes at n = 4..8, the 13
switching classes at n = 9, 10)"** describes 466 pairs; the 34 missing ones are the bijective maps, which
the study's verifier does not treat (`phase2/out/compare_derived.json`). Fix: say so.

**A17 (F14). `mechanisms.csv` and the atlas write gamma_min = 0 for bijective maps.** The value is m - 1
(sealed sample: full computation in all 14 bijective cases). This is the only field that differs between
the sealed sample and `mechanisms.csv` (14 of 194 records) and the only one in the atlas (80 of 1232
records compared). Not used in the report text. Fix: write m - 1 or leave the field empty.

**A18 (F16). Table 5.6: the column `distinct_cycles` counts rotation orbits of cycles, and the one-flip
paths called "exact certificates" are not stored** (only their lengths). An own search found and
re-verified a path for all 3400 sampled initial states (`phase2/out/sampled_reach_check.json`). Fix:
rename the column; store the paths.

**A19 (F19, query). `run_mech.py` line 11 documents an option `--max-rss-gb` that the parser does not
have.** Relevant to A4: no cap is enforced in code.

### Literature and attribution (step 7)

Sources read by this verification (`literature/literature_check.md`, section 1): Martin, Odlyzko and
Wolfram (1984) in full; Ellison (2000), published version, 15 of 29 pages (all definitions, Theorems 1 to
3, Section 6.2); Jen (1986, 1988, two papers) abstracts only; Wuensche and Lesser (1992) and the Wolfram
Atlas not obtained (hosts refused after approval); numeric comparisons were done against substitutes
(MOW tables, OEIS b-files, Table 2 of Bagnoli et al.). Samuelson (1994) and Noeldeke and Samuelson (1993)
were not read in the primary text.

**A20 (L1, attribution; provisional on the primary texts). Lemma B is in substance the
single-mutation-chain lemma that Ellison (2000, Section 6.2, pp. 37-38; working paper p. 30) attributes to
Samuelson (1994) and Noeldeke and Samuelson (1993, 1997).** The passage is in the version the study read
and is not mentioned. Location: lines 137-153; `ellison_remark.md` 1-7; `PR_DRAFT.md` 27-28. Not found in
the sources read: the value gamma_min = m + q - 2. Fix: present Lemma B as a restatement for this model,
keep the short proof, and limit "not found" to the explicit potential.

**A21 (L2, attribution; provisional). Lemma 1, Lemma 2 and the first sentence of Theorem A correspond to
the "mutation-connected component" and "locally stable component" results of Samuelson (1994, abstract)
and Noeldeke and Samuelson (1993, Proposition 1).** The latter is known here only through secondary
descriptions, which an additional search by the lead found in three independent papers and lecture notes.
Location: lines 110-132, line 16; `PR_DRAFT.md` 26-27. Not found in the sources read: gamma_min = m - 1
for a unique closed class. Fix: obtain and cite the primary texts; until then describe the structure as
known, marked "not read".

**A22 (L3). Ellison's Theorem 2 is numbered and described correctly** (published version: Theorem 2,
Section 4.2, p. 30; same numbering as the working paper). No wrong hypothesis, conclusion, volume, pages
or DOI was found. Two short summaries (lines 75-76; `literature_section.md` 38-39) omit conclusion (b),
the waiting-time bound W(y, Omega, eps) = O(eps^(-CR*(Omega))). Fix: cite the journal page, add (b).

**A23 (L4). "It adds equality" (lines 151-153; `PR_DRAFT.md` line 28) overstates the difference** when
the selected set is a single cycle: Ellison (p. 38) already gives mu*(Omega) = 1 for a single limit set.
Equality is an addition only for q > 1, and there it follows from rotation symmetry.

**A24 (L5). Bijectivity of rules 154 and 45 at odd n is in the literature** (Bhattacharjee and Das,
arXiv:1903.06011, Example 2; Fedoriaka, arXiv:2501.06648, by computation for N <= 20 and constructions;
Nobe and Yura 2004, abstract only). The study gives no reference for rule 45. Rule 45 is the output
complement of the mirror image of rule 154, so the two certificates of Lemma P are one statement. Fix:
cite; say that Lemma P re-proves a known fact.

**A25 (L6). Rule 90 at n = 2^k: the primary source is MOW, Lemma 3.5 (p. 230); the "iff" follows from
their Theorems 3.3 and 3.4 with corollaries.** The study cites MOW second-hand. Fix: cite directly.

**A26 (L7). Proposition R154 has partial precedents not mentioned:** OEIS A070886 (comment: rules 26 and
154 give the rule-90 pattern from a single cell on the line), MOW Section 5 (the same reduction for
rule 18), OEIS A334504 and A334507 (single-cell periods of rules 26 and 122 on rings). The ring statements
for rules 154 and 22 were not found in the sources read.

**A27 (L8, L13). Novelty wording stronger than "not found in the sources read":**
`literature_ring_size.md` line 239 ("consistent with the absence of any such statement in the
literature"); lines 146-147 and 152 of the report; `PR_DRAFT.md` lines 26-28 (Theorem A and Lemma B
listed as main results without prior art). Fix: reword.

**A28 (L10). `literature_ring_size.md` line 169 cites a "corollary to Theorem 3.2" of MOW that does not
exist;** the content is Theorems 3.2, 3.4 and the first corollary to Theorem 3.4.

**A29 (L11). Access statements are out of date:** MOW and the published Ellison article were reachable
(author copies); `literature_ring_size.md` and lines 40-42 say otherwise.

**A30 (L12). The class-94 crystal is the set of non-null fixed points of rule 90 given in MOW,
Lemma 3.7 (p. 234).** A reference to add; no change of status.

**A31 (L9).** See A8: the "undetermined" seed orbits of rules 26 and 154 are decided by Proposition R154.

## B. Checked and correct

1. **Sealed sample against the study's data** (`phase2/out/compare_sample.json`): 194 records on each
   side, 23 record fields; the only mismatch is A17. 60355 orbit rows of `cycle_orbits.csv.gz`: orbit
   size, temporal and spatial period, codes, radius and the selected flag agree in all rows; potentials in
   all 23833 rows where they were recomputed, and by histogram in all 180 non-bijective cases.
2. **k* table** (lines 186-200): all cells for n = 8..22 equal the sealed sample (also checked by the
   lead directly: 194 of 194), and the 52 cells for n = 4..7 equal an own computation.
3. **Numbers in the report** (`phase2/out/report_numbers.json`): 590 checks, 585 equal; the 5 unequal
   are A2, A3 (two checks), A13 and A16. Equal among others: "180 non-bijective records", "175 with a
   single closed class", the tables of 5.1 and 5.2, the derived tables (`zero_mechanism.csv`,
   `code_carriers.csv`, `rule35_blocks.csv`, `g1_distance_154.csv`: 0 mismatches).
4. **Atlas** (`phase2/out/atlas_check.json`): 1232 of 1327 records compared, 19 fields; only A17 differs.
5. **Proofs, by reading** (`phase2/out/proof_verdicts.json`; Theorem A and Lemma B also re-derived by the
   lead before the study's proofs were read): correct are the re-rooting statement, Lemma 1, Lemma 2,
   Theorem A including gamma_min = m - 1 and the k* consequence, Lemma B including gamma_min = m + q - 2,
   the internal logic of the Ellison paragraph, Lemma Z, Lemma H with tau = 3 for class 94, Lemma P,
   Proposition R154, Proposition R22 (every case of the induction), and the remark that the spatial
   period divides n. 16 statements correct, 1 tag too strong (A11).
6. **Observation on Lemma B (not an error).** The weight-2 edges are needed only for the value
   gamma_min = m + q - 2. For S = A it suffices that every cycle outside A reaches A by weight-1 edges:
   Theorem A then puts S inside A and rotation symmetry gives S = A. Part 2 uses this weaker form.
7. **Counterexample search** (`phase2/out/sweep88_summary.json`): all 88 classes, n = 3..19, 1476 cases
   solved of 1496. No counterexample to the re-rooting inequality, Lemma 1, Lemma 2, Theorem A (unique
   closed class in 1412 cases) or Lemma B (hypotheses hold in 327 cases). Lemma Z: 1664 cases; Lemma P:
   3328 cases (256 rules, n = 3..15), each without counterexample (`phase2/out/lemmaZP.json`).
   Observation: "S equals the union of all closed classes", tagged [computed] for the 180 records, is not
   a theorem; it fails for rule 164 at n = 16 (two closed classes, one selected).
8. **Certificates rebuilt.** Pair graphs for all 256 rules: 154 and 45 have off-diagonal component
   periods 2 and 2, and all 13 rows of `injectivity.csv` agree. Healing on the line: all 7 rows of
   `lightcone.csv` reproduced (class 94: tau = 3). Crystal radius: 333 rows, radius >= 2 for class 94 at
   every 3 | n from 6 to 399 and for 43, 142 at every 4 | n up to 400. Orbit identities of R154 for all
   127 even n <= 256 and of R22 for all 64 n <= 256 with 4 | n, step by step. Factor search: counts
   reproduced. (`phase2/out/pairgraph_all256.csv`, `crystal_checks.json`, `rule90_identities.json`,
   `misc_checks.json`.)
9. **Seed orbits** (`phase2/out/seed_compare.json`): on every row the study determined, return, transient
   and limit period agree (rule 22: 222 rows; rules 26, 122, 154: 220 each).
10. **Tags** (`phase2/out/tags_audit.csv`): 45 tags (17 [proved], 23 [computed], 5 [observed], three of
    them in the tag definitions); 36 match the evidence, 3 are overstated and 3 are attached to a wrong
    statement (lines 256, 299, 332, 349, 376, 378; items A1 to A3, A8, A11, A13). Patterns classified
    "explained, not proved" or "resists" keep that status in Sections 5 to 8; the exceptions are A9, A11
    and A15. The commit messages state no result.
11. **Sealing of the predictions** (`phase2/out/seal_timing.json`): the sealed file is unchanged since
    8d68e54 (2026-11-13 23:19:23); none of the 76 files and folders under `data/ring_size`,
    `code/ring_size`, `figures/ring_size` was created or modified before that. This does not exclude
    computations that left no file.
12. **Class 154 at n = 22, computed** (`phase2/out/v154_n22.json`): 76600 cycles in 38328 rotation orbits;
    G1 has 4756911 edges and one strongly connected component; rows of V for all 38328 orbit
    representatives (minimum 1, maximum 12); gamma = 76599 = m - 1 for every cycle; all cycles selected;
    all eight codes covered; k* = 0. This agrees with the sealed prediction, with Theorem A and with D2.
    48.2 CPU-minutes, peak 2266 MB, one process.
13. **Literature, consistent items** (`literature/literature_check.md`, section 3): the sentence-by-sentence
    comparison of the Ellison description; all compared numbers (rule-90 cycle counts for n = 4..22
    against MOW Table 2, 19 of 19; seed-orbit periods of rules 26 and 122 for n = 4..120 against OEIS, 112
    of 112 each; attractor counts of all 88 classes at L = 17 against Bagnoli et al., 88 of 88); no
    bibliographic error among the entries that could be checked.

## C. Not checked, and why

1. Wuensche and Lesser (1992) and the Wolfram Atlas: not obtained, hosts refused after approval. Whether
   they confirm or contradict cycle counts of the report is open. Jen (1986, 1988): abstracts only.
2. Samuelson (1994), Noeldeke and Samuelson (1993, 1997): primary texts not read; A20 and A21 are
   provisional on that point. Ellison (2000): appendix lemmas and 14 of 29 pages not read.
3. The study's code was not executed (its pipeline writes into existing files). `mech.py`, `ringlang.py`,
   `lightcone.py`, `run_local.py`, `analyze_mechanisms.py`, `factor_search.py` and `code/fw/` were not
   read beyond a few lines. Figures were not opened.
4. Counterexample sweep: 20 of 1496 cases skipped for size (rules 5, 29, 51, 76, 108, 170, 200, 204 at
   n >= 15); n >= 20 not searched. Atlas: 95 of 1327 records not compared.
5. Seed orbits still undetermined after 6e9 steps: rule 22 at n = 242, 243; rule 122 at 13 values of n
   (A8). The return sets of rules 22 and 122 for n <= 256 are open at those n.
6. Structural descriptions in 5.5 (carriers of class 26 and class 37; "half of the single flips start a
   domain of another phase" for classes 43, 142): not checked.
7. Class 154 at n = 22: the dense all-roots computation was not run; the level-wise variant used instead
   equals the dense one in all 1399 sweep cases where both were run, and the result gamma = m - 1 also
   follows directly from the strong connectivity of G1.
8. Per-orbit potentials of the 17 sample cases whose sealed solve took more than 30 CPU-seconds: compared
   by histogram only.
9. Stored one-flip paths of table 5.6 could not be verified because the study stores only their lengths
   (A18); an own search was substituted.
10. For the proofs of Part 2: no literature search was made for the statements D1 and D2 after they were
    proved, and no reader outside this verification has checked them.

---

# Part 2: own attempt (reported separately from Part 1)

## D. New proofs and counterexamples

The study reduces the crystal and zero-state patterns to one statement: every cycle reaches the selected
cycle by one-flip steps (lines 24-25, 479-481, and 7(c): "it requires ... a description of all cycles,
which was not found"). By B6 it suffices to show that every cycle outside the selected rotation orbit A
has a directed path in G1 into A. No counterexample was found for any class. No claim of novelty is made;
the statements below were not found in the sources read, and no search was made for them specifically.

### D1. Class 94, 3 | n, n >= 6 — **proved**

Full text: `part2_94/PROOF_94.md` (no computer-assisted step). Statement: the closed classes of G1 are
exactly the three phases A_1, A_2, A_3 of (011)^(n/3); every other cycle has a directed G1 path into A.
Hence S = A, and k_c = 0 for c in {3, 5, 6}, k_c = 1 otherwise, so k* = 1.

Idea. Rule 94 maps 1 to 0 only between two ones, and 0 to 1 only between unequal neighbours. So an
occurrence of 101 never changes (Lemma 1), and the set W(x) of cells lying in occurrences of 101 only
grows along an orbit and is constant on a cycle. A state with W(x) equal to the whole ring is exactly a
cyclic word over the blocks 01 and 011, and each such word is a fixed point (Lemma 2). If a state is not
fully frozen, flipping a suitable non-frozen cell creates a new 101 (Lemma 3, explicit case analysis), so
every cycle that is not fully frozen has a G1 edge to a cycle with a strictly larger frozen set; after at
most n edges a block word is reached. On block words, 01·011 becomes 011·01 by two one-flip edges through
a 2-cycle (Lemma 4), and 01·01·01 becomes 011·011 by one edge (Lemma 5); in both cases all cells outside a
window of 2 or 3 cells stay frozen, so the relaxation is a finite local computation. With a blocks 01 and
b blocks 011, 2a + 3b = n and 3 | n give 3 | a; sorting by swaps (the number of inversions decreases) and
merging three blocks 01 at a time ends at a = 0, a crystal phase. Lemma 6 shows by the same confinement
argument that every flip of a crystal phase heals in three steps, for every n >= 6; this re-proves the
study's radius statement without the separate computation at n = 6. No description of all cycles is
needed, because Lemma 3 applies to every state.

Checks. The lead read every step and re-tested the lemmas with separate code written from the rule table
(`audit/audit_94.py`, `audit/out/audit_94.json`): Lemmas 1 and 2 on all 32760 states for n = 3..14,
Lemma 3 on 32539 states, Lemma 4 on 965 and Lemma 5 on 730 occurrences for n = 6..18, Lemma 6 on 627 flips
for n = 6..60, and the closed classes at n = 6, 9, 12, 15; no violation. (The first version of the lead's
Lemma 5 test omitted the hypothesis that the third block is short and reported 550 failures; all 550 are
windows the lemma does not cover, and the output file keeps both counts.) The proof track tested each
lemma exhaustively at small n, executed the constructed chain on all 9504 cycles for n = 6..21, and
computed the closed classes of G1 directly up to n = 27 (101407 cycles; the three phases are the only
closed classes), which extends the study's exhaustive range (`part2_94/PROOF_94.md`, section 7).

Not attempted: the direction "3 does not divide n gives k* = 0". Lemmas 1 to 5 hold there too (every cycle
reaches a block word), but which cycles lie in the closed class was not determined.

### D2. Rule 154, all n >= 3 — **proved**

Full text: `part2_154/PROOF_154.md`, sections 1 to 4 (no computer-assisted step). Statements:

* **Theorem 1 (n = 2^k, k >= 2).** Every cycle has a directed G1 path to {0}, of length at most n/2; {0}
  is the only closed class; gamma({0}) = m - 1 and gamma(C) = m for every other cycle; S = {0};
  k_0 = 0 and k_c = 1 for c = 1..7, so k* = 1.
* **Theorem 2 (n >= 3 not a power of two).** G1 is strongly connected, all cycles are selected, k* = 0.
* Hence for rule 154, k* = 1 iff n is a power of two (n >= 4), for all n >= 3. This covers n = 22 (B12)
  and the row P9 of the predictions (n = 24, 28, 32).

Idea. (F x)_i = x_(i+1) + x_(i-1)(1 + x_i) mod 2. The key step is a description of all collisions
(Lemma 5): if F(x) = F(x') with x != x', then n is even and both states are supported on one parity class
of sites (or are the two checkerboards). On an even ring let M be the set of states with a one on an even
site and a one on an odd site. F maps M into M (Lemma 4) and is injective on M by Lemma 5, so F permutes
M: every state of M is periodic (Lemma 6). Therefore a single flip that stays in M moves from one cycle to
another without any transient, in both directions. Given a cycle in M, delete the ones of the minority
parity class one at a time: every intermediate state is in M, hence periodic, so each deletion is a G1
edge or stays on the same cycle; the last deletion leaves a state on one parity class, where rule 154
equals rule 90, which is nilpotent at n = 2^k. This supplies the description of the cycles that the study
says was not found: at n = 2^k the periodic states are exactly M and 0, (2^(n/2) - 1)^2 + 1 in number. For
other even n the rule-90 cycles on one parity class are joined to M in both directions, and for odd n the
map is a bijection, which gives Theorem 2.

Consequences for the study. Lemma 5 is a hand proof of the bijectivity of rule 154 at odd n (the content of
Lemma P for 154, and by A24 for 45). The study's statement "at even n not a power of two all cycles form
one strongly connected G1 [computed for even n <= 20]" holds for all n.

Checks. The lead read every step, re-derived the four local cases of Lemma 5, and tested the statements
with separate code for every n = 3..16 on all states (`audit/audit_154.py`, `audit/out/audit_154.json`):
the formula of Lemma 1; all pairs of states with equal image (257 pairs at n = 16) are of the three kinds
of Lemma 5; F(M) lies in M and every state of M is periodic at every even n; at n = 4, 8, 16 the periodic
states are M and 0 (65026 at n = 16), {0} has no out-edge, every cycle reaches {0}, and the G1 distance
never exceeds the bound of Theorem 1; G1 is strongly connected at n = 6, 10, 12, 14. The sealed sample
shows the potentials of Theorem 1(e) at n = 8 and 16 (m - 1 once, m otherwise) and gamma = m - 1 for all
cycles at n = 20 and 21.

Open for rule 154 (computed only): at n = 2^k all cycle lengths divide n (n = 4, 8, 16; sampled to 1024);
the maximum G1 distance to {0} equals n/2 (n = 4, 8, 16; the upper bound is proved).

### D3. Class 26, the zero state at odd n — **proved**

For rule 26 at odd n the zero state has radius 1, so with Proposition R154, "the zero state cannot be left
by one flip iff n is a power of two" holds for rule 26 at every n >= 3. Proof: f = 1 exactly on the codes
001, 011, 100. F(x) = 0 forces x_(i+1) <= x_(i-1) for all i, hence x constant when n is odd; and 1^n has
no preimage (a code 100 at i forces a code outside the set at i - 1, and codes 0?1 at every site are
contradictory). So no orbit other than that of 1^n reaches 0. Stated in `phase2/FINDINGS_part1.md` (B22),
checked there for odd n = 3..21 and by the seed orbits up to 256; the argument was checked by the lead.

### D4. Class 122 at even n — **attempted; partly proved**

Full text: `part2_154/PROOF_154.md`, section 7.1. Proved (read by the lead, tested there on every even
n <= 256): the only G1 out-neighbour of {0} is the checkerboard 2-cycle CB (Lemma R1); the out-neighbours
of CB are the rotations of one cycle, the limit of CB with one zero flipped (R2); a closed formula for that
orbit up to time n/2 - 1 (R3); and at n = 2^k - 2, k >= 3, that orbit passes through 1^n to 0, so
{ {0}, CB } is a closed class of G1 (R4). By Theorem A, {0} selected implies CB selected at every even n.
**Where it breaks:** that { {0}, CB } is the only closed class at n = 2^k - 2 is computed for n = 6 and 14
and open from n = 30; at the other even n the selection of the checkerboard depends on whether the closed
class reached from that limit cycle leads back to CB, which needs a description of the cycles that was not
found. Computed for even n = 4..26 (own G1 code, no potentials for n = 23..26, so provisional there): one
closed class at every n; CB and {0} are outside it exactly at n = 10 and 18; the guess "n = 2 (mod 8)"
fails at n = 26.

### D5. Class 26 away from powers of two — **attempted; computed only**

Full text: `part2_154/PROOF_154.md`, section 7.2. Proved: the block 111 in F(x) arises only from the block
10011 in x. Computed for n = 4..26 (provisional for n = 23..26 as in D4): one closed class K at every n;
away from powers of two every cycle without 111 belongs to K and the transient cycles are exactly the
111-carriers outside K; a 111-carrier lies in K, i.e. k* = 0, at n = 5, 11, 14, 17, 20, 22, 23, 26. The new
sizes 23 to 26 follow the mod-3 description; n = 22 remains its only exception up to 26. **Where it
breaks:** a one-flip path from K into the carrier (001)^a 00111 for n = 3a + 5 requires knowing K; the
method of D2 does not transfer because rule 26 is not permutive.

### Not attempted in Part 2

Classes 43 and 142 (reachability of the travelling crystal, and its radius beyond n = 400), class 35,
class 37, and the single switches of classes 45 (n = 8) and 73 (n = 9).

### Proposed changes of status in the study, if D1 to D3 are accepted

* Section 7(a): add class 94 (k* = 1 at every 3 | n, n >= 6) and class 154 (k* = 1 iff n = 2^k, all
  n >= 3); remove both from 7(b). For class 26: radius statement for all n.
* Section 7(c), first item: reachability no longer resists for classes 94 and 154; it remains open for
  43, 142, 26 at 2^k, 22 and 122.
* Predictions: the expected proof "radius + reachability" for class 94 and for class 154 is obtained.

---

## Files

| path | content |
|---|---|
| `VERIFICATION_ring_size.md` | this report |
| `verify_ring_size/SAMPLE.md`, `out/`, `logs/`, `core.c`, `eca_core.py`, `solve.py`, `validate.py` | sealed blind sample, solver, validation, batch log (commit a384763) |
| `verify_ring_size/phase2/` | steps 2 to 6: `FINDINGS_part1.md`, scripts, `out/`, `logs/` |
| `verify_ring_size/literature/` | step 7: `literature_check.md`, reading notes on Ellison (2000), comparison tables |
| `verify_ring_size/part2_94/` | D1: `PROOF_94.md`, scripts, `out/` |
| `verify_ring_size/part2_154/` | D2, D4, D5: `PROOF_154.md`, scripts, `out/` |
| `verify_ring_size/audit/` | the lead's re-tests of D1, D2 and of findings A1 to A4, A6 |
| `verify_ring_size/logs/BATCHES.md`, `BATCHES_phase2.md` | expected and measured CPU time and memory of every batch |
