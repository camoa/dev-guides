---
description: Convert React Router Link, Next.js Link, and anchor patterns to Drupal path(), url(), and link field rendering
drupal_version: "11.x"
---

## Link Handling

### When to Use
When converting React link and routing patterns (`<a href>`, React Router `<Link>`, Next.js `<Link>`, `onClick` navigation, dynamic routes) to Drupal Twig equivalents using `path()`, `url()`, `link()`, and link field formatters.

### Decision

| React / JSX Pattern | Drupal / Twig Equivalent | Why |
|---|---|---|
| `<a href="/path">` hardcoded | `<a href="{{ path('route.name') }}">` | Drupal generates language-prefixed, alias-aware paths |
| React Router `<Link to="/blog">` | `<a href="{{ path('entity.node.canonical', {node: node.id()}) }}">` | Entity routes resolve to current path alias |
| Next.js `<Link href="/blog/[slug]">` | `{{ path('entity.node.canonical', {node: node.id()}) }}` | Same entity canonical route pattern |
| `onClick={() => navigate('/path')}` | No direct equivalent — use `<a>` with `path()` | Drupal is server-rendered; no client-side routing |
| External link `<a href="https://…" target="_blank">` | `<a href="{{ url }}" target="_blank" rel="noopener noreferrer">` | `noopener noreferrer` is required for security |
| Link field rendered with text | `{{ content.field_link }}` | Formatter handles internal/external, link text, aria |
| Link field raw URI + title | `{{ node.field_link.uri }}` + `{{ node.field_link.title }}` | Raw access for custom markup only |
| `useLocation()` for active state | `is_active` / `in_active_trail` in menu item templates | Drupal active trail set server-side |
| Dynamic route params `[slug]` | `{{ path('entity.node.canonical', {node: node.id()}) }}` | Entity-based routing with Drupal path aliases |
| Absolute URL with domain | `{{ url('entity.node.canonical', {node: node.id()}) }}` | `url()` returns absolute, `path()` returns relative |

### Pattern

**Internal links via route:**
```twig
{# Relative path — preferred for internal links #}
<a href="{{ path('entity.node.canonical', {node: node.id()}) }}">
  {{ node.label }}
</a>

{# Named route with parameters #}
<a href="{{ path('view.frontpage.page_1') }}">View all</a>
```

**The `link()` Twig function — generates a full `<a>` tag:**
```twig
{# link(text, url, attributes) — url can be a string or URL object #}
{{ link('Read more', path('entity.node.canonical', {node: node.id()}), {'class': ['btn']}) }}
```

**Link field — preferred for field data:**
```twig
{# Renders with formatter: handles internal/external, link text, rel attribute #}
{{ content.field_link }}

{# Raw access for custom markup — check emptiness first #}
{% if node.field_link.uri %}
  <a href="{{ node.field_link.uri }}"
     {% if node.field_link.uri|url_is_external %}
       target="_blank" rel="noopener noreferrer"
     {% endif %}>
    {{ node.field_link.title ?: node.field_link.uri }}
  </a>
{% endif %}
```

**Active trail in menu templates:**
```twig
{# in_active_trail is provided by Drupal's menu system — no React useLocation() needed #}
<li class="{{ in_active_trail ? 'active' : '' }}">
  <a href="{{ url }}" {{ is_active ? 'aria-current="page"' : '' }}>{{ title }}</a>
</li>
```

## Common Mistakes

- **Wrong**: Hardcoding `/node/123` or `/en/about` paths → **Right**: Always use `path()` with a route name; hardcoded paths break on alias changes and environment differences
- **Wrong**: Using `url()` for internal links → **Right**: Use `path()` for internal links; `url()` generates an absolute URL including domain, which breaks on staging/local
- **Wrong**: Forgetting `rel="noopener noreferrer"` on `target="_blank"` external links → **Right**: Use the `url_is_external` filter to detect and add conditionally (security vulnerability)
- **Wrong**: Accessing `node.field_link.uri` for display instead of `{{ content.field_link }}` → **Right**: Use the formatter — it handles external/internal, link text fallback, and accessible markup
- **Wrong**: Trying to replicate React Router's client-side transitions → **Right**: Drupal is server-rendered; use Drupal's AJAX API or HTMX for SPA-like behavior
- **Wrong**: Using `{{ url }}` when you need a specific entity URL → **Right**: In node templates, `url` is the canonical URL of the current node, not the Twig `url()` function

## See Also

- [Event Handlers to Drupal Behaviors](event-handlers.md) — `onClick` navigation patterns
- [Conditional Rendering](conditional-rendering.md) — checking `node.field_link.uri` before rendering
- Reference: [Drupal `path()` Twig function — api.drupal.org](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/function/TwigExtension%3A%3AgetPath/11.x)
- Reference: [Drupal `url_is_external` filter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/function/TwigExtension%3A%3AisExternalUrl/11.x)
