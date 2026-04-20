---
description: SOLID principles in Drupal 11 development - services, plugins, entities, forms, hooks, dependency injection
guide-meta:
  concepts:
    - Drupal SOLID
    - services SRP
    - plugin system OCP
    - hooks events OCP
    - entity hierarchy LSP
    - form hierarchy LSP
    - entity interfaces ISP
    - service container DIP
    - hook classes
  not:
    - tool-agnostic SOLID theory
    - DRY principles
  requires:
    - drupal/services
  complements:
    - drupal/services
    - drupal/plugins
    - drupal/dry-principles
  specializes: development/solid-principles
  category: drupal
---

# SOLID Principles in Drupal

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand how Drupal embodies SOLID | [Overview](overview.md) | Understanding how Drupal's architecture embodies SOLID principles guides you to write code that aligns with core patterns rather than fighting them. |
| Keep services focused on single responsibilities | [Services & SRP](services-srp.md) | Every service should have one reason to change. If a service handles node access grants AND email notifications, split it. |
| Split fat controllers into services | [Controllers & SRP](controllers-srp.md) | Controllers should only handle HTTP request/response. Business logic belongs in services. |
| Organize Drupal 11 OOP hook classes | [Hook Classes & SRP](hook-classes-srp.md) | Drupal 11.1+ supports OOP hooks using class methods with `#[Hook]` attributes. Organize hook classes by domain concern, not by hook type. |
| Use plugins to extend without modification | [Plugin System & OCP](plugin-system-ocp.md) | Plugins are Drupal's primary OCP mechanism -- extend functionality without modifying existing code. Use plugins for blocks, field formatters/widgets, views plugins, etc. |
| Use hooks and events for extension | [Hooks & Events & OCP](hooks-events-ocp.md) | Hooks and event subscribers let you extend behavior without modifying existing code. Use `hook_alter()` for data modification, events for architectural extension points. |
| Override config safely | [Config Overrides & OCP](config-overrides-ocp.md) | Config overrides let you change configuration values without modifying stored config. Use for environment-specific settings (dev/staging/prod). |
| Understand entity hierarchy substitutability | [Entity Hierarchy & LSP](entity-hierarchy-lsp.md) | Drupal's entity system follows LSP -- any ContentEntityBase subclass (Node, User, Term) can be used wherever ContentEntityBase is expected. Behavioral contracts must be preserved. |
| Choose the right form base class | [Form Hierarchy & LSP](form-hierarchy-lsp.md) | Drupal form base classes follow LSP -- extend the right base for your use case. ConfigFormBase adds config-specific behavior; SettingsForm adds protected config behavior. |
| Combine access results correctly | [Access Results & LSP](access-results-lsp.md) | AccessResult follows LSP via three immutable subclasses: Allowed, Forbidden, Neutral. They can be combined with `orIf()`/`andIf()` and always produce valid AccessResultInterface. |
| Design role-based interfaces | [Entity Interfaces & ISP](entity-interfaces-isp.md) | Drupal provides role-specific entity interfaces. Implement only the interfaces your entity needs -- don't implement EntityPublishedInterface if your entity can't be published. |
| Use correct injection interfaces | [Injection Interfaces & ISP](injection-interfaces-isp.md) | Drupal provides focused interfaces for dependency injection. Use ContainerInjectionInterface for static::create() factory method, or AutowireTrait for automatic dependency resolution. |
| Depend on abstractions not implementations | [Service Container & DIP](service-container-dip.md) | The service container is Drupal's DIP foundation. Depend on abstractions (interfaces) defined in core.services.yml, not concrete implementations. |
| Inject dependencies correctly | [Dependency Injection Patterns & DIP](dependency-injection-patterns-dip.md) | Inject all dependencies through constructor. Use autowiring in Drupal 10.2+ to reduce boilerplate. |
| Avoid static service calls | [Anti-Patterns & DIP](anti-patterns-dip.md) | Recognize these patterns as violations of DIP. They create tight coupling, prevent testability, and make code fragile. |
| Structure a module following SOLID | [Module Architecture](module-architecture.md) | Structure your custom module following SOLID principles. This section shows recommended directory layout and organization patterns. |
| Review code for SOLID compliance | [Best Practices Checklist](best-practices-checklist.md) | Use this checklist during code review to verify SOLID compliance. |
| Identify SOLID violations | [Common Mistakes](common-mistakes.md) | Recognize these patterns as SOLID violations. Understanding WHY they're bad helps you avoid them and spot them in code review. |
| Find core examples of each principle | [Code Reference Map](code-reference-map.md) |  |
