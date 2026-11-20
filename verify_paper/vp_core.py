"""vp_core.py -- own engine for the verification of paper/ring_size_paper.tex.

Written from the definitions of Section 2 of the paper, without reading any script of the repository.

Conventions (Section 2.1 of the paper):
  a state x of the ring Z/n is an integer, cell i = bit i;
  (Fx)_i = f(x_{i-1}, x_i, x_{i+1}), f(a,b,c) = bit 4a+2b+c of the rule number;
  the code of cell i is the word (x_{i-1}, x_i, x_{i+1}), numbered 4a+2b+c;
  r(x, y) = Hamming(Fx, y); a path x_0..x_T has resistance sum r(x_t, x_{t+1});
  R(A -> B) = least resistance of a path from a state of A to a state of B; V(C, C') = R(C -> C');
  gamma(C) = least weight of a spanning in-tree on the cycles rooted at C with edge weights V;
  k_v = min_C [gamma(C) + R(C -> D_v)] - gamma_min, k* = max_v k_v.

The heavy loops are in C. The C source is the string C_SOURCE below; it is compiled at run time with `cc` into a
temporary directory (nothing is written into the repository). A pure numpy/Python implementation of every C routine
is in this file too (functions with suffix _py or _brute) and test T00 compares the two. The C program is run
as a separate process (at most 2 threads); numpy reads its output files from the temporary directory.

Search used for R: from a cycle C (which F maps onto itself) the states reachable with resistance <= d are found by a
0-1 breadth-first search with the moves "apply F" (cost 0) and "flip one cell" (cost 1). A sequence of such moves that
starts at a state of C is a path in the sense of the paper: consecutive flips form one step y = F(x) + e_j + e_j' + ...,
and a flip made before the first F from x in C is the step from the F-predecessor of x on C. Conversely every path is
such a sequence.
"""
import os, subprocess, sys, tempfile, itertools
import numpy as np

