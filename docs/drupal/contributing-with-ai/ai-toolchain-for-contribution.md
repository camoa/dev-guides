---
description: "AI toolchain setup for Drupal contribution — essential tools (phpcs, phpstan, pre-commit hooks), context management strategies, and mapping workflows to disclosure levels"
tldr: "Use this when setting up your AI development environment for Drupal contribution and you want to configure tools for responsible, well-guarded AI-assisted development."
drupal_version: "11.x"
---

# AI Toolchain for Contribution

## When to Use

> When setting up your AI development environment for Drupal contribution and you want to configure tools for responsible, well-guarded AI-assisted development.

## Decision: Tool Setup Priority

| Priority | Tool/Practice | Purpose |
|---|---|---|
| Essential | phpcs + DrupalPractice standard | Catches AI coding standard violations automatically |
| Essential | phpstan | Catches type errors, undefined methods, wrong return types |
| Essential | Pre-commit hooks | Blocks commits that fail standards before they reach the MR |
| Recommended | drupal-check | Catches deprecated API usage that AI commonly introduces |
| Recommended | Dev-guides / API docs | Authoritative reference to counteract training data bias |
| Recommended | Project-specific config (CLAUDE.md, skills) | Loads conventions and standards into AI context |
| Optional | IDE integration (phpcs in editor) | Catches violations as you write, not just at commit |

## Pattern: Pre-Commit Hook Setup

```bash
# Install phpcs with Drupal standards
composer require --dev drupal/coder dealerdirect/phpcodesniffer-composer-installer

# Create pre-commit hook
cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(php|module|install|theme)$')
if [ -n "$FILES" ]; then
    vendor/bin/phpcs --standard=Drupal,DrupalPractice $FILES
    if [ $? -ne 0 ]; then
        echo "Fix coding standards before committing."
        exit 1
    fi
fi
EOF
chmod +x .git/hooks/pre-commit
```

This catches AI-generated code that violates standards before it ever reaches a merge request.

## Pattern: Context Management for AI Tools

**At session start:**
- Load the relevant dev-guide for the API you're working with (forms, entities, services, etc.)
- Point AI to the project's coding conventions
- Specify the Drupal version explicitly ("We're targeting Drupal 11.x")

**During the session:**
- Keep sessions focused — one issue per session when practical
- When AI suggests an approach, verify against docs before proceeding
- If you've corrected the AI more than twice on the same issue, start fresh

**Between sessions:**
- Clear context — don't carry confusion from one issue to the next
- Review what was produced with fresh eyes before submitting

## Pattern: Mapping Disclosure Levels to Your Workflow

| Your Workflow | Likely Disclosure Level |
|---|---|
| AI autocompletes variable names and snippets while you write | AI Assisted Code |
| You discuss the approach with AI, it suggests code, you write and adapt | AI Assisted Code |
| You ask AI to write a function, review every line, test thoroughly | AI Generated Code |
| You ask AI to write the whole patch, glance at it, submit | Vibe Coded — reconsider |

## Common Mistakes

- **Not configuring standards enforcement** — Relying on CI to catch standards violations wastes review cycles. Catch them locally.
- **Loading too much context** — AI doesn't read everything. Load the specific guide or standard relevant to the current task, not everything.
- **Using AI's built-in "knowledge" instead of docs** — AI's training data is stale. For API specifics, always reference current documentation.
- **Forgetting to specify the Drupal version** — Without explicit version, AI will blend code from multiple Drupal versions

## See Also

- [Supervised AI Workflow](supervised-ai-workflow.md) — the philosophy behind these practices
- [Coding Standards](coding-standards.md) — what AI gets wrong
- [AI Code Review Checklist](ai-code-review-checklist.md) — what to check before submitting
