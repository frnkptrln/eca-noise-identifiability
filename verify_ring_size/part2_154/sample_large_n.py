"""Sampled tests of the statements of PROOF_154.md on rings too large to enumerate (n = 32 .. 1024).

Not part of the proof.  For random states x with ones on both parity classes (the set M):
  (a) x is periodic; in fact F^n(x) = x (observation O1; not proved);
  (b) the explicit descent of Theorem 1: delete the ones of the minority parity class one at a time; every
      intermediate state is in M and periodic (tested through F^n = id), the last one lies on one parity class
      and reaches 0 after at most n/2 steps of F.
States are Python integers, x_0 = most significant bit.  Seeded; single process.
Output: out/sample_large_n.jsonl
"""
import json
import os
import random
import time

HERE = os.path.dirname(os.path.abspath(__file__))


def make_F(n):
    mask = (1 << n) - 1

    def F(x):
        c = ((x << 1) | (x >> (n - 1))) & mask      # c_i = x_(i+1)
        a = (x >> 1) | ((x & 1) << (n - 1))         # a_i = x_(i-1)
        return c ^ (a & ~x & mask)
    return F


def brute_F(x, n, rule=154):
    b = [(x >> (n - 1 - i)) & 1 for i in range(n)]
    y = 0
    for i in range(n):
        y = (y << 1) | ((rule >> (4 * b[i - 1] + 2 * b[i] + b[(i + 1) % n])) & 1)
    return y


def main():
    rng = random.Random(154)
    t0 = time.process_time()
    with open(os.path.join(HERE, "out", "sample_large_n.jsonl"), "w") as fh:
        for n, nsamp in ((32, 2000), (64, 1000), (128, 300), (256, 100), (512, 30), (1024, 10)):
            F = make_F(n)
            E_mask = sum(1 << (n - 1 - i) for i in range(0, n, 2))
            O_mask = sum(1 << (n - 1 - i) for i in range(1, n, 2))
            rec = {"n": n, "samples": nsamp, "F_matches_table_lookup": True, "in_M_after_F": 0,
                   "F_pow_n_identity": 0, "descent_states_tested": 0, "descent_states_periodic": 0,
                   "descent_reaches_zero_within_half_n": 0, "max_descent_length": 0}
            for s in range(nsamp):
                dens = rng.choice((0.05, 0.2, 0.5, 0.8, 0.95))
                x = 0
                for i in range(n):
                    x = (x << 1) | (rng.random() < dens)
                if x & E_mask == 0:
                    x |= 1 << (n - 1 - 2 * rng.randrange(n // 2))
                if x & O_mask == 0:
                    x |= 1 << (n - 2 - 2 * rng.randrange(n // 2))
                if s < 5:
                    rec["F_matches_table_lookup"] &= (F(x) == brute_F(x, n))
                y = F(x)
                rec["in_M_after_F"] += int(bool(y & E_mask) and bool(y & O_mask))
                for _ in range(n - 1):
                    y = F(y)
                rec["F_pow_n_identity"] += int(y == x)
                # descent on the first 20 samples of each n (cost n F-steps per intermediate state)
                if s < 20:
                    ev, od = bin(x & E_mask).count("1"), bin(x & O_mask).count("1")
                    minority = O_mask if od <= ev else E_mask
                    ones = [i for i in range(n) if (x & minority) >> (n - 1 - i) & 1]
                    z = x
                    for j, i in enumerate(ones):
                        z ^= 1 << (n - 1 - i)
                        if j < len(ones) - 1:
                            w = z
                            for _ in range(n):
                                w = F(w)
                            rec["descent_states_tested"] += 1
                            rec["descent_states_periodic"] += int(w == z)
                    rec["max_descent_length"] = max(rec["max_descent_length"], len(ones))
                    w = z
                    for _ in range(n // 2):
                        w = F(w)
                    rec["descent_reaches_zero_within_half_n"] += int(w == 0)
            rec["descent_samples"] = min(nsamp, 20)
            rec["cpu_seconds_cumulative"] = round(time.process_time() - t0, 2)
            fh.write(json.dumps(rec, sort_keys=True) + "\n")
            fh.flush()
            print(rec)


if __name__ == "__main__":
    main()
