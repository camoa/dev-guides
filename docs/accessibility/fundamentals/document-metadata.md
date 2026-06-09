---
description: Set page language, craft front-loaded unique titles, and update both on SPA navigation so screen readers announce the correct context on every page load.
tldr: Declare `<html lang="en">`, front-load unique context in `<title>` ("Page Topic | Site Name" not "Site Name | Page Topic"), and on SPA route changes update `document.title` and move focus to the new `<h1>` or `<main tabindex="-1">`.
---

# Document Metadata

## When to Use

> Declare page language, craft unique front-loaded titles, and update both on SPA navigation — these provide the foundational orientation information screen readers announce on page load and on route change.

## Decision

| Need | Pattern | Anti-pattern |
|---|---|---|
| Page language | `<html lang="en">` | Missing `lang` |
| Inline language switch | `<span lang="fr">Bonjour</span>` | Unswitched mixed-language content |
| Page title | `Page Topic \| Site Name` (topic first) | `Site Name \| Page Topic` (topic buried) |
| Unique title per view | Include entity name / report name / step | Generic "Edit" or "Form" title |
| iFrame | `<iframe title="Interactive chart">` | Missing `title` |
| iFrame scrolling | Do not disable | `scrolling="no"` / `overflow: hidden` on iframe |
| SPA route change | Update `document.title` + move focus | Only changing URL; no title or focus update |

**Front-load unique context:** `Analytics Reports | Guidance Platform` tells a screen-reader user immediately which page they are on. `Guidance Platform | Analytics Reports` makes them wait through the site name.

## Pattern

```html
<html lang="en">
<head>
  <title>Analytics Reports | Guidance Platform</title>
</head>
<body>
  <p>The motto is <span lang="la">"Carpe diem"</span>.</p>
  <iframe title="Interactive Sales Chart" src="/chart"></iframe>
</body>
</html>
```

```javascript
// SPA route change handler
function onRouteChange(newTitle) {
  document.title = `${newTitle} | Site Name`;
  // Move focus to main heading or <main tabindex="-1">
  const heading = document.querySelector('main h1') || document.querySelector('main');
  heading?.focus();
}
```

## Common Mistakes

- **Wrong**: Missing `lang` attribute → **Right**: Screen readers use the default voice, which mispronounces foreign words
- **Wrong**: Non-unique page titles → **Right**: When multiple tabs show "Home | Site", users cannot differentiate them
- **Wrong**: Missing `iframe title` → **Right**: The iframe is announced as "frame" with no context; users cannot decide whether to enter it
- **Wrong**: No SPA focus management → **Right**: After navigation, focus remains on the link that triggered it; the new page content is never announced
- **Wrong**: `overflow: hidden` on iframe container → **Right**: Users who zoom cannot scroll to reach overflowed content

## See Also

- [Semantic Structure](semantic-structure.md) — landmark context that pairs with titles
- Reference: https://www.w3.org/TR/WCAG22/#page-titled (WCAG 2.4.2)
- Reference: https://www.w3.org/TR/WCAG22/#language-of-page (WCAG 3.1.1)
