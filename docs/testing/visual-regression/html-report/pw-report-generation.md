---
description: Where Playwright HTML reports are generated and how to manage multiple report versions.
tldr: Reports write to playwright-report/ by default and overwrite on every run. Override with outputFolder option. For historical archives, copy/zip after each run or use the blob reporter for sharded CI. Never confuse outputFolder (HTML SPA) with outputDir (raw test-results).
---

# Report Generation

## When to Use

> Use this when controlling where reports land, how they relate to test runs, or managing sharded CI report merging.

## Decision

| Approach | When |
|---|---|
| Default `playwright-report/` | Simple local development |
| Custom `outputFolder` | Consistent path in CI pipelines |
| Copy/zip after each run | Simple local archive of historical reports |
| `blob` reporter + merge | Sharded CI runs across multiple machines |

## Pattern

Override location:

```ts
reporter: [['html', { outputFolder: 'reports/html' }]],
```

Blob reporter for sharded runs:

```ts
// On each shard
reporter: [['blob']]
```

```bash
# After all shards complete
npx playwright merge-reports --reporter=html ./all-blobs
```

## Decision: `playwright-report/` vs `test-results/`

| Folder | Contains |
|---|---|
| `playwright-report/` | The HTML SPA + bundled attachments — the triage UI |
| `test-results/` | Raw per-test attachments (failure screenshots, traces, videos) — referenced at generation; safe to delete after |

Both are gitignored by convention. Only commit `*-snapshots/` (the baselines next to test files).

## Common Mistakes

- **Wrong**: committing `playwright-report/` to git → **Right**: gitignore it; it's regeneratable
- **Wrong**: assuming reports accumulate across runs → **Right**: every run overwrites; copy/zip if you want archives
- **Wrong**: confusing `outputFolder` (HTML report) with `outputDir` (test-results) → **Right**: different config keys, different folders

## See Also

- [Viewing](pw-report-viewing.md)
- [Sharing](pw-report-sharing.md)
- [Configuration Reference](pw-report-configuration.md)
