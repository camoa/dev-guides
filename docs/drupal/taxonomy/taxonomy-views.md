---
description: Build Views with taxonomy filters, arguments, and relationships
drupal_version: "11.x"
---

# Taxonomy Views Integration

## When to Use

> Use taxonomy Views plugins when building Views that filter, sort, or display content by taxonomy terms.

## Decision

| Situation | Use Plugin | Why |
|-----------|-----------|-----|
| Filter content by taxonomy term | `taxonomy_index_tid` filter | Specialized for taxonomy with hierarchy support |
| Contextual filter for term from URL | `taxonomy` argument | Filter view by term ID from path (e.g., `/taxonomy/term/123`) |
| Add term fields to node views | `node_term_data` relationship | Join nodes to terms through taxonomy_index table |
| Expose filter with autocomplete | `taxonomy_index_tid` with `type: textfield` | Better UX for large vocabularies |
| Show hierarchical dropdown | `taxonomy_index_tid` with `hierarchy: true` | Displays indented terms |

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

**TaxonomyIndexTid Filter Options:**

| Option | Values | Purpose |
|--------|--------|---------|
| `type` | `select`, `textfield` | Dropdown vs autocomplete |
| `vid` | Vocabulary ID | Limit terms to specific vocabulary |
| `hierarchy` | boolean | Show hierarchy in dropdown |
| `limit` | boolean | Restrict to vocabulary (use with `vid`) |

## Common Mistakes

- **Wrong**: Using entity reference filter instead of taxonomy_index_tid → **Right**: Use taxonomy-specific filter for term reference fields (supports hierarchy)
- **Wrong**: Exposing filter without vocabulary restriction → **Right**: Always set `vid` and `limit: true` for cleaner UX
- **Wrong**: Not enabling hierarchy when needed → **Right**: Enable `hierarchy: true` for navigational taxonomies
- **Wrong**: Forgetting taxonomy_index table limitation → **Right**: Only indexes nodes by default; for other entities, use entity reference relationship
- **Wrong**: Deep hierarchy in exposed filters → **Right**: Consider autocomplete widget for deep hierarchies (>3 levels)

## See Also

- [Term Management](term-management.md)
- [Taxonomy Permissions & Access](taxonomy-permissions.md)
- Reference: `/core/modules/taxonomy/src/Plugin/views/filter/TaxonomyIndexTid.php` (lines 159-176)
- Reference: `/core/modules/taxonomy/src/Plugin/views/argument/Taxonomy.php`
- Reference: `/core/modules/taxonomy/src/Plugin/views/relationship/NodeTermData.php`
