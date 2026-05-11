---
description: Crawled-site plan generation — tradeoffs, bounded-crawl pattern, and when not to use discovery as a test generation strategy.
tldr: Crawl-based plan generation catches forgotten surfaces on inherited projects but produces flat, unmaintainable plans on Drupal sites where infinite URL axes exist. Use it with strict path prefix restrictions, depth cap of 2, and admin/user exclusions — and treat the output as discovery material humans prune, not as production tests.
---

# Crawled Site

## When to Use

> Use crawled discovery when backfilling tests on an inherited project with no docs and no organized user stories. Do not use it as the default workflow.

## Decision

| Use crawl when... | Don't crawl when... |
|---|---|
| Backfilling tests on an inherited project with no docs | You have user stories — use them instead |
| Mapping unknown surface area before writing real tests | You know what to test — be explicit |
| Producing a one-off discovery report | You expect the output to ship as production tests |

### Tradeoffs

**Pros:**
- Catches surfaces nobody remembered (admin pages, legacy routes, settings forms)
- Good for "regression net" plans where breadth > depth
- Useful when documentation is poor

**Cons:**
- Plans become flat: "Visit /node/1, see a node"
- Crawls follow auth-gated links that fail without seed login → useless "redirect to /login" scenarios
- Drupal sites have infinite-axis surfaces (filtered views, paginated listings, every node URL) — Planner can't tell which are meaningfully different
- Generated plans become unmaintainable: every new node creates a hypothetical scenario

## Pattern: bounded crawl

```
Crawl from sitemap.xml.
Cap depth at 2.
Restrict to path prefixes: /contact, /search, /about.
Exclude /admin/*, /user/*, /node/*.
Treat plans as starting points humans prune.
```

## Common Mistakes

- **Wrong**: Crawl-and-generate as the default workflow → **Right**: produces 200 redundant scenarios; one selector change breaks all; PM cannot review
- **Wrong**: No path exclusions → **Right**: Planner generates auth-gate scenarios for every admin URL
- **Wrong**: Treating crawl output as final tests → **Right**: crawl output is discovery material; humans prune and scope before generating code

## See Also

- [Targeted Scope](ai-testgen-targeted-scope.md)
- [Hybrid Inputs](ai-testgen-hybrid-inputs.md)
- [Overview](ai-testgen-overview.md)
