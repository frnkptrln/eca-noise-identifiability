module

public import RingSize.Statement
public import Mathlib.Data.ZMod.Basic
public import Mathlib.Order.Lattice.Nat
public import Mathlib.Data.Fintype.Pi
public import Mathlib.Data.Fintype.EquivFin
public import Mathlib.Data.Set.Finite.Basic
public import Mathlib.Dynamics.PeriodicPts.Defs
public import Mathlib.InformationTheory.Hamming
public import Mathlib.Logic.Relation
public import Mathlib.Algebra.BigOperators.Group.Finset.Basic
public import Mathlib.SetTheory.Cardinal.Finite

/-!
# Section 2 of the ring-size paper: definitions and statements

This file contains only definitions and statements (as `Prop`-valued definitions). The proofs are in the
other files of `RingSize/TheoremA/` (`Paths.lean`, `ECA.lean`, `Checks.lean`); `AxiomCheckTheoremA.lean` checks
for every statement of this file that the theorem of that name has this type.
Source: `paper/ring_size_paper.tex`, Section 2 ("Setting"). Each definition names the place it formalizes.

The file has three parts.

1. Weighted graphs. A finite set of nodes with a weight `V a b`. In-trees, the stochastic potential, the
   selected set, the one-flip graph and its closed classes (paper, 2.2 and 2.4, where the nodes are the cycles).
2. Dynamics. A map `F` on a finite set of states with a resistance `r`. Paths, `R(A → B)`, cycles and the
   weights `V(C, C')` between cycles (paper, 2.2). The statements of Lemma 2.3 (first half), Lemmas 2.5 to 2.7
   and Theorem 2.8 are made in this generality; they do not use the structure of an elementary rule.
3. Elementary cellular automata on a ring of `n` cells (paper, 2.1 and 2.3), with Lemma 2.2 and the form of
   Lemma 2.3 that speaks of flips.

Proposition 2.1 of the paper, which links these integers to the noisy chain, is not formalized.
-/

@[expose] public section

namespace RingSize.TheoremA

open Function

universe u

/-! ## Part 1. Weighted graphs -/

section Graph

variable {ι : Type u} [Fintype ι] [DecidableEq ι] (V : ι → ι → ℕ)

/-- Paper, 2.2: a spanning in-tree rooted at `c` is "a set of `m - 1` edges `D → D'` between distinct
cycles, one out of every cycle `D ≠ C`, without directed circuit".
Here the tree is given by its parent map `p`: the edges are `d → p d` for `d ≠ c`. The value `p c` plays no
role (the root has no out-edge). The condition says that these edges contain no directed circuit: no node
comes back to itself after `k ≥ 1` steps without passing through the root. For `d ≠ c` and `k = 1` this says
`p d ≠ d`, so the edges join distinct nodes. (For `d = c` the condition says nothing.) -/
def IsInTree (c : ι) (p : ι → ι) : Prop :=
  ∀ (d : ι) (k : ℕ), 0 < k → (∀ j < k, p^[j] d ≠ c) → p^[k] d ≠ d

/-- Paper, 2.2: the weight of a tree is the sum of the weights `V d (p d)` of its edges `d → p d`, `d ≠ c`. -/
def treeWeight (c : ι) (p : ι → ι) : ℕ :=
  ∑ d ∈ Finset.univ.erase c, V d (p d)

/-- Paper, 2.2: the stochastic potential `γ(c)`, the least weight of a spanning in-tree rooted at `c`. -/
noncomputable def gamma (c : ι) : ℕ :=
  sInf {w | ∃ p, IsInTree c p ∧ treeWeight V c p = w}

/-- Paper, 2.2: `γ_min = min_c γ(c)`. -/
noncomputable def gammaMin : ℕ :=
  sInf (Set.range (gamma V))

/-- Paper, 2.2: the set of noise-selected nodes, those with `γ(c) = γ_min`. -/
def Sel : Set ι :=
  {c | gamma V c = gammaMin V}

/-- Paper, 2.4: the one-flip graph `G_1` has an edge `a → b` iff `V a b = 1`. -/
def G1 (a b : ι) : Prop :=
  V a b = 1

/-- There is a directed path of `G_1` from `a` to `b` (of length `≥ 0`). -/
def Reach (a b : ι) : Prop :=
  Relation.ReflTransGen (G1 V) a b

