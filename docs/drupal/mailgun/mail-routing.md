---
description: Route Drupal emails through Mailgun globally or selectively per module using system.mail.yml and the Mailsystem module.
tldr: Set system.mail.yml interface.default to mailgun_mail to route all Drupal mail through Mailgun, or use the Mailsystem module to route specific modules while keeping others on php_mail; never edit system.mail.yml without running drush cim or cex.
drupal_version: "11.x"
---

# Mail Routing

## When to Use

> Use this after installing the module — to tell Drupal which mail interface to use. Two layers exist: `system.mail.yml` for global routing, and the Mailsystem UI for per-module/per-key overrides.

## Decision

| Goal | Approach |
|------|----------|
| Route ALL Drupal emails through Mailgun | `system.mail.yml` → `default: mailgun_mail` |
| Keep core mail for some, Mailgun for specific modules | `mailsystem` module + Custom entries in UI |
| Test in dev with PHP mail, prod with Mailgun | Per-environment `system.mail.yml` via config-split |
| Different Mailgun keys per email type | Two domains in Mailgun, two interfaces, custom plugins |

## Pattern

#### Global route — all mail goes through Mailgun

```yaml
# config/sync/system.mail.yml
interface:
  default: mailgun_mail
```

Export with `drush cex -y` after switching at `/admin/config/system/mailsystem`.

#### Selective route — keep `php_mail` default, opt specific modules in

```yaml
interface:
  default: php_mail
  mailgun: mailgun_mail
```

In `/admin/config/system/mailsystem`: Add a "Custom" entry → Module: `user`, Mail key: (leave blank for all) → Formatter: `MailgunMail`, Sender: `MailgunMail`. Writes per-module overrides:

```yaml
modules:
  user:
    none:
      formatter: mailgun_mail
      sender: mailgun_mail
```

#### Per-environment routing via config-split

```yaml
# config/sync/system.mail.yml — committed default
interface:
  default: php_mail

# config/splits/prod/system.mail.yml — prod override
interface:
  default: mailgun_mail
```

#### Symfony Mailer (Mailer Plus)

```yaml
interface:
  default: symfony_mailer
mailer_dsn:
  scheme: mailgun+api
  host: default
  user: '{{ MAILGUN_API_KEY }}'
  password: 'mg.example.com'
  options:
    region: us
```

## Common Mistakes

- **Wrong**: Editing `system.mail.yml` directly and forgetting to `drush cim` → **Right**: Either edit via UI then `drush cex`, or edit the file then `drush cim` to load it into active config.
- **Wrong**: Setting `default: mailgun_mail` AND adding per-module Custom entries that also use mailgun_mail → **Right**: Redundant; pick one strategy.
- **Wrong**: Routing user-related mail through Mailgun without testing password reset emails → **Right**: User module's password reset is the most-used transactional path; verify it explicitly.

## See Also

- [UI Configuration](ui-configuration.md)
- [Programmatic Sending](programmatic-sending.md)
- Reference: [drupal/mailsystem](https://www.drupal.org/project/mailsystem)
