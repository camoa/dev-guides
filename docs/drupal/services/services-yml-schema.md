---
description: Structure and schema of *.services.yml files — top-level keys, _defaults, service IDs, and YAML schema validation for IDE support.
---

# services.yml Schema

## When to Use

When you need to understand the structure of *.services.yml files — the foundational configuration format for Drupal services.

## Structure

A services.yml file has two top-level keys:

**parameters**: Global container parameters (string/array values)
```yaml
parameters:
  my_module.setting: 'value'
  my_module.list: ['item1', 'item2']
```

**services**: Service definitions (the bulk of the file)
```yaml
services:
  _defaults:
    autoconfigure: true  # Applies to all services in this file

  my_module.example:
    class: Drupal\my_module\ExampleService
    arguments: ['@other_service', '%my_module.setting%']
    tags:
      - { name: event_subscriber }
```

## Schema Reference

**Symfony Schema Validation** (Drupal 10.3+ / 11.0+):
```yaml
# Add to top of services.yml for IDE autocomplete
# yaml-language-server: $schema=../vendor/symfony/dependency-injection/Loader/schema/services.schema.json
```

The schema path is relative to your module root. Adjust `../vendor/` based on your Drupal install location.

## Key Sections

| Section | Purpose | Example |
|---|---|---|
| `parameters:` | Define container-wide configuration values | `app.root: '/var/www/drupal'` |
| `services:` | Define service instances | All service definitions |
| `_defaults:` | Apply properties to all services in file | `autoconfigure: true` |
| Service ID | Unique identifier for the service | `my_module.manager` |

Reference: `/core/core.services.yml` (lines 1-80 for parameters, 81+ for services)

## Common Mistakes

- **Wrong indentation** — YAML is whitespace-sensitive; use 2 spaces per level
- **Mixing tabs and spaces** — Use spaces only; tabs cause parse errors
- **Missing quotes around special chars** — Quote service IDs with dots in arguments: `'@my_module.service'`
- **Forgetting @ prefix for service references** — `@service_id` is reference, `service_id` is string
- **Using wrong schema path** — Schema path must be relative to the *.services.yml file location

## See Also

- [Service Definition Properties](service-definition-properties.md)
- [Structure of a service file](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection/structure-of-a-service-file)
