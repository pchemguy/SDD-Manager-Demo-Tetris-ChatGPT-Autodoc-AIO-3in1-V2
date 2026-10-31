# Development handoff

## Workflow and authority

Full T-001 through T-047 implementation and all phase releases are authorized by the user request Do QC and full implement. Preparation passed DOCS-009 and was explicitly integrated/published into main 91856d370cdde025db6fcad06997922909295568; preparation milestone 1 is closed/read back.

## Current checkpoint

Working branch phase/1-classic-browser, creation parent/integration target main, branch-off 91856d370cdde025db6fcad06997922909295568. Classic browser delivery milestone 1.1 is verified; [report](reports/phases/1/1.1.md) records code review, tests and package limits. TASKS owns task checkboxes and verification evidence.

Publish/read back T-004 and close its issue, then close/read back milestone 1.1 before T-005 phase review. Phase integration/release 0.1.0 are pending at this snapshot. Continue all remaining phases after each verified integration/release, with no additional human checkpoint. No next phase may bypass required tracking or predecessor release gates.

## Environment

Node 24.22.1, Python 3.12, pytest 8.4.2 and Playwright 1.55.0. Dedicated managed Chromium headless shell 140.0.7339.16 and Firefox 141.0 passed repeated context/interaction/Canvas probes. Firefox default content process fails uid_map EPERM; process-local MOZ_DISABLE_CONTENT_SANDBOX=1 works for trusted local pages. Browser dependencies/state remain outside tracked source. Native Windows and actual sidebar checks have not run.

## Phase 1 review checkpoint

T-001 through T-004 are verified/published and milestone 1.1 is closed/read back. T-005 phase review passes code inspection, 23 current pytest cases, compiler and archive checks, plus prior Firefox/extracted-build evidence. [Phase report](reports/phases/1/PHASE-REPORT.md) records limits. Publish this review, close its issue and milestone 1.2, then explicitly merge/verify/publish to main and release 0.1.0 with final-source package/readback. Continue Phase 2 only after that release is verified. Full implementation authority remains active.

## Phase 1 integration

Verified phase/1-classic-browser ba78dede0aac343f906f7419ac7aa53d68a8a7dc is merged into its creation parent main. All Phase 1 issues and both milestones are closed/read back. Publish this merged state, then prepare the default-branch release marker and final-source browser package for 0.1.0. Hosted release/download verification remains pending. Full implementation continues to Phase 2 after release completion.
