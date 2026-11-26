module

public import RingSize.TheoremA.StatementRotation
public import RingSize.TheoremA.Checks

/-!
# Lemma 2.4 (rotation): proofs

A bijection of the nodes that preserves the weights maps in-trees to in-trees of the same weight; a bijection
of the states that commutes with `F` and preserves the resistance maps cycles to cycles and paths to paths
of the same resistance.
-/

public section

namespace RingSize.TheoremA

open Function

universe u

/-! ### Weighted graphs: a bijection of the nodes that preserves the weights -/

section Graph

variable {ι : Type u} [Fintype ι] [DecidableEq ι] (V : ι → ι → ℕ)

omit [Fintype ι] [DecidableEq ι] in
theorem iterate_conj (τ : ι ≃ ι) (p : ι → ι) (k : ℕ) (d : ι) :
    (fun a => τ (p (τ.symm a)))^[k] d = τ (p^[k] (τ.symm d)) := by
  induction k generalizing d with
  | zero => simp
  | succ k ih =>
    rw [Function.iterate_succ_apply, ih, Equiv.symm_apply_apply, ← Function.iterate_succ_apply]

omit [Fintype ι] [DecidableEq ι] in
/-- The image of an in-tree rooted at `c` is an in-tree rooted at `τ c`. -/
theorem isInTree_conj (τ : ι ≃ ι) {c : ι} {p : ι → ι} (hT : IsInTree c p) :
    IsInTree (τ c) (fun a => τ (p (τ.symm a))) := by
  intro d k hk hne
  rw [iterate_conj]
  intro h
  have h' : p^[k] (τ.symm d) = τ.symm d := ((Equiv.symm_apply_eq τ).mpr h.symm).symm
  refine hT (τ.symm d) k hk ?_ h'
  intro j hj hc
  apply hne j hj
  rw [iterate_conj, hc]

/-- The image tree has the same weight. -/
theorem treeWeight_conj (τ : ι ≃ ι) (hV : ∀ a b, V (τ a) (τ b) = V a b) (c : ι) (p : ι → ι) :
    treeWeight V (τ c) (fun a => τ (p (τ.symm a))) = treeWeight V c p := by
  unfold treeWeight
  symm
  refine Finset.sum_equiv τ ?_ ?_
  · intro i
    simp
  · intro i _
    simp [hV]

theorem gamma_conj_le (τ : ι ≃ ι) (hV : ∀ a b, V (τ a) (τ b) = V a b) (c : ι) :
    gamma V (τ c) ≤ gamma V c := by
  obtain ⟨p, hT, hw⟩ := exists_tree_gamma V c
  rw [← hw, ← treeWeight_conj V τ hV c p]
  exact gamma_le V (isInTree_conj τ hT)

/-- `γ(τ c) = γ(c)`. -/
theorem gamma_conj (τ : ι ≃ ι) (hV : ∀ a b, V (τ a) (τ b) = V a b) (c : ι) :
    gamma V (τ c) = gamma V c := by
  apply le_antisymm (gamma_conj_le V τ hV c)
  have hV' : ∀ a b, V (τ.symm a) (τ.symm b) = V a b := by
    intro a b
    have h := hV (τ.symm a) (τ.symm b)
    rw [Equiv.apply_symm_apply, Equiv.apply_symm_apply] at h
    exact h.symm
  have h := gamma_conj_le V τ.symm hV' (τ c)
  rw [Equiv.symm_apply_apply] at h
  exact h

end Graph

/-! ### Dynamics: a bijection of the states that commutes with `F` and preserves `r` -/

section Dynamics

variable {X : Type u} (F : X → X) (r : X → X → ℕ)

theorem iterate_comm_of_comm (s : X → X) (hs : ∀ x, F (s x) = s (F x)) :
    ∀ (t : ℕ) (y : X), F^[t] (s y) = s (F^[t] y) := by
  intro t
  induction t with
  | zero => intro y; rfl
  | succ t ih =>
    intro y
    rw [Function.iterate_succ_apply, hs, ih, ← Function.iterate_succ_apply]

/-- The image of a cycle is a cycle. -/
theorem isCycle_image (s : X → X) (hs : ∀ x, F (s x) = s (F x)) (C : Cyc F) :
    IsCycle F (s '' C.1) := by
  obtain ⟨x, hx, hC⟩ := C.2
  have hit := iterate_comm_of_comm F s hs
  refine ⟨s x, ?_, ?_⟩
  · obtain ⟨n, hn, hper⟩ := mem_periodicPts.mp hx
    refine mem_periodicPts.mpr ⟨n, hn, ?_⟩
    show F^[n] (s x) = s x
    rw [hit, hper.eq]
  · rw [hC]
    ext y
    constructor
    · rintro ⟨z, ⟨t, rfl⟩, rfl⟩
      exact ⟨t, hit t x⟩
    · rintro ⟨t, rfl⟩
      exact ⟨F^[t] x, ⟨t, rfl⟩, (hit t x).symm⟩

