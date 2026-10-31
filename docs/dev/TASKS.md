# Implementation tasks

[PLAN](PLAN.md) owns delivery boundaries; [SPEC](SPEC.md) and its children own acceptance, and [layout](layout.md) owns physical placement. This list contains planned executable work; all tasks are initially unchecked.

## Execution conditions

Each implementation task includes meaningful contract-derived tests, observed RED/GREEN for new behavior where applicable, affected user/module documentation, verification evidence, one closing commit with its initial checkbox and publication/readback before dependent work. Use pytest; build/type/lint/archive checks are separate. Preserve prior delivered capability regressions. No task closes from a commit subject or hosted issue alone.

Before a phase starts, its predecessor review/milestones, published integration and release are verified, preparation is accepted/integrated and eligible phase tracking is activated. The first phase has no delivered predecessor. Phase review happens after delivery milestone closure; default integration and release follow phase review and are separate post-task operations, never prerequisites of a task needing its own future commit/merge.

## Phase 1 - Classic browser

- [x] Phase 1 - Classic browser
    - [x] Milestone 1.1 - Classic browser game
        - [x] T-001 - Establish typed board and piece geometry
            Verified: RED: geometry stub produced 8 expected cell/rotation failures (4 bounds cases passed). GREEN: typecheck/build:test and 12 pytest geometry cases pass, covering exact spawn sets, active bounds, collision and clockwise rotation. Locked tooling and pytest driver are excluded from runtime builds.
            Scope: src/core geometry/types, locked TypeScript tooling and tests/unit fixtures.
            Depends on: none. Contracts: G-1/G-2.
            Acceptance/evidence: Seven four-cell shapes, bounds, collision and basic rotations match exact spawn coordinates; create a deterministic Node driver exercised by pytest without shipping it.
        - [x] T-002 - Implement the classic game state machine
            Verified: RED: classic no-op reducer failed all five state/timing/score/completion scenarios. GREEN: typecheck/build:test and 17 pytest unit cases pass. Verified immutable input state, exact gravity/pause time, failed-down lock and pre-clear level scoring, wall rejection, once-only top-out and unfinished restart without completion.
            Scope: src/core reducer/time/source and focused pytest scenarios.
            Depends on: T-001. Contracts: G-1/G-2.
            Acceptance/evidence: Verify movement, gravity, failed-downward lock, row compaction, scoring/levels, top-out, exactly-once game-over and pause/resume under injected RNG/time.
        - [x] T-003 - Integrate browser rendering and keyboard play
            Verified: RED: two browser acceptance cases failed on missing gameplay controls in the initial shell. GREEN: typecheck/build:test/production build, 19 Chromium unit/browser cases and 2 Firefox browser cases passed. Verified real keyboard play, exact two gameplay buttons, native focused-button activation, pause/restart, colored Canvas pixels and no page errors; screenshot inspected. Firefox uses diagnosed process-local content sandbox recovery for trusted local pages.
            Scope: src/app controller, src/ui, browser host and browser entry.
            Depends on: T-002. Contracts: G-7/U-1/P-2/Q.
            Acceptance/evidence: A real browser page plays the classic loop with the two permitted gameplay buttons; focus/modifier/key-repeat rules work and information reflects domain state.
        - [x] T-004 - Package and verify the classic browser baseline
            Verified: RED name-gate tests exposed versioned, duplicate and missing assets; GREEN 4 gate cases and full 23-test suite pass. Typecheck/build:test/production build, actual ZIP name/resource/source/checksum checks and 2 extracted-package browser tests pass. Whole-milestone code review and screenshot inspection passed; immediate held-key clearing tightened. Milestone report/HANDOFF and stable browser package/install/CI checks included; hosted release remains pending.
            Scope: browser build/package scripts, notices, installation/control docs and relevant pytest browser/package checks.
            Depends on: T-001, T-002, T-003. Contracts: A-1/P-2/P-5.
            Acceptance/evidence: Extract the actual browser archive, verify local resource resolution, no required network runtime, version 0.1.0 and stable tetris-browser.zip name; run representative Chromium/Firefox checks and document unavailable execution.
            Milestone exit: depends on all other milestone tasks T-001 through T-003; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/1/1.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [x] Milestone 1.2 - Phase review
        - [x] T-005 - Review test and report phase 1
            Verified: Whole-phase source review and task-closing commit audit passed; typecheck/build:test, 23 pytest cases and actual archive naming/resource/checksum checks pass. Prior 2 Firefox and 2 extracted-build browser cases and screenshot support runtime acceptance. No blockers/TODOs. Phase report and HANDOFF retain pending main integration and release/download checks; no hosted release success is claimed yet.
            Depends on: T-004, completion/verified closure of milestone 1.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/1/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 2 - Modern rules

