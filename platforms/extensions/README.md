# Sidebar delivery

Chromium uses Manifest V3 `side_panel` and a service worker, with minimum version 116 (`sidePanel.open`). Firefox uses Manifest V3 `sidebar_action` and background scripts, with minimum version 115 (`storage.session`). The toolbar action calls the family-specific opening API directly within its user gesture. No content scripts, site permissions, backend or remote runtime assets are used.

The explicit family adapter uses Chrome's callback API with `runtime.lastError` and Firefox's Promise API. It does not infer Firefox from the existence of `browser`, which is also available in recent Chromium versions. Backgrounds are classic IIFEs, and both panels reuse the game, view and local codecs. The narrow layout is defined by the shared stylesheet's sidebar rules.

Only `storage` and, in Chromium, `sidePanel` are requested. Extension CSP permits local scripts and WebAssembly compilation for SQLite, without `unsafe-eval`. All icons are original code-generated block graphics.

Primary API contracts:

- https://developer.chrome.com/docs/extensions/reference/api/sidePanel
- https://developer.chrome.com/docs/extensions/reference/api/storage
- https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/API/storage/session
- https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions/manifest.json/sidebar_action

Native sidebar launch and panel-document tests are separate verification categories; HTTP or mocked API checks alone do not establish native sidebar behavior.
