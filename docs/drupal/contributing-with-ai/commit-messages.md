---
description: "Commit messages for AI-assisted work — attribution trailers, drupal.org vs own-repo conventions, Co-Authored-By and Generated-by formats"
tldr: "Use this when committing AI-assisted code, either to a drupal.org issue fork or to your own contrib/custom project, and you want to properly attribute AI involvement."
drupal_version: "11.x"
---

# Commit Messages

## When to Use

> When committing AI-assisted code, either to a drupal.org issue fork or to your own contrib/custom project, and you want to properly attribute AI involvement.

## Decision: Attribution by Context

| Context | Format | Who Writes It |
|---|---|---|
| Drupal.org core contribution | `Issue #NNNNNNN by username: Description` | Maintainer (you don't control this) |
| Drupal.org contrib contribution | `Issue #NNNNNNN by username: Description` | Maintainer |
| Your own contrib module | Your convention + AI trailers | You |
| Custom project / team | Team convention + AI trailers | You |

## Pattern: AI Attribution Trailers

For repos you control, add trailers to commit messages:

**Co-Authored-By** (most common, GitHub renders in UI):
```
Fix entity query performance for large datasets

Optimized the entity query to use proper conditions
instead of loading all entities and filtering.

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Co-developed-by** (Linux kernel style):
```
Fix entity query performance for large datasets

Co-developed-by: Claude Sonnet 4 <noreply@anthropic.com>
Signed-off-by: Your Name <you@example.com>
```

**Generated-by** (Apache style, for primarily AI-generated code):
```
Add REST resource for widget export

Generated-by: Claude Sonnet 4
Reviewed-by: Your Name <you@example.com>
```

## Pattern: Drupal.org Convention

On drupal.org, **you don't write the final commit message**. The maintainer writes it when committing. Your AI disclosure lives in:
1. The issue checkboxes
2. The MR description
3. Issue comments explaining your approach

The maintainer may or may not mention AI in the commit message — that's their decision.

## Common Mistakes

- **Adding AI trailers to drupal.org issue fork commits** — These get squashed when the maintainer commits. Put AI disclosure in the issue and MR description instead.
- **Not attributing at all in your own repos** — If you maintain a contrib module and use AI, consider adding trailers for transparency
- **Using the wrong email for the AI tool** — Use `noreply@anthropic.com` for Claude, `noreply@github.com` for Copilot, or similar — don't use a real person's email
- **Overcomplicating attribution** — One trailer per AI tool is sufficient. Don't list every prompt.

## See Also

- [Industry Context](industry-context.md) — where these trailer conventions come from
- [Merge Request Workflow](merge-request-workflow.md) — the full contribution flow
