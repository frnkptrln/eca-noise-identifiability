module

public import RingSize.Rule154.Moves
import Mathlib.Algebra.CharP.Two
import Mathlib.Data.ZMod.Basic
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Tactic.Ring
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.IntervalCases

/-!
# Rule 154: Theorems 3.9, 3.10 and 3.11 of the ring-size paper

Proofs of the statements of `RingSize/Rule154/StatementMain.lean`.
-/

@[expose] public section

namespace RingSize.Rule154

open Function RingSize.TheoremA

/-! ### Weighted graphs -/

/-- The weight `V` with the value at `(z, cs)` replaced by `1`. -/
def patch {ι : Type} [DecidableEq ι] (V : ι → ι → ℕ) (z cs : ι) : ι → ι → ℕ :=
  fun a b => if a = z ∧ b = cs then 1 else V a b

theorem patch_self {ι : Type} [DecidableEq ι] (V : ι → ι → ℕ) (z cs : ι) : patch V z cs z cs = 1 := by
  unfold patch
  simp

theorem patch_of_not {ι : Type} [DecidableEq ι] (V : ι → ι → ℕ) (z cs : ι) {a b : ι}
    (h : ¬ (a = z ∧ b = cs)) : patch V z cs a b = V a b := by
  unfold patch
  simp [h]

theorem G1_patch {ι : Type} [DecidableEq ι] (V : ι → ι → ℕ) (z cs : ι) {a b : ι} (h : G1 V a b) :
    G1 (patch V z cs) a b := by
  by_cases hab : a = z ∧ b = cs
  · rw [hab.1, hab.2]
    exact patch_self V z cs
  · show patch V z cs a b = 1
    rw [patch_of_not V z cs hab]
    exact h

theorem reach_patch {ι : Type} [DecidableEq ι] (V : ι → ι → ℕ) (z cs : ι) {a b : ι}
    (h : Reach V a b) : Reach (patch V z cs) a b := by
  unfold Reach at h ⊢
  induction h with
  | refl => exact Relation.ReflTransGen.refl
  | tail _ hbc ih => exact Relation.ReflTransGen.tail ih (G1_patch V z cs hbc)

/-- If every node other than `z` reaches `c` in `G_1`, and `V z cs ≤ w + 1` for some `cs ≠ z`, then there is
an in-tree rooted at `c` of weight at most `(m - 1) + w` (paper, proof of Theorem 3.9(e)). -/
theorem gamma_le_card_add {ι : Type} [Fintype ι] [DecidableEq ι] (V : ι → ι → ℕ) (c z cs : ι)
    (hzc : z ≠ c) (hreach : ∀ d, d ≠ z → Reach V d c) (hcs : cs ≠ z) (w : ℕ) (hw : V z cs ≤ w + 1) :
    gamma V c ≤ Fintype.card ι - 1 + w := by
  have hreach' : ∀ d, Reach (patch V z cs) d c := by
    intro d
    by_cases hd : d = z
    · rw [hd]
      exact Relation.ReflTransGen.head (patch_self V z cs) (reach_patch V z cs (hreach cs hcs))
    · exact reach_patch V z cs (hreach d hd)
  obtain ⟨p, hT, hp⟩ := exists_G1_tree (patch V z cs) c hreach'
  refine (gamma_le V hT).trans ?_
  unfold treeWeight
  have hterm : ∀ d ∈ Finset.univ.erase c, V d (p d) ≤ 1 + (if d = z then w else 0) := by
    intro d hd
    have hdc : d ≠ c := (Finset.mem_erase.mp hd).1
    have h1 : patch V z cs d (p d) = 1 := hp d hdc
    by_cases hdz : d = z ∧ p d = cs
    · have e : V d (p d) = V z cs := by rw [hdz.2, hdz.1]
      have hite : (if d = z then w else 0) = w := by simp [hdz.1]
      rw [e, hite]
      omega
    · rw [patch_of_not V z cs hdz] at h1
      rw [h1]
      exact Nat.le_add_right 1 _
  have hz_mem : z ∈ Finset.univ.erase c := Finset.mem_erase.mpr ⟨hzc, Finset.mem_univ z⟩
  refine (Finset.sum_le_sum hterm).trans ?_
  rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_erase_of_mem (Finset.mem_univ c),
    Finset.card_univ, smul_eq_mul, mul_one, Finset.sum_ite_eq']
  simp [hz_mem]

/-- If `G_1` is strongly connected, the set of all nodes is its only closed class. -/
theorem closed_univ_of_connected {ι : Type} [Nonempty ι] (V : ι → ι → ℕ) (h : ∀ a b, Reach V a b) :
    IsClosedClass V Set.univ ∧ ∀ K', IsClosedClass V K' → K' = Set.univ := by
  refine ⟨⟨Set.univ_nonempty, fun a _ b _ => h a b, fun _ _ b _ => Set.mem_univ b⟩, ?_⟩
  rintro K' ⟨⟨a, ha⟩, -, hcl⟩
  ext b
  exact ⟨fun _ => Set.mem_univ b, fun _ => reach_mem_of_closed V hcl ha (h a b)⟩

