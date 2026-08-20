---
description: "Common Playwright VR anti-patterns — environment mismatch, threshold abuse, flake tolerance, and Drupal-specific pitfalls."
tldr: "The two most damaging mistakes are capturing baselines on macOS and comparing in Linux CI, and committing baselines from a flaky state. Pin a Docker image, add stability controls first, then capture."
---

# Anti-Patterns

## When to Use

> Use this when debugging persistent VR failures or reviewing a suite for reliability issues.

## Wrong vs Right

| Wrong | Right |
|---|---|
| Capturing on macOS, comparing in Linux CI | Same Docker image both places; pin the tag |
| `omitBackground: true` mixed with default white captures | Pick one; default is white |
| Relying on `loading="lazy"` images settling on their own | Force-load + wait for networkidle |
| `prefers-color-scheme` left to OS preference | Pin `colorScheme: 'light'` in `use` |
| Dismissing cookie banners via UI click in every test | Pre-set consent cookie or `localStorage` via `addInitScript` |
| Focused inputs producing OS-specific carets | `caret: 'hide'` (default) or blur first |
| `threshold: 0` chasing pixel-perfect | Trust default `0.2`; tighten only with a documented reason |
| First-run baselines created from a flaky state | Add stability controls first, then capture; never recapture without investigating flake |
| Re-running until green then committing | Same diagnosis, same fix; flake masks regressions |
| `fullPage: true` on every test | `clip` or element shots for components, full-page for whole templates — the objection is false positives from editorial content, not PNG size (~150 KB per masked baseline) |

## Drupal-Specific Pitfalls

| Issue | Fix |
|---|---|
| Big Pipe placeholders not yet swapped in | Wait for `networkidle` after `goto` |
| Contextual links / quickedit overlays | Mask `[data-contextual-id]` and `.contextual-region` |
| Admin toolbar timestamps | Mask the toolbar's "recent" tray |
| CKEditor 5 iframe content | `mask` doesn't pierce iframes; use `stylePath` to set `iframe { visibility: hidden; }` |

## See Also

- [Stability Controls](pw-vr-stability-controls.md)
- [Determinism](pw-vr-determinism.md)
- [Drupal & DDEV](pw-vr-drupal-ddev.md)
- Reference: [Playwright Visual Comparisons](https://playwright.dev/docs/test-snapshots)
