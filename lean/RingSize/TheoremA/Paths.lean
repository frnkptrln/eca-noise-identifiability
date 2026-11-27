module

public import RingSize.TheoremA.Trees
import Mathlib.Data.Fintype.Pigeonhole
import Mathlib.Data.Nat.Find

/-!
# Paths, cycles and the weights between cycles

Proofs for Part 2 of `Statement.lean`: cycles are invariant and pairwise disjoint, the orbit of every state
ends on exactly one cycle, `V(C, C') ≥ 1` for distinct cycles, and Lemma 2.3 in its general form. At the end
the statements of `Statement.lean` that live in the general setting are proved.
-/

public section

namespace RingSize.TheoremA

open Function

universe u

variable {X : Type u} [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ)

/-! ### Orbits and cycles -/

omit [Fintype X] [DecidableEq X] in
theorem mem_orbit_self (x : X) : x ∈ orbit F x := ⟨0, rfl⟩

omit [Fintype X] [DecidableEq X] in
theorem orbit_iterate_mem {x y : X} (h : y ∈ orbit F x) (t : ℕ) : F^[t] y ∈ orbit F x := by
  obtain ⟨s, rfl⟩ := h
  exact ⟨t + s, Function.iterate_add_apply F t s x⟩

omit [Fintype X] [DecidableEq X] in
/-- A periodic state lies on the orbit of every state of its orbit. -/
theorem mem_orbit_of_periodic {x z : X} (hx : x ∈ periodicPts F) (hz : z ∈ orbit F x) :
    x ∈ orbit F z := by
  obtain ⟨t, rfl⟩ := hz
  obtain ⟨n, hn, hper⟩ := mem_periodicPts.mp hx
  have ht : t ≤ t * n := Nat.le_mul_of_pos_right t hn
  have hper' : F^[t * n] x = x := hper.const_mul t
  refine ⟨t * n - t, ?_⟩
  rw [← Function.iterate_add_apply, Nat.sub_add_cancel ht]
  exact hper'

omit [Fintype X] [DecidableEq X] in
theorem Cyc.iterate_mem (C : Cyc F) {y : X} (hy : y ∈ C.1) (t : ℕ) : F^[t] y ∈ C.1 := by
  obtain ⟨x, -, hC⟩ := C.2
  rw [hC] at hy ⊢
  exact orbit_iterate_mem F hy t

omit [Fintype X] [DecidableEq X] in
theorem Cyc.nonempty (C : Cyc F) : C.1.Nonempty := by
  obtain ⟨x, -, hC⟩ := C.2
  exact ⟨x, by rw [hC]; exact mem_orbit_self F x⟩

omit [Fintype X] [DecidableEq X] in
/-- A cycle is the orbit of each of its states. -/
theorem Cyc.eq_orbit (C : Cyc F) {z : X} (hz : z ∈ C.1) : C.1 = orbit F z := by
  obtain ⟨x, hx, hC⟩ := C.2
  rw [hC] at hz ⊢
  have hxz : x ∈ orbit F z := mem_orbit_of_periodic F hx hz
  apply Set.Subset.antisymm
  · rintro y ⟨s, rfl⟩
    exact orbit_iterate_mem F hxz s
  · rintro y ⟨s, rfl⟩
    exact orbit_iterate_mem F hz s

