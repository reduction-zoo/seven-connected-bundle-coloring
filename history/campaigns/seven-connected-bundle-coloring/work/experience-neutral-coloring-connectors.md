# Neutral connectors for a connected bipartite coloring bundle

Tags: coloring, bipartite, connected-bundle, component-connector, witness-recovery.
Intended shared destination: `research/experience/neutral-coloring-connectors.md`.
Pending promotion: the campaign write boundary permits only campaign-local files.

## Claim and applicability

For a bipartite list-coloring source with global palette {1,2,3}, independently
orient each component so its chosen representative lies on side A. Join consecutive
representatives by paths of length two through fresh side-B vertices whose
available palette is all three colors. This makes the union connected and
bipartite without changing whether the original vertices admit a list coloring.
Every source coloring extends, because each new vertex avoids at most two
colors. Every target coloring restricts to a source coloring.

Apply this when all original vertices must belong to one induced-connected
bundle and fresh connector vertices may join that bundle. A separate mechanism
must already restrict the bundle's accepted colors to the three-color palette.
The connector argument does not itself supply that restriction or prove hardness.
It assumes free component orientations and freely colorable connector vertices.
It does not preserve arbitrary degree bounds, extra connector lists, or prescribed
absolute sides. With only two available colors, a length-two path instead forces
equal endpoint colors and is not neutral for independently colored components.

## Evidence and status

This is a standard elementary extension fact used in a complete reduction,
not a claimed new coloring lemma. The general proof and its composition with
weighted palette forcing appear in [the campaign proof](proof.md).
[Round 1](../rounds/001/round.md) records the construction and tests, including
disconnected source instances and arbitrary-witness recovery.
The [initial independent review](../reviews/initial/review.md) checks the component
orientations, both implications and connected partition; the
[follow-up review](../reviews/parser-and-attribution/review.md) advances the
repaired complete rule. These are agent reviews, not independent human validation.

## Consequence for search

Before designing a connectivity gadget for three-color list reductions, check
whether unrestricted length-two connectors satisfy the actual target conditions.
If so, connectivity can be imposed with one vertex per component boundary and
without synchronizing component colors. Keep the palette-forcing proof separate:
accepted target witnesses, not only intended colorings, must have the required
color bound before restriction is valid.

## Use history

Extracted on 2026-09-16 from the completed construction in this campaign.
There are no subsequent uses or measured search benefits. No existing shared
entry matched the applicable premises in the recorded retrieval.
