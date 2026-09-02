---
description: "Suppress hard bounces, complaints, and unsubscribes to protect sender reputation and avoid wasting API calls on dead addresses."
tldr: "Immediately suppress hard bounces and complaints via hook_mail_alter() checking a field_mail_status field on User; reconcile nightly with Mailgun's /v3/<domain>/bounces API because webhooks can be missed."
drupal_version: "10.3+/11/12"
---

# Bounce & Complaint Handling

## When to Use

> For any production site that sends mail to user-supplied addresses. Without bounce handling, you waste API calls on dead addresses, harm sender reputation, and risk being added to anti-spam blocklists.

## Decision

| Event | Suppress immediately? | Action |
|---|---|---|
| **Hard bounce** (`permanent_fail`) | **Yes** | Mark user as bounced; stop sending. Examples: invalid address, deactivated mailbox |
| **Complaint** (`complained`) | **Yes** | Mark user as spam-complained; stop sending. Recipient hit "mark as spam" |
| **Unsubscribe** (`unsubscribed`) | **Yes** | Honor unsubscribe; stop transactional + marketing per their preference |
| **Soft bounce** (`temporary_fail`) | After N retries | Mailgun retries automatically; suppress only after 7+ consecutive soft bounces over 7+ days |

## Pattern

#### Step 1 — Add a `mail_status` field on User entity

```bash
ddev drush entity:create-field --entity-type=user --name=field_mail_status \
  --type=list_string --label='Mail Status' \
  --allowed-values='active|Active' --allowed-values='bounced|Bounced' \
  --allowed-values='complained|Complained' --allowed-values='unsubscribed|Unsubscribed'
```

Default value: `active`.

#### Step 2 — Block sends to suppressed users in `hook_mail_alter()`

```php
function my_module_mail_alter(&$message) {
  $to = $message['to'];
  $user = user_load_by_mail($to);
  if ($user) {
    $status = $user->get('field_mail_status')->value;
    if (in_array($status, ['bounced', 'complained', 'unsubscribed'], TRUE)) {
      // Cancel the send.
      $message['send'] = FALSE;
      \Drupal::logger('my_module')->info(
        'Suppressed mail to @email (status: @status)',
        ['@email' => $to, '@status' => $status]
      );
    }
  }
}
```

#### Step 3 — Pull Mailgun's authoritative suppression lists

Mailgun maintains its own suppression lists at `/v3/<domain>/bounces`, `/v3/<domain>/complaints`, `/v3/<domain>/unsubscribes`. Pull nightly to reconcile:

```php
namespace Drupal\my_module\Commands;

use Drush\Commands\DrushCommands;
use GuzzleHttp\ClientInterface;

class MailgunSuppressionCommands extends DrushCommands {
  public function __construct(
    private readonly ClientInterface $httpClient,
  ) {
    parent::__construct();
  }

  /**
   * Sync Mailgun suppression lists into Drupal user records.
   *
   * @command mailgun:sync-suppressions
   */
  public function syncSuppressions(): void {
    $config = \Drupal::config('mailgun.settings');
    $domain = $config->get('working_domain');
    $endpoint = $config->get('api_endpoint') ?? 'https://api.mailgun.net';
    $key = $config->get('api_key');

    foreach (['bounces' => 'bounced', 'complaints' => 'complained', 'unsubscribes' => 'unsubscribed'] as $list => $status) {
      $url = "$endpoint/v3/$domain/$list";
      $next = $url;
      while ($next) {
        $response = $this->httpClient->get($next, [
          'auth' => ['api', $key],
          'query' => ['limit' => 1000],
        ]);
        $data = json_decode($response->getBody(), TRUE);
        foreach ($data['items'] as $item) {
          $email = $item['address'];
          $user = user_load_by_mail($email);
          if ($user && $user->get('field_mail_status')->value !== $status) {
            $user->set('field_mail_status', $status);
            $user->save();
            $this->logger()->notice("Marked $email as $status");
          }
        }
        $next = $data['paging']['next'] ?? NULL;
      }
    }
  }
}
```

Schedule via cron:

```bash
0 2 * * * cd /var/www && drush mailgun:sync-suppressions
```

#### Step 4 — Soft bounce tracking

Soft bounces aren't a clear suppress signal. Track count + first/last seen on the user; suppress only after a threshold:

```php
private function handleSoftBounce(array $event): void {
  $email = $event['recipient'];
  $user = user_load_by_mail($email);
  if (!$user) return;

  $count = (int) ($user->get('field_soft_bounce_count')->value ?? 0) + 1;
  $user->set('field_soft_bounce_count', $count);
  $user->set('field_last_soft_bounce', \Drupal::time()->getRequestTime());

  // Suppress after 7 soft bounces in 7+ days.
  if ($count >= 7) {
    $user->set('field_mail_status', 'bounced');
  }
  $user->save();
}
```

## Common Mistakes
- **Wrong**: Treating soft bounces as hard → **Right**: Soft bounces (mailbox full, server temporarily down) often resolve. Suppress only persistent ones.
- **Wrong**: Only relying on webhooks → **Right**: Webhooks can be missed (network issues, auth failures, replay rejection). Reconcile nightly with `/v3/.../bounces` API.
- **Wrong**: Suppressing in user data only, not informing Mailgun → **Right**: Mailgun maintains its own suppression list; both should agree. Use `/v3/<domain>/unsubscribes` POST to add Drupal-initiated unsubscribes to Mailgun's list.
- **Wrong**: Including transactional emails (password reset, order confirmation) in unsubscribe scope → **Right**: Distinguish marketing from transactional; legally required transactional mail should still send to unsubscribed-from-marketing users.

## See Also
- [Webhook Handling](webhook-handling.md)
- Reference: [Mailgun suppression API](https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun/bounces)