- [x] Phase 2 - Modern rules
    - [x] Milestone 2.1 - Modern browser game
        - [x] T-006 - Implement seven-bag source and hold lifecycle
            Verified: RED: six independent bag/hold lifecycle cases failed against stub/no-hold behavior. GREEN: typecheck/build:test and 23 unit cases pass, including four seeded 28-draw bag sequences, once-per-piece hold, queue-preserving swap and blocked held spawn. Phase 2 activation and verified v0.1.0 hosted-byte predecessor evidence retained in HANDOFF.
            Scope: src/core source/reducer and tests/unit.
            Depends on: T-005. Contracts: G-3.
            Acceptance/evidence: Each bag is a seven-piece permutation with seeded fixtures; hold consumes/swaps with correct spawn, once-per-piece eligibility and blocked-spawn game-over.
        - [x] T-007 - Implement SRS rotation and kick candidates
            Verified: RED: four independent I/T wall/floor fixtures failed with in-place-only rotation; blocked rotation already passed. GREEN: typecheck/build:test and 28 unit cases pass. Verified ordered screen-coordinate SRS offsets, distinct I behavior and rejection when every candidate is occupied; geometry/reducer/hold regressions remain green.
            Scope: src/core geometry/rotation data and tests/unit.
            Depends on: T-006. Contracts: G-3.
            Acceptance/evidence: Fixed both-direction I/JLSTZ wall/floor/rejection fixtures establish pivots and ordered kicks; O remains stationary and all active bounds hold.
        - [x] T-008 - Implement shared landing ghost and hard drop
            Verified: RED: four landing/drop integration scenarios failed against unchanged landing/no-drop behavior. GREEN: typecheck/build:test and 32 unit cases pass. Verified first-blocker landing, ghost/drop destination agreement, exact distance points, zero repeat-drop points and separate counterclockwise I/T wall-kick-to-floor scenarios. General drop does not lock merely because landing search ends.
            Scope: src/core landing/drop reducer and focused controller tests.
            Depends on: T-007. Contracts: G-4.
            Acceptance/evidence: Ghost/drop share a collision-free landing; drop points use actual distance and repeat drop adds zero; hard drop using general policy does not lock merely because search ends.
        - [x] T-009 - Implement gravity-interval grounded locking
            Verified: RED: 5 grounded-lock/policy scenarios failed under failed-attempt behavior; after reducer correction, 2 injected host-clock cases exposed late-key and hidden-wall-time ordering. GREEN: typecheck/build:test/production build and full 46-test suite pass. Verified exact deadlines, no grounded reset, true lift-off, pause, delayed frames, immediate/general drop and expired policy history. Controller advances elapsed deadlines before commands and drains scheduled repeats chronologically; classic failed-policy fixtures remain explicit.
            Scope: src/core time/reducer and deterministic boundary tests.
            Depends on: T-008. Contracts: G-5.
            Acceptance/evidence: Test exact deadline, already-grounded drop, failed soft drop, lateral/rotation non-reset, lift-off/reset, pause freezing and delayed-frame scheduling without wall-clock sleeps.
        - [x] T-010 - Expose and package modern gameplay
            Verified: RED: two modern browser scenarios failed on absent preview/keyboard controls. GREEN: typecheck/build:test/build, full 48 tests, 4 Firefox browser cases, 4 extracted-package Chromium cases and actual archive name/resource/checksum checks pass. Hold/next/ghost/hard-drop UI and timed keyboard repeat are integrated at 0.2.0; screenshot and full milestone source review inspected. Milestone report/HANDOFF retain pending phase review and hosted release effects.
            Scope: src/ui previews/hold/ghost, app composition, package outputs and user docs.
            Depends on: T-006, T-007, T-008, T-009. Contracts: A-2/G-3/G-4/G-5/P-5.
            Acceptance/evidence: Integrate modern capabilities with fixed defaults and visible bindings; verify actual 0.2.0 browser package, timing interactions and classic regressions.
            Milestone exit: depends on all other milestone tasks T-006 through T-009; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/2/2.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [x] Milestone 2.2 - Phase review
        - [x] T-011 - Review test and report phase 2
            Verified: Whole-phase code review and closing-commit audit passed; typecheck/build:test, full 48 pytest cases and actual archive checks pass. Phase report/HANDOFF record scoped coverage and native limits, with main integration/release readback still pending.
            Depends on: T-010, completion/verified closure of milestone 2.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/2/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 3 - Special landing rules

