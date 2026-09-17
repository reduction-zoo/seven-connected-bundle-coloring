"""The declared seeded scope, using the prepared independent oracles."""
import importlib.util
import json
from pathlib import Path
import random

work = Path(__file__).resolve().parents[2] / 'work'
spec = importlib.util.spec_from_file_location('prepared', work / 'check.py')
prepared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepared)
rng = random.Random(20260916)
yes = recoveries = 0
for index in range(160):
    n = rng.randrange(8)
    sides = [rng.randrange(2) for _ in range(n)]
    edges = [[u, v] for u in range(n) for v in range(u + 1, n)
             if sides[u] != sides[v] and rng.random() < 0.45]
    masks = [rng.randrange(8) if index % 2 else rng.randrange(1, 8) for _ in range(n)]
    source = {'n': n, 'edges': edges,
              'lists': [[c for c in range(1, 4) if mask & (1 << (c - 1))] for mask in masks]}
    target = prepared.run(work / 'algorithm.py', source)
    witnesses = prepared.compare(source, target)
    yes += bool(witnesses)
    for witness in witnesses:
        recovered = prepared.run(work / 'algorithm.py',
                                 {'source': source, 'target_solution': witness}, extract=True)
        assert prepared.source_witness(source, recovered), (index, source, witness, recovered)
        recoveries += 1
print(json.dumps({'seed': 20260916, 'cases': 160, 'yes': yes, 'no': 160 - yes,
                  'recoveries': recoveries, 'max_source_vertices': 7}))
