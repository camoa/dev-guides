---
description: Install and enable the drupal/mailgun 2.1.x module via Composer, with optional mailsystem and Key module support.
tldr: Require drupal/mailgun:^2.1 and drupal/mailsystem via Composer then enable both; use ^2.1 specifically to get the July 2025 release, and add Key module support via the open patch at issue #3452693 if your project already uses Key.
drupal_version: "11.x"
---

# Module Installation

## When to Use

> Use this after the Mailgun account is set up, the domain is added, and DNS records are verified. Run on the Drupal codebase, then deploy.

## Decision

| Step | Command | Notes |
|------|---------|-------|
| Install via Composer | `ddev composer require drupal/mailgun:^2.1` | Pulls `mailgun/mailgun-php` SDK transitively |
| Enable module | `ddev drush en mailgun -y` | Add `mailsystem` if routing per-module emails |
| Optional sub-module | `ddev drush en mailgun_test_form -y` | Adds a UI test sender at `/admin/config/services/mailgun/test` |
| Optional queue plugin | (configured via Mailsystem UI) | "Mailgun mailer (queued)" appears in Mailsystem dropdowns once mailgun is enabled |

## Pattern

#### Minimum installation

```bash
ddev composer require drupal/mailgun:^2.1
ddev drush en mailgun -y
ddev drush pm:list --status=enabled --type=Module | grep mailgun
```

#### With Mailsystem for per-module routing

```bash
ddev composer require drupal/mailgun:^2.1 drupal/mailsystem
ddev drush en mailgun mailsystem -y
```

#### With Key module (patch required as of April 2026)

```json
"drupal/mailgun": "^2.1",
"drupal/key": "^1.18",
"cweagans/composer-patches": "^1.7"
```

```json
"extra": {
  "patches": {
    "drupal/mailgun": {
      "Add Key module support (issue 3452693)":
        "https://www.drupal.org/files/issues/2025-10-09/3452693_add-key-support-9.patch"
    }
  }
}
```

```bash
ddev composer install
ddev drush en mailgun key -y
```

## Common Mistakes

- **Wrong**: Using `^2.0` constraint → **Right**: Use `^2.1` to get 2.1.0 (July 2025 release) and forward; 2.0.0 is from 2023 and lacks recent fixes.
- **Wrong**: Installing both `drupal/mailgun` AND `drupal/symfony_mailer` (Mailer Plus override mode) → **Right**: They fight for the mail interface. See [Module Decision](module-decision.md).
- **Wrong**: Skipping `drupal/mailsystem` and trying to route per-module emails through admin UI → **Right**: Without mailsystem, you only get a global `default` switch in `system.mail.yml`.

## See Also

- [Settings Configuration](settings-configuration.md)
- [Mail Routing](mail-routing.md)
- Reference: [drupal/mailgun 2.1.0 release](https://www.drupal.org/project/mailgun/releases/2.1.0)
