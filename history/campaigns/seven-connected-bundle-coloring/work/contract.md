# Executable rule contract

Source JSON: `{"n": n, "edges": [[u,v],...], "lists": [[color,...],...]}`.
Require exactly these keys, nonnegative integer n (excluding booleans), n lists
of distinct integers from {1,2,3}, and distinct unordered edges between different
vertices in range(n). Lists may be empty. Edge orientation is immaterial but
duplicate reverse edges are malformed. The graph must be bipartite.
Malformed JSON or a schema violation denotes a source NO string.

Target JSON: `{"n": N, "edges": [[u,v],...], "bundles": [[v,...],...]}`.
Use the same simple bipartite graph rules. The seven ordered nonempty bundles
partition range(N), each induces a connected graph, and the first six are
singletons. Weights [4096,1024,256,64,16,4,1] and threshold 5823 are fixed by the
target language, not input fields.

Both witness types are JSON lists of integer colors, one per vertex. Source
colors belong to their lists and differ on edges. Target colors are positive,
differ on edges, and have sum of weighted bundle maxima at most 5823.

Forward: `python3 algorithm.py` reads one source JSON value and returns one
legal target. Malformed inputs must produce the fixed legal NO target described
by the proof. Recovery: `python3 algorithm.py --extract` reads
`{"source": source_value, "target_solution": colors}` and returns source colors.
Recovery is required for every valid target witness of a constructed output;
invalid recovery inputs fail explicitly. Both modes work in fresh processes.
Testing programs must not import candidate code.
