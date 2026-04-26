---
description: Verify Mailgun + Drupal integration end-to-end using curl, drush eval, module test form, password reset, and test mode.
tldr: Always run a direct curl test first to isolate Mailgun credential and DNS issues from Drupal, then confirm with drush eval through the full mail stack; API success ("Queued. Thank you.") does not mean delivered — check Mailgun Logs for actual delivery status.
drupal_version: "11.x"
---

# Verification & Testing

## When to Use

> Use this after every configuration change. End-to-end verification ensures DNS, API key, region, routing, and Drupal mail templates all align.

## Decision

| Test type | Tool | When |
|-----------|------|------|
| API connectivity | `curl` direct to Mailgun API | First check — isolates Drupal from credential issues |
| Drush evaluation | `drush php:eval` with MailManager | Confirms full Drupal stack including `hook_mail` |
| Module test form | `/admin/config/services/mailgun/test` | Quick UI sanity check |
| Production smoke test | Real account password reset | Validates end-to-end UX |
| Automated test | PHPUnit `MailInterface` mock OR Mailgun test mode | CI |

## Pattern

#### Test 1 — Direct curl (isolates Drupal)

```bash
export MAILGUN_API_KEY=key-abc...
export MAILGUN_DOMAIN=mg.example.com
export MAILGUN_REGION=api.mailgun.net   # or api.eu.mailgun.net

curl -s --user "api:$MAILGUN_API_KEY" \
  https://$MAILGUN_REGION/v3/$MAILGUN_DOMAIN/messages \
  -F from="Test <postmaster@$MAILGUN_DOMAIN>" \
  -F to=you@example.com \
  -F subject='Direct curl test' \
  -F text='If you got this, Mailgun + DNS work.'
```

Success: `{"id":"<...>","message":"Queued. Thank you."}`.

#### Test 2 — Drush eval (Drupal stack)

```bash
ddev drush php:eval "
  \$result = \Drupal::service('plugin.manager.mail')->mail(
    'mailgun', 'test', 'you@example.com', 'en',
    ['subject' => 'Drush test', 'body' => ['Hello from Drupal']],
    NULL, TRUE
  );
  echo (\$result['result'] ? 'sent' : 'failed') . PHP_EOL;
"
```

#### Test 3 — Module test form

`/admin/config/services/mailgun/test` (requires `mailgun_test_form` submodule). The form output shows the exact API request and response.

#### Test 4 — Real password reset

Most common transactional path. Login page → "Reset your password" → enter email → check inbox. If using Mailsystem, this exercises the User module's `password_reset` key routing through Mailgun.

#### Test 5 — Test mode (CI)

```php
// settings.test.php
$config['mailgun.settings']['test_mode'] = TRUE;
```

Or mock the mail manager entirely:

```php
$container->set('plugin.manager.mail', new TestMailCollector());
// assert $collector->getMails() after operations
```

## Common Mistakes

- **Wrong**: Skipping Test 1 (curl) when Drupal mail "doesn't work" → **Right**: Curl rules out region, API key, and DNS issues independently of Drupal.
- **Wrong**: Testing only with admin's email → **Right**: Sandbox domain authorizes 5 recipients only; admin's email might be authorized while real users aren't.
- **Wrong**: Sending tests from a domain that hasn't propagated DNS → **Right**: Wait for green checkmarks in Mailgun's domain page (5-60 min typically).
- **Wrong**: Confusing "Queued. Thank you." with "Delivered" → **Right**: Check Mailgun dashboard → Logs for actual delivery status.

## See Also

- [Common Errors](common-errors.md)
- Reference: [Mailgun logs UI](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-email-with-mailgun/#logs)
