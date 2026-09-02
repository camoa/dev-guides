---
description: Upload files via AJAX using managed_file with validation, progress indicators, and preview callbacks
tldr: "Use `#type => 'managed_file'` with AJAX for file uploads that need immediate preview or feedback (avatars, attachments, media galleries). Always configure upload validators."
drupal_version: "11.x"
---

# File Upload Patterns

## When to Use

You need to upload files via AJAX without full form submission (avatar uploads, attachment addition, media galleries).

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
        'type' => 'bar',  // Progress bar for large files
        'message' => t('Uploading...'),
      ],
    ],
  ];

  $form['preview'] = [
    '#type' => 'container',
    '#attributes' => ['id' => 'file-preview'],
  ];

  // Show preview if file uploaded
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

- Not configuring upload validators → Security risk; always validate extensions, size, dimensions
- Using `#type => 'file'` instead of `managed_file` → File not saved to database, lost after form submission
- Forgetting upload location → Files saved to temporary directory, may be deleted
- Not handling upload errors → Users don't know why upload failed; check `$form_state->getErrors()`
- Missing progress bar for large files → Poor UX; use `'type' => 'bar'` for uploads >1MB

## See Also

- ← Previous: [Custom Route Implementation](custom-route-implementation.md) | Next: [Autocomplete Implementation](autocomplete-implementation.md)
- Reference: [File API documentation](https://www.drupal.org/docs/drupal-apis/file-api)
