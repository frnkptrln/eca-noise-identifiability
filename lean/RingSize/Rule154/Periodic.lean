module

public import RingSize.Rule154.StatementMain
public import RingSize.Rule154.Pow2
import Mathlib.Algebra.CharP.Two
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.LinearCombination
import Mathlib.Tactic.Ring

/-!
# Rule 154: invariance of `M`, collisions, periodic states (paper, Lemmas 3.5, 3.6, 3.7)

`Z n c x` says that the state `x` vanishes on the cells of parity `c`; `E` is `Z n 1`, `O` is `Z n 0`, and
`M` is the set of states with neither property.
-/

@[expose] public section

namespace RingSize.Rule154

open Function RingSize.TheoremA

/-- The state `x` vanishes on the cells of parity `c`. -/
def Z (n : ℕ) (c : ZMod 2) (x : State n) : Prop :=
  ∀ i, par n i = c → x i = 0

theorem mem_parM (n : ℕ) {x : State n} : x ∈ parM n ↔ ¬ Z n 1 x ∧ ¬ Z n 0 x := by
  unfold parM
  rw [Set.mem_compl_iff, Set.mem_union, not_or, mem_parE, mem_parO]
  exact Iff.rfl

theorem Z_cases (n : ℕ) {x : State n} (h : ∃ c, Z n c x) : x ∉ parM n := by
  obtain ⟨c, hc⟩ := h
  rw [mem_parM]
  rintro ⟨h1, h0⟩
  rcases zmod2_cases c with rfl | rfl
  · exact h0 hc
  · exact h1 hc

/-! ### Arithmetic on the ring of cells -/

theorem par_sub (n : ℕ) [NeZero n] (hn : Even n) (a b : ZMod n) :
    par n (a - b) = par n a + par n b := by
  have h : 2 ∣ n := hn.two_dvd
  rw [par_eq_castHom n h, par_eq_castHom n h, par_eq_castHom n h, map_sub, CharTwo.sub_eq_add]

theorem exists_two_mul_of_par_zero (n : ℕ) [NeZero n] (a : ZMod n) (h : par n a = 0) :
    ∃ s : ℕ, a = (s : ZMod n) * 2 := by
  unfold par at h
  rw [ZMod.natCast_eq_zero_iff_even] at h
  obtain ⟨s, hs⟩ := h
  refine ⟨s, ?_⟩
  have h1 : ((a.val : ℕ) : ZMod n) = a := ZMod.natCast_zmod_val a
  rw [hs] at h1
  rw [← h1]
  push_cast
  ring

/-- Cells of the same parity differ by an even number of steps (for even `n`). -/
theorem exists_step (n : ℕ) [NeZero n] (hn : Even n) (j c : ZMod n) (h : par n c = par n j) :
    ∃ s : ℕ, c = j + (s : ZMod n) * 2 := by
  have h0 : par n (c - j) = 0 := by
    rw [par_sub n hn, h]
    exact CharTwo.add_self_eq_zero _
  obtain ⟨s, hs⟩ := exists_two_mul_of_par_zero n (c - j) h0
  exact ⟨s, by rw [← hs]; ring⟩

theorem exists_step_back (n : ℕ) [NeZero n] (hn : Even n) (j c : ZMod n) (h : par n c = par n j) :
    ∃ s : ℕ, c = j + (s : ZMod n) * (-2) := by
  have h0 : par n (j - c) = 0 := by
    rw [par_sub n hn, h]
    exact CharTwo.add_self_eq_zero _
  obtain ⟨s, hs⟩ := exists_two_mul_of_par_zero n (j - c) h0
  refine ⟨s, ?_⟩
  have : (s : ZMod n) * (-2) = -(j - c) := by rw [hs]; ring
  rw [this]
  ring

/-- Induction along the ring with step `d`. -/
theorem ring_induction {n : ℕ} (P : ZMod n → Prop) (d : ZMod n) (h : ∀ i, P i → P (i + d))
    (i : ZMod n) (hi : P i) (s : ℕ) : P (i + (s : ZMod n) * d) := by
  induction s with
  | zero => simpa using hi
  | succ s ih =>
    have e : i + ((s + 1 : ℕ) : ZMod n) * d = i + (s : ZMod n) * d + d := by
      push_cast
      ring
    rw [e]
    exact h _ ih

/-- Every cell is reached from `i` by steps of 1. -/
theorem exists_steps_one (n : ℕ) [NeZero n] (i c : ZMod n) : ∃ s : ℕ, c = i + (s : ZMod n) * 1 := by
  refine ⟨(c - i).val, ?_⟩
  rw [ZMod.natCast_zmod_val]
  ring

