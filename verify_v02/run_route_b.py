"""Usage: python run_route_b.py OUTFILE n rule1,rule2,... [validate]
Route (b) orders per class; with 'validate' also the full 2^n-state tropical GTH and a state-by-state comparison."""
import sys, time, resource
import numpy as np
import eca, route_b

out, n = sys.argv[1], int(sys.argv[2])
rules = [int(r) for r in sys.argv[3].split(',')]
validate = len(sys.argv) > 4 and sys.argv[4] == 'validate'
done = {r['rule'] for r in eca.read_jsonl(out)}
Nc = eca.code_counts(n)
for rule in rules:
    if rule in done:
        continue
    t0 = time.time()
    res, h, V = route_b.orders_route_b(rule, n, Nc, return_states=True)
    res['sec'] = round(time.time() - t0, 2)
    if len(res['cycle_orders']) > 2000:  # keep the line small; the full vectors are not needed downstream
        res['cycle_orders_hist'] = np.bincount(res['cycle_orders']).tolist()
        for key in ('cycle_orders', 'cycle_lengths', 'cycle_min_state'):
            res.pop(key)
    if validate:
        t1 = time.time()
        hf = route_b.full_tropical_orders(rule, n)
        res['full_tropical_equal_all_states'] = bool(np.array_equal(h, hf))
        res['k_c_full'] = [int(hf[Nc[c] > 0].min()) for c in range(8)]
        res['sec_full'] = round(time.time() - t1, 2)
    res['maxrss_MB'] = round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**20, 1)
    eca.append_jsonl(out, res)
