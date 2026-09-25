---
description: "AI test generation patterns for Drupal sites — seed tests, ATK integration, Drupal-specific negative checks, and how AI generation complements ATK's catalog."
tldr: "For Drupal, point the Planner at *.routing.yml, buildForm(), and *.permissions.yml; seed state via a Testor snapshot restore. If ATK is installed, scope locators from its body classes and data-media-id attribute, not a generic test-id. Always include Drupal-specific negative checks. Don't regenerate ATK's catalog."
---

# Drupal & ATK Notes

## When to Use

> You're using the pattern with a Drupal site, optionally with ATK installed.

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

test('seed Drupal state', async ({ page }) => {
  // Requires a stored qa snapshot and a configured .testor.yml.
  execSync('ddev exec testor snapshot:restore --name=qa', { stdio: 'inherit' });
  await page.goto('/');
});
```

The Planner and Generator run the seed test before they explore. `npx playwright test` runs it as an ordinary spec, in parallel with scenario tests and in no set order. The seed must request the `page` fixture: the agents drive the browser the seed opened, and a seed without `page` or `context` fails setup with "Only tests that use default Playwright context or page fixture support test_debug". The agents run the seed inside one project. `planner_setup_page` and `generator_setup_page` take an optional `project` argument that the agent fills from the prompt; without it they use the first top-level project, in ATK `chromium`. If the seed file is outside that project, the agent reports "seed test not found" when it passed a seed path, and otherwise writes a blank `seed.spec.ts` in the project's test directory and explores with no restore. Give the seed its own project, and name the `seed` project in the agent prompt:

```ts
// playwright.config.ts (ATK ships playwright.config.js; the keys are the same)
projects: [
  { name: 'setup', testMatch: /.*\.setup\.js/ },
  {
    name: 'chromium',
    use: { ...devices['Desktop Chrome'] },
    dependencies: ['setup'],
    testIgnore: /seed\.drupal\.spec\.ts/,
  },
  { name: 'seed', use: { ...devices['Desktop Chrome'] }, testMatch: /seed\.drupal\.spec\.ts/ },
],
```

A plain `npx playwright test` runs every top-level project, `seed` included, so suite runs pass `--project=chromium`. For suite runs, put the same restore in a setup project, as in [ATK Integration's database decision](../playwright/pw-e2e-atk-integration.md#decision-database-state-across-parallel-workers). The Planner runs project dependencies before the seed. Once the seed project depends on a `restore` project, directly or through `setup`, the restore runs a second time; the seed can drop its own restore then.

## Pattern: ATK selector hooks in generated code

If ATK is installed, its preprocess hooks add body classes (`node-type-*`, `node-nid-*`, `term-vid-*`, `term-tid-*`) and a `data-media-id` attribute on media images:

```ts
await page.locator('body.node-nid-42').getByRole('heading');
```

The Generator's output can scope locators from the body class. Media IDs differ between databases, so read them at runtime rather than hard-coding them.

## Pattern: Drupal-specific negatives

Common Drupal negative checks to include in plans:

```markdown
**Negative checks:**
- `watchdog` has no new PHP notices or warnings for this request
- Browser console contains zero error-level messages
- No "There has been an error" status message is visible
- No `.messages--error` regions are visible
- The page does not redirect to `/user/login`
```

These catch Drupal-specific bug classes the Planner won't otherwise notice.

## Pattern: when the codebase uses ATK

If `composer.json` shows `drupal/automated_testing_kit`, the Planner can:
- Reference ATK helpers (`atkCommands.logInViaForm`, `atkCommands.execDrush`) instead of inlining setup
- Use `qa_accounts` users for role-based tests
- Reference ATK's pre-flight check (`tests/data/preflightTests.yml`) as a precondition. Cypress runs it in `before()`; Playwright runs it in the `setup` project, which ATK's shipped config makes every browser project depend on

See the [ATK](../atk/index.md) topic for the full integration story.

## Common Mistakes

- **Regenerating ATK's catalog with AI** — duplicates what ATK ships
- **Ignoring ATK's body classes** when ATK is installed: generated code re-derives the node ID or bundle from brittle markup
- **No Drupal-specific negatives** — misses watchdog/console-error class bugs

## See Also

- [Automated Testing Kit (ATK)](../atk/index.md)
- [Input: Code Analysis](ai-testgen-input-code.md)
- [Negative Assertions](ai-testgen-negative-assertions.md)
