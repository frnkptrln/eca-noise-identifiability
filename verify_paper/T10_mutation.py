"""T10 -- do the tests have teeth?  Each test is run again on short ranges with something deliberately wrong, and
must then report failures.

 (a) wrong rule: the engine is made to deliver another rule than the one the test names
       T02, T03 (rule 154): rule 26 instead (the closest relative: also rule 90 on E u O)
       T04, T05 (rule 94):  rule 90 instead
       T06 (rules 43, 142): the two rules exchanged
       T07 (rule 26):       rule 154 instead
 (b) wrong statement:
       T04: the 3-cycle of width 4 removed from the list of live window orbits (Lemma 3.35)
       T07: 'domain state' defined with source distances >= 5 instead of >= 3 (Definition 5.1)
       T08: the theorem row of rule 94 at n = 4 set to 0 (Table 1)
       T01: the potentials replaced by gamma + (cycle index mod 2) before S and k_v are formed (Section 2)
Output: out/T10.txt.  The mutated runs write their own outputs into a temporary directory.
"""
import sys, os, io, time, tempfile, importlib, contextlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import vp_core as vc

def run(modname, argv, patch):
    mod = importlib.import_module(modname)
    tmp = tempfile.mkdtemp(prefix="vp_mut_")
    os.makedirs(os.path.join(tmp, "out"))
    saved_here, saved_sys, saved_argv = mod.HERE, vc.System, sys.argv
    mod.HERE = tmp
    sys.argv = [modname] + [str(a) for a in argv]
    undo = patch(mod)
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            try:
                fails = mod.main()
            except Exception as e:           # a wrong rule may also break an assumption of the test code itself
                fails = "exception %s" % type(e).__name__
    finally:
        mod.HERE = saved_here; vc.System = saved_sys; sys.argv = saved_argv
        if undo: undo()
    return fails

def wrong_rule(mapping):
    def patch(mod):
        orig = vc.System
        class Sub(orig):
            def __init__(self, rule, n, **kw):
                orig.__init__(self, mapping.get(rule, rule), n, **kw)
        vc.System = Sub
        return None
    return patch

def main():
    t0 = time.process_time(); w0 = time.time()
    paper = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "paper")
    L = []; bad = 0
    def rec(name, fails):
        nonlocal bad
        caught = fails not in (0, None)
        if not caught: bad += 1
        L.append("%-70s -> %s" % (name, ("caught (%s)" % (fails if isinstance(fails, str) else "%d failures" % fails)) if caught else "NOT CAUGHT"))
        print(L[-1], flush=True)
    rec("T02 with rule 26 in place of rule 154 (NS=10, NG=8)", run("T02_rule154_lemmas", [10, 8], wrong_rule({154: 26})))
    rec("T03 with rule 26 in place of rule 154 (n <= 8)", run("T03_rule154_theorems", [8], wrong_rule({154: 26})))
    rec("T04 with rule 90 in place of rule 94 (short ranges)", run("T04_rule94_lemmas", [9, 9, 9, 8, 8, 9, 9], wrong_rule({94: 90})))
    rec("T05 with rule 90 in place of rule 94 (n <= 9)", run("T05_rule94_theorem", [9], wrong_rule({94: 90})))
    rec("T06 with rules 43 and 142 exchanged (n <= 8)", run("T06_rules43_142", [8, 8, 8], wrong_rule({43: 142, 142: 43})))
    rec("T07 with rule 154 in place of rule 26 (NS=10, NG=8)", run("T07_rule26", [10, 8, 12], wrong_rule({26: 154})))
    def p_live(mod):
        orig = mod.live_claim
        mod.live_claim = lambda l: set() if l == 4 else orig(l)
        return lambda: setattr(mod, "live_claim", orig)
    rec("T04 without the 3-cycle of width 4 in Lemma 3.35", run("T04_rule94_lemmas", [9, 9, 9, 8, 8, 9, 9], p_live))
    def p_dom(mod):
        orig = mod.analyse
        def wrong(x, n):
            chi, sources, sizes, dom = orig(x, n)
            if dom:
                dom = all(((sources[(q + 1) % len(sources)] - sources[q] - 1) % n) + 1 >= 5 for q in range(len(sources)))
            return chi, sources, sizes, dom
        mod.analyse = wrong
        return lambda: setattr(mod, "analyse", orig)
    rec("T07 with domain states defined by distances >= 5", run("T07_rule26", [10, 8, 12], p_dom))
    def p_tab(mod):
        orig = mod.theorem_value
        mod.theorem_value = lambda rule, n: "0" if (rule, n) == (94, 4) else orig(rule, n)
        # the mutated run reads the real outputs of T03..T07
        import shutil
        for fn in os.listdir(os.path.join(HERE, "out")):
            if fn.endswith(".csv"): shutil.copy(os.path.join(HERE, "out", fn), os.path.join(mod.HERE, "out", fn))
        return lambda: setattr(mod, "theorem_value", orig)
    rec("T08 with the theorem row of rule 94 at n = 4 set to 0", run("T08_table1", [paper, 4, 4], p_tab))
    def p_gamma(mod):
        orig = vc.System
        class Sub(orig):
            def _run(self, level, workers=1):
                orig._run(self, level, workers)
                if self.gamma is not None:
                    self.gamma = self.gamma + (np.arange(self.m) % 2)
        vc.System = Sub
        return None
    rec("T01 with perturbed potentials (n <= 6)", run("T01_section2", [6], p_gamma))
    L.append("T10 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS (every mutation was caught)" if bad == 0 else "FAIL (%d mutations not caught)" % bad, time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T10.txt"), "w").write("\n".join(L) + "\n")
    return bad

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
