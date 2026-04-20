---
description: AI disclosure checkboxes — which of the 4 drupal.org checkboxes to select, when multiple apply, and the responsible path for AI-assisted contributions
tldr: "Use this when creating or updating a drupal.org issue and you need to determine which AI disclosure checkboxes to select."
drupal_version: "11.x"
---

# Disclosure Checkboxes

## When to Use

> Use this when creating or updating a drupal.org issue and you need to determine which AI disclosure checkboxes to select.

## Decision

| Checkbox | Definition | Example | Review Impact |
|----------|-----------|---------|---------------|
| **AI Assisted Issue** | AI helped research, write, or analyze the problem | Used Claude to research a core API, draft steps to reproduce, or analyze a backtrace | Minimal — issue quality still evaluated normally |
| **AI Assisted Code** | Human wrote code with AI suggestions/completions; human reviewed every line | Used Copilot for autocomplete, asked Claude to suggest an approach, then wrote and reviewed the code yourself | Normal review — reviewer trusts the human understands the code |
| **AI Generated Code** | AI generated substantial portions of the code; human reviewed and tested | Asked AI to write a patch, then carefully reviewed every line, tested edge cases, verified APIs exist | Enhanced review — reviewer may probe understanding, test more thoroughly |
| **Vibe Coded** | AI generated most/all code with minimal human review | Gave AI a prompt, submitted the output with little to no modification | Maximum scrutiny — expect questions about every line, likely rejection if contributor can't explain |

## Pattern

```
Did AI help with the issue text (summary, research, analysis)?
  → Yes → Check "AI Assisted Issue"

Did you write code with AI assistance?
  → I used AI for suggestions but wrote/reviewed every line myself
    → Check "AI Assisted Code"
  → AI generated substantial code that I reviewed thoroughly
    → Check "AI Generated Code"
  → AI wrote most of it and I didn't review deeply
    → Check "Vibe Coded"

Multiple can apply:
  → AI helped write the issue AND assisted with code
    → Check both "AI Assisted Issue" + "AI Assisted Code"
```

The responsible path — **AI Assisted Code** with thorough human review:
1. Understand the problem before involving AI
2. Guide the AI toward the right approach
3. AI helps with implementation details
4. Review every line and understand why it's there
5. Test the result, including edge cases
6. Defend every technical decision in review

## Common Mistakes

- **Wrong**: Underdisclosing — checking "AI Assisted Code" when AI wrote most of the patch → **Right**: Be honest about the level of AI involvement
- **Wrong**: Overdisclosing out of fear — checking "AI Generated Code" for one autocomplete suggestion → **Right**: Match the checkbox to the actual level of AI involvement
- **Wrong**: Not checking any box after using AI → **Right**: If you used AI at any point, disclose — even autocomplete is "AI Assisted Code"
- **Wrong**: Thinking "AI Assisted Issue" covers code too → **Right**: Issue assistance and code assistance are separate disclosures; check both if both apply

## See Also

- [Drupal AI Policy](drupal-ai-policy.md)
- [Issue Creation](issue-creation.md)
- [Decision Trees](decision-trees.md)
