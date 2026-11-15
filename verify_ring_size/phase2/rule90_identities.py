"""Step 3 (d): the orbit identities used in the proofs of Propositions R154 and R22, by direct simulation for
n <= 256 (not only the conclusions).  Writes out/rule90_identities.json."""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orbitlib as O

OUT = os.path.join(O.HERE, "out")
t0 = time.process_time()
res = {}

# ---- rule tables
agree = {r: [c for c in range(8) if ((r >> c) & 1) == ((90 >> c) & 1)] for r in (154, 26, 22, 122)}
res["codes_agreeing_with_rule_90"] = {str(k): v for k, v in agree.items()}
res["codes_without_two_adjacent_ones"] = [c for c in range(8) if not ((c & 6) == 6 or (c & 3) == 3)]
f22 = all(((22 >> (4 * a + 2 * b + c)) & 1) == ((a + b + c + a * b * c) % 2) == int(a + b + c == 1)
          for a in (0, 1) for b in (0, 1) for c in (0, 1))
res["rule22_is_exactly_one_and_a+b+c+abc"] = f22
f90 = all(((90 >> (4 * a + 2 * b + c)) & 1) == (a ^ c) for a in (0, 1) for b in (0, 1) for c in (0, 1))
res["rule90_is_a_xor_c"] = f90


def is_pow2(n):
    return n & (n - 1) == 0


def poly_orbit(n, t):
    """X^{-t} (1 + X)^{2t} in GF(2)[X]/(X^n - 1) as a bit mask (cell i = coefficient of X^i).
    Coefficient of X^k in (1+X)^{2t} is 1 iff k & ~(2t) == 0 (Lucas)."""
    m = 0
    e = 2 * t
    k = e
    while True:                      # all submasks k of e
        m ^= 1 << ((k - t) % n)
        if k == 0:
            break
        k = (k - 1) & e
    return m


def gf2_mod(a, b):
    db = b.bit_length()
    while a.bit_length() >= db:
        a ^= b << (a.bit_length() - db)
    return a


def gf2_gcd(a, b):
    while b:
        a, b = b, gf2_mod(a, b)
    return a


def gf2_pow1px(n):
    """(1 + X)^n over GF(2) as an integer bit mask."""
    m = 0
    k = n
    while True:
        m |= 1 << k
        if k == 0:
            break
        k = (k - 1) & n
    return m


# ---- algebra: X^n - 1 divides a power of (1 + X) iff n is a power of two (n = 2..256)
alg_bad = []
for n in range(2, 257):
    xn1 = (1 << n) | 1
    g = gf2_gcd(xn1, gf2_pow1px(1 << 9))          # (1+X)^512 = 1 + X^512; gcd keeps the (1+X)-power part of X^n - 1
    divides = (g == xn1)
    if divides != is_pow2(n):
        alg_bad.append(n)
    # factorisation n = 2^a m: X^n - 1 = (X^m - 1)^(2^a) and (X^m - 1)/(1 + X) has no root at 1 for m > 1 odd
    a = (n & -n).bit_length() - 1
    m = n >> a
    if m > 1:
        cof = sum(1 << i for i in range(m))        # 1 + X + ... + X^(m-1)
        if bin(cof).count("1") % 2 != 1:           # value at X = 1
            alg_bad.append(-n)
res["algebra_Xn-1_divides_power_of_1+X_iff_power_of_two"] = {"n_range": [2, 256], "failures": alg_bad}

# ---- R154: on even rings the orbits of e_0 under rules 90, 154, 26 coincide, lie on sites of parity t,
#      and equal X^{-t}(1+X)^{2t}; they die iff n is a power of two (first zero at t = n/2).
r154 = {"even_n": 0, "steps_checked": 0, "orbit_mismatch": [], "parity_violation": [], "poly_mismatch": [],
        "death_time_pow2": {}, "dies_at_non_pow2_within_T": [], "odd_n_orbits_differ_from_90_first_time": {}}
even_mask = {}
for n in range(4, 257, 2):
    T = max(4 * n, 1024)
    ev = sum(1 << i for i in range(0, n, 2))
    od = ev << 1
    a = b = c = 1
    died = None
    r154["even_n"] += 1
    for t in range(T + 1):
        if not (a == b == c):
            r154["orbit_mismatch"].append([n, t])
            break
        if a & (od if t % 2 == 0 else ev):
            r154["parity_violation"].append([n, t])
        if t <= n and a != poly_orbit(n, t):
            r154["poly_mismatch"].append([n, t])
        if a == 0 and died is None:
            died = t
        a, b, c = O.step(90, n, a), O.step(154, n, b), O.step(26, n, c)
        r154["steps_checked"] += 1
    if is_pow2(n):
        r154["death_time_pow2"][str(n)] = died
    elif died is not None:
        r154["dies_at_non_pow2_within_T"].append(n)
for n in (5, 7, 9, 11, 15, 31):
    a = b = c = 1
    for t in range(200):
        if not (a == b == c):
            r154["odd_n_orbits_differ_from_90_first_time"][str(n)] = t
            break
        a, b, c = O.step(90, n, a), O.step(154, n, b), O.step(26, n, c)
res["R154"] = r154

# ---- R22: on rings with 4 | n the rule-22 orbit of e_0 is R_t (t even) and R_t | R_{t-1} (t odd)
r22 = {"n_4_divides": 0, "steps_checked": 0, "identity_failures": [], "distance2_failures": [], "dilation_failures": [],
       "returns_iff_pow2_failures": [], "first_zero_time_pow2": {}, "identity_fails_first_time_other_n": {}}


def dilate(x, half):
    return sum(1 << (2 * i) for i in range(half) if (x >> i) & 1)


for n in range(4, 257):
    T = max(4 * n, 1024) if n % 4 == 0 else 64
    s = 1
    R = [1]
    half_orbit = [1]            # rule 90 on the ring of size n/2
    fail = None
    zero_at = None
    for t in range(T + 1):
        want = R[t] if t % 2 == 0 else (R[t] | R[t - 1])
        if s != want and fail is None:
            fail = t
        if s == 0 and zero_at is None:
            zero_at = t
        if n % 4 == 0 and t % 2 == 0:
            x = R[t]
            mask = (1 << n) - 1
            rot2 = ((x << 2) | (x >> (n - 2))) & mask
            if x & rot2:
                r22["distance2_failures"].append([n, t])
            while len(half_orbit) <= t // 2:
                half_orbit.append(O.step(90, n // 2, half_orbit[-1]))
            if x != dilate(half_orbit[t // 2], n // 2):
                r22["dilation_failures"].append([n, t])
        s = O.step(22, n, s)
        R.append(O.step(90, n, R[-1]))
        if n % 4 == 0:
            r22["steps_checked"] += 1
    if n % 4 == 0:
        r22["n_4_divides"] += 1
        if fail is not None:
            r22["identity_failures"].append([n, fail])
        if (zero_at is not None) != is_pow2(n):
            r22["returns_iff_pow2_failures"].append(n)
        if is_pow2(n):
            r22["first_zero_time_pow2"][str(n)] = zero_at
    elif n <= 40:
        r22["identity_fails_first_time_other_n"][str(n)] = fail
res["R22"] = r22
res["cpu_seconds"] = round(time.process_time() - t0, 2)
json.dump(res, open(os.path.join(OUT, "rule90_identities.json"), "w"), indent=1)
print(json.dumps(res)[:3500])
