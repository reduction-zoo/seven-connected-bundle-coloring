# Seven connected coloring bundles

Status: **ready_for_expert_review** (2026-09-16).
Fixed target: [question](question.md).

Result: a deterministic Karp reduction from Bipartite List 3-Coloring to the
specified seven connected bundles with fixed weights and threshold, including
recovery from every accepted target witness. The endpoint is NP-complete.
[Maps](work/algorithm.py), [proof](work/proof.md), [six-page paper](work/manuscript.pdf)
and [Typst source](work/manuscript.typ) are complete. All final PDF pages were
visually inspected; two vector figures match the construction.

Budget: original 40-round allocation; 1 started and 1 completed, 39 unused.
The latest request authorized up to 20 further rounds. This continuation
finished the interrupted round; 0 new rounds were started. Early completion
makes further attempts on the same fixed question unnecessary. Total: one
construction family and one parser implementation repair, not 20 new attempts.

Correctness: [verification](work/verification.md) records 10 prepared cases /
9 recoveries, 160 seeded cases / 347 recoveries, and 74 separate cases /
112 recoveries. After the parser-only repair, the prepared and separate suites
passed again, together with eight raw-input regressions. Counts are not
deduplicated. The [independent follow-up review](reviews/parser-and-attribution/review.md)
advances the rule and adds eight parser checks and a legal recovery check.
No candidate change followed that review. Finite tests supplement the proof.

Novelty: the contribution is the exact fixed connected-bundle endpoint; the
palette and missing-color encoding are known. The [initial review](reviews/initial/review.md)
records primary comparisons and retrieval limits. Significance is modest;
minimum bundle count and the unweighted case remain outside this result.
Expert mathematical and novelty assessment remains outstanding.

Experience: 1 new [shared entry](../../research/experience/neutral-coloring-connectors.md),
0 updated, 0 pending. Promoted during subsequent topic selection after the
campaign ended; the local extraction and original closeout evidence are retained.
The board now records this completed result.

| Round | Result |
|---|---|
| [1](rounds/001/round.md) | Complete: one construction, parser repair, advance review, inspected paper |

Next: expert assessment of this result. No additional exploration is needed
to meet the fixed question. A stronger or different theorem needs a new question.
