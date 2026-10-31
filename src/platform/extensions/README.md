# Extension host boundaries

`Coordinator` serializes acknowledged writes and transfers ownership. It never advances time or applies game commands. `storage.local.settings` contains only `{formatVersion: 1, settings}`; `storage.session.session` contains `{formatVersion: 1, generation, session: {game, results}}`. All six canonical settings are stored together. Session data is validated before use and detached from callers.

Each connected document has a unique identity and increasing command sequence. Only the owner can commit state, settings or a Restore. A transfer asks the previous owner to pause and flush its accepted commands before returning a final snapshot. A bounded unresponsive-owner fallback uses the last confirmed snapshot and reports possible recent input loss. Disconnect and background recreation recover paused state; elapsed time while closed never advances play. Browser restart clears the transient store, including results.

A valid explicit panel URL setting seeds local settings (including defaults); omitted or invalid values retain the saved value. A secondary panel stays read-only until its existing Start button explicitly takes control; its URL seed is applied at that time. The extension does not rewrite panel URLs or use cookies.

Storage acknowledgments include readback. A foreground write failure must pause play and explain how to recover. File validation happens before either store is touched; Restore coordinates settings/results with rollback on failure. No permanent-score fallback is permitted.

The panel composition acknowledges every accepted command/50 ms foreground clock update. A bounded backlog pauses play instead of dropping accepted snapshots. Blur, visibility loss and page teardown clear held keys and pause; a later panel explicitly resumes the confirmed remainder of gravity/lock timing. Background retirement disconnects the foreground, which pauses and requests reopening. Recent input that never reached an acknowledgment may be lost after abrupt termination.

Both Save formats use the shared full-file validators and local Wasm. Restore commits validated settings/results through the coordinator before changing the controller; invalid files never write either store. Confirmed rollback restores both stores, while an unconfirmed rollback blocks ownership until extension reload. File-operation messages sit beside the sidebar's file buttons. Browser/desktop cookie and URL synchronization remain in their own host.

`tests/platforms/test_extension_panels.py` runs exact built background/panel JavaScript with a test-only local transport bridge and per-panel production CSP. It covers both API families in real Chromium/Firefox rendering engines. This is panel-document evidence, not native extension installation/sidebar evidence. The separate opt-in native Chromium tests use a fresh profile and actual unpacked extension APIs on compatible hosts.

A newly claimed panel keeps gameplay/configuration controls gated until its query seed has been acknowledged. Foreground time and keyboard commands cannot race that initialization; explicit resume/restart is applied afterward.
