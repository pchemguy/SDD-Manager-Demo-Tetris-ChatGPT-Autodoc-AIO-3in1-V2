# Delivery plan

## Strategy and dependencies

Build the simplest playable classic browser game first. Preserve that usable path through bounded capability increments, then add Windows and both sidebar extensions in the required order. The complete target is specified in [SPEC](SPEC.md); later-phase requirements are not baseline exit conditions. [ARCHITECTURE](ARCHITECTURE.md) and [DECOMPOSITION](DECOMPOSITION.md) keep rules/UI shared and host behavior separate.

Each phase depends on the preceding phase's verified review, explicit default-branch integration, publication and GitHub release. Retain versioned source tags and stable asset names. The version covers the capability set delivered by its phase; the first release need not contain the full project. No platform is claimed delivered from source code alone.

## Phase and milestone map

Every phase has one cohesive delivery milestone followed by a dedicated single-task phase review milestone. The small milestone count is deliberate: each phase is one user-visible increment, and separate technical-layer milestones would add handoffs without independently useful outcomes. TASKS divides each delivery milestone into bounded implementation units with their own tests/docs. Whole-milestone review/testing/report/HANDOFF is folded into the final implementation task because there is only one delivery milestone per phase.

| Phase / version | Delivery milestone and outcome | Included contracts and explicit deferrals | Review milestone |
| --- | --- | --- | --- |
| 1 / 0.1.0: Classic browser | 1.1 Classic browser game: playable falling-block loop with information and the two gameplay buttons | G-1/G-2/G-7 baseline, applicable Q and P-2/P-5. Independent piece draws, basic rotation and failed-downward lock. Defer modern rules, ghost, settings, results/files and final five-panel layout. | 1.2 Phase review |
| 2 / 0.2.0: Modern rules | 2.1 Modern browser game: hold, next, 7-bag, SRS, ghost, hard drop and interval locking together | G-3/G-4/G-5 modern behavior, all G-7 bindings for available actions. Ghost fixed show; hard drop/hold/preview on, general interval lock. Defer penetrator, dynamic visibility and configurable settings. | 2.2 Phase review |
| 3 / 0.3.0: Special landing rules | 3.1 Penetrator and conditional ghost: bonus earn/spend, transit, deepest landing and dynamic projection | G-4 dynamic predicate and G-6, integrated with modern locking/hold restrictions. Ghost fixed dynamic. Defer configuration controls/persistence. | 3.2 Phase review |
| 4 / 0.4.0: Session settings | 4.1 Six session settings: immediate, validated gameplay controls | C-1/C-4 and active-game transitions; settings panel. Explicitly do not read/write cookies, query settings or persistent stores. Defer persistence and files. | 4.2 Phase review |
| 5 / 0.5.0: Persistent settings | 5.1 Browser setting continuity: independent URL/cookie/default resolution | C-2/C-4, explicit URL/default cookie saving, changes update cookie/query. Defer leaderboard history and file exchange. | 5.2 Phase review |
| 6 / 0.6.0: Session leaderboard | 6.1 Ranked completed games: stable top-ten records and exactly-once updates | F-1 and leaderboard view, including ties and restart behavior. Scores remain in session memory; defer export/import and final toggles. | 6.2 Phase review |
| 7 / 0.7.0: Manual file exchange | 7.1 Versioned JSON and SQLite: complete validated snapshots, Save/Restore and schema | F-2 through F-6, persistent setting updates after successful import, local SQLite/schema dependencies. Defer final layout and extra platforms. | 7.2 Phase review |
| 8 / 0.8.0: Browser workspace | 8.1 Centered five-panel workspace: independent optional panels and retained information | U-1 including five-panel order, exact toggles and Save/Restore hiding; all earlier browser contracts preserved. Defer desktop and extensions. | 8.2 Phase review |
| 9 / 0.9.0: Windows desktop | 9.1 Portable Windows app: shared renderer under bundled Electron with local persistence/files | P-3, desktop C-3 and lifecycle, browser retained. Defer extensions and signing/store distribution. | 9.2 Phase review |
| 10 / 0.10.0: Browser sidebars | 10.1 Chromium and Firefox sidebars: both packaged with narrow UI and host adapters | U-2/P-1/P-4, extension C-3, file equivalence, browser/Windows retained. No persistent scores, background gameplay or signing/store claim. | 10.2 Phase review |

## Phase-specific exit evidence

