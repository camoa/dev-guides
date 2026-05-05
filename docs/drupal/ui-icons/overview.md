---
description: When to use UI Icons vs core Icon API, raw SVG, or custom field types in Drupal 11.1+.
tldr: Use UI Icons when you need a consistent icon picker UX across Field API, CKEditor 5, menu links, and components — it wraps Drupal core's Icon API (11.1+) and adds all integrations. Skip it for a single hardcoded icon in one template; use plain SVG instead.
drupal_version: "11.x"
---

# UI Icons Overview

## When to Use

> Use UI Icons when icons must be picker-selectable by editors across fields, body text, menu links, or components — and you want one source of truth for which packs are available. Use plain `<svg>` or `attach_library` when only a single icon is hardcoded into one theme template.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Icon picker in Field API | UI Icons (`ui_icon` field type) | Built-in autocomplete and modal picker |
| Inline icons in WYSIWYG body content | UI Icons + ui_icons_ckeditor5 | `<drupal-icon>` tag + filter; no manual SVG paste |
| Just one icon hardcoded in a template | Plain `<svg>` or `attach_library` | UI Icons is overkill for a single icon |
| Replace deprecated FontAwesome Icon Picker | UI Icons | Modern successor, plugin-based, framework-agnostic |
| Programmatic Icon API access only | Drupal core's `plugin.manager.icon_pack` | UI Icons is the UX/integration layer; core is the engine |
| Icons via media entities | UI Icons + ui_icons_media | Stores icon refs as media for reuse |

## Pattern

An icon pack is a YAML plugin declaring a unique `pack_id`, an extractor, a `config.sources` glob, optional `settings`, and a `template`:

```yaml
# my_theme.icons.yml
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
  template: >
    <svg xmlns="http://www.w3.org/2000/svg"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         aria-hidden="true">
      {{ content|raw }}
    </svg>
```

After clearing cache, every icon in `my_theme/icons/*.svg` is available as `my_theme_icons:{filename}` across all integrations.

## Relationship to Drupal Core Icon API (11.1+)

UI Icons **builds on** Drupal core's Icon API — it does not replace it:

| Layer | Responsibility |
|---|---|
| Drupal core (`plugin.manager.icon_pack`) | `IconDefinition`, `IconExtractorBase`, plugin discovery |
| UI Icons | Prebuilt extractors (path/svg/svg_sprite/font), form elements, Field/CKEditor/Patterns/Menu/Media/Filter integrations, admin Library browser |

For Drupal 10.4–11.0 use UI Icons 1.0.x (includes `ui_icons_backport`). For Drupal 11.1+ use UI Icons 1.1.x (backport submodule is empty/deprecated).

## Common Mistakes

- **Wrong**: reaching for raw `<svg>` in Twig when icons need to be editor-pickable → **Right**: use UI Icons; the picker UX is the value
- **Wrong**: confusing UI Icons with Iconify integration → **Right**: `iconify_icons` is a separate module; UI Icons supports any icon source via extractors
- **Wrong**: expecting CKEditor icons without enabling the filter → **Right**: enable "Embed icon" filter on every text format that should support inline icons

## See Also

- [Installation](installation.md)
- [Icon Pack Format](pack-format.md)
- [Extractors](extractors.md)
- Reference: https://www.drupal.org/project/ui_icons
