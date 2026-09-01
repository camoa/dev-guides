---
description: How to enable and use the Playwright Trace Viewer from the HTML report.
tldr: "Enable trace with `trace: 'on-first-retry'` (recommended CI default). The Trace Viewer provides DOM snapshots at every action step, timeline scrubbing, and network/console inspection. Open from the HTML report or standalone via `npx playwright show-trace`. Keep zip intact — the viewer expects the archive."
---

# Trace Viewer

## When to Use

> Use the Trace Viewer when stepping through a test action-by-action with full DOM snapshots — it's the most powerful debugging tool Playwright ships.

## What's in `trace.zip`

- Action log with arguments and results
- Full DOM snapshots at *before* and *after* each action — Trace Viewer reconstructs them in an iframe so you can inspect/scroll the page state at any point
- Screenshots filmstrip across the timeline
- Network requests with headers/bodies
- Console messages
- Test source code mapped to actions

## Decision

| Trace mode | When |
|---|---|
| `'off'` | No trace |
| `'on'` | Every test — heavy, dev only |
| `'retain-on-failure'` | Always record; keep only on failure |
| `'on-first-retry'` | **Recommended CI default** — first attempt lean; retry records |
| `'on-all-retries'` | All retry attempts |

## Pattern

Enable trace generation:

```ts
export default defineConfig({
  use: {
    trace: 'on-first-retry',
  },
});
```

Open trace standalone:

```bash
npx playwright show-trace path/to/trace.zip
```

Or upload to **trace.playwright.dev** — fully client-side viewer; processes the zip in-browser. Easiest way to share a trace without sharing the full report.

## Trace Viewer Panels

| Panel | What it shows |
|---|---|
| Timeline (top) | Filmstrip + action waterfall; click a frame to seek |
| Actions | Every Playwright call; selecting one highlights the locator in the DOM snapshot |
| Before / After | DOM snapshot at each side of the action |
| Source | Test source code mapped to the selected action |
| Log / Console / Network | Low-level call log, page console, and network requests |

## Common Mistakes

- **Wrong**: `trace: 'on'` in CI → **Right**: generates GBs of trace data; use `'on-first-retry'`
- **Wrong**: unzipping `trace.zip` before opening → **Right**: viewer expects the archive intact
- **Wrong**: missing the trace icon in the report → **Right**: you didn't enable trace generation; check `use.trace`

## See Also

- [Per-Test Detail](pw-report-per-test-detail.md)
- [Running Modes](pw-report-running-modes.md)
- Reference: [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
