# Round 1 — weighted palette and connected list-coloring core

Status: completed on 2026-09-16. One round, one construction family.
Original allocation: at most 40 rounds. Latest continuation allowance: 20 further
rounds; no new round was needed to finish the interrupted attempt.

## Plan

Hypothesis: the fixed six-vertex weighted palette, forbidden-color edges and
neutral two-edge component connectors give the complete rule in question.md.
Use the prepared oracle. First run all ten prepared injections, then 160 seeded
source instances with at most seven vertices, and test recovery from up to three
independently generated accepted colorings per YES instance. This is one
construction family. Input-validation repairs do not start another round.

The first discriminating check is arbitrary-witness recovery under the fixed
threshold, including disconnected and malformed inputs. A mismatch requires
diagnosis before further testing. Passing finite tests supports proceeding to
general proof and independent verification, not correctness by itself.

Experience retrieval: searched bundles, precoloring, lexicographic and palette
entries during screening; none had applicable premises. No inherited lemma is
being treated as established evidence. The screened inequalities and connector
check are in the question's linked evidence.

Remaining obligations include complete input handling, both implications,
polynomial encoding bounds, source-hardness verification and novelty review.
Short-term correctness prospects are high (uncalibrated judgment), because each
constraint has an explicit role and the interface check passed. Novelty prospects
are unknown pending comparison with earlier precoloring constructions.

## Evidence and diagnosis

Preparation passed before this round. The single candidate passes
[ten prepared injections](prepared-check.json), [160 seeded injections](injected-check.json)
and [74 separate verification cases](verify.json). See the current
[verification report](../../work/verification.md) for recovery counts and scope.
The initial suites required no implementation or checker repair. The general proof covers
palette forcing, composition, arbitrary-witness restriction, malformed input
and polynomial bit bounds.

The source-hardness citation needed clarification: bounded list size is not
bounded total palette. Theorem 5 of Chlebík and Chlebíková (2006), inspected in
the primary full text linked in proof.md, supplies the exact global-three-color
source premise. This is a citation audit, not a changed source problem or a new
round. The construction remains unchanged.

Observation: the complete rule passes the declared checks. Cause and confidence:
the budget pins all palette colors, so forbidden-color edges enforce lists;
the general earliest-deviation argument supports this beyond the finite probe.
The independent review then exposed a totality failure on a 5,000-digit integer
token. [Direct reproduction](parser-failure.json) records the parser ValueError.
Its cause is the Python runtime's integer conversion limit before schema
validation, not the graph construction. The initial review is complete. The original candidate is retained in
[parser-defect/algorithm.py](parser-defect/algorithm.py). One implementation
repair disables the decimal digit cap before decoding. Eight raw-input
regressions pass; both required suites pass after repair, as linked in the
verification report. Earlier finite passes did not cover this input family.

Consequence: the repaired rule received an independent
[advance review](../../reviews/parser-and-attribution/review.md). The initial
review's graph proof and finite witness enumeration remain applicable; its
new repair checks pass eight malformed strings and one legal forward/recovery
case. Prior-art comparison narrows the contribution to fixed seven connected
bundles, fixed weights and fixed threshold. The palette itself is not original.

The current [six-page manuscript](../../work/manuscript.pdf) contains native
Typst mathematics and two vector figures. All six final rendered pages were
visually inspected. The first render exposed excessive manual page breaks,
a clipped palette weight, and a Typst subscript attachment error; these were
corrected without changing the reviewed argument. The final language pass
applied how-to-technical-writing directly. Compilation succeeded with Typst
0.15.1. Figure adjacency was checked against the six off-diagonal palette
edges; local connector and list-edge views are explicitly schematic.
The appendix's forward/recovery example was executed and recovered [3].
Evidence is in work/evidence/ and work/figures/checks.json.

Actual scope: one graph construction, 10 prepared injections, 160 seeded
injections (seed 20260916, n <= 7), and 74 separate verifier cases; recovery
counts 9, 347, and 112. Suite counts overlap. One parser implementation repair
followed one confirmed failure; the required 10-case and 74-case suites were
rerun after repair, plus eight new malformed-input regressions. Reviewer checks
are reported separately above and in the initial review. No checker repair or
new mathematical mechanism was required. Manuscript compilation and parser
reruns are not research rounds. Total time and token use are unavailable.

**Experience extraction:** one qualifying entry is
[staged locally](../../work/experience-neutral-coloring-connectors.md): neutral
length-two connectors for bipartite three-color components, with their exact
premises and limitations. A second search of shared entries for palette,
precoloring, lexicographic and component-connector terms found no applicable
existing entry. Intended destination:
`research/experience/neutral-coloring-connectors.md`. Promotion is pending
because the campaign permits writes only within its own directory. Shared
entries created: 0; updated: 0; pending extraction files: 1. The known parser
failure is retained as a regression, not promoted as a mathematical finding.

## Next action

Stop exploration of this fixed question: the full rule, general proof, tests,
independent advance review and inspected manuscript meet the campaign's
completion conditions. Status is ready_for_expert_review, not human-confirmed
novelty or publication acceptance. Expert checking of prior literature is the
remaining assessment step. A different bundle threshold or unweighted theorem
would require a separately screened question; unused rounds do not justify
changing the target.

## Subsequent promotion (2026-09-16)

After the campaign ended, topic selection promoted the locally staged finding
to [the shared collection](../../../../research/experience/neutral-coloring-connectors.md)
and synchronized the board. The pending status above records the original
closeout boundary; current pending entries are zero. No new research round
or additional mathematical result is implied by this promotion.
