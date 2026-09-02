---
description: Reference for DaisyUI form input components — input, fieldset, select, textarea, checkbox, toggle, range, rating, file-input, floating-label, validator, calendar, and filter
tldr: "Form elements: text fields, selections, toggles, form structure, file pickers, floating labels, and CSS-driven validation display. Replace v4's `form-control` with `fieldset`. Use `.validator` only with native HTML validation attributes."
---

# Data Input Components

## When to Use

> Form elements: text fields, selections, toggles, and form structure.

## Decision: Which Input Component

| Component | Class | Use for |
|-----------|-------|---------|
| Text input | `.input` | Single-line text, email, search |
| Form group | `.fieldset` | Label + input + help text grouping (v5) |
| Select | `.select` | Dropdown selection |
| Multi-line | `.textarea` | Long-form text |
| Boolean | `.checkbox` | True/false selection |
| On/off | `.toggle` | Styled boolean switch |
| Radio | `.radio` | Single-select from group |
| Range | `.range` | Numeric slider |
| Rating | `.rating` | Star rating input |
| File picker | `.file-input` | Styled file upload field |
| Animated label | `.floating-label` | Placeholder-style label that animates on focus (v5) |
| CSS validation | `.validator` | Show/hide hints using native `:valid`/`:invalid` state |
| Calendar styling | `.calendar` | Skin for third-party datepicker libraries |
| Filter chips | `.filter` | Radio/checkbox inputs styled as selectable pill chips |

## .input — Text Input

**Modifiers:** `input-primary` through `input-error` (border color on focus) + `input-ghost` + sizes `input-xs` through `input-xl`

```html
<!-- Wrapper pattern (supports prefix/suffix icons) -->
<label class="input input-primary flex items-center gap-2">
  <svg .../><!-- prefix icon -->
  <input type="text" class="grow" placeholder="Search" />
</label>

<!-- Direct input (simpler) -->
<input type="text" class="input w-full" placeholder="Email" />
```

**Gotchas:**

- v5 changed the primary pattern to a wrapper `<label class="input">` containing `<input>` — this enables icon prefix/suffix without extra CSS
- `input-bordered` is no longer in v5 — borders are now default. Use `input-ghost` to remove them
- Mobile iOS: DaisyUI adds `font-size: max(0.875rem, 1rem)` on focus on coarse-pointer devices to prevent iOS zoom on small inputs

## .fieldset — Form Group Container

**v5 addition.** Groups label, input, and help text:

```html
<fieldset class="fieldset">
  <legend class="fieldset-legend">Account Details</legend>

  <label class="fieldset-label">Email</label>
  <input type="email" class="input w-full" placeholder="you@example.com" />
  <p class="fieldset-label text-error">Enter a valid email address</p>
</fieldset>
```

**Gotchas:** `.fieldset` replaces the old `form-control` class from v4. Do not use `form-control` in v5.

## .select — Select Dropdown

Same modifier pattern as `.input`: `select-primary` through `select-error` + `select-ghost` + sizes.

```html
<label class="select">
  <select>
    <option disabled selected>Pick a color</option>
    <option>Red</option>
    <option>Blue</option>
  </select>
</label>
```

## .textarea — Text Area

Same modifier pattern. No fixed height by default — use Tailwind `min-h-*` or `rows` attribute.

```html
<textarea class="textarea textarea-primary w-full" placeholder="Message" rows="4"></textarea>
```

## .checkbox — Checkbox

```html
<input type="checkbox" class="checkbox checkbox-primary" />
<input type="checkbox" class="checkbox checkbox-success checkbox-lg" checked />
```

**Modifiers:** semantic colors + sizes `checkbox-xs` through `checkbox-xl`

**Gotchas:** DaisyUI checkbox uses CSS `::before` for the checkmark animation — the native appearance is suppressed via `appearance: none`. This means browser built-in checkbox styling is completely replaced, including high-contrast mode (handled via forced-colors media query in the CSS).

## .radio — Radio Button

Same modifier pattern as checkbox. Always wrap related radios with a `<fieldset>` and provide `<legend>`.

```html
<input type="radio" name="plan" class="radio radio-primary" />
```

## .toggle — Toggle Switch

```html
<input type="checkbox" class="toggle toggle-primary" />
<input type="checkbox" class="toggle toggle-success toggle-lg" checked />
```

The toggle is a styled `<input type="checkbox">` — same semantics, different visual.

## .range — Range Slider

```html
<input type="range" min="0" max="100" value="40" class="range range-primary" />
```

## .rating — Star Rating

```html
<div class="rating rating-lg">
  <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" aria-label="1 star" />
  <input type="radio" name="rating-1" class="mask mask-star-2 bg-orange-400" checked aria-label="2 stars" />
  <!-- etc -->
</div>
```

**Gotchas:** Rating uses radio inputs with the `.mask` utility to clip to star shape. Requires `aria-label` on each input for accessibility.

## .file-input — File Upload Input

**Description:** Styled file picker input. Follows the same modifier pattern as `.input`.

**Modifiers:** `file-input-primary` through `file-input-error` + sizes `file-input-xs` through `file-input-xl`

