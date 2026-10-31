# Leaderboard and file contracts

## F-1: Completed-game results

A result is an object with exactly id, score and timestamp. Assign id once as a lowercase UUID v4 string; it is immutable and preserved on export/import. Score is an integer from zero through 9007199254740991 inclusive. Timestamp is a real UTC completion time in canonical YYYY-MM-DDTHH:mm:ss.sssZ form, with years 0001 through 9999, valid calendar days and hours/minutes/seconds; reject leap-second 60 and impossible dates rather than normalizing them. Require parse/format round-trip equivalence.

Rank by score descending, timestamp ascending, then id ascending by ASCII code point. Keep only the first ten. Duplicate IDs are invalid in an import, even if all other fields match. Live completion uses the controller's exactly-once event guard; an already handled game cannot insert another result. Zero-score game over is valid. Restarting an unfinished game does not produce a result. Browser/desktop page reload starts an empty session leaderboard; extension panel reopening uses its transient session data, cleared on browser restart.

Restore replaces the leaderboard, including with an empty list; it does not merge histories, regenerate IDs or change timestamps. Import order may be unsorted and is canonicalized only after all records validate. Arrays containing more than ten results are rejected rather than silently truncated, preserving full-file validation. Valid live completion may insert into eleven candidates and rank/truncate to ten.

## F-2: File operation experience

One Save button and one Restore button appear at the bottom of settings. Save opens a native/select format choice with JSON and SQLite, then downloads one file. These are file-operation controls, not extra gameplay buttons. Restore uses a file picker accepting either format. Cancellation leaves all state unchanged and is not an error. Hide settings to hide both buttons and their format choice.

Capture one immutable export snapshot; export does not pause or end play by itself. Opening native dialogs or losing focus pauses according to lifecycle rules. A completed restore pauses a running game without resetting its board, score or queue, and applies restored settings before explicit resume. Invalid/cancelled restore changes no gameplay, result or setting state beyond an independently triggered focus-loss pause. Serialize concurrent file operations and setting mutations; show progress, avoid double submissions and release temporary resources on all outcomes.

Export filenames are tetris-save.json and tetris-save.sqlite. Detect formats by validated content, not solely extension or MIME type: SQLite header "SQLite format 3" with its required terminator, otherwise strict UTF-8 JSON. Reject unknown binary files, unsupported text encoding and files over 2 MiB before decoding. No automatic network transfer, file watching or automatic reload is allowed.

## F-3: JSON version 1

The root object has exactly formatVersion, results and settings. formatVersion is integer 1. results is an array of zero to ten F-1 objects. settings is an object with exactly the six C-1 keys and canonical string values. All properties are required; reject additional properties at every level, nulls, type coercion, fractional or unsafe scores and duplicate object member names at any nesting level. Strict JSON syntax excludes comments, trailing commas and non-finite values. Decode UTF-8 with an optional single BOM.

Provide schemas/tetris-save.schema.json using JSON Schema draft 2020-12. The schema sets additionalProperties=false on root/result/settings, required fields, maxItems=10, integer bounds, const 1, a UUID v4 pattern, the canonical UTC timestamp pattern and date-time format, plus the six setting enums. A semantic pass enforces real-date validity, exact timestamp round trip and unique result IDs; a pattern alone is insufficient. Configure format validation explicitly rather than assuming an annotation rejects input. Duplicate JSON names require lexical parsing support before schema validation because JSON.parse alone discards them.

A minimal valid document is:

```json
{"formatVersion":1,"results":[],"settings":{"ghost":"show","hardDrop":"on","next":"on","hardDropLock":"general","lock":"interval","hold":"on"}}
```

## F-4: SQLite version 1

Use an ordinary SQLite 3 database, exported as a single complete file with no WAL/journal companion. Store version in PRAGMA user_version=1 and application identifier PRAGMA application_id=1413829714. The application identifier distinguishes this format from an unrelated database; both metadata values are required.

```sql
CREATE TABLE high_scores (
    id TEXT PRIMARY KEY NOT NULL,
    score INTEGER NOT NULL CHECK(score >= 0 AND score <= 9007199254740991),
    timestamp TEXT NOT NULL
);
CREATE TABLE settings (
    key TEXT PRIMARY KEY NOT NULL,
    value TEXT NOT NULL
);
```

settings contains exactly one row for each of the six C-1 keys, with TEXT values from its enum. high_scores contains zero to ten valid F-1 records. Inserts use bound parameters, never string interpolation. All rows and metadata are created in one transaction before exporting bytes.

Import opens the bytes in a separate in-memory database. Require integrity_check to return ok, exact user_version/application_id, the two named ordinary tables and exact column order/names/types/primary-key/nullability above. Require the score bound CHECK constraint semantically, accepting harmless SQLite whitespace/quoting differences. Reject extra user tables, views, triggers, virtual tables, duplicate key rows, missing/unknown settings, invalid SQLite storage classes and all F-1 semantic failures. SQLite internal bookkeeping tables do not count as extra user tables. Do not execute schema SQL from the file, run triggers, attach databases, load extensions or write the user's source file. Query fixed column names with trusted SQL and close the in-memory database on every path.

Do not silently upgrade a wrong or missing format version. An external SQLite tool must be able to inspect the exported metadata/tables and find exactly the same IDs, integer scores, timestamps and settings as JSON export.

## F-5: Validate before mutation

The import pipeline is byte-size/encoding detection, isolated decode, full structural/schema validation, semantic validation, canonical ranking, then candidate commit. No results, settings, URL parameters or cookies may change before the candidate has passed every stage. The controller commits only a complete candidate and replaces all six settings together.

Readable errors distinguish unsupported format/version, corrupt database/JSON, missing/extra data, invalid timestamp/result/setting and storage-write failure. A failed validation shows the error and preserves all observable pre-import results/settings/cookies/URL exactly. Never salvage only valid rows or apply settings from a partially invalid file. Rollback of failures during a validated commit follows the architecture's host-persistence contract; report any inability to restore external persistence rather than claiming an atomic success.

## F-6: Acceptance evidence

Round-trip both formats, empty and full leaderboards, zero and maximum scores, tied scores, stable IDs and timestamps, all six settings and cross-format semantic equality. Inspect real SQLite bytes with Python sqlite3 as an independent reader. Exercise corrupt bytes, wrong metadata, malformed schema, missing/duplicate/unknown settings, invalid dates, duplicate JSON member names/IDs, too many results and oversized input. For every rejection compare results, settings, cookies and URL before/after, not only an error message. Confirm a successful Restore updates persistence and export from the resulting state matches the accepted candidate.
