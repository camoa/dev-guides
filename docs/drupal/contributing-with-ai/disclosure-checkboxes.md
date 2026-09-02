---
description: "AI disclosure checkboxes — which drupal.org issue checkboxes to select, the significant-portion threshold, and the required disclosure comment format"
tldr: "Check the box matching your actual AI involvement level: AI Assisted Issue (text/research), AI Assisted Code (suggestions reviewed line-by-line), AI Generated Code (substantial generation you reviewed), or Vibe Coded. Multiple boxes can apply. When significant code was generated, also add an AI-Generated: Yes (...) comment."
drupal_version: "11.x"
---

# Disclosure Checkboxes

## When to Use

> When creating or updating a drupal.org issue and you need to determine which AI disclosure checkboxes to select and what to include in the disclosure comment.

## Decision: The "Significant Portion" Threshold

The adopted policy sets a clear threshold — disclosure is **required** when AI generated a **significant portion** of the work. Disclosure is **not** required for trivial use:

| Requires Disclosure | Does NOT Require Disclosure |
|---|---|
| AI wrote entire functions or classes | Standard single-line autocomplete suggestions |
| AI generated architectural scaffolding | Basic syntax corrections from an AI IDE plugin |
| AI wrote extensive documentation blocks | AI reformatted your code without changing logic |
| AI generated a whole patch you reviewed | AI suggested a variable name you typed yourself |

**When in doubt:** Disclose. The cost of over-disclosing is trivial; the cost of under-disclosing is trust erosion and potential credit revocation.

## Decision: Which Checkbox to Check

| Checkbox | Definition | Example | Review Impact |
|---|---|---|---|
| **AI Assisted Issue** | AI helped research, write the issue summary, or analyze the problem | Used Claude to research a core API, draft steps to reproduce, or analyze a backtrace | Minimal — issue quality still evaluated normally |
| **AI Assisted Code** | Human wrote code with AI suggestions; human reviewed every line; AI contribution did not cross the "significant portion" threshold | Used Copilot for completion hints, asked Claude to suggest an approach, then wrote and reviewed the code yourself | Normal review — reviewer trusts the human understands the code |
| **AI Generated Code** | AI generated substantial portions (functions, classes, scaffolding) that you reviewed and tested | Asked AI to write a patch, then carefully reviewed every line, tested edge cases, verified APIs exist | Enhanced review — reviewer may probe understanding, test more thoroughly |
| **Vibe Coded** | AI generated most/all code with minimal human review | Gave AI a prompt, submitted the output with little to no modification or understanding | Maximum scrutiny — expect questions about every line, likely rejection if contributor can't explain |

## Pattern: Disclosure Comment Format

When AI generated significant portions, append a disclosure statement to your issue comment or MR description using the policy's format:

```
AI-Generated: Yes (Used Claude Code to generate the cache invalidation logic
and entity query boilerplate; I reviewed all generated code, verified API calls
against Drupal 11 docs, and added the access control checks manually.)
```

The format: `AI-Generated: Yes (Used <tool> to help generate <component>.)` — be specific about which tool, which component, and what human review was done.

## Pattern: Decision Flow

```
Did AI help with the issue text (summary, research, analysis)?
  → Yes → Check "AI Assisted Issue"

Did AI help with code?
  → Only trivial autocomplete / single-line suggestions
    → No code checkbox needed (below the threshold)
  → AI wrote significant code I reviewed and tested thoroughly
    → Check "AI Generated Code" + add disclosure comment
  → AI wrote most/all with minimal review
    → Check "Vibe Coded" (reconsider submitting)
  → In between — AI suggestions I shaped and reviewed line by line
    → Check "AI Assisted Code"

Multiple can apply:
  → AI helped write the issue AND generated significant code
    → Check both "AI Assisted Issue" + "AI Generated Code"
```

## Pattern: The Responsible Path

**"AI Assisted Code" with thorough human review** is the recommended approach:

1. You understand the problem before involving AI
2. You guide the AI toward the right approach
3. AI helps with implementation details (boilerplate, API usage)
4. You review every line and understand why it's there
5. You test the result, including edge cases
6. You can defend every technical decision in review

This is how experienced developers use AI tools — as an assistant, not a replacement.

## Common Mistakes

- **Underdisclosing** — Checking "AI Assisted Code" when AI wrote entire functions or classes. Be honest about the level and scale of AI involvement.
- **Overclaiming the exemption** — "It's just autocomplete" doesn't apply to whole-function generation. Use the significant-portion test, not the tool-type test.
- **Skipping the disclosure comment** — Checking the box is not enough when significant portions were AI-generated. Add the `AI-Generated: Yes (...)` comment with specifics.
- **Thinking "AI Assisted Issue" covers code too** — Issue assistance and code assistance are separate disclosures. Check both if both apply.

## See Also

- [Drupal AI Policy](drupal-ai-policy.md) — the full policy and its rules
- [Issue Creation](issue-creation.md) — full issue creation workflow
- [Decision Trees](decision-trees.md) — quick flowcharts
