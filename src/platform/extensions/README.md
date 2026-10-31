# Extension host boundaries

`Coordinator` serializes acknowledged writes and transfers ownership. It never advances time or applies game commands. `storage.local.settings` contains only `{formatVersion: 1, settings}`; `storage.session.session` contains `{formatVersion: 1, generation, session: {game, results}}`. All six canonical settings are stored together. Session data is validated before use and detached from callers.

Each connected document has a unique identity and increasing command sequence. Only the owner can commit state, settings or a Restore. A transfer asks the previous owner to pause and flush its accepted commands before returning a final snapshot. A bounded unresponsive-owner fallback uses the last confirmed snapshot and reports possible recent input loss. Disconnect and background recreation recover paused state; elapsed time while closed never advances play. Browser restart clears the transient store, including results.

A valid explicit panel URL setting seeds local settings (including defaults); omitted or invalid values retain the saved value. A secondary panel stays read-only until its existing Start button explicitly takes control. The extension does not rewrite panel URLs or use cookies.

Storage acknowledgments include readback. A foreground write failure must pause play and explain how to recover. File validation happens before either store is touched; Restore coordinates settings/results with rollback on failure. No permanent-score fallback is permitted.
