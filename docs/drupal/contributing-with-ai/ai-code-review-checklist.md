---
description: Pre-submission checklist for AI-assisted Drupal contributions — understanding, API correctness, coding standards, security, testing, and disclosure verification
tldr: "Use this before submitting any AI-assisted code to drupal.org or any Drupal project. Run through every item every time."
drupal_version: "11.x"
---

# AI Code Review Checklist

## When to Use

> Use this before submitting any AI-assisted code to drupal.org or any Drupal project. Run through every item every time.

## Decision

Run through all six categories before submitting:

**Understanding:**
- [ ] I can explain what this code does and why it's needed
- [ ] I can explain why this approach was chosen over alternatives
- [ ] I understand every line — no code accepted without understanding
- [ ] I could defend every technical choice in a code review

**API Correctness:**
- [ ] All Drupal API calls exist in the target Drupal version
- [ ] No deprecated functions are used
- [ ] Dependency injection is used where appropriate (no `\Drupal::` in classes)
- [ ] Hook implementations use the correct mechanism for the Drupal version

**Standards Compliance:**
- [ ] `phpcs --standard=Drupal,DrupalPractice` passes
- [ ] `phpstan` passes at the configured level
- [ ] Docblocks are complete and correctly formatted
- [ ] Naming conventions match Drupal standards

**Security:**
- [ ] Output is properly sanitized (`Html::escape()`, `Xss::filter()`, `#plain_text`)
- [ ] Access checks are in place for routes and entity operations
- [ ] No SQL injection risks (using entity queries or database abstraction, not raw SQL)
- [ ] Form tokens are validated (automatic with Form API, manual with custom routes)
- [ ] No sensitive data in logs or error messages

**Testing:**
- [ ] Tests exist and pass
- [ ] Tests cover the change, not just the happy path
- [ ] Edge cases and error conditions are tested
- [ ] Existing tests still pass (no regressions)

**Disclosure:**
- [ ] AI disclosure checkboxes on the issue are correct
- [ ] MR description includes AI usage section
- [ ] Disclosure level matches actual AI involvement

## Pattern

> Can I explain every line of this code to a reviewer who asks "why?"

If the answer is no for any line, understand it before submitting. This is the difference between "AI Assisted Code" and "Vibe Coded."

## Common Mistakes

- **Wrong**: Skipping the checklist because "it's a small change" → **Right**: Small AI-generated changes can still contain hallucinated APIs or security issues
- **Wrong**: Checking boxes without actually verifying → **Right**: Running phpcs is required, not optional; "I think it passes" is not verification
- **Wrong**: Delegating the checklist to AI → **Right**: The checklist is for YOU to verify; asking AI "does this pass the checklist?" defeats the purpose

## See Also

- [Coding Standards](coding-standards.md)
- [Human Review Requirements](human-review-requirements.md)
- [Security Considerations](security-considerations.md)
