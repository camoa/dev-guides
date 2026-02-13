---
description: Validating media source field values with custom constraints
drupal_version: "11.x"
---

# Validation Constraints

## When to Use

> Use validation constraints when validating source field values before saving media entities (URL patterns, API connectivity, file types).

## Decision

| Validation Type | Constraint Approach | Example |
|----------------|---------------------|---------|
| URL pattern validation | Custom regex constraint | Instagram shortcode format |
| API connectivity check | Custom constraint with HTTP call | Verify resource exists at API |
| File type validation | Built-in file extension constraint | Already handled by File source |
| Value uniqueness | Unique field constraint | Prevent duplicate media items |

## Pattern

Implementing validation constraint (3 files, ~15 lines total):

Step 1 - Plugin implements interface:
```php
use Drupal\media\MediaSourceFieldConstraintsInterface;

class CustomApi extends MediaSourceBase implements MediaSourceFieldConstraintsInterface {
  public function getSourceFieldConstraints(): array {
    return ['CustomApiUrl' => []];
  }
}
```

Step 2 - Constraint definition:
```php
// src/Plugin/Validation/Constraint/CustomApiUrlConstraint.php
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\Validator\Constraint;
use Drupal\Core\Validation\Attribute\Constraint as ConstraintAttribute;

#[ConstraintAttribute(
  id: 'CustomApiUrl',
  label: new TranslatableMarkup('Custom API URL validation'),
)]
class CustomApiUrlConstraint extends Constraint {
  public string $message = 'URL must match pattern: @pattern';
}
```

Step 3 - Validator implementation:
```php
// src/Plugin/Validation/Constraint/CustomApiUrlConstraintValidator.php
use Symfony\Component\Validator\ConstraintValidator;

class CustomApiUrlConstraintValidator extends ConstraintValidator {
  const PATTERN = '@example\\.com/item/([^/?#]+)@i';

  public function validate($value, Constraint $constraint): void {
    if (empty($value->value)) return;

    if (!preg_match(self::PATTERN, $value->value)) {
      $this->context->addViolation($constraint->message, ['@pattern' => self::PATTERN]);
    }
  }
}
```

## Common Mistakes

- **Wrong**: Not implementing `MediaSourceFieldConstraintsInterface` → **Right**: Implement interface for constraint discovery
- **Wrong**: Expensive validation (API calls) → **Right**: Keep validation fast, queue expensive checks
- **Wrong**: Not handling empty values → **Right**: Check for empty and skip validation
- **Wrong**: Weak regex patterns → **Right**: Strong, security-focused regex
- **Wrong**: No user feedback → **Right**: Clear violation messages with examples

## See Also

- Previous: [Dependency Injection](dependency-injection.md)
- Next: [Display Configuration](display-configuration.md)
- Reference: core/modules/media/src/MediaSourceFieldConstraintsInterface.php
