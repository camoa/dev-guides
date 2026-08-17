---
description: CSS Craft — motion tokens, micro-interactions, depth, entrance animations, visual hierarchy, performance, visual effects, container query craft, cinematic effects, scroll-snap carousels, hover effects, CSS shapes, motion path, scroll-aware components, CSS-only UI, and fluid typography
tracks: []
guide-meta:
  concepts:
    - motion tokens
    - micro-interactions
    - CSS animations
    - entrance animations
    - glassmorphism
    - parallax
    - clip-path
    - 3D transforms
    - cinematic effects
    - spring physics easing
    - scroll-snap carousel
    - hover effects
    - card hover
    - button hover
    - CSS shapes
    - blob
    - wave divider
    - shape-outside
    - squircle
    - corner-shape
    - motion path
    - offset-path
    - scroll-aware
    - shrinking header
    - reading progress bar
    - CSS counters
    - animated counter
    - progress ring
    - CSS accordion
    - details summary
    - CSS popover
    - CSS tabs
    - marquee
    - logo ticker
    - bento grid
    - text reveal
    - variable font animation
    - font-variation-settings
    - fluid typography
    - clamp
    - SVG line draw
    - stroke-dashoffset
  not:
    - JavaScript animation libraries
    - CSS architecture (layers, scope, nesting)
  requires: []
  complements:
    - css/modern-css
    - js/interaction-craft
    - media/image-media-craft
  specializes: ""
  category: css
---

