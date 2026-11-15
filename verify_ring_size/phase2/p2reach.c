/* p2reach.c -- limit cycle of a state on a ring of n <= 64 cells (cell i = bit i), with the label used for
 * sampled reachability: the numerically smallest state on the limit cycle, its length, and
 * h = min over the cycle states of the number of cells whose neighbourhood code is not in `allowed`. */
#include <stdint.h>
typedef uint64_t u64;
static inline u64 step(int rule, int n, u64 x) {
    u64 mask = (n == 64) ? ~(u64)0 : (((u64)1 << n) - 1);
    u64 L = ((x << 1) | (x >> (n - 1))) & mask, R = (x >> 1) | ((x & 1) << (n - 1)), o = 0;
    for (int code = 0; code < 8; code++) if ((rule >> code) & 1)
        o |= ((code & 4) ? L : ~L) & ((code & 2) ? x : ~x) & ((code & 1) ? R : ~R);
    return o & mask;
}
static inline int bad_cells(int n, u64 x, int allowed) {
    u64 mask = (n == 64) ? ~(u64)0 : (((u64)1 << n) - 1);
    u64 L = ((x << 1) | (x >> (n - 1))) & mask, R = (x >> 1) | ((x & 1) << (n - 1)), ok = 0;
    for (int code = 0; code < 8; code++) if ((allowed >> code) & 1)
        ok |= ((code & 4) ? L : ~L) & ((code & 2) ? x : ~x) & ((code & 1) ? R : ~R);
    return n - __builtin_popcountll(ok & mask);
}
/* returns 1 on success; label = smallest state on the limit cycle of x */
int limit_info(int rule, int n, u64 x, u64 max_steps, int allowed, u64 *label, u64 *period, int *h, u64 *transient) {
    u64 t = x, hh = step(rule, n, x), power = 1, lam = 1, steps = 1;
    while (t != hh) {
        if (power == lam) { t = hh; power <<= 1; lam = 0; }
        hh = step(rule, n, hh); lam++; steps++;
        if (steps > max_steps) return 0;
    }
    t = x; hh = x;
    for (u64 i = 0; i < lam; i++) hh = step(rule, n, hh);
    u64 mu = 0;
    while (t != hh) { t = step(rule, n, t); hh = step(rule, n, hh); mu++; }
    u64 best = t, y = t; int hb = bad_cells(n, t, allowed);
    for (u64 i = 1; i < lam; i++) { y = step(rule, n, y); if (y < best) best = y; int b = bad_cells(n, y, allowed); if (b < hb) hb = b; }
    *label = best; *period = lam; *h = hb; *transient = mu;
    return 1;
}
/* all one-flip successors of the cycle through x0 (period P): writes up to cap entries (label, state, cell, h).
 * Returns the number of (state, cell) pairs examined, or -1 if an orbit exceeded max_steps. */
long successors(int rule, int n, u64 x0, u64 P, u64 max_steps, int allowed, long cap, u64 *lab, u64 *st, int *cell,
                int *hv, long *count) {
    u64 x = x0; long k = 0, seen = 0;
    for (u64 i = 0; i < P; i++) {
        for (int j = 0; j < n; j++) {
            u64 l, p, mu; int h;
            if (!limit_info(rule, n, x ^ ((u64)1 << j), max_steps, allowed, &l, &p, &h, &mu)) return -1;
            seen++;
            int dup = 0;
            for (long q = 0; q < k; q++) if (lab[q] == l) { dup = 1; break; }
            if (!dup && k < cap) { lab[k] = l; st[k] = x; cell[k] = j; hv[k] = h; k++; }
        }
        x = step(rule, n, x);
    }
    *count = k;
    return seen;
}