/-! ### States with two ones, and codes -/

/-- The state with ones exactly at the cells `p` and `q`. -/
def two (n : ℕ) (p q : ZMod n) : State n :=
  fun i => (if i = p then 1 else 0) + (if i = q then 1 else 0)

theorem two_first (n : ℕ) {p q : ZMod n} (h : p ≠ q) : two n p q p = 1 := by
  simp [two, h]

theorem two_second (n : ℕ) {p q : ZMod n} (h : p ≠ q) : two n p q q = 1 := by
  simp [two, h.symm]

theorem two_other (n : ℕ) {p q i : ZMod n} (h1 : i ≠ p) (h2 : i ≠ q) : two n p q i = 0 := by
  simp [two, h1, h2]

theorem two_eq_flip (n : ℕ) (p q : ZMod n) :
    two n p q = TheoremA.flip n (TheoremA.flip n 0 p) q := by
  funext i
  simp [two, TheoremA.flip, e]

theorem cast_ne (n : ℕ) (a b : ℕ) (hab : a < b) (hbn : b - a < n) :
    ((a : ℕ) : ZMod n) ≠ ((b : ℕ) : ZMod n) := by
  intro h
  have h' : ((b - a : ℕ) : ZMod n) = 0 := by
    rw [Nat.cast_sub hab.le, h, sub_self]
  rw [ZMod.natCast_eq_zero_iff] at h'
  have := Nat.le_of_dvd (Nat.sub_pos_of_lt hab) h'
  omega

theorem par_natCast (n : ℕ) [NeZero n] (hn : Even n) (k : ℕ) : par n (k : ZMod n) = (k : ZMod 2) := by
  rw [par_eq_castHom n hn.two_dvd, map_natCast]

theorem contains_at (n : ℕ) (x : State n) (k : ℕ) (a b c : ZMod 2)
    (h1 : x ((k : ℕ) : ZMod n) = a) (h2 : x ((k + 1 : ℕ) : ZMod n) = b)
    (h3 : x ((k + 2 : ℕ) : ZMod n) = c) : Contains n x (a, b, c) := by
  refine ⟨((k + 1 : ℕ) : ZMod n), ?_⟩
  have e1 : ((k + 1 : ℕ) : ZMod n) - 1 = ((k : ℕ) : ZMod n) := by
    push_cast
    ring
  have e2 : ((k + 1 : ℕ) : ZMod n) + 1 = ((k + 2 : ℕ) : ZMod n) := by
    push_cast
    ring
  rw [e1, e2, h1, h2, h3]

