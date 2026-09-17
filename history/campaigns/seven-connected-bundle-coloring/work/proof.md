# A fixed seven-bundle reduction

## Statement

Under the explicit languages of [contract.md](contract.md), algorithm.py gives
a deterministic polynomial many-one reduction from Bipartite List 3-Coloring to
the fixed seven-bundle target. Restriction to the original vertex indices
recovers a valid source coloring from every accepted target coloring.
NP-hardness uses a separate established hardness theorem for a global palette
of three colors, not merely lists of size three.

## Palette lemma

Use vertices a1,b1,a2,b2,a3,b3, in that order. Their edges are ai-bj for i != j.
Let d=(1,1,2,2,3,3) and w=(4096,1024,256,64,16,4). The vector d is proper and
has weighted cost 5820. For every i, direct integer arithmetic gives

    w_i > 2 + sum_{j>i} w_j (d_j-1).

Suppose a proper positive-integer palette coloring c and a positive integer h
satisfy sum_i w_i c_i + h <= 5823. If c differs from d, choose its earliest
differing position i. At positions 1 and 2 the desired value is the minimum
positive integer. Vertex a2 has earlier neighbor b1 of color 1, and b2 has
earlier neighbor a1 of color 1. Vertex a3 has earlier neighbors b1,b2 of colors
1,2; vertex b3 has earlier neighbors a1,a2 of colors 1,2. Thus c_i >= d_i+1.
Later colors are at least 1, and h >= 1. Therefore

    sum_j w_j c_j + h - 5823
       >= w_i - sum_{j>i} w_j(d_j-1) - 2 > 0,

a contradiction. Hence c=d and h<=3. This applies to arbitrary accepted
colorings, without assuming optimality, canonicalization or an a priori color
bound. In the target, take h to be the nonempty main bundle's actual maximum.

## Construction and legal outputs

Let the valid source have n vertices and m edges. For n>0, list its connected
components in increasing order of smallest vertex and choose that vertex as
representative. Bipartition each component with its representative on side A.
Retain all original vertices and edges in the main bundle. Between consecutive
representatives insert a new vertex on side B adjacent to both. For n=0 use a
single unconstrained dummy main vertex on side A instead.

The main induced subgraph is nonempty and connected. These two-edge paths
preserve bipartiteness. Introduce the six palette vertices, with ai on side A
and bi on side B and with the palette edges above. Each is its own singleton
bundle in the specified order. For each original vertex v and color j absent
from L(v), add an edge from v to the opposite-side palette vertex of color j.
The seven bundles partition the vertices; all are connected, and all added
edges cross the stated bipartition. Empty source lists do not invalidate the
output; they simply attach a vertex to all three opposite palette vertices.

The implementation orders original vertices first, then connector or dummy
vertices, then the palette. Its component bipartitions and sorting are
deterministic. Graph size does not depend on source satisfiability.

## YES direction

Given a valid source coloring, retain its colors on original vertices. Each
connector has at most two endpoint colors to avoid, so it can take a color
from {1,2,3}. An empty-source dummy takes color 1. Color the palette by d.
All forbidden-color edges are proper because the source respects its lists.
The main-bundle maximum is at most 3, so total cost is at most 5823. Thus every
source YES instance maps to a target YES instance.

## NO direction and arbitrary-witness recovery

Take any accepted target coloring. The palette lemma forces its six palette
colors to d and its main colors to lie in {1,2,3}. Each forbidden-color edge
then excludes exactly the corresponding absent list color from its original
endpoint. Original edges remain present. The first n colors therefore give a
proper source list coloring. The extractor returns precisely this prefix after
validating the supplied target witness. This proves the contrapositive NO
direction and recovery from every accepted witness, not just solver-generated
examples. For n=0, the empty prefix is a valid source witness.

## Malformed strings

