---
description: Accessibility testing — what automated tools catch (≈35% of WCAG issues) and what requires manual keyboard and screen reader testing.
tldr: Automated a11y tools (axe-core, Lighthouse) catch ~35% of detectable WCAG issues — missing alt text, contrast failures, duplicate IDs. The rest requires manual keyboard navigation and screen reader testing. Add axe-playwright to E2E tests and jest-axe to component tests; failing violations must block merges.
---

# Accessibility Testing Concepts

## When to Use

> Use automated a11y testing as a first gate for every UI change — it catches mechanical WCAG violations with minimal effort. Supplement with manual keyboard and screen reader testing for every new feature and major UI change. "Automated tests pass" does not mean "accessible."

## Decision

| Automated tools catch | Not automatable |
|---|---|
| Missing `alt` on images | Focus order makes sense |
| Form inputs without labels | Screen reader announces content correctly |
| Insufficient color contrast (4.5:1 for normal text) | Interaction is operable by keyboard |
| Missing ARIA roles or landmarks | Error messages are useful and contextual |
| Empty button or link text | Complex ARIA widget behavior |
| Duplicate IDs | Animations are not distracting for vestibular conditions |

Automated tools catch approximately **30–40% of WCAG issues**. The rest requires human judgment.

## Pattern

```javascript
// axe-core with Playwright — best coverage for page-level tests
import { checkA11y } from 'axe-playwright';

test('registration form has no critical accessibility violations', async ({ page }) => {
  await page.goto('/register');
  await checkA11y(page, undefined, {
    runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa'] },
    axeOptions: { reporter: 'v2' },
  });
});
```

Run automated a11y checks at two layers:
- Component/unit tests: `jest-axe` (React component level)
- E2E/functional tests: `axe-playwright` (page level)
- CI: failing violations block merges for new violations

**Manual checklist** for new features:
- Tab through all interactive elements — logical order, keyboard operable
- Screen reader announces content correctly (NVDA/Windows, VoiceOver/Mac)
- Color contrast passes WCAG AA (4.5:1 normal text, 3:1 large text/UI)
- No content relies solely on color to convey meaning
- Animations respect `prefers-reduced-motion`

## Common Mistakes

- **Wrong**: Treating automated a11y pass as "accessible" → **Right**: Passes only ~35% of detectable issues; manual testing is required
- **Wrong**: Running a11y tools only at the end of development → **Right**: Add axe to component-level tests; find violations early when cheap to fix
- **Wrong**: Ignoring "moderate" or "minor" violations → **Right**: They accumulate and block users with disabilities; triage and address them
- **Wrong**: Using ARIA to "fix" a11y failures → **Right**: Fix the underlying HTML structure first; `aria-label` hides problems

## See Also

- [Performance Testing Concepts](performance-testing-concepts.md) | Next: [Test Doubles](test-doubles.md)
- Reference: [W3C WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/)
- Reference: [Deque axe-core — rule descriptions](https://github.com/dequelabs/axe-core/blob/master/doc/rule-descriptions.md)
- Reference: [WebAIM — WCAG 2 Checklist](https://webaim.org/standards/wcag/checklist)
