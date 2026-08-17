---
description: "Importing CSV and external data into custom field columns via Feeds module -- one Feeds target dispatching to 23 per-column-type FeedsType plugins."
tldr: "You need to import CSV or other data sources into custom field columns via the Feeds module. A single Feeds target delegates per sub-field to 23 FeedsType plugins, one per supported column type. Target format is field_name:column_name, not double-underscore."
drupal_version: "11.x"
---

# Feeds Import Integration

## When to Use

You need to import CSV or other data sources into custom field columns via the Feeds module.

## Pattern

The module exposes a **single Feeds target** (`src/Feeds/Target/CustomField.php`) which delegates per sub-field to **23 FeedsType plugins** (`#[CustomFieldFeedsType]` in `src/Plugin/CustomField/FeedsType/`, discovered by `plugin.manager.custom_field_feeds`) -- one per supported column type. That is where a new source-value handler goes if you need one.

**Import mapping** (via Feeds UI):

1. Create Feed Type
2. Map source columns to custom field targets
3. Target format: `field_name:column_name`

**Example CSV**:

```csv
title,address_street,address_city,address_state,address_zip
"Node 1","123 Main St","Anytown","CA","12345"
```

**Feeds mapping**:

```yaml
mappings:
  - target: title
    map:
      value: title
  - target: field_address:street
    map:
      value: address_street
  - target: field_address:city
    map:
      value: address_city
  - target: field_address:state
    map:
      value: address_state
  - target: field_address:zip
    map:
      value: address_zip
```

## Common Mistakes

- **Wrong target format** -- Must be `field_name:column_name`, not `field_name__column_name`
- **Not validating data types** -- CSV imports as strings; Feeds doesn't auto-convert to integer/decimal
- **Forgetting required fields** -- If custom field or sub-field required, CSV must have data
- **Large imports without batching** -- Use Feeds batch processing for >1000 rows

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FeedsType/` -- the 23 per-column-type target plugins
- Reference: `/modules/contrib/custom_field/src/Feeds/Target/CustomField.php` -- the single Feeds target that dispatches to them
- Feeds module: https://www.drupal.org/project/feeds
