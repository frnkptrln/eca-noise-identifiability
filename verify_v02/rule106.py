"""Task 5: class 106 at n = 12 from own GTH solves (out/rule106_curve.jsonl, out/route_a_n12_w1.jsonl)."""
import math, json, numpy as np, eca
C = sorted(eca.read_jsonl('out/rule106_curve.jsonl'), key=lambda r: r['eps'])
G = sorted([r for r in eca.read_jsonl('out/route_a_n12_w1.jsonl') if r['rule'] == 106], key=lambda r: -r['eps'])
lam = lambda e: (1 - 2 * e) * math.log((1 - e) / e)
# local maximum: quadratic fit of rho through the grid points 0.009 .. 0.01
pts = [(r['eps'], r['rho']) for r in C if 0.0089 <= r['eps'] <= 0.0101]
x = np.array([p[0] for p in pts]); yv = np.array([p[1] for p in pts])
c2, c1, c0 = np.polyfit(x, yv, 2)
eps_star = -c1 / (2 * c2); rho_star = c0 + c1 * eps_star + c2 * eps_star ** 2
grid_max = max(C, key=lambda r: r['rho'])
# small-noise limit of min_c nu_c
eps = np.array([r['eps'] for r in G]); num = np.array([min(r['nu']) for r in G])
b = (num[-2] - num[-1]) / (eps[-2] - eps[-1]); a = num[-1] - b * eps[-1]
# crossing level: lambda(e) (a + b e) = rho_star, solved in log space
lo, hi = -400.0, -5.0
f = lambda L: lam(10 ** L) * (a + b * 10 ** L) - rho_star if L > -300 else (-L * math.log(10)) * a - rho_star
for _ in range(200):
    mid = (lo + hi) / 2
    if f(mid) > 0: lo = mid
    else: hi = mid
res = dict(grid=[(r['eps'], r['rho'], r['argmin_code']) for r in C], eps_star_fit=eps_star, rho_star_fit=rho_star,
           grid_argmax=(grid_max['eps'], grid_max['rho']), fit_points=len(pts),
           rho_left_neighbour_0p001=[r['rho'] for r in C if r['eps'] == 0.001][0],
           nu_min_small=list(zip(eps.tolist(), num.tolist())), rho_small=[(float(e), lam(e) * v) for e, v in zip(eps, num)],
           a_limit=a, b_linear=b, b_over_a=b / a, log10_crossing=(lo + hi) / 2,
           min_rho_on_small_grid=min(lam(e) * v for e, v in zip(eps, num)),
           k_c_route_b=[r for r in eca.read_jsonl('out/route_b_n12_w1.jsonl') + eca.read_jsonl('out/route_b_n12_w2.jsonl') if r['rule'] == 106][0]['k_c'])
json.dump(res, open('out/rule106_summary.json', 'w'), indent=1)
for k, v in res.items():
    if k != 'grid': print(k, v)
