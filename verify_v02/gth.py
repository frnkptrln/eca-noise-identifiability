"""Grassmann-Taksar-Heyman elimination (subtraction-free), numeric and tropical (min-plus).

Numeric: P is a row-stochastic matrix (float64), returns pi with pi P = pi.
Tropical: W[x, y] = order (exponent of the leading eps power) of P(x, y); W[x, x] ignored.
Because GTH uses only +, *, / on positive quantities, the order of every intermediate
equals its min-plus evaluation: ord(a+b) = min, ord(ab) = ord a + ord b, ord(a/b) = ord a - ord b
(all leading coefficients stay positive, so there is no cancellation). The tropical result h(x)
is therefore ord pi(x) up to an additive constant; we return h - min h.
"""
import numpy as np
from numba import njit


@njit(cache=True)
def _gth_numeric(A):
    N = A.shape[0]
    for k in range(N - 1, 0, -1):
        s = 0.0
        for j in range(k):
            s += A[k, j]
        for i in range(k):
            A[i, k] /= s
        for i in range(k):
            a = A[i, k]
            if a != 0.0:
                for j in range(k):
                    A[i, j] += a * A[k, j]
    x = np.zeros(N)
    x[0] = 1.0
    for j in range(1, N):
        t = 0.0
        for i in range(j):
            t += x[i] * A[i, j]
        x[j] = t
    return x / x.sum()


def gth_numeric(P):
    A = np.array(P, dtype=np.float64, copy=True, order='C')
    return _gth_numeric(A)


@njit(cache=True)
def _gth_tropical(W, INF):
    N = W.shape[0]
    for k in range(N - 1, 0, -1):
        s = INF
        for j in range(k):
            if W[k, j] < s:
                s = W[k, j]
        if s >= INF:
            return np.full(N, -1, dtype=np.int64)  # reducible: not handled
        for i in range(k):
            if W[i, k] < INF:
                W[i, k] -= s
        for i in range(k):
            a = W[i, k]
            if a < INF:
                for j in range(k):
                    b = W[k, j]
                    if b < INF and a + b < W[i, j]:
                        W[i, j] = a + b
    h = np.zeros(N, dtype=np.int64)
    for j in range(1, N):
        t = INF
        for i in range(j):
            if h[i] < INF and W[i, j] < INF and h[i] + W[i, j] < t:
                t = h[i] + W[i, j]
        h[j] = t
    return h - h.min()


INF = 1 << 40


def gth_tropical(W):
    A = np.array(W, dtype=np.int64, copy=True, order='C')
    A[A >= INF] = INF
    return _gth_tropical(A, INF)
