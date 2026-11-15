"""Read-only access to the outputs of the independent verification of 14 November 2026
(verify_ring_size/, VERIFICATION_ring_size.md; merged into this branch). The generators of this study
(make_report.py, check_predictions.py, stopped_runs.py) take from here every value that the study did
not compute itself, and name the file it comes from.
"""
import json, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
VER = os.path.join(HERE, "..", "..", "verify_ring_size")
V154_N22 = "verify_ring_size/phase2/out/v154_n22.json"
SEED_OWN = "verify_ring_size/phase2/out/seed_orbits_own.csv"
COST_CLAIM = "verify_ring_size/phase2/out/cost_claim.json"
RECOUNT = "verify_ring_size/phase2/out/predictions_recount.csv"
SWEEP88 = "verify_ring_size/phase2/out/sweep88_summary.json"
G1_94 = "verify_ring_size/part2_94/out/g1_classes.jsonl"
EXPLORE = "verify_ring_size/part2_154/out/explore_122_26.jsonl"
COMPARE = "verify_ring_size/phase2/out/compare_sample.json"
PROOF_94 = "verify_ring_size/part2_94/PROOF_94.md"
PROOF_154 = "verify_ring_size/part2_154/PROOF_154.md"


def _p(rel):
    return os.path.join(HERE, "..", "..", rel)


def v154_n22():
    """Class 154 at n = 22 as computed by the verification (cycles, gamma_min, k_c, kstar, cpu_seconds, ...)."""
    return json.load(open(_p(V154_N22)))


def cost_claim():
    return json.load(open(_p(COST_CLAIM)))


def sweep88():
    return json.load(open(_p(SWEEP88)))


def recount():
    return pd.read_csv(_p(RECOUNT))


def sample_comparison():
    """Comparison of the study's records with the sealed blind sample of the verification."""
    return json.load(open(_p(COMPARE)))


def explore_122_26():
    """G1 and closed classes of rules 122 and 26, n = 4..26, enumerated by the verification (no potentials)."""
    return [json.loads(l) for l in open(_p(EXPLORE))]


def g1_classes_94():
    return [json.loads(l) for l in open(_p(G1_94))]


def seed_status(so):
    """Status of every single-seed orbit: the study's seed_orbits.csv (so) completed by the verification.

    Returns so with the columns status in {"returns", "no return", "open"} and source in
    {"study", "verification (simulation)", "Proposition R154", "Proposition R22", ""}.
    A row the study determined keeps the study's value; a row capped in the study takes the verification's
    simulation if that closed the orbit, else a proof named by the verification, else it is open.
    """
    own = pd.read_csv(_p(SEED_OWN))
    m = so.merge(own, on=["rule", "n"], how="left", suffixes=("", "_own"))
    assert len(m) == len(so)
    st, src = [], []
    for r in m.itertuples():
        if r.capped == 0:
            st.append("returns" if int(r.returns_to_zero) == 1 else "no return"); src.append("study")
            if r.determined == 1:
                assert int(r.returns_to_zero_own) == int(r.returns_to_zero), (r.rule, r.n)
        elif r.determined == 1:
            st.append("returns" if int(r.returns_to_zero_own) == 1 else "no return"); src.append("verification (simulation)")
        elif isinstance(r.proof, str) and r.decided_by_proof == r.decided_by_proof:
            st.append("returns" if int(r.decided_by_proof) == 1 else "no return")
            src.append("Proposition R154" if "R154" in r.proof else "Proposition R22")
        else:
            st.append("open"); src.append("")
    m["status"] = st; m["source"] = src
    return m
