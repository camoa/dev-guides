---
description: When to use taxonomy vs other content organization approaches
drupal_version: "11.x"
---

# Taxonomy System Overview

## When to Use

> Use taxonomy when you need to categorize, tag, or organize content with reusable terms. Use list fields when you have a fixed list of options specific to one content type.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Flexible categorization across content types | Taxonomy vocabulary | Terms are reusable entities, not tied to specific content types |
| Fixed list of options specific to one content type | List field (options) | Simpler, no entity overhead, config-based values |
| User-created tags with autocomplete | Taxonomy with entity reference widget set to "Autocomplete (Tags style)" | Auto-creates terms on-the-fly when users type new values |
| Hierarchical categorization (parent-child) | Hierarchical taxonomy vocabulary | Built-in support for unlimited depth parent-child relationships |
| Simple key-value lookup without UI | List field or config entity | Lower overhead than taxonomy terms |

## Pattern

Taxonomy consists of two entity types:

**Vocabulary** — Config entity, bundle for terms. Define via YAML at `config/install/taxonomy.vocabulary.VOCAB_ID.yml`:
```yaml
langcode: en
status: true
name: Tags
vid: tags
description: 'Use tags to group content on similar topics.'
weight: 0
new_revision: false
```

**Term** — Content entity, the actual classification values. Managed via UI or code:
```php
$term = Term::create([
  'vid' => 'tags',
  'name' => 'Drupal',
]);
$term->save();
```

## Common Mistakes

- **Wrong**: Using taxonomy when a simple list field would suffice → **Right**: Use list fields for small, fixed sets of options that don't need pages or hierarchy
- **Wrong**: Creating separate vocabularies for each content type → **Right**: Vocabularies are site-wide; use one vocabulary across multiple content types when categorization is shared
- **Wrong**: Treating terms as content types → **Right**: If you need multiple fields, rich text, or complex relationships, use a content type with an entity reference field instead
- **Wrong**: Using vocabulary machine name over 32 characters → **Right**: Vid is max 32 characters (enforced in schema). Choose short, descriptive IDs

## See Also

- [Vocabulary Configuration Schema](vocabulary-config-schema.md)
- Reference: `/core/modules/taxonomy/src/Entity/Vocabulary.php`
- Reference: `/core/modules/taxonomy/src/Entity/Term.php`
- Reference: [Drupal.org Taxonomy User Guide](https://www.drupal.org/docs/user_guide/en/structure-taxonomy.html)
