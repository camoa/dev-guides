---
description: AI toolchain setup for Drupal contribution — essential tools (phpcs, phpstan, pre-commit hooks), context management strategies, and mapping workflows to disclosure levels
drupal_version: "11.x"
---

# AI Toolchain for Contribution

## When to Use

> Use this when setting up your AI development environment for Drupal contribution and you want to configure tools for responsible, well-guarded AI-assisted development.

## Decision

| Priority | Tool/Practice | Purpose |
|----------|--------------|---------|
| Essential | phpcs + DrupalPractice standard | Catches AI coding standard violations automatically |
| Essential | phpstan | Catches type errors, undefined methods, wrong return types |
| Essential | Pre-commit hooks | Blocks commits that fail standards before they reach the MR |
| Recommended | drupal-check | Catches deprecated API usage that AI commonly introduces |
| Recommended | Dev-guides / API docs | Authoritative reference to counteract training data bias |
| Recommended | Project-specific config (CLAUDE.md, skills) | Loads conventions and standards into AI context |
| Optional | IDE integration (phpcs in editor) | Catches violations as you write, not just at commit |

## Pattern

**Pre-commit hook setup:**

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

**Context management:**

| When | Action |
|------|--------|
| Session start | Load relevant dev-guide for the API you're working with; specify Drupal version explicitly |
| During session | Keep focused — one issue per session; verify AI suggestions against docs before proceeding |
| After 2+ corrections on same issue | Start fresh session |
| Between sessions | Clear context; review produced code with fresh eyes before submitting |

**Mapping workflow to disclosure level:**

| Your Workflow | Likely Disclosure Level |
|--------------|------------------------|
| AI autocompletes variable names and snippets while you write | AI Assisted Code |
| You discuss the approach with AI, it suggests code, you write and adapt | AI Assisted Code |
| You ask AI to write a function, review every line, test thoroughly | AI Generated Code |
| You ask AI to write the whole patch, glance at it, submit | Vibe Coded — reconsider |

## Common Mistakes

- **Wrong**: Not configuring standards enforcement → **Right**: Relying on CI to catch standards violations wastes review cycles; catch them locally
- **Wrong**: Loading too much context → **Right**: AI doesn't read everything; load the specific guide or standard relevant to the current task
- **Wrong**: Using AI's built-in "knowledge" instead of docs → **Right**: AI's training data is stale; for API specifics, reference current documentation
- **Wrong**: Forgetting to specify the Drupal version → **Right**: Without explicit version, AI will blend code from multiple Drupal versions

## See Also

- [Supervised AI Workflow](supervised-ai-workflow.md)
- [Coding Standards](coding-standards.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
