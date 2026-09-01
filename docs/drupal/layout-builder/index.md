---
description: Drupal Layout Builder development guides — configuration-first approach to sections, layouts, blocks, styles, and deployment.
guide-meta:
  concepts:
    - Layout Builder
    - layout sections
    - layout plugins
    - inline blocks
    - reusable blocks
    - LB Styles
    - style groups
    - defaults vs overrides
    - LB restrictions
    - custom layout plugins
  not:
    - block plugins (see drupal/blocks)
    - Canvas page builder (see drupal/canvas)
    - Paragraphs
  requires:
    - drupal/blocks
  complements:
    - drupal/blocks
    - drupal/ui-patterns
    - drupal/sdc
    - design-systems/radix-sdc
  category: drupal
tracks:
  - project: layout_builder_styles
    channel: stable
    declared: 2.1.0
    verified: 2026-07-01
---

# Layout Builder

**Philosophy**: Configuration-first approach. Layout Builder configuration lives in `core.entity_view_display.*.yml` with sections and components. Understand config schema, prioritize defaults over overrides, and use config management for deployment.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what Layout Builder does and when to use it | [Overview](lb-overview.md) | When you need visual layout control for entity displays — sections, multiple columns, block-based composition, per-entity or per-bundle layouts. |
| Enable LB on a content type or entity view mode | [Enabling Layout Builder](enabling-lb.md) | Enable LB via UI, config YAML, or enableLayoutBuilder(). For editor handoff grant three perms: configure any layout + create custom blocks + per-bundle editable overrides. Export the role config or editors lose access after deploy. |
| Read and edit LB configuration YAML | [Config Schema](lb-config-schema.md) | When reading, editing, or generating Layout Builder configuration in YAML files, understanding config structure for recipes, programmatic manipulation, or debugging. |
| Understand section structure and layout plugins | [Sections & Layouts](sections-layouts.md) | Sections (Section value object + layout plugin + regions) structure LB displays. Group components sharing section-level CSS into ONE section—style classes apply at the wrapper. Storage: Defaults (view display) or Overrides (entity field). |
| Find available core layout plugins | [Core Layout Plugins](core-layout-plugins.md) | When selecting a layout for a section or creating custom layouts based on core patterns. |
| Add blocks to layouts programmatically | [Block Placement](block-placement.md) | When adding blocks to Layout Builder sections programmatically, understanding component structure, or manipulating block configuration. |
| Decide between inline and reusable blocks | [Inline vs Reusable](inline-vs-reusable.md) | When deciding between non-reusable inline blocks (created within Layout Builder) and reusable block content entities. |
| Expose entity fields as blocks in layouts | [Field & Extra Field Blocks](field-extra-field-blocks.md) | When exposing entity field data or extra fields (pseudo-fields) as blocks in Layout Builder layouts. |
| Build repeating list components (testimonials, galleries) without Paragraphs | [Block Content List Components](block-content-list-components.md) | Use atomic block_content bundles + taxonomy + block_content_field_data View for LB list items (no Paragraphs). One ViewsBlock display per category (fixed arg). Register the three-hook block_content theme trio to enable per-bundle Twig templates. |
| Choose between default layouts and per-entity overrides | [Defaults vs Overrides](defaults-vs-overrides.md) | Use allow_custom:false for consistency bundles, allow_custom:true + restrictions for curated editor bundles — posture is per-bundle. Overrides are content, not config; default changes don't propagate to overridden entities. |
| Restrict which blocks editors can add | [Layout Builder Restrictions](lb-restrictions.md) | Use Layout Builder Restrictions (3.0.4, D11-compatible) to limit blocks/layouts per bundle; allowlist lives in third_party_settings.layout_builder_restrictions on the view-display config. Restrictions are UI governance, not access control. |
| Apply CSS classes to sections and blocks | [Layout Builder Styles Overview](lb-styles-overview.md) | When you need to apply CSS classes to Layout Builder sections (layouts) or components (blocks) without creating custom plugins. Layout Builder Styles provides a config entity system for defining reusable style options that editors select… |
| Create style groups and styles via YAML config | [Style Groups Config](lb-styles-groups.md) | Style groups organize related styles into categories (e.g., "Padding", "Background Color", "Border Style"). Editors see one form element per group, making the UI manageable when you have many styles. |
| Define individual styles with restrictions | [Style Definitions](lb-styles-definitions.md) | Individual styles define CSS classes to apply, which blocks/sections can use them, and which group they belong to. Styles are config entities exported as YAML for deployment via config sync. |
| Integrate LB Styles with Bootstrap/Radix | [Bootstrap Integration](lb-styles-bootstrap.md) | When using Bootstrap-based themes (Radix, Bootstrap Barrio), map Layout Builder Styles to Bootstrap utility classes for consistent design system integration. Avoids custom CSS for common patterns. |
| Extend LB Styles programmatically | [Extending LB Styles](lb-styles-extending.md) | When you need to programmatically alter which styles are available, modify CSS classes before rendering, or integrate custom logic into the style selection process. |
| Use UI Patterns as LB layouts + UI Styles | [UI Patterns Layouts & UI Styles Integration](ui-patterns-layouts.md) | When you want SDC components to serve as Layout Builder section layouts without writing custom `*.layouts.yml` or `LayoutDefault` plugins. Also covers UI Styles module as an alternative to Layout Builder Styles for CSS class management. |
| Create custom layout plugins | [Custom Layout Plugins](custom-layout-plugins.md) | When core layouts don't provide the regions or structure you need, or when you want theme-specific layouts. |
| React to layout rendering with events | [Events & Hooks](lb-events-hooks.md) | When you need to alter layout rendering, modify section/component behavior, or integrate custom logic during layout building. |
| Export and deploy LB configuration | [Config Export & Recipes](lb-config-recipes.md) | When deploying Layout Builder configuration across environments, creating reusable layout patterns, or managing LB config in version control. |
| Style LB admin UI and frontend output | [Theming Layout Builder](theming-lb.md) | Override layout templates in templates/layout/ and use attributes.addClass(). Any inline-block template MUST output {{ attributes }} and {{ title_suffix }} — omitting either silently breaks LB contextual edit and the Configure menu. |
| Harden the editor form display before handing Layout Builder to content editors | [Editor Form-Display Hardening](editor-form-display-hardening.md) | Harden the form display (separate config from view display) before editor handoff: set media_library_widget, hide legacy fields via hidden:, add descriptions. Applies to both node bundles and block_content inline-block bundles. |
| Follow configuration-first best practices | [Best Practices](best-practices.md) | When establishing Layout Builder workflows, governance, or making architectural decisions. |
| Avoid common mistakes | [Anti-Patterns](anti-patterns.md) | When you need to know what NOT to do — these are patterns that seem logical but cause problems. |
| Understand security and performance implications | [Security & Performance](security-performance.md) | When hardening Layout Builder against security issues, optimizing performance, or auditing for vulnerabilities. |
| Find key classes and files | [Code Reference Map](code-reference-map.md) |  |
| Check sources and version history | [Sources & Maintenance](sources-maintenance.md) |  |
