---
description: Understanding Radix's SDC architecture for component selection and customization decisions
---

# Radix Component Architecture

## When to Use

> Understanding Radix's SDC architecture for component selection and customization decisions.

## Architecture Overview

| Aspect | Implementation | Why |
|--------|----------------|-----|
| Single Directory Components | `.component.yml` + Twig + CSS + JS in one directory | Drupal core feature (10.1+); automatic asset loading |
| Bootstrap 5.3 foundation | All components map to Bootstrap patterns | Consistent styling, accessibility, responsive behavior |
| Radix as base theme | Never activate Radix directly; always use sub-theme | Updates won't break customizations |
| Component discovery | Drupal scans `themes/*/components/` automatically | Sub-theme components override Radix base |

## Pattern

```twig
{%
  include 'radix:card' with {
    card_title: 'My Card',
    card_body: content.body,
    card_utility_classes: ['shadow-sm', 'mb-4']
  }
%}
```

## Common Mistakes

- **Using Radix as active theme** → Always create sub-theme
- **Ignoring `*_utility_classes` props** → Use for Bootstrap utilities without template overrides
- **Duplicating unchanged templates** → Only override what you modify

## See Also

- [Component Selection Strategy](component-selection-strategy.md)
- Reference: https://docs.trydrupal.com/radix
