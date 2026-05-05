---
description: Define configurable per-icon settings (size, color, decorative, variant) and produce accessible output markup.
tldr: Declare settings as JSON Schema properties in the pack YAML; build the template to honor decorative vs meaningful intent by toggling aria-hidden/role/aria-label. Always include a decorative boolean and an ariaLabel or alt string so editors can comply with WCAG.
drupal_version: "11.x"
---

# Settings & Rendering

## When to Use

> Defining configurable per-icon properties and producing the correct output markup.

## Decision: which settings to declare

| Need | Setting | Type |
|---|---|---|
| Editor controls icon size | `size` | integer with min/max/multipleOf |
| Editor recolors icons inline | `color` | string with `format: color` |
| Differentiate decorative vs meaningful icons (a11y) | `decorative` | boolean |
| Multi-style packs (solid/outline/duotone) | `variant` | string with enum |
| Custom CSS class on output | `class` | string (free-form) |
| Accessible label for content icons | `ariaLabel` or `alt` | string |

## Pattern: setting schema

```yaml
settings:
  size:
    title: "Size"
    type: integer
    default: 24
    minimum: 8
    maximum: 96
    multipleOf: 4
  color:
    title: "Color"
    type: string
    format: color          # forces color-picker widget
  decorative:
    title: "Decorative only"
    type: boolean
    default: false
  variant:
    title: "Variant"
    type: string
    enum: ["solid", "outline"]
  alt:
    title: "Alt text"
    type: string
    default: ""
```

## Pattern: accessible template

```twig
<svg xmlns="http://www.w3.org/2000/svg"
     width="{{ size|default(24) }}" height="{{ size|default(24) }}"
     {% if decorative %}aria-hidden="true" role="presentation"
     {% else %}role="img" aria-label="{{ ariaLabel|default(alt|default(icon_id)) }}"{% endif %}>
  {{ content|raw }}
</svg>
```

## Decision: output format by extractor

| Extractor | Default output | Pros | Cons |
|---|---|---|---|
| svg / svg_sprite | Inline `<svg>` | CSS-styleable, animatable, accessible | Larger HTML |
| path | `<img>` | Cacheable, fewer DOM nodes | Not inline-styleable |
| font | `<i>`/`<span>` with character | Tiny HTML, CSS-color | Less semantic, font-loading dependency |

## Common Mistakes

- **Wrong**: no `decorative` or `ariaLabel` setting → **Right**: without them editors can't comply with WCAG; every icon gets the same default a11y
- **Wrong**: hardcoding `width`/`height` in template without honoring a `size` setting → **Right**: editors can't resize
- **Wrong**: using `format: color` with a non-CSS-color string default → **Right**: the color-picker widget breaks

## See Also

- [Pack Format](pack-format.md)
- [Extractors](extractors.md)
- [Twig Rendering](twig.md)
