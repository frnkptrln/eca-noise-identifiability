/* core.c -- independent verification core for noisy ECA on a ring.
 *
 * State encoding: a configuration x_0 x_1 ... x_{n-1} is the integer
 *   X = sum_i x_i 2^(n-1-i)      (x_0 is the most significant bit),
 * i.e. the bit string read as a binary numeral.  Cell i sits at bit position
 * p = n-1-i; its left neighbour x_{i-1} is bit p+1 (mod n), its right
 * neighbour x_{i+1} is bit p-1 (mod n).
 * Neighbourhood code at cell i: 4 x_{i-1} + 2 x_i + x_{i+1}.
 * Rule number N: f(a,b,c) = bit (4a+2b+c) of N.
 */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef uint32_t u32;
typedef int32_t i32;
typedef uint8_t u8;
typedef int64_t i64;

static inline u32 rotl1(u32 x, int n) { /* string rotated left: (x_1 ... x_{n-1} x_0) */
    u32 mask = (n == 32) ? 0xffffffffu : ((1u << n) - 1u);
    return ((x << 1) | (x >> (n - 1))) & mask;
}
static inline u32 rotr1(u32 x, int n) { /* string rotated right: (x_{n-1} x_0 ... x_{n-2}) */
    return (x >> 1) | ((x & 1u) << (n - 1));
}

/* Global map table and the set of neighbourhood codes present in each state. */
void build_F(int rule, int n, u32 *F, u8 *codemask) {
    u32 N = 1u << n, mask = N - 1u;
    for (u32 X = 0; X < N; X++) {
        u32 A = rotr1(X, n); /* bit p = bit p+1 of X = left neighbour  */
        u32 B = X;
        u32 C = rotl1(X, n); /* bit p = bit p-1 of X = right neighbour */
        u32 out = 0;
        u8 cm = 0;
        for (int code = 0; code < 8; code++) {
            u32 sel = ((code & 4) ? A : ~A) & ((code & 2) ? B : ~B) & ((code & 1) ? C : ~C) & mask;
            if (sel) cm |= (u8)(1u << code);
            if ((rule >> code) & 1) out |= sel;
        }
        F[X] = out;
        codemask[X] = cm;
    }
}

/* Periodic orbits (cycles) of F and basins.
 * cyc[x]  = cycle id if x is periodic, else -1
 * attr[x] = id of the cycle that x falls into under F
 * minstate[c] = numerically smallest state on cycle c, len[c] = its length,
 * ccodes[c] = set of codes occurring on cycle c.
 * Returns the number of cycles.  Output arrays need capacity 2^n. */
int find_cycles(int n, const u32 *F, i32 *cyc, i32 *attr, u32 *minstate, i32 *len, u8 *ccodes,
                const u8 *codemask) {
    u32 N = 1u << n;
    u32 *stack = (u32 *)malloc(sizeof(u32) * N);
    for (u32 x = 0; x < N; x++) { cyc[x] = -1; attr[x] = -1; }
    int m = 0;
    for (u32 x = 0; x < N; x++) {
        if (attr[x] != -1) continue;
        u32 sp = 0, y = x;
        while (attr[y] == -1) { attr[y] = -2; stack[sp++] = y; y = F[y]; }
        i32 a;
        if (attr[y] == -2) { /* closed a new cycle through y */
            u32 z = y, mn = y; i32 L = 0; u8 cm = 0;
            do { cyc[z] = m; attr[z] = m; if (z < mn) mn = z; cm |= codemask[z]; L++; z = F[z]; } while (z != y);
            minstate[m] = mn; len[m] = L; ccodes[m] = cm;
            a = m; m++;
        } else a = attr[y];
        for (u32 k = 0; k < sp; k++) if (attr[stack[k]] == -2) attr[stack[k]] = a;
    }
    free(stack);
    return m;
}

/* Rotation action on cycles: rot1[c] = id of the cycle obtained by rotating
 * every state of c one step to the left.  orb[c] = orbit id, reps[o] = one
 * cycle of orbit o, orbsize[o] = number of cycles, orbmin[o] = smallest state
 * over all cycles of the orbit.  Returns the number of orbits. */
int rotation_orbits(int n, int m, const i32 *cyc, const u32 *minstate, i32 *rot1, i32 *orb, i32 *reps,
                    i32 *orbsize, u32 *orbmin) {
    for (int c = 0; c < m; c++) { rot1[c] = cyc[rotl1(minstate[c], n)]; orb[c] = -1; }
    int no = 0;
    for (int c = 0; c < m; c++) {
        if (orb[c] != -1) continue;
        int d = c, sz = 0; u32 mn = minstate[c];
        do { orb[d] = no; sz++; if (minstate[d] < mn) mn = minstate[d]; d = rot1[d]; } while (d != c);
        reps[no] = c; orbsize[no] = sz; orbmin[no] = mn; no++;
    }
    return no;
}

