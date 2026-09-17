# Preparation

The exact source and target languages are fixed in [contract.md](contract.md).
Both decision oracles use Z3 5.1.0 integer constraints. Graph legality, witness
properness, list membership and weighted cost are checked directly; NetworkX
checks bipartiteness and induced-bundle connectivity. No candidate code is
imported. SAT yields an independently validated witness; UNSAT is NO and unknown
fails explicitly.

Source constraints assign a color from each input list and disequality on every
edge. Target constraints assign positive colors and an auxiliary upper bound
for each bundle's colors, then bound their weighted sum by 5823. An actual
coloring extends by its true maxima, and any feasible upper bounds dominate its
true cost, proving exact equivalence of this oracle encoding.

Ran `python3 campaigns/seven-connected-bundle-coloring/work/check.py --self-test`.
[Raw output](evidence/preparation/self-test.json) records ten hand-classified
source cases, two target controls, three deliberately faulty output rejections,
and two invalid-witness rejections. Source cases cover empty and disconnected
graphs, list contradictions, third-color use, and malformed inputs. The NO
target is a six-cycle palette with one vertex adjacent to all three opposite
anchors; its hand classification uses the screened palette inequalities.

The injection harness invokes both candidate modes in fresh subprocesses and
checks up to three distinct independently solved target colorings per YES
instance. This is finite coverage, not a proof or independent author review.
There is no candidate yet at preparation completion.
