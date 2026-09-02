---
description: "Reference table for LCP, INP, CLS, and TTFB thresholds with the web-vitals library collection pattern."
tldr: "Use to decide which Core Web Vital to investigate first and how to collect real-user data; INP replaced FID in March 2024; always confirm fixes in CrUX field data, not just Lighthouse lab scores."
---

# Core Web Vitals Overview

## When to Use

> Use this section to understand which metric to investigate first and how to collect real-user data. LCP, INP, and CLS are the three Core Web Vitals Google uses for Search ranking. TTFB is an informational diagnostic metric — not a Core Web Vital itself but the first signal when a server or CDN is the bottleneck.

## Metrics Reference

#### LCP — Largest Contentful Paint
**Measures:** How long until the largest visible text or image block renders.
**Thresholds:** Good ≤2.5s | Needs improvement ≤4.0s | Poor >4.0s
**Primary causes of poor LCP:** Render-blocking resources, slow server response (TTFB), unoptimized LCP image (missing `fetchpriority`, JS-rendered element, lazy-loaded).
**Fix first in:** [Critical Rendering Path](critical-rendering-path.md), [LCP Image Optimization](lcp-image-optimization.md).

#### INP — Interaction to Next Paint
**Measures:** The worst-case interaction latency across the full page lifecycle. Replaced FID in March 2024.
**Thresholds:** Good ≤200ms | Needs improvement ≤500ms | Poor >500ms
**Primary causes of poor INP:** Long JS tasks blocking the main thread, excessive rendering work after interaction.
**Fix first in:** [INP: Scheduler API](inp-scheduler-api.md). Diagnose in: [INP: Field Measurement](inp-field-measurement.md).

#### CLS — Cumulative Layout Shift
**Measures:** Unexpected visual instability — how much content jumps around as the page loads.
**Thresholds:** Good ≤0.1 | Needs improvement ≤0.25 | Poor >0.25
**Primary causes of poor CLS:** Images without `width`/`height`, web fonts swapping (FOUT), dynamically injected content above existing content, `content-visibility` without `contain-intrinsic-size`.
**Fix first in:** [LCP Image Optimization](lcp-image-optimization.md) (image dimensions), [Web Font Performance](web-font-performance.md), [CSS Containment Performance](css-containment-performance.md).

#### TTFB — Time to First Byte
**Measures:** Time from request to first byte of HTML response. Infrastructure metric, not a Core Web Vital.
**Thresholds:** Good ≤800ms | Needs improvement ≤1800ms | Poor >1800ms
**Primary causes:** Slow origin server, uncached dynamic pages, long redirect chains, poor CDN configuration.
**Fix at:** Server/CDN layer — outside the scope of this guide.

## Field vs Lab Data

| Data type | Tools | What it tells you |
|-----------|-------|-------------------|
| **Field (RUM)** | Chrome UX Report (CrUX), `web-vitals` library, PageSpeed Insights | Real-user devices, networks, interactions. Use for Google Search ranking signals. |
| **Lab (Synthetic)** | Lighthouse, WebPageTest, Chrome DevTools Performance panel | Repeatable, controllable. Use for debugging specific issues, not for ranking. |

**Rule:** Always confirm fixes improve field data — lab scores do not directly determine Search ranking.

## The `web-vitals` Library

The official Google library for collecting CWV in the field with minimal overhead.

```javascript
// Basic build — collect and beacon all Core Web Vitals
import { onLCP, onINP, onCLS, onTTFB } from 'web-vitals';

function sendToAnalytics(metric) {
  navigator.sendBeacon('/analytics', JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,  // 'good' | 'needs-improvement' | 'poor'
    id: metric.id,
  }));
}

onLCP(sendToAnalytics);
onINP(sendToAnalytics);
onCLS(sendToAnalytics);
onTTFB(sendToAnalytics);
```

Use the attribution build (`web-vitals/attribution`) to get INP subparts and Long Animation Frame data. See [INP: Field Measurement](inp-field-measurement.md) for the full pattern.

## Common Mistakes

- Optimizing only for Lighthouse scores without checking CrUX field data — Lighthouse runs in a controlled lab environment and misses real-user device/network conditions
- Treating all three CWV equally — prioritize the one with the worst field rating first; usually LCP or INP
- Forgetting that CWV signals affect Google Search ranking — fixes need to propagate to field data to impact ranking
- Using `onFID` (deprecated in web-vitals v4.0.0, removed in v5.0.0) — INP replaced FID; update any legacy RUM implementations

## See Also

- [INP: Field Measurement](inp-field-measurement.md) — collecting INP subparts and attribution in the field
- Reference: [web-vitals npm package](https://github.com/GoogleChrome/web-vitals)
- Reference: [web.dev Core Web Vitals](https://web.dev/articles/vitals)
