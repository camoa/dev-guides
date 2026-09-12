---
description: "Where Playwright HTML reports are generated and how to manage multiple report versions."
tldr: "Reports write to playwright-report/ by default and overwrite on every run. Override with outputFolder option. For historical archives, copy/zip after each run or use the blob reporter for sharded CI. Never confuse outputFolder (HTML SPA) with outputDir (raw test-results)."
---

# Report Generation

## When to Use

> Controlling where reports land and how they relate to test runs.

## Default Location

`playwright-report/` at the project root, written at the end of the run.

## Pattern: Override Location

```ts
reporter: [['html', { outputFolder: 'reports/html' }]],
```

## Per-Run Behavior

Playwright **overwrites** the contents of `outputFolder` at the start of every run. To keep historical reports:

| Approach | When |
|---|---|
| Configure unique `outputFolder` per run (timestamped) | Local long-term archive |
| Copy/zip `playwright-report/` after the run | Simple, manual |
| Use the **blob reporter** (`['blob']`), then `npx playwright merge-reports --reporter=html` | Sharded CI runs |

## Decision: `playwright-report/` vs `test-results/`

| Folder | Contains |
|---|---|
| `playwright-report/` | The HTML SPA + bundled attachments — the triage UI |
| `test-results/` | Raw per-test attachments (failure screenshots, traces, videos) — referenced by the report at generation; safe to delete after report is built |

Both are gitignored by convention. Only commit `*-snapshots/` (the baselines next to test files).

## Pattern: Blob Reporter for Sharded Runs

```ts
// On each shard
reporter: [['blob']]
```

```bash
# After all shards
npx playwright merge-reports --reporter=html ./all-blobs
```

Produces one unified HTML report from N parallel shards.

## Common Mistakes

- **Committing `playwright-report/`** — clutters the repo; regeneratable
- **Expecting reports to accumulate without explicit copying** — they don't; every run overwrites
- **Confusing `outputFolder` (HTML report) with `outputDir` (test-results)** — different config keys, different folders

## See Also

- [Viewing](pw-report-viewing.md)
- [Sharing](pw-report-sharing.md)
- [Configuration Reference](pw-report-configuration.md)
