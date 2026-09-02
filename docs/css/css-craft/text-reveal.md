---
description: Text reveal animations — line slide-up, clip-path wipe, per-character and per-word reveals with minimal JS text splitter
tldr: "Use CSS `overflow: hidden` + `translateY` for line reveals (no JS). Use a minimal JS text splitter for per-character or per-word reveals — the CSS does the animation, JS only wraps each token in a `<span>`."
---

# Text Reveal Animations

## When to Use
When a client wants headlines that animate in dramatically — text sliding up from behind a mask, letters appearing one by one, or words fading/clipping into view. The #1 most-requested animation effect on award-winning sites.

## Decision
| Client asks for... | CSS Only? | Use... |
|---|---|---|
| Single line slides up from behind mask | Yes | `overflow: hidden` + `translateY` |
| Clip-path reveal (wipe across text) | Yes | `clip-path: inset()` animation |
| Multi-line, line-by-line reveal | Yes (if lines are separate elements) | Staggered `translateY` per line |
| Letter-by-letter animation | **No** — needs JS text splitter | JS splits into `<span>`s, CSS animates each |
| Word-by-word reveal | **No** — needs JS text splitter | JS splits into `<span>`s, CSS animates each |
| Scroll-triggered text reveal | Yes | `animation-timeline: view()` |

## Pattern: Line Slide-Up (CSS Only)
```css
.text-reveal {
  overflow: hidden;
}

.text-reveal__line {
  display: block;
  transform: translateY(110%);
  animation: slide-up 0.8s var(--ease-emphasized-decel) forwards;
}

.text-reveal__line:nth-child(2) { animation-delay: 0.1s; }
.text-reveal__line:nth-child(3) { animation-delay: 0.2s; }

@keyframes slide-up {
  to { transform: translateY(0); }
}
```

## Pattern: Clip-Path Text Reveal (CSS Only)
```css
.text-reveal--clip {
  clip-path: inset(0 100% 0 0);
  animation: clip-reveal 1s var(--ease-emphasized-decel) forwards;
}

@keyframes clip-reveal {
  to { clip-path: inset(0 0% 0 0); }
}

/* Scroll-triggered variant */
.text-reveal--scroll {
  clip-path: inset(0 100% 0 0);
  animation: clip-reveal 1s linear forwards;
  animation-timeline: view();
  animation-range: entry 20% entry 60%;
}
```

## Pattern: Per-Character with Minimal JS
```html
<h1 class="split-text" data-split>Transform your business</h1>
```
```js
// Text splitter — ~10 lines
document.querySelectorAll('[data-split]').forEach(el => {
  el.innerHTML = el.textContent.split('').map((char, i) =>
    `<span class="char" style="--i:${i}">${char === ' ' ? '&nbsp;' : char}</span>`
  ).join('');
});
```
```css
.split-text .char {
  display: inline-block;
  opacity: 0;
  transform: translateY(40px);
  animation: char-in 0.5s var(--ease-emphasized-decel) forwards;
  animation-delay: calc(var(--i) * 0.03s);
}

@keyframes char-in {
  to { opacity: 1; transform: translateY(0); }
}

/* Scroll-triggered */
.split-text .char {
  animation-timeline: view();
  animation-range: entry 10% entry 50%;
}
```

## Pattern: Word-by-Word with Minimal JS
```js
document.querySelectorAll('[data-split-words]').forEach(el => {
  el.innerHTML = el.textContent.split(' ').map((word, i) =>
    `<span class="word" style="--i:${i}"><span class="word__inner">${word}</span></span>`
  ).join(' ');
});
```
```css
.word {
  display: inline-block;
  overflow: hidden;
}

.word__inner {
  display: inline-block;
  transform: translateY(110%);
  animation: word-up 0.6s var(--ease-emphasized-decel) forwards;
  animation-delay: calc(var(--i) * 0.08s);
}

@keyframes word-up {
  to { transform: translateY(0); }
}
```

## Stagger Timing Guidelines
| Split Type | Delay per Item | Total Feel |
|---|---|---|
| Characters | 20-40ms | Fast cascade |
| Words | 60-100ms | Readable reveal |
| Lines | 100-200ms | Dramatic, editorial |

## Common Mistakes
- **Animating on page load without trigger** — text reveal should be scroll-triggered or after a deliberate delay, not immediate
- **Too slow stagger** — >50ms per character feels sluggish; keep character delays at 20-35ms
- **Not wrapping split text in `overflow: hidden`** — text is visible during translateY animation start position
- **Forgetting `display: inline-block`** on split spans — `transform` doesn't work on inline elements
- **Missing `prefers-reduced-motion`** — replace with instant opacity: 1 for motion-sensitive users

## See Also
- [Entrance Animations](entrance-animations.md) → general scroll-triggered reveals
- [Text Effects](text-effects.md) → gradient text, knockout, shadows
- [Spring Physics](spring-physics-and-advanced-easing.md) → bouncy character reveals
