---
description: Add icon pickers to menu link content entities and render icons in menu templates.
tldr: Enable ui_icons_menu to add an icon widget to the menu_link_content form. Icons do not render automatically — override menu.html.twig or write a preprocess hook to extract icon data from link options, then call icon_preview() in the template.
drupal_version: "11.x"
---

# Menu Integration

## When to Use

> Adding an icon to each menu item (navigation, sidebar menus, mega-menu themes).

## Pattern

Enable `ui_icons_menu`. The module alters the `menu_link_content` entity to add an icon widget on the standard menu link form.

The icon data is stored in the menu link's link options. The default Drupal menu templates do **not** render it automatically — you must add a preprocess or override:

```php
function mytheme_preprocess_menu(&$variables): void {
  foreach ($variables['items'] as &$item) {
    $url = $item['url'];
    $options = $url->getOptions();
    if (isset($options['attributes']['data-icon-id'])) {
      $item['icon_id'] = $options['attributes']['data-icon-id'];
      $item['icon_settings'] = $options['attributes']['data-icon-settings'] ?? [];
    }
  }
}
```

Then in `menu.html.twig`, render via `icon_preview()` (see [Twig Rendering](twig.md)):

```twig
{% if item.icon_id %}
  {{ icon_preview(item.icon_id|split(':')[0], item.icon_id|split(':')[1], item.icon_settings) }}
{% endif %}
```

## Decision: Navigation module

If using Drupal core's Navigation module, define a `class` setting in the icon pack so navigation styles can target the icon element via CSS.

## Common Mistakes

- **Wrong**: expecting icons to render in menus automatically after enabling the module → **Right**: menu templates need an explicit preprocess hook or Twig override; the data is stored but not output by default

## See Also

- [Twig Rendering](twig.md)
- [Settings & Rendering](settings-rendering.md)
- Reference: `modules/ui_icons_menu/ui_icons_menu.module`