- [x] Phase 3 - Special landing rules
    - [x] Milestone 3.1 - Penetrator and conditional ghost
        - [x] T-012 - Implement penetrator transit bonus and valid locks
            Verified: RED: seven bonus/transit/deepest-landing scenarios failed; cap-at-three already passed. GREEN: typecheck/build:test and 48 unit cases pass. Verified capped four-line awards, spend-once activation, blocker transit, deepest cavity, white settled locks, hold rejection, invalid transformations and genuine-lift versus grounded timing. Impossible final destinations reject activation without spending. A minimal view cell-type bridge preserves compilation; active white rendering and dynamic visibility remain T-013.
            Scope: src/core landing/reducer and tests/unit.
            Depends on: T-011. Contracts: G-6.
            Acceptance/evidence: Earn/cap/spend bonuses, reject invalid activation and transformations, cross occupancy without erasure, choose deepest valid cavity and lock non-overlapping; hold is disabled while active.
        - [x] T-013 - Integrate dynamic ghost and bonus feedback
            Verified: RED: three occupied-cell midline cases and two real renderer cases failed; lower-half cases already passed. GREEN: compiler, test-harness and production builds, full 64 tests and 6 Firefox browser cases pass. Verified straddling/origin boundaries, hidden/shown ghost pixels, deepest white ghost/active/settled rendering and exact bonus-symbol counts. Added a separate non-shipped view harness with detached fixtures; real gameplay remains covered by production-page tests. X activation is keyboard-only.
            Scope: src/core ghost predicate, src/ui bonus/white-piece rendering and browser scenarios.
            Depends on: T-012. Contracts: G-4/G-6.
            Acceptance/evidence: Check occupied cells at rows 9/10 and straddling, match penetrator ghost/drop, show exact bonus-symbol count and reserve white exclusively for penetrator pieces.
        - [x] T-014 - Package and verify special landing behavior
            Verified: RED: an injected development renderer file was wrongly accepted in a complete ZIP; GREEN: package exclusion gate and full 70 tests pass. Typecheck/test-harness/production builds, 7 Firefox checks, 5 actual extracted-package production-page cases and archive name/resource/checksum checks pass. Added occupied-rotation, inactive activation and no-bonus hotkey regressions. Whole-milestone source review/report/HANDOFF and 0.3.0 package/install metadata included; renderer fixtures are explicitly separate from packaged gameplay evidence.
            Scope: build/package outputs, interaction regression fixtures and gameplay docs.
            Depends on: T-012, T-013. Contracts: A-3/P-5.
            Acceptance/evidence: Verify 0.3.0 extracted browser build across activation during grounded delay, lift-off, transit rotations, bonus award after four clears and session restart reset.
            Milestone exit: depends on all other milestone tasks T-012 through T-013; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/3/3.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [x] Milestone 3.2 - Phase review
        - [x] T-015 - Review test and report phase 3
            Verified: Whole-phase code review and closing-commit audit passed; typecheck/build:test, full 70 pytest cases and actual archive checks pass. Phase report/HANDOFF record scoped coverage and native limits, with main integration/release readback still pending.
            Depends on: T-014, completion/verified closure of milestone 3.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/3/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 4 - Session settings

