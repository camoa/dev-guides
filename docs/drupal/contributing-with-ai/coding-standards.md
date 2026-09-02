---
description: "Coding standards violations AI tools make — deprecated Drupal patterns AI introduces, why it happens, and verification commands to catch them"
tldr: "Use this when submitting AI-assisted code to drupal.org and you need to verify it meets Drupal coding standards. AI tools commonly produce code that looks correct but violates specific Drupal conventions."
drupal_version: "11.x"
---

# Coding Standards

## When to Use

> When submitting AI-assisted code to drupal.org and you need to verify it meets Drupal coding standards. AI tools commonly produce code that looks correct but violates specific Drupal conventions.

## Decision: Common AI Violations

| AI Mistake | Correct Drupal Pattern | How to Verify |
|---|---|---|
| Using `\Drupal::service()` in classes | Dependency injection via `__construct()` + `create()` | Check for `\Drupal::` in any class |
| Procedural hooks in Drupal 11 | OOP hook attributes (`#[Hook('form_alter')]`) | Check if module uses `.module` for hooks that should be attributes |
| Deprecated `db_query()` / `db_select()` | `\Drupal::database()->select()` or entity queries | Search for `db_query`, `db_select` |
| `drupal_set_message()` | `\Drupal::messenger()->addMessage()` | Search for `drupal_set_message` |
| `entity_load()` / `node_load()` | `\Drupal::entityTypeManager()->getStorage('node')->load()` | Search for `entity_load`, `node_load` |
| `format_date()` | `\Drupal::service('date.formatter')->format()` | Search for `format_date` |
| Wrong docblock format | `/** @var \Drupal\module\Class */` with full namespace | Run phpcs |
| Missing return type declarations | PHP 8.1+ return types required in Drupal 11 | Run phpstan |
| Using `t()` outside of classes | `$this->t()` in classes, `new TranslatableMarkup()` in static contexts | Search for standalone `t()` calls |
| Wrong form element `#type` values | Verify against Form API reference | Check Drupal API docs |
| `drush entity:updates` | Does NOT exist in Drupal 10+ — never use it | N/A |
| Hardcoded service calls | Use service container, tagged services, or plugin managers | Review service usage patterns |

## Pattern: Why AI Gets This Wrong

AI training data includes code from Drupal 7, 8, 9, and 10. Each version has different patterns:
- **Drupal 7**: Procedural, `db_query()`, `drupal_set_message()`, `.info` files
- **Drupal 8**: Early OOP, `*.services.yml`, `*.routing.yml`, still some procedural hooks
- **Drupal 9**: Deprecated D8 functions removed, stricter type hints
- **Drupal 10**: PHP 8.1+ required, more attributes, named arguments
- **Drupal 11**: Hook attributes, further API modernization

AI blends these eras. You must verify code targets the correct Drupal version.

## Pattern: Verification Commands

```bash
# Coding standards
phpcs --standard=Drupal,DrupalPractice --extensions=php,module,install,theme web/modules/custom/

# Static analysis
phpstan analyse web/modules/custom/ --level=6

# Deprecation check
drupal-check web/modules/custom/
```

## Common Mistakes

- **Trusting AI's confidence that code follows standards** — AI will say "this follows Drupal coding standards" while violating them. Always run phpcs.
- **Fixing phpcs errors with AI** — AI may introduce new violations while fixing old ones. Run phpcs again after each fix.
- **Not checking API existence** — AI invents function names. If a function name looks unfamiliar, verify it exists in the Drupal API docs.
- **Accepting "it works" as sufficient** — Working code that violates standards will be rejected in review.

## See Also

- [Merge Request Workflow](merge-request-workflow.md) — where standards fit in the process
- [AI Code Review Checklist](ai-code-review-checklist.md) — full pre-submission checklist
- [Security Considerations](security-considerations.md) — security-specific violations
- [Drupal Coding Standards at CI Parity](../contributing/drupal-coding-standards-ci-parity.md) — CI-parity gate setup, phpcs rulesets, phpstan config (this guide covers the AI-specific angle only)
- Reference: [Drupal coding standards](https://www.drupal.org/docs/develop/standards)
