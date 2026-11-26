module

public import RingSize.TheoremA.Paths
import Mathlib.Algebra.CharP.Two
import Mathlib.Data.Fintype.Prod
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Tactic.NormNum

/-!
# Elementary cellular automata on a ring: Lemmas 2.2 and 2.3

Proofs for Part 3 of `Statement.lean`.
-/

public section

namespace RingSize.TheoremA

open Function

variable (n : ℕ) [NeZero n] (f : LocalRule)

/-! ### The resistance and the flips -/

theorem resistanceECA : ResistanceECA := by
  intro n _ f x y
  unfold resistance
  rw [hammingDist_eq_zero]
  exact eq_comm

theorem ruleOfNumber_90 : ∀ a b c : ZMod 2, ruleOfNumber 90 a b c = a + c := by decide

theorem rule90IsRuleNumber90 : Rule90IsRuleNumber90 := by
  intro n _
  funext x i
  simp only [rule90, globalMap, ruleOfNumber_90]

theorem zmod2_eq_add_one : ∀ a b : ZMod 2, a ≠ b → b = a + 1 := by decide

theorem zmod2_ne_add_one : ∀ a : ZMod 2, a ≠ a + 1 := by decide

omit [NeZero n] in
theorem e_apply_self (j : ZMod n) : e n j j = 1 := by simp [e]

omit [NeZero n] in
theorem e_apply_ne {i j : ZMod n} (h : i ≠ j) : e n j i = 0 := by simp [e, h]

/-- A state and its flip differ in exactly one cell. -/
theorem hammingDist_flip (x : State n) (j : ZMod n) : hammingDist x (flip n x j) = 1 := by
  unfold hammingDist flip
  have hset : (Finset.univ.filter fun i => x i ≠ (x + e n j) i) = {j} := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton, Pi.add_apply]
    constructor
    · intro h
      by_contra hij
      apply h
      rw [e_apply_ne n hij, add_zero]
    · intro hij
      rw [hij, e_apply_self]
      exact zmod2_ne_add_one (x j)
  rw [hset, Finset.card_singleton]

/-- Two states at Hamming distance 1 differ by a flip. -/
theorem exists_flip_of_hammingDist_eq_one {x y : State n} (h : hammingDist x y = 1) :
    ∃ j, y = flip n x j := by
  unfold hammingDist at h
  obtain ⟨j, hj⟩ := Finset.card_eq_one.mp h
  refine ⟨j, ?_⟩
  funext i
  unfold flip
  by_cases hij : i = j
  · have hmem : i ∈ Finset.univ.filter (fun i => x i ≠ y i) := by
      rw [hj, hij]
      exact Finset.mem_singleton_self j
    have hne : x i ≠ y i := (Finset.mem_filter.mp hmem).2
    rw [Pi.add_apply, hij, e_apply_self, ← hij]
    exact zmod2_eq_add_one _ _ hne
  · have hnot : i ∉ Finset.univ.filter (fun i => x i ≠ y i) := by
      rw [hj]
      simpa using hij
    have heq : x i = y i := by
      by_contra hne
      exact hnot (Finset.mem_filter.mpr ⟨Finset.mem_univ _, hne⟩)
    rw [Pi.add_apply, e_apply_ne n hij, add_zero]
    exact heq.symm

omit [NeZero n] in
theorem flip_flip (x : State n) (j : ZMod n) : flip n (flip n x j) j = x := by
  funext i
  unfold flip
  rw [Pi.add_apply, Pi.add_apply, add_assoc, CharTwo.add_self_eq_zero, add_zero]

/-! ### Lemma 2.3 -/

