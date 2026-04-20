---
description: Facets value transformation processors — translate_entity, list_item, boolean_item, date_item, granularity_item, uid_to_username
tldr: "Use this guide when facet raw values need to be converted to human-readable labels — entity IDs to names, boolean values to Yes/No, dates to formatted strings."
drupal_version: "11.x"
---

# Value Transformation Processors

## When to Use

> Use this guide when facet raw values need to be converted to human-readable labels — entity IDs to names, boolean values to Yes/No, dates to formatted strings.

## Decision

| ID | Title | Stage:Weight | Purpose | When to Enable |
|---|---|---|---|---|
| `translate_entity` | Transform entity ID to label | build:5 | Convert taxonomy term IDs to names, node IDs to titles | Always for entity reference fields |
| `translate_entity_aggregated_fields` | Transform aggregated field IDs | build:5 | Handle aggregated field labels | When using aggregated fields |
| `uid_to_username_callback` | Transform UID to user name | build:5 | Convert user IDs to display names | For user reference facets |
| `list_item` | List item label | build:5 | Display labels for list_string/list_integer fields | For list fields |
| `boolean_item` | Boolean item label | build:35 | Show On/Off or Yes/No instead of 1/0 | For boolean fields |
| `date_item` | Date item processor | build:35 | Format dates with configurable granularity | For date facets |
| `granularity_item` | Granularity item processor | build:35 | Group numbers into ranges (e.g., 0-10, 10-20) | For numeric grouping |

## Pattern

**`translate_entity`** — The most commonly needed processor. Without it, taxonomy facets show term IDs instead of names.

Supports: Taxonomy terms, nodes, users, any entity reference field.

Limitation: Requires entity loading. For large result sets, this can be slow. Consider indexing the entity label directly in Search API and using `list_item` instead.

**`boolean_item` configuration:**
```
On label: "Yes" (or "Published", "Active", etc.)
Off label: "No" (or "Unpublished", "Inactive", etc.)
```

**`date_item` configuration:**

| Setting | Options |
|---|---|
| Date display | year, month, day, hour, minute, second |
| Granularity | Controls grouping level |
| Date format | PHP date format string |

## Common Mistakes

- **Wrong**: Not enabling `translate_entity` on taxonomy/entity reference facets → **Right**: Without it, taxonomy facets show IDs like "42" instead of "Technology". This is the #1 new-user issue.
- **Wrong**: Using `translate_entity` on text or list fields → **Right**: `translate_entity` only works for entity reference fields. For list fields, use `list_item` instead.
- **Wrong**: Using `translate_entity` on high-traffic sites with many items → **Right**: Loading hundreds of entities per request is expensive. Index the label and avoid entity loading.

## See Also

- [Processing Pipeline](processing-pipeline.md) — where transformations fit
- [Result Filtering Processors](result-filtering-processors.md) — filtering after transformation
- Reference: `web/modules/contrib/facets/src/Plugin/facets/processor/`
