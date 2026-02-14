---
description: Critical security and performance considerations for production views.
drupal_version: "11.x"
---

## 31. Security & Performance

### When to Use
Critical security and performance considerations for production views.

### Security Best Practices

#### SQL Injection
**Risk**: Views is generally safe from SQL injection (uses parameterized queries), but custom filter plugins or query alterations can introduce vulnerabilities.

**Mitigation**:
- Never concatenate user input into SQL strings
- Use placeholders: `$query->where('field = :value', [':value' => $input])`
- Validate and sanitize all exposed filter input
- Contextual filters use placeholders by default — keep it that way

#### Access Bypass via disable_sql_rewrite
**Risk**: Setting `query.options.disable_sql_rewrite: true` completely bypasses node access grants.

**Mitigation**:
- **NEVER** use on user-facing views
- Only use on admin views with strict permission checks (`perm: 'administer nodes'`)
- Document WHY it's disabled in view description
- Audit all views with `disable_sql_rewrite: true` during security reviews

#### REST Export Exposure
**Risk**: Unauthenticated REST exports expose data to anyone, including scrapers and attackers.

**Mitigation**:
- Always set `auth: ['basic_auth']` or stronger authentication
- Set appropriate `access` permissions (not `none`)
- Rate limit REST endpoints (use contrib module or reverse proxy)
- Only expose necessary fields
- Consider CORS headers for API endpoints

Reference: [Drupal Caching Best Practices](https://www.droptica.com/best-practices-drupal-caching-and-how-deal-caching-issues/)

#### Exposed Filter Injection
**Risk**: Exposed filters accept user input. Malicious input could expose data or cause errors.

**Mitigation**:
- Use grouped filters instead of free-text when possible
- Set `operator_limit_selection: true` to restrict available operators
- Validate filter values in custom filter plugins
- Use entity validators on entity reference exposed filters

#### Contextual Filter Validation Bypass
**Risk**: Unvalidated contextual filters accept arbitrary input, potentially exposing hidden content.

**Mitigation**:
- Always set `specify_validation: true`
- Use `entity:node` validator with `access: true` for node ID arguments
- Set `fail: 'not found'` to return 404 on invalid input
- Never trust URL arguments without validation

### Performance Best Practices

#### Query Optimization

**Index filtered and sorted fields**:
```sql
CREATE INDEX idx_node_status_changed
ON node_field_data (status, changed);
```

Views queries benefit from indexes on:
- Fields used in filters
- Fields used in sorts
- Fields used in contextual filters

**Avoid SELECT ***:
- Use fields-based row style instead of entity rendering when possible
- Only add fields you actually display
- Entity row loads ALL entity fields — expensive for large entities

**Use EXPLAIN to analyze slow queries**:
```php
// Enable query logging
$view->query->addTag('debug');
```

Then check query log for slow views queries.

#### Relationship Performance
- Each relationship adds a JOIN — limit to 2-3 relationships per view
- Use `required: true` (INNER JOIN) when relationship always exists — faster than LEFT JOIN
- Consider denormalizing data instead of deep relationships

#### Pager Performance
- Full pager requires count query — expensive on large datasets
- Mini pager skips count query — faster for "Previous/Next" use cases
- Some pager with LIMIT is fastest — no pagination overhead

#### Caching Strategy
- **Tag-based**: Best for content-driven views, auto-invalidates on entity changes
- **Time-based**: Best for high-traffic semi-static content, avoids tag tracking overhead
- **None**: Only for development/debugging, never in production

**Cache contexts matter**:
```yaml
cache_metadata:
  contexts:
    - 'user.permissions'  # Separate cache per permission set
    - 'url.query_args'    # Separate cache per exposed filter combo
```

More contexts = more cache bins = more cache misses. Balance freshness vs performance.

Reference: [Optimizing Drupal Views Caching](https://www.qed42.com/insights/optimising-drupal-views-and-forms-with-caching)

#### Avoid N+1 Queries
**Problem**: Views query returns 50 nodes. Entity row renders each node, loading 50 sets of field data (51 queries total).

**Solution**:
- Use fields row instead of entity row when possible
- Preload entities in `hook_views_pre_render()` with entity type manager
- Enable render caching on entity view modes

### Performance Monitoring

**Enable Views query debugging**:
```php
// settings.php or settings.local.php
$config['views.settings']['ui']['show']['sql_query']['enabled'] = TRUE;
```

Shows executed SQL in Views preview.

**Measure view execution time**:
```php
$start = microtime(TRUE);
$view->execute();
$time = microtime(TRUE) - $start;
\Drupal::logger('performance')->info('View @view took @time seconds', [
  '@view' => $view->id(),
  '@time' => round($time, 3),
]);
```

**Use database query logging**:
```php
// settings.local.php
$databases['default']['default']['log_queries'] = TRUE;
```

Logs all queries — check for duplicate or inefficient queries.

### Common Performance Mistakes
- Not using cache at all → Every page request re-runs query
- Using tag cache on high-traffic views with frequent content changes → Cache invalidates constantly, no performance benefit
- Deep relationship chains (3+ levels) → Exponential JOIN complexity
- Exposed filters on unindexed fields → Full table scans on every filter change
- Entity row on large lists → Loads full entities when only need title + link

### See Also
- Section 13: Caching Configuration — cache strategies
- Section 14: Access Control — access security
- Section 16: Query Settings — query tuning
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/) for web security
