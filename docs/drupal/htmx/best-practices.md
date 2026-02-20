---
description: HTMX best practices in Drupal — security, performance, accessibility, progressive enhancement, and coding standards
drupal_version: "11.x"
---

# Best Practices

## When to Use

> Reference this when implementing HTMX features and wanting to follow security, performance, accessibility, and development standards.

## Decision

| Area | Rule | Anti-pattern |
|------|------|-------------|
| Security | Validate all inputs server-side | Trusting client data |
| Security | Return render arrays, not HTML strings | Manual HTML strings = XSS risk |
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

**Performance — caching:**

```php
$build['#cache'] = [
  'keys' => ['my_module', 'content', $entity_id],
  'contexts' => ['url.query_args:page'],
  'tags' => ['node:' . $entity_id],
  'max-age' => 3600,
];
```

**Accessibility — ARIA live region:**

```php
$build['results'] = [
  '#type' => 'container',
  '#attributes' => ['id' => 'search-results', 'aria-live' => 'polite', 'aria-atomic' => 'true'],
];
```

**Progressive enhancement:**

```php
// Form works as normal POST without JavaScript
$form['#action'] = Url::fromRoute('my.form')->toString();
$form['#method'] = 'post';
// HTMX enhances the experience
(new Htmx())->post(Url::fromRoute('my.form'))->onlyMainContent()->applyTo($form['submit']);
```

## Common Mistakes

- **Wrong**: Trusting client input → **Right**: Always validate server-side
- **Wrong**: Not caching HTMX responses → **Right**: Performance degrades with traffic
- **Wrong**: Using static service calls → **Right**: Breaks testability; use dependency injection
- **Wrong**: Building HTML strings → **Right**: XSS vulnerabilities; use render arrays
- **Wrong**: Not testing without JavaScript → **Right**: Progressive enhancement fails
- **Wrong**: Using `<div>` with HTMX attributes → **Right**: Use semantic `<button>`, `<a>` elements

## See Also

- [Production Example: ConfigSingleExportForm](production-example-config-export.md)
- [Troubleshooting](troubleshooting.md)
- Reference: [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
- Reference: [WCAG Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
