# Gameplay contracts

## G-1: Board, pieces and lifecycle

Use ten columns and twenty visible rows, indexed x=0..9 and y=0..19 with y increasing downward. Two spawn rows y=-2,-1 may hold active cells but are never stored in the settled board. The seven tetrominoes are I, O, T, S, Z, J and L, with four-cell standard shapes and rotations. Use cyan, yellow, purple, green, red, blue and orange respectively; none is white. A penetrator and its visible ghost use white with opacity/outline differentiation.

A new game clears board, score, lines, hold and bonuses, resets level to 1 and creates a new piece source. Spawn orientation is 0 with origin x=3,y=-1. Local occupied cells are I: (0,1),(1,1),(2,1),(3,1); O: (1,0),(2,0),(1,1),(2,1); T: (1,0),(0,1),(1,1),(2,1); J: (0,0),(0,1),(1,1),(2,1); L: (2,0),(0,1),(1,1),(2,1); S: (1,0),(2,0),(0,1),(1,1); Z: (0,0),(1,0),(1,1),(2,1). Generate orientations 0,R,2,L by clockwise quarter-turns around local pivot (1,1) for JLSTZ and (1.5,1.5) for I; O rotation leaves its cells unchanged. Clockwise rotation in downward-y coordinates maps a local offset (dx,dy) to (-dy,dx). Reject any active cell above y=-2, below y=19 or outside x=0..9. Settled occupancy checks ignore negative rows. A blocked spawn ends the game. An attempted lock with any cell above row zero ends the game without writing outside the board. Game over reports the current score exactly once.

Lifecycle is idle, running, paused or game-over. Start from idle/game-over creates a fresh game. Restart while running/paused abandons that game without adding a result. Pause freezes gravity, lock deadlines and held input; resume continues remaining time. No gameplay command except start/restart/resume changes idle, paused or finished games.

## G-2: Baseline movement, score and progression

Move one column left/right if the resulting position is valid. Soft drop advances one row if possible and awards one point per successful row. Baseline rotation tries the next orientation in place and rejects collision; no wall kicks, hold, ghost, preview, penetrator or hard drop are required in the classic baseline. Baseline piece selection is independent uniform selection among seven types.

The baseline locks on a failed downward gravity or soft-drop attempt. Merge four cells, remove all complete rows simultaneously, compact surviving rows downward, then spawn the next piece. Score 100/300/500/800 multiplied by the level before the clear for one/two/three/four rows respectively. Level is 1+floor(total cleared rows/10). Gravity interval is max(100, 1000 * 0.8^(level-1)) milliseconds, using floating-point elapsed comparisons. No T-spin, combo or back-to-back scoring is required. Score is a non-negative safe integer; saturate at Number.MAX_SAFE_INTEGER if an addition would exceed it.

Hold left/right for repeat after 150 ms with a 50 ms repeat interval; perform the first movement immediately. Soft drop repeats at 50 ms while held. Rotation, hold, activation, pause/restart and hard drop fire once per physical key press, ignoring synthetic repeat keydown events. Release all held keys on blur/pause. Use an elapsed-time accumulator rather than relying on operating-system repeat rates.

## G-3: Modern piece source, hold and rotation

A 7-bag source shuffles each complete set of seven pieces independently with unbiased Fisher-Yates using the injected RNG. Every bag contains each piece exactly once; refill before the current queue runs out. Next preview shows the next one piece when enabled.

Hold stores the active type and either consumes the next piece or swaps with the held type. The incoming piece uses spawn orientation/location. Permit one hold per active-piece lifecycle, resetting eligibility only after a lock. Blocked held-piece spawn ends the game. Hold preserves score and bonuses, consumes no bonus and never carries penetrator state. Disabling hold or activating a penetrator prevents hold for that active piece while disabled/active; toggling the setting does not reset once-per-piece eligibility.

Use standard SRS orientations/pivots and ordered wall-kick candidates for I and JLSTZ, with the O piece stationary on rotation. Try candidates in order and accept the first valid result; reject rotation when all candidates fail. Test fixed wall/floor/kick fixtures, including separate I behavior, both rotation directions and rejected cases. Row coordinates increase downward, so convert any reference kick data consistently.

## G-4: Landing, ghost and hard drop

