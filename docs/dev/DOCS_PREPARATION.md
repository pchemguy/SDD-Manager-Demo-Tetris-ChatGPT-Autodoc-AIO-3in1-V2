# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, selected by the user's 2026-10-31 request.
- Scope: complete browser Tetris target, then Windows Electron, then Chromium and Firefox sidebar extensions together.
- Approval basis: PROJECT and its material proposals were approved by the user reply "k" on 2026-10-31; subsequent document checkpoints through TASKS are preapproved by autodoc. Stop after DOCS-008 before package QC. Implementation has not started.
- Tracking: enabled for documentation and implementation by existing root AGENTS.md. Preparation milestone 1 and issues 1 through 9 were created and their exact content and associations read back before repository modification.
- Publication: every owned commit is pushed and its exact remote ref read back.
- Reporting: concise Standard; Minimal and Explicit are available on request.
- Next boundary: complete ARCHITECTURE through TASKS under autodoc preapproval, stopping before whole-package QC.

## Scope sequence

One preparation pass covers the entire user-supplied scope. Delivery must start with a playable classic browser baseline, add bounded gameplay increments, deliver session-only settings before persistence, finish browser UI layout, then deliver Windows, then both extensions. This is delivery sequencing within one document pass.

## Decisions and document evidence

| Task | Evidence and decision basis |
| --- | --- |
| DOCS-001 | All four root files existed and are retained byte for byte against initial main b6cecff4fc3bc367bab2602a57972d54cdae7738. Provenance scaffold copied unchanged from bundled 0.16.0 assets; published seed 506cc66a40f1549a8afd0320a97c5a2e1303f767 and ignore-rule preservation correction 0202fd9; explicit published main merge 407c29fa92aa0b5788352733b76a3fb8e63ebd7f. Initialization commit submits this record, task completion and HANDOFF together. Issue 1 closure follows verified publication. |
| DOCS-002 | PROJECT proposal SHA-256 c5489b65511136ca2ad28f14f20c9e2c17ccf2c091a9ba7a8f431e964ef74f35; accepted by the user reply "k" on 2026-10-31, retaining the exact proposal bytes from 6a188c6d8c9ffe40319c8e7cce6223e5170676bd. Checked scope against the complete user request, separated principal intent from architecture/SPEC detail, and kept material choices explicitly proposed. README disclosure and usage links added. DOCS-002 closes in this approval commit. |
| DOCS-003 | ARCHITECTURE.md SHA-256 5cbd18628e6de8b7b3887704c0e0f6600b1bc3728d86faf79768e86a8e4ac303. Accepted under autodoc preapproval after user-approved PROJECT. Scoped conformance and document-boundary review passed; report references accompany SPEC, PLAN and TASKS. |
| DOCS-004 | DECOMPOSITION.md SHA-256 f4adaf7c7e11a8bb79222e56b9889534f0ddc7bd1490fc3479d6eea9c044ab78. Accepted under autodoc preapproval after user-approved PROJECT. Scoped conformance and document-boundary review passed; report references accompany SPEC, PLAN and TASKS. |
| DOCS-005 | Not started; autodoc preapproved. |
| DOCS-006 | Not started; autodoc preapproved. |
| DOCS-007 | Not started; autodoc preapproved. |
| DOCS-008 | Not started; autodoc preapproved. |
| DOCS-009 | Not selected; remains pending at the autodoc stop. |

## Approved material decisions

Approved with the brief on 2026-10-31: hide a straddling ghost if any occupied ghost cell is above the midline; delay begins on grounding and resets only on lift-off; pause freezes game time; disable hold while penetrator is active; reject invalid URL/cookie values independently and fall through to the next valid source; extension closure/focus loss pauses and reopening requires explicit resume. Precise scoring, defaults, bindings, formats and non-material contracts remain delegated to the document owners.

## Initialization

- Root files retained: AI_DISCLOSURE.md, SDD-MANAGER.md, AGENTS.md, SKILL_DISCOVERY_PROTOCOL.md. No root copy was needed. All-present state permits continuation.
- Manual provenance: default enabled; two-file scaffold on retained design-docs/ai-logs, merged explicitly into main before design-docs/main creation. No transcript generated or retrieved.
- Existing ignore rules preserved alongside *.tkn. Credential input is excluded and untracked.
- Git baseline: clean initial main b6cecff4fc3bc367bab2602a57972d54cdae7738. No prior workflow or product task records exist.
- Execution: Linux bash, Node 24.22.1, Python 3.12.14, native Git. Windows native execution has not been checked. gh is unavailable; GitHub API covers milestone operations absent from the connector.
- Reset: none.

## Pending transitions

DOCS-001 through DOCS-003 publication and issue closure/readback are verified. This DOCS-004 completion commit requires publication and issue 4 closure/readback before dependent progression. Whole-package QC, preparation integration and implementation are not selected. Stop after DOCS-008.
