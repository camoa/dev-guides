---
description: "Build Views with taxonomy filters, arguments, and relationships"
tldr: "Use taxonomy Views plugins when building Views that filter, sort, or display content by taxonomy terms."
drupal_version: "11.x"
---

# Taxonomy Views Integration

## When to Use

> Use this guide when building Views that filter, sort, or display content by taxonomy terms.

Taxonomy module provides specialized Views plugins.

## Taxonomy Views Plugins

### Filters

**TaxonomyIndexTid** — Filter by term ID with vocabulary restriction, hierarchy support

| Plugin ID | `taxonomy_index_tid` |
|-----------|---------------------|
| **Purpose** | Filter content by taxonomy term |
| **Key Options** | |
| `type` | `select` (dropdown) or `textfield` (autocomplete) |
| `vid` | Vocabulary ID to limit terms |
| `hierarchy` | Show hierarchy in dropdown (boolean) |
| `limit` | Restrict to specific vocabulary (boolean) |
| **Usage** | Exposed filter for taxonomy-based content listing |

**Gotchas:**
- Exposed filter with hierarchy enabled shows indented terms but may confuse users with deep trees
- Autocomplete type requires JavaScript; fallback to select for accessibility
- Filter uses `taxonomy_index` table for performance — only works with node entities by default

Reference: `/core/modules/taxonomy/src/Plugin/views/filter/TaxonomyIndexTid.php`

### Arguments

**Taxonomy (TermId)** — Contextual filter for term ID

| Plugin ID | `taxonomy` |
|-----------|-------------|
| **Purpose** | Filter view by term from URL (e.g., `/taxonomy/term/123`) |
| **Extends** | EntityArgument |
| **Usage** | Automatic term page views, breadcrumb context |

**Gotchas:**
- Inherits entity argument validation — can validate term exists and user has access
- Default term page view uses this argument

Reference: `/core/modules/taxonomy/src/Plugin/views/argument/Taxonomy.php`

### Relationships

**NodeTermData** — Relationship from nodes to taxonomy terms via taxonomy_index

| Plugin ID | `node_term_data` |
|-----------|------------------|
| **Purpose** | Join nodes to terms through taxonomy_index table |
| **Usage** | Add term fields to node views |

**Gotchas:**
- Only works for nodes; other entity types need different relationship
- Uses denormalized taxonomy_index table for performance

Reference: `/core/modules/taxonomy/src/Plugin/views/relationship/NodeTermData.php`

### Fields

**TermName** — Displays term name with optional link

| Plugin ID | `term_field_data` table fields |
|-----------|-------------------------------|
| **Purpose** | Show term name, description, weight in views |
| **Settings** | Link to term page (boolean) |

## Pattern

**Exposed filter with autocomplete:**
```yaml
# In view config (simplified)
display:
  default:
    display_options:
      filters:
        field_tags_target_id:
          id: field_tags_target_id
          plugin_id: taxonomy_index_tid
          type: textfield
          vid: tags
          hierarchy: false
```

**Argument for term page:**
```yaml
# View displays content on /taxonomy/term/%
arguments:
  tid:
    id: tid
    plugin_id: taxonomy
    table: taxonomy_index
    field: tid
```

## Common Mistakes

- Using entity reference filter instead of taxonomy_index_tid → Entity reference filter is slower, doesn't support hierarchy option. Use taxonomy-specific filter for term reference fields
- Exposing filter without vocabulary restriction → Shows all terms from all vocabularies. Always set `vid` and `limit: true` for cleaner UX
- Not enabling hierarchy when needed → Users expect hierarchical dropdowns for categorized vocabularies. Enable `hierarchy: true` for navigational taxonomies
- Forgetting taxonomy_index table limitation → Only indexes nodes by default. For other entities, use entity reference relationship instead
- Deep hierarchy in exposed filters → >3 levels creates unusable dropdown. Consider autocomplete widget or faceted search for deep hierarchies

## See Also

- ← Previous: [Term Management](term-management.md) | Next: [Taxonomy Permissions & Access](taxonomy-permissions.md) →
- Reference: `/core/modules/taxonomy/src/Plugin/views/filter/TaxonomyIndexTid.php` (lines 159-176)
