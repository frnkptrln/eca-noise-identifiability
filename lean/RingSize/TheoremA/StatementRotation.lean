module

public import RingSize.TheoremA.Statement
public import Mathlib.Logic.Equiv.Defs
public import Mathlib.Data.Set.Image

/-!
# Lemma 2.4 of the ring-size paper (rotation): statements

This file contains only definitions and statements. The proofs are in `RingSize/TheoremA/Rotation.lean`.
Source: `paper/ring_size_paper.tex`, Section 2, Lemma 2.4:

"`V(σC, σC') = V(C, C')` and `γ(σC) = γ(C)` for all cycles `C`, `C'`. Hence `S` and `G_1` are invariant under
rotation."

Here `σC` is the image of the cycle `C` under the rotation `σ`. In Lean a cycle is a set with a proof that it
is a cycle, so the statements below speak of cycles `D`, `D'` whose sets are the images of the sets of `C`,
`C'`; a separate clause says that the image of a cycle is a cycle, so that such `D`, `D'` exist, and another
that every cycle is the image of a cycle. With these two clauses `C ↦ σC` is a bijection of the set of cycles
(it is injective because `σ` is), so "`σC ∈ S` iff `C ∈ S`" gives `σ(S) = S`, and the clause on edges says
that `C ↦ σC` is an automorphism of `G_1`.
-/

@[expose] public section

namespace RingSize.TheoremA

open Function

universe u

/-- Paper, Lemma 2.4, for any bijection `s` of the states that commutes with the map `F` and preserves the
resistance (the two properties of the rotation that the paper's proof uses):
the image of a cycle is a cycle; every cycle is the image of a cycle; and if `D`, `D'` are the images of
the cycles `C`, `C'`, then `V(D, D') = V(C, C')`, `γ(D) = γ(C)`, `D` is selected iff `C` is, and `D → D'` is
an edge of `G_1` iff `C → C'` is. -/
def Lemma_2_4_general : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ) (s : X ≃ X),
    (∀ x, F (s x) = s (F x)) → (∀ x y, r (s x) (s y) = r x y) →
      (∀ C : Cyc F, IsCycle F (s '' C.1)) ∧
      (∀ D : Cyc F, ∃ C : Cyc F, D.1 = s '' C.1) ∧
      (∀ C C' D D' : Cyc F, D.1 = s '' C.1 → D'.1 = s '' C'.1 →
        Vc F r D D' = Vc F r C C' ∧
        gamma (Vc F r) D = gamma (Vc F r) C ∧
        (D ∈ Sel (Vc F r) ↔ C ∈ Sel (Vc F r)) ∧
        (G1 (Vc F r) D D' ↔ G1 (Vc F r) C C'))

/-- Paper, 2.1: the rotation `σ`, `(σ x)_i = x_{i-1}`. -/
def rot (n : ℕ) (x : State n) : State n :=
  fun i => x (i - 1)

/-- Paper, 2.1: "`F σ = σ F`", for every elementary rule. -/
def GlobalMap_rot : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule) (x : State n), globalMap n f (rot n x) = rot n (globalMap n f x)

/-- Paper, proof of Lemma 2.4: "`r(σ x, σ y) = r(x, y)`". -/
def Resistance_rot : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule) (x y : State n),
    resistance n f (rot n x) (rot n y) = resistance n f x y

/-- Paper, Lemma 2.4, for an elementary rule `f` on a ring of `n` cells and the rotation `σ = rot n`:
the rotation maps cycles to cycles; every cycle is a rotated cycle; and if `D`, `D'` are the rotated cycles
`σC`, `σC'`, then
`V(σC, σC') = V(C, C')`, `γ(σC) = γ(C)`, `σC ∈ S` iff `C ∈ S`, and `σC → σC'` is an edge of `G_1` iff
`C → C'` is. -/
def Lemma_2_4 : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule),
    (∀ C : Cyc (globalMap n f), IsCycle (globalMap n f) (rot n '' C.1)) ∧
    (∀ D : Cyc (globalMap n f), ∃ C : Cyc (globalMap n f), D.1 = rot n '' C.1) ∧
    (∀ C C' D D' : Cyc (globalMap n f), D.1 = rot n '' C.1 → D'.1 = rot n '' C'.1 →
      VE n f D D' = VE n f C C' ∧
      gamma (VE n f) D = gamma (VE n f) C ∧
      (D ∈ Sel (VE n f) ↔ C ∈ Sel (VE n f)) ∧
      (G1 (VE n f) D D' ↔ G1 (VE n f) C C'))

end RingSize.TheoremA

end
