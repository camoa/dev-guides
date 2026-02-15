---
description: Use Drupal core traits and custom traits to share cross-cutting concerns like translation, logging, and messaging across unrelated classes.
---

# Traits for Cross-Cutting Concerns

## When to Use

When you need to share functionality across classes that don't share the same inheritance hierarchy, or when you want to compose behaviors without deep inheritance.

## Core Drupal Traits

| Trait | Provides | Use When |
|-------|----------|----------|
| `StringTranslationTrait` | `$this->t()`, `$this->formatPlural()` | Any class that needs translatable strings |
| `MessengerTrait` | `$this->messenger()` | Classes that display user messages |
| `LoggerChannelTrait` | `$this->getLogger($channel)` | Classes that need logging |
| `RedirectDestinationTrait` | `$this->getRedirectDestination()` | Forms/controllers with redirect logic |
| `EntityChangedTrait` | `changed` field, `getChangedTime()` | Content entities tracking last modification |
| `EntityPublishedTrait` | `status` field, `isPublished()` | Content entities with publish/unpublish |
| `DependencySerializationTrait` | Serialization of DI properties | Services stored in serialized contexts |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Translation in non-base-class | `StringTranslationTrait` | Avoids duplicating `t()` implementations |
| Logging in plugin/service | `LoggerChannelTrait` | Consistent logger access pattern |
| Messages in custom class | `MessengerTrait` | Avoids `\Drupal::messenger()` static call |
| Multiple orthogonal behaviors | Compose multiple traits | Alternative to multiple inheritance |
| Shared logic in inheritance chain | Base class method | Traits can't access parent methods |

## Pattern

```php
namespace Drupal\mymodule;

use Drupal\Core\StringTranslation\StringTranslationTrait;
use Drupal\Core\Messenger\MessengerTrait;
use Drupal\Core\Logger\LoggerChannelTrait;

class MyService {

  use StringTranslationTrait;
  use MessengerTrait;
  use LoggerChannelTrait;

  public function processData(array $data): void {
    // Translation
    $message = $this->t('Processing @count items', ['@count' => count($data)]);

    // Logging
    $this->getLogger('mymodule')->info($message);

    // User message
    $this->messenger()->addStatus($message);
  }
}
```

Reference: `core/lib/Drupal/Core/StringTranslation/StringTranslationTrait.php`, `core/lib/Drupal/Core/Messenger/MessengerTrait.php`, `core/lib/Drupal/Core/Logger/LoggerChannelTrait.php`

## Creating Custom Traits

```php
// mymodule/src/MyValidationTrait.php
namespace Drupal\mymodule;

trait MyValidationTrait {

  protected function validateEmail(string $email): bool {
    return filter_var($email, FILTER_VALIDATE_EMAIL) !== FALSE;
  }

  protected function validateUrl(string $url): bool {
    return filter_var($url, FILTER_VALIDATE_URL) !== FALSE;
  }
}

// Use in multiple classes
class MyForm extends FormBase {
  use MyValidationTrait;

  public function validateForm(array &$form, FormStateInterface $form_state) {
    if (!$this->validateEmail($form_state->getValue('email'))) {
      $form_state->setErrorByName('email', $this->t('Invalid email'));
    }
  }
}
```

## Common Mistakes

- **Traits with state/dependencies** — Traits should be stateless or require dependencies via abstract methods; don't store config/services in trait properties
- **Overusing traits instead of services** — If the logic is complex, extract to a service and inject it; traits are for simple, composable behaviors
- **Method name conflicts** — When using multiple traits with same method names, use `as` to alias: `use TraitA, TraitB { TraitB::method as methodB; }`
- **Forgetting to inject dependencies** — `StringTranslationTrait` needs `setStringTranslation()` called if not using `FormBase`/`ControllerBase`
- **Using traits to hide God objects** — If your trait has 20+ methods, it's probably doing too much; split into focused traits or services

## See Also

- [Base Classes and Inheritance](base-classes-inheritance.md)
- [Plugin Reuse Patterns](plugin-reuse.md)
- Reference: `core/lib/Drupal/Core/Entity/EntityChangedTrait.php` (example entity trait)
- Reference: `core/lib/Drupal/Core/Form/FormBase.php` (uses multiple traits)
