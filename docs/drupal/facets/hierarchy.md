---
description: "Building hierarchical facets from taxonomy parent-child relationships or date year/month/day grouping"
tldr: "Use this guide when faceting on hierarchical data — taxonomy vocabularies with parent-child relationships or date facets with year → month → day grouping. Requires Index hierarchy in Search API plus use_hierarchy on the facet."
drupal_version: "11.x"
---

# Hierarchy

## When to Use

> When faceting on hierarchical data — taxonomy vocabularies with parent-child relationships or date facets with year → month → day grouping.

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

## Pattern

To use hierarchy, the Search API index must know about it:

1. Go to your Search API index → Processors
2. Enable "Index hierarchy" processor
3. Configure which fields should have hierarchy indexed
4. Reindex

**Hierarchy-related processors:**

| Processor | Purpose |
|---|---|
| `hierarchy_processor` | Builds the tree structure (LOCKED — always runs when hierarchy enabled) |
| `hide_inactive_siblings_processor` | Collapse branches without active selections |
| `show_siblings_processor` | Show all siblings of active items |
| `show_only_deepest_level_items_processor` | Only show leaf-level items |

## Common Mistakes

- **Wrong**: Enabling only `use_hierarchy` on the facet → **Right**: Must also enable "Index hierarchy" in Search API AND set `use_hierarchy: TRUE` on the facet.
- **Wrong**: Assuming hierarchy always builds correctly → **Right**: `hierarchy_processor` runs at weight 100. If another processor removes parent items before weight 100, the tree can't be built.
- **Wrong**: Looking for a "Build hierarchical tree" checkbox in `facets_exposed_filters` → **Right**: There is no such checkbox, despite what the module's own `docs/exposed_filters.md` still says. Enable the `hierarchy_processor` in the filter's processor list; **Hierarchy type** and **Always expand hierarchy** then become visible in the facet filter settings within the Views UI.

## See Also

- [Processing Pipeline](processing-pipeline.md) — where hierarchy_processor fits
- [Result Filtering Processors](result-filtering-processors.md) — hierarchy-related filters
- Reference: `src/Plugin/facets/hierarchy/`
