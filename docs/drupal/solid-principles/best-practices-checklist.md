---
description: Code review checklist for SOLID compliance in Drupal modules
drupal_version: "11.x"
---

# SOLID Best Practices Checklist

## When to Use

Use this checklist during code review to verify SOLID compliance.

## Checklist

**Single Responsibility Principle**

- [ ] Each service has one clear responsibility
- [ ] Controllers are thin (< 50 lines), delegate to services
- [ ] Forms only handle structure/validation, delegate processing to services
- [ ] Hook classes organized by domain (EntityHooks, FormHooks), not all in one
- [ ] No "Manager" or "Helper" services doing 10 unrelated things

**Open/Closed Principle**

- [ ] Using plugins to extend systems (blocks, fields, views)
- [ ] Using hooks/events to extend behavior, not modifying core
- [ ] Config overrides in settings.php, not editing config files
- [ ] Service decorators for extending existing services
- [ ] No patches to core unless absolutely necessary (and documented)

**Liskov Substitution Principle**

- [ ] Custom entities extend correct base (ContentEntityBase vs ConfigEntityBase)
- [ ] Forms extend correct base (FormBase vs ConfigFormBase vs SettingsForm)
- [ ] Calling parent methods in overrides (parent::submitForm())
- [ ] Access hooks return AccessResult, not boolean
- [ ] Not breaking behavioral contracts (e.g., save() must persist)

**Interface Segregation Principle**

- [ ] Entities implement only needed interfaces (EntityOwnerInterface if has owner)
- [ ] Not implementing interfaces with fake/stub methods
- [ ] Using focused injection interfaces (ContainerInjectionInterface, not fat interface)
- [ ] Role-specific interfaces, not one giant interface
- [ ] Using traits when implementing interfaces (EntityOwnerTrait)

**Dependency Inversion Principle**

- [ ] All dependencies constructor-injected, no `\Drupal::service()` in classes
- [ ] Type-hinting interfaces, not concrete classes
- [ ] Services defined in *.services.yml with `autowire: true`
- [ ] Service aliases for interfaces (Interface: '@service_id')
- [ ] No `new ClassName()` in business logic (use factories or injection)
- [ ] No global variables ($user), use injected services

**Security Best Practices**

- [ ] Access results include cache contexts (cachePerUser, cachePerPermissions)
- [ ] Using entity API, not direct database queries (access control built in)
- [ ] Input validation in forms, not just in services
- [ ] Not trusting user input (use $form_state->getValue(), validate/sanitize)
- [ ] Checking access in controllers (access callbacks in routing.yml)

**Performance Best Practices**

- [ ] Using OOP hooks (PSR-4 autoload) instead of procedural (always load)
- [ ] Autowiring services (reduces boilerplate)
- [ ] Caching expensive operations (entity queries, API calls)
- [ ] Lazy-loading services (`lazy: true` in services.yml for expensive services)
- [ ] Not doing heavy processing in hooks that run on every request

**Testability**

- [ ] Unit tests for services (mocked dependencies)
- [ ] Kernel tests for entity/form behavior
- [ ] All business logic in services, not controllers (easier to test)
- [ ] No static calls (mockable dependencies only)

## See Also

- [Common Mistakes](common-mistakes.md) for anti-patterns
