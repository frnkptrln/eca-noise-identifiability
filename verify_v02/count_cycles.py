"""Pre-seal: number of cycles of F for every class representative at n = 17, 20 (cost input only)."""
import eca, numpy as np, json, time, sys
out = 'out/cycle_counts_n17_n20.jsonl'
done = {(r['n'], r['rule']) for r in eca.read_jsonl(out)}
for n in [17, 20]:
    for r in eca.class_reps():
        if (n, r) in done: continue
        t = time.time()
        F = eca.step_map(r, n).astype(np.int64)
        cid, cyc = eca.cycles_of(F)
        eca.append_jsonl(out, dict(n=n, rule=r, m_cycles=len(cyc), cycle_states=int(sum(len(c) for c in cyc)), sec=round(time.time()-t, 2)))
