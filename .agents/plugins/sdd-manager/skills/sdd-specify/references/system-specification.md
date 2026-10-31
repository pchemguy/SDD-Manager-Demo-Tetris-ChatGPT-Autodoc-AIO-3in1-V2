# Complete system specification

`docs/dev/SPEC.md` and its focused children define the complete intended current system. A reader should be able to understand required outcomes without conversation history, a change document, or implementation logs. For a new project, describe the system that is to be built from scratch; for an existing project, distinguish verified behavior from intended corrections and do not fill evidentiary gaps by guessing.

## Root

Keep `SPEC.md` compact but substantive. Include the relevant:

- purpose and intended outcomes, principal users and system context, scope and non-goals;
- terminology and guarantees used across components;
- short orientation to the architectural blocks and permitted interactions, linking to design documents for structural detail;
- system-wide public, cross-component, data, lifecycle, compatibility, and error contracts;
- mapping to focused child specifications, if any;
- objective end-to-end acceptance conditions, including important boundaries and failures.

PROJECT owns the fuller project brief; ARCHITECTURE and DECOMPOSITION own the structural rationale. Include only the structural facts needed to make behavior intelligible. Do not copy design documents into SPEC or reduce its root to a table of contents.

## Design traceability

SPEC defines the observable guarantees the selected structure must satisfy. Link relevant contracts to responsible components in DECOMPOSITION and, where consequential, their consumers and architectural constraints. Cross-component guarantees have a canonical behavioral owner with links to participating boundaries; do not repeat the contract in every component description or require one specification per component.

Design supplies responsibility, dependency, extension, and verification seams; SPEC settles precise success/failure behavior and acceptance. Feedback is bidirectional: a contract can reveal an inadequate structural boundary, and design analysis can reveal an unresolved behavioral obligation. Surface the conflict to its requirement or design owner and resolve the accepted decision before dependent work. Do not silently redesign in SPEC, invent a requirement to fit the structure, or introduce a separate mapping artifact solely for traceability.

## Focused children

When distinct contracts have substantial independent detail, place them under `docs/dev/spec/` with stable semantic names. Split by cohesive behavior, component contract, public interface, external protocol, or persistent representation, rather than implementation phase or arbitrary requirement codes. Define each child's scope and relationship in its parent. The child owns detailed requirements; the root retains only the broader system guarantee and route to the child.

At the appropriate owner, define required successful behavior, inputs and outputs, invariants, rejection and error semantics, boundary cases, state and lifecycle, resource ownership, data formats, compatibility, and nonfunctional guarantees when those materially affect correct use. Specify externally observable outcomes and constraints, not an internal algorithm unless the algorithm itself is part of the accepted contract.

## Acceptance and review

Separate target-platform behavior and artifact requirements from the facilities used to verify them. Apply [cross-platform artifact and native-verification scope](../../sdd-verify/references/check-selection.md#cross-platform-artifacts-and-native-verification): unavailable native execution is outside verification scope by default, without deleting the target deliverable or promising unobserved compatibility. Do not invent a native-environment acceptance gate from a platform name.

Write acceptance conditions that can be assessed objectively: meaningful success cases, failures, edge cases, and interactions. A test command or an implementation task is not a behavioral requirement. Avoid prescribing redundant tests at every layer; verification planning owns check selection and execution.

Confirm every accepted requirement has one canonical owner, all parent/child links resolve, contracts are mutually consistent, and important behavior can be checked. Label intentionally deferred decisions and their limits. A missing choice that would force SPEC to invent public behavior is a blocker, not a license to complete the prose by assumption.

Read the main SPEC and affected children as a standalone end-state contract. Remove wording that narrates what an earlier draft or implementation did; express accepted behavior directly. Apply the detailed editorial check in [review](review.md).

## Finish the preparation boundary

Authoring includes the required SPEC/design QC gate in [review](review.md). Correct in-scope issues, resolve consequential decisions with their owners, recheck and produce the adjacent root review report before dependent PLAN authoring. A draft specification or report is not Ready. Complete the requested specification boundary without automatically starting planning.
