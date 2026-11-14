/* p2core.c -- additional routines for phase 2 of the ring-size verification.
 * State encoding as in ../core.c: x_0 is the most significant bit of the n-bit integer. */
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
typedef uint32_t u32; typedef int32_t i32; typedef uint8_t u8; typedef int64_t i64; typedef uint64_t u64;

/* dist[x] = minimum total resistance of a path from x to the set {target != 0}, in the arc model
 * x -> F(x) (cost 0), x -> x xor e_i (cost 1).  Reverse 0-1 search over F-preimages and flips. */
void dist_to_set(int n, const u32 *F, const u8 *target, u8 *dist) {
    u32 N = 1u << n;
    u32 *start = (u32 *)calloc((size_t)N + 1, sizeof(u32));
    u32 *pre = (u32 *)malloc(sizeof(u32) * (size_t)N);
    for (u32 x = 0; x < N; x++) start[F[x] + 1]++;
    for (u32 x = 0; x < N; x++) start[x + 1] += start[x];
    u32 *fill = (u32 *)malloc(sizeof(u32) * (size_t)N);
    memcpy(fill, start, sizeof(u32) * (size_t)N);
    for (u32 x = 0; x < N; x++) pre[fill[F[x]]++] = x;
    free(fill);
    u32 *qa = (u32 *)malloc(sizeof(u32) * (size_t)N), *qb = (u32 *)malloc(sizeof(u32) * (size_t)N);
    memset(dist, 255, N);
    u32 *cur = qa, *nxt = qb; u32 nc = 0, nn = 0;
    for (u32 x = 0; x < N; x++) if (target[x]) { dist[x] = 0; cur[nc++] = x; }
    int d = 0;
    while (nc) {
        nn = 0;
        for (u32 i = 0; i < nc; i++) {
            u32 w = cur[i];
            if (dist[w] != d) continue;
            for (u32 k = start[w]; k < start[w + 1]; k++) { u32 y = pre[k]; if (dist[y] > d) { dist[y] = (u8)d; cur[nc++] = y; } }
            for (int b = 0; b < n; b++) { u32 v = w ^ (1u << b); if (dist[v] > d + 1) { dist[v] = (u8)(d + 1); nxt[nn++] = v; } }
        }
        u32 *t = cur; cur = nxt; nxt = t; nc = nn; d++;
    }
    free(start); free(pre); free(qa); free(qb);
}
