# Certificates of the ring-size sweep

898 files `n{n}_rule_{rule}.json.gz` for n = 4..14, non-bijective classes only (bijective classes are analytic: k* = 0). Larger ring sizes of the sweep have no certificates.

Fields (one gzipped JSON file per class representative):

- `rule`, `n`, `m` (number of cycles), `cycles` (each cycle as its list of states in the order of F).
- `hierarchy`: laminar family from the root-free Edmonds contraction. Nodes 0..m-1 are the cycles, larger ids are contracted sets; `parent` (-1 for `top`), dual values `y`, and for every node except `top` its selected edge `sel_tail` -> `sel_head` (cycle indices, tail inside the set, head outside). Inside every contracted set the children's selected edges form one cyclic permutation of all children.
- `gamma` (stochastic potential of every cycle, = sum(y) - sum of y over the sets containing it), `gamma_min`, `stable` (the noise-selected cycles, gamma = gamma_min), `stable_cover_mask` (bit c set iff code c occurs on a noise-selected cycle), `tree` (one explicit minimum in-tree, rooted at `tree.root`).
- `k_c`: per code c the order k, a root cycle and a witness `trajectory` from that cycle to a state containing c with its `resistance`; `kstar` = max k.
- `uncovered_codes` (files with k* >= 1) and the report column of the same origin: the codes with k_c = k* (not all codes absent from the noise-selected cycles; codes with 1 <= k_c < k* are absent too); `covering_cycles` (files with k* = 0): noise-selected cycles whose states contain all eight codes.

Checked by `code/fw/check_cert.py` and independently by `verify_v02/check_certs.py` (see `VERIFICATION_v02.md`).
