---
description: You're optimizing theme performance
drupal_version: "11.x"
---

## 6.5 Performance Best Practices

### When to Use This Section
- You're optimizing theme performance
- You need guidance on caching strategies
- You're implementing responsive images and modern formats
- You want to optimize asset loading

### Render Caching: Cache Tags, Contexts, and Max-Age

#### CRITICAL CONCEPT: Three Dimensions of Caching

**1. CACHE TAGS** — "What data does this depend on?"

```php
$build['#cache']['tags'] = [
  'node:123',           // Invalidate when node 123 changes
  'user:456',           // Invalidate when user 456 changes
  'config:system.site', // Invalidate when site config changes
  'node_list:article',  // Invalidate when any article changes
];
```

**WHY:** When tagged data changes, Drupal automatically invalidates cache.

**COMMON MISTAKE:**

```php
// BAD: No cache tags
$build = ['#markup' => $this->renderContent()];
// Content changes won't invalidate cache
```

---

**2. CACHE CONTEXTS** — "What request context affects output?"

```php
$build['#cache']['contexts'] = [
  'url.path',      // Different cache per URL
  'user.roles',    // Different cache per role
  'languages',     // Different cache per language
  'theme',         // Different cache per theme (if multisite)
];
```

**WHY:** Creates separate cache entries for different contexts.

**EXAMPLE:** Admin sees edit links, anonymous doesn't → Use `'user.permissions'` context.

---

**3. MAX-AGE** — "How long is this valid?"

```php
$build['#cache']['max-age'] = Cache::PERMANENT;  // Until invalidated by tags
// OR
$build['#cache']['max-age'] = 3600;  // 1 hour
// OR
$build['#cache']['max-age'] = 0;  // Never cache
```

**WHY:** Balances performance with freshness.

**DECISION:**
- `Cache::PERMANENT` — Most content (invalidate with tags)
- `3600` (1 hour) — Time-sensitive data (stock prices, weather)
- `0` — User-specific, uncacheable (current time, CSRF tokens)

---

### Library Loading: Conditional Loading and Critical CSS

#### Pattern: Conditional Library Attachment

**BAD PRACTICE:**

```yaml
# THEME_NAME.info.yml
libraries:
  - THEME_NAME/carousel-styles
  - THEME_NAME/modal-styles
  - THEME_NAME/accordion-styles
  # Loading all libraries on every page
```

**WHY BAD:** Carousel CSS loads on pages without carousels.

**GOOD PRACTICE:**

```twig
{# Only attach carousel library when carousel component renders #}
{# components/carousel/carousel.scss auto-loaded with SDC #}
```

**OR in custom block:**

```php
public function build() {
  $build = [
    '#markup' => '<div class="custom-feature">...</div>',
  ];

  // Attach library only when block renders
  $build['#attached']['library'][] = 'THEME_NAME/custom-feature';

  return $build;
}
```

**PERFORMANCE IMPACT:**
- Loading all libraries: ~500KB CSS on every page
- Conditional loading: ~100KB CSS (80% reduction)

---

#### Pattern: Critical CSS

**STRATEGY:** Inline critical above-the-fold CSS, defer rest

**File: `THEME_NAME.info.yml`**

```yaml
libraries:
  - THEME_NAME/critical-inline  # Inline critical CSS
  - THEME_NAME/main-deferred    # Defer non-critical CSS
```

**File: `THEME_NAME.libraries.yml`**

```yaml
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

**WHAT GOES IN CRITICAL CSS:**
- Header styles
- Above-the-fold layout
- Logo, navigation
- Hero section styles

**WHAT GOES IN DEFERRED:**
- Footer styles
- Below-the-fold components
- Rarely-used components

**PERFORMANCE IMPACT:**
- Without critical CSS: 2-3 second blank page (waiting for CSS)
- With critical CSS: <1 second visible content

---

### Image Performance: Responsive Images, Lazy Loading, WebP/AVIF

#### Pattern: Responsive Images (Built-in Drupal)

**DRUPAL 10+ DEFAULT:** Responsive images and lazy loading enabled

**Verify Configuration:**
1. Admin → Configuration → Media → Responsive image styles
2. Ensure image styles defined (thumbnail, medium, large)
3. Set responsive image style on image field display

**GENERATED HTML:**

```html
<img
  src="/files/styles/large/image.jpg"
  srcset="
    /files/styles/thumbnail/image.jpg 320w,
    /files/styles/medium/image.jpg 768w,
    /files/styles/large/image.jpg 1200w
  "
  sizes="(min-width: 1200px) 1200px, (min-width: 768px) 768px, 320px"
  loading="lazy"
  alt="Description"
