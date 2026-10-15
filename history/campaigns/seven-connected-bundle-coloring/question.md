---
status: admitted
openness: supported-inferred-fixed-bundle-gap
difficulty: low
importance: moderate
tags: [Karp, coloring, bipartite, connected-partition, weighted-bundles]
last-literature-check: 2026-09-16
---

# Bipartite 3-List-Coloring → seven connected coloring bundles

Admitted for a 40-round campaign. The investigated route uses a fixed weighted
six-vertex palette and one connected main bundle. It could establish hardness
with a constant number of connected bundles. Correctness, novelty and
significance remain separate review obligations; no result is claimed yet.

## Exact question

Source: a finite simple bipartite graph G on explicitly indexed vertices, with
each vertex v carrying an explicit list L(v) contained in {1,2,3}. Empty lists
are allowed and make the source NO. A witness is a proper coloring using the
lists. Malformed encodings are outside the language.

Target: a finite simple bipartite graph H with an ordered partition into seven
nonempty vertex sets, each inducing a connected subgraph. The first six sets
are singleton bundles with respective weights 4096,1024,256,64,16,4; the seventh
has weight one. A witness assigns positive integer colors properly to H. It is
accepted when the sum of each bundle's weight times its maximum color is at
most the fixed threshold 5823. Inputs violating these restrictions are NO.

Prove a deterministic polynomial many-one reduction from the source to this
target, with polynomial recovery of a source list coloring from every accepted
target coloring. The intended construction has O(n+m) graph size and
O((n+m+1) log(n+2)) output bits; validation and construction must remain
polynomial under the explicit encodings. Provide a legal fixed NO output for
malformed source strings. A different threshold or restriction requires a new
question if this precise target is abandoned.

The resulting NP-completeness theorem must follow from a general proof, not
the finite screening experiment. A generic encoding into unrestricted weighted
coloring does not meet the target. A negative outcome may stop the campaign,
but does not itself count as the requested constructive result.

## Literature and the actual gap

Ito, Kakimura, Kamiyama, Kobayashi and Okamoto,
[Minimum Sum Coloring with Bundles in Trees and Bipartite Graphs](https://arxiv.org/html/2509.15080v1),
Section 4, gives hardness for three weighted bundles and four unweighted
bundles without requiring connected bundles. Section 3.4 gives a polynomial
algorithm for connected partitions on trees. Section 5 asks about independent
and connected partitions on bipartite graphs. The
[ISAAC 2025 version](https://drops.dagstuhl.de/storage/00lipics/lipics-vol359-isaac2025/LIPIcs.ISAAC.2025.40/LIPIcs.ISAAC.2025.40.pdf)
has the same question on printed p. 40:13.

The unrestricted number-of-bundles case is already hard: singleton bundles
include ordinary minimum sum coloring on bipartite graphs. Thus do not describe
the entire connected-partition problem as unclassified. The proposed contribution
is specifically a fixed-seven-bundle restriction. This is an inferred gap in
the published classification, rather than an explicitly posed seven-bundle
conjecture. The published Section 4 constructions include disconnected bundles;
they do not directly establish this fixed target.

The source's NP-completeness is explicitly stated in that primary paper just
before Theorem 10, with attribution to the Jansen–Scheffler construction and
Golovach–Paulusma's observation. The primary reduction proof in Section 4.1
was inspected; its output bundle partition includes separated anchor components.
The earlier source-hardness proof still needs direct checking before claiming
the campaign's final complexity classification.

Checked on 2026-09-16: the
[arXiv history](https://arxiv.org/abs/2509.15080), the full v1 and conference
paper, and searches `"Minimum Sum Coloring" "connected partition"`,
`"coloring with bundles" "2026" connected`,
`"Minimum Sum Coloring with Bundles" "partition" hardness 2026 seven`,
and `"bundles" "connected partition" "NP" coloring`.
No subsequent fixed-connected-bundle classification was identified. Equivalent
precoloring-extension results and weighted palette forcing must be checked in
the final novelty review. No exhaustive coverage claim is made.

## Construction route and executed first check

Use palette vertices a1,b1,a2,b2,a3,b3 in two sides of a bipartite graph.
Add every edge ai-bj with i different from j. Their desired colors in that
order are 1,1,2,2,3,3. Assign the six singleton weights stated above.
Their desired cost is 5820, leaving three units for the main bundle.

There is a direct forcing argument. If the earliest palette color differing
from the desired vector occurs at position i, it must be larger: earlier
palette neighbors forbid every smaller positive color. Its extra cost exceeds
all possible savings from later singleton colors and the main-bundle maximum.
The strict inequalities are checked by the probe and should be proved in the
campaign. Consequently every accepted coloring pins the palette and bounds the
main bundle by color three.

Keep each original vertex in the main bundle and connect it to the opposite-side
palette vertex of every forbidden list color. These edges encode its list.
Choose bipartitions so one representative per source component lies on side A.
Join consecutive representatives with paths of length two, using one new
main-bundle vertex per path. Any two endpoint colors in {1,2,3} extend across
such a path. The main bundle becomes connected while the whole graph stays
bipartite. Restricting any accepted target coloring to the original vertices
is the proposed extractor. Empty sources need a dummy main vertex; malformed
sources need a fixed legal NO construction.

The bounded screening exercise used three exact Z3 queries about the palette
and all nine pairs of endpoint colors for a two-edge connector. Reproduce with
`python3 research/evidence/connected-bundle-palette-probe.py`.
The [output](../../research/evidence/connected-bundle-palette-probe.json) reports SAT for
the desired palette, UNSAT for any different palette under budget, and UNSAT
for a main-bundle bound above three. All nine connector extensions exist.
This tests the proposed interface, not a full reduction or arbitrary source
inputs. No previous experience entry with applicable palette premises was
found by searching `bundles|precolor|lexicographic|palette`.

## Assessment and gates

Difficulty is low after the first check: the main remaining correctness work
is complete input handling, a general forcing proof, and independent injection
tests. Novelty risk is material because palette forcing is standard; the
contribution must be the new restricted complexity boundary, not the gadget
in isolation. Importance is moderate if that boundary survives review. It does
not locate the minimum possible number of connected bundles or settle the
unweighted constant-bundle threshold.

| Gate | Decision | Basis |
|---|---|---|
| 1. Precise target | Pass | Fixed languages, constants, witness predicates and recovery route |
| 2. Applicable results | Pass | Known fixed-bundle outputs are not connected partitions |
| 3. Openness | Pass within coverage | Inferred restriction gap; explicit limits above |
| 4. Significance | Pass provisionally | Fixed seven connected bundles, beyond unrestricted bundle count |
| 5. Proof route | Pass | Weighted palette plus list edges and neutral component connectors |
| 6. Initial investigation | Pass | Three exact palette queries and all connector color pairs |

Campaign obligations: independent source and target oracles before implementing
the rule; legal output checks on YES and NO sources; arbitrary-witness recovery;
general proofs and polynomial bounds; primary source-hardness and novelty audit;
native independent review; and an inspected Typst manuscript if the rule advances.
At most 40 genuine attempts, with early stopping if the target is already known,
the contribution is too immediate to qualify, or no justified route remains.
