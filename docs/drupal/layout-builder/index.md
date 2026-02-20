---
description: Drupal Layout Builder development guides — configuration-first approach to sections, layouts, blocks, styles, and deployment.
---

# Layout Builder

**Philosophy**: Configuration-first approach. Layout Builder configuration lives in `core.entity_view_display.*.yml` with sections and components. Understand config schema, prioritize defaults over overrides, and use config management for deployment.

## I Need To...

| Task | Guide |
|------|-------|
| Understand what Layout Builder does and when to use it | [Overview](lb-overview.md) |
| Enable LB on a content type or entity view mode | [Enabling Layout Builder](enabling-lb.md) |
| Read and edit LB configuration YAML | [Config Schema](lb-config-schema.md) |
| Understand section structure and layout plugins | [Sections & Layouts](sections-layouts.md) |
| Find available core layout plugins | [Core Layout Plugins](core-layout-plugins.md) |
| Add blocks to layouts programmatically | [Block Placement](block-placement.md) |
| Decide between inline and reusable blocks | [Inline vs Reusable](inline-vs-reusable.md) |
| Expose entity fields as blocks in layouts | [Field & Extra Field Blocks](field-extra-field-blocks.md) |
| Choose between default layouts and per-entity overrides | [Defaults vs Overrides](defaults-vs-overrides.md) |
| Restrict which blocks editors can add | [Layout Builder Restrictions](lb-restrictions.md) |
| Apply CSS classes to sections and blocks | [Layout Builder Styles Overview](lb-styles-overview.md) |
| Create style groups and styles via YAML config | [Style Groups Config](lb-styles-groups.md) |
| Define individual styles with restrictions | [Style Definitions](lb-styles-definitions.md) |
| Integrate LB Styles with Bootstrap/Radix | [Bootstrap Integration](lb-styles-bootstrap.md) |
| Extend LB Styles programmatically | [Extending LB Styles](lb-styles-extending.md) |
| Use UI Patterns as LB layouts + UI Styles | [UI Patterns Layouts & UI Styles Integration](ui-patterns-layouts.md) |
| Create custom layout plugins | [Custom Layout Plugins](custom-layout-plugins.md) |
| React to layout rendering with events | [Events & Hooks](lb-events-hooks.md) |
| Export and deploy LB configuration | [Config Export & Recipes](lb-config-recipes.md) |
| Style LB admin UI and frontend output | [Theming Layout Builder](theming-lb.md) |
| Follow configuration-first best practices | [Best Practices](best-practices.md) |
| Avoid common mistakes | [Anti-Patterns](anti-patterns.md) |
| Understand security and performance implications | [Security & Performance](security-performance.md) |
| Find key classes and files | [Code Reference Map](code-reference-map.md) |
| Check sources and version history | [Sources & Maintenance](sources-maintenance.md) |
