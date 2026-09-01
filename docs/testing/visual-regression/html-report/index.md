---
description: Playwright HTML Report — decision guides for configuring, viewing, navigating, and sharing the VR triage UI.
tracks:
  - project: playwright
    registry: npm
    channel: stable
    declared: null
    note: no version stated in prose
    verified: 2026-05-08
guide-meta:
  concepts:
    - playwright html report
    - show-report
    - VR diff panel
    - slider scrubber
    - Expected Actual Diff
    - trace viewer
    - trace.zip
    - outputFolder
    - attachmentsBaseURL
    - playwright-report
    - test-results
    - blob reporter
    - merge-reports
    - reporter combos
    - junit reporter
    - github reporter
    - artifact upload
    - DDEV playwright report
    - baseline updates
    - --update-snapshots
  not:
    - toHaveScreenshot setup and API options (see testing/visual-regression/playwright)
    - pixelmatch algorithm internals (see testing/visual-regression/pixelmatch)
    - VR workflow and triage procedure decisions (see testing/visual-regression/workflow)
  requires:
    - testing/visual-regression/playwright
  complements:
    - testing/visual-regression/workflow
    - testing/visual-regression/pixelmatch
  category: testing
---

# Playwright HTML Report

| I need to... | Guide | Summary |
|---|---|---|
| Understand what the HTML report is and when to use it | [Overview](pw-report-overview.md) | Use html reporter as the primary post-run triage artifact for VR — it's a self-contained static SPA with Expected/Actual/Diff panels and a slider scrubber. Always include it; combine with other reporters for CI integration but never replace it. |
| Enable the HTML reporter in my config | [Enabling](pw-report-enabling.md) | Set reporter to 'html' in playwright.config.ts for the simplest case, or use an array of arrays for multiple reporters. CLI --reporter flag overrides config. The most common mistake is the flat string array syntax — multi-reporter requires nested arrays. |
| Control where reports are generated | [Generation](pw-report-generation.md) | Reports write to playwright-report/ by default and overwrite on every run. Override with outputFolder option. For historical archives, copy/zip after each run or use the blob reporter for sharded CI. Never confuse outputFolder (HTML SPA) with outputDir (raw test-results). |
| Open and view a generated report | [Viewing](pw-report-viewing.md) | Use `npx playwright show-report` to open reports — never open index.html via file:// as it breaks the trace viewer. The command starts a static HTTP server at localhost:9323. On failure, the report auto-opens locally; in CI (CI=true) it never auto-opens. |
| Navigate the report to find a test | [Navigation](pw-report-navigation.md) | The report home page is a flat list filtered by status, project, and free-text search. Use status chip (Failed) → project filter → keyword search → click row as the standard triage flow. Tests are failed-first ordered; there is no manual sort. |
| Triage a toHaveScreenshot() failure with the diff panel | [VR Diff Panel](pw-report-vr-diff-panel.md) | When toHaveScreenshot() fails, the per-test detail shows a diff panel with Expected, Actual, and Diff images in four interactive modes — Slider is the most useful for catching pixel shifts. Red diff pixels exceed threshold; yellow are anti-aliasing skips. |
| Investigate a failure beyond the diff | [Per-Test Detail](pw-report-per-test-detail.md) | The per-test detail page shows errors, test source, step timings, attachments, console output, network log, and retry tabs. Use retry tabs to compare flaky attempts; use network log to find failed font or resource loads that cause visual changes. |
| Step through a test action-by-action with DOM snapshots | [Trace Viewer](pw-report-trace-viewer.md) | Enable trace with `trace: 'on-first-retry'` (recommended CI default). The Trace Viewer provides DOM snapshots at every action step, timeline scrubbing, and network/console inspection. Keep zip intact — the viewer expects the archive. |
| Read reports from a multi-browser or multi-viewport run | [Multiple Projects](pw-report-multiple-projects.md) | Each browser/viewport project appears as a separate row with a color-coded project tag. Filter by project chip to scope to one browser; the report has no cross-browser diff view — inspect one project at a time. |
| Update baselines after triaging a diff | [Baseline Updates](pw-report-baseline-updates.md) | The HTML report has no approve/accept button — baseline updates are CLI-only with --update-snapshots. Always scope updates with --grep to avoid silently accepting regressions. Commit baselines after updating or CI will still fail. |
| Share a report with a teammate or reviewer | [Sharing](pw-report-sharing.md) | Share by zip+send, GitHub Actions artifact upload, static hosting, or port forwarding. Recipient always needs a real HTTP server (show-report) — never file://. For large reports with CDN-offloaded images, use attachmentsBaseURL with a trailing slash. |
| Reference every HTML reporter config option | [Configuration Reference](pw-report-configuration.md) | The HTML reporter accepts outputFolder, open, host, port, attachmentsBaseURL, and noSnippets options. All have environment variable overrides. The most common mistake is omitting the trailing slash on attachmentsBaseURL. |
| Run reports locally, in DDEV, or in CI | [Running Modes](pw-report-running-modes.md) | Local runs auto-open the report on failure. In DDEV, run show-report on the host (not in the container) since playwright-report/ is on the bind-mounted volume. In CI, upload as an artifact with if:always() and set open:'never'. |
| Avoid common report anti-patterns | [Anti-Patterns](pw-report-anti-patterns.md) | The twelve most common HTML report mistakes — from file:// access breaking traces to bulk --update-snapshots accepting regressions. Each has a direct Right answer. Use as a pre-review checklist. |
| Combine HTML with other reporters | [Reporter Combos](pw-report-reporter-combos.md) | Use html+github+junit in CI for triage UI, PR annotations, and dashboard XML. Locally, use list+html. Always include html. Use json for machine consumption. Blob reporter is for sharded runs only. |
