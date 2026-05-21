---
description: Orchestration permission model, Basic Auth setup, and service account configuration for production
tldr: "There is one permission: `use orchestration connect`. It gates all five API endpoints and the admin UI — no per-service granularity in 1.0.0. Use Basic Auth with a dedicated service account user. Always enforce HTTPS in production; Basic Auth credentials travel Base64-encoded in every request."
drupal_version: "11.x"
---

# Authentication and Permissions

## When to Use

> Read this when configuring the service account, assigning permissions, or hardening the integration for production.

## Decision

| Question | Answer |
|---|---|
| How many Drupal permissions does Orchestration define? | One: `use orchestration connect` |
| What does that permission gate? | All five REST endpoints + all admin UI pages under `/admin/config/workflow/orchestration/` |
| Is there per-service permission granularity? | No — any user with the permission can list all services and execute any of them |
| Which auth methods are accepted? | `basic_auth` (required for external platforms) or `cookie` session (browser admin UI) |

## Pattern

**Service account setup:**

```
1. Create a Drupal user: e.g., "orchestration-service"
2. Create a dedicated role: e.g., "Orchestration Client"
3. Assign permission "use orchestration connect" to that role
4. Assign role to the service account user
5. Add only the additional permissions strictly required by the services being invoked
```

**Permission definition:**

```yaml
# orchestration.permissions.yml
use orchestration connect:
  title: 'Use Orchestration'
```

**Transport security checklist:**

- HTTPS only in production — Basic Auth credentials are Base64-encoded in every request header
- Per-webhook `verify` flag defaults to `true` — never set `false` in production
- Consider IP allowlisting at the web server or CDN/WAF level for `/orchestration/*` endpoints

## Common Mistakes

- **Wrong**: Assigning `use orchestration connect` to the `authenticated` role → **Right**: Any logged-in user could then enumerate services and execute them
- **Wrong**: Storing Basic Auth credentials in version control → **Right**: Use a secrets manager; never commit to git
- **Wrong**: Not rotating credentials when team members leave or platform connectors are reconfigured → **Right**: Treat the service account like any privileged credential
- **Wrong**: Using session cookie auth for external platforms → **Right**: External clients cannot maintain Drupal session state; use Basic Auth

## See Also

- [Installation and Setup](installation-and-setup.md)
- [Security Considerations](security-considerations.md)
- Reference: `orchestration.permissions.yml`, `orchestration.routing.yml`
