---
description: Building project-specific UI not in Radix/Bootstrap
---

# Creating Custom Components

## When to Use

> Building project-specific UI not in Radix/Bootstrap.

## Steps

1. Use CLI: `npx drupal-radix-cli component create my-component`
2. Or create manually: `my_subtheme/components/my-component/`
3. Define metadata in `.component.yml`
4. Build Twig following Bootstrap patterns
5. Test in isolation before integrating

## Common Mistakes

- **Not following Bootstrap patterns** → Radix ecosystem expects Bootstrap conventions
- **Omitting `*_utility_classes` props** → Users can't extend without overriding
- **Hardcoding colors/spacing** → Use Bootstrap variables

## See Also

- Tool: https://www.npmjs.com/package/drupal-radix-cli
