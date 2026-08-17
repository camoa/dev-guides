---
description: HTML Forms — modern, accessible, autofill-ready form patterns covering structure, input types, autocomplete tokens, native validation, field sizing, and styled selects.
tracks: []
guide-meta:
  concepts:
    - HTML forms
    - autocomplete
    - autofill
    - autocomplete tokens
    - form validation
    - Constraint Validation API
    - :user-invalid
    - :user-valid
    - setCustomValidity
    - field-sizing content
    - appearance base-select
    - customizable select
    - selectedcontent
    - accent-color
    - inputmode
    - enterkeyhint
    - autofill visual feedback
    - :autofill
    - rich media select options
  not:
    - Drupal Form API
    - React forms (Formik, React Hook Form)
    - Django / Rails form helpers
  requires: []
  complements:
    - js/interaction-craft
    - css/modern-css
    - js/passkeys
  specializes: ""
  category: js
---

# HTML Forms

Modern, accessible, autofill-ready form patterns using the full web platform — no library dependencies.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Structure a form with correct semantics, labels, and grouping | [Form Structure & Semantics](form-structure-semantics.md) | Wrap all controls in form, use fieldset+legend for groups, always associate label for with input id. Never disable the submit button for validation — keyboard users cannot trigger invalid events. |
| Pick the right type, inputmode, and enterkeyhint for mobile keyboards | [Input Types & Modes](input-types-and-modes.md) | Use type="text" + inputmode="numeric" for card numbers and ZIP codes — never type="number" which strips leading zeros. Set enterkeyhint on every field in multi-step forms. |
| Wire autocomplete tokens for address, payment, sign-in, sign-up | [Autocomplete & Autofill](autocomplete-and-autofill.md) | Add autocomplete to every input, select, and textarea. Use autocomplete="username" on sign-in email inputs. Never use autocomplete="off" on password fields. |
| Style fields that the browser has autofilled | [Autofill Visual Feedback](autofill-visual-feedback.md) | Use box-shadow inset to simulate background-color — background-color is blocked by the browser's security model. Always include :autofill:focus-visible with an explicit outline. |
| Show validation errors only after user interaction | [Native Validation](native-validation.md) | Use :user-invalid (not :invalid) so errors appear only after the user interacts. Bridge to AT with aria-invalid="true" via JS on blur and submit — :user-invalid is CSS-only and invisible to screen readers. |
| Make inputs and textareas auto-grow to fit content | [Field Sizing](field-sizing.md) | Use field-sizing:content as progressive enhancement — Chrome/Edge 123+, Safari 26.2+, not Firefox. Set min-inline-size on inputs; fixed width on textareas. Feature-detect with @supports. |
| Style a select on-brand without building a JS widget | [Styling Native Select](styling-native-select.md) | appearance:base-select is Chrome/Edge 135+ only; degrades gracefully. Apply to both the element AND ::picker(select). Grid layouts do not give 2D keyboard navigation. |
| Embed icons or descriptions inside option elements | [Rich Media Input](rich-media-input.md) | Use appearance:base-select + HTML in option. Older browsers render text nodes only — always include meaningful plain text. Add aria-label to options with complex rich content. |
