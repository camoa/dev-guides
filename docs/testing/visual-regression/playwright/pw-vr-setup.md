---
description: "Install and configure Playwright for visual regression in a Node or Drupal/PHP project."
tldr: "Use `npm init playwright@latest` for new Node projects; isolate under `tests/playwright/` for Drupal repos. After any package upgrade, always re-run `npx playwright install --with-deps` or browser binaries will be stale and fail to launch."
---

# Playwright Setup

## When to Use

> Use this when bootstrapping Playwright on a new project or installing into an existing Drupal site.

## Decision

| Project Type | Setup Path | Notes |
|---|---|---|
| New Node project | `npm init playwright@latest` | Interactive scaffold; picks TypeScript, test folder, CI workflow |
| Drupal/PHP repo | Manual install under `tests/playwright/` | Isolates Node artifacts from composer root |

## Pattern

### New Node project

```bash
npm init playwright@latest
```

Interactive prompts:
- TypeScript or JavaScript (default: TypeScript)
- Tests folder name (default: `tests`, or `e2e` if `tests` already exists)
- GitHub Actions workflow (recommended for CI)
- Install Playwright browsers (default: yes)

Scaffolds: `playwright.config.ts`, `package.json`, `tests/example.spec.ts`.

### Drupal/PHP repo layout

```
<drupal-root>/
├── composer.json
├── web/
└── tests/playwright/
    ├── package.json          # @playwright/test devDependency
    ├── playwright.config.ts
    └── e2e/
        └── homepage.spec.ts
```

Run from inside `tests/playwright/`. `testDir` resolves relative to the config file.

### Browser binary management

Playwright browser binaries are versioned with the Playwright package — they are **not** the system Chromium/Firefox/Safari already installed:

```bash
npx playwright install                # all bundled browsers
npx playwright install chromium       # one
npx playwright install --with-deps    # also install Linux system libs
```

After upgrading the Playwright package, always re-fetch browsers:

```bash
npm install -D @playwright/test@latest
npx playwright install --with-deps
```

## Common Mistakes

- **Wrong**: Skipping `--with-deps` on Linux → **Right**: missing system libraries (libnss3, libatk-bridge, fonts) cause Chromium to fail with cryptic errors
- **Wrong**: Upgrading `@playwright/test` without re-running `playwright install` → **Right**: always re-fetch after upgrade; mismatched binaries produce "browser not found"
- **Wrong**: Putting Playwright at the repo root of a PHP project → **Right**: isolate under `tests/playwright/` to avoid polluting the root with `node_modules/`

## See Also

- [Config Walkthrough](pw-vr-config-walkthrough.md)
- [Drupal & DDEV](pw-vr-drupal-ddev.md)
- Reference: [Playwright Installation](https://playwright.dev/docs/intro)
