---
description: Mapping the active theme to the correct HTML element and attribute type — class vs data-attribute, body vs html.
tldr: Match `target` and `key` to the CSS selectors your theme already uses. Bootstrap 5 uses `html[data-bs-theme]`; Tailwind dark mode uses `html.dark`; DaisyUI uses `html[data-theme]`. A mismatch between target and CSS selectors means nothing applies.
drupal_version: "11.x"
---

# Theme Targets & Keys

## When to Use

> Use this when picking how the active theme propagates to your CSS — deciding whether to inject a class or data-attribute, and whether it goes on `<body>` or `<html>`.

## Decision

| CSS pattern you wrote | Set theme plugin to |
|---|---|
| `body.theme-dark { ... }` | `target: body, key: class, value: theme-dark` |
| `[data-theme="dark"] { ... }` | `target: body, key: data-theme, value: dark` |
| `html.dark { ... }` (Tailwind dark mode) | `target: html, key: class, value: dark` |
| `html[data-bs-theme="dark"] { ... }` (Bootstrap 5) | `target: html, key: data-bs-theme, value: dark` |

## Pattern: Bootstrap 5 dark theme

```yaml
# my_theme.ui_skins.themes.yml
bootstrap_dark:
  label: "Bootstrap dark"
  target: html
  key: data-bs-theme
  value: dark
```

## Pattern: Tailwind dark class

```yaml
tailwind_dark:
  label: "Tailwind dark"
  target: html
  key: class
  value: dark
```

In `tailwind.config.js`, set `darkMode: 'class'` so utilities like `dark:bg-gray-900` activate.

## Common Mistakes

- **Mismatch between `target` and your CSS selectors** → If your CSS has `body.dark` but the theme plugin uses `target: html`, nothing applies. Confirm both sides match
- **Forgetting that `class` keys merge** → Multiple active themes (via dependencies) all add their classes. Combined: `<body class="theme-a theme-b">`. Make sure your CSS handles the combination

## See Also

- [Theme Definition](ui-skins-theme-definition.md)
- [Theme Dependencies](ui-skins-theme-dependencies.md)
