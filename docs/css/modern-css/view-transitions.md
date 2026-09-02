---
description: "Smooth transitions between UI states with View Transitions API"
tldr: "Use View Transitions for smooth animated transitions between UI states — page navigations, tab switches, content updates — without JS animation libraries. Use a JS library when you need complex choreographed sequencing."
---

# View Transitions

## When to Use

> For smooth animated transitions between UI states — page navigations, tab switches, content updates — without JavaScript animation libraries. The browser automatically cross-fades between old and new states, with the option to morph specific shared elements.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Animate a same-document state change | `document.startViewTransition(callback)` | JS triggers, browser handles the animation |
| Animate cross-document navigation (MPA) | `@view-transition { navigation: auto; }` | CSS-only, both pages opt in |
| Morph a specific element between states | `view-transition-name: unique-name` | Browser matches named elements and morphs them |
| Complex choreographed animation | JS animation library | View Transitions handle simple morph/fade; not sequencing |
| Override the default cross-fade | `::view-transition-old()` and `::view-transition-new()` pseudo-elements | Target old/new snapshot layers with CSS |

## Pattern

Same-document (SPA-style) — any DOM update wrapped in the callback gets a cross-fade:
```js
document.startViewTransition(() => {
  updateDOM(); // synchronous DOM change
});
```

```css
/* Morph a card image into a full-screen hero */
.card__image { view-transition-name: hero-image; }
.hero__image  { view-transition-name: hero-image; }
/* Browser morphs the element between these two states */

/* Override default animation */
::view-transition-old(hero-image),
::view-transition-new(hero-image) {
  animation-duration: 0.5s;
}
```

Cross-document (MPA) — add to both the outgoing and incoming page:
```css
@view-transition {
  navigation: auto;
}
```
That single CSS rule on both pages gives a default cross-fade navigation. No JavaScript.

**Browser support:**
- Same-document: Chrome 111, Firefox 144 (October 2025), Safari 18. Now baseline newly available (all major browsers).
- Cross-document: Chrome 126, Safari 18.2. **Firefox does not yet support cross-document view transitions.** Use with `@supports` for cross-document.

## Common Mistakes

- Using non-unique `view-transition-name` values — each name must be unique in the document at any given time; duplicate names cause the transition to skip that element
- Assigning `view-transition-name` to elements not visible in both states — the browser skips the morph if one snapshot is missing; animation falls back to default cross-fade
- Long-running async operations inside `startViewTransition` callback — the callback should return a promise, but the old state is frozen while it runs; keep it fast
- Using cross-document view transitions without checking Firefox support — they silently fall back to instant navigation in Firefox

## See Also

- ← [@starting-style Transitions](starting-style-transitions.md) | [Scroll-Driven Animations](scroll-driven-animations.md) →
- Reference: [MDN View Transitions API](https://developer.mozilla.org/en-US/docs/Web/API/View_Transitions_API)
