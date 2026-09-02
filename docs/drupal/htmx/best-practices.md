---
description: "HTMX best practices in Drupal — security, performance, accessibility, progressive enhancement, and coding standards"
tldr: "Reference this when implementing HTMX features and wanting to follow security, performance, accessibility, and development standards. Validate server-side, cache aggressively, use aria-live for dynamic regions, and never build HTML strings by hand."
drupal_version: "11.x"
---

# Best Practices

## When to Use

> You're implementing HTMX features and want to follow security, performance, accessibility, and development standards.

## Security

**Always validate and sanitize on server:**
- HTMX requests are HTTP requests — all standard security rules apply
- Never trust client data — validate form inputs and URL parameters
- Use CSRF tokens — Drupal forms include automatic token validation
- Check permissions — Use `#access` on form elements and `_permission` on routes
- Sanitize output — Use render arrays, not raw HTML strings
- Avoid XSS — Return render arrays through FormBuilder/Controller, not manual HTML

**Example: Proper Validation**
```php
public function buildForm(array $form, FormStateInterface $form_state, string $type = '') {
  // Validate URL parameter
  $allowed_types = ['a', 'b', 'c'];
  if (!in_array($type, $allowed_types)) {
    throw new AccessDeniedHttpException();
  }

  // Use form API for automatic sanitization
  $form['display'] = [
    '#markup' => $this->renderer->render($safe_render_array),
  ];
}
```

**Anti-pattern:**
```php
// NEVER do this - XSS vulnerability
$form['display']['#markup'] = '<div>' . $_GET['user_input'] . '</div>';
```

Reference: [OWASP XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

**Content Security Policy (CSP) limitation:**

Strict CSP policies that exclude `style-src 'unsafe-inline'` are not yet fully supported in Drupal core. A `style-src 'self'` policy (without `unsafe-inline`) causes CSP violations in multiple places across core. This is an open feature request tracked as [#3582309](https://www.drupal.org/node/3582309) (`main` branch, Active). Do not deploy a restrictive CSP in production without testing all HTMX interactions under that policy.

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

## Development Standards

**Use dependency injection:**
```php
// GOOD: Inject services
class MyForm extends FormBase {
  public function __construct(
    protected EntityTypeManagerInterface $entityTypeManager,
    protected ConfigFactoryInterface $configFactory,
  ) {}

  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('entity_type.manager'),
      $container->get('config.factory'),
    );
  }
}

// BAD: Static service calls
$entity = \Drupal::entityTypeManager()->getStorage('node')->load($id);
```

**Return render arrays, not HTML:**
```php
// GOOD: Render arrays
return ['#markup' => $this->renderer->render($build)];

// BAD: Manual HTML
return ['#markup' => '<div class="content">' . $content . '</div>'];
```

**Use Url objects:**
```php
// GOOD: Url objects
(new Htmx())->get(Url::fromRoute('my.route', ['id' => $id]));

// BAD: Hardcoded paths
(new Htmx())->get('/my-module/content/' . $id);
```

**Follow coding standards:**
- Use type hints on all methods
- Document complex logic with inline comments
- Follow Drupal coding standards (phpcs, phpstan)

**Test both HTMX and non-HTMX requests:**
- Initial page load is never HTMX
- Progressive enhancement means non-JavaScript fallback required
- Test form submissions with JavaScript disabled

## Progressive Enhancement

**Always provide fallback:**
```php
// Form works as normal POST without JavaScript
$form['#action'] = Url::fromRoute('my.form')->toString();
$form['#method'] = 'post';

// HTMX enhances the experience
(new Htmx())
  ->post(Url::fromRoute('my.form'))
  ->onlyMainContent()
  ->applyTo($form['submit']);
```

**Graceful degradation:**
- Links work as regular links without JavaScript
- Forms submit normally without JavaScript
- Content is accessible without HTMX enhancements

**Use semantic HTML:**
```php
// GOOD: Semantic button
$build['submit'] = ['#type' => 'button', '#value' => 'Submit'];
(new Htmx())->post($url)->applyTo($build['submit']);

// BAD: Non-semantic element
$build['submit'] = [
  '#type' => 'html_tag',
  '#tag' => 'div',
  '#value' => 'Submit',
  '#attributes' => ['role' => 'button'],
];
```

## Common Mistakes

- Trusting client input — Always validate server-side
- Not caching HTMX responses — Performance degrades with traffic
- Forgetting keyboard accessibility — Not all users use mouse
- Using static service calls — Breaks testability and best practices
- Not testing without JavaScript — Progressive enhancement fails
- Hardcoding URLs — Breaks multilingual sites and aliases
- Building HTML strings — XSS vulnerabilities and bypasses render system
- Not using semantic HTML — Accessibility and SEO suffer

## See Also

- Previous: [Complete Production Example](production-example-config-export.md)
- Next: [Troubleshooting](troubleshooting.md)
- Reference: [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
- Reference: [Web Content Accessibility Guidelines (WCAG)](https://www.w3.org/WAI/WCAG21/quickref/)
