---
description: Test accessibility with automated tools, keyboard-only navigation, DevTools accessibility tree inspection, and canonical screen-reader pairings.
tldr: Automated tools (axe-core, Lighthouse) catch only ~30-40% of issues — supplement with keyboard-only testing and screen-reader verification using JAWS+Chrome, NVDA+Firefox, VoiceOver+Safari; 100% Lighthouse score does not guarantee usability.
---

# Accessibility Testing

## When to Use

> Automated tools catch rule violations but cannot judge usability — supplement with keyboard-only testing and screen-reader verification using the canonical browser pairings.

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Automated scan | Violations found | Fix before continuing — automated issues are guaranteed bugs |
| Automated scan | No violations | Continue — a 100% score does not guarantee usability |
| Screen-reader test | Behavior differs by AT | Prioritize the most common pairings; note deviations |
| Screen-reader test | Custom element missing name/role | Inspect ElementInternals in DevTools accessibility tree |
| Zoom test | Content clips or scrolls horizontally | Fix container sizing; use `max-width` not fixed `width` in `px` |

## Steps

**1. Run automated scan:**

```bash
npx @axe-core/cli https://localhost:3000
```

Also available as a browser extension or integrated in Playwright/Cypress.

**2. Keyboard-only test** — Disconnect the mouse. Using only Tab, Shift+Tab, arrow keys, Enter, Space, and Escape:
- Confirm every interactive element is reachable
- Confirm focus indicator is always visible
- Confirm no focus traps (except inside open modals)
- Confirm modals close on Escape and return focus to the trigger
- Confirm skip links work and move focus to the target

**3. Accessibility-tree inspection** — DevTools → Accessibility panel. Verify:
- Roles are correct (especially for custom elements using ElementInternals)
- Names are present and meaningful on interactive elements
- States (`expanded`, `checked`, `selected`) update when changed

**4. Screen-reader test** — Use the canonical browser pairings:

| Screen reader | Browser | Platform |
|---|---|---|
| JAWS | Chrome | Windows |
| NVDA | Firefox | Windows |
| Narrator | Edge | Windows |
| VoiceOver | Safari | macOS / iOS |
| TalkBack | Chrome | Android |

Test: page load announces title and language; landmarks are navigable; headings list is correct; forms announce labels, hints, and errors; dialogs trap focus and announce title; live regions announce updates.

**5. Zoom and text-resize test** — Set browser zoom to 200%. Confirm no content is lost, no horizontal scroll is required in main content, and no text is clipped.

**6. User testing** — Include users with disabilities, especially for novel interaction patterns.

## Common Mistakes

- **Wrong**: Shipping at 100% Lighthouse score without keyboard test → **Right**: Automated tools cover ~30–40% of accessibility issues
- **Wrong**: Testing only with one screen reader → **Right**: JAWS+Chrome and NVDA+Firefox can have meaningfully different behavior; both should pass
- **Wrong**: Using outdated screen-reader / browser combinations → **Right**: AT behavior changes with updates; use current stable versions
- **Wrong**: Treating accessibility as a final QA step → **Right**: Bake in semantic HTML from the start; test as you build

## See Also

- Reference: https://github.com/dequelabs/axe-core
- Reference: https://www.nvaccess.org/
- Reference: https://www.w3.org/WAI/test-evaluate/
