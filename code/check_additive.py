"""Stage A: exact structural facts about the rules whose rate curves coincide
(nu_c = n/8 for every code): bijectivity and affinity of the global map, and, for the
affine non-bijective rules, the Walsh-basis argument for uniform three-cell marginals.

For an affine map F(x) = Lx + b over GF(2), the stationary law satisfies, in the Walsh basis,
    pi^(chi) = (1-2eps)^{|chi|} (-1)^{chi.b} pi^(L^T chi),
so pi^(chi) = 0 unless some power of L^T annihilates chi (generalised kernel).  The three-cell
marginal at (i-1, i, i+1) is uniform iff pi^(chi) = 0 for every nonzero chi supported there.
The script counts, for each affine rule, the nonzero characters supported on three adjacent
cells that lie in the generalised kernel of L^T.  Writes data/additive_rules.csv.
"""
import sys, os, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca_noise as E


def main(out="data"):
    n = E.N
    codes = E.neighborhood_codes()
    rows = []
    for rule in range(256):
        succ = E.successor_map(rule, codes=codes)
        bijective = len(set(succ.tolist())) == E.S
        f0 = int(succ[0])
        # affine iff F(x xor y) = F(x) xor F(y) xor F(0) for all x, y; it suffices to check the basis
        L = np.zeros((n, n), dtype=np.int64)
        for i in range(n):
            col = int(succ[1 << i]) ^ f0
            L[:, i] = [(col >> j) & 1 for j in range(n)]
        xs = np.arange(E.S)
        bits = ((xs[:, None] >> np.arange(n)) & 1)
        pred = (bits @ L.T) % 2
        pred_int = (pred << np.arange(n)).sum(axis=1) ^ f0
        affine = bool(np.array_equal(pred_int, succ))
        if not affine:
            continue
        LT = L.T % 2
        n_bad = 0
        for i in range(n):
            for mask in range(1, 8):
                chi = np.zeros(n, dtype=np.int64)
                for k, b in enumerate([(mask >> 2) & 1, (mask >> 1) & 1, mask & 1]):
                    if b:
                        chi[(i - 1 + k) % n] = 1
                v = chi.copy()
                for _ in range(n + 1):
                    if not v.any():
                        n_bad += 1; break
                    v = (LT @ v) % 2
        rank = int(np.linalg.matrix_rank(L.astype(float)))   # rank over the reals is an upper bound only; GF(2) rank below
        # GF(2) rank by elimination
        M = L.copy() % 2; r = 0
        for c in range(n):
            piv = next((k for k in range(r, n) if M[k, c]), None)
            if piv is None: continue
            M[[r, piv]] = M[[piv, r]]
            for k in range(n):
                if k != r and M[k, c]: M[k] ^= M[r]
            r += 1
        rows.append(dict(rule=rule, bijective=int(bijective), affine=1, gf2_rank=r, kernel_dim=n - r,
                         bad_characters=n_bad, f0=f0))
        print(rule, rows[-1], flush=True)
    with open(os.path.join(out, "additive_rules.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
