"""T05 -- Theorem 3.43 (rule 94) and Remark 3.44 from the definitions of Section 2, n = 3..NMAX (default 21).

For every n: all cycles, the matrix V, R(C -> D_v), gamma(C) for EVERY root by a minimum spanning in-tree (not by
Theorem 2.8), the selected set, k_v, k*, G1 and its closed classes.

 Part (i), 3 | n, n >= 6: the closed classes are exactly {A_1}, {A_2}, {A_3}; every other cycle has a G1 path to a
     crystal phase; S = {A_1, A_2, A_3}; k_v = 0 for 011, 101, 110 and k_v = 1 for 000, 001, 010, 100, 111; k* = 1;
     the words of Step 6 of the proof. Recorded in addition: gamma(A_i) - (m - 1).
 Part (ii), 3 not dividing n, n >= 5: exactly one closed class K; K contains every cycle with a non-empty frozen set;
     K = the set of cycles reachable in G1 from the block words; a cycle outside K is {0} or (n even) a cycle of
     doubled words; the states of K contain all eight codes; S = K, gamma_min = m - 1, k_v = 0, k* = 0.
 Remark 3.44: n = 4 (number of closed classes, the class, its codes, k*) and n = 3 (a flip leaves the crystal).
 For m <= MPY (default 320) every gamma(C) is recomputed per root in Python (too slow beyond that; for larger m the
 potentials rest on the C routine, which T00 validates).
Output: out/T05.txt, out/T05_rule94.csv.   Usage: python3 T05_rule94_theorem.py [NMAX] [MPY]
"""
import sys, time, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vp_core as vc
HERE = os.path.dirname(os.path.abspath(__file__))

def occ_fz(x, n):
    full = (1 << n) - 1
    a = ((x << 1) | (x >> (n - 1))) & full
    c = ((x >> 1) | (x << (n - 1))) & full
    occ = a & ~x & c & full
    return occ, (occ | ((occ << 1) | (occ >> (n - 1))) | ((occ >> 1) | (occ << (n - 1)))) & full

