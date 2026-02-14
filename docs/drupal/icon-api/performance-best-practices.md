---
description: Optimize icon rendering performance for large-scale sites with many icons or slow networks
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

You're optimizing icon rendering performance for large-scale sites with many icons or slow networks.

## Decision

| Optimization | Impact | When to use |
|---|---|---|
| SVG sprites over individual files | 70-90% reduction in HTTP requests | 10+ icons, especially in header/footer |
| Lazy loading for below-fold icons | Faster initial page load | Icons not in viewport on load |
| Inline critical icons | Eliminates HTTP request | Above-fold icons, small count (<5) |
| Icon pack consolidation | Reduced plugin overhead | Multiple small packs with same extractor |
| Settings caching | Faster render array processing | Icons with many dynamic settings |

## Pattern

Optimize with SVG sprites:

```yaml
# ❌ Avoid - 50 individual SVG files
individual_pack:
  extractor: svg
  config:
    sources:
      - icons/{icon_id}.svg  # 50 HTTP requests

# ✅ Good - One sprite file
sprite_pack:
  extractor: svg_sprite
  config:
    sources:
      - sprites/all-icons.svg  # 1 HTTP request
```

Lazy load below-fold icons:

```twig
{# Above-fold icons - render immediately #}
<header>
  {{ icon('my_theme:logo', { size: 40 }) }}
</header>

{# Below-fold icons - lazy load #}
<footer>
  {{ icon('my_theme:facebook', {
    size: 24,
    loading: 'lazy'  # If using <img>, not <svg>
  }) }}
</footer>
```

Inline critical SVGs:

```twig
{# Critical icon - inline for zero HTTP requests #}
{% set home_svg %}
  <svg width="24" height="24">
    <path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/>
  </svg>
{% endset %}

{# Use icon API for non-critical #}
{{ icon('my_theme:home', { size: 24 }) }}
```

Minimize pack overhead:

```yaml
# ❌ Avoid - Multiple small packs
pack_a:
  extractor: svg
  config: { sources: [icons/a/{icon_id}.svg] }

pack_b:
  extractor: svg
  config: { sources: [icons/b/{icon_id}.svg] }

# ✅ Good - Consolidated pack
combined_pack:
  extractor: svg
  config:
    sources:
      - icons/a/{icon_id}.svg
      - icons/b/{icon_id}.svg
```

Optimize templates:

```twig
{# ❌ Avoid - Complex logic in template #}
<svg width="{% if mobile %}16{% else %}24{% endif %}">
  {{ content }}
</svg>

{# ✅ Good - Pass pre-computed values #}
<svg width="{{ size|default(24) }}">
  {{ content }}
</svg>
```

Reference: Performance profiling with Webprofiler or Blackfire.

## Common Mistakes

- **Wrong**: Using individual SVG extractor for large icon sets → **Right**: Switch to sprites at 10+ icons
- **Wrong**: No HTTP/2 push for icon sprites → **Right**: Preload critical sprites in HTML head
- **Wrong**: Rendering all icons on page load → **Right**: Use lazy loading for below-fold icons
- **Wrong**: Not minifying SVG sources → **Right**: Run svgo on icon sources before deployment
- **Wrong**: Complex extractor logic without caching → **Right**: Cache expensive operations with proper tags

## See Also

- [Caching Strategy](caching-strategy.md)
- [SVG Security & Performance](svg-security-performance.md)
- Reference: [Drupal performance optimization](https://www.drupal.org/docs/managing-site-performance-and-scalability)
