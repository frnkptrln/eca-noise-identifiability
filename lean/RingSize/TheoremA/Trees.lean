module

public import RingSize.TheoremA.Statement
import Mathlib.Data.Set.Card
import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Nat.Find
import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Tactic.Ring

/-!
# In-trees on a finite weighted graph: re-rooting, closed classes, Theorem A

Proofs for Part 1 of `Statement.lean`. The only hypothesis on the weight is `1 ≤ V a b` for `a ≠ b`
(paper, Lemma 2.3, first sentence).
-/

public section

namespace RingSize.TheoremA

open Function

universe u

variable {ι : Type u} [Fintype ι] [DecidableEq ι] (V : ι → ι → ℕ)

/-! ### In-trees: no circuit iff every node reaches the root -/

omit [DecidableEq ι] in
/-- The definition of `IsInTree` ("no directed circuit") is equivalent to: every node reaches the root
along the parent map. -/
theorem isInTree_iff_reaches {c : ι} {p : ι → ι} :
    IsInTree c p ↔ ∀ d, ∃ k, p^[k] d = c := by
  constructor
  · intro h d
    by_contra hcon
    have hne : ∀ k, p^[k] d ≠ c := fun k hk => hcon ⟨k, hk⟩
    have key : ∀ i j : ℕ, i < j → p^[i] d = p^[j] d → False := by
      intro i j hlt heq
      have hk : 0 < j - i := Nat.sub_pos_of_lt hlt
      have hper : p^[j - i] (p^[i] d) = p^[i] d := by
        rw [← Function.iterate_add_apply, Nat.sub_add_cancel hlt.le]
        exact heq.symm
      refine h (p^[i] d) (j - i) hk ?_ hper
      intro l _
      rw [← Function.iterate_add_apply]
      exact hne (l + i)
    obtain ⟨i, j, hij, heq⟩ := Finite.exists_ne_map_eq_of_infinite (fun k : ℕ => p^[k] d)
    have heq' : p^[i] d = p^[j] d := heq
    rcases Nat.lt_or_gt_of_ne hij with hlt | hgt
    · exact key i j hlt heq'
    · exact key j i hgt heq'.symm
  · intro h d k hk hav hper
    obtain ⟨t, ht⟩ := h d
    have hpp : IsPeriodicPt p k d := hper
    have hmod := hpp.iterate_mod_apply t
    exact hav (t % k) (Nat.mod_lt _ hk) (hmod.trans ht)

omit [DecidableEq ι] in
/-- The star with centre `c` is an in-tree rooted at `c`. -/
theorem isInTree_const (c : ι) : IsInTree c (fun _ => c) := by
  rw [isInTree_iff_reaches]
  intro d
  exact ⟨1, rfl⟩

theorem gamma_le {c : ι} {p : ι → ι} (h : IsInTree c p) : gamma V c ≤ treeWeight V c p :=
  Nat.sInf_le ⟨p, h, rfl⟩

theorem exists_tree_gamma (c : ι) : ∃ p, IsInTree c p ∧ treeWeight V c p = gamma V c :=
  Nat.sInf_mem (⟨_, _, isInTree_const c, rfl⟩ :
    {w | ∃ p, IsInTree c p ∧ treeWeight V c p = w}.Nonempty)

theorem gammaMin_le (c : ι) : gammaMin V ≤ gamma V c :=
  Nat.sInf_le ⟨c, rfl⟩

theorem exists_gammaMin [Nonempty ι] : ∃ c, gamma V c = gammaMin V :=
  Nat.sInf_mem (Set.range_nonempty _)

omit [Fintype ι] [DecidableEq ι] in
/-- In an in-tree the edges join distinct nodes. -/
theorem parent_ne {c d : ι} {p : ι → ι} (h : IsInTree c p) (hd : d ≠ c) : p d ≠ d := by
  have h1 := h d 1 Nat.one_pos (by
    intro j hj
    have hj0 : j = 0 := by omega
    subst hj0
    simpa using hd)
  simpa using h1

/-! ### Re-rooting (Lemma 2.5) -/

