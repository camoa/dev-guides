---
description: Overview of Layout Builder and when to use it
drupal_version: "11.x"
---

# Layout Builder Overview

### When to Use

When you need visual layout control for entity displays — sections, multiple columns, block-based composition, per-entity or per-bundle layouts.

### Decision

| If you need... | Use... | Why |
|---|---|---|
| Per-bundle layout with sections and blocks | Layout Builder with defaults | Stored in view display config, exportable, visual editor, no content duplication |
| Per-entity custom layouts | Layout Builder with overrides enabled | Allows individual entities to override default layout, stored in entity field |
| Global site structure (header, footer, sidebars) | Block Layout (core Block system) | Site-wide regions, not entity-specific |
| Structured field-based content composition | Paragraphs module | Content modeling, reusable field collections, revision control at field level |
| Landing pages with full visual control | Layout Builder + Page Manager | Combines layout control with routing/context |

### Pattern

**Core concept**: Layout Builder extends entity view displays with sections. Each section has a layout plugin (defines regions) and components (blocks placed in regions).

```yaml
# core.entity_view_display.node.article.default.yml
third_party_settings:
  layout_builder:
    enabled: true
    allow_custom: false  # true enables per-entity overrides
    sections:
      - layout_id: layout_twocol_section
        layout_settings:
          label: ''
        components:
          - uuid: abc-123-uuid
            region: first
            configuration:
              id: 'field_block:node:article:title'
            weight: 0
```

Reference: `/core/modules/layout_builder/config/schema/layout_builder.schema.yml` for complete config structure.

### Common Mistakes

- **Using LB for site structure** → Use Block Layout for headers/footers (site-wide regions). LB is for entity display, not site architecture
- **Enabling overrides by default** → Start with defaults only. Overrides create maintenance burden — can't update existing content when defaults change
- **Mixing layout concerns** → Use Block Layout for site structure, LB for entity layouts, Paragraphs for content modeling. Each solves different problems
- **Ignoring config export** → LB config is just YAML in entity_view_display. Export it like any config, use recipes for reusable patterns
- **Forgetting about inline block orphans** → Non-reusable blocks persist in DB when removed from layout. Run cron regularly or use cleanup modules

### See Also

- Section 2: Enabling Layout Builder (how to turn it on)
- Section 9: Defaults vs Overrides (when to allow per-entity customization)
- Section 18: Security & Performance (caching, access control)
- Reference: [Layout Builder Overview](https://www.drupal.org/docs/8/core/modules/layout-builder/layout-builder-overview)
