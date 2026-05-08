---
description: What visual regression testing is for — and what it explicitly is not (design QA, a11y, performance).
tldr: Use VR when you need to catch unintended visual drift from a code change. VR is baseline governance — every diff is either an intentional baseline update or an unintended regression. Never use it as a substitute for design QA or accessibility testing.
---

# What VR Is For

## When to Use

> Use VR when you need to catch *unintended* visual drift introduced by a code change — a typography token edit that bled into 40 components, a Bootstrap upgrade that shifted card padding, a CSS specificity collision from a new module. Use design QA tools when you need to validate against design intent.

## Decision

| Concern | Tool | What VR adds |
|---------|------|--------------|
| Does the button submit the form? | Functional/E2E (Playwright `expect`) | VR adds *visual* verification on top — same runner, different assertion |
| Does the page meet WCAG? | Accessibility (`@axe-core/playwright`) | VR is silent on a11y; a page can be visually identical and still inaccessible |
| Is it fast? | Performance (Lighthouse, Web Vitals) | VR captures *after* stability; nothing to say about how long stability took |
| Does it match the Figma comp? | Visual approval / design QA | VR catches diffs against your *previous self*; visual approval catches diffs against *design intent*. Do not conflate |

## Pattern

VR is **baseline governance**, not screenshot diffing. The reference image is committed; the workflow is structured around when, why, and by whom that reference is changed. Every diff is either an intentional baseline update (with a code change explaining why) or an unintentional regression. There is no third category.

## Common Mistakes

- **Wrong**: treating VR as design QA → **Right**: VR can't tell you the design is wrong; it tells you it's the same as last time
- **Wrong**: mixing functional and visual assertions in the same test → **Right**: `expect(page).toHaveText(...)` failing masks `expect(page).toHaveScreenshot()` failing; keep them in separate tests
- **Wrong**: auto-accepting baseline updates in CI → **Right**: baseline updates must be a deliberate engineering action

## See Also

- [When to Add a VR Test](vr-when-to-add.md)
- [Baseline Update Workflow](vr-baseline-update-workflow.md)
- [Anti-Patterns](vr-anti-patterns.md)
