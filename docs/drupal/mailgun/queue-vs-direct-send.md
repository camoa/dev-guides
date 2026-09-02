---
description: "Decide whether to send Drupal mail through Mailgun immediately or via the queue plugin, with known open issues documented."
tldr: "Use direct send for time-sensitive mail (password resets, OTPs, payment confirmations) and the queue plugin for high-volume or webhook-triggered mail; beware open issues #3165209 and #3346676 that cause infinite re-claim loops with the queue submodule."
drupal_version: "10.3+/11/12"
---

# Queue vs Direct Send

## When to Use

> When deciding whether a given email type should be sent immediately or queued. Mailgun module ships a "Mailgun mailer (queued)" plugin that pushes outgoing mail into Drupal's queue API for cron processing.

## Decision

| Email type | Send mode | Reason |
|---|---|---|
| Password reset, magic link, OTP | **Direct** | User is waiting in the UI; queue delay is unacceptable |
| Payment confirmation, order receipt | **Direct** | Customer expectation of immediacy |
| 2FA code | **Direct** | Time-sensitive; expires |
| Welcome email | **Direct** (or short-queue) | UX expectation; queue OK if cron runs every 1-5 min |
| Daily digest, newsletter | **Queue** | High volume, no urgency |
| Bulk announcement (>500 recipients) | **Queue** | Avoid HTTP timeout and rate limits |
| Webhook-triggered notification | **Queue** | Decouple from incoming webhook processing |

## Pattern

#### Direct send (default)

Once Mailgun module is configured with the standard `mailgun_mail` plugin, all `MailManager::mail()` calls send directly. No queue. The HTTP request blocks until Mailgun's API returns.

```php
// Sends synchronously — request blocks ~100-500ms for API call
$result = $mailManager->mail($module, $key, $to, $langcode, $params, NULL, TRUE);
```

#### Queued send

Configure at `/admin/config/system/mailsystem`:
- Sender: `Mailgun mailer (queued)` (instead of `Mailgun`)

This wraps the API call in a queue item. Cron processes the queue; nothing sends until cron runs.

#### Hybrid — selective queueing

In Mailsystem UI, route specific modules through the queued plugin while keeping critical modules (user, commerce_order) on direct send:

```yaml
# system.mail.yml after Custom entries
modules:
  user:
    none:
      formatter: mailgun_mail
      sender: mailgun_mail        # direct
  webform:
    none:
      formatter: mailgun_mail
      sender: mailgun_send_mail   # queued (note: actual machine name varies)
  newsletter:
    none:
      formatter: mailgun_mail
      sender: mailgun_send_mail   # queued
```

#### Speeding up queue processing

Default cron is hourly — too slow for "queued" to feel transactional. Speed up via:

```bash
# Cron every 5 minutes
*/5 * * * * /usr/bin/curl -s https://example.com/cron/CRON_KEY > /dev/null

# Or run the specific queue out-of-band
*/2 * * * * cd /var/www && drush queue:run mailgun_send_mail
```

## Known Issues with the Queue Submodule (Still Open as of April 2026)

| Issue | Impact | Mitigation |
|---|---|---|
| [#3165209](https://www.drupal.org/project/mailgun/issues/3165209) — `RequeueException` causes infinite re-claim loop | One bad item blocks all queue processing | Monitor queue depth; manually delete stuck items |
| [#3346676](https://www.drupal.org/project/mailgun/issues/3346676) — Sandbox-rejected mails requeue endlessly | Dev environments hammer the API | Don't use queue plugin in dev with sandbox domain |

## Common Mistakes
- **Wrong**: Queueing password resets → **Right**: User waits in UI for the email; cron delay = bad UX.
- **Wrong**: Direct-sending bulk newsletters from a controller → **Right**: HTTP request times out before all sends complete; use queue or batch API.
- **Wrong**: Enabling queue plugin in dev with sandbox domain → **Right**: Hits issue #3346676; sandbox-unauthorized recipients requeue forever.
- **Wrong**: Hourly cron with queue plugin → **Right**: Up to 60 min latency. Use 1-5 min cron, or run `drush queue:run` more frequently.

## See Also
- [Programmatic Sending](programmatic-sending.md)
- Reference: [Mailgun module open issues](https://www.drupal.org/project/issues/mailgun)