C_SOURCE = r"""
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

void eca_map(int rule, int n, uint32_t *F, uint8_t *codes) {
    uint32_t N = 1u << n;
    for (uint32_t x = 0; x < N; x++) {
        uint32_t y = 0; uint8_t cm = 0;
        for (int i = 0; i < n; i++) {
            int a = (x >> ((i + n - 1) % n)) & 1, b = (x >> i) & 1, c = (x >> ((i + 1) % n)) & 1;
            int v = 4 * a + 2 * b + c;
            y |= (uint32_t)((rule >> v) & 1) << i;
            cm |= (uint8_t)(1u << v);
        }
        F[x] = y; codes[x] = cm;
    }
}

/* lab[x] = index of the cycle on which the orbit of x ends; per[x] = 1 iff x is periodic. Returns number of cycles. */
int label_cycles(int n, const uint32_t *F, int32_t *lab, uint8_t *per) {
    uint32_t N = 1u << n;
    int32_t *stamp = (int32_t *)calloc(N, sizeof(int32_t));
    uint32_t *stack = (uint32_t *)malloc((size_t)N * sizeof(uint32_t));
    int m = 0; int32_t walk = 0;
    memset(per, 0, N);
    for (uint32_t s = 0; s < N; s++) {
        if (stamp[s]) continue;
        walk++;
        uint32_t x = s; size_t top = 0;
        while (!stamp[x]) { stamp[x] = walk; stack[top++] = x; x = F[x]; }
        int32_t L;
        if (stamp[x] == walk) {            /* new cycle through x */
            L = m++;
            uint32_t y = x;
            do { per[y] = 1; lab[y] = L; y = F[y]; } while (y != x);
        } else L = lab[x];
        for (size_t t = 0; t < top; t++) lab[stack[t]] = L;
    }
    free(stamp); free(stack);
    return m;
}

/* 0-1 search from the cycles src_begin..src_end-1.  cyc_start[c]..cyc_start[c+1]-1 index cyc_states.
   V[(c-src_begin)*m + c'] = V(C_c, C_c'),  Rc[(c-src_begin)*8 + v] = R(C_c -> D_v)  (255 = not reached). */
void search_from_cycles(int n, const uint32_t *F, const int32_t *lab, int m,
                        const int64_t *cyc_start, const uint32_t *cyc_states, const uint8_t *codes,
                        int src_begin, int src_end, uint8_t *V, uint8_t *Rc) {
    uint32_t N = 1u << n;
    uint8_t *dist = (uint8_t *)malloc(N);
    uint32_t *cur = (uint32_t *)malloc((size_t)N * sizeof(uint32_t));
    uint32_t *nxt = (uint32_t *)malloc((size_t)N * sizeof(uint32_t));
    for (int c = src_begin; c < src_end; c++) {
        uint8_t *row = V + (size_t)(c - src_begin) * m;
        uint8_t *rc = Rc + (size_t)(c - src_begin) * 8;
        memset(dist, 255, N); memset(row, 255, m); memset(rc, 255, 8);
        size_t ncur = 0, nnxt = 0; int reached = 0, codes_seen = 0;
        for (int64_t t = cyc_start[c]; t < cyc_start[c + 1]; t++) { dist[cyc_states[t]] = 0; cur[ncur++] = cyc_states[t]; }
        int d = 0;
        while (ncur > 0) {
            for (size_t q = 0; q < ncur; q++) {       /* cur grows while it is scanned (cost-0 moves) */
                uint32_t x = cur[q];
                if (dist[x] != d) continue;           /* was reached earlier with smaller resistance */
                int L = lab[x];
                if (row[L] == 255) { row[L] = (uint8_t)d; reached++; }
                uint8_t cm = codes[x];
                if ((cm & ~codes_seen) != 0) {
                    for (int v = 0; v < 8; v++) if (((cm >> v) & 1) && rc[v] == 255) rc[v] = (uint8_t)d;
                    codes_seen |= cm;
                }
                uint32_t y = F[x];
                if (dist[y] > d) { dist[y] = (uint8_t)d; cur[ncur++] = y; }
                for (int j = 0; j < n; j++) {
                    uint32_t z = x ^ (1u << j);
                    if (dist[z] > d + 1) { dist[z] = (uint8_t)(d + 1); nxt[nnxt++] = z; }
                }
            }
            if (reached == m && codes_seen == 255) break;
            uint32_t *tmp = cur; cur = nxt; nxt = tmp; ncur = nnxt; nnxt = 0; d++;
        }
    }
    free(dist); free(cur); free(nxt);
}

/* Minimum spanning in-tree weight for EVERY root, weights W[u*m+v] for the edge u -> v (u != v), complete digraph.
   Edmonds' contraction carried out without a root (each node chooses a cheapest out-edge; circuits are contracted
   until one node is left); the contraction tree gives for the root r:
       gamma(r) = sum of the reduced costs c(t) of all tree nodes t except the top
                  - sum of c(t) over the tree nodes t that contain r (except the top).
   Validated against a per-root Chu-Liu/Edmonds and against enumeration of all in-trees (test T00). */
int in_tree_all_roots(int m, const uint8_t *W, int64_t *gamma) {
    if (m == 1) { gamma[0] = 0; return 0; }
    int32_t *red = (int32_t *)malloc((size_t)m * m * sizeof(int32_t));
    if (!red) return -1;
    for (size_t i = 0; i < (size_t)m * m; i++) red[i] = W[i];
    int T = 2 * m;
    int32_t *parent = (int32_t *)malloc(T * sizeof(int32_t));
    int64_t *c = (int64_t *)calloc(T, sizeof(int64_t));
    int32_t *tnode = (int32_t *)malloc(m * sizeof(int32_t));
    int32_t *pos = (int32_t *)malloc(m * sizeof(int32_t));
    int32_t *path = (int32_t *)malloc(m * sizeof(int32_t));
    uint8_t *alive = (uint8_t *)malloc(m);
    int32_t *alist = (int32_t *)malloc(m * sizeof(int32_t));
    for (int i = 0; i < T; i++) parent[i] = -1;
    for (int i = 0; i < m; i++) { tnode[i] = i; pos[i] = -1; alive[i] = 1; }
    int next = m, nalive = m, top = 0;
    path[0] = 0; pos[0] = 0;
    while (nalive > 1) {
        int u = path[top];
        int best = -1; int32_t bw = 0;
        const int32_t *ru = red + (size_t)u * m;
        for (int w = 0; w < m; w++) if (alive[w] && w != u) { if (best < 0 || ru[w] < bw) { best = w; bw = ru[w]; } }
        c[tnode[u]] = bw;
        int v = best;
        if (pos[v] < 0) { path[++top] = v; pos[v] = top; continue; }
        /* contract path[pos[v]..top] into the slot v */
        int p0 = pos[v]; int Tn = next++;
        int na = 0;
        for (int w = 0; w < m; w++) if (alive[w] && (pos[w] < p0)) alist[na++] = w;   /* alive nodes outside the segment */
        int32_t *rv = red + (size_t)v * m;
        for (int a = 0; a < na; a++) {
            int w = alist[a];
            int32_t out = 0x7fffffff, in = 0x7fffffff;
            for (int q = p0; q <= top; q++) {
                int x = path[q];
                int32_t o = red[(size_t)x * m + w] - (int32_t)c[tnode[x]];
                if (o < out) out = o;
                int32_t ii = red[(size_t)w * m + x];
                if (ii < in) in = ii;
            }
            rv[w] = out; red[(size_t)w * m + v] = in;
        }
        for (int q = p0; q <= top; q++) {
            int x = path[q];
            parent[tnode[x]] = Tn;
            if (x != v) { alive[x] = 0; pos[x] = -1; nalive--; }
        }
        tnode[v] = Tn; top = p0; path[top] = v; pos[v] = top;
    }
    int topnode = next - 1;
    int64_t total = 0;
    for (int t = 0; t < topnode; t++) total += c[t];
    for (int r = 0; r < m; r++) {
        int64_t s = 0;
        for (int t = r; t != topnode; t = parent[t]) s += c[t];
        gamma[r] = total - s;
    }
    free(red); free(parent); free(c); free(tnode); free(pos); free(path); free(alive); free(alist);
    return 0;
}
#include <stdio.h>
#include <pthread.h>

typedef struct { int n, m, b, e; const uint32_t *F; const int32_t *lab; const int64_t *cs; const uint32_t *cst;
                 const uint8_t *codes; uint8_t *V, *Rc; } job_t;
static void *job_run(void *a) {
    job_t *j = (job_t *)a;
    search_from_cycles(j->n, j->F, j->lab, j->m, j->cs, j->cst, j->codes, j->b, j->e,
                       j->V + (size_t)j->b * j->m, j->Rc + (size_t)j->b * 8);
    return 0;
}
static void dump(const char *prefix, const char *name, const void *p, size_t bytes) {
    char fn[4096]; snprintf(fn, sizeof fn, "%s%s", prefix, name);
    FILE *f = fopen(fn, "wb"); fwrite(p, 1, bytes, f); fclose(f);
}
/* usage:  tool all <rule> <n> <threads (1 or 2)> <level: 0 cycles only, 1 + V and Rc, 2 + gamma> <outprefix>
           tool intree <m> <infile (m*m bytes)> <outfile (m int64)>                                        */
int main(int argc, char **argv) {
    if (argc >= 5 && !strcmp(argv[1], "intree")) {
        int m = atoi(argv[2]);
        uint8_t *W = (uint8_t *)malloc((size_t)m * m);
        FILE *f = fopen(argv[3], "rb"); if (fread(W, 1, (size_t)m * m, f) != (size_t)m * m) return 2; fclose(f);
        int64_t *g = (int64_t *)malloc(m * sizeof(int64_t));
        if (in_tree_all_roots(m, W, g)) return 3;
        f = fopen(argv[4], "wb"); fwrite(g, sizeof(int64_t), m, f); fclose(f);
        return 0;
    }
    if (argc < 7 || strcmp(argv[1], "all")) return 1;
    int rule = atoi(argv[2]), n = atoi(argv[3]), nth = atoi(argv[4]), level = atoi(argv[5]);
    const char *prefix = argv[6];
    if (nth > 2) nth = 2;
    uint32_t N = 1u << n;
    uint32_t *F = (uint32_t *)malloc((size_t)N * 4); uint8_t *codes = (uint8_t *)malloc(N);
    eca_map(rule, n, F, codes);
    int32_t *lab = (int32_t *)malloc((size_t)N * 4); uint8_t *per = (uint8_t *)malloc(N);
    int m = label_cycles(n, F, lab, per);
    dump(prefix, "F.u32", F, (size_t)N * 4); dump(prefix, "codes.u8", codes, N);
    dump(prefix, "lab.i32", lab, (size_t)N * 4); dump(prefix, "per.u8", per, N);
    printf("%d\n", m);
    if (level < 1) return 0;
    /* cycle lists */
    int64_t *cs = (int64_t *)calloc(m + 2, sizeof(int64_t));
    size_t np_ = 0;
    for (uint32_t x = 0; x < N; x++) if (per[x]) { cs[lab[x] + 1]++; np_++; }
    for (int c = 0; c < m; c++) cs[c + 1] += cs[c];
    uint32_t *cst = (uint32_t *)malloc(np_ * 4 + 4);
    int64_t *fill = (int64_t *)malloc((m + 1) * sizeof(int64_t));
    memcpy(fill, cs, (m + 1) * sizeof(int64_t));
    for (uint32_t x = 0; x < N; x++) if (per[x]) cst[fill[lab[x]]++] = x;
    uint8_t *V = (uint8_t *)malloc((size_t)m * m), *Rc = (uint8_t *)malloc((size_t)m * 8);
    job_t jobs[2]; pthread_t th[2];
    for (int t = 0; t < nth; t++) {
        /* interleave is not needed: split the sources in two halves of equal count */
        jobs[t] = (job_t){n, m, (int)((int64_t)m * t / nth), (int)((int64_t)m * (t + 1) / nth), F, lab, cs, cst, codes, V, Rc};
        pthread_create(&th[t], 0, job_run, &jobs[t]);
    }
    for (int t = 0; t < nth; t++) pthread_join(th[t], 0);
    dump(prefix, "V.u8", V, (size_t)m * m); dump(prefix, "Rc.u8", Rc, (size_t)m * 8);
    if (level < 2) return 0;
    int64_t *g = (int64_t *)malloc(m * sizeof(int64_t));
    if (in_tree_all_roots(m, V, g)) return 3;
    dump(prefix, "gamma.i64", g, m * sizeof(int64_t));
    return 0;
}
"""

