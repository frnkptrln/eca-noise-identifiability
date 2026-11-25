import Lake
open Lake DSL

package RingSize where
  leanOptions := #[⟨`autoImplicit, false⟩]

-- Mathlib pinned to the release tag v4.36.0 (toolchain leanprover/lean4:v4.36.0).
require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.36.0"

-- `weakLeanArgs` limit each `lean` process of this library to 2 threads; they do not
-- enter the build trace (Lake README, package and library options).
@[default_target]
lean_lib RingSize where
  weakLeanArgs := #["-j2"]
