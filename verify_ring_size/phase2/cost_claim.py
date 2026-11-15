"""Step 6: evidence on the claim 'Class 154 at n = 22 was stopped after 7.4 h, above the stated cap of 5 h'.
Reads the study's logs and cost files, file birth/modification times, and the system power log (pmset -g log,
Sleep / Wake entries only).  Writes out/cost_claim.json and out/pmset_sleep_wake.txt."""
import csv
import json
import os
import re
import subprocess
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
D = os.path.join(REPO, "data", "ring_size")
OUT = os.path.join(HERE, "out")
fmt = "%Y-%m-%d %H:%M:%S"


def times(p):
    s = os.stat(p)
    return {"birth": time.strftime(fmt, time.localtime(s.st_birthtime)), "mtime": time.strftime(fmt, time.localtime(s.st_mtime)),
            "size": s.st_size}


res = {"timezone": time.strftime("%Z %z")}
res["stopped_runs_csv"] = list(csv.DictReader(open(os.path.join(D, "stopped_runs.csv"))))
res["stopped_runs_csv_columns"] = list(res["stopped_runs_csv"][0].keys())
res["log_mech_154_n22_txt"] = open(os.path.join(D, "log_mech_154_n22.txt")).read()
res["file_times"] = {f: times(os.path.join(D, f)) for f in
                     ["log_mech_154_n22.txt", "mech.jsonl", "mech_cost.csv", "stopped_runs.csv", "log_mech_n21_22.txt",
                      "log_mech_n8_20.txt", "factor_search.csv"]}
# CPU-time fields anywhere?
mech_first = json.loads(open(os.path.join(D, "mech.jsonl")).readline())
res["mech_jsonl_cost_fields"] = sorted(k for k in mech_first if k.startswith("cost"))
src = open(os.path.join(REPO, "code", "ring_size", "run_mech.py")).read()
res["run_mech_cost_seconds_definition"] = [l.strip() for l in src.split("\n") if "cost_seconds" in l or "t0 = time.time()" in l][:4]
res["run_mech_has_cap_or_timeout_option"] = bool(re.search(r"add_argument\(\"--(cap|timeout|max-hours|max-rss-gb)", src))
res["run_mech_docstring_mentions_max_rss_gb"] = "--max-rss-gb" in src
res["cap_mentions"] = {}
for f in ["reproduce_ring_size.sh", "PREDICTIONS_ring_size.md", "report_ring_size.md", "PR_DRAFT.md", "code/ring_size/run_mech.py",
          "code/ring_size/make_report.py", "code/ring_size/report_template.md"]:
    txt = open(os.path.join(REPO, f)).read().split("\n")
    res["cap_mentions"][f] = [[i + 1, l.strip()[:200]] for i, l in enumerate(txt) if re.search(r"\bcap\b|cap of|5 h\b|7\.4|2-3 h", l)]
# the study's time for class 154 at even n (wall seconds per job, 2 workers in parallel for n <= 20)
mc = [r for r in csv.DictReader(open(os.path.join(D, "mech_cost.csv"))) if r["rule"] == "154"]
res["mech_cost_154"] = [[int(r["n"]), int(r["cycles"]), float(r["cost_seconds"]), float(r["cost_maxrss_mb"])] for r in mc]
ev = {int(r["n"]): float(r["cost_seconds"]) for r in mc if int(r["n"]) % 2 == 0}
res["ratio_cost_154_n20_over_n18"] = round(ev[20] / ev[18], 2)
res["extrapolated_wall_seconds_154_n22_same_ratio"] = round(ev[20] * ev[20] / ev[18], 0)
# time-command lines of the n = 21, 22 batch: wall versus CPU
log = open(os.path.join(D, "log_mech_n21_22.txt")).read()
res["batch_n21_22_time_lines"] = re.findall(r"^(real|user|sys)\s+(\S+)", log, flags=re.M)[:3]
tot = sum(float(r["cost_seconds"]) for r in csv.DictReader(open(os.path.join(D, "mech_cost.csv"))))
res["sum_cost_seconds_hours"] = round(tot / 3600, 2)
# power log
try:
    pm = subprocess.run(["pmset", "-g", "log"], capture_output=True, text=True, timeout=120).stdout.split("\n")
except Exception as e:           # not available: keep the result explicit
    pm = []
    res["pmset_error"] = repr(e)
keep = []
for l in pm:
    mt = re.match(r"^(2026-11-1[34] \d\d:\d\d:\d\d) \+0100 ([A-Za-z ]+?)\s*\t(.*)$", l)
    if mt and mt.group(2) in ("Sleep", "Wake", "DarkWake") and "2026-11-13 22" <= mt.group(1) <= "2026-11-14 10":
        keep.append("%s +0100 %-8s %s" % (mt.group(1), mt.group(2), mt.group(3)[:110].strip()))
open(os.path.join(OUT, "pmset_sleep_wake.txt"), "w").write("\n".join(keep) + "\n")
res["pmset_sleep_wake_lines"] = keep
start = datetime.strptime(res["file_times"]["log_mech_154_n22.txt"]["birth"], fmt)
stop = datetime.strptime(res["stopped_runs_csv"][0]["stopped_cet"] + ":59", fmt)      # stated to the minute
ev_list = [(datetime.strptime(l[:19], fmt), l[26:34].strip()) for l in keep]
asleep = 0.0
sleep_at = None
intervals = []
for t, kind in ev_list:
    if kind == "Sleep" and sleep_at is None:
        sleep_at = t
    elif kind in ("Wake", "DarkWake") and sleep_at is not None:
        a, b = max(sleep_at, start), min(t, stop)
        if b > a:
            asleep += (b - a).total_seconds()
            intervals.append([a.strftime(fmt), b.strftime(fmt)])
        sleep_at = None
elapsed = (stop - start).total_seconds()
res["job_154_n22"] = {"start_log_birth": start.strftime(fmt), "stop_upper_bound": stop.strftime(fmt),
                      "elapsed_hours_upper": round(elapsed / 3600, 2), "asleep_intervals_within_job": intervals,
                      "asleep_hours_within_job": round(asleep / 3600, 2),
                      "awake_hours_upper_bound": round((elapsed - asleep) / 3600, 2),
                      "awake_minutes_upper_bound": round((elapsed - asleep) / 60, 1),
                      "cap_hours_in_stopped_runs_csv": float(res["stopped_runs_csv"][0]["cap_hours"]),
                      "wall_hours_in_stopped_runs_csv": float(res["stopped_runs_csv"][0]["wall_hours"])}
json.dump(res, open(os.path.join(OUT, "cost_claim.json"), "w"), indent=1)
print(json.dumps({k: res[k] for k in ["job_154_n22", "pmset_sleep_wake_lines", "mech_cost_154", "ratio_cost_154_n20_over_n18",
                                      "extrapolated_wall_seconds_154_n22_same_ratio", "batch_n21_22_time_lines",
                                      "sum_cost_seconds_hours", "run_mech_cost_seconds_definition",
                                      "run_mech_has_cap_or_timeout_option", "mech_jsonl_cost_fields"]}, indent=0))
print(json.dumps(res["cap_mentions"], indent=0)[:1800])
