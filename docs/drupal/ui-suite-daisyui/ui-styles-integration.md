---
description: Apply 30+ utility class styles to blocks, Layout Builder sections, and pattern instances
---

# UI Styles Integration

## What UI Styles Provides

The UI Styles module lets themes define reusable CSS utility classes as "styles" that site builders can apply to blocks, Layout Builder sections, and pattern instances through dropdown menus in the admin UI. The theme declares these in `ui_suite_daisyui.ui_styles.yml`.

## Style Categories

UI Suite DaisyUI defines **30+ style plugins** across 8 categories:

| Category | Styles | Example Classes |
|---|---|---|
| **DaisyUI Effects** | Glass, Mask | `glass`, `mask mask-squircle` |
| **Colors** | Background color, Text color, Border color | `bg-primary`, `text-error`, `border-accent` |
| **Typography** | Font size, Font weight, Text align | `text-xl`, `font-bold`, `text-center` |
| **Layout** | Aspect ratio, Container, Display, Overflow | `aspect-video`, `container`, `flex`, `overflow-hidden` |
| **Flexbox & Grid** | Align items, Place content, Justify content, Flex direction | `items-center`, `justify-between`, `flex-col` |
| **Effects** | Box shadow | `shadow-lg`, `shadow-inner` |
| **Sizing** | Width, Height, Max width, Min height | `w-full`, `h-screen`, `max-w-4xl` |
| **Spacing** | Padding, Padding top/horizontal/vertical, Space between, Margin bottom | `p-4`, `px-8`, `mb-6` |

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

The theme exposes all 20 DaisyUI semantic colors for background, text, and border:

- **Brand colors**: primary, secondary, accent, neutral (+ `-content` variants)
- **Base colors**: base-100, base-200, base-300, base-content
- **State colors**: info, success, warning, error (+ `-content` variants)

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
