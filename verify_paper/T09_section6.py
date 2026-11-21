"""T09 -- computed or proved statements of Section 6 that can be recomputed on small rings.

 (1) Section 6.1, Zhu and Richard: by Lemma 3.7 the states of rule 154 on no cycle are, for even n, the states of
     E u O that are not periodic under rule 90. The fraction of states on no cycle is computed for n = 13..27
     (directly from F for n <= ND, from Lemma 3.7 with rule 90 on E u O for all even n) and compared with the values
     quoted in the paper (macros ZRValues, ZRBound, ZRNmin, ZRNmax of paper/numbers.tex).
 (2) Section 6.2, classes 60 and 90: number of cycles and k* from the definitions, n = 4..NX; "k* >= 1 iff n is a
     power of two"; the values at n = 8, 16.
 (3) Section 6.2, class 45: rule 45 is the complement of the mirror image of rule 154; it is a bijection for odd n
     (n <= 21); k* = 0 at odd n <= NX.
 (4) Section 6.2, classes 35, 37, 45, 73, 122, 22: k* from the definitions for n = 8..NX against the lists of the
     paper (restricted to n <= NX); class 35: the selected cycles do not contain 101 where k* >= 1; class 22: the
     zero state is selected alone where k* >= 1.
 (5) Section 6.2, rule 94: is {0} in the closed class K (n = 5..NK, 3 not dividing n); how many cycles of doubled
     words lie in K.
 (6) Paragraph after Theorem 3.1: "Rule 43 and rule 142 are not equivalent under reflection and complementation of
     the rule": the classes of both rules under reflection, complementation and their product.
Output: out/T09.txt.   Usage: python3 T09_section6.py [path of paper/] [NX=16] [NK=20] [ND=24]
"""
import sys, time, os, re
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    paper = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "paper")
    arg = lambda k, d: int(sys.argv[k]) if len(sys.argv) > k else d
    NX, NK, ND = arg(2, 16), arg(3, 20), arg(4, 24)
    t0 = time.process_time(); w0 = time.time()
    num = open(os.path.join(paper, "numbers.tex")).read()
    macro = lambda name: re.search(r"\\newcommand\{\\%s\}\{(.*)\}" % name, num).group(1)
    ints = lambda s: [int(a) for a in re.findall(r"\d+", s)]
    L = []; fails = 0
    def rec(ok, msg):
        nonlocal fails
        if not ok: fails += 1
        L.append(("ok    " if ok else "FAIL  ") + msg); print(L[-1], flush=True)
    # (1)
    frac = {}
    for n in range(13, 28):
        if n % 2:
            frac[n] = 0.0 if n > ND else 1 - float(vc.System(154, n).per.mean())
            continue
        h = n // 2
        # E u O: states with ones on one parity class; rule 90 on them
        v = np.arange(1 << h, dtype=np.uint64)
        sp = np.zeros(1 << h, dtype=np.uint64)
        for i in range(h): sp |= ((v >> np.uint64(i)) & np.uint64(1)) << np.uint64(2 * i)
        st = np.unique(np.concatenate([sp, sp << np.uint64(1)]))
        full = np.uint64((1 << n) - 1)
        Lx = (((st << np.uint64(1)) | (st >> np.uint64(n - 1))) ^ ((st >> np.uint64(1)) | (st << np.uint64(n - 1)))) & full
        G = np.searchsorted(st, Lx); k = 1
        while k < len(st): G = G[G]; k *= 2
        nper = len(np.unique(G))
        frac[n] = (len(st) - nper) / 2.0 ** n
        if n <= ND:
            direct = 1 - float(vc.System(154, n).per.mean())
            rec(abs(direct - frac[n]) < 1e-15, "(1) n=%d fraction of states on no cycle: %.8f from Lemma 3.7 (E u O has %d states, %d periodic under rule 90), %.8f directly from F" % (n, frac[n], len(st), nper, direct))
    zr = macro("ZRValues")
    vals = re.findall(r"([0-9.]+) at \$n=(\d+)\$", zr)
    for val, n_ in vals:
        rec(abs(frac[int(n_)] - float(val)) < 5e-9, "(1) value quoted from Zhu and Richard at n=%s: %s; fraction given by Lemma 3.7: %.8f" % (n_, val, frac[int(n_)]))
    lo, hi, bd = int(macro("ZRNmin")), int(macro("ZRNmax")), float(macro("ZRBound"))
    mx = max(frac[n] for n in range(lo, hi + 1))
    rec(mx < bd, "(1) n = %d..%d: largest fraction %.6f (at n = %d), bound quoted %.2f; odd n > %d taken as 0 by Lemma 3.6" % (lo, hi, mx, max(range(lo, hi + 1), key=lambda n: frac[n]), bd, ND))
    # (2) classes 60, 90
    for rule, name in ((60, "KstarSixtyPos"), (90, "KstarNinetyPos")):
        ks = {}; ms = {}
        for n in range(4, NX + 1):
            S = vc.System(rule, n, level=2, workers=2)
            ks[n] = S.indices()[1]; ms[n] = S.m
        pos = [n for n in ks if ks[n] >= 1]
        pw = [n for n in ks if n & (n - 1) == 0]
        want = int(macro(name))
        rec(pos == pw and all(ks[n] == want for n in pw if n >= 8) and all(ms[n] == 1 for n in pw),
            "(2) rule %d, n = 4..%d: k* >= 1 exactly at n = %s (powers of two: %s); k* there: %s (paper: %d at n = 8, 16); number of cycles there: %s" % (rule, NX, pos, pw, [ks[n] for n in pw], want, [ms[n] for n in pw]))
    # (3) rule 45
    mirror154 = sum(((154 >> (4 * c + 2 * b + a)) & 1) << (4 * a + 2 * b + c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
    rec(255 - mirror154 == 45, "(3) mirror image of rule 154 is rule %d; its complement (255 - N) is rule %d" % (mirror154, 255 - mirror154))
    okb = True
    for n in range(3, 22, 2):
        S = vc.System(45, n)
        okb = okb and bool(S.per.all())
    rec(okb, "(3) rule 45 is a bijection for odd n = 3..21 (every state periodic)")
    # (4)
    lists = {35: ("pos", ints(macro("KposThirtyFive"))), 37: ("zero", ints(macro("KzeroThirtySeven"))), 45: ("pos", ints(macro("KposFortyFive"))),
             73: ("pos", ints(macro("KposSeventyThree"))), 122: ("zero", ints(macro("KzeroOneTwentyTwo"))), 22: ("pos", ints(macro("KposTwentyTwo")))}
    for rule, (kind, lst) in lists.items():
        ks = {}; extra = True
        for n in range(8, NX + 1):
            S = vc.System(rule, n, level=2, workers=2)
            kv, kstar, gmin, sel = S.indices()
            ks[n] = kstar
            if rule == 35 and kstar >= 1:
                extra = extra and not (int(np.bitwise_or.reduce(S.cycle_codes()[sel])) >> 5) & 1
            if rule == 22 and kstar >= 1:
                extra = extra and sel.sum() == 1 and sel[S.lab[0]]
            if rule == 45 and n % 2 == 1:
                extra = extra and kstar == 0
        got = [n for n in ks if (ks[n] >= 1) == (kind == "pos")]
        want = [n for n in lst if n <= NX]
        rec(got == want and extra, "(4) rule %d, n = 8..%d: k* %s at n = %s; list of the paper restricted to this range: %s%s" % (
            rule, NX, ">= 1" if kind == "pos" else "= 0", got, want,
            {35: "; selected cycles without 101 there: %s" % extra, 22: "; zero state selected alone there: %s" % extra, 45: "; k* = 0 at odd n: %s" % extra}.get(rule, "")))
    # (5)
    def fz(x, n):
        full = (1 << n) - 1
        a = ((x << 1) | (x >> (n - 1))) & full; c = ((x >> 1) | (x << (n - 1))) & full
        return a & ~x & c & full
    zin = {}; dbl = {}
    for n in range(5, NK + 1):
        if n % 3 == 0: continue
        S = vc.System(94, n, level=1, workers=2)
        classes, comp = S.closed_classes()
        K = np.zeros(S.m, dtype=bool)
        for Kc in classes: K[Kc] = True
        zin[n] = bool(K[S.lab[0]])
        emp = np.array([fz(int(S.states_of(q)[0]), n) == 0 for q in range(S.m)])
        emp[S.lab[0]] = False
        dbl[n] = (int((emp & K).sum()), int(emp.sum()))
    inK = [n for n in zin if zin[n]]
    rec(inK == [5, 7, 8], "(5) rule 94, 3 not dividing n, n = 5..%d: {0} lies in K exactly at n = %s (paper: in K for n = 5, 7, 8; proved not in K for n >= 10 with 8 not dividing n; computed not in K at n = 16)" % (NK, inK))
    txt = ", ".join("%d of %d at n=%d" % (dbl[n][0], dbl[n][1], n) for n in dbl if dbl[n][1])
    want = {int(n_): (int(a), int(b)) for a, b, n_ in re.findall(r"(\d+) of (\d+) at \$n=(\d+)\$", macro("NinetyFourDoubledInK"))}
    rec(all(dbl[n] == want[n] for n in want if n in dbl), "(5) cycles of doubled words in K: %s; paper: %s (compared for n <= %d)" % (txt, want, NK))
    # (6)
    def refl(N): return sum(((N >> (4 * c + 2 * b + a)) & 1) << (4 * a + 2 * b + c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
    def compl(N): return sum((1 - ((N >> (7 - v)) & 1)) << v for v in range(8))
    cls = lambda N: sorted({N, refl(N), compl(N), refl(compl(N))})
    rec(142 not in cls(43) and cls(154) == [154, 166, 180, 210] and cls(94) == [94, 133] and cls(26) == [26, 82, 167, 181],
        "(6) classes under reflection and complementation: rule 43: %s; rule 142: %s (different classes); also rule 154: %s, rule 94: %s, rule 26: %s" % (cls(43), cls(142), cls(154), cls(94), cls(26)))
    L.append("T09 %s   CPU %.1f s (Python) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T09.txt"), "w").write("\n".join(L) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