- [x] Phase 4 - Session settings
    - [x] Milestone 4.1 - Six session settings
        - [x] T-016 - Define canonical settings and active-game transitions
            Verified: RED: compiled driver rejected missing settings API. GREEN: build:test and 14 canonical-domain/atomic-rejection/controller-transition pytest cases pass. Policies preserve original grounding history; disabled hold/drop do not consume eligibility; restart retains settings. No host persistence is present.
            Scope: src/app settings validator/controller and src/core policy command boundary.
            Depends on: T-015. Contracts: C-1/G-5.
            Acceptance/evidence: Validate all six enum domains/defaults; lock-policy toggles retain grounding history, expired deadlines lock, and hold/drop toggles preserve piece eligibility.
        - [x] T-017 - Expose six settings in the shared panel
            Verified: RED: both new browser settings cases failed against absent controls. GREEN: compiled harness/production builds and nine real Chromium browser/renderer checks pass. Six labeled native selects apply immediately; next hides without queue mutation; hold/drop gating works; hiding retains values and focus clears held repeat. Only two gameplay buttons remain.
            Scope: src/ui settings panel and app command integration.
            Depends on: T-016. Contracts: C-1/U-1.
            Acceptance/evidence: All labels/controls reflect and immediately apply settings; hiding/repainting does not reset values; forms retain native keyboard behavior.
        - [x] T-018 - Package and verify session-only configuration
            Verified: Version 0.4.0 production package passes filename/resource/checksum checks. Full pytest 87 passed, Firefox 10 passed, extracted production package 8 passed. Cookie/storage/history observers confirm no configuration persistence I/O and reload defaults despite supplied URL/cookie values. Whole-milestone review, limits and no blockers recorded in 4.1 report/HANDOFF.
            Scope: browser package, tests/browser persistence observers and configuration docs.
            Depends on: T-016, T-017. Contracts: A-4/C-4/P-5.
            Acceptance/evidence: Verify 0.4.0 settings work during play and reload defaults; observe no configuration cookie/query/persistent-store reads or writes in this increment.
            Milestone exit: depends on all other milestone tasks T-016 through T-017; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/4/4.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [x] Milestone 4.2 - Phase review
        - [x] T-019 - Review test and report phase 4
            Verified: Whole-phase code review and closing-commit audit passed; typecheck/build:test, full 87 pytest cases and actual archive checks pass. Phase report/HANDOFF record scoped coverage and native limits, with main integration/release readback still pending.
            Depends on: T-018, completion/verified closure of milestone 4.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/4/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 5 - Persistent settings

