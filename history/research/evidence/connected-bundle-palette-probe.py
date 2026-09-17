"""Exact screening of a fixed weighted bipartite palette."""
import itertools
import json
import z3

colors = [z3.Int(f'c{i}') for i in range(6)]
height = z3.Int('h')
weights = [4096, 1024, 256, 64, 16, 4]
desired = [1, 1, 2, 2, 3, 3]
edges = [(0, 3), (0, 5), (2, 1), (2, 5), (4, 1), (4, 3)]
threshold = sum(w * c for w, c in zip(weights, desired)) + 3
solver = z3.Solver()
solver.add(*(c >= 1 for c in colors), height >= 1)
solver.add(*(colors[u] != colors[v] for u, v in edges))
solver.add(sum(w * c for w, c in zip(weights, colors)) + height <= threshold)
results = {}
for name, constraint, expected in [
    ('desired_palette', z3.And(*(c == d for c, d in zip(colors, desired)), height == 3), z3.sat),
    ('different_palette', z3.Or(*(c != d for c, d in zip(colors, desired))), z3.unsat),
    ('core_above_three', height > 3, z3.unsat),
]:
    solver.push()
    solver.add(constraint)
    result = solver.check()
    assert result == expected, (name, result)
    results[name] = str(result)
    solver.pop()
for i, w in enumerate(weights):
    assert w > sum(weights[j] * (desired[j] - 1) for j in range(i + 1, 6)) + 2
extensions = []
for a, b in itertools.product(range(1, 4), repeat=2):
    middle = next(c for c in range(1, 4) if c not in (a, b))
    extensions.append([a, middle, b])
print(json.dumps(dict(solver=z3.get_version_string(), weights=weights, desired=desired,
                     edges=edges, threshold=threshold, results=results,
                     connector_extensions=extensions), indent=2))
