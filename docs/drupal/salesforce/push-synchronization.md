---
description: Drupal to Salesforce push sync — queue architecture, event flow, async vs sync, upsert vs create/update
drupal_version: "11.x"
---

# Push Synchronization (Drupal → Salesforce)

## When to Use

> Use `salesforce_push` when you need to send Drupal entity changes to Salesforce. Use `async = TRUE` for production (queue-based, non-blocking). Use `async = FALSE` only for low-traffic, real-time requirements.

## Decision

| Situation | Choose | Why |
|---|---|---|
| High-traffic entities, production | `async = TRUE` | Non-blocking, queue processes via cron |
| Low-traffic, real-time needed | `async = FALSE` | Immediate sync during entity save |
| Salesforce has external ID field | `always_upsert = TRUE` | Handles create/update in one operation |
| No external ID on SF object | `always_upsert = FALSE` | Uses create for new, update for existing |

## Pattern

**Push event flow:**
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

**Configuration:**
- Global push limit: `salesforce.settings:global_push_limit` (default: 10,000/cron run)
- Per-mapping limit: mapping entity `push_limit`
- Retry attempts: mapping entity `push_retries`
- Push frequency: mapping entity `push_frequency`

**Services:**
- Queue service: `queue.salesforce_push`
- Queue class: `/web/modules/contrib/salesforce/modules/salesforce_push/src/PushQueue.php`
- Queue table: `salesforce_push_queue`

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
