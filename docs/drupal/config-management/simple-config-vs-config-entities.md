---
description: Choose between simple config (singleton YAML) and config entities (multiple instances with CRUD and UI).
---

# Simple Config vs Config Entities

## When to Use

When deciding whether to implement config as simple config (singleton YAML) or config entities (multiple instances, CRUD, UI).

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single instance of settings | Simple config | Site name, module settings, boolean toggles — only one copy exists |
| User-creatable lists | Config entities | Views, image styles, vocabularies — users create/delete multiple instances |
| No UI required | Simple config | Simpler implementation, read via Config API |
| Admin UI for CRUD | Config entities | Built-in forms, listing, dependencies, validation |
| Static dependencies only | Simple config | Only depends on the providing module |
| Dynamic dependencies | Config entities | Can depend on other entities, plugins, fields |
| Basic data types | Simple config | Booleans, integers, strings, simple arrays |
| Complex structures | Config entities | Plugins, references, nested data with validation |

## Pattern

**Simple Config:**
```php
// Define: config/install/mymodule.settings.yml
api_key: ''
enabled: false
max_items: 10

// Use in code:
$config = \Drupal::config('mymodule.settings');
$api_key = $config->get('api_key');
```

**Config Entity:**
```php
// Define entity type in MODULE.entity_type.yml
// Create ConfigEntityBase subclass
// Export to config/install/mymodule.example.MACHINE_NAME.yml

// Use in code:
$entity = \Drupal::entityTypeManager()
  ->getStorage('example')
  ->load('machine_name');
```

**Reference:** `/core/lib/Drupal/Core/Config/Config.php`, `/core/lib/Drupal/Core/Config/Entity/ConfigEntityBase.php`

## Quick Decision Guide

**Use Simple Config when:**
- One global setting (e.g., `system.site` for site name)
- Module-level configuration that admins rarely change
- No need for admin UI — developers edit YAML directly
- Data structure is flat and simple

**Use Config Entities when:**
- Users need to create/edit/delete multiple instances
- UI is required for non-developers
- Dependencies on other entities, plugins, modules
- Export/import needs entity-level granularity

## Common Mistakes

- Creating config entity for singleton settings — Unnecessary complexity, use simple config
- Using simple config for user-managed lists — No UI, no dependencies, manual YAML editing required
- Storing per-user data in config — Use State API or user data service instead
- Mixing content and config — Content (nodes, users) is NOT config
- Creating simple config with no schema — Validation failures, type casting errors

## See Also

- [Config Schema YAML](config-schema-yaml.md) — defining schema for simple config
- [Config Entities](config-entities.md) — creating config entity types
- Reference: [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types)
- Reference: [What Are Configuration Entities?](https://drupalize.me/tutorial/what-are-configuration-entities)
