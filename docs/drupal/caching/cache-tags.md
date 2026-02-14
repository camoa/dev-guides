---
description: Add cache tags to invalidate cached content on entity and config changes
---

# Cache Tags

## When to Use

When you need to invalidate cached content when specific data changes. Cache tags declare "this cached item depends on X" — when X changes, Drupal automatically invalidates all cache entries with that tag.

## Entity Cache Tags

Automatically added by entity system when entities are rendered or loaded.

| Entity type | Tag pattern | Example |
|---|---|---|
| Node | `node:{nid}` | `node:123` |
| User | `user:{uid}` | `user:456` |
| Taxonomy term | `taxonomy_term:{tid}` | `taxonomy_term:789` |
| Config entity | `config:{entity_type}:{id}` | `config:block:search` |
| Entity type list | `{entity_type}_list` | `node_list`, `user_list` |

```php
// Automatic when rendering entity
$node = Node::load(123);
$view = \Drupal::entityTypeManager()
  ->getViewBuilder('node')
  ->view($node);
// Tags automatically added: ['node:123', 'node_view', 'user:456']

// Manual tag addition
$build = [
  '#cache' => [
    'tags' => ['node:123'],  // Invalidates when node 123 changes
  ],
];
```

**Gotchas:**
- Entity view mode changes don't invalidate entity tags — add view mode to cache keys if varying: `['node_view', $view_mode, $nid]`
- List tags (`node_list`) invalidate when ANY node changes — use sparingly, prefer entity-specific tags
- Loading entity adds its tags automatically; you don't need to manually add them unless caching references

## Config Cache Tags

Invalidate when configuration changes.

| Config type | Tag pattern | Example |
|---|---|---|
| Simple config | `config:{name}` | `config:system.site` |
| Entity config | `config:{type}.{id}` | `config:node.type.article` |
| Module config | `config:{module}.settings` | `config:my_module.settings` |

```php
$build = [
  '#cache' => [
    'tags' => ['config:system.site'],  // Invalidates when site config changes
  ],
];

// Config entities automatically add their tags when loaded
$node_type = NodeType::load('article');
// Tags: ['config:node.type.article', 'config:node_type_list']
```

**Gotchas:**
- Config changes don't trigger cache rebuild until next request — expected behavior
- Overridden config (settings.php) doesn't invalidate config tags — config system doesn't know about overrides

## Custom Cache Tags

Developer-defined tags for non-entity data.

**Tag Format:** Freeform string, convention is `{module}:{type}:{identifier}`

```php
// Custom cache tag for API data
$build = [
  '#cache' => [
    'tags' => ['my_module:weather_data:portland'],
  ],
];

// Invalidate when weather data updates
\Drupal::service('cache_tags.invalidator')
  ->invalidateTags(['my_module:weather_data:portland']);
```

**Gotchas:**
- Custom tags never auto-invalidate — you must invalidate them programmatically
- No tag namespacing enforcement — use prefixes to avoid collisions (`my_module:*`)
- Tags are strings, not structured data — can't query "all tags matching pattern"

## View Cache Tags

Automatically added by Views when rendering.

| View element | Tag pattern | Example |
|---|---|---|
| View config | `config:views.view.{id}` | `config:views.view.frontpage` |
| View display | `{entity_type}_view` | `node_view`, `user_view` |
| Rendered entities | Individual entity tags | `node:123`, `node:456` |

```php
// Views automatically add comprehensive tags
$view = Views::getView('frontpage');
$view->execute();
// Tags include: config tags, entity list tags, individual entity tags
```

**Gotchas:**
- Views with relationships add tags from all joined entities — can create large tag sets
- Views cache plugins have separate cache configuration — don't confuse with render cache

## Common Mistakes

- Using entity list tags (`node_list`) instead of specific entity tags — Invalidates too frequently, cache never warms
- Forgetting to add tags when using entity data indirectly — Cache doesn't invalidate when source entity changes
- Creating too many unique tags — Cache tags table grows large; prefer reusable tags
- Not using `Cache::mergeTags()` when combining — Manual array merging doesn't deduplicate or optimize
- Invalidating tags synchronously in hot paths — Use queue or post-request processing for expensive invalidations

## See Also

- [Cache Invalidation Patterns](cache-invalidation-patterns.md) — How to invalidate tags
- [Custom Cache Tags](custom-cache-tags.md) — Creating custom tags
- Reference: [Cache tags documentation](https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags)
