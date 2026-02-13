---
description: Deciding whether to use base component, override, or create custom
---

# Component Selection Strategy

## When to Use

> Deciding whether to use base component, override, or create custom.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Standard Bootstrap pattern | Radix base component | Maintained, standards-compliant, accessible |
| Minor styling changes | Base + `*_utility_classes` props | No template override needed |
| Structural changes | Override in sub-theme | Preserves base, upgrades cleanly |
| New pattern | Custom component | Full control, follows SDC patterns |

## Pattern

```bash
# List Radix components
ls themes/contrib/radix/components/

# Override in sub-theme
my_subtheme/components/card/
  card.component.yml
  card.twig
  card.css
```

## Common Mistakes

- **Building custom for standard patterns** → Check Radix catalog first
- **Overriding unnecessarily** → Only override modified templates
- **Forgetting cache clear** → `drush cr` after `.component.yml` changes

## See Also

- [Radix Component Architecture](radix-component-architecture.md)
- [Component Override Patterns](component-override-patterns.md)
