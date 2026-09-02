---
description: "When to use taxonomy vs other content organization approaches"
tldr: "Use taxonomy when you need to categorize, tag, or organize content with reusable terms. Use list fields when you have a fixed list of options specific to one content type."
drupal_version: "11.x"
---

# Taxonomy System Overview

## When to Use

> Use taxonomy when you need to categorize, tag, or organize content with reusable terms. Use list fields when you have a fixed list of options specific to one content type.

Taxonomy is Drupal's built-in classification system consisting of vocabularies (config entities) and terms (content entities).

## Decision

| If you need... | Use... | Why |
|---|---|---|
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

Reference: `/core/modules/taxonomy/src/Entity/Vocabulary.php`, `/core/modules/taxonomy/src/Entity/Term.php`

## Common Mistakes

- Using taxonomy when a simple list field would suffice → Adds entity query overhead for static values. Use list fields for small, fixed sets of options that don't need pages or hierarchy
- Creating separate vocabularies for each content type → Terms aren't reusable. Vocabularies are site-wide; use one vocabulary across multiple content types when categorization is shared (e.g., "Topics" for articles, events, blog posts)
- Treating terms as content types → Terms are classification labels, not full content. If you need multiple fields, rich text, or complex relationships, use a content type with an entity reference field instead
- Forgetting vocabulary machine name limit → Vid is max 32 characters (enforced in schema). Choose short, descriptive IDs

## See Also

- → Next: [Vocabulary Configuration Schema](vocabulary-config-schema.md)
- Reference: [Drupal.org Taxonomy User Guide](https://www.drupal.org/docs/user_guide/en/structure-taxonomy.html)
