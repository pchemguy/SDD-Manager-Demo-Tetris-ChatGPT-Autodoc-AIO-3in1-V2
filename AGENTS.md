# Agent instructions

## Specification-driven development

This project uses the SDD Manager plugin for specification-driven development. If not already in the context, load `PLUGIN.md` from installed location or from `.agents/plugins/sdd-manager/PLUGIN.md` and the coordinator skill entry it references. If neither source is available, report the missing plugin before dependent workflow work.

**Follow the applicable SDD Manager workflows, including human checkpoints, Git publication and integration, and the tracking policy below.**

## Initialization

Execute the [skill and plugin discovery protocol](SKILL_DISCOVERY_PROTOCOL.md).

## Windows shell

On **Windows execution hosts only**, follow [WINDOWS_SHELL_POLICY.md](.agents/plugins/sdd-manager/assets/WINDOWS_SHELL_POLICY.md): CMD syntax, unavailable PowerShell/pwsh, temporary files for script text and shell operations, and the documented tool probe/recovery. This repository policy is independent of the plugin.

## Browser development

When developing or testing browser-based applications or browser extensions, follow [BROWSER_DEV_POLICY.md](.agents/plugins/sdd-manager/assets/BROWSER_DEV_POLICY.md). Prioritize Chromium and include Firefox by default; project documents may specify other choices. Use dedicated, isolated environments.

## Environment diagnostics

When Playwright is selected, follow [Playwright environment guidance](.agents/plugins/sdd-manager/assets/playwright.md) before dependent setup and execution, and when provisioning or browser runtime blocks required checks.

When a Vite-served module worker fails to start, especially from a linked Windows checkout or with an HTML entry response, follow [Vite worker-loading diagnostics](.agents/plugins/sdd-manager/assets/vite-worker-loading.md). Diagnose the loading stage before applying a workaround; this guidance does not apply to every SQLite or worker failure.

## Workflow continuity

For continuation, read `docs/dev/HANDOFF.md` and use `sdd-manage`'s continuity subworkflow to reconstruct later work from current development records and Git. The handoff describes a checkpoint, not necessarily the branch tip. At startup, inspect unfinished workflow branches against their recorded parents and request the continuation branch unless already selected. Preserve the recovered scope, approvals and stopping boundary.

## Human checkpoints

Present each necessary new development document with concise substantive analysis and pause for acceptance before dependent work. Honor the user's requested implementation range and stop when it is complete.

The user may explicitly preapprove future checkpoints at any time. Retain the scope and conditions of that decision, including after interruption; do not repeat a covered approval request. Preapproval does not waive QC, resolve blockers or expand the authorized implementation range.

## Commits and publication

Keep each task's verified result, required evidence and completion checkbox in the same commit. Push every owned commit and verify remote containment before further work or another commit, unless the user explicitly directs local-only or deferred publication.

Use SDD Manager's integration procedure at the authorized complete boundary.

## GitHub tracking

Enable and maintain GitHub tracking for documentation preparation and implementation **by default**. The user may disable tracking, select local-only work or choose another supported backend. Preserve an established choice through interruptions and access failures; copying this template does not reset it.

Follow `sdd-manage`'s preparation and phase-activation workflows for required tracking readiness and lifecycle updates. Reconcile uncertain effects before retrying and report unmet prerequisites before dependent work.

## Project guidance

Maintain project-specific navigation and validated setup/check commands here as they become established. Do not invent commands, paths, requirements or completion claims.

## Application navigation and established checks

Shared rule code lives in src/core, command ownership in src/app, rendering/input in src/ui and shared web composition in src/entries/web.ts, selected by browser.ts and desktop.ts. TASKS and HANDOFF retain actual execution status.

Validated checks: npm run typecheck, npm run build:test, npm run build and python -m pytest. Tests use the pinned requirements-test.txt and a dedicated PLAYWRIGHT_BROWSERS_PATH. Desktop main-process protocol/window/session policy is isolated in platforms/electron and renderer host selection in src/platform/desktop. The desktop uses a locally intercepted HTTPS origin for real Secure/SameSite cookies; custom-scheme cookies are unsupported in the pinned runtime. The opt-in native pytest probe uses Node Playwright and isolated Electron resources/profile; Linux root-test flags never ship as production flags. npm run build now builds browser and desktop renderer outputs; native Windows execution is separate from policy and HTTP shared-renderer checks. Browser tests default to Chromium headless shell; TETRIS_BROWSER=firefox selects the managed Firefox build with the diagnosed process-local content-sandbox recovery for trusted local test pages. Preserve the browser policy above and report native/sidebar coverage separately.

Sidebar composition lives in src/platform/extensions and explicit family entry points in src/entries. Production outputs are dist/extensions/chromium and dist/extensions/firefox; build versions derive from package.json. Coordinator owns storage/ownership, never gameplay time. Tests distinguish test-transport built-panel evidence from opt-in real extension/native sidebar checks. Preserve this distinction in reports and releases.
