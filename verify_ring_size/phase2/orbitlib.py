"""Single-orbit tools: Python big-integer CA step (cell i = bit i) and ctypes bindings for p2orbit.c."""
import ctypes as C
import os
import subprocess
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(HERE, "p2orbit.c")
_LIB = os.path.join(HERE, "build", "p2orbit.dylib")
os.makedirs(os.path.dirname(_LIB), exist_ok=True)
if (not os.path.exists(_LIB)) or os.path.getmtime(_LIB) < os.path.getmtime(_SRC):
    tmp = _LIB + ".%d.tmp" % os.getpid()
    subprocess.check_call(["/usr/bin/clang", "-O3", "-shared", "-fPIC", "-o", tmp, _SRC])
    os.replace(tmp, _LIB)
_lib = C.CDLL(_LIB)
_A = C.c_uint64 * 4
_lib.iterate.argtypes = [C.c_int, C.c_int, _A, C.c_uint64]
_lib.orbit.argtypes = [C.c_int, C.c_int, _A, C.c_uint64, C.POINTER(C.c_uint64), C.POINTER(C.c_uint64),
                       C.POINTER(C.c_int), C.POINTER(C.c_uint64)]
_lib.orbit.restype = C.c_int


def step(rule, n, x):
    """One CA step; cell i is bit i of x; code at cell i = 4 x_{i-1} + 2 x_i + x_{i+1}."""
    mask = (1 << n) - 1
    L = ((x << 1) | (x >> (n - 1))) & mask          # L_i = x_{i-1}
    R = (x >> 1) | ((x & 1) << (n - 1))             # R_i = x_{i+1}
    o = 0
    for code in range(8):
        if (rule >> code) & 1:
            o |= (L if code & 4 else ~L) & (x if code & 2 else ~x) & (R if code & 1 else ~R)
    return o & mask


def word_state(word, n):
    """Ring state with cell i = word[i mod p]."""
    p = len(word)
    assert n % p == 0
    return sum(1 << i for i in range(n) if word[i % p] == "1")


def to_str(x, n):
    return "".join("1" if (x >> i) & 1 else "0" for i in range(n))


def _arr(x):
    return _A(*[(x >> (64 * k)) & 0xFFFFFFFFFFFFFFFF for k in range(4)])


def iterate_c(rule, n, x, k):
    a = _arr(x)
    _lib.iterate(rule, n, a, k)
    return sum(int(a[i]) << (64 * i) for i in range(4))


def orbit_c(rule, n, x0, max_steps):
    """(determined, mu, lam, limit_is_zero, steps_used)"""
    mu, lam, used, zero = C.c_uint64(0), C.c_uint64(0), C.c_uint64(0), C.c_int(0)
    ok = _lib.orbit(rule, n, _arr(x0), max_steps, C.byref(mu), C.byref(lam), C.byref(zero), C.byref(used))
    return bool(ok), int(mu.value), int(lam.value), bool(zero.value), int(used.value)
