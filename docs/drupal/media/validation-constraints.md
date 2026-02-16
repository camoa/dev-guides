---
description: Validating source field values before saving media entities (URL patterns, API connectivity, file types).
---

# Validation Constraints

### When to Use

Validating source field values before saving media entities (URL patterns, API connectivity, file types).

### Decision

| Validation Type | Constraint Approach | Example |
|----------------|---------------------|---------|
| URL pattern validation | Custom regex constraint | Instagram shortcode format |
| API connectivity check | Custom constraint with HTTP call | Verify resource exists at API |
| File type validation | Built-in file extension constraint | Already handled by File source |
| Value uniqueness | Unique field constraint | Prevent duplicate media items |

### Pattern

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

### Common Mistakes

- Not implementing `MediaSourceFieldConstraintsInterface` → Constraint never applied
- Expensive validation (API calls) → Slows form saves, times out
- Not handling empty values → Validation error on optional fields
- Weak regex patterns → Security risk, allows malicious URLs
- No user feedback → Validation fails silently, confusing editors

**WHY:**
- **Interface required**: Drupal only applies constraints from plugins implementing this interface; missing it means validation skipped
- **Performance matters**: Validation runs on every form submission; expensive checks (API calls) should be queued or cached
- **Empty value handling**: Constraint validators receive empty values for optional fields; must check and skip validation
- **Security-critical regex**: URL validation prevents injection attacks; weak patterns allow attackers to submit malicious URLs

### See Also

- Previous: [Dependency Injection](index.md)
- Next: [Display Configuration](index.md)
- Reference: core/modules/media/src/MediaSourceFieldConstraintsInterface.php