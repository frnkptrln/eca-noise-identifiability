"""Step 5: did the sealing of PREDICTIONS_ring_size.md precede the computations?  Commit dates and file birth /
modification times of the study's files.  Writes out/seal_timing.json."""
import json
import os
import subprocess
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
fmt = "%Y-%m-%d %H:%M:%S"


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout.strip()


seal = git("log", "-1", "--format=%cd", "--date=format:" + fmt, "8d68e54")
res = {"seal_commit": "8d68e54", "seal_commit_time_local": seal,
       "commits": git("log", "--format=%h | %ad | %s", "--date=format:" + fmt, "2ef9d00..ring-size-mechanisms").split("\n"),
       "files_in_seal_commit": git("show", "--stat", "--format=", "8d68e54").split("\n"),
       "predictions_file_changed_since_seal": git("diff", "--stat", "8d68e54", "ring-size-mechanisms", "--", "PREDICTIONS_ring_size.md") != ""}
rows = []
for top in ["data/ring_size", "code/ring_size", "figures/ring_size", "data/cache"]:
    for dp, dn, fn in os.walk(os.path.join(REPO, top)):
        for f in fn + [""]:
            p = os.path.join(dp, f) if f else dp
            if "__pycache__" in p or ".pytest_cache" in p or p.endswith(".DS_Store"):
                continue
            s = os.stat(p)
            rows.append((time.strftime(fmt, time.localtime(s.st_birthtime)), time.strftime(fmt, time.localtime(s.st_mtime)),
                         os.path.relpath(p, REPO)))
rows.sort()
ring = [r for r in rows if not r[2].startswith("data/cache")]
cache = [r for r in rows if r[2].startswith("data/cache")]
res["ring_size_files_and_folders"] = len(ring)
res["ring_size_earliest_births"] = [list(r) for r in ring[:8]]
res["ring_size_born_before_seal"] = [list(r) for r in ring if r[0] < seal]
res["ring_size_modified_before_seal"] = [list(r) for r in ring if r[1] < seal]
res["data_cache_entries"] = len(cache)                    # untracked cache of the earlier versions (v0.1 / v0.2)
res["data_cache_latest_birth"] = max(r[0] for r in cache) if cache else None
res["data_cache_latest_mtime"] = max(r[1] for r in cache) if cache else None
res["data_cache_born_on_or_after_2026-11-13"] = [list(r) for r in cache if r[0] >= "2026-11-13"][:20]
s = os.stat(os.path.join(REPO, "PREDICTIONS_ring_size.md"))
res["predictions_file_birth"] = time.strftime(fmt, time.localtime(s.st_birthtime))
res["predictions_file_mtime"] = time.strftime(fmt, time.localtime(s.st_mtime))
json.dump(res, open(os.path.join(HERE, "out", "seal_timing.json"), "w"), indent=1)
print(json.dumps(res, indent=0)[:3500])