variable {n f} in
theorem VE_eq_one_iff {C C' : Cyc (globalMap n f)} (hne : C ≠ C') :
    VE n f C C' = 1 ↔ ∃ x ∈ C.1, ∃ j, EndsOn (globalMap n f) (flip n x j) C' := by
  have hr := resistanceECA n f
  rw [Vc_eq_one_iff hr hne]
  constructor
  · rintro ⟨y, hy, z, hrz, hz⟩
    obtain ⟨j, hj⟩ := exists_flip_of_hammingDist_eq_one n hrz
    rw [hj] at hz
    exact ⟨globalMap n f y, C.iterate_mem _ hy 1, j, hz⟩
  · rintro ⟨x, hx, j, hend⟩
    obtain ⟨y, hy, hyx⟩ := C.exists_preimage _ hx
    refine ⟨y, hy, flip n x j, ?_, hend⟩
    show hammingDist (globalMap n f y) (flip n x j) = 1
    rw [hyx]
    exact hammingDist_flip n x j

theorem lemma_2_3 : Lemma_2_3 := by
  intro n _ f C C' hne
  have hr := resistanceECA n f
  refine ⟨one_le_Vc hr hne, VE_eq_one_iff hne, ?_⟩
  intro x hx j hflip
  refine ⟨(VE_eq_one_iff hne).mpr ⟨x, hx, j, 0, hflip⟩, ?_⟩
  refine (VE_eq_one_iff (Ne.symm hne)).mpr ⟨flip n x j, hflip, j, 0, ?_⟩
  show flip n (flip n x j) j ∈ C.1
  rw [flip_flip]
  exact hx

/-! ### Lemma 2.2 -/

omit [NeZero n] in
/-- For `n ≥ 3` every code occurs in some state. -/
theorem D_nonempty (hn : 3 ≤ n) (v : Code) : (D n v).Nonempty := by
  obtain ⟨a, b, c⟩ := v
  have h10 : (1 : ZMod n) ≠ 0 := by
    intro h
    have h' : ((1 : ℕ) : ZMod n) = 0 := by exact_mod_cast h
    rw [ZMod.natCast_eq_zero_iff] at h'
    have := Nat.le_of_dvd (by norm_num) h'
    omega
  have h20 : (2 : ZMod n) ≠ 0 := by
    intro h
    have h' : ((2 : ℕ) : ZMod n) = 0 := by exact_mod_cast h
    rw [ZMod.natCast_eq_zero_iff] at h'
    have := Nat.le_of_dvd (by norm_num) h'
    omega
  have h21 : (2 : ZMod n) ≠ 1 := by
    intro h
    apply h10
    have h' : (1 : ZMod n) + 1 = 1 + 0 := by rw [add_zero, one_add_one_eq_two]; exact h
    exact add_left_cancel h'
  refine ⟨fun i => if i = 0 then a else if i = 1 then b else if i = 2 then c else 0, 1, ?_⟩
  simp [sub_self, one_add_one_eq_two, h10, h20, h21]

/-- The quantity minimized in the definition of `k_v`. -/
noncomputable abbrev kTerm (v : Code) (C : Cyc (globalMap n f)) : ℕ :=
  gamma (VE n f) C + R (resistance n f) C.1 (D n v)

theorem cyc_nonempty : Nonempty (Cyc (globalMap n f)) := by
  obtain ⟨C, _, _⟩ := endsOn_existsUnique (globalMap n f) (0 : State n)
  exact ⟨C⟩

theorem gammaMin_le_sInf_kTerm (v : Code) :
    gammaMin (VE n f) ≤ sInf (Set.range (kTerm n f v)) := by
  have hne : (Set.range (kTerm n f v)).Nonempty := by
    obtain ⟨C⟩ := cyc_nonempty n f
    exact ⟨_, C, rfl⟩
  obtain ⟨C, hC⟩ := Nat.sInf_mem hne
  rw [← hC]
  exact (gammaMin_le (VE n f) C).trans (Nat.le_add_right _ _)

