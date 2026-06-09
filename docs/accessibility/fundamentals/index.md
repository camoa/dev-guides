---
description: Accessibility Fundamentals — landmarks, ARIA, accessible names, keyboard, live regions, forms, media, color, motion, dialogs, metadata, and testing.
guide-meta:
  concepts:
    - accessibility
    - WCAG
    - ARIA
    - landmarks
    - skip links
    - screen reader
    - keyboard navigation
    - focus management
    - live regions
    - aria-live
    - forms accessibility
    - aria-invalid
    - user-invalid
    - alt text
    - color contrast
    - prefers-reduced-motion
    - native dialog
    - document language
    - axe-core
    - VoiceOver
    - NVDA
    - JAWS
    - inert
    - visually-hidden
  not:
    - WCAG audit methodology
    - accessibility testing tools comparison
    - procurement accessibility
  requires: []
  complements:
    - js/interaction-craft
    - css/css-craft
  specializes: ""
  category: accessibility
---

# Accessibility Fundamentals

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Structure pages with landmarks and headings | [Semantic Structure](semantic-structure.md) | Use `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` and `<h1>`–`<h6>` in strict sequence; add a skip link targeting `<main tabindex="-1">`; never label every `<section>` as a region landmark — more than 6–8 landmarks dilutes their value. |
| Decide when ARIA is and isn't appropriate | [ARIA Usage](aria-usage.md) | Use native HTML elements first (`<button>`, `<nav>`, `<ul>`); apply ARIA only when no native equivalent exists; when you set an ARIA role you MUST implement its full keyboard behavior or the result is worse than no ARIA at all. |
| Name interactive elements and landmarks | [Accessible Names](accessible-names.md) | Use `<label for="id">` for inputs, `<caption>` for tables, `<figcaption>` for figures; prefer `aria-labelledby` over `aria-label` when visible text exists — it survives translation and never goes stale. |
| Handle keyboard navigation and focus | [Keyboard and Focus](keyboard-and-focus.md) | Every action reachable by mouse must be reachable by keyboard; use `:focus-visible` with sufficient contrast; never use positive `tabindex` values; `aria-hidden="true"` on a focusable element creates an invisible focus trap. |
| Announce dynamic content changes | [Live Regions](live-regions.md) | Maintain two centralized live regions (one polite, one assertive) rather than scattering them per component; use `assertive` only for critical time-sensitive events; clear then set on next animation frame to guarantee re-announcement. |
| Build accessible forms with error handling | [Forms Accessibility](forms-accessibility.md) | Use `<label for="id">` for every input, `aria-describedby` for hints, `aria-errormessage`+`aria-invalid` for errors; bridge CSS `:user-invalid` to `aria-invalid` via JS so errors only announce after the user has interacted with the field. |
| Write alt text and caption media | [Media Alternatives](media-alternatives.md) | Calibrate alt text to context — functional images describe the action, informative images describe meaning, decorative images get `alt=""`; inline SVGs need `role="img"` + `<title>` when informative; never apply `aria-hidden="true"` to a focusable element. |
| Meet contrast and typography requirements | [Color and Typography](color-and-typography.md) | Normal text needs 4.5:1 contrast (WCAG AA), UI component boundaries need 3:1; use `rem`/`em` for font sizing (never `px`); always pair color-coded states with an icon or text label. |
| Respect reduced-motion preferences | [Motion Preferences](motion-preferences.md) | Default page state should be static — scope animations inside `@media (prefers-reduced-motion: no-preference)`; slowing down a spinning animation is not sufficient — motion itself is the trigger for vestibular disorders; never exceed 3 flashes/second. |
| Implement modal dialogs correctly | [Native Dialog](native-dialog.md) | Use `<dialog>.showModal()` for modals — the browser makes background content inert and handles Escape; never add a custom JS focus trap to a native modal; `inert` overlay must be a sibling not a descendant of the inerted element. |
| Set page language, title, and SPA metadata | [Document Metadata](document-metadata.md) | Declare `<html lang="en">`, front-load unique context in `<title>` ("Page Topic | Site Name"), and on SPA route changes update `document.title` and move focus to the new `<h1>` or `<main tabindex="-1">`. |
| Test with automated tools and screen readers | [Accessibility Testing](accessibility-testing.md) | Automated tools (axe-core, Lighthouse) catch only ~30–40% of issues — supplement with keyboard-only testing and canonical screen-reader pairings: JAWS+Chrome, NVDA+Firefox, VoiceOver+Safari. |
