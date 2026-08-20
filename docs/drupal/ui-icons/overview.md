---
description: "When to use UI Icons vs core Icon API, raw SVG, or custom field types in Drupal — verified against 1.1.2, with 2.0.0 claims flagged."
tldr: "Use UI Icons when editors need a picker UI across fields, CKEditor 5, menus, UI Patterns, media, or Canvas. Documents 2.0.0 but verified only against 1.1.2 — 2.0.0-only claims (Canvas, submodule set, core range) are unverified."
drupal_version: "11.x"
---

# UI Icons Overview

> **Verification status — this topic documents 2.0.0 but was verified against 1.1.2.**
> The reference site this guide is audited against runs **UI Icons 1.1.2**, and 2.0.0 cannot be
> installed on it: `ui_suite_daisyui 5.0.0-alpha6` — the newest release of that theme in
> existence — requires `drupal/ui_icons: ^1.1`, so Composer refuses the bump. (The
> `ui_icons_patterns 2.0.0` that appears in a lock file is a Composer **metapackage** with no
> code; it requires `drupal/ui_icons: "*"` and resolves happily against 1.1.2.)
>
> Everything below that is **specific to 2.0.0** is therefore drawn from release notes, not from
> reading 2.0.0 source. Treat these as unverified until someone installs 2.0.0: the submodule
> inventory and its dependency directions ([Installation](installation.md)), the `^11.3 || ^12.0`
> compatibility assertion ([Installation](installation.md)), the removal of `ui_icons_backport` /
> `ui_icons_iconify_api` and the `ui_icons_update_11201()` cleanup ([Installation](installation.md)),
> the `ui_icons_canvas` submodule and its `x-canvas-prop` shape routing
> ([Field API Integration](field-api.md)), `IconType::mainPropertyName()` / `IconType::ICON_ID_PCRE`
> ([Field API Integration](field-api.md)), and the claim that the project ships no `.module` files
> ([Code Reference](code-reference.md)).
>
> What **is** verified first-hand, against 1.1.2 and against Drupal core 11.4.5, is the part of
> this guide that is not version-specific: the icon-pack YAML format, all four extractors and
> their template variables, the settings schema, the UI Patterns PropType and its four sources,
> the CKEditor 5 / text-filter behaviour, the menu integration, `icon()` vs `icon_preview()`, and
> the core Icon API surface. Where 1.1.2 actively contradicts a 2.0.0 claim, this guide says so
> inline.

## When to Use

> Use UI Icons when icons must be picker-selectable by editors across fields, body text, menu links, components, or media — and you want one source of truth for which packs are available. Use plain `<svg>` or `attach_library` when only a single icon is hardcoded into one theme template.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Icon picker in Field API | UI Icons (`ui_icon` field type) | Built-in autocomplete and modal picker |
| Inline icons in WYSIWYG body content | UI Icons + `ui_icons_ckeditor5` | `<drupal-icon>` tag + filter, no manual SVG paste |
| Just one icon hardcoded into a template | Plain `<svg>` or `attach_library` | UI Icons is overkill for a single icon |
| Replace deprecated Fontawesome Icon Picker | UI Icons | Modern successor, plugin-based, framework-agnostic |
| Programmatic Drupal Icon API access only | Drupal core's `plugin.manager.icon_pack` | UI Icons is the UX/integration layer; core API is the engine |
| SVG packs rendered from Twig, no picker needed | Drupal core alone | Core already ships the `path`, `svg`, and `svg_sprite` extractors, the `icon()` Twig function, and the `#type: icon` element |
| Icons via media entities | UI Icons + `ui_icons_media` | Stores icon refs as media for reuse |
| Icon props editable in the Drupal Canvas builder | UI Icons + `ui_icons_canvas` | Registers the Canvas widget transform and the `x-canvas-prop: ui-icon` shape (2.0.0-only, unverified — see caveat above) |

## Pattern

An icon pack is a YAML plugin declaring a unique `pack_id`, an extractor (`path`, `svg`, `svg_sprite`, `font`), a `config.sources` glob/path list, optional `settings`, and a `template`:

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
         viewBox="{{ attributes.viewBox|default('0 0 24 24') }}"
         width="{{ size|default(24) }}"
         height="{{ size|default(24) }}"
         aria-hidden="true">
      {{ content|raw }}
    </svg>
```

After clearing cache, every icon in `my_theme/icons/*.svg` is available as `my_theme_icons:{filename}` across Field API, CKEditor 5, UI Patterns, menu links, media, and Canvas.

## Relationship to Drupal Core Icon API (11.1+)

Drupal 11.1+ ships a built-in Icon API (`\Drupal\Core\Theme\Icon\*`) — `IconDefinition`, `IconPackManagerInterface`, `IconExtractorBase`, attribute discovery for `#[IconExtractor]` plugins, the `plugin.manager.icon_pack` service, the `path`/`svg`/`svg_sprite` extractors (in `core/lib/Drupal/Core/Theme/Plugin/IconExtractor/`), the `#type: icon` render element, and the `icon()` Twig function.

UI Icons does **not** replace this API — it builds on it: adds the **`font`** extractor (the only extractor the module itself ships, in `ui_icons_font`), form elements (`icon_autocomplete`, `icon_picker`), Field API + CKEditor 5 + UI Patterns + Menu + Media + Canvas + Filter integrations, an admin Icon Library browser, and a Twig `icon_preview()` function for admin previews (core's general-purpose renderer is `icon()` — see [Twig Rendering](twig.md)).

UI Icons 2.0 requires core `^11.3 || ^12.0`; the Icon API itself has been in core since 11.1.

## Common Mistakes

- **Wrong**: reaching for raw `<svg>` in Twig templates when icons need to be editor-pickable → **Right**: use UI Icons; the picker UX is the value
- **Wrong**: confusing UI Icons with Iconify integration → **Right**: `iconify_icons` is a separate module wrapping the Iconify API; UI Icons supports any icon source via extractors
- **Wrong**: expecting icons in CKEditor without enabling the filter → **Right**: enable "Embed icon" on every text format that should support inline icons
- **Wrong**: applying a 2.0.0-only claim from this guide to a 1.x site without checking → **Right**: 1.1.2 and 2.0.0 diverge on the submodule inventory, dependency graph, and core compatibility range — read your own `.info.yml` first

## See Also

- [Installation](installation.md)
- [Icon Pack Format](pack-format.md)
- [Extractors](extractors.md)
- Reference: https://www.drupal.org/project/ui_icons