- [x] Phase 5 - Persistent settings
    - [x] Milestone 5.1 - Browser setting continuity
        - [x] T-020 - Implement independent URL cookie and default resolution
            Verified: RED: driver compilation rejected missing resolver. GREEN: build:test and 17 mixed-source/all-key precedence cases pass, including malformed percent encoding, repeated/empty/case-invalid values, ambiguous cookies, encoded keys/values, explicit URL defaults and omitted-cookie retention. Resolver returns only valid explicit writes and per-key diagnostics without host mutation.
            Scope: src/platform/browser query/cookie ports and src/app resolution logic.
            Depends on: T-019. Contracts: C-2.
            Acceptance/evidence: Exercise mixed-source settings, invalid/duplicate/encoded values, explicit default-valued URL cookies and omitted parameters retaining valid cookie values.
        - [x] T-021 - Synchronize setting changes with browser persistence
            Verified: RED: four production-browser persistence cases failed against the session-only build. GREEN: build:test/build and 13 browser/renderer checks pass for real cookie/URL precedence, explicit-default writes, omitted-cookie retention, duplicate replacement, unrelated queries/fragments, invalid fallback and blocked-cookie diagnostics while selection remains playable. Phase-4 no-I/O expectation is superseded by the persistence contract and retained in its release tag/report.
            Scope: src/app setting transaction and browser history/cookie readback.
            Depends on: T-020. Contracts: C-2/C-4.
            Acceptance/evidence: User changes update only the selected cookie/query key, preserve unrelated query/fragment data and show blocked-cookie diagnostics; invalid values never overwrite valid saved settings.
        - [x] T-022 - Package and verify setting continuity
            Verified: Version 0.5.0 typecheck/build/archive gates pass; full pytest 108 passed, Firefox browser/renderer 14 passed, extracted browser package 12 passed. Every setting covers default/cookie/explicit-default URL, changes and reload retention without persistent score storage. Whole-milestone review and native limits recorded in 5.1 report/HANDOFF; no blockers.
            Scope: browser package, reload integration scenarios and persistence guide.
            Depends on: T-020, T-021. Contracts: A-5/P-5.
            Acceptance/evidence: Verify 0.5.0 extracted build restores settings across reload with every precedence branch and preserves all prior gameplay behaviors; scores/files remain out of scope.
            Milestone exit: depends on all other milestone tasks T-020 through T-021; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/5/5.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [x] Milestone 5.2 - Phase review
        - [x] T-023 - Review test and report phase 5
            Verified: Whole-phase code review and closing-commit audit passed; typecheck/build:test, full 108 pytest cases and actual archive checks pass. Phase report/HANDOFF record scoped coverage and native limits, with main integration/release readback still pending.
            Depends on: T-022, completion/verified closure of milestone 5.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/5/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 6 - Session leaderboard

- [ ] Phase 6 - Session leaderboard
    - [ ] Milestone 6.1 - Ranked completed games
        - [ ] T-024 - Implement immutable completed results and ranking
            Scope: src/app leaderboard/controller and tests/unit.
            Depends on: T-023. Contracts: F-1.
            Acceptance/evidence: Generate immutable lowercase UUIDs and real UTC completion timestamps once; rank score/time/id and truncate live results to ten, including zero/tied scores.
        - [ ] T-025 - Integrate the session leaderboard view
            Scope: src/ui leaderboard and controller completion events.
            Depends on: T-024. Contracts: F-1/U-1.
            Acceptance/evidence: Update displayed top ten on completed games only, reject duplicate completion insertion, preserve IDs and exclude unfinished restarts; reload clears browser session history.
        - [ ] T-026 - Package and verify session score history
            Scope: browser package and completed-game integration fixtures/docs.
            Depends on: T-024, T-025. Contracts: A-6/P-5.
            Acceptance/evidence: Verify 0.6.0 ranking, timestamp display, stable identities and reload clearing without persistent score writes; configurations still restore independently.
            Milestone exit: depends on all other milestone tasks T-024 through T-025; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/6/6.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [ ] Milestone 6.2 - Phase review
        - [ ] T-027 - Review test and report phase 6
            Depends on: T-026, completion/verified closure of milestone 6.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/6/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 7 - Manual file exchange

