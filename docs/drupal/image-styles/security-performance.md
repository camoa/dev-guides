---
description: Secure image derivatives and optimize performance
drupal_version: "11.x"
---

# Security & Performance

## When to Use

> Use this when securing image derivatives against attacks and optimizing image delivery performance.

## Decision - Image Derivative Security

| If you have... | Set... | Why |
|---|---|---|
| Standard Drupal, no CDN | `allow_insecure_derivatives: FALSE` | Prevents DoS via arbitrary derivative requests |
| CDN with signed URLs | `allow_insecure_derivatives: TRUE`, `suppress_itok_output: TRUE` | CDN handles security, cleaner URLs |
| CDN without security | Keep secure (FALSE) | Drupal token is only protection |

## Pattern - Image Derivative Token (itok)

**Threat:** Unauthenticated users could generate unlimited derivatives by crafting URLs, causing denial-of-service through storage/CPU exhaustion.

**Protection:** Drupal adds `?itok=HASH` token to derivative URLs.

```php
// sites/default/settings.php

// Default: Require token (SECURE)
$config['image.settings']['allow_insecure_derivatives'] = FALSE;

// Allow insecure (ONLY if CDN handles security)
$config['image.settings']['allow_insecure_derivatives'] = TRUE;

// Suppress token from URLs (only with allow_insecure OR CDN)
$config['image.settings']['suppress_itok_output'] = TRUE;
```

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

## Pattern - Derivative Generation Strategy

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

## Pattern - CDN Integration

**Without CDN:**
```
Browser → Drupal → Generate derivative → Serve file
```

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
$settings['file_public_base_url'] = 'https://cdn.example.com';
```

## Storage Management

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

## Monitoring

```bash
# Derivative storage size
du -sh sites/default/files/styles/

# Derivative count
find sites/default/files/styles/ -type f | wc -l

# Failed derivatives
drush watchdog:show --type=image
```

## Common Mistakes

- **Wrong**: Disabling token protection without CDN security → **Right**: Keep tokens enabled (DoS vulnerability, arbitrary derivative generation)
- **Wrong**: Not flushing after style changes → **Right**: Flush affected styles (serving outdated derivatives, user confusion)
- **Wrong**: Pre-generating all derivatives → **Right**: Use lazy generation (wastes storage and processing, most unused)
- **Wrong**: Allowing insecure derivatives on public internet → **Right**: Use tokens or CDN security (attacker can exhaust disk/CPU)
- **Wrong**: Not monitoring derivative storage → **Right**: Monitor with du/find (disk fills silently, site crashes)

## See Also

- [WebP & AVIF Optimization](webp-avif-optimization.md)
- [Best Practices & Patterns](best-practices.md)
- Reference: core/modules/image/src/Entity/ImageStyle.php (getPathToken method)
- Reference: https://www.drupal.org/docs/security-in-drupal
