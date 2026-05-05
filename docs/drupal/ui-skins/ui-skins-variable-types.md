---
description: Choosing the form widget for a CSS variable — color picker, textfield, or custom element.
tldr: Use `ui_skins_alpha_color` for color tokens (stores 8-char hex with alpha), `textfield` for numeric/unit/arbitrary CSS values, or a custom form element plugin for specialized inputs. Mixing up type and value format silently breaks CSS.
drupal_version: "11.x"
---

# Variable Types & Widgets

## When to Use

> Use this when choosing the form widget for a CSS variable based on the value's nature.

## Decision

| Value nature | `type` | Widget |
|---|---|---|
| Color (with optional alpha) | `ui_skins_alpha_color` | Color picker with alpha slider; stores 8-char hex |
| Numeric / unit / arbitrary string | `textfield` | Plain text input — site builder responsible for valid CSS |
| Custom (file picker, select, etc.) | Your own form element plugin | Register a custom form element |

## Pattern

UI Skins uses Drupal's standard form-element plugin system. To add a custom widget type, register a class with `'#type' => 'my_custom_widget'` and reference it in the variable definition's `type` field.

## Common Mistakes

- **Using `textfield` for colors** → Site builders enter invalid hex codes; CSS silently breaks. Use `ui_skins_alpha_color`
- **Expecting input validation for arbitrary CSS values** → `textfield` does no validation. If the value must be a valid CSS length, validate in a custom widget

## See Also

- [CSS Variable Definition](ui-skins-css-variable-definition.md)
- Reference: `src/Element/AlphaColor.php`
