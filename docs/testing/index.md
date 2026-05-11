---
description: Testing — decision guides for visual regression, automated testing workflows, ATK Drupal E2E testing, and test suite design.
guide-meta:
  concepts:
    - visual regression testing
    - screenshot testing
    - Playwright
    - test suite design
    - baseline management
    - automated_testing_kit
    - ATK
    - Drupal E2E testing
  not:
    - PHPUnit (see drupal/tdd)
    - Drupal-specific unit tests (see drupal/tdd)
  requires: []
  complements:
    - drupal/tdd
    - drupal/storybook
    - testing/ai-test-generation
  specializes: ""
  category: testing
---

# Testing

| I need to... | Guide |
|-------------|-------|
| Design and maintain a visual regression test suite with Playwright | [Visual Regression Workflow](visual-regression/workflow/index.md) |
| Configure Playwright for VR — setup, APIs, projects, viewports, stability | [Playwright for Visual Regression](visual-regression/playwright/index.md) |
| Understand and tune pixelmatch — algorithm, threshold, API, CLI, alternatives | [Pixelmatch](visual-regression/pixelmatch/index.md) |
| Configure, view, navigate, and share the Playwright HTML triage report | [HTML Report](visual-regression/html-report/index.md) |
| Use ATK's curated catalog of Drupal-aware E2E tests | [Automated Testing Kit (ATK)](atk/index.md) |
| Write functional E2E tests with locators, auth, fixtures, API testing, and CI sharding | [Playwright (E2E)](playwright/index.md) |
| Generate E2E tests from user stories, code, or prompts using the plan-first AI workflow | [AI Test Generation](ai-test-generation/index.md) |
