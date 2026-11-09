"""Draw the sealed sample. Inputs: class representatives and out/cycle_counts_n17_n20.jsonl only."""
import json, numpy as np, eca
SEED = 20261109
reps = eca.class_reps()
fixed12 = [7, 19, 22, 23, 30, 41, 106, 108, 200, 232]
rest = [r for r in reps if r not in fixed12]
draw12 = sorted(int(x) for x in np.random.default_rng(SEED).choice(rest, 10, replace=False))
CAP = 20000  # cycles per class: tropical GTH on m cycles is O(m^3) time, 2 x 8 m^2 bytes RAM
cc = {(r['n'], r['rule']): r['m_cycles'] for r in eca.read_jsonl('out/cycle_counts_n17_n20.jsonl')}
def maxclass(n):
    ok = [(cc[(n, r)], -r) for r in reps if cc[(n, r)] <= CAP]
    m, negr = max(ok)
    return -negr, m
max17, m17 = maxclass(17)
max20, m20 = maxclass(20)
pool = [r for r in reps if cc[(20, r)] <= CAP and cc[(17, r)] <= CAP and r not in (max17, max20)]
draw_big = sorted(int(x) for x in np.random.default_rng(SEED + 1720).choice(pool, 4, replace=False))
sample = dict(seed=SEED, seed_big=SEED + 1720, cap_cycles=CAP,
              n4=reps, n5=reps, n12_fixed=fixed12, n12_drawn=draw12,
              n17=draw_big + [max17], n17_maxcycle_class=max17, n17_maxcycle_m=m17,
              n20=draw_big + [max20], n20_maxcycle_class=max20, n20_maxcycle_m=m20,
              m_cycles_n17={r: cc[(17, r)] for r in draw_big + [max17]},
              m_cycles_n20={r: cc[(20, r)] for r in draw_big + [max20]})
json.dump(sample, open('SAMPLE.json', 'w'), indent=1)
print(json.dumps(sample, indent=None))
