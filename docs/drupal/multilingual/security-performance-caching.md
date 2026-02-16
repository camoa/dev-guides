---
description: Drupal multilingual security, performance, and caching — access control, cache contexts, CDN configuration, database optimization
---

# Security, Performance & Caching

### When to Use
When optimizing multilingual site performance, securing translation access, or debugging cache issues.

### Decision: Security Measures

| Security concern | Mitigation | Implementation |
|---|---|---|
| Unauthorized translation | Permission checks | "translate ENTITY_TYPE" permission |
| XSS via translation | Never translate user input | Use `@placeholder`, not `!placeholder` |
| Privilege escalation | Check source content access | Verify `access('view')` before allowing translation |
| Translation spam | Moderation workflow | Require review before publishing translations |

### Pattern: Translation Access Control

**Permissions**:
- `translate any entity` — translate all entities of type
- `translate editable entities` — only entities user can edit
- `translate $entity_type` — per entity type (node, term, etc.)

**Check access before translation**:

```php
$node = Node::load(1);
$account = \Drupal::currentUser();

// Check if user can translate to Spanish
if ($node->access('view', $account) && $node->access('update', $account)) {
  if ($node->hasTranslation('es')) {
    $spanish = $node->getTranslation('es');
    if ($spanish->access('update', $account)) {
      // User can edit Spanish translation
    }
  }
  else {
    // Check if user can create translation
    $handler = \Drupal::service('content_translation.manager')
      ->getTranslationHandler($node->getEntityTypeId());
    if ($handler->getTranslationAccess($node, 'create')->isAllowed()) {
      // User can create Spanish translation
    }
  }
}
```

**Security best practices**:
- Require view access on source content before allowing translation
- Check update access per language
- Log translation changes for audit trail
- Use CSRF tokens on translation forms
- Validate langcode parameter input (prevent injection)

### Pattern: Cache Contexts for Language

**Cache contexts**:
- `languages:language_interface` — vary by UI language
- `languages:language_content` — vary by content language
- `languages:language_url` — vary by URL language
- `url.path` — vary by path (includes language prefix)

**When to use each**:

```php
// Interface language — for UI elements
$block = [
  '#markup' => $this->t('Welcome!'),
  '#cache' => ['contexts' => ['languages:language_interface']],
];

// Content language — for entity displays
$node_display = [
  '#theme' => 'node',
  '#node' => $node,
  '#cache' => ['contexts' => ['languages:language_content']],
];

// URL language — when using path-based routing
$menu = [
  '#theme' => 'menu',
  '#menu_name' => 'main',
  '#cache' => ['contexts' => ['languages:language_url', 'url.path']],
];
```

**Default cache contexts**:
- Drupal automatically adds `languages:language_interface` to most render arrays
- Views add language contexts automatically
- Custom render arrays may need explicit contexts

### Pattern: Performance Optimization

**Field translatability impact**:
- Translatable fields store values per language (higher storage)
- Non-translatable fields store once (shared across translations)
- Only mark fields translatable if they need different values per language

**Query optimization**:

```php
// SLOW — loads all translations then filters in PHP
$nodes = Node::loadMultiple($nids);
$spanish_nodes = [];
foreach ($nodes as $node) {
  if ($node->hasTranslation('es')) {
    $spanish_nodes[] = $node->getTranslation('es');
  }
}

// FAST — filter in database
$query = \Drupal::entityQuery('node')
  ->condition('nid', $nids, 'IN')
  ->condition('langcode', 'es')
  ->accessCheck(TRUE);
$spanish_nids = $query->execute();
$spanish_nodes = Node::loadMultiple($spanish_nids);
```

**Translation job batching**:
- Use Batch API for bulk translation operations
- Process translations in chunks (e.g., 50 nodes per batch)
- Avoid loading all entities into memory at once

### Pattern: CDN Configuration

**Varnish/CDN cache keys** for path prefix negotiation:

```vcl
# Vary cache by URL path (includes /es/, /fr/ prefix)
sub vcl_hash {
  hash_data(req.url);
  hash_data(req.http.host);
  return (lookup);
}
```

**For domain negotiation**:

```vcl
# Vary cache by domain (en.example.com vs es.example.com)
sub vcl_hash {
  hash_data(req.http.host);
  hash_data(req.url);
  return (lookup);
}
```

**For browser negotiation** (not recommended for CDN):

```vcl
# Vary cache by Accept-Language header
sub vcl_hash {
  hash_data(req.http.accept-language);
  hash_data(req.url);
  return (lookup);
}
# Warning: too many cache variations, poor hit rate
```

### Pattern: Database Performance

**Translation tables**:
- `node_field_data` — node translations (title, status, etc.)
- `node__body` — body field translations
- `taxonomy_term_field_data` — term translations
- Each translatable field has `langcode` column

**Index optimization**:

```sql
-- Composite indexes for language queries
CREATE INDEX idx_langcode_status ON node_field_data (langcode, status);
CREATE INDEX idx_langcode_type ON node_field_data (langcode, type);
```

**Query performance**:

```php
// Good — uses index on langcode + status
$query = \Drupal::entityQuery('node')
  ->condition('langcode', 'es')
  ->condition('status', 1)
  ->accessCheck(TRUE);

// Bad — no index on title alone
$query = \Drupal::entityQuery('node')
  ->condition('title', 'Something')
  ->accessCheck(TRUE);
```

### Common Mistakes

- **Missing language cache context** → Cached in one language, served to all. Always include language contexts for translatable content
- **Translating in loops without batching** → Creating 1000 translations in single request causes timeout. Use Batch API
- **Not configuring CDN for language prefixes** → CDN caches `/about` and serves to `/es/about` users. Configure cache keys correctly
- **Using browser negotiation with aggressive caching** → Too many cache variations (one per Accept-Language value). Prefer URL negotiation
- **Forgetting access checks in translation queries** → `accessCheck(FALSE)` bypasses permissions. Always use `accessCheck(TRUE)` unless specific reason

### See Also
- → [Language Negotiation](language-negotiation.md) — URL vs browser vs session
- → [Best Practices & Patterns](best-practices.md) — cache contexts
- → [Anti-Patterns & Common Mistakes](anti-patterns.md) — security issues
- Reference: https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-contexts
- Reference: https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Cache!Context!LanguagesCacheContext.php/class/LanguagesCacheContext/11.x
