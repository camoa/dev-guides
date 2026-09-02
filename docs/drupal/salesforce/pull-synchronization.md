---
description: "Salesforce to Drupal pull sync — queue handler, SOQL query, event flow, pull trigger date, WHERE clause filtering"
tldr: "Use `salesforce_pull` when you need to import Salesforce object changes into Drupal. Use `pull_trigger_date` for incremental sync of large datasets."
drupal_version: "11.x"
---

# Pull Synchronization (Salesforce → Drupal)

## When to Use

> Use `salesforce_pull` when you need to import Salesforce object changes into Drupal. Use `pull_trigger_date` for incremental sync of large datasets. Use custom WHERE clauses for filtered or subset sync.

**Purpose:** Pull Salesforce object changes to Drupal

## Decision: Pull Strategy

| Pull Strategy | Use When |
|---|---|
| `pull_trigger_date` | Large datasets, incremental sync — tracks `SystemModstamp` or `LastModifiedDate` |
| Custom WHERE clause | Filtered sync, specific record subsets (e.g., active records only) |
| Record type filter | Multi-RecordType objects with different mappings |
| `pull_frequency` | Rate limiting — prevents excessive API calls between pull runs |

**Decision Point - Pull Strategy:**
- Use `pull_trigger_date` for: Incremental sync, large datasets
- Use custom WHERE clause for: Filtered sync, specific record subsets
- Use record type filter for: Multi-RecordType objects with different mappings

## Architecture

**Queue Handler:**
- Service: `salesforce_pull.queue_handler`
- Class: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/QueueHandler.php`
- Populates queue during cron based on updated records

**Pull Queue:**
- Queue name: `cron_salesforce_pull`
- Queue worker: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/Plugin/QueueWorker/PullWorker.php`
- Item class: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/PullQueueItem.php`

**Delete Handler:**
- Service: `salesforce_pull.delete_handler`
- Class: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/DeleteHandler.php`
- Tracks deleted Salesforce records

## Event Flow

1. Cron runs → Query Salesforce for updated records
2. `SalesforceEvents::PULL_QUERY` → Modify SOQL query
3. Queue items created
4. Queue worker processes items
5. `SalesforceEvents::PULL_PREPULL` → Pre-processing, veto opportunity
6. `SalesforceEvents::PULL_ENTITY_VALUE` → Modify field values
7. `SalesforceEvents::PULL_PRESAVE` → Final entity modifications
8. Entity saved → Standard entity hooks fire

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

## Pull Query Configuration

**Pull Trigger Date Field:**
- Mapping entity → `pull_trigger_date`
- Salesforce field to track updates (usually `SystemModstamp` or `LastModifiedDate`)
- Used in WHERE clause to fetch only updated records

**Pull WHERE Clause:**
- Mapping entity → `pull_where_clause`
- Additional SOQL WHERE conditions
- Example: `Status__c = 'Active' AND Country__c = 'US'`

**Pull Record Type Filter:**
- Mapping entity → `pull_record_type_filter`
- Array of RecordType developer names to filter
- Only pull records matching specified RecordTypes

**Pull Frequency:**
- Mapping entity → `pull_frequency`
- Minimum seconds between pull operations
- Prevents excessive API calls

## Drush Commands

- Location: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/Commands/SalesforcePullCommands.php`
- `drush sfpull` - Process pull queue

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
