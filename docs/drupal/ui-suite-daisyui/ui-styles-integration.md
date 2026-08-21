---
description: "Apply 10 utility class styles across 6 categories to blocks, Layout Builder sections, and pattern instances"
tldr: "Apply the theme's 10 UI Styles plugins (background/text color, font size, box shadow, width, padding, margin, glass, mask) to blocks, Layout Builder sections, and pattern instances -- there is no border-color, layout, or flexbox/grid style; add those in a sub-theme."
---

# UI Styles Integration

## What UI Styles Provides

The UI Styles module lets themes define reusable CSS utility classes as "styles" that site builders can apply to blocks, Layout Builder sections, and pattern instances through dropdown menus in the admin UI. The theme declares these in `ui_suite_daisyui.ui_styles.yml`.

## Style Categories

UI Suite DaisyUI defines exactly **10 style plugins** across **6 categories**. This is a deliberately small set -- do not plan a design around utilities you expect to be there:

| Category | Plugin (machine name) | Options | Example classes |
|---|---|---|---|
| **DaisyUI effects** | Glass (`daisyui_glass`) | 1 | `glass` |
| **DaisyUI effects** | Mask (`daisyui_mask`) | 15 | `mask-squircle`, `mask-hexagon` |
| **Colors** | Background color (`colors_background_color`) | 7 | `bg-primary`, `bg-base-200` |
| **Colors** | Text color (`colors_text_color`) | 5 | `text-primary-content`, `text-base-content` |
| **Typography** | Font size (`typography_font_size`) | 13 | `text-xs` .. `text-9xl` |
| **Effects** | Box shadow (`effects_box_shadow`) | 8 | `shadow-lg`, `shadow-inner` |
| **Sizing** | Width (`sizing_width`) | 10 | `w-1/2`, `w-3/4` (fractions only -- no `w-full`) |
| **Spacing** | Padding top (`spacing_padding_top`) | 14 | `pt-0` .. `pt-8` |
| **Spacing** | Padding bottom (`spacing_padding_bottom`) | 14 | `pb-0` .. `pb-8` |
| **Spacing** | Margin bottom (`spacing_margin_bottom`) | 14 | `mb-0` .. `mb-8` |

There is **no** border-color, font-weight, text-align, aspect-ratio, container, display, overflow, flex, grid, height, max-width, min-height, horizontal-padding or space-between style. If you need those in the admin UI you have to add them in your sub-theme's own `*.ui_styles.yml`; UI Styles merges the sub-theme's definitions with the base theme's.

## Style Definition Format

Each style in `ui_suite_daisyui.ui_styles.yml` follows this structure:

```yaml
style_id:
  category: "Category Name"
  label: "Human-readable label"
  description: "What this style does."
  links:
    - "https://reference-url"
  options:
    css-class: "Label"
    # Or with extra preview classes:
    css-class:
      label: "Label"
      previewed_with: ["extra-class"]
  previewed_with:
    - preview-class-1
    - preview-class-2
```

## DaisyUI Color System in Styles

DaisyUI itself defines about 20 semantic color tokens, but the two color style plugins expose only a subset of them, and the two lists do not match each other:

- **Background color** (7): `bg-primary`, `bg-secondary`, `bg-accent`, `bg-neutral`, `bg-base-100`, `bg-base-200`, `bg-base-300`
- **Text color** (5): `text-primary-content`, `text-secondary-content`, `text-accent-content`, `text-neutral-content`, `text-base-content` -- the `-content` foreground tokens only, so the dropdown pairs with the background list rather than duplicating it
- **Not exposed as styles at all**: the state colors (`info`, `success`, `warning`, `error`) and any border color

The state colors are still reachable -- as component variants (`alert`, `badge`, `button`, ...) and as raw Tailwind classes typed into a `class` attribute -- just not from the UI Styles dropdowns.

## Where Styles Can Be Applied

With the full `ui_styles` module ecosystem:

| Sub-module | Applies to | Admin path |
|---|---|---|
| `ui_styles_block` | Block wrapper, title, content | Block configuration form |
| `ui_styles_layout_builder` | LB sections and regions | Layout Builder UI |
| `ui_styles_ui_patterns` | Pattern instances | Pattern configuration |
| `ui_styles_page` | Page-level wrapper | Theme settings |

## Common Mistakes

- **Stacking conflicting styles** -- Applying both `text-primary` and `text-error` to the same element. WHY: Only one will win (CSS specificity), but the UI shows both as "applied," creating confusion.
- **Expecting styles to cascade into components** -- Styles applied to a block wrapper do not cascade into SDC components rendered inside it unless the component's Twig explicitly inherits parent classes. WHY: SDC isolation means each component manages its own classes.

## See Also

- [Tailwind CSS utility reference](https://tailwindcss.com/docs) -- Full Tailwind documentation
- `design-system-tailwind.md` -- Tailwind fundamentals
