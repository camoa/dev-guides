---
description: "Master decision matrix — map any verification need to the right test type and the right guide, with quick-reference by stack."
tldr: "Map what you need to verify to the correct test type using this matrix. Most features need a combination: unit tests for logic, integration for seams, E2E for critical journeys only. Quick reference: Drupal uses PHPUnit Unit/Kernel/Functional; React/Next.js uses Vitest + RTL + Playwright."
---

# Choosing a Test Type

## When to Use

> When you know what you need to verify but are not sure which test type to reach for. This is the master decision matrix — map a need to the right test type(s) and the right guide.

## Master Decision Matrix

| I need to verify... | Primary test type | Secondary / complement | Cross-link |
|---|---|---|---|
| A function's return value for given inputs | Unit | Parameterized unit for edge cases | [Unit Testing Concepts](unit-testing-concepts.md) |
| A class behaves correctly when dependencies return specific values | Unit (with stubs) | — | [Test Doubles](test-doubles.md) |
| A service correctly queries and transforms database data | Integration (real test DB) | Unit for transformation logic | [Integration Testing Concepts](integration-testing-concepts.md) |
| An HTTP endpoint returns the correct response shape | Integration (HTTP layer) | Unit for business logic inside | [Integration Testing Concepts](integration-testing-concepts.md) |
| A multi-step workflow end-to-end within one process | Functional / system | Integration for individual seams | [Functional Testing Concepts](functional-testing-concepts.md) |
| A critical user journey through a real browser | E2E | Integration for logic; unit for components | [E2E Testing Concepts](e2e-testing-concepts.md) |
| A UI component renders correctly without regression | Visual regression | Unit/Integration for behavior | [Visual Regression Concepts](visual-regression-concepts.md) |
| An API consumer and provider stay in sync | Contract test | Integration for each side independently | [Contract & API Testing Concepts](contract-api-testing-concepts.md) |
| System behavior under concurrent users / load | Load/performance test | Unit for algorithmic bottlenecks | [Performance Testing Concepts](performance-testing-concepts.md) |
| A page has no WCAG violations | Automated a11y (axe) | Manual keyboard + screen reader | [Accessibility Testing Concepts](accessibility-testing-concepts.md) |
| A React/Next.js component's interactive behavior | Integration (Testing Library) | Unit for pure logic | [Integration Testing Concepts](integration-testing-concepts.md) |
| Drupal form submission, validation, redirects | Drupal Functional (BrowserTestBase) | Kernel for service logic | [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) |
| Drupal plugin / hook / service behavior | Drupal Kernel (KernelTestBase) | Unit for pure logic | [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) |
| Drupal E2E with Playwright against a DDEV site | Playwright + ATK | VR for visual stability | [testing/playwright](https://camoa.github.io/dev-guides/testing/playwright/), [testing/atk](https://camoa.github.io/dev-guides/testing/atk/) |
| AI-generated tests match spec and cover edge cases | AI test generation workflow | Unit + integration for gap coverage | [testing/ai-test-generation](https://camoa.github.io/dev-guides/testing/ai-test-generation/) |

## Test type is not test discipline

The matrix above picks a *type*. It does not say which **loop** the test belongs to, and mixing the two is how a suite ends up with a healthy count and unspecified behavior.

A test written before the code and watched to fail is a **specification**, produced by the TDD loop: unit, integration, contract, property-based, and a framework's in-process functional or browser tier all qualify. A test that can only be written against a system that already stands is **outer verification**: browser E2E, visual regression, load and performance, accessibility and security scans, mutation testing, fuzzing. Both are necessary. Only the first can drive a design decision, and only the first should be counted as TDD coverage.

The discriminator is not whether a browser is involved. Drupal's `BrowserTestBase` and `WebDriverTestBase` tiers drive real requests and a real browser, and are written red-green before the code — they are inside the loop. A Playwright journey against a running site is not, however similar it looks.

See [TDD — What TDD Covers](https://camoa.github.io/dev-guides/development/tdd-spec-driven/what-tdd-covers/) for the full table, and [TDD — When Not to Write a Test](https://camoa.github.io/dev-guides/development/tdd-spec-driven/when-not-to-write-a-test/) for what the loop requires from a change and what counts as excess.

## When One Test Type Is Not Enough

Most features need a combination. Use the pyramid/trophy shape as a guide:

```
Feature: User Registration

Unit tests:
  - Email format validation logic
  - Password strength rules
  - Hash function produces correct output format

Integration tests:
  - Registration endpoint: saves user to DB, returns 201
  - Duplicate email: returns 409 with correct error body
  - Weak password: returns 400 with validation errors

Functional tests:
  - Full registration form submission through Drupal
  - Email confirmation flow

E2E test:
  - One test: user fills form, submits, sees confirmation page

Security tests (at integration level):
  - SQL injection payload returns 400, not 500
  - Token in response is signed and contains correct claims
```

## Quick Reference by Stack

| Stack | Unit | Integration | E2E |
|---|---|---|---|
| PHP/Drupal | PHPUnit Unit | PHPUnit Kernel | PHPUnit Functional (in the TDD loop) / Playwright (outer) |
| JavaScript/React | Vitest/Jest | React Testing Library | Playwright |
| TypeScript/Next.js | Vitest/Jest | Supertest + Testing Library | Playwright |
| Python | pytest | pytest with real DB | Playwright / Selenium |
| Go | `testing` package | `httptest` + real DB | Playwright |

## See Also

- ← Previous: [Best Practices and Anti-Patterns](best-practices-and-anti-patterns.md)
- Related: [development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) — TDD workflow that uses these test types
- Related: [TDD — What TDD Covers](https://camoa.github.io/dev-guides/development/tdd-spec-driven/what-tdd-covers/) — which of these types the red-green loop actually produces
- Related: [drupal/testing](https://camoa.github.io/dev-guides/drupal/testing/) — Drupal-specific test types and setup
