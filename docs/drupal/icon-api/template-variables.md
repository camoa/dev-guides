---
description: "Which variables reach an icon pack template per extractor — attributes and the pack definition itself both leak into context"
tldr: "You're writing icon pack templates and need the real variable set; caller settings override extractor data but icon_id/source always win, and the pack definition's own keys (label, provider, ...) leak into context too."
drupal_version: "11.x"
---

# Template Variables

## When to Use

You're writing icon pack templates and need to understand available variables and how to use them effectively.

## Decision

| Variable | Available in... | Use for... |
|---|---|---|
| `icon_id` | Always | CSS classes, IDs, data attributes, sprite fragments |
| `source` | `svg`, `svg_sprite`, `path` (empty string for `font`) | File paths, URLs, sprite references |
| `content` | `svg` extractor; `font` only for `.codepoints` sources | SVG inner markup (paths, circles, …) |
| `attributes` | Always — populated by `svg` from the source root, empty `Attribute` otherwise | Passing the source SVG's own `viewBox`, `fill`, `stroke` through |
| Whatever the caller passed as `icon()`'s third argument | Always | Size, color, extra classes |

`Render\Element\Icon::preRenderIcon()` builds the context as `array_merge($extractor_data, $element['#settings'], $context)`, so:

- The pack definition itself leaks into the context — `label`, `id`, `provider`, `extractor`, `settings`, `library`, `version`, `license` are all readable in a pack template. Do not name a setting after one of them.
- Caller settings **override** extractor data, but `icon_id` and `source` are merged last and win over everything. A setting named `icon_id` or `source` is silently discarded.
- `{{ group }}` does not exist. `{group}` in a source pattern is stored on the `IconDefinition` and reachable only from PHP via `getGroup()`.

## Pattern

Template with all common variables. Prefer `{{ attributes }}` over a hardcoded `viewBox` — for the `svg` extractor it carries the source file's own root attributes:

```twig
<svg xmlns="http://www.w3.org/2000/svg"
     {{ attributes }}
     width="{{ size|default(24) }}"
     height="{{ size|default(24) }}"
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

Settings definition for the above. This builds the **admin form** for the pack; the `default:` values below never reach the template, which is why every one of them is repeated as a `|default()` above:

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

Reference: `/core/lib/Drupal/Core/Render/Element/Icon.php:59-99` for how the template context is assembled; `/core/lib/Drupal/Core/Theme/Icon/IconExtractorBase.php:24-30` for which definition keys are stripped before it.

## Common Mistakes

- Expecting `settings: default:` to populate a variable → It builds a form; the template must use `|default()`
- Declaring a setting in YAML and assuming that is what makes it available → Any key in `icon()`'s third argument reaches the template, declared or not. The `settings` schema only controls the admin form
- Naming a setting `icon_id` or `source` → Overwritten by the render element, always
- Hardcoding `viewBox` in an `svg` pack template → Print `{{ attributes }}` and let the source file decide
- Missing `clean_class` filter → Use `|clean_class` for icon_id in class names
- Printing `{{ content }}` with `|raw` → Unnecessary and unsafe. `SvgExtractor` already returns a `FormattableMarkup`, which Twig prints unescaped

## See Also

- [UI Icons Module Features](ui-icons-module-features.md)
- [Twig Icon Function](twig-icon-function.md)
- Reference: [Twig filters in Drupal](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/filters-modifying-variables-in-twig-templates)
