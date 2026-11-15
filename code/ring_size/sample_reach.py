"""Sampled test of one-flip reachability on rings too large to enumerate (n > 22).

No enumeration of the 2^n states: cycles are reached from random initial states (seeded), a cycle is
identified by its canonical label (smallest state over the cycle and all rotations), and its one-flip
successors are computed exactly by flipping every cell of every state of the cycle and following the
deterministic orbit to its cycle. From each sampled cycle a best-first search over one-flip edges
looks for a path to the target set (the zero state, or the rotation orbit of a crystal); the heuristic
only orders the search, every edge found is exact.

What a run establishes (tag "observed" in the report): for each sampled cycle, either an explicit
one-flip path into the target (a certificate that this cycle is not in a closed class other than the
target's), or "not found within the budget". It does not establish anything about unsampled cycles.

Cycles are handled up to rotation: `cycle_label` names a rotation orbit of cycles, and the column
`distinct rotation orbits` of the report counts these labels. The path found is stored in the column
`path` as steps "state:cell>label" joined by ";": `state` (hexadecimal, cell i at bit i) is a state of a
cycle of the current rotation orbit, `cell` the flipped cell, `label` (hexadecimal) the rotation orbit of
the cycle reached. Since F commutes with rotations, rotating the later steps turns the stored chain into
a one-flip path between actual cycles. Every stored path is re-verified step by step before it is
written (verify_path): the state is periodic, lies in the orbit named by the previous step, and its flip
ends in the orbit named by this step; the last label is the target's.

Usage: python3 sample_reach.py --rule 154 --n 32 --target zero --samples 200 --seed 1 --out ...csv
       python3 sample_reach.py --rule 94 --n 24 --target crystal:011 ...
"""
import argparse, csv, heapq, os, random, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from lightcone import step, from_word


def rot(x, n, k):
    k %= n
    return ((x << k) | (x >> (n - k))) & ((1 << n) - 1) if k else x


def limit(rule, x, n, cap=10 ** 6):
    """States of the cycle reached from x (list, in orbit order)."""
    seen = {}
    t = 0
    while x not in seen:
        seen[x] = t
        x = step(rule, x, n); t += 1
        if t > cap:
            raise RuntimeError("orbit cap exceeded")
    cyc = [x]; y = step(rule, x, n)
    while y != x:
        cyc.append(y); y = step(rule, y, n)
    return cyc


def canon_label(cyc, n):
    return min(min(rot(s, n, k) for k in range(n)) for s in cyc)


STATE_LABEL = {}      # cycle state -> canonical label (memo over the whole run)
CYCLES = {}           # canonical label -> one cycle (list of states) with that label


def register(cyc, n):
    lab = canon_label(cyc, n)
    for s in cyc:
        STATE_LABEL[s] = lab
    CYCLES.setdefault(lab, cyc)
    return lab


def label_of(rule, x, n, cap=10 ** 6):
    """Canonical label of the cycle reached from x; stops at the first known cycle state."""
    seen = {}
    t = 0
    while x not in STATE_LABEL:
        if x in seen:                       # new cycle closed
            cyc = [x]; y = step(rule, x, n)
            while y != x:
                cyc.append(y); y = step(rule, y, n)
            return register(cyc, n)
        seen[x] = t
        x = step(rule, x, n); t += 1
        if t > cap:
            raise RuntimeError("orbit cap exceeded")
    return STATE_LABEL[x]


def successors(rule, cyc, n):
    """{label: (state index, cell)} of the cycles reachable with one flip (excluding the cycle itself)."""
    own = register(cyc, n)
    out = {}
    for si, s in enumerate(cyc):
        for i in range(n):
            lab = label_of(rule, s ^ (1 << i), n)
            if lab != own and lab not in out:
                out[lab] = (si, i, CYCLES[lab])
    return out


