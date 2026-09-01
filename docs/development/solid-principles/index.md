---
description: SOLID principles for object-oriented design — decision guides for SRP, OCP, LSP, ISP, and DIP with practical examples in PHP, TypeScript, Python, and Java.
tracks: []
guide-meta:
  concepts:
    - Single Responsibility Principle
    - Open/Closed Principle
    - Liskov Substitution Principle
    - Interface Segregation Principle
    - Dependency Inversion Principle
    - SOLID anti-patterns
    - SOLID code smells
  not:
    - Drupal-specific SOLID patterns
    - DRY principles
  requires: []
  complements:
    - development/dry-principles
    - development/tdd-spec-driven
  category: dev-practices
---

# SOLID Principles

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what SOLID means and why it matters | [SOLID Overview](solid-overview.md) | What SOLID means, why it matters, and when to learn each principle across career stages. |
| Learn when a class has too many responsibilities | [Single Responsibility Principle](single-responsibility-principle.md) | When designing classes, modules, or functions -- especially when you notice code becoming harder to test, change, or understand. |
| Refactor code toward single responsibility | [SRP in Practice](srp-in-practice.md) | Practical refactoring strategies for Single Responsibility Principle — when to split, detection patterns, and when NOT to split. |
| Make code extensible without modification | [Open/Closed Principle](open-closed-principle.md) | When building systems that need to support new features without modifying existing, tested code. Especially critical in libraries, frameworks, and plugin architectures. |
| Implement plugin systems and middleware | [OCP in Practice](ocp-in-practice.md) | Practical OCP patterns — plugin systems, middleware, data-driven configuration, and when to apply or skip OCP. |
| Understand when subtypes break substitutability | [Liskov Substitution Principle](liskov-substitution-principle.md) | When designing inheritance hierarchies, implementing interfaces, or using polymorphism. LSP ensures subtypes don't break expectations set by base types. |
| Detect and fix LSP violations | [LSP in Practice](lsp-in-practice.md) | Detecting and fixing LSP violations — contract testing, covariance/contravariance, composition over inheritance, and refactoring patterns. |
| Avoid forcing clients to depend on unused methods | [Interface Segregation Principle](interface-segregation-principle.md) | When designing interfaces, APIs, or contracts that multiple clients will implement. ISP prevents forcing clients to depend on methods they don't use. |
| Refactor fat interfaces into role interfaces | [ISP in Practice](isp-in-practice.md) | Practical ISP patterns — adapter pattern for third-party interfaces, interface inheritance, granularity decisions, and refactoring fat interfaces. |
| Depend on abstractions instead of concrete classes | [Dependency Inversion Principle](dependency-inversion-principle.md) | When designing layered architectures, building testable systems, or decoupling high-level business logic from low-level implementation details. |
| Implement dependency injection and IoC containers | [DIP in Practice](dip-in-practice.md) | Practical DIP patterns — IoC containers, constructor/setter/interface injection, Ports and Adapters architecture, and testing with DIP. |
| Apply SOLID to microservices and component architecture | [SOLID in Modern Architecture](solid-modern-architecture.md) | Applying SOLID principles to microservices, component-based frontends, API design, and event-driven architecture. |
| Know when to bend SOLID rules pragmatically | [SOLID vs Pragmatism](solid-pragmatism.md) | When to bend SOLID rules — balancing principles with YAGNI, KISS, and pragmatic decision-making based on project context. |
| Recognize common SOLID violations | [SOLID Anti-Patterns](solid-anti-patterns.md) | Common SOLID anti-patterns — God Object, Modification Cascade, Refused Bequest, Interface Bloat, Service Locator, and more. |
| Detect principle violations during code review | [SOLID Code Smells](solid-code-smells.md) | During code reviews, use these smells to detect SOLID violations early. |
| Make daily development decisions using SOLID | [Best Practices Decision Framework](best-practices-framework.md) | Daily SOLID decision framework — decision tree, apply-or-skip matrix, security and performance best practices, and anti-pattern avoidance checklist. |
| Find authoritative books and articles | [Code Reference Map](code-reference-map.md) |  |
