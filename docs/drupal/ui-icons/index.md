---
description: UI Icons module — icon pack discovery, picker integrations (Field API, CKEditor 5, UI Patterns, menu, media), and Twig rendering in Drupal 11.1+.
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
    - icon pack
    - *.icons.yml
    - icon_preview
    - icon_autocomplete
    - icon_picker
    - drupal-icon
    - icon_embed
    - svg extractor
    - svg_sprite extractor
    - path extractor
    - font extractor
    - ui:icon PropType
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
  specializes: ""
  category: drupal
---

# UI Icons

**Philosophy**: Wrap Drupal core's Icon API (11.1+) with discoverable icon-pack plugins, prebuilt extractors, and integrations across Field API, CKEditor 5, UI Patterns, Menu links, Media, and Twig — so any icon set becomes available throughout Drupal via one YAML declaration per pack.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what UI Icons does and when to use it vs alternatives | [Overview](overview.md) | Use UI Icons when editors need a picker UI across fields, body text, menu links, or components. Skip it for a single hardcoded icon; use plain SVG instead. UI Icons wraps Drupal core's Icon API and adds all integrations — it is the UX layer, not the engine. |
| Install UI Icons and enable the right submodules | [Installation](installation.md) | Require drupal/ui_icons via Composer and enable only the submodules for integrations the site uses. Enabling ui_icons_ckeditor5 without ui_icons_text leaves drupal-icon tags unrendered. |
| Author an icon pack in YAML (`*.icons.yml`) | [Icon Pack Format](pack-format.md) | Place {name}.icons.yml at the theme/module root; prefix pack_id with the theme/module name to avoid collisions. Declare extractor, config.sources, optional settings, and a Twig template — omitting template leaves icons discoverable but rendering as empty markup. |
| Choose between path / svg / svg_sprite / font extractors | [Extractors](extractors.md) | Use svg for individual SVG files with inline content, svg_sprite for a single sprite sheet, path for URL-referenced files, and font for TTF/WOFF packs. Sprite extractor requires symbol elements; font extractor requires dompdf/php-font-lib or a codepoints/json/yml metadata file. |
| Define configurable per-icon settings (size, color, decorative) | [Settings & Rendering](settings-rendering.md) | Declare settings as JSON Schema properties; build the template to toggle aria-hidden/role/aria-label based on a decorative boolean. Always include decorative and an alt/ariaLabel setting for WCAG compliance. |
| Wire icons into a Drupal field | [Field API Integration](field-api.md) | Enable ui_icons_field and add an Icon field (type ui_icon); the widget stores pack:icon_id plus settings. Also enhances the core Link field with icon_link_widget and icon_link_formatter. |
| Embed icons inline in CKEditor 5 | [CKEditor 5 Integration](ckeditor5.md) | Enable ui_icons_ckeditor5 and ui_icons_text, then add the Icon toolbar button and Embed icon filter to each text format. The toolbar button without the filter leaves drupal-icon tags as raw text. |
| Use icons as UI Patterns props | [UI Patterns Integration](patterns.md) | Enable ui_icons_patterns to register the ui:icon PropType and four data sources. Declare icon props as type: ui:icon in component YAML; render via {{ prop_name }} in the template. |
| Attach icons to menu links | [Menu Integration](menu.md) | Enable ui_icons_menu to add the icon widget to the menu_link_content form. Icons do not render automatically — override menu.html.twig or write a preprocess hook to extract icon data and call icon_preview(). |
| Render icons in Twig templates | [Twig Rendering](twig.md) | Use icon_preview(pack_id, icon_id, settings) with three separate arguments — not the combined pack:icon_id string. Cache metadata bubbles correctly. |
| Add icons to media entities | [Media Integration](media.md) | Enable ui_icons_media and create a media type with source plugin Icon for true cross-page reuse. Use Field API or CKEditor integrations when reuse is not needed. |
| Browse all packs in the admin UI | [Library Admin](library-admin.md) | Enable ui_icons_library and visit /admin/appearance/ui-libraries/icons. Icon counts update only after clearing cache. |
| Pick between UI Styles, UI Skins, UI Icons for a concern | [Decision Rule](../ui-styles/decision-rule.md) | Q1/Q2/Q3 dispatch. **Scope clarification**: UI Icons handles pack REGISTRATION; per-instance icon CHOICE is handled by UI Patterns icon prop, Drupal Icon field, CKEditor 5 icon embed filter, or menu icon widget. |
| Ship a custom icon pack from a theme or module | [Authoring & Distribution](authoring.md) | Place SVG assets at the theme/module root, declare the pack in {name}.icons.yml, optionally attach a CSS library, then clear cache. Ship in a theme for site-specific icons, in a module for reuse. |
| Find pre-built community icon packs | [Pre-built Pack Catalog](pack-catalog.md) | The UI Icons Example repository provides ready-to-use YAML declarations for Bootstrap Icons, Heroicons, FontAwesome, and others. Several UI Suite themes bundle packs. Copy assets locally for production reliability. |
| Avoid common mistakes (caching, a11y, SVG XSS) | [Anti-Patterns](anti-patterns.md) | The most critical mistakes are trusting unvetted SVG, missing the icon_embed filter, using generic pack IDs, and skipping accessibility settings. |
| Find key classes and services | [Code Reference](code-reference.md) | Core services are plugin.manager.icon_pack and ui_icons.twig_extension. Form elements are icon_autocomplete and icon_picker. Cache tags are icon_pack_plugin and icon_pack_collector. |
