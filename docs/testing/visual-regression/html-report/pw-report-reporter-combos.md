---
description: How to combine the Playwright HTML reporter with other reporters for different audiences.
tldr: Use html+github+junit in CI for triage UI, PR annotations, and dashboard XML. Locally, use list+html. Always include html — it's the human triage artifact. Use json for machine consumption (Claude, scripts). Blob reporter is for sharded runs only.
---

# Reporter Combos

## When to Use

> Use this when configuring multiple reporters for different audiences — CI pipeline, PR reviewers, dashboard systems, or automated tooling.

## Decision

| Audience | Reporter |
|---|---|
| Local dev | `list` (terminal) + `html` (triage) |
| GitHub PR diff annotations | `github` |
| Jenkins / GitLab test tab | `junit` |
| Custom dashboards | `json` |
| Machine consumption (Claude, scripts) | `json` |
| Triage humans | `html` (always include) |
| Sharded CI runs | `blob` on each shard, merge to `html` |

## Pattern

Typical CI combo:

```ts
reporter: process.env.CI
  ? [['github'], ['html', { open: 'never' }], ['junit', { outputFile: 'junit.xml' }]]
  : [['list'], ['html']],
```

Machine-readable + human-readable:

```ts
reporter: [
  ['list'],                                   // Live terminal output
  ['html'],                                   // Human triage
  ['json', { outputFile: 'results.json' }],   // Machine consumption
]
```

## Common Mistakes

- **Wrong**: single reporter in CI → **Right**: either humans can't triage or machines can't parse; combine both
- **Wrong**: `html` and `junit` with the same `outputFile` path → **Right**: JUnit needs a file path; HTML needs a folder — different keys
- **Wrong**: omitting `github` reporter on GitHub Actions → **Right**: missing inline PR annotations is a lost UX win

## See Also

- [Enabling](pw-report-enabling.md)
- [Configuration Reference](pw-report-configuration.md)
- Reference: [Playwright Reporters](https://playwright.dev/docs/test-reporters)
- Reference: [Playwright Trace Viewer](https://playwright.dev/docs/trace-viewer)