- [ ] Phase 7 - Manual file exchange
    - [ ] Milestone 7.1 - Versioned JSON and SQLite
        - [ ] T-028 - Define the shared snapshot validator and JSON Schema
            Scope: src/app snapshot validator, schemas/tetris-save.schema.json and tests/codecs.
            Depends on: T-027. Contracts: F-1/F-3.
            Acceptance/evidence: Validate exact root/result/settings fields, enums, safe scores, UUIDs, real canonical UTC dates, duplicate IDs and ten-result limit; schema and semantic validator agree on a shared corpus.
        - [ ] T-029 - Implement strict JSON interchange and restore staging
            Scope: src/codecs JSON parser and src/app import/export transaction.
            Depends on: T-028. Contracts: F-2/F-3/F-5.
            Acceptance/evidence: Reject duplicate JSON member names before schema validation; export one immutable candidate; invalid decode/validation writes nothing and injected host failures keep original application state with explicit rollback reporting.
        - [ ] T-030 - Implement the SQLite versioned codec
            Scope: src/codecs SQLite loader, local runtime bundling and tests/codecs.
            Depends on: T-029. Contracts: F-4.
            Acceptance/evidence: Export actual SQLite 3 bytes with exact tables, six unique settings, metadata and bound inserts; validate schema/storage classes/integrity and close isolated databases on errors; inspect exports independently with Python sqlite3.
        - [ ] T-031 - Integrate manual Save Restore and format choice
            Scope: src/ui settings file controls, controller serialization and browser file port.
            Depends on: T-030. Contracts: F-2/F-5.
            Acceptance/evidence: One Save/Restore pair is at the bottom of settings; format choice/download/picker, cancellation, size/encoding detection, success pause and all-six persistence updates work without extra gameplay buttons.
        - [ ] T-032 - Package and verify cross-format file exchange
            Scope: browser build/local codec/schema assets, tests/codecs/browser and file guide.
            Depends on: T-028, T-029, T-030, T-031. Contracts: A-7/F-6/P-5.
            Acceptance/evidence: Verify 0.7.0 package round trips empty/full files, semantic JSON/SQLite equality and malformed corpus; compare results/settings/cookies/URL unchanged on every rejection and verify successful Restore readback.
            Milestone exit: depends on all other milestone tasks T-028 through T-031; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/7/7.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [ ] Milestone 7.2 - Phase review
        - [ ] T-033 - Review test and report phase 7
            Depends on: T-032, completion/verified closure of milestone 7.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/7/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 8 - Browser workspace

- [ ] Phase 8 - Browser workspace
    - [ ] Milestone 8.1 - Centered five-panel workspace
        - [ ] T-034 - Arrange the symmetric browser workspace
            Scope: src/ui layout/styles and responsive geometry checks.
            Depends on: T-033. Contracts: U-1.
            Acceptance/evidence: Place leaderboard/info/board/settings/help in order, preserve fixed board center and reachable information at specified browser widths/text scale without overlap.
        - [ ] T-035 - Integrate independent optional-panel toggles
            Scope: src/ui information panel/panel state and browser input tests.
            Depends on: T-034. Contracts: U-1.
            Acceptance/evidence: Exactly three visibility toggles sit above the two gameplay buttons; each changes only its target and hiding settings hides both file controls; settings/board state remain intact.
        - [ ] T-036 - Package and verify all panel combinations
            Scope: browser package, layout screenshots/geometry checks and controls guide.
            Depends on: T-034, T-035. Contracts: A-8/P-5.
            Acceptance/evidence: Verify 0.8.0 actual build at all five widths and eight optional-panel combinations, native focus behavior and complete gameplay/persistence/file regressions.
            Milestone exit: depends on all other milestone tasks T-034 through T-035; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/8/8.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [ ] Milestone 8.2 - Phase review
        - [ ] T-037 - Review test and report phase 8
            Depends on: T-036, completion/verified closure of milestone 8.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/8/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 9 - Windows desktop

- [ ] Phase 9 - Windows desktop
    - [ ] Milestone 9.1 - Portable Windows app
        - [ ] T-038 - Implement the isolated Electron host and app origin
            Scope: platforms/electron, src/platform/desktop and desktop entry.
            Depends on: T-037. Contracts: P-3/C-3.
            Acceptance/evidence: Load shared bundled UI under stable secure app origin with persistent settings cookies; reject traversal/remote navigation, preserve query history and enforce sandbox/context isolation/no renderer Node.
        - [ ] T-039 - Assemble the Windows portable runtime package
            Scope: build/package scripts and locked Electron distribution assets.
            Depends on: T-038. Contracts: P-3/P-5.
            Acceptance/evidence: Produce unsigned Windows x64 ZIP with executable/runtime/resources, local SQLite/schema/UI and notices; verify PE architecture, archive root and every required resource without a Node/server end-user dependency.
        - [ ] T-040 - Verify desktop integration and cumulative packages
            Scope: tests/platforms, packaged renderer/file checks, browser regression outputs and installation docs.
            Depends on: T-038, T-039. Contracts: A-9/P-5.
            Acceptance/evidence: Verify 0.9.0 browser plus Windows archives, secure protocol/error/file/cookie behavior with feasible host checks, explicit native-Windows limits and stable names/checksums.
            Milestone exit: depends on all other milestone tasks T-038 through T-039; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/9/9.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [ ] Milestone 9.2 - Phase review
        - [ ] T-041 - Review test and report phase 9
            Depends on: T-040, completion/verified closure of milestone 9.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/9/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.

