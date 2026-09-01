---
description: "Source references and maintenance manifest for the mailgun guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| Mailgun module project page | https://www.drupal.org/project/mailgun | 1.1, 4.1, 8.1, 11.1 | 2026-04-26 |
| Mailgun module 2.1.0 release | https://www.drupal.org/project/mailgun/releases/2.1.0 | 4.1 | 2026-04-26 |
| Issue #3452693 — Key module support | https://www.drupal.org/node/3452693 | 4.1, 8.1 | 2026-04-26 |
| Issue #3175875 — Webhook submodule | https://www.drupal.org/project/mailgun/issues/3175875 | 12.1 | 2026-04-26 |
| Issue #3165209 — Queue RequeueException | https://www.drupal.org/project/mailgun/issues/3165209 | 11.1 | 2026-04-26 |
| Issue #3346676 — Sandbox queue loop | https://www.drupal.org/project/mailgun/issues/3346676 | 11.1 | 2026-04-26 |
| Mailer Plus (drupal/symfony_mailer) | https://www.drupal.org/project/symfony_mailer | 1.1 | 2026-04-26 |
| Mailer Plus getting started | https://www.drupal.org/docs/contributed-modules/drupal-symfony-mailer/getting-started | 1.1 | 2026-04-26 |
| Symfony Mailer Lite | https://www.drupal.org/project/symfony_mailer_lite | 1.1 | 2026-04-26 |
| drupal/mailsystem | https://www.drupal.org/project/mailsystem | 1.1, 6.1 | 2026-04-26 |
| Core mailer_dsn structured config (#3399645) | https://www.drupal.org/project/drupal/issues/3399645 | 1.1, 6.1 | 2026-04-26 |
| Symfony Mailgun bridge | https://github.com/symfony/mailgun-mailer | 1.1, 6.1 | 2026-04-26 |
| Mailgun docs — domains | https://documentation.mailgun.com/docs/mailgun/user-manual/domains/ | 2.1, 3.1 | 2026-04-26 |
| Mailgun docs — DKIM Security | https://documentation.mailgun.com/docs/mailgun/user-manual/domains/dkim_security | 2.1 | 2026-04-26 |
| Mailgun docs — sandbox limits | https://help.mailgun.com/hc/en-us/articles/217531258-Authorized-Recipients | 7.1, 14.1, 15.1 | 2026-04-26 |
| Mailgun webhooks API | https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun/webhooks | 12.1 | 2026-04-26 |
| Mailgun message API | https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun/messages | 10.1 | 2026-04-26 |
| Mailgun pricing | https://www.mailgun.com/pricing/ | 17.1 | 2026-04-26 |
| Mailgun suppression API | https://documentation.mailgun.com/docs/mailgun/api-reference/suppressions/bounces | 13.1 | 2026-04-26 |
| Picozzi 2025 walkthrough | https://picozzi.com/notebook/2025/jul/drupal-mailgun-simple-setup-transactional-email | 4.1, 5.1, 7.1 | 2026-04-26 |
| Drupal MailManager API | https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Mail%21MailManagerInterface.php | 9.1 | 2026-04-26 |
| Drupal config override system | https://www.drupal.org/docs/8/api/configuration-api/configuration-override-system | 5.1, 8.1 | 2026-04-26 |
| drupal/brevo | https://www.drupal.org/project/brevo | 16.1 | 2026-04-26 |
| drupal/sendgrid_integration | https://www.drupal.org/project/sendgrid_integration | 16.1 | 2026-04-26 |

## Code Sources

| Module | Relative path | Guide sections | Drupal version |
|--------|---------------|----------------|----------------|
| Mailgun (contrib) | `web/modules/contrib/mailgun/` | 4.1, 5.1, 6.1, 9.1, 10.1, 11.1 | 2.1.0 (D10.3+/D11/D12) |
| Mail System (contrib) | `web/modules/contrib/mailsystem/` | 6.1, 11.1 | 8.x-4.5 |
| Symfony Mailer (Mailer Plus) | `web/modules/contrib/symfony_mailer/` | 1.1 | 2.0.0-beta4 / 1.6.2 stable |
| Mailgun PHP SDK | `vendor/mailgun/mailgun-php/` | 4.1 | latest stable |
| Symfony Mailgun bridge | `vendor/symfony/mailgun-mailer/` | 1.1, 6.1 | latest stable |

## Origin
Initial setup runbook reconstructed from `~/workspace/ixp-dev` commit `ddcee964` (2025-09-12, Brevo→Mailgun migration). Expanded for v2.0 with comprehensive 2026 research covering programmatic sending, queue patterns, webhook handling, bounce/complaint suppression, and provider comparison.

---

*Version 2.0.0 — Updated 2026-04-26 (was v1.0 reconstruction-only runbook)*
