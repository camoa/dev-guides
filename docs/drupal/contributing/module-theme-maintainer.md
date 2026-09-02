---
description: Serving as a Drupal module or theme maintainer — queue management, owning the CI config, credit decisions, reviewing AI-assisted MRs, and co-maintainer succession
tldr: "As maintainer you own the `.gitlab-ci.yml` (make phpcs blocking at minimum), the triage queue (respond promptly), and all credit decisions. If you can no longer maintain a project, add a co-maintainer before stepping down."
drupal_version: "11.x"
---

# Serving as a Drupal Module/Theme Maintainer

## When to Use

> Use this when you own or co-own a contrib module or theme on drupal.org. The maintainer role has different responsibilities from being a contributor — you own the CI config, the triage queue, the credit decisions, and the release process.

## When to Use This Role

You are a maintainer when: you created the project, were added as a co-maintainer, or have been given the "maintainer" role on `drupal.org/project/<name>`. The maintainer role carries full authority and full accountability for the project's health.

## Queue Management

Triage promptly and politely. The etiquette:

- Respond to new issues within a reasonable time — even "confirmed, added to the queue" keeps contributors engaged.
- Fix incorrect issue field values (status, priority, category, component).
- Encourage contribution — acknowledge effort even when feedback is needed.
- Offer co-maintainership to skilled regulars who contribute repeatedly.
- Mentor newcomers on your subsystem's patterns.

A stale queue (unresponded issues, unreviewed MRs) deters contribution and signals abandonment, which can trigger Drupal.org to mark the project as unsupported.

## Owning and Maintaining the CI Config

As maintainer you own the `.gitlab-ci.yml` — you decide which jobs are blocking. Best practice for a healthy module:

```yaml
# Make phpcs blocking (recommended for all modules)
phpcs:
  allow_failure: false

# Make phpstan blocking when you have it configured
phpstan:
  allow_failure: false

# Opt into previous-major testing when you support two Drupal major versions
variables:
  OPT_IN_TEST_PREVIOUS_MAJOR: "1"
  _TARGET_CORE: "^10 || ^11"
```

Keep `gitlab_templates` auto-updating by not pinning `_GITLAB_TEMPLATES_REF` to a fixed tag unless you have a specific reason to freeze. The DA updates the tag regularly (v1.15.4 as of May 2026).

## Credit Decisions

Credit is your call as maintainer. Recommended practice:

- Credit all contributors who made substantive contributions to the issue (code, tests, documentation, review).
- Credit organizations for contributors who mark employer sponsorship on their profile.
- Do not wait to be asked — proactively apply credit when closing an issue.
- You can add credit after the issue is closed.

See [Contribution Records](https://www.drupal.org/drupalorg/blog/the-new-contribution-records-system) for the API endpoints if you need to bulk-query credit data.

## Reviewing AI-Assisted MRs

AI-assisted contributions require extra review discipline from maintainers. Signs of an insufficiently reviewed AI contribution:

- Code that passes phpcs but contains no tests
- Logic that looks plausible but doesn't match the stated issue
- Dependencies on APIs or behaviors that are guessed rather than verified
- Docblocks that describe a function differently from its implementation

The [Drupal AI contribution policy](https://www.drupal.org/docs/develop/development-tools/ai-tools/ai-policy-for-drupal-contributors) (adopted 2026-04-23) places full responsibility on the contributor, not the AI tool. As maintainer you are not responsible for verifying AI use — but you are responsible for ensuring the code is correct. Apply the same quality bar regardless of how the code was produced.

For the complete AI overlay — disclosure requirements, the "significant portion" threshold, acceptable vs. unacceptable AI use — see `drupal/contributing-with-ai/`.

## Co-maintainer Succession

If you can no longer maintain a project:

- Add a co-maintainer before stepping down so the project is not orphaned.
- Use the drupal.org project page to transfer maintainership.
- If the project is unmaintained, mark it as such on drupal.org so users are warned.

Abandoning a project without marking it unsupported or transferring it harms the users who depend on it and reflects on the Drupal ecosystem.

## Common Mistakes

- Leaving phpcs as `allow_failure: true` on a module you maintain — set it to blocking; it is a basic quality signal.
- Not updating the CI config when Drupal releases a new minor or major — run `OPT_IN_TEST_NEXT_MINOR` to validate before the release.
- Merging MRs without running their tests locally — CI passes are not a substitute for understanding the change.
- Forgetting to grant credit when closing an issue — go back and add it; contributors notice.
- Abandoning a module without marking it unsupported — orphaned modules cause security and compatibility problems for users.

## See Also

- [Contrib Project Scaffolding](contrib-project-scaffolding.md)
- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md)
- AI overlay: [Contributing with AI — Human Review Requirements](../contributing-with-ai/human-review-requirements.md)
- Reference: [drupal.org/community/contributor-guide/role/contributed-module-theme-or-distribution-maintainer](https://www.drupal.org/community/contributor-guide/role/contributed-module-theme-or-distribution-maintainer)
- Reference: [drupal.org/docs/develop/issues/issue-procedures-and-etiquette/maintaining-and-responding-to-issues-for-a-project](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/maintaining-and-responding-to-issues-for-a-project)
