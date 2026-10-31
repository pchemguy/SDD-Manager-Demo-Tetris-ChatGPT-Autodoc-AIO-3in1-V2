# Tetris for Windows x64

This is an unsigned portable development package. It is not a signed installer or Microsoft Store distribution. The upstream Electron runtime and its licenses are bundled; this does not make the custom application a signed distribution.

Extract the entire tetris-windows-x64.zip archive into a writable folder. Keep Tetris.exe, its DLL/data/locales and resources directory together, then launch Tetris.exe. No separate Node.js installation, development server or backend is needed. Verify the archive against SHA256SUMS.txt before installation.

The app uses the same keyboard game, settings, leaderboard and manual JSON/SQLite files as the browser build. Three information-panel toggles hide optional panels. Focus loss/minimization pauses; returning requires explicit Start/P to resume. Completed results remain session-only; close/reload starts a fresh history. Configuration cookies use the application profile and are separate from score history. Read FILES.md beside this guide for manual Save/Restore and schema details.

The stable local origin is app://tetris/index.html. To supply explicit settings at launch, quote one complete argument, for example:

```text
Tetris.exe "--game-url=app://tetris/index.html?ghost=dynamic&hardDropLock=immediate"
```

Only this app origin and its index entry are accepted. Remote URLs or traversal paths cannot become launch destinations. Query parameters override saved cookies independently; omitted keys retain saved values. Renderer code has no Node integration, preload or arbitrary filesystem IPC. Native file selection/downloads remain user-initiated.

The package pins Electron 45.2.1 and includes the required Windows x64 runtime assets. runtime-info.json records upstream archive identity; build-info.json records application version and source. The package's archive inventory, executable/DLL PE architecture, runtime hashes, shared renderer and host-policy checks are verified during development. Native Windows launch is a separate check; do not infer it from Linux/browser tests. Release notes and phase reports state exactly which native checks were available.
