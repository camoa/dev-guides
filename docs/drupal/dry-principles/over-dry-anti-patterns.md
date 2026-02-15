---
description: Recognize and avoid over-DRY anti-patterns in Drupal - god services, premature base classes, over-configurable plugins, and forced reuse.
---

# Over-DRY Anti-Patterns

## When to Use

When deciding whether to abstract or duplicate. Over-DRY is worse than under-DRY because wrong abstractions are harder to remove than duplication.

## Common Over-DRY Mistakes in Drupal

| Anti-Pattern | What It Looks Like | Why It's Bad | Better Approach |
|--------------|-------------------|--------------|-----------------|
| **God Service** | Service with 20+ methods, handles "everything" | Violates Single Responsibility, hard to test, unclear dependencies | Split into focused services by domain |
| **Premature Base Class** | Shared base class created after 1 similar class | Wrong abstraction, inflexible, hard to change | Wait for Rule of Three, then abstract |
| **Over-Configurable Plugin** | Plugin with 30+ config options covering every use case | Complexity explosion, hard to use, hard to maintain | Create separate plugins for distinct use cases |
| **God Trait** | Trait with 15+ methods for "utilities" | Hides complexity, unclear dependencies, namespace pollution | Split into focused traits or use services |
| **Forced Reuse** | Making unrelated things fit same abstraction | Coupling unrelated code, breaks when requirements diverge | Allow duplication when domains differ |

## Pattern: God Service Anti-Pattern

```php
// WRONG: God service doing everything
class SiteHelper {

  public function formatDate($date) { }
  public function sendEmail($to, $subject, $body) { }
  public function processPayment($amount) { }
  public function generatePdf($content) { }
  public function validateAddress($address) { }
  public function geocodeLocation($address) { }
  public function calculateShipping($weight) { }
  public function applyDiscount($price, $code) { }
  // ... 20+ more methods
}

// RIGHT: Focused services by domain
class DateFormatter { public function format($date) { } }
class EmailService { public function send($to, $subject, $body) { } }
class PaymentProcessor { public function process($amount) { } }
class PdfGenerator { public function generate($content) { } }
class AddressValidator { public function validate($address) { } }
class GeocodingService { public function geocode($address) { } }
class ShippingCalculator { public function calculate($weight) { } }
class DiscountService { public function apply($price, $code) { } }
```

## Pattern: Premature Base Class

```php
// WRONG: Base class created after 1 similar class
abstract class MyProjectFormBase extends FormBase {
  // Shared code that only applies to ONE form so far
  protected function validateCustomField($value) { }
}

class MyForm extends MyProjectFormBase { }

// RIGHT: Wait until you have 3+ forms needing same code
// Keep validation in the form until duplication appears elsewhere
class MyForm extends FormBase {
  protected function validateCustomField($value) { }
}

// Later, when you have 3 forms with same validation...
abstract class MyProjectFormBase extends FormBase {
  protected function validateCustomField($value) { }
}
```

## Decision Framework: When to Abstract

| Signals to Abstract | Signals to Keep Duplicate |
|---------------------|---------------------------|
| Exact same logic in 3+ places (Rule of Three) | Similar code but different reasons (knowledge domains differ) |
| Changes to logic require updating all copies | Code looks similar but is changing independently |
| Logic represents same business rule | Logic serves different features with different stakeholders |
| High cost of bugs from inconsistency | Low coupling between instances |

## Common Mistakes

- **Abstracting at first duplication** — Wait for Rule of Three (3 instances before abstracting)
- **Making unrelated code share abstraction** — Accidental duplication (similar code, different knowledge) is acceptable
- **Creating "flexible" config to avoid creating new classes** — Results in complex, hard-to-use abstractions
- **Using inheritance when composition would work** — Favor services (composition) over base classes (inheritance)
- **Assuming all duplication is bad** — Some duplication is healthy; eliminates coupling

## See Also

- [Drush and CLI Reuse](drush-cli-reuse.md)
- [Best Practices Decision Framework](best-practices-decision-framework.md)
- Reference: [Dependency injection anti-patterns in Drupal](https://mglaman.dev/blog/dependency-injection-anti-patterns-drupal)
- Reference: `dev-dry-principles.md` section on Over-DRY Anti-Patterns
