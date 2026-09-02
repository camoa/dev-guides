---
description: "Send transactional email programmatically using MailManager::mail() and hook_mail() so routing, queue, and test mode all apply."
tldr: "Implement hook_mail() to set subject/body/headers on $message, then call MailManager::mail() from a service injected with mail.manager; never call the Mailgun PHP SDK directly — it bypasses routing, test mode, and the queue."
drupal_version: "10.3+/11/12"
---

# Programmatic Sending

## When to Use

> When custom code needs to send transactional email — order confirmations, invitations, password resets, onboarding sequences, payment receipts. Use `MailManager` + `hook_mail()` rather than calling Mailgun's API directly so the routing layer applies.

## Decision

| Approach | Use When |
|---|---|
| `MailManager::mail()` + `hook_mail()` | Default — works with `system.mail.yml` routing, supports Mailgun-specific params |
| EmailBuilder plugin (Mailer Plus) | Using Mailer Plus; want Twig templates and policies |
| Direct Mailgun SDK call | Almost never — bypasses routing, mocks, test mode, queue. Only for cases where Drupal's mail abstraction is genuinely wrong (e.g., Mailgun's batch send API for bulk templated mailings) |

## Pattern

#### Step 1 — Implement `hook_mail()` in your module

`my_module.module`:

```php
function my_module_mail($key, &$message, $params) {
  $options = ['langcode' => $message['langcode']];

  switch ($key) {
    case 'welcome':
      $message['subject'] = t('Welcome to @site', ['@site' => $params['site_name']], $options);
      $message['body'][] = $params['body'];
      $message['headers']['Content-Type'] = 'text/html; charset=UTF-8; format=flowed; delsp=yes';

      // Pass-through Mailgun extras to the mailgun_mail plugin.
      $passthrough = ['tags', 'tracking', 'tracking_clicks', 'tracking_opens',
                      'attachments', 'reply-to', 'bcc', 'cc'];
      foreach ($passthrough as $k) {
        if (isset($params[$k])) {
          $message['params'][$k] = $params[$k];
        }
      }
      break;

    case 'order_confirmation':
      $message['subject'] = t('Your order #@id', ['@id' => $params['order_id']]);
      $message['body'][] = $params['body'];
      $message['headers']['Content-Type'] = 'text/html; charset=UTF-8';
      $message['params']['tags'] = ['order', 'transactional'];
      break;
  }
}
```

#### Step 2 — Send the mail from a service or controller

```php
public function sendWelcome(UserInterface $user): bool {
  $params = [
    'site_name' => \Drupal::config('system.site')->get('name'),
    'body' => '<p>Hi <strong>' . $user->getDisplayName() . '</strong>, welcome!</p>',
    'tags' => ['welcome', 'transactional'],
    'tracking' => TRUE,
    'tracking_clicks' => TRUE,
    'tracking_opens' => TRUE,
    'reply-to' => 'support@example.com',
  ];

  $result = $this->mailManager->mail(
    'my_module',
    'welcome',
    $user->getEmail(),
    $user->getPreferredLangcode(),
    $params,
    NULL,    // From — defaults to Mailgun module's "From email" config
    TRUE     // Send immediately
  );

  return !empty($result['result']);
}
```

Inject `mail.manager` into your service:

```yaml
# my_module.services.yml
services:
  my_module.mailer:
    class: Drupal\my_module\MyMailer
    arguments: ['@plugin.manager.mail']
```

```php
// MyMailer.php
public function __construct(
  private readonly MailManagerInterface $mailManager,
) {}
```

#### Step 3 — HTML emails

The `mailgun_mail` plugin natively handles HTML when `Content-Type: text/html` is in headers. Don't use MimeMail or Swiftmailer in 2026.

```php
$message['headers']['Content-Type'] = 'text/html; charset=UTF-8';
$message['body'][] = '<p>HTML content here</p>';
```

For Twig-themed HTML, use Mailer Plus instead — it ships with template suggestions and `*.libraries.yml`-based CSS injection.

#### Step 4 — Attachments

```php
$params['attachments'] = [
  [
    'filepath' => '/sites/default/files/private/invoice-' . $invoice_id . '.pdf',
    'filename' => 'invoice.pdf',
    'filemime' => 'application/pdf',
  ],
];
```

Attachments are passed to Mailgun's API and counted against message size limits (25 MB total per message).

## Common Mistakes
- **Wrong**: Calling Mailgun's PHP SDK directly from a controller → **Right**: Use `MailManager::mail()` so routing, mailsystem, queue, and test mode all apply.
- **Wrong**: Putting subject/body/headers in `$params` and accessing them in `hook_mail()` → **Right**: Set them on `$message` directly. `$params` is for arbitrary data you pass through; `$message` is the standardized output.
- **Wrong**: Forgetting `Content-Type: text/html` for HTML emails → **Right**: Without it, Mailgun receives the HTML as plain text and recipients see raw markup.
- **Wrong**: Hardcoding the From address in `hook_mail()` → **Right**: Let the Mailgun module's "From email" default apply, or pass via the `$from` parameter to `MailManager::mail()`.

## See Also
- [Mailgun-Specific Params](mailgun-specific-params.md)
- [Queue vs Direct Send](queue-vs-direct-send.md)
- Reference: [Drupal MailManager API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Mail%21MailManagerInterface.php)
