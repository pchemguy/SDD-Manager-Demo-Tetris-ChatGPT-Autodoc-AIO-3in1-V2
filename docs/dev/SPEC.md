# System specification

## Scope and contract owners

The application provides a local desktop-keyboard Tetris game with browser, Windows Electron and Chromium/Firefox sidebar packages. [PROJECT](PROJECT.md), [ARCHITECTURE](ARCHITECTURE.md) and [DECOMPOSITION](DECOMPOSITION.md) define intent and responsibility. These documents describe target behavior, not a claim of implemented features.

| Contract | Canonical detail | Responsible components |
| --- | --- | --- |
| G: gameplay, timing and special rules | [Gameplay](spec/gameplay.md) | Geometry, source, landing, reducer, input mapper |
| C: six settings and persistence | [Configuration](spec/configuration.md) | Settings validator, controller, host stores |
| F: leaderboard and file exchange | [Files](spec/files.md) | Leaderboard, snapshot validator, codecs, file port |
| U/P: presentation, lifecycle and packages | [Platforms](spec/platforms.md) | View, controller, adapters, packaging |

No backend, account system, multiplayer or automatic file synchronization is required. Settings persist only when the persistence capability is delivered. Completed-game results remain session-only except when manually saved and restored; persistent settings never carry scores.

## System invariants

The board and game-information panel remain reachable throughout play. Game rules use a single monotonic game-time owner. No completed lock overlaps existing cells or writes outside the visible board. Ghost and hard drop agree on their landing. Paused and hidden-host games do not advance. Completion is emitted once per game, independent of repaint or repeated commands.

All external settings are validated through one canonical value model. Both file formats decode to one complete snapshot model and validate fully before any live state or persistence mutation. Invalid restores cannot change results, configuration, cookies or URL. Errors are visible in an accessible status region and do not silently reset the session.

## Quality and execution requirements

Q-1: Distribute runtime code/assets locally without requiring Node.js, a development server or a backend in desktop and extension packages. Browser deployment is static HTTP(S). No remote code, CDN, analytics or network account is necessary to play or use files.

Q-2: Input is responsive to ordinary key events; use monotonic elapsed game time and bounded rendering work, with no busy-wait loops. Pause preserves the remaining gravity/lock interval. Board drawing must remain legible at different device pixel ratios.

Q-3: Controls use native buttons/selects with labels, visible keyboard focus and readable text; status is exposed through an aria-live region. Canvas has an accessible game-state description including lifecycle, score and level. Keyboard-only gameplay is intentional; do not add touch or pointer move/rotate/drop controls.

Q-4: Source and assets are reproducibly built from locked dependencies, include third-party notices and expose version information. Separate development prerequisites from end-user installation instructions. Reports identify performed checks, unsupported checks and unverified behavior.

Q-5: Verification uses pytest as the test runner, deterministic game/controller drivers and Python Playwright for browser integration. TypeScript compilation and build/lint/package tools remain build checks. Prefer representative Chromium and Firefox checks, dedicated profiles, and the repository browser/Playwright recovery policy. No product contract is relaxed because a particular automation facility is unavailable.

## Acceptance by capability

| ID | Observable acceptance |
| --- | --- |
| A-1 | An extracted browser build starts, moves, rotates, drops with gravity, clears rows, changes score/level, ends, pauses/resumes and restarts; only the two allowed gameplay buttons exist. |
| A-2 | Modern queue/hold/kicks/ghost/drop work together; a grounded piece waits the selected full interval; horizontal/rotation input cannot extend it without lift-off. |
| A-3 | A ghost crossing the midline hides/shows according to its occupied cells. A penetrator spends one available bonus, crosses occupied cells without erasing them, and previews/locks at the deepest valid landing. Four-line clears award one bonus up to three. |
| A-4 | All six settings act immediately and remain session-only in the intermediate release; reload resets to defaults in that release. |
| A-5 | Each persisted setting independently resolves URL, cookie and default; explicit default-valued URL inputs update cookies and omitted parameters retain saved values. |
| A-6 | Only finished games enter the top ten; ties, IDs and UTC completion times remain deterministic and restarting unfinished play adds no result. |
| A-7 | JSON and SQLite round-trip identical settings/results. Malformed files, invalid timestamps/settings, duplicate keys/IDs and wrong versions leave all pre-import state and host persistence unchanged. |
| A-8 | Browser/desktop panel order matches the brief; optional-panel toggles leave the board center fixed, and hiding settings hides Save/Restore. |
| A-9 | Windows archive contains a launchable application layout, Electron runtime and all application assets; no separate Node/server is needed. Applicable archive/build checks pass and unavailable Windows execution is reported explicitly. |
| A-10 | Both extension archives are self-contained and have correct sidebar integration. Settings persist in extension-local storage; session-only data never moves to persistent storage. Closing/reopening pauses and explicit resume works, with actual-host and fallback evidence clearly distinguished. |
| A-11 | Every phase release has the right version/tag/notes and cumulative verified packages under stable names. Downloaded hosted bytes agree with verified local checksums. |

Acceptance is scoped by the phase's included capability set. A platform is delivered only after its actual package passes applicable checks. Unavailable native Windows execution is outside the current Linux verification scope by default, not an invented blocker to artifact delivery; it remains an explicit unverified behavior. Actual sidebar launch/closure checks are distinct from loading an extension panel page as a normal browser page.
