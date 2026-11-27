module

public import RingSize.Rule154.Statement

/-!
# Rule 154: the rest of Section 3.1 of the ring-size paper, statements

This file contains only definitions and statements. The proofs are in `RingSize/Rule154/Periodic.lean`,
`Moves.lean` and `Main.lean`. Source: `paper/ring_size_paper.tex`, Section 3.1: Lemma 3.4(b), Lemmas 3.5 to 3.8,
Theorems 3.9, 3.10 and 3.11. Theorem 3.11 is part (a) of the main theorem (Theorem 3.1) of the paper.

`F154 n` is the global map of rule 154, `V154 n` the weights `V(C, C')` between its cycles, `k154 n v` the index
`k_v` and `kStar154 n` the index `k*`. In this file `k` in "`n = 2^k`" is the `k` of the paper.
-/

@[expose] public section

namespace RingSize.Rule154

open Function RingSize.TheoremA

/-- Paper, 3.1: `M`, the set of states that lie neither in `E` nor in `O` ("`M = {0,1}^n \ (E ∪ O)`"). -/
def parM (n : ℕ) : Set (State n) :=
  (parE n ∪ parO n)ᶜ

/-- `V(C, C')` for rule 154. -/
noncomputable abbrev V154 (n : ℕ) [NeZero n] : Cyc (F154 n) → Cyc (F154 n) → ℕ :=
  VE n (ruleOfNumber 154)

/-- `k_v` for rule 154. -/
noncomputable abbrev k154 (n : ℕ) [NeZero n] (v : Code) : ℕ :=
  kIndex n (ruleOfNumber 154) v

/-- `k*` for rule 154. -/
noncomputable abbrev kStar154 (n : ℕ) [NeZero n] : ℕ :=
  kStar n (ruleOfNumber 154)

/-- "`n` is a power of two". -/
def IsPowTwo (n : ℕ) : Prop :=
  ∃ k : ℕ, n = 2 ^ k

/-- Paper, Lemma 3.4(b): "If `n` is even and not a power of two, then `F^t(e_j) ≠ 0` for all `t ≥ 0` and all
cells `j`." Stated here for the cell `j = 0` only; the paper obtains the other cells by rotation. -/
def Lemma_3_4_b_zero : Prop :=
  ∀ (n : ℕ) [NeZero n], Even n → ¬ IsPowTwo n → ∀ t : ℕ, (F154 n)^[t] (e n 0) ≠ 0

/-- Paper, Lemma 3.5 (invariance of `M`): "Let `n` be even, `n ≥ 4`. Then `F(M) ⊆ M`." Stated for every even
`n ≥ 2`. -/
def Lemma_3_5 : Prop :=
  ∀ (n : ℕ) [NeZero n], Even n → ∀ x ∈ parM n, F154 n x ∈ parM n

/-- Paper, Lemma 3.6 (collisions), the part "In particular": if `F(x) = F(y)` with `x ≠ y`, then `n` is even
and both states lie in `E ∪ O`; and `F` is a bijection when `n` is odd. (The paper's list of the three forms of
such pairs is not stated here.) Stated for every `n ≥ 1`. -/
def Lemma_3_6_in_particular : Prop :=
  ∀ (n : ℕ) [NeZero n],
    (∀ x y : State n, F154 n x = F154 n y → x ≠ y →
      Even n ∧ x ∈ parE n ∪ parO n ∧ y ∈ parE n ∪ parO n) ∧
    (¬ Even n → Function.Bijective (F154 n))

/-- Paper, Lemma 3.7 (periodic states), first sentence: "Let `n` be even, `n ≥ 4`. The restriction of `F` to
`M` is a permutation of `M`, and every state of `M` is periodic." Stated for every even `n ≥ 2`. (The second
sentence of the lemma is not stated here; its third sentence is part (a) of `Theorem_3_9`.) -/
def Lemma_3_7 : Prop :=
  ∀ (n : ℕ) [NeZero n], Even n →
    Set.BijOn (F154 n) (parM n) (parM n) ∧ ∀ x ∈ parM n, x ∈ periodicPts (F154 n)

/-- Paper, Lemma 3.8(a): "Let `n` be even, `n ≥ 4`, let `C` be a cycle contained in `M`, `x ∈ C`, `j` a cell and
`y = x + e_j`. If `y ∈ M`, then `y` lies on a cycle `C_y ⊆ M`, and either `C_y = C` or both `C → C_y` and
`C_y → C` are edges of `G_1`." Stated for every even `n ≥ 2`. -/
def Lemma_3_8_a : Prop :=
  ∀ (n : ℕ) [NeZero n], Even n → ∀ (C : Cyc (F154 n)) (x : State n) (j : ZMod n),
    C.1 ⊆ parM n → x ∈ C.1 → TheoremA.flip n x j ∈ parM n →
      ∃ Cy : Cyc (F154 n), TheoremA.flip n x j ∈ Cy.1 ∧ Cy.1 ⊆ parM n ∧
        (Cy = C ∨ (G1 (V154 n) C Cy ∧ G1 (V154 n) Cy C))

