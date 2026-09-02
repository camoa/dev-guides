---
description: "Drupal-specific Playwright E2E patterns — Form API, AJAX waits, Big Pipe, session cookies, Drush setup, and entity CRUD via JSON:API."
tldr: "Wait for AJAX with waitForResponse targeting /system/ajax — not waitForTimeout or jQuery.active. Handle Big Pipe by asserting on final content, not placeholder markup. Create entities via JSON:API, drive UI for the feature under test, verify via JSON:API."
---

# Drupal & DDEV Patterns

## When to Use

> Functional E2E against Drupal sites under DDEV. (DDEV plumbing — `baseURL`, `ignoreHTTPSErrors`, storage state — is in the [VR guide's Drupal section](../visual-regression/playwright/pw-vr-drupal-ddev.md).)

## Pattern: Form API Specifics

Drupal forms include hidden fields you generally don't touch (`form_token`, `form_id`, `form_build_id`). Submit via the actual button — Playwright fills visible inputs, hidden fields ride along.

Where you have to be careful:

**Entity reference autocomplete fields** — typing matches via AJAX; wait for the dropdown:

```ts
await page.getByLabel('Author').fill('admin');
await page.getByRole('option', { name: /^admin\s/ }).click();
```

**`--SELECT--` placeholder option** on entity reference dropdowns and many select widgets — assert it's gone (or pick a real option) before submitting.

**Machine-name fields** — Drupal AJAX-fills these after typing the human label. Wait via `expect(...).toHaveValue(...)` rather than `waitForTimeout`.

## Pattern: AJAX-Driven Forms

Two robust waiting patterns:

```ts
// Wait for the response that matters, not for arbitrary time
await Promise.all([
  page.waitForResponse(r => r.url().includes('/system/ajax') && r.ok()),
  page.getByRole('button', { name: 'Add another item' }).click(),
]);

// Wait for the throbber to disappear
await expect(page.locator('.ajax-progress, .throbber')).toHaveCount(0);
```

Avoid `window.jQuery.active === 0` via `evaluate()` — fragile, long-time flake source. `waitForResponse` is more specific and faster.

## Pattern: Big Pipe Placeholders

Big Pipe streams placeholders, then injects real markup via `<script type="application/vnd.drupal-ajax">` tags.

For locators that match the placeholder *and* the replaced content:

```ts
// Reliable: wait for the real content, not the placeholder
await expect(page.getByRole('region', { name: 'User account menu' }))
  .toContainText(/Log out/);
```

For elements that don't exist until Big Pipe replaces the placeholder, use `toBeAttached()` first, then act.

## Pattern: Contextual Links and Quickedit

These render only on hover for users with `access contextual links`. Mitigations:
- Test as a role lacking the permission unless the test is *about* contextual links
- Or dismiss in setup: `await page.keyboard.press('Escape');` after any hover near `.contextual`

## Drupal Session Cookies

- Cookie name is `SESS<32-char-hash>` over HTTP, `SSESS<…>` over HTTPS
- DDEV defaults to HTTPS — expect `SSESS…`
- `secure: true, sameSite: 'Lax'` are typical; if injecting cookies manually, mirror those flags or login silently fails
- Don't hard-code the name — use `context.cookies()` and filter by prefix

## Pattern: Drush from Tests for Setup

```ts
import { execSync } from 'child_process';

test.beforeAll(() => {
  execSync('ddev drush en my_module -y', { stdio: 'inherit' });
  execSync('ddev drush cr', { stdio: 'inherit' });
});
```

Wrap in a worker-scoped fixture if the cost is significant. Couples tests to a DDEV/Drush environment — fine for project repos, problematic for portable test catalogs.

## Decision: Entity CRUD via UI vs JSON:API + UI Verification

The recommended pattern (Section 7's "killer pattern" applied to Drupal):

1. Create the node via JSON:API or `drush content:export` recipe (fast, deterministic)
2. Drive UI for the *thing under test* (publishing, paragraph editing, moderation transition)
3. Verify via JSON:API

UI-creating a node touches dozens of fields, alters, and behaviors irrelevant to most tests.

## Drupal-Specific Waits

| Scenario | Approach |
|---|---|
| Cache rebuild after config change | `await execSync('ddev drush cr')` then re-navigate; assert with `expect(...).toContainText(...)` for post-cr slow first request |
| Deferred fields / lazy builders | Same as Big Pipe — assert against final content |
| Search index reindex | `expect.toPass({ timeout: 60_000 })` polling search results |

## Common Mistakes

- **Hardcoded `waitForTimeout` after AJAX** — use `waitForResponse` or assertion auto-retry
- **Not handling Big Pipe** — first assertion fails on placeholder content
- **`ddev drush cr` between every test** — kills suite time; use sparingly

## See Also

- [API Testing](pw-e2e-api-testing.md) — the JSON:API + UI hybrid pattern in detail
- [Authentication](pw-e2e-authentication.md) — Drupal session cookies and `storageState`
- [ATK Integration](pw-e2e-atk-integration.md) — Drush-backed DB reset with Testor
- Reference: [Lullabot/playwright-drupal](https://github.com/Lullabot/playwright-drupal) — parallel SQLite per worker for full DB isolation
