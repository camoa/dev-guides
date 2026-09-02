---
description: DaisyUI best practices and anti-patterns — when to use component classes vs Tailwind utilities, performance, and team conventions
tldr: "Code review, architecture decisions, and onboarding guidance for DaisyUI projects."
---

# Best Practices

## When to Use

> Code review, architecture decisions, and onboarding guidance for DaisyUI projects.

## When DaisyUI Classes Beat Raw Utilities

Use DaisyUI component classes when:

- **You want multi-theme support** — one `btn btn-primary` automatically adapts to all 35 themes; raw Tailwind `bg-blue-600` does not
- **Interactive states are complex** — `.btn` handles hover, focus-visible, active, disabled, and even print styles. Recreating this in utilities is dozens of lines
- **Consistency matters more than control** — DaisyUI's visual language is deliberately consistent. Teams spend less time debating border-radius, padding, and typography

Use raw Tailwind utilities when:

- **Layout and spacing** — `mt-4 px-6 grid grid-cols-2` — DaisyUI has no layout utilities
- **One-off customization** — DaisyUI classes define the component; utilities add project-specific adjustments
- **Override a DaisyUI default** — `card w-full` where `w-full` is the override

```html
<!-- RIGHT — adapts to all 35 themes automatically -->
<button class="btn btn-primary">Submit</button>
<div class="bg-base-100 text-base-content">Content</div>

<!-- Tailwind for layout, DaisyUI for semantics -->
<button class="btn btn-primary mt-4 w-full max-w-xs">Submit</button>
```

## Anti-Pattern: Using `@apply` for DaisyUI Component Classes

```css
/* WRONG — this inlines the CSS at build time */
.my-button { @apply btn btn-primary; }

/* Why it's wrong: .my-button can't be combined with btn-ghost, btn-outline etc.
   The component modifiers no longer work because the CSS has been extracted */
```

```html
<!-- RIGHT — use the class directly in HTML/JSX -->
<button class="btn btn-primary">Click</button>
```

## Anti-Pattern: Overriding DaisyUI with `!important`

```css
/* WRONG */
.btn { background-color: red !important; }

/* RIGHT — match the layer */
@layer daisyui.l1.l2 { .btn { --btn-color: var(--color-error); } }
```

## Anti-Pattern: Hardcoding Theme-Specific Colors in Utilities

```html
<!-- WRONG — breaks on dark theme, breaks on theme switch -->
<div class="bg-white text-gray-900">

<!-- RIGHT — uses DaisyUI semantic colors that change with theme -->
<div class="bg-base-100 text-base-content">
```

## Anti-Pattern: Using DaisyUI Interactive Patterns (Checkbox Tricks) in React State-Managed Components

```tsx
// WRONG — hidden checkbox inside React is hard to control
<input type="checkbox" id="modal-toggle" class="modal-toggle" />

// RIGHT — use JS state and class toggling
const [open, setOpen] = useState(false);
<div className={cn("modal", open && "modal-open")}>
```

## Performance

- **CSS output size:** DaisyUI adds ~50KB minified CSS. For CSS-only usage, this is fixed cost regardless of how many components you use. With `exclude:` option, trim unused components
- **Theme count:** Each additional theme adds ~25 CSS variable declarations. 35 themes adds negligible CSS but increases build time. Only include themes you use
- **Animation:** DaisyUI uses CSS transitions (not JS). All animations respect `prefers-reduced-motion` via `@media (prefers-reduced-motion: no-preference)`

## Consistency Rules

Establish these team conventions to prevent visual inconsistency:

1. **Color discipline:** Only use DaisyUI semantic colors (`text-primary`, `bg-error`) for semantic meaning. Never apply `text-red-500` when you mean "error state"
2. **Size scale discipline:** Use component size modifiers (`btn-sm`, `input-lg`) rather than overriding font-size or height with utilities
3. **Don't mix component libraries** without prefixes — if using both DaisyUI and Flowbite/Material UI, enable DaisyUI's `prefix` option

## See Also

- [Customization Patterns](customization-patterns.md)
- [DaisyUI and React](daisyui-react.md)
- Reference: `design-system-tailwind.md` Section 13 — Tailwind best practices and anti-patterns
