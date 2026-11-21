"""Mutation checks: deliberately wrong statements must be caught by the tests of test_94.py."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['x', '14']
import test_94 as T
import numpy as np
out = {}
def run(name, fn):
    T.results.clear(); fn(); out[name] = [(r['test'], r['violations']) for r in T.results]
    print(name, out[name], flush=True)
orig = T.live_claimed
T.live_claimed = lambda w: orig(w) - {(1, 0, 0, 1)}
run('T1 without 1001 live', lambda: T.test_T1(3, 12))
run('L8 without 1001 live', lambda: T.test_L8(8))
T.live_claimed = lambda w: orig(w) | ({(1, 1, 1, 1, 1)} if w == 5 else set())
run('T1 with 11111 live', lambda: T.test_T1(3, 12))
T.live_claimed = orig
od = T.dw_set
T.dw_set = lambda n: set()
run('T1 without doubled words', lambda: T.test_T1(3, 12))
T.dw_set = od
oA = T.A_w
T.A_w = lambda w: T.B_w(w)
run('L10 with A replaced by B', lambda: T.test_L10(3, 12))
T.A_w = oA
oz = T.z15
T.z15 = lambda n: '0100101' + oz(n)[7:] if n != 7 else '0101001'
run('L15 with a wrong z', lambda: T.test_L15(12, 30))
T.z15 = oz
ow = T.is_word_001_0011
T.is_word_001_0011 = lambda x, n: ow(x, n) or x == 0b1
run('L16 with a wrong word set', lambda: T.test_L16(3, 10))
json.dump(out, open(os.path.join(T.OUT, 'mutate_94.json'), 'w'), indent=1)
