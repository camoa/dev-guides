---
description: Modifying Radix base component for sub-theme
---

# Component Override Patterns

## When to Use

> Modifying Radix base component for sub-theme.

## Steps

1. Copy component from Radix to sub-theme: `cp -r themes/contrib/radix/components/card themes/custom/my_subtheme/components/`
2. Modify `.component.yml` if adding/changing props
3. Update Twig template (preserve Bootstrap classes, ARIA attributes)
4. Add component CSS/JS (auto-loads with component)
5. Clear cache: `drush cr`

## Common Mistakes

- **Removing base props** → Keep for compatibility
- **Not preserving accessibility** → Maintain ARIA attributes
- **Global CSS instead of component files** → Component CSS loads only when needed

## See Also

- [Creating Custom Components](creating-custom-components.md)
