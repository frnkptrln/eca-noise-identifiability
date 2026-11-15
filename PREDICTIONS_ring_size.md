# Predictions for the ring-size study (sealed before any new computation)

Branch `ring-size-mechanisms`, written on 2026-11-13 before any new computation, from the v0.2 data
(`data/fw_sweep.csv`, n = 4..20) and the rule tables alone. The literature review (step 0)
was running while this file was written; nothing below depends on it. The file is committed
before the first new computation and is not edited afterwards. The outcome of each prediction goes
into `report_ring_size.md`, not into this file.

Conventions as in `note/note_v0.2.tex`: code c = 4 x_{i-1} + 2 x_i + x_{i+1}; a noise-selected
cycle has minimum stochastic potential gamma; k* = 0 iff the noise-selected cycles jointly contain
all eight codes. "Crystal" = a cycle whose states are spatially periodic with a period p that is
smaller than n. Tags used in the report: proved / computed / observed.

## General statements expected to be proved (for all n)

G1. Closure: if C is noise-selected and V(C, C') = 1, then C' is noise-selected (re-rooting an
    optimal in-tree along an edge of weight 1 never increases its weight). Expected: proved.
G2. Two-level criterion: let A be a rotation orbit of cycles with V(A_i, C) >= 2 for every C != A_i,
    and suppose every cycle reaches A_1 in the graph whose edges are the weight-1 edges out of
    cycles not in A and the weight-2 edges out of cycles in A. Then the noise-selected cycles are
    exactly A, and gamma_min = m + |A| - 2 (m = number of cycles). This is the step-by-step
    (one-flip-at-a-time) argument; it does not need the direct entry cost V(C, A_1), which can grow
    with n. Expected: proved. (Ellison's modified coradius gives the same conclusion; it is cited
    only if read in this session.)
G3. Incommensurability: for a fixed rule and code c, the ring configurations whose whole forward
    orbit avoids c form a sofic/finite-type language; if every cycle of its finite graph
    has length divisible by p, then for p not dividing n no cycle of F on Z/nZ avoids c.
    Expected: proved by a finite, machine-checked certificate, for every class where it applies.

## The 13 switching classes (n >= 8)

For each class: the expected mechanism, the expected period p, and whether I expect a proof for
all n of each direction. "Direction +": the condition on n implies k* >= 1; "direction 0": its
negation implies k* = 0.

| class | v0.2 pattern | expected mechanism | proof for all n expected? |
|---|---|---|---|
| 94 | k* >= 1 iff 3 \| n | crystal capture, p = 3: the fixed point (011)^{n/3} (3 shifts, codes 3, 5, 6) is selected alone | direction 0: yes (G3 + G1). Direction +: radius of the crystal = 2: yes; reachability of the crystal from every cycle by one-flip steps (G2): only if the cycles admit a finite block description; I expect "explained, not proved" |
| 43 | k* >= 1 iff 4 \| n | crystal capture, p = 4: the travelling wave (0011)^{n/4} (codes 1, 3, 4, 6; temporal period 4) is selected alone | as for 94 |
| 142 | k* >= 1 iff 4 \| n | crystal capture with the same crystal (0011)^{n/4} as class 43: rules 43 and 142 agree on codes 1, 3, 4, 6 and differ exactly on the four codes the crystal misses | as for 94 |
| 35 | k* >= 1 iff 3 \| n | not crystal capture. The missing code at 3 \| n is 5 (101). Expected mechanism ("crystal exclusion"): at 3 \| n code 101 occurs only on cycles built from a 3-periodic pattern, which have radius 1 and are not selected; at 3 ∤ n the incommensurate cycles carry 101 in defects and are selected | no proof expected for direction +; direction 0 possibly via G3 for codes other than 101 plus an explicit check of the 101-carrying cycles |
| 122 | k* = 0 iff 4 \| n | inverted crystal capture ("crystal completion"): at 4 \| n a cycle with spatial period 4 that carries code 2 (010) is selected; at 4 ∤ n code 010 is missing from the selected cycles | no proof expected for either direction |
| 60, 90 | k* >= 1 iff n = 2^k | nilpotency at n = 2^k (Proposition 1 of v0.2): the zero state is the only cycle, a crystal of period 1 | already proved (v0.2) |
| 154 | k* >= 1 iff n = 2^k (n <= 20) | inherited from rule 90: rule 154 = rule 90 XOR (l AND c), so F_154 = F_90 on every configuration without two adjacent 1s. A single flip of the zero state creates a rule-90 light cone that stays on one parity sublattice and dies at n = 2^k: the zero state cannot be left with one flip at n = 2^k (radius >= 2), and can be at even n that are not powers of two. At n = 2^k every other cycle reaches 0 by one-flip steps, so 0 is selected alone (G2) | radius part: proved for all n = 2^k. Odd n: F_154 bijective, k* = 0, proof expected. Even n not a power of two: k* = 0 expected; proof expected only if all cycles are shown to be mutually reachable by one-flip steps. Reachability of 0 at n = 2^k for all k: not expected in full; to be tested at n = 32 by a method that does not enumerate 2^32 states |
| 22, 26, 37, 45, 73 | no divisibility pattern | see below | no proof required or expected |

### Specific predictions, n = 8..20 (to be checked against new mechanism data)

P1 (94). At 3 \| n the noise-selected set is exactly the 3 shifts of (011)^{n/3}; its radius is 2;
    every other cycle has radius 1; the one-flip graph between cycles has a single closed class,
    the crystal orbit. At 3 ∤ n no cycle avoids all of codes 0, 1, 2, 4, 7.
P2 (43, 142). At 4 \| n the noise-selected set is exactly the rotation orbit of the travelling wave
    (0011)^{n/4} (one cycle of temporal period 4); radius 2; all other cycles radius 1; single
    closed class. At 4 ∤ n no cycle has spatial period 4.
P3 (35). At 3 \| n the cycles that contain code 5 are exactly the cycles that are not selected
    (11 of 12 selected at n = 9, 700 of 710 at n = 18), and each of them has spatial period 3 or
    consists of 3-periodic segments. Crystal capture is falsified for class 35 (already known).
P4 (122). At 4 \| n some noise-selected cycle has spatial period 4 and carries code 2; at 4 ∤ n
    the missing code is 2 for n in {9, 10, 11, 13, 17, 18, 19} (as in v0.2) and the selected cycles
    at n = 14, 15 are the uniform states (codes 0, 2, 5 at n = 14 and code 0 at n = 15, as in v0.2)
    with a different mechanism (zero state with radius >= 2).
P5 (154). At even n not a power of two, every cycle has radius 1 and the one-flip graph between
    cycles is strongly connected (all cycles selected, as in v0.2); at n = 8, 16 the zero state has
    radius 2, every other cycle has radius 1, and {0} is the single closed class.
P6 (22, 26). The switches of class 22 (k* = 1 at n = 8, 14, 15, 16; 0 at 9..13, 17..20) coincide with
    the zero state having radius >= 2, i.e. with the single-flip orbit of the zero state returning to
    the zero state on the ring of size n. For class 26 the same holds at n = 16 (k* = 2, zero state
    alone); at the other n with k* = 1 the missing code is 7 (111) with a different mechanism.
P7 (45). The switch at n = 8 is the 2-cycle of the uniform states being selected alone; at odd n
    F_45 is bijective (k* = 0); at even n >= 10 the uniform 2-cycle has radius 1.
P8 (37, 73). No crystal of a fixed period explains the switches. For class 37, n = 8..20 fit
    "k* = 0 iff n mod 6 in {0, 5}" (low confidence; two repetitions only). For class 73 the only
    switch for n >= 8 is n = 9 (code 7 missing).

### Predicted k* at n = 21 and 22 (where computed)

| class | 21 | 22 | basis |
|---|---|---|---|
| 35 | 1 | 0 | 3 \| n |
| 94 | 1 | 0 | 3 \| n |
| 43 | 0 | 0 | 4 ∤ n |
| 142 | 0 | 0 | 4 ∤ n |
| 122 | 1 | 1 | 4 ∤ n |
| 60, 90 | 0 | 0 | Proposition 1 |
| 154 | 0 | 0 | odd: bijective; 22 not a power of two |
| 45 | 0 | 0 | odd: bijective; even n >= 10: k* = 0 |
| 73 | 0 | 0 | k* = 0 for all n >= 10 so far |
| 37 | 1 | 1 | low-confidence mod-6 fit |
| 22 | single-flip orbit criterion (P6) | same | conditional prediction: k* = 1 iff the single-flip orbit of 0 returns to 0 |
| 26 | no prediction | no prediction | |

### Rule 154 beyond n = 20

P9. At n = 32 (and 64), the zero state has radius >= 2 (to be proved for all n = 2^k), and every
    cycle reached from sampled initial states reaches the zero state by one-flip steps; hence I
    predict k* = 1 at n = 32. At n = 24 and 28, k* = 0.
