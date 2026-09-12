---
description: "How to combine the Playwright HTML reporter with other reporters for different audiences."
tldr: "Use html+github+junit in CI for triage UI, PR annotations, and dashboard XML. Locally, use list+html. Always include html — it's the human triage artifact. Use json for machine consumption (Claude, scripts). Blob reporter is for sharded runs only."
---

# Reporter Combos

## When to Use

> Combining HTML with other reporters for different audiences.

## Pattern: Typical CI Combo

```ts
reporter: process.env.CI
  ? [['github'], ['html', { open: 'never' }], ['junit', { outputFile: 'junit.xml' }]]
  : [['list'], ['html']],
```

| Reporter | Audience | Output |
|---|---|---|
| `github` | GitHub Actions PR diff | Inline annotations on changed files |
| `html` | Triage UI | The static SPA |
| `junit` | CI dashboards (Jenkins, GitLab tab) | JUnit XML |

## Pattern: Machine-Readable + Human-Readable

For Claude or other automation that consumes test results plus humans who triage:

```ts
reporter: [
  ['list'],                                   // Live terminal output
  ['html'],                                   // Human triage
  ['json', { outputFile: 'results.json' }],   // Machine consumption
]
```

## Decision: Which Reporters to Combine

| Audience | Reporter |
|---|---|
| Local dev | `list` (terminal) + `html` (triage) |
| GitHub PR diff annotations | `github` |
| Jenkins / GitLab test tab | `junit` |
| Custom dashboards | `json` |
| Machine consumption (Claude, scripts) | `json` |
| Triage humans | `html` (always include) |
| Sharded CI runs | `blob` on each shard, merge to `html` |

## Common Mistakes

- **Single reporter in CI** — either humans can't triage or machines can't parse; combine
- **`html` and `junit` with same `outputFile`** — JUnit needs a file path, HTML needs a folder; don't conflate
- **Forgetting `github` reporter on GitHub Actions** — losing inline PR annotations is a missed UX win

## See Also

- [Playwright for Visual Regression](../playwright/index.md) — the assertions that produce the diffs the report shows
- [Pixelmatch Image Diff](../pixelmatch/index.md) — the engine producing the diff colors you see
- [Visual Regression Workflow](../workflow/index.md) — how to use the report in your triage procedure
- Reference: [Playwright Reporters](https://playwright.dev/docs/test-reporters)
- Reference: [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
