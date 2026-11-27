module

public import RingSize.Rule154.Statement
public import RingSize.TheoremA.Checks
public import RingSize.Proof
import Mathlib.Algebra.CharP.Two
import Mathlib.Data.ZMod.Basic

/-!
# Rule 154 on a ring whose size is a power of two: proofs

Proofs of the statements of `RingSize/Rule154/Statement.lean`. The parity of a cell `i : ZMod n` is the
image of `i.val` in `ZMod 2`; for even `n` it is the image of `i` under the ring homomorphism
`ZMod n → ZMod 2`, so the neighbours of a cell have the other parity.
-/

public section

namespace RingSize.Rule154

open Function RingSize.TheoremA

/-- The parity of a cell. -/
@[expose] def par (n : ℕ) (i : ZMod n) : ZMod 2 :=
  ((i.val : ℕ) : ZMod 2)

theorem zmod2_cases : ∀ a : ZMod 2, a = 0 ∨ a = 1 := by decide

theorem par_eq_castHom (n : ℕ) [NeZero n] (h : 2 ∣ n) (a : ZMod n) :
    par n a = ZMod.castHom h (ZMod 2) a := by
  unfold par
  rw [ZMod.castHom_apply, ZMod.natCast_val]

theorem par_add_one (n : ℕ) [NeZero n] (hn : Even n) (i : ZMod n) : par n (i + 1) = par n i + 1 := by
  have h : 2 ∣ n := hn.two_dvd
  rw [par_eq_castHom n h, par_eq_castHom n h, map_add, map_one]

theorem par_sub_one (n : ℕ) [NeZero n] (hn : Even n) (i : ZMod n) : par n (i - 1) = par n i + 1 := by
  have h : 2 ∣ n := hn.two_dvd
  rw [par_eq_castHom n h, par_eq_castHom n h, map_sub, map_one, CharTwo.sub_eq_add]

theorem mem_parE (n : ℕ) {x : State n} : x ∈ parE n ↔ ∀ i, par n i = 1 → x i = 0 := by
  unfold parE par
  simp only [Set.mem_ofPred_eq, ZMod.natCast_eq_one_iff_odd]

theorem mem_parO (n : ℕ) {x : State n} : x ∈ parO n ↔ ∀ i, par n i = 0 → x i = 0 := by
  unfold parO par
  simp only [Set.mem_ofPred_eq, ZMod.natCast_eq_zero_iff_even]

theorem exists_par_of_mem (n : ℕ) {x : State n} (hx : x ∈ parE n ∪ parO n) :
    ∃ c : ZMod 2, ∀ i, par n i = c → x i = 0 := by
  rcases hx with h | h
  · exact ⟨1, (mem_parE n).mp h⟩
  · exact ⟨0, (mem_parO n).mp h⟩

/-- Paper, Lemma 3.2, as a formula for the global map. -/
theorem F154_apply (n : ℕ) [NeZero n] (x : State n) (i : ZMod n) :
    F154 n x i = x (i + 1) + x (i - 1) * (1 + x i) := by
  show ruleOfNumber 154 (x (i - 1)) (x i) (x (i + 1)) = _
  exact rule154_local _ _ _

/-- One step on a parity class: if `x` vanishes on the cells of parity `c`, then `F x = L x`, and `F x`
vanishes on the cells of the other parity. -/
theorem step_aux (n : ℕ) [NeZero n] (hn : Even n) (c : ZMod 2) {x : State n}
    (hx : ∀ i, par n i = c → x i = 0) :
    F154 n x = rule90 n x ∧ ∀ i, par n i = c + 1 → F154 n x i = 0 := by
  have key : ∀ i, F154 n x i = rule90 n x i ∧ (par n i = c + 1 → F154 n x i = 0) := by
    intro i
    rw [F154_apply]
    show x (i + 1) + x (i - 1) * (1 + x i) = x (i - 1) + x (i + 1) ∧ _
    by_cases hi : par n i = c
    · have hxi := hx i hi
      refine ⟨by rw [hxi, add_zero, mul_one, add_comm], fun h => ?_⟩
      exact absurd (hi.symm.trans h) (zmod2_ne_add_one c)
    · have hpar : par n i = c + 1 := zmod2_eq_add_one c (par n i) (Ne.symm hi)
      have h1 : x (i + 1) = 0 :=
        hx _ (by rw [par_add_one n hn, hpar, add_assoc, CharTwo.add_self_eq_zero, add_zero])
      have h2 : x (i - 1) = 0 :=
        hx _ (by rw [par_sub_one n hn, hpar, add_assoc, CharTwo.add_self_eq_zero, add_zero])
      exact ⟨by rw [h1, h2, zero_mul, add_zero], fun _ => by rw [h1, h2, zero_mul, add_zero]⟩
  exact ⟨funext fun i => (key i).1, fun i => (key i).2⟩

theorem iterate_aux (n : ℕ) [NeZero n] (hn : Even n) :
    ∀ (t : ℕ) (c : ZMod 2) (x : State n), (∀ i, par n i = c → x i = 0) →
      (F154 n)^[t] x = (rule90 n)^[t] x := by
  intro t
  induction t with
  | zero => intro c x _; rfl
  | succ t ih =>
    intro c x hx
    obtain ⟨hF, hO⟩ := step_aux n hn c hx
    rw [Function.iterate_succ_apply, Function.iterate_succ_apply, ← hF]
    exact ih (c + 1) (F154 n x) hO

