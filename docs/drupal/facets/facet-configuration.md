---
description: Facet entity configuration keys — field identifier, widget, query operator, processors, hierarchy settings, and programmatic creation
tldr: "Use this guide when creating or configuring a facet entity — selecting the source, field, widget, operators, and processors."
drupal_version: "11.x"
---

# Facet Configuration

## When to Use

> Use this guide when creating or configuring a facet entity — selecting the source, field, widget, operators, and processors.

## Decision

**AND vs OR operator:**

| Operator | Behavior | Use Case |
|---|---|---|
| **OR** (default) | Selecting multiple values expands results (union) | "Show red OR blue items" |
| **AND** | Selecting multiple values narrows results (intersection) | "Show items that are BOTH red AND blue" |

OR is the most common choice. AND is useful when items can have multiple values for the same field (e.g., tags).

**Facet entity configuration keys:**

| Key | Type | Default | Purpose |
|---|---|---|---|
| `id` | string | — | Machine name |
| `name` | string | — | Human-readable label |
| `url_alias` | string | — | URL parameter name (e.g., 'color') |
| `facet_source_id` | string | — | Which search source |
| `field_identifier` | string | — | Search API field to facet on |
| `widget` | mapping | links | Display widget (type + config) |
| `query_operator` | string | 'or' | 'and' or 'or' for multi-value |
| `query_type` | string | auto-detected | Query type plugin ID |
| `hard_limit` | int | 0 | Max items to show (0 = unlimited) |
| `min_count` | int | 1 | Minimum result count to display item |
| `exclude` | bool | FALSE | Exclude instead of include matches |
| `use_hierarchy` | bool | FALSE | Enable hierarchical display |
| `keep_hierarchy_parents_active` | bool | FALSE | Keep parents selected |
| `expand_hierarchy` | bool | FALSE | Always expand all levels |
| `show_title` | bool | TRUE | Display facet title in block |
| `show_only_one_result` | bool | FALSE | Hide if only 1 result |

## Pattern

```php
use Drupal\facets\Entity\Facet;

$facet = Facet::create([
  'id' => 'category',
  'name' => 'Category',
  'url_alias' => 'category',
  'facet_source_id' => 'search_api:views_page__search__page_1',
  'field_identifier' => 'field_category',
  'widget' => [
    'type' => 'links',
    'config' => [
      'soft_limit' => 0,
      'show_reset_link' => TRUE,
      'reset_text' => 'Show all',
    ],
  ],
  'query_operator' => 'or',
  'processor_configs' => [
    'url_processor_handler' => ['weights' => ['pre_query' => -10, 'build' => -10]],
    'translate_entity' => ['weights' => ['build' => 5]],
    'count_widget_order' => ['weights' => ['sort' => 30], 'settings' => ['sort' => 'DESC']],
    'display_value_widget_order' => ['weights' => ['sort' => 40], 'settings' => ['sort' => 'ASC']],
    'active_widget_order' => ['weights' => ['sort' => 20], 'settings' => ['sort' => 'ASC']],
  ],
]);
$facet->save();
```

## Common Mistakes

- **Wrong**: Using AND operator on a single-value field with multiple selections → **Right**: OR is almost always what users expect. AND on a single-value field returns no results when multiple are selected.
- **Wrong**: Setting hard_limit on database backend and expecting alphabetical cutoff → **Right**: On the database backend, hard limit sorts by count first, then by raw value (entity ID). Items alphabetically later with the same count may be cut.
- **Wrong**: Two facets sharing the same URL alias → **Right**: Each facet needs a unique URL alias. Shared aliases cause URL parameter conflicts.

## See Also

- [Processing Pipeline](processing-pipeline.md) — how processors transform results
- [Widgets](widgets.md) — choosing a display widget
- Reference: `web/modules/contrib/facets/src/Entity/Facet.php`
