"""ruleOfNumber of Statement.lean against the local rules written out in the paper (asymmetric rules, so the
bit order and the orientation a = x_{i-1}, c = x_{i+1} are tested). Run from this directory."""
from lean_defs import rule_of_number, CODES

out = []
paper = {   # paper/ring_size_paper.tex: rule -> set of codes abc with f(a,b,c) = 1
    154: ({'001', '011', '100', '111'}, 'l. 371-372'),
    26: ({'001', '011', '100'}, 'l. 1335-1336'),
    142: ({'001', '010', '011', '111'}, 'table l. 607'),
    43: ({'000', '001', '011', '101'}, 'table l. 608'),
}
for N, (ones, where) in paper.items():
    f = rule_of_number(N)
    mine = {''.join(map(str, v)) for v in CODES if f(*v) == 1}
    out.append(f'rule {N} ({where}): ruleOfNumber gives f = 1 on {sorted(mine)}; paper {sorted(ones)}; '
               f'{"agree" if mine == ones else "DISAGREE"}')
f = rule_of_number(154)
out.append('rule 154, Lemma 3.2 (l. 391) f(a,b,c) = c + a(1+b): '
           + ('agree on all 8 codes' if all(f(a, b, c) == (c + a * (1 + b)) % 2 for a, b, c in CODES) else 'DISAGREE'))
for N, g, name in ((90, lambda a, b, c: (a + c) % 2, 'a + c'), (204, lambda a, b, c: b, 'b')):
    f = rule_of_number(N)
    out.append(f'rule {N}: ruleOfNumber = {name}: ' + str(all(f(*v) == g(*v) for v in CODES)))
print('\n'.join(out))
open('out/rule_tables.txt', 'w').write('\n'.join(out) + '\n')
