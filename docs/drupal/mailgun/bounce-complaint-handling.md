---
description: Suppress hard bounces, complaints, and unsubscribes to protect sender reputation and avoid wasting API calls on dead addresses.
tldr: Immediately suppress hard bounces and complaints via hook_mail_alter() checking a field_mail_status field on User; reconcile nightly with Mailgun's /v3/<domain>/bounces API because webhooks can be missed.
drupal_version: "11.x"
---

# Bounce & Complaint Handling

## When to Use

> Use this for any production site that sends mail to user-supplied addresses. Without bounce handling, you waste API calls on dead addresses, harm sender reputation, and risk being added to anti-spam blocklists.

## Decision

| Event | Suppress immediately? | Action |
|-------|----------------------|--------|
| **Hard bounce** (`permanent_fail`) | **Yes** | Mark user as bounced; stop sending |
| **Complaint** (`complained`) | **Yes** | Mark user as spam-complained; stop sending |
| **Unsubscribe** (`unsubscribed`) | **Yes** | Honor unsubscribe; stop transactional + marketing |
| **Soft bounce** (`temporary_fail`) | After N retries | Mailgun retries automatically; suppress only after 7+ consecutive over 7+ days |

## Pattern

#### Step 1 — Add a `mail_status` field on User entity

```bash
ddev drush entity:create-field --entity-type=user --name=field_mail_status \
  --type=list_string --label='Mail Status' \
  --allowed-values='active|Active' --allowed-values='bounced|Bounced' \
  --allowed-values='complained|Complained' --allowed-values='unsubscribed|Unsubscribed'
```

#### Step 2 — Block sends to suppressed users in `hook_mail_alter()`

```php
function my_module_mail_alter(&$message) {
  $user = user_load_by_mail($message['to']);
  if ($user) {
    $status = $user->get('field_mail_status')->value;
    if (in_array($status, ['bounced', 'complained', 'unsubscribed'], TRUE)) {
      $message['send'] = FALSE;
      \Drupal::logger('my_module')->info(
        'Suppressed mail to @email (status: @status)',
        ['@email' => $message['to'], '@status' => $status]
      );
    }
  }
}
```

#### Step 3 — Reconcile nightly with Mailgun's suppression API

```php
// Drush command: drush mailgun:sync-suppressions
foreach (['bounces' => 'bounced', 'complaints' => 'complained', 'unsubscribes' => 'unsubscribed'] as $list => $status) {
  $url = "$endpoint/v3/$domain/$list";
  // paginated GET with auth: ['api', $key]
  // update field_mail_status on matching user accounts
}
```

Schedule: `0 2 * * * cd /var/www && drush mailgun:sync-suppressions`

#### Step 4 — Soft bounce tracking (suppress after threshold)

```php
private function handleSoftBounce(array $event): void {
  $user = user_load_by_mail($event['recipient']);
  if (!$user) return;
  $count = (int) ($user->get('field_soft_bounce_count')->value ?? 0) + 1;
  $user->set('field_soft_bounce_count', $count);
  if ($count >= 7) {
    $user->set('field_mail_status', 'bounced');
  }
  $user->save();
}
```

## Common Mistakes

- **Wrong**: Treating soft bounces as hard → **Right**: Soft bounces (mailbox full, server temporarily down) often resolve. Suppress only persistent ones.
- **Wrong**: Only relying on webhooks → **Right**: Webhooks can be missed. Reconcile nightly with `/v3/.../bounces` API.
- **Wrong**: Suppressing in Drupal only, not informing Mailgun → **Right**: Use `/v3/<domain>/unsubscribes` POST to add Drupal-initiated unsubscribes to Mailgun's list too.
- **Wrong**: Including transactional emails in unsubscribe scope → **Right**: Distinguish marketing from transactional; legally required transactional mail should still send to marketing-unsubscribed users.

## See Also

- [Webhook Handling](webhook-handling.md)
- Reference: [Mailgun suppression API](https://documentation.mailgun.com/docs/mailgun/api-reference/suppressions/bounces)
