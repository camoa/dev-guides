---
description: Understand Playwright baseline file naming, storage layout, snapshotPathTemplate, and version control strategy.
tldr: Baselines follow `<test-name>-<ordinal>-<projectName>-<platform>.png` stored in `<spec>.ts-snapshots/` next to the spec file. Commit `*-snapshots/`; gitignore `test-results/`. Use `snapshotPathTemplate` to centralize baselines, but set it once and never change it.
---

# Baseline Files

## When to Use

> Use this when configuring where baselines are stored, understanding filename patterns, or deciding how to organize snapshots in version control.

## Default Layout

```
tests/
├── homepage.spec.ts
└── homepage.spec.ts-snapshots/
    ├── homepage-1-chromium-linux.png
    └── homepage-1-firefox-linux.png
```

Filename pattern: `<test-name>-<ordinal>-<projectName>-<platform>.png`

| Segment | Source |
|---|---|
| `test-name` | Sanitized test title |
| `ordinal` | Incremented per assertion in one test |
| `projectName` | Project name from config; falls back to browser name |
| `platform` | `process.platform` — `darwin`, `linux`, `win32` |

## Pattern

### Named snapshot

```ts
await expect(page).toHaveScreenshot('landing.png');
// → tests/landing.spec.ts-snapshots/landing-chromium-linux.png

await expect(page).toHaveScreenshot(['marketing', 'pricing.png']);
// → tests/landing.spec.ts-snapshots/marketing/pricing-chromium-linux.png
```

### `snapshotPathTemplate` — centralize baselines

```ts
snapshotPathTemplate: '__screenshots__{/projectName}/{testFilePath}/{arg}{ext}'
```

Per-assertion-type override:

```ts
expect: {
  toHaveScreenshot: {
    pathTemplate: '{testDir}/__screenshots__{/projectName}/{testFilePath}/{arg}{ext}'
  },
}
```

### `--update-snapshots` modes

| Mode | Behavior |
|---|---|
| `'all'` | Update all executed tests' snapshots |
| `'changed'` (CLI `-u` default) | Update only mismatching; create missing |
| `'missing'` (default without flag) | Only create missing |
| `'none'` | Never update |

```bash
npx playwright test --update-snapshots         # = changed
npx playwright test --update-snapshots=all
npx playwright test -u                         # short form
```

## Version Control

| Path | Action |
|---|---|
| `*-snapshots/` | Commit to git |
| `test-results/` (`*-actual.png`, `*-diff.png`) | Gitignore |
| `playwright-report/` | Gitignore |

## Common Mistakes

- **Wrong**: Committing `test-results/` → **Right**: it contains per-run diff PNGs and bloats the repo
- **Wrong**: Changing `snapshotPathTemplate` after baselines exist → **Right**: set it once; changing it orphans every existing baseline
- **Wrong**: Renaming a test without deleting old baselines → **Right**: orphaned files accumulate; delete manually

## See Also

- [CLI Cheatsheet](pw-vr-cli-cheatsheet.md)
- [Browser Projects](pw-vr-browser-projects.md)
- Reference: [Playwright Snapshots](https://playwright.dev/docs/test-snapshots)
