"""Predicted small-noise orders of the stationary law for every state, from a classify() result.

ord pi_eps(x) = min_C [gamma(C) + R(C -> x)] - min_C gamma(C), with R(C -> x) taken from the BFS of the
rotation representative of C: R(rot^k C_rep -> x) = R(C_rep -> rot^-k x)."""
import numpy as np
import fwlib


def state_orders(res):
    cs = res["cs"]; n = cs.n
    x = np.arange(1 << n, dtype=np.int64)
    best = np.full(1 << n, 10 ** 9, dtype=np.int64)
    for j in range(cs.m):
        r = int(res["rep"][j]); k = int(res["shift"][j])
        d = res["dists"][r].astype(np.int64)
        dj = d[fwlib.rotate(x, n, -k)]
        best = np.minimum(best, res["gamma"][j] + dj)
    return best - res["gmin"]
