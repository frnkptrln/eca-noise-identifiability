"""Rules 204, 90 and 154 at n = 3 and n = 4: cycles, V, gamma, S, G1, closed classes, k_v, k*,
all from the literal model of Statement.lean, and the statement checks. Run from this directory."""
from instance import Instance

out = []
for N in (204, 90, 154):
    for n in (3, 4):
        I = Instance(N, n)
        ch = I.check_statements()
        out.append(I.summary())
        out.append(f'  statement checks: {len(ch)} run, failed: {[k for k, v in ch.items() if not v] or "none"}')
        out.append(f'  run: {sorted(ch)}')
        out.append('')
print('\n'.join(out))
open('out/small_cases.txt', 'w').write('\n'.join(out) + '\n')