## Phase 10 - Browser sidebars

- [ ] Phase 10 - Browser sidebars
    - [ ] Milestone 10.1 - Chromium and Firefox sidebars
        - [ ] T-042 - Implement extension stores and single-owner sessions
            Scope: src/platform/extensions storage/messaging/coordinator and tests/platforms.
            Depends on: T-041. Contracts: C-3/P-1.
            Acceptance/evidence: Persistent six-key settings and transient paused game/results use separate stores; serialized generations, ownership transfer, disconnect and failed writes never run background gameplay or persist scores.
        - [ ] T-043 - Implement both sidebar manifests and launch adapters
            Scope: platforms/extensions chromium/firefox manifests/background launch and extension entry.
            Depends on: T-042. Contracts: P-4.
            Acceptance/evidence: Chromium MV3 side_panel and Firefox sidebar_action launch the shared panel with required minimum APIs/permissions/CSP and local assets; no content scripts or site permissions are introduced.
        - [ ] T-044 - Adapt the shared view to a narrow resizable sidebar
            Scope: src/ui sidebar styles/sections and browser panel geometry checks.
            Depends on: T-043. Contracts: U-2.
            Acceptance/evidence: Widths 280/360/480 retain board/information, optional capabilities, keyboard access and file controls without horizontal overflow; resize preserves current state.
        - [ ] T-045 - Integrate extension lifecycle configuration and files
            Scope: src/platform/extensions, controller/session integration and host scenarios.
            Depends on: T-044. Contracts: P-1/C-3/F-2.
            Acceptance/evidence: Close/focus loss and ownership transfer pause; reopen confirmed session snapshot paused with explicit resume, browser restart clears results, local settings survive, valid query seeds and both file flows preserve validation semantics.
        - [ ] T-046 - Package and verify both sidebar extensions
            Scope: extension packaging/lint/CSP checks, actual-host attempts, cumulative browser/Windows rebuilds and install docs.
            Depends on: T-042, T-043, T-044, T-045. Contracts: A-10/P-5.
            Acceptance/evidence: Verify 0.10.0 all four archives and local assets; attempt real sidebar launch/closure in isolated Chromium/Firefox and distinguish unavailable native/sidebar checks from panel-page fallback; signing/store status is explicit.
            Milestone exit: depends on all other milestone tasks T-042 through T-045; review the entire capability code and applicable tests separately, repair blockers and include docs/dev/reports/phases/10/10.1.md plus refreshed HANDOFF with this task's result/initial completion. Include Findings/Blockers and TODO (None if empty), actual check limits and package/version evidence.
    - [ ] Milestone 10.2 - Phase review
        - [ ] T-047 - Review test and report phase 10
            Depends on: T-046, completion/verified closure of milestone 10.1 and all its issues; the review milestone itself remains open until this task closes.
            Scope/evidence: independent whole-phase code review, applicable focused/regression checks and package readiness; repair contract blockers, retain docs/dev/reports/phases/10/PHASE-REPORT.md and refresh HANDOFF in this task's closing commit. Carry unresolved eligible TODOs with stable evidence/options and identify pending integration/release operations without claiming success.
            Final scope: also write docs/dev/reports/IMPLEMENTATION-REPORT.md aggregating full-task-list outcome, all unresolved/deferred milestone/phase TODOs, proposed solutions and native/sidebar verification limits.

