---
description: Avoid common pitfalls that cause bugs, performance issues, or security vulnerabilities in blocks
drupal_version: "11.x"
---

# Anti-Patterns & Common Mistakes

## When to Use

> Reference when reviewing block code or debugging unexpected behavior. Every pattern here has been shipped in production and caused real problems.

## Decision

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Using `\Drupal::service()` in blocks | Not testable, tight coupling, bypasses DI | Inject services via `ContainerFactoryPluginInterface` |
| `max-age = 0` for varying content | Kills performance, database hit every request | Use cache contexts to vary cache properly |
| Business logic in templates | Not testable, violates MVC, hard to maintain | Put logic in `build()` or preprocess |
| Returning HTML strings from `build()` | Not themeable, security risk (XSS), breaks render pipeline | Return render arrays with `#theme` or `#markup` (sanitized) |
| Using `echo`/`print` in block plugin | Output appears before page render, breaks layout | Return render arrays |
| Not checking access in custom rendering | Security hole, bypasses access control | Call `blockAccess()` or use entity access checks |
| Hardcoding entity IDs | Breaks across environments, fragile | Use UUIDs or entity queries |
| Creating content blocks for dynamic data | Database overhead, editor confusion | Use block plugins for logic-driven content |
| Creating block plugins for static content | Code changes required for edits, inflexible | Use content blocks for editor-managed content |
| Placing blocks in code when config works | Not site-builder friendly, requires deploys | Use Block config entities |
| Over-using `AccessResult::forbidden()` | Uncacheable, performance hit | Use `neutral()` or `allowedIf()` with contexts |
| Not merging cache metadata | Loses parent cache tags/contexts, incorrect caching | Use `Cache::mergeTags()`, `Cache::mergeContexts()` |
| Ignoring empty results | Renders empty wrapper with class/ID | Return `[]` when no content |
| Complex queries in `build()` without lazy builder | Slow page loads, defeats BigPipe | Use `#lazy_builder` for expensive operations |

## Pattern

**Anti-pattern: Static service calls**
```php
// WRONG
public function build() {
  $nodes = \Drupal::entityTypeManager()
    ->getStorage('node')
    ->loadByProperties(['type' => 'article']);
}

// RIGHT
public function __construct(..., EntityTypeManagerInterface $etm) {
  $this->entityTypeManager = $etm;
}
public function build() {
  $nodes = $this->entityTypeManager
    ->getStorage('node')
    ->loadByProperties(['type' => 'article']);
}
```

**Anti-pattern: max-age = 0**
```php
// WRONG - hits database every request
public function build() {
  $user = User::load(\Drupal::currentUser()->id());
  return ['#markup' => $user->getDisplayName(), '#cache' => ['max-age' => 0]];
}

// RIGHT - cache per user
public function build() {
  $user = User::load($this->currentUser->id());
  return ['#markup' => $user->getDisplayName(), '#cache' => ['contexts' => ['user']]];
}
```

**Anti-pattern: HTML in build()**
```php
// WRONG - not themeable, XSS risk
return ['#markup' => '<div class="my-block"><h2>' . $title . '</h2></div>'];

// RIGHT - themeable, safe
return ['#theme' => 'my_block', '#title' => $title]; // Auto-escaped in template
```

**Anti-pattern: Not handling empty**
```php
// WRONG - renders empty wrapper
public function build() {
  $items = $this->getItems();
  return ['#theme' => 'item_list', '#items' => $items];
}

// RIGHT - no wrapper when empty
public function build() {
  $items = $this->getItems();
  if (empty($items)) {
    return [];
  }
  return ['#theme' => 'item_list', '#items' => $items];
}
```

**Anti-pattern: Forgetting cache merge**
```php
// WRONG - loses parent cache metadata
public function getCacheTags() { return ['node:1']; }

// RIGHT - preserves parent tags
public function getCacheTags() {
  return Cache::mergeTags(parent::getCacheTags(), ['node:1']);
}
```

## Common Mistakes

- **Wrong**: "It works on my machine" without testing caching → **Right**: Works uncached, fails in production
- **Wrong**: Not profiling block performance → **Right**: 500ms query in block destroys page load time
- **Wrong**: Copying patterns from Drupal 7 → **Right**: D7 patterns don't apply; use D10+ APIs
- **Wrong**: Not reading core examples → **Right**: Core blocks demonstrate best practices
- **Wrong**: Skipping code review → **Right**: Blocks affect every page; errors expensive

## See Also

- [Best Practices](best-practices.md)
- [Security & Performance](security-performance.md)
- [Block Caching Strategies](block-caching.md)
- Reference: https://www.drupal.org/docs/develop/coding-standards
