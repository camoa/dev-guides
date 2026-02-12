---
description: Form API core classes — interfaces, base classes, services
drupal_version: "11.x"
---

# Architecture: Core Form Classes

## When to Use

> Use this reference when choosing a form base class or understanding the core form services.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Need config management | ConfigFormBase | Built-in config operations |
| Need confirmation dialog | ConfirmFormBase | Standard confirm pattern |
| Entity create/edit | EntityForm | Entity operations |
| Custom business logic | FormBase | General purpose with DI |

## Primary Interfaces

**FormInterface** - Base form contract
- Location: `/web/core/lib/Drupal/Core/Form/FormInterface.php`
- Methods: `getFormId()`, `buildForm()`, `validateForm()`, `submitForm()`
- When to implement: Custom form without base class benefits

**FormStateInterface** - State management contract
- Location: `/web/core/lib/Drupal/Core/Form/FormStateInterface.php`
- Size: 1160+ lines defining all state operations
- Purpose: Value access, storage, control flags, error handling

**FormBuilderInterface** - Form building service contract
- Location: `/web/core/lib/Drupal/Core/Form/FormBuilderInterface.php`
- Service: `@form_builder`
- Use for: Programmatic form rendering, submission

## Base Form Classes

| Class | Purpose | Location |
|-------|---------|----------|
| FormBase | Standard forms with DI | `/web/core/lib/Drupal/Core/Form/FormBase.php` |
| ConfigFormBase | Config management | `/web/core/lib/Drupal/Core/Form/ConfigFormBase.php` |
| ConfirmFormBase | Confirmation dialogs | `/web/core/lib/Drupal/Core/Form/ConfirmFormBase.php` |

## Core Services

| Service | Purpose | File |
|---------|---------|------|
| FormBuilder | Main building engine | `/web/core/lib/Drupal/Core/Form/FormBuilder.php` |
| FormValidator | Validation orchestration | `/web/core/lib/Drupal/Core/Form/FormValidator.php` |
| FormSubmitter | Submission handling | `/web/core/lib/Drupal/Core/Form/FormSubmitter.php` |

## Common Mistakes

- **Wrong**: Not using dependency injection via `create()` method → **Right**: Inject services via static `create()` and constructor
  - WHY BAD: Breaks unit testing (can't mock services), violates SOLID principles, prevents service substitution
- **Wrong**: Extending wrong base class (ConfigFormBase for non-config forms) → **Right**: Match base class to use case
  - WHY BAD: ConfigFormBase expects config schema, requires getEditableConfigNames(), adds unnecessary overhead
- **Wrong**: Implementing FormInterface directly when base class would work → **Right**: Extend appropriate base class
  - WHY BAD: Lose helper methods (t(), messenger(), config()), must implement all interface methods manually

## See Also

- [Form Lifecycle](architecture-lifecycle.md)
- [Standard Form Pattern](pattern-standard-form.md)
- [Config Form Pattern](pattern-config-form.md)
- [Confirm Form Pattern](pattern-confirm-form.md)
- Dependency Injection Guide
- Configuration API Guide
- Reference: `/web/core/lib/Drupal/Core/Form/`
