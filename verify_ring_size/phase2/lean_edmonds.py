"""Memory-lean all-roots Edmonds: level-wise contraction of the strongly connected components of the
zero-reduced-weight arcs.  Level 1 needs only the radii and the arcs of minimum weight out of each cycle
(the one-flip graph G1 for cycles of radius 1); the dense matrix V is never stored.
gamma(r) = sum of rho over all contraction levels and super-nodes - sum of rho over the super-nodes containing r."""
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

BIG = 1 << 40


def edmonds_dense_levels(W):
    """W: K x K integer matrix of arc weights (diagonal ignored).  Returns (total, acc) with
    gamma(r) = total - acc[r]."""
    W = np.array(W, dtype=np.int64)
    K = W.shape[0]
    comp_of = np.arange(K)
    total = 0
    acc = np.zeros(K, np.int64)
    np.fill_diagonal(W, BIG)
    while W.shape[0] > 1:
        k = W.shape[0]
        rho = W.min(axis=1)
        total += int(rho.sum())
        acc += rho[comp_of]
        W = W - rho[:, None]
        np.fill_diagonal(W, BIG)
        z = csr_matrix(W == 0)
        nc, lab = connected_components(z, directed=True, connection="strong")
        assert nc < k, "every node has a zero arc, so some component must be non-trivial"
        W2 = np.full((nc, nc), BIG, np.int64)
        for a in range(k):
            np.minimum.at(W2[lab[a]], lab, W[a])
        np.fill_diagonal(W2, BIG)
        W = W2
        comp_of = lab[comp_of]
    return total, acc


def lean_gamma(c, radius=None, log=None):
    """c: p2lib.Case.  Returns (gamma for all cycles, info dict)."""
    m = c.m
    if m == 1:
        return np.zeros(1, np.int64), {"levels": 0, "supernodes_after_level1": 1, "bfs_rows": 0}
    rho = c.radius() if radius is None else radius
    # arcs of minimum weight: G1 edges for radius-1 cycles, V == radius arcs for the others
    s, d = [c.src], [c.dst]
    nb = 0
    for cc in np.nonzero(rho >= 2)[0]:
        row, _ = c.row(cc)
        nb += 1
        t = np.nonzero(row == rho[cc])[0]
        t = t[t != cc]
        s.append(np.full(len(t), cc, np.int32))
        d.append(t.astype(np.int32))
    s, d = np.concatenate(s), np.concatenate(d)
    G = csr_matrix((np.ones(len(s), np.int8), (s, d)), shape=(m, m))
    K, lab = connected_components(G, directed=True, connection="strong")
    info = {"supernodes_after_level1": int(K), "bfs_rows": nb}
    total = int(rho.sum())
    acc = rho.astype(np.int64).copy()
    if K > 1:
        # reduced weights between the super-nodes: one forward search per rotation orbit of cycles
        W2 = np.full((K, K), BIG, np.int64)
        for o in range(c.no):
            r = int(c.reps[o])
            row, _ = c.row(r)
            nb += 1
            row = row.astype(np.int64)
            perm = np.arange(m)
            cr = r
            while True:
                w = row - rho[cr]
                w[r] = BIG                     # position of the source cycle itself (before the rotation)
                np.minimum.at(W2[lab[cr]], lab[perm], w)
                cr = int(c.rot1[cr])
                perm = c.rot1[perm]
                if cr == r:
                    break
            if log and o % 200 == 0:
                log(o)
        t2, a2 = edmonds_dense_levels(W2)
        total += t2
        acc += a2[lab]
        info["bfs_rows"] = nb
    return total - acc, info
