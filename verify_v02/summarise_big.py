"""Collect the n = 17, 20 route (b) results of the sealed sample into out/sample_results_n17_n20.csv."""
import pandas as pd, eca
rows = []
for n in (17, 20):
    for w in ('w1', 'w2'):
        for r in eca.read_jsonl(f'out/route_b_n{n}.jsonl.{w}'):
            rows.append(dict(n=n, rule=r['rule'], m_cycles=r['m_cycles'], k_c_b=r['k_c'], k_star_b=r['k_star'],
                             consistent=r['consistent'], max_h=r['max_h'], sec=r['sec'], maxrss_MB=r['maxrss_MB'],
                             n_cycles_order0=(r['cycle_orders_hist'][0] if 'cycle_orders_hist' in r else sum(v == 0 for v in r['cycle_orders']))))
df = pd.DataFrame(rows).sort_values(['n', 'rule'])
df.to_csv('out/sample_results_n17_n20.csv', index=False)
print(df.to_string(index=False))
