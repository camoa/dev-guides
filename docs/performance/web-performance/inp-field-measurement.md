---
description: Collect INP subparts and Long Animation Frame data in the field using the web-vitals attribution build.
tldr: Use `web-vitals/attribution` to beacon inputDelay/processingDuration/presentationDelay; Long Animation Frames API (Chrome/Edge only) profiles heavy scripts in production; use `fetchLater` (Chrome/Edge only, polyfill needed) for reliable beacon delivery on page unload.
---

# INP: Field Measurement

## When to Use

> Lab tools (Lighthouse, DevTools) show task durations but miss real-user conditions. Collect INP and its sub-metrics in the field to find the real-world interactions that are slow for actual users. Always measure before you optimize.

## INP Subparts

| Subpart | What it measures | What causes it |
|---------|-----------------|----------------|
| **Input Delay** | Time from user input to event handler starting | Other running JS tasks blocking the main thread |
| **Processing Duration** | Time event handler(s) take to execute | Slow handler code, DOM mutations in the handler |
| **Presentation Delay** | Time from handler end to next frame paint | Heavy rendering work triggered by the handler |

**Start with subparts to diagnose:** input delay → fix scheduler/task splitting; processing duration → fix handler code; presentation delay → fix rendering work (see [CSS Containment Performance](css-containment-performance.md)).

> **LIMITED AVAILABILITY:** Long Animation Frames API — Chrome 123+, Edge 123+ only; no Firefox, no Safari as of June 2026. Safe to use without fallback — ignored in unsupported browsers.

> **LIMITED AVAILABILITY:** `fetchLater` — Chrome 135+, Edge 135+ only; no Firefox, no Safari. Requires polyfill for cross-browser use.

## Pattern: INP with Attribution Build

```javascript
import { onINP } from 'web-vitals/attribution';

onINP((metric) => {
  navigator.sendBeacon('/analytics', JSON.stringify({
    name: 'INP',
    value: metric.value,
    rating: metric.rating,
    inputDelay: metric.attribution.inputDelay,
    processingDuration: metric.attribution.processingDuration,
    presentationDelay: metric.attribution.presentationDelay,
    interactionTarget: metric.attribution.interactionTarget,
    sourceURL: metric.attribution.longestScript.entry?.sourceURL,
    sourceFunctionName: metric.attribution.longestScript.entry?.sourceFunctionName,
  }));
});
```

## Pattern: Long Animation Frames Field Profiling

```javascript
const observer = new PerformanceObserver(list => {
  const allScripts = list.getEntries().flatMap(e => e.scripts);
  const bySource = [...new Set(allScripts.map(s => s.sourceURL))]
    .map(url => ({
      sourceURL: url,
      totalDuration: allScripts
        .filter(s => s.sourceURL === url)
        .reduce((sum, s) => sum + s.duration, 0),
    }))
    .filter(s => s.totalDuration > 100)
    .sort((a, b) => b.totalDuration - a.totalDuration);
  sendToAnalytics({ heavyScripts: bySource });
});
observer.observe({ type: 'long-animation-frame', buffered: true });
```

## Pattern: Reliable Beaconing with fetchLater Polyfill

```javascript
// Install polyfill before any call-sites
globalThis.fetchLater ??= function fetchLater(url, init = {}) {
  function sendNow() {
    if (!(init.signal?.aborted)) {
      fetch(url, { ...init, keepalive: true });
    }
    destroy();
  }
  function destroy() {
    document.removeEventListener('visibilitychange', sendNow);
  }
  if (document.visibilityState === 'hidden') { queueMicrotask(sendNow); }
  else {
    document.addEventListener('visibilitychange', sendNow);
    if (typeof init.activateAfter === 'number')
      setTimeout(sendNow, init.activateAfter);
  }
  return { get activated() { return false; } };
};
```

## Common Mistakes

- **Wrong**: Logging INP locally with `console.log` only → **Right**: Always beacon to a collection endpoint; local logs never reach analytics
- **Wrong**: Using `unload` or `beforeunload` for final beacons → **Right**: Unreliable on mobile; use `fetchLater` or `visibilitychange` to `'hidden'`
- **Wrong**: Sending the full Long Animation Frame entry object → **Right**: Extract only `sourceURL`, `duration`, `invokerType` — the full entry is very large
- **Wrong**: Only measuring in lab (Lighthouse) → **Right**: Lab conditions don't reflect real device capabilities or cached page state

## See Also

- [INP: Scheduler API](inp-scheduler-api.md) — fix the long tasks that field data reveals
- [Core Web Vitals Overview](core-web-vitals-overview.md) — `web-vitals` library for LCP/CLS/TTFB collection
- Reference: [web.dev: Diagnose slow INP](https://web.dev/articles/diagnose-slow-interactions-in-the-field)
- Reference: [web.dev: Long Animation Frames API](https://web.dev/articles/long-animation-frames)
