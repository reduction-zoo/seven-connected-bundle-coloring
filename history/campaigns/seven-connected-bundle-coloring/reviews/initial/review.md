# Independent initial review

Date: 2026-09-16. Decision: **REVISE**.

The graph-level reduction and arbitrary-witness recovery are correct on legal
source instances. The executable is not total on malformed source strings,
contrary to the fixed question. Repair that failure and acknowledge the older
palette construction in the literature discussion before advancing. I do not
find evidence justifying a stop as an already proved fixed-seven-bundle theorem.
Novelty attaches only to the restricted bundle conclusion, not to palette
forcing or the underlying list/precoloring encoding.

## Correctness

The palette proof works for all positive integer colors, not merely three-color
or optimal witnesses. The six margins
`w_i - 2 - sum_{j>i} w_j(d_j-1)` are respectively
`3734, 662, 150, 22, 6, 2`, all positive. At the earliest differing coordinate,
the previously fixed opposite-side neighbors exclude every smaller color.
Consequently an accepted witness fixes the palette to `(1,1,2,2,3,3)` and
bounds the nonempty seventh bundle by three. No hidden optimality premise is
needed.

The original vertices retain their edges. Their edges to the opposite-side
palette encode precisely the colors absent from their lists. Thus a source
witness extends by coloring each connector with a color missing from its two
endpoints; conversely every accepted coloring restricts to a source witness.
The extractor at `work/algorithm.py:67–80` checks the actual reconstructed target
and returns precisely this restriction. The empty source is correctly handled
by a dummy vertex and empty recovery. Empty lists correctly produce NO targets.

For each source component the least vertex is put on side zero; each connector
then joins two side-zero representatives. This keeps the graph bipartite and
makes the seventh induced subgraph connected. Six singleton bundles are
connected regardless of their external edges. IDs are consecutive, palette IDs
follow the core, and no added edge is a loop or repeated edge. Deterministic
component orientations remove the arbitrary global orientation of a bipartition.

The stated counts `n+c+5` vertices and at most `m+5n+4` edges for nonempty valid
sources are correct. Fixed weights, threshold, and O(log(n+2))-bit IDs give the
claimed output-size bound. Sorting means polynomial time, not a claimed linear
running time. Explicit list arrays bound n by source encoding length before
allocation. Recovery is polynomial in source-plus-witness length; accepted
witness colors are bounded constants. Target legality and witness verification
are polynomial, so the NP membership argument is sound.

### Blocking implementation finding: malformed-input totality

Location: `work/algorithm.py:88–89`, and `work/proof.md`, section “Malformed
strings,” especially its inference that the reduction is total.

The code catches `json.JSONDecodeError` only. In the installed Python runtime,
this 5,028-character input raises a different exception:

```python
raw = '{"n":' + '9' * 5000 + ',"edges":[],"lists":[]}'
```

It is outside the source language because its claimed vertex count does not
match its empty list array. The required result is the fixed legal NO target.
The current program instead exits with status 1 and no target:

```text
ValueError: Exceeds the limit (4300 digits) for integer string conversion:
value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit
```

Required correction: make forward decoding route this malformed source string
to the existing legal NO construction. Keep the legal input language and
accepted witness guarantees unchanged. Audit the other concrete decoder failure
modes against the same totality obligation; do not silently alter the source
language. This is a repairable implementation defect, not a graph-theorem
counterexample. A 20,000-level nested-array control did return the fixed NO
output in this environment; it is not reported as a failure.

## Independent executable evidence

`targeted_checks.py` imports no candidate or checker implementation. It executes
both candidate modes in fresh processes, checks graph simplicity, bipartiteness,
partition and induced connectivity by its own traversals, decides source
instances by exhaustive list assignments, and solves actual target outputs with
Z3 using exact nested maxima. It exhausts all accepted target witnesses of five
small cases, rather than trusting one intended witness.

Command:

```text
python3 campaigns/seven-connected-bundle-coloring/reviews/initial/targeted_checks.py
```

`targeted-results.json` records five matching source/target decisions, including
two NO cases, and all 16 accepted target colorings recovered successfully. The
empty source has three accepted target witnesses; three isolated pinned
vertices have one; an unrestricted three-vertex path has twelve. The fixed NO
output was also independently checked. The oversized-integer failure is saved
in the same report. The script reports this defect rather than masking it with
an expected passing assertion.

I inspected the existing three raw campaign results: 10/160/74 cases and
9/347/112 recoveries respectively, agreeing with verification.md. Those are
reused evidence, not independent reviewer reruns. Neither those checks nor my
finite exhaustive examples substitute for the general argument above.

## Novelty audit

All searches and primary-text inspections below were performed on 2026-09-16.

