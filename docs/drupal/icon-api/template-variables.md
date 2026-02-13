---
description: Available variables in icon pack templates and how to use them
drupal_version: "11.x"
---

# Template Variables

## When to Use

> Use when you're writing icon pack templates and need to understand available variables and how to use them effectively.

## Decision

| Variable | Available in... | Use for... |
|---|---|---|
| `icon_id` | All extractors | CSS classes, IDs, data attributes |
| `source` | All extractors | File paths, URLs, sprite references |
| `content` | SVG extractor only | SVG inner content (paths, circles, etc.) |
| Custom settings | When defined in pack | User-configurable options (size, color, style) |

## Pattern

Template with all common variables:

```twig
<svg xmlns="http://www.w3.org/2000/svg"
     width="{{ size|default(24) }}"
     height="{{ size|default(24) }}"
     viewBox="0 0 {{ viewBox|default('24 24') }}"
     fill="{{ color|default('currentColor') }}"
     stroke="{{ stroke|default('none') }}"
     stroke-width="{{ stroke_width|default(0) }}"
     class="icon icon-{{ icon_id|clean_class }}{{ class ? ' ' ~ class : '' }}"
     aria-hidden="{{ decorative|default(true) ? 'true' : 'false' }}"
     {% if not decorative and aria_label %}aria-label="{{ aria_label }}"{% endif %}
     focusable="false">
  {{ content }}
</svg>
```

Settings definition for above template:

```yaml
settings:
  size:
    type: "integer"
    default: 24
  color:
    type: "string"
    default: "currentColor"
  stroke:
    type: "string"
    default: "none"
  stroke_width:
    type: "number"
    default: 0
  class:
    type: "string"
    default: ""
  decorative:
    type: "boolean"
    default: true
  aria_label:
    type: "string"
    default: ""
```

Reference: `/core/lib/Drupal/Core/Theme/Icon/IconDefinition.php` for variable processing.

## Common Mistakes

- **Wrong**: Accessing undefined variables → **Right**: Define in `settings` schema first
- **Wrong**: No default values → **Right**: Always provide defaults using `|default()` filter
- **Wrong**: Hardcoded values in template → **Right**: Make configurable via settings for flexibility
- **Wrong**: Missing `clean_class` filter → **Right**: Use `|clean_class` for icon_id in class names
- **Wrong**: Not escaping user input → **Right**: Twig auto-escapes, but be cautious with `|raw` filter

## See Also

- [Font Extractor](font-extractor.md)
- [Twig Icon Function](twig-icon-function.md)
- Reference: [Twig filters in Drupal](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/filters-modifying-variables-in-twig-templates)
