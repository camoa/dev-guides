---
description: Define user-provided values that vary per environment to enable recipe portability
tldr: "Use inputs when you need to externalize site-specific data that varies per environment, making recipes portable and reusable."
drupal_version: "11.x"
---

# Input System - Defining Inputs

## When to Use

> Use inputs when you need to externalize site-specific data that varies per environment, making recipes portable and reusable.

Define user-provided values that vary per environment. Inputs enable recipe portability by externalizing site-specific data.

## Steps: Define Inputs, Types, Constraints, Prompts and Forms

1. **Define input structure** — Each input requires description, data_type, default
   ```yaml
   input:
     site_name:
       description: 'The name of the site'
       data_type: string
       default:
         source: value
         value: 'My Site'
   ```

2. **Specify data type** — Only primitive types supported
   ```yaml
   input:
     enable_feature:
       description: 'Enable experimental feature'
       data_type: boolean
       default: { source: value, value: false }
     cache_lifetime:
       description: 'Cache lifetime in seconds'
       data_type: integer
       default: { source: value, value: 3600 }
   ```

3. **Add constraints** — Validate input values using Symfony constraints
   ```yaml
   input:
     admin_email:
       description: 'Administrator email address'
       data_type: string
       constraints:
         Email: ~
       default: { source: value, value: 'admin@example.com' }
   ```

4. **Configure CLI prompts** — Control how inputs are collected interactively
   ```yaml
   input:
     site_name:
       description: 'Site name'
       data_type: string
       prompt:
         method: ask
         arguments:
           question: 'What is your site name?'
       default: { source: value, value: 'Default Site' }
   ```

5. **Configure form elements** — Define Form API properties for web forms
   ```yaml
   input:
     site_name:
       description: 'Site name'
       data_type: string
       form:
         '#title': 'Site name'
         '#required': true
       default: { source: value, value: 'My Site' }
   ```

## Decision Points: Choosing a Default Source

| At this step... | If... | Then... |
|---|---|---|
| Value varies per environment | Different staging/prod values | Use `source: env` with environment variable |
| Value comes from existing config | Recipe extends existing site | Use `source: config` with config path |
| Value is fixed | All sites use same value | Use `source: value` with literal value |
| Validation needed | Input format matters | Add `constraints` using Symfony validators |

## Common Mistakes

- Using complex data types → Only primitives (string, integer, boolean, float) supported; no arrays or objects
- Forgetting default is required → Every input must have default source defined; no default = validation error
- Not validating inputs → Add constraints for format validation (email, URL, regex patterns)
- Assuming inputs persist → Inputs are apply-time only; not stored in config after recipe runs
- Using Form API child elements in form definition → Inputs are primitives; no child elements allowed

## See Also

- Previous: ← [Config Actions - Advanced Patterns](config-actions-advanced.md)
- Next: [Input System - Default Sources](input-default-sources.md) →
- Reference: `core/lib/Drupal/Core/Recipe/InputConfigurator.php`
