---
tldr: "When you need to render a view, block, entity, or field from within a Twig template without a preprocess function — particularly useful for CMS-style layouts and quick embeds."
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

#### `drupal_view_result(view_id, display_id, ...args)`
**Description:** Returns raw result rows from a View (not rendered). Useful for counting or checking if results exist.
**Usage:**
```twig
{% if drupal_view_result('related', 'block_1', node.id())|length > 0 %}
  {{ drupal_view('related', 'block_1', node.id()) }}
{% endif %}
```
**Gotchas:** Returns `ResultRow[]`, not rendered HTML. Must be processed or counted, not printed directly.

#### `drupal_form(form_id, ...args)`
**Description:** Builds and returns a form render array by form class name.
**Usage:**
```twig
{{ drupal_form('Drupal\\search\\Form\\SearchBlockForm') }}
{{ drupal_form('Drupal\\mymodule\\Form\\QuickFeedbackForm') }}
```
**Gotchas:** Use the full namespace (double backslashes). Additional args passed to form constructor.

#### `drupal_title()`
**Description:** Returns the current page's route title as a render array.
**Usage:**
```twig
{{ drupal_title() }}
```

#### `drupal_url(user_input, options, check_access)`
**Description:** Returns a `\Drupal\Core\Url` object from a path string.
**Usage:**
```twig
{% set my_url = drupal_url('/node/42') %}
{% set external = drupal_url('https://example.com') %}
```

#### `drupal_link(text, user_input, options, check_access)`
**Description:** Returns a `\Drupal\Core\Link` object.
**Usage:**
```twig
{{ drupal_link('Contact us'|t, '/contact') }}
{{ drupal_link('Visit site'|t, 'https://example.com', {attributes: {target: '_blank'}}) }}
```

#### `drupal_messages()`
**Description:** Returns the status messages render array.
**Usage:**
```twig
{{ drupal_messages() }}
```

#### `drupal_breadcrumb()`
**Description:** Returns the current page's breadcrumb render array.
**Usage:**
```twig
{{ drupal_breadcrumb() }}
```

#### `drupal_contextual_links(id)`
**Description:** Renders contextual links placeholder for a given ID string.
**Usage:**
```twig
{{ drupal_contextual_links('node:node=42:') }}
```

#### `drupal_breakpoint()`
**Description:** Triggers an Xdebug breakpoint — all Twig context variables accessible in debugger.
**Usage:**
```twig
{{ drupal_breakpoint() }}
```
**Gotchas:** Requires Xdebug. Does nothing without it.

### Twig Tweak Filters
| Filter | Usage | Description |
|---|---|---|
| `\|token_replace` | `{{ text\|token_replace }}` | Replaces all tokens in a string |
| `\|image_style` | `{{ 'public://img.jpg'\|image_style('thumbnail') }}` | Returns absolute URL of styled image derivative |
| `\|check_markup` | `{{ text\|check_markup('basic_html') }}` | Runs text through a Drupal text format |
| `\|view` | `{{ entity\|view('teaser') }}` | Renders an entity, FieldItemList, or FieldItem object |
| `\|entity_url` | `{{ node\|entity_url }}` or `{{ node\|entity_url('edit-form') }}` | Gets entity URL object (workaround for sandbox blocking `toUrl()`) |
| `\|entity_link` | `{{ node\|entity_link('Read more'\|t) }}` | Gets entity Link object |
| `\|translation` | `{{ media\|translation }}` | Returns entity translation for current/specified language |
| `\|file_url` | `{{ 'public://img.jpg'\|file_url }}` | File URI to relative URL. `\|file_url(false)` for absolute URL |
| `\|file_uri` | `{{ media.field_media_image\|file_uri }}` | Extracts file URI from file entity or field item |
| `\|children` | `{{ content\|children }}` or `{{ content\|children(true) }}` | Returns child render elements only. `true` sorts by `#weight` |
| `\|with` | `{{ element\|with('#prefix', '<div>') }}` | Adds/sets key in render array. Opposite of `\|without` |
| `\|cache_metadata` | `{{ content.field_ref\|cache_metadata }}` | Extracts and bubbles cache metadata |
| `\|preg_replace` | `{{ text\|preg_replace('/\\d+/', '#') }}` | Regex search-and-replace |
| `\|transliterate` | `{{ text\|transliterate }}` | Unicode to US-ASCII transliteration |
| `\|truncate` | `{{ text\|truncate(100, true, true) }}` | Safe UTF-8 truncation (max_length, wordsafe, ellipsis) |
| `\|format_size` | `{{ filesize\|format_size }}` | Human-readable byte size (e.g., "1.5 MB") |
| `\|data_uri` | `{{ source(directory ~ '/logo.svg')\|data_uri('image/svg+xml') }}` | RFC 2397 data URI encoding (inline SVGs, images) |
| `\|php` | `{{ 'date("Y")'\|php }}` | Evaluates PHP. **Disabled by default.** Requires `$settings['twig_tweak_enable_php_filter'] = TRUE` in `settings.php` |

### Common Mistakes
- Using `drupal_config()` for values that affect rendering → cache metadata not bubbled, stale cache
- Using `drupal_entity()` to re-render an entity that's already available in the template → use `{{ content.field_ref }}` instead
- Using `drupal_block()` with the block config entity ID (e.g., `bartik_branding`) instead of plugin ID → must be plugin ID
- `drupal_view_result()` returns the raw results array, not rendered output — needs further processing
- Enabling `|php` filter in production → severe security risk, only for development/debugging
- Missing `|file_uri` when you have a media entity → use `{{ media.field_media_image|file_uri }}` to extract the URI, then `|file_url` for the URL

### See Also
- Core field rendering → [Accessing Field Values](accessing-field-values.md)
- Module source: `modules/contrib/twig_tweak/src/TwigTweakExtension.php`
- Reference: [Twig Tweak 3.x cheat sheet](https://git.drupalcode.org/project/twig_tweak/-/blob/3.x/docs/cheat-sheet.md)
