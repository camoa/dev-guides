---
description: Salesforce performance — caching strategy, queue processing for high volume, API call optimization for push and pull
drupal_version: "11.x"
---

# Performance

## When to Use

> Optimize Salesforce sync performance when experiencing high API usage, slow entity saves, or large queue backlogs. The primary levers are: caching object metadata, async queue processing, and selective field/record queries.

## Decision

| Scenario | Strategy |
|---|---|
| High volume entity saves | Enable `async = TRUE` on all mappings |
| Need low latency sync | Use `async = FALSE` with retry on `PUSH_FAIL` |
| Large Salesforce objects | Use specific field lists, not all fields |
| Repeated schema inspection | Metadata is cached — do not disable caching |
| High pull frequency | Increase `pull_frequency` to rate-limit API calls |

## Pattern

**Cache keys and lifetimes:**
```
salesforce:objects          — object list (short_term_cache_lifetime, default 300s)
salesforce:object:[name]    — single object metadata (300s)
salesforce:versions         — API versions (long_term_cache_lifetime, default 86400s)
salesforce:record_types     — record types (300s)

Clear: drush cache:rebuild  OR via /admin/config/salesforce
```

**High-volume push configuration:**
```
async = TRUE on all mappings
standalone endpoints with custom scheduling (higher frequency than cron)
global_push_limit and push_limit tuned to API limits
Monitor: drush queue:list → salesforce_push
```

**Pull query optimization:**
```
Use specific field lists (never use wildcard)
Implement pull_trigger_date for incremental sync
Set pull_where_clause to limit records
Avoid subqueries in PULL_QUERY event unless necessary
```

**API call efficiency:**
- Batch queue processing vs real-time (`async = TRUE`)
- Use upsert when appropriate (one call vs two for create+update)
- Minimize field mappings — only map fields you actually need
- Use `pull_record_type_filter` to reduce pull volume for multi-RecordType objects

## Common Mistakes

- **Wrong**: Disabling caching to force fresh metadata on every API call → **Right**: The 300-second short-term cache is appropriate; cache miss on every call wastes API quota
- **Wrong**: Using `async = FALSE` for bulk import operations → **Right**: Always use `async = TRUE` for bulk operations; process the resulting queue via `drush sfpushq` in batch

## See Also

- [Queue Processing](queue-processing.md)
- [Pull Synchronization](pull-synchronization.md)
- [Configuration Management](configuration-management.md)
- [Troubleshooting](troubleshooting.md)
