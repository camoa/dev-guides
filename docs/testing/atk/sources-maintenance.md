---
description: "Source references and maintenance manifest for the atk guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Web Sources
| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Drupal.org project page | https://www.drupal.org/project/automated_testing_kit | 1, 4, 5, 18 | 2026-05-08 |
| Releases page | https://www.drupal.org/project/automated_testing_kit/releases | 4, 18 | 2026-05-08 |
| Canonical repo | https://git.drupalcode.org/project/automated_testing_kit | 4, 17, 18 | 2026-05-08 |
| Demo recipe project page | https://www.drupal.org/project/automated_testing_kit_demo_recipe | 5, 18 | 2026-05-08 |
| qa_accounts project page | https://www.drupal.org/project/qa_accounts | 5, 18 | 2026-05-08 |
| Vendor docs (PerformantLabs) | https://performantlabs.com/automated-testing-kit/ | 18 | 2026-05-08 |
| Lullabot/playwright-drupal | https://github.com/Lullabot/playwright-drupal | 2, 16, 18 | 2026-05-08 |
| Lullabot/ddev-playwright | https://github.com/Lullabot/ddev-playwright | 13, 18 | 2026-05-08 |
| ddev/github-action-setup-ddev | https://github.com/ddev/github-action-setup-ddev | 13, 18 | 2026-05-08 |
| Drupal core issue #3467492 (Replace Nightwatch with Playwright) | https://www.drupal.org/project/drupal/issues/3467492 | 2, 18 | 2026-05-08 |

## Code Sources
`automated_testing_kit` and `qa_accounts` are not present under `/home/camoa/workspace/contrib/web/modules/contrib/` — neither module is installed on the research site. No installed ATK source was read for this guide. Every code sample (selector hook attribute name, helper function names, Drush command names, `atk_prerequisites.yml` shape, Testor subcommands) is example code from the guide's own text, and the guide repeatedly flags these as needing verification against the current module (see sections 7, 8, 9, 10, 12, 18: "verify against your repo" / "verify exact ... against the current"). Treat those names as unverified pending an install.

| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| automated_testing_kit | not installed on research site — not verified in this pass | 5-14, 17, 18 | 2.0.0 stable (per TRACKS input; not read from an installed `.info.yml`) |
| qa_accounts | not installed on research site — not verified in this pass | 5, 7, 10, 18 | not verified in this pass |

## Version History
| Date | Change |
|------|--------|
| 2026-05-08 | Manifest reconstructed from the guide's own citations and the installed source. |
