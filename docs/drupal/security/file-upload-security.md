---
description: Securing file uploads with extension whitelists, MIME validation, private file storage, filename sanitization, and directory protection.
---

# File Upload Security

## When to Use
Whenever users can upload files -- unrestricted file upload is one of the most dangerous vulnerabilities (remote code execution).

## Steps
1. **Use managed_file form element (automatic validation)**
   ```php
   $form['attachment'] = [
     '#type' => 'managed_file',
     '#title' => $this->t('Upload file'),
     '#upload_location' => 'private://attachments/',
     '#upload_validators' => [
       'FileExtensionValidator' => [
         'extensions' => 'jpg jpeg png gif pdf doc docx',
       ],
       'FileSizeValidator' => [
         'fileLimit' => '5M',
       ],
     ],
   ];
   ```

2. **Configure safe upload locations**
   ```php
   // Public files (web-accessible) - for images, CSS, JS
   'public://path/to/files'

   // Private files (access-controlled) - for user documents
   'private://secure/documents/'

   // Temporary files (auto-cleaned)
   'temporary://uploads/'
   ```

   Set private path in settings.php:
   ```php
   $settings['file_private_path'] = '/var/www/private';
   ```

3. **Whitelist extensions, never blacklist**
   ```php
   // CORRECT: Whitelist known-safe
   'extensions' => 'jpg jpeg png gif'

   // WRONG: Blacklist dangerous (incomplete, bypassable)
   'extensions_blacklist' => 'php phtml exe'
   ```

4. **Validate MIME types**
   ```php
   use Symfony\Component\Mime\MimeTypes;

   $mime_types = new MimeTypes();
   $allowed_mimes = ['image/jpeg', 'image/png', 'application/pdf'];

   $file_mime = $mime_types->guessMimeType($file->getFileUri());
   if (!in_array($file_mime, $allowed_mimes)) {
     // Reject
   }
   ```

5. **Sanitize filenames**
   ```php
   use Drupal\Component\Utility\Html;

   // Drupal sanitizes automatically, but for manual handling:
   $filename = \Drupal::service('file_system')->basename($original_filename);
   $filename = preg_replace('/[^a-zA-Z0-9._-]/', '_', $filename);
   ```

6. **Protect upload directories**
   ```apache
   # In .htaccess for upload directory
   <FilesMatch "\.(php|phtml|pl|py|jsp|asp|sh|cgi)$">
     Require all denied
   </FilesMatch>
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Upload location | Public display (images) | Use `public://` with extension whitelist |
| Upload location | User documents | Use `private://` with access checks |
| Extension policy | Accepting uploads | Whitelist only, minimal set needed |
| File processing | Images | Re-encode with GD/ImageMagick to strip exploits |
| File type | Executables needed | **DON'T** -- find alternative (JSON data, etc.) |

## Common Mistakes
- Allowing .php, .phtml, .php5 uploads -- **CRITICAL**: Remote code execution
- Using blacklist instead of whitelist -- Bypassable (.php5, .phar, etc.)
- Trusting file extension -- Attacker can rename; validate MIME too
- Uploading to web root -- Files directly accessible, executable
- Not validating file size -- Disk exhaustion DoS
- Allowing double extensions (file.php.jpg) -- Some servers execute .php
- Not re-encoding images -- Embedded PHP in EXIF/comment metadata

## See Also
- Reference: `/core/modules/file/src/Upload/FileUploadHandler.php`
- [Input Validation and Sanitization](input-validation-and-sanitization.md) for general validation
- Reference: https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload
