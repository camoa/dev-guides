---
description: "Eliminate render-blocking CSS and JS from the critical path using inline styles, defer/async, and media attributes."
tldr: "Inline only above-fold CSS (~14KB target), use `<script defer>` for app JS and `<script async>` for independent scripts; CSS `@import` inside stylesheets creates sequential request chains that block CSSOM — replace with parallel `<link>` tags."
---

# Critical Rendering Path

## When to Use

> Apply these patterns to every page. The critical rendering path (CRP) is the sequence of steps the browser takes from receiving the HTML to painting pixels. Any render-blocking resource in the `<head>` delays the first paint — often by hundreds of milliseconds before a single pixel appears.

## Decision

| Resource | Default behavior | Recommended |
|----------|-----------------|-------------|
| Critical above-fold CSS | Normally linked → blocks render | Inline in `<style>` in `<head>` |
| Non-critical CSS (e.g., below-fold, print) | Blocks render if in `<link>` | `rel=preload` + `onload` swap, or `media` attribute |
| App JS with DOM dependency | Parser-blocking if in `<head>` | `<script defer>` — executes after DOM, in order |
| Independent utility JS | Parser-blocking if in `<head>` | `<script async>` — no guaranteed order |
| Modern ES modules | Parser-blocking if in `<head>` | `<script type="module">` — deferred by default; add `async` for independent modules |
| Third-party scripts (analytics, chat) | Often in `<head>`, parser-blocking | `<script defer>` near end of `<body>`, or `async` |
| CSS `@import` inside stylesheets | Sequential request chain | Replace with `<link>` tags — download in parallel |

## Pattern

```html
<!-- 1. Inline only the CSS needed for above-fold paint -->
<style>
  body { margin: 0; font-family: system-ui; }
  .hero { min-height: 100svh; display: grid; }
</style>

<!-- 2. Defer non-critical CSS via preload → stylesheet swap -->
<link rel="preload" href="/css/app.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="/css/app.css"></noscript>

<!-- 3. Media-split CSS: non-matching query is downloaded but non-blocking -->
<link rel="stylesheet" href="/css/print.css" media="print">

<!-- 4. App JS: defer preserves execution order -->
<script defer src="/js/app.js"></script>

<!-- 5. ES module: deferred by default -->
<script type="module" src="/js/components.js"></script>

<!-- 6. Independent analytics: async, fetchpriority low -->
<script async fetchpriority="low" src="/js/analytics.js"></script>
```

## Common Mistakes

- `@import url('other.css')` inside CSS files — creates sequential request chains that block CSSOM; replace with parallel `<link>` tags
- Large framework bundle in `<head>` without `defer` or `async` — halts DOM construction until download + parse + execute completes
- Inlining all CSS — defeats HTTP caching; inline only the minimum above-fold styles (~14KB uncompressed is a useful target)
- Using `defer` on scripts that use `document.write()` — deferred scripts cannot use `document.write()`
- Forgetting `<noscript>` fallback on the preload-to-stylesheet pattern — users with JS disabled never receive the stylesheet

## See Also

- [Resource Hints](resource-hints.md) — preconnect/preload to accelerate third-party and asset fetches
- [Code Splitting](code-splitting.md) — reduce JS bundle size before deferring it
- Reference: [web.dev: Render-blocking resources](https://web.dev/learn/performance/understanding-the-critical-path)