The forward parser checks the entire source schema, edge and list restrictions,
and bipartiteness. Python's decimal-integer digit limit is disabled before
decoding; arbitrary-length numeric tokens are read before the explicit schema
and list-length checks. This avoids imposing a runtime-dependent restriction
on the mathematical input language. An invalid JSON string or source value is mapped by running
the same construction on one vertex with an empty list. This yields seven
vertices, the palette edges, and a main vertex adjacent to b1,b2,b3. It is a
legal target graph, but the palette lemma leaves its main vertex no available
color, so it is NO. Since malformed strings are outside the source language,
the reduction is total. Recovery has no obligation on these NO outputs.

## Resource bounds and membership

If n>0 and the source has c components, the output has n+c+5 <= 2n+5 vertices
and at most m+2(c-1)+3n+6 <= m+5n+4 edges. For n=0, or malformed input, it has
seven vertices and constant size. All weights and the threshold are constants.
Every output identifier uses O(log(n+2)) bits, giving
O((n+m+1) log(n+2)) output length for valid inputs. Parsing, graph traversal,
sorting and writing are deterministic polynomial-time operations; a conservative
bit bound polynomial in the source length covers integer validation and sorting.
The constructor performs no coloring search or oracle call.

Recovery reconstructs this graph, verifies its coloring and returns n integers.
It is polynomial in the encoded source and supplied witness lengths, including
the bit cost of reading colors. Valid witnesses have original colors at most
three. More generally, every color of any target YES witness is at most 5823,
because all weights are positive and every vertex is in a bundle. Thus target
membership is in NP by direct graph, partition, properness and cost checks.

## Literature obligations

The screening question records the closest bundle results and their different
hypotheses. The original citation chain there uses the ambiguous notation
“3-List Coloring”, which can mean lists of size three with unbounded palette.
For the hardness consequence use Chlebík and Chlebíková,
[Hard coloring problems in low degree planar bipartite graphs](https://doi.org/10.1016/j.dam.2006.03.014),
Theorem 5, printed pp. 1962–1964, explicitly bounds the union of all lists to
three colors; its palette {0,1,2} can be relabeled {1,2,3}. The
[author-hosted full text](https://pure.port.ac.uk/ws/portalfiles/portal/1952693/1_s2.0_S0166218X06001260_main.pdf)
was inspected on 2026-09-16. It reduces Cubic Planar Monotone 1-in-3SAT through
list-constrained variable and clause gadgets. Its 3-regular planar bipartite
inputs are contained in our source domain. This supports the NP-hardness
consequence without the ambiguous earlier citation. Novelty and significance
of the fixed connected-bundle conclusion remain independent review obligations.

The six-vertex palette graph and missing-color neighbors are prior techniques.
Murat and Paschos, *The Probabilistic Minimum Coloring Problem*, Proposition 1,
uses the same off-diagonal bipartite palette in a different probabilistic
objective; see the [indexed primary text](https://citeseerx.ist.psu.edu/document?doi=f5131b993afdf2a4716b9f655e3c297cdc7119cc&repid=rep1&type=pdf).
Chlebík–Chlebíková Theorem 6 encodes absent list colors using precolored
neighbors. Bodlaender, Jansen and Woeginger,
[Scheduling with incompatible jobs](https://doi.org/10.1016/0166-218X(94)90009-4),
Section 2, Theorem 1, already retains bipartite coloring hardness with three
designated precolored vertices. None of these mechanisms is claimed new here.

The proposed contribution is the fixed weighted maximum-over-bundles endpoint
with seven induced-connected parts, six of them singleton, and fixed threshold.
The weighted earliest-deviation inequality and connected-core extension justify
that endpoint; ordinary precoloring hardness alone does not establish its cost
constraint. The initial independent review checked these comparisons and judged
the contribution modest. Its coverage and retrieval limits, including failed
full-PDF access for the probabilistic-coloring source, are retained in
[the review](../reviews/initial/review.md). No broad novelty or acceptance claim
follows from this bounded literature coverage.
