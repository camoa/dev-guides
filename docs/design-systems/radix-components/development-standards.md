---
description: Maintaining code quality, security, maintainability
---

# Development Standards

## When to Use

> Maintaining code quality, security, maintainability.

## Best Practices

| Practice | Implementation | Why |
|----------|----------------|-----|
| Never activate Radix | Always use sub-theme | Updates won't break site |
| Use drupal-radix-cli | Scaffold components properly | Correct structure/schema |
| Sanitize input | Twig auto-escape; never `|raw` on user content | Prevents XSS |
| Use render arrays | Pass render arrays not HTML strings | Preserves cacheability |
| Follow BEM | Block__Element--Modifier | Prevents naming conflicts |
| No `@extend` | Use mixins/utilities | Prevents selector explosion |
| Production build | `npm run production` before commit | Minified CSS |

## Pattern

```twig
{# GOOD: Auto-escaped #}
{%
  include 'radix:card' with {
    card_title: node.label  {# Safe #}
  }
%}

{# BAD: XSS vulnerability #}
{%
  include 'radix:card' with {
    card_title: node.label|raw  {# NEVER! #}
  }
%}
```

## See Also

- Tool: https://www.npmjs.com/package/drupal-radix-cli
