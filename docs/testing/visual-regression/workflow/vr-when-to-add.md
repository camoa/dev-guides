---
description: Deciding whether a component, page, or state warrants a visual regression test.
tldr: Add a VR test when you can identify the smallest screenshot that would catch a regression in this change. High-signal, stable surfaces (SDC atoms, hero, forms, critical landing pages) get VR; volatile surfaces (live feeds, external-API pages, dashboards) do not.
---

# When to Add a VR Test

## When to Use

> Use this guide when deciding whether a particular change, component, or page warrants VR coverage. The anchor question: *what's the smallest set of screenshots that would catch a visual regression in this change?*

## Decision

| Subject | VR? | Rationale |
|---------|-----|-----------|
| New SDC / paragraph / block plugin | Yes | Cheap to baseline, high-signal, stable |
| New view mode (teaser, card variant) | Yes | Confined surface, predictable content |
| Hero, navbar, footer, mega-menu | Yes | High visual prominence, design-token-driven |
| Custom form widget Twig | Yes | CSS-heavy, easily destabilized |
| Home page | Yes (selectively) | Critical landing — mask editorial regions aggressively |
| Login / registration screens | Yes | Stable, brand-critical |
| 1–4 critical landing pages | Yes | High visibility, low maintenance if masked |
| Each content type's primary node render | Yes | One per type; pick a stable example node |
| Layout Builder default layouts | Yes | Test the *defaults*, not per-page overrides |
| Search results / news feeds | No (without robust masking) | Volatility eats the test |
| Dashboards with live metrics | No | Same |
| External-API-driven pages | No | Test environment can't pin the response |
| Feature-flagged content | No | Flag flips ≠ regressions |
| Email rendering | No | Use email-specific tools |
| Admin pages with timestamps + counters | Maybe | Only if you mask aggressively |

## Pattern

The anchor heuristic: **what's the smallest set of screenshots that would catch a visual regression in this change?**

If the answer is "one screenshot of one component at one viewport," that *is* the test. Nothing more.

## Common Mistakes

- **Wrong**: capturing every component "just in case" → **Right**: bloats the suite; signal-to-noise drops; team stops trusting the suite
- **Wrong**: adding VR to a page nobody can stabilize → **Right**: the test becomes a flake factory
- **Wrong**: skipping VR on "small" components → **Right**: utility classes get applied 100s of times; small components get the most regressions

## See Also

- [What VR Is For](vr-what-its-for.md)
- [What to Capture](vr-what-to-capture.md)
- [Stability Checklist](vr-stability-checklist.md)
