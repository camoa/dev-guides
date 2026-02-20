---
description: Salesforce mapping admin UI — sync triggers, field direction, queue options, UI vs code decision
drupal_version: "11.x"
---

# Mapping UI and Sync Triggers

## When to Use

> Use the mapping UI for initial setup, simple mappings, and site builder workflows. Use code/config for complex mappings, multi-site deployments, and version-controlled configuration.

## Decision

| Sync Trigger | Direction | When It Fires |
|---|---|---|
| `push_create` | Drupal → SF | Drupal entity created |
| `push_update` | Drupal → SF | Drupal entity updated |
| `push_delete` | Drupal → SF | Drupal entity deleted |
| `pull_create` | SF → Drupal | Salesforce record created |
| `pull_update` | SF → Drupal | Salesforce record updated |
| `pull_delete` | SF → Drupal | Salesforce record deleted |

| Field Direction Constant | Value | Meaning |
|---|---|---|
| `SALESFORCE_MAPPING_DIRECTION_DRUPAL_SF` | `drupal_sf` | Push only |
| `SALESFORCE_MAPPING_DIRECTION_SF_DRUPAL` | `sf_drupal` | Pull only |
| `SALESFORCE_MAPPING_DIRECTION_SYNC` | `sync` | Bidirectional |

**Queue processing options:**
- `async = TRUE` — Queue-based push (recommended for production)
- `async = FALSE` — Real-time push during entity save (blocking)
- `push_standalone` — Use standalone endpoint for push
- `pull_standalone` — Use standalone endpoint for pull

## Pattern

**Admin routes:**
- `/admin/structure/salesforce` — Mapping overview
- `/admin/structure/salesforce/mapping/add` — Create mapping
- `/admin/structure/salesforce/mapping/{mapping}/edit` — Edit mapping
- `/admin/structure/salesforce/mapping/{mapping}/fields` — Field config

**Config export path:** `config/sync/salesforce_mapping.salesforce_mapping.[mapping_id].yml`

## Common Mistakes

- **Wrong**: Enabling both `push_create` and `pull_create` for the same bundle without deduplication logic → **Right**: Use the `PUSH_ALLOWED` or `PULL_PREPULL` events to prevent infinite sync loops
- **Wrong**: Setting `async = FALSE` on high-traffic entities → **Right**: Use `async = TRUE` to avoid blocking entity saves

## See Also

- [Mapping Framework](mapping-framework.md)
- [Push Synchronization](push-synchronization.md)
- [Pull Synchronization](pull-synchronization.md)
- [Queue Processing](queue-processing.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping_ui/src/Form/SalesforceMappingFieldsForm.php`
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappingConstants.php`
