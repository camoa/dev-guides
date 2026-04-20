---
description: Decision guides for Test-Driven Development and Spec-Driven Development practices
guide-meta:
  concepts:
    - TDD
    - Red-Green-Refactor
    - spec-driven development
    - test doubles
    - mocks stubs fakes spies
    - unit testing
    - integration testing
    - test coverage strategy
  not:
    - Drupal PHPUnit testing
    - framework-specific test runners
  requires: []
  complements:
    - development/solid-principles
    - development/security-practices
  specializes: ""
  category: dev-practices
---

# TDD & Spec-Driven Development

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what TDD is and why it matters | [TDD Overview](tdd-overview.md) | You're starting a new feature, fixing a bug, or working on complex business logic where you want to catch errors early and design better code through tests. |
| Know when to use TDD vs traditional testing | [TDD vs Traditional Testing](tdd-vs-traditional.md) | You're deciding whether to adopt TDD for a project or choosing testing strategy for different parts of your codebase. |
| Learn the core rules of TDD | [The Three Laws of TDD](three-laws-tdd.md) | You're practicing strict TDD and need the precise discipline to maintain test-first workflow. |
| Follow the TDD workflow step-by-step | [Red-Green-Refactor Workflow](red-green-refactor.md) | Every time you implement a new feature or fix a bug using TDD. This is the core TDD workflow. |
| Write effective unit tests | [Unit Testing Fundamentals](unit-testing-fundamentals.md) | Writing any unit test, whether in TDD workflow or traditional testing approach. These principles define what makes a good unit test. |
| Use mocks, stubs, fakes, and spies correctly | [Test Doubles](test-doubles.md) | You need to test code that depends on external systems (databases, APIs, file systems) or collaborating objects that are slow, unavailable, or difficult to set up in tests. |
| Structure my tests properly | [Testing Patterns](testing-patterns.md) | Structuring any test - unit, integration, or end-to-end. These patterns create readable, maintainable tests. |
| Understand spec-driven development | [Spec-Driven Development Overview](spec-driven-overview.md) | You're using AI coding assistants and want to maintain control over architecture while leveraging AI for implementation. Essential for production-quality code generation with tools like Claude Code, GitHub Copilot, Cursor, or Amazon Kiro. |
| Write specifications that drive implementation | [Writing Effective Specifications](writing-specs.md) | Before implementing any feature using AI code generation or when you want specifications to serve as living documentation and development contract. |
| Use AI to generate code from specs | [From Spec to Implementation](spec-to-implementation.md) | You have a detailed specification and are ready to generate or write code using AI assistance, or you're manually implementing code that must match a specification. |
| Plan integration testing strategy | [Integration Testing Strategy](integration-testing.md) | Your unit tests verify individual components work correctly, and now you need to verify they work together correctly. Essential for multi-component systems, APIs, databases, and microservices. |
| Set meaningful coverage goals | [Test Coverage Strategy](test-coverage.md) | You're deciding what to test, how much to test, and evaluating whether your test suite is adequate. Coverage metrics are tools for finding gaps, not goals to hit. |
| Refactor safely with test coverage | [Refactoring with Confidence](refactoring-confidence.md) | Code works but is messy, duplicated, or hard to understand. You want to improve structure without breaking behavior. |
| Avoid common TDD mistakes | [TDD Anti-Patterns](anti-patterns.md) | You're practicing TDD or reviewing tests and want to identify common mistakes that reduce test value or create maintenance burden. |
| Apply TDD security best practices | [Security Best Practices](security-best-practices.md) | Writing tests for any code that handles authentication, authorization, user input, sensitive data, or external integrations. Security must be tested, not assumed. |
| Optimize test performance | [Performance Best Practices](performance-best-practices.md) | Writing performance-critical code, optimizing slow tests, or ensuring your test suite runs fast enough to be run frequently. |
| Follow development standards | [Development Standards](development-standards.md) | Every development project using TDD or testing. These standards ensure code quality, maintainability, and team consistency. |
| Find testing resources by language | [Code Reference Map](code-reference-map.md) |  |
