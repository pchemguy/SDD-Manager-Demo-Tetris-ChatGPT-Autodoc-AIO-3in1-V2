# Configuration contracts

## C-1: Canonical settings

Exactly these six keys comprise the gameplay configuration. JSON, SQLite, query parameters, cookies and adapters use the same canonical strings. Boolean-looking settings are strings, not permissive truthy values.

| Key and label | Allowed strings | Default | Behavior owner |
| --- | --- | --- | --- |
| ghost / Ghost visibility | hide, dynamic, show | show | G-4 projected occupied-cell predicate |
| hardDrop / Hard drop | on, off | on | G-4 and G-5 |
| next / Next-piece preview | on, off | on | G-3 |
| hardDropLock / Hard-drop lock | general, immediate | general | G-5 |
| lock / General lock | failed, interval | interval | G-5 |
| hold / Hold piece | on, off | on | G-3 |

The session-only settings release keeps state in page memory and does not read/write cookies, persistent storage or query parameters. Reload starts at defaults. Earlier gameplay releases use their scoped fixed behavior: classic baseline uses failed-attempt lock; modern rules use interval locking; the conditional-ghost release uses dynamic visibility until settings expose its selection.

Changes apply immediately without restarting play. Turning preview off hides it without changing the queue. Turning hold or hard drop off blocks subsequent commands. Turning either on preserves existing hold eligibility and active state. Lock policy transitions obey G-5. Invisible settings continue to apply; hiding a panel never resets its values.

## C-2: Browser URL/cookie resolution

Use the canonical key names above as query parameters and cookie names prefixed tetris_. Parse each setting independently. A single exactly matching decoded URL value takes precedence; otherwise try its valid cookie, otherwise default. Empty, unknown, case-mismatched, malformed percent encoding or repeated values for one recognized parameter are invalid for that key. Never coerce unknown strings, numbers or booleans into canonical values. Unknown unrelated URL parameters remain untouched. Report invalid recognized inputs by key in a clear non-blocking status.

On startup, save each valid explicit URL value into its corresponding cookie, including values equal to defaults. A parameter omitted from the URL does not overwrite its cookie or force a default into the cookie. An invalid explicit value does not overwrite a valid saved cookie; leave the original URL parameter unchanged until a user setting change or successful Restore replaces it. Cookie values are percent-encoded; decode safely and reject duplicate same-name cookies as ambiguous.

On a user change, save that setting's canonical value in its cookie and replace all instances of its query key with exactly one selected value using history.replaceState. Preserve unrelated parameters, pathname and fragment. Cookie attributes: Path=/, SameSite=Lax, Max-Age=31536000, Secure on HTTPS/app secure origin. Detect cookie write/readback failure and report that persistence could not be confirmed; do not falsely claim saved state. A setting selected in the session can still remain usable if persistence is blocked.

Successful Restore writes all six cookies and all six query values and applies them as one application-level replacement. Invalid files write nothing. Snapshot and rollback old host values if a write operation fails after validation; report a rollback failure and block further persistence until reconciliation. JavaScript cannot make browser history and cookies crash-atomic, so do not claim resilience to process termination mid-commit. This limitation does not weaken invalid-file non-mutation.

## C-3: Desktop and extension adaptations

The desktop secure app origin supports the same cookie/query contract through its Electron session and renderer history; persistence is local to that application profile. Use the packaged root URL on startup, then resolve cookies. A URL entered through a supported app launch path uses the same per-key precedence; arbitrary remote navigation is not a supported configuration channel.

Extensions replace cookies with extension storage.local, storing the six keys under one versioned settings object. Valid explicit query values in the extension panel entry URL override local values at initialization and save back, including default-valued strings; omitted/invalid values retain valid stored values. There is no ongoing extension-page query synchronization requirement. User changes and successful Restore update the same local settings object. All six values remain canonical; corrupted stored values fall back independently with a diagnostic.

Keep extension game snapshots and score history in storage.session under separate keys. Browser/extension restart clears them; persistent settings remain. No adapter may silently persist scores to storage.local, cookies or a desktop settings file. Reopening a panel in the same session does not count as a fresh browser session.

## C-4: Validation acceptance

Check all allowed values, each invalid category, all three precedence sources per key, mixed-source startup, explicit default values, omitted parameters, duplicate recognized parameters, unrelated query preservation and fragments. Observe actual cookie values and URL after user changes and successful restores. Verify the intermediate session-only build performs no persistent settings writes. Adapter checks cover rejected asynchronous storage writes and distinction between persistent settings and transient results.
