## 13. Caching Configuration

### When to Use
When optimizing view performance by caching query results and rendered output.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Content changes frequently, precise invalidation | Tag-based | Auto-invalidates when content updates, always fresh |
| Content changes infrequently, predictable schedule | Time-based | Lower overhead, no tag tracking, predictable cache lifetime |
| Always fresh data, no caching | None | Admin views, personalized content, debugging |
| API responses with stale tolerance | Time-based | Reduce server load, acceptable staleness window |

### Cache Types

#### Tag-Based Cache
```yaml
cache:
  type: tag
  options: {}
```

- **Invalidation**: Automatic via cache tags (entity changes invalidate caches)
- **Max-age**: Permanent until invalidated
- **Best for**: Content-driven views, user-facing listings
- **Overhead**: Tag tracking and invalidation system

Reference: `core/modules/views/src/Plugin/views/cache/Tag.php`

#### Time-Based Cache
```yaml
cache:
  type: time
  options:
    results_lifespan: 3600  # Query results cache (seconds)
    results_lifespan_custom: 0  # Custom seconds if results_lifespan: custom
    output_lifespan: 3600  # Rendered output cache (seconds)
    output_lifespan_custom: 0  # Custom seconds if output_lifespan: custom
```

- **results_lifespan**: How long to cache raw query results
- **output_lifespan**: How long to cache rendered HTML
- **Values**: `0` (no cache), `60`, `300`, `1800`, `3600`, `21600`, `518400`, or `custom`
- **Invalidation**: Time expiration only

Reference: `core/modules/views/src/Plugin/views/cache/Time.php` lines 72-80

#### None (No Cache)
```yaml
cache:
  type: none
```

### Pattern
Time-based cache for semi-static content:

```yaml
cache:
  type: time
  options:
    results_lifespan: 3600  # 1 hour
    output_lifespan: 1800   # 30 minutes
```

Tag-based cache for dynamic content:

```yaml
cache:
  type: tag
```

Reference: `core/modules/node/config/optional/views.view.content.yml` line 336

### Two-Level Caching
Views caches both:
1. **Query results** (raw data from database)
2. **Rendered output** (HTML after theming)

Time-based cache allows different lifespans:
- **Longer results cache** → Database queries less frequent
- **Shorter output cache** → Theming changes appear faster

### Cache Metadata (Auto-Generated)
```yaml
cache_metadata:
  max-age: 0  # -1 = permanent, 0 = no cache, >0 = seconds
  contexts:
    - 'languages:language_interface'
    - 'url.query_args'
    - 'user.permissions'
  tags:
    - 'config:views.view.my_view'
```

Cache metadata is calculated automatically on view save based on display config, handlers, and dependencies.

Reference: `core/modules/views/src/Entity/View.php` lines 321-343

### Best Practices from Research

**Tag-based caching:**
- Most precise invalidation
- Auto-invalidates when related content changes
- Slightly higher overhead due to tag tracking

**Time-based caching:**
- Avoid excessive invalidations by not relying on entity list tags
- Good for views that tolerate staleness (reports, archives)
- Combine with smart lifespans: longer for results, shorter for output

**Combined strategy:**
- High-traffic pages → time-based (reduce server load)
- Admin interfaces → none (always current)
- Content listings → tag-based (auto-invalidate on edits)

Reference: [Drupal Views Caching Best Practices](https://www.qed42.com/insights/optimising-drupal-views-and-forms-with-caching)
Reference: [Pantheon Views Caching Guide](https://docs.pantheon.io/drupal-caching-views)

### Common Mistakes
- Tag cache on high-traffic pages with frequent edits → Cache invalidates too often; time-based may perform better
- Time cache with `results_lifespan: 0` and `output_lifespan > 0` → Output cache useless without query cache; both should be >0 or use tag cache
- Using cache `none` in production → Always cache user-facing views; debugging without cache is fine, production without is not
- Not understanding cache contexts → Caches separate by context (URL, user role, language); check `cache_metadata.contexts` to understand cache bins
- Time-based cache on personalized views → User-specific content needs per-user caching; consider contexts and max-age carefully

### See Also
- Section 31: Security & Performance — cache poisoning risks
- Reference: [Caching Overview](https://www.drupal.org/docs/7/managing-site-performance-and-scalability/caching-to-improve-performance/caching-overview)

