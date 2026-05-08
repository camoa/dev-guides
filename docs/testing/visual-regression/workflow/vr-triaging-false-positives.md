---
description: Decision tree for triaging a VR diff — flakiness vs environment drift vs real regression.
tldr: When a diff fires, work the triage tree: same image on re-run (flake → stability checklist), differs by machine (env drift → pin Docker image), differs per browser (browser-specific rendering → per-browser baselines), differs CI vs local (always capture inside Docker). Skip only with a linked issue; never skip to ship a suspected regression.
---

# Triaging False Positives

## When to Use

> Use this guide when a diff fires. Before assuming it's intentional, work through the triage tree.

## Decision

| Question | Finding | Resolution |
|----------|---------|------------|
| Same diff on re-run? | No — diff varies run-to-run | Flakiness. Go to [Stability Checklist](vr-stability-checklist.md). Most likely: animations, fonts, or network idle |
| Different on different machines? | Yes | Environment drift. Pin the Playwright Docker image version exactly (no `:latest`); use the same image locally and in CI |
| Different per browser? | Yes | Browser-specific rendering. Accept per-browser baselines (Playwright keys by project name) or mask the affected region |
| Different in CI vs local? | Yes | Almost always fonts, DPI, or GPU rendering. Only capture and compare inside the Playwright Docker image — never on the host |

### When to `.skip` vs fix immediately

`.skip` is acceptable when:
- The diff is a known flake under active investigation (link the issue in the skip comment)
- A vendor library upgrade introduced rendering differences you'll address in a follow-up PR

`.skip` is **not** acceptable as a way to ship a PR you suspect contains a real regression. If skips accumulate beyond ~5% of the suite, the suite is dead.

## Pattern

```bash
# Q1: Re-run the failing test twice
npx playwright test --grep "<failing test>"
npx playwright test --grep "<failing test>"
# If diff differs run-to-run → flakiness (not a regression)
```

## Common Mistakes

- **Wrong**: re-running until it passes → **Right**: produces a "stable enough" baseline that masks real diffs
- **Wrong**: bumping `threshold` instead of fixing the env → **Right**: silent erosion of test value
- **Wrong**: `.skip`-ing flakes indefinitely → **Right**: flake debt accumulates; team stops trusting the suite

## See Also

- [Stability Checklist](vr-stability-checklist.md)
- [Threshold Tuning](vr-threshold-tuning.md)
- [VR Debt & Hygiene](vr-debt-and-hygiene.md)
