---
description: "BUILD-stage processors that convert raw facet values to human-readable labels — entities, booleans, dates, list fields"
tldr: "Use this guide when facet raw values need conversion to labels — entity IDs to names, booleans to Yes/No, dates to formatted strings. translate_entity is the most commonly needed processor."
drupal_version: "11.x"
---

# Value Transformation Processors

## When to Use

> When facet raw values need to be converted to human-readable labels — entity IDs to names, boolean values to Yes/No, dates to formatted strings.

## Decision: Transformation Processors

| ID | Title | Stage:Weight | Purpose | When to Enable |
|---|---|---|---|---|
| `translate_entity` | Transform entity ID to label | build:5 | Convert taxonomy term IDs to names, node IDs to titles | Always for entity reference fields |
| `translate_entity_aggregated_fields` | Transform aggregated field IDs | build:5 | Handle aggregated field labels | When using aggregated fields |
| `uid_to_username_callback` | Transform UID to user name | build:5 | Convert user IDs to display names | For user reference facets |
| `list_item` | List item label | build:5 | Display labels for list_string/list_integer fields | For list fields |
| `boolean_item` | Boolean item label | build:35 | Show On/Off or Yes/No instead of 1/0 | For boolean fields |
| `date_item` | Date item processor | build:35 | Format dates with configurable granularity | For date facets |
| `granularity_item` | Granularity item processor | build:35 | Group numbers into ranges (e.g., 0-10, 10-20) | For numeric grouping |

## Pattern: translate_entity

This is the most commonly needed processor. Without it, taxonomy facets show term IDs instead of names.

**Supports:** Taxonomy terms, nodes, users, any entity reference field.

**Limitation:** Requires entity loading. For large result sets, this can be slow. Consider indexing the entity label directly in Search API and using `list_item` instead.

## Pattern: boolean_item Configuration

```
On label: "Yes" (or "Published", "Active", etc.)
Off label: "No" (or "Unpublished", "Inactive", etc.)
```

## Pattern: date_item Configuration

| Setting | Options |
|---|---|
| Date display | year, month, day, hour, minute, second |
| Granularity | Controls grouping level |
| Date format | PHP date format string |

## Common Mistakes

- **Forgetting translate_entity** — Without it, taxonomy facets show IDs like "42" instead of "Technology". This is the #1 new-user issue.
- **translate_entity on text fields** — Only works for entity reference fields. For list fields, use `list_item` instead.
- **Performance with translate_entity** — Loading hundreds of entities per request is expensive. For high-traffic sites, index the label and avoid entity loading.

## See Also

- [Processing Pipeline](processing-pipeline.md) — where transformations fit
- [Result Filtering Processors](result-filtering-processors.md) — filtering after transformation
- Reference: `src/Plugin/facets/processor/`
