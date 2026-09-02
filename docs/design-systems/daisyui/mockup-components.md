---
description: Reference for DaisyUI mockup components — browser, code terminal, phone, and application window frames
tldr: "Decorative device and UI frames for documentation, marketing, and onboarding screens where the UI itself is the content being shown. Always add `border border-base-300` — without it the frame has no visible edge."
---

# Mockup Components

## When to Use

> Presenting code snippets, browser previews, phone UI demonstrations, and application window mockups — typically in documentation, marketing, and onboarding screens where the UI itself is the content being shown.

## Decision: Which Mockup Frame

| Component | Class | Use for |
|-----------|-------|---------|
| Browser frame | `.mockup-browser` | Product screenshots and UI demos inside a browser chrome |
| Terminal / code block | `.mockup-code` | Command-line output and code snippets |
| Phone frame | `.mockup-phone` | Mobile UI previews inside a device silhouette |
| App window frame | `.mockup-window` | Desktop application screenshots without an address bar |

## .mockup-browser — Browser Window Frame

**Description:** A decorative browser chrome frame (address bar, window controls) for wrapping content. Used for product screenshots and UI demos.

**Required structure:**

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

**Gotchas:**

- `.mockup-browser-toolbar` contains the address bar — the `.input` child inside it renders as the URL bar (no need for `<input>` element; it's a visual-only display)
- The toolbar has fixed styling — do not add padding/margin utilities directly to `.mockup-browser-toolbar`; it will break the dot controls layout
- Background color on the wrapper (`bg-base-100`) does NOT apply inside the content area automatically — set background on the content `<div>` separately

## .mockup-code — Code Block Terminal Frame

**Description:** Renders content as a styled terminal/code block with a dark background and colored line numbers. Used in documentation and tutorials.

**Required structure:**

```html
<div class="mockup-code">
  <pre data-prefix="$"><code>npm install daisyui</code></pre>
  <pre data-prefix=">" class="text-success"><code>Installing...</code></pre>
  <pre data-prefix=">" class="text-warning"><code>Found deprecated peer</code></pre>
</div>
```

**Gotchas:**

- `data-prefix` sets the text shown before each line (e.g., `$`, `>`, line numbers). It is rendered via CSS `::before { content: attr(data-prefix) }`
- Color modifiers (`text-success`, `text-error`) apply to the line text — useful for simulating terminal output
- Content inside `<code>` is not syntax-highlighted by DaisyUI — integrate a syntax highlighting library (Prism.js, Shiki) separately
- Long lines do not wrap by default — add `overflow-x-auto` to the `.mockup-code` wrapper for horizontal scroll

## .mockup-phone — Mobile Phone Frame

**Description:** A decorative phone device frame for wrapping mobile UI previews.

**Required structure:**

```html
<div class="mockup-phone">
  <div class="mockup-phone-camera"></div>
  <div class="mockup-phone-display">
    <div class="artboard artboard-demo phone-1">
      <!-- Mobile content goes here -->
      <p>App content</p>
    </div>
  </div>
</div>
```

**Gotchas:**

- `.mockup-phone-camera` is the notch element — required for visual completeness; omitting it breaks the phone silhouette
- Use `.artboard` with size classes (`phone-1` through `phone-6`) to set standard phone screen dimensions inside `.mockup-phone-display`
- The phone frame is a fixed SVG-based shape — it cannot be resized via Tailwind width/height utilities without breaking the frame

## .mockup-window — Application Window Frame

**Description:** A decorative macOS/desktop application window frame with traffic-light window controls. Lighter than `.mockup-browser` — no address bar.

**Required structure:**

```html
<div class="mockup-window border border-base-300 bg-base-100">
  <div class="border-t border-base-300 px-4 py-8">
    Application content or screenshot here
  </div>
</div>
```

**Gotchas:**

- The window title bar (with colored dots) is rendered purely via CSS — no extra markup needed beyond the wrapper
- Content area needs its own background — `bg-base-100` on the wrapper sets the title bar background, not the content area
- Unlike `.mockup-browser`, there is no toolbar slot — if you need a custom title, add it inside the content area

## Common Mistakes

- Using `<input>` element inside `.mockup-browser-toolbar` — the `.input` class on a `<div>` is sufficient; an actual `<input>` element triggers focus styles and keyboard interaction
- Forgetting `border border-base-300` on the mockup wrappers — without it, the frame has no visible border against the page background
- Nesting mockups inside each other — each mockup is a standalone presentational element; nesting breaks the visual proportions

## See Also

- [Data Display Components](data-display-components.md) — `.kbd` for inline keyboard key display in documentation
- [Feedback Components](feedback-components.md) — feedback components for loading states inside mockup content
- Reference: https://daisyui.com/components/mockup-browser/
- Reference: https://daisyui.com/components/mockup-phone/