/* Per-cycle geometry starting from state x (must be the smallest state over
 * the cycle and all rotations): spatial period, the smallest t>0 with F^t x a
 * rotation of x, and the smallest s>=0 with F^t x = sigma^s x where
 * (sigma x)_i = x_{i-1} (string rotated right by one). */
static u32 canon(u32 y, int n) { u32 b = y, z = y; for (int k = 1; k < n; k++) { z = rotl1(z, n); if (z < b) b = z; } return b; }
void cycle_geometry(int n, const u32 *F, int count, const u32 *x0, i32 *sper, i32 *trot, i32 *srot) {
    for (int k = 0; k < count; k++) {
        u32 x = x0[k];
        int s = 1; u32 z = rotr1(x, n);
        while (z != x) { z = rotr1(z, n); s++; }
        sper[k] = s;
        int pc = __builtin_popcount(x);
        u32 y = F[x]; int t = 1;
        while (!(__builtin_popcount(y) == pc && canon(y, n) == x)) { y = F[y]; t++; }
        trot[k] = t;
        int r = 0; z = x;
        while (z != y) { z = rotr1(z, n); r++; }
        srot[k] = r;
    }
}

/* One-flip graph G1, sparse definition: C -> C' (C != C') iff some state v of
 * C and some cell i have v with cell i flipped in the basin of C'.
 * If src==NULL only counts.  stamp needs capacity m.  Returns #edges. */
i64 g1_edges(int n, const u32 *F, const i32 *attr, int m, const u32 *minstate, const i32 *len, i32 *src,
             i32 *dst) {
    i32 *stamp = (i32 *)malloc(sizeof(i32) * (size_t)m);
    for (int c = 0; c < m; c++) stamp[c] = -1;
    i64 ne = 0;
    for (int c = 0; c < m; c++) {
        u32 v = minstate[c];
        for (i32 k = 0; k < len[c]; k++) {
            for (int i = 0; i < n; i++) {
                i32 t = attr[v ^ (1u << i)];
                if (t != c && stamp[t] != c) { stamp[t] = c; if (src) { src[ne] = c; dst[ne] = t; } ne++; }
            }
            v = F[v];
        }
    }
    free(stamp);
    return ne;
}

/* Minimum resistance R(C -> x) from the cycle through s0 to every state x.
 * Because the source set C satisfies F(C) = C, R(C -> .) is the shortest-path
 * distance in the graph with arcs x -> F(x) (cost 0) and x -> x xor e_i
 * (cost 1): a step x -> F(x) xor z of resistance |z| is "apply F, then flip
 * the cells of z one at a time", and every state reached is either a source
 * (which has a preimage in C) or was itself produced by such a step.
 * Dial's algorithm with two buffers.  dist: u8[2^n]; qa,qb: u32[2^n]. */
static void bfs_cycle(int n, const u32 *F, u32 s0, u8 *dist, u32 *qa, u32 *qb) {
    u32 N = 1u << n;
    memset(dist, 255, N);
    u32 *cur = qa, *nxt = qb; u32 nc = 0, nn = 0;
    u32 z = s0;
    do { dist[z] = 0; cur[nc++] = z; z = F[z]; } while (z != s0);
    int d = 0;
    while (nc) {
        nn = 0;
        for (u32 i = 0; i < nc; i++) {
            u32 w = cur[i];
            if (dist[w] != d) continue; /* stale entry */
            u32 y = F[w];
            if (dist[y] > d) { dist[y] = (u8)d; cur[nc++] = y; }
            for (int b = 0; b < n; b++) {
                u32 v = w ^ (1u << b);
                if (dist[v] > d + 1) { dist[v] = (u8)(d + 1); nxt[nn++] = v; }
            }
        }
        u32 *t = cur; cur = nxt; nxt = t; nc = nn; d++;
    }
}

/* Single BFS exposed for validation: fills dist. */
void bfs_from_cycle(int n, const u32 *F, u32 s0, u8 *dist) {
    u32 N = 1u << n;
    u32 *qa = (u32 *)malloc(sizeof(u32) * N), *qb = (u32 *)malloc(sizeof(u32) * N);
    bfs_cycle(n, F, s0, dist, qa, qb);
    free(qa); free(qb);
}

/* V matrix (m x m, u8, row-major: V[c*m+c'] = V(c,c')) and code distances.
 * For each listed source cycle reps[k]: BFS, row over all cycles, and
 * kd[k*8+code] = min resistance from the cycle to a state containing code.
 * If use_rot != 0 the row is copied to all rotations of the source cycle via
 * V(sigma C, sigma C') = V(C, C'); otherwise only row reps[k] is written. */
