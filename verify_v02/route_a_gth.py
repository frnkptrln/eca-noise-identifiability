"""Route (a) at n = 12: stationary law by own GTH elimination (float64) at given eps values.
Usage: python route_a_gth.py OUTFILE n rule1,rule2,... eps1,eps2,...
Writes one JSON line per (rule, eps) with nu_c, rho, min pi and the componentwise relative residual."""
import sys, time, math
import numpy as np
import eca, gth

out, n = sys.argv[1], int(sys.argv[2])
rules = [int(r) for r in sys.argv[3].split(',')]
epss = [float(e) for e in sys.argv[4].split(',')]
done = {(r['rule'], r['eps']) for r in eca.read_jsonl(out)}
N = 1 << n
pc = eca.popcount(np.arange(N, dtype=np.uint32))
Nc = eca.code_counts(n).astype(np.float64)
y = np.arange(N, dtype=np.uint32)
for rule in rules:
    F = eca.step_map(rule, n)
    D = pc[F[:, None] ^ y[None, :]]
    for eps in epss:
        if (rule, eps) in done:
            continue
        t0 = time.time()
        pw = np.array([eps ** d * (1 - eps) ** (n - d) for d in range(n + 1)])
        P = pw[D]
        pi = gth.gth_numeric(P)
        res = np.abs(pi @ P - pi) / pi
        nu = Nc @ pi
        lam = (1 - 2 * eps) * math.log((1 - eps) / eps)
        eca.append_jsonl(out, dict(rule=rule, n=n, eps=eps, nu=[float(v) for v in nu],
                                   rho=float(lam * nu.min()), argmin_code=int(nu.argmin()),
                                   min_pi=float(pi.min()), max_rel_resid=float(res.max()),
                                   sec=round(time.time() - t0, 2)))
