---
description: Debug when icons render incorrectly, template variables are missing, or SVG markup is malformed
drupal_version: "11.x"
---

# Debugging Templates

## When to Use

Icons render incorrectly, template variables are missing, or SVG markup is malformed.

## Decision

| Issue | Debug technique | Fix |
|---|---|---|
| Missing variables | `{{ dump(_context) }}` | Define in settings schema |
| SVG not rendering | View page source | Check xmlns, viewBox, paths |
| Styles not applying | Browser DevTools | Verify CSS classes, inline styles |
| Icon ID incorrect | `{{ dump(icon_id) }}` | Check icon() function arguments |
| Content empty | `{{ dump(content) }}` | Verify SVG file has inner content |

## Pattern

Template debugging workflow:

```twig
{# Step 1: Dump all available variables #}
{# Temporarily add to icon pack template #}
<pre>{{ dump(_context) }}</pre>

{# Step 2: Check specific variables #}
{{ dump({
  'icon_id': icon_id,
  'source': source,
  'content_length': content|length,
  'size': size|default('not set'),
  'color': color|default('not set')
}) }}

{# Step 3: Validate SVG structure #}
<svg xmlns="http://www.w3.org/2000/svg"
     width="{{ size|default(24) }}"
     height="{{ size|default(24) }}"
     viewBox="0 0 24 24">
  {# Ensure content is not empty #}
  {% if content %}
    {{ content }}
  {% else %}
    {# Debug: content is empty #}
    <text x="0" y="12" font-size="12">NO CONTENT</text>
  {% endif %}
</svg>
```

Browser debugging:

```javascript
// Console: Check rendered SVG
document.querySelectorAll('svg.icon').forEach(svg => {
  console.log({
    classes: svg.className.baseVal,
    width: svg.getAttribute('width'),
    height: svg.getAttribute('height'),
    innerHTML: svg.innerHTML,
    computedStyle: getComputedStyle(svg)
  });
});
```

Validate SVG source files:

```bash
# Check SVG file structure
cat themes/my_theme/icons/home.svg

# Should NOT include outer <svg> wrapper for SVG extractor
# ❌ Bad (for SVG extractor):
# <svg><path d="..."/></svg>

# ✅ Good (for SVG extractor):
# <path d="..."/>
# <circle cx="12" cy="12" r="10"/>

# Note: SVG sprite extractor expects <symbol> elements
```

Check CSS conflicts:

```css
/* Common CSS issues */

/* ❌ Bad - Overriding icon dimensions */
.icon {
  width: 16px !important; /* Breaks size setting */
}

/* ✅ Good - Respect inline styles */
.icon {
  width: auto;
  height: auto;
}

/* ❌ Bad - Hiding icons */
svg {
  display: none; /* Hides all SVGs */
}

/* ✅ Good - Specific selectors */
.content svg {
  display: inline-block;
}
```

Reference: Browser DevTools for inspecting rendered SVG.

## Common Mistakes

- **Wrong**: Debugging in production → **Right**: Remove debug code before deployment
- **Wrong**: Not checking browser console → **Right**: SVG errors appear in console, not visible on page
- **Wrong**: Forgetting `xmlns` attribute → **Right**: Required for inline SVG, icons won't render
- **Wrong**: Hardcoded viewBox → **Right**: Make configurable or match icon source dimensions
- **Wrong**: Not escaping variables → **Right**: Twig auto-escapes, but verify with |raw only when safe

## See Also

- [Troubleshooting Icon Discovery](troubleshooting-icon-discovery.md)
- [Migration Patterns](migration-patterns.md)
- Reference: [Twig debugging](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/debugging-twig-templates)
