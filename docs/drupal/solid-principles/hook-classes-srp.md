---
description: Organize Drupal 11 OOP hook classes by domain concern, not by hook type
drupal_version: "11.x"
---

# Hook Classes - Single Responsibility (Drupal 11+)

## When to Use

Drupal 11.1+ supports OOP hooks using class methods with `#[Hook]` attributes. Organize hook classes by domain concern, not by hook type.

## Decision

| Organize by... | Pattern | Example |
|---|---|---|
| Domain/feature area | `NodeEntityHooks`, `NodeFormHooks`, `NodeBlockHooks` | Focused, logical grouping |
| Hook type | Do not use `AlterHooks`, `LoadHooks` | Mixes unrelated domains |
| Module function | Do not use one class with all hooks | Violates SRP |

## Pattern

**GOOD: Domain-organized hook classes (SRP)**

```php
// src/Hook/NodeEntityHooks.php - only node entity hooks
namespace Drupal\node\Hook;

class NodeEntityHooks {
  #[Hook('entity_view_display_alter')]
  public function entityViewDisplayAlter(EntityViewDisplayInterface $display, $context): void {
    if ($context['entity_type'] == 'node') {
      // Node display logic only
    }
  }

  #[Hook('entity_extra_field_info')]
  public function entityExtraFieldInfo(): array {
    // Node extra fields only
  }
}

// src/Hook/NodeFormHooks.php - only node form hooks
class NodeFormHooks {
  #[Hook('form_alter')]
  public function formAlter(&$form, FormStateInterface $form_state, $form_id): void {
    // Node form alterations only
  }
}
```

**BAD: Mixed concerns (violates SRP)**

```php
// All hooks in one class
class MyModuleHooks {
  #[Hook('entity_view_display_alter')]
  public function entityViewDisplayAlter() { }  // Entity concern

  #[Hook('mail_alter')]
  public function mailAlter() { }               // Email concern

  #[Hook('cron')]
  public function cron() { }                    // Batch concern
}
```

Reference: `/core/modules/node/src/Hook/` -- domain-organized hook classes (NodeEntityHooks, NodeFormHooks, NodeBlockHooks, etc.)

## Common Mistakes

- All hooks in one `Hooks.php` class -- split by domain (EntityHooks, FormHooks, BlockHooks). **WHY:** 50 hooks in one class is unmaintainable; changes to form logic risk breaking entity logic
- Hook class with injected services for unrelated features -- split classes, each with its own dependencies. **WHY:** Injecting 10 services into one class indicates mixed responsibilities
- Mixing procedural `.module` hooks and OOP hooks inconsistently -- prefer OOP for new code. **WHY:** Procedural hooks always load; OOP hooks use PSR-4 autoloading (performance)
- Hook class doing business logic directly -- delegate to services. **WHY:** Can't reuse hook logic outside hook context; can't unit test without invoking hooks

## See Also

- [Services & SRP](services-srp.md) for service delegation
- Reference: [Drupal 11.1 Hooks as Classes](https://drupalize.me/blog/drupal-111-adds-hooks-classes-history-how-and-tutorials-weve-updated)
- Reference: [Drupal 11 OOP Hooks Architecture](https://www.hashbangcode.com/article/drupal-11-object-oriented-hooks-and-hook-service-classes)
