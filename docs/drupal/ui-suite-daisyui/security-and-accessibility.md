---
description: Asset pipeline security, Twig escaping, form security, DaisyUI component accessibility, and WCAG concerns
---

# Security & Accessibility

## Security Considerations

### Asset Pipeline

Alpha6 ships pre-compiled CSS (`dist/css/app.css`) with no CDN dependencies. The base theme and starterkit both use local build pipelines, eliminating CDN-related supply chain and CSP risks that were present in earlier alpha releases.

For sub-themes using the starterkit, npm dependencies (Tailwind, DaisyUI, Vite) are dev-only build tools that do not ship to production. Only compiled CSS is served to browsers.

### Twig Output Escaping

All SDC component Twig templates use Drupal's `attributes` object and `{{ }}` syntax, which auto-escape HTML. The theme does not use `|raw` filter. Slots receive pre-rendered Drupal content that has already been sanitized by the render pipeline.

### Form Security

The `form_alter` hook only adds CSS classes to form elements -- it does not modify form behavior, validation, or CSRF tokens. DaisyUI's `<dialog>` modal uses the HTML `<form method="dialog">` pattern, which is a standard browser API that does not submit data to the server.

## Accessibility

### DaisyUI Component A11Y

DaisyUI 5 components have baseline accessibility:

| Component | A11Y Features |
|---|---|
| Alert | `role="alert"` attribute applied by the theme |
| Modal | Uses native `<dialog>` element with `showModal()` API (keyboard trap, escape to close) |
| Accordion/Collapse | Uses `<input type="radio">` or `<details>` for native keyboard interaction |
| Menu | Uses `<details>` for collapsible sub-menus (keyboard accessible) |
| Tabs | Uses `<a>` links (standard focus/navigation) |
| Breadcrumbs | Uses `<a>` links with semantic list |
| Skip link | `<a id="main-content" tabindex="-1">` in page template |

### Concerns

1. **Color contrast**: Not all 35 DaisyUI themes meet WCAG 2.1 AA contrast ratios. Test your chosen theme with a contrast checker. Themes like `pastel` and `wireframe` may have insufficient contrast for body text.

2. **Loading indicators**: The `loading` component is purely visual (CSS animation). Add `aria-busy="true"` and `aria-label` when using it to indicate loading state to screen readers.

3. **Carousel**: DaisyUI's carousel is CSS-only (scroll-snap). It lacks ARIA carousel attributes (`role="region"`, `aria-roledescription="carousel"`). Add these manually for screen reader support.

4. **Icon-only buttons**: When using `button` with only an `icon` prop and no `label`, add `aria-label` to the button for screen reader accessibility.

## Common Mistakes

- **Assuming DaisyUI themes are WCAG-compliant** -- Not all themes pass contrast requirements, especially lighter themes. WHY: DaisyUI themes prioritize aesthetics; accessibility compliance varies per theme.
- **Not rebuilding CSS after changes** -- In the starterkit workflow, forgetting to run `npm run build` means production deploys outdated CSS. WHY: Unlike CDN-based approaches, the build pipeline requires an explicit compile step.

## See Also

- `drupal-security.md` -- Drupal security patterns
- `design-system-daisyui.md` -- DaisyUI accessibility details
