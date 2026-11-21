"""run_all.py -- runs T00 to T11 one after the other with the parameters used for VERIFICATION_paper.md and writes
out/run_all.txt (exit code, wall time and CPU time of each test; the CPU time includes the C program, which uses at
most 2 threads). At most 2 threads are busy at any time. Nothing is written outside this folder and the system's
temporary directory.

Usage (from the root of the repository):   python3 verify_paper/run_all.py [path of paper/] [tests, e.g. T11 or T03,T05]
With a list of tests only these are run, and their lines replace the old ones in out/run_all.txt.
Needs: Python 3 with numpy and scipy, and a C compiler reachable as `cc`.
"""
import os, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "paper")
RUNS = [
    ("T00_engine.py", []),
    ("T01_section2.py", ["12"]),
    ("T02_rule154_lemmas.py", ["22", "16"]),
    ("T03_rule154_theorems.py", ["20"]),
    ("T04_rule94_lemmas.py", []),
    ("T05_rule94_theorem.py", ["21"]),
    ("T06_rules43_142.py", ["16", "18", "13"]),
    ("T07_rule26.py", ["18", "20", "40"]),
    ("T08_table1.py", [PAPER, "20", "20"]),
    ("T09_section6.py", [PAPER, "16", "20", "24"]),
    ("T10_mutation.py", [PAPER]),
    ("T11_certificates.py", ["18", "21", "18", "20"]),
]
ONLY = sys.argv[2].split(",") if len(sys.argv) > 2 else None
head = "test,exit_code,wall_s,cpu_s_including_C_program"
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
old = {}
fn_all = os.path.join(HERE, "out", "run_all.txt")
if ONLY and os.path.exists(fn_all):
    for l in open(fn_all).read().splitlines():
        if l.startswith("T") and "," in l:
            old[l.split(",")[0]] = l
results = dict(old)
def write(final=False):
    lines = [head] + [results[sc] for sc, _ in RUNS if sc in results]
    if final:
        ok = len(lines) - 1 == len(RUNS) and all(l.split(",")[1] == "0" for l in lines[1:])
        lines.append("ALL PASS" if ok else ("SOME TEST FAILED" if any(l.split(",")[1] != "0" for l in lines[1:]) else "NOT ALL TESTS RUN"))
    open(fn_all, "w").write("\n".join(lines) + "\n")
    return lines
for script, args in RUNS:
    if ONLY and script[:3] not in ONLY:
        continue
    t = os.times(); w = time.time()
    with open(os.path.join(HERE, "out", script[:3] + "_stdout.txt"), "w") as fh:
        rc = subprocess.call([sys.executable, os.path.join(HERE, script)] + args, stdout=fh, stderr=subprocess.STDOUT)
    t2 = os.times()
    cpu = (t2.children_user - t.children_user) + (t2.children_system - t.children_system)
    results[script] = "%s,%d,%.1f,%.1f" % (script, rc, time.time() - w, cpu)
    print(results[script], flush=True)
    write()
lines = write(final=True)
print(lines[-1])
sys.exit(0 if lines[-1] == "ALL PASS" else 1)
