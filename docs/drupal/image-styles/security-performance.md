---
description: Secure image derivatives with itok tokens, optimize derivative generation strategies, and manage CDN integration for performance
---

# Security & Performance

## When to Use

> Use this when you need to secure image derivatives against attacks and optimize image delivery performance.

## Security Concerns

### 1. Image Derivative Token (itok)

**Threat:** Unauthenticated users could generate unlimited derivatives by crafting URLs, causing denial-of-service through storage/CPU exhaustion.

**Protection:** Drupal adds `?itok=HASH` token to derivative URLs. Server validates token before generating derivative.

**Config:**
```php
// sites/default/settings.php

// Default: Require token (SECURE)
$config['image.settings']['allow_insecure_derivatives'] = FALSE;

// Allow insecure (ONLY if CDN handles security)
$config['image.settings']['allow_insecure_derivatives'] = TRUE;

// Suppress token from URLs (only with allow_insecure OR CDN)
$config['image.settings']['suppress_itok_output'] = TRUE;
```

**Decision:**

| If you have... | Set... | Why |
|---|---|---|
| Standard Drupal, no CDN | `allow_insecure_derivatives: FALSE` | Prevents DoS via arbitrary derivative requests |
| CDN with signed URLs | `allow_insecure_derivatives: TRUE`, `suppress_itok_output: TRUE` | CDN handles security, cleaner URLs |
| CDN without security | Keep secure (FALSE) | Drupal token is only protection |

**Attack scenario prevented:**
```
# Without token protection
GET /styles/custom_9999x9999/public/image.jpg
→ Server generates 9999x9999 derivative
→ Attacker loops, fills disk, crashes server

# With token protection
GET /styles/custom_9999x9999/public/image.jpg
→ 403 Forbidden (missing valid token)
```

### 2. Directory Traversal

**Threat:** Crafted URIs could access files outside public files directory.

**Protection:** Drupal validates stream wrapper scheme and normalizes paths before derivative generation.

**Example attack prevented:**
```php
// Malicious attempt
$uri = 'public://../../private/secret.pdf';
$style->buildUri($uri);

// Drupal normalizes to
// public://private/secret.pdf (within public)
// OR rejects entirely
```

### 3. Source Image Validation

**Threat:** Uploaded files could contain malicious code disguised as images.

**Protection:**
- File module validates MIME type
- Image toolkit validates image structure
- GD/ImageMagick reject non-image files

**Best practice:**
```php
// In custom upload handling
$image = \Drupal::service('image.factory')->get($uri);
if (!$image->isValid()) {
  // Reject file, not a real image
}
```

## Performance Optimization

### 1. Derivative Generation Strategy

**Lazy generation (default):**
- Derivatives created on first request
- **Pro:** No wasted processing for unused images
- **Con:** First user experiences delay (200-500ms)

**Pre-generation (optional):**
```php
// In cron or post-save hook
$image_style = ImageStyle::load('large');
$image_style->createDerivative($source_uri, $derivative_uri);
```
- **Pro:** No user-facing delay
- **Con:** Generates derivatives that may never be used

**Recommendation:** Use lazy for most cases. Pre-generate for critical above-fold images only.

### 2. CDN Integration

**Without CDN:**
```
Browser → Drupal → Generate derivative → Serve file
```
Every request hits Drupal, even for cached derivatives.

**With CDN:**
```
Browser → CDN (cache hit) → Return file
Browser → CDN (cache miss) → Drupal → Generate → CDN caches → Return file
```

**Config for CDN:**
```php
// settings.php
$config['image.settings']['allow_insecure_derivatives'] = TRUE;
$config['image.settings']['suppress_itok_output'] = TRUE;

// Ensure CDN is configured in settings
$settings['file_public_base_url'] = 'https://cdn.example.com';
```

### 3. Storage Management

**Derivatives location:**
```
public://styles/{style_name}/{scheme}/{original_path}
```

**Flush strategies:**

| When to flush... | Command | Impact |
|---|---|---|
| After style config change | `drush image:flush {style}` | Regenerates only that style |
| After bulk image updates | `drush image:flush --all` | Regenerates all, may take hours |
| After disk full | `drush image:flush --all` then `drush cr` | Cleans space, regenerates on demand |

**Storage estimate:**
```
Average source image: 2 MB
Image styles per image: 5
Responsive multipliers: 2
Total derivatives: 10

Storage per image = 2 MB × 0.3 (WebP compression) × 10 = 6 MB
For 1000 images = 6 GB derivatives storage
```

### 4. Caching

**Render cache:**
```php
// Image render element includes cache metadata
$image = [
  '#theme' => 'image_style',
  '#style_name' => 'large',
  '#uri' => $uri,
  '#cache' => [
    'tags' => ['image_style:large'],
    'contexts' => ['url.site'],
  ],
];
```

**Clear cache on style change:**
```bash
# Automatic on style save
drush cr

# Manual if needed
drush cache:rebuild
```

### 5. Batch Processing

**For large derivative generation:**
```php
// In batch operation
$batch = [
  'operations' => [
    ['my_module_generate_derivatives', [$image_uri]],
  ],
];
batch_set($batch);

function my_module_generate_derivatives($uri, &$context) {
  $styles = ImageStyle::loadMultiple();
  foreach ($styles as $style) {
    $derivative_uri = $style->buildUri($uri);
    $style->createDerivative($uri, $derivative_uri);
  }
}
```

Prevents timeout/memory errors on large imagesets.

## Monitoring

**Derivative storage size:**
```bash
du -sh sites/default/files/styles/
```

**Derivative count:**
```bash
find sites/default/files/styles/ -type f | wc -l
```

**Failed derivatives (check logs):**
```bash
drush watchdog:show --type=image
```

## Common Mistakes

- Disabling token protection without CDN security → DoS vulnerability, arbitrary derivative generation
- Not flushing after style changes → Serving outdated derivatives, user confusion
- Pre-generating all derivatives → Wastes storage and processing, most unused
- Allowing insecure derivatives on public internet → Attacker can exhaust disk/CPU
- Not monitoring derivative storage → Disk fills silently, site crashes
- Using token URLs with aggressive CDN caching → Cache miss on every token change, poor hit rate

## See Also

- [WebP & AVIF Optimization](webp-avif-optimization.md)
- [Best Practices & Patterns](best-practices.md)
- Reference: core/modules/image/src/Entity/ImageStyle.php (getPathToken method)
- Reference: https://www.drupal.org/docs/security-in-drupal
