"""Step 5: recount of the sealed predictions (PREDICTIONS_ring_size.md as of commit 8d68e54).
Every part is enumerated here from the sealed text, decided (a) from own data and (b) from the study's data files,
and matched to the row of data/ring_size/predictions_outcome.csv that covers it (or 'omitted').
Writes out/predictions_recount.json and out/predictions_recount.csv."""
import csv
import glob
import gzip
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
OUT = os.path.join(HERE, "out")
D = os.path.join(REPO, "data", "ring_size")
RULES = [22, 26, 35, 37, 43, 45, 60, 73, 90, 94, 122, 142, 154]


def is_rot(p, w):
    n = len(p)
    return n % len(w) == 0 and p in ((w * (n // len(w))) * 2)


class Own:
    name = "own"

    def __init__(self):
        self.s = {(r["rule"], r["n"]): r for r in map(json.loads, open(os.path.join(ROOT, "out", "sample.jsonl")))}
        self.seed = {(int(r["rule"]), int(r["n"])): r for r in csv.DictReader(open(os.path.join(OUT, "seed_orbits_own.csv")))}
        self.pg = {int(r["rule"]): r for r in csv.DictReader(open(os.path.join(OUT, "pairgraph_all256.csv")))}
        self.sr = json.load(open(os.path.join(OUT, "sampled_reach_check.json")))
        p = os.path.join(OUT, "v154_n22.json")
        self.v154 = json.load(open(p)) if os.path.exists(p) else None
        self._o = {}

    def has(self, rule, n):
        return (rule, n) in self.s or (rule == 154 and n == 22 and self.v154 is not None and self.v154.get("kstar") is not None)

    def kstar(self, rule, n):
        if (rule, n) in self.s:
            return self.s[(rule, n)]["kstar"]
        if rule == 154 and n == 22 and self.v154 is not None:
            return self.v154.get("kstar")
        return None

    def ncyc(self, rule, n):
        return self.s[(rule, n)]["n_cycles"]

    def nsel(self, rule, n):
        return self.s[(rule, n)]["selected"]["n_cycles"]

    def missing(self, rule, n):
        return self.s[(rule, n)]["codes_missing"]

    def closed(self, rule, n):
        return self.s[(rule, n)]["g1"]["n_closed_classes"]

    def sccs(self, rule, n):
        return self.s[(rule, n)]["g1"]["n_scc"]

    def bij(self, rule, n):
        return self.s[(rule, n)]["bijective"]

    def orbits(self, rule, n):
        if (rule, n) not in self._o:
            sel = self.s[(rule, n)]["selected"]
            if sel["orbits_complete"]:
                reps = {o["rep"] for o in sel["orbits"]}
            else:
                reps = {r["rep"] for r in csv.DictReader(open(os.path.join(ROOT, "out", "selected", "sel_r%d_n%d.tsv" % (rule, n))), delimiter="\t")}
            rows = []
            for r in csv.DictReader(open(os.path.join(OUT, "own_orbits", "orb_r%d_n%d.csv" % (rule, n)))):
                rows.append(dict(pattern=r["rep"], T=int(r["temporal_period"]), S=int(r["spatial_period"]), codes=r["codes"],
                                 radius=int(r["radius"]), selected=r["rep"] in reps, size=int(r["orbit_size"])))
            self._o[(rule, n)] = rows
        return self._o[(rule, n)]

    def seed_returns(self, rule, n):
        r = self.seed[(rule, n)]
        return None if r["returns_to_zero"] == "" else int(r["returns_to_zero"])

    def certified(self, rule):
        return int(self.pg[rule]["certified_bijective_odd_n"]) == 1

    def sampled(self, rule, n):
        t = self.sr["files"].get("rule%d_n%d.csv" % (rule, n))
        return None if t is None else (t["own_paths_found"], t["sampled"])


class Study:
    name = "study"

    def __init__(self):
        self.m = {(int(r["rule"]), int(r["n"])): r for r in csv.DictReader(open(os.path.join(D, "mechanisms.csv")))}
        self.o = defaultdict(list)
        with gzip.open(os.path.join(D, "cycle_orbits.csv.gz"), "rt") as fh:
            for r in csv.DictReader(fh):
                self.o[(int(r["rule"]), int(r["n"]))].append(
                    dict(pattern=r["pattern"], T=int(r["temporal_period"]), S=int(r["spatial_period"]), codes=r["codes"],
                         radius=int(r["radius"]), selected=r["selected"] == "True", size=int(r["orbit_size"])))
        self.seed = {(int(r["rule"]), int(r["n"])): r for r in csv.DictReader(open(os.path.join(D, "seed_orbits.csv")))}
        self.inj = {int(r["rule"]): r for r in csv.DictReader(open(os.path.join(D, "injectivity.csv")))}

    def has(self, rule, n):
        return (rule, n) in self.m

    def kstar(self, rule, n):
        return int(self.m[(rule, n)]["kstar"]) if (rule, n) in self.m else None

    def ncyc(self, rule, n):
        return int(self.m[(rule, n)]["cycles"])

    def nsel(self, rule, n):
        return int(self.m[(rule, n)]["n_selected"])

    def missing(self, rule, n):
        return [c for c in range(8) if str(c) not in self.m[(rule, n)]["selected_cover"]]

    def closed(self, rule, n):
        return int(float(self.m[(rule, n)]["g1_closed"]))

    def sccs(self, rule, n):
        return int(float(self.m[(rule, n)]["g1_sccs"]))

    def bij(self, rule, n):
        return int(self.m[(rule, n)]["bijective"]) == 1

    def orbits(self, rule, n):
        return self.o[(rule, n)]

    def seed_returns(self, rule, n):
        r = self.seed[(rule, n)]
        return None if int(r["capped"]) == 1 else int(float(r["returns_to_zero"]))

    def certified(self, rule):
        return int(self.inj[rule]["certified_bijective_odd_n"]) == 1

    def sampled(self, rule, n):
        p = os.path.join(D, "sampled_reach", "rule%d_n%d.csv" % (rule, n))
        if not os.path.exists(p):
            return None
        rows = list(csv.DictReader(open(p)))
        return (sum(int(r["found"]) for r in rows), len(rows))


def zero_orbit(B, rule, n):
    return [o for o in B.orbits(rule, n) if set(o["pattern"]) == {"0"}][0]


def hf(ok):
    return "holds" if ok else "fails"


NS = range(8, 23)
parts = []      # (id, sealed fragment, test(B) -> (outcome, detail), study rows (id, substring) or None, basis)


def P(pid, text, fn, row=None, basis="data"):
    parts.append((pid, text, fn, row, basis))


def sel(B, rule, n):
    return [o for o in B.orbits(rule, n) if o["selected"]]


# ---------------- P1
n3 = [n for n in NS if n % 3 == 0]
P("P1a", "94, 3|n: selected set is exactly the 3 shifts of (011)^{n/3}",
  lambda B: (hf(all(len(sel(B, 94, n)) == 1 and sel(B, 94, n)[0]["size"] == 3 and is_rot(sel(B, 94, n)[0]["pattern"], "011") for n in n3)), "n = %s" % n3),
  ("P1", "selected set"))
P("P1b", "94, 3|n: its radius is 2", lambda B: (hf(all(sel(B, 94, n)[0]["radius"] == 2 for n in n3)), ""), ("P1", "radius of the crystal"))
P("P1c", "94, 3|n: every other cycle has radius 1",
  lambda B: (hf(all(o["radius"] == 1 for n in n3 for o in B.orbits(94, n) if not o["selected"])), ""), ("P1", "radius of the crystal"))
P("P1d", "94, 3|n: the one-flip graph has a single closed class, the crystal orbit",
  lambda B: (hf(all(B.closed(94, n) == 1 for n in n3)), "closed classes: %s" % sorted({B.closed(94, n) for n in n3})), ("P1", "single closed class"))
P("P1e", "94, 3 does not divide n: no cycle avoids all of codes 0, 1, 2, 4, 7",
  lambda B: (hf(not any(set(o["codes"]) <= set("356") for n in NS if n % 3 for o in B.orbits(94, n))), ""), ("P1", "no cycle avoids"))
# ---------------- P2
n4 = [n for n in NS if n % 4 == 0]
for r in (43, 142):
    P("P2a_%d" % r, "%d, 4|n: selected set is exactly the rotation orbit of the travelling wave (0011)^{n/4}, one cycle of temporal period 4" % r,
      lambda B, r=r: (hf(all(len(sel(B, r, n)) == 1 and sel(B, r, n)[0]["size"] == 1 and sel(B, r, n)[0]["T"] == 4
                             and is_rot(sel(B, r, n)[0]["pattern"], "0011") for n in n4)), "n = %s" % n4), ("P2", "class %d" % r))
    P("P2b_%d" % r, "%d, 4|n: radius 2" % r, lambda B, r=r: (hf(all(sel(B, r, n)[0]["radius"] == 2 for n in n4)), ""), ("P2", "class %d" % r))
    P("P2c_%d" % r, "%d, 4|n: all other cycles radius 1" % r,
      lambda B, r=r: (hf(all(o["radius"] == 1 for n in n4 for o in B.orbits(r, n) if not o["selected"])), ""), ("P2", "class %d" % r))
    P("P2d_%d" % r, "%d, 4|n: single closed class" % r, lambda B, r=r: (hf(all(B.closed(r, n) == 1 for n in n4)), ""), ("P2", "class %d" % r))
P("P2e", "43, 142, 4 does not divide n: no cycle has spatial period 4",
  lambda B: ("holds (trivially)" if not any(o["S"] == 4 for r in (43, 142) for n in NS if n % 4 for o in B.orbits(r, n)) else "fails",
             "the spatial period divides n"), ("P2", "no cycle with spatial period 4"))
# ---------------- P3
P("P3a", "35, 3|n: the cycles that contain code 5 are exactly the cycles that are not selected",
  lambda B: (hf(all(("5" in o["codes"]) == (not o["selected"]) for n in n3 for o in B.orbits(35, n))), ""), ("P3", "cycles containing code 5"))
P("P3a2", "35: 11 of 12 cycles selected at n = 9, 700 of 710 at n = 18",
  lambda B: (hf((B.nsel(35, 9), B.ncyc(35, 9), B.nsel(35, 18), B.ncyc(35, 18)) == (11, 12, 700, 710)),
             "selected/cycles: %d/%d at n = 9, %d/%d at n = 18" % (B.nsel(35, 9), B.ncyc(35, 9), B.nsel(35, 18), B.ncyc(35, 18))), None)
P("P3b", "35, 3|n: each of them has spatial period 3 or consists of 3-periodic segments",
  lambda B: (hf(all(o["S"] == 3 for n in n3 for o in B.orbits(35, n) if "5" in o["codes"])),
             "spatial periods of the code-5 cycles: %s; they are words over the blocks 10 and 100 (out/compare_derived.json); "
             "'3-periodic segments' is not a mechanical test: the 100-blocks are, the 10-blocks are not"
             % sorted({o["S"] for n in n3 for o in B.orbits(35, n) if "5" in o["codes"]})), ("P3", "spatial period 3"))
P("P3c", "35: crystal capture is falsified (already known)",
  lambda B: (hf(all(len(sel(B, 35, n)) > 1 for n in n3)), "more than one selected orbit at every 3|n"), None)
# ---------------- P4
P("P4a", "122, 4|n: some noise-selected cycle has spatial period 4 and carries code 2",
  lambda B: (hf(all(any(o["S"] == 4 and "2" in o["codes"] for o in sel(B, 122, n)) for n in n4)),
             "selected carriers of code 2 have spatial periods %s" % sorted({o["S"] for n in n4 for o in sel(B, 122, n) if "2" in o["codes"]})),
  ("P4", "spatial period 4 carries code 2"))
l4 = [9, 10, 11, 13, 17, 18, 19]
P("P4b", "122: the missing code is 2 for n in {9, 10, 11, 13, 17, 18, 19}",
  lambda B: (hf(all(B.missing(122, n) == [2] for n in l4)), "missing codes: %s" % sorted({tuple(B.missing(122, n)) for n in l4})),
  ("P4", "missing code is 2"))
P("P4c", "122, n = 14: the selected cycles are the uniform states",
  lambda B: (hf(all(o["S"] == 1 for o in sel(B, 122, 14))), "selected: %s" % [o["pattern"] for o in sel(B, 122, 14)]),
  ("P4", "n = 14"))
P("P4c2", "122, n = 14: codes 0, 2, 5", lambda B: (hf(B.missing(122, 14) == [1, 3, 4, 6, 7]), ""), None)
P("P4d", "122, n = 15: the selected cycles are the uniform states, code 0",
  lambda B: (hf([o["pattern"] for o in sel(B, 122, 15)] == ["0" * 15] and B.missing(122, 15) == [1, 2, 3, 4, 5, 6, 7]), ""), ("P4", "n = 15"))
P("P4e14", "122, n = 14: mechanism = zero state with radius >= 2",
  lambda B: (hf(zero_orbit(B, 122, 14)["radius"] >= 2), "radius of the zero state: %d" % zero_orbit(B, 122, 14)["radius"]), ("P4", "n = 14"))
P("P4e15", "122, n = 15: mechanism = zero state with radius >= 2",
  lambda B: (hf(zero_orbit(B, 122, 15)["radius"] >= 2), "radius of the zero state: %d" % zero_orbit(B, 122, 15)["radius"]), ("P4", "n = 15"))
# ---------------- P5
def ev154(B):
    return [n for n in (10, 12, 14, 18, 20) if B.has(154, n)]
P("P5a", "154, even n not a power of two (n <= 20): every cycle has radius 1",
  lambda B: (hf(all(o["radius"] == 1 for n in ev154(B) for o in B.orbits(154, n))), "n = %s" % ev154(B)), ("P5", "even n not a power of 2"))
P("P5b", "154, even n not a power of two (n <= 20): the one-flip graph is strongly connected (all cycles selected)",
  lambda B: (hf(all(B.sccs(154, n) == 1 and B.nsel(154, n) == B.ncyc(154, n) for n in ev154(B))), ""), ("P5", "even n not a power of 2"))
P("P5c", "154, n = 8, 16: the zero state has radius 2, every other cycle radius 1, {0} is the single closed class",
  lambda B: (hf(all(zero_orbit(B, 154, n)["radius"] == 2 and all(o["radius"] == 1 for o in B.orbits(154, n) if set(o["pattern"]) != {"0"})
                    and B.closed(154, n) == 1 and [o["pattern"] for o in sel(B, 154, n)] == ["0" * n] for n in (8, 16))), ""), ("P5", "n = 8, 16"))
# ---------------- P6
P("P6a", "22: k* = 1 exactly where the zero state has radius >= 2, i.e. where the single-flip orbit of 0 returns to 0 (n = 8..20; here 8..22)",
  lambda B: (hf(all((B.kstar(22, n) == 1) == bool(B.seed_returns(22, n)) == (zero_orbit(B, 22, n)["radius"] >= 2) for n in NS)),
             "k* = 1 at n = %s" % [n for n in NS if B.kstar(22, n) == 1]), ("P6", "22: k* = 1 exactly"))
P("P6b", "26, n = 16: the same holds (k* = 2, zero state alone)",
  lambda B: (hf(B.kstar(26, 16) == 2 and [o["pattern"] for o in sel(B, 26, 16)] == ["0" * 16] and B.seed_returns(26, 16) == 1), ""), ("P6", "26, n = 16"))
def p6c(B):
    ns = [n for n in NS if B.kstar(26, n) == 1]
    bad = [n for n in ns if B.missing(26, n) != [7]]
    return (hf(not bad), "n with k* = 1: %s; n among them where the missing codes are not exactly {7}: %s%s"
            % (ns, bad, "".join(" (n = %d: zero state selected alone, codes %s missing)" % (n, B.missing(26, n)) for n in bad)))
P("P6c", "26: at the other n with k* = 1 the missing code is 7 (111), with a different mechanism", p6c, ("P6", "26, other n"))
# ---------------- P7
P("P7a", "45, n = 8: the 2-cycle of the uniform states is selected alone",
  lambda B: (hf(len(sel(B, 45, 8)) == 1 and set(sel(B, 45, 8)[0]["pattern"]) <= {"0"} and sel(B, 45, 8)[0]["T"] == 2 and B.nsel(45, 8) == 1), ""), ("P7", "n = 8"))
P("P7b", "45, odd n: F_45 is bijective (k* = 0)",
  lambda B: (hf(B.certified(45) and all(B.bij(45, n) and B.kstar(45, n) == 0 for n in NS if n % 2)), "pair-graph certificate and n = 9..21"), ("P7", "odd n"))
P("P7c", "45, even n >= 10: the uniform 2-cycle has radius 1",
  lambda B: (hf(all(zero_orbit(B, 45, n)["radius"] == 1 for n in NS if n % 2 == 0 and n >= 10)), ""), ("P7", "even n"))
# ---------------- P8
P("P8a", "37, 73: no crystal of a fixed period explains the switches", lambda B: ("not a testable statement", ""), None, "reading")
P("P8b", "37: k* = 0 iff n mod 6 in {0, 5} (n = 8..20; here 8..22)",
  lambda B: (hf(all((B.kstar(37, n) == 0) == (n % 6 in (0, 5)) for n in NS)), ""), ("P8", "37:"))
P("P8c", "73: the only switch for n >= 8 is n = 9", lambda B: (hf([n for n in NS if B.kstar(73, n) >= 1] == [9]), ""), ("P8", "73:"))
P("P8d", "73, n = 9: code 7 missing", lambda B: (hf(B.missing(73, 9) == [7]), ""), None)
# ---------------- k* at 21, 22
pred = {35: (1, 0), 94: (1, 0), 43: (0, 0), 142: (0, 0), 122: (1, 1), 60: (0, 0), 90: (0, 0), 154: (0, 0), 45: (0, 0), 73: (0, 0), 37: (1, 1)}
for r, ks in pred.items():
    for n, k in zip((21, 22), ks):
        P("K_%d_%d" % (r, n), "class %d, n = %d: k* = %d" % (r, n, k),
          lambda B, r=r, n=n, k=k: (("not tested", "no record") if B.kstar(r, n) is None else (hf(B.kstar(r, n) == k), "computed k* = %d" % B.kstar(r, n))),
          ("k*(21,22)", "class %d, n = %d:" % (r, n)))
for n in (21, 22):
    P("K_22_%d" % n, "class 22, n = %d: k* = 1 iff the single-flip orbit of 0 returns to 0" % n,
      lambda B, n=n: (hf((B.kstar(22, n) == 1) == bool(B.seed_returns(22, n))), "k* = %d, seed returns = %s" % (B.kstar(22, n), B.seed_returns(22, n))),
      ("k*(21,22)", "class 22, n = %d" % n))
# ---------------- P9
P("P9a32", "154, n = 32: the zero state has radius >= 2", lambda B: (hf(B.seed_returns(154, 32) == 1), "seed orbit returns"), ("P9", "zero radius"))
P("P9a64", "154, n = 64: the zero state has radius >= 2", lambda B: (hf(B.seed_returns(154, 64) == 1), "seed orbit returns"), None)
P("P9b32", "154, n = 32: every cycle reached from sampled initial states reaches the zero state by one-flip steps",
  lambda B: (("holds (observed, sampled)" if B.sampled(154, 32)[0] == B.sampled(154, 32)[1] else "fails"), "%d of %d samples" % B.sampled(154, 32)), ("P9", "sampled cycles"))
P("P9b64", "154, n = 64: the same sampled test", lambda B: (("not tested", "no sample at n = 64") if B.sampled(154, 64) is None else ("?", "")), None)
P("P9c", "154: k* = 1 at n = 32", lambda B: ("not tested", "k* not computed"), ("P9", "k* = 1 at n = 32"))
P("P9d", "154: k* = 0 at n = 24", lambda B: ("not tested", "k* not computed"), ("P9", "k* = 1 at n = 32"))
P("P9e", "154: k* = 0 at n = 28", lambda B: ("not tested", "k* not computed"), ("P9", "k* = 1 at n = 32"))
# ---------------- general statements and proof expectations (decided by reading the report; same for both columns)
R = "reading"
P("G1", "closure (Lemma 1): expected proved", lambda B: ("holds", "Lemma 1, proof complete; 0 counterexamples in out/sweep88_summary.json"), None, R)
P("G2", "two-level criterion (Lemma B): expected proved", lambda B: ("holds", "Lemma B, proof complete; 0 counterexamples in out/sweep88_summary.json"), None, R)
P("G3", "incommensurability: expected proved by a finite machine-checked certificate for every class where it applies",
  lambda B: ("fails", "the tool exists (ringlang.avoid_graph, tested against brute force) but neither the report nor data/ring_size contains such a "
                      "certificate; 'no cycle of class 94 within codes {3,5,6} at 3 does not divide n' is tagged [computed n <= 22] only"), None, R)
P("T94_dir0", "94: direction 0 (3 does not divide n gives k* = 0): proof for all n expected (G3 + G1)",
  lambda B: ("fails", "report 5.1: 'A proof for all n would need the closed classes of G1 for all n; not found'"), None, R)
P("T94_radius", "94: radius of the crystal = 2: proof expected", lambda B: ("holds", "Lemma H with tau = 3, n >= 6"), None, R)
P("T94_reach", "94: reachability: expected 'explained, not proved'", lambda B: ("holds", "report 7(b)"), None, R)
for r in (43, 142):
    P("T%d_dir0" % r, "%d: as for 94: direction 0 proof expected" % r, lambda B: ("fails", "not proved (report 5.1)"), None, R)
    P("T%d_radius" % r, "%d: as for 94: radius proof expected" % r, lambda B: ("fails", "Lemma H does not apply; radius only computed up to n = 400 (report 5.1)"), None, R)
    P("T%d_reach" % r, "%d: as for 94: reachability 'explained, not proved'" % r, lambda B: ("holds", "report 7(b)"), None, R)
P("T142_codes", "rules 43 and 142 agree on codes 1, 3, 4, 6 and differ exactly on the four codes the crystal misses",
  lambda B: (hf([c for c in range(8) if ((43 >> c) & 1) == ((142 >> c) & 1)] == [1, 3, 4, 6]), "rule tables"), None)
P("T35_missing5", "35: the missing code at 3|n is 5", lambda B: (hf(all(B.missing(35, n) == [5] for n in n3)), ""), None)
P("T35_radius", "35, 3|n: the cycles carrying 101 have radius 1 and are not selected",
  lambda B: (hf(all(o["radius"] == 1 and not o["selected"] for n in n3 for o in B.orbits(35, n) if "5" in o["codes"])), ""), None)
P("T35_other", "35, 3 does not divide n: cycles carrying 101 are selected",
  lambda B: (hf(all(any("5" in o["codes"] for o in sel(B, 35, n)) for n in NS if n % 3)), ""), None)
P("T122_4notdiv", "122: at 4 does not divide n code 010 is missing from the selected cycles (n = 14 is excepted by P4 itself)",
  lambda B: (hf(all(2 in B.missing(122, n) for n in NS if n % 4 and n != 14)),
             "code 2 not missing at n = %s" % [n for n in NS if n % 4 and n != 14 and 2 not in B.missing(122, n)]),
  ("k*(21,22)", "class 122, n = 22:"))
P("T154_identity", "rule 154 = rule 90 XOR (l AND c); equal to rule 90 on configurations without two adjacent ones",
  lambda B: (hf(all(((154 >> (4 * a + 2 * b + c)) & 1) == ((a ^ c) ^ (a & b)) for a in (0, 1) for b in (0, 1) for c in (0, 1))), "rule tables"), None)
P("T154_radius_proof", "154: radius part proved for all n = 2^k", lambda B: ("holds", "Proposition R154"), None, R)
P("T154_odd_proof", "154: odd n bijective, k* = 0, proof expected", lambda B: ("holds", "Lemma P"), None, R)
P("T154_even_left", "154: the zero state can be left with one flip at even n that are not powers of two",
  lambda B: (hf(all(zero_orbit(B, 154, n)["radius"] == 1 for n in ev154(B))), "n = %s; for all even n by Proposition R154" % ev154(B)), None)
P("T154_reach_2k", "154: at n = 2^k every other cycle reaches 0 by one-flip steps, so 0 is selected alone (computed range n = 8, 16)",
  lambda B: (hf(all([o["pattern"] for o in sel(B, 154, n)] == ["0" * n] and B.closed(154, n) == 1 for n in (8, 16))), ""), None)
P("T154_even_k0", "154: even n not a power of two: k* = 0 expected",
  lambda B: (hf(all(B.kstar(154, n) == 0 for n in (10, 12, 14, 18, 20, 22) if B.kstar(154, n) is not None)),
             "n = %s" % [n for n in (10, 12, 14, 18, 20, 22) if B.kstar(154, n) is not None]), None)

study_rows = list(csv.DictReader(open(os.path.join(D, "predictions_outcome.csv"))))
own, study = Own(), Study()
out = []
used_rows = set()
for pid, text, fn, row, basis in parts:
    o1, d1 = fn(own)
    try:
        o2, d2 = fn(study)
    except Exception as e:           # the study's files cannot decide this part
        o2, d2 = "not decidable from the study's files", type(e).__name__
    rep = "omitted"
    if row is not None:
        cand = [i for i, r in enumerate(study_rows) if r["id"] == row[0] and row[1] in r["part"]]
        assert len(cand) == 1, (pid, row, cand)
        used_rows.add(cand[0])
        rep = study_rows[cand[0]]["outcome"]
        rep_part = study_rows[cand[0]]["part"]
    else:
        rep_part = ""
    out.append({"id": pid, "sealed_part": text, "basis": basis, "own_outcome": o1, "own_detail": d1,
                "study_data_outcome": o2, "study_data_detail": d2, "study_reported_outcome": rep, "study_row": rep_part,
                "differs_from_study_report": (rep != "omitted" and rep != o1)})
# counts
def cnt(key, rows):
    return dict(Counter(r[key] for r in rows))
core = [r for r in out if r["study_reported_outcome"] != "omitted"]
# outcome per study row, from own data: a row holds iff all of its sealed parts hold
by_row = defaultdict(list)
for r in out:
    if r["study_reported_outcome"] != "omitted":
        by_row[r["study_row"]].append(r)
row_own = {}
for k, rs in by_row.items():
    oc = [r["own_outcome"] for r in rs]
    if any(o == "fails" for o in oc):
        row_own[k] = "fails"
    elif all(o == "not tested" for o in oc):
        row_own[k] = "not tested"
    elif len(set(oc)) == 1:
        row_own[k] = oc[0]
    else:
        row_own[k] = "holds"
res = {
    "sealed_file_changed_after_sealing": subprocess.run(["git", "-C", REPO, "diff", "--stat", "8d68e54", "ring-size-mechanisms", "--", "PREDICTIONS_ring_size.md"],
                                                        capture_output=True, text=True).stdout.strip() != "",
    "sealed_file_equals_working_tree": subprocess.run(["git", "-C", REPO, "show", "8d68e54:PREDICTIONS_ring_size.md"], capture_output=True, text=True).stdout
                                       == open(os.path.join(REPO, "PREDICTIONS_ring_size.md")).read(),
    "study_table_rows": len(study_rows), "study_table_counts": dict(Counter(r["outcome"] for r in study_rows)),
    "study_rows_covered_by_own_parts": len(used_rows),
    "own_parts_total": len(out),
    "own_counts_all_parts": cnt("own_outcome", out),
    "study_data_counts_all_parts": cnt("study_data_outcome", out),
    "own_counts_on_study_rows": dict(Counter(row_own.values())),
    "study_rows_judged_differently": [{"row": k, "study": by_row[k][0]["study_reported_outcome"], "own": v,
                                       "parts": [[r["id"], r["own_outcome"], r["own_detail"]] for r in by_row[k]]}
                                      for k, v in row_own.items() if v != by_row[k][0]["study_reported_outcome"]],
    "parts_omitted_by_study_table": [[r["id"], r["sealed_part"], r["own_outcome"]] for r in out if r["study_reported_outcome"] == "omitted"],
    "omitted_counts": cnt("own_outcome", [r for r in out if r["study_reported_outcome"] == "omitted"]),
    "own_vs_study_data_disagreements": [[r["id"], r["own_outcome"], r["study_data_outcome"]] for r in out if r["own_outcome"] != r["study_data_outcome"]],
    "parts": out}
json.dump(res, open(os.path.join(OUT, "predictions_recount.json"), "w"), indent=1)
with open(os.path.join(OUT, "predictions_recount.csv"), "w", newline="") as fh:
    w = csv.DictWriter(fh, list(out[0]))
    w.writeheader()
    w.writerows(out)
print(json.dumps({k: v for k, v in res.items() if k != "parts"}, indent=0))
