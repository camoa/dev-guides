---
description: Selection and file upload elements - select, radios, checkboxes, file uploads
drupal_version: "11.x"
---

# Form Elements: Selection and File Elements

## When to Use

> Choose selection elements based on number of options and whether multiple selections are allowed. Use entity_autocomplete for >50 options.

## Decision

| Situation | Element | Why |
|-----------|---------|-----|
| 2-5 options, single choice | radios | Visibility, clarity |
| >5 options, single choice | select | Space-efficient |
| >50 options, single choice | entity_autocomplete | Performance |
| Multiple selections, few options | checkboxes | All options visible |
| Multiple selections, many options | select with #multiple | Space-efficient |
| Binary choice | checkbox | Simple yes/no |
| File upload, no management | file | Basic upload |
| File upload with entity | managed_file | Drupal file handling |

## Selection Pattern

```php
// Select dropdown
$form['type'] = [
  '#type' => 'select',
  '#title' => $this->t('Type'),
  '#options' => [
    'option1' => 'Label 1',
    'option2' => 'Label 2',
  ],
  '#empty_option' => '- Select -',
];

// Radio buttons
$form['choice'] = [
  '#type' => 'radios',
  '#title' => $this->t('Choose One'),
  '#options' => [
    'yes' => 'Yes',
    'no' => 'No',
  ],
];

// Checkboxes (multiple)
$form['tags'] = [
  '#type' => 'checkboxes',
  '#title' => $this->t('Tags'),
  '#options' => ['tag1' => 'Tag 1', 'tag2' => 'Tag 2'],
];

// Single checkbox
$form['agree'] = [
  '#type' => 'checkbox',
  '#title' => $this->t('I agree to terms'),
  '#return_value' => 1,
];
```

## File Upload Pattern

```php
$form['document'] = [
  '#type' => 'managed_file',
  '#title' => $this->t('Upload Document'),
  '#upload_location' => 'private://documents/', // CRITICAL: private, not public
  '#upload_validators' => [
    'file_validate_extensions' => ['pdf doc docx'], // Whitelist only
    'file_validate_size' => [5 * 1024 * 1024], // 5MB max
  ],
  '#description' => $this->t('Allowed: PDF, DOC, DOCX. Max 5MB.'),
];
```

## Upload Validators

| Validator | Purpose | Example |
|-----------|---------|---------|
| file_validate_extensions | Whitelist file types | `['jpg jpeg png pdf']` |
| file_validate_size | Max file size (bytes) | `[5 * 1024 * 1024]` (5MB) |
| file_validate_image_resolution | Max image dimensions | `['5000x5000']` |

## Common Mistakes

- **Wrong**: No #upload_validators on file uploads → **Right**: Always validate (security risk)
- **Wrong**: Using file instead of managed_file → **Right**: Use managed_file (prevents orphans)
- **Wrong**: public:// for user uploads → **Right**: Use private:// (security)
- **Wrong**: No allowed extensions in description → **Right**: Inform users

## See Also

- [File API Guide](https://www.drupal.org/docs/drupal-apis/file-api)
- [Security: File Upload](security-best-practices.md)
- Reference: `/web/core/modules/file/src/Element/ManagedFile.php`
