---
description: Drupal contribution etiquette — RTBC checklist and no-self-RTBC rule, the Contribution Records credit system, Code of Conduct pillars, and comment conventions
tldr: "RTBC asserts the full checklist (tests pass, phpcs clean, all threads resolved, gates passed for core) — never just a code read. Credit is maintainer-granted via Contribution Records; never demand it. No self-RTBC on core issues where you are the sole author."
drupal_version: "11.x"
---

# Contribution Etiquette, RTBC Discipline & the Credit System

## When to Use

> Use this when you are ready to set RTBC, review someone else's work, write an issue comment, or understand how credit is granted. The cultural norms here are what separate accepted contributions from ones that stall in review.

## Comment Conventions

A constructive review comment follows the pattern: **thank → identify what works → specific feedback → actionable next step**.

```
Thank you for working on this — the approach in X is correct.
The issue is in Y: [specific problem]. 
[Exact change needed or pointer to the correct API].
```

Avoid: "but" directly after thanks (it erases the positive tone), vague feedback ("this needs work"), bare "+1 RTBC" without substantive review, noise that doesn't advance the issue. Use `#123` to cross-reference within a project; full URLs for cross-project references.

## RTBC Checklist

Before setting RTBC (classic queue) or applying `state::rtbc` + MR approval (GitLab):

- [ ] Automated tests pass
- [ ] Test-only change fails as expected (if the issue is a test gap)
- [ ] No coding-standard violations (`phpcs` clean)
- [ ] All discussion threads resolved
- [ ] All "Needs…" tags addressed
- [ ] Follow-up issues created if any were tagged
- [ ] Change records created if tagged
- [ ] For **core**: all applicable core gates pass (Accessibility, Documentation, Frontend, Performance, Testing, Usability)

**No-self-RTBC rule:**

- **Core:** do not RTBC a patch where you are the sole or main author — even if technically correct, it erodes trust.
- **Your own contrib:** you may self-RTBC as the maintainer.
- **Someone else's contrib:** no self-RTBC unless the maintainer's documented policy allows it.

Anyone can set RTBC — but the checklist discipline is expected. A maintainer can revert an inappropriately set RTBC to *Needs review*.

## The Contribution Records System (Credit)

Credit is **maintainer-granted** through the Contribution Records system on `new.drupal.org`:

- **Nothing is automatic** — not even the issue creator is credited automatically.
- **Only maintainers grant credit**, via checkboxes on the issue's Contribution Record. Contributors self-attribute work to an employer/customer (if that org has a drupal.org page) through their profile.
- **Credit appears** on user and org profiles once the issue reaches *Fixed* or *Closed*; maintainers can add credit afterward.
- **Impact:** organizations are ranked in the Drupal Marketplace by weighted credit — real financial incentive, hence maintainer oversight matters.
- **Etiquette:** never demand credit; let the contribution speak. Each project sets its own crediting policy.

Credit works identically for GitLab-migrated issues — the Contribution Records system is decoupled from issue hosting.

## Code of Conduct

The Drupal Code of Conduct (updated 2023-07-01) has five pillars:

1. Consider others' needs
2. Disagree respectfully
3. Collaborate openly
4. Zero tolerance for abuse
5. Transition responsibly

Violations go to the **Conflict Resolution Team** via the Incident Report Form at drupal.org/dcoc.

**Issue queue:** be constructive and professional; respect the maintainer's authority; help with existing issues before opening new ones. **Drupal Slack:** check channel topic/pins before posting; use threads; ask in a public channel before DMing. Hate speech and harassment are not tolerated; moderators coach before removing.

## Best-Practice Differences by Workflow

| Dimension | Core | Your own contrib | Someone else's contrib |
|---|---|---|---|
| RTBC discipline | Strict; no self-RTBC as sole author | Relaxed; self-RTBC OK | Strict; no self-RTBC unless allowed |
| Credit decision | Core committers decide | You decide | Maintainer decides |
| Pace expectation | Slow; release-phase limits | You control | Maintainer's pace — be patient |
| Review burden | Multi-reviewer, very strict | You set it | Maintainer sets it |

## Common Mistakes

- Setting RTBC after reading the code but without running the tests — RTBC asserts the full checklist, not just a code read.
- Demanding credit in an issue comment — it signals entitlement and antagonizes maintainers.
- Writing "+1 RTBC" without a substantive review — treated as noise; can damage your reputation with maintainers.
- Self-RTBCing a core issue where you are the sole author — a committer will revert it and leave a note.
- Commenting in a closed issue to add a +1 or report it still happens — open a new issue instead.

## See Also

- [The Drupal Issue Lifecycle](drupal-issue-lifecycle.md)
- [Issue Forks & Merge Requests, Step by Step](issue-forks-merge-requests.md)
- [Serving as a Drupal Module/Theme Maintainer](module-theme-maintainer.md)
- AI overlay: [Contributing with AI — Credit System](../contributing-with-ai/credit-system.md)
- Reference: [drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/issue-etiquette)
- Reference: [drupal.org/drupalorg/blog/the-new-contribution-records-system](https://www.drupal.org/drupalorg/blog/the-new-contribution-records-system)
- Reference: [drupal.org/dcoc](https://www.drupal.org/dcoc)
