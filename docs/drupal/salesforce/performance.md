---
description: "Salesforce performance — caching strategy, queue processing for high volume, API call optimization for push and pull"
tldr: "Optimize Salesforce sync performance when experiencing high API usage, slow entity saves, or large queue backlogs. The primary levers are: caching object metadata, async queue processing, and selective field/record queries."
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

## Caching

**Object Metadata:**
- Cache: `salesforce:objects`, `salesforce:object:[name]`
- Lifetime: `short_term_cache_lifetime` (default: 300s)
- Clear: `drush cache:rebuild` or Salesforce admin UI

**API Versions:**
- Cache: `salesforce:versions`
- Lifetime: `long_term_cache_lifetime` (default: 86400s)

**Record Types:**
- Cache: `salesforce:record_types`
- Lifetime: `short_term_cache_lifetime`

## Queue Processing Strategy

**High Volume Sites:**
- Enable `async = TRUE` on all mappings
- Use standalone endpoints with custom scheduling
- Increase `global_push_limit` and `push_limit`
- Monitor queue size and API limits

**Low Latency Requirements:**
- Use `async = FALSE` for critical mappings
- Accept blocking during entity save
- Implement retry logic via `PUSH_FAIL` event

## API Call Optimization

**Pull Queries:**
- Use specific field lists (not SELECT *)
- Implement WHERE clauses to limit records
- Use pull_trigger_date for incremental sync
- Avoid unnecessary subqueries

**Push Operations:**
- Batch queue processing vs real-time
- Use upsert when appropriate
- Minimize field mappings to required fields

Also worth applying: use `pull_record_type_filter` to reduce pull volume for multi-RecordType objects.

## Common Mistakes

- **Wrong**: Disabling caching to force fresh metadata on every API call → **Right**: The 300-second short-term cache is appropriate; cache miss on every call wastes API quota
- **Wrong**: Using `async = FALSE` for bulk import operations → **Right**: Always use `async = TRUE` for bulk operations; process the resulting queue via `drush sfpushq` in batch

## See Also

- [Queue Processing](queue-processing.md)
- [Pull Synchronization](pull-synchronization.md)
- [Configuration Management](configuration-management.md)
- [Troubleshooting](troubleshooting.md)
