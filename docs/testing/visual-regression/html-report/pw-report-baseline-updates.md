---
description: "How to update VR baselines after triaging failures in the Playwright HTML report."
tldr: "The HTML report has no approve/accept button — baseline updates are CLI-only with --update-snapshots. Always scope updates with --grep to avoid silently accepting regressions. Commit baselines after updating or CI will still fail."
---

# Baseline Updates

## When to Use

> After a triage decision — "this is intentional, accept the new baseline."

## The Hard Limitation

> **The HTML report has no "approve" / "accept new baseline" button.**

It is a read-only artifact viewer. Updating snapshots is exclusively a CLI operation.

## Pattern: Update from CLI

```bash
# Update all snapshots
npx playwright test --update-snapshots

# Update only matching tests (recommended)
npx playwright test --update-snapshots --grep "checkout flow"

# Single file
npx playwright test tests/header.spec.ts -u
```

## Pattern: Triage → Update → Re-run

```
1. Open report          → npx playwright show-report
2. Triage failed tests  → confirm intentional
3. Update baselines     → npx playwright test -u --grep "<test title>"
4. Re-run               → npx playwright test --grep "<test title>"
5. Confirm green        → all baselines match
6. Commit baselines     → git add tests/**/*-snapshots/
```

## Why No Approve Button?

The Playwright maintainers decline to add this on purpose: an "approve" click that auto-runs `--update-snapshots` removes the friction that makes baseline updates an explicit engineering action. Auto-accept is how regressions ship.

Community workflows fill this gap with PR-comment bots (`/approve-snapshots`) that re-run `--update-snapshots` in CI and commit back to the PR branch — but this is out of scope for the core report.

## Common Mistakes

- **Looking for the approve button forever** — it's not there; CLI is the answer
- **Bulk `--update-snapshots`** of the whole suite as the default response — accepts regressions silently
- **Forgetting to commit baselines** — re-running locally green; CI fails because baselines are still old

## See Also

- [VR Diff Panel](pw-report-vr-diff-panel.md)
- [Baseline Management](../workflow/vr-baseline-management.md)
- [Baseline Update Workflow](../workflow/vr-baseline-update-workflow.md)
