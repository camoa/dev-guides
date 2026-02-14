---
description: Validating user input with Form API, typed data constraints, URL validation, file validation, and output sanitization patterns.
---

# Input Validation and Sanitization

## When to Use
Every point where user input enters the system -- validation ensures data integrity; sanitization prevents injection attacks.

## Steps
1. **Form API validation (preferred)**
   ```php
   public function validateForm(array &$form, FormStateInterface $form_state) {
     $email = $form_state->getValue('email');

     // Email validation
     if (!\Drupal::service('email.validator')->isValid($email)) {
       $form_state->setErrorByName('email', $this->t('Invalid email address.'));
     }

     // Range validation
     $age = $form_state->getValue('age');
     if ($age < 0 || $age > 120) {
       $form_state->setErrorByName('age', $this->t('Age must be between 0 and 120.'));
     }

     // Length validation
     $name = $form_state->getValue('name');
     if (mb_strlen($name) > 255) {
       $form_state->setErrorByName('name', $this->t('Name too long.'));
     }
   }
   ```

2. **Use typed data for complex validation**
   ```php
   // In entity field definition
   $fields['email'] = BaseFieldDefinition::create('email')
     ->setLabel('Email')
     ->setRequired(TRUE)
     // Validation happens automatically based on type
     ->addConstraint('Email');  // EmailConstraint validator

   $fields['age'] = BaseFieldDefinition::create('integer')
     ->addConstraint('Range', ['min' => 0, 'max' => 120]);
   ```

3. **Validate URLs**
   ```php
   use Drupal\Component\Utility\UrlHelper;

   // Check if valid URL
   if (!UrlHelper::isValid($url, TRUE)) {  // TRUE = require absolute URL
     // Invalid
   }

   // Check if external
   if (UrlHelper::isExternal($url)) {
     // External URL, handle carefully
   }

   // Strip dangerous protocols
   $safe_url = UrlHelper::filterBadProtocol($url);
   // Removes javascript:, data:, vbscript: etc.
   ```

4. **Sanitize on output (not input)**
   ```php
   // WRONG: Don't sanitize on input (store original)
   $form_state->setValue('bio', Xss::filter($bio));  // Loses data

   // CORRECT: Sanitize on output
   $build['#markup'] = Xss::filter($node->get('bio')->value);
   ```

5. **File validation**
   ```php
   // In form
   $form['file'] = [
     '#type' => 'managed_file',
     '#upload_validators' => [
       'FileExtensionValidator' => [
         'extensions' => 'jpg jpeg png gif',
       ],
       'FileSizeValidator' => [
         'fileLimit' => '2M',
       ],
     ],
   ];
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Validation stage | User submitting form | Use Form API `validateForm()` |
| Validation stage | Saving entity | Use entity constraints/typed data |
| Validation stage | REST API input | Use serialization denormalization constraints |
| Data type | Email | Use `email.validator` service |
| Data type | URL | Use `UrlHelper::isValid()` |
| Data type | Numeric range | Use typed data constraints |
| Output | Displaying user input | Sanitize with `Xss::filter()` or Twig autoescape |

## Common Mistakes
- Sanitizing on input instead of output -- Data loss, can't reconstruct original
- Trusting client-side validation -- Always validate server-side
- Not validating length -- Database errors, buffer overflows
- Blacklisting instead of whitelisting -- Allow known-good, don't block known-bad
- Using `filter_var()` inconsistently -- Use Drupal's utilities for consistency
- Not validating file uploads -- **CRITICAL**: Unrestricted upload = remote code execution

## See Also
- Reference: `/core/lib/Drupal/Component/Utility/UrlHelper.php`
- [XSS Prevention](xss-prevention.md) for output sanitization
- Reference: https://www.drupal.org/docs/administering-a-drupal-site/security-in-drupal/writing-secure-code-for-drupal
