---
description: What the Playwright HTML report is and when to use it over other reporters.
tldr: Use html reporter as the primary post-run triage artifact for VR — it's a self-contained static SPA with Expected/Actual/Diff panels and a slider scrubber. Always include it; combine with other reporters for CI integration but never replace it.
---

# HTML Report Overview

## When to Use

> Use `html` reporter when VR tests fail and you need to see what changed and why. Use other reporters (`list`, `junit`, `github`) to complement it for terminal output or CI integration — never as a replacement.

## Decision

| Reporter | When |
|---|---|
| `html` | Triage VR diffs, browse traces — the canonical post-run artifact |
| `list` | Streaming line-per-test in terminal — local dev flow |
| `line` | Single updating terminal line — minimal CI logs |
| `dot` | One char per test — very large suites |
| `json` | Machine-readable — custom dashboards |
| `junit` | Required by Jenkins, Bamboo, Azure DevOps, GitLab test tab |
| `github` | GitHub Actions inline annotations on PR diff |
| `blob` | Sharded runs — merge later with `playwright merge-reports` |

For VR, **always include `html`**. Combine with others for CI integration; never replace.

## Pattern

The report is a self-contained static HTML bundle containing:

- `index.html` — the SPA entry point
- `data/` folder with screenshots (expected, actual, diff PNGs), videos, trace archives, console logs, network logs
- All JS/CSS bundled in — no external CDN required

Open from disk or any static host (but use `show-report` for traces — see [Viewing](pw-report-viewing.md)).

## Common Mistakes

- **Wrong**: using `list` only and trying to triage VR from terminal → **Right**: no diff viewer in terminal; the slider scrubber is the triage tool
- **Wrong**: skipping `html` because reports "take up space" → **Right**: they're regeneratable; developer time saved on triage dwarfs the disk cost

## See Also

- [Enabling](pw-report-enabling.md)
- [VR Diff Panel](pw-report-vr-diff-panel.md)
- Reference: [Playwright Reporters](https://playwright.dev/docs/test-reporters)
