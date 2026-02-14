---
description: Configure entity reference field widgets and formatters for taxonomy term fields
drupal_version: "11.x"
---

# Taxonomy with Entity Reference

## When to Use

> Use this guide to configure entity reference field widgets and formatters for taxonomy term fields. Widget choice affects UX and term creation workflow.

## Decision

| Situation | Use Widget | Why |
|-----------|-----------|-----|
| Tag-style entry with autocomplete and auto-creation | `entity_reference_autocomplete_tags` | Users type comma-separated terms, creates non-existent terms on-the-fly (requires `auto_create: true`) |
| Single term selection from dropdown | `options_select` | Simple, accessible, good for small vocabularies (<50 terms) |
| Multiple term checkboxes | `options_buttons` | Clear visual selection, best for small sets (<20 terms) |
| Hierarchical dropdown | `options_select` with hierarchy exposed filter | Shows indented terms, good for navigational taxonomies |
| Large vocabulary selection (>100 terms) | `entity_reference_autocomplete` | Avoids loading all terms in widget, uses AJAX |

## Pattern

**Autocomplete tags widget (field config):**
```yaml
settings:
  handler: 'default:taxonomy_term'
  handler_settings:
    target_bundles:
      tags: tags
    auto_create: true
    auto_create_bundle: tags
```

**Form display config (widget):**
```yaml
# core.entity_form_display.node.article.default
field_tags:
  type: entity_reference_autocomplete_tags
  weight: 3
  settings:
    match_operator: CONTAINS
    match_limit: 10
    size: 60
    placeholder: 'Enter tags...'
```

**View display config (formatter):**
```yaml
# core.entity_view_display.node.article.default
field_tags:
  type: entity_reference_label
  label: above
  settings:
    link: true  # Link to term page
```

**Formatter options:**
- `entity_reference_label` — Term name as text or link
- `entity_reference_entity_view` — Rendered term entity (custom view mode)
- `entity_reference_rss_category` — RSS-specific formatter

**TermSelection handler settings:**
```php
'handler_settings' => [
  'target_bundles' => ['tags' => 'tags'], // Restrict to vocabulary
  'sort' => [
    'field' => '_none', // or 'name', 'weight'
    'direction' => 'ASC',
  ],
  'auto_create' => TRUE, // Allow term creation
  'auto_create_bundle' => 'tags', // Vocabulary for new terms
]
```

## Common Mistakes

- **Wrong**: Not enabling `auto_create` for tag-style fields → **Right**: Set `auto_create: true` for tag autocomplete widgets
- **Wrong**: Using checkboxes for large vocabularies → **Right**: Switch to autocomplete for >20 terms
- **Wrong**: Forgetting `target_bundles` restriction → **Right**: Widget shows terms from ALL vocabularies without restriction
- **Wrong**: Not configuring placeholder text → **Right**: Add helpful placeholder: "Start typing to add tags..."
- **Wrong**: Linking to terms that have no content → **Right**: Either add term view or disable link in formatter
- **Wrong**: Assuming auto-created terms validate → **Right**: Auto-created terms bypass normal validation; add `hook_ENTITY_TYPE_presave()` to enforce rules

## See Also

- [Programmatic Term Operations](programmatic-terms.md)
- [Config Export & Recipes](taxonomy-config-recipes.md)
- Reference: `/core/modules/taxonomy/src/Plugin/EntityReferenceSelection/TermSelection.php`
- Reference: `/core/recipes/article_tags/recipe.yml` (lines 17-42)
