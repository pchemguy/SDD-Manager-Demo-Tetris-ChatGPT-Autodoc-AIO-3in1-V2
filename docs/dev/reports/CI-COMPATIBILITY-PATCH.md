# CI compatibility patch 0.10.1

## Problem and change

The GitHub ubuntu-latest migration selected Ubuntu 26.04, which pinned Playwright 1.55.0 rejects during browser provisioning. The application build/tests never ran in that failing workflow. Pinning ubuntu-24.04 restores the supported toolchain while preserving all runtime dependencies and gameplay/file contracts. The maintenance version and generated manifest versions advance to 0.10.1; all ten phases and four deliverables remain available. The immutable v0.10.0 release/tag is retained.

## Verification


## Hosted verification confirmed

[Actions run 41203876000](https://github.com/pchemguy/SDD-Manager-Demo-Tetris-ChatGPT-Autodoc-AIO-3in1-V2/actions/runs/41203876000) completed successfully at 5e8c56113c51fbb6dd2a13cad0ade5a4af7cc379 on Ubuntu 24.04. The hosted full suite reports 347 passed and 3 explicitly native-only skips; Firefox browser/panel checks report 48 passed. Production builds and all four actual archive/runtime/manifest/checksum gates pass. The local compatible-host Electron probe supplies the native desktop-resource check omitted by CI. Version 0.10.1 compiler/build and 17 version/manifest/package checks pass. Final publication additionally requires a successful workflow for its exact release marker, a clean-source four-archive rebuild, actual extracted browser/panel/native-compatible-host checks, annotated tag and hosted byte/latest readback. Native Windows/sidebar limits remain unchanged.

## Findings and blockers

None. Release operations listed above are subsequent effects at this report's source checkpoint.

## TODO

None. Environment-limited native Windows/sidebar checks and compatible-host follow-up are retained in IMPLEMENTATION-REPORT.md.