void compute_V(int n, const u32 *F, const i32 *cyc, const u8 *codemask, int m, const u32 *minstate,
               const i32 *rot1, const i32 *reps, int nreps, int use_rot, u8 *V, u8 *kd) {
    u32 N = 1u << n;
    u8 *dist = (u8 *)malloc(N);
    u32 *qa = (u32 *)malloc(sizeof(u32) * N), *qb = (u32 *)malloc(sizeof(u32) * N);
    u8 *row = (u8 *)malloc((size_t)m);
    i32 *perm = (i32 *)malloc(sizeof(i32) * (size_t)m);
    for (int k = 0; k < nreps; k++) {
        int r = reps[k];
        bfs_cycle(n, F, minstate[r], dist, qa, qb);
        memset(row, 255, (size_t)m);
        u8 orm[64]; memset(orm, 0, 64);
        for (u32 x = 0; x < N; x++) {
            u8 dx = dist[x];
            i32 c = cyc[x];
            if (c >= 0 && dx < row[c]) row[c] = dx;
            orm[dx < 63 ? dx : 63] |= codemask[x];
        }
        for (int code = 0; code < 8; code++) {
            int best = 255;
            for (int d = 0; d < 64; d++) if (orm[d] & (1u << code)) { best = d; break; }
            kd[k * 8 + code] = (u8)best;
        }
        if (!use_rot) { memcpy(V + (size_t)r * m, row, (size_t)m); continue; }
        for (int c = 0; c < m; c++) perm[c] = c;
        int cr = r;
        do {
            u8 *dstrow = V + (size_t)cr * m;
            for (int c = 0; c < m; c++) dstrow[perm[c]] = row[c];
            cr = rot1[cr];
            for (int c = 0; c < m; c++) perm[c] = rot1[perm[c]];
        } while (cr != r);
    }
    free(dist); free(qa); free(qb); free(row); free(perm);
}

/* Stochastic potentials for ALL roots at once.
 * gamma[r] = minimum weight of a spanning in-tree rooted at r in the complete
 * digraph with weights W[i*m+j] (arc i -> j).  Full Edmonds contraction along
 * a growing path (every node chooses its cheapest outgoing arc; a closed loop
 * of choices is contracted with reduced weights) until one super-node is
 * left; rho(v) = reduced weight of the arc chosen by tree node v.  For root r
 * exactly the choices of the tree nodes containing r are dropped, hence
 *   gamma(r) = sum_v rho(v) - sum_{v contains r} rho(v).
 * W is destroyed. */
int edmonds_all_roots(int m, u8 *W, i64 *gamma) {
    if (m == 1) { gamma[0] = 0; return 0; }
    i32 *act = (i32 *)malloc(sizeof(i32) * (size_t)m), *pos = (i32 *)malloc(sizeof(i32) * (size_t)m);
    i32 *tid = (i32 *)malloc(sizeof(i32) * (size_t)m), *path = (i32 *)malloc(sizeof(i32) * (size_t)m);
    i32 *onpath = (i32 *)malloc(sizeof(i32) * (size_t)m);
    i32 *parent = (i32 *)malloc(sizeof(i32) * (size_t)(2 * m));
    i64 *rho = (i64 *)calloc((size_t)(2 * m), sizeof(i64));
    int nact = m, ntree = m, np = 0;
    for (int i = 0; i < m; i++) { act[i] = i; pos[i] = i; tid[i] = i; onpath[i] = -1; }
    for (int i = 0; i < 2 * m; i++) parent[i] = -1;
    path[np] = 0; onpath[0] = np; np++;
    while (nact > 1) {
        int v = path[np - 1];
        u8 *rv = W + (size_t)v * m;
        int best = 256, u = -1;
        for (int a = 0; a < nact; a++) { int j = act[a]; if (j != v && rv[j] < best) { best = rv[j]; u = j; } }
        rho[tid[v]] = best;
        if (best) for (int a = 0; a < nact; a++) { int j = act[a]; if (j != v) rv[j] = (u8)(rv[j] - best); }
        if (onpath[u] < 0) { path[np] = u; onpath[u] = np; np++; continue; }
        int pu = onpath[u], t = ntree++;
        for (int q = pu; q < np; q++) parent[tid[path[q]]] = t;
        for (int q = pu + 1; q < np; q++) { /* remove the other members from the active list */
            int w = path[q]; int pw = pos[w]; int last = act[nact - 1];
            act[pw] = last; pos[last] = pw; nact--; onpath[w] = -1;
        }
        u8 *ru = W + (size_t)u * m;
        for (int q = pu + 1; q < np; q++) {
            int w = path[q]; u8 *rw = W + (size_t)w * m;
            for (int a = 0; a < nact; a++) {
                int j = act[a]; if (j == u) continue;
                if (rw[j] < ru[j]) ru[j] = rw[j];
                u8 *rj = W + (size_t)j * m;
                if (rj[w] < rj[u]) rj[u] = rj[w];
            }
        }
        tid[u] = t; np = pu + 1;
    }
    i64 total = 0;
    for (int t = 0; t < ntree - 1; t++) total += rho[t];
    i64 *acc = (i64 *)calloc((size_t)ntree, sizeof(i64));
    for (int t = ntree - 2; t >= 0; t--) acc[t] = rho[t] + (parent[t] >= 0 ? acc[parent[t]] : 0);
    for (int r = 0; r < m; r++) gamma[r] = total - acc[r];
    int nt = ntree;
    free(act); free(pos); free(tid); free(path); free(onpath); free(parent); free(rho); free(acc);
    return nt;
}
