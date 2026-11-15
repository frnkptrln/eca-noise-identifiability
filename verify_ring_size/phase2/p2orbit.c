/* p2orbit.c -- single orbits of an elementary CA on a ring of n <= 256 cells without enumerating states.
 * Encoding: cell i is bit (i mod 64) of word i/64.  Code at cell i: 4 x_{i-1} + 2 x_i + x_{i+1};
 * rule number N: f(a,b,c) = bit (4a+2b+c) of N. */
#include <stdint.h>
#include <string.h>
typedef uint64_t u64;
#define W 4
typedef struct { u64 w[W]; } st;

static inline void step(int rule, int n, const st *x, st *y) {
    st L, R;                                   /* L_i = x_{i-1}, R_i = x_{i+1} */
    int top = (n - 1) >> 6, tb = (n - 1) & 63;
    u64 carry = (x->w[top] >> tb) & 1u;        /* x_{n-1} enters at cell 0 */
    for (int k = 0; k < W; k++) { u64 v = x->w[k]; L.w[k] = (v << 1) | carry; carry = v >> 63; }
    u64 low = x->w[0] & 1u;                    /* x_0 enters at cell n-1 */
    for (int k = 0; k < W; k++) { u64 nxt = (k + 1 < W) ? x->w[k + 1] : 0; R.w[k] = (x->w[k] >> 1) | (nxt << 63); }
    R.w[top] |= low << tb;
    for (int k = 0; k < W; k++) {
        u64 a = L.w[k], b = x->w[k], c = R.w[k], o = 0;
        for (int code = 0; code < 8; code++) if ((rule >> code) & 1)
            o |= ((code & 4) ? a : ~a) & ((code & 2) ? b : ~b) & ((code & 1) ? c : ~c);
        y->w[k] = o;
    }
    /* mask to n bits */
    for (int k = top + 1; k < W; k++) y->w[k] = 0;
    if (tb < 63) y->w[top] &= ((u64)1 << (tb + 1)) - 1;
}
static inline int eq(const st *a, const st *b) { return memcmp(a, b, sizeof(st)) == 0; }
static inline int iszero(const st *a) { return (a->w[0] | a->w[1] | a->w[2] | a->w[3]) == 0; }

/* k steps from x (in place) */
void iterate(int rule, int n, u64 *x, u64 k) {
    st a, b; memcpy(&a, x, sizeof(st));
    for (u64 i = 0; i < k; i++) { step(rule, n, &a, &b); a = b; }
    memcpy(x, &a, sizeof(st));
}

/* Orbit of x0: mu = index of the first state on the limit cycle, lam = its length, zero = 1 if the limit
 * cycle is the fixed point 0 (requires f(000) = 0).  Brent's algorithm; gives up (return 0) once more than
 * max_steps map evaluations were used in the search for lam, or 3*max_steps in total. */
int orbit(int rule, int n, const u64 *x0, u64 max_steps, u64 *mu, u64 *lam, int *zero, u64 *used) {
    st t, h, tmp; memcpy(&t, x0, sizeof(st));
    u64 steps = 0, power = 1, l = 1;
    step(rule, n, &t, &h); steps++;
    while (!eq(&t, &h)) {
        if (power == l) { t = h; power <<= 1; l = 0; }
        step(rule, n, &h, &tmp); h = tmp; steps++; l++;
        if (steps > max_steps) { *used = steps; return 0; }
    }
    *lam = l;
    memcpy(&t, x0, sizeof(st)); h = t;
    for (u64 i = 0; i < l; i++) { step(rule, n, &h, &tmp); h = tmp; steps++; }
    u64 m = 0;
    while (!eq(&t, &h)) { step(rule, n, &t, &tmp); t = tmp; step(rule, n, &h, &tmp); h = tmp; m++; steps += 2; }
    *mu = m; *zero = iszero(&t); *used = steps;
    return 1;
}
