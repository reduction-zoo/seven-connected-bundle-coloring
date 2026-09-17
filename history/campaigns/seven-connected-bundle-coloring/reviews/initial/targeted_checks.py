"""Independent review checks; execute the candidate only as subprocesses."""
import itertools
import json
from pathlib import Path
import subprocess
import sys
import z3

CANDIDATE = Path(__file__).resolve().parents[2] / 'work/algorithm.py'
WEIGHTS = [4096, 1024, 256, 64, 16, 4, 1]


def call(raw, extract=False):
    return subprocess.run([sys.executable, str(CANDIDATE)] + (['--extract'] if extract else []), input=raw, text=True, capture_output=True, check=False)


def solve(target):
    n, edges, bundles = target['n'], target['edges'], target['bundles']
    assert len(bundles) == 7 and all(bundles) and all(len(b) == 1 for b in bundles[:6])
    assert sorted(v for b in bundles for v in b) == list(range(n))
    assert len({tuple(sorted(e)) for e in edges}) == len(edges)
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        assert 0 <= a < n and 0 <= b < n and a != b
        adjacency[a].add(b)
        adjacency[b].add(a)
    side = {}
    for root in range(n):
        if root in side:
            continue
        side[root] = 0
        queue = [root]
        for v in queue:
            for u in adjacency[v]:
                if u not in side:
                    side[u] = 1-side[v]
                    queue.append(u)
                assert side[u] != side[v]
    for bundle in bundles:
        seen = {bundle[0]}
        queue = list(seen)
        for v in queue:
            for u in adjacency[v] & set(bundle):
                if u not in seen:
                    seen.add(u)
                    queue.append(u)
        assert seen == set(bundle)
    colors = [z3.Int('c'+str(v)) for v in range(n)]
    solver = z3.Solver()
    solver.add(*[c >= 1 for c in colors])
    solver.add(*[colors[a] != colors[b] for a,b in edges])
    maxima = []
    for bundle in bundles:
        value = colors[bundle[0]]
        for v in bundle[1:]:
            value = z3.If(value >= colors[v], value, colors[v])
        maxima.append(value)
    solver.add(sum(w*m for w,m in zip(WEIGHTS,maxima)) <= 5823)
    return solver, colors


def main():
    result = {'cases': [], 'malformed_failures': []}
    cases = [
        {'n':0,'edges':[],'lists':[]},
        {'n':1,'edges':[],'lists':[[]]},
        {'n':2,'edges':[[0,1]],'lists':[[1],[1]]},
        {'n':3,'edges':[],'lists':[[1],[2],[3]]},
        {'n':3,'edges':[[0,1],[1,2]],'lists':[[1,2,3]]*3},
    ]
    for source in cases:
        run = call(json.dumps(source))
        assert run.returncode == 0, run.stderr
        target = json.loads(run.stdout)
        solver, colors = solve(target)
        source_yes = any(all(c[a]!=c[b] for a,b in source['edges']) for c in itertools.product(*source['lists']))
        count = 0
        while solver.check() == z3.sat:
            model = solver.model()
            witness = [model.eval(c).as_long() for c in colors]
            recovery = call(json.dumps({'source':source,'target_solution':witness}), True)
            assert recovery.returncode == 0, recovery.stderr
            c = json.loads(recovery.stdout)
            assert len(c)==source['n'] and all(c[v] in source['lists'][v] for v in range(source['n']))
            assert all(c[a]!=c[b] for a,b in source['edges'])
            solver.add(z3.Or(*[var!=value for var,value in zip(colors,witness)]))
            count += 1
        assert solver.check() == z3.unsat
        assert source_yes == (count > 0)
        result['cases'].append({'source':source,'source_yes':source_yes,'all_target_witnesses_recovered':count})
    fixed = call('null')
    fixed_target = json.loads(fixed.stdout)
    assert solve(fixed_target)[0].check() == z3.unsat
    bad = [('large_integer','{"n":'+'9'*5000+',"edges":[],"lists":[]}'), ('deep_nesting','['*20000+'0'+']'*20000)]
    for name, raw in bad:
        run = call(raw)
        if run.returncode != 0:
            result['malformed_failures'].append({'name':name,'length':len(raw),'returncode':run.returncode,'last_error':run.stderr.splitlines()[-1]})
        else:
            assert json.loads(run.stdout) == fixed_target
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
