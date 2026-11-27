"""Compare the records of rule 154 in data/fw_sweep.csv (read as data) with
  (1) the literal model (out/model_k_values.csv, written by theorems.py, n = 1..12), and
  (2) the conclusions of Theorem_3_11 for every n in the file: k*, the eight k_v (column k_c, code order
      4a + 2b + c), and the number of selected cycles (column n_stable: 1 for powers of two, all cycles otherwise).
Run: python sweep_compare.py <path to fw_sweep.csv> > out/sweep_compare.txt
"""
import csv
import sys
from model import is_pow_two


def main(path):
    rows = [r for r in csv.DictReader(open(path)) if r["rule"] == "154"]
    model = {int(r["n"]): r for r in csv.DictReader(open("out/model_k_values.csv"))}
    print(f"records of rule 154: {len(rows)}; n = {sorted(int(r['n']) for r in rows)}")
    ok = True
    for r in sorted(rows, key=lambda r: int(r["n"])):
        n = int(r["n"])
        kc = list(map(int, r["k_c"].split("-")))
        ks = int(r["kstar"])
        ns = int(r["n_stable"])
        m = int(r["cycles"])
        if is_pow_two(n):
            th_k = [0] + [1] * 7
            th_ks, th_ns = 1, 1
        else:
            th_k = [0] * 8
            th_ks, th_ns = 0, m
        th = (kc == th_k and ks == th_ks and ns == th_ns)
        msg = f"n={n:2d} cycles={m:6d} k_c={r['k_c']} kstar={ks} n_stable={ns} | Theorem_3_11 agrees: {th}"
        if n in model:
            md = model[n]
            ag = (md["k_c"] == r["k_c"] and int(md["kstar"]) == ks and int(md["n_selected"]) == ns
                  and int(md["cycles"]) == m)
            msg += f" | model (m={md['cycles']}, k_c={md['k_c']}, k*={md['kstar']}, |Sel|={md['n_selected']}) agrees: {ag}"
            ok = ok and ag
        ok = ok and th
        print(msg)
    print("ALL AGREE" if ok else "DISAGREEMENT")


if __name__ == "__main__":
    main(sys.argv[1])