>
```

**PERFORMANCE IMPACT:**
- Desktop: Loads 1200px image
- Tablet: Loads 768px image (smaller file)
- Mobile: Loads 320px image (smallest file)
- **Data savings: up to 70%** on mobile

---

#### Pattern: WebP and AVIF Support

**DRUPAL 10+:** Native WebP support

**Configuration:**
1. Admin → Configuration → Media → Image toolkit
2. Enable WebP generation
3. Image styles automatically generate WebP versions

**GENERATED HTML:**

```html
<picture>
  <source type="image/avif" srcset="/files/styles/large/image.avif">
  <source type="image/webp" srcset="/files/styles/large/image.webp">
  <img src="/files/styles/large/image.jpg" alt="Description">
</picture>
```

**FILE SIZE COMPARISON:**
- JPEG (original): 500KB
- WebP: 175KB (65% smaller)
- AVIF: 125KB (75% smaller)

**BROWSER SUPPORT:**
- AVIF: Modern browsers (fallback to WebP)
- WebP: 95%+ browsers (fallback to JPEG)

**RECOMMENDED MODULES:**
- **ImageAPI Optimize WebP**: Automatic WebP conversion
- **Image Optimize**: Compression with TinyPNG, Kraken

---

#### Pattern: Lazy Loading (Default in Drupal 10+)

**AUTOMATIC:** Drupal adds `loading="lazy"` to images

**PERFORMANCE IMPACT:**
- Without lazy loading: 50 images load immediately (slow)
- With lazy loading: Only visible images load (fast)
- **Initial load time: 40% faster**

**TO DISABLE (rare cases):**

```twig
{# Disable lazy loading for above-the-fold images #}
<img src="{{ image.url }}" loading="eager" alt="{{ image.alt }}">
```

**WHEN TO DISABLE:** Above-the-fold hero image (prevents layout shift)

---

### Asset Aggregation and Minification

#### Pattern: Production Settings

**File: `sites/default/settings.php`**

```php
// Development
$config['system.performance']['css']['preprocess'] = FALSE;
$config['system.performance']['js']['preprocess'] = FALSE;

// Production
$config['system.performance']['css']['preprocess'] = TRUE;
$config['system.performance']['js']['preprocess'] = TRUE;
$config['system.performance']['css']['gzip'] = TRUE;
$config['system.performance']['js']['gzip'] = TRUE;
```

**AGGREGATION:**
- Combines multiple CSS/JS files into one
- Reduces HTTP requests

**MINIFICATION:**
- Removes whitespace, comments
- Reduces file size

**GZIP:**
- Compresses files before sending
- 70-80% size reduction

**PERFORMANCE IMPACT:**
- Development (no aggregation): 50+ CSS/JS requests
- Production (aggregation): 2-3 CSS/JS requests
- **Page load: 60% faster**

---

### Common Performance Mistakes

**1. No cache metadata on render arrays**

```php
// BAD: No caching
return ['#markup' => $expensive_content];
```

**CORRECT:**

```php
return [
  '#markup' => $expensive_content,
  '#cache' => [
    'tags' => ['node:123'],
    'contexts' => ['url.path'],
    'max-age' => Cache::PERMANENT,
  ],
];
```

---

**2. Loading all libraries globally**

```yaml
# BAD: Everything on every page
libraries:
  - THEME_NAME/everything
```

**CORRECT:**

```yaml
# Only site-wide essentials
libraries:
  - THEME_NAME/base
# Component-specific libraries load with components
```

---

**3. Not using responsive images**

```twig
{# BAD: Full-size image on mobile #}
<img src="/files/original/huge-image.jpg" alt="...">
```

**CORRECT:**

```twig
{# GOOD: Responsive image #}
{{ content.field_image }}
{# Uses responsive image formatter #}
```

---

**4. Twig debug/cache disabled in production**

```yaml
# BAD: Debug on in production
twig.config:
  debug: true
  cache: false
```

**CORRECT:**

```yaml
# Production settings
twig.config:
  debug: false
  cache: true
  auto_reload: false
```

**PERFORMANCE IMPACT:** 50-70% slower with debug on.

---

**5. Blocking JavaScript in <head>**

```html
<!-- BAD: Blocks page rendering -->
<script src="/js/large-library.js"></script>
```

**CORRECT:**

```yaml
# THEME_NAME.libraries.yml
main:
  js:
    js/large-library.js:
      defer: true  # Or async
```

#### See Also
- Drupal Cache API: https://www.drupal.org/docs/develop/drupal-apis/cache-api
- Drupal Responsive Images: https://www.drupal.org/docs/8/mobile-guide/responsive-images-in-drupal-8
- Image Optimize Module: https://www.drupal.org/project/imageapi_optimize