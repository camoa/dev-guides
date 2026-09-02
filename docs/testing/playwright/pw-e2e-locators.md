---
description: "Pick the right Playwright locator — role, label, text, test-id, CSS — in the correct priority order."
tldr: "Use getByRole() first, then getByLabel() for form fields, then getByTestId() for explicit test contracts — the priority order doubles as a soft a11y check. Avoid CSS class chains; they break on every theme refactor. Locators are lazy and compose — chain and filter instead of reaching for .first()."
---

# Locators

## When to Use

> Targeting elements in tests. The locator API is the single most important thing to internalize — every modern Playwright test should be ~95% locators.

## Decision

Choose locators in this order, falling back only when a higher tier is infeasible:

1. **`page.getByRole()`** — accessibility role + accessible name. Doubles as a soft a11y check
2. **`page.getByLabel()`** — for form fields. Resilient to markup churn
3. **`page.getByPlaceholder()` / `getByText()` / `getByAltText()` / `getByTitle()`** — user-visible attributes
4. **`page.getByTestId()`** — explicit test contract via `data-testid` (configurable)
5. **CSS selectors** — only when no semantic anchor exists. Prefer attribute selectors (`[data-foo="bar"]`) over class chains
6. **XPath** — last resort

## Pattern: Each Locator with Idiomatic Call

```ts
// Role — pass accessible name; exact:false matches substring; regex allowed
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('heading', { level: 2, name: /Latest news/i });
await page.getByRole('link', { name: 'Read more', exact: true });

// Text — visible text content; default substring + case-insensitive trim
await expect(page.getByText('Welcome, Carlos')).toBeVisible();
await page.getByText('Welcome', { exact: true });
await page.getByText(/order \d{6}/);

// Label — input/textarea/select via associated <label>
await page.getByLabel('Email').fill('user@example.com');

// Placeholder, alt, title
await page.getByPlaceholder('Search articles').fill('Drupal');
await page.getByAltText('Company logo').click();
await page.getByTitle('Close dialog').click();

// Test ID — default attribute is data-testid
await page.getByTestId('nav-toggle').click();
```

## Pattern: `testIdAttribute` Config

By default `getByTestId` reads `data-testid`. To target a different attribute (e.g. ATK's `data-qa-id`):

```ts
// playwright.config.ts
export default defineConfig({
  use: {
    testIdAttribute: 'data-qa-id',
  },
});
```

Now `page.getByTestId('login-form')` matches `<form data-qa-id="login-form">`.

## Pattern: Chaining and Filtering

The locator API composes. Each call returns a new Locator, lazy-evaluated at use time:

```ts
// Chain: scope inside a parent
const card = page.getByRole('article', { name: 'Welcome to Drupal' });
await card.getByRole('button', { name: 'Edit' }).click();

// .filter({ hasText }) — keep elements whose subtree contains text
await page.getByRole('listitem')
  .filter({ hasText: 'Premium' })
  .getByRole('button', { name: 'Buy' })
  .click();

// .filter({ has: locator }) — keep elements containing a child locator
await page.getByRole('row')
  .filter({ has: page.getByRole('cell', { name: 'Active' }) })
  .getByRole('button', { name: 'Disable' })
  .click();

// .filter({ hasNot, hasNotText }) — negative filters
await page.getByRole('listitem').filter({ hasNotText: 'Sold out' });

// .and() / .or() — composing locators on the same node
const primary = page.getByRole('button').and(page.locator('.btn-primary'));
const dialog = page.getByRole('dialog').or(page.getByRole('alertdialog'));

// Positional — first/last/nth — use sparingly; indicates test smell
await page.getByRole('listitem').first();
await page.getByRole('listitem').nth(2);
```

## Best-Practice Rules

- **One locator per concept**: `const submitBtn = page.getByRole('button', { name: 'Submit' })` once at the top, reuse
- **Never assert on locator count without a filter** — `.toHaveCount(3)` on a generic role is brittle; pair with `.filter()`
- **Locators are lazy** — storing `const x = page.getByText('Loading')` doesn't query the DOM until the next action/assertion
- **Avoid `.first()` as a shortcut** — silently hides "two elements match" bugs; use `.filter()` to disambiguate or `.toHaveCount(1)` to assert uniqueness
- **Don't mix locators with raw `page.evaluate(() => document.querySelector(...))`** — loses auto-wait, locator highlight, retry

## Common Mistakes

- **Brittle CSS chains** like `.btn.btn-primary.mt-3 > span:nth-child(2)` — break on every theme refactor
- **Class-name selectors** for Drupal-emitted markup that varies by render context — use `data-drupal-selector` or role-based locators
- **Porting Cypress `cy.get('.foo')` literally** — translate to `getByRole`/`getByText` instead

## See Also

- [Web-First Assertions](pw-e2e-assertions.md) — what to assert after locating
- [ATK Integration](pw-e2e-atk-integration.md) — using `data-qa-id` with ATK's selector hooks
- Reference: [Playwright Locators](https://playwright.dev/docs/locators)
