---
description: Decision guide for choosing between UI Patterns 2 story.yml, drupal/storybook module, storybook-addon-sdc, and sdc_styleguide
drupal_version: "11.x"
---

# Storybook Tool Landscape & Decision

## When to Use

> Use UI Patterns 2 `.story.yml` when you're on a UI Suite DaisyUI / UI Patterns 2 theme — no Node.js required. Use `drupal/storybook` module when you need Storybook.js with real Drupal Twig rendering. Use `storybook-addon-sdc` when you need offline/CI component previews without a running Drupal instance.

## Critical Clarification: Two Independent Story Systems

UI Suite DaisyUI already uses `.story.yml` stories on every component. These work WITHOUT the `drupal/storybook` module. They use UI Patterns 2's story format — a YAML-based story system completely independent of Storybook.js.

| Story system | Format | Requires Storybook.js? | Requires Drupal running? |
|---|---|---|---|
| UI Patterns 2 | `.story.yml` files | No | No — built-in pattern library |
| `drupal/storybook` module | `{% stories %}` / `{% story %}` Twig tags | Yes (v10+) | Yes — server-rendered |

These two systems do not interact and can coexist.

## Decision

| Tool | Version (2025) | When to Use | Requires Drupal? | Node.js? |
|---|---|---|---|---|
| **UI Patterns 2 `.story.yml`** | Part of `ui_patterns` 2.x | UI Suite DaisyUI theme, any UI Patterns 2 component | No — built-in styleguide at `/admin/appearance/ui/components` | No |
| **`drupal/storybook` module** | 1.0.2 | Custom Twig components needing real Drupal data, Radix-based themes | Yes — server-rendered | Yes (Storybook.js v10+) |
| **`storybook-addon-sdc`** | 0.21.2 | Offline development, CI/CD, decoupled preview | No — decoupled | Yes (Vite + Twig.js) |
| **`sdc_styleguide`** | N/A | Simple Drupal-native browser, no Node.js setup | Yes | No |

### Deprecated Tools — Do Not Use

| Tool | Status | Reason |
|---|---|---|
| `cl_server` | Deprecated | Superseded by `drupal/storybook` module as of Storybook 8+ |
| `sdc_story_generator` | Deprecated | CLI-based generator replaced by native story format |

Storybook.js is currently at **v10.2** (ESM-only since v9 — the old CJS config format no longer works).

## Pattern

```
UI Suite DaisyUI site:
  components/alert/alert.default.story.yml  ← already here, no extra setup
  ↓
  /admin/appearance/ui/components           ← browse in Drupal

Custom Twig theme + full Drupal fidelity:
  drupal/storybook module + Storybook.js v10
  → stories/*.stories.twig (server-rendered via running Drupal)

Offline / decoupled / CI:
  storybook-addon-sdc + Vite + Twig.js
  → .component.yml thirdPartySettings.sdcStorybook
```

## Common Mistakes

- **Wrong**: Installing `drupal/storybook` on a UI Suite DaisyUI theme to browse `.story.yml` stories → **Right**: Use `sdc_styleguide` or the built-in UI Patterns library at `/admin/appearance/ui/components`
- **Wrong**: Using `cl_server` or `sdc_story_generator` → **Right**: These are deprecated; use `drupal/storybook` module or `storybook-addon-sdc`
- **Wrong**: Storybook config with `module.exports = {}` on v9+ → **Right**: ESM-only since v9 — use `export default {}`
- **Wrong**: Conflating "Storybook" (the JS tool) with "stories" (the YAML concept in UI Patterns 2) → **Right**: These are independent naming coincidences

## See Also

- [UI Patterns 2 .story.yml Format](story-yml-format.md)
- [drupal/storybook Module](drupal-storybook-module.md)
- [storybook-addon-sdc (Offline)](addon-sdc-offline.md)
- Reference: `drupal-ui-suite-daisyui.md` — base theme component catalog
- Reference: `drupal-ui-patterns.md` — UI Patterns 2 full documentation
