# Repository layout and ownership

## Allocation model

This is the intended source layout for the [architecture](ARCHITECTURE.md), [components](DECOMPOSITION.md) and [delivery plan](PLAN.md). Paths are introduced by their owning implementation tasks; this document does not claim they already exist. Keep shared code independent of host APIs and keep generated archives out of tracked source.

| Path | Canonical ownership and boundary |
| --- | --- |
| package.json and package-lock.json | Tooling/dependencies/scripts and one authoritative application version. Generate host manifest versions from it. |
| tsconfig*.json and vite.config.ts | Shared TypeScript/build configuration and host entry build targets; no gameplay rules. |
| index.html | Static browser entry and shared application mount. |
| src/core/ | Immutable game types, geometry, source, SRS/landing and reducer/time rules; no DOM, Node, storage or Electron imports. |
| src/app/ | Controller/command queue, settings model, leaderboard, snapshot validator and host-port types. Import core and codec contracts; no host-global access. |
| src/ui/ | Canvas drawing, DOM panels, keyboard/focus mapping, accessible status and shared styles. Consume application snapshots and callbacks. |
| src/codecs/ | JSON parser/schema integration and SQLite codec/loader. Decode to the shared candidate model; no live-state writes. |
| src/platform/browser/ | Cookies, query/history, clock, IDs/UTC time, download and file-input implementations. |
| src/platform/desktop/ | Renderer-side composition for the app origin and desktop lifecycle; no unrestricted IPC. |
| src/platform/extensions/ | Local/session stores, runtime messaging, ownership/snapshot protocol and browser API normalization. No background game loop. |
| src/entries/ | Browser, desktop and extension composition roots, selecting host ports and shared UI. |
| platforms/electron/ | Electron main-process source and fixed secure protocol/window/session policy; compile to packaged main entry. |
| platforms/extensions/chromium/ | MV3 manifest template, action/side-panel service-worker entry and Chromium-specific assets. |
| platforms/extensions/firefox/ | Firefox manifest template, sidebar/action/background entry and Firefox-specific assets. |
| schemas/tetris-save.schema.json | Canonical version-1 JSON Schema distributed with browser/desktop/extensions after file support. |
| public/ | Static project-owned icons and assets; third-party runtime files are copied from locked dependencies during build. |
| tests/unit/ | Pytest rule/controller/settings/leaderboard tests using deterministic Node drivers. |
| tests/codecs/ | Pytest JSON/SQLite validation, independent sqlite3 inspection, round-trip and mutation-guard scenarios. |
| tests/browser/ | Python Playwright pytest integration tests for browser/panel UI, focus, layout and files. |
| tests/platforms/ | Pytest desktop protocol/window policy, extension API adapters, lifecycle/storage ownership and package checks. |
| tests/support/ | TypeScript CLI drivers compiled separately for pytest subprocess use; deterministic fixture builders and shared Python helpers. Never copy test drivers into runtime bundles. |
| tests/fixtures/ | Small valid/invalid source-controlled interchange and board fixtures; no secrets or user data. |
| requirements-test.txt and pytest.ini | Pinned Python test dependencies and test selection conventions. All tests run through pytest; compiler/linter/build/package tools remain separate checks. |
| scripts/ | Cohesive build/package/release verification utilities, including actual asset-name enforcement and checksum/readback operations. ASCII-only script source. |
| .github/workflows/ | Linux/browser CI and applicable Windows/package checks with declared scoped permissions. Tests and packaging follow project environment policy. |
| docs/ | User install/control/file guides and development owners under docs/dev; document supported delivered behavior separately from plans. |
| THIRD-PARTY-NOTICES.md | Runtime/build dependency notices and redistribution license information. |
| RELEASE-NOTES.md | Finalized release-message Markdown, reused exactly for eligible release commit/tag and GitHub body. |

## Generated outputs and packages

Use dist/browser for the static browser build, dist/desktop for the shared desktop renderer plus compiled main entry, and dist/extensions/chromium and dist/extensions/firefox for complete unpacked extension roots. Keep .test-build for compiled test drivers, build for intermediate tooling output and artifacts for verified release files. Ignore these outputs, node_modules, Python caches, browser reports and test downloads while preserving existing ignore rules and *.tkn.

The release assembly produces only the P-5 stable names as applicable: tetris-browser.zip, tetris-windows-x64.zip, tetris-chromium-extension.zip, tetris-firefox-extension.zip and SHA256SUMS.txt. Archive roots contain usable deployment/install layouts, local codecs/Wasm/schema and notices. The Electron archive includes runtime resources; the extension ZIP roots contain their manifest.json without an extra enclosing directory. Build scripts resolve imported runtime assets from pinned dependencies and verify MIME/resource paths rather than fetching from a CDN at runtime.

Keep archive extraction/inspection and hosted-download verification in scripts and pytest platform checks. Scripts must inspect the actual filenames/bytes, not just a naming plan. Never include gh.tkn, test fixtures/drivers, private profiles, caches or node_modules in a user runtime archive. A JavaScript package required only for build remains a developer dependency; required runtime assets are explicitly copied into each applicable host build.

## Documentation and evidence owners

Main project documents live at docs/dev/PROJECT.md, ARCHITECTURE.md, DECOMPOSITION.md, SPEC.md with semantic children under spec, PLAN.md, layout.md and TASKS.md. Adjacent SPEC/PLAN/TASKS review reports own per-document conformance evidence. DOCS_TASKS owns preparation checkboxes, DOCS_PREPARATION owns mode/decisions, and HANDOFF supplies recovery checkpoints. DOCS-QC-REPORT.md is reserved for separately authorized whole-package QC.

Milestone evidence belongs at docs/dev/reports/phases/<phase>/<milestone>.md, phase evidence at docs/dev/reports/phases/<phase>/PHASE-REPORT.md and final aggregated evidence at docs/dev/reports/IMPLEMENTATION-REPORT.md. TASKS links expected reports without creating empty report files. Manual conversation records remain under docs/ai-logs and are not specification inputs. The bundled SDD Manager is tooling, not part of runtime archives.

## Dependency and change rules

Core does not import application, UI, codecs or adapters. Application consumes host/file interfaces; composition supplies concrete adapters and codecs. UI uses browser DOM/Canvas but no Electron or extension globals. Host-specific APIs remain in platform roots. Codec schema semantics are shared with application validation, without a cycle through controller code. Tests can import/drive compiled owned modules but do not create a second executable task registry.

Create focused files as cohesive implementations emerge instead of preallocating a file per function. A task may update a few related modules with tests/docs. Respect existing root AGENTS.md; add navigation and validated setup/check commands when implementation establishes them. Do not replace root guidance or rewrite bundled plugin files during application work.
