---
description: "Choose between drupal/mailgun, Symfony Mailer (Mailer Plus), or Symfony Mailer Lite for routing Drupal email through Mailgun."
tldr: "Use drupal/mailgun 2.1.x as the default for 2026 Drupal sites; choose Mailer Plus only when you need Twig-templated emails, multi-language policies, or signing. Mixing both on the same site causes conflicts."
drupal_version: "10.3+/11/12"
---

# Module Decision

## When to Use

> When choosing the Drupal module(s) that route email through Mailgun. Drupal 10.3+ supports three patterns; pick one and commit to it for the project.

## Decision

| Approach | Use When | Pros | Cons |
|---|---|---|---|
| **drupal/mailgun (classic)** | Default choice; existing site uses `MailManager`/`hook_mail()`; want Mailgun-specific UI controls | Mature (since 2013), 4,000+ sites, queue submodule, tracking toggles, tag support, native admin UI | Maintainers self-describe as "minimally maintained"; Key module integration still pending merge |
| **drupal/symfony_mailer (Mailer Plus)** | New site planning rich HTML email with Twig theming, multi-language, policies; comfortable replacing Drupal's mail system entirely | Twig templates, libraries.yml CSS, signing/encryption, async via Symfony Mailer Queue, EmailBuilder plugins | Invasive (replaces mail system); v2.0 still beta as of Jan 2026; future depends on core direction |
| **drupal/symfony_mailer_lite + Mailgun bridge** | Want Symfony transport without Mailer Plus rewrite; direct migration from Swiftmailer | Lighter than Mailer Plus, modern transport DSN, drop-in Swiftmailer replacement | Requires `drupal/mailsystem`; loses Mailgun module's UI conveniences |
| **Pure core `mailer_dsn` + `symfony/mailgun-mailer`** | Minimal module footprint; team prefers code-config over UI | Zero contrib modules beyond the bridge; modern Symfony transport | No queue submodule, no tracking UI, no test sender |

## Pattern

**Recommended default for 2026: `drupal/mailgun` 2.1.x** + `drupal/mailsystem` for routing.

```bash
ddev composer require drupal/mailgun:^2.1 drupal/mailsystem
ddev drush en mailgun mailsystem -y
```

**Alternative for new HTML-heavy sites: Mailer Plus + Symfony bridge:**

```bash
ddev composer require drupal/symfony_mailer:^2.0 symfony/mailgun-mailer
ddev drush en symfony_mailer symfony_mailer_override -y
```

In `system.mail.yml` for the Symfony approach, the structured `mailer_dsn` field replaces the legacy URI form (Drupal core 10.2+ via [#3399645](https://www.drupal.org/project/drupal/issues/3399645)):

```yaml
mailer_dsn:
  scheme: mailgun+api
  host: default
  user: '{{ MAILGUN_API_KEY }}'
  password: 'mg.example.com'
  options:
    region: us
```

## Common Mistakes
- **Wrong**: Mixing `drupal/mailgun` AND Mailer Plus on the same site → **Right**: Pick one; they fight for the `system.mail` interface.
- **Wrong**: Using Swiftmailer in 2026 → **Right**: Deprecated end of November 2021. Pick one of the three patterns above.
- **Wrong**: Going straight to Mailer Plus for a simple transactional setup → **Right**: Classic mailgun module is enough; Mailer Plus pays off when you need Twig templates, multi-language, signing.

## See Also
- [Module Installation](module-installation.md)
- [Mail Routing](mail-routing.md)
- Reference: [drupal/mailgun project page](https://www.drupal.org/project/mailgun)
- Reference: [Mailer Plus getting started](https://www.drupal.org/docs/contributed-modules/drupal-symfony-mailer/getting-started)
