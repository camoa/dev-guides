---
description: Where baselines live, how they enter version control, and how to keep them clean.
tldr: Commit baselines to the repo (Playwright default) for Drupal/DDEV teams without a VR-vendor budget. Keep baselines on main, update them in PRs with the UI change, and never auto-update on main from CI. Prune orphans quarterly.
---

# Baseline Management

## When to Use

> Use this guide when deciding where baselines live, how they enter version control, and how to keep them clean.

## Decision

| Pattern | Pros | Cons |
|---------|------|------|
| **Committed to repo** (Playwright default — `*-snapshots/` next to test files) | PR diffs show baseline changes; reviewers see exactly what changed; reproducible from any clone | Repo size grows; binary diffs in git are noisy |
| **External baseline service** (Argos, Lost Pixel, Chromatic, Percy) | No repo bloat; central governance UI; web-based approval | Vendor lock-in; offline review impossible; budget |

For Drupal/DDEV teams without a VR-vendor budget, **committed baselines are the default**.

## Pattern

Branch strategy:
- `main` holds the canonical baselines
- A PR that intentionally changes UI updates baselines as part of the PR
- The reviewer's job is to confirm the new baselines match design intent
- **Never** auto-update baselines on `main` from CI

Storage cost math:
```
total bytes ≈ baseline_count × avg_pixel_count × 4 bytes (RGBA) × git_history_factor
```

A 50-test suite at 1200×800 with 3 viewports and ~10 revisions/year is ~600 MB of git history per year.

Mitigations:
- `.gitattributes`: mark `*.png` as binary
- `git lfs` once total exceeds ~1 GB
- Move to an external service if PR diff loading becomes painful

Pruning stale baselines quarterly: run `npx playwright test --update-snapshots` against the full suite; orphaned PNGs aren't touched, then `git status` reveals them for manual deletion.

## Common Mistakes

- **Wrong**: auto-update baselines on `main` → **Right**: accepts regressions silently
- **Wrong**: committing `.auth/admin.json` → **Right**: contains session cookies; gitignore it
- **Wrong**: keeping baselines for tests that no longer exist → **Right**: orphans accumulate; quarterly prune

## See Also

- [Baseline Update Workflow](vr-baseline-update-workflow.md)
- [VR Debt & Hygiene](vr-debt-and-hygiene.md)
- [Drupal & DDEV Procedure](vr-drupal-ddev-procedure.md)
