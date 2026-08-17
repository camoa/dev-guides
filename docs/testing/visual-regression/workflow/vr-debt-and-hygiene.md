---
description: Quarterly VR suite maintenance — pruning stale baselines, fixing flaky ones, and deciding when to move to an external service.
tldr: "Run quarterly hygiene: prune orphan PNGs, fix drifting baselines at the root cause (never bump threshold), cull whole-page shots covered by component shots, and walk the suite with the team to retire tests that haven't caught a regression in 6 months. Move to an external service when baseline directory exceeds 1 GB."
---

# VR Debt & Hygiene

## When to Use

> Use this guide for quarterly maintenance, or when the suite starts feeling slow or noisy.

## Decision

| Issue | Tactic |
|-------|--------|
| Stale baselines (PNGs whose tests no longer exist) | Run full-suite `--update-snapshots`; orphans surface in `git status` |
| Flaky baselines (small consistent drift on every run) | Find what's drifting (subpixel font hint? incomplete animation disable?) and fix; do not bump threshold |
| Bloated suites (>10 min locally, >500 PNGs) | Cull whole-page shots covered by component shots; drop viewports that haven't caught a regression in 6 months; drop cross-browser baselines that have never differed cross-browser |
| Snapshot bloat in git (>1 GB) | `git gc --aggressive`; mark `*.png` binary in `.gitattributes`; consider git LFS or external service |

Symptoms suggesting move to an external service (Argos, Lost Pixel, Chromatic):
- Baseline directory > 1 GB
- `git clone` takes minutes
- Reviewers rarely open the Playwright report; they just merge baseline PRs
- Multiple teams contribute baselines and conflicts are common

## Pattern

Quarterly walk-the-suite review with the team:
- For each test: has it caught a real regression in the past 6 months? If no, candidate for deletion
- For each baseline directory: are there orphans?
- For each threshold override: is the comment still true?

## Common Mistakes

- **Wrong**: no periodic review → **Right**: suite rots; team loses trust; nobody cares
- **Wrong**: pruning by deleting tests instead of fixing flakes → **Right**: loses coverage
- **Wrong**: treating bloat as inevitable → **Right**: it's a budget problem; impose a budget

## See Also

- [Baseline Management](vr-baseline-management.md)
- [Triaging False Positives](vr-triaging-false-positives.md)
- [Reference Program](vr-reference-program.md)
