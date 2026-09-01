---
description: Storybook and component story tooling for Drupal SDC themes — UI Patterns 2 story.yml (static, no Node.js, any theme) vs Storybook.js tools (interactive Controls)
drupal_version: "11.x"
tracks:
  - project: storybook
    channel: stable
    declared: "1.0.4"
    verified: 2026-08-16
guide-meta:
  concepts:
    - stories.yml
    - Storybook.js
    - component preview
    - interactive controls
    - SDC stories
  not:
    - story.yml
    - UI Patterns
    - prop definitions
    - source plugins
  requires:
    - drupal/sdc
  complements:
    - drupal/ui-patterns
  category: drupal
---

# Drupal Storybook & Stories

Component story tooling for Drupal SDC themes. The key decision: UI Patterns 2 `.story.yml` gives you static variant browsing with zero Node.js setup — available on **any theme** with the `ui_patterns` module, not just UI Suite DaisyUI. Storybook.js tools add interactive Controls — live prop manipulation in the browser — at the cost of Node.js setup.

## Guides

- [Tool Landscape & Decision](storybook-landscape.md) — which tool for which context, static vs interactive
- [UI Patterns 2 .story.yml Format](story-yml-format.md) — complete schema, all slot value types, verbatim examples
- [drupal/storybook Module](drupal-storybook-module.md) — Twig stories with interactive Controls and full Drupal fidelity
- [storybook-addon-sdc (Offline)](addon-sdc-offline.md) — decoupled development without Drupal
- [DDEV + Storybook Setup](ddev-storybook-setup.md) — port exposure, addon, workflow
- [Sub-Theme Stories](subtheme-stories.md) — override and extend base theme stories
