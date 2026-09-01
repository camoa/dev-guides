---
description: Playwright for E2E Testing — decision guides for locators, web-first assertions, fixtures, auth, network mocking, API testing, CI sharding, and Drupal-specific patterns.
tracks:
  - project: playwright
    registry: npm
    channel: stable
    declared: null
    note: no version stated in prose
    verified: 2026-05-08
guide-meta:
  concepts:
    - playwright
    - E2E testing
    - end-to-end testing
    - locators
    - getByRole
    - getByLabel
    - getByTestId
    - web-first assertions
    - toBeVisible
    - toContainText
    - toHaveText
    - expect.poll
    - toPass
    - fixtures
    - test.extend
    - storageState
    - authentication
    - page.route
    - network mocking
    - HAR replay
    - request fixture
    - API testing
    - test.describe
    - test.step
    - sharding
    - blob reporter
    - trace viewer
    - UI Mode
    - PWDEBUG
    - page.pause
    - codegen
    - Drupal E2E
    - DDEV playwright
    - Big Pipe
    - AJAX wait
    - waitForResponse
    - ATK integration
    - data-qa-id
    - Testor
  not:
    - toHaveScreenshot (see testing/visual-regression/playwright)
    - visual regression (see testing/visual-regression/playwright)
    - baseline files (see testing/visual-regression/playwright)
    - pixelmatch (see testing/visual-regression/pixelmatch)
    - ATK full catalog (see testing/atk)
  requires:
    - testing/visual-regression/playwright
  complements:
    - testing/visual-regression/playwright
    - testing/visual-regression/workflow
    - testing/atk
    - testing/visual-regression/html-report
  category: testing
---

# Playwright (E2E)

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Choose between E2E, VR, unit tests, and Drupal FunctionalJavascript | [Layer Selection](pw-e2e-layer-selection.md) | Default to Playwright web-first E2E for any test whose acceptance criterion includes "the user sees" or "the user clicks." Keep VR and E2E in separate test files — VR demands frozen animations and network idle; mixing the two produces tests that are both over-sensitive and under-sensitive. |
| Pick the right locator (role, text, test-id, CSS) | [Locators](pw-e2e-locators.md) | Use getByRole() first, then getByLabel() for form fields, then getByTestId() for explicit test contracts — the priority order doubles as a soft a11y check. Avoid CSS class chains; they break on every theme refactor. Locators are lazy and compose — chain and filter instead of reaching for .first(). |
| Use every web-first assertion correctly | [Web-First Assertions](pw-e2e-assertions.md) | Always use expect(locator) — not isVisible() or textContent() — because only expect() auto-retries until the condition holds or expect.timeout elapses. Never use waitForTimeout(); replace with a web-first assertion or expect.poll() for conditions outside the DOM. |
| Build custom fixtures with `test.extend` | [Fixtures](pw-e2e-fixtures.md) | Replace beforeEach with test.extend fixtures — they're typed, compose across files, and scope setup to only the tests that need it. Use worker scope for expensive shared resources (OAuth token, DB pool); use test scope (default) for anything tests must not share. |
| Set up auth flows with storageState | [Authentication](pw-e2e-authentication.md) | Run a one-time setup project that logs in via API, saves storageState to a .auth/ file, then configure test projects to read that file via dependencies. Never commit .auth/ files — they contain live session cookies. Prefer programmatic API login over UI login for speed and stability. |
| Mock network calls with `page.route` | [Network Mocking](pw-e2e-network-mocking.md) | Use page.route() with fulfill to return canned responses for third-party dependencies and error states; use abort to silence analytics. Never mock the endpoint that is the subject of the test. Always await route handler setup before the action that triggers the request. |
| Test APIs or set up state via API + verify via UI | [API Testing](pw-e2e-api-testing.md) | The request fixture shares the browser context's cookie jar — use it to log in via API then drive UI as an authenticated user. The killer pattern: create state via JSON:API (fast), drive UI for the feature under test, verify via API (authoritative). |
| Organize tests with describe/hooks/tags/parallelism | [Test Organization](pw-e2e-test-organization.md) | Use fullyParallel:true globally and reserve test.describe.serial only for genuine multi-step wizards where each step depends on the previous. Use test.step() aggressively in long tests — steps appear collapsibly in the HTML report and Trace Viewer, making triage dramatically faster. |
| Debug failures (UI Mode, Trace Viewer, Inspector) | [Debugging](pw-e2e-debugging.md) | Start with UI Mode (npx playwright test --ui) — it caches setup, has a locator picker, and shows DOM snapshots per action. Set trace:'on-first-retry' in CI config so the first lean run is fast and the retry captures the smoking gun cheaply. |
| Run E2E in CI with sharding | [CI Patterns](pw-e2e-ci-patterns.md) | Shard with --shard=N/M, collect blob reports from each node, then merge into one HTML report. Set workers:'50%' in CI (browsers are RAM-hungry), retries:2, trace:'on-first-retry', and artifacts failure-only. Add forbidOnly:true to catch committed test.only leaks. |
| Apply Drupal-specific E2E patterns | [Drupal & DDEV Patterns](pw-e2e-drupal-patterns.md) | Wait for AJAX with waitForResponse targeting /system/ajax — not waitForTimeout or jQuery.active. Handle Big Pipe by asserting on final content, not placeholder markup. Create entities via JSON:API, drive UI for the feature under test, verify via JSON:API. |
| Use ATK helpers in plain Playwright | [ATK Integration](pw-e2e-atk-integration.md) | Set testIdAttribute:'data-qa-id' in playwright.config.ts to get ATK's stable selector guarantees without writing your own preprocess hooks. Import only the ATK helper functions you need — drupalLogin, createNode — rather than adopting the full 36-test catalog. |
| Avoid common mistakes | [Anti-Patterns](pw-e2e-anti-patterns.md) | The top three flake causes are waitForTimeout as the default wait, tests that depend on each other's state, and brittle CSS selectors instead of role/label/test-id. Replace each with web-first assertions, fixture-based state isolation, and getByRole/getByLabel. |
| Find services and references | [Code Reference](pw-e2e-code-reference.md) | Quick lookup for getByRole/getByLabel/getByTestId locators, expect() assertions, test.extend fixtures, page.route mocking, request fixture, and the sharding/debugging CLI commands. |
