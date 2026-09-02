---
description: Avoid these patterns that lead to brittle, untestable, or unmaintainable recipes
tldr: "Avoid these anti-patterns when creating recipes to prevent brittle, untestable, or unmaintainable code."
drupal_version: "11.x"
---

# Anti-Patterns & Common Mistakes

## When to Use

> Avoid these anti-patterns when creating recipes to prevent brittle, untestable, or unmaintainable code.

Avoid these patterns that lead to brittle, untestable, or unmaintainable recipes.

## Decision: Anti-Patterns and What to Do Instead

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

## Pattern: Worked Examples of Each Anti-Pattern

**What NOT to do** — Monolithic recipe:
```yaml
name: 'Everything Recipe'
install:
  - node
  - media
  - taxonomy
  - comment
  - workflows
  # ... 30 more modules
config:
  strict: true  # BAD: Prevents applying to existing sites
  import:
    # ... 100 config imports
  actions:
    # ... 50 config actions mixed together
```

**What to do** — Composed recipes:
```yaml
# article_content_type recipe
name: 'Article Content Type'
install:
  - node
  - image
config:
  strict:
    - field.storage.node.field_image  # Only critical schema
  # ... focused on article setup

# site recipe
name: 'My Site'
recipes:
  - article_content_type
  - page_content_type
  - administrator_role
```

**Why strict mode is dangerous** — Existing config prevents application:
```yaml
# BAD: Fails if user.role.authenticated already exists with different permissions
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

**Why hardcoded values break** — Not reusable:
```yaml
# BAD: Only works for this specific site
config:
  actions:
    system.site:
      simpleConfigUpdate:
        name: 'Acme Corp Website'
        mail: 'admin@acmecorp.com'

# GOOD: Uses inputs
input:
  site_name:
    data_type: string
    default: { source: config, config: [system.site, name] }
  site_mail:
    data_type: string
    default: { source: config, config: [system.site, mail] }
config:
  actions:
    system.site:
      simpleConfigUpdate:
        name: ${site_name}
        mail: ${site_mail}
```

**Why missing createIfNotExists fails**:
```yaml
# BAD: Fails if display doesn't exist
config:
  actions:
    core.entity_form_display.node.article.default:
      setComponents:  # ERROR: Display doesn't exist yet
        - name: body

# GOOD: Creates display first
config:
  actions:
    core.entity_form_display.node.article.default:
      createIfNotExists:
        targetEntityType: node
        bundle: article
        mode: default
      setComponents:
        - name: body
```

## Common Mistakes

- Treating recipes as update mechanisms → Recipes are apply-once; config is permanent; use config management for updates
- Not handling existing config → Test on both clean installs AND existing sites with similar config
- Forgetting recipes are public once published → Don't commit secrets, API keys, or sensitive data
- Assuming action order doesn't matter → YAML preserves order; actions run sequentially
- Using `@extend` pattern from Sass → No recipe inheritance; use composition via `recipes:` key
- Not documenting breaking changes → Version bumps with new required inputs or changed config structure need migration path

## See Also

- Previous: ← [Best Practices & Patterns](best-practices-patterns.md)
- Next: [Security & Performance](security-performance.md) →
