---
description: Configuring threshold, maxDiffPixels, and maxDiffPixelRatio to balance flakiness against missed regressions.
tldr: Use threshold 0.20 (Playwright default) for standard tests; tighten to 0.05–0.10 for pixel-perfect same-env captures; use maxDiffPixels for small components and maxDiffPixelRatio for full-page shots. Set a global floor in playwright.config.ts and override per assertion only with a comment.
---

# Threshold Tuning

## When to Use

> Use this guide when configuring how forgiving the diff is — too tight = flake; too loose = miss regressions.

## Decision

| Scenario | Recommended `threshold` |
|----------|------------------------|
| Pixel-perfect, same OS, same browser | 0.05–0.10 |
| Default Playwright tests | 0.20 (the default) |
| Cross-OS comparisons (mac vs Linux CI) | 0.20–0.30 |
| Components with complex shadows / blur / video posters | 0.30 (combine with `maxDiffPixels`) |
| Different font hinting across OSes | Above 0.40 — switch tools or fix the env (pin Docker image) |

| Use | When |
|-----|------|
| `maxDiffPixels` | Small components — a button is 200×40 = 8000 px; `maxDiffPixels: 50` allows ~0.6% drift |
| `maxDiffPixelRatio` | Full-page screenshots — `maxDiffPixelRatio: 0.001` allows 0.1% of any size |

## Pattern

Three knobs, three jobs:

| Option | Default | Job |
|--------|---------|-----|
| `threshold` (0–1) | 0.2 (Playwright) | Per-pixel YIQ color tolerance |
| `maxDiffPixels` | unset | Absolute count of differing pixels allowed |
| `maxDiffPixelRatio` (0–1) | unset | Fraction of total pixels allowed to differ |

Note: pixelmatch's library default is **0.1**. Playwright passes through but defaults to **0.2**.

Global floor + per-test exceptions:

```ts
// playwright.config.ts — the floor
expect: {
  toHaveScreenshot: {
    threshold: 0.15,
    maxDiffPixelRatio: 0.005,
    animations: 'disabled',
    caret: 'hide',
  },
}
```

Override per assertion only with a comment:

```ts
// Brand logo must match token RGB exactly — tighter threshold required.
await expect(logo).toHaveScreenshot({ threshold: 0.02 });
```

## Common Mistakes

- **Wrong**: bumping `threshold` to silence a flake → **Right**: bandaid; investigate the root cause (env/font/animation) instead
- **Wrong**: setting `threshold: 0.5+` → **Right**: effectively not testing
- **Wrong**: per-test thresholds without a "why" comment → **Right**: six months later nobody knows why

## See Also

- [Stability Checklist](vr-stability-checklist.md)
- [Triaging False Positives](vr-triaging-false-positives.md)
