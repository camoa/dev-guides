---
description: "SVG source files must be complete well-formed <svg> documents — stripping the wrapper breaks XML parsing, it doesn't produce empty markup"
tldr: "Icons render incorrectly or content is missing; source files for the svg extractor must be full <svg> documents with a single root — two root nodes fails simplexml_load_string() and the icon renders as nothing."
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

# Source files MUST be complete, well-formed SVG documents. simplexml_load_string()
# parses the file; the root's CHILDREN become {{ content }} and the root's
# ATTRIBUTES become {{ attributes }}.

# ✅ Good (for SVG extractor):
# <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
#   <path d="..."/>
# </svg>

# ❌ Bad - two root nodes is not well-formed XML. simplexml_load_string() fails,
# loadIcon() returns NULL, and the icon renders as nothing:
# <path d="..."/>
# <circle cx="12" cy="12" r="10"/>

# Note: SVG sprite extractor expects <symbol> elements (top level or in <defs>)
```

Compare against core's own fixtures, which are full documents:

```bash
cat core/modules/system/tests/modules/icon_test/icons/flat/foo.svg
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

- **Wrong**: Stripping the `<svg>` root from source files → **Right**: Breaks XML parsing; the icon disappears with no error anywhere
- **Wrong**: Debugging in production → **Right**: Remove debug code before deployment
- **Wrong**: Not checking browser console → **Right**: SVG errors appear in console, not visible on page
- **Wrong**: Forgetting `xmlns` attribute → **Right**: Required for inline SVG, icons won't render
- **Wrong**: Hardcoded viewBox → **Right**: Print `{{ attributes }}` instead so the source file's own viewBox comes through
- **Wrong**: Reaching for `|raw` on `{{ content }}` → **Right**: Already a `FormattableMarkup`; `|raw` adds nothing and hides the fact that it is unsanitized

## See Also

- [Troubleshooting Icon Discovery](troubleshooting-icon-discovery.md)
- [Migration Patterns](migration-patterns.md)
- Reference: [Twig debugging](https://www.drupal.org/docs/theming-drupal/twig-in-drupal/debugging-twig-templates)
