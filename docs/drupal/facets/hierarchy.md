---
description: Facets hierarchy — taxonomy and date hierarchy plugins, Search API index hierarchy processor, hierarchy configuration settings
tldr: "Use this guide when faceting on hierarchical data — taxonomy vocabularies with parent-child relationships or date facets with year → month → day grouping."
drupal_version: "11.x"
---

# Hierarchy

## When to Use

> Use this guide when faceting on hierarchical data — taxonomy vocabularies with parent-child relationships or date facets with year → month → day grouping.

## Decision

**Hierarchy plugins:**

| ID | Class | Purpose |
|---|---|---|
| `taxonomy` | Taxonomy | Taxonomy term parent-child hierarchy |
| `date_items` | DateItems | Year → Month → Day temporal hierarchy |

**Hierarchy configuration:**

| Setting | Config Key | Default | Purpose |
|---|---|---|---|
| Use hierarchy | `use_hierarchy` | FALSE | Enable hierarchical display |
| Keep parents active | `keep_hierarchy_parents_active` | FALSE | Parent stays selected when child is selected |
| Expand hierarchy | `expand_hierarchy` | FALSE | Always show all levels expanded |
| Enable parent on child disable | `enable_parent_when_child_gets_disabled` | FALSE | Re-enable parent when last child is deselected |

**Hierarchy-related processors:**

| Processor | Purpose |
|---|---|
| `hierarchy_processor` | Builds the tree structure (LOCKED — always runs when hierarchy enabled) |
| `hide_inactive_siblings_processor` | Collapse branches without active selections |
| `show_siblings_processor` | Show all siblings of active items |
| `show_only_deepest_level_items_processor` | Only show leaf-level items |

## Pattern

To use hierarchy, the Search API index must know about it:

1. Go to your Search API index → Processors
2. Enable "Index hierarchy" processor
3. Configure which fields should have hierarchy indexed
4. Reindex

## Common Mistakes

- **Wrong**: Enabling hierarchy on the facet without enabling it in Search API → **Right**: Must enable "Index hierarchy" in Search API AND set `use_hierarchy: TRUE` on the facet.
- **Wrong**: Flat results despite hierarchy enabled → **Right**: The `hierarchy_processor` runs at weight 100. If something removes parent items before weight 100, the tree can't be built.
- **Wrong**: Expecting hierarchy to work in facets_exposed_filters without extra config → **Right**: In `facets_exposed_filters`, enable "Build hierarchical tree" in the facet filter settings within the Views UI.

## See Also

- [Processing Pipeline](processing-pipeline.md) — where hierarchy_processor fits
- [Result Filtering Processors](result-filtering-processors.md) — hierarchy-related filters
- Reference: `web/modules/contrib/facets/src/Plugin/facets/hierarchy/`
