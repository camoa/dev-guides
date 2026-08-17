---
description: "Common anti-patterns when using the UI Styles module and the correct alternative pattern."
tldr: "The most common mistakes are relying on the extra freeform field instead of curated options, using generic plugin IDs that collide, defining mega-styles with too many options, and deleting style definitions without auditing existing config references."
drupal_version: "11.x"
---

# Anti-Patterns

## When to Use

> Consult this before finalizing a UI Styles implementation to avoid patterns that cause silent failures or maintenance debt.

## Common Mistakes

- **Wrong**: declaring `extra: "<random>"` everywhere → **Right**: extend the curated style options instead
- **Wrong**: shipping a generic `border` plugin ID → **Right**: prefix with theme/module name (`mytheme_border`)
- **Wrong**: defining one mega-style with 50 options → **Right**: split by axis (color, spacing, border) and category
- **Wrong**: using UI Styles to inject content/structure → **Right**: UI Styles is for classes only. Use SDC, Twig templates, or paragraphs for structure
- **Wrong**: hand-editing rendered HTML to add classes UI Styles already injects → **Right**: trust the form selections; if the class isn't appearing, debug the integration submodule
- **Wrong**: deleting a style definition without auditing references → **Right**: search config for `ui_styles` storage keys before removing styles in production
- **Wrong**: declaring options whose classes only render visibly with structural classes (e.g. `text-truncate` without `d-block`) without `previewed_with` → **Right**: use `previewed_with` so the library page shows them honestly

## See Also

- [Style Definition Format](definition-format.md)
- [Overriding & Disabling](overriding.md)
- [Block Layout Integration](block-layout.md)
