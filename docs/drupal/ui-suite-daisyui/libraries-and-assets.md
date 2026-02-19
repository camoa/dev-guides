---
description: Pre-compiled CSS library, CKEditor 5 integration, and Heroicon pack configuration
---

# Libraries & Assets

## Library Structure

Alpha6 ships with a single pre-compiled library instead of CDN dependencies. The theme defines one library in `ui_suite_daisyui.libraries.yml`:

| Library | Type | Source | Purpose |
|---|---|---|---|
| `daisyui` | CSS | `dist/css/app.css` (minified) | Pre-compiled DaisyUI 5 + Tailwind CSS 4 + theme styles + custom utilities |

```yaml
# ui_suite_daisyui.libraries.yml
daisyui:
  license:
    name: MIT
    url: https://github.com/saadeghi/daisyui/blob/v5/packages/daisyui/LICENSE
    gpl-compatible: false
  css:
    theme:
      "dist/css/app.css":
        { minified: true }
```

The base theme now uses a build pipeline (same toolchain as the starterkit) to compile all CSS at build time. No CDN dependencies are required. The `dist/css/app.css` file contains DaisyUI component classes, all 35 themes, Tailwind utilities used by the theme's components, and custom styles.

## CKEditor 5 Stylesheet

The theme also registers its compiled CSS for CKEditor 5 WYSIWYG editing:

```yaml
ckeditor5-stylesheets:
  - dist/css/app.css
```

This ensures DaisyUI styles are visible in the content editor.

## Icon Packs

The theme defines 4 Heroicon packs in `ui_suite_daisyui.icons.yml`:

| Pack ID | Description | ViewBox | Default Size |
|---|---|---|---|
| `hero_solid_16` | Heroicons solid 16px | 0 0 16 16 | 16px |
| `hero_solid_20` | Heroicons solid 20px | 0 0 20 20 | 20px |
| `hero_solid_24` | Heroicons solid 24px | 0 0 24 24 | 24px |
| `hero_outline_24` | Heroicons outline 24px | 0 0 24 24 | 24px |

Icons are loaded from `/libraries/heroicons/` using the SVG extractor. Each pack supports `size` and `color` settings; the outline pack additionally supports `stroke_width`.

## Common Mistakes

- **Overriding the `daisyui` library without providing replacement CSS** -- If a sub-theme disables `dist/css/app.css` via `libraries-override` without providing its own compiled CSS, the theme has no styles. WHY: Alpha6 uses pre-compiled CSS instead of CDN; disabling it removes all DaisyUI and Tailwind styles. The starterkit handles this correctly with its own `daisyui` library.
- **Assuming Heroicons are bundled** -- The icon packs reference `/libraries/heroicons/` which must be installed separately (e.g., via `npm` or `composer`). WHY: The theme only defines the icon pack configuration; the actual SVG files must exist at the specified path.

## See Also

- `design-system-tailwind.md` -- Tailwind CSS build pipelines
- `design-system-daisyui.md` -- DaisyUI asset management