For a regular piece, landing is the lowest position reachable by consecutive one-row collision-free descent from its current position. Ghost previews that position and never changes state. Hard drop moves directly there and scores two points per descended row. Repeated drop at the same position awards zero extra points. Disabled hard drop is a no-op.

For a penetrator, landing is the maximum downward y offset for which all four final cells are within visible board bounds and none overlaps a settled cell. Occupied cells between the current piece and landing do not block descent and are not removed. Search every candidate through the bottom bound rather than stopping at the first blocker or first valid cavity. The ghost and hard drop call this same landing definition.

In dynamic ghost mode, hide the ghost whenever any of its four occupied projected cells has y<10. Show it when all projected cells have y>=10. Use occupied cells, not the bounding-box origin; a straddling piece is hidden. Always-hide/show override this predicate. When the ghost coincides with the active piece, rendering may suppress the duplicate while preserving its logical position.

## G-5: Grounding and locking

A normal piece is grounded if its next downward row is invalid. A penetrator is grounded only when it is at its deepest valid landing. Passing through occupied cells is transit, not grounding. After a successful move/rotation/drop or gravity step, detect grounding at that event's game time.

With interval locking, set one deadline at grounding time plus the gravity interval at that moment. Lateral moves/rotations while still grounded retain the original deadline; they do not reset it. Only actual lift-off clears the grounded deadline; subsequent grounding starts a new full interval. Gravity interval changes do not shorten an existing deadline. Pause freezes elapsed game time. If a command and deadline coincide, process the due lock before the command, so input cannot escape an expired deadline.

A failed soft-drop/downward gravity attempt during the interval does not lock early. Hard drop with the general policy starts a full delay only if it newly grounds the piece; an already grounded piece retains its deadline. The immediate hard-drop policy locks at the drop command, independently of the general policy. With failed-attempt locking, hard drop using general policy moves to landing and waits until a subsequent failed downward command/gravity attempt; it does not count its own search boundary as that attempt.

Changing general policy to interval while already grounded uses the recorded grounding time and the interval captured there; if expired, lock immediately. Changing to failed-attempt removes the pending deadline but retains grounding history; a later switch back cannot restart the interval. A genuine lift-off resets this history. Hard-drop immediate policy affects subsequent drops, not a piece merely sitting on the floor. Settings changes are serialized with game events.

Use elapsed-time substeps at scheduled gravity/lock/input-repeat boundaries. Never skip a lock because a frame was delayed. On focus loss or document visibility loss, pause before further advancement; do not catch up hidden-wall-clock time on resume. Time advancement is deterministic for equivalent command/time sequences.

## G-6: Penetrator activation and valid transit

Clearing exactly four rows simultaneously awards one bonus, capped at three. A successful X activation spends one bonus immediately and makes the current piece a penetrator until it locks. The indicator renders one symbol per available bonus and updates on earn/spend. At zero bonuses, while already active or outside running state, activation is a no-op with no spend.

Activation starts from the currently valid regular position and recomputes landing/grounding. If the piece can now descend through occupied cells, it lifts off and clears the grounded deadline. Do not destroy settled cells. Penetrator lateral/rotation moves may pass through occupancy but must stay inside horizontal/floor bounds and leave at least one valid final landing at or below the resulting position. Reject transformations without such a landing. Rotation still respects piece orientation and bounds; SRS candidate order chooses the first position satisfying these penetrator validity rules.

Downward transit may overlap settled cells; final locking may not. Intermediate overlaps do not clear lines or cause game over. At the deepest valid landing, apply the selected general/hard-drop lock policy. Merge the four final cells, clear rows, award score/bonuses and reset penetrator status for the newly spawned regular piece. Hold is disabled while penetrator is active. Restart clears unused bonuses and active status.

## G-7: Keyboard and focus

Use Left/Right arrows for horizontal movement, Down for soft drop, Up or Space for clockwise rotation, Z for counterclockwise rotation, Enter for hard drop, C for hold, X for penetrator, P for pause/resume and R for restart. Show these bindings in help. Space rotates rather than dropping. Keyboard events originating in select/input/textarea/button or editable content keep their native behavior; a focused button is activated natively, without an extra game command. Only handled game keys prevent page scroll/defaults, and modifier shortcuts are not intercepted. Tab navigation remains available.
