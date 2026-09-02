---
description: "Collect INP subparts and Long Animation Frame data in the field using the web-vitals attribution build."
tldr: "Use `web-vitals/attribution` to beacon inputDelay/processingDuration/presentationDelay; Long Animation Frames API (Chrome/Edge only) profiles heavy scripts in production; use `fetchLater` (Chrome/Edge only, polyfill needed) for reliable beacon delivery on page unload."
---

# INP: Field Measurement

## When to Use

> Lab tools (Lighthouse, DevTools) show task durations but miss real-user conditions — actual device capabilities, cached state, user interaction patterns. Collect INP and its sub-metrics in the field to find the real-world interactions that are slow for actual users. Always measure before you optimize.

## INP Subparts

The Event Timing API splits INP duration into three phases:

| Subpart | What it measures | What causes it |
|---------|-----------------|----------------|
| **Input Delay** | Time from user input to event handler starting | Other running JS tasks blocking the main thread when the interaction fires |
| **Processing Duration** | Time the event handler(s) take to execute | Slow event handler code, DOM mutations in the handler |
| **Presentation Delay** | Time from handler end to next frame paint | Heavy rendering work (layout, paint) triggered by the handler |

**Start with subparts to diagnose:** input delay → fix scheduler/task splitting; processing duration → fix handler code; presentation delay → fix rendering work (see [CSS Containment Performance](css-containment-performance.md)).

**Baseline for Event Timing API:** Newly Available since 2025-12-12. Supported: Chrome 76+, Edge 79+, Firefox 89+, Safari 26.2+.

## Pattern: Collect INP with web-vitals Attribution Build

```javascript
import { onINP } from 'web-vitals/attribution';

onINP((metric) => {
  navigator.sendBeacon('/analytics', JSON.stringify({
    name: 'INP',
    value: metric.value,          // ms
    rating: metric.rating,        // 'good' | 'needs-improvement' | 'poor'
    // Subparts — identify which phase is slow
    inputDelay: metric.attribution.inputDelay,
    processingDuration: metric.attribution.processingDuration,
    presentationDelay: metric.attribution.presentationDelay,
    // Which element was interacted with
    interactionTarget: metric.attribution.interactionTarget,
    // Long Animation Frame data — which script caused the delay
    invokerType: metric.attribution.longestScript.entry?.invokerType,
    sourceURL: metric.attribution.longestScript.entry?.sourceURL,
    sourceFunctionName: metric.attribution.longestScript.entry?.sourceFunctionName,
    subpart: metric.attribution.longestScript.subpart,
    intersectingDuration: metric.attribution.longestScript.intersectingDuration,
  }));
});
```

## Pattern: Long Animation Frames API (Field Profiling)

Use this for identifying heavy-running scripts in the field. More lightweight than the JS Self-Profiling API.