/-- Paper, 2.4: a closed class is "a strongly connected component of `G_1` that no edge of `G_1` leaves".
Here: a non-empty set of nodes, any two of which are joined by directed paths of `G_1` in both directions,
and which no edge of `G_1` leaves. (Such a set is a strongly connected component: a node that is reachable
from the set lies in it.) -/
def IsClosedClass (K : Set ι) : Prop :=
  K.Nonempty ∧ (∀ a ∈ K, ∀ b ∈ K, Reach V a b) ∧ (∀ a ∈ K, ∀ b, G1 V a b → b ∈ K)

end Graph

/-! ## Part 2. Dynamics -/

section Dynamics

variable {X : Type u} [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ)

/-- Paper, 2.2: "A step has resistance 0 iff it is a step of `F`." This is the only property of the
resistance that Lemmas 2.5 to 2.7 and Theorem 2.8 use. -/
def IsResistance : Prop :=
  ∀ x y, r x y = 0 ↔ y = F x

/-- Paper, 2.2: a path is a finite sequence of states; "its resistance is the sum of the resistances of its
steps". -/
def pathRes : List X → ℕ
  | [] => 0
  | [_] => 0
  | x :: y :: l => r x y + pathRes (y :: l)

/-- Paper, 2.2: `R(A → B)`, "the least resistance of a path from a state of `A` to a state of `B`".
(If `A` or `B` is empty there is no such path and the value is `0`. Cycles are never empty. `D_v` is empty
exactly when `n ≤ 2` and no state contains `v`; see `kIndex`.) -/
noncomputable def R (A B : Set X) : ℕ :=
  sInf {w | ∃ (l : List X) (h : l ≠ []), l.head h ∈ A ∧ l.getLast h ∈ B ∧ pathRes r l = w}

/-- The orbit of `x` under `F`. -/
def orbit (x : X) : Set X :=
  {y | ∃ t : ℕ, F^[t] x = y}

/-- Paper, 2.2: "A state `x` is periodic if `F^t x = x` for some `t ≥ 1`; a cycle is the orbit of a periodic
state." (`Function.periodicPts F` is Mathlib's set of periodic points.) -/
def IsCycle (C : Set X) : Prop :=
  ∃ x ∈ periodicPts F, C = orbit F x