1. Ito et al., *Minimum Sum Coloring with Bundles in Trees and Bipartite
   Graphs*, [ISAAC 2025 primary text](https://drops.dagstuhl.de/storage/00lipics/lipics-vol359-isaac2025/html/LIPIcs.ISAAC.2025.40/LIPIcs.ISAAC.2025.40.html),
   Theorems 8, 10–13, Section 4 construction, and Section 5; also
   [full version](https://arxiv.org/html/2509.15080v1), Sections 4.1 and 5.
   Their hardness constructions do not impose connected bundles. Their
   connected-partition algorithm is for trees. Neither result specializes to
   this target. The unrestricted connected-partition problem already includes
   singleton-bundle sum coloring; the contribution must therefore be the
   constant-bundle restriction. Their published classification supports the
   relevance of that distinction but is not a novelty certificate.

2. Chlebík and Chlebíková, [author-hosted primary paper](https://pure.port.ac.uk/ws/files/1952693/1_s2.0_S0166218X06001260_main.pdf),
   Theorem 5, printed pp. 1962–1964, and Theorem 6, p. 1965.
   Theorem 5 explicitly uses a global palette of three colors and establishes
   hardness on simple planar cubic bipartite graphs. It supports the campaign's
   source NP-hardness without a list-size/global-palette ambiguity. Theorem 6
   encodes missing list colors using precolored neighbors. This part of the
   candidate is a standard encoding, not new machinery.

3. Bodlaender, Jansen and Woeginger, *Scheduling with incompatible jobs*,
   [DOI](https://doi.org/10.1016/0166-218X(94)90009-4),
   Section 2, Theorem 1, printed p. 221 onward. The publisher fetch was blocked;
   the [indexed primary-paper text](https://www.researchgate.net/publication/226484106_Scheduling_with_incompatible_jobs)
   was inspectable. It proves hardness of bipartite three-color extension with
   one designated vertex per color. Section 4, Theorem 4's proof explicitly
   uses the three anchors in one bipartition class. This already establishes
   that a constant precolored interface can retain hardness. It does not state
   this bundle objective, weights, connectivity restriction, or threshold.

4. Murat and Paschos, *The Probabilistic Minimum Coloring Problem*,
   [primary-paper PDF indexed text](https://citeseerx.ist.psu.edu/document?doi=f5131b993afdf2a4716b9f655e3c297cdc7119cc&repid=rep1&type=pdf),
   Proposition 1 and its construction following Figure 1; also
   [author-uploaded text](https://www.researchgate.net/publication/220752625_The_Probabilistic_Minimum_Coloring_Problem).
   This older construction adds three opposite-side anchors and exactly the
   off-diagonal edges `v_i u_j` for `i != j`, with geometrically separated
   anchor probabilities. Thus the six-vertex palette graph is demonstrably
   not new. Its objective sums probabilities of nonempty color classes, rather
   than weighted maxima over predetermined bundles. Its theorem does not
   immediately instantiate to the fixed target; translating it requires the
   candidate's deterministic numerical forcing and connected-core argument.
   Full PDF retrieval failed, so this comparison uses the displayed primary
   Proposition 1 construction, not an asserted inspection of its entire proof.

Searches included `"coloring" "connected bundles" bipartite`,
`"Minimum Sum Coloring with Bundles" connected`,
`"Minimum Sum Coloring with Bundles" "2026" hardness connected`,
`"precoloring extension" bipartite "six" vertices`,
`"bipartite" "precoloring" "three vertices" NP complete`,
`"weighted coloring" "connected" bundles seven`,
`"Scheduling with incompatible jobs" "Theorem" "precolored"`, and
`"The Probabilistic Minimum Coloring Problem" "K" "precoloring"`.
No exact prior theorem with the fixed connected-bundle endpoint was identified.
This is bounded coverage; unpublished work and unindexed equivalents remain
unresolved. The generic NP-completeness of precoloring is not itself a theorem
for this objective. Conversely, absence of the exact constants in a search is
not evidence of novelty.

**Novelty judgment:** the restricted complexity conclusion is plausibly distinct
within the inspected primary literature; the core palette and list encoding
are prior techniques. Update `work/proof.md`'s literature discussion to cite
these precursors and state the precise remaining contribution. Do not describe
the palette construction as original. A stronger novelty claim is unsupported.

## Significance judgment

The concrete addition is hardness with exactly seven connected bundles, six
of them singleton, fixed numerical weights and fixed threshold. It shows that
connected bundles and constant bundle count do not together remove hardness,
even with only one non-singleton bundle. That is a modest but meaningful
restriction result relative to the fixed question's acceptance criteria.

The proof is a short combination of known precoloring mechanisms, numerical
forcing, and neutral two-edge connectors. It does not determine the minimum
number of connected bundles, settle the unweighted threshold, or discover a
new palette mechanism. I would accept its significance only as this narrow
complexity-boundary observation, not as a broad breakthrough or a novel gadget
method. The old precoloring theorems alone omit the cost and induced-connectivity
requirements, so simplicity alone is not sufficient evidence to classify this
exact conclusion as a known result. No change of question is needed for the
identified repairs.

## Required follow-up

Repair forward parser totality, add the missing prior-art comparison, and rerun
the targeted malformed-input check plus the campaign's required relevant
checks. The mathematical construction can remain unchanged. A follow-up review
can reuse the graph proof and witness evidence here and inspect those repairs.
No advance or expert-review-ready status is granted by this report.
