---
description: Reference for DaisyUI mockup components — browser, code terminal, phone, and application window frames
tldr: "Decorative device and UI frames for documentation, marketing, and onboarding screens where the UI itself is the content being shown. Always add `border border-base-300` — without it the frame has no visible edge."
---

# Mockup Components

## When to Use

> Use mockup components when presenting code snippets, browser previews, phone UI demonstrations, or application window mockups — typically in documentation, marketing, and onboarding screens where the UI itself is the content being shown.

## Decision

| Component | Class | Use for |
|-----------|-------|---------|
| Browser frame | `.mockup-browser` | Product screenshots and UI demos inside a browser chrome |
| Terminal / code block | `.mockup-code` | Command-line output and code snippets |
| Phone frame | `.mockup-phone` | Mobile UI previews inside a device silhouette |
| App window frame | `.mockup-window` | Desktop application screenshots without an address bar |

## Pattern

### .mockup-browser — Browser Window Frame

```html
<div class="mockup-browser border border-base-300 bg-base-100">
  <div class="mockup-browser-toolbar">
    <div class="input">https://example.com</div>
  </div>
  <div class="border-t border-base-300 px-4 py-8">
    <p>Content displayed inside the browser frame</p>
  </div>
</div>
```

`.mockup-browser-toolbar` contains the address bar — the `.input` child is a visual-only display (use a `<div>`, not an `<input>` element).

### .mockup-code — Code Block Terminal Frame

```html
<div class="mockup-code">
  <pre data-prefix="$"><code>npm install daisyui</code></pre>
  <pre data-prefix=">" class="text-success"><code>Installing...</code></pre>
  <pre data-prefix=">" class="text-warning"><code>Found deprecated peer</code></pre>
</div>
```

`data-prefix` sets the text shown before each line via `::before { content: attr(data-prefix) }`. Color modifiers (`text-success`, `text-error`) apply to the line text. DaisyUI does not provide syntax highlighting — integrate Prism.js or Shiki separately. Add `overflow-x-auto` to the wrapper for long lines.

### .mockup-phone — Mobile Phone Frame

```html
<div class="mockup-phone">
  <div class="mockup-phone-camera"></div>
  <div class="mockup-phone-display">
    <div class="artboard artboard-demo phone-1">
      <p>App content</p>
    </div>
  </div>
</div>
```

`.mockup-phone-camera` is the notch element — required for visual completeness. Use `.artboard` with size classes (`phone-1` through `phone-6`) to set standard phone screen dimensions. The phone frame is a fixed SVG-based shape — do not resize with Tailwind `w-*`/`h-*` utilities.

### .mockup-window — Application Window Frame

```html
<div class="mockup-window border border-base-300 bg-base-100">
  <div class="border-t border-base-300 px-4 py-8">
    Application content or screenshot here
  </div>
</div>
```

The window title bar (with colored dot controls) is rendered purely via CSS — no extra markup needed. Unlike `.mockup-browser`, there is no toolbar slot for custom content. The content area needs its own background.

## Common Mistakes

- **Wrong**: Using `<input>` element inside `.mockup-browser-toolbar` — **Right**: Use `<div class="input">` for the address bar; an `<input>` element triggers focus styles and keyboard interaction
- **Wrong**: Omitting `border border-base-300` on the wrapper — **Right**: Without it, the frame has no visible edge against the page background
- **Wrong**: Nesting mockups inside each other — **Right**: Each mockup is a standalone presentational element; nesting breaks visual proportions
- **Wrong**: Resizing `.mockup-phone` with Tailwind utilities — **Right**: The phone frame is SVG-based and cannot be freely resized without breaking the silhouette

## See Also

- [Data Display Components](data-display-components.md) — `.kbd` for inline keyboard key display in documentation
- [Feedback Components](feedback-components.md) — loading states inside mockup content
- Reference: https://daisyui.com/components/mockup-browser/
- Reference: https://daisyui.com/components/mockup-phone/
