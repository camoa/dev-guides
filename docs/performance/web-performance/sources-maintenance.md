---
description: "Source references and maintenance manifest for the web performance guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Path: N/A — this guide covers web platform APIs only; no Drupal-specific code referenced.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| MWG: performance.md (root) | /tmp/mwg/performance/performance.md | All sections | 2026-06-09 |
| MWG: break-up-long-tasks.md | /tmp/mwg/performance/break-up-long-tasks.md | inp-scheduler-api | 2026-06-09 |
| MWG: identify-inp-causes.md | /tmp/mwg/performance/identify-inp-causes.md | inp-field-measurement | 2026-06-09 |
| MWG: identify-heavy-scripts.md | /tmp/mwg/performance/identify-heavy-scripts.md | inp-field-measurement | 2026-06-09 |
| MWG: optimize-script-priority.md | /tmp/mwg/performance/optimize-script-priority.md | resource-hints, critical-rendering-path | 2026-06-09 |
| MWG: optimize-preload-priority.md | /tmp/mwg/performance/optimize-preload-priority.md | resource-hints | 2026-06-09 |
| MWG: optimize-image-priority.md | /tmp/mwg/performance/optimize-image-priority.md | lcp-image-optimization | 2026-06-09 |
| MWG: schedule-tasks-by-priority.md | /tmp/mwg/performance/schedule-tasks-by-priority.md | inp-scheduler-api | 2026-06-09 |
| MWG: defer-rendering-heavy-content.md | /tmp/mwg/performance/defer-rendering-heavy-content.md | css-containment-performance | 2026-06-09 |
| MWG: efficient-background-processing.md | /tmp/mwg/performance/efficient-background-processing.md | css-containment-performance | 2026-06-09 |
| MWG: faster-spa-view-transitions.md | /tmp/mwg/performance/faster-spa-view-transitions.md | css-containment-performance | 2026-06-09 |
| MWG: interactions-in-complex-layouts.md | /tmp/mwg/performance/interactions-in-complex-layouts.md | css-containment-performance | 2026-06-09 |
| MWG: conditional-async-dependencies.md | /tmp/mwg/performance/conditional-async-dependencies.md | code-splitting | 2026-06-09 |
| MWG: improve-next-page-load-performance.md | /tmp/mwg/performance/improve-next-page-load-performance.md | code-splitting | 2026-06-09 |
| MWG: batch-analytics-events.md | /tmp/mwg/performance/batch-analytics-events.md | inp-field-measurement | 2026-06-09 |
| MWG: full-session-analytics.md | /tmp/mwg/performance/full-session-analytics.md | inp-field-measurement | 2026-06-09 |
| MWG: defer-work-until-scroll-ends.md | /tmp/mwg/performance/defer-work-until-scroll-ends.md | inp-scheduler-api | 2026-06-09 |
| MWG: deprioritize-background-fetches.md | /tmp/mwg/performance/deprioritize-background-fetches.md | resource-hints | 2026-06-09 |
| MWG: detect-initial-visibility-state.md | /tmp/mwg/performance/detect-initial-visibility-state.md | inp-field-measurement | 2026-06-09 |
| MWG: calculate-total-foreground-time.md | /tmp/mwg/performance/calculate-total-foreground-time.md | inp-field-measurement | 2026-06-09 |
| MWG: resolution-optimized-pseudo-elements.md | /tmp/mwg/performance/resolution-optimized-pseudo-elements.md | lcp-image-optimization | 2026-06-09 |
| MWG: sequence-distributed-events.md | /tmp/mwg/performance/sequence-distributed-events.md | inp-field-measurement (reference only) | 2026-06-09 |
| web-vitals library (Google) | https://github.com/GoogleChrome/web-vitals | core-web-vitals-overview, inp-field-measurement | 2026-06-09 |
| web.dev: Core Web Vitals | https://web.dev/articles/vitals | core-web-vitals-overview | 2026-06-09 |
| web.dev: Fetch Priority | https://web.dev/articles/fetch-priority | resource-hints, lcp-image-optimization | 2026-06-09 |
| web.dev: Optimize LCP | https://web.dev/articles/optimize-lcp | lcp-image-optimization | 2026-06-09 |
| web.dev: Optimize Long Tasks | https://web.dev/articles/optimize-long-tasks | inp-scheduler-api | 2026-06-09 |
| web.dev: Diagnose slow INP | https://web.dev/articles/diagnose-slow-interactions-in-the-field | inp-field-measurement | 2026-06-09 |
| web.dev: Long Animation Frames | https://web.dev/articles/long-animation-frames | inp-field-measurement | 2026-06-09 |
| web.dev: content-visibility | https://web.dev/articles/content-visibility | css-containment-performance | 2026-06-09 |
| Workbox documentation | https://developer.chrome.com/docs/workbox/ | service-worker-caching | 2026-06-09 |
| web.dev: Font best practices | https://web.dev/articles/font-best-practices | web-font-performance | 2026-06-09 |
| web.dev: CSS size-adjust | https://web.dev/articles/css-size-adjust | web-font-performance | 2026-06-09 |
| Speculation Rules API | https://developer.chrome.com/docs/web-platform/prerender-pages | code-splitting | 2026-06-09 |

## Code Sources

| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| workbox-routing | npm package | service-worker-caching | workbox 7.x |
| workbox-strategies | npm package | service-worker-caching | workbox 7.x |
| workbox-expiration | npm package | service-worker-caching | workbox 7.x |
| workbox-cacheable-response | npm package | service-worker-caching | workbox 7.x |

## Limited-Availability API Flags

The following APIs are flagged as limited-availability in the MWG source files and require fallbacks or feature detection:

| API | Support as of MWG source | Fallback documented in |
|-----|--------------------------|----------------------|
| `scheduler.yield()` | Chrome 129+, Edge 129+, Firefox 142+; NO Safari | inp-scheduler-api |
| `scheduler.postTask()` | Chrome 129+, Edge 129+, Firefox 142+; NO Safari | inp-scheduler-api |
| Long Animation Frames (`long-animation-frame`) | Chrome 123+, Edge 123+; NO Firefox, NO Safari | inp-field-measurement |
| `fetchLater()` | Chrome 135+, Edge 135+; NO Firefox, NO Safari | inp-field-measurement |
| Speculation Rules API | Chrome + Edge only; NO Firefox, NO Safari | code-splitting |
| `VisibilityStateEntry` (`visibility-state` perf entries) | Chrome 115+, Edge 115+; NO Firefox, NO Safari | inp-field-measurement |
| `Temporal` API | Chrome 144+, Edge 144+, Firefox 139+; NO Safari | Not included in main sections; referenced in MWG source |

Verify all Baseline statuses at [web.dev/baseline](https://web.dev/baseline) before production reliance — browser support changes regularly.
