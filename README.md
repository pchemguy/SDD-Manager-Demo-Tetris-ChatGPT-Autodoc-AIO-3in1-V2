# Tetris

A keyboard-controlled Tetris browser game with 7-bag pieces, SRS wall kicks, hold/next preview, ghost, hard drop and gravity-interval lock delay. Classic movement, scoring, levels, restart and pause remain available. Penetrator bonuses and dynamic ghost visibility are also implemented. All six settings support URL/cookie persistence. Session-only top-ten completed-game history is implemented. Manual JSON/SQLite file exchange is implemented. The centered five-panel layout is implemented. An unsigned Windows x64 portable Electron build is implemented; Chromium and Firefox sidebars follow in the final phase; see [PLAN](docs/dev/PLAN.md).

## Play and controls

Click Start, then use Left/Right to move, Down to soft drop, Up or Space to rotate clockwise, Z to rotate back, Enter to hard drop, C to hold, X to spend a penetrator bonus, P to pause/resume and R to restart. A grounded piece waits one gravity interval, including after hard drop; grounded movement does not restart the timer. The information panel has only Start/Restart and Pause/Start gameplay buttons. Losing focus pauses play; returning focus requires explicit resume.

## Build and run

Development uses Node.js 24 and Python 3.12 in the verified environment. End-user browser play requires only a modern browser and static HTTP(S) hosting.

```text
npm ci
npm run typecheck
npm run build
python -m http.server 8000 --directory dist/browser
```

Open http://localhost:8000. File-URL deployment is unsupported for persistence. See [installation](INSTALL.md). Create and check the stable browser archive with python scripts/package.py after a production build; python scripts/verify_packages.py artifacts verifies actual names, resources and checksums.

## Verification

Install the pinned Python requirements in your chosen Python environment, set PLAYWRIGHT_BROWSERS_PATH to one absolute dedicated browser directory, and use it consistently for provisioning and execution.

```text
python -m pip install -r requirements-test.txt
python -m playwright install chromium --only-shell firefox
npm run build:test
npm run build
python -m pytest
```

Browser tests default to Chromium headless shell; select Firefox with the TETRIS_BROWSER environment variable. In this Linux sandbox Firefox requires process-local content-sandbox recovery for trusted local tests because its content process reports uid_map EPERM. Tests apply that recovery only to isolated local application pages; native-window/sidebar behavior remains separate coverage.

## Project records

[Project brief](docs/dev/PROJECT.md), [development handoff](docs/dev/HANDOFF.md) and [tasks](docs/dev/TASKS.md) describe scope and actual workflow progress. This repository uses [SDD Manager](SDD-MANAGER.md); see the [AI-assisted development disclosure](AI_DISCLOSURE.md).

## Penetrator and ghost

A four-line clear awards one penetrator activation, up to three. Press X to activate the current piece; it crosses settled cells without erasing them, and its ghost/hard drop choose the deepest valid landing. Hold is disabled while active. White denotes penetrator cells, including after lock. Dynamic ghost mode hides a projection whenever any occupied ghost cell is above row 10, including straddling projections.

## Gameplay settings

The settings panel exposes ghost visibility (hide/dynamic/show), hard drop, next preview, hard-drop lock (general/immediate), general lock (failed attempt/full interval) and hold. Defaults show the ghost and preview, enable hold/drop and use full-interval locking. Changes apply immediately; switching lock policy retains grounding history. The intermediate v0.4.0 release kept settings only in page memory. The current release resolves each setting independently from a valid explicit URL parameter, then a saved cookie, then its default. Invalid inputs fall back with a diagnostic. Explicit URL values, including defaults, update their cookies; omitted parameters retain saved values. User changes update that setting in both cookies and the current URL, preserving unrelated parameters and fragments. Cookies last one year where permitted; blocked persistence is reported while the selected setting remains usable in the current page.

## Session leaderboard

Completed games enter the top ten ranked by score descending, UTC completion time ascending and stable lowercase UUID ascending. Each result is recorded once; restarting an unfinished game adds nothing. History stays in this page session, survives panel toggles and restarts, and clears on reload. Configuration cookies never contain scores.

## Manual files

Choose JSON or SQLite at the bottom of Settings, then Save or Restore one file. Complete validation precedes changes; successful restore replaces all results/settings and pauses play while retaining the active game. See the [file guide](FILES.md) and [JSON Schema](schemas/tetris-save.schema.json). All codec assets are bundled locally.

## Panels and narrow windows

The workspace orders leaderboard, game information, board, settings and controls/help. Three independent toggles above the two gameplay buttons hide the optional panels. Board position stays centered; hiding Settings also hides Save/Restore. Narrow browser windows keep compact game information beside the board and provide horizontal scrolling inside the workspace to reach side panels. Header, notices and footer remain outside that scroller. Resizing or returning focus to the board recenters it without changing play or configuration. Text wraps at increased text scale.

## Windows desktop

The Windows ZIP bundles Electron and the full shared renderer, codecs and runtime assets. Extract everything and run Tetris.exe; no Node.js or server installation is required. It is an unsigned portable development distribution. See [Windows installation](platforms/electron/INSTALL.md) and [host/verification details](platforms/electron/README.md). Native Linux Electron checks exercise the packaged app resources; native Windows execution is separately reported and is not inferred from them.
