---
description: Media system security and performance — file upload validation, access control, oEmbed security, CSP, image delivery optimization, caching, and CDN integration.
---

## 20. Security & Performance

### Security Best Practices

**File Upload Validation**

**Whitelist file extensions**:
```yaml
settings:
  file_extensions: 'png gif jpg jpeg webp'  # Images only
  # Documents: 'pdf doc docx xls xlsx ppt pptx'
  # NEVER: svg php js exe sh
```
- **Why**: SVG can contain XSS, PHP/JS can execute on server
- **Threshold**: Never allow executable extensions

**Limit file size**:
```yaml
settings:
  max_filesize: '10 MB'
  max_resolution: '3840x3840'
```
- **Why**: Prevent DoS via huge uploads, disk exhaustion
- **Threshold**: 10 MB for images, 50 MB for videos, 5 MB for documents

**Validate image dimensions**:
```yaml
settings:
  min_resolution: '100x100'
  max_resolution: '3840x3840'
```
- **Why**: Reject tiny images (tracking pixels) and massive images (memory exhaustion)

**Access Control**

**Never bypass media access checks**:
```php
// WRONG: Direct file URL
$url = $media->field_media_image->entity->getFileUri();

// CORRECT: Access-controlled URL
$url = $media->field_media_image->entity->createFileUrl();
```

**Check permissions before showing widgets**:
```php
if (\Drupal::currentUser()->hasPermission('create image media')) {
  // Show upload widget
}
```

**Filter unpublished media in public queries**:
```php
$query->condition('status', 1);
```

**Use private files for restricted content**:
```yaml
settings:
  uri_scheme: private
```
- **Why**: Public files accessible via direct URL, bypass access control

**oEmbed Security**

**Validate oEmbed providers**:
```yaml
source_configuration:
  providers:
    - YouTube
    - Vimeo
  # Don't allow arbitrary URLs
```
- **Why**: Prevents SSRF attacks, malicious embed codes

**Set iframe_domain for oEmbed isolation**:
```yaml
# media.settings.yml
iframe_domain: 'https://media.example.com'
```
- **Why**: Isolates third-party embeds to separate domain, prevents XSS

**Content Security Policy**

Configure CSP headers for media:
```php
// settings.php or .htaccess
$config['media']['csp'] = [
  'frame-src' => ['https://www.youtube.com', 'https://player.vimeo.com'],
  'img-src' => ['https://i.ytimg.com', 'https://i.vimeocdn.com'],
];
```

### Performance Optimization

**Image Delivery**

**Always use responsive images**:
```yaml
content:
  field_media_image:
    type: responsive_image
    settings:
      responsive_image_style: hero
```
- **Why**: Delivers appropriate size per device, saves bandwidth
- **Impact**: 50-70% bandwidth reduction on mobile

**Enable lazy loading**:
```yaml
settings:
  image_loading:
    attribute: lazy
```
- **Why**: Defers offscreen image loading, faster initial page load
- **Impact**: 20-40% faster page load
- **Exception**: Disable for above-fold hero images (loads too late)

**Use WebP format**:
```yaml
# In image style config:
effects:
  convert:
    id: image_convert
    data:
      extension: webp
```
- **Why**: 25-35% smaller than JPEG at same quality
- **Fallback**: Use `<picture>` with JPEG fallback for old browsers

**Queue remote thumbnails**:
```yaml
queue_thumbnail_downloads: true
```
- **Why**: Non-blocking thumbnail fetch, doesn't delay media save
- **Impact**: Eliminates 1-3s wait on oEmbed uploads

**CDN Integration**

**Use CDN for media files**:
- Drupal CDN module: https://www.drupal.org/project/cdn
- Flysystem S3: https://www.drupal.org/project/flysystem_s3
- **Impact**: 40-60% faster image delivery, offloads app server

**Set appropriate cache max-age**:
```php
// settings.php — configure page cache lifetime
$config['system.performance']['css']['preprocess'] = TRUE;
$config['system.performance']['js']['preprocess'] = TRUE;
// Image derivatives are cached at the web server level via .htaccess rules
// For CDN: set Cache-Control headers via CDN configuration, not Drupal config
```

**Caching**

**Enable entity view caching**:
```yaml
# In view mode config:
cache: true
```

**BigPipe** (enabled by default in Drupal 10+):
- Works automatically for authenticated users — no display config needed
- Streams page content progressively, improving perceived performance for media-heavy pages

**Cache remote API responses**:
```php
// For custom media sources
$cache_backend->set($cid, $data, $expire_time);
```

**Database Optimization**

**Index media reference fields**:
```yaml
# Drupal handles this automatically for entity_reference
# Verify with: drush sqlq "SHOW INDEX FROM node__field_hero_image"
```

**Limit cardinality on unlimited fields**:
- **Why**: Unbounded galleries cause memory issues, slow rendering
- **Threshold**: Cap at 50-100 images per gallery

**File System**

**Organize uploads by date**:
```yaml
settings:
  file_directory: '[date:custom:Y]-[date:custom:m]'
```
- **Why**: Too many files in one directory degrades filesystem performance
- **Threshold**: Keep directories under 5000 files

**Use public:// for public media**:
- **Why**: private:// requires Drupal bootstrap for every file request (slow)
- **Impact**: 10x faster file delivery with public:// + CDN

**Monitoring**

**Key metrics to monitor**:
- Average image file size: target < 500 KB for heroes, < 150 KB for cards
- Lazy loading effectiveness: measure LCP improvement
- CDN cache hit rate: target > 85%
- Media entity cache hit rate: target > 90%
- Image derivative generation time: target < 2s for largest size

**Performance testing**:
```bash
# Measure page weight
drush pm:enable webprofiler
# Analyze delivered image sizes

# Test image derivative generation
time drush image:flush --all
drush image:derive thumbnail public://2026-02/test.jpg

# Measure Media Library load time
drush webprofiler:analyze --url=/admin/content/media
```

### See Also

- [Media File System](media-file-system.md)
- [Best Practices & Patterns](best-practices-patterns.md)
- Reference: https://www.drupal.org/docs/security/securing-file-uploads-and-directories
- Reference: https://web.dev/articles/fast (general web performance)
