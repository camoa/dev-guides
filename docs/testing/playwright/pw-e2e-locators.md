---
description: Pick the right Playwright locator — role, label, text, test-id, CSS — in the correct priority order.
tldr: Use getByRole() first, then getByLabel() for form fields, then getByTestId() for explicit test contracts — the priority order doubles as a soft a11y check. Avoid CSS class chains; they break on every theme refactor. Locators are lazy and compose — chain and filter instead of reaching for .first().
---

# Locators

## When to Use

> Use locators for every element target in a Playwright test. Choose from the priority order below, falling back only when a higher tier is infeasible.

## Decision

| Priority | Locator | When |
|---|---|---|
| 1 | `page.getByRole()` | Accessibility role + accessible name — most resilient, doubles as a11y check |
| 2 | `page.getByLabel()` | Form fields — resilient to markup churn |
| 3 | `page.getByPlaceholder()` / `getByText()` / `getByAltText()` / `getByTitle()` | User-visible attributes |
| 4 | `page.getByTestId()` | Explicit test contract via `data-testid` (configurable) |
| 5 | CSS selectors | Only when no semantic anchor exists — prefer attribute selectors (`[data-foo="bar"]`) over class chains |
| 6 | XPath | Last resort |

## Pattern

```ts
// Role — pass accessible name; exact:false matches substring; regex allowed
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('heading', { level: 2, name: /Latest news/i });

// Label — form fields
await page.getByLabel('Email').fill('user@example.com');

// Text
await expect(page.getByText('Welcome, Carlos')).toBeVisible();

// Test ID — default attribute is data-testid
await page.getByTestId('nav-toggle').click();

// Chain: scope inside a parent
const card = page.getByRole('article', { name: 'Welcome to Drupal' });
await card.getByRole('button', { name: 'Edit' }).click();

// Filter: keep elements whose subtree contains text
await page.getByRole('listitem')
  .filter({ hasText: 'Premium' })
  .getByRole('button', { name: 'Buy' })
  .click();
```

### `testIdAttribute` config

```ts
// playwright.config.ts — target a different attribute (e.g. ATK's data-qa-id)
export default defineConfig({
  use: { testIdAttribute: 'data-qa-id' },
});
```

### Chaining and filtering

```ts
// .and() / .or() — composing on the same node
const primary = page.getByRole('button').and(page.locator('.btn-primary'));

// .filter({ has: locator }) — keep elements containing a child locator
await page.getByRole('row')
  .filter({ has: page.getByRole('cell', { name: 'Active' }) })
  .getByRole('button', { name: 'Disable' })
  .click();

// Positional — use sparingly; indicates test smell
await page.getByRole('listitem').first();
```

## Common Mistakes

- **Wrong**: Brittle CSS chains like `.btn.btn-primary.mt-3 > span:nth-child(2)` — break on every theme refactor. **Right**: `getByRole('button', { name: 'Submit' })`
- **Wrong**: Class-name selectors for Drupal-emitted markup that varies by render context. **Right**: Use `data-drupal-selector` or role-based locators
- **Wrong**: Porting Cypress `cy.get('.foo')` literally. **Right**: Translate to `getByRole`/`getByText`
- **Wrong**: Using `.first()` as a shortcut — silently hides "two elements match" bugs. **Right**: Use `.filter()` to disambiguate or `.toHaveCount(1)` to assert uniqueness

## See Also

- [Web-First Assertions](pw-e2e-assertions.md) — what to assert after locating
- [ATK Integration](pw-e2e-atk-integration.md) — using `data-qa-id` with ATK's selector hooks
- Reference: [Playwright Locators](https://playwright.dev/docs/locators)
