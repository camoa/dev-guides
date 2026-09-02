---
description: Follow these patterns to create maintainable, reusable, testable recipes
tldr: "Apply these practices when creating recipes to ensure maintainability, reusability, and testability."
drupal_version: "11.x"
---

# Best Practices & Patterns

## When to Use

> Apply these practices when creating recipes to ensure maintainability, reusability, and testability.

Follow these patterns to create maintainable, reusable, testable recipes.

## Decision: Practices and When to Apply Them

| Practice | When to Apply | Why |
|----------|---------------|-----|
| Granular recipes | Building reusable components | Small focused recipes compose better than monoliths |
| Strict mode carefully | Recipe enforces schema | Use `strict: false` for flexibility, `strict: true` for critical config (fields) |
| Config actions over imports | Dynamic config needed | Actions merge with existing config; imports replace entirely |
| Inputs for site-specific values | Recipe reusable across environments | Hardcoded values make recipes brittle |
| Composer packages | Distributing recipes | Versioning, dependency management, discoverability |
| Testing on clean installs | Validating recipes | Catches missing dependencies and strict mode issues |
| Semantic naming | Organizing recipes | `{feature}_{entity_type}_recipe` pattern (article_content_type, not article_recipe) |

## Pattern: Layered Composition and Action-vs-Import

**Layered composition** — Base → feature → site pattern:
```yaml
# base_role recipe
name: 'Base Role'
config:
  actions:
    user.role.editor:
      createIfNotExists:
        label: 'Editor'

# content_permissions recipe
name: 'Content Permissions'
recipes:
  - base_role
config:
  actions:
    user.role.editor:
      grantPermissionsForEachNodeType:
        - 'create %bundle content'

# site recipe
name: 'My Site'
recipes:
  - content_permissions
```

**Config action vs import decision**:
```yaml
# Use import for static config
config:
  import:
    views:
      - views.view.content  # No changes needed

# Use actions for dynamic config
config:
  actions:
    user.role.editor:
      grantPermissions:
        - 'access content'  # Additive, merges with existing
```

## Common Mistakes

- Creating monolithic recipes → Hard to test, hard to reuse, hard to maintain
- Hardcoding environment-specific values → Site names, API keys, theme names should be inputs
- Using `strict: true` everywhere → Prevents applying to existing sites; use selectively for schema (fields)
- Not documenting recipe dependencies → README should explain what recipe does and what it depends on
- Skipping clean install testing → Recipe may work on dev site but fail on production clean install
- Over-using config imports → Config actions are more flexible; import only truly static config
- Not versioning recipes → Use Git tags and semantic versioning; communicate breaking changes

## See Also

- Previous: ← [Core Recipes Catalog](core-recipes-catalog.md)
- Next: [Anti-Patterns & Common Mistakes](anti-patterns-mistakes.md) →
