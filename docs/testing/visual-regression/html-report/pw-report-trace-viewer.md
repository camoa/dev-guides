---
description: "How to enable and use the Playwright Trace Viewer from the HTML report."
tldr: "Enable trace with `trace: 'on-first-retry'` (recommended CI default). The Trace Viewer provides DOM snapshots at every action step, timeline scrubbing, and network/console inspection. Keep zip intact — the viewer expects the archive."
---

# Trace Viewer

## When to Use

> Stepping through a test action-by-action with full DOM snapshots — the most powerful debugging tool Playwright ships.

## Pattern: Enable Trace Generation

```ts
export default defineConfig({
  use: {
    trace: 'on-first-retry',
  },
});
```

## Decision: Trace Modes

| Mode | When |
|---|---|
| `'off'` | No trace |
| `'on'` | Every test (heavy, dev only) |
| `'retain-on-failure'` | Always record; keep only on failure |
| `'on-first-retry'` | **Recommended CI default** — first attempt lean; retry records |
| `'on-all-retries'` | All retry attempts |
| Granular: `{ mode: 'on', screenshots: true, snapshots: true, sources: true }` | Fine control |

## What's in `trace.zip`

- Action log with arguments and results
- Full DOM snapshots at *before* and *after* each action — Trace Viewer reconstructs them in an iframe so you can inspect/scroll the page state at any point
- Screenshots filmstrip across the timeline
- Network requests with headers/bodies
- Console messages
- Test source code mapped to actions

## Trace Viewer Panels

- **Timeline** (top) — filmstrip + action waterfall; click a frame to seek
- **Actions** — list of every Playwright call; selecting one shows the locator highlight in the DOM snapshot iframe
- **Bottom pane tabs** — Before / After / Action / Source / Call / Log / Errors / Console / Network / Attachments

## Pattern: Open from HTML Report

The HTML report links to the Trace Viewer via the trace icon on each retry/attempt. Clicking opens the trace **inside** the report (when served via `show-report`).

## Pattern: Standalone Trace Viewing

```bash
npx playwright show-trace path/to/trace.zip
```

Or upload to **trace.playwright.dev** — fully client-side viewer (no upload to a server; processes the zip in-browser). Easiest way to share a trace with a teammate when you can't share the whole report.

## Common Mistakes

- **`trace: 'on'`** in CI — generates GBs of trace data
- **Unzipping `trace.zip`** before opening — viewer expects the archive intact
- **Missing the trace icon in the report** — you didn't enable trace generation; check `use.trace`

## See Also

- [Per-Test Detail](pw-report-per-test-detail.md)
- [Running Modes](pw-report-running-modes.md)
- Reference: [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
