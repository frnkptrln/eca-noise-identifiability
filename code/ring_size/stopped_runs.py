"""Write data/ring_size/stopped_runs.csv: jobs of this study that were stopped before they finished.

The one such job is class 154 at n = 22 (run_mech.py --nmin 22 --nmax 22 --rules 154 --workers 1). Its
start is the creation time of data/ring_size/log_mech_154_n22.txt and its stop was noted by hand; the
job wrote no record and no CPU time. The interval during which the machine was asleep is taken from the
verification (verify_ring_size/phase2/out/cost_claim.json, read from the system power log), which also
gives the upper bound on the time the job can have run. An earlier version of this file called the job
"stopped above the stated cap" of 5 h; that compared wall time including sleep with a cap that no script
defined (finding A4 of VERIFICATION_ring_size.md).
"""
import csv, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verif

OUT = os.path.join(HERE, "..", "..", "data", "ring_size")
JOBS = [dict(rule=154, n=22, workers=1, stopped_local="2026-11-14 08:09")]     # noted by hand when the job was stopped


def main():
    c = verif.cost_claim()
    j = c["job_154_n22"]
    rows = []
    for job in JOBS:
        (s0, s1), = j["asleep_intervals_within_job"]
        rows.append(dict(rule=job["rule"], n=job["n"], workers=job["workers"],
                         started_local=j["start_log_birth"][:16], stopped_local=job["stopped_local"],
                         wall_hours=round(j["elapsed_hours_upper"], 1),
                         asleep_from=s0[11:16], asleep_to=s1[11:16],
                         asleep_hours=j["asleep_hours_within_job"],
                         awake_hours_upper=j["awake_hours_upper_bound"],
                         cpu_hours="not recorded",
                         outcome="stopped unfinished; no record written",
                         source_of_sleep_interval=verif.COST_CLAIM))
    with open(os.path.join(OUT, "stopped_runs.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print("stopped_runs.csv:", rows)


if __name__ == "__main__":
    main()