_exe = None
_tmp = None


def exe():
    """Compile C_SOURCE into a temporary directory (outside the repository) and return the path of the program."""
    global _exe, _tmp
    if _exe is None:
        _tmp = tempfile.mkdtemp(prefix="vp_core_")
        csrc = os.path.join(_tmp, "vp_tool.c")
        with open(csrc, "w") as fh:
            fh.write(C_SOURCE)
        _exe = os.path.join(_tmp, "vp_tool")
        subprocess.check_call(["cc", "-O2", "-o", _exe, csrc, "-lpthread"])
    return _exe


def in_tree_all_roots(W):
    """gamma for every root with the C routine. W: m x m array of weights 0..255 (diagonal ignored)."""
    W = np.ascontiguousarray(W, dtype=np.uint8)
    m = W.shape[0]
    e = exe()
    fi = os.path.join(_tmp, "w_%d.bin" % os.getpid())
    fo = os.path.join(_tmp, "g_%d.bin" % os.getpid())
    W.tofile(fi)
    subprocess.check_call([e, "intree", str(m), fi, fo])
    g = np.fromfile(fo, dtype=np.int64)
    os.remove(fi)
    os.remove(fo)
    return g


CODE_WORDS = ["000", "001", "010", "011", "100", "101", "110", "111"]


