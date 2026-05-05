---
description: Using multiple default_values scopes to ship different CSS variable defaults under different parent classes.
tldr: `default_values` is a map of CSS selector → value. Multiple scopes emit separate CSS rules at render time, letting the cascade deliver the right default in different contexts (`:root`, `.theme-dark`, `.callout-warning`). Site-builder edits only replace the `:root` scope value.
drupal_version: "11.x"
---

# Variable Scopes

## When to Use

> Use multiple scopes when a single CSS variable needs different default values in different parts of the page — for example, a lighter shade inside a dark theme container. Use a single `:root` scope when one global default is enough.

## Decision

| Want | Use |
|---|---|
| Same value everywhere | Single `:root` scope |
| Override inside a theme variant | Add `.theme-{name}` scope matching the theme plugin's value |
| Override inside a component | Add the component's class as a scope |

## Pattern

```yaml
brand_primary:
  type: ui_skins_alpha_color
  label: "Brand primary"
  default_values:
    ":root": "#0066ccff"
    ".theme-dark": "#3399ffff"
    ".callout-warning": "#ff8800ff"
```

This emits at render time:

```css
:root { --brand-primary: #0066ccff; }
.theme-dark { --brand-primary: #3399ffff; }
.callout-warning { --brand-primary: #ff8800ff; }
```

The CSS cascade determines which value applies to a given DOM subtree.

## Common Mistakes

- **Multiple scopes with conflicting expectations** → CSS cascade — not plugin order — determines which wins. Audit specificity if a value isn't applying
- **Site-builder-edited values overriding all scopes uniformly** → User input from theme settings replaces only the scope it was edited in (typically `:root`). Other scopes retain their declared defaults

## See Also

- [CSS Variable Definition](ui-skins-css-variable-definition.md)
- [Theme Targets & Keys](ui-skins-theme-targets-keys.md)
