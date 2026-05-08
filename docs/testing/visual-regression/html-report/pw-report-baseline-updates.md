---
description: How to update VR baselines after triaging failures in the Playwright HTML report.
tldr: The HTML report has no approve/accept button — baseline updates are CLI-only with --update-snapshots. Always scope updates with --grep to avoid silently accepting regressions. Commit baselines after updating or CI will still fail.
---

# Baseline Updates

## When to Use

> Use this after triaging a diff in the report and deciding "this change is intentional — accept the new baseline."

## Decision

| Situation | Command |
|---|---|
| Update all snapshots | `npx playwright test --update-snapshots` |
| Update only matching tests (recommended) | `npx playwright test --update-snapshots --grep "test title"` |
| Single spec file | `npx playwright test tests/header.spec.ts -u` |

## Pattern

Full triage → update → confirm workflow:

```
1. Open report          → npx playwright show-report
2. Triage failed tests  → confirm intentional
3. Update baselines     → npx playwright test -u --grep "<test title>"
4. Re-run               → npx playwright test --grep "<test title>"
5. Confirm green        → all baselines match
6. Commit baselines     → git add tests/**/*-snapshots/
```

## Why There Is No Approve Button

The Playwright maintainers intentionally decline to add this: an "approve" click that auto-runs `--update-snapshots` removes the friction that makes baseline updates an explicit engineering action. Auto-accept is how regressions ship.

Community workflows fill this gap with PR-comment bots (`/approve-snapshots`) that re-run `--update-snapshots` in CI and commit back to the PR branch — but this is outside the core report.

## Common Mistakes

- **Wrong**: looking for the approve button → **Right**: it doesn't exist; CLI is the only path
- **Wrong**: bulk `--update-snapshots` across the whole suite as a default response → **Right**: use `--grep` to scope; bulk accept silently accepts regressions
- **Wrong**: not committing baselines after updating → **Right**: local run is green but CI fails because baselines are still old

## See Also

- [VR Diff Panel](pw-report-vr-diff-panel.md)
- [Baseline Management](../workflow/vr-baseline-management.md)
- [Baseline Update Workflow](../workflow/vr-baseline-update-workflow.md)