def verify_path(rule, n, start_label, path, tlab):
    """Exact re-check of a stored path [(state, cell, label), ...] from the orbit start_label to the orbit tlab."""
    cur = start_label
    for x, i, lab in path:
        cyc = limit(rule, x, n)
        assert x in cyc, "path state is not periodic"
        assert canon_label(cyc, n) == cur, "path state is not in the current rotation orbit"
        assert canon_label(limit(rule, x ^ (1 << i), n), n) == lab, "flip does not end in the stated orbit"
        cur = lab
    assert cur == tlab, "path does not end in the target orbit"
    return True


def popmean(cyc):
    return sum(bin(s).count("1") for s in cyc) / len(cyc)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rule", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--target", required=True)          # zero | crystal:<word>
    ap.add_argument("--samples", type=int, default=100)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--budget", type=int, default=400)   # cycles expanded per sample
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rule, n = a.rule, a.n
    if a.target == "zero":
        assert step(rule, 0, n) == 0
        target_cyc = [0]
    else:
        word = a.target.split(":")[1]
        target_cyc = limit(rule, from_word(word, n), n)
    tlab = canon_label(target_cyc, n)
    tstates = set(target_cyc)
    # radius of the target: one flip of each target state; >= 2 iff every flip returns to the target orbit
    # (for a crystal: to the same cycle, not only the same rotation orbit)
    t0 = time.time()
    rad2 = True
    for s in target_cyc:
        for i in range(n):
            c2 = limit(rule, s ^ (1 << i), n)
            if not (set(c2) & tstates):
                rad2 = False
    def h(cyc):
        if a.target == "zero":
            return popmean(cyc)
        return min(bin(s ^ t).count("1") for s in cyc[:8] for t in target_cyc)
    rng = random.Random(a.seed)
    rows = []
    cache = {}
    for k in range(a.samples):
        x0 = rng.getrandbits(n)
        cyc = limit(rule, x0, n)
        lab = canon_label(cyc, n)
        if lab == tlab:
            rows.append(dict(sample=k, x0=x0, cycle_label=lab, period=len(cyc), found=1, path_len=0, expanded=0, path=""))
            continue
        # best-first search over one-flip edges; cache[l] = {l2: (flipped state, cell, a cycle of orbit l2)}
        pq = [(h(cyc), 0, lab)]
        info = {lab: (cyc, 0, None)}          # label -> (cycle, depth, (parent label, state, cell))
        found, expanded = False, 0
        while pq and expanded < a.budget:
            _, d, l = heapq.heappop(pq)
            c = info[l][0]
            if l not in cache:
                cache[l] = {l2: (c[v[0]], v[1], v[2]) for l2, v in successors(rule, c, n).items()}
            expanded += 1
            if tlab in cache[l]:
                found = True; plen = d + 1
                x, i, _ = cache[l][tlab]
                path = [(x, i, tlab)]
                while info[l][2] is not None:
                    pl, px, pi = info[l][2]
                    path.append((px, pi, l)); l = pl
                path.reverse()
                break
            for l2, (x, i, c2) in cache[l].items():
                if l2 not in info:
                    info[l2] = (c2, d + 1, (l, x, i))
                    heapq.heappush(pq, (h(c2), d + 1, l2))
        if found:
            assert len(path) == plen and verify_path(rule, n, lab, path, tlab)
        rows.append(dict(sample=k, x0=x0, cycle_label=lab, period=len(cyc), found=int(found),
                         path_len=plen if found else -1, expanded=expanded,
                         path=";".join(f"{x:x}:{i}>{l2:x}" for x, i, l2 in path) if found else ""))
    with open(a.out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["rule", "n", "target", "target_radius_ge2", "sample", "x0", "cycle_label",
                                            "period", "found", "path_len", "expanded", "path"])
        w.writeheader()
        for r in rows:
            w.writerow(dict(rule=rule, n=n, target=a.target, target_radius_ge2=int(rad2), **r))
    nf = sum(r["found"] for r in rows)
    print(f"rule {rule} n {n} target {a.target}: radius>=2 {rad2}; {nf}/{len(rows)} sampled cycles reach the "
          f"target by one-flip steps (all stored paths re-verified); distinct rotation orbits {len(set(r['cycle_label'] for r in rows))}; "
          f"{time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
