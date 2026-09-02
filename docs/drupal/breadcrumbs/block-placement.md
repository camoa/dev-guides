---
description: Place the SystemBreadcrumbBlock via block UI or config YAML — regions, visibility conditions, and programmatic rendering
tldr: "The `SystemBreadcrumbBlock` (plugin ID `system_breadcrumb_block`) is the only standard way to render breadcrumbs in a region. Place via the Block UI or via config YAML for themes, recipes, or installation profiles."
drupal_version: "11.x"
---

# Block Placement

## When to Use

> The `SystemBreadcrumbBlock` (plugin ID `system_breadcrumb_block`) is the only standard way to render breadcrumbs in a region. Place it via the Block UI or via config YAML in custom themes or installation profiles.

## Pattern

The block uses `createPlaceholder(): true` which means Drupal renders it as a BigPipe placeholder. The actual breadcrumb HTML is sent after the page's main content, replaced in the browser via a JavaScript-free SSR mechanism. This prevents slow breadcrumb resolution from blocking the page response.

**Block config YAML** (e.g., for a custom theme or recipe):
```yaml
# config/install/block.block.mytheme_breadcrumbs.yml
langcode: en
status: true
dependencies:
  theme:
    - mytheme
id: mytheme_breadcrumbs
theme: mytheme
region: breadcrumb
weight: -10
provider: null
plugin: system_breadcrumb_block
settings:
  id: system_breadcrumb_block
  label: Breadcrumbs
  label_display: '0'
  provider: system
visibility: {}
```

**Key fields:**
| Field | Value | Notes |
|---|---|---|
| `plugin` | `system_breadcrumb_block` | Always this for breadcrumbs |
| `region` | `breadcrumb` | Must match a region declared in your theme's `.info.yml` |
| `label_display` | `'0'` | `'0'` hides the block title; `visible` shows it |
| `weight` | integer | Lower = higher position in region |
| `visibility` | `{}` | Add request path conditions to hide on specific pages |

**Hiding on the front page:**
```yaml
visibility:
  request_path:
    id: request_path
    pages: '<front>'
    negate: true
    context_mapping: {}
```

**Programmatic block rendering** (in a controller or preprocess, if needed outside of a region):
```php
$block_manager = \Drupal::service('plugin.manager.block');
$block = $block_manager->createInstance('system_breadcrumb_block', []);
$render = $block->build();
```

## Common Mistakes

- Placing the breadcrumb block in a region not declared in the theme — the block will not appear; check the theme's `.info.yml` for available regions
- Disabling the `label_display` at the wrong key — YAML value must be the string `'0'` not boolean `false`
- Trying to render breadcrumbs by calling `BreadcrumbManager::build()` in a preprocess function — this bypasses caching; use the block or a render array with `#theme => 'breadcrumb'` instead

## See Also

- Template for the block output → [Twig Theming](twig-theming.md)
- Cache behavior → [Caching](caching.md)
- Reference: `core/modules/system/src/Plugin/Block/SystemBreadcrumbBlock.php`
- Reference: `core/profiles/demo_umami/config/install/block.block.umami_breadcrumbs.yml`
