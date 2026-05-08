---
description: Achieve consistent Playwright screenshots across local and CI by using the official Docker image and pinned versions.
tldr: Always capture baselines inside the same Docker image that runs in CI. Pin `@playwright/test` and the Docker tag to the same version number. Never capture on macOS and compare in Linux — antialiasing differs every time.
---

# Determinism Across Environments

## When to Use

> Use this when screenshots pass locally but fail in CI, or when setting up a project to avoid local-vs-CI drift from the start.

## The Core Rule

Playwright's own docs: *"Browser rendering can vary based on the host OS, version, settings, hardware, power source, headless mode, and other factors. Run tests in the same environment where the baselines were generated."*

## Decision

| Scenario | Right approach |
|---|---|
| New project | Capture baselines inside Docker from day one |
| macOS dev, Linux CI | Run `--update-snapshots` inside the Docker container |
| Which platform is "truth"? | `linux` — CI runs there; `*-linux.png` are the canonical baselines |

## Pattern

### Official Docker image

```bash
docker pull mcr.microsoft.com/playwright:v1.59.1-noble
```

Tag taxonomy:
- `v1.X.Y-noble` — Ubuntu 24.04 LTS (current default)
- `v1.X.Y-jammy` — Ubuntu 22.04 LTS

Recommended flags: `--init`, `--ipc=host`

### Pin everything

```json
"devDependencies": { "@playwright/test": "1.59.1" }
```

Pin the Docker tag to the same version. Never use `:latest`.

### Capture baselines inside Docker

```bash
docker run --rm \
  --ipc=host \
  -v $(pwd):/work -w /work \
  --add-host=mysite.ddev.site:host-gateway \
  mcr.microsoft.com/playwright:v1.59.1-noble \
  npx playwright test --update-snapshots
```

## Common Mistakes

- **Wrong**: `mcr.microsoft.com/playwright:latest` → **Right**: pin the tag; `:latest` changes with every release
- **Wrong**: Capturing on macOS, comparing in CI → **Right**: antialiasing differs; always use the same Docker image
- **Wrong**: Custom Dockerfile without `--with-deps` → **Right**: missing fonts and system libs produce rendering differences

## See Also

- [Browser Projects](pw-vr-browser-projects.md)
- [Drupal & DDEV](pw-vr-drupal-ddev.md)
- Reference: [Playwright Docker](https://playwright.dev/docs/docker)
