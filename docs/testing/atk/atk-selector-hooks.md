---
description: ATK selector hooks — stable data-qa-id test attributes added via Drupal preprocess hooks to prevent test breakage from volatile DOM changes.
tldr: ATK adds stable data-qa-id attributes to common Drupal markup via preprocess hooks, decoupling tests from volatile class names and Form API ID mangling. Extend the same convention in your module/theme preprocess hooks for custom markup.
drupal_version: "11.x"
---

# ATK Selector Hooks

## When to Use

> Use selector hooks when targeting Drupal-rendered markup from tests. Use volatile class names only when no selector hook exists and the element has no other stable identifier.

## Decision

| Test target | Selector |
|---|---|
| ATK-supplied UI (login, content edit, admin menu) | ATK's `data-qa-id` attribute |
| Your custom markup | Add `data-qa-id` in a preprocess hook in your module/theme |
| Third-party module's rendered markup | Add a preprocess hook in your module/theme to inject the attribute |

### The Problem

Drupal's rendered DOM contains classes and IDs that change across versions, themes, and modules:
- `#edit-name` becomes `#edit-name--BG87f2qDxQk` after Form API mangling
- `.node--type-article` varies by render context
- View list classes change when the view's machine name does

## Pattern

### Use ATK's selector hook (Playwright)

```ts
await page.locator('[data-qa-id="login-form-submit"]').click();
await page.locator('[data-qa-id="user-menu-account"]').hover();
```

### Use ATK's selector hook (Cypress)

```js
cy.get('[data-qa-id="login-form-submit"]').click();
```

### Extend in your module/theme

```php
function mytheme_preprocess_node(array &$variables): void {
  if ($variables['node']->bundle() === 'article') {
    $variables['attributes']['data-qa-id'] = 'article-' . $variables['view_mode'];
  }
}
```

Your tests now select `[data-qa-id="article-teaser"]` reliably across theme changes.

## Common Mistakes

- **Wrong**: Using Drupal-generated class names in selectors → **Right**: they break on every Drupal upgrade or theme change
- **Wrong**: Adding `data-qa-id` to render arrays directly → **Right**: preprocess hooks are the right place; render arrays get rebuilt and lose attribute additions
- **Wrong**: Reusing the same `data-qa-id` value across multiple elements → **Right**: selectors return ambiguous matches

## See Also

- [Custom Tests](atk-custom-tests.md)
- [Anti-Patterns](atk-anti-patterns.md)
- Reference: `automated_testing_kit.module` in the canonical repo
