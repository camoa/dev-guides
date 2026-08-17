---
description: Visual regression workflow — decisions for designing, running, and maintaining a pixel-comparison test suite with Playwright.
tracks:
  - project: playwright
    registry: npm
    channel: stable
    declared: null
    note: no version stated in prose
    verified: 2026-05-08
guide-meta:
  concepts:
    - visual regression testing
    - VR testing
    - screenshot testing
    - baseline management
    - pixel diff
    - pixelmatch
    - toHaveScreenshot
    - Playwright VR
    - snapshot testing
    - baseline governance
    - animations disabled
    - data-vrt-mask
    - threshold tuning
    - maxDiffPixels
    - maxDiffPixelRatio
    - storage-state authentication
    - DDEV playwright
    - Playwright Docker image
    - vrSnapshot
    - waitForStableLayout
    - flaky VR tests
  not:
    - unit testing (see drupal/tdd)
    - PHPUnit tests (see drupal/tdd)
    - functional testing
    - accessibility testing (axe-core)
    - performance testing (Lighthouse)
    - Storybook visual testing (see drupal/storybook)
    - design QA / Figma comparison
  requires: []
  complements:
    - drupal/tdd
    - drupal/storybook
    - drupal/sdc
  specializes: ""
  category: testing
---

# Visual Regression Workflow

**Philosophy**: VR testing answers exactly one question — did the rendered pixels of this UI change between baseline and current? The whole workflow is about getting truthful pixel comparisons: stable captures, intentional baselines, and a triage habit that treats every diff as a real regression until proven otherwise.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what VR catches and what it doesn't | [What VR Is For](vr-what-its-for.md) | Use VR when you need to catch unintended visual drift from a code change. VR is baseline governance — every diff is either an intentional baseline update or an unintended regression. Never use it as a substitute for design QA or accessibility testing. |
| Decide whether a change needs a VR test | [When to Add a VR Test](vr-when-to-add.md) | Add a VR test when you can identify the smallest screenshot that would catch a regression in this change. High-signal, stable surfaces (SDC atoms, hero, forms, critical landing pages) get VR; volatile surfaces (live feeds, external-API pages, dashboards) do not. |
| Pick what to capture (scope, state, breakpoint, browser, theme) | [What to Capture](vr-what-to-capture.md) | Use the 5-axis cube (scope × state × breakpoint × browser × theme) and pick the smallest cross-section per test. Default to component-level scope, Chromium-only, 3 breakpoints for responsive components, and only capture states with distinct CSS. |
| Design the browser × viewport matrix | [Matrix Design](vr-matrix-design.md) | Use a tiered matrix instead of a uniform N×M cube — component-shared tests use 1 viewport, layout-aware and page tests use 3 viewports, cross-browser tests use 1 viewport with 3 browsers. Name projects so the name flows into the baseline filename. |
| Decide where baselines live and how to manage them | [Baseline Management](vr-baseline-management.md) | Commit baselines to the repo (Playwright default) for Drupal/DDEV teams without a VR-vendor budget. Keep baselines on main, update them in PRs with the UI change, and never auto-update on main from CI. Prune orphans quarterly. |
| Stabilize captures before any baseline is set | [Stability Checklist](vr-stability-checklist.md) | Run the 10-point checklist before any baseline capture: disable animations, hide carets, wait for fonts and images, wait for network idle, mask dynamic regions, normalize scroll and focus, dismiss cookie banners, and pin the Chromium version via the official Playwright Docker image. |
| Tune threshold, maxDiffPixels, maxDiffPixelRatio | [Threshold Tuning](vr-threshold-tuning.md) | Use threshold 0.20 (Playwright default) for standard tests; tighten to 0.05–0.10 for pixel-perfect same-env captures; use maxDiffPixels for small components and maxDiffPixelRatio for full-page shots. Set a global floor in playwright.config.ts and override per assertion only with a comment. |
| Author tests with reusable patterns | [Authoring Patterns](vr-authoring-patterns.md) | Extract a waitForStableLayout helper and a vrSnapshot macro so most tests are 1–3 lines. Use data-vrt-mask in Twig markup to decouple volatility masking from test files. Prefer dedicated fixture routes over real content pages for SDC atoms. |
| Update baselines after intentional UI changes | [Baseline Update Workflow](vr-baseline-update-workflow.md) | Always scope baseline updates with --grep to affected tests. Pair every baseline update with the UI change in the same commit or PR. Never do a bulk --update-snapshots as a default response to red CI. Review diffs using the Playwright HTML report, not just GitHub's PNG diff. |
| Triage a failed VR test | [Triaging False Positives](vr-triaging-false-positives.md) | When a diff fires, work the triage tree: same image on re-run (flake → stability checklist), differs by machine (env drift → pin Docker image), differs per browser (browser-specific → per-browser baselines), differs CI vs local (always capture inside Docker). |
| Keep the suite healthy long-term | [VR Debt & Hygiene](vr-debt-and-hygiene.md) | Run quarterly hygiene: prune orphan PNGs, fix drifting baselines at the root cause, cull whole-page shots covered by component shots, and walk the suite with the team to retire tests that haven't caught a regression in 6 months. |
| Apply this to a Drupal/DDEV site | [Drupal & DDEV Procedure](vr-drupal-ddev-procedure.md) | Use storage-state authentication (.auth/admin.json, gitignored). Set baseURL to DDEV_PRIMARY_URL with ignoreHTTPSErrors and run inside ddev exec. Clear Drupal cache once before the suite, never between individual tests. Mask time, counters, contextual links, and Big Pipe placeholders. |
| Avoid common procedural mistakes | [Anti-Patterns](vr-anti-patterns.md) | The most destructive VR anti-patterns are: bulk --update-snapshots as the default response to failures, capturing on host and comparing in CI, bumping threshold to silence flakes, and committing .auth/ session files. |
| Plan a sane VR program from scratch | [Reference Program](vr-reference-program.md) | Build a 4-tier program: Tier 1 smoke set (~15 baselines); Tier 2 component set (~50 baselines against fixture routes); Tier 3 theme variants (~20 baselines, conditional); Tier 4 cross-browser (~10 baselines, nightly). Total: ~95 baselines, ~5 minutes locally. |
