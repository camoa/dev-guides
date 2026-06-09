---
description: Respect prefers-reduced-motion by defaulting to static and scoping motion to the no-preference query; provide pause controls for auto-playing content.
tldr: Default page state should be static — scope animations inside `@media (prefers-reduced-motion: no-preference)` so users opt in to motion; slowing down a spinning animation is not sufficient — motion itself is the trigger for vestibular disorders; never exceed 3 flashes/second.
---

# Motion Preferences

## When to Use

> Reduce or eliminate animations for users who have configured their system to prefer reduced motion — default-static is safer than requiring users to opt out of motion that may cause discomfort or seizures.

## Decision

| Scenario | Pattern | Notes |
|---|---|---|
| Spinning / rotating animation | Disable entirely under reduced-motion | Don't substitute with a slowed version — still causes nausea |
| Parallax / sliding transitions | Use `prefers-reduced-motion: reduce` to substitute with fade or instant | Fade is generally safe |
| Auto-playing carousel / banner | Provide pause control | Required by WCAG 2.2.2 for anything playing >5 seconds |
| Flash / strobe effect | Never exceed 3 flashes per second | Threshold for photosensitive seizures; applies regardless of preference |
| Default page state | Static | Let users opt in to motion, not opt out |

**"Reduce" is not "remove":** `prefers-reduced-motion: reduce` means reduce to the minimum necessary. A simple opacity transition is usually fine; a spinning loader or sliding carousel is not.

## Pattern

```css
/* Default: static. Opt in to motion. */
.spinner { opacity: 0.5; }

@media (prefers-reduced-motion: no-preference) {
  .spinner { animation: spin 1s linear infinite; opacity: 1; }
}

/* Alternative: motion-first, then dampen */
@media (prefers-reduced-motion: reduce) {
  .spinner { animation: none; opacity: 0.5; }
  * { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}
```

```html
<!-- Pause control for auto-playing content -->
<div class="carousel" aria-label="Featured articles">
  <div class="carousel-slides">...</div>
  <button type="button" aria-label="Pause carousel" aria-pressed="false">
    &#9646;&#9646;
  </button>
</div>
```

## Common Mistakes

- **Wrong**: Slowing down rather than stopping problematic animation → **Right**: Vestibular disorders are triggered by the motion itself, not the speed
- **Wrong**: No pause mechanism on auto-playing carousels → **Right**: WCAG 2.2.2 violation; keyboard users cannot navigate carousels that change while they focus
- **Wrong**: Flash effects anywhere in the UI → **Right**: Three or more flashes per second can cause seizures regardless of user preference
- **Wrong**: Using `prefers-reduced-motion: reduce` without testing → **Right**: Verify the static state renders correctly; hidden or broken states are common

## See Also

- Reference: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- Reference: https://www.w3.org/TR/WCAG22/#pause-stop-hide (WCAG 2.2.2)
