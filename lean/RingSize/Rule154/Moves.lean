module

public import RingSize.Rule154.Periodic
import Mathlib.Algebra.CharP.Two
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic.Ring

/-!
# Rule 154: one-flip moves between cycles (paper, Lemma 3.8 and the proofs of Theorems 3.9 and 3.10)

The cycle of the constant state `1` is used as a hub: from a set of periodic states that is closed under
setting a zero to one, every cycle reaches the hub and is reached from it by edges of `G_1`.
-/

@[expose] public section

namespace RingSize.Rule154

open Function RingSize.TheoremA

/-- The constant state `1`. -/
def one (n : ℕ) : State n := fun _ => 1

/-- The state with ones exactly on the even cells (the paper's `1_E`). -/
def evens (n : ℕ) : State n := fun i => if par n i = 0 then 1 else 0

theorem evens_of_even (n : ℕ) {i : ZMod n} (h : par n i = 0) : evens n i = 1 := by
  unfold evens
  simp [h]

theorem evens_of_odd (n : ℕ) {i : ZMod n} (h : par n i = 1) : evens n i = 0 := by
  unfold evens
  simp [h]

theorem flip_apply_self (n : ℕ) (x : State n) (j : ZMod n) : TheoremA.flip n x j j = x j + 1 := by
  show x j + e n j j = x j + 1
  rw [e_apply_self]

theorem flip_apply_ne (n : ℕ) (x : State n) {i j : ZMod n} (h : i ≠ j) :
    TheoremA.flip n x j i = x i := by
  show x i + e n j i = x i
  rw [e_apply_ne n h, add_zero]

theorem F154_one (n : ℕ) [NeZero n] : F154 n (one n) = one n := by
  funext i
  rw [F154_apply]
  show (1 : ZMod 2) + 1 * (1 + 1) = 1
  decide

theorem par_zero (n : ℕ) : par n 0 = 0 := by
  unfold par
  rw [ZMod.val_zero]
  exact Nat.cast_zero

theorem par_zero_add_one (n : ℕ) [NeZero n] (hn : Even n) : par n (0 + 1) = 1 := by
  rw [par_add_one n hn, par_zero, zero_add]

theorem not_Z_of (n : ℕ) {x : State n} {c : ZMod 2} (i : ZMod n) (hi : par n i = c) (hx : x i ≠ 0) :
    ¬ Z n c x := fun h => hx (h i hi)

theorem mem_parM_of (n : ℕ) {x : State n} (c : ZMod 2) (h1 : ¬ Z n c x) (h2 : ¬ Z n (c + 1) x) :
    x ∈ parM n := by
  rw [mem_parM]
  rcases zmod2_cases c with rfl | rfl
  · rw [zero_add] at h2
    exact ⟨h2, h1⟩
  · have e : (1 : ZMod 2) + 1 = 0 := CharTwo.add_self_eq_zero 1
    rw [e] at h2
    exact ⟨h1, h2⟩

theorem one_mem_parM (n : ℕ) [NeZero n] (hn : Even n) : one n ∈ parM n :=
  mem_parM_of n 0 (not_Z_of n 0 (par_zero n) one_ne_zero)
    (by rw [zero_add]; exact not_Z_of n (0 + 1) (par_zero_add_one n hn) one_ne_zero)

/-- Setting a zero of a state of `M` to one gives a state of `M`. -/
theorem flip_mem_parM (n : ℕ) {x : State n} (hx : x ∈ parM n) (j : ZMod n) (hxj : x j = 0) :
    TheoremA.flip n x j ∈ parM n := by
  rw [mem_parM] at hx ⊢
  have key : ∀ c, Z n c (TheoremA.flip n x j) → Z n c x := by
    intro c hZ i hi
    by_cases hij : i = j
    · rw [hij]
      exact hxj
    · have h := hZ i hi
      rwa [flip_apply_ne n x hij] at h
  exact ⟨fun h => hx.1 (key 1 h), fun h => hx.2 (key 0 h)⟩

/-- Paper, Lemma 2.3 (last sentence), as reachability: if `x` lies on `C` and its flip on `C'`, then `C` and
`C'` are equal or joined by edges of `G_1` in both directions. -/
theorem flip_reach (n : ℕ) [NeZero n] {C C' : Cyc (F154 n)} {x : State n} (hx : x ∈ C.1) (j : ZMod n)
    (hy : TheoremA.flip n x j ∈ C'.1) : Reach (V154 n) C C' ∧ Reach (V154 n) C' C := by
  by_cases h : C = C'
  · subst h
    exact ⟨reach_refl _, reach_refl _⟩
  · obtain ⟨h1, h2⟩ := (lemma_2_3 n (ruleOfNumber 154) C C' h).2.2 x hx j hy
    exact ⟨Relation.ReflTransGen.single h1, Relation.ReflTransGen.single h2⟩

/-- The hub lemma: if all states of `S` are periodic and `S` is closed under setting a zero to one, then the
cycle of every state of `S` reaches the cycle of the constant state `1` and is reached from it. -/
theorem hub (n : ℕ) [NeZero n] (S : Set (State n)) (hper : ∀ x ∈ S, x ∈ periodicPts (F154 n))
    (hup : ∀ x ∈ S, ∀ j, x j = 0 → TheoremA.flip n x j ∈ S)
    (C1 : Cyc (F154 n)) (h1 : one n ∈ C1.1) :
    ∀ (k : ℕ) (x : State n), x ∈ S → (Finset.univ.filter fun i => x i = 0).card = k →
      ∀ C : Cyc (F154 n), x ∈ C.1 → Reach (V154 n) C C1 ∧ Reach (V154 n) C1 C := by
  intro k
  induction k with
  | zero =>
    intro x _ hk C hxC
    have hx1 : x = one n := by
      funext i
      have hmem : i ∉ Finset.univ.filter fun i => x i = 0 := by
        rw [Finset.card_eq_zero.mp hk]
        exact Finset.notMem_empty i
      have hne : x i ≠ 0 := fun h => hmem (Finset.mem_filter.mpr ⟨Finset.mem_univ i, h⟩)
      exact bit_eq_one_of_ne_zero _ hne
    rw [hx1] at hxC
    have hC : C = C1 := Cyc.eq_of_mem (F154 n) hxC h1
    rw [hC]
    exact ⟨reach_refl _, reach_refl _⟩
  | succ k ih =>
    intro x hxS hk C hxC
    have hpos : 0 < (Finset.univ.filter fun i => x i = 0).card := by
      rw [hk]
      exact Nat.succ_pos k
    obtain ⟨j, hj⟩ := Finset.card_pos.mp hpos
    have hxj : x j = 0 := (Finset.mem_filter.mp hj).2
    have hyS : TheoremA.flip n x j ∈ S := hup x hxS j hxj
    have hset : (Finset.univ.filter fun i => TheoremA.flip n x j i = 0) =
        (Finset.univ.filter fun i => x i = 0).erase j := by
      ext i
      simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_erase]
      by_cases hij : i = j
      · rw [hij, flip_apply_self, hxj, zero_add]
        simp
      · rw [flip_apply_ne n x hij]
        simp [hij]
    have hcard : (Finset.univ.filter fun i => TheoremA.flip n x j i = 0).card = k := by
      rw [hset, Finset.card_erase_of_mem hj, hk, Nat.add_sub_cancel]
    have hyC : TheoremA.flip n x j ∈ (cycleOf (F154 n) _ (hper _ hyS)).1 := mem_cycleOf (F154 n) _ _
    obtain ⟨a1, a2⟩ := flip_reach n hxC j hyC
    obtain ⟨b1, b2⟩ := ih _ hyS hcard _ hyC
    exact ⟨reach_trans a1 b1, reach_trans b2 a2⟩

/-- Paper, Lemma 3.8(b), through the hub: for even `n` the cycle of every state of `M` reaches the cycle of
`1` and is reached from it. -/
theorem hub_parM (n : ℕ) [NeZero n] (hn : Even n) (C1 : Cyc (F154 n)) (h1 : one n ∈ C1.1)
    {x : State n} (hx : x ∈ parM n) (C : Cyc (F154 n)) (hxC : x ∈ C.1) :
    Reach (V154 n) C C1 ∧ Reach (V154 n) C1 C :=
  hub n (parM n) (fun _ h => periodic_of_mem_parM n hn h) (fun _ h j hj => flip_mem_parM n h j hj)
    C1 h1 _ x hx rfl C hxC

/-- For odd `n` every cycle reaches the cycle of `1` and is reached from it. -/
theorem hub_odd (n : ℕ) [NeZero n] (hn : ¬ Even n) (C1 : Cyc (F154 n)) (h1 : one n ∈ C1.1)
    (C : Cyc (F154 n)) : Reach (V154 n) C C1 ∧ Reach (V154 n) C1 C := by
  obtain ⟨x, hxC⟩ := C.nonempty (F154 n)
  exact hub n Set.univ (fun y _ => periodic_of_odd n hn y) (fun _ _ _ _ => Set.mem_univ _)
    C1 h1 _ x (Set.mem_univ x) rfl C hxC

/-- For even `n`: a cycle with a state outside `M` other than `0` reaches the hub and is reached from it
(paper, proof of Theorem 3.10, step (2)). -/
theorem hub_not_parM (n : ℕ) [NeZero n] (hn : Even n) (C1 : Cyc (F154 n)) (h1 : one n ∈ C1.1)
    {x : State n} (hx : x ∉ parM n) (hx0 : x ≠ 0) (C : Cyc (F154 n)) (hxC : x ∈ C.1) :
    Reach (V154 n) C C1 ∧ Reach (V154 n) C1 C := by
  have hZ : ∃ c, Z n c x := by
    rw [mem_parM, not_and_or, not_not, not_not] at hx
    rcases hx with h | h
    · exact ⟨1, h⟩
    · exact ⟨0, h⟩
  obtain ⟨c, hc⟩ := hZ
  obtain ⟨i, hi⟩ := Function.ne_iff.mp hx0
  have hi' : x i ≠ 0 := hi
  have hpi : par n i = c + 1 := zmod2_eq_add_one c (par n i) (fun h => hi' (hc i h.symm))
  have hpj : par n (i + 1) = c := by
    rw [par_add_one n hn, hpi, add_assoc, CharTwo.add_self_eq_zero, add_zero]
  have hxj : x (i + 1) = 0 := hc _ hpj
  have hij : i ≠ i + 1 := by
    intro h
    have h2 : par n i = par n (i + 1) := congrArg (par n) h
    rw [hpi, hpj] at h2
    exact zmod2_ne_add_one c h2.symm
  have hyM : TheoremA.flip n x (i + 1) ∈ parM n := by
    refine mem_parM_of n c (not_Z_of n (i + 1) hpj ?_) (not_Z_of n i hpi ?_)
    · rw [flip_apply_self, hxj, zero_add]
      exact one_ne_zero
    · rw [flip_apply_ne n x hij]
      exact hi'
  have hyC : TheoremA.flip n x (i + 1) ∈ (cycleOf (F154 n) _ (periodic_of_mem_parM n hn hyM)).1 :=
    mem_cycleOf (F154 n) _ _
  obtain ⟨a1, a2⟩ := flip_reach n hxC (i + 1) hyC
  obtain ⟨b1, b2⟩ := hub_parM n hn C1 h1 hyM _ hyC
  exact ⟨reach_trans a1 b1, reach_trans b2 a2⟩

theorem F154_evens (n : ℕ) [NeZero n] (hn : Even n) : F154 n (evens n) = 0 := by
  have hZ : ∀ i, par n i = 1 → evens n i = 0 := fun i hi => evens_of_odd n hi
  obtain ⟨hF, -⟩ := step_aux n hn 1 hZ
  rw [hF]
  funext i
  show evens n (i - 1) + evens n (i + 1) = 0
  have h : evens n (i - 1) = evens n (i + 1) := by
    unfold evens
    rw [par_sub_one n hn, par_add_one n hn]
  rw [h]
  exact CharTwo.add_self_eq_zero _

/-- For even `n` there is a state of `M` whose cycle has an edge of `G_1` to `{0}` (paper, proof of
Theorem 3.10, step (3): `y = 1_E + e_1`). -/
theorem exists_edge_to_zero (n : ℕ) [NeZero n] (hn : Even n) (C0 : Cyc (F154 n)) (hC0 : C0.1 = {0}) :
    ∃ y, y ∈ parM n ∧ ∀ Cy : Cyc (F154 n), y ∈ Cy.1 → Reach (V154 n) Cy C0 := by
  have hp1 := par_zero_add_one n hn
  have h01 : (0 : ZMod n) ≠ 0 + 1 := by
    intro h
    have h2 : par n 0 = par n (0 + 1) := congrArg (par n) h
    rw [par_zero, hp1] at h2
    exact zero_ne_one h2
  have hy1 : TheoremA.flip n (evens n) (0 + 1) (0 + 1) = 1 := by
    rw [flip_apply_self, evens_of_odd n hp1, zero_add]
  have hy0 : TheoremA.flip n (evens n) (0 + 1) 0 = 1 := by
    rw [flip_apply_ne n _ h01, evens_of_even n (par_zero n)]
  refine ⟨TheoremA.flip n (evens n) (0 + 1), ?_, ?_⟩
  · refine mem_parM_of n 0 (not_Z_of n 0 (par_zero n) ?_) (not_Z_of n (0 + 1) ?_ ?_)
    · rw [hy0]
      exact one_ne_zero
    · exact hp1.trans (zero_add 1).symm
    · rw [hy1]
      exact one_ne_zero
  · intro Cy hyC
    have hne : Cy ≠ C0 := by
      intro h
      rw [h, hC0] at hyC
      have h0 : TheoremA.flip n (evens n) (0 + 1) = 0 := Set.mem_singleton_iff.mp hyC
      have h1 := congrFun h0 0
      rw [hy0] at h1
      exact one_ne_zero h1
    have hG : V154 n Cy C0 = 1 := by
      refine (VE_eq_one_iff hne).mpr ⟨_, hyC, 0 + 1, 1, ?_⟩
      rw [TheoremA.flip_flip, hC0]
      exact Set.mem_singleton_iff.mpr (F154_evens n hn)
    exact Relation.ReflTransGen.single hG

/-- A node without outgoing edge of `G_1` reaches only itself. -/
theorem reach_eq_of_no_out {ι : Type} (V : ι → ι → ℕ) {a b : ι} (hno : ∀ c, ¬ G1 V a c)
    (h : Reach V a b) : b = a := by
  rcases Relation.ReflTransGen.cases_head h with h1 | ⟨c, hc, -⟩
  · exact h1.symm
  · exact absurd hc (hno c)

end RingSize.Rule154

end
