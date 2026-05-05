---
description: Ship a custom icon pack from a Drupal theme or module for site-specific or cross-site distribution.
tldr: Place SVG assets in the theme/module, declare the pack in {name}.icons.yml at the root, optionally attach a CSS library for font-face or base styles, then clear cache. Ship in a theme for site-specific icons; in a custom module for cross-site reuse; in a contrib module for public distribution.
drupal_version: "11.x"
---

# Authoring & Distribution

## When to Use

> Shipping a custom icon pack inside a theme or module.

## Decision: ship in a theme vs a module

| Scope | Where |
|---|---|
| Icons specific to one theme/site | Inside the theme |
| Icons reusable across sites/themes | Inside a custom module |
| Public distribution | Custom contrib module on drupal.org |

## Pattern

**1. Place icon assets at the theme/module root:**

```
my_theme/
  icons/
    arrow-left.svg
    arrow-right.svg
    menu.svg
    close.svg
```

**2. Declare the pack in `my_theme.icons.yml` at the theme root:**

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

**3. (Optional) Attach a CSS library** for supporting styles (font-face for font extractor, base classes for path extractor):

```yaml
# my_theme.libraries.yml
icon-styles:
  css:
    theme:
      css/icons.css: {}
```

**4. Clear cache** (`drush cr`). Visit the Library admin page to confirm the pack is discovered.

## Common Mistakes

- **Wrong**: editing icon files but not seeing changes → **Right**: clear `plugin.manager.icon_pack` cache
- **Wrong**: using the same pack_id as an already-installed contrib pack → **Right**: always prefix with the theme/module name; ID collisions are unpredictable
- **Wrong**: forgetting to whitelist `<svg>` and `<symbol>` in text formats when icons go through filtered text → **Right**: update the allowed HTML list in affected text formats

## See Also

- [Pack Format](pack-format.md)
- [Pre-built Pack Catalog](pack-catalog.md)
- [Library Admin](library-admin.md)
