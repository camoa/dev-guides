---
description: "Salesforce Drush commands reference — push queue, pull queue, mapping maintenance, token management"
tldr: "Use Drush commands for manual queue processing, debugging, maintenance operations, and resyncing data. All commands are namespaced under `salesforce:`, `salesforce_mapping:`, `salesforce_push:`, and `salesforce_pull:`."
drupal_version: "11.x"
---

# Drush Commands Reference

## When to Use

> Use Drush commands for manual queue processing, debugging, maintenance operations, and resyncing data. All commands are namespaced under `salesforce:`, `salesforce_mapping:`, `salesforce_push:`, and `salesforce_pull:`.

## Decision

| Task | Command family | Start with |
|---|---|---|
| Inspect the Salesforce org (objects, fields, record types) | `salesforce:` | `sflo`, `sfdf`, `sfdrt` |
| Read or write single records ad hoc | `salesforce:` | `sfro`, `sfco`, `sfqo`, `soql` |
| Diagnose or refresh authentication | `salesforce:` | `sflp`, `sfrt`, `sfrvk` |
| Move Drupal changes to Salesforce now | `salesforce_push:` | `sfpushq`, `sfrq`, `sfpu` |
| Bring Salesforce changes into Drupal now | `salesforce_pull:` | `sfpq`, `sfpf`, `sf-pull-reset` |
| Clean up stale mapped objects and revisions | `salesforce_mapping:` | `sfprune`, `sfpd`, `sfpsf`, `sfpall` |

All Salesforce drush commands are defined in the following locations:
- Base: `/web/modules/contrib/salesforce/src/Commands/SalesforceCommands.php`
- Mapping: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/Commands/SalesforceMappingCommands.php`
- Push: `/web/modules/contrib/salesforce/modules/salesforce_push/src/Commands/SalesforcePushCommands.php`
- Pull: `/web/modules/contrib/salesforce/modules/salesforce_pull/src/Commands/SalesforcePullCommands.php`

## Base Module Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `salesforce:rest-version` | `sfrv` | Display REST API version info |
| `salesforce:list-objects` | `sflo` | List available Salesforce objects |
| `salesforce:describe-fields` | `sfdo`, `sfdf` | Describe object fields |
| `salesforce:describe-metadata` | `sfdom` | Describe object metadata |
| `salesforce:describe-record-types` | `sfdrt` | Describe object record types |
| `salesforce:dump-object` | `sf-dump-object` | Dump raw describe response |
| `salesforce:list-resources` | `sflr` | List available API resources |
| `salesforce:read-object` | `sfro` | Read object by Salesforce ID |
| `salesforce:create-object` | `sfco` | Create a new Salesforce object |
| `salesforce:query-object` | `sfqo` | Query objects with WHERE/fields/limit |
| `salesforce:execute-query` | `sfeq`, `soql` | Execute raw SOQL query |
| `salesforce:list-providers` | `sflp` | List configured auth providers |
| `salesforce:refresh-token` | `sfrt` | Refresh authentication token |
| `salesforce:revoke-token` | `sfrvk` | Revoke authentication token |

## Mapping Module Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `salesforce_mapping:prune-revisions` | `sfprune` | Delete old mapped object revisions |
| `salesforce_mapping:purge-drupal` | `sfpd` | Purge mapped objects with missing Drupal entities |
| `salesforce_mapping:purge-salesforce` | `sfpsf` | Purge mapped objects with missing SF records |
| `sf:purge-mapping` | `sfpmap` | Purge mapped objects with missing mappings |
| `salesforce_mapping:purge-all` | `sfpall` | Run all purge operations |

## Push Module Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `salesforce_push:push-queue` | `sfpushq`, `sfpm` | Process push queue for one or all mappings |
| `salesforce_push:requeue` | `sfrq` | Requeue all mapped entities for push |
| `salesforce_push:push-unmapped` | `sfpu` | Push entities not yet linked to SF |

**Usage Examples:**
```bash
drush sfpushq                    # Process all push queues
drush sfpushq contact_mapping    # Process specific mapping
drush sfrq contact_mapping       # Requeue all entities for mapping
drush sfpu contact_mapping --count=100  # Push 100 unmapped entities
```

## Pull Module Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `salesforce_pull:pull-query` | `sfpq`, `sfiq` | Query and enqueue records for pull |
| `salesforce_pull:pull-file` | `sfpf`, `sfif` | Pull records from CSV file of SFIDs |
| `salesforce_pull:pull-reset` | `sf-pull-reset` | Reset pull timestamps for mapping |
| `salesforce_pull:pull-set` | `sf-pull-set` | Set specific pull timestamp |

**Usage Examples:**
```bash
drush sfpq                       # Pull all mappings
drush sfpq user_mapping          # Pull specific mapping
drush sfpq user --where="Email LIKE '%@example.com'"  # Pull with filter
drush sfpq --start="-1 hour"     # Pull records updated in last hour
drush sfpf /path/to/sfids.csv user_mapping  # Pull from CSV file
drush sf-pull-reset user_mapping # Reset pull timestamp (force re-pull)
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
