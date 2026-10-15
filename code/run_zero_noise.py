"""Stage Z: exact zero-noise orbits for all 256 rules x 4096 initial states.

Writes
  data/zero_noise_per_state.csv.gz : rule, x0, transient, period, tau, N_inf_size, class_size, N_inf_mask
  data/zero_noise_per_rule.csv     : per-rule summary incl. the cycle-coverage classification used for Lemma 2
"""
import sys, os, csv, gzip
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca_noise as E


def main(out="data"):
    codes = E.neighborhood_codes(); counts = E.code_counts()
    reps, rep_of = E.rule_class_representatives()
    per_state = gzip.open(os.path.join(out, "zero_noise_per_state.csv.gz"), "wt", newline="")
    ws = csv.writer(per_state)
    ws.writerow(["rule", "x0", "transient", "period", "tau", "N_inf_size", "class_size", "N_inf_mask"])
    rows = []
    for rule in range(256):
        succ = E.successor_map(rule, codes=codes)
        z = E.zero_noise_classes(succ, counts)
        for x0 in range(E.S):
            ws.writerow([rule, x0, int(z["transient"][x0]), int(z["period"][x0]), int(z["tau"][x0]),
                         int(z["N_inf_size"][x0]), int(z["class_size"][x0]), int(z["N_inf_mask"][x0])])
        # cycle structure
        on_cycle = z["on_cycle"]
        # enumerate cycles and their individual coverage masks
        visited = np.zeros(E.S, dtype=bool); cycles = []
        mask_state = np.zeros(E.S, dtype=np.int64)
        for c in range(8):
            mask_state |= (counts[:, c] > 0).astype(np.int64) << c
        for s0 in range(E.S):
            if on_cycle[s0] and not visited[s0]:
                cyc = [s0]; visited[s0] = True; s = int(succ[s0])
                while s != s0:
                    cyc.append(s); visited[s] = True; s = int(succ[s])
                m = 0
                for v in cyc:
                    m |= int(mask_state[v])
                cycles.append((len(cyc), m))
        n_cycles = len(cycles)
        all_cycles_full = all(m == 255 for _, m in cycles)
        union_full = (int(z["cycle_union_mask"]) == 255)
        if not union_full:
            limit_type = "B_proved"        # some code never appears on any cycle -> rho -> 0 as eps -> 0
        elif all_cycles_full:
            limit_type = "A_proved"        # every cycle covers all 8 codes -> rho -> infinity as eps -> 0
        else:
            limit_type = "undetermined"    # depends on the small-noise weights of the cycles
        rows.append(dict(
            rule=rule, rep=rep_of[rule],
            frac_full_identification=float((z["N_inf_size"] == 8).mean()),
            mean_class_size=float(z["class_size"].mean()),
            max_class_size=int(z["class_size"].max()),
            mean_N_inf=float(z["N_inf_size"].mean()),
            mean_tau=float(z["tau"].mean()), max_tau=int(z["tau"].max()),
            n_cycle_states=int(on_cycle.sum()), n_cycles=n_cycles,
            max_period=max(l for l, _ in cycles),
            cycle_union_mask=int(z["cycle_union_mask"]), cycle_union_size=bin(int(z["cycle_union_mask"])).count("1"),
            all_cycles_full=int(all_cycles_full), limit_type=limit_type,
        ))
        print(f"rule {rule} done", flush=True)
    per_state.close()
    with open(os.path.join(out, "zero_noise_per_rule.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)


if __name__ == "__main__":
    main()
