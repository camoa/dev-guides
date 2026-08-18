---
description: UI Icons module — icon pack discovery, picker integrations (Field API, CKEditor 5, UI Patterns, menu, media, Canvas), and Twig rendering in Drupal 11.3+.
tracks:
  - project: ui_icons
    channel: stable
    declared: "2.0.0"
    verified: 2026-08-16
guide-meta:
  concepts:
    - UI Icons
    - ui_icons
    - ui_icons_field
    - ui_icons_ckeditor5
    - ui_icons_patterns
    - ui_icons_menu
    - ui_icons_media
    - ui_icons_library
    - ui_icons_font
    - ui_icons_canvas
    - icon pack
    - "*.icons.yml"
    - icon_preview
    - icon_autocomplete
    - icon_picker
    - drupal-icon
    - icon_embed
    - svg extractor
    - svg_sprite extractor
    - path extractor
    - font extractor
    - icon PropType
    - ui-patterns://icon
    - x-canvas-prop
    - plugin.manager.icon_pack
    - icon_pack_plugin
    - IconDefinition
    - IconExtractorBase
  not:
    - iconify_icons (separate module wrapping the Iconify API)
    - UI Styles (CSS class options — see drupal/ui-styles)
    - UI Skins (CSS variable theming — see drupal/ui-skins)
    - Drupal core Icon API in isolation (UI Icons builds on top of it)
  requires:
    - drupal/ui-patterns
  complements:
    - drupal/ui-patterns
    - drupal/ui-styles
    - drupal/ui-skins
    - drupal/ui-suite-daisyui
    - drupal/canvas
  specializes: ""
  category: drupal
---

# UI Icons

**Philosophy**: Wrap Drupal core's Icon API (11.1+) with discoverable icon-pack plugins, the `font` extractor, and integrations across Field API, CKEditor 5, UI Patterns, Menu links, Media, Drupal Canvas, and Twig — so any icon set becomes available throughout Drupal via one YAML declaration per pack.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what UI Icons does and when to use it vs alternatives | [Overview](overview.md) | Use UI Icons when editors need a picker UI across fields, CKEditor 5, menus, UI Patterns, media, or Canvas — it wraps core's Icon API and adds the font extractor plus every integration. Skip it for one hardcoded icon; use plain SVG. |
| Install UI Icons and enable the right submodules | [Installation](installation.md) | Composer-require drupal/ui_icons, enable it as the engine, then enable submodules per integration needed. Requires core 11.3+/12, PHP 8.3+; iconify_api and backport submodules were removed in 2.0.0. |
| Author an icon pack in YAML (`*.icons.yml`) | [Icon Pack Format](pack-format.md) | Declare pack_id, extractor, config.sources, optional settings, and a required Twig template in {module\|theme}.icons.yml at the extension root. Omitting template throws an exception, not blank output; a library: key is the only way to attach CSS/@font-face to a pack. |
| Choose between path / svg / svg_sprite / font extractors | [Extractors](extractors.md) | Use svg for individual SVG files needing inline content, svg_sprite for a single sprite sheet, path for URL-referenced files, and font (ui_icons_font) for TTF/WOFF packs. Only font ships from UI Icons; the other three live in Drupal core. Never print font content bare — it isn't a glyph. |
| Define configurable per-icon settings (size, color, decorative) | [Settings & Rendering](settings-rendering.md) | Declare settings as typed properties (size, color, decorative, variant); build the template to switch aria-hidden/role/aria-label on a decorative boolean. Always include decorative plus an alt/ariaLabel setting for WCAG compliance. |
| Wire icons into a Drupal field | [Field API Integration](field-api.md) | Enable ui_icons_field and add a ui_icon field; the widget stores pack_id:icon_id in target_id. Per-value settings aren't supported — they live on the formatter. ui_icons_canvas makes the field, and matching SDC props, editable in Canvas. |
| Make an icon prop editable in the Drupal Canvas builder | [Field API Integration](field-api.md) | Enable ui_icons_field and add a ui_icon field; the widget stores pack_id:icon_id in target_id. Per-value settings aren't supported — they live on the formatter. ui_icons_canvas makes the field, and matching SDC props, editable in Canvas. |
| Embed icons inline in CKEditor 5 | [CKEditor 5 Integration](ckeditor5.md) | Enable ui_icons_ckeditor5 + ui_icons_text, add the Icon toolbar button and Embed icon filter to a text format. The passthrough attributes land on a wrapper span, not the pack's own markup, and aria-hidden="false" inverts to a bare aria-hidden — omit it instead. |
| Use icons as UI Patterns props | [UI Patterns Integration](patterns.md) | Enable ui_icons_patterns to register the icon PropType (pack_id, icon_id, settings) and four data sources. An icon prop is plain data, not a renderable — call icon(prop.pack_id, prop.icon_id, prop.settings) in the template, or use a slot fed by icon_renderable. |
| Attach icons to menu links | [Menu Integration](menu.md) | Enable ui_icons_menu to add an icon widget to the menu_link_content form. Three hooks inject the icon markup into link titles automatically — no preprocess or template override is needed, and there is no data-icon-id attribute to read. |
| Render icons in Twig templates | [Twig Rendering](twig.md) | Use core's icon(pack_id, icon_id, settings) as the general renderer in theme templates; needs no contrib module. icon_preview() is the admin-preview renderer and forces size 48 (not the pack's own default) when settings are omitted. |
| Add icons to media entities | [Media Integration](media.md) | Enable ui_icons_media and create a media type with source plugin Icon; each entity stores pack_id:icon_id plus optional settings. Use Field API or CKEditor integrations instead when reuse across pages isn't needed. |
| Browse all packs in the admin UI | [Library Admin](library-admin.md) | Enable ui_icons_library and visit /admin/appearance/ui/icons to browse packs and preview icons with a fuzzy search bar. Requires access ui icons library; clear cache after adding icons since YamlDiscovery caches pack contents. |
| Ship a custom icon pack from a theme/module | [Authoring & Distribution](authoring.md) | Place SVG assets at the theme/module root, declare the pack in {name}.icons.yml with extractor/config/settings/template, then clear cache. A CSS library needs two edits — declare it AND point the pack's library: key at it, or nothing attaches. |
| Find pre-built community icon packs | [Pre-built Pack Catalog](pack-catalog.md) | The UI Icons Example repository provides starting-point *.icons.yml declarations for Bootstrap Icons, Heroicons, Lucide, FontAwesome, and more — copy, adapt, add the icon files. Several UI Suite themes already bundle a pack. |
| Avoid common mistakes (caching, a11y, SVG XSS) | [Anti-Patterns](anti-patterns.md) | Never trust SVG as fully sanitized — UI Icons does not strip <script> tags. Always prefix pack IDs, clear cache after file changes, declare decorative/ariaLabel settings, and enable only the integrations a site actually uses. |
| Find key classes and services | [Code Reference](code-reference.md) | Core service is plugin.manager.icon_pack; UI Icons adds ui_icons.search and ui_icons.twig_extension. Form elements: icon_autocomplete, icon_picker. Cache tags: icon_pack_plugin, icon_pack_collector. No .module files since 2.0.0. |