class System:
    """Rule `rule` on the ring of n cells: map F, cycles, and (on demand) V, R(C -> D_v), gamma, k_v."""

    def __init__(self, rule, n, level=0, workers=1):
        """level 0: map and cycles; 1: also V and R(C -> D_v); 2: also gamma for every root."""
        self.rule, self.n = rule, n
        self.N = 1 << n
        self.V = self.Rc = self.gamma = None
        self._run(level, workers)
        pst = np.nonzero(self.per)[0].astype(np.uint32)
        order = np.argsort(self.lab[pst], kind="stable")
        self.cyc_states = np.ascontiguousarray(pst[order])
        counts = np.bincount(self.lab[pst], minlength=self.m)
        self.cyc_start = np.zeros(self.m + 1, dtype=np.int64)
        np.cumsum(counts, out=self.cyc_start[1:])

    def _run(self, level, workers=1):
        e = exe()
        prefix = os.path.join(_tmp, "r%d_n%d_p%d_" % (self.rule, self.n, os.getpid()))
        out = subprocess.check_output([e, "all", str(self.rule), str(self.n), str(min(int(workers), 2)), str(level),
                                       prefix])
        self.m = m = int(out.split()[0])
        rd = lambda name, dt: np.fromfile(prefix + name, dtype=dt)
        self.F = rd("F.u32", np.uint32)
        self.codes = rd("codes.u8", np.uint8)
        self.lab = rd("lab.i32", np.int32)
        self.per = rd("per.u8", np.uint8)
        if level >= 1:
            self.V = rd("V.u8", np.uint8).reshape(m, m)
            self.Rc = rd("Rc.u8", np.uint8).reshape(m, 8)
        if level >= 2:
            self.gamma = rd("gamma.i64", np.int64)
        for name in ["F.u32", "codes.u8", "lab.i32", "per.u8", "V.u8", "Rc.u8", "gamma.i64"]:
            if os.path.exists(prefix + name):
                os.remove(prefix + name)

    def states_of(self, c):
        return self.cyc_states[self.cyc_start[c]:self.cyc_start[c + 1]]

    def cycle_codes(self):
        """8-bit mask per cycle: the codes contained in its states."""
        cc = np.zeros(self.m, dtype=np.uint8)
        np.bitwise_or.at(cc, self.lab[self.cyc_states], self.codes[self.cyc_states])
        return cc

    def search(self, workers=1):
        """V (m x m) and Rc (m x 8) from the definitions; at most 2 threads."""
        if self.V is None:
            self._run(1, workers)
        return self.V, self.Rc

    def potentials(self, workers=1):
        """gamma(C) for every root C: a minimum spanning in-tree for every root (C routine in_tree_all_roots)."""
        if self.gamma is None:
            self._run(2, workers)
        return self.gamma

    def indices(self):
        """(k_v for the eight codes, k*, gamma_min, selected: bool array) from equation (1) of the paper."""
        if self.gamma is None:
            self.potentials()
        gmin = int(self.gamma.min())
        tot = self.gamma[:, None] + self.Rc.astype(np.int64)
        k = tot.min(axis=0) - gmin
        return [int(a) for a in k], int(k.max()), gmin, self.gamma == gmin

    def g1(self):
        """One-flip graph: boolean m x m matrix, edge C -> C' iff V(C, C') = 1."""
        return self.V == 1

    def closed_classes(self):
        """List of closed classes (arrays of cycle indices), and the SCC label of every cycle."""
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import connected_components
        A = self.g1()
        ncomp, comp = connected_components(csr_matrix(A), directed=True, connection="strong")
        src, dst = np.nonzero(A)
        leaving = np.zeros(ncomp, dtype=bool)
        dif = comp[src] != comp[dst]
        leaving[comp[src[dif]]] = True
        return [np.nonzero(comp == q)[0] for q in range(ncomp) if not leaving[q]], comp

    def g1_dist_to(self, targets):
        """Length of a shortest directed path of G1 from every cycle to the set `targets` (-1: none)."""
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import breadth_first_order
        m = self.m
        AT = csr_matrix(self.g1().T)
        dist = -np.ones(m, dtype=np.int64)
        front = list(targets)
        for t in front:
            dist[t] = 0
        d = 0
        indptr, indices = AT.indptr, AT.indices
        while front:
            d += 1
            nf = []
            for u in front:
                for w in indices[indptr[u]:indptr[u + 1]]:
                    if dist[w] < 0:
                        dist[w] = d
                        nf.append(w)
            front = nf
        return dist


