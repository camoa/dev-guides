---
description: Security risks and mitigations for the Orchestration module — credential exposure, overprivileged accounts, SSRF, and webhook delivery logging gaps
tldr: "Orchestration exposes an HTTP API that executes arbitrary Drupal logic. Enforce HTTPS (Basic Auth credentials are Base64 in every header), use a minimal-permission dedicated service account, enable only needed submodules, and never assign `use orchestration connect` to the authenticated role. Failed webhook deliveries are silently discarded in 1.0.0."
drupal_version: "11.x"
---

# Security Considerations

## When to Use

> Review this before deploying Orchestration in any environment beyond local development. The module's design — an open HTTP API executing arbitrary Drupal logic — requires deliberate hardening.

## Attack Surface

The Orchestration API exposes whatever your enabled providers expose. If `orchestration_ai_agents` is enabled and an AI Agent can query the database or send emails, then any authenticated caller of `/orchestration/service/execute` can do so as well. The attack surface scales with the number and capability of enabled providers.

## Key Risks and Mitigations

**Credential exposure (Basic Auth)**
- Risk: Basic Auth credentials travel Base64-encoded (not encrypted) in every HTTP request header
- Mitigation: **HTTPS only in production** — enforce at the web server or load balancer. Never allow HTTP for `/orchestration/*` endpoints.

**Overprivileged service account**
- Risk: A compromised credential gives the attacker access to all Orchestration-exposed capabilities
- Mitigation: Assign `use orchestration connect` to a dedicated role on a dedicated user. Grant only the additional Drupal permissions strictly needed by the services being invoked. Audit periodically.

**No per-service permission granularity**
- Risk: Any user with `use orchestration connect` can call any service — there is no service-level access control in 1.0.0
- Mitigation: Design your enabled providers' `execute()` implementations defensively. Validate input. If a service should only operate on content a user owns, enforce that in `execute()`.

**Webhook SSRF (Server-Side Request Forgery)**
- Risk: The webhook admin form accepts any URL. An admin with `use orchestration connect` could register a webhook pointing to an internal network address and trigger it via ECA, causing Drupal to make outbound requests to internal infrastructure
- Mitigation: Validate webhook URLs server-side against an allowlist of trusted external domains. Be aware that the service account (if it can register webhooks) can reach internal network resources. The `verify: true` default mitigates TLS-stripping on external URLs but does not prevent SSRF to internal HTTP endpoints.

**Webhook delivery not logged on failure**
- Risk: `Webhooks::dispatch()` silently discards `GuzzleException` and `\JsonException` (source has `// @todo Log this exception.`). Failed outbound webhook deliveries are invisible in Drupal logs
- Mitigation: Monitor delivery at the receiving platform. Until this is patched upstream, do not rely on Drupal-side webhook failure logs.

**Poll endpoint data leakage**
- Risk: The poll endpoint returns whatever ECA "Add item to poll result" actions have accumulated; if ECA models add sensitive data without checking content access, any caller with `use orchestration connect` can retrieve it
- Mitigation: In ECA models that add poll items, include condition checks that limit what data is added based on content access rules.

**TLS verification disabled on outbound webhooks**
- Risk: Setting `verify: false` on a webhook allows MITM attacks on outbound requests
- Mitigation: Never use `verify: false` in production. Use it only for local development with self-signed certificates.

## Production Checklist

- [ ] HTTPS enforced for all `/orchestration/*` endpoints
- [ ] Service account user has minimal permissions (only `use orchestration connect` plus what the services genuinely require)
- [ ] `use orchestration connect` not assigned to `authenticated` or `anonymous`
- [ ] Only the needed submodules are enabled (minimize exposed service surface)
- [ ] All registered webhook URLs use HTTPS with `verify: true`
- [ ] Service account credentials stored in a secrets manager, not in VCS or `.env` committed to git
- [ ] Consider IP allowlisting for `/orchestration/*` at CDN/WAF level
- [ ] Webhook delivery monitored at the receiving platform (Drupal-side failure logging not available in 1.0.0)

## Common Mistakes

- **Treating `use orchestration connect` as a low-stakes permission because the endpoint "just calls ECA"** — ECA can send emails, modify entities, call external APIs, and more
- **Disabling TLS verification for any webhook beyond local development**
- **Not auditing which ECA models subscribe to the Tool event after enabling `orchestration_eca`** — every Tool-subscribed model becomes callable via the Orchestration API

## See Also

- [Authentication and Permissions](authentication-and-permissions.md) → for the permission and service account setup
- [Webhooks and Outbound Events](webhooks-and-outbound-events.md) → for webhook configuration options
- OWASP API Security Top 10: https://owasp.org/API-Security/
- OWASP SSRF: https://owasp.org/www-community/attacks/Server_Side_Request_Forgery
