#!/bin/sh
# Ring-size study (branch ring-size-mechanisms): regenerate data/ring_size, figures/ring_size and
# report_ring_size.md from scratch. At most 2 worker processes. Wall time on a laptop (Apple silicon):
# verifier ~6 min; mechanisms n = 8..20 ~10 min; n = 21, 22 without class 154 at 22 ~51 min;
# local results ~1 min; sampled tests ~4.5 CPU-min (paths are stored and re-verified);
# atlas (all 88 classes, n = 4..20) ~1 h. Checkpoints are append-only (resumable).
# Costs are wall times of the first run; run_mech.py now records CPU time per job as well, and a cost cap,
# where one is stated, refers to CPU time (the machine may sleep).
# Inputs from the independent verification (verify_ring_size/, kept in this branch) are read by
# check_predictions.py, stopped_runs.py and make_report.py through verif.py: class 154 at n = 22, seed
# orbits settled beyond the cut-off of run_local.py, the sleep interval of the stopped job, the sealed
# statements outside the outcome table.
set -e
cd "$(dirname "$0")/code/ring_size"
python3 -m pytest -q test_ring_size.py | tee ../../data/ring_size/log_pytest.txt
python3 verify_mech.py --nmin 4 --nmax 8 --rules all --out ../../data/ring_size/verify_mech_n4_8_all.csv
python3 verify_mech.py --nmin 9 --nmax 10 --rules switching --out ../../data/ring_size/verify_mech_n9_10_switching.csv
python3 run_mech.py --nmin 8 --nmax 20 --workers 2
python3 run_mech.py --nmin 21 --nmax 22 --rules 22,26,35,37,43,45,60,73,90,94,122,142 --workers 2
python3 run_mech.py --nmin 21 --nmax 21 --rules 154 --workers 1
# class 154 at n = 22 is not run here. A first attempt was stopped unfinished; the machine was asleep for
# most of its 7.4 h of wall time, so it ran for at most about 1.3 h and its CPU time was not recorded
# (data/ring_size/stopped_runs.csv, written by stopped_runs.py). The verification computed the case with
# its own solver in 48 CPU-minutes: k* = 0 (verify_ring_size/phase2/out/v154_n22.json). To run it here:
# python3 run_mech.py --nmin 22 --nmax 22 --rules 154 --workers 1
python3 stopped_runs.py
python3 run_local.py
python3 factor_search.py
D=../../data/ring_size/sampled_reach; mkdir -p $D; : > $D/log_sampled.txt
for a in "154 32 zero" "154 24 zero" "154 28 zero" "26 32 zero" "22 30 zero" "22 31 zero" "22 32 zero" "122 31 zero" \
         "94 24 crystal:011" "94 27 crystal:011" "94 30 crystal:011" "43 24 crystal:0011" "43 28 crystal:0011" \
         "43 32 crystal:0011" "142 24 crystal:0011" "142 28 crystal:0011" "142 32 crystal:0011"; do
  set -- $a; python3 sample_reach.py --rule $1 --n $2 --target $3 --samples 200 --seed 1 --out $D/rule$1_n$2.csv | tee -a $D/log_sampled.txt
done
SW=22,26,35,37,43,45,60,73,90,94,122,142,154
OTHERS=$(python3 -c "import sys; sys.path.insert(0,'../fw'); import fwlib; sw={22,26,35,37,43,45,60,73,90,94,122,142,154}; print(','.join(str(r) for r in fwlib.class_reps() if r not in sw))")
python3 run_mech.py --rules $SW --nmin 4 --nmax 7 --workers 1 --selected-only --out ../../data/ring_size/atlas --tag _atlas
python3 run_mech.py --rules $OTHERS --nmin 4 --nmax 20 --workers 1 --selected-only --out ../../data/ring_size/atlas --tag _atlas
gzip -c -9 ../../data/ring_size/atlas/mech_atlas.jsonl > ../../data/ring_size/atlas/mech_atlas.jsonl.gz
python3 analyze_mechanisms.py
python3 check_predictions.py
python3 figures_ring_size.py
python3 make_report.py --literature literature_section.md --ellison ellison_remark.md
cd ../../data/ring_size && find . -type f ! -name MANIFEST.sha256 ! -name mech_atlas.jsonl ! -name .DS_Store | sort | xargs shasum -a 256 > MANIFEST.sha256
