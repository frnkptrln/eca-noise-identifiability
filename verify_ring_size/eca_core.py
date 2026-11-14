"""ctypes bindings for core.c (compiled on demand with /usr/bin/clang)."""
import ctypes as C
import os
import subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "core.c")
LIB = os.path.join(HERE, "build", "core.dylib")


def _build():
    os.makedirs(os.path.dirname(LIB), exist_ok=True)
    if (not os.path.exists(LIB)) or os.path.getmtime(LIB) < os.path.getmtime(SRC):
        tmp = LIB + ".%d.tmp" % os.getpid()
        subprocess.check_call(["/usr/bin/clang", "-O2", "-shared", "-fPIC", "-o", tmp, SRC])
        os.replace(tmp, LIB)


_build()
_lib = C.CDLL(LIB)


def _p(a, t):
    return a.ctypes.data_as(C.POINTER(t))


u32p, i32p, u8p, i64p = (C.POINTER(C.c_uint32), C.POINTER(C.c_int32), C.POINTER(C.c_uint8), C.POINTER(C.c_int64))
_lib.build_F.argtypes = [C.c_int, C.c_int, u32p, u8p]
_lib.build_F.restype = None
_lib.find_cycles.argtypes = [C.c_int, u32p, i32p, i32p, u32p, i32p, u8p, u8p]
_lib.find_cycles.restype = C.c_int
_lib.rotation_orbits.argtypes = [C.c_int, C.c_int, i32p, u32p, i32p, i32p, i32p, i32p, u32p]
_lib.rotation_orbits.restype = C.c_int
_lib.cycle_geometry.argtypes = [C.c_int, u32p, C.c_int, u32p, i32p, i32p, i32p]
_lib.cycle_geometry.restype = None
_lib.g1_edges.argtypes = [C.c_int, u32p, i32p, C.c_int, u32p, i32p, i32p, i32p]
_lib.g1_edges.restype = C.c_int64
_lib.bfs_from_cycle.argtypes = [C.c_int, u32p, C.c_uint32, u8p]
_lib.bfs_from_cycle.restype = None
_lib.compute_V.argtypes = [C.c_int, u32p, i32p, u8p, C.c_int, u32p, i32p, i32p, C.c_int, C.c_int, u8p, u8p]
_lib.compute_V.restype = None
_lib.edmonds_all_roots.argtypes = [C.c_int, u8p, i64p]
_lib.edmonds_all_roots.restype = C.c_int


def build_F(rule, n):
    N = 1 << n
    F = np.empty(N, np.uint32)
    cm = np.empty(N, np.uint8)
    _lib.build_F(rule, n, _p(F, C.c_uint32), _p(cm, C.c_uint8))
    return F, cm


def find_cycles(n, F, cm):
    N = 1 << n
    cyc = np.empty(N, np.int32)
    attr = np.empty(N, np.int32)
    mn = np.empty(N, np.uint32)
    ln = np.empty(N, np.int32)
    cc = np.empty(N, np.uint8)
    m = _lib.find_cycles(n, _p(F, C.c_uint32), _p(cyc, C.c_int32), _p(attr, C.c_int32), _p(mn, C.c_uint32),
                         _p(ln, C.c_int32), _p(cc, C.c_uint8), _p(cm, C.c_uint8))
    return m, cyc, attr, mn[:m].copy(), ln[:m].copy(), cc[:m].copy()


def rotation_orbits(n, m, cyc, minstate):
    rot1 = np.empty(m, np.int32)
    orb = np.empty(m, np.int32)
    reps = np.empty(m, np.int32)
    osz = np.empty(m, np.int32)
    omin = np.empty(m, np.uint32)
    no = _lib.rotation_orbits(n, m, _p(cyc, C.c_int32), _p(minstate, C.c_uint32), _p(rot1, C.c_int32),
                              _p(orb, C.c_int32), _p(reps, C.c_int32), _p(osz, C.c_int32), _p(omin, C.c_uint32))
    return no, rot1, orb, reps[:no].copy(), osz[:no].copy(), omin[:no].copy()


def cycle_geometry(n, F, x0):
    x0 = np.ascontiguousarray(x0, np.uint32)
    k = len(x0)
    sp = np.empty(k, np.int32)
    tr = np.empty(k, np.int32)
    sr = np.empty(k, np.int32)
    _lib.cycle_geometry(n, _p(F, C.c_uint32), k, _p(x0, C.c_uint32), _p(sp, C.c_int32), _p(tr, C.c_int32),
                        _p(sr, C.c_int32))
    return sp, tr, sr


def g1_edges(n, F, attr, m, minstate, length):
    ne = _lib.g1_edges(n, _p(F, C.c_uint32), _p(attr, C.c_int32), m, _p(minstate, C.c_uint32),
                       _p(length, C.c_int32), None, None)
    src = np.empty(max(ne, 1), np.int32)
    dst = np.empty(max(ne, 1), np.int32)
    ne2 = _lib.g1_edges(n, _p(F, C.c_uint32), _p(attr, C.c_int32), m, _p(minstate, C.c_uint32),
                        _p(length, C.c_int32), _p(src, C.c_int32), _p(dst, C.c_int32))
    assert ne == ne2
    return src[:ne], dst[:ne]


def bfs_from_cycle(n, F, s0):
    d = np.empty(1 << n, np.uint8)
    _lib.bfs_from_cycle(n, _p(F, C.c_uint32), int(s0), _p(d, C.c_uint8))
    return d


def compute_V(n, F, cyc, cm, m, minstate, rot1, reps, use_rot=True):
    reps = np.ascontiguousarray(reps, np.int32)
    V = np.empty((m, m), np.uint8)
    kd = np.empty((len(reps), 8), np.uint8)
    _lib.compute_V(n, _p(F, C.c_uint32), _p(cyc, C.c_int32), _p(cm, C.c_uint8), m, _p(minstate, C.c_uint32),
                   _p(rot1, C.c_int32), _p(reps, C.c_int32), len(reps), 1 if use_rot else 0, _p(V, C.c_uint8),
                   _p(kd, C.c_uint8))
    return V, kd


def edmonds_all_roots(W):
    """W: uint8 (m,m) C-contiguous, destroyed.  Returns int64 gamma[m]."""
    m = W.shape[0]
    assert W.dtype == np.uint8 and W.flags.c_contiguous and W.shape == (m, m)
    g = np.empty(m, np.int64)
    _lib.edmonds_all_roots(m, _p(W, C.c_uint8), _p(g, C.c_int64))
    return g
