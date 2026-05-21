---
description: Security risks and mitigations for the Orchestration module — credential exposure, overprivileged accounts, SSRF, and webhook delivery logging gaps
tldr: "Orchestration exposes an HTTP API that executes arbitrary Drupal logic. Enforce HTTPS (Basic Auth credentials are Base64 in every header), use a minimal-permission dedicated service account, enable only needed submodules, and never assign `use orchestration connect` to the authenticated role. Failed webhook deliveries are silently discarded in 1.0.0."
drupal_version: "11.x"
---

# Security Considerations

## When to Use

> Review this before deploying Orchestration in any environment beyond local development. The module's design — an open HTTP API executing arbitrary Drupal logic — requires deliberate hardening.

## Decision

The attack surface scales with the number and capability of enabled providers. If `orchestration_ai_agents` is enabled and an agent can query the database or send emails, then any authenticated caller of `/orchestration/service/execute` can do so as well.

| Risk | Mitigation |
|---|---|
| Credential exposure via Basic Auth | HTTPS only in production — enforce at web server or load balancer |
| Overprivileged service account | Dedicated role + user; grant only permissions strictly needed |
| No per-service permission granularity | Design `execute()` implementations defensively; validate input; enforce content ownership checks inside `execute()` |
| Webhook SSRF | Validate webhook URLs against an allowlist; be aware that the service account can reach internal network resources if it can register webhooks |
| Failed webhook delivery not logged | Monitor at the receiving platform; Drupal-side failure logging not available in 1.0.0 |
| Poll endpoint data leakage | Include content access condition checks in ECA models that add poll items |
| TLS verification disabled on outbound webhooks | Never `verify: false` in production |

## Pattern

**Production checklist:**

- [ ] HTTPS enforced for all `/orchestration/*` endpoints
- [ ] Service account user has minimal permissions (`use orchestration connect` + only what the services genuinely require)
- [ ] `use orchestration connect` NOT assigned to `authenticated` or `anonymous`
- [ ] Only the needed submodules are enabled (minimize exposed service surface)
- [ ] All registered webhook URLs use HTTPS with `verify: true`
- [ ] Service account credentials stored in a secrets manager, not in VCS or `.env` committed to git
- [ ] Consider IP allowlisting for `/orchestration/*` at CDN/WAF level
- [ ] Webhook delivery monitored at the receiving platform (Drupal-side failure logging not available in 1.0.0)

## Common Mistakes

- **Wrong**: Treating `use orchestration connect` as a low-stakes permission → **Right**: ECA can send emails, modify entities, call external APIs, and more — the permission is high-privilege
- **Wrong**: Disabling TLS verification for any webhook beyond local development → **Right**: `verify: false` is acceptable only for self-signed certs in local dev
- **Wrong**: Not auditing which ECA models subscribe to the Tool event after enabling `orchestration_eca` → **Right**: Every Tool-subscribed model becomes callable via the Orchestration API; audit periodically

## See Also

- [Authentication and Permissions](authentication-and-permissions.md)
- [Webhooks and Outbound Events](webhooks-and-outbound-events.md)
- Reference: OWASP API Security Top 10 — https://owasp.org/API-Security/
- Reference: OWASP SSRF — https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