| Phase | Demonstration and decisive failure/interaction checks | Required package set |
| --- | --- | --- |
| 1 | Play an actual extracted browser build through start, movement/rotation, lock/clear, score/level, game over, pause/resume and restart. Check exact permitted gameplay buttons, keyboard focus and absence of browser errors. Deterministic reducer tests and Chromium/Firefox representative startup are required where available. | Browser |
| 2 | Show queue/hold and bag permutation, wall/floor kick fixtures, ghost/hard-drop agreement and elapsed lock timing. Test repeat drop, already-grounded drop, lift-off reset and paused timer. Review RNG and kick-table direction independently of implementation-shaped assertions. | Browser |
| 3 | Demonstrate dynamic ghost at rows 9/10 and straddling; earn/cap/spend bonuses, transit through blockers, deepest valid cavity and hold rejection while active. Test invalid penetrator transformations and final collision-free lock. | Browser |
| 4 | Change every setting during play, including lock policy transitions; verify effect without restart and reload defaults. Observe no cookie/query/persistent-store mutations in this build. | Browser |
| 5 | Reload with mixed URL/cookie/default sources, explicit default and omitted/invalid values. Verify cookie/URL readback, unrelated query/fragment preservation and blocked-persistence diagnostics. | Browser |
| 6 | Finish games with zero/tied scores, rank/truncate to ten, verify stable IDs/UTC dates, restart an unfinished game and reload. Confirm no score persistence. | Browser |
| 7 | Save/Restore both actual file formats, inspect SQLite independently, and compare semantic content. Reject the full malformed/invalid corpus while comparing results/settings/cookies/URL unchanged. Exercise duplicate JSON names, storage commit failure and cancellation. | Browser with bundled codecs/schema |
| 8 | Compare board center and panel order at specified widths for every optional-panel combination. Verify information stays reachable, text does not overlap and Save/Restore disappear with settings. | Browser |
| 9 | Inspect extracted Windows runtime, PE architecture, app resources, protocol mapping and all local asset references. Run feasible packaged/shared-renderer checks; distinguish native Windows execution unavailable on Linux. Verify desktop cookie origin, file flow and deny navigation/traversal. | Browser and Windows x64 |
| 10 | Validate/lint both manifests and CSP, exercise narrow layouts, API adapters, persistent versus transient stores, ownership, close/reopen paused state and file exchange. Attempt actual sidebar launch/closure with isolated Chromium/Firefox; record exact unavailable checks and panel-page fallback limits. Recheck all cumulative packages after shared changes. | Browser, Windows x64, Chromium extension and Firefox extension |

At each demonstration the evidence makes continued development, amendment, simplification or stopping assessable to the human. It introduces no new approval pause beyond the user's selected execution boundary and existing material-decision checkpoints.

## Milestone and phase completion

A delivery milestone exits only when its included behavior and applicable prior regressions pass, code is reviewed independently from tests, required defects are repaired, documentation is accurate and a milestone report plus HANDOFF is committed with its final implementation task. Reports include Findings/Blockers and TODO (None when empty); confirmed contract failures cannot be deferred as non-critical TODOs.

The dedicated phase review starts after the delivery milestone and all its task issues close. It assesses the complete phase, cross-component effects, package contents and release readiness, and retains its report. The final phase review also aggregates the full implementation report and unresolved eligible TODOs. Review task completion does not claim the later merge, upload or hosted download verification has happened.

After phase review and its hosted closure, explicitly merge the complete phase into the actual default branch, verify the merged state and publish/read back. Prepare the release commit/notes on that eligible default history, publish its tag, upload verified cumulative packages, download them and compare checksums, and verify latest-release state. Release operations occur after task completion/integration; they are not circular acceptance prerequisites of a task that must first be committed. Their verified completion gates the next phase.

## Verification approach and risks

Use pytest for deterministic TypeScript-driver, application, codec and Python Playwright checks. TypeScript type checking, production build, dependency/manifest lint and archive verification complement runtime tests. Select checks from the phase's actual contracts; collect expected/actual boundary outcomes rather than duplicating internal implementation. Browser profiles are isolated, with Chromium prioritized and Firefox included by default under repository policy.

Preflight matching Playwright/browser execution before browser-dependent work. On provisioning/runtime failure, follow bundled recovery, diagnose full-browser versus headless-shell behavior and retain exact fallback coverage. Do not treat a loaded ordinary panel page as proof of extension launch/reopening. Unavailable native Windows checks are excluded by default with explicit reporting; feasible build/archive/shared runtime checks remain required and the artifact remains in scope.

File-codec risk is reduced by a shared validator, bounded file size and independent Python SQLite inspection. Browser persistence is not process-crash atomic; test invalid-file non-mutation separately from valid-import commit failures and reported rollback limitations. Extension snapshot loss on forcible teardown is bounded by continuously saved generations; verify ownership and never substitute persistent scores for session storage. Packaging verifies actual emitted assets and rejects missing Wasm/schema/runtime files before publication.

## Version and release policy

Use the phase versions above, v-prefixed tags and stable asset names from P-5. Patch releases are permitted for scoped repairs without changing phase identity. Every release contains every platform delivered by then, checksum manifest, installation steps, development/signing status and honest check limits. Scripts and CI must enforce the actual filename contract; if names or contents fail, repair source/scripts/docs, publish the correction, rebuild and recheck before finishing the release. Hosted upload success alone is insufficient.
