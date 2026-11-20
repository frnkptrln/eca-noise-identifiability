# Own findings, written down before any comparison

Written on 20 November 2026 by the verifying session (Claude), after the tests T00 to T07 were written and T00 to T04
had been run in full, and BEFORE (a) the reports of the reading sub-sessions (paper against sources) were collected,
(b) any script of the repository was opened, (c) `paper/REFEREE_NOTES.md` was opened. Kept unchanged afterwards; the
final numbering is in `VERIFICATION_paper.md`.

## Read line by line as a referee (Part 1)

Section 2 (Lemmas 2.2 to 2.7, Theorem 2.8), Section 3.1 (Lemmas 3.2 to 3.8, Theorems 3.9 to 3.11), and for rule 94
the statements used by Theorem 3.43(i): Lemmas 3.29, 3.30, 3.31, 3.32, 3.34, 3.38, 3.39 with their proofs in
Appendix A, and part (i) of the proof of Theorem 3.43 (Steps 1 to 6). Every step was followed; the smallest ring
sizes (n = 3 and 4 for rule 154; n = 6 with the coinciding cells j-3 = j+3 for Lemma 3.32; n = 5 and n = 6 for the
windows of Lemmas 3.38 and 3.39) were followed by hand.

Result: no false statement and no gap found in these proofs.

## Points noted while reading

O1. Introduction, tex l. 93-95 ("Under rules 43 and 142 the state (0011)^(n/4), and under rule 94 the state
    (011)^(n/3), has a cycle that no single flip can leave and that every other cycle can reach by single flips; when
    it exists it is selected, alone or with its rotations."). No range of n is given. For rule 94 at n = 3 the state
    011 exists, a single flip leaves it (Remark 3.44 says so), and by my computation it is not selected: the selected
    set at n = 3 is {{0}} (k_v = 0,1,1,1,1,1,1,1). The sentence is true for n >= 6 (rule 94) and n >= 4 (rules 43,
    142) and needs these bounds.
O2. Remark 3.44, tex l. 1241: "For n = 3 and n = 4 nothing is proved (Lemma 3.31 needs n >= 5, Lemma 3.32 needs
    n >= 6)". By computation Lemma 3.31 holds at n = 4 as stated (all 14 states that are not fully frozen; in case (a)
    of its proof only j-2, j+2 not in {j-1, j, j+1} is used, which holds for n >= 4). What fails at n = 4 is Step 3 of
    part (ii) (no block word with a long block; the closed class carries only the codes 010 and 101) and
    Lemma 3.42. The parenthesis names a reason that is not the reason. Cosmetic.
O3. Lemma 3.4(b), tex l. 398-400: "it has degree q - 1 >= 2 and therefore has an irreducible factor different from
    z + 1". The conclusion is right; the reason is that the factor is not constant and not divisible by z + 1 (shown
    in the clause before); the degree bound is not what gives it. Cosmetic.
O4. Lemma 2.5, proof (tex l. 265): "N has no out-edge, so there is no directed circuit" is short: a circuit in a set
    of edges with at most one out-edge per node consists of nodes that never leave it, so none of them would reach N,
    against the sentence before. Correct, could be said. Cosmetic.
O5. Theorem 3.43(i) does not state gamma_min. Computed: gamma(A_i) = m + 1 at n = 6, 9, 12, 15, 18 (and so on, see
    T05). Not a finding; the paper does not claim a value (TRACE says so too).

## Computations done at this point (all pass)

T00 engine; T01 Section 2 on all 256 rules, n = 3..12; T02 Lemmas 3.2-3.8 (all states to n = 22, G1 to n = 16);
T03 Theorems 3.9-3.11 from the definitions, n = 3..18; T04 rule 94 lemmas; T05 (Theorem 3.43) passed for n = 3..19
and was still running for n = 20, 21 when this file was written; T06 and T07 passed on short ranges.
