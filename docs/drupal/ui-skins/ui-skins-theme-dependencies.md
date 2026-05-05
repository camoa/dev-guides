---
description: Composing themes that activate together via the dependencies key — additive, not exclusive.
tldr: Theme dependencies are additive — declaring one theme as a dependency of another causes both to activate simultaneously, producing multiple classes on the target element. They are not a mutual-exclusivity mechanism; separate plugin IDs handle that.
drupal_version: "11.x"
---

# Theme Dependencies

## When to Use

> Use theme dependencies when two themes should always activate together (e.g., "high contrast" must layer on top of "dark mode"). Do not use dependencies to model mutually exclusive variants — they add, not replace.

## Decision

| Goal | Mechanism |
|---|---|
| Two themes always active together | Declare one with the other as `dependencies` |
| Mutually exclusive variants | Don't use dependencies — use separate plugin IDs, site builder picks one |
| Conditional activation (per role, per env) | Not supported declaratively — alter via custom code |

## Pattern

```yaml
dark:
  label: "Dark"
  target: body
  key: class
  value: theme-dark

high_contrast_dark:
  label: "High contrast (dark)"
  target: body
  key: class
  value: theme-high-contrast
  dependencies:
    - dark
```

When the site builder picks `high_contrast_dark`, UI Skins also activates `dark`. Result: `<body class="theme-dark theme-high-contrast">`.

## Common Mistakes

- **Modeling exclusive variants with dependencies** → Dependencies *add*, not replace. Use separate plugin IDs and let the site builder pick one
- **Dependency order assumptions** → Resolution order isn't guaranteed beyond "dependencies first"; don't rely on alphabetic or weighted ordering between siblings

## See Also

- [Theme Definition](ui-skins-theme-definition.md)
- [Theme Targets & Keys](ui-skins-theme-targets-keys.md)
