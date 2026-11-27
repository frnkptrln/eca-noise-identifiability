# Lean pilot: rule 90 and powers of two

This folder is a Lake project that checks one theorem of `paper/ring_size_paper.tex` in Lean 4 with Mathlib.
It is the first result in this repository that is checked by a proof assistant
rather than by Claude sessions checking each other.

## The theorem

**In words.** Let n ≥ 1 and consider a ring of n cells, indexed by ℤ/nℤ, with one bit (an element of GF(2)) per
cell. Rule 90 is the map A with (A x)_i = x_(i−1) + x_(i+1), indices mod n, sum mod 2. Let e_i be the state with a
single 1, at cell i. Then: for every cell i there is a t ≥ 0 with A^t(e_i) = 0 **if and only if** n = 2^k for
some k ≥ 0.

**In Lean** (`RingSize/Statement.lean`, everything except the `module`/import header, the file comment and the namespace/section lines):

```lean
/-- A state of the ring of `n` cells: one bit per cell. -/
abbrev State (n : ℕ) := ZMod n → ZMod 2

/-- One step of rule 90, the map `A`: the new value of cell `i` is
`x (i - 1) + x (i + 1)`, computed in `ZMod 2`. -/
def rule90 (n : ℕ) (x : State n) : State n :=
  fun i => x (i - 1) + x (i + 1)

/-- `e n i` is the indicator of cell `i`: the state with a single 1, at cell `i`. -/
def e (n : ℕ) (i : ZMod n) : State n :=
  fun j => if j = i then 1 else 0

/-- **Main theorem.** For `n ≥ 1`: the orbit under rule 90 of every single-1 state
reaches the zero state if and only if `n` is a power of two.
Here `(rule90 n)^[t]` is the `t`-fold iterate `A^t`, and `0` is the all-zero state. -/
def MainTheorem : Prop :=
  ∀ n : ℕ, 1 ≤ n →
    ((∀ i : ZMod n, ∃ t : ℕ, (rule90 n)^[t] (e n i) = 0) ↔ ∃ k : ℕ, n = 2 ^ k)
```

`(rule90 n)^[t]` is Mathlib's notation for the t-fold iterate `Nat.iterate`, so it is A^t.
The cells are `ZMod n` and the bits are `ZMod 2`, exactly as in the statement above; no other type is used,
so no transfer to an equivalent type was needed. `Statement.lean` imports only `Mathlib.Data.ZMod.Defs`.
The proof is `RingSize.mainTheorem : RingSize.MainTheorem` in `RingSize/Proof.lean`; `AxiomCheck.lean` checks that
it has exactly this type.

Files:

| File | Content |
|---|---|
| `RingSize/Statement.lean` | definitions `State`, `rule90`, `e` and the statement `MainTheorem` (40 lines, no proofs) |
| `RingSize/Iterate.lean` | `iterate_two_pow`: A^(2^j) x i = x(i − 2^j) + x(i + 2^j) for every state x |
| `RingSize/Proof.lean` | both directions, `main_all_n`, `mainTheorem`, and the extra lemma `iterate_half_eq_zero` |
| `RingSize.lean` | library root, imports the three files |
| `AxiomCheck.lean` | `#check` of the type of `mainTheorem` and `#print axioms` |
| `lakefile.lean`, `lean-toolchain`, `lake-manifest.json` | Lake configuration and pinned versions |

