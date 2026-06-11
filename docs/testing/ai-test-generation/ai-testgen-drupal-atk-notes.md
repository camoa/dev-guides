---
description: AI test generation patterns for Drupal sites — seed tests, ATK integration, Drupal-specific negative checks, and how AI generation complements ATK's catalog.
tldr: For Drupal, point the Planner at *.routing.yml + buildForm() + *.permissions.yml. Use a seed test that runs drush si + recipe. If ATK is installed, set testIdAttribute:'data-qa-id' to get stable selectors for free. Always include Drupal-specific negative checks (watchdog, console errors, no unexpected /user/login redirects). Don't regenerate ATK's catalog — use ATK for generic Drupal tests, AI for project-specific feature tests.
---

# Drupal & ATK Notes

## When to Use

> Use this when applying the AI test generation pattern to a Drupal site, optionally with ATK installed.

## Decision

| Need | Source |
|---|---|
| Generic Drupal tests (login, content CRUD, page errors) | ATK's shipped catalog — already written |
| Project-specific feature tests | AI-generated via this pattern |
| Both | Both coexist; ATK is the baseline, AI fills the gaps |

## Pattern: useful Drupal code-analysis sources

| Source | Yields |
|---|---|
| `*.routing.yml` | Routes + access |
| `src/Form/*.php` `buildForm()` | Field names, labels, `#required`, `#type` |
| `node.type.*.yml`, `field.field.*.yml` | Content types and field structure |
| `*.permissions.yml` | Roles for boundary cases |
| `composer.json` | ATK / qa_accounts / Drush detection |
| `drush role:list`, `drush role:perms` | Live permission inventory |

## Pattern: seed test for Drupal

```ts
// tests/seed.drupal.spec.ts
import { test, expect } from '@playwright/test';
import { execSync } from 'child_process';

test('seed Drupal state', async () => {
  execSync('ddev drush si --existing-config -y', { stdio: 'inherit' });
  execSync('ddev drush recipe ../recipes/atk-demo', { stdio: 'inherit' });
  execSync('ddev drush testor:restore qa-baseline', { stdio: 'inherit' });
});
```

## Pattern: ATK selector hooks in generated code

If ATK is installed:

```ts
// playwright.config.ts
use: { testIdAttribute: 'data-qa-id' }
```

The Generator's output then uses `getByTestId('login-form')`, which matches ATK's `data-qa-id` attributes. The plan stays behavioral; the code gets stable selectors for free.

## Pattern: Drupal-specific negatives

Include these in every plan for a Drupal site:

```markdown
**Negative checks:**
- `watchdog` has no new PHP notices or warnings for this request
- Browser console contains zero error-level messages
- No "There has been an error" status message is visible
- No `.messages--error` regions are visible
- The page does not redirect to `/user/login`
```

## Common Mistakes

- **Wrong**: Regenerating ATK's catalog with AI → **Right**: duplicates what ATK ships; use ATK for generic Drupal tests
- **Wrong**: Not using ATK's selector hooks when ATK is installed → **Right**: generated code uses brittle selectors when stable ones are available for free
- **Wrong**: No Drupal-specific negatives → **Right**: misses watchdog/console-error class bugs

## See Also

- [Automated Testing Kit (ATK)](../atk/index.md)
- [Input: Code Analysis](ai-testgen-input-code.md)
- [Negative Assertions](ai-testgen-negative-assertions.md)
