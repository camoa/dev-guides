---
description: Place the SystemBreadcrumbBlock via block UI or config YAML — regions, visibility conditions, and programmatic rendering
tldr: "The `SystemBreadcrumbBlock` (plugin ID `system_breadcrumb_block`) is the only standard way to render breadcrumbs in a region. Place via the Block UI or via config YAML for themes, recipes, or installation profiles."
drupal_version: "11.x"
---

# Block Placement

## When to Use

> The `SystemBreadcrumbBlock` (plugin ID `system_breadcrumb_block`) is the only standard way to render breadcrumbs in a region. Place via the Block UI or via config YAML for themes, recipes, or installation profiles.

## Decision

| Need | Approach |
|---|---|
| Standard placement in a region | Block UI or config YAML |
| Hide on front page | Block visibility conditions with `<front>` path |
| Hide on specific paths | Block visibility `request_path` condition |
| Render breadcrumb outside a region | `plugin.manager.block` — but prefer config-based placement |

## Pattern

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
plugin: system_breadcrumb_block
settings:
  id: system_breadcrumb_block
  label: Breadcrumbs
  label_display: '0'
  provider: system
visibility: {}
```

**Hiding on the front page:**
```yaml
visibility:
  request_path:
    id: request_path
    pages: '<front>'
    negate: true
    context_mapping: {}
```

**Key fields:**

| Field | Notes |
|---|---|
| `plugin` | Always `system_breadcrumb_block` |
| `region` | Must match a region declared in the theme's `.info.yml` |
| `label_display` | `'0'` hides block title (string, not boolean) |
| `visibility` | Empty `{}` = show everywhere; use `request_path` to restrict |

**Programmatic rendering** (outside a region — use sparingly):
```php
$block = \Drupal::service('plugin.manager.block')
  ->createInstance('system_breadcrumb_block', []);
$render = $block->build();
```

Note: The block uses `createPlaceholder(): true` — it renders via BigPipe as a lazy placeholder. This prevents slow breadcrumb resolution from blocking the page response.

## Common Mistakes

- **Wrong**: Placing the breadcrumb block in a region not declared in the theme `.info.yml` → **Right**: The block will silently not appear; check available regions in the theme file
- **Wrong**: Setting `label_display: false` (boolean) → **Right**: Use the string `'0'`; YAML boolean `false` is not recognized by the block system
- **Wrong**: Calling `BreadcrumbManager::build()` directly in a preprocess function → **Right**: Bypasses caching; use the block or a render array with `#theme => 'breadcrumb'` instead

## See Also

- [Twig Theming](twig-theming.md)
- [Caching](caching.md)
- Reference: `core/modules/system/src/Plugin/Block/SystemBreadcrumbBlock.php`
- Reference: `core/profiles/demo_umami/config/install/block.block.umami_breadcrumbs.yml`
