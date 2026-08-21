---
description: "How UI Styles generates an optimized stylesheet containing only the CSS rules matching declared style options."
tldr: "The ui_styles.stylesheet_generator service parses all theme/module CSS, filters it to only rules matching declared style option classes, and serves the result as ui_styles/generated_styles on every page. Output is cached; clear cache after editing CSS or style definitions."
drupal_version: "11.x"
---

# Stylesheet Generation

## When to Use

> Use this guide when understanding how UI Styles emits an optimized stylesheet — useful for performance tuning and debugging missing CSS.

## Decision

| Goal | Action |
|---|---|
| Reduce CSS size in production | Rely on the generator — only used UI Styles classes ship |
| Keep all utility classes available regardless of UI Styles options | Skip the generator; load utilities via your normal library |

## Pattern

The `ui_styles.stylesheet_generator` service (`StylesheetGenerator`):

1. Collects all CSS files from theme and module libraries
2. Parses each with **Sabberworm PHP CSS Parser**
3. Filters out every CSS rule whose selector doesn't match a class declared in any active UI Styles option
4. Outputs a single optimized stylesheet served via `StylesheetController`
5. Caches the result; invalidates when style definitions or libraries change

The generated stylesheet is attached to every page via `hook_page_top()` as `ui_styles/generated_styles`.

## Common Mistakes

- **Editing CSS files but not seeing changes** → Clear the `ui_styles` cache discovery and the page cache; the generator caches output
- **Composer not patching `php-css-parser`** → The generator may fail on certain CSS edge cases. Confirm `cweagans/composer-patches` is active and patches applied

## See Also

- [Installation](installation.md)
- [Code Reference](code-reference.md)
- Reference: `src/Service/StylesheetGenerator.php` in the UI Styles module