> **LIMITED AVAILABILITY — Long Animation Frames API:** Chrome 123+, Edge 123+ only; **not supported in Firefox or Safari** as of June 2026. Safe to use without fallback — ignored in unsupported browsers. Verify current support at [web.dev/baseline](https://web.dev/baseline) before production reliance.

```javascript
const allScripts = [];

const observer = new PerformanceObserver(list => {
  allScripts.push(...list.getEntries().flatMap(e => e.scripts));

  // Aggregate by sourceURL to find cumulative offenders
  const bySource = [...new Set(allScripts.map(s => s.sourceURL))]
    .map(url => ({
      sourceURL: url,
      count: allScripts.filter(s => s.sourceURL === url).length,
      totalDuration: allScripts
        .filter(s => s.sourceURL === url)
        .reduce((sum, s) => sum + s.duration, 0),
    }))
    .filter(s => s.totalDuration > 100)  // noise threshold
    .sort((a, b) => b.totalDuration - a.totalDuration);

  // In production: beacon to analytics. In dev: log.
  sendToAnalytics({ heavyScripts: bySource });
});

observer.observe({ type: 'long-animation-frame', buffered: true });
```

## Pattern: Reliable Analytics Beaconing with fetchLater

`navigator.sendBeacon` has reliability issues on page unload (especially mobile). `fetchLater` queues a deferred fetch that the browser delivers even if the page is closed before the timeout.

> **LIMITED AVAILABILITY — fetchLater:** Chrome 135+, Edge 135+ only; **not supported in Firefox or Safari** as of June 2026. Requires polyfill for cross-browser use. Verify current support at [web.dev/baseline](https://web.dev/baseline) before production reliance.

```javascript
// Install polyfill before any call-sites
globalThis.fetchLater ??= function fetchLater(url, init = {}) {
  let timeoutHandle, activated = false;
  function sendNow() {
    if (!(init.signal?.aborted)) {
      if ('keepalive' in Request.prototype || init.method !== 'POST' || init.headers) {
        fetch(url, { ...init, keepalive: true });
        activated = true;
      } else { activated = navigator.sendBeacon(url, init.body); }
    }
    destroy();
  }
  function destroy() {
    document.removeEventListener('visibilitychange', sendNow);
    clearTimeout(timeoutHandle);
  }
  if (document.visibilityState === 'hidden') { queueMicrotask(sendNow); }
  else {
    document.addEventListener('visibilitychange', sendNow);
    if (typeof init.activateAfter === 'number') timeoutHandle = setTimeout(sendNow, init.activateAfter);
  }
  if (init.signal) init.signal.addEventListener('abort', destroy);
  return { get activated() { return activated; } };
};

// Batch analytics events within a 10-second window
const BATCH_WINDOW = 10_000;
const eventQueue = [];
let flc = null, flr = null;

function trackEvent(data) {
  if (flr?.activated || eventQueue.length > 100) {
    flc = null; flr = null; eventQueue.length = 0;
  }
  eventQueue.push(data);
  flc?.abort();
  flc = new AbortController();
  try {
    flr = fetchLater('/analytics', {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify(eventQueue),
      signal: flc.signal,
      activateAfter: BATCH_WINDOW,
    });
  } catch (_) { /* quota exceeded */ }
}
```

## Measuring Page Visibility for Analytics Accuracy

Pages loaded in background tabs have artificially inflated LCP/FCP. Use `VisibilityStateEntry` to filter them.

> **LIMITED AVAILABILITY — VisibilityStateEntry:** Chrome 115+, Edge 115+ only; **not supported in Firefox or Safari** as of June 2026. Falls back gracefully (returns empty array). Verify current support at [web.dev/baseline](https://web.dev/baseline) before production reliance.

```javascript
function wasInitiallyBackgrounded() {
  const entries = performance.getEntriesByType('visibility-state');
  if (entries.length === 0) return false;  // API unsupported; assume foreground
  return entries[0].name === 'hidden';
}
// Filter out background-loaded pages before computing CWV averages
```

## Common Mistakes

- Logging INP locally with `console.log` only — production data never reaches analytics; always beacon to a collection endpoint
- Using `unload` or `beforeunload` event listeners for final beacons — unreliable on mobile (page is killed, not unloaded); use `fetchLater` or `visibilitychange` to `'hidden'`
- Sending the full Long Animation Frame entry object — it is very large; extract only `sourceURL`, `duration`, `invokerType` and relevant subpart
- Only measuring in lab (Lighthouse) — lab conditions don't reflect real device capabilities or cached page state

## See Also

- [INP: Scheduler API](inp-scheduler-api.md) — fix the long tasks that field data reveals
- [Core Web Vitals Overview](core-web-vitals-overview.md) — the `web-vitals` library for LCP/CLS/TTFB collection
- Reference: [web.dev: Diagnose slow INP](https://web.dev/articles/find-slow-interactions-in-the-field)
- Reference: [web.dev: Long Animation Frames API](https://developer.chrome.com/docs/web-platform/long-animation-frames)
