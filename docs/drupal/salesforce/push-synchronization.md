---
description: "Drupal to Salesforce push sync — queue architecture, event flow, async vs sync, upsert vs create/update"
tldr: "Use `salesforce_push` when you need to send Drupal entity changes to Salesforce. Use `async = TRUE` for production (queue-based, non-blocking)."
drupal_version: "11.x"
---

# Push Synchronization (Drupal → Salesforce)

## When to Use

> Use `salesforce_push` when you need to send Drupal entity changes to Salesforce. Use `async = TRUE` for production (queue-based, non-blocking). Use `async = FALSE` only for low-traffic, real-time requirements.

**Purpose:** Push Drupal entity changes to Salesforce

## Decision: Sync vs Async, Upsert vs Create/Update

| Situation | Choose | Why |
|---|---|---|
| High-traffic entities, production | `async = TRUE` | Non-blocking, queue processes via cron |
| Low-traffic, real-time needed | `async = FALSE` | Immediate sync during entity save |
| Salesforce has external ID field | `always_upsert = TRUE` | Handles create/update in one operation |
| No external ID on SF object | `always_upsert = FALSE` | Uses create for new, update for existing |

**Decision Point - Sync vs Async:**
- `async = FALSE`: Real-time push during entity save (blocking)
- `async = TRUE`: Queue-based push during cron (non-blocking, recommended)

**Decision Point - Upsert vs Create/Update:**
- `always_upsert = TRUE`: Always use upsert operation (requires external ID field)
- `always_upsert = FALSE`: Use create for new, update for existing
- Upsert key: Mapping entity → `key` field

## Architecture

**Queue System:**
- Service: `queue.salesforce_push`
- Class: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueue.php`
- Table: `salesforce_push_queue`
- Default limit: 10,000 items per cron run

**Queue Processor Plugin System:**
- Manager: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueueProcessorPluginManager.php`
- Default processor: `rest` plugin
- Custom processors: Extend `PushQueueProcessorInterface`

## Event Flow

1. Entity saved → `salesforce_push_entity_crud()` → Queue item created
2. Cron/standalone → Queue processor runs
3. `SalesforceEvents::PUSH_ALLOWED` → Veto opportunity
4. `SalesforceEvents::PUSH_MAPPING_OBJECT` → Modify mapped object
5. `SalesforceEvents::PUSH_PARAMS` → Modify push parameters
6. API call (create/update/upsert/delete)
7. `SalesforceEvents::PUSH_SUCCESS` or `SalesforceEvents::PUSH_FAIL`

```
Entity saved
  → salesforce_push_entity_crud()
  → Queue item created (salesforce_push_queue table)
  → Cron or standalone endpoint processes queue
  → SalesforceEvents::PUSH_ALLOWED    (veto here)
  → SalesforceEvents::PUSH_MAPPING_OBJECT
  → SalesforceEvents::PUSH_PARAMS     (modify fields here)
  → API call (create / update / upsert / delete)
  → SalesforceEvents::PUSH_SUCCESS or PUSH_FAIL
```

## Configuration

- Global push limit: `/admin/config/salesforce` → `global_push_limit`
- Per-mapping limits: Mapping entity → `push_limit`
- Retry attempts: Mapping entity → `push_retries`
- Push frequency: Mapping entity → `push_frequency`

## Drush Commands

- Location: `/web/modules/contrib/salesforce/modules/salesforce_push/src/Commands/SalesforcePushCommands.php`
- `drush sfpush` - Process push queue

## Common Mistakes

- **Wrong**: Relying on `async = FALSE` in production for entities saved frequently → **Right**: Use `async = TRUE` and process via cron or standalone endpoint
- **Wrong**: Ignoring `push_retries` — failed items accumulate indefinitely → **Right**: Set `push_retries` and monitor `salesforce_push_queue` for permanently failed items

## See Also

- [Pull Synchronization](pull-synchronization.md)
- [Queue Processing](queue-processing.md)
- [Event System](event-system.md)
- [Push Queue Operations](push-queue-operations.md)
- [Drush Commands](drush-commands.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueue.php`
