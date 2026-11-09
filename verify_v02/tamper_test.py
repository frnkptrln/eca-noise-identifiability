"""Tampered copies of two certificates must all be rejected by check_certs.py."""
import gzip, json, copy, os
import check_certs, eca
srcs = ['../data/fw_certificates_n12/rule_106.json.gz', '../data/fw_certificates_sweep/n14_rule_076.json.gz',
        '../data/fw_certificates_n12/rule_232.json.gz']
def tampers(d):
    m = d['m']; H = d['hierarchy']; top = H['top']
    t = copy.deepcopy(d); t['hierarchy']['y'][0] += 1; yield 'leaf y + 1', t
    t = copy.deepcopy(d); t['gamma'][m - 1] -= 1; yield 'gamma - 1', t
    t = copy.deepcopy(d); X = m; t['hierarchy']['sel_head'][X] = t['hierarchy']['sel_tail'][X]; yield 'selected edge head inside its set', t
    t = copy.deepcopy(d); t['k_c'][7]['k'] += 1; yield 'k_7 + 1', t
    t = copy.deepcopy(d); t['cycles'] = t['cycles'][:-1]; yield 'cycle dropped', t
    t = copy.deepcopy(d); t['k_c'][7]['trajectory'][-1] ^= 1; yield 'witness end state altered', t
    t = copy.deepcopy(d); t['kstar'] = d['kstar'] + 1; yield 'kstar + 1', t
    t = copy.deepcopy(d); t['stable'] = d['stable'][:-1]; yield 'stable set shortened', t
    # move dual mass from one internal set to its parent (keeps the total, breaks tightness or feasibility)
    t = copy.deepcopy(d); y = t['hierarchy']['y']
    cand = [X for X in range(m, len(y)) if y[X] > 0 and X != top]
    if cand:
        X = cand[0]; y[X] -= 1; y[t['hierarchy']['parent'][X]] += 1; yield 'internal y moved to parent', t
    t = copy.deepcopy(d); t['tree']['parent'][1] = 1 if t['tree']['root'] != 1 else 2; yield 'explicit tree self-loop', t
rows = []
for s in srcs:
    d = json.load(gzip.open(s))
    base = check_certs.check(s)
    rows.append(dict(src=s.split('/')[-1], tamper='none', ok=base['ok'], fails=base['fails']))
    for name, t in tampers(d):
        p = f'out/tamper/{s.split("/")[-1]}'
        with gzip.open(p, 'wt') as fh: json.dump(t, fh)
        try:
            r = check_certs.check(p)
        except Exception as ex:
            r = dict(ok=False, fails=['EXC ' + repr(ex)[:80]])
        rows.append(dict(src=s.split('/')[-1], tamper=name, ok=r['ok'], fails=r['fails']))
        os.remove(p)
for r in rows: eca.append_jsonl('out/tamper_test.jsonl', r)
for r in rows: print(r)
print('tampered accepted:', sum(r['ok'] for r in rows if r['tamper'] != 'none'), 'of', sum(r['tamper'] != 'none' for r in rows))
