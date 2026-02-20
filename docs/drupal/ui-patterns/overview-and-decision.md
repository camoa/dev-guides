---
description: UI Patterns 2.x overview — when to use SDC plugins vs standalone SDC
drupal_version: "10.3+ / 11"
---

## Overview & Decision

### What UI Patterns Is

UI Patterns 2.x loads Single Directory Components (SDC) as Drupal plugins, making them available in Drupal configuration UIs for site-builders. It provides a bridge layer that connects JSON Schema-typed component definitions to Drupal's form API, context system, configuration management, and rendering pipeline.

The module decorates Drupal core's `ComponentPluginManager` (the SDC plugin manager) to annotate each component's props and slots with type metadata, then provides "source plugins" that map Drupal data (entity fields, menus, blocks, tokens, manual input) to those typed props and slots.

### When to Use

| Scenario | Recommendation |
|---|---|
| Site-builders need to configure components via UI | **Use UI Patterns** -- this is its core purpose |
| Components used only in Twig templates by developers | SDC alone is sufficient; UI Patterns adds unnecessary overhead |
| Layout Builder sections need component-based layouts | **Use UI Patterns Layouts** sub-module |
| Views rows/styles need component rendering | **Use UI Patterns Views** sub-module |
| Field formatters should render through components | **Use UI Patterns Field Formatters** sub-module |
| Need a component library for design review | **Use UI Patterns Library** sub-module |
| Custom render pipeline with `#type => 'component'` only | SDC alone works; UI Patterns adds `#ui_patterns` config layer |
| Experience Builder (XB) is the target display builder | UI Patterns complements XB -- both consume SDC components |

### Key Principle

UI Patterns does not replace SDC. It extends SDC by adding the "source" layer that connects Drupal's data APIs to SDC's typed props/slots interface. Components remain vanilla SDC and work without UI Patterns installed.

### See Also

- SDC Development Guide (existing guide)
- Drupal Layout Builder Guide (existing guide)