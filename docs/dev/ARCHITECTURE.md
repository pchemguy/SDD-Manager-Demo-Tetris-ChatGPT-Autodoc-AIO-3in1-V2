# Application architecture

## Context and direction

The [project brief](PROJECT.md) defines a local, keyboard-driven Tetris application shared by a browser, Windows Electron and two browser sidebar extensions. A TypeScript core supplies game behavior independently of DOM, timers, files, storage APIs and Electron. Canvas renders the board; ordinary HTML renders information, controls, settings and leaderboard. Platform adapters compose the same application with their lifecycle, persistence and packaging integrations.

## Blocks and dependency direction

| Block | Responsibility and dependencies |
| --- | --- |
| Game domain | Own board, active piece, queue, hold, scoring, bonuses and elapsed game time. Consume injected random draws and elapsed-time events; depend on no platform block. |
| Application | Serialize player commands and time advancement; own settings and leaderboard; coordinate validation, persistence and UI snapshots. Depend on domain and narrow host ports. |
| Shared presentation | Map keyboard and permitted buttons to application commands; draw snapshots and accessible HTML feedback. Depend on application contracts, never host globals. |
| File codecs | Decode and encode versioned JSON/SQLite snapshots. Depend on a shared pure snapshot validator; return candidate data without mutating application state. |
| Platform adapters | Implement settings storage, URL access, download/read, clock, lifecycle and transient sessions. Depend inward on application ports; select browser, desktop or extension integration at composition. |
| Packaging | Assemble the shared build and host entry files with all required local runtime assets. Does not own gameplay rules. |

A single application controller is the authority for state transitions. Presentation never writes domain fields. Domain events report lock, score and game completion without invoking storage. Read-only render snapshots prevent the UI from changing game state accidentally.

## State and data ownership

Game state is per running game. Settings are six independently validated values; visibility toggles are presentation state outside the exported settings contract. The leaderboard contains up to ten immutable completed-game records. File snapshots are independent values, not references to live state. UTC completion timestamps and stable IDs are assigned once through application ports when game over occurs.

Browser adapters use URL parameters and cookies for settings, and memory for scores. Desktop adapters use a packaged stable app origin so renderer URL/cookie behavior works without a development server; Electron's session partition retains cookies. Extension adapters use storage.local for settings and storage.session for paused snapshots and session scores. Never save session scores into persistent settings storage.

Extension snapshot writes are serialized after each accepted command and time advancement, with a final awaited write on explicit pause/close when possible. Reopening always forces a running snapshot into paused state before display. Unload events alone cannot guarantee writes: continuously retained snapshots bound recovery loss if the browser forcibly destroys the panel. One active owner per browser profile serializes multiple extension panels; secondary panels show the latest paused state and require acquiring ownership before running. Background code coordinates ownership/storage only, never gravity or rendering.

## Restore transaction and failure isolation

Save captures one immutable settings-and-results snapshot. JSON and SQLite export the same semantic data. Decode, structural validation, semantic validation and ranking run in isolation before the controller accepts a candidate. Untrusted SQLite is opened only as an in-memory database and queried with fixed statements; never execute imported SQL or attach external files.

Restore takes a pre-change snapshot of settings, results and host persistence. After validation, a serialized application transaction stages host updates and commits the replacement UI state. If host persistence fails, restore prior host values and keep the original application state; expose any rollback failure explicitly and block further persistence operations until reconciliation. Invalid files never enter this transaction and cause no writes. File initialization or parsing errors are local to the operation; gameplay remains usable.

## Rendering and scheduling

requestAnimationFrame supplies monotonic elapsed time to the controller. The domain advances on explicit elapsed-time input, allowing deterministic checks of lock boundaries without wall-clock sleeps. Pause stops domain time; rendering may continue to show paused state. Input is ignored for gameplay while form controls own focus, and page-scroll defaults are suppressed only for handled game keys.

Canvas coordinates stay in board units with device-pixel-ratio scaling. A symmetric browser/desktop layout reserves equal left and right space around the board so optional panels cannot move it. Narrow browser windows can scroll the symmetric workspace; sidebar presentation instead stacks the information and board with independently reachable settings/help/leaderboard sections.

## Host boundaries and dependencies

Use Vite/TypeScript for build tooling, without a server dependency in distributed packages. Bundle a pinned SQLite JavaScript/Wasm runtime and a JSON Schema validator locally; select the exact dependency versions and audit licenses at implementation. Load SQLite in the renderer without a module worker to keep one initialization path across all hosts. Resource URLs resolve from the packaged application base; no CDN is required at runtime.

Electron's main process owns only the window and a fixed app protocol mapping to bundled files. Use nodeIntegration=false, contextIsolation=true and sandbox=true; deny navigation and unexpected permissions. No general filesystem bridge is needed: shared download and file-input flows handle Save/Restore. The stable desktop origin is https://tetris.invalid/index.html, intercepted locally by the persistent session's HTTPS protocol handler before window creation. Serve only whitelisted bundled files with correct MIME types; no DNS/TLS connection or server is involved. Fixed native blur/hide/minimize callbacks dispatch the standard shared blur event, supplementing DOM lifecycle notifications without a renderer API or resume-on-focus. This built-in secure/standard scheme preserves normal Secure/SameSite cookies; the selected Electron runtime does not support cookies on custom schemes.

Chromium uses Manifest V3 side_panel and a small service worker; Firefox uses sidebar_action and its supported background entry. Manifests grant storage and sidebar capabilities without content scripts, site permissions or a backend. Both package the same shared panel build and codecs under extension CSP, including the required Wasm allowance when applicable.

## Invariants and verification seams

- No lock writes outside the board or overlaps an occupied cell.
- Ghost and hard drop use the same landing function, including penetrator rules.
- All settings entry paths share one validator; all file formats share one snapshot validator.
- No file decoder or renderer can commit settings or leaderboard state.
- Only one clock owner can advance a game; losing focus or panel ownership pauses it.
- Packaged builds reference only bundled runtime files, and artifact verification inspects actual archives.

Injected RNG, clock, identifier, UTC timestamp, storage and file ports allow focused domain checks, application rollback checks, real browser integration checks and archive-level verification. Platform integration tests complement shared tests rather than duplicating rules in host adapters.

## Reference basis

[Chrome storage](https://developer.chrome.com/docs/extensions/reference/api/storage) and [Firefox storage.session](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/session) document memory-only session storage. [Chrome sidePanel](https://developer.chrome.com/docs/extensions/reference/api/sidePanel) and [Firefox sidebarAction](https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/sidebarAction) supply distinct panel integrations. [Electron security guidance](https://www.electronjs.org/docs/latest/tutorial/security/) informs the renderer boundary; [sql.js](https://sql.js.org/) supplies an in-memory SQLite codec option. These are design inputs; live execution remains to be verified.
