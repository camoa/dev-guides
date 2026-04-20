---
description: Coding standards violations AI tools make — deprecated Drupal patterns AI introduces, why it happens, and verification commands to catch them
tldr: "Use this when submitting AI-assisted code to drupal.org and you need to verify it meets Drupal coding standards. AI tools commonly produce code that looks correct but violates specific Drupal conventions."
drupal_version: "11.x"
---

# Coding Standards

## When to Use

> Use this when submitting AI-assisted code to drupal.org and you need to verify it meets Drupal coding standards. AI tools commonly produce code that looks correct but violates specific Drupal conventions.

## Decision

| AI Mistake | Correct Drupal Pattern | How to Verify |
|-----------|----------------------|---------------|
| Using `\Drupal::service()` in classes | Dependency injection via `__construct()` + `create()` | Check for `\Drupal::` in any class |
| Procedural hooks in Drupal 11 | OOP hook attributes (`#[Hook('form_alter')]`) | Check if `.module` is used for hooks that should be attributes |
| Deprecated `db_query()` / `db_select()` | `\Drupal::database()->select()` or entity queries | Search for `db_query`, `db_select` |
| `drupal_set_message()` | `\Drupal::messenger()->addMessage()` | Search for `drupal_set_message` |
| `entity_load()` / `node_load()` | `\Drupal::entityTypeManager()->getStorage('node')->load()` | Search for `entity_load`, `node_load` |
| `format_date()` | `\Drupal::service('date.formatter')->format()` | Search for `format_date` |
| Wrong docblock format | `/** @var \Drupal\module\Class */` with full namespace | Run phpcs |
| Missing return type declarations | PHP 8.1+ return types required in Drupal 11 | Run phpstan |
| Using `t()` outside of classes | `$this->t()` in classes, `new TranslatableMarkup()` in static contexts | Search for standalone `t()` calls |
| `drush entity:updates` | Does NOT exist in Drupal 10+ — never use it | N/A |

## Pattern

Why AI gets this wrong: AI training data includes code from Drupal 7, 8, 9, 10, and 11. Each version has different patterns and AI blends them. Always verify code targets the correct Drupal version.

```bash
# Coding standards
phpcs --standard=Drupal,DrupalPractice --extensions=php,module,install,theme web/modules/custom/

# Static analysis
phpstan analyse web/modules/custom/ --level=6

# Deprecation check
drupal-check web/modules/custom/
```

## Common Mistakes

- **Wrong**: Trusting AI's confidence that code follows standards → **Right**: AI will say "this follows Drupal coding standards" while violating them; always run phpcs
- **Wrong**: Fixing phpcs errors with AI → **Right**: AI may introduce new violations while fixing old ones; run phpcs again after each fix
- **Wrong**: Not checking API existence → **Right**: AI invents function names; if a function name looks unfamiliar, verify it exists in the Drupal API docs
- **Wrong**: Accepting "it works" as sufficient → **Right**: Working code that violates standards will be rejected in review

## See Also

- [Merge Request Workflow](merge-request-workflow.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Security Considerations](security-considerations.md)
- Reference: [Drupal coding standards](https://www.drupal.org/docs/develop/standards)
