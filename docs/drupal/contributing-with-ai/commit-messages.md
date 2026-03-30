---
description: Commit messages for AI-assisted work — attribution trailers, drupal.org vs own-repo conventions, Co-Authored-By and Generated-by formats
drupal_version: "11.x"
---

# Commit Messages

## When to Use

> Use this when committing AI-assisted code and you want to properly attribute AI involvement — either to a drupal.org issue fork or to your own contrib/custom project.

## Decision

| Context | Format | Who Writes It |
|---------|--------|---------------|
| Drupal.org core contribution | `Issue #NNNNNNN by username: Description` | Maintainer (you don't control this) |
| Drupal.org contrib contribution | `Issue #NNNNNNN by username: Description` | Maintainer |
| Your own contrib module | Your convention + AI trailers | You |
| Custom project / team | Team convention + AI trailers | You |

## Pattern

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

**On drupal.org**: You don't write the final commit message. The maintainer writes it when committing. Your AI disclosure lives in the issue checkboxes, the MR description, and issue comments.

## Common Mistakes

- **Wrong**: Adding AI trailers to drupal.org issue fork commits → **Right**: These get squashed when the maintainer commits; put AI disclosure in the issue and MR description instead
- **Wrong**: Not attributing at all in your own repos → **Right**: If you maintain a contrib module and use AI, add trailers for transparency
- **Wrong**: Using a real person's email for the AI tool → **Right**: Use `noreply@anthropic.com` for Claude, `noreply@github.com` for Copilot, or similar
- **Wrong**: Overcomplicating attribution → **Right**: One trailer per AI tool is sufficient; don't list every prompt

## See Also

- [Industry Context](industry-context.md)
- [Merge Request Workflow](merge-request-workflow.md)
