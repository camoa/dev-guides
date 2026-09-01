---
description: "Icon API - unified system for managing and rendering icons across Drupal 11.1+ sites"
tracks:
  - project: drupal
    channel: stable
    verified: 2026-02-13
guide-meta:
  concepts:
    - Icon API
    - icon packs
    - SVG extractor
    - SVG sprite extractor
    - font extractor
    - path extractor
    - Twig icon function
    - SDC icon props
    - IconPackManager
  not:
    - Font Awesome module
    - manual SVG include
    - CSS icon sprites
  requires:
    - drupal/sdc
  complements:
    - drupal/twig
    - drupal/ui-patterns
  category: drupal
---

# Icon API

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the Icon API system | [What is Icon API](what-is-icon-api.md) | You need a unified, performant system for managing icons across Drupal 11.1+ rather than hand-rolling SVG, icon fonts, or external resources in templates and CSS; Icon API's PHP classes are marked experimental/internal, so treat *.icons.yml and icon() as the stable surface. |
| Understand icon pack discovery and lifecycle | [Icon Pack Architecture](icon-pack-architecture.md) | You need to understand how icon packs are discovered, loaded, and rendered; schema validation only runs when justinrainbow/json-schema is installed, and the render element carries no #cache of its own. |
| Create a new icon pack in YAML | [Icon Pack Definition](icon-pack-definition.md) | You're creating a new icon pack and need the full YAML structure; only extractor and template are schema-required, and settings: default: values never reach the Twig template — repeat them with \|default(). |
| Choose the right extractor for my icons | [Choosing Extractors](choosing-extractors.md) | Select the right extractor by icon source and remoteness; svg_sprite cannot read a remote sprite (discovers zero icons, silently), and local sources are restricted to svg/png/gif. |
| Use individual SVG files | [SVG Extractor](svg-extractor.md) | You have local SVG files and want automatic discovery and template-controlled inline rendering; the extractor does not sanitize — it only refuses remote sources, so treat every file in the pack as trusted code. |
| Use SVG sprite files for large icon sets | [SVG Sprite Extractor](svg-sprite-extractor.md) | You have a large local SVG sprite and want one cached request for every icon; remote sprites cannot work — IconFinder refuses any URI with a scheme, so a CDN sprite source discovers nothing. |
| Use any image format or remote sources | [Path Extractor](path-extractor.md) | You need to reference icon files by URL — local svg/png/gif or any remote format; path never reads the file server-side, and {icon_id} is not expanded in remote URLs, so one URL means one icon. |
| Integrate existing icon fonts | [Font Extractor](font-extractor.md) | You have an icon font with codepoint metadata and want it in Icon API via the UI Icons contrib module; .woff2 sources are silently skipped, and {{ content }} exists only for .codepoints sources — guard it with \|default(icon_id). |
| Add icon fields, menu icons, or CKEditor integration | [UI Icons Module Features](ui-icons-module-features.md) | You need icon fields, menu icons, or CKEditor embedding beyond core rendering; link-field icons ship from ui_icons_field (no separate Link submodule), and ui_icons_ckeditor5 needs ui_icons_text to actually render the embed. |
| Understand template variables | [Template Variables](template-variables.md) | You're writing icon pack templates and need the real variable set; caller settings override extractor data but icon_id/source always win, and the pack definition's own keys (label, provider, ...) leak into context too. |
| Render icons in Twig templates | [Twig Icon Function](twig-icon-function.md) | icon(pack_id, icon_id, settings) is the only signature; icon('pack:id') is a fatal ArgumentCountError/TypeError on every Drupal 11 release, never a deprecation — a missing icon just returns [] with no error. |
| Build SDC components with icon props | [SDC Icon Props](sdc-icon-props.md) | You're building SDC components that need configurable icon props; YAML default: is never applied and required: runs behind assert(), off in production — write the Twig so it's correct with no props declared at all. |
| Use icon slots in components | [Icon Slots](icon-slots.md) | Your component needs maximum icon flexibility via slots; under {% embed %} a slot value arrives as a Twig block, so {% if icon %}{{ icon }}{% endif %} is silently false — render every slot as {% block name %}{% endblock %}. |
| Access icons programmatically in PHP | [IconPackManager Service](iconpackmanager-service.md) | You need programmatic icon access in PHP; getIcons() returns discovery arrays with no label (call getIcon()->getLabel() for that), and the render element properties are #pack_id/#icon_id — #pack/#icon renders nothing, raises nothing. |
| Understand icon caching | [Caching Strategy](caching-strategy.md) | Icon pack definitions cache in cache.discovery under cid icon_pack (icon_pack_plugin is a tag, not the cid); nothing watches *.icons.yml file changes, and the icon render element itself adds no #cache — add your own on the parent. |
| Optimize icon performance | [Performance Best Practices](performance-best-practices.md) | Pick the extractor by repetition, not icon count: svg is 0 HTTP requests since it inlines server-side, so 'switch to sprites to cut requests' is backwards — sprites only win when one icon repeats many times on a page. |
| Handle SVG security and optimization | [SVG Security & Performance](svg-security-performance.md) | Core does not sanitize SVG anywhere; the svg extractor inlines file contents unescaped and only refuses remote sources, so review every file you ship as trusted code — never route user uploads through Icon API. |
| Secure remote icon sources | [Remote Resource Security](remote-resource-security.md) | path records a URL and the visitor's browser fetches it; svg filters remote sources out; svg_sprite accepts a remote source and then reads zero icons. SSRF applies only to a custom extractor you write that calls httpClient(). |
| Debug icon discovery issues | [Troubleshooting Icon Discovery](troubleshooting-icon-discovery.md) | Icons aren't appearing or pack IDs aren't resolving; without justinrainbow/json-schema, validateDefinition() returns TRUE unconditionally and a bad pack fails later at render time with IconPackConfigErrorException instead. |
| Debug template rendering issues | [Debugging Templates](debugging-templates.md) | Icons render incorrectly or content is missing; source files for the svg extractor must be full <svg> documents with a single root — two root nodes fails simplexml_load_string() and the icon renders as nothing. |
| Migrate from existing icon systems | [Migration Patterns](migration-patterns.md) | Migrating to Icon API from manual markup, an icon font, or image files; search-and-replacing old markup into icon('pack:id') is fatal — the Twig function always takes pack and icon as two separate arguments. |
| Build a custom extractor plugin | [Custom Extractor Development](custom-extractor-development.md) | Core/contrib extractors don't cover your source; discoverIcons() must key by the full pack_id:icon_id or the icon lists but never renders, and overriding loadIcon() with a different signature is fatal at class load. |
