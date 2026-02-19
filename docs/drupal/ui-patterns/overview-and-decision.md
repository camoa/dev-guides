---
description: UI Patterns Overview & Decision — when to use UI Patterns vs SDC alone
drupal_version: "11.x"
---

# UI Patterns Overview & Decision

## When to Use

> Use UI Patterns when site-builders need to configure components via Drupal's UI. Use SDC alone when components are consumed only by developers in Twig templates.

## Decision

| Scenario | Recommendation |
|----------|---------------|
| Site-builders need to configure components via UI | **Use UI Patterns** — this is its core purpose |
| Components used only in Twig templates by developers | SDC alone is sufficient; UI Patterns adds unnecessary overhead |
| Layout Builder sections need component-based layouts | **Use UI Patterns Layouts** sub-module |
| Views rows/styles need component rendering | **Use UI Patterns Views** sub-module |
| Field formatters should render through components | **Use UI Patterns Field Formatters** sub-module |
| Need a component library for design review | **Use UI Patterns Library** sub-module |
| Custom render pipeline with `#type => 'component'` only | SDC alone works; UI Patterns adds `#ui_patterns` config layer |
| Experience Builder (XB) is the target display builder | UI Patterns complements XB — both consume SDC components |

## Pattern

UI Patterns does not replace SDC. It extends SDC by adding the "source" layer that connects Drupal's data APIs to SDC's typed props/slots interface. Components remain vanilla SDC and work without UI Patterns installed.

The module decorates Drupal core's `ComponentPluginManager` to annotate each component's props and slots with type metadata, then provides "source plugins" that map Drupal data (entity fields, menus, blocks, tokens, manual input) to those typed props and slots.

## Common Mistakes

- **Wrong**: Installing UI Patterns for components only rendered by developers in Twig → **Right**: Use SDC directly; UI Patterns is for site-builder configurability
- **Wrong**: Assuming UI Patterns replaces SDC components → **Right**: Components remain standard SDC; removing UI Patterns should not break templates

## See Also

- [Architecture](architecture.md)
- [SDC Integration](sdc-integration.md)
- Reference: [UI Patterns 2 Official Docs](https://project.pages.drupalcode.org/ui_patterns/)
- Reference: [UI Patterns FAQ](https://project.pages.drupalcode.org/ui_patterns/faq/)
