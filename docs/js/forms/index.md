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
| Structure a form with correct semantics, labels, and grouping | [Form Structure & Semantics](form-structure-semantics.md) | Wrap all controls in <form>, use fieldset+legend for groups, always associate <label for> with <input id>. Never disable the submit button for validation — keyboard users cannot trigger invalid events. Use method="POST" for mutations. Labels above inputs, never placeholder-as-label. |
| Pick the right type, inputmode, and enterkeyhint for mobile keyboards | [Input Types & Modes](input-types-and-modes.md) | Use type="text" + inputmode="numeric" for card numbers and ZIP codes — never type="number" which strips leading zeros and adds spinners. Set enterkeyhint on every field in multi-step forms. Pattern performs a full match; allow spaces and international characters users naturally type. |
| Wire autocomplete tokens for address, payment, sign-in, sign-up | [Autocomplete & Autofill](autocomplete-and-autofill.md) | Add autocomplete to every input, select, and textarea. Autofill requires a stable name/id, a <form> wrapper, a submit button, and a recognised token. Use autocomplete="username" on sign-in email inputs so password managers link them to stored credentials. Never use autocomplete="off" on password fields. |
| Style fields that the browser has autofilled | [Autofill Visual Feedback](autofill-visual-feedback.md) | Use box-shadow inset to simulate background-color on autofilled inputs — background-color is blocked by the browser's security model. Always include :autofill:focus-visible with an explicit outline; never remove focus indicators from autofilled fields. Progressive enhancement — no Firefox support. |
| Show validation errors only after user interaction | [Native Validation](native-validation.md) | Use :user-invalid (not :invalid) so errors appear only after the user has interacted with a field. Bridge to AT with aria-invalid="true" via JS on blur and submit — :user-invalid is CSS-only and invisible to screen readers. Clear setCustomValidity() on the input event or the custom message sticks after correction. |
| Make inputs and textareas auto-grow to fit content | [Field Sizing](field-sizing.md) | Use field-sizing:content as progressive enhancement — Chrome/Edge 123+, Safari 26.2+, not Firefox. Set min-inline-size on inputs (prevents zero-width collapse when empty) and fixed width on textareas (prevents jarring horizontal shift). Override width:100% global CSS with width:auto. Feature-detect with @supports. |
| Style a select on-brand without building a JS widget | [Styling Native Select](styling-native-select.md) | appearance:base-select is Chrome/Edge 135+ only; degrades gracefully to OS native on other browsers. Apply to both the element AND ::picker(select) or the picker retains OS styling. Grid picker layouts do not give 2D keyboard navigation — Up/Down arrows only. Guard all animations with prefers-reduced-motion. |
| Embed icons or descriptions inside option elements | [Rich Media Input](rich-media-input.md) | Use appearance:base-select + HTML in <option> for icon-and-label options. Older browsers strip HTML tags and render only text nodes — always include meaningful plain text. Add aria-label to options whose rich HTML would read badly when concatenated. Mark decorative SVGs aria-hidden="true". |
