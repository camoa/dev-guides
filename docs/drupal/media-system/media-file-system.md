---
description: Media file storage configuration — public vs private files, date-organized directories, S3/CDN integration, and oEmbed thumbnail storage.
---

## 17. Media File System

### When to Use

You need to configure where media files are stored: public vs private, directory structure, CDN integration.

### Decision

| Storage Type | Use Case | Path |
|---|---|---|
| Public files | Images, videos for public site | `public://` (sites/default/files/) |
| Private files | PDFs, documents with access control | `private://` (sites/default/files/private/) |
| S3/CDN (contrib) | High-traffic sites, distributed storage | `s3://` via flysystem module |
| Date-organized | Default media organization | `public://[date:custom:Y-m]/` |

### Pattern

**Public image storage** (default):
```yaml
# In field.field.media.image.field_media_image.yml
settings:
  file_directory: '[date:custom:Y]-[date:custom:m]'
  uri_scheme: public
```

Resulting path: `sites/default/files/2026-02/image.jpg`

**Private document storage**:
```yaml
# In field.field.media.document.field_media_document.yml
settings:
  file_directory: 'documents/[date:custom:Y]'
  uri_scheme: private
```

Resulting path: `sites/default/files/private/documents/2026/document.pdf`

**S3 storage via Flysystem**:

1. Install: `composer require drupal/flysystem drupal/flysystem_s3`
2. Configure settings.php:

```php
$settings['flysystem'] = [
  's3' => [
    'driver' => 's3',
    'config' => [
      'key' => getenv('S3_KEY'),
      'secret' => getenv('S3_SECRET'),
      'region' => 'us-east-1',
      'bucket' => 'my-bucket',
      'prefix' => 'media',
    ],
    'serve_js' => TRUE,
    'serve_css' => TRUE,
  ],
];
```

3. Configure field to use S3:

```yaml
settings:
  uri_scheme: s3
```

**oEmbed thumbnail storage**:
```yaml
# In media.type.remote_video.yml
source_configuration:
  source_field: field_media_oembed_video
  thumbnails_directory: 'public://oembed_thumbnails/[date:custom:Y-m]'
```

### Common Mistakes

- Using private:// for public images → breaks image styles and CDN delivery; use public:// for site images
- Not organizing by date → thousands of files in one directory causes filesystem performance issues
- Hardcoding file paths → breaks portability; use stream wrappers (public://, private://)
- Exposing private files via direct URLs → bypasses access control; use Drupal file download routes
- Not configuring CDN for media → serving large files from Drupal app server wastes resources; use CDN
- Mixed storage schemes on same media type → causes confusion; be consistent per media type

### See Also

- [Media Access & Permissions](media-access-permissions.md)
- Reference: `/core/modules/file/file.module`
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/managing-files
- Reference: https://www.drupal.org/project/flysystem
