module

public import Mathlib.Data.ZMod.Defs

/-!
# Rule 90 on a ring of `n` cells: definitions and the main statement

This file contains only definitions and the statement. The proof is in
`RingSize/Proof.lean`, which proves `RingSize.mainTheorem : RingSize.MainTheorem`.

Cells are indexed by `ZMod n`, so `i - 1` and `i + 1` are taken modulo `n`.
A state assigns a bit (an element of `ZMod 2`) to every cell.
-/

@[expose] public section

namespace RingSize

/-- A state of the ring of `n` cells: one bit per cell. -/
abbrev State (n : ℕ) := ZMod n → ZMod 2

/-- One step of rule 90, the map `A`: the new value of cell `i` is
`x (i - 1) + x (i + 1)`, computed in `ZMod 2`. -/
def rule90 (n : ℕ) (x : State n) : State n :=
  fun i => x (i - 1) + x (i + 1)

/-- `e n i` is the indicator of cell `i`: the state with a single 1, at cell `i`. -/
def e (n : ℕ) (i : ZMod n) : State n :=
  fun j => if j = i then 1 else 0

/-- **Main theorem.** For `n ≥ 1`: the orbit under rule 90 of every single-1 state
reaches the zero state if and only if `n` is a power of two.
Here `(rule90 n)^[t]` is the `t`-fold iterate `A^t`, and `0` is the all-zero state. -/
def MainTheorem : Prop :=
  ∀ n : ℕ, 1 ≤ n →
    ((∀ i : ZMod n, ∃ t : ℕ, (rule90 n)^[t] (e n i) = 0) ↔ ∃ k : ℕ, n = 2 ^ k)

end RingSize

end
