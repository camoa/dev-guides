---
description: Security best practices (XSS protection, access checks, CSRF) and performance optimization (cache strategies, lazy loading, efficient attachments).
---

# Security & Performance

## Security Best Practices

### XSS Protection in Render Arrays

**The Render API's security model:**

| Property | XSS Protection | When to Use |
|---|---|---|
| `#plain_text` | **Full protection** -- all HTML escaped | User input, untrusted data |
| `#markup` | **Filtered** -- admin XSS filter applied | Trusted admin content, module output |
| `Markup::create()` | **NONE** -- you guarantee it's safe | Already-sanitized HTML, trusted sources only |
| `#value` in `html_tag` | **Filtered** if string, none if Markup | Mix of trusted/untrusted |

---

### RULE 1: Never Use #markup with Raw User Input

**VULNERABLE:**

```php
// User-submitted comment
$comment_body = $_POST['comment'];

return [
  '#markup' => $comment_body,
];
// Attacker submits: <script>alert('XSS')</script>
// Script executes on other users' browsers
```

**SAFE:**

```php
use Drupal\Component\Utility\Html;

$comment_body = $_POST['comment'];

return [
  '#markup' => Html::escape($comment_body),
];

// BETTER: Use #plain_text
return [
  '#plain_text' => $comment_body,
];
```

