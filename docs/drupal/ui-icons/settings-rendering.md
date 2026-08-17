---
description: "Declare configurable per-icon settings (size, color, decorative) and choose the right output markup."
tldr: "Declare settings as typed properties (size, color, decorative, variant); build the template to switch aria-hidden/role/aria-label on a decorative boolean. Always include decorative plus an alt/ariaLabel setting for WCAG compliance."
drupal_version: "11.x"
---

# Settings & Rendering

## When to Use

> Defining configurable per-icon properties (size, color, decorative role) and producing the right output markup.

## Pattern: Setting Schema

```yaml
settings:
  size:
    title: "Size"
    description: "Icon edge in px"
    type: integer
    default: 24
    minimum: 8
    maximum: 96
    multipleOf: 4
  color:
    title: "Color"
    type: string
    format: color           # forces color-picker widget
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
    description: "Leave blank for decorative icons"
    type: string
    default: ""
```

## Decision: which settings to declare

| Need | Setting | Type |
|---|---|---|
| Editor controls icon size | `size` | integer with min/max/multipleOf |
| Editor recolors icons inline | `color` | string with format: color |
| Differentiate decorative vs meaningful icons (a11y) | `decorative` | boolean |
| Multi-style packs (solid/outline/duotone) | `variant` | string with enum |
| Custom CSS class on output | `class` | string (free-form) |
| Accessible label for content icons | `ariaLabel` or `alt` | string |

## Decision: Output Format Choice

| Extractor | Default output | Pros | Cons |
|---|---|---|---|
| svg / svg_sprite | Inline `<svg>` | CSS-styleable, animatable, accessible | larger HTML |
| path | `<img>` | cacheable, fewer DOM nodes | not inline-styleable |
| font | `<i>`/`<span>` with character | tiny HTML, CSS-color | less semantic, font-loading dependency |

## Pattern: Accessibility

```twig
<svg xmlns="http://www.w3.org/2000/svg"
     width="{{ size|default(24) }}" height="{{ size|default(24) }}"
     {% if decorative %}aria-hidden="true" role="presentation"
     {% else %}role="img" aria-label="{{ ariaLabel|default(alt|default(icon_id)) }}"{% endif %}>
  {{ content|raw }}
</svg>
```

Site builders pick `decorative: true` for purely visual icons (chevrons, checkmarks next to label text); leave it false and provide `ariaLabel` for icons that carry meaning on their own.

## Common Mistakes

- **Wrong**: no `decorative` or `ariaLabel` setting → **Right**: declare them so editors can comply with WCAG; without them every icon gets the same default a11y
- **Wrong**: hardcoding `width`/`height` in the template without honoring a `size` setting → **Right**: reference `{{ size|default(...) }}` so editors can resize
- **Wrong**: using `format: color` with a non-CSS-color string default → **Right**: default to a valid color value or the form widget breaks

## See Also

- [Icon Pack Format](pack-format.md)
- [Extractors](extractors.md)
- [Anti-Patterns](anti-patterns.md)
