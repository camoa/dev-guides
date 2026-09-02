---
description: "Feature detection and graceful degradation for CREATE category features"
tldr: "Use this when implementing CREATE category features (advanced features outside Bootstrap scope) to ensure graceful degradation and browser compatibility."
drupal_version: "11.x"
---

# Progressive Enhancement Guidelines

## When to Use

> Use this when implementing CREATE category features (advanced features outside Bootstrap scope) to ensure graceful degradation and browser compatibility.

- You're implementing CREATE category features (advanced features outside Bootstrap scope)
- You need to ensure modern CSS features degrade gracefully in older browsers
- You're assessing browser compatibility for custom implementations
- You need to evaluate performance impact of advanced features

## Modern CSS Features Strategy

**Feature Detection Approach:**

Use feature detection (not browser detection) to provide fallbacks for modern CSS features. This ensures functionality works across all target browsers while enhancing the experience where support exists.

### Pattern: Progressive Enhancement Mixin

```scss
@mixin progressive-enhancement($property, $value, $fallback-property: null, $fallback-value: null) {
  // Provide fallback first (for browsers without modern feature support)
  @if $fallback-property and $fallback-value {
    #{$fallback-property}: $fallback-value;
  }

  // Enhanced version with feature detection
  @supports (#{$property}: #{$value}) {
    #{$property}: $value;
  }
}
```

### Usage Example

```scss
// Apply backdrop blur with fallback
.modern-component {
  @include progressive-enhancement(
    backdrop-filter, blur(10px),
    background, rgba(255, 255, 255, 0.9)
  );
}

// Result in CSS:
// .modern-component {
//   background: rgba(255, 255, 255, 0.9); /* Fallback */
// }
// @supports (backdrop-filter: blur(10px)) {
//   .modern-component {
//     backdrop-filter: blur(10px); /* Enhanced */
//   }
// }
```

## Browser Compatibility Considerations

**Best Practices:**

1. **Always provide fallbacks** - Every modern CSS feature must have a functional fallback for browsers without support
2. **Test across target browsers** - Validate functionality during development in oldest supported browser
3. **Document browser support requirements** - Clearly state minimum browser versions in implementation guide
4. **Use feature detection** - Use `@supports` queries, never user-agent sniffing
5. **Graceful degradation** - Ensure core functionality works without enhancement (enhancement is additive)

### Decision Table: Browser Compatibility Strategy

| Feature Type | Strategy | Example |
|--------------|----------|---------|
| Modern layout (Grid, Flexbox) | Fallback to simpler layout | Grid → Flexbox → Float |
| Visual effects (backdrop-filter) | Fallback to solid color | Blur → Solid background |
| Modern selectors (:has, :is) | Fallback to standard selectors | `:has()` → Direct child selectors |
| CSS custom properties | Fallback to SCSS variables | `var(--color)` → `$color` |
| Modern units (dvh, svh) | Fallback to vh/% | `100dvh` → `100vh` |

## Performance Impact Assessment

**Before Implementing Advanced Features:**

1. **Measure baseline performance** - Capture metrics without custom features using browser DevTools
2. **Test on lower-end devices** - Validate performance impact on target minimum hardware specs
3. **Monitor bundle size increase** - Track CSS file size growth from custom implementations
4. **Evaluate runtime performance** - Test complex effects (animations, filters) for frame rate impact
5. **Document performance considerations** - Record findings for team awareness and future optimization

### Performance Checklist

- [ ] **Baseline metrics captured** - Page load time, CSS parse time, render time without custom features
- [ ] **Low-end device testing** - Validated on lowest spec device in target support matrix
- [ ] **Bundle size tracked** - CSS file size increase < 15% from custom features
- [ ] **Runtime performance validated** - No frame drops below 60fps on target devices
- [ ] **Performance budget documented** - Clear thresholds for acceptable performance impact
- [ ] **Optimization strategy planned** - Fallback plan if performance degrades

## Common Mistakes

**Mistake:** Using modern features without fallbacks, breaking functionality in older browsers
**Correction:** Always provide functional fallback first, then enhance with `@supports` query

**Mistake:** Browser detection instead of feature detection (`if (navigator.userAgent.includes('Chrome'))`)
**Correction:** Use `@supports` in CSS for feature detection, never parse user agents

**Mistake:** Implementing advanced features without measuring performance impact
**Correction:** Test on low-end devices and measure frame rate, render time before deploying

**Mistake:** Assuming all modern browsers support all modern features equally
**Correction:** Check caniuse.com for each feature, test in Firefox, Safari, Chrome separately

## See Also

- ← Previous: [Quality Assurance Framework](quality-assurance-framework.md)
- Next: [Project Organization Principles](project-organization-principles.md)
- Related: [Decision Categories](bootstrap-accommodation-decision-framework.md) - CREATE category
