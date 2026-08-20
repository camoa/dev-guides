---
description: color-scheme infrastructure for dark mode — FOUC prevention, scrollbar theming, accent-color, component-scoped schemes, and two-state toggle UX.
tldr: Set color-scheme:light dark on :root and mirror it with <meta name="color-scheme"> in <head> before any stylesheets to prevent the white canvas flash. Inline synchronous script reads localStorage before paint — never defer or type="module". Re-declare inherited color properties (color, accent-color) after any component-level color-scheme override; they resolve at the ancestor's scheme and don't re-resolve on their own.
drupal_version: "11.x"
---

# color-scheme and Dark Mode Mechanics

## When to Use

> Use when `light-dark()` tokens are in place but you need the surrounding infrastructure: telling the browser which schemes are supported, preventing a white canvas flash, customizing scrollbars and accent colors, scoping dark mode to a single component, and wiring up a user toggle. The `light-dark()` function handles token values; this section covers everything it relies on.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Enable dark-mode theming of form controls and scrollbars | `color-scheme: light dark` on `:root` | Signals supported schemes; browser themes native UI automatically |
| Prevent white canvas flash before CSS parses | `<meta name="color-scheme" content="light dark">` in `<head>` | Sets canvas hint at HTML parse time, before any stylesheet loads |
| Prevent flash for users with a pinned preference | Inline `<script>` reading `localStorage` before paint | Runs synchronously; `defer`/`type="module"` executes too late |
| Custom scrollbar thumb and track colors | `scrollbar-color` on `:root` | Baseline newly available Dec 2025 (Safari 26); macOS needs `scrollbar-width` to activate |
| Brand-match checkboxes, sliders, range inputs | `accent-color` on `:root` | Progressive enhancement — Chrome and Firefox only; Safari unsupported |
| Force a component into dark mode on a light page | `color-scheme: dark` on the element | Affects nested form controls, scrollbars, and `light-dark()` for that subtree |
| Prevent browser from overriding a component's scheme | `color-scheme: only dark` | The `only` keyword blocks the browser from reverting to the system scheme |
| User toggle between system preference and an override | Two-state: system + pinned override | Three-state violates the feedback principle — see Toggle UX below |

## Pattern

**FOUC prevention and root declaration:**

```html
<!-- In <head> BEFORE any stylesheets -->
<meta name="color-scheme" content="light dark">

<!-- Inline sync script — NOT defer, NOT type="module" -->
<script>
{
  const saved = localStorage.getItem('color-scheme');
  if (saved) {
    document.querySelector('meta[name="color-scheme"]').content = saved;
  }
}
</script>
```

```css
:root {
  color-scheme: light dark; /* mirrors meta; required for light-dark() to function */

  /* Scrollbar tokens — Baseline newly available Dec 2025 */
  --scrollbar-thumb: light-dark(oklch(60% 0 0), oklch(45% 0 0));
  --scrollbar-track: light-dark(oklch(92% 0 0), oklch(20% 0 0));
  scrollbar-color: var(--scrollbar-thumb) var(--scrollbar-track);
  scrollbar-width: thin; /* Required on macOS to activate color rendering */

  /* Accent color — progressive enhancement; ignored by Safari */
  accent-color: light-dark(var(--color-accent-light), var(--color-accent-dark));
}
```

**Scrollbar-color fallback for pre-Dec-2025 browsers:**

```css
@supports not (scrollbar-color: auto) {
  .scroller::-webkit-scrollbar { width: 8px; height: 8px; }
  .scroller::-webkit-scrollbar-thumb { background: var(--scrollbar-thumb); }
  .scroller::-webkit-scrollbar-track { background: var(--scrollbar-track); }
}
```

**Component-scoped color scheme:**

```css
pre, code, .media-player {
  color-scheme: dark; /* use 'only dark' to block any browser override */
  background: var(--surface-dark); /* REQUIRED: element must have a background */

  /* REQUIRED: re-declare inherited <color> properties — they resolved at the
     ancestor's scheme and do not re-resolve from tokens on their own */
  color: var(--text-color);
  accent-color: var(--accent-color);
}
```

**`light-dark()` inheritance gotcha:** Unregistered custom properties (tokens like `--surface-color`) re-resolve under the new `color-scheme` automatically. But inherited `<color>` properties (`color`, `accent-color`, `fill`) resolve to a single computed color at the ancestor and pass that fixed value down. Re-declare them explicitly after a `color-scheme` override.

**Do not register design-token custom properties as `syntax: '<color>'`** — registered `<color>` properties also resolve at computed value time, stripping the `light-dark()` expression. Use `syntax: '<color>'` only for per-element animation targets.

**JS toggle (two-state):**

```js
const meta = document.querySelector('meta[name="color-scheme"]');

function toggleScheme() {
  if (meta.content !== 'light dark') {
    meta.content = 'light dark'; // return to system
  } else {
    const prefersDark = matchMedia('(prefers-color-scheme: dark)').matches;
    meta.content = prefersDark ? 'light' : 'dark'; // pin the opposite
  }
  localStorage.setItem('color-scheme', meta.content);
}
```

**Toggle UX — use two-state, not three-state.** Three-state (System / Light / Dark) always has two states producing the same visual result, violating the feedback principle. Two-state (System + Override) is sufficient: when the user pins an override, that exact scheme persists regardless of later OS changes.

**macOS scrollbar caveats:** macOS uses overlay scrollbars by default — `scrollbar-color` is silently ignored unless `scrollbar-width: thin` or `auto` forces permanent gutter rendering. Add `scrollbar-gutter: stable` to reserve gutter space. Never animate or transition `scrollbar-color` — a WebKit bug causes flickering on every change.

## Common Mistakes

- **`color-scheme` on `body` instead of `:root`/`html`** → root scrollbars and canvas background are controlled by the root element; `body`-only leaves them in the wrong scheme
- **Omitting `<meta name="color-scheme">`** → canvas flashes white before the stylesheet loads
- **`defer` or `type="module"` on the FOUC-prevention script** → deferred scripts execute after the first paint; the script must be inline and synchronous
- **Defaulting `:root` to `color-scheme: dark`** → overrides the user's system preference; always default to `light dark`
- **Not re-declaring inherited `<color>` properties after a component-level override** → `color`, `accent-color` carry the already-resolved ancestor value rather than re-resolving the token
- **`color-scheme` on an element without a background** → risks mixing light-scheme text from an ancestor with a dark-scheme background
- **Animating or transitioning `scrollbar-color`** → causes scrollbar flickering in WebKit/Blink (known bug); set it statically only
- **Relying on `accent-color` for essential UI** → Safari does not support it; the OS default accent applies silently

## See Also

- [light-dark() Function](light-dark.md) — declaring per-token light/dark color values
- [Relative Color Syntax](relative-color.md) — deriving dark variants from a base token
- Reference: [MDN color-scheme](https://developer.mozilla.org/en-US/docs/Web/CSS/color-scheme)
- Reference: [MDN scrollbar-color](https://developer.mozilla.org/en-US/docs/Web/CSS/scrollbar-color)
- Reference: [MDN accent-color](https://developer.mozilla.org/en-US/docs/Web/CSS/accent-color)
