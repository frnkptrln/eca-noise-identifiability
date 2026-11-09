"""Summary of step 6 at n = 17: rebuilt single-flip chain vs Bagnoli et al. Table 2, vs fw_sweep.csv and own route (b)."""
import glob, eca, pandas as pd
R = eca.read_jsonl('out/bagnoli_n17_w1.jsonl') + eca.read_jsonl('out/bagnoli_n17_w2.jsonl')
b = pd.read_csv('lit/bagnoli_L17_table2.csv'); sw = pd.read_csv('../data/fw_sweep.csv'); sw = sw[sw.n == 17]
d = pd.DataFrame(R).merge(b, on='rule').merge(sw[['rule', 'kstar', 'n_stable', 'cycles']], on='rule')
d['dS'] = (d.Sstar_rebuilt - d.Sstar).abs()
mine = {}
for f in ['out/route_b_n17.jsonl.w1', 'out/route_b_n17.jsonl.w2', 'out/route_b_switch_n17.jsonl']:
    for r in eca.read_jsonl(f):
        mine[r['rule']] = r
L = []
L.append(f'classes: {len(d)}; attractor counts: Table 2 = own = fw_sweep for {int(((d.m_cycles == d.n_attr) & (d.cycles == d.n_attr)).sum())}')
L.append(f'S* rebuilt from their Section 5 recipe vs Table 2: max |diff| = {d.dS.max():.4f} (table has 3 decimals)')
L.append(f'single-flip graph: one closed class for {int((d.n_closed == 1).sum())} classes; several closed classes: {d[d.n_closed > 1][["rule", "n_closed", "closed_sizes"]].values.tolist()}')
one = d[d.n_closed == 1]
L.append(f'one closed class: support of their limit law = number of noise-selected cycles in fw_sweep (n_stable) for {int((one.support_size == one.n_stable).sum())} of {len(one)}')
L.append(f'one closed class: (support covers all 8 codes) == (k* = 0 in fw_sweep) for {int(((one.support_cover_mask == 255) == (one.kstar == 0)).sum())} of {len(one)}')
chk = [r for r in one.rule if r in mine]
L.append(f'own route (b) at n=17 available for {len(chk)} classes {sorted(chk)}: support size = own noise-selected count for '
         f'{sum(int(one[one.rule == r].support_size.iloc[0]) == (mine[r]["cycle_orders_hist"][0] if "cycle_orders_hist" in mine[r] else sum(v == 0 for v in mine[r]["cycle_orders"])) for r in chk)}')
many = d[d.n_closed > 1]
for _, x in many.iterrows():
    L.append(f'class {x.rule}: {x.n_closed} closed classes, their limit support {x.support_size} cycles (min states {x.support_min_states}), fw_sweep n_stable {x.n_stable}, k* {x.kstar}, cover mask {x.support_cover_mask}')
d.to_csv('out/bagnoli_n17_compare.csv', index=False)
open('out/bagnoli_n17_summary.txt', 'w').write('\n'.join(L) + '\n'); print('\n'.join(L))
