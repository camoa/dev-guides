---
description: Receive and verify Mailgun webhook events (delivery, bounces, complaints) via a custom Drupal controller with HMAC signature validation.
tldr: Build a custom controller at a no-cache, no-CSRF route to receive Mailgun webhook POST requests; always verify the HMAC signature and reject events older than 5 minutes to prevent replay attacks — the drupal/mailgun module does not ship a webhook receiver as of 2.1.0.
drupal_version: "11.x"
---

# Webhook Handling

## When to Use

> Use this when you need Drupal to react to Mailgun events — delivery, opens, clicks, bounces, complaints, unsubscribes. Critical for: bounce list cleanup, engagement scoring, audit trails, retry logic on temp failures.

## Decision

| Event | Action |
|-------|--------|
| `accepted` | Mailgun received the message; not yet delivered |
| `delivered` | Mailgun delivered to recipient's mail server |
| `opened` | Recipient opened (tracking pixel hit) |
| `clicked` | Recipient clicked a tracked link |
| `unsubscribed` | Recipient hit the unsubscribe link |
| `complained` | Recipient marked as spam — **immediate suppress** |
| `permanent_fail` | Hard bounce (invalid address) — **immediate suppress** |
| `temporary_fail` | Soft bounce — Mailgun retries; track for repeated soft bounces |

## Pattern

`drupal/mailgun` does NOT ship a webhook receiver as of 2.1.0 ([issue #3175875](https://www.drupal.org/project/mailgun/issues/3175875)). Build a custom controller.

#### Route definition

```yaml
# my_mailgun_webhooks.routing.yml
my_mailgun_webhooks.receive:
  path: '/mailgun/webhook'
  defaults:
    _controller: '\Drupal\my_mailgun_webhooks\Controller\WebhookController::receive'
  methods: [POST]
  requirements:
    _access: 'TRUE'
  options:
    no_cache: TRUE
    _csrf: FALSE
```

#### Controller with HMAC verification and replay protection

```php
public function receive(Request $request): JsonResponse {
  $payload = json_decode($request->getContent(), TRUE);
  if (!isset($payload['signature'], $payload['event-data'])) {
    return new JsonResponse(['error' => 'Invalid payload'], 400);
  }

  $signing_key = getenv('MAILGUN_WEBHOOK_SIGNING_KEY');
  $expected = hash_hmac('sha256',
    $payload['signature']['timestamp'] . $payload['signature']['token'],
    $signing_key
  );
  if (!hash_equals($expected, $payload['signature']['signature'])) {
    return new JsonResponse(['error' => 'Invalid signature'], 401);
  }

  // Replay protection — reject if timestamp older than 5 minutes.
  if (abs(time() - (int) $payload['signature']['timestamp']) > 300) {
    return new JsonResponse(['error' => 'Stale request'], 401);
  }

  $event = $payload['event-data'];
  match ($event['event']) {
    'permanent_fail' => $this->handleHardBounce($event),
    'complained'     => $this->handleComplaint($event),
    'unsubscribed'   => $this->handleUnsubscribe($event),
    'temporary_fail' => $this->handleSoftBounce($event),
    default          => $this->logEvent($event),
  };

  return new JsonResponse(['status' => 'ok']);
}
```

#### Mailgun dashboard configuration

Sending → Webhooks → Add webhook:
- URL: `https://example.com/mailgun/webhook`
- Events: `delivered`, `permanent_fail`, `complained`, `unsubscribed`

Get signing key: Sending → Webhook security → "HTTP webhook signing key". Store as env var `MAILGUN_WEBHOOK_SIGNING_KEY`.

## Common Mistakes

- **Wrong**: Skipping HMAC signature verification → **Right**: Without it, anyone can POST fake events and corrupt user data.
- **Wrong**: Reusing one webhook URL for staging and production → **Right**: Webhooks are per-environment; stage events shouldn't update prod data.
- **Wrong**: Synchronous heavy processing inside the webhook handler → **Right**: Mailgun expects 2xx within ~10 seconds. Push heavy work to a queue from the handler.
- **Wrong**: Trusting `event-data` without validating timestamp → **Right**: Replay attacks are possible; reject events older than ~5 min.

## See Also

- [Bounce & Complaint Handling](bounce-complaint-handling.md)
- Reference: [Mailgun webhook signing](https://documentation.mailgun.com/docs/mailgun/api-reference/send/mailgun/webhooks)
- Reference: [Issue #3175875 — webhook submodule](https://www.drupal.org/project/mailgun/issues/3175875)
