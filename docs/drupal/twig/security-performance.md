---
topic: drupal/twig
guide: security-performance
---

## Security & Performance

### When to Use
When writing or reviewing Twig templates and preprocess functions — these rules apply to all template work.

### Security

**Autoescape — Drupal's default protection:**
Drupal overrides Twig's escape filter with `TwigExtension::escapeFilter()`. ALL variables printed in templates are HTML-escaped unless they implement `MarkupInterface` (which signals they are already safe). You cannot accidentally output raw user data through normal template printing.

**The `|raw` filter — the single biggest XSS risk in Twig:**
- `{{ user_content|raw }}` — NEVER. User content must never be marked raw
- `{{ node.field_body.value|raw }}` — NEVER. Even if it's "HTML", it hasn't been filtered
- `{{ node.field_body.processed }}` — OK. This applies the configured text format filter
- `{{ content.field_body }}` — BEST. Renders with full formatter, filter, and cache pipeline
- `|raw` is only safe on: output from `t()`, `render()`, confirmed `MarkupInterface` objects, or your own generated markup wrapped in `Markup::create()`

**URI attributes and `javascript:` injection:**
```twig
{# WRONG — user-provided URLs can contain javascript: protocol #}
<a href="{{ node.field_link.uri }}">Link</a>

{# RIGHT — use link() which handles URL sanitization #}
{{ link(node.field_link.title, node.field_link.uri) }}
```

**Sandbox restrictions protect against template injection:**
- Twig sandbox blocks non-whitelisted methods (see [Twig Overview](twig-overview.md))
- Do not add arbitrary methods to the sandbox whitelist without security review
- `twig_sandbox_allowed_methods` in `settings.php` overrides defaults — treat with care

**Access control in templates:**
```twig
{# WRONG — loads entity without checking access #}
{{ drupal_entity('node', 42, 'full', null, false) }}

{# RIGHT — access checked by default #}
{{ drupal_entity('node', 42) }}

{# For custom logic, check in preprocess, not template #}
```

### Performance

**Template-level caching — render arrays carry cache metadata:**
- `{{ content.field_name }}` carries the field's cache metadata automatically
- Custom variables added in preprocess without cache metadata bypass caching → stale output
- Always bubble cache metadata from config/entities loaded in preprocess (see [Adding Variables in Preprocess](adding-variables-preprocess.md))

**Heavy operations in templates:**
- Database queries triggered by entity traversal (e.g., `node.field_tags.entity`) load entities lazily — each traversal may trigger a DB query
- In loops, pre-load entities in preprocess and pass an array to the template
- `drupal_view()` executes a full View query — avoid in loops or per-item templates

**`attach_library()` in templates:**
```twig
{# Attaches library on every render — acceptable for component-level CSS/JS #}
{{ attach_library('mytheme/my-component') }}

{# Better for libraries shared across many templates: attach in page/theme preprocess #}
```

**Twig cache — never disable in production:**
```yaml
# services.yml — development only
twig.config:
  debug: true
  auto_reload: true
  cache: false
```
With debug mode off and cache on, templates are compiled to PHP and cached. Drupal's render cache still applies on top of this.

**Avoid logic-heavy preprocess that runs unconditionally:**
```php
// BAD — runs for every node render, even if view_mode doesn't need it
function mytheme_preprocess_node(&$variables): void {
  $variables['related'] = $this->loadRelated($variables['node']); // Always runs
}

// GOOD — gate on view mode
function mytheme_preprocess_node(&$variables): void {
  if ($variables['view_mode'] === 'full') {
    $variables['related'] = $this->loadRelated($variables['node']);
  }
}
```

### Common Mistakes
- `|raw` on any user-provided content → XSS
- Not bubbling cache metadata for custom preprocess variables → stale page cache
- Entity traversal inside `{% for %}` loops → N+1 query problem
- Disabling Twig cache in production → 10-100x rendering slowdown
- Using `drupal_config()` in twig_tweak for values that affect rendering → cache metadata not bubbled

### See Also
- Cache metadata in render arrays → `drupal-render-api.md`
- OWASP XSS prevention: `https://owasp.org/www-community/attacks/xss/`