**Reference:** [OWASP XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

---

### RULE 2: Use t() with Placeholders, Not Concatenation

**VULNERABLE:**

```php
$username = $user->getDisplayName();  // Could contain HTML

return [
  '#markup' => '<p>' . t('Welcome, ' . $username) . '</p>',
];
// t() doesn't escape the concatenated part
```

**SAFE:**

```php
return [
  '#markup' => '<p>' . t('Welcome, @username', ['@username' => $username]) . '</p>',
];
// @placeholder escapes HTML
// !placeholder doesn't escape (for trusted HTML only)
// :placeholder escapes and wraps in <em> (for emphasized text)
```

---

### RULE 3: Validate and Sanitize in Lazy Builders

Lazy builders run after cache retrieval -- validate all arguments:

```php
public static function buildUserWidget($user_id) {
  // VALIDATE: Ensure $user_id is actually numeric
  if (!is_numeric($user_id) || $user_id < 1) {
    return ['#markup' => ''];
  }

  $user = User::load($user_id);

  // CHECK: Ensure user exists and current user can view it
  if (!$user || !$user->access('view')) {
    return ['#markup' => ''];
  }

  return [
    '#theme' => 'user_widget',
    '#user' => $user,
  ];
}
```

---

### RULE 4: Use Access Checks, Not Manual Permission Checks

**WRONG:**

```php
$current_user = \Drupal::currentUser();

if (in_array('administrator', $current_user->getRoles())) {
  // Show admin content
  $build['admin_section'] = ['#markup' => 'Admin stuff'];
}
```

**RIGHT:**

```php
$access_result = $this->currentUser()->hasPermission('administer site configuration');

$build['admin_section'] = [
  '#access' => $access_result,
  '#markup' => 'Admin stuff',
  '#cache' => ['contexts' => ['user.permissions']],
];
```

**Why:** Using `#access` with proper cache contexts prevents caching the wrong access decision for different users.

## Performance Best Practices

### Cache Strategy Decision Tree

```
Does output vary by request?
+-- NO -> Cache with max-age = Cache::PERMANENT, keys only
+-- YES -> What does it vary by?
    +-- User identity -> Add context 'user'
    +-- User permissions -> Add context 'user.permissions'
    +-- URL -> Add context 'url.path' or 'url.query_args'
    +-- Language -> Add context 'languages:language_interface'
    +-- Time -> Use appropriate max-age (60 for 1 min, 3600 for 1 hour)

Does output depend on entities/config?
+-- YES -> Add cache tags from those objects
    Example: $node->getCacheTags(), $config->getCacheTags()

Is part of it expensive/uncacheable?
+-- YES -> Split into:
    +-- Cacheable part (static content)
    +-- Lazy builder for expensive/dynamic part
```

---

### Performance Pattern: Lazy-Load Expensive Content

**BEFORE (slow):**

```php
public function build() {
  // Expensive: API call, complex query, external service
  $expensive_data = $this->fetchDataFromAPI();

  return [
    '#markup' => $this->formatData($expensive_data),
    '#cache' => ['max-age' => 0],  // Can't cache (personalized)
  ];
}
// Result: Every page load waits for API call
```

**AFTER (fast):**

```php
public function build() {
  return [
    'static_header' => [
      '#markup' => '<h2>Data Section</h2>',
      '#cache' => ['max-age' => Cache::PERMANENT],
    ],
    'dynamic_data' => [
      '#lazy_builder' => ['\Drupal\mymodule\Builder::fetchData', []],
      '#create_placeholder' => TRUE,
    ],
  ];
}

// In Builder::fetchData()
public static function fetchData() {
  $data = self::fetchDataFromAPI();  // Expensive call
  return [
    '#markup' => self::formatData($data),
    '#cache' => ['max-age' => 0],
  ];
}
// Result: Static header cached, API call only for dynamic part
// With Big Pipe: Page loads immediately, dynamic part streams in
```

**Performance gain:** 80%+ faster page loads for cached users.

---

### Avoid Rendering in Loops

**SLOW:**

```php
foreach ($items as $item) {
  $build[] = \Drupal::service('renderer')->render([
    '#markup' => $item->label(),
  ]);
}
```

**FAST:**

```php
foreach ($items as $item) {
  $build[] = ['#markup' => $item->label()];
}
// Let parent render all children at once
```

**Why:** Each `render()` call has overhead. Batch rendering is more efficient.

---

### Use #attached Efficiently

**INEFFICIENT:**

```php
// Loading library for every item
foreach ($products as $product) {
  $build[$product->id()] = [
    '#theme' => 'product_teaser',
    '#product' => $product,
    '#attached' => ['library' => ['mymodule/product-behavior']],
  ];
}
// Result: Same library attached 20 times (though Drupal deduplicates)
```

**EFFICIENT:**

```php
$build = [
  '#attached' => ['library' => ['mymodule/product-behavior']],
];

foreach ($products as $product) {
  $build[$product->id()] = [
    '#theme' => 'product_teaser',
    '#product' => $product,
  ];
}
// Result: Library attached once at parent level
```

---

### Monitor Cache Hit Rates

```php
// In a custom service or hook
public function logCachePerformance() {
  $cache = \Drupal::cache('render');

  // Check if specific render cache exists
  $cid = implode(':', ['mymodule', 'widget', $id]);
  $cached = $cache->get($cid);

  if ($cached) {
    \Drupal::logger('mymodule')->info('Cache hit for @cid', ['@cid' => $cid]);
  }
  else {
    \Drupal::logger('mymodule')->info('Cache miss for @cid', ['@cid' => $cid]);
  }
}
```

**Analysis:**

- High cache miss rate -- Too many cache contexts, or keys not consistent
- No cache hits -- Missing cache keys, or max-age = 0

## Common Security Vulnerabilities

### Vulnerability: Cached Access Decisions

**VULNERABLE:**

```php
function mymodule_preprocess_node(&$variables) {
  $node = $variables['node'];

  // WRONG: Boolean access check
  if ($node->access('update')) {
    $variables['edit_link'] = Link::createFromRoute('Edit', 'entity.node.edit_form', ['node' => $node->id()]);
  }
}
// Result: If admin views node, edit link cached and shown to all users
```

**SECURE:**

```php
function mymodule_preprocess_node(&$variables) {
  $node = $variables['node'];
  $access_result = $node->access('update', NULL, TRUE);

  $variables['edit_link'] = [
    '#access' => $access_result,
    '#type' => 'link',
    '#title' => t('Edit'),
    '#url' => Url::fromRoute('entity.node.edit_form', ['node' => $node->id()]),
  ];

  \Drupal::service('renderer')->addCacheableDependency($variables, $access_result);
}
// Result: Proper cache contexts ensure edit link only shown to users with permission
```

---

### Vulnerability: Missing CSRF Protection

Render arrays don't provide CSRF protection -- use Form API for state-changing operations:

**WRONG:**

```php
// Link that deletes content (GET request, no CSRF protection)
$build['delete_link'] = [
  '#type' => 'link',
  '#title' => t('Delete'),
  '#url' => Url::fromRoute('mymodule.delete', ['id' => $id]),
];

// In controller
public function delete($id) {
  Entity::load($id)->delete();  // VULNERABLE: Any GET request can trigger
  return new RedirectResponse('/');
}
```

**RIGHT:**

```php
// Use confirm form (POST with CSRF token)
$build['delete_link'] = [
  '#type' => 'link',
  '#title' => t('Delete'),
  '#url' => Url::fromRoute('mymodule.delete_confirm', ['id' => $id]),
];

// In controller (confirm form)
public function deleteConfirm($id) {
  return $this->formBuilder()->getForm(
    '\Drupal\mymodule\Form\DeleteConfirmForm',
    $id
  );
}
```

## See Also

- [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) for caching details
- [Anti-Patterns & Common Mistakes](anti-patterns-common-mistakes.md) for what not to do
- Reference: [OWASP Drupal Security](https://owasp.org/www-project-drupal-security/)
