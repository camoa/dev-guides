---
description: Reference table for LCP, INP, CLS, and TTFB thresholds with the web-vitals library collection pattern.
tldr: Use when diagnosing which Core Web Vital to investigate first; INP replaced FID in March 2024; always confirm fixes in CrUX field data, not just Lighthouse lab scores.
---

# Core Web Vitals Overview

## When to Use

> Use this section to understand which metric to investigate first and how to collect real-user data. LCP, INP, and CLS are the three Core Web Vitals Google uses for Search ranking. TTFB is an informational diagnostic metric — not a Core Web Vital itself but the first signal when a server or CDN is the bottleneck.

## Decision

| Metric | Measures | Good | Needs Improvement | Poor |
|--------|----------|------|-------------------|------|
| **LCP** | Largest visible text or image block renders | ≤2.5s | ≤4.0s | >4.0s |
| **INP** | Worst-case interaction latency (replaced FID March 2024) | ≤200ms | ≤500ms | >500ms |
| **CLS** | Cumulative unexpected visual instability | ≤0.1 | ≤0.25 | >0.25 |
| **TTFB** | Time to first byte — server/CDN metric, not a CWV | ≤800ms | ≤1800ms | >1800ms |

| Data type | Tools | What it tells you |
|-----------|-------|-------------------|
| **Field (RUM)** | CrUX, `web-vitals` library, PageSpeed Insights | Real-user devices, networks, interactions. Use for Search ranking signals. |
| **Lab (Synthetic)** | Lighthouse, WebPageTest, DevTools Performance | Repeatable, controllable. Use for debugging, not for ranking. |

**Rule:** Always confirm fixes improve field data — lab scores do not directly determine Search ranking.

## Pattern

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

Use the attribution build (`web-vitals/attribution`) for INP subparts and Long Animation Frame data — see [INP: Field Measurement](inp-field-measurement.md).

## Common Mistakes

- **Wrong**: Optimizing only for Lighthouse scores without checking CrUX → **Right**: Verify fixes in field data; Lighthouse misses real device/network conditions
- **Wrong**: Treating all three CWV equally → **Right**: Prioritize the metric with the worst field rating first (usually LCP or INP)
- **Wrong**: Using `onFID` (removed in web-vitals v4) → **Right**: Switch to `onINP`; INP replaced FID

## See Also

- [INP: Field Measurement](inp-field-measurement.md) — collecting INP subparts and attribution in the field
- Reference: [web-vitals npm package](https://github.com/GoogleChrome/web-vitals)
- Reference: [web.dev Core Web Vitals](https://web.dev/articles/vitals)
