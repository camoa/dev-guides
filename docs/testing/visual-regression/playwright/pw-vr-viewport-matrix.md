---
description: "Capture VR screenshots at multiple viewport sizes using Playwright's project-per-viewport convention."
tldr: "Use one project per (browser × viewport) combination — the project name flows into the baseline filename, giving each tuple its own image. Never call `page.setViewportSize()` mid-test; it causes baseline filename collisions."
---

# Viewport & Device Matrix

## When to Use

> Use this when capturing the same component or page at multiple viewport sizes.

## Decision

| Approach | Correct | Why |
|---|---|---|
| One project per viewport | Yes | Project name in filename → each size gets its own baseline |
| `page.setViewportSize()` mid-test | No | Single filename, multiple captures → baselines collide |

## Pattern

### Viewport-per-project

```ts
projects: [
  { name: 'chromium-1440',
    use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } } },
  { name: 'chromium-768',
    use: { ...devices['Desktop Chrome'], viewport: { width: 768,  height: 1024 } } },
  { name: 'chromium-375',
    use: { ...devices['Desktop Chrome'], viewport: { width: 375,  height: 667 } } },
]
```

`viewport` must come **after** `...devices['Desktop Chrome']`; the device preset defines a viewport that would override yours.

### Device emulation (touch/mobile behavior)

```ts
projects: [
  { name: 'mobile-ios',     use: { ...devices['iPhone 13'] } },
  { name: 'mobile-android', use: { ...devices['Pixel 5'] } },
]
```

## `use` Keys for VR

| Key | Purpose |
|---|---|
| `viewport: { width, height }` | Fixed viewport size |
| `deviceScaleFactor` | High-DPI emulation (`2` for retina) |
| `isMobile` | Whether `<meta viewport>` and touch events are honored |
| `hasTouch` | Touch events |
| `userAgent` | UA string (preset devices use platform-specific UA; set `userAgent: undefined` to use the host UA) |
| `colorScheme` | `'light' \| 'dark' \| 'no-preference'` for `prefers-color-scheme` |
| `locale`, `timezoneId` | Localization |

## Common Mistakes

- **Wrong**: `viewport: { ... }` before `...devices['Desktop Chrome']` → **Right**: device preset overrides yours; spread device first
- **Wrong**: One project with multiple `setViewportSize` calls → **Right**: separate projects per viewport
- **Wrong**: Mobile project without `isMobile: true` → **Right**: captures desktop layout in a mobile-sized viewport

## See Also

- [Browser Projects](pw-vr-browser-projects.md)
- [Config Walkthrough](pw-vr-config-walkthrough.md)
- Reference: [Playwright Devices](https://playwright.dev/docs/emulation)
