---
description: "What the Playwright per-test detail page contains and how to use it to investigate failures."
tldr: "The per-test detail page shows errors, test source, step timings, attachments, console output, network log, and retry tabs. Use retry tabs to compare flaky attempts; use network log to find failed font or resource loads that cause visual changes."
---

# Per-Test Detail

## When to Use

> Investigating a test failure beyond just the diff — understanding context.

## What's on the Page

Beyond the VR diff panel:

| Section | Contents |
|---|---|
| **Errors** | Full stack with the failing line of source code highlighted |
| **Test source** | Synced view of the test file with the executed step pointer |
| **Steps** | Collapsible tree of `test.step()` blocks and built-in actions, with timings |
| **Attachments** | `page.screenshot()` files, videos (when `video: 'on'` or `'retain-on-failure'`), arbitrary `testInfo.attach('name', { body, contentType })` payloads |
| **Console output** | Captured `console.log/warn/error` from the page under test |
| **Network log** | Every request/response with method, status, content type, size |
| **Stdout / Stderr** | Captured from the test process itself |
| **Trace** link | Opens the [Trace Viewer](pw-report-trace-viewer.md) |
| **Retry tabs** | When `retries > 0`, each attempt gets its own tab to compare attempts |

## Pattern: Investigating a Flake

When the same test was flaky (passed on retry):

1. Click the test row (status: `flaky`)
2. Per-test page shows multiple retry tabs
3. Compare the failed attempt vs the passing attempt
4. Likely causes: console errors only on first attempt, network requests timing differently, dynamic content not yet stable

## Pattern: Video for "What Happened?"

If `video: 'retain-on-failure'` is set, the report includes a `<video>` player. Useful when:

- The page navigated to an unexpected URL
- A click triggered a redirect you didn't expect
- A modal appeared that wasn't visible in the screenshot

## Common Mistakes

- **`video: 'on'` in CI** — produces large videos for every test; use `'retain-on-failure'`
- **Ignoring console errors** — a JavaScript error often causes the rendering issue you're seeing in the diff
- **Not checking the network log** — failed font loads are a classic source of "visual changed mysteriously"

## See Also

- [VR Diff Panel](pw-report-vr-diff-panel.md)
- [Trace Viewer](pw-report-trace-viewer.md)
- [Navigation](pw-report-navigation.md)
