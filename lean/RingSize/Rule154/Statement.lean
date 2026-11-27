module

public import RingSize.TheoremA.Statement
public import Mathlib.Algebra.Group.Even
public import Mathlib.Algebra.Ring.Parity

/-!
# Rule 154 on a ring whose size is a power of two: statements

This file contains only definitions and statements. The proofs are in `RingSize/Rule154/Pow2.lean`.
Source: `paper/ring_size_paper.tex`, Section 3.1 ("Rule 154"): Lemma 3.3 (rule 90 on the parity classes),
Lemma 3.4(a) (nilpotency on `E ∪ O`) and Theorem 3.9(b) (no edge of `G_1` leaves `{0}`).

The local form of rule 154 (Lemma 3.2) is the statement `Rule154_local` of `RingSize/TheoremA/Statement.lean`.
The map `L` of the paper, `(L x)_i = x_{i-1} + x_{i+1}`, is `RingSize.rule90 n` of the pilot.

Not in this file: Lemma 3.4(b), Lemmas 3.5 to 3.8, the other parts of Theorem 3.9, and Theorems 3.10 and 3.11.

The paper writes powers of two as `n = 2^k` with `k ≥ 2`. The statements below write `n = 2^(k+1)` with `k ≥ 0`,
so the `k` of this file is the paper's `k - 1`.
-/

@[expose] public section

namespace RingSize.Rule154

open Function RingSize.TheoremA

/-- The global map of rule 154 on a ring of `n` cells. -/
abbrev F154 (n : ℕ) [NeZero n] : State n → State n :=
  globalMap n (ruleOfNumber 154)

/-- Paper, 3.1: `E`, "the set of states that are `0` on all odd cells". A cell `i : ZMod n` is odd if its
representative `i.val` in `{0, …, n - 1}` is odd. (The paper uses `E` and `O` only for even `n`, where the
parity of a cell does not depend on the representative.) -/
def parE (n : ℕ) : Set (State n) :=
  {x | ∀ i : ZMod n, Odd i.val → x i = 0}

/-- Paper, 3.1: `O`, the set of states that are `0` on all even cells. -/
def parO (n : ℕ) : Set (State n) :=
  {x | ∀ i : ZMod n, Even i.val → x i = 0}

/-- The zero state is a fixed point of rule 154, so `{0}` is a cycle. (Used in the paper throughout
Section 3.1; needed here so that the cycle `{0}` of `Theorem_3_9_b`, and of `Theorem_3_9` and `Theorem_3_11` in
`StatementMain.lean`, exists.) -/
def Zero_cycle : Prop :=
  ∀ (n : ℕ) [NeZero n], IsCycle (F154 n) {(0 : State n)}

/-- Paper, Lemma 3.3: "Let `n` be even, `n ≥ 4`. If `x ∈ E`, then `F(x) ∈ O` and
`(F x)_i = x_{i-1} + x_{i+1}` for all `i`; the same holds with `E` and `O` exchanged. Hence `F^t(x) = L^t x`
for all `t ≥ 0` and all `x ∈ E ∪ O`."
Stated here for every even `n ≥ 2`. -/
def Lemma_3_3 : Prop :=
  ∀ (n : ℕ) [NeZero n], Even n → ∀ x : State n,
    (x ∈ parE n → F154 n x ∈ parO n ∧ F154 n x = rule90 n x) ∧
    (x ∈ parO n → F154 n x ∈ parE n ∧ F154 n x = rule90 n x) ∧
    (x ∈ parE n ∪ parO n → ∀ t : ℕ, (F154 n)^[t] x = (rule90 n)^[t] x)

/-- Paper, Lemma 3.4(a): "If `n = 2^k`, `k ≥ 2`, then `F^{n/2}(x) = 0` for every `x ∈ E ∪ O`."
Stated here for `n = 2^(k+1)` with `k ≥ 0`, that is, for every power of two `n ≥ 2`. The `k` here is the
paper's `k - 1`. -/
def Lemma_3_4_a : Prop :=
  ∀ (n : ℕ) [NeZero n] (k : ℕ), n = 2 ^ (k + 1) →
    ∀ x : State n, x ∈ parE n ∪ parO n → (F154 n)^[n / 2] x = 0

/-- Paper, proof of Theorem 3.9(b): "The state `e_j` lies in `E ∪ O`." -/
def Single_mem : Prop :=
  ∀ (n : ℕ) (j : ZMod n), e n j ∈ parE n ∪ parO n

/-- Paper, Theorem 3.9(b): "Let `n = 2^k`, `k ≥ 2`. No edge of `G_1` leaves `{0}`: `V({0}, C) ≥ 2` for every
cycle `C ≠ {0}`."
Stated here for `n = 2^(k+1)` with `k ≥ 0`, that is, for every power of two `n ≥ 2`. The `k` here is the
paper's `k - 1`. `C0` is the cycle whose set of states is `{0}`. -/
def Theorem_3_9_b : Prop :=
  ∀ (n : ℕ) [NeZero n] (k : ℕ), n = 2 ^ (k + 1) →
    ∀ C0 : Cyc (F154 n), C0.1 = {0} →
      (∀ C : Cyc (F154 n), C ≠ C0 → 2 ≤ VE n (ruleOfNumber 154) C0 C) ∧
      (∀ C : Cyc (F154 n), ¬ G1 (VE n (ruleOfNumber 154)) C0 C)

end RingSize.Rule154

end
