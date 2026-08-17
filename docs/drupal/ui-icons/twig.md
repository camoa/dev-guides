---
description: "Render an icon in a custom Twig template with core's icon() function, not UI Icons' admin-only icon_preview()."
tldr: "Use core's icon(pack_id, icon_id, settings) as the general renderer in theme templates; needs no contrib module. icon_preview() is the admin-preview renderer and silently defaults to size 32 when settings are omitted."
drupal_version: "11.x"
---

# Twig Rendering

## When to Use

> Rendering an icon directly in a custom Twig template (block, paragraph, layout).

## Pattern

Use **core's** `icon(pack_id, icon_id, settings)`, from `Drupal\Core\Template\IconsTwigExtension`. It is the general-purpose renderer and needs no contrib module:

```twig
{# Render with pack defaults #}
{{ icon('my_theme_icons', 'menu') }}

{# Render with overrides #}
{{ icon('my_theme_icons', 'menu', {
  size: 32,
  color: '#0066cc',
  decorative: true,
}) }}
```

It returns the `#type: icon` render array below, so cache metadata bubbles correctly.

## `icon_preview()` is not the same function

UI Icons also registers `icon_preview(pack_id, icon_id, settings)`, but it is the **admin-preview** renderer behind the Library page and the picker — not the one to reach for in a theme template. It returns `IconPreview::getPreview()`, and when you omit the settings argument it silently substitutes `{size: 32}` rather than the pack's own defaults.

## Decision

| Twig context | Approach |
|---|---|
| Static, theme-author-defined icon | `{{ icon(...) }}` with literal arguments |
| Rendering a preview in an admin/config UI | `{{ icon_preview(...) }}` |
| Icon from a field on the entity | Pass through field rendering — the field formatter handles it |
| Icon from a UI Patterns prop | Pattern templates render the prop automatically |

## Pattern: Programmatic Render Array (PHP)

```php
$build = [
  '#type' => 'icon',
  '#pack_id' => 'my_theme_icons',
  '#icon_id' => 'menu',
  '#settings' => ['size' => 32],
];
```

The property is `#icon_id`. `#icon` is not a recognized property of core's `Icon` element — it is ignored, `#icon_id` stays empty, and the element renders nothing.

Or via the plugin manager:

```php
$icon = \Drupal::service('plugin.manager.icon_pack')->getIcon('my_theme_icons:menu');
$build = $icon->getRenderable(['size' => 32]);
```

## Common Mistakes

- **Wrong**: calling `icon()` or `icon_preview()` with the full ID string (`my_theme_icons:menu`) → **Right**: both expect `(pack_id, icon_id, settings)` as separate arguments
- **Wrong**: using `icon_preview()` as the general renderer in theme templates → **Right**: it's the admin preview helper and forces `size: 32` when settings are omitted
- **Wrong**: hardcoding the SVG content from the source file → **Right**: bypasses settings, accessibility templating, and cache metadata

## See Also

- [UI Patterns Integration](patterns.md)
- [Field API Integration](field-api.md)
- Reference: `\Drupal\Core\Template\IconsTwigExtension`
- Reference: `src/Template/IconPreviewTwigExtension.php`
