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
| `<a href="/path">` hardcoded | `{{ link(label, path('route.name')) }}` | Drupal generates language-prefixed, alias-aware paths |
| React Router `<Link to="/blog">` | `{{ link(label, path('entity.node.canonical', {node: node.id()})) }}` | `link()` generates a full `<a>` tag; entity routes resolve to current path alias |
| Next.js `<Link href="/blog/[slug]">` | `{{ link(label, path('entity.node.canonical', {node: node.id()})) }}` | Same entity canonical route pattern |
| `onClick={() => navigate('/path')}` | No direct equivalent — use `<a>` with `path()` | Drupal is server-rendered; no client-side routing |
| External link `<a href="https://…" target="_blank">` | `<a href="{{ url }}" target="_blank" rel="noopener noreferrer">` | `noopener noreferrer` is required for security |
| Link field rendered with text | `{{ content.field_link }}` | Formatter handles internal/external, link text, aria |
| Link field raw URI + title | `{{ node.field_link.uri }}` + `{{ node.field_link.title }}` | Raw access for custom markup only |
| `useLocation()` for active state | `is_active` / `in_active_trail` in menu item templates | Drupal active trail set server-side — never add manually |
| Dynamic route params `[slug]` | `{{ path('entity.node.canonical', {node: node.id()}) }}` | Entity-based routing with Drupal path aliases |
| Absolute URL with domain | `{{ url('entity.node.canonical', {node: node.id()}) }}` | `url()` returns absolute, `path()` returns relative |
| `<a href={dynamicUrl}>` from state / props | `<a href="{{ dynamic_url }}">` where `dynamic_url` prepared in preprocess | Build and validate URLs in PHP preprocess — never construct from raw user input in Twig |
| `<a href="#section-id">` (anchor link) | `<a href="#section-id">` (no change) | Pure HTML — no Drupal routing involved |
| `<a href="mailto:email@example.com">` | `<a href="mailto:{{ email }}">` | Raw HTML — no Drupal function needed; sanitize `email` in preprocess |
| `<a href="tel:+1234567890">` | `<a href="tel:{{ phone }}">` | Raw HTML — no Drupal function needed; sanitize `phone` in preprocess |
| `<a download href={fileUrl}>` | `{{ content.field_file }}` with File formatter | File formatter generates the correct URL with `download` attribute and access control |
| `<a className="btn btn-primary" href={path}>` | `{{ link('Text', path('route.name'), {'class': ['btn', 'btn-primary']}) }}` or DaisyUI button | `link()` accepts an attributes array; or use `ui_suite_daisyui:button` with `url` prop |

### Pattern

**Internal links via `link()` function — preferred for most cases:**

```jsx
// JSX: React Router or Next.js Link
import Link from 'next/link';

return <Link href={`/blog/${node.slug}`}>{node.title}</Link>;
```
```twig
{# link(text, url, attributes) — generates a full <a> tag #}
{{ link(node.label, path('entity.node.canonical', {node: node.id()})) }}

{# With CSS classes — DaisyUI button style #}
{{ link('Read more', path('entity.node.canonical', {node: node.id()}), {'class': ['btn', 'btn-primary']}) }}

{# Named route with no params #}
{{ link('View all', path('view.frontpage.page_1')) }}
```

**Raw `<a>` with `path()` — when you need custom inner markup:**

```jsx
// JSX: link wrapping an icon + text
return (
  <Link href={path}>
    <span className="icon">→</span> {node.title}
  </Link>
);
```
```twig
{# Use raw <a> only when link() cannot wrap the inner markup #}
<a href="{{ path('entity.node.canonical', {node: node.id()}) }}">
  <span class="icon">→</span> {{ node.label }}
</a>
```

**Link field — preferred for field data:**

```jsx
// JSX: link field from CMS query
const { fieldLink } = node;
return (
  <a
    href={fieldLink.url}
    target={fieldLink.isExternal ? '_blank' : undefined}
    rel={fieldLink.isExternal ? 'noopener noreferrer' : undefined}
  >
    {fieldLink.title || fieldLink.url}
  </a>
);
```
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

```jsx
// JSX: usePathname() to detect active route
const pathname = usePathname();
const isActive = pathname === item.href;

return (
  <li className={isActive ? 'active' : ''}>
    <a href={item.href} aria-current={isActive ? 'page' : undefined}>
      {item.title}
    </a>
  </li>
);
```
```twig
{# in_active_trail and is_active are provided by Drupal's menu system —
   never add the active class manually #}
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
- **Wrong**: Translating Next.js `<Link prefetch>` behavior to Drupal → **Right**: No equivalent — Drupal uses BigPipe for progressive server-side rendering; link prefetching is not a Drupal pattern
- **Wrong**: Adding `active` or `is-active` CSS class manually via Twig logic → **Right**: Drupal's `active-link` library automatically adds `is-active` to links matching the current URL — manual class management conflicts with it

## See Also

- [Event Handlers to Drupal Behaviors](event-handlers.md) — `onClick` navigation patterns
- [Conditional Rendering](conditional-rendering.md) — checking `node.field_link.uri` before rendering
- [Props to Twig Variables](props-to-twig.md) — passing URL data as SDC props
- Reference: [Drupal `link()` Twig function — api.drupal.org](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/function/TwigExtension%3A%3AgetLink/11.x)
- Reference: [Drupal `path()` Twig function — api.drupal.org](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/function/TwigExtension%3A%3AgetPath/11.x)
- Reference: [DaisyUI Button component](https://daisyui.com/components/button/)
- Reference: [Drupal `url_is_external` filter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Template%21TwigExtension.php/function/TwigExtension%3A%3AisExternalUrl/11.x)
