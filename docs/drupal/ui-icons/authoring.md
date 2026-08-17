---
description: "Ship a custom icon pack from a theme or module: assets, YAML declaration, optional library, cache clear."
tldr: "Place SVG assets at the theme/module root, declare the pack in {name}.icons.yml with extractor/config/settings/template, optionally attach a CSS library, then clear cache. Ship in a theme for site icons, a module for cross-site reuse."
drupal_version: "11.x"
---

# Authoring & Distribution

## When to Use

> Shipping a custom icon pack inside a theme or module.

## Pattern

1. **Place icon assets** at the theme/module root:
   ```
   my_theme/
     icons/
       arrow-left.svg
       arrow-right.svg
       menu.svg
       close.svg
   ```

2. **Declare the pack** in `my_theme.icons.yml` at the theme/module root:
   ```yaml
   my_theme_icons:
     label: "My Theme Icons"
     extractor: svg
     config:
       sources:
         - icons/*.svg
     settings:
       size:
         title: "Size"
         type: integer
         default: 24
       decorative:
         title: "Decorative"
         type: boolean
         default: false
     template: >
       <svg xmlns="http://www.w3.org/2000/svg"
            width="{{ size|default(24) }}" height="{{ size|default(24) }}"
            viewBox="0 0 24 24"
            {% if decorative %}aria-hidden="true"{% endif %}>
         {{ content|raw }}
       </svg>
   ```

3. **(Optional)** Attach a CSS library if your icons need supporting styles (font-face for font extractor, base classes for path extractor):
   ```yaml
   # my_theme.libraries.yml
   icon-styles:
     css:
       theme:
         css/icons.css: {}
   ```

4. **Clear cache** (`drush cr`). Visit the Library admin page to confirm.

## Decision: ship in a theme vs a module

| Scope | Where |
|---|---|
| Icons specific to one theme/site | Inside the theme |
| Icons reusable across sites/themes | Inside a custom module |
| Public distribution | Custom contrib module on drupal.org |

## Common Mistakes

- **Wrong**: editing icon files but not seeing changes → **Right**: clear the `plugin.manager.icon_pack` cache
- **Wrong**: using the same pack_id as an already-installed contrib pack → **Right**: ID collision means one wins unpredictably; prefix pack IDs
- **Wrong**: forgetting to whitelist `<svg>` and `<symbol>` in text formats → **Right**: CKEditor strips them from filtered text if the format's allowed HTML doesn't include them

## See Also

- [Icon Pack Format](pack-format.md)
- [Icon Library Admin](library-admin.md)
- [Pre-built Pack Catalog](pack-catalog.md)
