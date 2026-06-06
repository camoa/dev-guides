---
description: Choose the right test layer — E2E, VR, unit, or Drupal FunctionalJavascript — for the question you're actually answering.
tldr: Default to Playwright web-first E2E for any test whose acceptance criterion includes "the user sees" or "the user clicks." Keep VR and E2E in separate test files — VR demands frozen animations and network idle; mixing the two produces tests that are both over-sensitive and under-sensitive.
---

# Layer Selection

## When to Use

> Use Playwright E2E when the acceptance criterion includes "the user sees" or "the user clicks." Use unit tests when testing pure functions; use VR when asserting visual sameness; use Drupal FunctionalJavascript when you need `\Drupal::state()` / service container assertions mid-test.

## Decision

| Question being asked | Layer | Tool |
|---|---|---|
| "Does this pure function/class produce the right output?" | Unit | Vitest (preferred) or Jest for JS; PHPUnit `Unit` for PHP |
| "Do these N modules wire together in-process?" | Integration | Vitest + MSW; PHPUnit `Kernel` |
| "Does this rendered component look the same as last week?" | Visual regression | Playwright `expect(page).toHaveScreenshot()` — see VR guide |
| "Does the user journey through real Drupal/JS/network actually work?" | **E2E (functional)** | **Playwright with web-first assertions — this guide** |
| "Does the JS-on-the-page work against a fully-bootstrapped Drupal kernel?" | Drupal FunctionalJavascript | PHPUnit `FunctionalJavascript` (Mink + ChromeDriver) |
| "Does the HTTP route return the right JSON?" | API | Playwright `request` fixture **or** Pest/PHPUnit |

## Pattern

```ts
// E2E: user-visible behavior
test('user can publish a node', async ({ page }) => {
  await page.goto('/node/1/edit');
  await page.getByLabel('Published').check();
  await page.getByRole('button', { name: 'Save' }).click();
  await expect(page.getByText('Article has been updated')).toBeVisible();
});
```

## Common Mistakes

- **Wrong**: Using Playwright as a unit-test runner — booting Chromium for a function is two orders of magnitude too expensive. **Right**: Use Vitest for pure logic
- **Wrong**: Converting all PHPUnit Functional tests to Playwright — Drupal contrib modules need PHPUnit coverage. **Right**: Playwright supplements, doesn't replace
- **Wrong**: Single mega-suite with VR + E2E mixed — different stability requirements, different failure modes. **Right**: Keep VR and E2E in separate test files/projects

## See Also

- [Playwright for Visual Regression](../visual-regression/playwright/index.md) — when the question is visual sameness
- [Automated Testing Kit (ATK)](../atk/index.md) — Drupal-specific E2E test catalog
- Reference: [Playwright Best Practices](https://playwright.dev/docs/best-practices)
