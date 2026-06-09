---
description: Structure pages with HTML landmarks, heading hierarchy, and skip links so screen-reader users have a navigable outline.
tldr: Use `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` for page regions and `<h1>`–`<h6>` in strict sequence; add a skip link targeting `<main tabindex="-1">`; never label every `<section>` as a region landmark — more than 6–8 landmarks dilutes their value.
---

# Semantic Structure

## When to Use

> Use semantic HTML landmarks and heading hierarchy on every web page — they give screen-reader users a navigable outline and region shortcuts that CSS styling alone cannot provide.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Page regions | `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>` | AT can jump between landmarks |
| Navigable content outline | `<h1>`–`<h6>` in sequence | Screen readers list headings; no skipping levels |
| Bypass repeated navigation | Skip link before `<nav>`, target `tabindex="-1"` | WCAG 2.4.1; required for keyboard users |
| Grouped items with a count | `<ul>` / `<ol>` | AT announces item count up front |
| Tabular data | `<table>` + `<caption>` + `<th scope="col|row">` | Column/row headers are read with each cell |
| Section needing a landmark | No landmark — leave `<section>` unlabeled | `region` landmark is a last resort |
| Layout grid | CSS Grid / Flexbox | `<table>` for layout confuses AT |

**Landmark overuse:** More than 6–8 landmarks on a page dilutes their value. Reserve `region` for genuinely distinct areas with no better semantic element.

**`<details>`/`<summary>` and headings:** Do not place headings inside `<summary>` — they disappear from screen-reader heading lists.

## Pattern

```html
<header>
  <a href="#content" class="skip-link visually-hidden">Skip to main content</a>
  <nav aria-label="Primary">
    <ul><li><a href="/">Home</a></li></ul>
  </nav>
</header>
<main id="content" tabindex="-1">
  <h1>Platform Dashboard</h1>
  <section>
    <h2>User Statistics</h2>
    <table>
      <caption>Monthly active users</caption>
      <tr><th scope="col">Month</th><th scope="col">Users</th></tr>
      <tr><td>January</td><td>12,000</td></tr>
    </table>
  </section>
</main>
```

## Common Mistakes

- **Wrong**: Styling a `<div>` as a heading → **Right**: Use `<h1>`–`<h6>`; visual styling is irrelevant to screen readers
- **Wrong**: Heading level jumps (`h1` → `h4`) → **Right**: Each level must nest within the previous
- **Wrong**: Missing `tabindex="-1"` on skip-link target → **Right**: `<main>` is not natively focusable; `.focus()` silently fails without it
- **Wrong**: Labeling every `<section>` → **Right**: Creates a region landmark storm; leave sections unlabeled unless genuinely distinct
- **Wrong**: Using `<table>` for layout → **Right**: Breaks AT row/column navigation

## See Also

- [Accessible Names](accessible-names.md) — `visually-hidden` CSS utility
- [Keyboard and Focus](keyboard-and-focus.md) — skip-link focus management
- Reference: https://www.w3.org/WAI/ARIA/apg/patterns/landmarks/