# ---------------------------------------------------------------------------------------------------------------
# Pure Python / numpy reference implementations (independent of the C routines)
# ---------------------------------------------------------------------------------------------------------------

def eca_map_py(rule, n):
    N = 1 << n
    x = np.arange(N, dtype=np.uint32)
    y = np.zeros(N, dtype=np.uint32)
    codes = np.zeros(N, dtype=np.uint8)
    for i in range(n):
        a = (x >> np.uint32((i - 1) % n)) & 1
        b = (x >> np.uint32(i)) & 1
        c = (x >> np.uint32((i + 1) % n)) & 1
        v = 4 * a + 2 * b + c
        y |= ((np.uint32(rule) >> v) & 1) << np.uint32(i)
        codes |= (np.uint8(1) << v.astype(np.uint8))
    return y, codes


def cycles_py(F):
    """Periodic states and cycles by iteration: x is periodic iff x is in the image of F^K, K >= number of states."""
    N = len(F)
    G = F.copy()
    k = 1
    while k < N:
        G = G[G]
        k *= 2
    per = np.zeros(N, dtype=bool)
    per[G] = True
    cyc_of = {}
    cycles = []
    for x in np.nonzero(per)[0]:
        x = int(x)
        if x in cyc_of:
            continue
        c = len(cycles)
        orb = [x]
        y = int(F[x])
        while y != x:
            orb.append(y)
            y = int(F[y])
        for y in orb:
            cyc_of[y] = c
        cycles.append(orb)
    lab = np.array([cyc_of[int(G[x])] for x in range(N)], dtype=np.int64)
    return per, cycles, lab


