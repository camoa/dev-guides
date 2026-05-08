---
description: Playwright for Visual Regression — decision guides for setup, screenshot APIs, browser projects, viewports, stability, determinism, and Drupal/DDEV integration.
guide-meta:
  concepts:
    - playwright
    - toHaveScreenshot
    - toMatchSnapshot
    - page.screenshot
    - playwright.config.ts
    - browser projects
    - viewport matrix
    - baseline files
    - snapshotPathTemplate
    - stability controls
    - screenshot.css
    - determinism
    - Docker playwright
    - CLI cheatsheet
    - DDEV playwright
    - storage state auth
    - pixelmatch
    - animations disabled
    - mask locator
  not:
    - pixelmatch internals (see pixelmatch guide)
    - playwright-html-report (see playwright HTML report guide)
    - VR procedure and workflow decisions (see testing/visual-regression/workflow)
  requires:
    - testing/visual-regression/workflow
  complements:
    - testing/visual-regression/workflow
  specializes: ""
  category: testing
---

# Playwright for Visual Regression

| I need to... | Guide | Summary |
|---|---|---|
| Install Playwright in a Node or Drupal project | [Setup](pw-vr-setup.md) | Use `npm init playwright@latest` for new Node projects; isolate under `tests/playwright/` for Drupal repos. After any package upgrade, always re-run `npx playwright install --with-deps` or browser binaries will be stale and fail to launch. |
| Choose between screenshot APIs | [Screenshot APIs](pw-vr-screenshot-apis.md) | Use `expect(page).toHaveScreenshot()` for all VR assertions — it auto-retries for stability and diffs against a baseline. `page.screenshot()` captures only; `toMatchSnapshot()` diffs but skips the stability retry. |
| Configure browser projects (Chromium / Firefox / WebKit) | [Browser Projects](pw-vr-browser-projects.md) | Define one project per browser in `playwright.config.ts` using `devices` presets; the project name flows into baseline filenames. Start with Chromium-only for VR — adding browsers multiplies baselines 2-3x and should only be done when your suite is stable. |
| Capture at multiple viewport sizes | [Viewport & Device Matrix](pw-vr-viewport-matrix.md) | Use one project per (browser × viewport) combination — the project name flows into the baseline filename, giving each tuple its own image. Never call `page.setViewportSize()` mid-test; it causes baseline filename collisions. |
| Reference all options for toHaveScreenshot() | [Screenshot Options](pw-vr-screenshot-options.md) | Set `animations: 'disabled'`, `caret: 'hide'`, `threshold: 0.15`, and `maxDiffPixelRatio: 0.005` globally in `expect.toHaveScreenshot`. Never override `animations: 'allow'` — it reintroduces flake. |
| Understand baseline file naming and storage | [Baseline Files](pw-vr-baseline-files.md) | Baselines follow `<test-name>-<ordinal>-<projectName>-<platform>.png` stored in `<spec>.ts-snapshots/` next to the spec file. Commit `*-snapshots/`; gitignore `test-results/`. |
| Make captures deterministic (animations, fonts, masks) | [Stability Controls](pw-vr-stability-controls.md) | Add `document.fonts.ready`, `animations: 'disabled'`, and a `stylePath` injecting `screenshot.css` to eliminate font swap, CSS animation frames, and dynamic content regions. |
| Ensure local and CI produce the same screenshots | [Determinism](pw-vr-determinism.md) | Always capture baselines inside the same Docker image that runs in CI. Pin `@playwright/test` and the Docker tag to the same version number. Never capture on macOS and compare in Linux. |
| Organize tests with fixtures and parallelism | [Test Organization](pw-vr-test-organization.md) | Use `test.extend` fixtures for shared auth and page state instead of globals or `beforeEach` chains. Set `fullyParallel: true` globally but apply `mode: 'serial'` only to tests that share Drupal editorial state. |
| Configure every key in playwright.config.ts | [Config Walkthrough](pw-vr-config-walkthrough.md) | Set `reporter: 'html'`, `outputDir: 'test-results'`, `forbidOnly: !!process.env.CI`, and pin `colorScheme`, `locale`, `timezoneId` in `use`. Define the browser × viewport matrix under `projects`. |
| Run the right CLI command | [CLI Cheatsheet](pw-vr-cli-cheatsheet.md) | Use `npx playwright test --project=<name>` to scope runs, `npx playwright test -u` to update only changed baselines, and `npx playwright show-report` to open the HTML diff viewer. |
| Identify and fix common anti-patterns | [Anti-Patterns](pw-vr-anti-patterns.md) | The two most damaging mistakes are capturing baselines on macOS and comparing in Linux CI, and committing baselines from a flaky state. Pin a Docker image, add stability controls first, then capture. |
| Use Playwright outside the test runner | [Programmatic API](pw-vr-programmatic.md) | Use the `playwright` package (not `@playwright/test`) for standalone scripts. `toHaveScreenshot()` only works inside the test runner — for diffing in custom scripts, call pixelmatch directly. |
| Run Playwright against Drupal/DDEV | [Drupal & DDEV](pw-vr-drupal-ddev.md) | Set `baseURL` to `DDEV_PRIMARY_URL`, `ignoreHTTPSErrors: true`, and run via `ddev exec npx playwright test`. Use storage-state auth with a setup project; gitignore `.auth/`. |