def is_doubled(x, n):
    if n % 2: return False
    for p in (0, 1):
        if all(((x >> ((2 * k + p) % n)) & 1) == ((x >> ((2 * k + p + 1) % n)) & 1) for k in range(n // 2)):
            return True
    return False

def main():
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 21
    MPY = int(sys.argv[2]) if len(sys.argv) > 2 else 320
    t0 = time.process_time(); w0 = time.time()
    L = []; fails = 0
    rows = ["n,case,m,closed_classes,selected,gamma_min,gamma_min_minus_(m-1),k000,k001,k010,k011,k100,k101,k110,k111,kstar,roots_rechecked_per_root,verdict"]
    for n in range(3, NMAX + 1):
        w1 = time.time()
        S = vc.System(94, n, level=2, workers=2)
        m = S.m; V = S.V; g = S.gamma; lab = S.lab
        kv, kstar, gmin, sel = S.indices()
        classes, comp = S.closed_classes()
        px = S.cyc_states
        N = 1 << n
        fzs = np.array([occ_fz(int(z), n)[1] for z in px], dtype=np.int64)
        fzc = np.zeros(m, dtype=np.int64); fzc[lab[px]] = fzs
        cc = S.cycle_codes()
        ok = True; notes = []
        special = [int(lab[0])]
        if n % 3 == 0:
            base = vc.from_word("011" * (n // 3))
            A = [int(lab[vc.rot(base, n, s)]) for s in range(3)]
            special = A
            fixed = all(int(S.F[vc.rot(base, n, s)]) == vc.rot(base, n, s) for s in range(3))
        roots = range(m) if m <= MPY else []
        nre = 0
        for r in roots:
            nre += 1
            if vc.in_tree_root_py(V, r) != g[r]:
                ok = False; notes.append("per-root mismatch at root %d" % r)
        if n % 3 == 0:
            case = "3|n"
            cl = sorted(tuple(int(c) for c in K) for K in classes)
            a = fixed and cl == sorted((a_,) for a_ in A)
            dist = S.g1_dist_to(A)
            b = bool((dist >= 0).all())
            c = sorted(np.nonzero(sel)[0].tolist()) == sorted(A)
            d = kv == [1, 1, 1, 0, 1, 0, 0, 1] and kstar == 1
            # Step 6: a block on p, p+1, p+2; y = x + e_{p+1}
            e = True
            for s in range(3):
                x = vc.rot(base, n, s)
                for p in range(n):
                    if (x >> p) & 1: continue
                    y = x ^ (1 << ((p + 1) % n)); y1 = int(S.F[y]); y2 = int(S.F[y1])
                    wd = lambda st: "".join(str((st >> ((p - 2 + i) % n)) & 1) for i in range(6))
                    code_at = lambda st, c_: 4 * ((st >> ((c_ - 1) % n)) & 1) + 2 * ((st >> (c_ % n)) & 1) + ((st >> ((c_ + 1) % n)) & 1)
                    e = e and wd(y) == "110010" and code_at(y, p) == 4 and code_at(y, p + 1) == 1 and code_at(y, p + 2) == 2
                    e = e and wd(y1) == "111110" and code_at(y1, p) == 7 and wd(y2) == "100010" and code_at(y2, p) == 0
            crystal_codes = sorted(v for v in range(8) if (int(cc[A[0]]) >> v) & 1)
            e = e and crystal_codes == [3, 5, 6]
            ok = ok and a and b and c and d and e
            if n >= 6:
                notes.append("closed classes exactly {A_1},{A_2},{A_3}: %s; every other cycle has a G1 path to a phase (longest shortest path %d): %s; S = A: %s; k_v as stated, k* = 1: %s; Step 6 words: %s; gamma(A_i) = m - 1 + %d" % (a, int(dist.max()), b, c, d, e, int(g[A[0]]) - (m - 1)))
            else:
                ok = True
                out = sorted({int(lab[vc.rot(base, n, s) ^ (1 << j)]) for s in range(3) for j in range(n)} - set(A))
                notes = ["n = 3 (not covered): closed classes %s, selected %s, k_v %s, k* = %d; cycles other than the phases reached by one flip of a phase: %d (Remark 3.44: 'a single flip can leave the crystal phase')" % (
                    [list(map(int, K)) for K in classes], np.nonzero(sel)[0].tolist(), kv, kstar, len(out))]
                ok = len(out) > 0
        else:
            case = "3 not | n"
            bwmask = (fzc == N - 1)
            K = np.zeros(m, dtype=bool)
            for Kc in classes: K[Kc] = True
            a = len(classes) == 1
            b = bool(K[fzc != 0].all())
            # reachable from block words
            reach = bwmask.copy(); front = np.nonzero(bwmask)[0].tolist()
            G1 = S.g1()
            while front:
                nf = []
                for u in front:
                    for w_ in np.nonzero(G1[u])[0]:
                        if not reach[w_]:
                            reach[w_] = True; nf.append(int(w_))
                front = nf
            c = bool((reach == K).all())
            outside = np.nonzero(~K)[0]
            d = all((S.states_of(q)[0] == 0 and len(S.states_of(q)) == 1) or all(is_doubled(int(z), n) for z in S.states_of(q)) for q in outside)
            e = int(np.bitwise_or.reduce(cc[K])) == 255 if K.any() else False
            f = bool((sel == K).all()) and gmin == m - 1 and kv == [0] * 8 and kstar == 0
            if n >= 5:
                ok = ok and a and b and c and d and e and f
                notes.append("one closed class: %s (|K| = %d of %d cycles); contains every cycle with non-empty frozen set: %s; = cycles reachable from block words: %s; outside K only {0} or doubled words (%d cycles outside): %s; all eight codes in K: %s; S = K, gamma_min = m-1, k_v = 0: %s" % (a, int(K.sum()), m, b, c, len(outside), d, e, f))
            else:
                codesK = [vc.CODE_WORDS[v] for v in range(8) if (int(np.bitwise_or.reduce(cc[K])) >> v) & 1]
                kstates = sorted(vc.word(int(z), n) for q in np.nonzero(K)[0] for z in S.states_of(q))
                notes.append("n = 4 (not covered): closed classes %d; the class consists of the states %s; block words: %s; its codes: %s; selected = class: %s; k_v %s; k* = %d" % (
                    len(classes), kstates, sorted(vc.word(int(z), n) for z in px[fzs == N - 1]), codesK, bool((sel == K).all()), kv, kstar))
                ok = ok and len(classes) == 1 and kstates == ["0101", "1010"] and codesK == ["010", "101"] and kstar == 1
        if len(classes) == 1:
            Km = np.zeros(m, dtype=bool); Km[classes[0]] = True
            t28 = bool((Km == sel).all()) and gmin == m - 1
            ok = ok and t28
            notes.append("Theorem 2.8 agrees with the in-trees: %s" % t28)
        else:
            Kall = np.zeros(m, dtype=bool)
            for Kc in classes: Kall[Kc] = True
            t28 = all(sel[Kc].all() or not sel[Kc].any() for Kc in classes) and not sel[~Kall].any()
            ok = ok and t28
            notes.append("S is a union of closed classes: %s" % t28)
        if not ok: fails += 1
        rows.append("%d,%s,%d,%d,%d,%d,%d,%s,%d,%d,%s" % (n, case, m, len(classes), int(sel.sum()), gmin, gmin - (m - 1), ",".join(map(str, kv)), kstar, nre, "ok" if ok else "FAIL"))
        L.append("n=%2d m=%5d %s k*=%d  %s  [%d roots rechecked per root; wall %.1f s]" % (n, m, "ok  " if ok else "FAIL", kstar, "; ".join(notes), nre, time.time() - w1))
        print(L[-1], flush=True)
    L.append("T05 %s   n = 3..%d   CPU %.1f s (Python; the C program runs with 2 threads in addition) wall %.1f s" % ("PASS" if fails == 0 else "FAIL", NMAX, time.process_time() - t0, time.time() - w0))
    print(L[-1])
    open(os.path.join(HERE, "out", "T05.txt"), "w").write("\n".join(L) + "\n")
    open(os.path.join(HERE, "out", "T05_rule94.csv"), "w").write("\n".join(rows) + "\n")
    return fails

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
