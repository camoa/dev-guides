---
description: Merge request workflow with AI disclosure — the full drupal.org contribution flow, MR description template, issue fork commands, and common CI failure causes
tldr: "Use this when you are ready to submit code to a drupal.org project and need to follow the full contribution workflow with AI disclosure at each step."
drupal_version: "11.x"
---

# Merge Request Workflow

## When to Use

> Use this when you are ready to submit code to a drupal.org project and need to follow the full contribution workflow with AI disclosure at each step.

## Decision

| Step | Action | AI Disclosure Point |
|------|--------|---------------------|
| 1 | Find or create issue | Check AI disclosure boxes on issue |
| 2 | Create issue fork on GitLab | — |
| 3 | Write code (with AI assistance) | Follow coding standards, review all AI output |
| 4 | Run local tests | Verify AI code passes phpcs, phpstan, phpunit |
| 5 | Create merge request | Add AI disclosure in MR description |
| 6 | CI pipeline runs | Fix any failures — AI code often fails phpcs |
| 7 | Request review | Reviewers see AI flags from issue |
| 8 | Address feedback | Iterate, provide interdiffs |
| 9 | Maintainer commits | Credit assigned |

## Pattern

**MR description AI disclosure section:**

```markdown
## Summary
[What this MR does and why]

## AI Usage
- **Disclosure level**: AI Assisted Code
- **Tools used**: Claude Code
- **What AI helped with**: Suggested the approach for the form alter, helped write the test
- **What I did manually**: Reviewed all code, wrote the access check logic, tested edge cases

## Testing
- [ ] phpcs passes
- [ ] phpunit tests pass
- [ ] Manual testing completed
```

**Issue fork workflow:**

```bash
# Add the remote
git remote add drupal git@git.drupal.org:issue/PROJECT-NNNNNNN.git

# Create your changes on the issue branch, then push
git push drupal HEAD:NNNNNNN-branch-name

# CI runs phpcs, phpstan, phpunit automatically
```

Provide interdiffs for each revision so reviewers can see incremental changes.

## Common Mistakes

- **Wrong**: Skipping the MR description AI section → **Right**: Even if the issue has checkboxes, describe AI usage in the MR description too
- **Wrong**: Not providing interdiffs → **Right**: Reviewers need to see what changed between revisions; especially important for AI-assisted code where large rewrites are common
- **Wrong**: Ignoring CI failures → **Right**: AI-generated code frequently fails phpcs; fix before requesting review
- **Wrong**: Submitting without local testing → **Right**: Always run tests locally before pushing; CI is a safety net, not a substitute

## See Also

- [Issue Creation](issue-creation.md)
- [Coding Standards](coding-standards.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- Reference: [Drupal git workflow](https://www.drupal.org/docs/develop/git)
