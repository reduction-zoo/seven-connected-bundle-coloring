"""Independent exact language oracles and subprocess injection harness."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

import networkx as nx
import z3

WEIGHTS = [4096, 1024, 256, 64, 16, 4, 1]
THRESHOLD = 5823


def graph(value, extra):
    if not isinstance(value, dict) or set(value) != {'n', 'edges', extra}:
        return None
    n, edges = value['n'], value['edges']
    if type(n) is not int or n < 0 or not isinstance(edges, list):
        return None
    pairs = set()
    for e in edges:
        if not isinstance(e, list) or len(e) != 2 or any(type(v) is not int or not 0 <= v < n for v in e):
            return None
        pair = tuple(sorted(e))
        if e[0] == e[1] or pair in pairs:
            return None
        pairs.add(pair)
    g = nx.Graph()
    g.add_nodes_from(range(n))
    g.add_edges_from(pairs)
    return g if nx.is_bipartite(g) else None


def valid_source(s):
    if graph(s, 'lists') is None:
        return False
    lists = s['lists']
    return (isinstance(lists, list) and len(lists) == s['n'] and
            all(isinstance(a, list) and all(type(c) is int and c in (1, 2, 3) for c in a)
                and len(set(a)) == len(a) for a in lists))


def valid_target(t):
    g = graph(t, 'bundles')
    if g is None:
        return False
    bundles = t['bundles']
    if not isinstance(bundles, list) or len(bundles) != 7:
        return False
    if not all(isinstance(b, list) and b and all(type(v) is int and 0 <= v < t['n'] for v in b) for b in bundles):
        return False
    if sorted(v for b in bundles for v in b) != list(range(t['n'])):
        return False
    return all(len(b) == 1 for b in bundles[:6]) and all(nx.is_connected(g.subgraph(b)) for b in bundles)


def proper(value, colors):
    return (isinstance(colors, list) and len(colors) == value['n'] and
            all(type(c) is int and c > 0 for c in colors) and
            all(colors[u] != colors[v] for u, v in value['edges']))


def source_witness(s, colors):
    return valid_source(s) and proper(s, colors) and all(c in a for c, a in zip(colors, s['lists']))


def target_witness(t, colors):
    return (valid_target(t) and proper(t, colors) and
            sum(w * max(colors[v] for v in b) for w, b in zip(WEIGHTS, t['bundles'])) <= THRESHOLD)


def solve(value, target=False, limit=1):
    if not (valid_target(value) if target else valid_source(value)):
        return []
    solver = z3.Solver()
    colors = [z3.Int(f'c{i}') for i in range(value['n'])]
    solver.add(*(c >= 1 for c in colors))
    solver.add(*(colors[u] != colors[v] for u, v in value['edges']))
    if target:
        maxima = [z3.Int(f'm{i}') for i in range(7)]
        for maximum, bundle in zip(maxima, value['bundles']):
            solver.add(*(maximum >= colors[v] for v in bundle))
        solver.add(sum(w * m for w, m in zip(WEIGHTS, maxima)) <= THRESHOLD)
    else:
        solver.add(*(z3.Or(*(c == a for a in allowed)) for c, allowed in zip(colors, value['lists'])))
    witnesses = []
    for _ in range(limit):
        verdict = solver.check()
        assert verdict in (z3.sat, z3.unsat), verdict
        if verdict == z3.unsat:
            break
        model = solver.model()
        witness = [model.eval(c, model_completion=True).as_long() for c in colors]
        assert (target_witness if target else source_witness)(value, witness)
        witnesses.append(witness)
        solver.add(z3.Or(*(c != a for c, a in zip(colors, witness))))
    return witnesses


def run(candidate, payload, extract=False):
    command = [sys.executable, str(candidate)] + (['--extract'] if extract else [])
    result = subprocess.run(command, input=json.dumps(payload), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def compare(source, target):
    assert valid_target(target), target
    witnesses = solve(target, target=True, limit=3)
    assert bool(solve(source)) == bool(witnesses), (source, target)
    return witnesses


def self_test(cases):
    for case in cases:
        assert bool(solve(case['source'])) == case['yes'], case['name']
    yes = {'n': 7, 'edges': [], 'bundles': [[i] for i in range(7)]}
    no = {'n': 7, 'edges': [[0,3],[0,5],[2,1],[2,5],[4,1],[4,3],[6,1],[6,3],[6,5]],
          'bundles': [[i] for i in range(7)]}
    assert solve(yes, target=True) and not solve(no, target=True)
    for source, target in [(cases[0]['source'], no), (cases[2]['source'], yes), (cases[0]['source'], {})]:
        try:
            compare(source, target)
        except AssertionError:
            pass
        else:
            raise AssertionError('faulty output was accepted')
    assert not source_witness(cases[4]['source'], [1, 1])
    assert not target_witness(yes, [5823] * 7)
    print(json.dumps({'source_cases': len(cases), 'target_controls': 2,
                      'faulty_outputs_rejected': 3, 'faulty_witnesses_rejected': 2,
                      'solver': z3.get_version_string()}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    cases = json.loads(Path(__file__).with_name('cases.json').read_text())
    if args.self_test:
        self_test(cases)
    elif args.candidate:
        recoveries = 0
        for case in cases:
            source = case['source']
            target = run(args.candidate, source)
            for witness in compare(source, target):
                answer = run(args.candidate, {'source': source, 'target_solution': witness}, extract=True)
                assert source_witness(source, answer), (case['name'], witness, answer)
                recoveries += 1
        print(json.dumps({'cases': len(cases), 'recoveries': recoveries}))
    else:
        parser.error('choose --self-test or --candidate')