omit [Fintype X] [DecidableEq X] in
/-- Two cycles with a common state are equal. -/
theorem Cyc.eq_of_mem {C C' : Cyc F} {z : X} (hz : z ∈ C.1) (hz' : z ∈ C'.1) : C = C' :=
  Subtype.ext ((C.eq_orbit F hz).trans (C'.eq_orbit F hz').symm)

omit [Fintype X] [DecidableEq X] in
/-- Every state of a cycle is the image of a state of the cycle. -/
theorem Cyc.exists_preimage (C : Cyc F) {y : X} (hy : y ∈ C.1) : ∃ z ∈ C.1, F z = y := by
  obtain ⟨x, hx, hC⟩ := C.2
  rw [hC] at hy ⊢
  obtain ⟨t, rfl⟩ := hy
  obtain ⟨n, hn, hper⟩ := mem_periodicPts.mp hx
  cases t with
  | zero =>
    refine ⟨F^[n - 1] x, ⟨n - 1, rfl⟩, ?_⟩
    have h1 : F (F^[n - 1] x) = F^[n - 1 + 1] x := (Function.iterate_succ_apply' F (n - 1) x).symm
    rw [h1, Nat.sub_add_cancel hn]
    exact hper
  | succ t =>
    exact ⟨F^[t] x, ⟨t, rfl⟩, (Function.iterate_succ_apply' F t x).symm⟩

omit [DecidableEq X] in
theorem exists_iterate_periodic (x : X) : ∃ t, F^[t] x ∈ periodicPts F := by
  have key : ∀ i j : ℕ, i < j → F^[i] x = F^[j] x → ∃ t, F^[t] x ∈ periodicPts F := by
    intro i j hlt h
    refine ⟨i, mem_periodicPts.mpr ⟨j - i, Nat.sub_pos_of_lt hlt, ?_⟩⟩
    show F^[j - i] (F^[i] x) = F^[i] x
    rw [← Function.iterate_add_apply, Nat.sub_add_cancel hlt.le]
    exact h.symm
  obtain ⟨i, j, hij, heq⟩ := Finite.exists_ne_map_eq_of_infinite (fun k : ℕ => F^[k] x)
  have heq' : F^[i] x = F^[j] x := heq
  rcases Nat.lt_or_gt_of_ne hij with h | h
  · exact key i j h heq'
  · exact key j i h heq'.symm

/-- The cycle of a periodic state. -/
def cycleOf (y : X) (hy : y ∈ periodicPts F) : Cyc F :=
  Subtype.mk (orbit F y) ⟨y, hy, rfl⟩

omit [Fintype X] [DecidableEq X] in
theorem mem_cycleOf (y : X) (hy : y ∈ periodicPts F) : y ∈ (cycleOf F y hy).1 :=
  mem_orbit_self F y

omit [DecidableEq X] in
/-- Paper, 2.2: the orbit of every state ends on exactly one cycle. -/
theorem endsOn_existsUnique (x : X) : ∃! C : Cyc F, EndsOn F x C := by
  obtain ⟨t, ht⟩ := exists_iterate_periodic F x
  refine ⟨cycleOf F _ ht, ⟨t, mem_orbit_self F _⟩, ?_⟩
  rintro C' ⟨t', ht'⟩
  have h1 : F^[t' + t] x ∈ (cycleOf F _ ht).1 := by
    rw [Function.iterate_add_apply]
    exact (cycleOf F _ ht).iterate_mem F (mem_orbit_self F _) t'
  have h2 : F^[t' + t] x ∈ C'.1 := by
    rw [Nat.add_comm, Function.iterate_add_apply]
    exact C'.iterate_mem F ht' t
  exact Cyc.eq_of_mem F h2 h1

/-! ### Paths -/

omit [Fintype X] [DecidableEq X] in
theorem pathRes_cons (x : X) (l : List X) (h : l ≠ []) :
    pathRes r (x :: l) = r x (l.head h) + pathRes r l := by
  cases l with
  | nil => exact absurd rfl h
  | cons y l => rfl

variable {F r} in
omit [Fintype X] [DecidableEq X] in
/-- A path of resistance 0 follows `F`. -/
theorem pathRes_eq_zero (hr : IsResistance F r) :
    ∀ (l : List X) (h : l ≠ []), pathRes r l = 0 → l.getLast h = F^[l.length - 1] (l.head h)
  | [], h, _ => absurd rfl h
  | [x], _, _ => rfl
  | x :: y :: l, _, h0 => by
    rw [pathRes_cons r x (y :: l) (List.cons_ne_nil _ _)] at h0
    have h1 : r x y = 0 := by
      have : r x ((y :: l).head (List.cons_ne_nil _ _)) = 0 := by omega
      exact this
    have h2 : pathRes r (y :: l) = 0 := by omega
    have hy : y = F x := (hr x y).mp h1
    have ih := pathRes_eq_zero hr (y :: l) (List.cons_ne_nil _ _) h2
    rw [List.getLast_cons (List.cons_ne_nil _ _), ih]
    simp only [List.head_cons, List.length_cons]
    rw [hy, show l.length + 1 + 1 - 1 = (l.length + 1 - 1) + 1 by omega, Function.iterate_succ_apply]

variable {F r} in
omit [Fintype X] [DecidableEq X] in
/-- A path of resistance 1 follows `F`, makes one step of resistance 1, and follows `F` again. -/
theorem pathRes_eq_one (hr : IsResistance F r) :
    ∀ (l : List X) (h : l ≠ []), pathRes r l = 1 →
      ∃ (s : ℕ) (y z : X) (t : ℕ), y = F^[s] (l.head h) ∧ r y z = 1 ∧ F^[t] z = l.getLast h
  | [], h, _ => absurd rfl h
  | [x], _, h1 => by simp [pathRes] at h1
  | x :: y :: l, _, h1 => by
    rw [pathRes_cons r x (y :: l) (List.cons_ne_nil _ _)] at h1
    have hhead : (y :: l).head (List.cons_ne_nil _ _) = y := rfl
    rw [hhead] at h1
    by_cases hxy : r x y = 0
    · have h2 : pathRes r (y :: l) = 1 := by omega
      have hy : y = F x := (hr x y).mp hxy
      obtain ⟨s, y', z, t, hy', hrz, hlast⟩ :=
        pathRes_eq_one hr (y :: l) (List.cons_ne_nil _ _) h2
      refine ⟨s + 1, y', z, t, ?_, hrz, ?_⟩
      · rw [hy']
        simp only [List.head_cons]
        rw [hy, Function.iterate_succ_apply]
      · rw [hlast, List.getLast_cons (List.cons_ne_nil _ _)]
    · have h2 : pathRes r (y :: l) = 0 := by omega
      have h3 : r x y = 1 := by omega
      have hl := pathRes_eq_zero hr (y :: l) (List.cons_ne_nil _ _) h2
      refine ⟨0, x, y, (y :: l).length - 1, rfl, h3, ?_⟩
      rw [List.getLast_cons (List.cons_ne_nil _ _), hl]
      rfl

/-- The path `z, F z, ..., F^t z`. -/
def orbitList (z : X) : ℕ → List X
  | 0 => [z]
  | t + 1 => z :: orbitList (F z) t

omit [Fintype X] [DecidableEq X] in
theorem orbitList_ne_nil (z : X) (t : ℕ) : orbitList F z t ≠ [] := by
  cases t <;> simp [orbitList]

omit [Fintype X] [DecidableEq X] in
theorem head_orbitList (z : X) (t : ℕ) : (orbitList F z t).head (orbitList_ne_nil F z t) = z := by
  cases t <;> simp [orbitList]

omit [Fintype X] [DecidableEq X] in
theorem getLast_orbitList :
    ∀ (t : ℕ) (z : X), (orbitList F z t).getLast (orbitList_ne_nil F z t) = F^[t] z
  | 0, z => by simp [orbitList]
  | t + 1, z => by
    have h : orbitList F z (t + 1) = z :: orbitList F (F z) t := rfl
    simp only [h]
    rw [List.getLast_cons (orbitList_ne_nil F (F z) t), getLast_orbitList t (F z),
      Function.iterate_succ_apply]

variable {F r} in
omit [Fintype X] [DecidableEq X] in
theorem pathRes_orbitList (hr : IsResistance F r) : ∀ (t : ℕ) (z : X), pathRes r (orbitList F z t) = 0
  | 0, z => rfl
  | t + 1, z => by
    have h : orbitList F z (t + 1) = z :: orbitList F (F z) t := rfl
    rw [h, pathRes_cons r z _ (orbitList_ne_nil F (F z) t), head_orbitList, pathRes_orbitList hr t (F z),
      (hr z (F z)).mpr rfl]

/-! ### `R` and `V` -/

omit [Fintype X] [DecidableEq X] in
theorem R_le_of_path {A B : Set X} (l : List X) (h : l ≠ []) (hA : l.head h ∈ A)
    (hB : l.getLast h ∈ B) : R r A B ≤ pathRes r l :=
  Nat.sInf_le ⟨l, h, hA, hB, rfl⟩

omit [Fintype X] [DecidableEq X] in
theorem exists_path_R {A B : Set X} (hA : A.Nonempty) (hB : B.Nonempty) :
    ∃ (l : List X) (h : l ≠ []), l.head h ∈ A ∧ l.getLast h ∈ B ∧ pathRes r l = R r A B := by
  obtain ⟨a, ha⟩ := hA
  obtain ⟨b, hb⟩ := hB
  exact Nat.sInf_mem (⟨_, [a, b], List.cons_ne_nil _ _, ha, hb, rfl⟩ :
    {w | ∃ (l : List X) (h : l ≠ []), l.head h ∈ A ∧ l.getLast h ∈ B ∧ pathRes r l = w}.Nonempty)

omit [Fintype X] [DecidableEq X] in
variable {F r} in
/-- Paper, Lemma 2.3, first sentence: `V(C, C') ≥ 1` for distinct cycles. -/
theorem one_le_Vc (hr : IsResistance F r) {C C' : Cyc F} (hne : C ≠ C') : 1 ≤ Vc F r C C' := by
  by_contra hlt
  have h0 : Vc F r C C' = 0 := by omega
  obtain ⟨l, h, hA, hB, hres⟩ := exists_path_R r (C.nonempty F) (C'.nonempty F)
  have hres0 : pathRes r l = 0 := hres.trans h0
  have hlast := pathRes_eq_zero hr l h hres0
  have hmem : l.getLast h ∈ C.1 := by
    rw [hlast]
    exact C.iterate_mem F hA _
  exact hne (Cyc.eq_of_mem F hmem hB)

omit [Fintype X] [DecidableEq X] in
variable {F r} in
/-- Paper, Lemma 2.3, second sentence, without the flips. -/
theorem Vc_eq_one_iff (hr : IsResistance F r) {C C' : Cyc F} (hne : C ≠ C') :
    Vc F r C C' = 1 ↔ ∃ y ∈ C.1, ∃ z, r y z = 1 ∧ EndsOn F z C' := by
  constructor
  · intro h1
    obtain ⟨l, h, hA, hB, hres⟩ := exists_path_R r (C.nonempty F) (C'.nonempty F)
    have hres1 : pathRes r l = 1 := hres.trans h1
    obtain ⟨s, y, z, t, hy, hrz, hlast⟩ := pathRes_eq_one hr l h hres1
    refine ⟨y, ?_, z, hrz, t, ?_⟩
    · rw [hy]
      exact C.iterate_mem F hA s
    · rw [hlast]
      exact hB
  · rintro ⟨y, hy, z, hrz, t, ht⟩
    have hle : Vc F r C C' ≤ 1 := by
      have hpath := R_le_of_path r (A := C.1) (B := C'.1) (y :: orbitList F z t)
        (List.cons_ne_nil _ _) hy (by
          rw [List.getLast_cons (orbitList_ne_nil F z t), getLast_orbitList]
          exact ht)
      rw [pathRes_cons r y _ (orbitList_ne_nil F z t), head_orbitList, pathRes_orbitList hr, hrz]
        at hpath
      exact hpath
    have hge := one_le_Vc hr hne
    omega

variable {F r} in
omit [Fintype X] [DecidableEq X] in
/-- `R(C → B) = 0` iff a state of the cycle `C` lies in `B`. -/
theorem R_cycle_eq_zero_iff (hr : IsResistance F r) (C : Cyc F) {B : Set X} (hB : B.Nonempty) :
    R r C.1 B = 0 ↔ ∃ x ∈ C.1, x ∈ B := by
  constructor
  · intro h0
    obtain ⟨l, h, hA, hBl, hres⟩ := exists_path_R r (C.nonempty F) hB
    have hlast := pathRes_eq_zero hr l h (hres.trans h0)
    refine ⟨l.getLast h, ?_, hBl⟩
    rw [hlast]
    exact C.iterate_mem F hA _
  · rintro ⟨x, hxC, hxB⟩
    have hle := R_le_of_path r (A := C.1) (B := B) [x] (List.cons_ne_nil _ _) hxC hxB
    exact Nat.le_zero.mp hle

/-! ### The statements of `Statement.lean` in the general setting -/

theorem endsOnExactlyOneCycle : EndsOnExactlyOneCycle.{u} := by
  intro X _ _ F x
  exact endsOn_existsUnique F x

theorem lemma_2_3_general : Lemma_2_3_general.{u} := by
  intro X _ _ F r hr C C' hne
  exact ⟨one_le_Vc hr hne, Vc_eq_one_iff hr hne⟩

theorem lemma_2_5 : Lemma_2_5.{u} := by
  intro X _ _ F r hr B N p hT hN
  exact ⟨reroot_isInTree N hT,
    fun h1 => reroot_le (Vc F r) (fun _ _ hab => one_le_Vc hr hab) hT hN h1⟩

theorem lemma_2_6 : Lemma_2_6.{u} := by
  intro X _ _ F r hr C C' hC h1
  exact closure (Vc F r) (fun _ _ hab => one_le_Vc hr hab) hC h1

theorem closedClassReachable : ClosedClassReachable.{u} := by
  intro ι _ _ V a
  exact exists_closedClass_reach V a

theorem lemma_2_7 : Lemma_2_7.{u} := by
  intro X _ _ F r hr C hC
  exact inclosed (Vc F r) (fun _ _ hab => one_le_Vc hr hab) hC

theorem theorem_2_8 : Theorem_2_8.{u} := by
  intro X _ _ F r hr
  have hV : ∀ a b : Cyc F, a ≠ b → 1 ≤ Vc F r a b := fun _ _ hab => one_le_Vc hr hab
  refine ⟨fun C hC => theoremA_union (Vc F r) hV hC, fun K hK huniq => ?_⟩
  have h := theoremA_unique (Vc F r) hV hK huniq
  rw [numCycles, Nat.card_eq_fintype_card]
  exact h

end RingSize.TheoremA

end
