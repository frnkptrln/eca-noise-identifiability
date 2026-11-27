"""Lemma_3_5, Lemma_3_6_in_particular, Lemma_3_7, Lemma_3_8_a, Lemma_3_8_b (StatementMain.lean) on the literal
model for n = 1..12, with the paper's fuller forms next to them:
  Lemma 3.6: the three forms of a colliding pair (x + y = 1_E, x + y = 1_O, {x, y} = {1_E, 1_O});
  Lemma 3.7: second sentence (periodic states = M u periodic states of L in E u O) and third sentence
             (for n = 2^k, k >= 2: periodic states = M u {0});
  Lemma 3.8(b): "through cycles contained in M" (G1 restricted to the cycles contained in M strongly connected).
Also: G1 from the literal V against the criterion of Lemma 2.3, and R from the 0-1 BFS against Dijkstra on the
complete step graph (n <= 6).
Run: python lemmas.py > out/lemmas.txt
"""
from collections import defaultdict
from model import (Model, F154, global_map, cycles, periodic_points, in_parE, in_parO, in_parM, is_pow_two, oneE,
                   oneO, R_direct, contains, CODES)


def ends_on(F, idx, x):
    seen = set()
    while x not in idx:
        seen.add(x)
        x = F[x]
    return idx[x]


def main():
    allok = True
    for n in range(1, 13):
        F = F154(n)
        N = 1 << n
        even = n % 2 == 0
        EO = [x for x in range(N) if in_parE(x, n) or in_parO(x, n)]
        Mset = {x for x in range(N) if in_parM(x, n)}
        # Lemma 3.5
        l35 = all(F[x] in Mset for x in Mset)
        # Lemma 3.6
        pre = defaultdict(list)
        for x in range(N):
            pre[F[x]].append(x)
        pairs = [(x, y) for ys in pre.values() for i, x in enumerate(ys) for y in ys[i + 1:]]
        l36a = all(even and (x not in Mset) and (y not in Mset) for x, y in pairs)
        bij = len(pre) == N
        l36b = even or bij
        forms = {"E": 0, "O": 0, "EO": 0, "other": 0}
        for x, y in pairs:
            if in_parE(x, n) and in_parE(y, n) and x ^ y == oneE(n):
                forms["E"] += 1
            elif in_parO(x, n) and in_parO(y, n) and x ^ y == oneO(n):
                forms["O"] += 1
            elif {x, y} == {oneE(n), oneO(n)}:
                forms["EO"] += 1
            else:
                forms["other"] += 1
        line = (f"n={n:2d} even={even!s:5} |M|={len(Mset):4d} Lemma_3_5={l35!s:5} Lemma_3_6(pairs part)={l36a!s:5} "
                f"(bijection for odd n)={l36b!s:5} colliding pairs={len(pairs)} paper forms {forms}")
        print(line)
        ok_here = l36a and l36b and (l35 or not even)
        if not even:
            print(f"      (odd n: Lemma 3.5 is not claimed; F(M) in M here: {l35})")
        if even:
            # Lemma 3.7
            maps = l35
            inj = len({F[x] for x in Mset}) == len(Mset)
            surj = {F[x] for x in Mset} == Mset
            per = set(periodic_points(F))
            l37b = Mset <= per
            L = global_map(n, 90)
            perL = set(periodic_points(L))
            sent2 = per == Mset | {x for x in EO if x in perL}
            sent3 = (per == Mset | {0}) if (is_pow_two(n) and n >= 4) else None
            # Lemma 3.8
            Md = Model(n, need_gamma=False)
            cyc, idx, m = Md.cyc, Md.idx, Md.m
            inM = [all(x in Mset for x in C) for C in cyc]
            meetM = [any(x in Mset for x in C) for C in cyc]
            hyp_equiv = inM == meetM
            l38a = True
            for c in range(m):
                if not inM[c]:
                    continue
                for x in cyc[c]:
                    for j in range(n):
                        y = x ^ (1 << j)
                        if y not in Mset:
                            continue
                        if y not in idx:
                            l38a = False
                            continue
                        cy = idx[y]
                        if not inM[cy]:
                            l38a = False
                        if not (cy == c or (Md.G1[c][cy] and Md.G1[cy][c])):
                            l38a = False
            Mc = [c for c in range(m) if meetM[c]]
            l38b = all(d in Md.reach[c] for c in Mc for d in Mc)
            # paper: through cycles contained in M
            Min = [c for c in range(m) if inM[c]]
            Minset = set(Min)

            def reach_within(a):
                seen, st = {a}, [a]
                while st:
                    u = st.pop()
                    for w in Min:
                        if Md.G1[u][w] and w not in seen:
                            seen.add(w)
                            st.append(w)
                return seen
            l38b_paper = all(Minset <= reach_within(c) for c in Min)
            # G1 against Lemma 2.3
            g1_23 = [[False] * m for _ in range(m)]
            for c in range(m):
                for x in cyc[c]:
                    for j in range(n):
                        d = ends_on(F, idx, x ^ (1 << j))
                        if d != c:
                            g1_23[c][d] = True
            g1_agree = all(g1_23[a][b] == Md.G1[a][b] for a in range(m) for b in range(m))
            print(f"      Lemma_3_7: MapsTo={maps} InjOn={inj} SurjOn={surj} periodic={l37b}; paper 2nd sentence={sent2};"
                  f" 3rd sentence (n=2^k, k>=2)={sent3}")
            print(f"      cycles m={m}, meeting M={len(Mc)}, contained in M={len(Min)}, 'meets M' <-> 'contained in M': {hyp_equiv}")
            print(f"      Lemma_3_8_a={l38a} Lemma_3_8_b={l38b}; paper 3.8(b) through cycles in M={l38b_paper};"
                  f" G1 (literal V) = G1 (Lemma 2.3 criterion): {g1_agree}")
            ok_here = ok_here and maps and inj and surj and l37b and l38a and l38b and l38b_paper and g1_agree \
                and sent2 and sent3 is not False and hyp_equiv
        if n <= 6 and n >= 1:
            Md = Model(n, need_gamma=False)
            agree = all(Md.V[a][b] == R_direct(Md.F, n, Md.cyc[a], set(Md.cyc[b]))
                        for a in range(Md.m) for b in range(Md.m))
            Dagree = True
            for v in CODES:
                Dv = {x for x in range(N) if contains(x, v, n)}
                for a in range(Md.m):
                    bfs = min((Md.dist[a][x] for x in Dv), default=0)
                    if bfs != R_direct(Md.F, n, Md.cyc[a], Dv):
                        Dagree = False
            print(f"      R by 0-1 BFS = R by Dijkstra on all steps: V {agree}, R(C -> D_v) {Dagree}")
            ok_here = ok_here and agree and Dagree
        allok = allok and ok_here
    print("ALL OK" if allok else "SOME CHECK FAILED")


if __name__ == "__main__":
    main()
