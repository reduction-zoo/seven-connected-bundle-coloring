"""Bipartite list coloring to seven fixed weighted connected bundles."""
import json
import sys

import networkx as nx

WEIGHTS = (4096, 1024, 256, 64, 16, 4, 1)


def parse_source(value):
    if type(value) is not dict or set(value) != {'n', 'edges', 'lists'}:
        return None
    n, edges, lists = value['n'], value['edges'], value['lists']
    if type(n) is not int or n < 0 or type(edges) is not list or type(lists) is not list or len(lists) != n:
        return None
    for allowed in lists:
        if type(allowed) is not list or any(type(c) is not int or c not in (1, 2, 3) for c in allowed):
            return None
        if len(allowed) != len(set(allowed)):
            return None
    seen = set()
    for edge in edges:
        if type(edge) is not list or len(edge) != 2 or any(type(v) is not int or not 0 <= v < n for v in edge):
            return None
        u, v = sorted(edge)
        if u == v or (u, v) in seen:
            return None
        seen.add((u, v))
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(sorted(seen))
    return graph if nx.is_bipartite(graph) else None


def forward(source):
    graph = parse_source(source)
    if graph is None:
        source = {'n': 1, 'edges': [], 'lists': [[]]}
        graph = nx.empty_graph(1)
    original_n = source['n']
    if original_n == 0:
        graph.add_node(0)
    components = sorted((sorted(c) for c in nx.connected_components(graph)), key=lambda c: c[0])
    side = nx.bipartite.color(graph)
    for component in components:
        root_side = side[component[0]]
        for v in component:
            side[v] ^= root_side
    for first, second in zip(components, components[1:]):
        connector = len(graph)
        graph.add_edges_from([(first[0], connector), (connector, second[0])])
    core_size = len(graph)
    palette = list(range(core_size, core_size + 6))
    graph.add_nodes_from(palette)
    for i in range(3):
        for j in range(3):
            if i != j:
                graph.add_edge(palette[2 * i], palette[2 * j + 1])
    for v, allowed in enumerate(source['lists']):
        for color in range(1, 4):
            if color not in allowed:
                graph.add_edge(v, palette[2 * (color - 1) + 1 - side[v]])
    return {'n': len(graph), 'edges': sorted([min(u,v), max(u,v)] for u,v in graph.edges()),
            'bundles': [[v] for v in palette] + [list(range(core_size))]}


def extract(payload):
    if type(payload) is not dict or set(payload) != {'source', 'target_solution'}:
        raise ValueError('invalid recovery payload')
    source, colors = payload['source'], payload['target_solution']
    if parse_source(source) is None:
        raise ValueError('invalid recovery source')
    target = forward(source)
    if type(colors) is not list or len(colors) != target['n'] or any(type(c) is not int or c < 1 for c in colors):
        raise ValueError('invalid target coloring')
    if any(colors[u] == colors[v] for u, v in target['edges']):
        raise ValueError('improper target coloring')
    if sum(w * max(colors[v] for v in b) for w, b in zip(WEIGHTS, target['bundles'])) > 5823:
        raise ValueError('target coloring exceeds budget')
    return colors[:source['n']]


if __name__ == '__main__':
    if sys.argv[1:] == ['--extract']:
        print(json.dumps(extract(json.load(sys.stdin))))
    elif not sys.argv[1:]:
        try:
            source = json.load(sys.stdin)
        except json.JSONDecodeError:
            source = None
        print(json.dumps(forward(source)))
    else:
        raise ValueError('expected no arguments or --extract')
