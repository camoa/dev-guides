---
description: Decision trees for AI contribution — quick flowcharts for disclosure checkbox selection, whether to disclose, git attribution context, and submission readiness
drupal_version: "11.x"
---

# Decision Trees

## When to Use

> Use this when you need quick answers to common AI contribution questions without reading the full guides.

## Decision: Which Disclosure Checkbox?

```
Did AI help with the issue text (summary, research, analysis)?
└── Yes → Check "AI Assisted Issue"

Did AI help with code?
├── I wrote code with AI suggestions/completions, reviewed every line
│   └── Check "AI Assisted Code"
├── AI generated substantial code that I reviewed and tested thoroughly
│   └── Check "AI Generated Code"
└── AI wrote most/all code with minimal review
    └── Check "Vibe Coded"

Note: Multiple checkboxes can apply together
```

## Decision: Should I Disclose?

```
Did you use any AI tool at any point?
├── Yes → Disclose
│   ├── "I only used it for a small thing" → Still disclose
│   ├── "It just autocompleted one line" → Disclose as AI Assisted Code
│   └── "I'm not sure if my IDE counts" → If it has AI features enabled, disclose
└── No AI tools used at all → No disclosure needed
```

## Decision: How to Attribute in Git?

```
Where is this contribution going?
├── Drupal.org core/contrib
│   └── Use issue checkboxes + MR description. Maintainer writes commit message.
├── Your own contrib module
│   └── Add Co-Authored-By or Generated-by trailer to commit message
└── Custom project / team
    └── Follow team convention. Consider Co-Authored-By for transparency.
```

## Decision: Is My Code Ready to Submit?

```
Can I explain every line?
├── No → Don't submit. Understand first.
└── Yes
    └── Do coding standards pass (phpcs)?
        ├── No → Fix first.
        └── Yes
            └── Do tests cover the change?
                ├── No → Add tests.
                └── Yes
                    └── Is there a simpler approach?
                        ├── Yes → Simplify.
                        └── No
                            └── Are disclosure boxes checked?
                                ├── No → Update issue.
                                └── Yes → Ready to submit
```

## Common Mistakes

- **Wrong**: Using decision trees as a substitute for judgment → **Right**: These are starting points, not complete guides; read the full guide for nuanced situations
- **Wrong**: Stopping at the first "yes" → **Right**: Walk through the entire tree; multiple conditions must be satisfied

## See Also

- [Disclosure Checkboxes](disclosure-checkboxes.md)
- [AI Code Review Checklist](ai-code-review-checklist.md)
- [Resources](resources.md)