theorem pathRes_map (s : X → X) (hr : ∀ x y, r (s x) (s y) = r x y) :
    ∀ l : List X, pathRes r (l.map s) = pathRes r l
  | [] => rfl
  | [_] => rfl
  | x :: y :: l => by
    show r (s x) (s y) + pathRes r ((y :: l).map s) = r x y + pathRes r (y :: l)
    rw [hr, pathRes_map s hr (y :: l)]

theorem R_image_le (s : X → X) (hr : ∀ x y, r (s x) (s y) = r x y) {A B : Set X}
    (hA : A.Nonempty) (hB : B.Nonempty) : R r (s '' A) (s '' B) ≤ R r A B := by
  obtain ⟨l, h, hAl, hBl, hres⟩ := exists_path_R r hA hB
  rw [← hres, ← pathRes_map r s hr l]
  have hne : l.map s ≠ [] := by simpa using h
  refine R_le_of_path r (l.map s) hne ?_ ?_
  · rw [List.head_map]
    exact ⟨_, hAl, rfl⟩
  · rw [List.getLast_map]
    exact ⟨_, hBl, rfl⟩

end Dynamics

theorem lemma_2_4_general : Lemma_2_4_general.{u} := by
  intro X _ _ F r s hs hr
  have hs' : ∀ x, F (s.symm x) = s.symm (F x) := by
    intro x
    apply s.injective
    rw [← hs, Equiv.apply_symm_apply, Equiv.apply_symm_apply]
  have hr' : ∀ x y, r (s.symm x) (s.symm y) = r x y := by
    intro x y
    have h := hr (s.symm x) (s.symm y)
    rw [Equiv.apply_symm_apply, Equiv.apply_symm_apply] at h
    exact h.symm
  refine ⟨isCycle_image F s hs, ?_⟩
  let τ : Cyc F ≃ Cyc F :=
    { toFun := fun C => ⟨s '' C.1, isCycle_image F s hs C⟩
      invFun := fun C => ⟨s.symm '' C.1, isCycle_image F s.symm hs' C⟩
      left_inv := fun C => Subtype.ext (Equiv.symm_image_image s C.1)
      right_inv := fun C => Subtype.ext (Equiv.image_symm_image s C.1) }
  have hVτ : ∀ a b : Cyc F, Vc F r (τ a) (τ b) = Vc F r a b := by
    intro a b
    apply le_antisymm (R_image_le r s hr (a.nonempty F) (b.nonempty F))
    have h := R_image_le r s.symm hr' ((a.nonempty F).image s) ((b.nonempty F).image s)
    rw [Equiv.symm_image_image, Equiv.symm_image_image] at h
    exact h
  intro C C' D D' hD hD'
  have hDτ : D = τ C := Subtype.ext hD
  have hDτ' : D' = τ C' := Subtype.ext hD'
  subst hDτ hDτ'
  have hg := gamma_conj (Vc F r) τ hVτ C
  refine ⟨hVτ C C', hg, ?_, ?_⟩
  · show gamma (Vc F r) (τ C) = gammaMin (Vc F r) ↔ gamma (Vc F r) C = gammaMin (Vc F r)
    rw [hg]
  · show Vc F r (τ C) (τ C') = 1 ↔ Vc F r C C' = 1
    rw [hVτ]

/-! ### The rotation of the ring -/

theorem globalMap_rot : GlobalMap_rot := by
  intro n _ f x
  funext i
  show f (x (i - 1 - 1)) (x (i - 1)) (x (i + 1 - 1)) = f (x (i - 1 - 1)) (x (i - 1)) (x (i - 1 + 1))
  rw [sub_add_cancel, add_sub_cancel_right]

theorem hammingDist_rot (n : ℕ) [NeZero n] (x y : State n) :
    hammingDist (rot n x) (rot n y) = hammingDist x y := by
  unfold hammingDist
  let ε : ZMod n ≃ ZMod n :=
    ⟨fun i => i - 1, fun i => i + 1, fun i => sub_add_cancel i 1, fun i => add_sub_cancel_right i 1⟩
  refine Finset.card_equiv ε ?_
  intro i
  simp only [Finset.mem_filter, Finset.mem_univ, true_and]
  exact Iff.rfl

theorem resistance_rot : Resistance_rot := by
  intro n _ f x y
  unfold resistance
  rw [globalMap_rot, hammingDist_rot]

/-- The rotation as a bijection of the states. -/
def rotEquiv (n : ℕ) : State n ≃ State n :=
  ⟨rot n, fun x i => x (i + 1),
    fun x => by funext i; show x (i + 1 - 1) = x i; rw [add_sub_cancel_right],
    fun x => by funext i; show x (i - 1 + 1) = x i; rw [sub_add_cancel]⟩

theorem lemma_2_4 : Lemma_2_4 := by
  intro n _ f
  exact lemma_2_4_general.{0} (State n) (globalMap n f) (resistance n f) (rotEquiv n)
    (globalMap_rot n f) (resistance_rot n f)

end RingSize.TheoremA

end
