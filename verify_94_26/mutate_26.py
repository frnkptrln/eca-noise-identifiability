"""Mutation checks: deliberately wrong statements must be caught by the tests of test_26.py."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = ['x', '12']
import test_26 as T
import eca
out = {}
def run(name, fn):
    T.results.clear(); fn(); out[name] = [(r['test'], r['violations']) for r in T.results]
    print(name, out[name], flush=True)
o = T.is_domain
T.is_domain = lambda x, n: T.in_M(x, n) and all((s2 - s1) % n >= 1 for s1, s2 in zip(T.sources(x, n), T.sources(x, n)[1:] + T.sources(x, n)[:1]))
run('domain distance >= 1 instead of >= 3', lambda: T.test_M3(10))
T.is_domain = o
oc = T.c1
T.c1 = lambda x, n: len(T.ones(x, n))
run('c = number of ones', lambda: (T.test_M3(10)))
T.c1 = oc
ocar = T.test_M7
oR = T.RULE
T.RULE = 154
run('rule 154 in Lemma 7 and Lemma 1', lambda: (T.test_M7(15), T.test_M1()))
T.RULE = oR
oev = T.EVEN
T.POW2 = (4, 8, 16, 12)
run('12 declared a power of two', T.test_enum)
json.dump(out, open(os.path.join(T.OUT, 'mutate_26.json'), 'w'), indent=1)
