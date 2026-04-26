---
description: Use Mailgun-specific params (tags, tracking, deliverytime, recipient-variables, custom headers) via hook_mail() params passthrough.
tldr: Pass tags, tracking toggles, deliverytime, bcc, and custom headers via $params in MailManager::mail() and copy them to $message['params'] in hook_mail(); Mailgun limits 3 tags per message and rejects deliverytime set in the past.
drupal_version: "11.x"
---

# Mailgun-Specific Params

## When to Use

> Use this when your transactional email needs Mailgun features beyond standard Drupal mail — tags for analytics segmentation, tracking toggles per-message, custom headers, scheduled delivery, or batch personalization.

## Decision

| Param | Type | Effect |
|-------|------|--------|
| `tags` | array | Mailgun analytics filtering. Limit 3 tags per message |
| `tracking` | bool | Master tracking toggle — opens AND clicks |
| `tracking_clicks` | bool | Click tracking only |
| `tracking_opens` | bool | Open tracking only |
| `attachments` | array | File attachments |
| `reply-to` | string | Reply-To header |
| `bcc` / `cc` | string | BCC and CC recipients |
| `deliverytime` | RFC 2822 string | Schedule delivery up to 3 days in the future |
| `recipient-variables` | array (JSON) | Per-recipient personalization for batch sends |
| `o:require-tls` | bool | Force TLS-only delivery |
| `h:X-Custom-Header` | string | Any custom header — `h:` prefix is Mailgun convention |

## Pattern

#### Tags for analytics

```php
$params['tags'] = ['welcome', 'onboarding', 'transactional'];
```

#### Per-message tracking control (sensitive emails)

```php
$params['tracking_opens'] = FALSE;
$params['tracking_clicks'] = FALSE;
```

#### Scheduled delivery

```php
$params['deliverytime'] = (new \DateTime('+2 hours'))->format(\DateTime::RFC2822);
```

Maximum: 3 days in the future. Past times are rejected with 400.

#### Custom headers for webhook correlation

```php
$message['headers']['X-Mailgun-Variables'] = json_encode([
  'order_id' => $order->id(),
  'customer_id' => $customer->id(),
]);
```

These appear in Mailgun's webhook payloads.

#### `List-Unsubscribe` header (bulk-ish transactional)

```php
$message['headers']['List-Unsubscribe'] = '<https://example.com/unsubscribe?token=' . $token . '>';
$message['headers']['List-Unsubscribe-Post'] = 'List-Unsubscribe=One-Click';
```

Required for Gmail/Yahoo bulk-sender compliance (>5,000 emails/day to Gmail).

## Common Mistakes

- **Wrong**: Using more than 3 tags → **Right**: Mailgun limits 3 per message; extras are silently dropped.
- **Wrong**: Setting `deliverytime` to a past date → **Right**: Mailgun rejects with a 400 error.
- **Wrong**: Tracking opens on transactional security emails (password resets, MFA codes) → **Right**: Disable tracking; pixels can be blocked by privacy-aware clients and may flag as suspicious.
- **Wrong**: Putting `bcc` value in headers → **Right**: Pass via `$params['bcc']`; the Mailgun module reads it and sets the API call correctly.

## See Also

- [Programmatic Sending](programmatic-sending.md)
- Reference: [Mailgun message API](https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun/messages)
