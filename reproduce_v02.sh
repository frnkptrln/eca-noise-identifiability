#!/usr/bin/env bash
# Proposed v0.2: noise-selected cycles and small-noise orders. Run after reproduce.sh (v0.1, unchanged).
# Worker count: WORKERS (default 2). Approximate wall time at 2 workers on a laptop: about 1.5 h,
# dominated by the GTH stage (10 min) and the sweep at n = 19, 20 (47 min).
# By default everything is recomputed from scratch: the committed sweep checkpoint data/fw_sweep.jsonl and the
# GTH caches in data/cache/ are discarded first (VER-9). REUSE_CHECKPOINTS=1 resumes from them instead.
set -euo pipefail
cd "$(dirname "$0")"
W=${WORKERS:-2}
if [ "${REUSE_CHECKPOINTS:-0}" != "1" ]; then
    rm -f data/fw_sweep.jsonl
    rm -rf data/cache
    echo "from scratch: sweep checkpoint and GTH caches discarded (REUSE_CHECKPOINTS=1 keeps them)"
fi
cd code/fw
python3 make_predictions.py                           # PREDICTIONS.md from v0.1 data (sealed in the first commit)
python3 -m pytest -q test_fw.py > ../../data/log_fw_pytest.txt
python3 verify_stationary.py --nmin 3 --nmax 10 --workers "$W"     # (a) stage A: GTH slopes (cache, data/cache/gth)
python3 verify_orders.py --nmin 3 --nmax 10                        # (a) stage B: compare with the solver
python3 verify_trees.py --workers "$W"                             # (a') exact minimum in-trees on full state graphs
python3 verify_n12.py --gth 106,7,19,23,232,41,200,30,22,108 --workers "$W"   # (b)-(d), GTH at n = 12
python3 verify_n12.py --gth 106 --workers 1 --eps 1e-4,1e-5,1e-6,1e-7,1e-8,1e-9 --out fw_n12_gth_rule106_deep.csv
python3 run_n12.py                                                 # decider at n = 12, certificates
python3 check_cert.py ../../data/fw_certificates_n12/*.json.gz > ../../data/log_fw_check_n12_certs.txt
python3 affine_analysis.py
python3 run_sweep.py --nmin 4 --nmax 20 --workers "$W" --cert-nmax 14   # resumable (data/fw_sweep.jsonl)
python3 check_cert.py ../../data/fw_certificates_sweep/*.json.gz > ../../data/log_fw_check_sweep_certs.txt
python3 wall_estimate.py
python3 make_report.py                                             # report.md, note/numbers_v02.tex, table, certificate READMEs
cd ../..
diff -u note/note.tex note/note_v0.2.tex > note/note_v0.2.diff || true
code/fw/make_manifest.sh
python3 code/fw/make_report.py                                     # second pass: manifest count (ManifestFilesVtwo)
echo "done: report.md, note/note_v0.2.tex"
