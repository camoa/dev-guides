---
description: Salesforce to Drupal pull sync — queue handler, SOQL query, event flow, pull trigger date, WHERE clause filtering
drupal_version: "11.x"
---

# Pull Synchronization (Salesforce → Drupal)

## When to Use

> Use `salesforce_pull` when you need to import Salesforce object changes into Drupal. Use `pull_trigger_date` for incremental sync of large datasets. Use custom WHERE clauses for filtered or subset sync.

## Decision

| Pull Strategy | Use When |
|---|---|
| `pull_trigger_date` | Large datasets, incremental sync — tracks `SystemModstamp` or `LastModifiedDate` |
| Custom WHERE clause | Filtered sync, specific record subsets (e.g., active records only) |
| Record type filter | Multi-RecordType objects with different mappings |
| `pull_frequency` | Rate limiting — prevents excessive API calls between pull runs |

## Pattern

**Pull event flow:**
```
Cron runs
  → Query Salesforce for updated records (SOQL)
  → SalesforceEvents::PULL_QUERY     (modify query here)
  → Queue items created (cron_salesforce_pull)
  → Queue worker processes items
  → SalesforceEvents::PULL_PREPULL   (veto/pre-process here)
  → SalesforceEvents::PULL_ENTITY_VALUE (modify field values)
  → SalesforceEvents::PULL_PRESAVE   (final entity modifications)
  → Entity saved → standard entity hooks fire
```

**Key configuration fields on mapping entity:**
- `pull_trigger_date` — Salesforce field to track updates
- `pull_where_clause` — Additional SOQL WHERE conditions
  - Example: `Status__c = 'Active' AND Country__c = 'US'`
- `pull_record_type_filter` — Array of RecordType developer names
- `pull_frequency` — Minimum seconds between pulls

**Services:**
- Queue handler: `salesforce_pull.queue_handler`
- Delete handler: `salesforce_pull.delete_handler`
- Queue worker: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/Plugin/QueueWorker/PullWorker.php`

## Common Mistakes

- **Wrong**: Not setting `pull_trigger_date` for large objects — every cron run queries all records → **Right**: Always set `pull_trigger_date` (typically `SystemModstamp`) to enable incremental sync
- **Wrong**: Vetoing pull in `PULL_PRESAVE` after entity relationships have been set up → **Right**: Veto in `PULL_PREPULL` before any processing begins

## See Also

- [Push Synchronization](push-synchronization.md)
- [Event System](event-system.md)
- [SOQL Query Builder](soql-query-builder.md)
- [Drush Commands](drush-commands.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/QueueHandler.php`
- Docs: https://www.drupal.org/docs/contributed-modules/salesforce-suite/push-and-pull
