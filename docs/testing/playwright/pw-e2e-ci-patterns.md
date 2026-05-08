---
description: Run Playwright E2E efficiently in CI — sharding, blob reporter merge, worker limits, retries, timeout levels, and GitHub Actions matrix.
tldr: Shard with --shard=N/M, collect blob reports from each node, then merge into one HTML report. Set workers:'50%' in CI (browsers are RAM-hungry), retries:2, trace:'on-first-retry', and artifacts failure-only. Add forbidOnly:true to catch committed test.only leaks.
---

# CI Patterns

## When to Use

> Use sharding for suites over 100 tests. Combine blob reporter on each shard with `merge-reports` to get a unified HTML report. Store artifacts on failure only.

## Decision

| Knob | Default | Scope |
|---|---|---|
| `timeout` | 30000ms | Whole test |
| `expect.timeout` | 5000ms | Each `expect()` web-first assertion |
| `actionTimeout` | 0 (falls back to test timeout) | Each `click`, `fill`, etc. |
| `navigationTimeout` | 0 (falls back to test timeout) | `goto`, `waitForURL` |

Bias toward defaults. Raising `expect.timeout` to mask flake hides bugs.

## Pattern

```ts
// playwright.config.ts (CI-aware)
export default defineConfig({
  workers: process.env.CI ? '50%' : undefined,
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  forbidOnly: !!process.env.CI,
  reporter: process.env.CI ? [['blob']] : 'html',
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
});
```

```bash
# Sharding
npx playwright test --shard=1/4   # node 1
npx playwright test --shard=2/4   # node 2

# Merge after all shards complete
npx playwright merge-reports --reporter=html ./all-blob-reports
```

### GitHub Actions matrix

```yaml
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: blob-report-${{ matrix.shardIndex }}
          path: blob-report
          retention-days: 7

  merge-reports:
    if: ${{ !cancelled() }}
    needs: [test]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - uses: actions/download-artifact@v4
        with: { path: all-blob-reports, pattern: blob-report-* }
      - run: npx playwright merge-reports --reporter=html ./all-blob-reports
      - uses: actions/upload-artifact@v4
        with: { name: html-report, path: playwright-report }
```

## Common Mistakes

- **Wrong**: No sharding on suites > 100 tests — wastes wall time
- **Wrong**: Sharding without `blob` + merge — N partial reports, no unified view
- **Wrong**: `workers: 100%` — RAM exhaustion on small CI runners
- **Wrong**: Storing artifacts on success — multiplies cost; failure-only is the default

## See Also

- [Test Organization](pw-e2e-test-organization.md) — `fullyParallel`, `forbidOnly`, `test.only` guards
- [Debugging](pw-e2e-debugging.md) — reading traces from CI artifacts
- [HTML Report](../visual-regression/html-report/index.md) — navigating the merged HTML report
