---
description: Render UI Icons directly in Twig templates using icon_preview() or a render array.
tldr: Use icon_preview(pack_id, icon_id, settings) in Twig to render an icon with correct cache metadata; it takes three separate arguments, not the combined pack:icon_id string. For PHP, use the #type => icon render array or plugin.manager.icon_pack->getIcon()->getRenderable().
drupal_version: "11.x"
---

# Twig Rendering

## When to Use

> Rendering an icon directly in a custom Twig template (block, paragraph, layout).

## Decision: which approach to use

| Twig context | Approach |
|---|---|
| Static, theme-author-defined icon | `{{ icon_preview(...) }}` with literal arguments |
| Icon from a field on the entity | Pass through field rendering — the formatter handles it |
| Icon from a UI Patterns prop | Pattern templates render the prop automatically |

## Pattern: `icon_preview()` Twig function

```twig
{# Render with default settings #}
{{ icon_preview('my_theme_icons', 'menu') }}

{# Render with overrides #}
{{ icon_preview('my_theme_icons', 'menu', {
  size: 32,
  color: '#0066cc',
  decorative: true,
}) }}
```

The function returns a renderable array — cache metadata bubbles correctly.

## Pattern: programmatic render array (PHP)

```php
$build = [
  '#type' => 'icon',
  '#pack_id' => 'my_theme_icons',
  '#icon' => 'menu',
  '#settings' => ['size' => 32],
];
```

Or via the plugin manager:

```php
$icon = \Drupal::service('plugin.manager.icon_pack')
  ->getIcon('my_theme_icons:menu');
$build = $icon->getRenderable(['size' => 32]);
```

## Common Mistakes

- **Wrong**: calling `icon_preview()` with the full ID string `'my_theme_icons:menu'` → **Right**: the function expects three arguments: `(pack_id, icon_id, settings)`, not one combined string
- **Wrong**: hardcoding the SVG content from the source file → **Right**: bypasses settings, accessibility templating, and cache metadata

## See Also

- [Settings & Rendering](settings-rendering.md)
- [Menu Integration](menu.md)
- Reference: `src/Template/IconPreviewTwigExtension.php`
