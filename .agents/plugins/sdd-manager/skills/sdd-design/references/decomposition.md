# Decomposition

Refine accepted architecture into understandable component responsibilities and collaboration. ARCHITECTURE owns the major arrangement and consequential rationale; DECOMPOSITION owns logical units within it. Use the [document boundaries](../SKILL.md#document-boundaries) comparison when routing overlapping structural concerns. Read only the relevant ARCHITECTURE root and children, existing code or contracts where applicable, and the shared **sdd-conventions** modularity reference. Revisit architecture when decomposition reveals a weak block boundary rather than hiding the conflict in detail.

When a consequential uncertainty needs human-guided comparison, use [exploration](exploration.md) at the affected component/interface depth, then return here. Preserve settled project direction and route an actual architectural change to its owner.

## Document ownership

`docs/dev/DECOMPOSITION.md` is the compact entry point for the logical component model. Identify principal components within each architectural block, their responsibility and non-responsibility, provided and required interfaces at the level needed to assess the design, dependency direction, data or state ownership, lifecycle and failure boundaries when architectural, and relevant verification seams. Give each child document a precise scope and link to it from the root.

Focused children under `docs/dev/decomposition/` may detail a component or coherent area: subcomponents, collaboration, important invariants and design-level interface shape, and how it relates to its parent and peers. A parent defines relationships and shared constraints; a child owns detail. Split only when independent detail justifies it. Avoid duplicating the same normative interface in parent and child.

Interfaces here may be provisional enough to test the architecture for coherence. Link the relevant SPEC owners and consumers when established; a cross-component guarantee can span several structural units without being copied into each. Feed incompatible obligations back to the affected design or requirement owner for an accepted decision. Identify contract details that SPEC must settle; do not present undecided errors, formats, or behavior as final requirements. Do not turn component descriptions into a file inventory, implementation order, or task checklist.

## Existing systems and changes

Inspect actual component boundaries and dependents before proposing changes. For a feature, retain the accepted [FEATURE brief](feature-brief.md) scope and decisions alongside the applicable accepted architecture. `docs/dev/FEATURE_DECOMPOSITION.md` may describe only affected units, altered collaborations and interface boundaries, compatibility needs, and component impact for a scoped architectural revision. Reference unchanged main nodes rather than copying them. It may accompany FEATURE_ARCHITECTURE when both levels change; neither is obligatory for a change that does not affect its level.

Main ARCHITECTURE and DECOMPOSITION describe the coherent intended system after accepted decisions are incorporated. Feature documents serve the proposed delta until **sdd-integrate-feature** incorporates the accepted change into the main documents. Do not leave both contradictory descriptions as current truth.

## Review

For each unit, answer what it does, how it is used, what it depends on, and how its boundary can be checked without inspecting its internals. Inspect dependency cycles and unclear ownership; prefer a focused contract or a genuine combined unit to artificial layers. Check that a later SPEC could define objective behavior for each affected boundary, and that planned implementation could proceed in localized, verifiable changes. Report unresolved design decisions rather than inventing final contracts.

Read the main DECOMPOSITION and affected children as the intended component model. Remove narration of prior drafts or implementations after incorporating a feature; describe each settled boundary and responsibility directly. A feature overlay may describe the proposed change while it is active.
