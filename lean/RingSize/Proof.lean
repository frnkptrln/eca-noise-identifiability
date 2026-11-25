module

public import RingSize.Iterate
import Mathlib.Algebra.CharP.Two
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Tactic.LinearCombination

/-!
# Proof of the main theorem

* If `n = 2^k`, then `A^n x i = x (i - n) + x (i + n) = x i + x i = 0` for every
  state `x` (`iterate_self_eq_zero`).
* Conversely, if `A^t (e n 0) = 0`, then also `A^(2^t) (e n 0) = 0`, because the
  zero state is fixed and `t ≤ 2^t`. Evaluating at cell `2^t` gives
  `e n 0 0 + e n 0 (2^(t+1)) = 0`, so `2^(t+1) = 0` in `ZMod n`, so `n ∣ 2^(t+1)`,
  so `n` is a power of two (`pow_two_of_iterate_eq_zero`).

The proof does not use the hypothesis `1 ≤ n`; `main_all_n` states the result
for every `n : ℕ` (for `n = 0`, `ZMod 0 = ℤ` is the infinite line).
-/

public section

namespace RingSize

/-- The zero state is a fixed point of rule 90. -/
lemma rule90_zero (n : ℕ) : rule90 n 0 = 0 := by
  funext i
  simp [rule90]

lemma iterate_zero_state (n t : ℕ) : (rule90 n)^[t] 0 = 0 :=
  Function.iterate_fixed (rule90_zero n) t

/-- On a ring of `2^k` cells, `A^(2^k)` sends every state to zero. -/
theorem iterate_self_eq_zero (k : ℕ) (x : State (2 ^ k)) :
    (rule90 (2 ^ k))^[2 ^ k] x = 0 := by
  funext i
  rw [iterate_two_pow]
  have h : (2 : ZMod (2 ^ k)) ^ k = 0 := by
    have := ZMod.natCast_self (2 ^ k)
    push_cast at this
    exact this
  rw [h, sub_zero, add_zero, Pi.zero_apply]
  exact CharTwo.add_self_eq_zero (x i)

/-- On a ring of `2^(k+1)` cells already `A^(2^k)` sends every state to zero.
Not needed for the main theorem; it is the form used for rule 154 in the paper
(Lemma 3.4(a), with `n/2 = 2^k`). -/
theorem iterate_half_eq_zero (k : ℕ) (x : State (2 ^ (k + 1))) :
    (rule90 (2 ^ (k + 1)))^[2 ^ k] x = 0 := by
  funext i
  rw [iterate_two_pow]
  have h0 : (2 : ZMod (2 ^ (k + 1))) ^ (k + 1) = 0 := by
    have := ZMod.natCast_self (2 ^ (k + 1))
    push_cast at this
    exact this
  have h : i - (2 : ZMod (2 ^ (k + 1))) ^ k = i + 2 ^ k := by
    linear_combination -h0
  rw [h, Pi.zero_apply]
  exact CharTwo.add_self_eq_zero _

/-- If the single-1 state at cell `0` reaches zero, then `n` is a power of two. -/
theorem pow_two_of_iterate_eq_zero (n t : ℕ) (ht : (rule90 n)^[t] (e n 0) = 0) :
    ∃ k : ℕ, n = 2 ^ k := by
  have hle : t ≤ 2 ^ t := Nat.lt_two_pow_self.le
  have h0 : (rule90 n)^[2 ^ t] (e n 0) = 0 := by
    obtain ⟨s, hs⟩ : ∃ s, 2 ^ t = s + t := ⟨2 ^ t - t, by omega⟩
    rw [hs, Function.iterate_add_apply, ht, iterate_zero_state]
  have h1 := congrFun h0 ((2 : ZMod n) ^ t)
  rw [iterate_two_pow, sub_self, Pi.zero_apply] at h1
  have h2 : (2 : ZMod n) ^ t + 2 ^ t = 0 := by
    by_contra hne
    simp [e, hne] at h1
  have h3 : ((2 ^ (t + 1) : ℕ) : ZMod n) = 0 := by
    push_cast
    rw [pow_succ, mul_two]
    exact h2
  have h4 : n ∣ 2 ^ (t + 1) := (CharP.cast_eq_zero_iff (ZMod n) n _).mp h3
  obtain ⟨k, -, hk⟩ := (Nat.dvd_prime_pow Nat.prime_two).mp h4
  exact ⟨k, hk⟩

/-- The main theorem without the hypothesis `1 ≤ n`. -/
theorem main_all_n (n : ℕ) :
    (∀ i : ZMod n, ∃ t : ℕ, (rule90 n)^[t] (e n i) = 0) ↔ ∃ k : ℕ, n = 2 ^ k := by
  constructor
  · intro h
    obtain ⟨t, ht⟩ := h 0
    exact pow_two_of_iterate_eq_zero n t ht
  · rintro ⟨k, rfl⟩ i
    exact ⟨2 ^ k, iterate_self_eq_zero k _⟩

/-- The main theorem, as stated in `RingSize/Statement.lean`. -/
theorem mainTheorem : MainTheorem :=
  fun n _ => main_all_n n

end RingSize

end
