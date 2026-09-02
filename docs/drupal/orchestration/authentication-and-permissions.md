---
description: Orchestration permission model, Basic Auth setup, and service account configuration for production
tldr: "There is one permission: `use orchestration connect`. It gates all five API endpoints and the admin UI — no per-service granularity in 1.0.0. Use Basic Auth with a dedicated service account user. Always enforce HTTPS in production; Basic Auth credentials travel Base64-encoded in every request."
drupal_version: "11.x"
---

# Authentication and Permissions

## When to Use

> Read this when configuring the service account, assigning permissions, or hardening the integration for production.

## Permission Model

There is a single Drupal permission:

```yaml
# orchestration.permissions.yml
use orchestration connect:
  title: 'Use Orchestration'
```

This permission gates all five REST API endpoints and all admin UI pages under `/admin/config/workflow/orchestration/`. There is no per-service or per-provider permission granularity in 1.0.0.

**Implication**: any authenticated user with `use orchestration connect` can list all services, execute any of them, and register/unregister webhooks. Keep this permission on a tightly controlled dedicated role.

## Authentication Method

Core **Basic Auth** is the required dependency and the authentication method for all API calls. Session cookie auth is also accepted for admin UI browser requests (listed in routing YAML as `['basic_auth', 'cookie']`).

External platforms must use Basic Auth. Cookie-based auth requires a Drupal session which external platforms cannot maintain reliably across stateless API calls.

## Service Account Setup

```
1. Create a Drupal user: e.g., "orchestration-service"
2. Create a dedicated role: e.g., "Orchestration Client"
3. Assign permission "Use Orchestration" (use orchestration connect) to that role
4. Assign role to the service account user
5. Add only the additional Drupal permissions strictly required by the services
   being invoked (e.g., content access permissions for AI agents that query nodes)
```

## Transport Security

- **Always use HTTPS in production** — Basic Auth credentials travel Base64-encoded in every request header; HTTP exposes them to interception
- **TLS verification** — when Drupal dispatches outbound webhooks, the `Webhooks` service supports per-webhook `verify` flag (default `true`); never set `false` in production
- Consider IP allowlisting at the web server or CDN/WAF level to restrict which external IPs can reach `/orchestration/*` endpoints

## Common Mistakes

- **Assigning `use orchestration connect` to the global `authenticated` role** — any logged-in user can then enumerate services and execute them
- **Storing Basic Auth credentials in version control** (e.g., hardcoded in a Makefile or `.env` committed to git)
- **Not rotating service account credentials when team members leave or platform connectors are reconfigured**
- **Assuming session cookie auth is equivalent to Basic Auth for external platforms** — it is not; external clients cannot maintain Drupal session state

## See Also

- [Installation and Setup](installation-and-setup.md) → for the drush steps that activate `basic_auth`
- [Security Considerations](security-considerations.md) → for the broader security posture
- Reference: `orchestration.permissions.yml`, `orchestration.routing.yml`
