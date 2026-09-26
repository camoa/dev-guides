---
description: "ATK's two preprocess hooks (body classes, data-media-id) for finding entity IDs, and how ATK's own tests select markup otherwise."
tldr: "ATK adds no generic test attribute — only two preprocess hooks: body classes like node-nid-42 on node/term routes, and data-media-id on images tied to a media entity. Read them with atkCommands.getNid()/getMid() or cy.getNid()/getMid(); ATK never added data-qa-id."
drupal_version: "11.x"
---

# ATK Selector Hooks

## When to Use

> Finding the ID of the node, term or media item a test just created.

## What ATK Adds

ATK adds **no generic test attribute**. `automated_testing_kit.module` has two preprocess hooks:

| Hook | Adds | Example |
|---|---|---|
| `automated_testing_kit_preprocess_html()` | Body classes on node and term routes | `node-type-article`, `node-nid-42`, `term-vid-tags`, `term-tid-7` |
| `automated_testing_kit_preprocess_image()` | `data-media-id` on an image that belongs to a media entity | `<img data-media-id="12">` |

The image hook matches the file by name, strips a `.webp` or `.avif` suffix, and reads `field_media_image`.

## Pattern: reading the IDs

The helpers read these for you:

```js
// Playwright
const nid = await atkCommands.getNid(page)          // parses node-nid-N from <body>
const mid = await atkCommands.getMid(imageLocator)  // reads data-media-id
```

```js
// Cypress
cy.getNid().then((nid) => { /* ... */ })
cy.get('img[alt*="token"]').getMid().then((mid) => { /* ... */ })
```

## Pattern: selecting everything else

ATK's own tests use Drupal's markup directly:

- Form IDs: `#edit-name`, `#edit-pass`, `#user-login-form > #edit-actions > #edit-submit`
- Labels and roles: `page.getByLabel('Username')`, `page.getByRole('button', { name: 'Log in' })`
- Field names: `input[name="title[0][value]"]`
- Messages: `[data-drupal-selector="messages"]` (in `expectMessage()`)

If you want a dedicated test attribute, add your own in a preprocess hook:

```php
function mytheme_preprocess_node(array &$variables): void {
  $variables['attributes']['data-testid'] = 'node-' . $variables['node']->bundle();
}
```

Playwright's `getByTestId()` reads `data-testid` by default.

## Common Mistakes

- **Looking for `data-qa-id`** — ATK never added it, in any release
- **Calling `getNid()` on a non-node page** — it throws, because the body has no `node-nid-*` class
- **Expecting `data-media-id` on every image** — only images whose file belongs to a media entity get it

## See Also

- [Helper Functions](atk-helper-functions.md)
- [Custom Tests](atk-custom-tests.md)
- [Anti-Patterns](atk-anti-patterns.md)
- Reference: `automated_testing_kit.module` at https://git.drupalcode.org/project/automated_testing_kit