/-- Paper, Lemma 3.8(b): "Any two cycles contained in `M` are joined, in both directions, by a directed path
of `G_1` through cycles contained in `M`." Stated here without the clause "through cycles contained in `M`":
any two cycles that contain a state of `M` are joined by a directed path of `G_1` (in both directions, since
the statement is symmetric). For every even `n ≥ 2`. -/
def Lemma_3_8_b : Prop :=
  ∀ (n : ℕ) [NeZero n], Even n → ∀ (C C' : Cyc (F154 n)) (x x' : State n),
    x ∈ C.1 → x ∈ parM n → x' ∈ C'.1 → x' ∈ parM n → Reach (V154 n) C C'

/-- Paper, Theorem 3.9: "Let `n = 2^k`, `k ≥ 2`.
(a) The cycles are `{0}` and the cycles contained in `M`.
(b) No edge of `G_1` leaves `{0}`: `V({0}, C) ≥ 2` for every cycle `C ≠ {0}`.
(c) Every cycle `C ≠ {0}` has a directed path in `G_1` to `{0}` [of length at most `μ(C) ≤ n/2`].
(d) `{{0}}` is the only closed class of `G_1`.
(e) `γ({0}) = m - 1` and `γ(C) = m` for every cycle `C ≠ {0}`; hence `S = {{0}}`.
(f) `k_000 = 0` and `k_v = 1` for each of the seven codes `v ≠ 000`; hence `k* = 1`."
`C0` is the cycle whose set of states is `{0}`. The bound on the length of the path in (c) is not stated. -/
def Theorem_3_9 : Prop :=
  ∀ (n : ℕ) [NeZero n] (k : ℕ), 2 ≤ k → n = 2 ^ k →
    ∀ C0 : Cyc (F154 n), C0.1 = {0} →
      (∀ C : Cyc (F154 n), C ≠ C0 → C.1 ⊆ parM n) ∧
      ((∀ C : Cyc (F154 n), C ≠ C0 → 2 ≤ V154 n C0 C) ∧ ∀ C : Cyc (F154 n), ¬ G1 (V154 n) C0 C) ∧
      (∀ C : Cyc (F154 n), Reach (V154 n) C C0) ∧
      (IsClosedClass (V154 n) {C0} ∧ ∀ K, IsClosedClass (V154 n) K → K = {C0}) ∧
      (gamma (V154 n) C0 = numCycles (F154 n) - 1 ∧
        (∀ C : Cyc (F154 n), C ≠ C0 → gamma (V154 n) C = numCycles (F154 n)) ∧
        Sel (V154 n) = {C0}) ∧
      (k154 n (0, 0, 0) = 0 ∧ (∀ v : Code, v ≠ (0, 0, 0) → k154 n v = 1) ∧ kStar154 n = 1)

/-- Paper, Theorem 3.10: "Let `n ≥ 3` not be a power of two. Then `G_1` is strongly connected, `γ(C) = m - 1`
for every cycle `C`, all cycles are selected, `k_v = 0` for all eight codes `v`, and `k* = 0`." -/
def Theorem_3_10 : Prop :=
  ∀ (n : ℕ) [NeZero n], 3 ≤ n → ¬ IsPowTwo n →
    (∀ C C' : Cyc (F154 n), Reach (V154 n) C C') ∧
    (∀ C : Cyc (F154 n), gamma (V154 n) C = numCycles (F154 n) - 1) ∧
    (∀ C : Cyc (F154 n), C ∈ Sel (V154 n)) ∧
    (∀ v : Code, k154 n v = 0) ∧
    kStar154 n = 0

/-- Paper, Theorem 3.11 (part (a) of the main theorem): "For rule 154 and every `n ≥ 3`: `k* = 1` if `n` is a
power of two (`n ≥ 4`), and `k* = 0` otherwise. In the first case `S = {{0}}`, `k_000 = 0` and `k_v = 1` for the
seven other codes `v`; in the second case `S` is the set of all cycles and `k_v = 0` for all eight codes `v`." -/
def Theorem_3_11 : Prop :=
  ∀ (n : ℕ) [NeZero n], 3 ≤ n →
    (IsPowTwo n →
      kStar154 n = 1 ∧
      (∀ C0 : Cyc (F154 n), C0.1 = {0} → Sel (V154 n) = {C0}) ∧
      k154 n (0, 0, 0) = 0 ∧ ∀ v : Code, v ≠ (0, 0, 0) → k154 n v = 1) ∧
    (¬ IsPowTwo n →
      kStar154 n = 0 ∧
      (∀ C : Cyc (F154 n), C ∈ Sel (V154 n)) ∧
      ∀ v : Code, k154 n v = 0)

end RingSize.Rule154

end
