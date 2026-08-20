---
description: "Configuring threshold, maxDiffPixels, and maxDiffPixelRatio to balance flakiness against missed regressions."
tldr: "Use threshold 0.20 (Playwright default), tighter for pixel-perfect captures. Use maxDiffPixels for small components and full-page shots alike — never maxDiffPixelRatio on full-page. Start at zero and measure your own floor."
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
| `maxDiffPixels` | Small components (a button is 200×40 = 8000 px; `maxDiffPixels: 50` allows ~0.6% drift) **and full-page shots** — an absolute count means the same thing at every page height |
| `maxDiffPixelRatio` | Fixed-size captures only, where you want the budget to scale with the element |

**Never use a ratio for full-page shots.** The ratio is a fraction of image *area*, and a full-page image is as tall as the document, so the budget grows with page height and is loosest exactly where pages are tallest. 0.5% of 1440×900 is about 6,500 px — a sane gate. The same 0.5% of 1440×8000 is about 57,600 px, enough to hide a whole component. `maxDiffPixels` does not drift with page length. Mixing both is fine — Playwright takes the **smaller** of the two budgets, so the tighter constraint wins.

## Pattern

Three knobs, three jobs:

| Option | Default | Job |
|--------|---------|-----|
| `threshold` (0–1) | 0.2 (Playwright) | Per-pixel YIQ color tolerance |
| `maxDiffPixels` | unset — **means 0** | Absolute count of differing pixels allowed |
| `maxDiffPixelRatio` (0–1) | unset — **means 0** | Fraction of total pixels allowed to differ |

Note: pixelmatch's library default for `threshold` is **0.1**. Playwright passes through to pixelmatch but defaults to **0.2**. `unset` is not a fallback default — Playwright resolves the budget as `maxDiffPixels ?? (imageArea × maxDiffPixelRatio) ?? 0`, so a config with neither key already runs a zero-pixel budget.

**Start at zero, then measure your own floor.** On a stabilized Drupal capture (frozen CSS, a lazy-content settle, `document.fonts.ready`, a double `requestAnimationFrame`), five runs against an unchanged site with every tolerance key removed produced 75 of 75 byte-identical captures — with the capture properly stabilized there was no nondeterminism left for a tolerance to absorb, and since unset means zero, no configuration was needed to get there. So the order is: stabilize the capture first, then run the suite several times against an unchanged site and set the budget from the residual you actually observe — which may well be nothing. A project that needs a large tolerance has an unstabilized capture, and the tolerance is hiding it rather than fixing it.

Global floor + per-test exceptions:

```ts
// playwright.config.ts — the floor
expect: {
  toHaveScreenshot: {
    threshold: 0.15,
    animations: 'disabled',
    caret: 'hide',
    // No maxDiffPixels / maxDiffPixelRatio: unset means a zero-pixel budget.
    // Add an absolute maxDiffPixels only once repeat runs on an unchanged
    // site show a residual, and set it from that number.
  },
}
```

Override per assertion only with a comment explaining why:

```ts
// Brand logo must match token RGB exactly — tighter threshold required.
await expect(logo).toHaveScreenshot({ threshold: 0.02 });
```

## Common Mistakes

- **Wrong**: bumping `threshold` to silence a flake → **Right**: bandaid; investigate the root cause (env/font/animation) instead
- **Wrong**: setting `threshold: 0.5+` → **Right**: effectively not testing
- **Wrong**: `maxDiffPixelRatio` on a full-page shot → **Right**: the budget is a fraction of image area, so it grows with page height and is loosest on the tallest pages; use an absolute `maxDiffPixels` instead
- **Wrong**: reaching for a tolerance before the capture is stable → **Right**: unset already means zero, and a stabilized capture can hold it; a large tolerance is hiding an unstabilized capture
- **Wrong**: per-test thresholds without a "why" comment → **Right**: six months later nobody knows why and the comment is the only justification for keeping the test

## See Also

- [Stability Checklist](vr-stability-checklist.md)
- [Triaging False Positives](vr-triaging-false-positives.md)
