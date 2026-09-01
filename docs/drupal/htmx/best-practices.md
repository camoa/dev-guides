---
description: HTMX best practices in Drupal — security, performance, accessibility, progressive enhancement, and coding standards
tldr: "Reference this when implementing HTMX features and wanting to follow security, performance, accessibility, and development standards."
drupal_version: "11.x"
---

# Best Practices

## When to Use

> Reference this when implementing HTMX features and wanting to follow security, performance, accessibility, and development standards.

## Performance

**Use minimal responses:**
- Always use `onlyMainContent()` or `_htmx_route: TRUE` for HTMX-only endpoints
- Return only necessary content via `select()` attribute
- Cache render arrays with appropriate contexts and tags

**Optimize swap strategies:**
- Use `swap('innerHTML')` for content-only updates
- Use `swap('outerHTML')` when wrapper changes
- Use `swap('beforeend')` for append operations (load more, infinite scroll)
- Avoid `swap('none')` unless using OOB swaps

**Leverage differential asset loading:**
- Drupal automatically loads only new CSS/JS files
- Don't manually manage asset loading — trust `ajax_page_state` integration
- Group related functionality in libraries to minimize requests

**Cache aggressively:**
```php
$build['#cache'] = [
  'keys' => ['my_module', 'content', $entity_id],
  'contexts' => ['url.query_args:page'],
  'tags' => ['node:' . $entity_id],
  'max-age' => 3600,
];
```

**Avoid N+1 queries in loops:**
```php
// GOOD: Load all at once
$entities = $this->entityTypeManager
  ->getStorage('node')
  ->loadMultiple($ids);

// BAD: Loop loading
foreach ($ids as $id) {
  $entity = $this->entityTypeManager->getStorage('node')->load($id);
}
```

**Consider request debouncing:**
```php
// For live search, debounce keystrokes
(new Htmx())
  ->trigger('keyup changed delay:500ms')  // Wait 500ms after typing stops
  ->applyTo($form['search']);
```

## Accessibility

**Status messages:**
- HtmxRenderer automatically includes `#type: 'status_messages'` in responses
- Messages announce to screen readers via Drupal's messaging system

**Focus management:**
- HTMX maintains focus on triggering element by default
- For modals or major swaps, set focus explicitly via `hx-on`:
  ```php
  (new Htmx())
    ->on('::afterSwap', 'document.querySelector("#modal-content").focus()')
    ->applyTo($build['trigger']);
  ```

**Keyboard navigation:**
- Test all HTMX interactions with keyboard only
- Ensure buttons/links are focusable and activatable with Enter/Space
- Don't use `<div>` with HTMX attributes — use semantic HTML (`<button>`, `<a>`)

**ARIA attributes:**
- Add `aria-live` regions for dynamic content updates:
  ```php
  $build['results'] = [
    '#type' => 'container',
    '#attributes' => [
      'id' => 'search-results',
      'aria-live' => 'polite',
      'aria-atomic' => 'true',
    ],
  ];
  ```

**Screen reader announcements:**
- Use `aria-busy` during requests:
  ```php
  (new Htmx())
    ->indicator('#status[aria-busy="true"]')
    ->applyTo($form['submit']);
  ```

## Decision

| Area | Rule | Anti-pattern |
|------|------|-------------|
| Security | Validate all inputs server-side | Trusting client data |
| Security | Return render arrays, not HTML strings | Manual HTML strings = XSS risk |
| Security | Test all HTMX interactions under your CSP | Assuming strict CSP works out of the box |
| Performance | Use `onlyMainContent()` or `_htmx_route` | Full page responses for HTMX endpoints |
| Performance | Cache render arrays with contexts/tags | Uncached HTMX responses |
| Performance | Debounce live search (500ms) | Request on every keystroke |
| Accessibility | Use `aria-live` on dynamic regions | No screen reader announcements |
| Accessibility | Use semantic HTML elements | `<div>` with HTMX attributes |
| Code | Use dependency injection | Static `\Drupal::` service calls |
| Code | Use `Url` objects | Hardcoded path strings |
| Progressive enhancement | Form works without JavaScript | JavaScript-only form behavior |

## Pattern

**Security — proper validation:**

```php
public function buildForm(array $form, FormStateInterface $form_state, string $type = '') {
  if (!in_array($type, $this->getAllowedTypes())) {
    throw new AccessDeniedHttpException();
  }
  // Use render arrays, not raw HTML
  $form['display'] = ['#markup' => $this->renderer->render($safe_build)];
}
```

**CSP limitation:** Strict CSP policies that exclude `style-src 'unsafe-inline'` are not yet fully supported in Drupal core. A `style-src 'self'` policy (without `unsafe-inline`) causes CSP violations in multiple places across core. Tracked as [#3582309](https://www.drupal.org/node/3582309) (`main` branch, Active). Do not deploy a restrictive CSP in production without testing all HTMX interactions under that policy.

**Performance — caching:**

```php
$build['#cache'] = [
  'keys' => ['my_module', 'content', $entity_id],
  'contexts' => ['url.query_args:page'],
  'tags' => ['node:' . $entity_id],
  'max-age' => 3600,
];
```

**Performance — avoid N+1 queries:**

```php
// GOOD: Load all at once
$entities = $this->entityTypeManager->getStorage('node')->loadMultiple($ids);

// BAD: Loop loading
foreach ($ids as $id) {
  $entity = $this->entityTypeManager->getStorage('node')->load($id);
}
```

**Accessibility — ARIA live region:**

```php
$build['results'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'search-results', 'aria-live' => 'polite', 'aria-atomic' => 'true'],
];
```

**Accessibility — focus management for major swaps:**

```php
(new Htmx())
  ->on('::afterSwap', 'document.querySelector("#modal-content").focus()')
  ->applyTo($build['trigger']);
```

**Progressive enhancement:**

```php
// Form works as normal POST without JavaScript
$form['#action'] = Url::fromRoute('my.form')->toString();
$form['#method'] = 'post';
// HTMX enhances the experience
(new Htmx())->post(Url::fromRoute('my.form'))->onlyMainContent()->applyTo($form['submit']);
```

**Dependency injection:**

```php
// GOOD
class MyForm extends FormBase {
  public function __construct(
    protected EntityTypeManagerInterface $entityTypeManager,
  ) {}
  public static function create(ContainerInterface $container) {
    return new static($container->get('entity_type.manager'));
  }
}
// BAD: Static service call
$entity = \Drupal::entityTypeManager()->getStorage('node')->load($id);
```

## Common Mistakes

- **Wrong**: Trusting client input → **Right**: Always validate server-side
- **Wrong**: Not caching HTMX responses → **Right**: Performance degrades with traffic
- **Wrong**: Using static service calls → **Right**: Breaks testability; use dependency injection
- **Wrong**: Building HTML strings → **Right**: XSS vulnerabilities; use render arrays
- **Wrong**: Not testing without JavaScript → **Right**: Progressive enhancement fails
- **Wrong**: Using `<div>` with HTMX attributes → **Right**: Use semantic `<button>`, `<a>` elements
- **Wrong**: Deploying strict CSP without testing → **Right**: Core has known CSP issues (#3582309); test thoroughly

## See Also

- [Production Example: ConfigSingleExportForm](production-example-config-export.md)
- [Troubleshooting](troubleshooting.md)
- Reference: [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
- Reference: [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- Reference: [Drupal Core Issue #3582309 — CSP support](https://www.drupal.org/node/3582309)
