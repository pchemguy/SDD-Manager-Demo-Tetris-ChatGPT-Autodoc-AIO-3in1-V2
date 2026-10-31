# Installation and controls

## Browser

Extract tetris-browser.zip into one directory. Serve that directory through ordinary static HTTP(S) hosting, then open its index page. No application backend or Node.js runtime is needed to play. For a local test with Python available, run python -m http.server 8000 from the extracted directory and open http://localhost:8000. Opening the page as a file URL is unsupported for persistence.

## Keyboard

Start with the left Start button. Left/Right move, Down soft drops, Up or Space rotates clockwise, Z rotates back, Enter hard drops, C holds, X activates a penetrator bonus, P pauses/resumes and R restarts. A grounded piece locks after one full gravity interval; hard drop follows that delay and movement on the ground does not restart it. The two information-panel gameplay buttons are Start/Restart and Pause/Start. Losing focus pauses; return and resume explicitly.

## Distribution status

The browser bundle is a static deployment artifact. Releases through v0.8.0 contain the browser app; v0.9.0 adds Windows and v0.10.0 adds both sidebar extensions. Desktop and extension packages are unsigned development distributions; no store distribution or signing is implied.

## Special landing rules

Clearing four rows awards one penetrator bonus, up to three. An activated piece passes through occupied cells without destroying them; its ghost and hard drop choose the lowest entirely valid landing. Hold is disabled while active. White marks penetrator cells, including settled cells. Dynamic ghost visibility hides the projection if any occupied cell is above the board midline, including a piece that straddles it.

## Settings continuity

Use canonical query keys ghost, hardDrop, next, hardDropLock, lock and hold. For example, ?ghost=dynamic&lock=interval&hardDropLock=immediate selects a dynamic ghost and immediate hard-drop locking. Each valid explicit parameter overrides its saved tetris_ cookie, which overrides the default. Invalid/duplicate values fall back independently with a status message. Settings changes update that key's cookie and URL; omitted keys retain their cookies. Use the same origin/profile to reopen saved settings. Cookie restrictions may prevent continuity and produce a warning. The session leaderboard keeps only the ten best completed games and clears on page reload. Scores are not written to cookies or persistent storage. Manual JSON/SQLite Save and Restore are available at the bottom of Settings. See FILES.md in this package. Restored scores remain session-only; restoring settings updates cookies and URL values.

## Panel layout

Use the three information-panel toggles to show/hide leaderboard, settings and controls/help. The board and information panel remain available. At narrow window widths, scroll horizontally within the workspace to reach optional panels; the board recenters on resize, panel toggles and board focus. Settings and files retain their state when hidden.

## Windows package in this release

Download the separate tetris-windows-x64.zip, extract all files together and run Tetris.exe. It includes Electron and the app runtime, so no separate Node.js or development server is needed. This is an unsigned portable development package, not a signed installer or store distribution. Its own INSTALL.md explains the app-owned local HTTPS origin, profile settings and supported launch query. Native Windows execution is a separately reported verification limit.

## Sidebar extensions

Use tetris-chromium-extension.zip with Chromium 116+ Developer mode / Load unpacked, or tetris-firefox-extension.zip with Firefox 115+ about:debugging / Load Temporary Add-on. Extract first and select the manifest root. Firefox temporary add-ons disappear after browser restart. The included extension-specific INSTALL.md explains local settings, paused browser-session recovery, ownership, files and native-verification limits. Neither package is signed or store-distributed.