# CSS Craft

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Set up a consistent easing and duration token system | [Motion Design Tokens](motion-design-tokens.md) | Use motion tokens when you need a shared vocabulary for animation timing and easing across a project. Without tokens, developers pick arbitrary values (`300ms ease`, `0.5s linear`) creating inconsistent, untuneable motion. |
| Make hover, active, and focus states feel polished | [Micro-Interactions](micro-interactions.md) | Use micro-interactions on every interactive element (buttons, cards, links, toggles). These are the difference between a flat prototype and a production interface. |
| Add realistic depth and shadows to cards and modals | [Elevation and Shadows](elevation-and-shadows.md) | Use elevation shadows when components need visual depth — cards resting on a surface, modals floating above content, dropdowns popping over elements. Shadows establish spatial relationships in a flat medium. |
| Animate elements in as they scroll into view | [Entrance Animations](entrance-animations.md) | Use entrance animations for content appearing on scroll to signal freshness and guide the eye. Use IntersectionObserver for wide browser support and precise control; use scroll-driven `animation-timeline: view()` for pure CSS progressive… |
| Create text hierarchy with opacity and alpha | [Opacity and Visual Hierarchy](opacity-and-visual-hierarchy.md) | Use color alpha for text hierarchy (primary/secondary/tertiary weight) without changing font size or weight. Use `color-mix()` to create semi-transparent versions of existing tokens. |
| Know which properties are safe to animate at 60fps | [Animation Performance](animation-performance.md) | Before animating any CSS property, know its rendering cost. The difference between animating `transform` and `width` is the difference between 60fps and dropped frames. |
| Handle reduced motion, focus rings, and forced colors | [Accessibility and Motion](accessibility-and-motion.md) | Apply reduced-motion handling to every animation pattern. WCAG 2.1 SC 2.3.3 requires it. |
| Apply @starting-style, @property, scroll-driven, or view transitions | [Modern CSS Craft Patterns](modern-css-craft-patterns.md) | Use this guide for applying modern CSS features to craft and polish. Feature syntax and browser support live in [modern-css.md](../modern-css/index.md). |
| Add depth with scrolling at different speeds | [Parallax Effects](parallax-effects.md) | Use parallax for marketing heroes, editorial pages, and portfolio pieces — one or two layers max. Use CSS perspective technique for compositor-safe zero-JS parallax; use scroll-driven for modern browsers with fine-grained control. |
| Create a frosted glass or blurred panel effect | [Glassmorphism and Frosted Glass](glassmorphism-and-frosted-glass.md) | Use frosted glass when there is rich, colorful content behind the element — navigation bars over hero images, floating cards over gradients. On a plain white background it just looks like a blurry rectangle. |
| Apply color blending, overlays, or duotone to images | [Blend Modes and Visual Effects](blend-modes-and-visual-effects.md) | Use CSS blend modes for image color treatment (duotone, tinted overlays), text knockout effects, or creative layering without image editing. Always set `isolation: isolate` on the container to control which stacking context the blend… |
| Shape, reveal, or animate elements with clip-path | [Clip-Path and Masks](clip-path-and-masks.md) | Use `clip-path` for shaped containers, animated reveals (wipes, sweeps, iris), comparison sliders, and creative transitions. It is compositor-accelerated and produces no layout shifts. |
| Create gradient text, text shadows, or knockout text | [Text Effects](text-effects.md) | Use text effects on display type only: hero headlines, pull quotes, section titles. Body copy with gradient text or heavy shadows destroys readability. |
| Build card flips, perspective tilt, or 3D hover effects | [3D Transforms](3d-transforms.md) | Use CSS 3D transforms for interactive components that benefit from a spatial metaphor: flip cards, showcase elements, hover-responsive cards. Do not apply to body copy, long lists, or navigation. |
| Add springy, bouncy animations without JavaScript | [Spring Physics and Advanced Easing](spring-physics-and-advanced-easing.md) | Use CSS `linear()` for spring-like bounce in drawers, modals, toggle switches, and toasts. Use JS spring libraries when animations are frequently interrupted — CSS springs handle interrupts unnaturally because they require a fixed duration. |
| Build skeleton loading screens and shimmer animations | [Skeleton and Loading States](skeleton-and-loading-states.md) | Use skeleton screens for content-heavy components (cards, feeds, profiles) — they reduce perceived wait by showing the layout shape. Use spinners for actions with indeterminate duration (form submit, file upload). |
| Create mesh gradients, animated gradients, noise, or gradient borders | [Gradient Craft](gradient-craft.md) | Use gradient craft techniques for mesh-like layered backgrounds, animated color transitions, grainy texture overlays, and gradient borders. Avoid animating mesh gradients directly — each radial gradient triggers repaint; use a static mesh… |
| Copy a ready-to-use token set | [Quick Reference: Recommended Defaults](quick-reference-recommended-defaults.md) | Copy this complete token set into any project as a starting point. All values are based on MD3 motion tokens, cross-design-system opacity standards, and layered shadow methodology. |
| Make components respond to their container width, not the viewport | [Container Query Craft](container-queries-craft.md) | Use `@container` when a reusable component needs to change its layout based on the space its container gives it. Use `@media` for page-level structure, device preferences (dark mode, reduced motion), and print styles. |
| Add border beams, glows, aurora, neon, shimmer, particles, or perspective grids | [Cinematic Effects](cinematic-effects.md) | Use cinematic effects on hero sections, primary CTAs, and feature highlights — one or two per page maximum. Do not use on navigation, body copy, form fields, dashboards, or secondary CTAs. |
| Build a CSS carousel, image gallery, or paginated scroll | [Scroll-Snap Carousels](scroll-snap-carousels.md) | Use CSS scroll-snap when you need a carousel, image gallery, slider, or paginated scrolling experience with native browser physics. Use JavaScript carousel libraries when you need infinite looping — CSS scroll-snap does not support it… |
| Pick the right hover/active/focus effect for a button, card, link, or image | [Hover Effects Collection](hover-effects-collection.md) | Use this guide when you need the right hover/active/focus effect for a specific UI element. This is the cookbook companion to [Micro-Interactions](micro-interactions.md), which covers the underlying principles and easing tokens. |
| Create wave dividers, blobs, diagonal sections, or organic shapes | [CSS Shapes & Decorative Geometry](css-shapes.md) | Use `clip-path` when you need precise geometric cuts or responsive curves. Use `border-radius` with uneven values when you need animatable organic blob shapes. |
| Wrap text around a circular image or custom shape (magazine layout) | [Shape Outside & Text Flow](shape-outside.md) | Use `shape-outside` when a client wants the "magazine layout" effect — text flowing around a non-rectangular element. Requires `float`; does not work with flexbox or grid. |
| Apply squircle, scooped, or notched corners | [Corner Shapes](corner-shapes.md) | Use `corner-shape: squircle` for iOS-style superellipse corners on Chrome 2025+. Use `clip-path: polygon()` for notched/beveled corners across all browsers. |
| Animate an element along a curved or circular path | [Motion Path](motion-path.md) | Use `offset-path` when a client wants an element to animate along a curve, orbit, or custom path — loading animations, decorative elements, flight paths. No JavaScript needed. |
| Build a shrinking header, reading progress bar, or back-to-top button without JavaScript | [Scroll-Aware Components](scroll-aware-components.md) | Use scroll-driven animations when a client wants headers that shrink on scroll, progress indicators, or scroll-triggered reveals — all without JavaScript scroll listeners. |
| Create animated counters, circular progress rings, or step indicators | [CSS Counters & Progress](css-counters-progress.md) | Use `@property` + `counter()` for animated counting numbers and SVG `stroke-dashoffset` for progress rings — both without JavaScript counting libraries. |
| Build an accordion without JavaScript | [CSS-Only Accordions](css-only-accordions.md) | Use `<details>`/`<summary>` for all accordion patterns — they handle toggle, accessibility, and keyboard for free. Add animation with the grid height trick (cross-browser) or `interpolate-size` (Chrome 129+). |
| Build a popover or tooltip without JavaScript | [CSS-Only Popovers & Tooltips](css-only-popovers.md) | Use the Popover API (`popover` attribute + `popovertarget`) for click-triggered panels with built-in light dismiss and focus trapping. Use CSS `:hover` + `::after` for simple hover tooltips that need to work everywhere. |
| Build a tab interface or toggle without JavaScript | [CSS-Only Tabs & Toggles](css-only-tabs.md) | Use radio inputs + `:checked` + sibling selectors for CSS-only tab interfaces. Add ARIA roles for accessibility. |
| Create a scrolling text ribbon or logo ticker | [Marquee & Infinite Scroll](marquee-infinite-scroll.md) | Use CSS `@keyframes translateX` with duplicated content for seamless infinite scrolling ribbons. Always pause on hover and respect `prefers-reduced-motion`. |
| Build an asymmetric Apple-style feature grid | [Bento Grid Layouts](bento-grid.md) | Use CSS Grid with `span` values or `grid-template-areas` for bento layouts. Asymmetry (varying tile sizes) is what defines bento — equal-sized tiles are just a grid. |
| Make headlines animate in with slide-up, wipe, or per-character reveals | [Text Reveal Animations](text-reveal.md) | Use CSS `overflow: hidden` + `translateY` for line reveals (no JS). Use a minimal JS text splitter for per-character or per-word reveals — the CSS does the animation, JS only wraps each token in a `<span>`. |
| Animate typography weight or width on hover or scroll | [Variable Font Animation](variable-font-animation.md) | Use `font-variation-settings` transitions for typography that changes weight, width, or slant on interaction. Requires a variable font — standard fonts ignore these properties. |
| Scale font sizes and spacing fluidly across viewports | [Fluid Typography](fluid-typography.md) | Use `clamp()` for font sizes and spacing that scale smoothly between viewport sizes with no jarring breakpoint jumps. Use `cqi` units for component-relative scaling inside container queries. |
| Make an icon or logo draw itself | [SVG Line Draw](svg-line-draw.md) | Use `stroke-dasharray` + `stroke-dashoffset` animation when a client wants icons, logos, or illustrations that draw themselves. Pure CSS on SVG strokes — no JavaScript needed. |
