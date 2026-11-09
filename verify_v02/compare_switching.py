"""Post-seal: own route (b) for the 13 switching classes at n = 15..20 vs data/fw_sweep.csv."""
import glob, pandas as pd, eca
sw = pd.read_csv('../data/fw_sweep.csv')
R = []
for f in sorted(glob.glob('out/route_b_switch_n*')):
    R += eca.read_jsonl(f)
rows = []
for r in R:
    s = sw[(sw.n == r['n']) & (sw.rule == r['rule'])].iloc[0]
    sel = r['cycle_orders_hist'][0] if 'cycle_orders_hist' in r else sum(v == 0 for v in r['cycle_orders'])
    rows.append(dict(n=r['n'], rule=r['rule'], m=r['m_cycles'], k_c_mine='-'.join(map(str, r['k_c'])), k_c_file=s.k_c,
                     kstar_mine=r['k_star'], kstar_file=int(s.kstar), selected_mine=sel, selected_file=int(s.n_stable),
                     consistent=r['consistent'], sec=r['sec'], maxrss_MB=r['maxrss_MB']))
df = pd.DataFrame(rows).sort_values(['rule', 'n'])
df['ok'] = (df.k_c_mine == df.k_c_file) & (df.kstar_mine == df.kstar_file) & (df.m == sw.set_index(['n', 'rule']).loc[list(zip(df.n, df.rule))].cycles.values) & (df.selected_mine == df.selected_file)
df.to_csv('out/compare_switching_n15_n20.csv', index=False)
print(len(df), 'runs; all equal (k_c, k*, cycles, number of noise-selected cycles):', bool(df.ok.all()), '; mismatches:', df[~df.ok][['n', 'rule']].values.tolist())
print('max sec', df.sec.max(), 'max RSS MB', df.maxrss_MB.max(), 'total CPU s', round(df.sec.sum()))
