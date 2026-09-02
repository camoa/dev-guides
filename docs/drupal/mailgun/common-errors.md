---
description: "Diagnose common Mailgun + Drupal errors including 401 Unauthorized, 421 not verified, 404 domain not found, sandbox restrictions, and HTML rendering failures."
tldr: "Most failures fall into four categories — region mismatch (401), DNS not propagated (421), wrong working_domain (404), and sandbox recipient restriction; start with a direct curl test to isolate the layer before debugging Drupal."
drupal_version: "10.3+/11/12"
---

# Common Errors

## When to Use

> When tests fail or production mail doesn't deliver. Most issues fall into a small number of categories with deterministic fixes.

## Decision

| Symptom | Likely cause | Fix |
|---|---|---|
| `401 Unauthorized` (region OK in dropdown) | Used Public API key instead of Private/Sending | Mailgun → API Security → use Private/Sending key |
| `401 Unauthorized` (key looks right) | Region mismatch — US key on EU endpoint or vice versa | Check Mailgun dashboard URL (`app.mailgun.com` = US, `app.eu.mailgun.com` = EU); match `api_endpoint` |
| `401 Unauthorized` (region matches) | Domain not added in Mailgun for that region | Add domain in correct region's dashboard |
| `404 Domain not found` | Typo in `working_domain` | Match exact spelling shown in Mailgun dashboard |
| `421 Domain not verified` | DNS not yet propagated | Wait up to 48h; verify with `dig` |
| `421 Domain not verified` (DNS looks right) | Click "Verify DNS Settings" in Mailgun dashboard to trigger re-check | Manual verify required after DNS edits |
| Email accepted by API but not delivered | Sandbox domain restriction — recipient not authorized | Add recipient in Mailgun → Domain Settings → Authorized Recipients OR upgrade off Free plan |
| Email rejected with `Free accounts are restricted` | Free plan limits | Add a credit card to unlock unverified recipients |
| Sender shown as `postmaster@sandboxXXX.mailgun.org` | Using sandbox domain in production config | Configure your real domain (`mg.example.com`) |
| `Rate limit exceeded` (429) | Burst above plan's per-second cap | Throttle via queue submodule, or upgrade plan |
| HTML email arrives as raw markup | Missing `Content-Type: text/html` header | Add to `$message['headers']` in `hook_mail()` |
| Test email lands in spam | DKIM/SPF/DMARC not aligned | Run mail through https://mail-tester.com to identify alignment issues |
| Double-send issue (queue + direct on same mail) | Two senders configured on same mail key | Check Mailsystem UI for duplicate Custom entries |

## Pattern

#### Diagnostic decision tree

```
Email not arriving
├─ Does curl test (Test 1) succeed?
│   ├─ NO → API key, region, or DNS issue
│   │       Check: Mailgun dashboard which region; key prefix
│   │       Verify: `dig` SPF, DKIM CNAMEs
│   └─ YES → Drupal layer issue
│            └─ Does drush eval (Test 2) succeed?
│                ├─ NO → hook_mail not implemented or wrong key
│                │       Check: enable `kint` to dump $message inside hook
│                └─ YES → Mailgun received but didn't deliver
│                          Check: Mailgun → Logs → status reason
│                          Common: sandbox restriction, hard bounce, complaint
```

#### Verbose logging during debug

Enable Mailgun module's logging:

```yaml
# config/sync/mailgun.settings.yml (only enable temporarily)
debug_mode: true
```

Then check `/admin/reports/dblog` filtered by `mailgun` — the API request/response is logged.

For deeper debug, hook the API client:

```php
// In your debug code (settings.local.php)
\Drupal::logger('mailgun_debug')->debug(
  'Mailgun API call: <pre>@call</pre>',
  ['@call' => print_r(['payload' => $payload], TRUE)]
);
```

## Common Mistakes
- **Wrong**: Editing `mailgun.settings.yml` to add `debug_mode: true` and committing it → **Right**: Use `settings.local.php` to set; never commit debug toggles.
- **Wrong**: Assuming "Mailgun says it sent" means delivered → **Right**: API success = queued. Mailgun's Logs page shows actual delivery, bounces, deferrals.
- **Wrong**: Generating a new API key without revoking the old one → **Right**: After confirming new key works, revoke old key in Mailgun dashboard. Compromised keys leak into git or logs.

## See Also
- [Verification & Testing](verification-testing.md)
- [Region Selection](region-selection.md)
- Reference: [Mailgun error codes](https://documentation.mailgun.com/docs/mailgun/api-reference/api-overview)
