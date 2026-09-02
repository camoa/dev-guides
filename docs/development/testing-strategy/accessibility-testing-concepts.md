---
description: "Accessibility testing — what automated tools catch (≈35% of WCAG issues) and what requires manual keyboard and screen reader testing."
tldr: "Automated a11y tools (axe-core, Lighthouse) catch ~35% of detectable WCAG issues — missing alt text, contrast failures, duplicate IDs. The rest requires manual keyboard navigation and screen reader testing. Add axe-playwright to E2E tests and jest-axe to component tests; failing violations must block merges."
---

# Accessibility Testing Concepts

## When to Use

> Whenever you build or modify UI — accessibility testing is not optional for public-facing applications. Automated a11y tools catch a known, auditable subset of WCAG violations with minimal effort; manual testing with keyboard and screen reader is required to catch the rest. This section explains what automation can and cannot do, so you invest in the right combination.

## What Automated Accessibility Testing Catches

Automated tools (axe-core, Lighthouse, Pa11y, WAVE) check for **mechanically verifiable** WCAG criteria:

| Automated catches | Example |
|---|---|
| Missing `alt` on images | `<img src="logo.png">` |
| Form inputs without labels | `<input type="text">` with no `<label>` |
| Insufficient color contrast ratio | Text #777 on #fff fails WCAG AA (4.5:1) |
| Missing ARIA roles or landmarks | No `<main>`, no `role="navigation"` |
| Empty button or link text | `<button><svg>...</svg></button>` with no aria-label |
| Duplicate IDs | Two elements with `id="submit"` |

Studies consistently find that automated tools catch approximately **30–40% of WCAG issues** that are detectable at all. The rest require human judgment.

## What Automation Cannot Catch

| Not automatable | Why |
|---|---|
| Focus order makes sense | Requires a human to tab through and verify flow |
| Screen reader announces content correctly | Requires a screen reader and judgment |
| Interaction is operable by keyboard | Requires actually tabbing and pressing keys |
| Error messages are useful | Requires reading and understanding context |
| Animations are not distracting | Requires vestibular sensitivity awareness |
| Complex ARIA widget behavior | Requires testing with assistive technology |

**Do not confuse "automated tests pass" with "this is accessible."** Automated tests are a necessary first gate, not a sufficient one.

## Integrating Automated A11y into Tests

```javascript
// Using axe-core with Playwright (best coverage for component tests)
import { checkA11y } from 'axe-playwright';

test('registration form has no critical accessibility violations', async ({ page }) => {
  await page.goto('/register');
  // Run axe against the page; fails if any violations at 'critical' or 'serious' level
  await checkA11y(page, undefined, {
    runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] },
    axeOptions: { reporter: 'v2' },
  });
});
```

Run automated a11y checks:
- In component/unit tests using `jest-axe` (React component level)
- In E2E/functional tests using `axe-playwright` (page level)
- As part of CI — failing a11y violations should block merges for new violations

## Manual Testing Checklist

Run manually on new features and major UI changes:
- Tab through all interactive elements in logical order
- All interactive elements are reachable and operable by keyboard alone
- Screen reader (NVDA/Windows, VoiceOver/Mac, TalkBack/Android) announces content correctly
- Color contrast passes WCAG AA (4.5:1 for normal text, 3:1 for large text/UI)
- No content relies solely on color to convey meaning
- Animations respect `prefers-reduced-motion`

## Common Mistakes

- Treating automated a11y pass as "accessible" → Passes only ~35% of detectable issues; manual testing is required
- Only running a11y tools at the end of development → Find violations early when they are cheap to fix; add axe to component-level tests
- Ignoring "moderate" or "minor" violations → These accumulate and block users with disabilities; triage and address them
- Not testing with an actual screen reader → Automated tools cannot catch screen reader announcement errors; NVDA (free, Windows) or VoiceOver (built-in, Mac) are minimum requirements
- Using ARIA incorrectly to "fix" a11y failures → `aria-label` hides problems; fix the underlying HTML structure first

## See Also

- ← Previous: [Performance Testing Concepts](performance-testing-concepts.md) | Next: [Test Doubles](test-doubles.md) →
- Reference: [W3C WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) (current W3C Recommendation since Oct 2023; supersedes 2.1)
- Reference: [Deque axe-core — rule descriptions](https://github.com/dequelabs/axe-core/blob/master/doc/rule-descriptions.md)
- Reference: [WebAIM — WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist)
