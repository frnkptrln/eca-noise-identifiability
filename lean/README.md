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
