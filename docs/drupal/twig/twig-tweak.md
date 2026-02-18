---
topic: drupal/twig
guide: twig-tweak
---

## Twig Tweak Module

### When to Use
When you need to render a view, block, entity, or field from within a Twig template without a preprocess function — particularly useful for CMS-style layouts and quick embeds.

**Install:** `composer require drupal/twig_tweak` then enable the module.

### Items

#### `drupal_view(view_id, display_id, ...args)`
**Description:** Embeds a View display.
**Usage:**
```twig
{{ drupal_view('frontpage', 'page_1') }}
{{ drupal_view('related_content', 'block_1', node.id()) }}
```
**Gotchas:** Arguments after display_id become contextual filter values. Returns rendered HTML directly.

#### `drupal_block(plugin_id, configuration, wrapper)`
**Description:** Renders a block plugin by its plugin ID.
**Usage:**
```twig
{{ drupal_block('system_branding_block') }}
{{ drupal_block('views_block:frontpage-block_1', {label_display: false}) }}
```
**Gotchas:** `wrapper: FALSE` skips the `block.html.twig` wrapper. Use plugin ID, not block config entity ID.

#### `drupal_region(region, theme)`
**Description:** Renders all blocks in a region.
**Usage:**
```twig
{{ drupal_region('sidebar_first') }}
```
**Gotchas:** Renders the full region including all placed blocks. Bypasses the normal page template — use sparingly.

#### `drupal_entity(entity_type, id, view_mode, langcode, check_access)`
**Description:** Loads and renders an entity by ID.
**Usage:**
```twig
{{ drupal_entity('node', 42) }}
{{ drupal_entity('node', node.id(), 'card') }}
{{ drupal_entity('taxonomy_term', node.field_category.target_id, 'full') }}
```
**Gotchas:** `check_access` defaults to `TRUE` — the entity won't render if current user lacks view access. Always prefer this over manual entity loading in templates.

#### `drupal_entity_form(entity_type, id, form_mode, values, check_access)`
**Description:** Renders an entity form.
**Usage:**
```twig
{{ drupal_entity_form('contact_message', NULL, 'default') }}
```

#### `drupal_field(field_name, entity_type, id, view_mode, langcode, check_access)`
**Description:** Renders a single field from an entity.
**Usage:**
```twig
{{ drupal_field('field_tags', 'node', node.id(), 'full') }}
```
**Gotchas:** Returns a render array for the specific field only, rendered in the given view mode. Less efficient than `{{ content.field_tags }}` since it loads the entity again.

#### `drupal_menu(menu_name, level, depth, expand)`
**Description:** Renders a menu.
**Usage:**
```twig
{{ drupal_menu('main') }}
{{ drupal_menu('footer', 1, 2) }}
```

#### `drupal_image(selector, style, attributes, responsive, check_access)`
**Description:** Renders an image from a URI, file path, or file entity ID.
**Usage:**
```twig
{{ drupal_image('public://hero.jpg', 'large') }}
{{ drupal_image(node.field_image.target_id, 'card_thumbnail') }}
```

#### `drupal_token(token, data, options)`
**Description:** Replaces a Drupal token.
**Usage:**
```twig
{{ drupal_token('site:name') }}
{{ drupal_token('node:title', {node: node}) }}
```

#### `drupal_config(config_name, key)`
**Description:** Gets a configuration value.
**Usage:**
```twig
{% if drupal_config('system.site', 'name') == 'My Site' %}
```
**Gotchas:** No cache metadata is bubbled — config changes may not invalidate the page cache. Use in preprocess instead for cache correctness.

#### `drupal_dump(variable)` / `dd(variable)`
**Description:** Dumps a variable using Devel's dumper.
**Usage:**
```twig
{{ drupal_dump(node) }}
{{ dd(content) }}
```
**Gotchas:** Requires Devel module. Remove before deployment.

### Twig Tweak Filters
| Filter | Usage | Description |
|---|---|---|
| `\|token_replace` | `{{ text\|token_replace }}` | Replaces tokens in a string |
| `\|image_style` | `{{ 'public://img.jpg'\|image_style('thumbnail') }}` | Returns styled image URL |
| `\|check_markup` | `{{ text\|check_markup('basic_html') }}` | Applies text format |
| `\|view` | `{{ entity\|view('teaser') }}` | Renders an entity object |
| `\|entity_url` | `{{ node\|entity_url }}` | Gets entity canonical URL |
| `\|entity_link` | `{{ node\|entity_link('Read more'\|t) }}` | Gets entity link render array |
| `\|file_url` | `{{ 'public://img.jpg'\|file_url }}` | File URI to URL (alias of core) |
| `\|children` | `{{ content\|children }}` | Returns child render elements only |
| `\|cache_metadata` | For cache debugging | Extracts cache metadata |

### Common Mistakes
- Using `drupal_config()` for values that affect rendering → cache metadata not bubbled, stale cache
- Using `drupal_entity()` to re-render an entity that's already available in the template → use `{{ content.field_ref }}` instead
- Using `drupal_block()` with the block config entity ID (e.g., `bartik_branding`) instead of plugin ID → must be plugin ID
- `drupal_view_result()` returns the raw results array, not rendered output — needs further processing

### See Also
- Core field rendering → [Accessing Field Values](accessing-field-values.md)
- Module source: `modules/contrib/twig_tweak/src/TwigTweakExtension.php`
