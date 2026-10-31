# Tetris across browser, Windows and browser sidebars

## Purpose and outcomes

Develop a keyboard-controlled Tetris game for desktop players, starting with a simple playable browser baseline. Add the complete gameplay, configuration, leaderboard and file capabilities through bounded useful increments, then deliver a Windows Electron app and Chromium and Firefox sidebar extensions. Most application logic and UI should be shared, with platform integrations kept separate.

## Complete target scope

The classic baseline provides a falling-block board, movement, rotation, gravity, line clearing, scoring, levels, game over, restart and pause. The game information panel shows score and level and has exactly two clickable gameplay buttons at its bottom: Start/Restart on the left and Pause/Start on the right. Other gameplay actions use the keyboard.

Modern rules add hold, next preview, ghost, 7-bag randomization, wall kicks, hard drop and a full gravity-interval lock delay. Conditional ghost visibility depends on the projected landing position. Penetrator bonuses are earned by clearing four lines, capped at three, and spent by hotkey to let the current piece pass through occupied cells until it locks at an entirely in-bounds, non-overlapping position. Its hard drop and ghost use the same deepest valid landing; penetrator pieces are entirely white and regular pieces never use white. One symbol per available bonus appears in game information.

Six settings control ghost visibility, hard drop, next preview, hard-drop locking policy, general locking policy and hold. Deliver session-only settings before persistence. Browser persistence resolves each setting independently from URL parameter, cookie, then default; changing a setting updates both URL and cookie, and explicit valid URL values are saved even when equal to defaults.

A session leaderboard keeps the ten highest completed-game scores. Manual Save and Restore controls belong at the bottom of settings and disappear with that panel. Both JSON and SQLite files carry the leaderboard, all six settings and format versioning, preserving stable result IDs, non-negative integer scores and UTC completion timestamps. Supply a JSON Schema. Validate the entire file before applying anything; invalid restores leave results, settings, cookies and URL unchanged. SQLite uses high_scores(id, score, timestamp) and uniquely keyed settings(key, value), with format version in database metadata.

Browser and desktop panels run left to right: leaderboard, game information and controls, centered board, settings, controls/help. The board and game information stay visible. Three independent visibility toggles sit above the two gameplay buttons. Showing or hiding panels preserves board centering; extensions adapt this layout to a narrow resizable sidebar while retaining access to all capabilities.

## Delivery constraints

Deliver browser first, Windows Electron after browser UI layout is verified, and both browser extensions together after Windows delivery. Windows and extension packages bundle their runtime assets and require no separately installed Node.js, development server or backend. Browser availability continues through later releases.

Choose and maintain versions and publish a GitHub release after each completed, verified and integrated implementation phase. Each release contains verified deployable/installable artifacts for all platforms delivered by that point, installation instructions and clear unsigned/development versus signed/store status. Use stable version-free release asset names with platform suffixes. Do not call a platform delivered before its packaged artifact passes applicable checks; report unavailable native checks and remaining unverified behavior explicitly.

## Proposed decisions requiring brief approval

| Interaction | Proposed direction |
| --- | --- |
| Ghost straddling midline | Hide whenever any occupied ghost cell is above the midline; show only when all cells are in the lower half. |
| Lock delay | Start a full current gravity interval on grounding; horizontal moves and rotations do not restart it unless the piece actually lifts off. Pause freezes elapsed game time. A hard drop following the general policy does not restart an existing grounded countdown. |
| Penetrator and hold | Hold is disabled while the current piece is a penetrator. Failed or repeated activation spends no bonus. Locks never overlap existing cells; intermediate passage does not erase them. |
| Invalid configuration | Reject malformed or unknown setting values per setting, show a clear diagnostic, and fall through to the next valid source without affecting valid settings. |
| Active-game setting changes | Apply immediately. Changing general lock policy recomputes grounded timing without granting repeated timer resets; disabling hold or hard drop prevents subsequent use. Precise transitions belong in SPEC. |
| Extension lifecycle | Pause on focus loss, hidden panel or closure; require explicit resume. Reopen the same browser-session snapshot paused; do not persist leaderboard or active game across browser restarts. Background code may retain state but never runs gameplay. |
| Extension configuration and files | Use extension-local settings storage instead of cookies and ongoing URL synchronization. Valid explicit extension-page parameters can seed settings; omitted values retain stored values. Save/Restore uses bundled file codecs and a panel download/file-picker flow with the same complete-validation rule. |
| Restart and completion | Only game-over results enter the leaderboard; restarting an unfinished game abandons it without a completed-game entry. |

## Technical direction and delegated details

Recommend a shared TypeScript game core, Canvas board and ordinary HTML controls, with thin browser, Electron and extension adapters. This supports deterministic gameplay checks and reuses the UI without a large UI framework. Plain JavaScript would reduce type tooling but weaken state-contract checks; a framework would add dependencies without a demonstrated need. The proposed shared TypeScript approach is subject to brief approval.

Architecture and SPEC will choose exact scoring, progression, key bindings, sensible setting defaults, persistence keys and strict file limits, while preserving these approved material interactions. Prefer established rotation and wall-kick rules. All external runtime dependencies must be bundled for desktop and extensions.

## Scope boundaries

No account system, backend leaderboard, multiplayer, automatic score persistence or automatic file synchronization is requested. Signing and store distribution are not assumed; development packages must be labeled accurately. UI visibility is separate from the six exported gameplay settings.
