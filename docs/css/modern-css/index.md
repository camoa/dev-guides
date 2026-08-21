---
description: Modern CSS features from 2022–2025 — container queries, @scope, @layer, scroll-driven animations, view transitions, oklch, and more
tracks: []
guide-meta:
  concepts:
    - container queries
    - "@scope"
    - "@layer"
    - cascade layers
    - scroll-driven animations
    - view transitions
    - oklch
    - color-mix
    - ":has() selector"
    - native CSS nesting
    - popover API
    - anchor positioning
    - "@starting-style"
    - "@property"
    - subgrid
    - light-dark()
    - color-scheme
    - dark mode FOUC
    - scrollbar-color
    - accent-color
    - interpolate-size
    - animate height auto
    - field-sizing
    - scroll snap
    - carousel CSS
    - discrete animations
    - allow-discrete
    - scroll-state container queries
    - "@function"
    - "if()"
    - css mixins
  not:
    - CSS motion/animation craft (easing, micro-interactions)
    - SCSS/Sass features
  requires: []
  complements:
    - css/css-craft
    - design-systems/tailwind
  specializes: ""
  category: css
---

# Modern CSS

Recently-shipped CSS features with decision guidance — when to reach for each, what it replaces, and browser support reality. These features are new enough that training data is sparse; this guide exists to make AI-assisted frontend work accurate.

## Selectors & Logic
- [:has() — Parent & Sibling Selection](has-selector.md)
- [:user-valid / :user-invalid — Interaction-Gated Validation](user-valid-invalid.md)

## Layout
- [Container Queries (@container)](container-queries.md)
- [Container Query Units (cqi, cqw, cqb)](container-units.md)
- [Subgrid](subgrid.md)

## Cascade & Scoping
- [@layer — Cascade Layers](cascade-layers.md)
- [@scope — Scoped Styles](css-scope.md)
- [Native CSS Nesting](native-nesting.md)

## Custom Properties
- [@property — Registered Custom Properties](at-property.md)

## Color
- [oklch() / oklab() — Modern Color Spaces](oklch-color.md)
- [color-mix()](color-mix.md)
- [Relative Color Syntax](relative-color.md)
- [light-dark() — One-Line Dark Mode](light-dark.md)
- [color-scheme & Dark Mode Mechanics](color-scheme-dark-mode.md)

## Animation
- [Scroll-Driven Animations](scroll-driven-animations.md)
- [@starting-style & Discrete Transitions](starting-style-transitions.md)
- [Discrete Property Animations](discrete-animations.md)
- [View Transitions](view-transitions.md)

## Sizing & Layout Behavior
- [interpolate-size — Animate to height: auto](interpolate-size.md)
- [field-sizing: content — Auto-Sizing Form Controls](field-sizing.md)

## Scroll
- [CSS Scroll Snap](scroll-snap.md)
- [Container Scroll-State Queries](container-scroll-state.md)

## Native UI
- [Popover API](popover-api.md)
- [Anchor Positioning](anchor-positioning.md)

## Typography & Units
- [text-wrap: balance / pretty](text-wrap.md)
- [Dynamic Viewport Units (dvh, svh, lvh)](viewport-units.md)

## Native CSS Logic
- [CSS @function, if(), and Upcoming Mixins](css-functions.md)
