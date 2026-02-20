---
description: Complete reference of all 28 DaisyUI v5 CSS variables
---

# DaisyUI CSS Variable Reference

## When to Use

> Use this when you need to know every CSS variable that DaisyUI v5 provides. This is the complete reference for theming.

## Decision

**Color Variables (20 total)**

| CSS Variable | Category | Description |
|---|---|---|
| --color-primary | Brand | Main brand / action color |
| --color-primary-content | Brand | Text/icon color on primary background |
| --color-secondary | Brand | Supporting brand color |
| --color-secondary-content | Brand | Text/icon color on secondary background |
| --color-accent | Brand | Highlight / emphasis color |
| --color-accent-content | Brand | Text/icon color on accent background |
| --color-neutral | Neutral | Dark neutral for contrast areas |
| --color-neutral-content | Neutral | Text/icon color on neutral background |
| --color-base-100 | Base | Page background (lightest) |
| --color-base-200 | Base | Slightly darker shade (cards, inputs) |
| --color-base-300 | Base | Even darker shade (borders, dividers) |
| --color-base-content | Base | Default text color on base backgrounds |
| --color-info | Feedback | Informational state color |
| --color-info-content | Feedback | Text on info background |
| --color-success | Feedback | Positive state color |
| --color-success-content | Feedback | Text on success background |
| --color-warning | Feedback | Caution state color |
| --color-warning-content | Feedback | Text on warning background |
| --color-error | Feedback | Error / destructive state color |
| --color-error-content | Feedback | Text on error background |

**Shape Variables (3 total)**

| CSS Variable | Category | Description | Components |
|---|---|---|---|
| --radius-selector | Border radius | Small selectors | Checkbox, toggle, badge, radio |
| --radius-field | Border radius | Input fields | Input, select, textarea, tab, button |
| --radius-box | Border radius | Large containers | Card, modal, alert, drawer, dropdown |

**Size Variables (2 total)**

| CSS Variable | Category | Description | Components |
|---|---|---|---|
| --size-selector | Scale | Base size for small selectors | Checkbox, toggle, radio, badge |
| --size-field | Scale | Base size for input fields | Input, select, textarea, tab, button |

**Other Variables (3 total)**

| CSS Variable | Category | Description | Values |
|---|---|---|---|
| --border | Border | Border width for all components | e.g. 1px, 2px |
| --depth | Effects | Adds 3D depth effect (box-shadow) | 0 (off) or 1 (on) |
| --noise | Effects | Adds background noise texture | 0 (off) or 1 (on) |

**Total: 28 CSS variables** that fully define a DaisyUI theme.

## Pattern

**Drupal Integration**

UI Suite DaisyUI exposes all 28 variables via ui_suite_daisyui.ui_skins.css_variables.yml, allowing site builders to override them through the Drupal admin UI. The theme applies them via data-theme attribute on html.

## See Also

- [DaisyUI v5 Color Token System](daisyui-v5-color-token-system.md)
- [Custom DaisyUI Theme Definition](custom-daisyui-theme-definition.md)
- [UI Suite DaisyUI Starterkit Patterns](ui-suite-daisyui-starterkit-patterns.md)
- Reference: https://daisyui.com/docs/colors/