/-- The type of cycles of `F`. -/
def Cyc : Type u :=
  {C : Set X // IsCycle F C}

noncomputable instance : Fintype (Cyc F) := by
  unfold Cyc; exact Fintype.ofFinite _

noncomputable instance : DecidableEq (Cyc F) := Classical.decEq _

/-- Paper, 2.2: `m`, the number of cycles. -/
noncomputable def numCycles : ℕ :=
  Nat.card (Cyc F)

/-- Paper, 2.2: "the orbit of `x` ends on" the cycle `C`. -/
def EndsOn (x : X) (C : Cyc F) : Prop :=
  ∃ t : ℕ, F^[t] x ∈ C.1

/-- Paper, 2.2: `V(C, C') = R(C → C')` for cycles `C`, `C'`. -/
noncomputable def Vc (C C' : Cyc F) : ℕ :=
  R r C.1 C'.1

end Dynamics

/-! ### Statements in the general setting -/

/-- Paper, 2.2: "The orbit of every state `x` enters exactly one cycle." -/
def EndsOnExactlyOneCycle : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (x : X), ∃! C : Cyc F, EndsOn F x C

/-- Paper, Lemma 2.3, without the flips: for cycles `C ≠ C'`, `V(C, C') ≥ 1`, and `V(C, C') = 1` iff some
step of resistance 1 leads from a state of `C` to a state whose orbit ends on `C'`. -/
def Lemma_2_3_general : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    ∀ C C' : Cyc F, C ≠ C' →
      1 ≤ Vc F r C C' ∧
      (Vc F r C C' = 1 ↔ ∃ y ∈ C.1, ∃ z, r y z = 1 ∧ EndsOn F z C')

/-- Paper, Lemma 2.5 (re-rooting): "Let `T` be an in-tree rooted at a cycle `B`, and let `N ≠ B`. Then `T`
without the out-edge of `N` and with the edge `B → N` is an in-tree rooted at `N`. If `V(B, N) = 1`, its
weight is at most the weight of `T`."
In terms of parent maps: the new tree is `Function.update p B N` with root `N`. -/
def Lemma_2_5 : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    ∀ (B N : Cyc F) (p : Cyc F → Cyc F), IsInTree B p → N ≠ B →
      IsInTree N (update p B N) ∧
      (Vc F r B N = 1 → treeWeight (Vc F r) N (update p B N) ≤ treeWeight (Vc F r) B p)

/-- Paper, Lemma 2.6 (closure): "If `C ∈ S` and `V(C, C') = 1`, then `C' ∈ S`." -/
def Lemma_2_6 : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    ∀ C C' : Cyc F, C ∈ Sel (Vc F r) → Vc F r C C' = 1 → C' ∈ Sel (Vc F r)

/-- Paper, 2.4: "Every finite directed graph has a closed class, and from every node there is a directed
path into some closed class." Stated here is the second half, which gives the first for every graph with at
least one node. (For the graph without nodes the first half is false; the graphs of the paper have a node.) -/
def ClosedClassReachable : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι] (V : ι → ι → ℕ) (a : ι),
    ∃ K, IsClosedClass V K ∧ ∃ b ∈ K, Reach V a b

/-- Paper, Lemma 2.7: "Every noise-selected cycle lies in a closed class of `G_1`." -/
def Lemma_2_7 : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    ∀ C : Cyc F, C ∈ Sel (Vc F r) → ∃ K, IsClosedClass (Vc F r) K ∧ C ∈ K

/-- Paper, Theorem 2.8 (Theorem A): "The set `S` of noise-selected cycles is a union of closed classes of
`G_1`. If `G_1` has a unique closed class `K`, then `S = K` and `γ_min = m - 1`."
First part: every selected cycle lies in a closed class that consists of selected cycles. -/
def Theorem_2_8 : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    (∀ C ∈ Sel (Vc F r), ∃ K, IsClosedClass (Vc F r) K ∧ C ∈ K ∧ K ⊆ Sel (Vc F r)) ∧
    (∀ K, IsClosedClass (Vc F r) K → (∀ K', IsClosedClass (Vc F r) K' → K' = K) →
      Sel (Vc F r) = K ∧ gammaMin (Vc F r) = numCycles F - 1)

/-! ### Checks of the definitions

Statements that would fail if a definition above said something else than intended. -/

/-- The condition "no directed circuit" in `IsInTree` is equivalent to: every node reaches the root along
the parent map. -/
def InTree_iff_reaches : Prop :=
  ∀ (ι : Type u) [Fintype ι] (c : ι) (p : ι → ι), IsInTree c p ↔ ∀ d, ∃ k, p^[k] d = c

/-- A set is a closed class in the sense of `IsClosedClass` iff it is a strongly connected component of
`G_1` (the set of nodes that reach a node `a` and are reached from it) that no edge of `G_1` leaves. -/
def ClosedClass_iff_component : Prop :=
  ∀ (ι : Type u) (V : ι → ι → ℕ) (K : Set ι),
    IsClosedClass V K ↔
      ∃ a, K = {b | Reach V a b ∧ Reach V b a} ∧ ∀ b ∈ K, ∀ c, G1 V b c → c ∈ K

/-- Paper, proof of Theorem 2.8: "every in-tree has weight at least `m - 1`". -/
def TreeWeight_lower_bound : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    ∀ (C : Cyc F) (p : Cyc F → Cyc F), IsInTree C p → numCycles F - 1 ≤ treeWeight (Vc F r) C p

/-- Consequence of `TreeWeight_lower_bound`: `γ(C) ≥ m - 1` for every cycle `C`. -/
def Gamma_lower_bound : Prop :=
  ∀ (X : Type u) [Fintype X] [DecidableEq X] (F : X → X) (r : X → X → ℕ), IsResistance F r →
    ∀ C : Cyc F, numCycles F - 1 ≤ gamma (Vc F r) C

/-! ## Part 3. Elementary cellular automata on a ring -/

section ECA

/-- Paper, 2.1: an elementary rule is a map `f : {0,1}^3 → {0,1}`. -/
abbrev LocalRule : Type :=
  ZMod 2 → ZMod 2 → ZMod 2 → ZMod 2

/-- Paper, 2.1: "rule number `N` is the map with `f(a, b, c)` equal to the bit of weight `2^(4a + 2b + c)`
in the binary expansion of `N`." -/
def ruleOfNumber (N : ℕ) : LocalRule :=
  fun a b c => if N.testBit (4 * a.val + 2 * b.val + c.val) then 1 else 0

/-- Paper, 2.1: a code is a word `v = abc`. -/
abbrev Code : Type :=
  ZMod 2 × ZMod 2 × ZMod 2

variable (n : ℕ) [NeZero n]

/-- Paper, 2.1: the global map, `(F x)_i = f(x_{i-1}, x_i, x_{i+1})`, indices mod `n`.
States are `RingSize.State n = (ZMod n → ZMod 2)`, as in the pilot. -/
def globalMap (f : LocalRule) (x : State n) : State n :=
  fun i => f (x (i - 1)) (x i) (x (i + 1))

/-- Paper, 2.1: the resistance `r(x, y) = H(F x, y)`, with `H` the Hamming distance. -/
def resistance (f : LocalRule) (x y : State n) : ℕ :=
  hammingDist (globalMap n f x) y

/-- Paper, 2.1: "a state `x` contains `v` if `(x_{i-1}, x_i, x_{i+1}) = v` for some cell `i`". -/
def Contains (x : State n) (v : Code) : Prop :=
  ∃ i : ZMod n, (x (i - 1), x i, x (i + 1)) = v

/-- Paper, 2.1: `D_v`, the set of states that contain `v`. -/
def D (v : Code) : Set (State n) :=
  {x | Contains n x v}

/-- Paper, 2.1: `x + e_j`, the flip of cell `j` of `x`. (`RingSize.e n j` is the state with a single one, at
cell `j`.) -/
def flip (x : State n) (j : ZMod n) : State n :=
  x + e n j

/-- `V(C, C')` for the cycles of the rule `f` on the ring of `n` cells. -/
noncomputable abbrev VE (f : LocalRule) : Cyc (globalMap n f) → Cyc (globalMap n f) → ℕ :=
  Vc (globalMap n f) (resistance n f)

/-- Paper, (1): `k_v = min_C [γ(C) + R(C → D_v)] - γ_min`, the minimum over all cycles.
The paper defines `k_v` for `n ≥ 3`. For `n ≤ 2` some codes occur in no state (for `n = 1` only `000` and `111`
occur, for `n = 2` only `000`, `010`, `101`, `111`); for such a code `D_v` is empty, `R(C → D_v)` is `0` by the
convention of `R`, and this definition gives `k_v = 0`. The statements about `k_v` and `k*` that need the paper's
meaning (`Lemma_2_2`, `KStar_unique_class`) assume `n ≥ 3`. -/
noncomputable def kIndex (f : LocalRule) (v : Code) : ℕ :=
  sInf (Set.range fun C : Cyc (globalMap n f) => gamma (VE n f) C + R (resistance n f) C.1 (D n v))
    - gammaMin (VE n f)

/-- Paper, (1): `k* = max_v k_v`, the maximum over the eight codes. -/
noncomputable def kStar (f : LocalRule) : ℕ :=
  Finset.univ.sup (kIndex n f)

end ECA

/-! ### Statements for elementary cellular automata -/

/-- The resistance `H(F x, y)` satisfies the hypothesis of Part 2. -/
def ResistanceECA : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule), IsResistance (globalMap n f) (resistance n f)

/-- The map `rule90` of the pilot is the global map of rule number 90. -/
def Rule90IsRuleNumber90 : Prop :=
  ∀ (n : ℕ) [NeZero n], rule90 n = globalMap n (ruleOfNumber 90)

/-- A check of the definitions of rule numbers and cycles: under rule 204 (the identity) every state is a
cycle by itself. -/
def Rule204_cycles : Prop :=
  ∀ (n : ℕ) [NeZero n] (x : State n), IsCycle (globalMap n (ruleOfNumber 204)) {x}

/-- A check of the rule numbering on a rule that is not its own mirror image: rule 154 has the local rule
`f(a, b, c) = c + a (1 + b)` (paper, Section 3.1, Lemma 3.2). A numbering with `a` and `c` exchanged would give
`a + c (1 + b)` instead. -/
def Rule154_local : Prop :=
  ∀ a b c : ZMod 2, ruleOfNumber 154 a b c = c + a * (1 + b)

/-- A check of the orientation of rule numbering and global map together: rule 170 (binary `10101010`, the local
rule `f(a, b, c) = c`) copies the right neighbour, `(F x)_i = x_{i+1}`. With a mirrored neighbourhood in
`globalMap` it would give `x_{i-1}`. -/
def Rule170_shift : Prop :=
  ∀ (n : ℕ) [NeZero n] (x : State n) (i : ZMod n), globalMap n (ruleOfNumber 170) x i = x (i + 1)

/-- A check of the definition of `kIndex`, for every `n ≥ 1` (so also where `D_v` is empty): the subtraction in `k_v = min_C [...] - γ_min` is a subtraction
of natural numbers and is exact, because the minimum is at least `γ_min`. -/
def KIndex_subtraction_exact : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule) (v : Code),
    gammaMin (VE n f) ≤
      sInf (Set.range fun C : Cyc (globalMap n f) => gamma (VE n f) C + R (resistance n f) C.1 (D n v))

