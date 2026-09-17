"""Separate exhaustive source oracle and exact target-coloring check."""
import argparse
import itertools
import json
from pathlib import Path
import subprocess
import sys

import networkx as nx
import z3


def execute(path, value, recover=False):
    process = subprocess.run([sys.executable, str(path)] + (['--extract'] if recover else []),
                             input=json.dumps(value), text=True, capture_output=True, check=True)
    return json.loads(process.stdout)


def verify(path, source):
    source_solutions = [list(c) for c in itertools.product(*source['lists'])
                        if all(c[u] != c[v] for u, v in source['edges'])]
    target = execute(path, source)
    assert set(target) == {'n', 'edges', 'bundles'}
    n = target['n']
    assert type(n) is int and n >= 7
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    pairs = [tuple(sorted(e)) for e in target['edges']]
    assert len(pairs) == len(set(pairs))
    assert all(type(u) is int and type(v) is int and 0 <= u < v < n for u, v in pairs)
    graph.add_edges_from(pairs)
    assert nx.is_bipartite(graph)
    bundles = target['bundles']
    assert len(bundles) == 7 and all(len(b) == 1 for b in bundles[:6])
    assert sorted(v for b in bundles for v in b) == list(range(n))
    assert all(b and nx.is_connected(graph.subgraph(b)) for b in bundles)
    c = [z3.Int(f'x{i}') for i in range(n)]
    solver = z3.Solver()
    solver.add(*(z3.And(x >= 1, x <= 5823) for x in c))
    solver.add(*(c[u] != c[v] for u, v in pairs))
    terms = []
    for weight, bundle in zip([4096,1024,256,64,16,4,1], bundles):
        maximum = c[bundle[0]]
        for v in bundle[1:]:
            maximum = z3.If(maximum >= c[v], maximum, c[v])
        terms.append(weight * maximum)
    solver.add(sum(terms) <= 5823)
    verdict = solver.check()
    assert verdict in (z3.sat, z3.unsat)
    assert bool(source_solutions) == (verdict == z3.sat), source
    recovered = 0
    for _ in range(4):
        if verdict == z3.unsat:
            break
        model = solver.model()
        witness = [model.eval(x).as_long() for x in c]
        assert all(witness[u] != witness[v] for u, v in pairs)
        assert sum(w * max(witness[v] for v in b) for w, b in zip([4096,1024,256,64,16,4,1], bundles)) <= 5823
        answer = execute(path, {'source': source, 'target_solution': witness}, recover=True)
        assert answer in source_solutions, (source, witness, answer)
        recovered += 1
        solver.add(z3.Or(*(x != v for x, v in zip(c, witness))))
        verdict = solver.check()
        assert verdict in (z3.sat, z3.unsat)
    return bool(source_solutions), recovered


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--candidate', required=True, type=Path)
    args = parser.parse_args()
    cases = [{'n': 0, 'edges': [], 'lists': []}]
    for edge in ([], [[0,1]]):
        for a, b in itertools.product([[],[1],[2],[3],[1,2],[1,2,3]], repeat=2):
            cases.append({'n': 2, 'edges': edge, 'lists': [a,b]})
    cases.append({'n':4, 'edges':[[0,1],[2,3]], 'lists':[[3],[1],[2],[3]]})
    results = [verify(args.candidate, source) for source in cases]
    print(json.dumps({'cases':len(cases), 'yes':sum(a for a,b in results),
                      'no':sum(not a for a,b in results), 'recoveries':sum(b for a,b in results),
                      'source_oracle':'exhaustive list assignments', 'target_solver':z3.get_version_string()}))
