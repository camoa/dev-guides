---
description: Balanced headings and orphan-free text with text-wrap: balance and pretty
---

# text-wrap: balance and pretty

## When to Use

> Use `text-wrap: balance` on headings (up to ~6 lines) for even line breaks. Use `text-wrap: pretty` on body copy to prevent orphaned last words. Never use `balance` on long paragraphs.

## Decision

| If you need... | Use... | Notes |
|---|---|---|
| Balanced heading that breaks evenly across lines | `text-wrap: balance` | Browser balances line lengths; max ~6 lines |
| Body text without orphaned last word | `text-wrap: pretty` | Adjusts last few lines to prevent short last line |
| Long body copy performance | Avoid `balance` | `balance` is expensive on long blocks; use `pretty` instead |
| Safari support for last-line orphan control | `text-wrap: balance` | `pretty` not yet in Safari as of early 2026 |

## Pattern

```css
/* Headings — balanced line breaks */
h1, h2, h3, h4 {
  text-wrap: balance;
}

/* Body copy — prevent orphaned last word */
p, blockquote, li {
  text-wrap: pretty;
}
```

**`balance` behavior:** The browser rebalances all lines so they are approximately equal width. Best for headings of up to ~6 lines. On longer text blocks, the rebalancing becomes visible as content shifts during load and the performance cost rises.

**`pretty` behavior:** Only adjusts the last few lines (typically the last 4 in Chrome's implementation) to prevent a short word from sitting alone on the final line. No visible rebalancing — safe for body copy.

**Browser support:**
- `text-wrap: balance` — Chrome 114, Firefox 121, Safari 17.5. Safe to use.
- `text-wrap: pretty` — Chrome 117, Firefox 134, **Safari not yet** (expected in Safari 26+). Use as progressive enhancement.

## Common Mistakes

- **Wrong**: Applying `text-wrap: balance` to long paragraphs → **Right**: Performance cost is real; the browser recalculates the entire block on resize; limit to headings and short display text
- **Wrong**: Expecting `pretty` to affect the whole paragraph → **Right**: It intentionally adjusts only the last few lines; it does not rebalance the entire text block
- **Wrong**: Using `text-wrap: balance` to prevent orphans in body copy → **Right**: `balance` rebalances lines equally which may or may not prevent a short last word; `pretty` is the right tool for orphan control

## See Also

- [Dynamic Viewport Units (dvh, svh, lvh)](viewport-units.md)
- Reference: [MDN text-wrap](https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap)
