"""Own single-flip simulator on rows of up to ~100 cells (Python ints, bit i = cell i)."""
def step_fn(rule, n, bnd='null'):
    full = (1 << n) - 1
    lits = [c for c in range(8) if (rule >> c) & 1]
    def F(x):
        l = (x << 1) & full; r = x >> 1
        if bnd == 'reflect':
            l |= x & 1; r |= ((x >> (n - 1)) & 1) << (n - 1)
        elif bnd == 'one':
            l |= 1; r |= 1 << (n - 1)
        nl, nc, nr = full ^ l, full ^ x, full ^ r
        y = 0
        for c in lits:
            y |= (l if c & 4 else nl) & (x if c & 2 else nc) & (r if c & 1 else nr)
        return y
    return F
def orbit_cycle(F, x, limit):
    """Brent: return a frozenset of the cycle the orbit of x ends on, or None if not found within limit steps."""
    power = lam = 1; tort = x; hare = F(x); steps = 1
    while tort != hare:
        if power == lam:
            tort = hare; power *= 2; lam = 0
        hare = F(hare); lam += 1; steps += 1
        if steps > limit: return None
    cyc = {hare}; z = F(hare)
    while z != hare: cyc.add(z); z = F(z)
    return frozenset(cyc)
def cycle_of(F, x):
    seen = [x]; z = F(x); s = {x}
    while z not in s: s.add(z); seen.append(z); z = F(z)
    return frozenset(seen[seen.index(z):])
def radius2(rule, n, x0, bnd='null', limit=20000):
    """True/False/None: every single flip of every state of the cycle of x0 returns to it (None = undecided)."""
    F = step_fn(rule, n, bnd); X = cycle_of(F, x0)
    und = False
    for x in X:
        for i in range(n):
            c = orbit_cycle(F, x ^ (1 << i), limit)
            if c is None: und = True; continue
            if not (c & X): return False
    return None if und else True
