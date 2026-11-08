"""Append-only, fsynced JSON-lines checkpoints. A resumed run skips records whose key is present;
final tables are written from the checkpoint sorted by key, so they do not depend on the order
in which records were produced or on interruptions.

BUG-2 (fixed): a kill during a write leaves a torn last line without a newline; the next append then
landed on the same line and both records were lost. load() now truncates a torn tail (and fsyncs)
before anything is appended, and append() refuses to write after a missing newline."""
import json, os


def _repair(path):
    with open(path, "rb+") as fh:
        data = fh.read()
        if data and not data.endswith(b"\n"):
            cut = data.rfind(b"\n") + 1          # 0 if no complete line at all
            fh.truncate(cut)
            fh.flush(); os.fsync(fh.fileno())


def load(path):
    recs = {}
    if os.path.exists(path):
        _repair(path)
        with open(path) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    r = json.loads(line)           # after repair every line is complete
                    recs[tuple(r["key"])] = r
    return recs


def append(path, rec):
    line = json.dumps(rec, sort_keys=True, separators=(",", ":")) + "\n"
    if os.path.exists(path) and os.path.getsize(path):
        with open(path, "rb") as fh:
            fh.seek(-1, os.SEEK_END)
            assert fh.read(1) == b"\n", "checkpoint has a torn tail; call load() first"
    with open(path, "a") as fh:
        fh.write(line)
        fh.flush()
        os.fsync(fh.fileno())
