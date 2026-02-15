---
description: Querying, filtering, sorting, and displaying custom field data in Views with custom field, date, and entity reference plugins.
---

# Views Integration

## When to Use

You need to query, filter, sort, or display custom field data in Views.

## Pattern

**Field plugin** (`CustomField`) -- displays custom field columns in Views:

```yaml
# In view display
fields:
  field_address:
    id: field_address
    table: node__field_address
    field: field_address
    plugin_id: custom_field
    settings:
      # Select which sub-fields to display
      columns:
        street: street
        city: city
        state: state
```

**Filter plugins**:

- `CustomFieldDate` -- filter by datetime/daterange columns
- `CustomFieldEntityReference` -- filter by entity reference columns

**Sort plugin** (`CustomFieldDate`) -- sort by datetime columns

**Date argument plugins** (7 total):

- `CustomFieldFullDate` -- full date (CCYYMMDD)
- `CustomFieldYearDate` -- year (CCYY)
- `CustomFieldYearMonthDate` -- year + month (CCYYMM)
- `CustomFieldMonthDate` -- month (MM)
- `CustomFieldWeekDate` -- week (WW)
- `CustomFieldDayDate` -- day (DD)

## Decision

| If you need... | Use... | Notes |
|---|---|---|
| Display custom field columns | CustomField field plugin | Choose which columns to show |
| Filter by date range | CustomFieldDate filter | Supports all datetime column types |
| Filter by referenced entity | CustomFieldEntityReference filter | Autocomplete or select widget |
| Sort by date column | CustomFieldDate sort | Ascending/descending |
| Date-based contextual filter | Date argument plugins | For date-based archives |

## Common Mistakes

- **Querying with entity query instead of Views** -- Views integration built-in; use it for performance
- **Not selecting columns in field settings** -- By default all columns display; select only needed ones
- **Forgetting to expose filters** -- Custom field filters work like core fields; expose for user filtering
- **Complex joins on sub-fields** -- All columns in same table; no joins needed unlike Paragraphs

## See Also

- Reference: [Entity Query custom fields](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field/entity-query-custom-fields)
- Reference: `/modules/contrib/custom_field/src/Plugin/views/field/CustomField.php`
