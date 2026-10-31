# Component decomposition

## Component model

[ARCHITECTURE](ARCHITECTURE.md) owns the major blocks. The components below assign state and interfaces within them. [SPEC](SPEC.md) supplies observable contracts; physical allocation belongs to layout.

| Component | Owns and provides | Requires and excludes | Verification seam |
| --- | --- | --- | --- |
| Board and piece geometry | Board occupancy, tetromino orientations, collision and row compaction functions | Coordinates and immutable cells; no input, time or rendering | Small board fixtures, rotations and compaction snapshots |
| Piece source | Baseline independent random selection and modern 7-bag queue | Injected random draws; no global Math.random in rule code | Seeded draws and bag-permutation assertions |
| Rotation and landing rules | Basic rotation, modern SRS wall kicks, normal/penetrator landing search and ghost projection | Geometry and board; does not spend bonuses or change state | Known kick fixtures, cavities, overlapping transit and deepest valid landing |
| Game reducer | Active piece, board, score, level, hold state, penetrator bonuses, lock deadline, lifecycle and event emission | Geometry, piece source and rule functions; no host APIs | Command/time sequences with explicit deterministic inputs |
| Settings validator | Canonical six-value settings object, defaults and per-key parsing | Raw external values; no host reads or writes | Value tables, invalid/unknown entries and precedence cases |
| Leaderboard | Immutable result list, top-ten order, stable record identity and duplicate rejection | Completion events, ID and UTC ports; no disk persistence | Ties, repeated completion and restore candidate fixtures |
| Snapshot validator | Versioned settings/results structure, timestamp and ID semantics, size/count limits | Decoded candidate; neither parses files nor mutates live state | Full invalid-input matrix and JSON Schema agreement |
| JSON codec | UTF-8 JSON parsing/export, duplicate-key rejection and schema validation | Snapshot validator and bundled schema validator | Round trips, malformed syntax and full-content rejection |
| SQLite codec | Fixed schema creation, metadata, prepared inserts and read-only import queries | Bundled SQLite runtime and snapshot validator | External SQLite inspection and cross-format semantic equivalence |
| Application controller | Single serialized state transition queue; setting updates, completion insertion, import commit and UI snapshots | Reducer, validators, leaderboard and narrow host ports | In-memory host ports with injected failures and side-effect history |
| Input mapper | Keyboard/button mapping, focus checks and repeat handling | Application commands; no direct reducer field access | Browser keyboard/focus events and command observation |
| View | Canvas board/ghost/previews plus information, settings, leaderboard and help DOM | Read-only application snapshots and command callbacks | Screenshots, semantic DOM checks, responsive geometry and keyboard reachability |
| Browser host | Cookie/URL settings, monotonic clock, timestamps, IDs and Blob/file-input operations | Browser APIs; no rule code | Browser context cookie/history/filesystem assertions |
| Desktop host | Fixed packaged app origin, window policy, application lifecycle and Electron download behavior | Electron main-process APIs; no Node access in renderer | Packaged resource inspection, protocol traversal rejection and host smoke checks |
| Extension host | Separate manifests, panel launch, settings storage.local, transient storage.session and single-panel ownership | Extension APIs; no webpage content access or background gameplay | Host API contract doubles, manifest lint and actual extension/panel checks where available |
| Build and release assembly | Bundled host entry points, dependency notices, archives, checksums and asset-name checks | Locked dependencies and verified source/version; no gameplay ownership | Extracted archive inventory and actual release downloads |

## Core command and state boundaries

The reducer accepts start/restart, pause/resume, move, rotate, soft drop, hard drop, hold, activate penetrator and advance-time commands. Its result contains a new state plus lock/line-clear/game-over events. A completed-game event carries score exactly once; the application assigns the stable ID and UTC timestamp, then ranks it. Immutable reducer state and injected queue state allow a paused snapshot to resume deterministically.

Geometry defines whether a position is in bounds and non-overlapping. Landing defines the destination for normal or penetrator mode. The reducer owns activation and locking, so searching for a ghost can never spend a bonus, merge cells or trigger scoring. Hold exchanges regular pieces only and does not transfer penetrator state.

## Timing and lifecycle collaboration

The clock adapter reports monotonic elapsed deltas while the controller is running. The reducer owns gravity accumulation and grounded lock timing. The controller pauses on host lifecycle events, releases held keys and suspends advancement. Restoring or reopening a running snapshot changes it to paused before accepting input. UI and panel ownership never create a second timer.

Extension storage/ownership operations are serialized by a single coordinator with a monotonically increasing generation. Each write carries its generation; stale panel writes are rejected. A panel heartbeat identifies a live owner; loss of heartbeat or port disconnect causes the retained snapshot to be marked paused. The coordinator stores snapshots and arbitrates owners, with no rule advancement. A new panel may acquire a stale lease and always begins paused. Exact lease intervals are adapter details with tests; they cannot cause automatic gameplay or score persistence.

## Persistence and file interfaces

A settings store exposes read, write and restore-previous operations for the six keys; a URL port exposes query read and replace. Browser composition resolves each key separately; extension composition substitutes its persistent store and uses explicit page parameters only as an initial override. The transient-session port is distinct from persistent settings, making accidental score persistence detectable.

File ports accept or return bytes and a safe fixed filename. The import coordinator captures a pre-change state, obtains decoded candidate data, validates the entire candidate, stages side effects, and replaces results/settings only after success. The file is never a live database. Export captures one logical snapshot so settings cannot change halfway through serialization. Failed or cancelled operations produce readable status through the view and release temporary URLs/database objects.

## Error ownership

Invalid player commands are harmless domain no-ops. Invalid external configuration is reported by the application and resolved per-key. Codec errors contain a user-facing category and technical detail for diagnostics without mutating state. Host storage failures are reported separately from validation failures. Rendering failures cannot be used to accept an import. Initialization failures disable only the unavailable file format where possible and explain the recovery action.

## Boundary assessment

Each rule has one domain owner; codecs and rendering do not share mutable board state. JSON and SQLite converge on one candidate model, and every host supplies the same application ports. No general plugin registry, service container or backend is required. Tests can exercise the real reducer, controller and codecs independently, while browser/host checks establish integration assumptions.
