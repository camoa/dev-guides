---
description: Upload files via AJAX using managed_file with validation, progress indicators, and preview callbacks
drupal_version: "11.x"
---

# File Upload Patterns

## When to Use

> Use `#type => 'managed_file'` with AJAX for file uploads that need immediate preview or feedback (avatars, attachments, media galleries). Always configure upload validators.

## Pattern

```php
public function buildForm(array $form, FormStateInterface $form_state) {
  $form['file_upload'] = [
    '#type' => 'managed_file',
    '#title' => t('Upload File'),
    '#upload_location' => 'public://uploads/',
    '#upload_validators' => [
      'FileExtension' => ['extensions' => 'jpg jpeg png gif'],
      'FileSizeLimit' => ['fileLimit' => '2M'],
    ],
    '#ajax' => [
      'callback' => '::fileUploadCallback',
      'wrapper' => 'file-preview',
      'event' => 'change',
      'progress' => [
        'type' => 'bar',       // Progress bar for large files
        'message' => t('Uploading...'),
      ],
    ],
  ];

  $form['preview'] = [
    '#type' => 'container',
    '#attributes' => ['id' => 'file-preview'],
  ];

  $file_id = $form_state->getValue('file_upload');
  if (!empty($file_id[0])) {
    $file = File::load($file_id[0]);
    $form['preview']['image'] = [
      '#theme' => 'image_style',
      '#style_name' => 'thumbnail',
      '#uri' => $file->getFileUri(),
    ];
  }

  return $form;
}

public function fileUploadCallback(array &$form, FormStateInterface $form_state) {
  return $form['preview'];
}
```

Reference: `core/modules/file/src/Element/ManagedFile.php`

## Common Mistakes

- **Wrong**: Not configuring upload validators → **Right**: Security risk; always validate extensions, size, and MIME type
- **Wrong**: Using `#type => 'file'` instead of `managed_file` → **Right**: File not saved to database, lost after form submission
- **Wrong**: Forgetting upload location → **Right**: Files saved to temporary directory, may be deleted automatically
- **Wrong**: Not handling upload errors → **Right**: Users don't know why upload failed; check `$form_state->getErrors()`
- **Wrong**: No progress bar for large files → **Right**: Poor UX; use `'type' => 'bar'` for uploads >1MB

## See Also

- [Custom Route Implementation](custom-route-implementation.md)
- [Autocomplete Implementation](autocomplete-implementation.md)
- Reference: [File API documentation](https://www.drupal.org/docs/drupal-apis/file-api)
