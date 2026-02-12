---
description: Selection and file elements — dropdowns, radios, checkboxes, uploads
drupal_version: "11.x"
---

# Form Elements: Selection and File Elements

### Selection Elements

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

**#options Format:**
```
Simple: ['key1' => 'Label 1', 'key2' => 'Label 2']
Grouped: ['Group' => ['key1' => 'Label 1']]
From entity: Use EntityAutocomplete or custom callback
```

**Select Element Special Properties:**
```
#empty_option: Placeholder text (e.g., "- Select -")
#empty_value: Value when empty option chosen (default: '')
#multiple: Enable multi-select
#size: Visible rows (multi-select only)
```

### Decision Matrix: Selection Elements

```
Options visible always? → radios or checkboxes
Save space? → select
Binary choice? → checkbox (single)
2-5 options? → radios (single) or checkboxes (multiple)
>5 options? → select
>50 options? → entity_autocomplete
User needs to see all options? → radios/checkboxes
```

### File Upload Elements

**File Element Types:**
| Element | Purpose | Managed | Features |
|---------|---------|---------|----------|
| file | Basic upload | No | #upload_validators, #multiple |
| managed_file | Drupal file entity | Yes | Same + permanent file handling |

**Upload Validators:**
```
file_validate_extensions: ['jpg jpeg png']
file_validate_size: [max_bytes]
file_validate_image_resolution: [max_width, max_height]
```

**File Element Properties:**
```
#upload_location: 'public://uploads' or 'private://docs'
#upload_validators: Array of validator callbacks
#multiple: Allow multiple files
#description: Shows allowed extensions/size to user
```

**Security Considerations:**
```
Always validate file extensions
Set reasonable file size limits
Use private:// for sensitive files
Never trust client-provided filenames
```

**Reference:** `/web/core/modules/file/src/Element/ManagedFile.php`

**Common Mistakes:**
- Not setting #upload_validators (security risk)
- Using file instead of managed_file (file orphans)
- Forgetting to set #upload_location
- Not showing allowed extensions in #description

**See Also:**
- File API Guide
- Security: File Upload Guide
- Media vs File Decision Guide
