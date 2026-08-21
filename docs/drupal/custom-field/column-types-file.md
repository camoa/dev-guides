---
description: "File and image column types in Custom Field 5.0.2 -- storage settings, extended alt/title/width/height properties, and upload gotchas."
tldr: "file stores a bare file entity ID; image adds extended field__alt/field__title/field__width/field__height properties with dimensions auto-populated on save -- widget settings, not storage, control allowed extensions."
drupal_version: "11.x"
---

# Column Types: File Fields

## When to Use

Storing file uploads or images in custom field columns.

## file

File upload reference (stores file entity ID).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| target_type | string | file | Always 'file' (auto-set) |
| uri_scheme | string | public | public/private |

**Schema:** `INT UNSIGNED NOT NULL DEFAULT 0` (file entity ID)

```yaml
columns:
  attachment:
    name: attachment
    type: file
    uri_scheme: public
```

**Gotchas:** File entity ID stored, not file path. Use FileWidget with upload_location, max_filesize, file_extensions settings.

## image

Image file with extended properties (alt, title, width, height).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| target_type | string | file | Always 'file' (auto-set) |
| uri_scheme | string | public | public/private |

**Schema:** `INT UNSIGNED NOT NULL DEFAULT 0` (file entity ID)

**Extended properties:**

- `field__alt` -- VARCHAR(512) alt text
- `field__title` -- VARCHAR(1024) title text
- `field__width` -- INT image width in pixels
- `field__height` -- INT image height in pixels

```yaml
columns:
  thumbnail:
    name: thumbnail
    type: image
    uri_scheme: public
```

**Gotchas:** Width/height auto-populated from image dimensions on save. Alt text separate from file entity. Access via `$item->{'thumbnail__alt'}`.

## Common Mistakes

- **Not configuring file extensions** -- Widget settings control allowed extensions; storage doesn't validate
- **Using public for sensitive files** -- Set uri_scheme=private for files requiring access control
- **Forgetting alt text for accessibility** -- image type stores alt in extended property; required for accessibility
- **Not setting upload location** -- Configure via widget settings: `upload_location` like `field/[entity_type]/[field_name]`

## See Also

- [Column Types: Reference Fields](column-types-reference.md)
- [Column Types: Data Fields](column-types-data.md)
- [Files and Images](files-images.md) -- widget configuration and code access patterns
