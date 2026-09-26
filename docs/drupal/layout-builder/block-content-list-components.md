---
tldr: "Use atomic block_content bundles + taxonomy + block_content_field_data View for LB list items (no Paragraphs). One ViewsBlock display per category (fixed arg). Register the block_content render trio (hook_theme and the suggestions alter in the theme, hook_block_content_view scoped to the View rows' list_item view mode in a module) to enable per-bundle Twig templates."

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

Drupal core ships NO `block_content` entity render theme hook (only an admin add-list template), and `BlockContentViewBuilder::getBuildDefaults()` unsets `#theme`. Its parent `EntityViewBuilder` sets `#theme` only when the theme registry has a `block_content` hook, and the child removes it even then. So when a `block_content` entity renders OUTSIDE the Block plugin path (e.g. as a View row) it has no template and no suggestions. Register the theme hook, set `#theme` on the build, and add bundle suggestions. That takes three hooks, and they cannot all live in the theme:

| Hook | Lives in | Why |
|---|---|---|
| 1. `hook_theme()` | Theme | The theme registry invokes `hook_theme()` for the active theme and its base themes |
| 2. `hook_block_content_view()` | Module | `EntityViewBuilder::buildMultiple()` calls all entity view hooks through `moduleHandler()` only: `invokeAll()` for `hook_block_content_view()` and `hook_entity_view()`, `alter()` for their `_alter` variants. A theme's `mytheme_block_content_view()` never runs |
| 3. `hook_theme_suggestions_block_content_alter()` | Theme | `ThemeManager` runs suggestion alters for modules and then for the active theme |

Hooks 1 and 3 go in the theme:

```php
// mytheme.theme
// 1. Register the theme hook — core does not.
function mytheme_theme(array $existing, string $type, string $theme, string $path): array {
  return [
    'block_content' => [
      'render element' => 'elements',
      'template' => 'content/block-content',
    ],
  ];
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

Hook 2 goes in a module: the site's custom module, or a small companion module shipped with the theme. Scope it to a dedicated view mode that only the listing View uses. First create a Content block view mode `list_item` (config `core.entity_view_mode.block_content.list_item`). Then set the listing View's row to the rendered Content block (row plugin `entity:block_content`) and select `list_item` in its view mode setting. On Drupal 11.1 and later, write hook 2 as a `#[Hook]` method in a `src/Hook/` class:

```php
// my_module/src/Hook/BlockContentRenderHooks.php
namespace Drupal\my_module\Hook;

use Drupal\Core\Entity\Display\EntityViewDisplayInterface;
use Drupal\Core\Entity\EntityInterface;
use Drupal\Core\Hook\Attribute\Hook;

class BlockContentRenderHooks {

  // 2. BlockContentViewBuilder unsets #theme; set it again for View rows only.
  #[Hook('block_content_view')]
  public function blockContentView(array &$build, EntityInterface $entity, EntityViewDisplayInterface $display, string $view_mode): void {
    if ($view_mode === 'list_item') {
      $build['#theme'] = 'block_content';
    }
  }

}
```

`getBuildDefaults()` already puts the entity in `#block_content` and the view mode in `#view_mode`, so hook 2 sets only `#theme`.

Drupal 10 and 11.0 do not collect `#[Hook]` classes. To support them, also add `my_module_block_content_view()` to `my_module.module`, marked `#[LegacyHook]` so 11.1 and later skip it and the hook runs once. Those cores do not autowire the class either, so register it in `my_module.services.yml` (change record 3442349):

```yaml
# my_module.services.yml
services:
  Drupal\my_module\Hook\BlockContentRenderHooks:
    class: Drupal\my_module\Hook\BlockContentRenderHooks
    autowire: true
```

```php
// my_module.module
use Drupal\Core\Entity\Display\EntityViewDisplayInterface;
use Drupal\Core\Entity\EntityInterface;
use Drupal\Core\Hook\Attribute\LegacyHook;
use Drupal\my_module\Hook\BlockContentRenderHooks;

#[LegacyHook]
function my_module_block_content_view(array &$build, EntityInterface $entity, EntityViewDisplayInterface $display, string $view_mode): void {
  \Drupal::service(BlockContentRenderHooks::class)->blockContentView($build, $entity, $display, $view_mode);
}
```

This trio enables per-bundle templates when `block_content` renders as View rows. For a `testimonial` row, the suggestion alter offers `block-content--testimonial.html.twig` and `block-content--testimonial--list-item.html.twig`; the second is more specific and wins. Without either, `content/block-content.html.twig` renders. The template receives the build as `elements` (render element `elements`), not `content`: print `{{ elements }}` or its children, such as `{{ elements.field_quote }}`.

The `list_item` view mode keeps placed and inline blocks unchanged. `BlockContentBlock` and Layout Builder's `InlineBlock` build in the view mode set on the placement, `full` by default, so hook 2 skips them. Inside Layout Builder, `BlockComponentRenderArray` moves the content `#attributes` to the block wrapper whatever `#theme` is. For a `BlockContentBlock` placed through the block layout, `BlockViewBuilder` moves them only while the content has no `#theme`, which the scoping preserves. Do not select `list_item` on a placement. If the admin theme can also render the listing View, guard hook 2 with `\Drupal::service('theme.registry')->getRuntime()->has('block_content')`; otherwise a theme without hook 1 logs "Theme hook block_content not found.".

### Common Mistakes

- **Modeling as a wrapper block with multi-value entity_reference to CHILD blocks** → This "wrapper block_content referencing many child block_content entities" pattern was NOT found in production. The only multi-value `entity_reference` on a block bundle referenced MEDIA, not blocks. Use the taxonomy-ref + View pattern instead
- **Expecting one parameterized ViewsBlock display to accept a per-placement term id** → `ViewsBlock` reads the argument from the context system, not block config. Create one fixed-argument display per category
- **Expecting block_content to theme itself as a View row** → `BlockContentViewBuilder` unsets the `#theme` its parent sets. Without the theme-hook trio the row renders with no template and no suggestions
- **Putting hook 2 in the theme** → Core invokes entity view hooks for modules only, so `mytheme_block_content_view()` never runs and `#theme` stays unset. Put hook 2 in a module
- **Setting `#theme` in an unscoped `hook_entity_view()`** → It fires for every `block_content` build, including every placed and inline block site-wide. Those blocks gain the `block_content` template, and `BlockViewBuilder` stops moving content `#attributes` on placed reusable blocks to the wrapper. Check for the listing View's view mode
- **Reaching for Paragraphs by reflex** → For reusable, filterable list items the atomic block_content + View pattern avoids Paragraphs' host-entity coupling

### See Also

- Section 7: Inline vs Reusable Blocks (`inline-vs-reusable`) — choosing reusable block_content
- Section 15: Theming Layout Builder (`theming-lb`) — template suggestions and preprocessing
- Views topic — building the `block_content_field_data` listing View
- Reference: `/core/modules/block_content/src/BlockContentViewBuilder.php`
