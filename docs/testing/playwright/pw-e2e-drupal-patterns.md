---
description: Drupal-specific Playwright E2E patterns — Form API, AJAX waits, Big Pipe, session cookies, Drush setup, and entity CRUD via JSON:API.
tldr: Wait for AJAX with waitForResponse targeting /system/ajax — not waitForTimeout or jQuery.active. Handle Big Pipe by asserting on final content, not placeholder markup. Create entities via JSON:API, drive UI for the feature under test, verify via JSON:API.
---

# Drupal & DDEV Patterns

## When to Use

> Use these patterns for functional E2E against Drupal sites under DDEV. For DDEV plumbing (baseURL, ignoreHTTPSErrors, storage state), see the [VR guide's Drupal section](../visual-regression/playwright/pw-vr-drupal-ddev.md).

## Drupal Session Cookies

- Cookie name is `SESS<32-char-hash>` over HTTP, `SSESS<…>` over HTTPS
- DDEV defaults to HTTPS — expect `SSESS…`
- `secure: true, sameSite: 'Lax'` are typical; if injecting cookies manually, mirror those flags or login silently fails
- Don't hard-code the name — use `context.cookies()` and filter by prefix

## Decision

| Scenario | Approach |
|---|---|
| Cache rebuild after config change | `execSync('ddev drush cr')` then re-navigate; assert with `expect(...).toContainText(...)` |
| Deferred fields / lazy builders | Same as Big Pipe — assert against final content |
| Search index reindex | `expect.toPass({ timeout: 60_000 })` polling search results |
| Entity CRUD | Create via JSON:API, drive UI for the feature under test, verify via JSON:API |

## Pattern

### Form API specifics

```ts
// Entity reference autocomplete — wait for AJAX dropdown
await page.getByLabel('Author').fill('admin');
await page.getByRole('option', { name: /^admin\s/ }).click();
```

Drupal forms include hidden fields (`form_token`, `form_id`, `form_build_id`). Submit via the actual button — Playwright fills visible inputs, hidden fields ride along.

### AJAX-driven forms

```ts
// Wait for the response that matters
await Promise.all([
  page.waitForResponse(r => r.url().includes('/system/ajax') && r.ok()),
  page.getByRole('button', { name: 'Add another item' }).click(),
]);

// Wait for the throbber to disappear
await expect(page.locator('.ajax-progress, .throbber')).toHaveCount(0);
```

### Big Pipe placeholders

```ts
// Reliable: wait for real content, not the placeholder
await expect(page.getByRole('region', { name: 'User account menu' }))
  .toContainText(/Log out/);
// For elements that don't exist until Big Pipe replaces the placeholder:
await expect(myLocator).toBeAttached();
```

### Session cookies (DDEV)

- Cookie name is `SESS<32-char-hash>` over HTTP, `SSESS<…>` over HTTPS
- DDEV defaults to HTTPS — expect `SSESS…`
- Don't hard-code the name — use `context.cookies()` and filter by prefix

### Drush from tests for setup

```ts
import { execSync } from 'child_process';

test.beforeAll(() => {
  execSync('ddev drush en my_module -y', { stdio: 'inherit' });
  execSync('ddev drush cr', { stdio: 'inherit' });
});
```

Wrap in a worker-scoped fixture if the cost is significant.

### Entity CRUD — recommended pattern

1. Create the node via JSON:API or Drush (fast, deterministic)
2. Drive UI for the thing under test (publishing, paragraph editing, moderation transition)
3. Verify via JSON:API

UI-creating a node touches dozens of fields, alters, and behaviors irrelevant to most tests.

## Common Mistakes

- **Wrong**: Hardcoded `waitForTimeout` after AJAX — use `waitForResponse` or assertion auto-retry
- **Wrong**: Not handling Big Pipe — first assertion fails on placeholder content
- **Wrong**: `ddev drush cr` between every test — kills suite time; use sparingly

## See Also

- [API Testing](pw-e2e-api-testing.md) — the JSON:API + UI hybrid pattern in detail
- [Authentication](pw-e2e-authentication.md) — Drupal session cookies and `storageState`
- [ATK Integration](pw-e2e-atk-integration.md) — Drush-backed DB reset with Testor
- Reference: [Lullabot/playwright-drupal](https://github.com/Lullabot/playwright-drupal) — parallel SQLite per worker for full DB isolation
