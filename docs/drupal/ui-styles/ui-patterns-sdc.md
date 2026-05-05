---
description: Apply UI Styles to UI Patterns components and SDC instances in Layout Builder via prop slot integration.
tldr: Enable ui_styles_ui_patterns; pattern instances in Layout Builder gain UI Styles form fieldsets per exposed prop slot. Styles merge into the rendered Twig template's attributes. Component-internal markup not exposed as a styleable slot cannot be targeted — modify the Twig template instead.
drupal_version: "11.x"
---

# Integration: UI Patterns & SDC

## When to Use

> Use this guide when applying utility styles to UI Patterns components or SDC used in Layout Builder or via the UI Patterns module.

## Decision

| Component layer | Apply UI Styles? |
|---|---|
| Component root wrapper | Yes — for variant-style choices (size, theme, density) |
| Component internal slots | Yes if the pattern declares them as styleable prop slots |
| Component-internal markup not exposed as a slot | No — modify the SDC's Twig template instead |

## Pattern

Enable `ui_styles_ui_patterns`. Pattern/component instances in Layout Builder gain a UI Styles form per known prop slot — for example, separate fieldsets for the component root, the title, and the body.

Style application is wired through the pattern's prop schema; styles selected in the form are merged into the rendered Twig template's `attributes`.

## Common Mistakes

- **Trying to override component-internal markup with UI Styles** → If the slot isn't exposed by the pattern's declaration, no UI exists. Add a styleable prop to the pattern, or theme the component

## See Also

- [Integration: Layout Builder](layout-builder.md)
- [drupal/ui-patterns](../ui-patterns/index.md)
- [drupal/sdc](../sdc/index.md)
- Reference: `modules/ui_styles_ui_patterns/` in the UI Styles module
