---
description: DRY (Don't Repeat Yourself), code reuse, and abstraction strategies - when to abstract, when to duplicate, and how to avoid premature abstraction
tracks: []
guide-meta:
  concepts:
    - DRY principle
    - WET principle
    - AHA principle
    - Rule of Three
    - knowledge duplication
    - code duplication
    - abstraction strategies
    - over-DRY anti-patterns
  not:
    - Drupal-specific DRY patterns
    - SOLID principles
  requires: []
  complements:
    - development/solid-principles
    - development/tdd-spec-driven
  category: dev-practices
---

# DRY and Code Reuse Principles

Tool-agnostic, language-agnostic development principles for understanding DRY, code reuse, and abstraction strategies.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what DRY actually means | [DRY Overview](dry-overview.md) | When making architectural decisions about code organization, abstraction, and knowledge representation across your entire software system. |
| Know when duplication is acceptable | [Four Types of Duplication](four-types-of-duplication.md) | When analyzing whether duplication in your codebase is problematic and deciding how to address it. |
| Choose between DRY, WET, or AHA approaches | [DRY vs WET vs AHA](dry-vs-wet-vs-aha.md) | When deciding whether to abstract duplicated code or let it remain duplicated, especially early in a feature's lifecycle. |
| Identify code duplication in my project | [Code Duplication](code-duplication.md) | When identifying and deciding how to address duplicated code blocks in your codebase. |
| Ensure single source of truth for business rules | [Knowledge Duplication](knowledge-duplication.md) | When ensuring business rules, validation logic, data schemas, and domain knowledge exist in only one authoritative place. |
| Learn abstraction strategies | [Abstraction Strategies](abstraction-strategies.md) | When deciding how to eliminate duplication through abstraction — choosing the right abstraction mechanism for the situation. |
| Know when it's safe to abstract | [Rule of Three](rule-of-three.md) | When deciding whether it's time to refactor duplicated code into an abstraction. |
| Apply DRY to configuration | [DRY in Configuration](dry-in-configuration.md) | When managing application configuration, environment variables, feature flags, and settings across environments. |
| Apply DRY to documentation | [DRY in Documentation](dry-in-documentation.md) | When writing and maintaining technical documentation, API docs, code comments, and system documentation. |
| Apply DRY to tests | [DRY in Testing](dry-in-testing.md) | When writing test suites and encountering repeated setup, teardown, or assertion patterns across tests. |
| Apply DRY across system boundaries | [DRY Across Boundaries](dry-across-boundaries.md) | When dealing with knowledge duplication across system boundaries: microservices, frontend/backend, multiple programming languages, or separate repositories. |
| Avoid over-abstraction | [Over-DRY Anti-Patterns](over-dry-anti-patterns.md) | When evaluating whether an abstraction is helping or hurting, and when to choose duplication over the wrong abstraction. |
| Get a practical decision framework | [Best Practices Decision Framework](best-practices-decision-framework.md) | When making architectural decisions about abstraction, duplication, and code organization. |
| Detect duplication in my codebase | [Code Smells and Detection](code-smells-detection.md) | When reviewing code, performing maintenance, or evaluating technical debt related to duplication. |
| Find authoritative sources | [Code Reference Map](code-reference-map.md) |  |
