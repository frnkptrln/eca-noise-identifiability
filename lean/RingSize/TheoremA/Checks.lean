module

public import RingSize.TheoremA.ECA

/-!
# Checks of the definitions

Proofs of the statements in the section "Checks of the definitions" of `Statement.lean`.
-/

public section

namespace RingSize.TheoremA

open Function

universe u

theorem inTree_iff_reaches : InTree_iff_reaches.{u} := by
  intro ι _ c p
  exact isInTree_iff_reaches

/-- A set that no edge of `G_1` leaves contains everything reachable from it. -/
theorem reach_mem_of_closed {ι : Type u} (V : ι → ι → ℕ) {K : Set ι}
    (hcl : ∀ a ∈ K, ∀ b, G1 V a b → b ∈ K) {a b : ι} (ha : a ∈ K) (h : Reach V a b) : b ∈ K := by
  unfold Reach at h
  induction h with
  | refl => exact ha
  | tail _ hbc ih => exact hcl _ ih _ hbc

theorem closedClass_iff_component : ClosedClass_iff_component.{u} := by
  intro ι V K
  constructor
  · rintro ⟨⟨a, haK⟩, hsc, hcl⟩
    refine ⟨a, ?_, hcl⟩
    ext b
    constructor
    · intro hb
      exact ⟨hsc a haK b hb, hsc b hb a haK⟩
    · rintro ⟨hab, -⟩
      exact reach_mem_of_closed V hcl haK hab
  · rintro ⟨a, rfl, hcl⟩
    refine ⟨⟨a, reach_refl a, reach_refl a⟩, ?_, hcl⟩
    rintro b ⟨-, hba⟩ c ⟨hac, -⟩
    exact reach_trans hba hac

theorem treeWeight_lower_bound : TreeWeight_lower_bound.{u} := by
  intro X _ _ F r hr C p hT
  rw [numCycles, Nat.card_eq_fintype_card]
  exact card_sub_one_le_treeWeight (Vc F r) (fun _ _ hab => one_le_Vc hr hab) hT

theorem gamma_lower_bound : Gamma_lower_bound.{u} := by
  intro X _ _ F r hr C
  obtain ⟨p, hT, hw⟩ := exists_tree_gamma (Vc F r) C
  rw [← hw, numCycles, Nat.card_eq_fintype_card]
  exact card_sub_one_le_treeWeight (Vc F r) (fun _ _ hab => one_le_Vc hr hab) hT

theorem ruleOfNumber_204 : ∀ a b c : ZMod 2, ruleOfNumber 204 a b c = b := by decide

theorem rule204_cycles : Rule204_cycles := by
  intro n _ x
  have hF : ∀ y : State n, globalMap n (ruleOfNumber 204) y = y := by
    intro y
    funext i
    simp only [globalMap, ruleOfNumber_204]
  have hit : ∀ (t : ℕ) (y : State n), (globalMap n (ruleOfNumber 204))^[t] y = y := by
    intro t
    induction t with
    | zero => intro y; rfl
    | succ t ih => intro y; rw [Function.iterate_succ_apply, hF, ih]
  refine ⟨x, mem_periodicPts.mpr ⟨1, Nat.one_pos, hit 1 x⟩, ?_⟩
  ext y
  constructor
  · intro hy
    exact ⟨0, (Set.mem_singleton_iff.mp hy).symm⟩
  · rintro ⟨t, ht⟩
    rw [hit] at ht
    exact Set.mem_singleton_iff.mpr ht.symm

theorem rule154_local : Rule154_local := by
  unfold Rule154_local
  decide

theorem ruleOfNumber_170 : ∀ a b c : ZMod 2, ruleOfNumber 170 a b c = c := by decide

theorem rule170_shift : Rule170_shift := by
  intro n _ x i
  simp only [globalMap, ruleOfNumber_170]

theorem section_2_4_ECA : Section_2_4_ECA := by
  intro n _ f
  have hr := resistanceECA n f
  have h8 := theorem_2_8.{0} (State n) (globalMap n f) (resistance n f) hr
  exact ⟨lemma_2_5.{0} (State n) (globalMap n f) (resistance n f) hr,
    lemma_2_6.{0} (State n) (globalMap n f) (resistance n f) hr,
    lemma_2_7.{0} (State n) (globalMap n f) (resistance n f) hr, h8.1, h8.2⟩

theorem kIndex_subtraction_exact : KIndex_subtraction_exact := by
  intro n _ f v
  exact gammaMin_le_sInf_kTerm n f v

end RingSize.TheoremA

end