theorem reroot_isInTree {B : ι} (N : ι) {p : ι → ι} (hT : IsInTree B p) :
    IsInTree N (update p B N) := by
  classical
  rw [isInTree_iff_reaches] at hT ⊢
  intro d
  obtain ⟨k, hk, hmin⟩ : ∃ k, p^[k] d = B ∧ ∀ j < k, p^[j] d ≠ B :=
    ⟨Nat.find (hT d), Nat.find_spec (hT d), fun j hj => Nat.find_min (hT d) hj⟩
  have hsame : ∀ j, j ≤ k → (update p B N)^[j] d = p^[j] d := by
    intro j
    induction j with
    | zero => intro _; rfl
    | succ j ih =>
      intro hj
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih (by omega),
        Function.update_of_ne (hmin j (by omega))]
  refine ⟨k + 1, ?_⟩
  rw [Function.iterate_succ_apply', hsame k le_rfl, hk, Function.update_self]

theorem reroot_weight {B N : ι} (p : ι → ι) (hN : N ≠ B) :
    treeWeight V N (update p B N) + V N (p N) = treeWeight V B p + V B N := by
  unfold treeWeight
  have hB : B ∈ Finset.univ.erase N := Finset.mem_erase.mpr ⟨hN.symm, Finset.mem_univ _⟩
  have hN' : N ∈ Finset.univ.erase B := Finset.mem_erase.mpr ⟨hN, Finset.mem_univ _⟩
  rw [← Finset.add_sum_erase _ _ hB, ← Finset.add_sum_erase _ _ hN']
  have hsum : ∑ d ∈ (Finset.univ.erase N).erase B, V d (update p B N d)
      = ∑ d ∈ (Finset.univ.erase B).erase N, V d (p d) := by
    rw [Finset.erase_right_comm]
    refine Finset.sum_congr rfl ?_
    intro d hd
    have hdB : d ≠ B := (Finset.mem_erase.mp (Finset.mem_of_mem_erase hd)).1
    rw [Function.update_of_ne hdB]
  rw [hsum, Function.update_self]
  omega

theorem reroot_le (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {B N : ι} {p : ι → ι} (hT : IsInTree B p)
    (hN : N ≠ B) (h1 : V B N = 1) :
    treeWeight V N (update p B N) ≤ treeWeight V B p := by
  have hw := reroot_weight V p hN
  have h2 := hV N (p N) (parent_ne hT hN).symm
  omega

/-! ### Closure (Lemma 2.6) -/

theorem closure (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {C C' : ι} (hC : C ∈ Sel V) (h1 : V C C' = 1) :
    C' ∈ Sel V := by
  by_cases hCC : C' = C
  · rw [hCC]; exact hC
  · obtain ⟨p, hT, hw⟩ := exists_tree_gamma V C
    have h2 := gamma_le V (reroot_isInTree C' hT)
    have h3 := reroot_le V hV hT hCC h1
    have h4 := gammaMin_le V C'
    have h5 : gamma V C = gammaMin V := hC
    show gamma V C' = gammaMin V
    omega

omit [Fintype ι] [DecidableEq ι] in
variable {V} in
theorem reach_refl (a : ι) : Reach V a a := Relation.ReflTransGen.refl

omit [Fintype ι] [DecidableEq ι] in
variable {V} in
theorem reach_trans {a b c : ι} (h1 : Reach V a b) (h2 : Reach V b c) : Reach V a c :=
  Relation.ReflTransGen.trans h1 h2

omit [Fintype ι] [DecidableEq ι] in
variable {V} in
theorem reach_tail {a b c : ι} (h1 : Reach V a b) (h2 : G1 V b c) : Reach V a c :=
  Relation.ReflTransGen.tail h1 h2

theorem closure_reach (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {C C' : ι} (hC : C ∈ Sel V)
    (h : Reach V C C') : C' ∈ Sel V := by
  unfold Reach at h
  induction h with
  | refl => exact hC
  | tail _ hbc ih => exact closure V hV ih hbc

/-! ### Closed classes exist and are reachable (paper, 2.4) -/

omit [DecidableEq ι] in
theorem exists_closedClass_reach (a : ι) : ∃ K, IsClosedClass V K ∧ ∃ b ∈ K, Reach V a b := by
  classical
  have hS : {k : ℕ | ∃ b, Reach V a b ∧ ({c | Reach V b c} : Set ι).ncard = k}.Nonempty :=
    ⟨_, a, reach_refl a, rfl⟩
  obtain ⟨b, hab, hcard⟩ := Nat.sInf_mem hS
  have hmin : ∀ c, Reach V a c →
      ({d | Reach V b d} : Set ι).ncard ≤ ({d | Reach V c d} : Set ι).ncard := by
    intro c hc
    exact hcard.le.trans (Nat.sInf_le ⟨c, hc, rfl⟩)
  have hback : ∀ c, Reach V b c → Reach V c b := by
    intro c hc
    have hsub : ({d | Reach V c d} : Set ι) ⊆ {d | Reach V b d} := fun d hd => reach_trans hc hd
    have heq : ({d | Reach V c d} : Set ι) = {d | Reach V b d} :=
      Set.eq_of_subset_of_ncard_le hsub (hmin c (reach_trans hab hc)) (Set.toFinite _)
    have hb : b ∈ ({d | Reach V c d} : Set ι) := by rw [heq]; exact reach_refl b
    exact hb
  refine ⟨{c | Reach V b c}, ⟨⟨b, reach_refl b⟩, ?_, ?_⟩, b, reach_refl b, hab⟩
  · intro c hc d hd
    exact reach_trans (hback c hc) hd
  · intro c hc d hcd
    exact reach_tail hc hcd

/-! ### Every selected node lies in a closed class (Lemma 2.7) -/

/-- Re-rooting along a path of `G_1` from `a` to `D`. If the out-edge of `D` weighs at least 2, the tree
rooted at `D` at the end is lighter by at least 1. The path is cut at its first visit to `D`. -/
theorem reroot_path_strict (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {D a : ι} (h : Reach V a D) :
    ∀ p, IsInTree a p → D ≠ a → 2 ≤ V D (p D) →
      ∃ p', IsInTree D p' ∧ treeWeight V D p' + 1 ≤ treeWeight V a p := by
  unfold Reach at h
  induction h using Relation.ReflTransGen.head_induction_on with
  | refl => intro p _ hne _; exact absurd rfl hne
  | @head a c hac _ ih =>
    intro p hT hDa h2
    by_cases hcD : c = D
    · have hac' : V a D = 1 := by rw [← hcD]; exact hac
      refine ⟨update p a D, reroot_isInTree D hT, ?_⟩
      have hw := reroot_weight V p hDa
      omega
    · by_cases hca : c = a
      · rw [hca] at ih
        exact ih p hT hDa h2
      · have hT1 : IsInTree c (update p a c) := reroot_isInTree c hT
        have hw1 : treeWeight V c (update p a c) ≤ treeWeight V a p := reroot_le V hV hT hca hac
        have hpD : update p a c D = p D := Function.update_of_ne hDa c p
        obtain ⟨p', hT', hw'⟩ := ih (update p a c) hT1 (fun h => hcD h.symm) (by rw [hpD]; exact h2)
        exact ⟨p', hT', by omega⟩

theorem inclosed (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {C : ι} (hC : C ∈ Sel V) :
    ∃ K, IsClosedClass V K ∧ C ∈ K := by
  classical
  obtain ⟨K, hK, E, hEK, hCE⟩ := exists_closedClass_reach V C
  refine ⟨K, hK, ?_⟩
  by_contra hCK
  obtain ⟨p, hT, hw⟩ := exists_tree_gamma V C
  obtain ⟨k, hk⟩ := (isInTree_iff_reaches.mp hT) E
  have hex : ∃ j, p^[j] E ∉ K := ⟨k, by rw [hk]; exact hCK⟩
  obtain ⟨j0, hj0, hjmin⟩ : ∃ j0, p^[j0] E ∉ K ∧ ∀ j < j0, ¬ (p^[j] E ∉ K) :=
    ⟨Nat.find hex, Nat.find_spec hex, fun j hj => Nat.find_min hex hj⟩
  have hj0pos : j0 ≠ 0 := by
    intro h0
    rw [h0] at hj0
    exact hj0 hEK
  obtain ⟨j1, hj1⟩ := Nat.exists_eq_succ_of_ne_zero hj0pos
  have hDK : p^[j1] E ∈ K := by
    by_contra hn
    exact hjmin j1 (by omega) hn
  have hpD : p (p^[j1] E) ∉ K := by
    rw [← Function.iterate_succ_apply' p j1 E]
    rw [hj1] at hj0
    exact hj0
  generalize p^[j1] E = D at hDK hpD
  have hDC : D ≠ C := by
    intro h; rw [h] at hDK; exact hCK hDK
  have hne : D ≠ p D := by
    intro h; rw [← h] at hpD; exact hpD hDK
  have h1 := hV D (p D) hne
  have h2 : V D (p D) ≠ 1 := fun h => hpD (hK.2.2 D hDK (p D) h)
  have hCD : Reach V C D := reach_trans hCE (hK.2.1 E hEK D hDK)
  obtain ⟨p', hT', hw'⟩ := reroot_path_strict V hV hCD p hT hDC (by omega)
  have h3 := gamma_le V hT'
  have h4 := gammaMin_le V D
  have h5 : gamma V C = gammaMin V := hC
  omega

/-! ### Theorem A for a weighted graph -/

/-- Every in-tree has weight at least `m - 1`. -/
theorem card_sub_one_le_treeWeight (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {c : ι} {p : ι → ι}
    (hT : IsInTree c p) : Fintype.card ι - 1 ≤ treeWeight V c p := by
  unfold treeWeight
  have hcard : (Finset.univ.erase c).card = Fintype.card ι - 1 := by
    rw [Finset.card_erase_of_mem (Finset.mem_univ c), Finset.card_univ]
  rw [← hcard, Finset.card_eq_sum_ones]
  refine Finset.sum_le_sum ?_
  intro d hd
  exact hV d (p d) (parent_ne hT (Finset.mem_erase.mp hd).1).symm

/-- The nodes from which `c` is reached in at most `k` steps of `G_1`. -/
def lev (c : ι) : ℕ → Set ι
  | 0 => {c}
  | k + 1 => lev c k ∪ {d | ∃ e ∈ lev c k, G1 V d e}

omit [Fintype ι] [DecidableEq ι] in
theorem exists_lev_of_reach {c d : ι} (h : Reach V d c) : ∃ k, d ∈ lev V c k := by
  unfold Reach at h
  induction h using Relation.ReflTransGen.head_induction_on with
  | refl => exact ⟨0, by simp [lev]⟩
  | @head d e hde _ ih =>
    obtain ⟨k, hk⟩ := ih
    exact ⟨k + 1, by simp only [lev]; exact Or.inr ⟨e, hk, hde⟩⟩

/-- If every node reaches `c` in `G_1`, there is an in-tree rooted at `c` all of whose edges are edges of
`G_1` (a breadth-first tree). -/
theorem exists_G1_tree (c : ι) (hreach : ∀ d, Reach V d c) :
    ∃ p, IsInTree c p ∧ ∀ d, d ≠ c → V d (p d) = 1 := by
  classical
  have : Nonempty ι := ⟨c⟩
  have hlev : ∀ d, ∃ k, d ∈ lev V c k := fun d => exists_lev_of_reach V (hreach d)
  have hstep : ∀ d, d ≠ c → ∃ e, G1 V d e ∧ Nat.find (hlev e) < Nat.find (hlev d) := by
    intro d hd
    have hspec : d ∈ lev V c (Nat.find (hlev d)) := Nat.find_spec (hlev d)
    have hpos : Nat.find (hlev d) ≠ 0 := by
      intro h0
      rw [h0] at hspec
      exact hd (by simpa [lev] using hspec)
    obtain ⟨k, hk⟩ := Nat.exists_eq_succ_of_ne_zero hpos
    have hnot : d ∉ lev V c k := Nat.find_min (hlev d) (by omega)
    rw [hk] at hspec
    simp only [lev] at hspec
    rcases hspec with h | ⟨e, he, hde⟩
    · exact absurd h hnot
    · refine ⟨e, hde, ?_⟩
      have hle : Nat.find (hlev e) ≤ k := Nat.find_min' (hlev e) he
      omega
  choose! nxt hnxt using hstep
  refine ⟨nxt, ?_, fun d hd => (hnxt d hd).1⟩
  rw [isInTree_iff_reaches]
  have main : ∀ m d, Nat.find (hlev d) = m → ∃ j, nxt^[j] d = c := by
    intro m
    induction m using Nat.strong_induction_on with
    | _ m ih =>
      intro d hL
      by_cases hd : d = c
      · exact ⟨0, hd⟩
      · obtain ⟨j, hj⟩ := ih (Nat.find (hlev (nxt d))) (by rw [← hL]; exact (hnxt d hd).2) (nxt d) rfl
        exact ⟨j + 1, by rw [Function.iterate_succ_apply]; exact hj⟩
  exact fun d => main _ d rfl

/-- Theorem 2.8, first sentence, for a weighted graph. -/
theorem theoremA_union (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {C : ι} (hC : C ∈ Sel V) :
    ∃ K, IsClosedClass V K ∧ C ∈ K ∧ K ⊆ Sel V := by
  obtain ⟨K, hK, hCK⟩ := inclosed V hV hC
  exact ⟨K, hK, hCK, fun D hD => closure_reach V hV hC (hK.2.1 C hCK D hD)⟩

/-- Theorem 2.8, second sentence, for a weighted graph. -/
theorem theoremA_unique (hV : ∀ a b, a ≠ b → 1 ≤ V a b) {K : Set ι} (hK : IsClosedClass V K)
    (huniq : ∀ K', IsClosedClass V K' → K' = K) :
    Sel V = K ∧ gammaMin V = Fintype.card ι - 1 := by
  obtain ⟨c, hcK⟩ := hK.1
  have : Nonempty ι := ⟨c⟩
  obtain ⟨c0, hc0⟩ := exists_gammaMin V
  have hc0S : c0 ∈ Sel V := hc0
  obtain ⟨K0, hK0, _, hK0S⟩ := theoremA_union V hV hc0S
  have hK0eq := huniq K0 hK0
  have hSel : Sel V = K := by
    apply Set.Subset.antisymm
    · intro C hC
      obtain ⟨K', hK', hCK'⟩ := inclosed V hV hC
      rw [← huniq K' hK']; exact hCK'
    · rw [← hK0eq]; exact hK0S
  refine ⟨hSel, le_antisymm ?_ ?_⟩
  · have hreach : ∀ d, Reach V d c := by
      intro d
      obtain ⟨K', hK', b, hbK', hdb⟩ := exists_closedClass_reach V d
      rw [huniq K' hK'] at hbK'
      exact reach_trans hdb (hK.2.1 b hbK' c hcK)
    obtain ⟨p, hT, hp⟩ := exists_G1_tree V c hreach
    have hw : treeWeight V c p = Fintype.card ι - 1 := by
      unfold treeWeight
      rw [Finset.sum_congr rfl (fun d hd => hp d (Finset.mem_erase.mp hd).1), Finset.sum_const,
        smul_eq_mul, mul_one, Finset.card_erase_of_mem (Finset.mem_univ c), Finset.card_univ]
    calc gammaMin V ≤ gamma V c := gammaMin_le V c
      _ ≤ treeWeight V c p := gamma_le V hT
      _ = Fintype.card ι - 1 := hw
  · obtain ⟨p, hT, hw⟩ := exists_tree_gamma V c0
    rw [← hc0, ← hw]
    exact card_sub_one_le_treeWeight V hV hT

end RingSize.TheoremA

end
