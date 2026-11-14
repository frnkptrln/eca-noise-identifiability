"""Search for block maps Phi of width w <= 4 (Phi: {0,1}^w -> {0,1}, not constant) and radius-1 rules G with
Phi o F_rule = F_G o Phi on every configuration (checked on all windows of length w + 2, which suffices
because both sides depend only on such a window). Writes data/ring_size/factor_search.csv: one row per
(w, G) found, with the number of block maps. A factor onto an additive rule (60, 90, 102, 150, ...) would
have transferred nilpotency at n = 2^k directly.
Usage: python3 factor_search.py [--rule 154]"""
import argparse, csv, itertools, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "ring_size")


def search(rule, w):
    W = list(itertools.product([0, 1], repeat=w + 2))
    Fw = [tuple((rule >> (4 * x[i - 1] + 2 * x[i] + x[i + 1])) & 1 for i in range(1, w + 1)) for x in W]
    idx = lambda t: int("".join(map(str, t)), 2)
    found = {}
    for phi in range(1, (1 << (1 << w)) - 1):
        P = lambda t: (phi >> idx(t)) & 1
        G, ok = {}, True
        for x, fx in zip(W, Fw):
            tri = (P(x[0:w]), P(x[1:w + 1]), P(x[2:w + 2])); out = P(fx)
            if G.setdefault(tri, out) != out:
                ok = False; break
        if ok:
            g = sum(G.get((a, b, c), 0) << (4 * a + 2 * b + c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
            undetermined = 8 - len(G)
            found.setdefault((g, undetermined), 0)
            found[(g, undetermined)] += 1
    return found


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--rule", type=int, default=154); a = ap.parse_args()
    rows = []
    for w in (1, 2, 3, 4):
        for (g, und), cnt in sorted(search(a.rule, w).items()):
            rows.append(dict(rule=a.rule, width=w, target_rule=g, undetermined_codes=und, block_maps=cnt))
    with open(os.path.join(OUT, "factor_search.csv"), "w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=list(rows[0])); wr.writeheader(); wr.writerows(rows)
    print(rows)


if __name__ == "__main__":
    main()
