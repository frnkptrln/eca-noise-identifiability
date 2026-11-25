"""Sweep: python sweep.py BND NMIN NMAX RULESET CAP OUTCSV [EXACT_BIJ_NMAX]
RULESET: all | nullreps | ringreps | comma list.  CAP: exact potentials if m <= CAP, else one-flip graph only."""
import sys, os, time, csv
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, vb
from multiprocessing import Pool

def rules_of(spec):
    if spec == 'all': return list(range(256))
    if spec == 'nullreps': return sorted({min(r, vb.refl_rule(r)) for r in range(256)})
    if spec == 'ringreps':
        return sorted({min(r, vb.refl_rule(r), vb.comp_rule(r), vb.refl_rule(vb.comp_rule(r))) for r in range(256)})
    return [int(x) for x in spec.split(',')]

def mstr(mask): return ''.join(str(c) for c in range(8) if (mask >> c) & 1)

def job(args):
    bnd, n, r, cap, bijmax = args
    t0 = time.time()
    s = vb.Sys(r, n, bnd)
    rec = dict(bnd=bnd, n=n, rule=r, m=s.m, bij=int(s.bijective), union=mstr(s.union_mask), btype=int(s.union_mask != 255))
    cl = s.closed_classes()
    rec['n_closed'] = len(cl)
    rec['closed_cover'] = '|'.join(mstr(int(np.bitwise_or.reduce(s.cycle_mask[K]))) for K in cl)
    rec['closed_sizes'] = '|'.join(str(len(K)) for K in cl)
    exact = (not s.bijective or n <= bijmax) and s.m <= cap
    if exact:
        V, R = s.resist(); g = vb.gammas(V); gmin = int(g.min()); sel = np.flatnonzero(g == gmin)
        kc = (g[:, None] + R).min(axis=0) - gmin
        cover = int(np.bitwise_or.reduce(s.cycle_mask[sel]))
        rec.update(exact=1, gmin=gmin, nsel=len(sel), cover=mstr(cover), missed=mstr(255 & ~cover),
                   kc='-'.join(map(str, kc)), kstar=int(kc.max()),
                   sel_eq_closed=int(sorted(sel.tolist()) == sorted(np.concatenate(cl).tolist())),
                   sel_min_states='|'.join(str(int(np.flatnonzero((s.cyc == c) & (s.per == 1)).min())) for c in sel[:20]))
    else:
        rec.update(exact=0)
        if s.bijective:   # proved: uniform law stationary, k* = 0 since every code occurs (n >= 3)
            rec.update(nsel=s.m, cover=rec['union'], missed=mstr(255 & ~s.union_mask), kstar=0 if s.union_mask == 255 else '')
        elif len(cl) == 1:  # Theorem A (checked against potentials below the cap)
            K = cl[0]; cover = int(np.bitwise_or.reduce(s.cycle_mask[K]))
            rec.update(gmin=s.m - 1, nsel=len(K), cover=mstr(cover), missed=mstr(255 & ~cover),
                       kstar=('0' if cover == 255 else '>=1'))
    rec['sec'] = round(time.time() - t0, 3)
    return rec

FIELDS = ['bnd','n','rule','m','bij','union','btype','n_closed','closed_sizes','closed_cover','exact','gmin','nsel','cover','missed','kc','kstar','sel_eq_closed','sel_min_states','sec']
if __name__ == '__main__':
    bnd, nmin, nmax, spec, cap, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], int(sys.argv[5]), sys.argv[6]
    bijmax = int(sys.argv[7]) if len(sys.argv) > 7 else 8
    jobs = [(bnd, n, r, cap, bijmax) for n in range(nmin, nmax + 1) for r in rules_of(spec)]
    t0 = time.time()
    with Pool(2) as p, open(outp, 'w', newline='') as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader()
        for rec in p.imap(job, jobs, chunksize=4):
            w.writerow(rec)
    print(len(jobs), 'records', round(time.time() - t0, 1), 's ->', outp)
