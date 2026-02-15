---
description: What SOLID means, why it matters, and when to learn each principle across career stages.
---

# SOLID Overview

## What SOLID Means

SOLID is an acronym representing five foundational principles in object-oriented programming:

- **S**ingle Responsibility Principle (SRP)
- **O**pen/Closed Principle (OCP)
- **L**iskov Substitution Principle (LSP)
- **I**nterface Segregation Principle (ISP)
- **D**ependency Inversion Principle (DIP)

These principles were popularized by Robert C. "Uncle Bob" Martin in the early 2000s, drawing from work by Barbara Liskov, Bertrand Meyer, and others. They form the foundation of Martin's "Clean Architecture" and "Clean Code" philosophies.

## Why SOLID Matters

According to the JetBrains Developer Ecosystem Survey 2024, over 65% of high-performing teams attribute maintainable code to adherence to foundational design principles like SOLID. The principles address core software engineering challenges:

| Without SOLID | With SOLID |
|---|---|
| Classes grow into "god objects" doing everything | Each class has one clear purpose |
| Changes ripple across unrelated code | Changes are localized and controlled |
| Subtypes break when replacing base types | Subtypes work seamlessly as replacements |
| Interfaces force clients to implement unused methods | Clients depend only on what they use |
| High-level code depends on low-level details | Both depend on stable abstractions |

## When to Learn SOLID

**Early career**: Learn the principles conceptually. Recognize violations in code reviews.
**Mid-level**: Apply principles during refactoring. Use them to guide design decisions.
**Senior**: Balance principles with pragmatism. Know when to bend the rules and why.

## SOLID as a Framework, Not Rules

These are **principles**, not laws. They represent trade-offs between coupling vs reuse, simplicity vs flexibility, abstraction vs clarity. Use them to make better decisions under pressure, not as dogma.

## Common Mistakes

- **Applying SOLID to everything** -- Start with single principles on new code, not wholesale rewrites
- **Treating SOLID as binary** -- Principles exist on a spectrum; partial compliance is progress
- **Ignoring the "why"** -- Understanding the reasoning matters more than memorizing definitions
- **SOLID without context** -- Consider project size, team experience, timeline constraints
- **Over-engineering simple code** -- SOLID adds value in complex domains; don't force it on simple scripts
