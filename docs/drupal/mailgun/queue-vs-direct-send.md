---
description: Decide whether to send Drupal mail through Mailgun immediately or via the queue plugin, with known open issues documented.
tldr: Use direct send for time-sensitive mail (password resets, OTPs, payment confirmations) and the queue plugin for high-volume or webhook-triggered mail; beware open issues #3165209 and #3346676 that cause infinite re-claim loops with the queue submodule.
drupal_version: "11.x"
---

# Queue vs Direct Send

## When to Use

> Use this when deciding whether a given email type should be sent immediately or queued. The Mailgun module ships a "Mailgun mailer (queued)" plugin that pushes outgoing mail into Drupal's queue API for cron processing.

## Decision

| Email type | Send mode | Reason |
|------------|-----------|--------|
| Password reset, magic link, OTP | **Direct** | User is waiting in the UI; queue delay is unacceptable |
| Payment confirmation, order receipt | **Direct** | Customer expectation of immediacy |
| 2FA code | **Direct** | Time-sensitive; expires |
| Welcome email | **Direct** (or short-queue) | UX expectation; queue OK if cron runs every 1-5 min |
| Daily digest, newsletter | **Queue** | High volume, no urgency |
| Bulk announcement (>500 recipients) | **Queue** | Avoid HTTP timeout and rate limits |
| Webhook-triggered notification | **Queue** | Decouple from incoming webhook processing |

## Pattern

#### Direct send (default)

```php
// Sends synchronously — request blocks ~100-500ms for API call
$result = $mailManager->mail($module, $key, $to, $langcode, $params, NULL, TRUE);
```

#### Queued send

Configure at `/admin/config/system/mailsystem`:
- Sender: `Mailgun mailer (queued)`

Nothing sends until cron processes the queue.

#### Hybrid — selective queueing

```yaml
modules:
  user:
    none:
      sender: mailgun_mail        # direct
  newsletter:
    none:
      sender: mailgun_send_mail   # queued
```

#### Speed up queue processing (default hourly is too slow)

```bash
*/5 * * * * /usr/bin/curl -s https://example.com/cron/CRON_KEY > /dev/null
# Or run the specific queue
*/2 * * * * cd /var/www && drush queue:run mailgun_send_mail
```

#### Known open issues (April 2026)

| Issue | Impact | Mitigation |
|-------|--------|------------|
| [#3165209](https://www.drupal.org/project/mailgun/issues/3165209) — `RequeueException` infinite re-claim loop | One bad item blocks all queue processing | Monitor queue depth; manually delete stuck items |
| [#3346676](https://www.drupal.org/project/mailgun/issues/3346676) — Sandbox-rejected mails requeue endlessly | Dev environments hammer the API | Don't use queue plugin in dev with sandbox domain |

## Common Mistakes

- **Wrong**: Queueing password resets → **Right**: User waits in UI for the email; cron delay = bad UX.
- **Wrong**: Direct-sending bulk newsletters from a controller → **Right**: HTTP request times out; use queue or batch API.
- **Wrong**: Enabling queue plugin in dev with sandbox domain → **Right**: Hits issue #3346676; sandbox-unauthorized recipients requeue forever.
- **Wrong**: Hourly cron with queue plugin → **Right**: Up to 60 min latency. Use 1-5 min cron or run `drush queue:run` more frequently.

## See Also

- [Programmatic Sending](programmatic-sending.md)
- Reference: [Mailgun module open issues](https://www.drupal.org/project/issues/mailgun)
