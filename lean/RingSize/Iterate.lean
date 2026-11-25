module

public import RingSize.Statement
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

/-!
# The iterates `A^(2^j)` of rule 90

In characteristic 2, `A = S + S⁻¹` satisfies `A^(2^j) = S^(2^j) + S^(-2^j)`.
We prove the pointwise form directly, by induction on `j`, without introducing
`S` or any linear algebra: `A^(2^j) x i = x (i - 2^j) + x (i + 2^j)` for every
state `x`.
-/

public section

namespace RingSize

/-- In `ZMod 2`, the two middle terms cancel: `(a + b) + (b + c) = a + c`. -/
lemma zmod2_add_add_cancel (a b c : ZMod 2) : (a + b) + (b + c) = a + c := by
  have h2 : (2 : ZMod 2) = 0 := rfl
  linear_combination b * h2

/-- `A^(2^j) x i = x (i - 2^j) + x (i + 2^j)`. -/
theorem iterate_two_pow (n j : ℕ) (x : State n) (i : ZMod n) :
    (rule90 n)^[2 ^ j] x i = x (i - 2 ^ j) + x (i + 2 ^ j) := by
  induction j generalizing x i with
  | zero => simp [rule90]
  | succ j ih =>
    have h : 2 ^ (j + 1) = 2 ^ j + 2 ^ j := by ring
    rw [h, Function.iterate_add_apply, ih, ih, ih]
    have e1 : i - 2 ^ j - 2 ^ j = i - 2 ^ (j + 1) := by ring
    have e2 : i - 2 ^ j + 2 ^ j = i := by ring
    have e3 : i + 2 ^ j - 2 ^ j = i := by ring
    have e4 : i + 2 ^ j + 2 ^ j = i + 2 ^ (j + 1) := by ring
    rw [e1, e2, e3, e4]
    exact zmod2_add_add_cancel _ _ _

end RingSize

end
