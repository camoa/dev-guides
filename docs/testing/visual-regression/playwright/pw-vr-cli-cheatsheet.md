---
description: Quick reference for VR-relevant Playwright CLI commands — running tests, updating baselines, managing reports.
tldr: Use `npx playwright test --project=<name>` to scope runs, `npx playwright test -u` to update only changed baselines, and `npx playwright show-report` to open the HTML diff viewer. Always pass `--grep` when using `-u` to avoid bulk-updating the entire suite.
---

# CLI Cheatsheet

## When to Use

> Use this as a quick reference for running tests, updating baselines, and managing reports.

## Pattern

### Run tests

```bash
npx playwright test                                       # all tests, all projects
npx playwright test --project=chromium-1440              # single project
npx playwright test --grep "homepage"                    # filter by title
npx playwright test e2e/homepage.spec.ts                 # filter by file
npx playwright test e2e/homepage.spec.ts:42              # by line number
npx playwright test --headed                             # visible browser
npx playwright test --ui                                 # interactive UI mode
npx playwright test --workers=1                          # serialize
```

### Update baselines

```bash
npx playwright test --update-snapshots                   # = changed (mismatches + missing)
npx playwright test -u                                   # short form
npx playwright test --update-snapshots --grep "button"   # scoped update
npx playwright test --update-snapshots=all               # all executed tests
npx playwright test --update-snapshots=missing           # only create missing
npx playwright test --update-snapshots=none              # never update
```

### Reporter overrides

```bash
npx playwright test --reporter=html
npx playwright test --reporter=list,html
npx playwright test --reporter=json --output=results.json
```

### HTML report viewer

```bash
npx playwright show-report
npx playwright show-report ./playwright-report
npx playwright show-report --port 8080
npx playwright show-report --host 0.0.0.0               # LAN sharing
```

### Browser install

```bash
npx playwright install
npx playwright install chromium webkit
npx playwright install --with-deps
```

### Codegen (bootstrap a test scaffold)

```bash
npx playwright codegen https://playwright.dev
npx playwright codegen --browser=firefox
```

Let the recorder generate navigation; add `expect(page).toHaveScreenshot()` manually.

### Debug

```bash
npx playwright test --debug                              # PWDEBUG=1, headed, single worker
npx playwright test -x                                   # stop on first failure
npx playwright test --list                               # list tests without running
```

## Common Mistakes

- **Wrong**: `-u` without `--grep` → **Right**: accidentally updates the entire suite; always scope with `--grep`
- **Wrong**: `--debug` without realizing it implies `--workers=1` → **Right**: slower; use only when actually debugging
- **Wrong**: `show-report` without specifying path → **Right**: may open an old report; pass an explicit path

## See Also

- [Baseline Files](pw-vr-baseline-files.md)
- [Config Walkthrough](pw-vr-config-walkthrough.md)
- Reference: [Playwright CLI](https://playwright.dev/docs/test-cli)
