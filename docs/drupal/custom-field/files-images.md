---
description: File upload and image sub-fields with widget configuration, extended properties for alt/title/dimensions, and media library integration.
---

# Files and Images

## When to Use

You need file uploads or images within a custom field column.

## Pattern

**File column configuration**:

```yaml
columns:
  attachment:
    name: attachment
    type: file
    uri_scheme: public
```

**Image column configuration**:

```yaml
columns:
  photo:
    name: photo
    type: image
    uri_scheme: public
```

**Widget configuration**:

```php
$settings['field_settings']['photo'] = [
  'widget' => 'image',
  'widget_settings' => [
    'upload_location' => 'field/custom/[entity_type]/[field_name]',
    'file_extensions' => 'png jpg jpeg gif',
    'max_filesize' => '5 MB',
    'max_resolution' => '1920x1080',
    'min_resolution' => '100x100',
    'alt_field' => TRUE,
    'alt_field_required' => TRUE,
    'title_field' => FALSE,
  ],
];
```

**Accessing image data**:

```php
$file_id = $node->field_custom->photo;
$alt = $node->field_custom->{'photo__alt'};
$title = $node->field_custom->{'photo__title'};
$width = $node->field_custom->{'photo__width'};
$height = $node->field_custom->{'photo__height'};

$file = \Drupal::entityTypeManager()->getStorage('file')->load($file_id);
if ($file) {
  $url = $file->createFileUrl();
}
```

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Single file upload (PDF, doc, etc.) | file type + FileWidget | Basic upload with extension filtering |
| Image with alt text and dimensions | image type + ImageWidget | Includes accessibility fields, auto-dimensions |
| Media library integration | image type + custom_field_media sub-module | Media entity integration, reusable media |

## Common Mistakes

- **Not setting upload_location** -- Files go to default location; harder to organize
- **Public files for sensitive content** -- Use uri_scheme=private for access-controlled files
- **Missing alt_field_required** -- Accessibility requirement; make alt text required for images
- **Not cleaning up files on entity delete** -- File entities orphaned; use file_usage tracking
- **Forgetting to check file exists** -- File entity can be deleted separately; always check `$file !== NULL`

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/ImageWidget.php`
- Sub-module: custom_field_media
