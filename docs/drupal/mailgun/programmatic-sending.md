---
description: Send transactional email programmatically using MailManager::mail() and hook_mail() so routing, queue, and test mode all apply.
tldr: Implement hook_mail() to set subject/body/headers on $message, then call MailManager::mail() from a service injected with mail.manager; never call the Mailgun PHP SDK directly — it bypasses routing, test mode, and the queue.
drupal_version: "11.x"
---

# Programmatic Sending

## When to Use

> Use `MailManager::mail()` + `hook_mail()` when custom code needs to send transactional email — order confirmations, invitations, password resets, onboarding sequences, payment receipts. This approach ensures the routing layer applies.

## Decision

| Approach | Use When |
|----------|----------|
| `MailManager::mail()` + `hook_mail()` | Default — works with `system.mail.yml` routing, supports Mailgun-specific params |
| EmailBuilder plugin (Mailer Plus) | Using Mailer Plus; want Twig templates and policies |
| Direct Mailgun SDK call | Almost never — bypasses routing, mocks, test mode, queue |

## Pattern

#### Step 1 — Implement `hook_mail()` in your module

```php
// my_module.module
function my_module_mail($key, &$message, $params) {
  switch ($key) {
    case 'welcome':
      $message['subject'] = t('Welcome to @site', ['@site' => $params['site_name']]);
      $message['body'][] = $params['body'];
      $message['headers']['Content-Type'] = 'text/html; charset=UTF-8';
      // Pass Mailgun extras through.
      foreach (['tags', 'tracking', 'tracking_clicks', 'tracking_opens', 'reply-to', 'bcc'] as $k) {
        if (isset($params[$k])) {
          $message['params'][$k] = $params[$k];
        }
      }
      break;
  }
}
```

#### Step 2 — Send from a service

```php
// Inject mail.manager into your service:
// arguments: ['@plugin.manager.mail']
public function sendWelcome(UserInterface $user): bool {
  $params = [
    'site_name' => \Drupal::config('system.site')->get('name'),
    'body' => '<p>Hi <strong>' . $user->getDisplayName() . '</strong>, welcome!</p>',
    'tags' => ['welcome', 'transactional'],
    'tracking' => TRUE,
  ];

  $result = $this->mailManager->mail(
    'my_module', 'welcome', $user->getEmail(),
    $user->getPreferredLangcode(), $params, NULL, TRUE
  );
  return !empty($result['result']);
}
```

#### HTML emails

```php
$message['headers']['Content-Type'] = 'text/html; charset=UTF-8';
$message['body'][] = '<p>HTML content here</p>';
```

For Twig-themed HTML, use Mailer Plus — it ships with template suggestions and `*.libraries.yml`-based CSS injection.

#### Attachments

```php
$params['attachments'] = [
  [
    'filepath' => '/sites/default/files/private/invoice-' . $invoice_id . '.pdf',
    'filename' => 'invoice.pdf',
    'filemime' => 'application/pdf',
  ],
];
```

Attachments are counted against Mailgun's 25 MB per-message limit.

## Common Mistakes

- **Wrong**: Calling Mailgun's PHP SDK directly from a controller → **Right**: Use `MailManager::mail()` so routing, mailsystem, queue, and test mode all apply.
- **Wrong**: Putting subject/body/headers in `$params` → **Right**: Set them on `$message` in `hook_mail()`. `$params` is for arbitrary pass-through data.
- **Wrong**: Forgetting `Content-Type: text/html` for HTML emails → **Right**: Without it, Mailgun receives HTML as plain text and recipients see raw markup.
- **Wrong**: Hardcoding the From address in `hook_mail()` → **Right**: Let the Mailgun module's "From email" default apply.

## See Also

- [Mailgun-Specific Params](mailgun-specific-params.md)
- [Queue vs Direct Send](queue-vs-direct-send.md)
- Reference: [Drupal MailManager API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Mail%21MailManagerInterface.php)
