---
description: Decision guide — UI Patterns 2 story.yml (static browsing, no Node.js, any theme with ui_patterns module) vs Storybook.js tools (interactive Controls) — choose based on whether you need live prop manipulation
drupal_version: "11.x"
---

# Storybook Tool Landscape & Decision

## When to Use

> Use UI Patterns 2 `.story.yml` when you need static variant browsing with zero Node.js setup — works on any theme with the `ui_patterns` module. Use Storybook.js tools (`drupal/storybook` or `storybook-addon-sdc`) when you need interactive Controls — live prop manipulation in the browser.

## Decision

### Critical Clarification: Two Independent Story Systems

**UI Suite DaisyUI already uses `.story.yml` stories on every component.** These work WITHOUT the `drupal/storybook` module. They use UI Patterns 2's story format — a YAML-based story system completely independent of Storybook.js. The same is true for any theme with UI Patterns 2 module installed — `.story.yml` is a module feature, not a DaisyUI feature.

| Story system | Format | Requires Storybook.js? | Requires Drupal running? |
|---|---|---|---|
| UI Patterns 2 | `.story.yml` files | No | No — built-in pattern library |
| `drupal/storybook` module | `{% stories %}` / `{% story %}` Twig tags | Yes (v10+) | Yes — server-rendered |

These two systems do not interact and can coexist.

### The Key Capability Difference: Static vs Interactive

**UI Patterns 2 pattern library is static browsing.** You define variants in YAML and the browser shows exactly those — nothing more. You cannot change a prop value without editing the `.story.yml` file.

**Storybook Controls are interactive.** The Controls panel lets you type new text, toggle booleans, pick from enums, change colors — live, in the browser, without touching code.

| Need | Right tool |
|---|---|
| Developers browsing and verifying defined component variants | UI Patterns 2 pattern library — sufficient, zero Node.js setup |
| Any theme with UI Patterns 2 module (not just DaisyUI) | UI Patterns 2 pattern library — works for all SDC components |
| Designers or clients exploring "what if I change this prop" | Storybook.js (`drupal/storybook` or `storybook-addon-sdc`) |
| QA checking all defined states | UI Patterns 2 pattern library — sufficient |
| Design system handoff where non-devs tweak component values | Storybook.js — interactive Controls panel |

Most Drupal projects don't need interactive controls — developers know the props and designers work from Figma. The setup cost of Storybook is only justified when non-developers need to explore component behavior directly.

### All Active Tools

| Tool | Version (2025) | When to Use | Requires Drupal? | Node.js? |
|---|---|---|---|---|
| **UI Patterns 2 `.story.yml`** | Part of `ui_patterns` 2.x | Any theme with UI Patterns 2 module — static variant browsing, zero Node.js | No — built-in styleguide at `/admin/appearance/ui/components` | No |
| **`drupal/storybook` module** | 1.0.2 | Interactive Controls, real Drupal Twig rendering, design system handoff | Yes — server-rendered | Yes (Storybook.js v10+) |
| **`storybook-addon-sdc`** | 0.21.2 | Interactive Controls offline, CI/CD, decoupled preview | No — decoupled | Yes (Vite + Twig.js) |
| **`sdc_styleguide`** | N/A | Simple Drupal-native browser, no Node.js, no Controls | Yes | No |

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

- **Wrong**: Assuming UI Suite DaisyUI `.story.yml` requires the `drupal/storybook` module → **Right**: Completely separate systems. `.story.yml` is a UI Patterns 2 module feature available to any SDC theme.
- **Wrong**: Installing `drupal/storybook` just to browse existing component variants → **Right**: UI Patterns 2 pattern library at `/admin/appearance/ui/components` already does this with zero Node.js setup.
- **Wrong**: Installing Storybook for interactive controls when the team only needs to browse variants → **Right**: The setup cost (Node.js, CORS, Twig cache config) is only justified when you need live prop manipulation.
- **Wrong**: Using `cl_server` or `sdc_story_generator` → **Right**: Both deprecated, do not use.
- **Wrong**: Installing Storybook v8+ with the old CJS config format (`module.exports = {}`) → **Right**: ESM-only since v9 (`export default {}`).
- **Wrong**: Conflating "Storybook" (the JavaScript tool) with "stories" (the YAML concept in UI Patterns 2) → **Right**: Two independent concepts.

## See Also

- [UI Patterns 2 .story.yml Format](story-yml-format.md)
- Reference: `drupal-ui-suite-daisyui.md` — base theme component catalog
- Reference: `drupal-ui-patterns.md` — UI Patterns 2 full documentation
