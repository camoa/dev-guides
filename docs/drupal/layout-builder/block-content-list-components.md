---
tldr: "Use atomic block_content bundles + taxonomy + block_content_field_data View for LB list items (no Paragraphs). One ViewsBlock display per category (fixed arg). Register the three-hook block_content theme trio to enable per-bundle Twig templates."

---
## 8.1. Modeling List Components with block_content (No Paragraphs)

### When to Use

When you need repeating page-section lists (testimonials, gallery items, client logos) inside Layout Builder but do NOT want the Paragraphs module. Model each list item as an atomic reusable `block_content` bundle and assemble the list with a View, keeping items reusable and query-filterable rather than locked inside a host entity.

### Pattern

**(a) Atomic block_content + taxonomy grouping + View listing**

Create one reusable `block_content` bundle per item type (e.g. `testimonial`). Give it a single-value `entity_reference` field to a taxonomy term used purely for grouping/filtering. Then list the items with a View whose base table is `block_content_field_data`, filtered by the grouping term.

```yaml
# field.storage.block_content.field_category.yml (verified real config)
type: entity_reference
cardinality: 1
settings:
  target_type: taxonomy_term
```

```yaml
# The listing View base table
base_table: block_content_field_data
```

The View selects all `block_content` items of the bundle whose `field_category` matches a given term, and renders them as rows in a single Layout Builder placement.

**(b) Fixed-argument per-category View display workaround**

Core's `ViewsBlock` plugin reads a contextual filter value from the context system, NOT from per-placement block config — so you cannot pass a per-Layout-Builder-placement category id through a single parameterized block display. The verified workaround is ONE block display per category, each overriding `defaults.arguments: false` and hard-coding a fixed contextual-filter argument:

```yaml
block_category_a:
  id: block_category_a
  display_plugin: block
  display_options:
    defaults:
      arguments: false
    arguments:
      field_category_target_id:
        id: field_category_target_id
        table: block_content__field_category
        field: field_category_target_id
        plugin_id: numeric
        default_action: default
        default_argument_type: fixed
        default_argument_options:
          argument: '1'
```

Each additional per-category display (`block_category_b`, etc.) repeats this shape with its own fixed term id. Editors then place the display matching the category they want.

**(c) The block_content render theme-hook trio**

Drupal core ships NO `block_content` entity render theme hook (only an admin add-list template), and `BlockContentViewBuilder` does not set `#theme`. So when a `block_content` entity renders OUTSIDE the Block plugin path (e.g. as a View row) it has no template and no suggestions. Register the theme hook, set `#theme` on the build, and add bundle suggestions — three hooks in a theme (or module):

```php
// 1. Register the theme hook — core does not.
function mytheme_theme(array $existing, string $type, string $theme, string $path): array {
  return [
    'block_content' => [
      'render element' => 'elements',
      'template' => 'content/block-content',
    ],
  ];
}
// 2. BlockContentViewBuilder sets no #theme; set it so the hook fires.
function mytheme_entity_view(array &$build, \Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display, string $view_mode): void {
  if ($entity->getEntityTypeId() === 'block_content') {
    $build['#theme'] = 'block_content';
    $build['#block_content'] = $entity;
    $build['#view_mode'] = $view_mode;
  }
}
// 3. Core adds no bundle suggestions for block_content (only for the block plugin). Add them.
function mytheme_theme_suggestions_block_content_alter(array &$suggestions, array $variables): void {
  if (!empty($variables['elements']['#block_content'])) {
    $bundle = $variables['elements']['#block_content']->bundle();
    $suggestions[] = 'block_content__' . $bundle;
    if (!empty($variables['elements']['#view_mode'])) {
      $view_mode = strtr($variables['elements']['#view_mode'], '.', '_');
      $suggestions[] = 'block_content__' . $bundle . '__' . $view_mode;
    }
  }
}
```

This trio enables per-bundle templates like `block-content--testimonial.html.twig` when `block_content` renders as View rows.

### Common Mistakes

- **Modeling as a wrapper block with multi-value entity_reference to CHILD blocks** → This "wrapper block_content referencing many child block_content entities" pattern was NOT found in production. The only multi-value `entity_reference` on a block bundle referenced MEDIA, not blocks. Use the taxonomy-ref + View pattern instead
- **Expecting one parameterized ViewsBlock display to accept a per-placement term id** → `ViewsBlock` reads the argument from the context system, not block config. Create one fixed-argument display per category
- **Expecting block_content to theme itself as a View row** → Core sets no `#theme` on `BlockContentViewBuilder` output. Without the theme-hook trio the row renders with no template and no suggestions
- **Reaching for Paragraphs by reflex** → For reusable, filterable list items the atomic block_content + View pattern avoids Paragraphs' host-entity coupling

### See Also

- Section 7: Inline vs Reusable Blocks (`inline-vs-reusable`) — choosing reusable block_content
- Section 15: Theming Layout Builder (`theming-lb`) — template suggestions and preprocessing
- Views topic — building the `block_content_field_data` listing View
- Reference: `/core/modules/block_content/src/BlockContentViewBuilder.php`
