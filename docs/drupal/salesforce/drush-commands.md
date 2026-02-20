---
description: Salesforce Drush commands reference — push queue, pull queue, mapping maintenance, token management
drupal_version: "11.x"
---

# Drush Commands Reference

## When to Use

> Use Drush commands for manual queue processing, debugging, maintenance operations, and resyncing data. All commands are namespaced under `salesforce:`, `salesforce_mapping:`, `salesforce_push:`, and `salesforce_pull:`.

## Decision

**Base module commands:**

| Command | Alias | Use For |
|---|---|---|
| `salesforce:list-objects` | `sflo` | List available SF objects |
| `salesforce:describe-fields` | `sfdf` | Describe object fields |
| `salesforce:read-object` | `sfro` | Read record by SFID |
| `salesforce:query-object` | `sfqo` | Query with WHERE/fields/limit |
| `salesforce:execute-query` | `soql` | Execute raw SOQL |
| `salesforce:list-providers` | `sflp` | List auth providers |
| `salesforce:refresh-token` | `sfrt` | Refresh auth token |

**Push commands:**

| Command | Alias | Use For |
|---|---|---|
| `salesforce_push:push-queue` | `sfpushq` | Process push queue |
| `salesforce_push:requeue` | `sfrq` | Requeue all entities for push |
| `salesforce_push:push-unmapped` | `sfpu` | Push entities not yet in SF |

**Pull commands:**

| Command | Alias | Use For |
|---|---|---|
| `salesforce_pull:pull-query` | `sfpq` | Query and enqueue for pull |
| `salesforce_pull:pull-file` | `sfpf` | Pull from CSV of SFIDs |
| `salesforce_pull:pull-reset` | `sf-pull-reset` | Reset pull timestamps |
| `salesforce_pull:pull-set` | `sf-pull-set` | Set specific pull timestamp |

**Mapping maintenance:**

| Command | Alias | Use For |
|---|---|---|
| `salesforce_mapping:prune-revisions` | `sfprune` | Delete old mapped object revisions |
| `salesforce_mapping:purge-drupal` | `sfpd` | Purge mapped objects with missing Drupal entities |
| `salesforce_mapping:purge-salesforce` | `sfpsf` | Purge mapped objects with missing SF records |
| `salesforce_mapping:purge-all` | `sfpall` | Run all purge operations |

## Pattern

```bash
# Process all push queues
drush sfpushq

# Process specific mapping's push queue
drush sfpushq contact_mapping

# Requeue all entities for a mapping (force re-push)
drush sfrq contact_mapping

# Push 100 entities not yet linked to Salesforce
drush sfpu contact_mapping --count=100

# Pull all mappings
drush sfpq

# Pull specific mapping
drush sfpq user_mapping

# Pull with WHERE filter
drush sfpq user --where="Email LIKE '%@example.com'"

# Pull records updated in the last hour
drush sfpq --start="-1 hour"

# Pull from CSV file of SFIDs
drush sfpf /path/to/sfids.csv user_mapping

# Reset pull timestamp (forces re-pull of all records)
drush sf-pull-reset user_mapping
```

## Common Mistakes

- **Wrong**: Using `drush sf-pull-reset` in production without understanding it will re-pull all records → **Right**: Use only when you intend a full resync; it resets the timestamp so all records appear "updated"
- **Wrong**: Running `drush sfpall` (purge all) without backing up first → **Right**: `sfpall` deletes mapped objects with missing Drupal entities or SF records — run `sfpd` and `sfpsf` separately to review first

## See Also

- [Push Synchronization](push-synchronization.md)
- [Pull Synchronization](pull-synchronization.md)
- [Queue Processing](queue-processing.md)
- [Troubleshooting](troubleshooting.md)
- Reference: `/web/modules/contrib/salesforce/src/Commands/SalesforceCommands.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_push/src/Commands/SalesforcePushCommands.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/Commands/SalesforcePullCommands.php`
