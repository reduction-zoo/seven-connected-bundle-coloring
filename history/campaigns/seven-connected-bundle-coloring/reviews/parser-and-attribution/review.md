# Focused follow-up review

Date: 2026-09-16. Decision: **ADVANCE**.

The initial review's two required repairs are resolved. This judgment applies to
the unchanged fixed-seven-connected-bundle theorem and its implemented forward
and recovery maps. It permits proceeding to the manuscript and expert-review
stage; it does not establish publication acceptance or eliminate the recorded
literature-coverage limitations.

## Scope and actual changes

I reread the initial review and current algorithm and proof. A direct diff
against `rounds/001/parser-defect/algorithm.py` contains exactly one insertion:
`sys.set_int_max_str_digits(0)` at the start of the executable entry point,
before either JSON decoder. The graph construction, source schema, fixed NO
instance, and witness extractor are unchanged. I therefore reuse the initial
review's general correctness audit and its independent complete enumeration of
all target witnesses on the five small cases.

The proof now explains the decoder setting, attributes the palette graph to
Murat–Paschos Proposition 1, the missing-color neighbor technique to
Chlebík–Chlebíková Theorem 6, and constant-anchor bipartite precoloring hardness
to Bodlaender–Jansen–Woeginger Theorem 1. It confines the contribution to the
specified weighted connected-bundle endpoint. These changes address the initial
attribution finding without changing the question.

## Correctness and repair verification

Disabling the decimal digit cap lets the decoder read the reported long integer.
The existing explicit count/list-length check then rejects its source schema
before graph allocation and returns the required fixed legal NO instance.
Large decimal conversion remains polynomial in token length; the setting does
not affect the graph size or output encoding bound. The legal source and target
languages and the premise of arbitrary accepted target witnesses are unchanged.

My new `check_repair.py` invokes the candidate in fresh processes and imports no
candidate or campaign checker implementation. It independently specifies the
seven-vertex fixed NO graph. Eight malformed inputs return exactly that graph:
the original 5,000-digit count, its negative counterpart, 10,000-digit endpoint
and color tokens, a 30,000-level array, its truncated form, an overflowing
numeric exponent, and trailing JSON. A legal singleton source pinned to color
three also passes forward construction and recovery from a directly validated
target witness with cost exactly 5823. Results are in `results.json`.

Command:

```text
python3 campaigns/seven-connected-bundle-coloring/reviews/parser-and-attribution/check_repair.py
```

I also inspected `rounds/001/parser-check.json` (eight legal NO outputs),
`prepared-after-parser-repair.json` (10 cases, nine recoveries), and
`verify-after-parser-repair.json` (74 cases, 112 recoveries). The focused check
ran on Python 3.14.7. There is no remaining demonstrated parser failure in the
reviewed executable. These finite checks support the repair; the initial general
proof remains the basis for YES/NO equivalence, arbitrary-witness recovery,
bipartiteness, bundle connectivity, deterministic execution, and bit bounds.

## Novelty

The initial primary-literature comparisons, URLs, theorem locations, search date,
and access limitations remain applicable and are incorporated by reference to
`../initial/review.md`; no repeated literature search was needed for an unchanged
mathematical construction. The new attribution accurately distinguishes the
old mechanisms from the claimed endpoint. Within those examined sources, none
states or directly specializes to the fixed weights, threshold and seven
induced-connected bundles here. Moving from precoloring to that endpoint needs
the numerical forcing argument and the connected-core extension, both proved.

I support advancing the narrow endpoint novelty claim for expert assessment.
This is a comparison against identified prior results, not an inference that
missing search hits prove originality. Unindexed equivalent work and the
previously documented incomplete full-PDF retrieval remain explicit coverage
limits. No originality claim for the six-vertex palette is supported or made.

## Significance

The result establishes hardness with a constant number of connected bundles,
fixed weights and threshold, and only one non-singleton bundle. That modest
restriction result meets the fixed question's significance criterion. The
revised proof makes no claim to determine the minimum bundle threshold, solve
the unweighted case, or introduce a new palette mechanism. There is no reason
to weaken or change the fixed question, and no remaining revision requirement
from this focused review.