/-- For even `n ≥ 4` each of the codes 001, 011, 110, 100, 101 occurs in a state of `M`. -/
theorem codes_in_M (n : ℕ) [NeZero n] (hn : Even n) (hn4 : 4 ≤ n) (v : Code)
    (hv : v = (0, 0, 1) ∨ v = (0, 1, 1) ∨ v = (1, 1, 0) ∨ v = (1, 0, 0) ∨ v = (1, 0, 1)) :
    ∃ x ∈ parM n, Contains n x v := by
  have ne : ∀ a b : ℕ, a < b → b - a < n → ((a : ℕ) : ZMod n) ≠ ((b : ℕ) : ZMod n) := cast_ne n
  have p2 : par n ((2 : ℕ) : ZMod n) = 0 := by rw [par_natCast n hn]; decide
  have p3 : par n ((3 : ℕ) : ZMod n) = 0 + 1 := by rw [par_natCast n hn]; decide
  have p5 : par n ((5 : ℕ) : ZMod n) = 0 + 1 := by rw [par_natCast n hn]; decide
  have h23 := ne 2 3 (by norm_num) (by omega)
  have h24 := ne 2 4 (by norm_num) (by omega)
  have h25 := ne 2 5 (by norm_num) (by omega)
  have h34 := ne 3 4 (by norm_num) (by omega)
  have h35 := ne 3 5 (by norm_num) (by omega)
  have h45 := ne 4 5 (by norm_num) (by omega)
  have h02 := ne 0 2 (by norm_num) (by omega)
  have h03 := ne 0 3 (by norm_num) (by omega)
  have h12 := ne 1 2 (by norm_num) (by omega)
  have h13 := ne 1 3 (by norm_num) (by omega)
  -- the state `A` with ones at the cells 2 and 3
  have A0 : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ((0 : ℕ) : ZMod n) = 0 := two_other n h02 h03
  have A1 : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ((1 : ℕ) : ZMod n) = 0 := two_other n h12 h13
  have A2 : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ((2 : ℕ) : ZMod n) = 1 := two_first n h23
  have A3 : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) = 1 := two_second n h23
  have A4 : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n) = 0 :=
    two_other n h24.symm h34.symm
  have A5 : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ((5 : ℕ) : ZMod n) = 0 :=
    two_other n h25.symm h35.symm
  have AM : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ∈ parM n :=
    mem_parM_of n 0 (not_Z_of n _ p2 (by rw [A2]; exact one_ne_zero))
      (not_Z_of n _ p3 (by rw [A3]; exact one_ne_zero))
  -- the state `B` with ones at the cells 2, 4 and 5
  have B2 : TheoremA.flip n (two n ((2 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n)) ((5 : ℕ) : ZMod n)
      ((2 : ℕ) : ZMod n) = 1 := by
    rw [flip_apply_ne n _ h25, two_first n h24]
  have B3 : TheoremA.flip n (two n ((2 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n)) ((5 : ℕ) : ZMod n)
      ((3 : ℕ) : ZMod n) = 0 := by
    rw [flip_apply_ne n _ h35, two_other n h23.symm h34]
  have B4 : TheoremA.flip n (two n ((2 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n)) ((5 : ℕ) : ZMod n)
      ((4 : ℕ) : ZMod n) = 1 := by
    rw [flip_apply_ne n _ h45, two_second n h24]
  have B5 : TheoremA.flip n (two n ((2 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n)) ((5 : ℕ) : ZMod n)
      ((5 : ℕ) : ZMod n) = 1 := by
    rw [flip_apply_self, two_other n h25.symm h45.symm, zero_add]
  have BM : TheoremA.flip n (two n ((2 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n)) ((5 : ℕ) : ZMod n) ∈ parM n :=
    mem_parM_of n 0 (not_Z_of n _ p2 (by rw [B2]; exact one_ne_zero))
      (not_Z_of n _ p5 (by rw [B5]; exact one_ne_zero))
  rcases hv with rfl | rfl | rfl | rfl | rfl
  · exact ⟨_, AM, contains_at n _ 0 _ _ _ A0 A1 A2⟩
  · exact ⟨_, AM, contains_at n _ 1 _ _ _ A1 A2 A3⟩
  · exact ⟨_, AM, contains_at n _ 2 _ _ _ A2 A3 A4⟩
  · exact ⟨_, AM, contains_at n _ 3 _ _ _ A3 A4 A5⟩
  · exact ⟨_, BM, contains_at n _ 2 _ _ _ B2 B3 B4⟩

/-- For even `n ≥ 5` the code 010 occurs in a state of `M`. -/
theorem code_010_in_M (n : ℕ) [NeZero n] (hn : Even n) (hn5 : 5 ≤ n) :
    ∃ x ∈ parM n, Contains n x (0, 1, 0) := by
  have p4 : par n ((4 : ℕ) : ZMod n) = 0 := by rw [par_natCast n hn]; decide
  have p1 : par n ((1 : ℕ) : ZMod n) = 0 + 1 := by rw [par_natCast n hn]; decide
  have h14 := cast_ne n 1 4 (by norm_num) (by omega)
  have h01 := cast_ne n 0 1 (by norm_num) (by omega)
  have h04 := cast_ne n 0 4 (by norm_num) (by omega)
  have h12 := cast_ne n 1 2 (by norm_num) (by omega)
  have h24 := cast_ne n 2 4 (by norm_num) (by omega)
  have C0' : two n ((1 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n) ((0 : ℕ) : ZMod n) = 0 := two_other n h01 h04
  have C1' : two n ((1 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n) ((1 : ℕ) : ZMod n) = 1 := two_first n h14
  have C2' : two n ((1 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n) ((2 : ℕ) : ZMod n) = 0 :=
    two_other n h12.symm h24
  have C4' : two n ((1 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n) ((4 : ℕ) : ZMod n) = 1 := two_second n h14
  exact ⟨_, mem_parM_of n 0 (not_Z_of n _ p4 (by rw [C4']; exact one_ne_zero))
    (not_Z_of n _ p1 (by rw [C1']; exact one_ne_zero)), contains_at n _ 0 _ _ _ C0' C1' C2'⟩

/-- For `n ≥ 3` the flip of the cell 1 of the zero state contains the code 010. -/
theorem code_010_flip (n : ℕ) (hn3 : 3 ≤ n) :
    Contains n (TheoremA.flip n 0 ((1 : ℕ) : ZMod n)) (0, 1, 0) := by
  have h01 := cast_ne n 0 1 (by norm_num) (by omega)
  have h12 := cast_ne n 1 2 (by norm_num) (by omega)
  refine contains_at n _ 0 _ _ _ ?_ ?_ ?_
  · rw [flip_apply_ne n _ h01]
    rfl
  · rw [flip_apply_self]
    exact zero_add 1
  · rw [flip_apply_ne n _ h12.symm]
    rfl

/-! ### The indices `k_v` -/

/-- If a cycle `C` with `γ(C) ≤ γ_min + 1` has a state that contains `v`, then `k_v ≤ 1`. -/
theorem k_le_one_of_cycle (n : ℕ) [NeZero n] (hn3 : 3 ≤ n) (v : Code) (C : Cyc (F154 n))
    (hg : gamma (V154 n) C ≤ gammaMin (V154 n) + 1) (x : State n) (hx : x ∈ C.1)
    (hc : Contains n x v) : k154 n v ≤ 1 := by
  have hr := resistanceECA n (ruleOfNumber 154)
  have hR : R (resistance n (ruleOfNumber 154)) C.1 (D n v) = 0 :=
    (R_cycle_eq_zero_iff hr C (D_nonempty n hn3 v)).mpr ⟨x, hx, hc⟩
  have h1 : k154 n v ≤ gamma (V154 n) C + R (resistance n (ruleOfNumber 154)) C.1 (D n v)
      - gammaMin (V154 n) := by
    have hmem : gamma (V154 n) C + R (resistance n (ruleOfNumber 154)) C.1 (D n v) ∈
        Set.range fun C : Cyc (globalMap n (ruleOfNumber 154)) =>
          gamma (VE n (ruleOfNumber 154)) C + R (resistance n (ruleOfNumber 154)) C.1 (D n v) :=
      ⟨C, rfl⟩
    show kIndex n (ruleOfNumber 154) v ≤ _
    unfold kIndex
    exact Nat.sub_le_sub_right (Nat.sInf_le hmem) _
  rw [hR, add_zero] at h1
  omega

/-- `V({0}, C) ≤ 2` for the cycle of a state with two ones. -/
theorem V_zero_le_two (n : ℕ) [NeZero n] (C0 CA : Cyc (F154 n)) (h0 : (0 : State n) ∈ C0.1)
    (p q : ZMod n) (hA : two n p q ∈ CA.1) : V154 n C0 CA ≤ 1 + 1 := by
  have hpath := R_le_of_path (resistance n (ruleOfNumber 154)) (A := C0.1) (B := CA.1) [0, two n p q]
    (List.cons_ne_nil _ _) h0 hA
  refine hpath.trans ?_
  show hammingDist (F154 n 0) (two n p q) + 0 ≤ 1 + 1
  rw [F154_zero, add_zero, two_eq_flip]
  refine (hammingDist_triangle _ (TheoremA.flip n 0 p) _).trans ?_
  rw [hammingDist_flip, hammingDist_flip]

/-! ### Lemma 3.4(b) and the lemmas 3.5 to 3.8 -/

theorem lemma_3_4_b_zero : Lemma_3_4_b_zero := by
  intro n _ hn hnp t h
  rw [iterate_aux n hn t (par n 0 + 1) (e n 0) (single_aux n 0)] at h
  exact hnp (pow_two_of_iterate_eq_zero n t h)

theorem lemma_3_5 : Lemma_3_5 := fun n _ hn _ hx => F154_mem_parM n hn hx

theorem mem_union_of_not_mem_parM (n : ℕ) {x : State n} (h : x ∉ parM n) : x ∈ parE n ∪ parO n := by
  by_contra hcon
  exact h hcon

theorem lemma_3_6_in_particular : Lemma_3_6_in_particular := by
  intro n _
  refine ⟨fun x y hF hne => ?_, fun hn => ?_⟩
  · obtain ⟨hx, hy⟩ := collision_not_mem n x y hF hne
    exact ⟨(collision n x y hF hne).1, mem_union_of_not_mem_parM n hx, mem_union_of_not_mem_parM n hy⟩
  · exact Finite.injective_iff_bijective.mp (F154_injective_of_odd n hn)

theorem iterate_mem_parM (n : ℕ) [NeZero n] (hn : Even n) :
    ∀ (t : ℕ) (x : State n), x ∈ parM n → (F154 n)^[t] x ∈ parM n := by
  intro t
  induction t with
  | zero => intro x hx; exact hx
  | succ t ih =>
    intro x hx
    rw [Function.iterate_succ_apply']
    exact F154_mem_parM n hn (ih x hx)

theorem lemma_3_7 : Lemma_3_7 := by
  intro n _ hn
  have hper : ∀ x ∈ parM n, x ∈ periodicPts (F154 n) := fun x hx => periodic_of_mem_parM n hn hx
  refine ⟨⟨fun x hx => F154_mem_parM n hn hx, ?_, ?_⟩, hper⟩
  · intro x hx y _ h
    by_contra hne
    exact (collision_not_mem n x y h hne).1 hx
  · intro y hy
    obtain ⟨p, hp, hpy⟩ := mem_periodicPts.mp (hper y hy)
    refine ⟨(F154 n)^[p - 1] y, iterate_mem_parM n hn (p - 1) y hy, ?_⟩
    have e : p = (p - 1) + 1 := by omega
    have h := hpy
    unfold Function.IsPeriodicPt Function.IsFixedPt at h
    rw [e, Function.iterate_succ_apply'] at h
    exact h

/-- A cycle with a state of `M` is contained in `M` (even `n`). -/
theorem cycle_subset_parM (n : ℕ) [NeZero n] (hn : Even n) (C : Cyc (F154 n)) {y : State n}
    (hy : y ∈ C.1) (hyM : y ∈ parM n) : C.1 ⊆ parM n := by
  intro z hz
  rw [C.eq_orbit (F154 n) hy] at hz
  obtain ⟨t, rfl⟩ := hz
  exact iterate_mem_parM n hn t y hyM

theorem lemma_3_8_a : Lemma_3_8_a := by
  intro n _ hn C x j _ hx hyM
  have hyp := periodic_of_mem_parM n hn hyM
  have hyC := mem_cycleOf (F154 n) _ hyp
  refine ⟨cycleOf (F154 n) _ hyp, hyC, cycle_subset_parM n hn _ hyC hyM, ?_⟩
  by_cases h : cycleOf (F154 n) _ hyp = C
  · exact Or.inl h
  · exact Or.inr ((lemma_2_3 n (ruleOfNumber 154) C _ (Ne.symm h)).2.2 x hx j hyC)

/-- The cycle of the constant state `1`. -/
noncomputable def cycOne (n : ℕ) [NeZero n] : Cyc (F154 n) :=
  Subtype.mk {one n} (isCycle_singleton (F154 n) (F154_one n))

theorem one_mem_cycOne (n : ℕ) [NeZero n] : one n ∈ (cycOne n).1 := Set.mem_singleton _

/-- The cycle `{0}`. -/
noncomputable def cycZero (n : ℕ) [NeZero n] : Cyc (F154 n) :=
  Subtype.mk {0} (zero_cycle n)

theorem lemma_3_8_b : Lemma_3_8_b := by
  intro n _ hn C C' x x' hx hxM hx' hxM'
  exact reach_trans (hub_parM n hn (cycOne n) (one_mem_cycOne n) hxM C hx).1
    (hub_parM n hn (cycOne n) (one_mem_cycOne n) hxM' C' hx').2

/-! ### Theorem 3.9 -/

theorem theorem_3_9 : Theorem_3_9 := by
  intro n _ k hk2 hk C0 hC0
  obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
  have hn : Even n := by
    rw [hk]
    exact Nat.even_pow.mpr ⟨even_two, Nat.succ_ne_zero k'⟩
  have hn4 : 4 ≤ n := by
    rw [hk]
    calc 4 = 2 ^ 2 := by norm_num
      _ ≤ 2 ^ (k' + 1) := Nat.pow_le_pow_right (by norm_num) hk2
  have hn3 : 3 ≤ n := by omega
  have h0 : (0 : State n) ∈ C0.1 := by
    rw [hC0]
    exact Set.mem_singleton _
  have hb := theorem_3_9_b n k' hk C0 hC0
  have h1 := one_mem_cycOne n
  -- (a)
  have hM : ∀ C : Cyc (F154 n), C ≠ C0 → C.1 ⊆ parM n := by
    intro C hne x hx
    by_contra hxM
    have hdie := lemma_3_4_a n k' hk x (mem_union_of_not_mem_parM n hxM)
    have hmem := C.iterate_mem (F154 n) hx (n / 2)
    rw [hdie] at hmem
    exact hne (Cyc.eq_of_mem (F154 n) hmem h0)
  have hhub : ∀ C : Cyc (F154 n), C ≠ C0 →
      Reach (V154 n) C (cycOne n) ∧ Reach (V154 n) (cycOne n) C := by
    intro C hne
    obtain ⟨x, hx⟩ := C.nonempty (F154 n)
    exact hub_parM n hn (cycOne n) h1 (hM C hne hx) C hx
  -- (c)
  have hreach0 : ∀ C : Cyc (F154 n), Reach (V154 n) C C0 := by
    obtain ⟨y, hyM, hy⟩ := exists_edge_to_zero n hn C0 hC0
    have hyp := periodic_of_mem_parM n hn hyM
    have hto : Reach (V154 n) (cycOne n) C0 :=
      reach_trans (hub_parM n hn (cycOne n) h1 hyM _ (mem_cycleOf (F154 n) y hyp)).2
        (hy _ (mem_cycleOf (F154 n) y hyp))
    intro C
    by_cases hC : C = C0
    · rw [hC]
      exact reach_refl _
    · exact reach_trans (hhub C hC).1 hto
  -- (d)
  have hK : IsClosedClass (V154 n) {C0} := by
    refine ⟨Set.singleton_nonempty _, ?_, ?_⟩
    · intro a ha b hb'
      rw [Set.mem_singleton_iff.mp ha, Set.mem_singleton_iff.mp hb']
      exact reach_refl _
    · intro a ha b hG
      rw [Set.mem_singleton_iff.mp ha] at hG
      exact absurd hG (hb.2 b)
  have huniq : ∀ K, IsClosedClass (V154 n) K → K = {C0} := by
    rintro K ⟨⟨a, ha⟩, hsc, hcl⟩
    have hC0K : C0 ∈ K := reach_mem_of_closed (V154 n) hcl ha (hreach0 a)
    ext C
    constructor
    · intro hC
      exact Set.mem_singleton_iff.mpr (reach_eq_of_no_out (V154 n) hb.2 (hsc C0 hC0K C hC))
    · intro hC
      rw [Set.mem_singleton_iff.mp hC]
      exact hC0K
  -- (e)
  obtain ⟨hSel, hgmin0⟩ := (section_2_4_ECA n (ruleOfNumber 154)).2.2.2.2 {C0} hK huniq
  have hgmin : gammaMin (V154 n) = numCycles (F154 n) - 1 := hgmin0
  have hC0Sel : C0 ∈ Sel (V154 n) := by
    rw [hSel]
    exact Set.mem_singleton _
  have hg0 : gamma (V154 n) C0 = gammaMin (V154 n) := hC0Sel
  have hcard : numCycles (F154 n) = Fintype.card (Cyc (F154 n)) := Nat.card_eq_fintype_card
  have hpos : 0 < Fintype.card (Cyc (F154 n)) := Fintype.card_pos_iff.mpr ⟨C0⟩
  -- a cycle of `M` at distance two from `{0}`
  obtain ⟨-, -⟩ := hb
  have h23 := cast_ne n 2 3 (by norm_num) (by omega)
  have p2 : par n ((2 : ℕ) : ZMod n) = 0 := by rw [par_natCast n hn]; decide
  have p3 : par n ((3 : ℕ) : ZMod n) = 0 + 1 := by rw [par_natCast n hn]; decide
  have hAM : two n ((2 : ℕ) : ZMod n) ((3 : ℕ) : ZMod n) ∈ parM n :=
    mem_parM_of n 0 (not_Z_of n _ p2 (by rw [two_first n h23]; exact one_ne_zero))
      (not_Z_of n _ p3 (by rw [two_second n h23]; exact one_ne_zero))
  have hAp := periodic_of_mem_parM n hn hAM
  have hAC := mem_cycleOf (F154 n) _ hAp
  have hCA : cycleOf (F154 n) _ hAp ≠ C0 := by
    intro h
    rw [h, hC0] at hAC
    have h' := congrFun (Set.mem_singleton_iff.mp hAC) ((2 : ℕ) : ZMod n)
    rw [two_first n h23] at h'
    exact one_ne_zero h'
  have hVA := V_zero_le_two n C0 _ h0 _ _ hAC
  have hgam : ∀ C : Cyc (F154 n), C ≠ C0 → gamma (V154 n) C = numCycles (F154 n) := by
    intro C hne
    have hnotSel : gamma (V154 n) C ≠ gammaMin (V154 n) := by
      intro h
      have hC : C ∈ Sel (V154 n) := h
      rw [hSel] at hC
      exact hne (Set.mem_singleton_iff.mp hC)
    have hge := gammaMin_le (V154 n) C
    have hle := gamma_le_card_add (V154 n) C C0 _ (Ne.symm hne)
      (fun d hd => reach_trans (hhub d hd).1 (hhub C hne).2) hCA 1 hVA
    rw [hgmin, hcard] at hnotSel hge
    rw [hcard]
    omega
  have hgle : ∀ C : Cyc (F154 n), gamma (V154 n) C ≤ gammaMin (V154 n) + 1 := by
    intro C
    by_cases hC : C = C0
    · rw [hC, hg0]
      exact Nat.le_succ _
    · rw [hgam C hC, hgmin]
      omega
  -- (f)
  have hkM : ∀ (v : Code) (x : State n), x ∈ parM n → Contains n x v → k154 n v ≤ 1 :=
    fun v x hxM hc => k_le_one_of_cycle n hn3 v _ (hgle _) x
      (mem_cycleOf (F154 n) x (periodic_of_mem_parM n hn hxM)) hc
  have hk1 : ∀ v : Code, k154 n v ≤ 1 := by
    rintro ⟨a, b, c⟩
    rcases zmod2_cases a with rfl | rfl <;> rcases zmod2_cases b with rfl | rfl <;>
      rcases zmod2_cases c with rfl | rfl
    · exact k_le_one_of_cycle n hn3 _ C0 (hgle C0) 0 h0 ⟨0, rfl⟩
    · obtain ⟨x, hx, hc⟩ := codes_in_M n hn hn4 (0, 0, 1) (Or.inl rfl)
      exact hkM _ x hx hc
    · exact kIndex_le_one n _ _ ⟨C0, hC0Sel, 0, h0, _, code_010_flip n hn3⟩
    · obtain ⟨x, hx, hc⟩ := codes_in_M n hn hn4 (0, 1, 1) (Or.inr (Or.inl rfl))
      exact hkM _ x hx hc
    · obtain ⟨x, hx, hc⟩ := codes_in_M n hn hn4 (1, 0, 0) (Or.inr (Or.inr (Or.inr (Or.inl rfl))))
      exact hkM _ x hx hc
    · obtain ⟨x, hx, hc⟩ := codes_in_M n hn hn4 (1, 0, 1) (Or.inr (Or.inr (Or.inr (Or.inr rfl))))
      exact hkM _ x hx hc
    · obtain ⟨x, hx, hc⟩ := codes_in_M n hn hn4 (1, 1, 0) (Or.inr (Or.inr (Or.inl rfl)))
      exact hkM _ x hx hc
    · exact k_le_one_of_cycle n hn3 _ (cycOne n) (hgle _) (one n) h1 ⟨0, rfl⟩
  have hk000 : k154 n (0, 0, 0) = 0 :=
    (kIndex_eq_zero_iff n _ hn3 _).mpr ⟨C0, hC0Sel, 0, h0, ⟨0, rfl⟩⟩
  have hkne : ∀ v : Code, v ≠ (0, 0, 0) → k154 n v = 1 := by
    intro v hv
    refine le_antisymm (hk1 v) (Nat.one_le_iff_ne_zero.mpr fun hz => ?_)
    obtain ⟨C, hCS, x, hxC, i, hi⟩ := (kIndex_eq_zero_iff n _ hn3 v).mp hz
    rw [hSel] at hCS
    rw [Set.mem_singleton_iff.mp hCS, hC0] at hxC
    rw [Set.mem_singleton_iff.mp hxC] at hi
    exact hv hi.symm
  have hkstar : kStar154 n = 1 := by
    apply le_antisymm
    · exact Finset.sup_le fun v _ => hk1 v
    · have h := Finset.le_sup (f := kIndex n (ruleOfNumber 154))
        (Finset.mem_univ ((1 : ZMod 2), (1 : ZMod 2), (1 : ZMod 2)))
      have h111 : kIndex n (ruleOfNumber 154) (1, 1, 1) = 1 := hkne _ (by decide)
      rw [h111] at h
      exact h
  have hb2 := theorem_3_9_b n k' hk C0 hC0
  refine ⟨hM, hb2, hreach0, ⟨hK, huniq⟩, ⟨?_, hgam, hSel⟩, hk000, hkne, hkstar⟩
  rw [hg0, hgmin]

/-! ### Theorem 3.10 -/

theorem theorem_3_10 : Theorem_3_10 := by
  intro n _ hn3 hnp
  have h1 := one_mem_cycOne n
  have h0 : (0 : State n) ∈ (cycZero n).1 := Set.mem_singleton _
  have hC0 : (cycZero n).1 = {0} := rfl
  have hr := resistanceECA n (ruleOfNumber 154)
  -- every cycle reaches the hub and is reached from it
  have hconn : ∀ C : Cyc (F154 n),
      Reach (V154 n) C (cycOne n) ∧ Reach (V154 n) (cycOne n) C := by
    by_cases hn : Even n
    · have hnz : ∀ C : Cyc (F154 n), C ≠ cycZero n →
          Reach (V154 n) C (cycOne n) ∧ Reach (V154 n) (cycOne n) C := by
        intro C hne
        obtain ⟨x, hx⟩ := C.nonempty (F154 n)
        have hx0 : x ≠ 0 := by
          intro h
          rw [h] at hx
          exact hne (Cyc.eq_of_mem (F154 n) hx h0)
        by_cases hxM : x ∈ parM n
        · exact hub_parM n hn (cycOne n) h1 hxM C hx
        · exact hub_not_parM n hn (cycOne n) h1 hxM hx0 C hx
      intro C
      by_cases hC : C = cycZero n
      · rw [hC]
        constructor
        · obtain ⟨C', ⟨t, ht⟩, -⟩ := endsOn_existsUnique (F154 n) (e n 0)
          have hne' : C' ≠ cycZero n := by
            intro h
            rw [h, hC0] at ht
            exact lemma_3_4_b_zero n hn hnp t (Set.mem_singleton_iff.mp ht)
          have hflip : TheoremA.flip n 0 0 = e n 0 := zero_add _
          have hG : V154 n (cycZero n) C' = 1 :=
            (VE_eq_one_iff (Ne.symm hne')).mpr ⟨0, h0, 0, t, by rw [hflip]; exact ht⟩
          exact Relation.ReflTransGen.head hG (hnz C' hne').1
        · obtain ⟨y, hyM, hy⟩ := exists_edge_to_zero n hn (cycZero n) hC0
          have hyp := periodic_of_mem_parM n hn hyM
          exact reach_trans (hub_parM n hn (cycOne n) h1 hyM _ (mem_cycleOf (F154 n) y hyp)).2
            (hy _ (mem_cycleOf (F154 n) y hyp))
      · exact hnz C hC
    · exact fun C => hub_odd n hn (cycOne n) h1 C
  have hsc : ∀ C C' : Cyc (F154 n), Reach (V154 n) C C' :=
    fun C C' => reach_trans (hconn C).1 (hconn C').2
  have : Nonempty (Cyc (F154 n)) := ⟨cycZero n⟩
  obtain ⟨hK, huniq⟩ := closed_univ_of_connected (V154 n) hsc
  obtain ⟨hSel, hgmin0⟩ := (section_2_4_ECA n (ruleOfNumber 154)).2.2.2.2 Set.univ hK huniq
  have hgmin : gammaMin (V154 n) = numCycles (F154 n) - 1 := hgmin0
  have hall : ∀ C : Cyc (F154 n), C ∈ Sel (V154 n) := by
    intro C
    rw [hSel]
    exact Set.mem_univ C
  -- every code occurs in a periodic state
  have hcodes : ∀ v : Code, ∃ x, x ∈ periodicPts (F154 n) ∧ Contains n x v := by
    by_cases hn : Even n
    · have hn4 : 4 ≤ n := by
        obtain ⟨m, hm⟩ := hn
        omega
      have hn5 : 5 ≤ n := by
        rcases Nat.lt_or_ge n 5 with h | h
        · exfalso
          have h4 : n = 4 := by omega
          exact hnp ⟨2, by rw [h4]; norm_num⟩
        · exact h
      have hMper : ∀ v : Code, (∃ x ∈ parM n, Contains n x v) →
          ∃ x, x ∈ periodicPts (F154 n) ∧ Contains n x v := by
        rintro v ⟨x, hxM, hc⟩
        exact ⟨x, periodic_of_mem_parM n hn hxM, hc⟩
      rintro ⟨a, b, c⟩
      rcases zmod2_cases a with rfl | rfl <;> rcases zmod2_cases b with rfl | rfl <;>
        rcases zmod2_cases c with rfl | rfl
      · exact ⟨0, mem_periodicPts.mpr ⟨1, Nat.one_pos, F154_zero n⟩, ⟨0, rfl⟩⟩
      · exact hMper _ (codes_in_M n hn hn4 (0, 0, 1) (Or.inl rfl))
      · exact hMper _ (code_010_in_M n hn hn5)
      · exact hMper _ (codes_in_M n hn hn4 (0, 1, 1) (Or.inr (Or.inl rfl)))
      · exact hMper _ (codes_in_M n hn hn4 (1, 0, 0) (Or.inr (Or.inr (Or.inr (Or.inl rfl)))))
      · exact hMper _ (codes_in_M n hn hn4 (1, 0, 1) (Or.inr (Or.inr (Or.inr (Or.inr rfl)))))
      · exact hMper _ (codes_in_M n hn hn4 (1, 1, 0) (Or.inr (Or.inr (Or.inl rfl))))
      · exact ⟨one n, mem_periodicPts.mpr ⟨1, Nat.one_pos, F154_one n⟩, ⟨0, rfl⟩⟩
    · intro v
      obtain ⟨x, hx⟩ := D_nonempty n hn3 v
      exact ⟨x, periodic_of_odd n hn x, hx⟩
  have hk0 : ∀ v : Code, k154 n v = 0 := by
    intro v
    obtain ⟨x, hxp, hc⟩ := hcodes v
    exact (kIndex_eq_zero_iff n _ hn3 v).mpr ⟨cycleOf (F154 n) x hxp, hall _, x, mem_cycleOf (F154 n) x hxp, hc⟩
  refine ⟨hsc, fun C => ?_, hall, hk0, (kStar_eq_zero_iff n _).mpr hk0⟩
  have hC : gamma (V154 n) C = gammaMin (V154 n) := hall C
  rw [hC, hgmin]

/-! ### Theorem 3.11 -/

theorem theorem_3_11 : Theorem_3_11 := by
  intro n _ hn3
  refine ⟨fun hp => ?_, fun hnp => ?_⟩
  · obtain ⟨k, hk⟩ := hp
    have hk2 : 2 ≤ k := by
      by_contra hlt
      have hk' : k = 0 ∨ k = 1 := by omega
      rcases hk' with rfl | rfl
      · rw [hk] at hn3
        norm_num at hn3
      · rw [hk] at hn3
        norm_num at hn3
    obtain ⟨-, -, -, -, -, hk000, hkne, hkstar⟩ := theorem_3_9 n k hk2 hk (cycZero n) rfl
    refine ⟨hkstar, fun C0 hC0 => ?_, hk000, hkne⟩
    exact (theorem_3_9 n k hk2 hk C0 hC0).2.2.2.2.1.2.2
  · obtain ⟨-, -, hall, hk0, hkstar⟩ := theorem_3_10 n hn3 hnp
    exact ⟨hkstar, hall, hk0⟩

end RingSize.Rule154

end
