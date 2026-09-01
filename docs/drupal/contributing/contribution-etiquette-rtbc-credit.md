---
description: Drupal contribution etiquette — RTBC checklist and no-self-RTBC rule, the Contribution Records credit system, Code of Conduct pillars, and comment conventions
tldr: "RTBC asserts the full checklist (tests pass, phpcs clean, all threads resolved, gates passed for core) — never just a code read. Credit is maintainer-granted via Contribution Records; never demand it. No self-RTBC on core issues where you are the sole author."
drupal_version: "11.x"
---

# Contribution Etiquette, RTBC Discipline & the Credit System

## When to Use

> Use this when you are ready to set RTBC, review someone else's work, write an issue comment, or understand how credit is granted.

## Decision

**RTBC — by workflow:**

| Workflow | RTBC discipline |
|---|---|
| Core | Strict; no self-RTBC as sole author |
| Your own contrib | Relaxed; self-RTBC OK as maintainer |
| Someone else's contrib | Strict; no self-RTBC unless maintainer allows |

**RTBC checklist** — before setting RTBC (classic) or applying `state::rtbc` + MR approval (GitLab):

- [ ] Automated tests pass
- [ ] Test-only change fails as expected (if the issue is a test gap)
- [ ] No coding-standard violations (`phpcs` clean)
- [ ] All discussion threads resolved
- [ ] All "Needs…" tags addressed
- [ ] Follow-up issues created if any were tagged
- [ ] Change records created if tagged
- [ ] For **core**: all applicable core gates pass

Anyone can set RTBC — but the checklist discipline is expected. A maintainer can revert an inappropriately set RTBC to *Needs review*.

## Comment Conventions

Pattern: **thank → identify what works → specific feedback → actionable next step**

```
Thank you for working on this — the approach in X is correct.
The issue is in Y: [specific problem].
[Exact change needed or pointer to the correct API].
```

Avoid: vague feedback, bare "+1 RTBC" without substantive review, noise that doesn't advance the issue.

## The Contribution Records System (Credit)

- **Nothing is automatic** — not even the issue creator is credited automatically
- **Only maintainers grant credit** via checkboxes on the issue's Contribution Record
- **Credit appears** on user and org profiles once the issue reaches Fixed or Closed
- **Impact:** organizations are ranked in the Drupal Marketplace by weighted credit
- **Etiquette:** never demand credit; let the contribution speak

Credit works identically for GitLab-migrated issues — Contribution Records is decoupled from issue hosting.

## Best-Practice Differences by Workflow

| Dimension | Core | Your own contrib | Someone else's contrib |
|---|---|---|---|
| RTBC discipline | Strict; no self-RTBC as sole author | Relaxed; self-RTBC OK | Strict; no self-RTBC unless allowed |
| Credit decision | Core committers decide | You decide | Maintainer decides |
| Pace expectation | Slow; release-phase limits | You control | Maintainer's pace — be patient |
| Review burden | Multi-reviewer, very strict | You set it | Maintainer sets it |

## Code of Conduct — Five Pillars

1. Consider others' needs
2. Disagree respectfully
3. Collaborate openly
4. Zero tolerance for abuse
5. Transition responsibly

Violations go to the Conflict Resolution Team via the Incident Report Form at drupal.org/dcoc.

## Common Mistakes

- **Wrong**: Setting RTBC after reading the code but without running the tests → **Right**: RTBC asserts the full checklist, not just a code read
- **Wrong**: Demanding credit in an issue comment → **Right**: It signals entitlement and antagonizes maintainers
- **Wrong**: Writing "+1 RTBC" without a substantive review → **Right**: Treated as noise; damages your reputation
- **Wrong**: Self-RTBCing a core issue where you are the sole author → **Right**: A committer will revert it
- **Wrong**: Commenting in a closed issue → **Right**: Open a new related issue instead

## See Also

- [The Drupal Issue Lifecycle](drupal-issue-lifecycle.md)
- [Issue Forks & Merge Requests, Step by Step](issue-forks-merge-requests.md)
- [Serving as a Drupal Module/Theme Maintainer](module-theme-maintainer.md)
- AI overlay: [Contributing with AI — Credit System](../contributing-with-ai/credit-system.md)
- Reference: [drupal.org/drupalorg/blog/the-new-contribution-records-system](https://www.drupal.org/drupalorg/blog/the-new-contribution-records-system)
- Reference: [drupal.org/dcoc](https://www.drupal.org/dcoc)
