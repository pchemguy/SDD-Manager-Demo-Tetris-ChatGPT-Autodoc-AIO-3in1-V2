# Install the sidebar development packages

These ZIPs are unsigned development packages. They are not signed extensions or store distributions. All runtime code, icons, SQLite WebAssembly and the save-file schema are included; no Node.js, development server, backend or account is needed.

## Chromium 116 or later

Extract `tetris-chromium-extension.zip` into a folder. Open `chrome://extensions` (or your Chromium browser's extension manager), enable Developer mode, select **Load unpacked**, and choose the folder containing `manifest.json`. Use the extension's toolbar action to open Tetris in the side panel. Keep the extracted folder available. Sidebar support in other Chromium derivatives depends on that browser implementing the Chromium side-panel API.

## Firefox 115 or later

Extract `tetris-firefox-extension.zip`. Open `about:debugging#/runtime/this-firefox`, select **Load Temporary Add-on**, and choose the extracted `manifest.json`. Open Tetris using its toolbar action or the browser's sidebar selector. This temporary installation lasts until Firefox restarts. Normal permanent installation requires a Mozilla-signed package, which this release does not provide.

## Play, close and reopen

Use the keyboard controls in Help. Existing Start/Restart and Pause/Start are the only clickable gameplay actions. The narrow layout places game information and board before the optional leaderboard, settings and help; use the three toggles to show or hide those sections. Resize without restarting play.

Focus loss, hiding or closing a panel pauses play and clears held keys. Reopening recovers the confirmed game paused, including its remaining gravity/lock interval. Press Start or P to resume. If several panels/documents are open, one owns play; other panels show a read-only snapshot. Their existing Start button or restart hotkey explicitly takes control, pausing the old owner before play resumes or restarts.

Settings persist in extension-local storage. Game, queue/RNG/hold/bonuses/timing and the top-ten leaderboard use extension session storage and clear when the browser session ends. Extension disable/reload/update may also clear that transient store. Scores are never automatically persisted across browser restarts. Abrupt termination may lose recent input that had not been acknowledged; recovery reports this possibility. Storage failures pause play with a recovery message, rather than switching to persistent score storage.

## Settings and files

All six browser settings are available. An explicitly supplied valid query parameter on the panel document seeds its extension-local setting, including a value equal to the default. Omitted or invalid values retain valid saved settings, then defaults. A read-only panel applies its query seed when it explicitly takes control. Extension settings changes write local storage; extension pages do not synchronize cookies or rewrite their URLs. See FILES.md for canonical query names and formats.

At the bottom of Settings, choose JSON or SQLite and select Save to download one file. Restore accepts either format by content and replaces session results and all six settings only after complete validation. It pauses the current game. Invalid input leaves results and settings unchanged. File errors appear next to the controls. Hiding Settings also hides Save/Restore. Downloads and file selection use the browser's own UI; a browser may ask for a destination. An unconfirmed storage rollback blocks further ownership and asks you to reload the extension.

## Verification boundaries

The release checks both archives, manifests, API floors, local resource bytes, checksums and shared panel behavior in Chromium and Firefox engines. The current managed Linux host blocks full Chromium's singleton Unix socket and cannot navigate Firefox's internal add-on-debugger page through the selected runner; native sidebar installation/open/close and toolbar UI checks are unverified. These limits do not represent successful native checks. Use a compatible desktop browser for native sidebar acceptance; check installation, toolbar opening, keyboard play, close/reopen paused recovery, second-panel ownership and both Save formats.
