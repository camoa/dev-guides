---
description: "Choose the right test layer — E2E, VR, unit, or Drupal FunctionalJavascript — for the question you're actually answering."
tldr: "Default to Playwright web-first E2E for any test whose acceptance criterion includes \"the user sees\" or \"the user clicks.\" Keep VR and E2E in separate test files — VR demands frozen animations and network idle; mixing the two produces tests that are both over-sensitive and under-sensitive."
---

# Layer Selection

## When to Use

> Picking the right test layer for the question you're actually trying to answer.

## Decision

| Question being asked | Layer | Tool |
|---|---|---|
| "Does this pure function/class produce the right output?" | Unit | Vitest (preferred) or Jest for JS; PHPUnit `Unit` for PHP |
| "Do these N modules wire together in-process?" | Integration | Vitest + MSW; PHPUnit `Kernel` |
| "Does this rendered component look the same as last week?" | Visual regression | Playwright `expect(page).toHaveScreenshot()` — see VR guide |
| "Does the user journey through real Drupal/JS/network actually work?" | **E2E (functional)** | **Playwright with web-first assertions — this guide** |
| "Does the JS-on-the-page work against a fully-bootstrapped Drupal kernel?" | Drupal FunctionalJavascript | PHPUnit `FunctionalJavascript` (Mink + ChromeDriver) |
| "Does the HTTP route return the right JSON?" | API | Playwright `request` fixture **or** Pest/PHPUnit |

## Practical Rules

- **Default to Playwright web-first E2E** for any test whose acceptance criterion includes "the user sees" or "the user clicks"
- **Prefer Playwright over Drupal FunctionalJavascript** for user-visible behavior tests; FunctionalJavascript stays appropriate when you need `\Drupal::state()` / service container assertions during the test, or for contrib modules destined for drupal.org CI
- **Keep VR and E2E in separate test files / projects** — VR demands frozen animations, fonts loaded, network idle; E2E only demands the action completed. Mixing produces tests that are simultaneously over-sensitive (VR diffs) and under-sensitive (missed behavior)
- **Unit tests are not optional** even when Playwright is "easy" — booting Chromium to test a regex is 100–1000× more expensive than Vitest

## Common Mistakes

- **Using Playwright as a unit-test runner** — booting Chromium for a function is two orders of magnitude too expensive
- **Converting all PHPUnit Functional tests to Playwright** — Drupal contrib modules need PHPUnit coverage; Playwright supplements, doesn't replace
- **Single mega-suite with VR + E2E mixed** — different stability requirements, different failure modes

## See Also

- [Playwright for Visual Regression](../visual-regression/playwright/index.md) — when the question is visual sameness
- [Automated Testing Kit (ATK)](../atk/index.md) — Drupal-specific E2E test catalog
- Reference: [Playwright Best Practices](https://playwright.dev/docs/best-practices)
