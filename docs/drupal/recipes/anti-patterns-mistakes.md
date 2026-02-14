---
description: Avoid these patterns that lead to brittle, untestable, or unmaintainable recipes
drupal_version: "11.x"
---

# Anti-Patterns & Common Mistakes

## When to Use

> Avoid these anti-patterns when creating recipes to prevent brittle, untestable, or unmaintainable code.

## Decision

| Anti-Pattern | Why It's Wrong | Do This Instead |
|--------------|----------------|-----------------|
| Monolithic recipes | Hard to test, impossible to reuse components, all-or-nothing application | Compose granular recipes with clear single responsibilities |
| Duplicating config across recipes | Config drift, maintenance burden, inconsistency | Reference shared recipes or use base recipes with overrides |
| Strict mode everywhere | Can't apply to existing sites, brittle on config changes | Use `strict: false` by default, `strict: true` only for schema (fields) |
| Missing dependencies | Runtime errors, incomplete setup, user confusion | Declare all module dependencies in `install:` and recipe dependencies in `recipes:` |
| Hardcoded values | Not reusable across environments, brittle | Use input system for site-specific values |
| Untested recipes | Breaks on clean installs, missing dependencies, config errors | Test every recipe on vanilla Drupal before publishing |
| Actions before entity exists | Config action fails if entity doesn't exist | Use `createIfNotExists` before entity-specific actions |
| Using install profiles | Install profiles deprecated in favor of recipes | Migrate to recipe-based approach |
| Custom code in recipes | Recipes are declarative YAML; no PHP, no hooks, no dynamic logic | Put custom code in a module, require it via `install:` |
| Expecting upgrade paths | Recipes have no update mechanism; no way to track or reapply changes | Version recipes semantically; document breaking changes; use config management for ongoing updates |
| Dynamic/conditional logic | No if/else, no loops, no runtime decisions in recipe.yml | Use modules for dynamic behavior; recipes are static declarations |

## Pattern

What NOT to do (monolithic recipe):

```yaml
name: 'Everything Recipe'
install:
  - node
  - media
  # ... 30 more modules
config:
  strict: true  # BAD: Prevents applying to existing sites
  # ... 100 config imports and 50 mixed actions
```

What to do (composed recipes):

```yaml
# article_content_type recipe
name: 'Article Content Type'
install:
  - node
  - image
config:
  strict:
    - field.storage.node.field_image  # Only critical schema

# site recipe
name: 'My Site'
recipes:
  - article_content_type
  - page_content_type
  - administrator_role
```

Why strict mode is dangerous:

```yaml
# BAD: Fails if role already exists with different permissions
config:
  strict: true
  actions:
    user.role.authenticated:
      grantPermission: 'access content'

# GOOD: Adds permission to existing role
config:
  strict: false
  actions:
    user.role.authenticated:
      grantPermission: 'access content'
```

Why hardcoded values break:

```yaml
# BAD: Only works for this specific site
config:
  actions:
    system.site:
      simpleConfigUpdate:
        name: 'Acme Corp Website'

# GOOD: Uses inputs
input:
  site_name:
    data_type: string
    default: { source: config, config: [system.site, name] }
config:
  actions:
    system.site:
      simpleConfigUpdate:
        name: ${site_name}
```

## Common Mistakes

- **Wrong**: Treating recipes as update mechanisms → **Right**: Recipes are apply-once; config is permanent; use config management for updates
- **Wrong**: Not handling existing config → **Right**: Test on both clean installs AND existing sites with similar config
- **Wrong**: Forgetting recipes are public once published → **Right**: Don't commit secrets, API keys, or sensitive data
- **Wrong**: Assuming action order doesn't matter → **Right**: YAML preserves order; actions run sequentially
- **Wrong**: Not documenting breaking changes → **Right**: Version bumps with new required inputs or changed config structure need migration path

## See Also

- [Best Practices & Patterns](best-practices-patterns.md)
- [Security & Performance](security-performance.md)
