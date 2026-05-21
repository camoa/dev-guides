---
description: Serving as a Drupal module or theme maintainer — queue management, owning the CI config, credit decisions, reviewing AI-assisted MRs, and co-maintainer succession
tldr: "As maintainer you own the `.gitlab-ci.yml` (make phpcs blocking at minimum), the triage queue (respond promptly), and all credit decisions. If you can no longer maintain a project, add a co-maintainer before stepping down."
drupal_version: "11.x"
---

# Serving as a Drupal Module/Theme Maintainer

## When to Use

> Use this when you own or co-own a contrib module or theme on drupal.org. The maintainer role has different responsibilities from being a contributor — you own the CI config, the triage queue, the credit decisions, and the release process.

## Decision

| Dimension | Maintainer responsibility |
|---|---|
| CI config | You define which jobs are blocking — make phpcs blocking at minimum |
| Triage | Respond to new issues promptly; fix incorrect field values; encourage contribution |
| Credit | Your call — grant proactively; never wait to be asked |
| AI-assisted MRs | Apply the same quality bar regardless of how code was produced |
| Succession | Add a co-maintainer before stepping down; mark unsupported if orphaning |

## Pattern

**CI config best practice for a healthy module:**

```yaml
# Make phpcs blocking (recommended for all modules)
phpcs:
  allow_failure: false

# Make phpstan blocking when configured
phpstan:
  allow_failure: false

# Opt into previous-major testing when supporting two Drupal majors
variables:
  OPT_IN_TEST_PREVIOUS_MAJOR: "1"
  _TARGET_CORE: "^10 || ^11"
```

Keep `gitlab_templates` auto-updating by not pinning `_GITLAB_TEMPLATES_REF` to a fixed tag unless you have a specific reason to freeze.

## Queue Management

- Respond to new issues promptly — even "confirmed, added to the queue" keeps contributors engaged
- Fix incorrect issue field values (status, priority, category, component)
- Offer co-maintainership to skilled regulars
- A stale queue can trigger drupal.org to mark the project as unsupported

## Reviewing AI-Assisted MRs

Signs of an insufficiently reviewed AI contribution:
- Code that passes phpcs but contains no tests
- Logic that looks plausible but doesn't match the stated issue
- Dependencies on APIs or behaviors that are guessed rather than verified
- Docblocks that describe a function differently from its implementation

The [Drupal AI contribution policy](https://www.drupal.org/docs/develop/development-tools/ai-tools/ai-policy-for-drupal-contributors) (adopted 2026-04-23) places full responsibility on the contributor, not the AI tool. As maintainer, apply the same quality bar regardless of how code was produced.

## Credit Decisions

- Credit all contributors who made substantive contributions (code, tests, docs, review)
- Credit organizations for contributors who mark employer sponsorship
- Apply credit proactively when closing an issue — you can add it after closing too

## Common Mistakes

- **Wrong**: Leaving phpcs as `allow_failure: true` → **Right**: Set it to blocking; it is a basic quality signal
- **Wrong**: Not updating CI config when Drupal releases a new minor/major → **Right**: Run `OPT_IN_TEST_NEXT_MINOR` to validate before release
- **Wrong**: Merging MRs without running their tests locally → **Right**: CI passes do not substitute for understanding the change
- **Wrong**: Forgetting to grant credit when closing an issue → **Right**: Go back and add it; contributors notice
- **Wrong**: Abandoning a module without marking it unsupported → **Right**: Orphaned modules cause security and compatibility problems

## See Also

- [Contrib Project Scaffolding](contrib-project-scaffolding.md)
- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Contribution Etiquette, RTBC & Credit](contribution-etiquette-rtbc-credit.md)
- AI overlay: [Contributing with AI — Human Review Requirements](../contributing-with-ai/human-review-requirements.md)
- Reference: [drupal.org/community/contributor-guide/role/contributed-module-theme-or-distribution-maintainer](https://www.drupal.org/community/contributor-guide/role/contributed-module-theme-or-distribution-maintainer)
- Reference: [drupal.org/docs/develop/issues/issue-procedures-and-etiquette/maintaining-and-responding-to-issues-for-a-project](https://www.drupal.org/docs/develop/issues/issue-procedures-and-etiquette/maintaining-and-responding-to-issues-for-a-project)
