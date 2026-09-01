---
description: "Source references and maintenance manifest for the interaction craft guides — web sources, code sources, and version history"
---

# Sources & Maintenance

This guide covers vanilla JS interaction craft — no Drupal-specific or framework-specific code sources. All sources are web references.

## Drupal Research Install
Path: N/A — this guide is framework-agnostic; no Drupal code sources

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| CSS-Tricks: Debouncing and Throttling Explained | https://css-tricks.com/debouncing-throttling-explained-examples/ | debounce-and-throttle | 2026-03-04 |
| Go Make Things: Debouncing with rAF | https://gomakethings.com/debouncing-events-with-requestanimationframe-for-better-performance/ | debounce-and-throttle | 2026-03-04 |
| MDN: requestAnimationFrame | https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame | debounce-and-throttle, animation-orchestration | 2026-03-04 |
| W3C APG: Keyboard Interface | https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/ | keyboard-navigation-craft | 2026-03-04 |
| MDN: Keyboard-navigable JS widgets | https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Keyboard-navigable_JavaScript_widgets | keyboard-navigation-craft | 2026-03-04 |
| Adrian Roselli: Modal Focus Placement | https://adrianroselli.com/2025/06/where-to-put-focus-when-opening-a-modal-dialog.html | keyboard-navigation-craft | 2026-03-04 |
| W3C: Modal Dialog Example (APG) | https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/examples/dialog/ | keyboard-navigation-craft | 2026-03-04 |
| MDN: Intersection Observer API | https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API | scroll-interaction-patterns | 2026-03-04 |
| MDN: History.scrollRestoration | https://developer.mozilla.org/en-US/docs/Web/API/History/scrollRestoration | scroll-interaction-patterns | 2026-03-04 |
| ITNEXT: IntersectionObserver vs Scroll Events performance | https://itnext.io/1v1-scroll-listener-vs-intersection-observers-469a26ab9eb6 | scroll-interaction-patterns, debounce-and-throttle | 2026-03-04 |
| MDN: HTML Drag and Drop API | https://developer.mozilla.org/en-US/docs/Web/API/HTML_Drag_and_Drop_API | drag-and-drop-craft | 2026-03-04 |
| W3C: WCAG 2.5.7 Dragging Movements | https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html | drag-and-drop-craft | 2026-03-04 |
| GitHub Blog: Accessible Sortable List | https://github.blog/engineering/user-experience/exploring-the-challenges-in-creating-an-accessible-sortable-list-drag-and-drop/ | drag-and-drop-craft | 2026-03-04 |
| Salesforce: Accessible DnD Patterns | https://salesforce-ux.github.io/dnd-a11y-patterns/ | drag-and-drop-craft | 2026-03-04 |
| JS Plain English: Optimistic UI Architecture | https://javascript.plainenglish.io/optimistic-ui-in-frontend-architecture-do-it-right-avoid-pitfalls-7507d713c19c | optimistic-ui | 2026-03-04 |
| MDN: Pinch Zoom with Pointer Events | https://developer.mozilla.org/en-US/docs/Web/API/Pointer_events/Pinch_zoom_gestures | touch-and-gesture-craft | 2026-03-04 |
| Chrome Developers: 300ms Tap Delay Gone | https://developer.chrome.com/blog/300ms-tap-delay-gone-away | touch-and-gesture-craft | 2026-03-04 |
| MDN: Navigator.clipboard | https://developer.mozilla.org/en-US/docs/Web/API/Navigator/clipboard | clipboard-and-copy-patterns | 2026-03-04 |
| SitePoint: Clipboard API | https://www.sitepoint.com/clipboard-api/ | clipboard-and-copy-patterns | 2026-03-04 |
| Smashing Magazine: Inline Validation UX | https://www.smashingmagazine.com/2022/09/inline-validation-web-forms-ux/ | form-interaction-craft | 2026-03-04 |
| MDN: Using the Web Animations API | https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API/Using_the_Web_Animations_API | animation-orchestration | 2026-03-04 |
| CSS-Tricks: CSS Animations vs WAAPI | https://css-tricks.com/css-animations-vs-web-animations-api/ | animation-orchestration | 2026-03-04 |
| web.dev: Optimize Long Tasks | https://web.dev/articles/optimize-long-tasks | performance-and-event-handling | 2026-03-04 |
| Chrome Developers: scheduler.yield | https://developer.chrome.com/blog/use-scheduler-yield | performance-and-event-handling | 2026-03-04 |
| MDN: Scheduler.yield() | https://developer.mozilla.org/en-US/docs/Web/API/Scheduler/yield | performance-and-event-handling | 2026-03-04 |
| LogRocket: Event Delegation Deep Dive | https://blog.logrocket.com/deep-internals-event-delegation/ | performance-and-event-handling | 2026-03-04 |
| DEV: Avoiding Event Listener Memory Leaks | https://dev.to/alex_aslam/how-to-avoid-memory-leaks-in-javascript-event-listeners-4hna | performance-and-event-handling | 2026-03-04 |
| DebugBear: Getting Started with scheduler.yield | https://www.debugbear.com/blog/scheduler-yield | performance-and-event-handling | 2026-03-04 |

## Code Sources
None — this guide is framework-agnostic and references only web standards and MDN documentation.

## Cross-Guide References
| This Guide Section | References | Other Guide Section |
|---|---|---|
| debounce-and-throttle | css-craft.md | animation-performance |
| keyboard-navigation-craft | css-craft.md | accessibility-and-motion |
| scroll-interaction-patterns | css-craft.md | entrance-animations, parallax-effects |
| optimistic-ui | css-craft.md | skeleton-and-loading-states |
| animation-orchestration | css-craft.md | spring-physics-and-advanced-easing, animation-performance |
