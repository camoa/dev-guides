---
description: Text reveal animations — line slide-up, clip-path wipe, per-character and per-word reveals with minimal JS text splitter
tldr: "Use CSS `overflow: hidden` + `translateY` for line reveals (no JS). Use a minimal JS text splitter for per-character or per-word reveals — the CSS does the animation, JS only wraps each token in a `<span>`."
---

# Text Reveal Animations

## When to Use

> Use CSS `overflow: hidden` + `translateY` for line reveals (no JS). Use a minimal JS text splitter for per-character or per-word reveals — the CSS does the animation, JS only wraps each token in a `<span>`.

## Decision

| Client asks for... | CSS Only? | Use... |
|---|---|---|
| Single line slides up from behind mask | Yes | `overflow: hidden` + `translateY` |
| Clip-path reveal (wipe across text) | Yes | `clip-path: inset()` animation |
| Multi-line, line-by-line reveal | Yes (if lines are separate elements) | Staggered `translateY` per line |
| Letter-by-letter animation | No — needs JS text splitter | JS splits into `<span>`s, CSS animates each |
| Word-by-word reveal | No — needs JS text splitter | JS splits into `<span>`s, CSS animates each |
| Scroll-triggered text reveal | Yes | `animation-timeline: view()` |

## Pattern

```css
/* Line slide-up */
.text-reveal { overflow: hidden; }
.text-reveal__line {
  display: block;
  transform: translateY(110%);
  animation: slide-up 0.8s var(--ease-emphasized-decel) forwards;
}
.text-reveal__line:nth-child(2) { animation-delay: 0.1s; }
@keyframes slide-up { to { transform: translateY(0); } }

/* Clip-path wipe */
.text-reveal--clip {
  clip-path: inset(0 100% 0 0);
  animation: clip-reveal 1s var(--ease-emphasized-decel) forwards;
}
@keyframes clip-reveal { to { clip-path: inset(0 0% 0 0); } }
```
```js
// Minimal text splitter (~10 lines)
document.querySelectorAll('[data-split]').forEach(el => {
  el.innerHTML = el.textContent.split('').map((char, i) =>
    `<span class="char" style="--i:${i}">${char === ' ' ? '&nbsp;' : char}</span>`
  ).join('');
});
```
```css
.split-text .char {
  display: inline-block; opacity: 0; transform: translateY(40px);
  animation: char-in 0.5s var(--ease-emphasized-decel) forwards;
  animation-delay: calc(var(--i) * 0.03s);
}
@keyframes char-in { to { opacity: 1; transform: translateY(0); } }
```

**Stagger timing:** Characters: 20–40ms. Words: 60–100ms. Lines: 100–200ms.

## Common Mistakes

- **Animating on page load without trigger** — text reveals should be scroll-triggered or delayed, not immediate
- **Too slow stagger** — >50ms per character feels sluggish; keep character delays at 20–35ms
- **Not wrapping in `overflow: hidden`** — text is visible at the `translateY` start position without it
- **Forgetting `display: inline-block`** on split spans — `transform` doesn't work on inline elements
- **Missing `prefers-reduced-motion`** — replace with instant `opacity: 1` for motion-sensitive users

## See Also

- [Entrance Animations](entrance-animations.md) → general scroll-triggered reveals
- [Text Effects](text-effects.md) → gradient text, knockout, shadows
- [Spring Physics and Advanced Easing](spring-physics-and-advanced-easing.md) → bouncy character reveals
