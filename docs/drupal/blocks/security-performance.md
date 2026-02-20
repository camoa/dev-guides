---
description: Ensure blocks don't introduce security vulnerabilities or performance bottlenecks
drupal_version: "11.x"
---

# Security & Performance

## When to Use

> Apply these patterns when blocks handle user input, load entities, or call external APIs. Security issues in blocks affect every page they appear on.

## Decision

**Security:**

| Risk | Mitigation | Why |
|------|------------|-----|
| XSS in block output | Use render arrays, never raw HTML; Twig auto-escapes | User input in raw HTML can inject scripts |
| Access bypass | Always implement `blockAccess()` with cache metadata | Don't rely only on visibility conditions |
| CSRF in forms | Use Form API, never manual forms | Drupal Form API has built-in CSRF protection |
| SQL injection | Use EntityQuery or query builders, never raw SQL | Parameterized queries prevent injection |
| Sensitive data in cache | Use `user` cache context for user-specific data | Shared cache shows wrong user's data |
| Unrestricted entity access | Use `->accessCheck(TRUE)` in queries | Bypassing access leaks private content |
| Hardcoded credentials | Never put API keys in code; use Key module or config | Code is often public (Git, staging sites) |

**Performance:**

| Issue | Solution | Why |
|-------|----------|-----|
| N+1 queries | Use `loadMultiple()`, eager load relationships | Each `load()` is a query; batch loading is one query |
| Expensive queries in build() | Use lazy builders or cache aggressively | Block build() runs on every page load |
| Missing cache contexts | Add contexts for varying content | Wrong content cached for wrong users |
| Too-broad cache tags | Tag with specific entities, not entity type | More precise invalidation = better hit rate |
| Large result sets | Paginate or limit results | Loading 1000 nodes crashes page, breaks memory |
| Synchronous API calls | Use Guzzle async or queue API | External API delays block entire page render |

## Pattern

**Security: Safe output**
```php
// WRONG - XSS vulnerability
return ['#markup' => '<h2>' . $_GET['title'] . '</h2>'];

// RIGHT - Auto-escaped via theme
$title = \Drupal::request()->query->get('title');
return ['#theme' => 'my_block', '#title' => $title];
```

**Security: Proper access checks**
```php
// WRONG - Exposes private content
$nodes = $this->entityTypeManager->getStorage('node')
  ->loadByProperties(['type' => 'private_content']);

// RIGHT - Respects entity access
$query = $storage->getQuery()
  ->condition('type', 'private_content')
  ->accessCheck(TRUE); // Applies view access
$nids = $query->execute();

protected function blockAccess(AccountInterface $account) {
  return AccessResult::allowedIfHasPermission($account, 'view private content')
    ->addCacheContexts(['user.permissions']);
}
```

**Performance: Lazy builder for expensive operations**
```php
// WRONG - Slow API call on every page
public function build() {
  $response = $client->get('https://api.example.com/data');
  return ['#markup' => json_decode($response->getBody())->message];
}

// RIGHT - Lazy builder + cache
public function build() {
  return [
    '#lazy_builder' => ['mymodule.lazy_builder:buildApiBlock', []],
    '#create_placeholder' => TRUE,
  ];
}
```

**Performance: Efficient entity loading**
```php
// WRONG - N+1 queries
foreach ($nids as $nid) {
  $node = Node::load($nid); // Query per loop iteration
  $items[] = $node->label();
}

// RIGHT - Single query
$nodes = Node::loadMultiple($nids); // One query for all
foreach ($nodes as $node) {
  $items[] = $node->label();
}
```

**Reference:** https://www.drupal.org/docs/security, https://www.drupal.org/docs/develop/drupal-apis/cache-api

## Common Mistakes

- **Wrong**: Trusting user input → **Right**: Always validate and sanitize
- **Wrong**: Forgetting `accessCheck(TRUE)` → **Right**: Exposes content users shouldn't see
- **Wrong**: Using `#markup` with user-provided data → **Right**: XSS vulnerability if not escaped
- **Wrong**: Long-running operations in `build()` → **Right**: Blocks entire page render
- **Wrong**: Not profiling blocks → **Right**: "Feels slow" is too late; use Webprofiler or Blackfire
- **Wrong**: Caching user-specific content without `user` context → **Right**: Shows User A's data to User B
- **Wrong**: Storing secrets in block configuration → **Right**: Configuration is exportable, visible in Git

## See Also

- [Block Caching Strategies](block-caching.md)
- [Best Practices](best-practices.md)
- [Anti-Patterns & Common Mistakes](anti-patterns.md)
- Reference: https://www.drupal.org/docs/security/writing-secure-code
- Reference: https://cheatsheetseries.owasp.org/cheatsheets/Drupal_Security_Cheat_Sheet.html
