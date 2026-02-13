---
description: File and image fields with security validation and performance optimization
drupal_version: "11.x"
---

# File and Image Field Patterns

## When to Use

When handling file uploads (documents, images, media) requiring file validation, storage organization, and derivative generation.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Generic file upload | file field type | Handles any MIME type with validation |
| Images with derivatives | image field type | Automatic image styles, metadata |
| File organization | file_directory setting | Token-based directory structure |
| Security validation | file_extensions, max_filesize | Prevent malicious uploads |
| Image metadata | alt/title fields | Accessibility and SEO |

## Pattern

Image field with security and performance settings:

```php
BaseFieldDefinition::create('image')
  ->setLabel(t('Image'))
  ->setSetting('file_directory', 'images/[date:custom:Y]-[date:custom:m]')
  ->setSetting('file_extensions', 'png jpg jpeg webp')
  ->setSetting('max_filesize', '5 MB')
  ->setSetting('max_resolution', '3000x3000')
  ->setSetting('min_resolution', '400x300')
  ->setSetting('alt_field', TRUE)
  ->setSetting('alt_field_required', TRUE)
  ->setSetting('title_field', FALSE)
  ->setDisplayOptions('form', [
    'type' => 'image_image',
    'weight' => 5,
  ])
  ->setDisplayOptions('view', [
    'type' => 'image',
    'label' => 'hidden',
    'settings' => [
      'image_style' => 'large',
      'image_loading' => ['attribute' => 'lazy'],
    ],
  ]);
```

File field with upload validation:

```php
BaseFieldDefinition::create('file')
  ->setLabel(t('Document'))
  ->setSetting('file_directory', 'documents/[node:created:custom:Y]')
  ->setSetting('file_extensions', 'pdf doc docx xls xlsx txt')
  ->setSetting('max_filesize', '10 MB')
  ->setSetting('description_field', TRUE);
```

Reference: `/core/modules/file/src/Plugin/Field/FieldType/FileItem.php`, `/core/modules/image/src/Plugin/Field/FieldType/ImageItem.php`

## Common Mistakes

- **Wrong**: Not restricting file_extensions → **Right**: CRITICAL security risk; allow .php uploads = RCE
- **Wrong**: Missing max_filesize → **Right**: Disk space exhaustion, DoS attacks
- **Wrong**: Not requiring alt_field → **Right**: Accessibility failure, WCAG violation
- **Wrong**: Allowing dangerous extensions → **Right**: .exe, .js, .phtml, .svg (can contain JavaScript)
- **Wrong**: Using public:// for sensitive files → **Right**: Files directly accessible; use private:// with access control
- **Wrong**: Not setting file_directory → **Right**: All files in root; poor organization, slow filesystem operations
- **Wrong**: Using original images in display → **Right**: Performance issue; always use image_style

**Security (CRITICAL)**:
- ALWAYS whitelist file_extensions. NEVER allow executable types.
- Dangerous extensions: php, phtml, php3, php4, php5, phar, exe, js, html, htm, svg (can embed JS)
- Safe extensions: png, jpg, jpeg, gif, webp, pdf, doc, docx, txt, csv, zip
- Use private:// stream for sensitive files. Public files bypass access control.
- Validate uploaded files in hook_file_validate(). Don't trust MIME types (client-provided).
- Set max_filesize to prevent disk exhaustion DoS attacks.

**Performance**:
- Use file_directory with date tokens to distribute files: `[date:custom:Y]-[date:custom:m]`
- Prevents single directory with millions of files (filesystem performance degrades)
- ALWAYS use image_style in formatters. Never display original images.
- Set image_loading: lazy for below-fold images (improves LCP by ~30%)
- Use WebP format for web delivery (image styles can auto-convert)

**Accessibility**:
- ALWAYS require alt_field for images. It's not optional.
- alt_field_required: TRUE is mandatory for WCAG 2.1 Level A compliance.
- Provide helpful alt text guidance in field description.

## See Also

- [Entity Reference Patterns](entity-reference-patterns.md)
- [Computed Field Patterns](computed-field-patterns.md)
- Reference: [File fields](https://www.drupal.org/docs/drupal-apis/entity-api/fieldtypes-fieldwidgets-and-fieldformatters)
