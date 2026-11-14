"""Run a list of (rule, n) cases with a fixed number of worker processes; append-only checkpoint.

Usage: python run_batch.py NAME [--workers 2] [--mcap M] RULE:N [RULE:N ...]
Each case runs `solve.py RULE N` in its own process (so peak memory is per case) and its JSON line is
appended to out/sample.jsonl by this driver (single writer).  Cases already present are skipped, so a
restart resumes.  Per-case log lines go to logs/batch_NAME.log, totals to logs/batch_NAME_measured.json.
"""
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "sample.jsonl")


def done_cases():
    d = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            if line.strip():
                r = json.loads(line)
                d.add((r["rule"], r["n"]))
    return d


def run_one(rule, n, mcap):
    cmd = [sys.executable, os.path.join(HERE, "solve.py"), str(rule), str(n)]
    if mcap:
        cmd += ["--mcap", str(mcap)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    return rule, n, p.returncode, p.stdout, p.stderr


def main():
    name = sys.argv[1]
    args = sys.argv[2:]
    workers, mcap = 2, None
    cases = []
    i = 0
    while i < len(args):
        if args[i] == "--workers":
            workers = int(args[i + 1]); i += 2
        elif args[i] == "--mcap":
            mcap = int(args[i + 1]); i += 2
        else:
            r, n = args[i].split(":"); cases.append((int(r), int(n))); i += 1
    assert workers <= 2, "load budget: at most 2 worker processes"
    done = done_cases()
    todo = [c for c in cases if c not in done]
    todo.sort(key=lambda c: (c[1], c[0]))
    log = open(os.path.join(HERE, "logs", "batch_%s.log" % name), "a")
    log.write("# start %s: %d cases requested, %d already done, workers=%d\n" % (time.strftime("%Y-%m-%d %H:%M:%S"), len(cases), len(cases) - len(todo), workers))
    log.flush()
    cpu, peak, nok, failed = 0.0, 0.0, 0, []
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(run_one, r, n, mcap) for r, n in todo]
        for f in as_completed(futs):
            rule, n, rc, out, err = f.result()
            if rc != 0:
                failed.append("%d:%d" % (rule, n))
                log.write("FAIL rule=%d n=%d rc=%d %s\n" % (rule, n, rc, err.strip().splitlines()[-1] if err.strip() else ""))
                log.flush()
                continue
            rec = json.loads(out)
            with open(OUT, "a") as fh:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
            cpu += rec["cpu_seconds"]; peak = max(peak, rec["peak_rss_mb"]); nok += 1
            log.write("ok rule=%d n=%d cycles=%d method=%s cpu=%.1fs rss=%.0fMB checks=%s\n" % (
                rule, n, rec["n_cycles"], rec["method"], rec["cpu_seconds"], rec["peak_rss_mb"], rec["checks_all_true"]))
            log.flush()
    meas = {"batch": name, "cases_run": nok, "cases_failed": failed, "cpu_seconds_sum": round(cpu, 1),
            "peak_rss_mb_max_single_case": peak, "finished": time.strftime("%Y-%m-%d %H:%M:%S")}
    json.dump(meas, open(os.path.join(HERE, "logs", "batch_%s_measured.json" % name), "w"), indent=1)
    log.write("# end %s\n" % json.dumps(meas))
    log.close()
    print(json.dumps(meas))


if __name__ == "__main__":
    main()