theorem kIndex_eq_zero_iff (hn : 3 ≤ n) (v : Code) :
    kIndex n f v = 0 ↔ ∃ C ∈ Sel (VE n f), ∃ x ∈ C.1, Contains n x v := by
  have hr := resistanceECA n f
  have hge := gammaMin_le_sInf_kTerm n f v
  have hne : (Set.range (kTerm n f v)).Nonempty := by
    obtain ⟨C⟩ := cyc_nonempty n f
    exact ⟨_, C, rfl⟩
  have hk : kIndex n f v = sInf (Set.range (kTerm n f v)) - gammaMin (VE n f) := rfl
  constructor
  · intro h0
    obtain ⟨C, hC⟩ := Nat.sInf_mem hne
    have hCmin : kTerm n f v C = gammaMin (VE n f) := by omega
    have hg := gammaMin_le (VE n f) C
    have hsel : gamma (VE n f) C = gammaMin (VE n f) := by
      have : kTerm n f v C = gamma (VE n f) C + R (resistance n f) C.1 (D n v) := rfl
      omega
    have hR : R (resistance n f) C.1 (D n v) = 0 := by
      have : kTerm n f v C = gamma (VE n f) C + R (resistance n f) C.1 (D n v) := rfl
      omega
    obtain ⟨x, hxC, hxD⟩ := (R_cycle_eq_zero_iff hr C (D_nonempty n hn v)).mp hR
    exact ⟨C, hsel, x, hxC, hxD⟩
  · rintro ⟨C, hsel, x, hxC, hxD⟩
    have hR : R (resistance n f) C.1 (D n v) = 0 :=
      (R_cycle_eq_zero_iff hr C (D_nonempty n hn v)).mpr ⟨x, hxC, hxD⟩
    have hsel' : gamma (VE n f) C = gammaMin (VE n f) := hsel
    have hle : sInf (Set.range (kTerm n f v)) ≤ kTerm n f v C := Nat.sInf_le ⟨C, rfl⟩
    have : kTerm n f v C = gamma (VE n f) C + R (resistance n f) C.1 (D n v) := rfl
    omega

theorem kStar_eq_zero_iff : kStar n f = 0 ↔ ∀ v : Code, kIndex n f v = 0 := by
  unfold kStar
  rw [← Nat.bot_eq_zero, Finset.sup_eq_bot_iff]
  simp

theorem kIndex_le_one (v : Code)
    (h : ∃ C ∈ Sel (VE n f), ∃ x ∈ C.1, ∃ j, Contains n (flip n x j) v) : kIndex n f v ≤ 1 := by
  obtain ⟨C, hsel, x, hxC, j, hcont⟩ := h
  obtain ⟨y, hy, hyx⟩ := C.exists_preimage _ hxC
  have hpath := R_le_of_path (resistance n f) (A := C.1) (B := D n v) [y, flip n x j]
    (List.cons_ne_nil _ _) hy hcont
  have hres : pathRes (resistance n f) [y, flip n x j] = 1 := by
    show hammingDist (globalMap n f y) (flip n x j) + 0 = 1
    rw [hyx, hammingDist_flip]
  rw [hres] at hpath
  have hsel' : gamma (VE n f) C = gammaMin (VE n f) := hsel
  have hle : sInf (Set.range (kTerm n f v)) ≤ kTerm n f v C := Nat.sInf_le ⟨C, rfl⟩
  have hk : kIndex n f v = sInf (Set.range (kTerm n f v)) - gammaMin (VE n f) := rfl
  have : kTerm n f v C = gamma (VE n f) C + R (resistance n f) C.1 (D n v) := rfl
  omega

theorem lemma_2_2 : Lemma_2_2 := by
  intro n _ hn f
  refine ⟨fun v => kIndex_eq_zero_iff n f hn v, ?_, fun v h => kIndex_le_one n f v h⟩
  rw [kStar_eq_zero_iff]
  exact forall_congr' fun v => kIndex_eq_zero_iff n f hn v

/-! ### The consequence of Theorem 2.8 for `k*` -/

theorem corollary_2_8 : Corollary_2_8 := by
  intro n _ hn f K hK huniq
  have hr := resistanceECA n f
  have hSel : Sel (VE n f) = K := ((theorem_2_8 (State n) (globalMap n f) (resistance n f) hr).2 K hK huniq).1
  rw [(lemma_2_2 n hn f).2.1, hSel]

end RingSize.TheoremA

end
