---
description: What the Playwright per-test detail page contains and how to use it to investigate failures.
tldr: The per-test detail page shows errors, test source, step timings, attachments, console output, network log, and retry tabs. Use retry tabs to compare flaky attempts; use network log to find failed font or resource loads that cause visual changes.
---

# Per-Test Detail

## When to Use

> Use this when investigating a test failure beyond the diff — to understand context, diagnose flakes, or trace unexpected navigation.

## Pattern: video for "what happened?"

If `video: 'retain-on-failure'` is set, the report includes a `<video>` player. Useful when:

- The page navigated to an unexpected URL
- A click triggered a redirect you didn't expect
- A modal appeared that wasn't visible in the screenshot

## Decision

| Situation | Where to look |
|---|---|
| Stack trace for the failure | Errors section |
| Which step took too long | Steps tree with timings |
| Video of what happened | Attachments → video player |
| Console errors on the page | Console output section |
| Failed font or resource loads | Network log section |
| Comparing flaky retry attempts | Retry tabs |

## Pattern

Investigating a flaky test:

```
1. Click flaky test row (status: flaky)
2. Per-test page shows multiple retry tabs
3. Compare failed attempt vs passing attempt
4. Check: console errors only on first attempt? Network requests timing differently? Dynamic content not stable?
```

## Page Sections

| Section | Contents |
|---|---|
| Errors | Full stack with failing line highlighted |
| Test source | Synced view of test file with step pointer |
| Steps | Collapsible tree of `test.step()` blocks and built-in actions with timings |
| Attachments | `page.screenshot()` files, videos, arbitrary `testInfo.attach()` payloads |
| Console output | Captured `console.log/warn/error` from the page |
| Network log | Every request/response — method, status, content type, size |
| Stdout / Stderr | Output from the test process itself |
| Trace link | Opens the Trace Viewer |
| Retry tabs | Each attempt gets its own tab when `retries > 0` |

## Common Mistakes

- **Wrong**: `video: 'on'` in CI → **Right**: use `'retain-on-failure'` — avoid generating large videos for every test
- **Wrong**: ignoring console errors → **Right**: a JS error often causes the rendering issue visible in the diff
- **Wrong**: skipping the network log → **Right**: failed font loads are a classic source of mysterious visual changes

## See Also

- [VR Diff Panel](pw-report-vr-diff-panel.md)
- [Trace Viewer](pw-report-trace-viewer.md)
- [Navigation](pw-report-navigation.md)
