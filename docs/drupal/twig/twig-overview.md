---
topic: drupal/twig
guide: twig-overview
---

## Twig in Drupal Overview

### When to Use
When you need to understand how the Twig template engine integrates with Drupal's theme system before diving into specific template work.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Safe output with field formatters | `{{ content.field_name }}` | Renders with all cache metadata, format settings respected |
| Raw field value for logic/conditions | `{{ node.field_name.value }}` | Bypasses formatters — use for conditions, not display |
| Plain HTML output you fully control | Preprocess function → custom variable | Logic stays in PHP, template stays clean |
| Programmatic entity building | `drupal_entity()` (twig_tweak) | Avoids raw PHP in Twig, respects access checks |

### Pattern
```twig
{# Variables are automatically escaped — safe by default #}
{{ node.label }}

{# Render arrays are rendered via renderVar() — safe, includes cache metadata #}
{{ content.field_body }}

{# Use |t filter for translatable strings in templates #}
{{ 'Read more'|t }}
```

### How Twig Works in Drupal
Drupal replaces the default Twig escape filter with `TwigExtension::escapeFilter()`. This filter:
1. Checks for render arrays and passes them through `RendererInterface::render()`
2. Checks for `MarkupInterface` objects (already safe) and passes them through untouched
3. HTML-escapes all other strings via `Html::escape()`

Every variable printed in a template goes through this filter automatically. You cannot accidentally output raw user data unless you explicitly use `|raw`.

The **Twig sandbox** (`TwigSandboxPolicy`) restricts which object methods can be called from templates. Allowed methods on all objects:
- Exact names: `id`, `label`, `bundle`, `get`, `__toString`, `toString`
- Any method starting with: `get`, `has`, `is`
- The `Attribute` class is fully unrestricted (needed for `addClass()`, etc.)

The `#[TwigAllowed]` attribute on a PHP method marks it as callable from templates.

### Common Mistakes
- Using `|raw` on user-provided content → XSS vulnerability. Only use on pre-sanitized `MarkupInterface` objects
- Trying to call `delete()`, `save()`, or other non-idempotent methods from Twig → sandbox will throw `SecurityError`
- Assuming printed variables are un-escaped → they are always escaped unless they implement `MarkupInterface`
- Not understanding that `{{ variable }}` and `{% if variable %}` go through different code paths

### See Also
- Security rules in detail → [Security & Performance](security-performance.md)
- Core source: `core/lib/Drupal/Core/Template/TwigExtension.php`
- Core source: `core/lib/Drupal/Core/Template/TwigSandboxPolicy.php`
