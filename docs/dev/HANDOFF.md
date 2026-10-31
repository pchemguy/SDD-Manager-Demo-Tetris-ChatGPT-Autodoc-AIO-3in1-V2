# Development handoff

## Authority and current checkpoint

The user request Do QC and full implement authorizes all T-001 through T-047, tracking, phase integration, packages and releases. Preparation is integrated and its milestone closed. Working branch phase/3-special-landing-rules was created from main 87f6a765bd3c8f79b9126be01410dce21cb9d1f1 and integrates into main. Phase 3 delivery milestone is closed/read back; its phase review passes 70 pytest cases, compiler/build-driver and archive checks with code review/audit evidence in [phase report](reports/phases/3/PHASE-REPORT.md).

## Pending effects and next action

Publish/read back T-015, close its issue and review milestone, then explicitly merge/verify/publish to main. Rebuild from the exact default-branch release commit, tag, publish and verify hosted bytes/latest before activating the next phase. Full remaining implementation authority continues; no extra approval is required. This checkpoint cannot prove its future effects. TASKS and reports own actual task/evidence state.

## Environment limits

Linux execution with Node 24, Python 3.12, pytest and dedicated Playwright Chromium headless/Firefox builds. Firefox content sandbox recovery is process-local for trusted local pages. Native Windows and actual-sidebar checks remain separately reported; no unavailable mode is claimed verified.

## Integration checkpoint

Phase 3 source a88f18abd32c3c2698654c4c625b735f01737ffa is merged into its recorded parent main 87f6a765bd3c8f79b9126be01410dce21cb9d1f1; all phase issues/milestones are closed/read back. Merged checks and publication precede the release marker/tag. Full remaining scope remains authorized.
