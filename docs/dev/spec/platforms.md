# Presentation and platform contracts

## U-1: Browser and desktop workspace

Five panels appear left to right: leaderboard, game information and controls, board, settings, controls/help. Board center stays at the viewport horizontal midpoint when panels are toggled. Use symmetric side reservations sized for the larger side; hiding a panel does not collapse that symmetry. On narrow browser/desktop windows where the five-panel arrangement cannot fit, preserve the ordered workspace with horizontal overflow and a clearly reachable board/information group. Do not obscure game information behind optional panels. Verify viewport widths 640, 960, 1280, 1600 and 1920 and default plus increased text scale; no text may overlap the board.

The information panel shows score, level, cleared lines, lifecycle, hold and next preview when available/enabled, and one bonus symbol per available penetrator activation. At its bottom, the only two clickable gameplay controls are the left Start/Restart and right Pause/Start button. The left label is Start before the first game and Restart thereafter. The right label is Pause while running and Start while idle/paused/game-over; its action starts a fresh game from idle/game-over or resumes paused play. Above them are exactly three distinct show/hide toggles for leaderboard, settings and controls/help, with aria-expanded and correct target names.

All panels default visible in the full layout. Panel visibility does not affect any game setting and is not exported among the six settings. Keyboard help shows the actual bindings. File-operation controls belong only in settings. Native focus navigation and form controls remain usable without moving the falling piece.

## U-2: Sidebar presentation

Adapt to resizable sidebar widths 280, 360 and 480 pixels with a vertically scrollable layout. Keep game information and board displayed together before optional sections. Use a board fitting the available width, readable controls and at least 24 CSS-pixel actionable targets; no horizontal scrolling is required at these widths. Information-panel toggles independently reveal the leaderboard, settings and help below the game group. Keep their state and Save/Restore semantics equivalent to browser/desktop.

Do not inject the game into the visited page or modify page content. Keyboard gameplay is scoped to the focused extension panel. Resizing must not reset the game, clear history or change settings.

## P-1: Host lifecycle and extension sessions

Browser and desktop focus loss or hidden document automatically pauses running play; returning focus never resumes automatically. Extension blur, hidden panel or closure has the same effect. Release held input on pause. Reopening a panel in the same browser session restores the retained board/queue/RNG/hold/bonuses/timing, settings and score list, always paused; a new browser session starts idle with no scores and persistent settings restored.

Use extension storage.session for transient snapshots/results and storage.local only for the six persistent settings. A single coordinator arbitrates panel ownership so two windows cannot advance the same game. A secondary panel is read-only until it obtains ownership and explicitly resumes; acquiring ownership pauses the previous owner. Background service workers/scripts never advance gravity, lock time or scoring.

After each accepted command and elapsed-time update, serialize the latest snapshot into transient storage; coalesce redundant renders, not state commits. Await a final save on explicit pause and ownership transfer. Browser teardown may prevent the last asynchronous save; recovery uses the latest confirmed snapshot and begins paused, with a recovery notice if the generation is stale. Do not promise lossless recovery after process crashes or extension reload/update. Storage failure pauses the panel and explains the issue; it must not silently switch to persistent score storage.

## P-2: Browser package

Ship a static bundle that works when extracted and served over ordinary HTTP(S), with no backend. Include index entry, assets, dependency notices and installation instructions. File:// browser launch is not a supported persistence/deployment path. Browser startup makes no required external runtime request. Query/cookie persistence uses C-2.

## P-3: Windows Electron package

Ship an unsigned Windows x64 portable ZIP containing the executable, Electron runtime, resources, shared UI build, SQLite runtime and installation/launch instructions. Extraction and launching the executable require no system Node.js or development server. Label it unsigned development distribution, not signed installer or store distribution. Native Windows execution is reported separately from cross-built archive checks.

Use a stable secure app origin with a fixed protocol handler rooted in bundled resources; reject traversal, unexpected hosts and methods. Preserve query strings/fragments for the renderer while mapping only a whitelisted pathname to files. Enable standard/secure origin privileges needed for cookies/history/Wasm. Use an Electron persistent session for settings cookies, sandbox/context isolation, no Node renderer integration, no arbitrary filesystem IPC and no remote navigation/popups. Download Save files through Electron's download handling with the same names/content; Restore uses the ordinary file chooser.

## P-4: Extension packages

Produce both Chromium MV3 and Firefox sidebar packages in the final platform phase. Chromium uses side_panel with a default panel page and action-click launch through sidePanel. Firefox uses sidebar_action with the same application panel entry and its supported action/sidebar launch behavior. Set minimum versions Chromium 116 and Firefox 115, covering sidePanel.open and storage.session respectively. Verify all additional selected APIs against these floors during packaging; do not silently raise a floor or claim compatibility for unavailable APIs. Use chrome.* APIs on the Chromium floor and browser.* on Firefox through the adapter.

Bundle every script, Wasm asset, schema, icon and notice; configure extension CSP for local scripts and Wasm as required, with no unsafe-eval or remote code. Request only storage and host-specific sidebar capabilities. No content scripts, arbitrary site permissions, backend, development server or separate Node install is required. Handle promise/callback API differences in the adapter.

Distribute Chromium as an unpacked-development ZIP and Firefox as an unsigned temporary-install ZIP, with extraction/loading instructions and limitations. Do not represent either as signed CRX/XPI or store-listed. A supported signing/store workflow is outside the requested delivery unless subsequently selected.

## P-5: Releases and package verification

Use initial browser version 0.1.0 and minor increments for each capability/platform phase through 0.10.0. A patch version denotes an in-scope repair without a new capability phase. Tags are v-prefixed semantic versions. Version metadata in source, UI and applicable manifests must agree.

Use these exact stable, version-free release assets when applicable: tetris-browser.zip, tetris-windows-x64.zip, tetris-chromium-extension.zip, tetris-firefox-extension.zip and SHA256SUMS.txt. Release notes identify version, delivered capabilities, installation, development/signing status, performed checks, unavailable checks and remaining unverified behavior. Each release includes all platforms delivered by that phase, rebuilt/verified against its selected source where shared changes affect them.

Before tagging/publication, verify scripts enforce the name set, archive inventory has no secrets/development dependencies, all resource references resolve locally, and the packaged application passes scoped smoke/functional checks. Browser/desktop/extension assets include their SQLite dependencies after file support arrives. Inspect Windows PE/runtime/resource layout even without Windows execution; exercise the same renderer/protocol on an available compatible host where feasible. For extensions, validate manifests/CSP, run available lint and shared panel checks, and attempt actual sidebar lifecycle testing with isolated profiles. Distinguish unavailable actual-sidebar checks from successful panel-page checks.

After verified integration, publish the release tag on the eligible default-branch release commit and upload only the verified archives. Read back release/tag/source identities, asset names and sizes; download the hosted assets and compare SHA-256 bytes with local verified outputs. Check latest-release status and version-free latest/download links. A completed build or an uploaded asset without these applicable checks is not a verified platform delivery.

## API reference basis

[Chrome sidePanel](https://developer.chrome.com/docs/extensions/reference/api/sidePanel) documents programmatic launch support; [MDN storage compatibility data](https://github.com/mdn/browser-compat-data/blob/main/webextensions/api/storage.json) documents Firefox session-storage support. [Chrome storage](https://developer.chrome.com/docs/extensions/reference/api/storage) and [Firefox storage.session](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/session) define transient storage lifetime. Verify candidate-specific packaged behavior independently of these API references.
