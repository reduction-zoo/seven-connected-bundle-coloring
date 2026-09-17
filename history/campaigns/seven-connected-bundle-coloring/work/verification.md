# Verification of the complete rule

Both executable maps and the general proof are present. The initial review
found a parser totality defect on a 5,000-digit integer token; the original
[reproduction](../rounds/001/parser-failure.json) is retained. Disabling the
runtime decimal digit cap before decoding repairs this defect without changing
the graph construction or witness recovery. The [eight raw-input regressions](../rounds/001/parser-check.json)
all produce legal NO targets. The repaired candidate passed the
[prepared suite](../rounds/001/prepared-after-parser-repair.json) (10 cases,
9 recoveries) and [separate verifier](../rounds/001/verify-after-parser-repair.json)
(74 cases, 112 recoveries). The seeded result below predates this parser-only
repair and is retained as evidence for the unchanged graph construction.
Neither oracle imports the candidate. Counts are not deduplicated.

| Check | Evidence | Result |
|---|---|---|
| Prepared injection | [Raw output](../rounds/001/prepared-check.json) | 10 cases; 9 recoveries |
| Declared seeded injection | [Raw output](../rounds/001/injected-check.json) | 160 cases; 126 YES, 34 NO; 347 recoveries |
| Separate verification | [Raw output](../rounds/001/verify.json) | 74 cases; 49 YES, 25 NO; 112 recoveries |

Commands, from the repository root:

    python3 campaigns/seven-connected-bundle-coloring/work/check.py --candidate campaigns/seven-connected-bundle-coloring/work/algorithm.py
    python3 campaigns/seven-connected-bundle-coloring/rounds/001/inject.py
    python3 campaigns/seven-connected-bundle-coloring/work/verify.py --candidate campaigns/seven-connected-bundle-coloring/work/algorithm.py

The prepared source oracle uses list constraints in Z3. The separate verifier
enumerates source list assignments exactly; its target solver uses nested exact
maximum expressions, rather than the prepared oracle's auxiliary upper bounds.
Both check graph restrictions and actual coloring cost directly. Target solver
witnesses, including alternate colorings, are supplied to the extractor in fresh
processes and compared with the source witness predicate.

Seeded tests use at most seven source vertices. Separate tests cover all pairs
of lists from {},{1},{2},{3},{1,2},{1,2,3} on two vertices with and without an
edge, plus empty and disconnected pinned cases. Invalid schema and non-bipartite
source controls occur in the prepared suite. Finite tests do not establish
general correctness, novelty or significance. Focused independent re-review of the parser repair and prior-art attribution
[advanced the rule](../reviews/parser-and-attribution/review.md). Its independent
checks passed eight malformed inputs and one legal forward/recovery case;
its initial review checked five decisions and all 16 accepted target witnesses.
