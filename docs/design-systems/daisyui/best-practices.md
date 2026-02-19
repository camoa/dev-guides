---
description: DaisyUI best practices and anti-patterns — when to use component classes vs Tailwind utilities, performance, and team conventions
---

# Best Practices

## When to Use

> Code review, architecture decisions, and onboarding guidance for DaisyUI projects.

## Decision

| Situation | Use DaisyUI class | Use Tailwind utility |
|-----------|-------------------|----------------------|
| Multi-theme color | Always | Never for semantic colors |
| Interactive states (hover, focus, disabled) | `.btn` handles all | Too many utilities to replicate |
| Layout and spacing | No DaisyUI equivalent | `mt-4 px-6 grid grid-cols-2` |
| One-off customization | DaisyUI sets the base | Utilities add adjustments |

## Pattern

**Prefer DaisyUI when multi-theme matters:**

```html
<!-- RIGHT — adapts to all 35 themes automatically -->
<button class="btn btn-primary">Submit</button>
<div class="bg-base-100 text-base-content">Content</div>
```

**Use Tailwind for layout, DaisyUI for semantics:**

```html
<button class="btn btn-primary mt-4 w-full max-w-xs">Submit</button>
```

## Anti-Patterns

**`@apply` with DaisyUI component classes:**

```css
/* WRONG — inlines CSS at build time; btn-ghost/btn-outline modifiers stop working */
.my-button { @apply btn btn-primary; }

/* RIGHT — use the class directly in HTML/JSX */
```
```html
<button class="btn btn-primary">Click</button>
```

**Overriding with `!important`:**

```css
/* WRONG */
.btn { background-color: red !important; }

/* RIGHT — match the DaisyUI layer */
@layer daisyui.l1.l2 { .btn { --btn-color: var(--color-error); } }
```

**Hardcoding theme-specific colors:**

```html
<!-- WRONG — breaks on dark theme or any theme switch -->
<div class="bg-white text-gray-900">

<!-- RIGHT — semantic colors change with theme -->
<div class="bg-base-100 text-base-content">
```

**Checkbox tricks in React:**

```tsx
// WRONG — hidden checkbox is hard to control in React's virtual DOM
<input type="checkbox" id="modal-toggle" className="modal-toggle" />

// RIGHT — use state and class toggling
const [open, setOpen] = useState(false);
<div className={cn("modal", open && "modal-open")}>
```

## Performance

- **CSS output size:** DaisyUI adds ~50KB minified CSS. Fixed cost regardless of components used. Use `exclude:` to trim unused components
- **Theme count:** Each theme adds ~25 CSS variable declarations. 35 themes = negligible CSS but adds build time noise — only include themes you use
- **Animation:** DaisyUI uses CSS transitions, not JS. All animations respect `prefers-reduced-motion` via `@media (prefers-reduced-motion: no-preference)`

## Team Conventions

1. **Color discipline:** Only use DaisyUI semantic colors for semantic meaning — never `text-red-500` when you mean "error state"
2. **Size discipline:** Use component size modifiers (`btn-sm`, `input-lg`) rather than overriding font-size or height with utilities
3. **Multi-library prefix:** If using DaisyUI alongside Flowbite or Material UI, enable `prefix: "d-"` option

## See Also

- [Customization Patterns](customization-patterns.md)
- [DaisyUI and React](daisyui-react.md)
- Reference: `design-system-tailwind.md` Section 13 — Tailwind best practices