theorem lemma_3_3 : Lemma_3_3 := by
  intro n _ hn x
  refine ⟨fun hx => ?_, fun hx => ?_, fun hx t => ?_⟩
  · obtain ⟨hF, hO⟩ := step_aux n hn 1 ((mem_parE n).mp hx)
    refine ⟨(mem_parO n).mpr fun i hi => hO i ?_, hF⟩
    rw [hi]
    exact (CharTwo.add_self_eq_zero (1 : ZMod 2)).symm
  · obtain ⟨hF, hE⟩ := step_aux n hn 0 ((mem_parO n).mp hx)
    refine ⟨(mem_parE n).mpr fun i hi => hE i ?_, hF⟩
    rw [hi, zero_add]
  · obtain ⟨c, hc⟩ := exists_par_of_mem n hx
    exact iterate_aux n hn t c x hc

theorem lemma_3_4_a : Lemma_3_4_a := by
  intro n _ k hk x hx
  subst hk
  have hn : Even (2 ^ (k + 1)) := Nat.even_pow.mpr ⟨even_two, Nat.succ_ne_zero k⟩
  have hhalf : 2 ^ (k + 1) / 2 = 2 ^ k := by
    rw [pow_succ]
    exact Nat.mul_div_cancel _ (by norm_num)
  obtain ⟨c, hc⟩ := exists_par_of_mem _ hx
  rw [hhalf, iterate_aux _ hn (2 ^ k) c x hc]
  exact iterate_half_eq_zero k x

theorem single_aux (n : ℕ) (j : ZMod n) : ∀ i, par n i = par n j + 1 → e n j i = 0 := by
  intro i hi
  refine e_apply_ne n fun hij => ?_
  rw [hij] at hi
  exact zmod2_ne_add_one _ hi

theorem single_mem : Single_mem := by
  intro n j
  rcases zmod2_cases (par n j) with h | h
  · left
    rw [mem_parE]
    intro i hi
    exact single_aux n j i (by rw [hi, h, zero_add])
  · right
    rw [mem_parO]
    intro i hi
    refine single_aux n j i ?_
    rw [hi, h]
    exact (CharTwo.add_self_eq_zero (1 : ZMod 2)).symm

theorem F154_zero (n : ℕ) [NeZero n] : F154 n 0 = 0 := by
  funext i
  rw [F154_apply]
  simp

/-- A fixed point is a cycle by itself. -/
theorem isCycle_singleton {X : Type} (F : X → X) {x : X} (h : F x = x) : IsCycle F {x} := by
  have hit : ∀ t, F^[t] x = x := fun t => Function.iterate_fixed h t
  refine ⟨x, mem_periodicPts.mpr ⟨1, Nat.one_pos, hit 1⟩, ?_⟩
  ext y
  constructor
  · intro hy
    exact ⟨0, (Set.mem_singleton_iff.mp hy).symm⟩
  · rintro ⟨t, ht⟩
    rw [hit] at ht
    exact Set.mem_singleton_iff.mpr ht.symm

theorem zero_cycle : Zero_cycle := fun n _ => isCycle_singleton (F154 n) (F154_zero n)

/-- Paper, Theorem 3.9(b). The paper refers to part (a) (the list of the cycles) for the fact that no state
of the orbit of `e_j` lies on a cycle other than `{0}`. Here this follows from the invariance of cycles:
a cycle that contains a state of the orbit contains its later states, hence `0`. -/
theorem theorem_3_9_b : Theorem_3_9_b := by
  intro n _ k hk C0 hC0
  have hr := resistanceECA n (ruleOfNumber 154)
  have h0 : (0 : State n) ∈ C0.1 := by
    rw [hC0]
    exact Set.mem_singleton _
  have hno : ∀ C : Cyc (F154 n), C ≠ C0 → VE n (ruleOfNumber 154) C0 C ≠ 1 := by
    intro C hne h1
    obtain ⟨x, hx, j, t, ht⟩ := (VE_eq_one_iff (Ne.symm hne)).mp h1
    rw [hC0] at hx
    have hx0 : x = 0 := Set.mem_singleton_iff.mp hx
    have hflip : TheoremA.flip n x j = e n j := by
      rw [hx0]
      unfold TheoremA.flip
      rw [zero_add]
    rw [hflip] at ht
    have hdie := lemma_3_4_a n k hk (e n j) (single_mem n j)
    have hmem := C.iterate_mem (F154 n) ht (n / 2)
    rw [← Function.iterate_add_apply, Nat.add_comm (n / 2) t, Function.iterate_add_apply, hdie,
      Function.iterate_fixed (F154_zero n)] at hmem
    exact hne (Cyc.eq_of_mem (F154 n) hmem h0)
  refine ⟨fun C hne => ?_, fun C hG => ?_⟩
  · have h1 : 1 ≤ VE n (ruleOfNumber 154) C0 C := one_le_Vc hr (Ne.symm hne)
    have h2 := hno C hne
    omega
  · by_cases hC : C = C0
    · rw [hC] at hG
      have hle : VE n (ruleOfNumber 154) C0 C0 ≤ 0 :=
        R_le_of_path _ [0] (List.cons_ne_nil _ _) h0 h0
      have h1 : VE n (ruleOfNumber 154) C0 C0 = 1 := hG
      omega
    · exact hno C hC hG

end RingSize.Rule154

end
