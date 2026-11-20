"""Rule 154 on even rings: the fraction of states that are not on a cycle, from Lemma 6 of
verify_ring_size/part2_154/PROOF_154.md, compared with the two values quoted from Zhu and Richard,
arXiv:2610.10967, Section 4.2 (0.00048828 at n = 22, 0.00045776 at n = 24). One process; writes
out/zhu_richard_154.json. For literature_addendum.md.

Lemma 6 (n even, n >= 4): the periodic states of rule 154 are the states of M (a one on an even site and a one on an
odd site; |M| = (2^(n/2) - 1)^2) and the periodic states inside E u O (states supported on one parity class).
The lemma gives the number of the latter only for n = 2^k (the zero state alone). Here it is counted by iterating
rule 154 on the 2^(n/2+1) - 1 states of E u O only (no enumeration of 2^n states):

    count_lemma6(n) = (2^(n/2) - 1)^2 + #{periodic states of rule 154 in E u O}.

Three numbers are compared for every even n = 4..26:
  (1) the fraction 1 - count_lemma6(n) / 2^n;
  (2) the fraction from a direct enumeration of all 2^n states (independent of Lemma 6; n <= 24 only);
  (3) the closed form 2^(1 - n/2) (1 - 2^(-2^j)), where n/2 = 2^j q with q odd.
The closed form is not part of PROOF_154.md; it is only compared here (status: computed for n = 4..26).
For n <= 24 the number of states without preimage is recorded as well: the multiplicity of the eigenvalue 0 of the
matrix of F is the number of non-periodic states if it is the algebraic multiplicity, and the number of states
without preimage if it is the dimension of the kernel; the two differ at n = 24.

Source of the two quoted values: the task statement of this work (a search made outside this session). The paper
itself could not be opened from the execution environment (arxiv.org not reachable); see literature_addendum.md.
"""
import json
import os
import resource
import sys
import time
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ring  # noqa: E402

QUOTED = {22: "0.00048828", 24: "0.00045776"}        # values as quoted in the task from arXiv:2610.10967, Sect. 4.2


def periodic_in_EO(n):
    """Number of periodic states of rule 154 among the states supported on the even or on the odd sites."""
    even_cells = list(range(0, n, 2))
    states = set()
    for v in range(1 << (n // 2)):
        xe = sum(1 << even_cells[k] for k in range(n // 2) if (v >> k) & 1)
        states.add(xe)
        states.add(ring.rot_up(xe, n, 1))
    nxt = {x: ring.step(154, x, n) for x in states}
    assert all(y in states for y in nxt.values()), "E u O is not mapped into itself"
    # periodic states of a self-map of a finite set: the eventual image
    img = set(states)
    while True:
        new = {nxt[x] for x in img}
        if new == img:
            break
        img = new
    return len(img), len(states)


def main():
    t0 = time.process_time()
    rows = []
    for n in range(4, 27, 2):
        pEO, nEO = periodic_in_EO(n)
        count6 = (2 ** (n // 2) - 1) ** 2 + pEO
        frac6 = Fraction(2 ** n - count6, 2 ** n)
        direct = nopre = None
        if n <= 24:
            F = ring.build_F(154, n)
            on, _ = ring.periodic_mask(F, n)
            direct = int(on.sum())
            nopre = int((np.bincount(F, minlength=1 << n) == 0).sum())      # states without preimage
            del F, on
        N = n // 2
        j = 0
        while N % 2 == 0:
            N //= 2
            j += 1
        closed = Fraction(2, 2 ** (n // 2)) * (1 - Fraction(1, 2 ** (2 ** j)))
        row = dict(n=n, states_EO=nEO, periodic_in_EO=pEO, periodic_lemma6=count6, periodic_direct=direct,
                   lemma6_equals_direct=(count6 == direct) if direct is not None else None, fraction_not_periodic=str(frac6),
                   fraction_decimal=f"{float(frac6):.12f}", closed_form=str(closed), closed_form_equal=closed == frac6,
                   states_without_preimage=nopre,
                   fraction_without_preimage=(f"{nopre / 2 ** n:.12f}" if nopre is not None else None))
        if n in QUOTED:
            q = QUOTED[n]
            digits = len(q.split(".")[1])
            row["quoted"] = q
            row["rounded_to_quoted_digits"] = f"{float(frac6):.{digits}f}"
            row["truncated_to_quoted_digits"] = f"{float(frac6):.16f}"[: 2 + digits]
            row["agrees_with_quoted"] = q in (row["rounded_to_quoted_digits"], row["truncated_to_quoted_digits"])
        rows.append(row)
        print(row, flush=True)
    cpu = time.process_time() - t0
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    out = dict(script="zhu_richard_154.py", quoted=QUOTED,
               all_lemma6_equal_direct=all(r["lemma6_equals_direct"] for r in rows if r["periodic_direct"] is not None),
               direct_n_max=max(r["n"] for r in rows if r["periodic_direct"] is not None), n_max=rows[-1]["n"],
               all_closed_form_equal=all(r["closed_form_equal"] for r in rows),
               quoted_values_agree=all(r["agrees_with_quoted"] for r in rows if "quoted" in r),
               below_0_01_from_n=min(r["n"] for r in rows if all(float(Fraction(s["fraction_not_periodic"])) < 0.01
                                                                 for s in rows if s["n"] >= r["n"])),
               cpu_seconds=round(cpu, 2), peak_mb=round(peak / 1e6 if sys.platform == "darwin" else peak / 1e3),
               rows=rows)
    with open(os.path.join(HERE, "out", "zhu_richard_154.json"), "w") as fh:
        json.dump(out, fh, indent=1)
    print(f"Lemma 6 count = direct count for all n <= 24: {out['all_lemma6_equal_direct']}; quoted values agree: "
          f"{out['quoted_values_agree']}; CPU {cpu:.2f} s")


if __name__ == "__main__":
    main()
