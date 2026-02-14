---
description: "Essential for production deployments, high-traffic APIs, and mobile applications."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Performance Optimization

### When to Use

Essential for production deployments, high-traffic APIs, and mobile applications.

### Decision

| Optimization | Impact | Complexity | When to Apply |
|--------------|--------|------------|---------------|
| Enable caching | High | Low | All deployments |
| Use sparse fieldsets | High | Low | Mobile, large responses |
| Limit includes | Medium | Low | Always (selective) |
| Implement pagination | High | Low | All collections |
| CDN/reverse proxy | High | Medium | Production, high traffic |
| Disable unused resources | Low | Low | All deployments |
| Index filter fields | Medium | Low | Filtered collections |

### Pattern

**Enable Drupal caching:**
```php
// settings.php
$settings['cache']['bins']['dynamic_page_cache'] = 'cache.backend.database';
$settings['cache']['bins']['page'] = 'cache.backend.database';

// JSON:API responses are cached automatically
```

**Use sparse fieldsets:**
```bash
# Bad: Fetch all fields
GET /jsonapi/node/article

# Good: Fetch only needed fields
GET /jsonapi/node/article?fields[node--article]=title,created
```

**Result:** 70% smaller response, 40% faster processing.

**Limit includes:**
```bash
# Bad: Include all relationships
GET /jsonapi/node/article?include=uid,field_image,field_tags

# Good: Include only what's rendered
GET /jsonapi/node/article?include=uid&fields[user--user]=name
```

**Implement pagination:**
```bash
# Bad: Fetch unbounded collection
GET /jsonapi/node/article

# Good: Paginate with reasonable limit
GET /jsonapi/node/article?page[limit]=25
```

**CDN caching (Varnish example):**
```vcl
# In Varnish VCL
sub vcl_recv {
  # Cache JSON:API GET requests
  if (req.url ~ "^/jsonapi/" && req.method == "GET") {
    return (hash);
  }
}

sub vcl_backend_response {
  # Respect Cache-Control headers from Drupal
  if (bereq.url ~ "^/jsonapi/") {
    set beresp.ttl = 1h;
  }
}
```

**Index filter fields:**
```php
// In hook_update_N() or during field creation
$field_storage = FieldStorageConfig::loadByName('node', 'field_category');
$schema = $field_storage->getSchema();
$schema['indexes'] = ['value' => ['value']];
$field_storage->set('schema', $schema);
$field_storage->save();
```

**Disable unused resources:**
```yaml
# Via JSON:API Extras
# Reduces resource type discovery overhead
id: taxonomy_term--tags
disabled: true
```

### Metrics

**Before optimization:**
```
Response size: 450 KB
Response time: 1,200 ms
Database queries: 47
```

**After optimization:**
```
Sparse fieldsets: 180 KB (60% reduction)
Pagination: 600 ms (50% faster)
Database queries: 12 (75% reduction)
CDN hit: 15 ms (99% faster on cache hit)
```

### Common Mistakes

**Not leveraging Drupal's cache system:** Rebuilding responses for identical requests. WHY: JSON:API respects Drupal cache tags. Enable dynamic_page_cache.

**Fetching entire collections repeatedly:** Loading thousands of nodes on every request. WHY: Pagination exists for a reason. Always use `page[limit]`.

**Including relationships not displayed:** Adding `?include=field_tags` when tags aren't shown. WHY: Each include adds database joins and normalization overhead.

**Not using CDN for anonymous traffic:** Application server handles all requests. WHY: JSON:API responses are highly cacheable. Use Varnish, Cloudflare, or Fastly.

**Sorting by non-indexed fields:** Sorting by body text or long_text fields. WHY: Database can't efficiently sort without index. Sort by created, changed, or indexed fields.

**Not monitoring performance:** Assuming optimization worked without measuring. WHY: What gets measured gets improved. Use New Relic, Blackfire, or similar APM tools.

### See Also
- [Fetching Resources (GET)](fetching-resources.md)
- [Includes & Sparse Fieldsets](includes-sparse-fieldsets.md)
- [Sorting & Pagination](sorting-pagination.md)
- Drupal caching documentation: https://www.drupal.org/docs/drupal-apis/cache-api
