---
description: Selection and file elements — dropdowns, radios, checkboxes, uploads
drupal_version: "11.x"
---

# Form Elements: Selection and File Elements

## When to Use

> Use radios/checkboxes when options should be visible. Use select to save space. Use entity_autocomplete for many options.

## Decision

| Scenario | Element | Why |
|----------|---------|-----|
| 2-5 options, single choice | radios | All options visible |
| >5 options, single choice | select | Space-efficient |
| >50 options | entity_autocomplete | Performance |
| Multiple selections | checkboxes | Clear multi-select |
| Boolean choice | checkbox | Single toggle |
| File upload (basic) | file | Simple upload |
| File upload (managed) | managed_file | Drupal file entity |

## Selection Elements

**Single-Choice Elements:**
| Element | Display | When to Use | Key Properties |
|---------|---------|-------------|----------------|
| select | Dropdown | >5 options, space-limited | #options, #empty_option, #empty_value |
| radios | Radio buttons | 2-5 options, need visibility | #options |

**Multiple-Choice Elements:**
| Element | Display | When to Use | Key Properties |
|---------|---------|-------------|----------------|
| checkboxes | Checkbox group | Multiple selections | #options |
| checkbox | Single checkbox | Boolean choice | #return_value, #default_value |
| select with #multiple | Multi-select | Many options, power users | #options, #multiple => TRUE, #size |

## #options Format

```php
// Simple
['key1' => 'Label 1', 'key2' => 'Label 2']

// Grouped
['Group' => ['key1' => 'Label 1']]

// From entity
// Use EntityAutocomplete or custom callback
```

## Select Element Special Properties

```php
'#empty_option' => '- Select -',  // Placeholder text
'#empty_value' => '',             // Value when empty option chosen
'#multiple' => TRUE,              // Enable multi-select
'#size' => 10,                    // Visible rows (multi-select only)
```

## File Upload Elements

**File Element Types:**
| Element | Purpose | Managed | Features |
|---------|---------|---------|----------|
| file | Basic upload | No | #upload_validators, #multiple |
| managed_file | Drupal file entity | Yes | Same + permanent file handling |

**Upload Validators:**
```php
'#upload_validators' => [
  'file_validate_extensions' => ['jpg jpeg png'],
  'file_validate_size' => [2 * 1024 * 1024], // 2MB
  'file_validate_image_resolution' => ['1920x1080'],
],
```

**File Element Properties:**
```php
'#upload_location' => 'public://uploads',  // or 'private://docs'
'#upload_validators' => [...],             // Array of validators
'#multiple' => TRUE,                       // Allow multiple files
'#description' => t('Allowed: jpg, png. Max 2MB'), // User guidance
```

## Security Considerations

- Always validate file extensions
- Set reasonable file size limits
- Use private:// for sensitive files
- Never trust client-provided filenames

Reference: `/web/core/modules/file/src/Element/ManagedFile.php`

## Common Mistakes

- **Wrong**: Not setting #upload_validators (security risk) → **Right**: Always validate extensions and size
- **Wrong**: Using file instead of managed_file (file orphans) → **Right**: Use managed_file for permanent files
- **Wrong**: Forgetting to set #upload_location → **Right**: Specify public:// or private://
- **Wrong**: Not showing allowed extensions in #description → **Right**: Guide users with clear requirements

## See Also

- [Input Elements](elements-input.md)
- [Security Best Practices](security-best-practices.md)
- [File API](https://www.drupal.org/docs/drupal-apis/file-api)
- Reference: `/web/core/lib/Drupal/Core/Render/Element/Select.php`
