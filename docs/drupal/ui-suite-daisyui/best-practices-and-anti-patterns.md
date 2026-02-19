---
description: When UI Suite DaisyUI fits, recommended patterns, anti-patterns to avoid, and performance considerations
---

# Best Practices & Anti-Patterns

## When UI Suite DaisyUI Is the Right Choice

**Good fit:**
- Content-focused sites where site builders need visual control
- Projects that benefit from DaisyUI's theme system (multi-brand, dark mode)
- Rapid prototyping with Drupal + Layout Builder
- Teams where front-end expertise is limited (low-code component assembly)

**Poor fit:**
- Projects requiring pixel-perfect custom designs with no DaisyUI dependency
- Projects already heavily invested in Bootstrap/Radix ecosystem

## Best Practices

1. **Use the component system, not raw DaisyUI classes** -- Always render through SDC components rather than writing DaisyUI classes directly in templates. This ensures consistency and enables UI Patterns features (sources, Layout Builder integration).

2. **Choose a DaisyUI theme early** -- The 35 available themes have dramatically different color palettes. Select one during development and customize via CSS variables rather than switching themes late.

3. **Use grid components for page layouts** -- The grid_1_region through grid_4_regions components handle responsive breakpoints properly. Avoid writing custom grid CSS when these components cover the use case.

4. **Keep sub-theme overrides minimal** -- Override only what you need. The base theme's component library is well-structured; wholesale replacement creates maintenance burden when the base theme updates.

5. **Use UI Styles for one-off visual adjustments** -- Instead of creating a new component variant for a single use case, apply a UI Style (e.g., background color, padding) to the block.

## Anti-Patterns

| Anti-Pattern | Why It Is Wrong | Do This Instead |
|---|---|---|
| Writing raw DaisyUI classes in custom templates | Bypasses UI Patterns discovery, breaks Layout Builder | Use or extend existing SDC components |
| Editing `dist/` files directly instead of source `.pcss` files | Changes lost on next build | Edit source files in `css/` and `components/`, then run `npm run build` |
| Overriding all 35 DaisyUI themes in CSS variables | Massive CSS variable blocks that conflict | Pick one base theme and customize only it |
| Mixing Bootstrap and DaisyUI classes | Class name collisions (`btn` exists in both) | Choose one framework per project |
| Ignoring `prose` class on formatted text | WYSIWYG content loses all formatting | Keep the `prose` class or provide equivalent styles |
| Hardcoding colors instead of using semantic tokens | Breaks theme switching | Use DaisyUI semantic colors (`primary`, `error`, etc.) |

## Performance Considerations

1. **Pre-compiled CSS**: Alpha6 ships `dist/css/app.css` pre-compiled. No CDN dependencies or runtime CSS compilation required in the base theme.
2. **Sub-theme build pipeline**: The starterkit uses Vite + PostCSS to compile CSS at build time, not at runtime. Run `npm run build` before deployment.
3. **Component count**: 51 components are registered at boot. This is normal SDC overhead; components are lazy-loaded when rendered.

## Common Mistakes

- **Treating this as "just a theme"** -- UI Suite DaisyUI is a full component system, not just a CSS theme. WHY: It integrates with Layout Builder, field formatters, and views through UI Patterns, which means changes to the theme can affect content display across the site.

## See Also

- `design-system-daisyui.md` -- DaisyUI performance and optimization