/-- Paper, Lemma 2.2, for `n ≥ 3` as in the paper: "`k_v = 0` iff `v` is contained in a state of a
noise-selected cycle. Hence `k* = 0` iff the states of the noise-selected cycles jointly contain all eight
codes; and `k_v ≤ 1` if some flip of some state of a noise-selected cycle contains `v`." -/
def Lemma_2_2 : Prop :=
  ∀ (n : ℕ) [NeZero n], 3 ≤ n → ∀ (f : LocalRule),
    (∀ v : Code, kIndex n f v = 0 ↔ ∃ C ∈ Sel (VE n f), ∃ x ∈ C.1, Contains n x v) ∧
    (kStar n f = 0 ↔ ∀ v : Code, ∃ C ∈ Sel (VE n f), ∃ x ∈ C.1, Contains n x v) ∧
    (∀ v : Code, (∃ C ∈ Sel (VE n f), ∃ x ∈ C.1, ∃ j, Contains n (flip n x j) v) → kIndex n f v ≤ 1)

/-- Paper, Lemma 2.3: "For cycles `C ≠ C'`: `V(C, C') ≥ 1`, and `V(C, C') = 1` iff there are a state `x` of
`C` and a cell `j` such that the orbit of `x + e_j` ends on `C'`. In particular, if `x` and `x + e_j` are
periodic and lie on different cycles `C` and `C'`, then `C → C'` and `C' → C` are edges of `G_1`." -/
def Lemma_2_3 : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule) (C C' : Cyc (globalMap n f)), C ≠ C' →
    1 ≤ VE n f C C' ∧
    (VE n f C C' = 1 ↔ ∃ x ∈ C.1, ∃ j, EndsOn (globalMap n f) (flip n x j) C') ∧
    (∀ x ∈ C.1, ∀ j, flip n x j ∈ C'.1 → G1 (VE n f) C C' ∧ G1 (VE n f) C' C)

/-- Paper, Lemmas 2.5, 2.6, 2.7 and Theorem 2.8 as the paper states them, for the cycles of an elementary rule
`f` on a ring of `n` cells. These are the general statements `Lemma_2_5`, `Lemma_2_6`, `Lemma_2_7` and
`Theorem_2_8` with `F = globalMap n f` and `r = resistance n f`; the five parts are, in this order: Lemma 2.5,
Lemma 2.6, Lemma 2.7, and the two sentences of Theorem 2.8. -/
def Section_2_4_ECA : Prop :=
  ∀ (n : ℕ) [NeZero n] (f : LocalRule),
    (∀ (B N : Cyc (globalMap n f)) (p : Cyc (globalMap n f) → Cyc (globalMap n f)), IsInTree B p → N ≠ B →
      IsInTree N (update p B N) ∧
      (VE n f B N = 1 → treeWeight (VE n f) N (update p B N) ≤ treeWeight (VE n f) B p)) ∧
    (∀ C C' : Cyc (globalMap n f), C ∈ Sel (VE n f) → VE n f C C' = 1 → C' ∈ Sel (VE n f)) ∧
    (∀ C : Cyc (globalMap n f), C ∈ Sel (VE n f) → ∃ K, IsClosedClass (VE n f) K ∧ C ∈ K) ∧
    (∀ C ∈ Sel (VE n f), ∃ K, IsClosedClass (VE n f) K ∧ C ∈ K ∧ K ⊆ Sel (VE n f)) ∧
    (∀ K, IsClosedClass (VE n f) K → (∀ K', IsClosedClass (VE n f) K' → K' = K) →
      Sel (VE n f) = K ∧ gammaMin (VE n f) = numCycles (globalMap n f) - 1)

/-- Paper, the sentence after the proof of Theorem 2.8 (it has no number in the paper): "if `G_1` has a unique
closed class `K`, then `k* = 0` iff the states of the cycles of `K` jointly contain all eight codes."
(For `n ≥ 3`.) -/
def KStar_unique_class : Prop :=
  ∀ (n : ℕ) [NeZero n], 3 ≤ n → ∀ (f : LocalRule) (K : Set (Cyc (globalMap n f))),
    IsClosedClass (VE n f) K → (∀ K', IsClosedClass (VE n f) K' → K' = K) →
      (kStar n f = 0 ↔ ∀ v : Code, ∃ C ∈ K, ∃ x ∈ C.1, Contains n x v)

end RingSize.TheoremA

end
