---
description: Field validation with custom constraints and business rules
drupal_version: "11.x"
---

# Field Validation Patterns

## When to Use

When enforcing data integrity constraints on field values, requiring validation beyond basic required/max_length checks, ensuring data quality and business rule compliance.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Simple constraints | Built-in constraints (NotNull, Length, Range) | Symfony validation, well-tested |
| Custom validation | Custom constraint plugin | Reusable validation logic |
| Field-level validation | Constraint in propertyDefinitions() | Applied automatically on save |
| Cross-field validation | Entity validation constraints | Validate multiple fields together |
| Widget-specific validation | #element_validate | UI-specific validation feedback |

## Pattern

Custom validation constraint:

```php
// src/Plugin/Validation/Constraint/ValidEmailDomainConstraint.php
namespace Drupal\my_module\Plugin\Validation\Constraint;

use Symfony\Component\Validator\Constraint;

/**
 * @Constraint(
 *   id = "ValidEmailDomain",
 *   label = @Translation("Valid email domain", context = "Validation"),
 * )
 */
class ValidEmailDomainConstraint extends Constraint {
  public $message = 'The email domain @domain is not allowed.';
  public $allowedDomains = [];
}
```

Constraint validator:

```php
// src/Plugin/Validation/Constraint/ValidEmailDomainConstraintValidator.php
namespace Drupal\my_module\Plugin\Validation\Constraint;

use Symfony\Component\Validator\Constraint;
use Symfony\Component\Validator\ConstraintValidator;

class ValidEmailDomainConstraintValidator extends ConstraintValidator {

  public function validate($value, Constraint $constraint) {
    if (!isset($value)) {
      return;
    }

    $email = $value->value;
    $domain = substr(strrchr($email, "@"), 1);

    if (!in_array($domain, $constraint->allowedDomains)) {
      $this->context->addViolation($constraint->message, [
        '@domain' => $domain,
      ]);
    }
  }
}
```

Apply constraint to field:

```php
public static function propertyDefinitions(FieldStorageDefinitionInterface $def) {
  $properties['value'] = DataDefinition::create('email')
    ->setLabel(t('Email'))
    ->setRequired(TRUE)
    ->addConstraint('ValidEmailDomain', [
      'allowedDomains' => ['example.com', 'example.org'],
    ]);

  return $properties;
}
```

Built-in constraints:

```php
$properties['value'] = DataDefinition::create('string')
  ->addConstraint('Length', ['max' => 255])
  ->addConstraint('Regex', ['pattern' => '/^[A-Z0-9-]+$/']);

$properties['age'] = DataDefinition::create('integer')
  ->addConstraint('Range', ['min' => 0, 'max' => 150]);
```

Reference: `/core/lib/Drupal/Core/Validation/Plugin/Validation/Constraint/`

## Common Mistakes

- **Wrong**: Validating in widgets instead of constraints → **Right**: Validation bypassed via API, imports, migrations
- **Wrong**: Not extending ConstraintValidator → **Right**: Validator won't be discovered
- **Wrong**: Missing @Constraint annotation → **Right**: Constraint not registered
- **Wrong**: Hardcoding error messages → **Right**: Use translatable strings with placeholders
- **Wrong**: Validating on display, not storage → **Right**: Users see errors after save; validate on input
- **Wrong**: Not handling NULL values → **Right**: Check isset() before validation logic

**Security**:
- ALWAYS validate untrusted input with constraints, not widget validation
- Widget validation is UI-only. API calls bypass widgets.
- Use whitelist validation (allowed values) not blacklist when possible
- Sanitize constraint violation messages (use placeholders, not concatenation)

**Development Standards**:
- Place constraints in src/Plugin/Validation/Constraint/
- Use Symfony validation where possible (well-tested, standard)
- Document constraint parameters in class property doc blocks
- Inject dependencies via create() method in validators
- Return early from validate() if value is NULL/empty (unless checking required)

**Common Built-in Constraints**:
- NotNull, NotBlank: Required checks
- Length: String length validation
- Range: Numeric range validation
- Regex: Pattern matching
- Email: RFC email validation
- Url: URL validation
- Count: Array/collection size validation

## See Also

- [Entity Query Performance](entity-query-performance.md)
- Reference: [Validation API](https://www.drupal.org/docs/drupal-apis/entity-api/entity-validation-api)
