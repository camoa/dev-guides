---
description: Ship a custom theme with its own UI Styles definitions tied to the theme's CSS libraries.
tldr: Place {theme}.ui_styles.yml at the theme root (not a subdirectory); clear cache after creation. Prefix plugin IDs with the theme name. Subthemes inherit parent UI Styles and add to them; suppress parent styles with enabled: false on the same plugin ID.
drupal_version: "11.x"
---

# Theme Authoring

## When to Use

> Use this guide when shipping a custom theme (Radix sub-theme, Olivero sub-theme, fully custom) with its own UI Styles definitions tied to the theme's CSS.

## Pattern

1. **Declare CSS** in `{theme}.libraries.yml`:
   ```yaml
   global-styling:
     css:
       theme:
         css/utilities.css: {}
   ```

2. **Author utilities** in `css/utilities.css` (or generate with Tailwind/PostCSS):
   ```css
   .text-primary { color: var(--brand-primary); }
   .text-secondary { color: var(--brand-secondary); }
   ```

3. **Declare UI Styles** in `{theme}.ui_styles.yml`:
   ```yaml
   mytheme_text_color:
     label: "Text color"
     category: "Typography"
     options:
       text-primary: "Primary"
       text-secondary: "Secondary"
   ```

4. **Clear cache** — UI Styles' YamlDiscovery picks up the new file.

### Subtheme Inheritance

Subthemes automatically inherit parent theme UI Styles. Subtheme-declared styles add to parent styles unless the subtheme declares the same plugin ID with `enabled: false`.

## Common Mistakes

- **Declaring styles whose CSS classes aren't in any library attached to pages** → The class injects but has no effect. Ensure the library is attached globally (`info.yml` `libraries:` key) or per-context
- **Putting UI Styles YAML in a subdirectory** → File must sit at the theme root: `themes/custom/mytheme/mytheme.ui_styles.yml`. Subdirectories are not scanned

## See Also

- [Style Definition Format](definition-format.md)
- [Overriding & Disabling](overriding.md)
- [Stylesheet Generation](stylesheet-generation.md)
