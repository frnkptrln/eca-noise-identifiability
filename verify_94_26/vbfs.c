/* Minimum path resistances from every cycle, by 0-1 BFS on a two-layer state graph.
   Layer A: the states x_t of a path. Layer B: "F applied, flips being made".
   A_x -> B_(F x) cost 0;  B_z -> B_(z + e_i) cost 1;  B_z -> A_z cost 0.
   A path x_0 .. x_T with total resistance sum_t H(F x_t, x_(t+1)) is a walk A_x0 -> ... -> A_xT of the same cost.
   V(C, C') = min over periodic states y of C' of dist(A_rep(C), A_y); since F-steps along C cost 0, one state
   of C suffices as the source. R(C -> D_c) = min over states y containing code c of dist(A_rep(C), A_y).

   input file (little endian): int32 n, int32 m, uint32 F[2^n], int32 label[2^n] (cycle id of a periodic state,
   -1 otherwise), uint8 codes[2^n] (bit c set iff the state contains code c), int32 reps[m]
   output file: int32 V[m*m], int32 R[m*8]
   usage: vbfs in.bin out.bin */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: vbfs in out\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    int32_t n, m;
    if (fread(&n, 4, 1, f) != 1 || fread(&m, 4, 1, f) != 1) return 2;
    uint32_t N = 1u << n;
    uint32_t *F = malloc(4 * (size_t)N);
    int32_t *lab = malloc(4 * (size_t)N);
    uint8_t *codes = malloc(N);
    int32_t *reps = malloc(4 * (size_t)m);
    if (fread(F, 4, N, f) != N || fread(lab, 4, N, f) != N || fread(codes, 1, N, f) != N ||
        fread(reps, 4, m, f) != (size_t)m) return 3;
    fclose(f);
    uint8_t *dA = malloc(N), *dB = malloc(N);
    /* node encoding: (x << 1) | layer, layer 0 = A, 1 = B */
    uint32_t *cur = malloc(4 * (size_t)N * 2 * (n + 2));
    uint32_t *nxt = malloc(4 * (size_t)N * 2 * (n + 2));
    int32_t *V = malloc(4 * (size_t)m * m);
    int32_t *R = malloc(4 * (size_t)m * 8);
    for (int s = 0; s < m; s++) {
        memset(dA, 255, N);
        memset(dB, 255, N);
        size_t nc = 0, nn = 0;
        uint32_t src = (uint32_t)reps[s];
        dA[src] = 0;
        cur[nc++] = src << 1;
        int d = 0;
        while (nc > 0) {
            while (nc > 0) {
                uint32_t node = cur[--nc];
                uint32_t x = node >> 1;
                if ((node & 1) == 0) {
                    if (dA[x] != d) continue;
                    uint32_t z = F[x];
                    if (dB[z] > d) { dB[z] = d; cur[nc++] = (z << 1) | 1; }
                } else {
                    if (dB[x] != d) continue;
                    if (dA[x] > d) { dA[x] = d; cur[nc++] = x << 1; }
                    for (int i = 0; i < n; i++) {
                        uint32_t z = x ^ (1u << i);
                        if (dB[z] > d + 1) { dB[z] = d + 1; nxt[nn++] = (z << 1) | 1; }
                    }
                }
            }
            uint32_t *t = cur; cur = nxt; nxt = t;
            nc = nn; nn = 0;
            d++;
        }
        for (int c = 0; c < m; c++) V[(size_t)s * m + c] = 1 << 30;
        for (int c = 0; c < 8; c++) R[(size_t)s * 8 + c] = 1 << 30;
        for (uint32_t y = 0; y < N; y++) {
            int dy = dA[y];
            if (lab[y] >= 0 && dy < V[(size_t)s * m + lab[y]]) V[(size_t)s * m + lab[y]] = dy;
            for (int c = 0; c < 8; c++)
                if (((codes[y] >> c) & 1) && dy < R[(size_t)s * 8 + c]) R[(size_t)s * 8 + c] = dy;
        }
    }
    FILE *g = fopen(argv[2], "wb");
    fwrite(V, 4, (size_t)m * m, g);
    fwrite(R, 4, (size_t)m * 8, g);
    fclose(g);
    return 0;
}
