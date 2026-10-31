# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, selected by the user's 2026-10-31 request.
- Scope: complete browser Tetris target, then Windows Electron, then Chromium and Firefox sidebar extensions together.
- Approval basis: PROJECT approval remains pending; subsequent document checkpoints through TASKS are preapproved by autodoc. Stop after DOCS-008 before package QC. Implementation has not started.
- Tracking: enabled for documentation and implementation by existing root AGENTS.md. Preparation milestone 1 and issues 1 through 9 were created and their exact content and associations read back before repository modification.
- Publication: every owned commit is pushed and its exact remote ref read back.
- Reporting: concise Standard; Minimal and Explicit are available on request.
- Next boundary: publish PROJECT proposal and await human approval of its scope and proposed material decisions.

## Scope sequence

One preparation pass covers the entire user-supplied scope. Delivery must start with a playable classic browser baseline, add bounded gameplay increments, deliver session-only settings before persistence, finish browser UI layout, then deliver Windows, then both extensions. This is delivery sequencing within one document pass.

## Decisions and document evidence

| Task | Evidence and decision basis |
| --- | --- |
| DOCS-001 | All four root files existed and are retained byte for byte against initial main b6cecff4fc3bc367bab2602a57972d54cdae7738. Provenance scaffold copied unchanged from bundled 0.16.0 assets; published seed 506cc66a40f1549a8afd0320a97c5a2e1303f767 and ignore-rule preservation correction 0202fd9; explicit published main merge 407c29fa92aa0b5788352733b76a3fb8e63ebd7f. Initialization commit submits this record, task completion and HANDOFF together. Issue 1 closure follows verified publication. |
| DOCS-002 | PROJECT proposal SHA-256 c5489b65511136ca2ad28f14f20c9e2c17ccf2c091a9ba7a8f431e964ef74f35; human acceptance pending. Checked scope against the complete user request, separated principal intent from architecture/SPEC detail, and kept material choices explicitly proposed. README disclosure and usage links added. DOCS-002 remains unchecked. |
| DOCS-003 through DOCS-008 | Not started; document checkpoints preapproved after PROJECT acceptance. |
| DOCS-009 | Not selected; remains pending at the autodoc stop. |

## Material decisions for approval

Proposals, not human-confirmed requirements: hide a straddling ghost if any occupied ghost cell is above the midline; delay begins on grounding and resets only on lift-off; pause freezes game time; disable hold while penetrator is active; reject invalid URL/cookie values independently and fall through to the next valid source; extension closure/focus loss pauses and reopening requires explicit resume. Detailed contracts and defaults will be specified after brief acceptance.

## Initialization

- Root files retained: AI_DISCLOSURE.md, SDD-MANAGER.md, AGENTS.md, SKILL_DISCOVERY_PROTOCOL.md. No root copy was needed. All-present state permits continuation.
- Manual provenance: default enabled; two-file scaffold on retained design-docs/ai-logs, merged explicitly into main before design-docs/main creation. No transcript generated or retrieved.
- Existing ignore rules preserved alongside *.tkn. Credential input is excluded and untracked.
- Git baseline: clean initial main b6cecff4fc3bc367bab2602a57972d54cdae7738. No prior workflow or product task records exist.
- Execution: Linux bash, Node 24.22.1, Python 3.12.14, native Git. Windows native execution has not been checked. gh is unavailable; GitHub API covers milestone operations absent from the connector.
- Reset: none.

## Pending transitions

Initialization f992d92 published and issue 1 closed/read back. PROJECT proposal publication follows; verify remote state before presentation. PROJECT approval, dependent documents, package QC and preparation integration remain pending. Do not infer later success from this checkpoint.
