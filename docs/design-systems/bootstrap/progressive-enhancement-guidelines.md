---
description: Feature detection and graceful degradation for CREATE category features
---

# Progressive Enhancement Guidelines

## When to Use

> Use this when implementing CREATE category features (advanced features outside Bootstrap scope) to ensure graceful degradation and browser compatibility.

## Modern CSS Features Strategy

**Use feature detection (not browser detection) to provide fallbacks.**

## Pattern

Progressive enhancement mixin:

```scss
@mixin progressive-enhancement($property, $value, $fallback-property: null, $fallback-value: null) {
  // Provide fallback first
  @if $fallback-property and $fallback-value {
    #{$fallback-property}: $fallback-value;
  }

  // Enhanced version with feature detection
  @supports (#{$property}: #{$value}) {
    #{$property}: $value;
  }
}
```

Usage:

```scss
.modern-component {
  @include progressive-enhancement(
    backdrop-filter, blur(10px),
    background, rgba(255, 255, 255, 0.9)
  );
}

// Result:
// .modern-component {
//   background: rgba(255, 255, 255, 0.9); /* Fallback */
// }
// @supports (backdrop-filter: blur(10px)) {
//   .modern-component {
//     backdrop-filter: blur(10px); /* Enhanced */
//   }
// }
```

## Browser Compatibility Strategy

| Feature Type | Strategy | Example |
|--------------|----------|---------|
| Modern layout (Grid, Flexbox) | Fallback to simpler layout | Grid → Flexbox → Float |
| Visual effects (backdrop-filter) | Fallback to solid color | Blur → Solid background |
| Modern selectors (:has, :is) | Fallback to standard selectors | `:has()` → Direct child |
| CSS custom properties | Fallback to SCSS variables | `var(--color)` → `$color` |
| Modern units (dvh, svh) | Fallback to vh/% | `100dvh` → `100vh` |

## Best Practices

1. **Always provide fallbacks** - Every modern CSS feature needs functional fallback
2. **Test across target browsers** - Validate in oldest supported browser
3. **Document browser support** - State minimum versions
4. **Use feature detection** - Use `@supports`, never user-agent sniffing
5. **Graceful degradation** - Core functionality works without enhancement

## Performance Impact Assessment

### Before Implementing Advanced Features

1. **Measure baseline** - Capture metrics without custom features
2. **Test on lower-end devices** - Validate on minimum hardware specs
3. **Monitor bundle size** - Track CSS file size growth
4. **Evaluate runtime performance** - Test for frame rate impact
5. **Document findings** - Record for team awareness

### Performance Checklist

- [ ] Baseline metrics captured (load time, CSS parse time, render time)
- [ ] Low-end device testing completed
- [ ] Bundle size increase < 15%
- [ ] No frame drops below 60fps on target devices
- [ ] Performance budget documented
- [ ] Optimization strategy planned

## Common Mistakes

- **Wrong**: Modern features without fallbacks → **Right**: Functional fallback first, then @supports
- **Wrong**: Browser detection via user-agent → **Right**: Feature detection via @supports
- **Wrong**: No performance measurement → **Right**: Test on low-end devices first
- **Wrong**: Assuming uniform modern browser support → **Right**: Check caniuse.com per feature

## See Also

- [Quality Assurance Framework](quality-assurance-framework.md)
- [Bootstrap Accommodation Decision Framework](bootstrap-accommodation-decision-framework.md) - CREATE category
- [Project Organization Principles](project-organization-principles.md)
