---
description: Authoritative books, articles, tools, and specifications for DRY principles and code reuse
---

# Code Reference Map

## Key Books

- **"The Pragmatic Programmer: Your Journey to Mastery" (2019 Edition)** by Andrew Hunt & Dave Thomas
  Original source of DRY principle; covers knowledge duplication, types of duplication, and practical applications.

- **"Refactoring: Improving the Design of Existing Code" (2nd Edition)** by Martin Fowler
  Rule of Three, refactoring techniques, code smells related to duplication.

- **"99 Bottles of OOP" (2nd Edition)** by Sandi Metz
  Deep dive on when to abstract, wrong abstractions, and the cost of duplication vs abstraction.

## Foundational Articles

- **Sandi Metz - "The Wrong Abstraction"** (2016)
  https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
  "Duplication is far cheaper than the wrong abstraction."

- **Kent C. Dodds - "AHA Programming"** (2020)
  https://kentcdodds.com/blog/aha-programming
  Avoid Hasty Abstractions; balance between DRY and WET.

- **Dan Abramov - "Goodbye, Clean Code"** (2020)
  https://overreacted.io/goodbye-clean-code/
  Critique of dogmatic "clean code" and premature abstraction.

- **Dan Abramov - "The WET Codebase"** (2019)
  https://overreacted.io/the-wet-codebase/
  When to Write Everything Twice instead of abstracting.

## Modern Perspectives (2024-2026)

- **"Duplication Is Not the Enemy"** (Terrible Software, 2025)
  https://terriblesoftware.org/2025/05/28/duplication-is-not-the-enemy/
  Modern take on balancing DRY with pragmatism.

- **"Premature Abstraction in Software Engineering"** (Codeling, 2024)
  https://codeling.dev/blog/premature-abstraction-in-software-engineering/
  Consequences of abstracting too early.

- **"The Cost of Wrong Abstractions"** (Alex Kondov, 2023)
  https://alexkondov.com/the-cost-of-wrong-abstractions/
  Practical examples of abstraction failures.

## Tools and Detection

- **jscpd** -- Copy/paste detector for 150+ languages
  https://github.com/kucherenko/jscpd

- **PMD CPD** -- Copy-Paste Detector for 31+ languages
  https://pmd.github.io/pmd/pmd_userdocs_cpd.html

- **SonarQube** -- Code quality platform with duplication tracking
  https://www.sonarqube.org/

## Standards and Specifications

- **Single Source of Truth (SSOT)** -- Wikipedia
  https://en.wikipedia.org/wiki/Single_source_of_truth

- **DRY Principle** -- Wikipedia
  https://en.wikipedia.org/wiki/Don't_repeat_yourself

- **Rule of Three (Software)** -- Wikipedia
  https://en.wikipedia.org/wiki/Rule_of_three_(computer_programming)

## Schema and Code Generation

- **Protocol Buffers** -- Language-neutral schema
  https://protobuf.dev/

- **OpenAPI Generator** -- Generate clients/servers from OpenAPI specs
  https://openapi-generator.tech/

- **Zod** -- TypeScript-first schema validation
  https://zod.dev/

- **JSON Schema** -- Vocabulary for JSON validation
  https://json-schema.org/

## Configuration Management

- **PKL Configuration Language** (Apple, 2024)
  https://pkl-lang.org/

- **Formae + PKL Infrastructure Automation** (2025)
  https://dzone.com/articles/formae-pkl-infrastructure-automation

## Testing Resources

- **Pytest Fixtures Documentation**
  https://docs.pytest.org/en/stable/how-to/fixtures.html

- **Test Automation Frameworks (2026)**
  https://testrigor.com/blog/test-automation-frameworks/

## Community Discussions

- **Hacker News: "The Wrong Abstraction" Discussion** (2020)
  https://news.ycombinator.com/item?id=23739596

- **Hacker News: "Prefer Duplication Over Wrong Abstraction"** (2016)
  https://news.ycombinator.com/item?id=12061453
