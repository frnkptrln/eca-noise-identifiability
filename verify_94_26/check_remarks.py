"""Side remarks: (1) PROOF_94_converse s6: on states without 101, the walls w_i = x_i + x_(i+1) of rule 94 evolve
by rule 18 for one step; (2) PROOF_26 s7: c of a carrier word with p blocks 11100 is (n + 4p)/3."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import eca, test_26 as T
res = {}
viol = cases = 0
for n in range(4, 17):
    mask = (1 << n) - 1
    F = eca.step_all(94, n)
    for x in range(1 << n):
        if eca.has_code(x, n, 5):
            continue
        walls = x ^ eca.rot(x, n, -1)          # bit i = x_i + x_(i+1)
        fw = int(F[x]) ^ eca.rot(int(F[x]), n, -1)
        cases += 1
        if fw != int(eca.step_all(18, n, [walls])[0]):
            viol += 1
res['walls_rule18_one_step'] = dict(n='4..16', cases=cases, violations=viol)
viol = cases = 0
for n in range(6, 32, 2):   # c is defined on even rings only
    for p in range(1, n // 5 + 1):
        if (n - 5 * p) % 3:
            continue
        q = (n - 5 * p) // 3
        for k in range(p + 1):          # a few block orders
            w = '11100' * k + '100' * q + '11100' * (p - k)
            if len(w) != n:
                continue
            cases += 1
            if 3 * T.c1(eca.from_word(w), n) != n + 4 * p:
                viol += 1
res['carrier_c_formula'] = dict(n='6..30 even', cases=cases, violations=viol)
print(res)
json.dump(res, open(os.path.join(T.OUT, 'remarks.json'), 'w'), indent=1)