/-! ### Facts about bits -/

theorem bit_eq_one_of_ne_zero : ∀ a : ZMod 2, a ≠ 0 → a = 1 := by decide

theorem bit_inv : ∀ a b : ZMod 2, 1 + a * (1 + b) = 0 → a = 1 ∧ b = 0 := by decide

theorem bit_L1 : ∀ a b c a' b' c' : ZMod 2, c + a * (1 + b) = c' + a' * (1 + b') →
    a = a' → b = b' → c = c' := by decide

theorem bit_L2 : ∀ a b c a' b' c' : ZMod 2, c + a * (1 + b) = c' + a' * (1 + b') →
    a ≠ a' → b = b' → c ≠ c' → b = 0 := by decide

theorem bit_L3 : ∀ a b c a' b' c' : ZMod 2, c + a * (1 + b) = c' + a' * (1 + b') →
    a = a' → b ≠ b' → a = 0 → c = c' := by decide

theorem bit_L4 : ∀ a b c a' b' c' : ZMod 2, c + a * (1 + b) = c' + a' * (1 + b') →
    a ≠ a' → b ≠ b' → c ≠ c' → b = a + 1 := by decide

/-! ### Lemma 3.5: invariance of `M` -/

/-- If `F x` vanishes on the class `c` and `x` does not vanish on the class `c + 1`, then `x` vanishes on the
class `c`. -/
theorem Z_of_Z_F (n : ℕ) [NeZero n] (hn : Even n) (c : ZMod 2) (x : State n)
    (hF : Z n c (F154 n x)) (hx : ¬ Z n (c + 1) x) : Z n c x := by
  have hstep : ∀ j, par n j = c + 1 → x j = 1 → x (j - 2) = 1 ∧ x (j - 1) = 0 := by
    intro j hj hxj
    have hpar : par n (j - 1) = c := by
      rw [par_sub_one n hn, hj, add_assoc, CharTwo.add_self_eq_zero, add_zero]
    have h0 := hF (j - 1) hpar
    rw [F154_apply] at h0
    have e1 : j - 1 + 1 = j := by ring
    have e2 : j - 1 - 1 = j - 2 := by ring
    rw [e1, e2, hxj] at h0
    exact bit_inv _ _ h0
  have hex : ∃ j0, par n j0 = c + 1 ∧ x j0 = 1 := by
    by_contra hcon
    apply hx
    intro i hi
    by_contra hne
    exact hcon ⟨i, hi, bit_eq_one_of_ne_zero _ hne⟩
  obtain ⟨j0, hj0, hx0⟩ := hex
  have hall : ∀ s : ℕ, par n (j0 + (s : ZMod n) * (-2)) = c + 1 ∧ x (j0 + (s : ZMod n) * (-2)) = 1 := by
    intro s
    refine ring_induction (fun j => par n j = c + 1 ∧ x j = 1) (-2) ?_ j0 ⟨hj0, hx0⟩ s
    rintro j ⟨hj, hxj⟩
    have e : j + (-2) = j - 1 - 1 := by ring
    have e' : j + (-2) = j - 2 := by ring
    refine ⟨?_, ?_⟩
    · rw [e, par_sub_one n hn, par_sub_one n hn, hj, add_assoc, CharTwo.add_self_eq_zero, add_zero]
    · rw [e']
      exact (hstep j hj hxj).1
  intro i hi
  have hpar : par n (i + 1) = par n j0 := by rw [par_add_one n hn, hi, hj0]
  obtain ⟨s, hs⟩ := exists_step_back n hn j0 (i + 1) hpar
  have h1 := hall s
  rw [← hs] at h1
  have h2 := (hstep (i + 1) h1.1 h1.2).2
  have e : i + 1 - 1 = i := by ring
  rw [e] at h2
  exact h2

theorem F154_mem_parM (n : ℕ) [NeZero n] (hn : Even n) {x : State n} (hx : x ∈ parM n) :
    F154 n x ∈ parM n := by
  rw [mem_parM] at hx ⊢
  refine ⟨fun h => hx.1 (Z_of_Z_F n hn 1 x h ?_), fun h => hx.2 (Z_of_Z_F n hn 0 x h ?_)⟩
  · have e : (1 : ZMod 2) + 1 = 0 := CharTwo.add_self_eq_zero 1
    rw [e]
    exact hx.2
  · rw [zero_add]
    exact hx.1

/-! ### Lemma 3.6: collisions -/

/-- Two different states with the same image: `n` is even and `x` vanishes on a parity class. -/
theorem collision (n : ℕ) [NeZero n] (x y : State n) (hF : F154 n x = F154 n y) (hne : x ≠ y) :
    Even n ∧ ∃ c, Z n c x := by
  have tri : ∀ j, x (j + 2) + x j * (1 + x (j + 1)) = y (j + 2) + y j * (1 + y (j + 1)) := by
    intro j
    have h := congrFun hF (j + 1)
    rw [F154_apply, F154_apply] at h
    have e1 : j + 1 + 1 = j + 2 := by ring
    have e2 : j + 1 - 1 = j := by ring
    rw [e1, e2] at h
    exact h
  have e12 : ∀ j : ZMod n, j + 1 + 1 = j + 2 := fun j => by ring
  have e13 : ∀ j : ZMod n, j + 1 + 2 = j + 2 + 1 := fun j => by ring
  -- no two neighbouring cells on which `x` and `y` agree
  have NZ : ∀ i, ¬ (x i = y i ∧ x (i + 1) = y (i + 1)) := by
    rintro i ⟨h1, h2⟩
    apply hne
    have hall : ∀ s : ℕ, x (i + (s : ZMod n) * 1) = y (i + (s : ZMod n) * 1) ∧
        x (i + (s : ZMod n) * 1 + 1) = y (i + (s : ZMod n) * 1 + 1) := by
      intro s
      refine ring_induction (fun j => x j = y j ∧ x (j + 1) = y (j + 1)) 1 ?_ i ⟨h1, h2⟩ s
      rintro j ⟨ha, hb⟩
      refine ⟨hb, ?_⟩
      rw [e12]
      exact bit_L1 _ _ _ _ _ _ (tri j) ha hb
    funext c
    obtain ⟨s, hs⟩ := exists_steps_one n i c
    rw [hs]
    exact (hall s).1
  by_cases hA : ∃ i, x i = y i
  · -- Case A
    obtain ⟨i, hi⟩ := hA
    have hR0 : x (i - 1) ≠ y (i - 1) ∧ x (i - 1 + 1) = y (i - 1 + 1) := by
      have e : i - 1 + 1 = i := by ring
      refine ⟨fun h => NZ (i - 1) ⟨h, by rw [e]; exact hi⟩, by rw [e]; exact hi⟩
    have stepR : ∀ j, (x j ≠ y j ∧ x (j + 1) = y (j + 1)) →
        x (j + 1) = 0 ∧ (x (j + 2) ≠ y (j + 2) ∧ x (j + 2 + 1) = y (j + 2 + 1)) := by
      rintro j ⟨ha, hb⟩
      have hc : x (j + 2) ≠ y (j + 2) := fun h => NZ (j + 1) ⟨hb, by rw [e12]; exact h⟩
      have hb0 : x (j + 1) = 0 := bit_L2 _ _ _ _ _ _ (tri j) ha hb hc
      refine ⟨hb0, hc, ?_⟩
      have h3 := tri (j + 1)
      rw [e12, e13] at h3
      exact bit_L3 _ _ _ _ _ _ h3 hb hc hb0
    have hall : ∀ s : ℕ, x (i - 1 + (s : ZMod n) * 2) ≠ y (i - 1 + (s : ZMod n) * 2) ∧
        x (i - 1 + (s : ZMod n) * 2 + 1) = y (i - 1 + (s : ZMod n) * 2 + 1) := by
      intro s
      exact ring_induction (fun j => x j ≠ y j ∧ x (j + 1) = y (j + 1)) 2 (fun j hj => (stepR j hj).2)
        (i - 1) hR0 s
    have heven : Even n := by
      rcases Nat.even_or_odd n with h | ⟨m, hm⟩
      · exact h
      · exfalso
        have hcast : ((2 * m + 1 : ℕ) : ZMod n) = 0 := by
          rw [← hm]
          exact ZMod.natCast_self n
        have hs := (hall (m + 1)).1
        have e : i - 1 + ((m + 1 : ℕ) : ZMod n) * 2 = i - 1 + 1 := by
          push_cast at hcast ⊢
          linear_combination hcast
        rw [e] at hs
        exact hs hR0.2
    refine ⟨heven, par n i, ?_⟩
    intro c hc
    have hpar : par n c = par n (i - 1 + 1) := by
      have e : i - 1 + 1 = i := by ring
      rw [e, hc]
    obtain ⟨s, hs⟩ := exists_step n heven (i - 1 + 1) c hpar
    have h1 := (stepR _ (hall s)).1
    have e : i - 1 + 1 + (s : ZMod n) * 2 = i - 1 + (s : ZMod n) * 2 + 1 := by ring
    rw [hs, e]
    exact h1
  · -- Case B: `x` and `y` differ at every cell
    have hB : ∀ i, x i ≠ y i := fun i h => hA ⟨i, h⟩
    have halt : ∀ j, x (j + 1) = x j + 1 := fun j =>
      bit_L4 _ _ _ _ _ _ (tri j) (hB j) (hB (j + 1)) (hB (j + 2))
    have hwalk : ∀ s : ℕ, x ((s : ZMod n)) = x 0 + (s : ZMod 2) := by
      intro s
      induction s with
      | zero => simp
      | succ s ih =>
        push_cast
        rw [halt, ih, add_assoc]
    have heven : Even n := by
      have h := hwalk n
      rw [ZMod.natCast_self] at h
      have h0 : ((n : ℕ) : ZMod 2) = 0 := by
        have : x 0 + 0 = x 0 + ((n : ℕ) : ZMod 2) := by rw [add_zero]; exact h
        exact (add_left_cancel this).symm
      exact ZMod.natCast_eq_zero_iff_even.mp h0
    refine ⟨heven, x 0, ?_⟩
    intro c hc
    have h := hwalk c.val
    rw [ZMod.natCast_zmod_val] at h
    have hp : ((c.val : ℕ) : ZMod 2) = x 0 := hc
    rw [h, hp]
    exact CharTwo.add_self_eq_zero _

/-- Paper, Lemma 3.6, "in particular": for odd `n` the map is injective. -/
theorem F154_injective_of_odd (n : ℕ) [NeZero n] (hn : ¬ Even n) : Function.Injective (F154 n) := by
  intro x y h
  by_contra hne
  exact hn (collision n x y h hne).1

/-- Paper, Lemma 3.6, "in particular": two different states with the same image lie outside `M`. -/
theorem collision_not_mem (n : ℕ) [NeZero n] (x y : State n) (hF : F154 n x = F154 n y) (hne : x ≠ y) :
    x ∉ parM n ∧ y ∉ parM n :=
  ⟨Z_cases n (collision n x y hF hne).2, Z_cases n (collision n y x hF.symm (Ne.symm hne)).2⟩

/-! ### Lemma 3.7: periodic states -/

/-- A map that sends a set into itself and is injective on it has only periodic points in the set. -/
theorem periodic_of_injOn {X : Type} [Fintype X] (F : X → X) (S : Set X)
    (hmaps : ∀ x ∈ S, F x ∈ S) (hinj : ∀ x ∈ S, ∀ y ∈ S, F x = F y → x = y) :
    ∀ x ∈ S, x ∈ periodicPts F := by
  have hmapsT : ∀ (t : ℕ) (x : X), x ∈ S → F^[t] x ∈ S := by
    intro t
    induction t with
    | zero => intro x hx; exact hx
    | succ t ih =>
      intro x hx
      rw [Function.iterate_succ_apply']
      exact hmaps _ (ih x hx)
  have hinjT : ∀ (t : ℕ), ∀ x ∈ S, ∀ y ∈ S, F^[t] x = F^[t] y → x = y := by
    intro t
    induction t with
    | zero => intro x _ y _ h; exact h
    | succ t ih =>
      intro x hx y hy h
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply'] at h
      exact ih x hx y hy (hinj _ (hmapsT t x hx) _ (hmapsT t y hy) h)
  intro x hx
  obtain ⟨t, ht⟩ := exists_iterate_periodic F x
  obtain ⟨p, hp, hper⟩ := mem_periodicPts.mp ht
  have h1 : F^[t] (F^[p] x) = F^[t] x := by
    rw [← Function.iterate_add_apply, Nat.add_comm, Function.iterate_add_apply]
    exact hper
  exact mem_periodicPts.mpr ⟨p, hp, hinjT t _ (hmapsT p x hx) x hx h1⟩

/-- Paper, Lemma 3.7: for even `n` every state of `M` is periodic. -/
theorem periodic_of_mem_parM (n : ℕ) [NeZero n] (hn : Even n) {x : State n} (hx : x ∈ parM n) :
    x ∈ periodicPts (F154 n) := by
  refine periodic_of_injOn (F154 n) (parM n) (fun y hy => F154_mem_parM n hn hy) ?_ x hx
  intro y hy z _ h
  by_contra hne
  exact (collision_not_mem n y z h hne).1 hy

/-- For odd `n` every state is periodic. -/
theorem periodic_of_odd (n : ℕ) [NeZero n] (hn : ¬ Even n) (x : State n) :
    x ∈ periodicPts (F154 n) :=
  periodic_of_injOn (F154 n) Set.univ (fun _ _ => Set.mem_univ _)
    (fun _ _ _ _ h => F154_injective_of_odd n hn h) x (Set.mem_univ x)

end RingSize.Rule154

end