**Proof.** `iterate_two_pow` is proved by induction on j for all states at once: A^(2^(j+1)) x = A^(2^j)(A^(2^j) x),
and the middle terms cancel because b + b = 0 in GF(2). No linear algebra, no shift operator and no polynomials are
needed. If n = 2^k, then A^n x i = x(i − n) + x(i + n) = x i + x i = 0 for every state x. Conversely, if
A^t(e_0) = 0, then A^(2^t)(e_0) = 0 as well, because t ≤ 2^t and the zero state is fixed. Evaluating at cell 2^t gives
e_0(2^(t+1)) = 1, so n divides 2^(t+1), so n is a power of two (Mathlib's `Nat.dvd_prime_pow`).

Two by-products:

* `main_all_n` proves the equivalence without the hypothesis 1 ≤ n. For n = 0, `ZMod 0 = ℤ` is the infinite line
  and both sides are false.
* `iterate_half_eq_zero`: on 2^(k+1) cells, already A^(2^k) = 0. This is the form used for rule 154,
  Lemma 3.4(a) of the paper. The converse direction above is Lemma 3.4(b) for e_0. Translating it to every e_j needs
  only the rotation symmetry, which is not yet formalized.

**Rules kept.** There is no `sorry`, no `admit`, no `axiom`, no `native_decide` and no `decide` in the sources
(checked with `grep`). The output of `lake env lean -j2 AxiomCheck.lean` is:

```
RingSize.mainTheorem : RingSize.MainTheorem
'RingSize.mainTheorem' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Build

Prerequisite: elan, the Lean toolchain manager. Install it once with
`curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh -s -- -y --default-toolchain none`.
elan reads `lean-toolchain` and downloads Lean 4.36.0 by itself.

```sh
cd lean
export LEAN_NUM_THREADS=2 RAYON_NUM_THREADS=2   # machine load, see below
lake exe cache get        # clones Mathlib and its dependencies, then downloads prebuilt Mathlib (no Mathlib build)
lake build                # builds the 3 project files
lake env lean -j2 AxiomCheck.lean
```

`lake build` must not start compiling Mathlib files. With the cache in place, it prints only the three
`RingSize.*` modules as built; the other jobs are replayed.

### Versions

| Component | Version |
|---|---|
| elan | 4.4.0 (3cc76985a 2026-11-18) |
| Lean | 4.36.0, commit 611c117bfaf7, `leanprover/lean4:v4.36.0` (pinned in `lean-toolchain`) |
| Lake | 5.0.0-src+611c117 (ships with Lean 4.36.0) |
| Mathlib | release tag `v4.36.0` = `fc4f59e577feb1a4956671bc04ac18aaaf8cd842` (pinned in `lakefile.lean`) |

Dependencies, as resolved in `lake-manifest.json` (input revision, resolved commit):

| Package | Input | Commit |
|---|---|---|
| mathlib | `v4.36.0` | `fc4f59e577fe` |
| plausible | `main` | `054b228ce0ac` |
| LeanSearchClient | `main` | `4fb58e749ef3` |
| importGraph | `main` | `8370c640afcd` |
| proofwidgets | `main` | `2f0f3520daea` |
| aesop | `master` | `66ff77cf0c4c` |
| Qq | `master` | `ff055a2fcc83` |
| batteries | `main` | `b4b25a3886a1` |
| Cli | `v4.36.0` | `50810f72af76` |

Deleting `lake-manifest.json` and running `lake update` was tested: it regenerated a byte-identical manifest.
The pin is therefore fully determined by `lakefile.lean` and `lean-toolchain`.

### Machine load: 2 threads

Read in the documentation and sources shipped with the installed toolchain and Mathlib, and measured:

* **Lake** is a Lean program. The Lean runtime sizes its task-manager thread pool from the environment variable
  `LEAN_NUM_THREADS`, falling back to the number of hardware threads (`get_lean_num_threads` in
  `src/runtime/object.cpp` of v4.36.0; the string is present in the installed `libleanshared.dylib`).
  Lake 5.0 has no `-j` option. Measured: the `lake build` process had at most 7 OS threads with
  `LEAN_NUM_THREADS=2` and 17 without it.
* **`lean`** ignores `LEAN_NUM_THREADS`: it sizes its pool from its own `-j/--threads` option (`lean --help`), whose
  default is the number of hardware threads. Measured on `RingSize/Proof.lean`: 13 OS threads with
  `LEAN_NUM_THREADS=2`, 11 without, 5 with `-j2`. So `lakefile.lean` sets `weakLeanArgs := #["-j2"]` on the library.
  `weakLeanArgs` are documented in Lake's README; unlike `moreLeanArgs`, they do not enter the build trace.
  `lake build -v` shows `lean -j2 …/RingSize/Proof.lean`. For a hand-run file, pass `-j2` yourself, as above.
* **`lake exe cache get`** downloads with one `curl` process. `MATHLIB_CACHE_PARALLEL_MAX` (default 50) is the number
  of simultaneous transfers, which is network load, not threads. Decompression is done by `leantar`, which uses the
  Rayon thread pool: the binary contains Rayon's `RAYON_NUM_THREADS` hook. Hence `RAYON_NUM_THREADS=2`.
  This setting was not measured separately. The whole `cache get` took 68.8 s wall time and 133 s CPU time
  (user + sys), on average 1.9 cores.

OS thread counts include a few threads that are not workers (main thread, I/O), so "2 threads" means 2 worker threads.
Not measured: how many `lean` processes Lake runs in parallel under `LEAN_NUM_THREADS=2`, because the sandbox cannot
list grandchild processes. For this project it does not matter: the three modules depend on each other in a chain and
compile one after the other.

### Wall time and disk space

Measured on this laptop (Apple Silicon, 12 cores) in the Claude Science sandbox, with the limits above:

| Step | Wall time |
|---|---|
| `elan toolchain install leanprover/lean4:v4.36.0` | 38 s |
| Clean build from a fresh copy of the sources, with no `.lake` and an empty download cache: dependency clones + `lake exe cache get` (9117 files) | 107 s |
| then `lake build` (3 project files) | 5 s |
| **total clean build with the Mathlib cache** | **112 s** |
| `lake build` of the project alone, after `rm -rf .lake/build` | 3.9 s |

The download times depend on the network. In the sandbox, the clean build also included a workaround that does not
apply on a normal terminal: the sandbox forbids creating `.vscode` and `.devcontainer` directories, so the dependency
clones were checked out sparsely, without those directories.

| Item | Disk |
|---|---|
| Lean toolchain 4.36.0 (elan home; elan itself is 5.7 MB) | 3.0 GB |
| `lean/.lake` (git clones of the 9 dependencies plus unpacked Mathlib build) | 7.3 GB, of which Mathlib's build output is 6.7 GB |
| Mathlib download cache (`.ltar` archives; default `~/.cache/mathlib`, may be deleted afterwards) | 457 MB |
| **total** | **about 10.8 GB** |

## Cost and outlook

### How long this took

About 50 minutes of wall-clock time, from installing elan to this README, in one Claude session. Approximate split,
from file timestamps:

| Part | Time |
|---|---|
| Toolchain install, including three network-allowlist approvals in the sandbox | ~5 min |
| Dependency checkout blocked by the sandbox (`.vscode`/`.devcontainer`) and the sparse-checkout workaround | ~5 min |
| Mathlib cache download | ~1 min |
| Writing statement and proofs | ~5 min (the first build had no errors) |
| Converting to Lean's module system (removes the build warnings; two missing imports to fix) | ~3 min |
| Finding and verifying the 2-thread limits | ~10 min |
| Clean-build timing, manifest check, extra lemma | ~6 min |
| README and the outlook below | ~12 min |

The mathematics cost almost nothing. The infrastructure (sandbox, thread limits, measurements) took most of the time.
This is not representative of the theorems in (a) and (b) below: the proof here is about ten lines on paper
and needs no combinatorics.

### What in Mathlib helped, and what was missing

Used: `ZMod n` as a commutative ring with decidable equality (so `i - 1`, `i + 1` and `if j = i` work as written);
`Function.iterate_add_apply` and `Function.iterate_fixed`; `ZMod.natCast_self`; `CharP.cast_eq_zero_iff`;
`CharTwo.add_self_eq_zero`; `Nat.dvd_prime_pow`; `Nat.lt_two_pow_self`; the tactics `ring`, `linear_combination`,
`push_cast`, `omega`, `simp`.

Missing: nothing for this theorem. The polynomial route of the paper, with GF(2)[z]/(z^n + 1) and the factorization
of z^q + 1, would have needed considerably more (`AdjoinRoot`, divisibility in `Polynomial (ZMod 2)`, irreducible
factors). The pointwise induction avoids it. Mathlib has no cellular automata, no notion of a stochastic potential or
spanning in-tree (arborescence), and only a thin directed-graph layer (`Digraph`, `Quiver` paths, `Relation.ReflTransGen`
for reachability). These are the gaps that matter for (a) and (b).

Practical note: with Lean 4.36 the files are in the new module system (`module`, `public import`, `@[expose]`). An
`import` there is not re-exported, so each file must import what it uses itself. This cost two rebuilds.

### Estimates for further formalization

*All numbers in this subsection are estimates, not measurements*, with wide uncertainty. They assume the same
working mode (a Claude session writing Lean with the compiler in the loop, Frank reviewing the statement file).
For orientation: this pilot is 193 lines of Lean, comments included.

**(a) Definitions of resistance, the one-flip graph, the stochastic potential and k\*, with Theorem 2.8 (Theorem A).**

* Definitions, roughly 150–300 lines. These are: global map of an elementary rule; resistance r(x, y) = H(Fx, y);
  path resistance and R(A → B) as a minimum over paths (well defined via `Nat.find`, or as a shortest path in a finite
  graph); cycles as orbits of periodic states (Mathlib's `Function.periodicPts` and `minimalPeriod` help); V(C, C′);
  spanning in-trees, best defined as a parent map on the non-root cycles whose iterates reach the root, which avoids
  general graph theory; γ, γ_min, the selected set; k_v and k\*; G1 and closed classes. Defining a closed class
  directly (nonempty, closed under G1 edges, mutually reachable) avoids strongly-connected-component machinery.
  The statement file would be longer than here, perhaps 80–150 lines. Reviewing that these definitions match the
  paper is the part that needs a mathematician.
* Lemma 2.3 (edges of G1: a resistance-1 path has exactly one flip step): 100–200 lines.
* Lemmas 2.5–2.7 and Theorem A (re-rooting in-trees, absence of circuits, the induction along a G1 path in Lemma 2.7):
  300–600 lines. This is the riskiest part: arguments about finite trees that take five lines on paper are often
  ten times longer in Lean.
* Theorem A does not use the structure of elementary rules. It holds for any map F on a finite set with a
  resistance that vanishes exactly on the steps of F. Proving it at that generality is no harder and makes it reusable.
* Total for (a): about 500–1,000 lines, about 1–3 working days of sessions.

**(b) Rule 154: k\* = 1 iff n is a power of two**, on top of (a):

* Already available from this pilot: the rule-90 iterate formula, Lemma 3.4(a) (`iterate_half_eq_zero`) and
  Lemma 3.4(b) for e_0. Still needed for (b): the rotation symmetry, for e_j and for Lemma 2.4.
* Local form (Lemma 3.2, a finite check over 8 codes), the parity classes E, O, M and Lemma 3.3: about 100–200 lines.
* Invariance of M (Lemma 3.5) and the collision lemma (Lemma 3.6): about 300–600 lines. The collision lemma is a case
  analysis that propagates along the cells i + 2s of an even ring. Arithmetic with parities in `ZMod n` is fiddly in
  Lean, and this is probably the longest single proof.
* Periodic states and one-flip moves (Lemmas 3.7, 3.8): about 150–300 lines (injective self-map of a finite set
  is a permutation: in Mathlib).
* Theorem 3.9 (n = 2^k: the in-tree of weight m − 1, γ(C) = m, and the seven codes with k_v = 1 via explicit states),
  Theorem 3.10 (other n: strong connectivity of G1 for odd and even n, and the eight codes on explicit periodic states
  such as 0^(n−2)11 for general n): about 600–1,200 lines.
* Total for (b): about 1,200–2,500 lines beyond (a), about 1–2 weeks of sessions. A sensible first milestone is
  Theorem 3.9(b) alone: no edge of G1 leaves 0 when n is a power of two. It needs only Lemma 3.3, this pilot and
  Lemma 2.3.

### What I think is not worth formalizing

My reading covered sections 2 and 3.1 in full; for the other sections the judgement rests on their headings and
lengths.

* Proposition 2.1, the small-noise asymptotics of π_ε cited from the earlier note. It is used only to interpret k\*,
  and it would need Markov chains, the Markov chain tree theorem and asymptotics in ε. That is weeks of work for a
  statement the paper does not rely on.
* The computed table (Table 1), the figures and the data files. Checking values for single n by proof would need
  evaluation over 2^n states, which plain `decide` cannot do at these sizes, and `native_decide` is excluded by the
  rules of this pilot. Independent re-computation by separate code checks them better and more cheaply.
* The related-work and attribution sections, and the healing-time proposition for rules 43/142 unless a later
  result depends on it.
* Rules 94 and 26 only after (a) and (b). Their proofs are long combinatorial case analyses (the rule-94 appendix
  alone is about 500 lines of TeX), so the cost per theorem is highest there. They are also the proofs that have so
  far only been checked by Claude sessions, so the formal check would add the most there. That is a decision for
  Frank, not a technical one.

## What was done and what was not

Done:

* Lake project with pinned toolchain and Mathlib.
* Statement file, proof files and the axiom check; the build passes with no errors and no warnings.
* Thread limits read from the documentation and sources, and measured.
* Clean-build wall time and disk space measured.
* `.gitignore` gets `lean/.lake/`.

Not done:

* **No git branch or commit.** The repository is read-only to code in the Claude Science sandbox, so the branch
  `lean-pilot` could not be created. The files were placed in the working tree of the checked-out branch `main`,
  uncommitted. Commands for Frank are in the session report; nothing was pushed.
* elan was installed into the Claude Science workspace, not into Frank's home directory. Whether elan is already
  installed there could not be checked: the sandbox denies access to `~/.elan` ("Operation not permitted").
  So the build has not yet been run from Frank's own terminal.
* The concurrency of Lake's `lean` processes under `LEAN_NUM_THREADS=2` and the effect of `RAYON_NUM_THREADS` were
  not measured (see above).

## Independent build (25 November 2026)

Written by Claude, the reader outside the sessions (the conversation in which the pilot was planned).

* **How the files got here.** The session's sandbox could write only this README into the repository. The other
  eight files were taken from the session's archive and placed here by the reader; the author committed them
  (fe08456) and added `lean/.lake/` to `.gitignore`. Two statements above therefore describe what the session
  intended, not what happened: "The files were placed in the working tree" and "`.gitignore` gets `lean/.lake/`".
* **Built again in a separate environment** (Linux x86_64 container, 2 cores, `LEAN_NUM_THREADS=2`). Lean 4.36.0,
  commit 611c117bfaf7, from the release archive `lean-4.36.0-linux.tar.zst` on GitHub; Mathlib at fc4f59e577fe with
  the dependencies of `lake-manifest.json`. The Mathlib cache was not reachable from there, so `lake build`
  compiled from source the part of Mathlib that the project imports: 2462 jobs, under 15 minutes, no error and no
  warning. `.lake` took 1.7 GB.
* **Axioms.** `lake env lean -j2 AxiomCheck.lean` printed the two lines quoted above, word for word.
* **Sources.** None of `sorry`, `admit`, `native_decide`, `decide`, `axiom`, `unsafe`, `implemented_by`, `extern`
  occurs in the Lean files (grep). The files that were built are byte-identical to the committed ones (md5).
* **Read.** The reader read `RingSize/Statement.lean` against the statement in the task of the pilot, and the two
  proof files.
* **Not done.** A build on macOS from the author's own terminal; a build with the Mathlib cache outside the
  session.

Claude

## Section 2 of the paper: definitions, Lemmas 2.2, 2.3, 2.5 to 2.7 and Theorem 2.8 (26 November 2026)

Written by Claude, the reader outside the sessions, who also wrote this part of the Lean code, in the conversation
in which the work is planned. It was not written by a Claude Science session: the session started for it could not
install Lean in its sandbox.

**The proofs are checked by Lean. The statement file was read against the paper by an independent session**
(`VERIFICATION_lean_theorem_a.md`, on commit 3425cc7): it found no statement that differs from the paper or is
weaker, one difference that had to be stated (values at n ≤ 2, item 4 below) and seven points of wording and
missing checks. They are worked in here; what was changed is listed at the top of that file. The changes made
afterwards (four new statements, one renamed, comments) were checked by Lean and were not read by a second reader.

### What is proved

`RingSize/TheoremA/Statement.lean` (362 lines, definitions and statements only) has three parts:

1. a finite set of nodes with weights `V a b`: in-trees, the stochastic potential `gamma`, the selected set `Sel`,
   the one-flip graph `G1`, closed classes;
2. a map `F` on a finite set of states with a resistance `r` such that `r x y = 0` iff `y = F x`: paths, `R(A → B)`,
   cycles, and `V(C, C') = R(C → C')` between cycles;
3. elementary cellular automata on a ring of `n` cells: rule numbers, the global map, `r(x, y) = H(F x, y)`,
   codes, `k_v` and `k*`.

Each statement is a `Prop`-valued definition, and a theorem of that type is proved in the other files:

| Statement in `Statement.lean` | Paper | Proved in |
|---|---|---|
| `EndsOnExactlyOneCycle` | 2.2, "the orbit of every state enters exactly one cycle" | `Paths.lean` |
| `Lemma_2_3_general` | not a statement of the paper: the content of Lemma 2.3 without the flips (`V(C, C') ≥ 1`; `V = 1` iff one step of resistance 1 leads from `C` to a state whose orbit ends on `C'`) | `Paths.lean` |
| `Lemma_2_5` | Lemma 2.5 (re-rooting), for every `F`, `r` of part 2 | `Trees.lean`, `Paths.lean` |
| `Lemma_2_6` | Lemma 2.6 (closure), for every `F`, `r` of part 2 | `Trees.lean`, `Paths.lean` |
| `ClosedClassReachable` | 2.4, "from every node there is a directed path into some closed class" | `Trees.lean` |
| `Lemma_2_7` | Lemma 2.7, for every `F`, `r` of part 2 | `Trees.lean`, `Paths.lean` |
| `Theorem_2_8` | Theorem 2.8 (Theorem A), both sentences, with `γ_min = m - 1`, for every `F`, `r` of part 2 | `Trees.lean`, `Paths.lean` |
| `TreeWeight_lower_bound` | proof of Theorem 2.8, "every in-tree has weight at least `m - 1`" | `Trees.lean`, `Checks.lean` |
| `ResistanceECA` | 2.2, "a step has resistance 0 iff it is a step of `F`", for `r = H(F x, y)` | `ECA.lean` |
| `Section_2_4_ECA` | Lemmas 2.5, 2.6, 2.7 and Theorem 2.8 as the paper states them, for an elementary rule on a ring of `n` cells | `Checks.lean` |
| `Lemma_2_2` | Lemma 2.2, all three parts, for `n ≥ 3` | `ECA.lean` |
| `Lemma_2_3` | Lemma 2.3 as in the paper, with flips, both sentences | `ECA.lean` |
| `KStar_unique_class` | the sentence after the proof of Theorem 2.8 (no number in the paper): with a unique closed class `K`, `k* = 0` iff the states of the cycles of `K` contain all eight codes; for `n ≥ 3` | `ECA.lean` |

Lemmas 2.5 to 2.7 and Theorem 2.8 are proved for every finite weighted graph with `V a b ≥ 1` for `a ≠ b`
(`Trees.lean`), then for every `F` and `r` as in part 2. `Section_2_4_ECA` is their application to
`globalMap n f` and `resistance n f`, which satisfy the hypothesis by `ResistanceECA`. The proofs do not use the
structure of an elementary rule, as the session of the pilot expected.

Checks of the definitions, also stated in `Statement.lean` and proved in `Checks.lean` and `ECA.lean`:

* `InTree_iff_reaches`, `ClosedClass_iff_component`, `Gamma_lower_bound`, `KIndex_subtraction_exact`;
* `Rule204_cycles` and `Rule90IsRuleNumber90` (the map `rule90` of the pilot is the global map of rule number 90).
  Rules 90 and 204 are their own mirror images, so these two do not test the orientation of the neighbourhood;
* `Rule154_local` (rule 154 is `f(a, b, c) = c + a (1 + b)`, as in Lemma 3.2 of the paper) and `Rule170_shift`
  (under rule 170, `(F x)_i = x_{i+1}`). These two fail if left and right are exchanged in `ruleOfNumber` or in
  `globalMap`. `Rule170_shift` alone would not notice it if both were mirrored at once; `Rule154_local` excludes
  that. The other statements do not depend on the orientation: they hold equally for the mirror image of the
  rule (both verification reports note this). The two checks make sure that a rule number in Lean names the rule
  of the paper.

### Differences from the paper

1. **In-trees.** The paper's tree is a set of `m - 1` edges, one out of every cycle other than the root, without
   directed circuit. Here it is a parent map `p` on all nodes; the edges are `d → p d` for `d` other than the root,
   and the value of `p` at the root is ignored. "Without directed circuit" is the condition of `IsInTree`.
   `InTree_iff_reaches` proves it equivalent to: every node reaches the root along `p`. Re-rooting at `N` (Lemma
   2.5) becomes `Function.update p B N` with root `N`.
2. **Closed classes.** The paper says "a strongly connected component of `G_1` that no edge of `G_1` leaves".
   `IsClosedClass` says: non-empty, any two nodes joined by directed paths both ways, no edge leaves.
   `ClosedClass_iff_component` proves the two equivalent.
3. **Generality.** `Lemma_2_3_general`, `Lemma_2_5`, `Lemma_2_6`, `Lemma_2_7`, `Theorem_2_8`,
   `TreeWeight_lower_bound` and `Gamma_lower_bound` are stated for any map on a finite set with a resistance that
   vanishes exactly on the steps of the map (`IsResistance`). The paper states them for elementary rules; that form
   is `Section_2_4_ECA`.
4. **Ring size.** The paper fixes `n ≥ 3` and defines `D_v`, `R(C → D_v)`, `k_v` and `k*` only there. The Lean
   definitions exist for every `n ≥ 1`. For `n ≤ 2` some codes occur in no state (for `n = 1` only 000 and 111
   occur, for `n = 2` only 000, 010, 101, 111). For such a code `D_v` is empty and **`kIndex` gives the value 0,
   where the paper defines nothing**; so `kStar` at `n ≤ 2` treats a code that cannot occur like a code with
   `k_v = 0`. `Lemma_2_2` and `KStar_unique_class` assume `n ≥ 3` and are false without it (rule 204, `n = 2`,
   code 100). All other statements of part 3 are stated and proved for every `n ≥ 1`: `ResistanceECA`,
   `Lemma_2_3`, `Section_2_4_ECA`, `Rule90IsRuleNumber90`, `Rule204_cycles`, `Rule170_shift` and
   `KIndex_subtraction_exact`.
5. **`R` of an empty set.** `R A B` is an infimum over paths, and the infimum of the empty set of natural numbers
   is `0` in Mathlib. Cycles are never empty. `D_v` is empty exactly in the case of item 4, and there
   `KIndex_subtraction_exact` uses `R` of an empty set (it still holds: `γ_min ≤ min_C γ(C)`).
6. **Subtraction.** `k_v` is defined with the subtraction of natural numbers; `KIndex_subtraction_exact` proves
   that nothing is cut off.
7. **The empty graph.** The paper says in 2.4: "Every finite directed graph has a closed class, and from every
   node there is a directed path into some closed class." The first half is false for the graph without nodes.
   `ClosedClassReachable` states the second half, which gives the first for every graph with a node. The graphs
   of the paper have at least one cycle as a node. The paper is not changed for this.
8. **Proofs.** The proof of Lemma 2.7 re-roots along one path of `G_1` from `C` to `D` and stops at the first visit
   of `D`, by induction along the path, instead of taking paths without repeated node as the paper does. The tree
   of weight `m - 1` in Theorem 2.8 is built from the sets of nodes that reach the root in at most `k` steps.

No statement of the paper had to be changed in content, and no gap was found in the proofs of the statements
listed above.

### Not formalized

* The noisy chain of 2.2 (its kernel, positivity, uniqueness and full support of the stationary distribution),
  the quantities `ν_v` and `ρ`, and Proposition 2.1, which links them to the integers above; as planned.
* Not part of this step, and formalized in the next section: Lemma 2.4 (invariance under rotation) with the
  remark `F σ = σ F` of 2.1, and Stage 4 of the plan (rule 154: no edge of `G_1` leaves `{0}` when `n` is a power
  of two).

### Build and axioms

Built in the environment of the independent build above (Lean 4.36.0, commit 611c117bfaf7; Mathlib at fc4f59e577fe;
no Mathlib cache there, so the imported part of Mathlib was compiled from source): `lake build` completed 3056 jobs
without error or warning. `lake env lean -j2 AxiomCheckTheoremA.lean` checks the type of each of the 21 theorems
against its statement and prints their axioms: 20 depend on `propext`, `Classical.choice`, `Quot.sound`, and
`closedClass_iff_component` on `propext`, `Quot.sound`. The sources contain no `sorry`, `admit`, `native_decide`,
`axiom`, `unsafe`, `implemented_by` or `extern`. `decide` is used six times, for statements about all elements of
`ZMod 2` (the tables of rules 90, 154, 170 and 204 and two facts of arithmetic mod 2).

Not done: a build with the Mathlib cache, and a build on macOS.

### Cost

1381 lines of Lean in five files, of which 362 are definitions and statements. The estimate of the pilot for this
part was 500 to 1,000 lines and one to three working days of sessions; the lines are above the estimate, the time
was below it (one conversation; not measured more exactly).

Claude

## Lemma 2.4 and rule 154 on rings of 2^k cells: Lemmas 3.3, 3.4(a), Theorem 3.9(b) (26 November 2026)

Written by Claude, the reader outside the sessions, who also wrote this part of the Lean code.

**The proofs are checked by Lean. The two statement files were read against the paper by an independent session**
(`VERIFICATION_lean_rule154.md`, on commit cf6f77e): no statement differs from the paper or is weaker; six points
of wording. They are worked in here; what was changed is listed at the top of that file. One clause was added to
`Lemma_2_4_general` and `Lemma_2_4` afterwards (every cycle is the image of a cycle); it was checked by Lean and
not read by a second reader.

### What is proved

Statements only: `RingSize/TheoremA/StatementRotation.lean` (78 lines) and `RingSize/Rule154/Statement.lean`
(81 lines). Proofs: `RingSize/TheoremA/Rotation.lean` and `RingSize/Rule154/Pow2.lean`.

| Statement | Paper | Proved in |
|---|---|---|
| `Lemma_2_4_general` | Lemma 2.4 for any bijection of the states that commutes with `F` and preserves the resistance: the image of a cycle is a cycle; every cycle is such an image; `V`, `γ`, membership in `S` and the edges of `G_1` are preserved | `Rotation.lean` |
| `GlobalMap_rot` | 2.1, "`F σ = σ F`" | `Rotation.lean` |
| `Resistance_rot` | proof of Lemma 2.4, "`r(σ x, σ y) = r(x, y)`" | `Rotation.lean` |
| `Lemma_2_4` | Lemma 2.4 for an elementary rule and the rotation `(σ x)_i = x_{i-1}` | `Rotation.lean` |
| `Zero_cycle` | 3.1: `{0}` is a cycle of rule 154 | `Pow2.lean` |
| `Lemma_3_3` | Lemma 3.3 (rule 154 acts as rule 90 on the parity classes `E`, `O`), for every even `n ≥ 2` | `Pow2.lean` |
| `Lemma_3_4_a` | Lemma 3.4(a): `F^(n/2) x = 0` for `x ∈ E ∪ O`, for `n = 2^(k+1)`, `k ≥ 0` | `Pow2.lean` |
| `Single_mem` | proof of Theorem 3.9(b), "the state `e_j` lies in `E ∪ O`" | `Pow2.lean` |
| `Theorem_3_9_b` | Theorem 3.9(b): `V({0}, C) ≥ 2` for every cycle `C ≠ {0}`, and no edge of `G_1` leaves `{0}`, for `n = 2^(k+1)`, `k ≥ 0` | `Pow2.lean` |

Lemma 3.2 (the local form of rule 154) is `Rule154_local` of the part above. `Lemma_3_4_a` uses the theorem
`iterate_half_eq_zero` of the pilot (`RingSize/Proof.lean`): on a ring of `2^(k+1)` cells, `2^k` steps of rule 90
send every state to zero.

### Differences from the paper

1. **`σC` as a cycle.** In Lean a cycle is a set together with a proof that it is a cycle. `Lemma_2_4` and
   `Lemma_2_4_general` therefore speak of cycles `D`, `D'` whose sets are the images of the sets of `C`, `C'`, and
   a first clause says that the image of a cycle is a cycle, so such `D`, `D'` exist.
2. **"Hence `S` and `G_1` are invariant under rotation."** Stated as: `σC ∈ S` iff `C ∈ S`, and `σC → σC'` is an
   edge of `G_1` iff `C → C'` is. A further clause says that every cycle is the image of a cycle. Since `σ` is
   injective, `C ↦ σC` is then a bijection of the set of cycles, so these clauses give `σ(S) = S` as sets and say
   that `C ↦ σC` is an automorphism of `G_1`.
3. **Parity of a cell.** `E` and `O` are defined for every `n` through the representative of a cell in
   `{0, …, n - 1}` (`ZMod.val`). The paper defines them for even `n`, and all statements here that use them
   assume `n` even, except `Single_mem`, which holds for every `n` with this definition.
4. **Ring sizes.** The paper states Lemma 3.3 for even `n ≥ 4` and Lemma 3.4(a) and Theorem 3.9 for `n = 2^k`,
   `k ≥ 2`. The Lean statements include `n = 2`; they are true there (for `n = 2` the cycles of rule 154 are `{00}`
   and `{11}`, and `V({00}, {11}) = 2`). `Theorem_3_9_b` is false for `n = 1`, which is excluded.
   The Lean statements write `n = 2^(k+1)` with `k ≥ 0`, so their `k` is the paper's `k - 1`.
   The paper fixes `n ≥ 3` in Section 2; `GlobalMap_rot`, `Resistance_rot`, `Lemma_2_4` and `Zero_cycle` are
   stated for every `n ≥ 1`, and `Single_mem` for every `n`.
5. **Proof of Theorem 3.9(b).** The paper uses part (a) of the theorem (the list of the cycles, from Lemma 3.7)
   to conclude that no state of the orbit of `e_j` lies on a cycle other than `{0}`. The Lean proof does not use
   it: a cycle that contains a state of the orbit contains all later states of the orbit, hence `0`, and two
   cycles with a common state are equal. So part (b) depends only on Lemmas 2.3, 3.2 and 3.4(a) (which rests
   on 3.3), on `e_j ∈ E ∪ O`, on `F(0) = 0`, and on the fact that cycles are invariant under `F` and pairwise
   disjoint (paper, 2.2: "the orbit of every state enters exactly one cycle"). The independent session checked
   this argument on paper and found it valid; the paper's proof is correct too and uses more than it needs.
6. **Proof of Lemma 3.3.** One statement covers both parity classes: if `x` vanishes on the cells of parity `c`,
   then `F x = L x` and `F x` vanishes on the cells of parity `c + 1`.

No gap or false statement was found in the paper for these statements.

### Check outside Lean

A separate Python computation from the definitions (`reader_checks/lean_rule154/check.py`, output in `out.txt`
there) gives, for rule 154, the least
`V({0}, C)` over the cycles `C ≠ {0}`: 2 at `n = 2, 4, 8` and 1 at `n = 1, 3, 5, 6`; and it confirms `Lemma_3_3` at
`n = 2, 4, 6, 8, 16` and `Lemma_3_4_a` at `n = 2, 4, 8, 16` for all states of `E ∪ O`.

### Not formalized

Not part of this step, and formalized in the next section: the rest of Section 3.1 (Lemma 3.4(b), Lemmas 3.5 to
3.8, the other parts of Theorem 3.9, Theorems 3.10 and 3.11). Sections 3.2 to 6 are not formalized.

### Build and axioms

Same environment as above. `lake build` completed 3064 jobs without error or warning (run again after the
changes that followed the verification).
`lake env lean -j2 AxiomCheckTheoremA.lean` now checks 25 theorems (23 depend on `propext`, `Classical.choice`,
`Quot.sound`; `closedClass_iff_component` and `globalMap_rot` on `propext`, `Quot.sound`), and
`lake env lean -j2 AxiomCheckRule154.lean` checks the five theorems on rule 154 (the same three axioms). No
`sorry`, `admit`, `native_decide`, `axiom`, `unsafe`, `implemented_by` or `extern`; one more `decide`, for
"every element of `ZMod 2` is 0 or 1".

562 lines of Lean in four files, of which 159 are statements.

Claude

## Rule 154 complete: Theorems 3.9, 3.10 and 3.11 (27 November 2026)

Written by Claude, the reader outside the sessions, who also wrote this part of the Lean code.

**The proofs are checked by Lean. The statement file was read against the paper by an independent session**
(`VERIFICATION_lean_rule154_full.md`, on commit 20f1e9e): no statement differs from the paper beyond the
weakenings listed below; three points of wording. They are worked in here; what was changed is listed at the top
of that file. The session's own model of the Lean definitions reproduces every conclusion of Theorems 3.9, 3.10
and 3.11 for `n = 3, …, 12`.

With this part, part (a) of the main theorem of the paper (Theorem 3.1(a), which is Theorem 3.11) is proved in
Lean from the definitions of Section 2: for rule 154 and every ring size `n ≥ 3`, `k* = 1` if `n` is a power of
two and `k* = 0` otherwise. What "from the definitions" does not include: Proposition 2.1, which links `k*` to
the noisy chain, is not formalized, so the Lean theorem is about the integers `k_v` and `k*` as defined in
Section 2.2 of the paper, not about the stationary distribution.

### What is proved

Statements only: `RingSize/Rule154/StatementMain.lean` (138 lines). Proofs: `RingSize/Rule154/Periodic.lean`,
`Moves.lean` and `Main.lean`.

| Statement | Paper | Proved in |
|---|---|---|
| `Lemma_3_4_b_zero` | Lemma 3.4(b), for the cell 0: for even `n` that is not a power of two, `F^t(e_0) ≠ 0` for all `t` | `Main.lean` (uses `pow_two_of_iterate_eq_zero` of the pilot) |
| `Lemma_3_5` | Lemma 3.5: `F(M) ⊆ M`, for every even `n ≥ 2` | `Periodic.lean` |
| `Lemma_3_6_in_particular` | Lemma 3.6, the part "In particular": two different states with the same image exist only for even `n` and lie in `E ∪ O`; `F` is a bijection for odd `n` | `Periodic.lean` |
| `Lemma_3_7` | Lemma 3.7, first sentence: `F` restricted to `M` is a permutation of `M`, and every state of `M` is periodic (even `n ≥ 2`) | `Periodic.lean`, `Main.lean` |
| `Lemma_3_8_a` | Lemma 3.8(a) | `Main.lean` |
| `Lemma_3_8_b` | Lemma 3.8(b), without the clause "through cycles contained in `M`" | `Moves.lean`, `Main.lean` |
| `Theorem_3_9` | Theorem 3.9, parts (a) to (f), for `n = 2^k`, `k ≥ 2`; in (c) without the bound on the length of the path | `Main.lean` |
| `Theorem_3_10` | Theorem 3.10, all five claims, for `n ≥ 3` not a power of two | `Main.lean` |
| `Theorem_3_11` | Theorem 3.11, both cases with `S` and all `k_v` | `Main.lean` |

### Differences from the paper

1. **Lemma 3.6.** Only the part "In particular" is stated. The list of the three forms of a pair `x ≠ y` with
   `F(x) = F(y)` (`x + y = 1_E`, `x + y = 1_O`, `{x, y} = {1_E, 1_O}`) is not stated. The Lean proof follows the
   paper's cases A and B and gets from each that `n` is even and that `x` vanishes on a parity class.
2. **Lemma 3.7.** The second sentence ("The periodic states of `F` are the states of `M` and the periodic states
   of `L` in `E ∪ O`") is not stated. Of the third sentence, "the cycles are `{0}` and the cycles contained in
   `M`" is part (a) of `Theorem_3_9` together with `Zero_cycle`; its other clause, "the periodic states are
   exactly the states of `M ∪ {0}`", is not stated.
3. **Lemma 3.8(b).** Stated as: any two cycles that contain a state of `M` are joined by a directed path of
   `G_1`. The clause "through cycles contained in `M`" is not stated. (For even `n` a cycle that contains a state
   of `M` is contained in `M`; this is `cycle_subset_parM` in `Main.lean`.)
4. **Lemma 3.4(b).** Stated for the cell 0 only. The paper's statement for every cell follows by rotation, which
   is not carried out here; the proofs below need only the cell 0.
5. **Ring sizes.** Lemmas 3.5, 3.7 and 3.8 are stated for every even `n ≥ 2` (paper: `n ≥ 4`), Lemma 3.6 for
   every `n ≥ 1` (paper: `n ≥ 3`). Theorems 3.9, 3.10 and 3.11 have the ring sizes of the paper; in `Theorem_3_9`
   the exponent `k` is the `k` of the paper.
6. **Theorem 3.9(c).** The paper removes the ones on the odd cells one at a time and gets a path of length at
   most `μ(C) ≤ n/2`. The Lean proof goes through the cycle `{1}`: from `C` to `{1}` by setting zeros to one
   (Lemma 3.8(b)), from `{1}` to the cycle of `1_E + e_1` in the same way, and from there to `{0}` by one flip,
   because `F(1_E) = 0`. It gives a path, not the bound on its length; the bound is not stated.
7. **Theorem 3.9(e).** The upper bound `γ(C) ≤ m` is the paper's tree: a tree of edges of `G_1` on the cycles
   other than `{0}`, and one edge out of `{0}` of weight at most 2 (in Lean to the cycle of the state with ones
   at the cells 2 and 3; in the paper to the cycle of `e_0 + e_1`). The lower bound `γ(C) ≥ m` is obtained
   differently: `S = {{0}}` and `γ_min = m - 1` follow from Theorem 2.8, so a cycle `C ≠ {0}` is not selected and
   `γ(C) > m - 1`. The paper counts the edge that leaves `{0}`.
8. **Theorem 3.9(f).** For `k_v ≤ 1` the paper uses `e_0` and `F(e_0)` for the codes 001, 010, 100 and 101 and
   the states `e_0 + e_1` and `1` for 011, 110 and 111. Lean uses the flip `e_1` of `0` for 010 (Lemma 2.2), the
   state with ones at the cells 2, 3 for 001, 011, 110, 100, the state with ones at the cells 2, 4, 5 for 101,
   and `1` for 111; the last three lie on cycles with `γ = m = γ_min + 1`. For the lower bound `k_v ≥ 1`,
   `v ≠ 000`, the paper uses `γ({0}) = m - 1`, `γ(C) = m` and `R({0} → D_v) ≥ 1`; Lean uses `S = {{0}}` and
   Lemma 2.2 (`k_v = 0` would need a selected cycle with a state that contains `v`, and the state `0` contains
   only 000).
9. **Theorem 3.10.** "`G_1` is strongly connected" is stated as: every cycle is joined to every cycle by a
   directed path. In step (3) of the paper's proof Lean flips only the cell 0 of `0` and does not use that the
   cycle reached lies in `E ∪ O`. For the codes on periodic states Lean uses, for even `n ≥ 6`, the states with
   ones at the cells 2, 3; at 2, 4, 5; and at 1, 4 (the paper: `0^(n-2)11` and `0^(n-4)1011`), and for odd `n`
   any state that contains the code, since all states are periodic; this covers `n = 3`, which the paper treats
   separately. For `γ(C) = m - 1` the paper uses a spanning in-tree of edges of `G_1` rooted at each cycle; Lean
   applies Theorem 2.8 to the closed class of all cycles, which gives `S` = all cycles and `γ_min = m - 1`.
10. **"`n` is a power of two"** is `∃ k, n = 2^k`. It includes 1 and 2; the theorems that use it assume `n ≥ 3`.
11. **The cycle `{0}`.** `Theorem_3_9` (all six parts) and the clause on `S` of `Theorem_3_11` are stated for
    every cycle `C0` whose set of states is `{0}`; "`S = {{0}}`" is `S = {C0}` for every such `C0`. That `{0}` is
    a cycle is the separate statement `Zero_cycle`; it makes these statements non-empty, and with it they are the
    paper's (a cycle is determined by its set of states). Part (a) of `Theorem_3_9` does not itself say that
    `{0}` is a cycle.

No gap or false statement was found in the paper for these statements.

### Check outside Lean

The conclusions of `Theorem_3_11` (the value of `k*`, the eight `k_v`, the number of selected cycles) agree with
the computed records of rule 154 in `data/fw_sweep.csv` for every `n = 4, …, 20` (17 records; compared by the
author of the Lean files, with a few lines of Python that are not in the repository). The file has no record for
`n = 3`.

### Not formalized

Proposition 2.1; the parts of Lemmas 3.4(b), 3.6, 3.7 (its second sentence and the first clause of its third),
3.8(b) and Theorem 3.9(c) named above; Sections 3.2 to 6 (rules 43, 142, 94 and 26).

### Build and axioms

Same environment as above. `lake build` completed 3074 jobs without error or warning (run again after the
changes that followed the verification, which are comments only).
`lake env lean -j2 AxiomCheckRule154.lean` now checks 14 theorems on rule 154, all depending on `propext`,
`Classical.choice`, `Quot.sound`; `AxiomCheckTheoremA.lean` is unchanged (25 theorems). No `sorry`, `admit`,
`native_decide`, `axiom`, `unsafe`, `implemented_by` or `extern`. `decide` is used for facts about bits (elements
of `ZMod 2`) and for the parity of the numbers 1 to 5.

Two existing files were changed: `RingSize/TheoremA/Paths.lean` (one lemma added, `mem_cycleOf`) and
`RingSize/Rule154/Pow2.lean` (the definition `par` is now visible to the files that import it).

1307 lines of Lean in four new files, of which 138 are statements.

Claude
