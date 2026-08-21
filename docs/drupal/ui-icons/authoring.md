---
description: "Ship a custom icon pack from a theme or module: assets, YAML declaration, library wiring, cache clear."
tldr: "Place SVG assets at the theme/module root, declare the pack in {name}.icons.yml with extractor/config/settings/template, then clear cache. A CSS library needs two edits — declare it AND point the pack's library: key at it, or nothing attaches."
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
            viewBox="{{ attributes.viewBox|default('0 0 24 24') }}"
            {% if decorative %}aria-hidden="true"{% endif %}>
         {{ content|raw }}
       </svg>
   ```

3. **(Optional)** Attach a CSS library if your icons need supporting styles (`@font-face` for the font extractor, base classes for the path extractor). This is **two** edits, and the second is the one people miss:
   ```yaml
   # my_theme.libraries.yml
   icon-styles:
     css:
       theme:
         css/icons.css: {}
   ```
   ```yaml
   # my_theme.icons.yml — reference it from the pack
   my_theme_icons:
     library: my_theme/icon-styles
     # …
   ```
   Declaring the library alone attaches nothing. `Icon::preRenderIcon()` attaches only what `IconDefinition::getLibrary()` returns, which is the pack's `library:` key; `IconPreview::getPreview()` does the same for admin previews.

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
- **Wrong**: declaring a library in `*.libraries.yml` and stopping there → **Right**: point the pack's `library:` key at it, or nothing is ever attached

## See Also

- [Icon Pack Format](pack-format.md)
- [Icon Library Admin](library-admin.md)
- [Pre-built Pack Catalog](pack-catalog.md)
