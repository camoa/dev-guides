---
description: Importing CSV and external data into custom field columns via Feeds module with 28 target handlers and mapping configuration.
---

# Feeds Import Integration

## When to Use

You need to import CSV or other data sources into custom field columns via the Feeds module.

## Pattern

**28 target handlers** for mapping CSV columns to custom field sub-fields.

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

- Reference: `/modules/contrib/custom_field/src/Feeds/Target/`
- Feeds module: https://www.drupal.org/project/feeds