```html
<label class="form-control w-full max-w-xs">
  <div class="label"><span class="label-text">Pick a file</span></div>
  <input type="file" class="file-input file-input-primary w-full" />
</label>

<!-- Ghost variant (minimal border) -->
<input type="file" class="file-input file-input-ghost w-full" />
```

**Gotchas:**

- The browser's native file picker UI is not replaceable — DaisyUI only styles the surrounding element
- On Safari/iOS, the "Choose File" button text is browser-controlled and cannot be changed via CSS
- Always pair with a `<label>` for accessibility — `<input type="file">` without an accessible label is non-compliant

## .label — Form Label with Floating Variant

**Description:** Wrapper for form field labels. v5 supports floating labels (placeholder-style labels that animate on focus).

**Required structure — Standard label:**

```html
<fieldset class="fieldset">
  <label class="fieldset-label">Email address</label>
  <input type="email" class="input w-full" />
</fieldset>
```

**Required structure — Floating label:**

```html
<label class="floating-label">
  <span>Email address</span>
  <input type="email" class="input" placeholder="Email address" />
</label>
```

**Gotchas:**

- Floating labels require the `placeholder` attribute to be set to the same text as the label — the placeholder is used to detect the empty state via CSS `:placeholder-shown`
- `floating-label` is a v5 addition — not available in v4
- For error state text, use a second `<span class="fieldset-label text-error">` after the input, not inside the floating label wrapper

## .validator — Inline Validation Display

**Description:** Validates input values and shows contextual success/error messages without JavaScript. Uses CSS `:valid` / `:invalid` pseudo-classes on the native input.

**Required structure:**

```html
<input
  type="email"
  class="input validator"
  required
  placeholder="user@example.com"
/>
<p class="validator-hint">Must be a valid email address</p>
```

**With fieldset:**

```html
<fieldset class="fieldset">
  <label class="fieldset-label">Email</label>
  <input type="email" class="input validator w-full" required />
  <p class="validator-hint">Enter a valid email address</p>
</fieldset>
```

**Gotchas:**

- `.validator` relies on **native HTML validation** — the input must have `required`, `type="email"`, `pattern`, `min`/`max`, or other native validation attributes. Without them, `:valid`/`:invalid` never trigger
- Validation state only shows **after the user interacts** with the field (`:user-invalid` in modern browsers) — the error does not display on initial page load
- `.validator-hint` is hidden by default and shown only on `:invalid` state — the text should describe the validation rule, not the error
- For custom validation logic (e.g., async username availability), `.validator` cannot help — use JS to add/remove error classes manually

## .calendar — Calendar Date Picker Styling

**Description:** CSS styles for third-party calendar/datepicker libraries. DaisyUI provides the visual theme; the calendar interaction logic must come from a JS library (e.g., Pikaday, Cally web component).

**Note:** `.calendar` is a styling skin, not a standalone component. It does not ship with calendar logic.

**Recommended pairing — Cally web component:**

```html
<!-- Install: npm install cally -->
<script type="module" src="node_modules/cally/src/index.js"></script>

<calendar-date class="calendar">
  <svg slot="previous"><!-- left arrow icon --></svg>
  <svg slot="next"><!-- right arrow icon --></svg>
</calendar-date>
```

**Gotchas:**

- Without a JS library, `.calendar` renders nothing meaningful — the component is a CSS skin only
- DaisyUI's calendar CSS targets Cally web component element selectors — compatibility with other datepicker libraries is not guaranteed
- Theme colors apply automatically via CSS variable inheritance — no extra config needed

## .filter — Toggleable Filter Chips

**Description:** A group of radio or checkbox inputs styled as filter chips/pills. CSS-only selection state management.

**Required structure:**

```html
<div class="filter">
  <input class="btn filter-reset" type="radio" name="category" aria-label="All" checked />
  <input class="btn btn-sm" type="radio" name="category" aria-label="Electronics" />
  <input class="btn btn-sm" type="radio" name="category" aria-label="Clothing" />
  <input class="btn btn-sm" type="radio" name="category" aria-label="Books" />
</div>
```

**Gotchas:**

- Filter chip labels come from `aria-label` attribute — DaisyUI renders them via CSS `content: attr(aria-label)`, so `aria-label` is both the visible text and the accessible label
- `filter-reset` styles the "All" / reset option distinctly — include one reset chip at the start
- Use `type="radio"` for single-select filters, `type="checkbox"` for multi-select
- For filtering actual content, add JavaScript to listen for change events and filter DOM elements — DaisyUI provides no filtering logic

## Common Mistakes

- Using old `form-control` wrapper class (v4) in v5 projects — replaced by `fieldset`
- Not providing `<label>` or `aria-label` for checkbox/radio/toggle — these are `<input>` elements; screen readers need explicit labels
- Setting `input-bordered` in v5 — this class no longer exists; borders are on by default
- Using `.validator` without native HTML validation attributes — no `required`/`type`/`pattern` means `:invalid` never fires

## See Also

- [Customization Patterns](customization-patterns.md)
- [Security and Accessibility](security-accessibility.md)
- Reference: `react-design-system.md` Section 8 — react-hook-form integration
- Reference: `node_modules/daisyui/components/input/object.js`
- Reference: `node_modules/daisyui/components/fieldset/object.js`
