---
description: When a class has too many responsibilities and how to identify SRP violations using the "one reason to change" test.
---

# Single Responsibility Principle (SRP)

## When to Use

When designing classes, modules, or functions -- especially when you notice code becoming harder to test, change, or understand.

## Decision: What Counts as a Single Responsibility?

| If your class... | It likely has... | Refactor toward... |
|---|---|---|
| Changes for multiple business reasons (reporting AND calculation) | Multiple responsibilities | Separate classes per concern |
| Has methods unrelated to each other | Lack of cohesion | Extract groups into their own classes |
| Mixes persistence, business logic, and presentation | Layer violations | Layer separation (repository, service, controller) |
| Has "Manager", "Handler", or "Util" in the name | Vague responsibility | Specific, focused classes |

## Pattern: SRP in Action

**Violation** (PHP):
```php
class UserAccount {
  public function authenticate($username, $password) { /* auth logic */ }
  public function updateProfile($data) { /* update DB */ }
  public function sendWelcomeEmail() { /* email logic */ }
  public function generateReport() { /* PDF generation */ }
}
// Changes for auth, DB schema, email provider, report format
```

**SRP-Compliant** (PHP):
```php
class Authenticator {
  public function authenticate($username, $password) { /* auth only */ }
}
class UserRepository {
  public function update(User $user) { /* DB only */ }
}
class EmailService {
  public function sendWelcomeEmail(User $user) { /* email only */ }
}
class UserReportGenerator {
  public function generate(User $user): Report { /* reporting only */ }
}
```

**TypeScript Example**:
```typescript
// Violation: mixed concerns
class OrderProcessor {
  processOrder(order: Order) { /* business logic */ }
  saveToDatabase(order: Order) { /* persistence */ }
  sendConfirmationEmail(order: Order) { /* notification */ }
}

// SRP-Compliant: separated concerns
class OrderService {
  processOrder(order: Order): ProcessedOrder { /* business logic */ }
}
class OrderRepository {
  save(order: Order): void { /* persistence */ }
}
class NotificationService {
  sendOrderConfirmation(order: Order): void { /* notification */ }
}
```

## The "One Reason to Change" Test

A class should have **one reason to change**. If you can describe a class's purpose with "and" or "or", it has multiple responsibilities.

**Test**: "This class changes when..."
- "...the authentication method changes **and** the email provider changes" -- Multiple responsibilities
- "...the authentication method changes" -- Single responsibility

## Common Mistakes

- **"One method = one class"** -- SRP is about cohesion, not granularity. Related methods belong together
- **Creating anemic domain models** -- Business logic IS a responsibility; don't extract it if it belongs to the entity
- **Splitting too early** -- Wait until you have a real reason to change before splitting
- **Confusing SRP with "one public method"** -- Private helpers supporting one responsibility are fine
- **God objects with "Manager" suffix** -- UserManager doing auth, CRUD, reporting, notifications violates SRP. Why: impossible to test in isolation, changes ripple everywhere, unclear ownership
