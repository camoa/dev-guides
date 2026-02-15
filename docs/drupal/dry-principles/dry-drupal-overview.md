---
description: Overview of DRY principles in Drupal's architecture - config, services, base classes, traits, plugins, templates, SDC, and render API.
---

# DRY in Drupal Overview

## When to Use

When making architectural decisions about code organization in Drupal projects — deciding between configuration vs code, services vs static calls, base classes vs traits, plugins vs custom implementations, or template inheritance vs duplication.

## Drupal's DRY Architecture

| Mechanism | What It Eliminates | Primary Use Case |
|-----------|-------------------|------------------|
| **Configuration Management** | Duplicating site settings in code and database | Site settings, field definitions, entity types, views |
| **Service Container** | Duplicating business logic across classes | Shared functionality, API integrations, utilities |
| **Base Classes** | Duplicating common entity/form/block patterns | Entity types, form types, plugin types |
| **Traits** | Duplicating cross-cutting concerns | Translation, logging, messaging, cache invalidation |
| **Plugin System** | Duplicating discovery and instantiation logic | Extensible, swappable components (blocks, field types, filters) |
| **Template Inheritance** | Duplicating markup structure | Theme overrides, component variations |
| **SDC Components** | Duplicating UI patterns | Reusable UI elements (buttons, cards, forms) |
| **Render API** | Duplicating rendering logic | Structured render arrays, theme hooks |

## Core Insight

In Drupal, **configuration is the primary single source of truth**. When you can express something as configuration, you should. Only use custom code when configuration cannot express your requirements.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Site settings, entity definitions, field config | Configuration entities | Version-controlled, environment-portable, UI-manageable |
| Shared business logic | Services with dependency injection | Testable, reusable, follows SOLID principles |
| Common patterns across entity/form/block types | Base classes (ContentEntityBase, FormBase, BlockBase) | Inherit proven patterns, reduce boilerplate |
| Cross-cutting concerns (logging, translation) | Traits | Compose behaviors without deep inheritance |
| Extensible, discoverable component types | Plugins | Reusable, overridable, discoverable via annotations/attributes |
| Markup structure variations | Twig template inheritance | Maintain consistency, override specific sections |
| UI components used across pages | Single Directory Components | Props/slots for reusability, design system consistency |

## Pattern

```php
// WRONG: Hardcoded logic duplicated across controllers
class NodeController {
  public function view() {
    $site_name = 'My Site'; // Duplicated
    $api_key = 'abc123'; // Duplicated
    // Logic here
  }
}

// RIGHT: Config as single source of truth
class NodeController {
  public function __construct(
    protected ConfigFactoryInterface $configFactory,
  ) {}

  public function view() {
    $site_name = $this->configFactory->get('system.site')->get('name');
    $api_key = $this->configFactory->get('mymodule.settings')->get('api_key');
    // Logic here
  }
}
```

Reference: `core/lib/Drupal/Core/Config/ConfigFactory.php`, `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php`

## Common Mistakes

- **Duplicating config values in code** — Always read from config, never hardcode what config already stores
- **Using static \Drupal:: calls instead of DI** — Makes testing impossible, hides dependencies, violates DRY by duplicating container access logic
- **Copy-pasting entity/form classes** — Extend base classes or create shared base classes for your project
- **Ignoring contrib modules** — Before writing custom code, check if contrib already solves your problem
- **Premature service extraction** — Don't create a service until you have multiple consumers (Rule of Three)

## See Also

- [Config as Single Source of Truth](config-single-source-truth.md)
- Universal: `dev-dry-principles.md` for tool-agnostic DRY concepts
- Reference: [Best practices for developers | Drupal API](https://api.drupal.org/api/drupal/core!core.api.php/group/best_practices/11.x)