def search_py(n, F, cycles, lab, codes):
    """V and Rc by a level-by-level search with numpy boolean arrays."""
    N = len(F)
    m = len(cycles)
    V = np.full((m, m), 255, dtype=np.int64)
    Rc = np.full((m, 8), 255, dtype=np.int64)
    idx = np.arange(N, dtype=np.uint32)
    for c, orb in enumerate(cycles):
        seen = np.zeros(N, dtype=bool)
        front = np.zeros(N, dtype=bool)
        front[orb] = True
        d = 0
        while front.any():
            new = front.copy()
            while True:                       # close the level under F
                img = np.zeros(N, dtype=bool)
                img[F[new]] = True
                img &= ~front & ~seen
                if not img.any():
                    break
                front |= img
                new = img
            for L in np.unique(lab[front]):
                if V[c, L] == 255:
                    V[c, L] = d
            cm = int(np.bitwise_or.reduce(codes[front]))
            for v in range(8):
                if (cm >> v) & 1 and Rc[c, v] == 255:
                    Rc[c, v] = d
            seen |= front
            nxt = np.zeros(N, dtype=bool)
            fi = idx[front]
            for j in range(n):
                nxt[fi ^ np.uint32(1 << j)] = True
            front = nxt & ~seen
            d += 1
    return V, Rc


def in_tree_root_py(W, r):
    """Minimum weight of a spanning in-tree rooted at r (Chu-Liu/Edmonds for one root, repeated contraction).
    W: square array, W[u, v] = weight of u -> v; the diagonal is ignored."""
    W = np.array(W, dtype=np.int64)
    BIG = 10 ** 12
    total = 0
    while True:
        m = W.shape[0]
        if m == 1:
            return total
        Wd = W.copy()
        np.fill_diagonal(Wd, BIG)
        choice = Wd.argmin(axis=1)
        cost = Wd.min(axis=1)
        choice[r] = -1
        state = np.zeros(m, dtype=np.int64)   # 0 new, 1 on the current walk, 2 done
        cyc_nodes = []
        for s in range(m):
            if state[s]:
                continue
            path = []
            u = s
            while u != -1 and state[u] == 0:
                state[u] = 1
                path.append(u)
                u = choice[u]
            if u != -1 and state[u] == 1:
                cyc_nodes.append(path[path.index(u):])
            for u in path:
                state[u] = 2
        if not cyc_nodes:
            return total + int(sum(cost[u] for u in range(m) if u != r))
        newid = -np.ones(m, dtype=np.int64)
        nn = 0
        incyc = np.zeros(m, dtype=bool)
        for cn in cyc_nodes:
            for u in cn:
                newid[u] = nn
                incyc[u] = True
            total += int(sum(cost[u] for u in cn))
            nn += 1
        for u in range(m):
            if newid[u] < 0:
                newid[u] = nn
                nn += 1
        Wr = W - np.where(incyc, cost, 0)[:, None]          # reduced weights of the edges leaving a circuit
        W2 = np.full((nn, nn), BIG, dtype=np.int64)
        np.minimum.at(W2, (newid[:, None].repeat(m, 1), newid[None, :].repeat(m, 0)), Wr)
        np.fill_diagonal(W2, BIG)
        W = W2
        r = int(newid[r])


def in_tree_brute(W, r):
    """Minimum weight over ALL spanning in-trees rooted at r, by enumeration of all choices of out-edges."""
    m = len(W)
    others = [u for u in range(m) if u != r]
    best = None
    for ch in itertools.product(range(m), repeat=len(others)):
        par = dict(zip(others, ch))
        if any(u == v for u, v in par.items()):
            continue
        ok = True
        for u in others:      # every node must reach r
            seen = set()
            x = u
            while x != r and x not in seen:
                seen.add(x)
                x = par[x]
            if x != r:
                ok = False
                break
        if not ok:
            continue
        w = sum(W[u][par[u]] for u in others)
        if best is None or w < best:
            best = w
    return best


def rot(x, n, s=1):
    """sigma^s x, where (sigma x)_i = x_{i-1}: the content of cell i moves to cell i+1."""
    s %= n
    return ((x << s) | (x >> (n - s))) & ((1 << n) - 1)


def word(x, n):
    """State as the word x_0 x_1 ... x_{n-1}."""
    return "".join(str((int(x) >> i) & 1) for i in range(n))


def from_word(w):
    return sum(1 << i for i, ch in enumerate(w) if ch == "1")
