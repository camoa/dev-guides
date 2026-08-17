---
description: Consolidated list of VR anti-patterns — wrong approach paired with the correct alternative.
tldr: "The most destructive VR anti-patterns are: bulk --update-snapshots as the default response to failures, capturing on host and comparing in CI, bumping threshold to silence flakes, and committing .auth/ session files. Each silently destroys test value."
---

# Anti-Patterns

## When to Use

> Reference this when reviewing VR tests, diagnosing suite problems, or onboarding developers to the VR program.

## Common Mistakes

- **Wrong**: capturing on every keystroke/hover/state change → **Right**: capture distinct visual states only
- **Wrong**: updating baselines as the default response to a failure → **Right**: treat every diff as a real regression until proven otherwise
- **Wrong**: VR tests without disabling animations → **Right**: `animations: 'disabled'` (Playwright default; never override to `'allow'`)
- **Wrong**: single-viewport baselines for responsive components → **Right**: capture all relevant breakpoints, or document explicitly why one is enough
- **Wrong**: treating "small diff" as "good enough" → **Right**: investigate small diffs; 0.3% drift × 80 components = a UI that looks subtly wrong everywhere
- **Wrong**: running VR only in CI → **Right**: run locally pre-push (Husky pre-push hook on the affected suite, not the whole thing)
- **Wrong**: committing `playwright/.auth/admin.json` → **Right**: `.gitignore` it; storage state contains session cookies
- **Wrong**: mixing functional and visual assertions in the same test → **Right**: separate tests per assertion type
- **Wrong**: `mcr.microsoft.com/playwright:latest` → **Right**: pin a specific tag; upgrade deliberately
- **Wrong**: capturing host-side, comparing CI-side → **Right**: same Docker image both places, no exceptions
- **Wrong**: bumping `threshold` to silence flakes → **Right**: fix the underlying instability (env, fonts, animations)
- **Wrong**: a baseline-only commit (`update baselines`) → **Right**: every baseline change paired with a source change explaining why

## See Also

- [What VR Is For](vr-what-its-for.md)
- [Stability Checklist](vr-stability-checklist.md)
- [Threshold Tuning](vr-threshold-tuning.md)
- [Baseline Update Workflow](vr-baseline-update-workflow.md)
- [Triaging False Positives](vr-triaging-false-positives.md)
