---
description: "icon() takes pack and icon id as two separate arguments — the combined pack:id string has never been valid Twig syntax"
tldr: "icon(pack_id, icon_id, settings) is the only signature; icon('pack:id') is a fatal ArgumentCountError/TypeError on every Drupal 11 release, never a deprecation — a missing icon just returns [] with no error."
drupal_version: "11.x"
---

# Twig Icon Function

## When to Use

You need to render icons in Twig templates with caching and settings support.

## Decision

There is exactly one signature. `IconsTwigExtension::getIconRenderable()` takes the pack and the icon as **two separate arguments**:

```php
public function getIconRenderable(?string $pack_id, ?string $icon_id, ?array $settings = []): array
```

| Call | Result |
|---|---|
| `icon('my_theme', 'home')` | Correct. Settings default to `[]` |
| `icon('my_theme', 'home', {size: 32})` | Correct, with settings |
| `icon(pack_var, icon_var, settings)` | Correct — the arguments are ordinary values |
| `icon('my_theme:home')` | **Fatal `ArgumentCountError`** — `$icon_id` has no default |
| `icon('my_theme:home', {size: 32})` | **Fatal `TypeError`** — an array is passed into `?string $icon_id`, and the file is `declare(strict_types=1)` |

The combined `pack:id` string is the identifier used by *PHP* APIs (`IconPackManager::getIcon()`, `IconDefinition::getRenderable()`, the UI Icons field's `target_id`). It has never been accepted by the Twig function: `IconsTwigExtension.php` has one commit in its entire history — the one that created it, `ed6e929` for issue #3471494 — and the signature there is byte-identical to the one in 11.3.11. The single-string form was never valid in any Drupal release; it is an error, not a deprecation.

When either ID is empty or NULL, `getIconRenderable()` returns `[]` — so a *missing* icon renders nothing and raises nothing. Only the wrong *arity* is fatal.

## Pattern

Basic icon rendering:

```twig
{# Simple icon #}
{{ icon('my_theme', 'home') }}

{# Icon with size #}
{{ icon('my_theme', 'home', { size: 32 }) }}

{# Icon with multiple settings #}
{{ icon('my_theme', 'home', {
  size: 32,
  color: '#007bff',
  class: 'me-2'
}) }}

{# Conditional icon #}
{% if user.isAuthenticated %}
  {{ icon('my_theme', 'user', { size: 24 }) }}
{% else %}
  {{ icon('my_theme', 'user-guest', { size: 24 }) }}
{% endif %}

{# Dynamic icon ID #}
{% set status_icons = {
  'success': 'check-circle',
  'error': 'x-circle',
  'warning': 'alert-circle'
} %}
{{ icon('my_theme', status_icons[status], { size: 20 }) }}
```

Splitting a stored `pack:id` string (icon field values, config, imported data):

```twig
{% set parts = full_id|split(':', 2) %}
{{ icon(parts[0], parts[1], { size: 24 }) }}
```

Semantic icons with labels. `decorative` and `aria_label` are not core settings — they only do anything if your pack template reads them:

```twig
<a href="/search">
  {{ icon('my_theme', 'search', {
    size: 20,
    decorative: false,
    aria_label: 'Search'
  }) }}
  <span class="visually-hidden">Search</span>
</a>
```

Reference: `/core/lib/Drupal/Core/Template/IconsTwigExtension.php` for the `icon()` Twig function definition.

## Common Mistakes

- **Wrong**: `icon('pack:id')` or `icon('pack:id', {…})` → **Right**: Fatal, on every Drupal 11 release. Split into two arguments
- **Wrong**: Assuming the render array carries cache metadata → **Right**: It does not. `getIconRenderable()` returns `#type`/`#pack_id`/`#icon_id`/`#settings` and nothing else, and `preRenderIcon()` adds no `#cache`
- **Wrong**: Expecting an error when the icon does not exist → **Right**: You get an empty render array and blank output; check `/admin/appearance/ui/icons` or `getIcons()` instead
- **Wrong**: Passing a setting the pack template does not print → **Right**: Silently ignored; settings are just context keys
- **Wrong**: Not providing text alternatives → **Right**: Decorative icons need `aria-hidden`, semantic icons need labels

## See Also

- [Template Variables](template-variables.md)
- [SDC Icon Props](sdc-icon-props.md)
- Reference: [Icon API Twig documentation](https://www.drupal.org/docs/develop/drupal-apis/icon-api)
