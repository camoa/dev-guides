# Design: Interaction Craft + Image & Media Craft Guides

**Date:** 2026-03-04
**Status:** Approved
**Approach:** Parallel research and creation (Option A)

## Context

The css-craft guide covers CSS execution craft — making things look alive via CSS. Two companion guides are needed for the JS interaction layer and the image/media pipeline layer. The design-intelligence plugin covers *design decisions* (what style, what treatment) — these guides cover *execution craft* (how to implement it well).

## Guide 1: `interaction-craft.md`

**Scope:** Vanilla JS execution craft. Framework-agnostic. No Drupal/React/Alpine specifics.

**Cross-references:** css-craft (for CSS animation counterparts), NOT design-intelligence plugin content.

### Partitions

| Partition | Coverage | Cross-refs |
|---|---|---|
| `debounce-and-throttle` | When to use which, timing values, scroll/resize/input patterns, implementation | css-craft → animation-performance |
| `keyboard-navigation-craft` | Focus trapping, roving tabindex, arrow-key patterns, skip links, focus restoration | css-craft → accessibility-and-motion |
| `scroll-interaction-patterns` | IntersectionObserver orchestration, scroll-linked state, infinite scroll, scroll-snap JS enhancement | css-craft → entrance-animations, parallax |
| `drag-and-drop-craft` | Native drag API vs pointer events, visual feedback, drop zones, reorder UX, touch support | — |
| `optimistic-ui` | Instant feedback, rollback patterns, pending states, error recovery | css-craft → skeleton-and-loading-states |
| `touch-and-gesture-craft` | Swipe detection, pinch-zoom, long-press, touch vs mouse discrimination, passive listeners | — |
| `clipboard-and-copy-patterns` | Copy-to-clipboard feedback, paste handling, selection highlights | — |
| `form-interaction-craft` | Validation timing (blur vs submit vs realtime), input masking, auto-resize textareas, autosave | — |
| `animation-orchestration` | Sequencing JS + CSS, WAAPI basics, canceling/interrupting, promise-based chaining | css-craft → spring-physics |
| `performance-and-event-handling` | Passive listeners, requestAnimationFrame, event delegation, avoiding layout thrashing | css-craft → animation-performance |

## Guide 2: `image-media-craft.md`

**Scope:** Full media pipeline — build-time optimization through loading craft to visual effects. Includes Drupal-specific section.

**Cross-references:** css-craft (for visual effects), drupal-media.md, drupal-image-styles.md. NOT design-intelligence plugin (that covers art direction/treatment decisions).

### Partitions

| Partition | Coverage | Cross-refs |
|---|---|---|
| `responsive-images-craft` | `<picture>`, `srcset`, `sizes`, art direction, breakpoint strategy, density descriptors | drupal-image-styles |
| `image-format-strategy` | WebP vs AVIF vs JPEG, when to use which, quality settings, fallback chains | — |
| `loading-and-decode-craft` | `loading="lazy"`, `decoding="async"`, `fetchpriority`, LCP optimization, above-fold strategy | — |
| `placeholder-strategies` | blur-up (LQIP), dominant-color, skeleton, thumb-hash, aspect-ratio preservation, CLS prevention | css-craft → skeleton-and-loading-states |
| `video-and-embed-craft` | Lazy video, poster frames, facade pattern (YouTube/Vimeo), autoplay policies, `<video>` attributes | — |
| `svg-craft` | Inline vs `<img>`, icon systems, animated SVG, accessibility (title/desc/role), currentColor | — |
| `image-effects-craft` | object-fit/position mastery, reveal animations, comparison sliders, lightbox patterns | css-craft → clip-path, blend-modes |
| `build-pipeline-optimization` | Image optimization tooling, CDN strategies, responsive breakpoint generation, automated compression | — |
| `drupal-media-pipeline` | Responsive image styles, media library, focal point, image styles vs responsive styles, conversion workflow, what Drupal gives OOTB | drupal-media, drupal-image-styles |

## Decisions

- **Interaction Craft:** Vanilla JS only, no framework adapters
- **Image & Media Craft:** One guide with Drupal section (not two separate guides)
- **Execution:** Both guides researched and written in parallel by guide-framework-maintainer agents
- **Publishing:** Partitioned and pushed together after both complete
