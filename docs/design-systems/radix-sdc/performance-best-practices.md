---
description: Theme performance best practices — caching strategies, asset loading, image optimization, responsive images
drupal_version: "11.x"
---

# Performance Best Practices

## When to Use

> Use this when optimizing theme performance, implementing caching strategies, or optimizing asset and image loading.

## Decision

**Cache Strategy:**

| Cache Type | Use When | Example |
|------------|----------|---------|
| `Cache::PERMANENT` | Most content (invalidate with tags) | Articles, pages, blocks |
| `3600` (1 hour) | Time-sensitive data | Stock prices, weather |
| `0` (never cache) | User-specific, uncacheable | Current time, CSRF tokens |

**Library Loading:**

| Approach | When | Performance Impact |
|----------|------|-------------------|
| Global libraries | Site-wide styles/scripts | ~500KB CSS on every page |
| Component-specific (SDC auto-load) | Component-only styles | ~100KB CSS (80% reduction) |
| Conditional attachment | Block/template specific | Only load when needed |

**Image Formats:**

| Format | Use When | Savings vs JPEG |
|--------|----------|-----------------|
| WebP | Modern browsers (90%+ support) | 25-35% smaller |
| AVIF | Cutting-edge (limited support) | 50% smaller |
| JPEG | Fallback for old browsers | Baseline |

## Pattern

**Render Caching — Three Dimensions:**

**1. Cache Tags (What data does this depend on?):**

```php
$build['#cache']['tags'] = [
  'node:123',           // Invalidate when node 123 changes
  'user:456',           // Invalidate when user 456 changes
  'config:system.site', // Invalidate when site config changes
  'node_list:article',  // Invalidate when any article changes
];
```

**2. Cache Contexts (What request context affects output?):**

```php
$build['#cache']['contexts'] = [
  'url.path',      // Different cache per URL
  'user.roles',    // Different cache per role
  'languages',     // Different cache per language
];
```

**3. Max-Age (How long is this valid?):**

```php
$build['#cache']['max-age'] = Cache::PERMANENT;  // Until invalidated
// OR
$build['#cache']['max-age'] = 3600;  // 1 hour
```

**Conditional Library Loading:**

```php
// Attach library only when block renders
public function build() {
  $build = [
    '#markup' => '<div class="custom-feature">...</div>',
  ];

  $build['#attached']['library'][] = 'THEME_NAME/custom-feature';

  return $build;
}
```

**SDC auto-loads component SCSS/JS:**

```
components/carousel/
├── carousel.component.yml
├── carousel.twig
├── carousel.scss  # Auto-loaded when component renders
└── carousel.js    # Auto-loaded when component renders
```

**Critical CSS:**

```yaml
# THEME_NAME.libraries.yml

critical-inline:
  css:
    theme:
      css/critical.css:
        preprocess: false
        inline: true  # Inline in <head>

main-deferred:
  css:
    theme:
      css/main.css:
        preprocess: true  # Aggregated and minified
```

**Responsive Images:**

**Drupal Image Styles:**

```php
// Create multiple sizes
admin/config/media/image-styles

// Use responsive image formatter
$build['field_image'] = [
  '#type' => 'responsive_image',
  '#responsive_image_style_id' => 'article_hero',
  '#uri' => $image->getFileUri(),
];
```

**WebP Conversion:**

```yaml
# Enable WebP module or use image styles with WebP conversion
image_style:
  name: large_webp
  effects:
    - id: image_scale
      data: {width: 1200}
    - id: image_convert
      data: {extension: webp}
```

**Loading Attribute:**

```twig
{# Lazy load below-the-fold images #}
<img src="{{ image_url }}" loading="lazy" decoding="async" alt="{{ alt }}">

{# Eager load above-the-fold images #}
<img src="{{ hero_image }}" loading="eager" alt="{{ alt }}">
```

**Asset Optimization:**

```yaml
# File: sites/default/services.yml

parameters:
  twig.config:
    debug: false  # Disable in production
    auto_reload: false  # Disable in production
    cache: true

  # Enable CSS/JS aggregation
  http.response.debug_cacheability_headers: false
```

## Common Mistakes

- **Wrong**: No cache tags → **Right**: Tag with dependent data (`'node:123'`, `'node_list:article'`)
- **Wrong**: No cache contexts → **Right**: Add contexts for varying output (`'url.path'`, `'user.roles'`)
- **Wrong**: Loading all libraries globally → **Right**: Use conditional or component-specific loading
- **Wrong**: Inline all CSS → **Right**: Inline only critical above-the-fold CSS
- **Wrong**: Not using responsive images → **Right**: Use Drupal image styles with srcset
- **Wrong**: Not converting to WebP → **Right**: Enable WebP conversion in image styles
- **Wrong**: Eager loading all images → **Right**: Lazy load below-the-fold images
- **Wrong**: Not aggregating CSS/JS → **Right**: Enable aggregation in production
- **Wrong**: Twig debug enabled in production → **Right**: Disable debug mode
- **Wrong**: Not using cache warming → **Right**: Warm cache after deployments

## See Also

- [Layout Builder Best Practices](layout-builder-best-practices.md)
- [SDC Component Best Practices](sdc-component-best-practices.md)
- [Radix Sub-Theme Best Practices](radix-sub-theme-best-practices.md)
- Drupal Performance: https://www.drupal.org/docs/performance
