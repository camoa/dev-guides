---
description: "Configure entity reference field widgets and formatters for taxonomy term fields"
tldr: "Use this guide to configure entity reference field widgets and formatters for taxonomy term fields. Widget choice affects UX and term creation workflow."
drupal_version: "11.x"
---

# Taxonomy with Entity Reference

## When to Use

> Use this guide when configuring entity reference field widgets and formatters for taxonomy term fields.

Widget choice affects UX and term creation workflow.

## Decision

| If you need... | Use widget... | Why |
|---|---|---|
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

## TermSelection Handler

**Purpose:** Controls which terms appear in autocomplete/select widgets

**Default handler settings:**
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

**Custom selection with Views:**
```yaml
# Use View to filter available terms
handler: 'views'
handler_settings:
  view:
    view_name: taxonomy_term_reference
    display_name: entity_reference_1
    arguments: []
```

Reference: `/core/modules/taxonomy/src/Plugin/EntityReferenceSelection/TermSelection.php`

## Common Mistakes

- Not enabling `auto_create` for tag-style fields → Users can't create terms, must use taxonomy UI first. Set `auto_create: true` for tag autocomplete widgets
- Using checkboxes for large vocabularies → Renders all terms on page load. Switch to autocomplete for >20 terms
- Forgetting `target_bundles` restriction → Widget shows terms from ALL vocabularies. Always restrict to specific vocabulary
- Not configuring placeholder text → Empty autocomplete is confusing. Add helpful placeholder: "Start typing to add tags..."
- Linking to terms that have no content → If term page has no view, links go to empty page. Either add term view or disable link in formatter
- Assuming auto-created terms validate → Auto-created terms bypass normal validation. Add hook_ENTITY_TYPE_presave() to enforce rules (e.g., max length, allowed characters)

## See Also

- ← Previous: [Programmatic Term Operations](programmatic-terms.md) | Next: [Config Export & Recipes](taxonomy-config-recipes.md) →
- Reference: `/core/recipes/article_tags/recipe.yml` (lines 17-42)
