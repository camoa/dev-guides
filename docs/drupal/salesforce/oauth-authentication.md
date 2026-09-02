---
description: "Salesforce OAuth 2.0 Web Server authentication setup — when to use OAuth vs JWT, Connected App configuration"
tldr: "Use OAuth when interactive user authorization is needed or for single-org integrations. Use JWT when server-to-server automation is required, no interactive auth is possible, or multiple orgs are involved."
drupal_version: "11.x"
---

# OAuth 2.0 Authentication

## When to Use

> Use OAuth when interactive user authorization is needed or for single-org integrations. Use JWT when server-to-server automation is required, no interactive auth is possible, or multiple orgs are involved.

**Purpose:** OAuth 2.0 Web Server authentication flow

## Decision: OAuth vs JWT

| Situation | Choose | Why |
|---|---|---|
| Interactive user must authorize the connection | OAuth | Requires browser redirect flow |
| Automated server-to-server integration | JWT | No interactive auth needed |
| Single Salesforce org | Either | Both work |
| Multiple Salesforce orgs | JWT | Simpler credential management |
| Scheduled background jobs | JWT | No token expiry interruption |

**Decision Point - OAuth vs JWT:**
- Use OAuth when: Interactive user authorization needed, single org integration
- Use JWT when: Server-to-server integration, automated processes, multiple orgs

## Setup Requirements

1. Create Connected App in Salesforce (Setup > Apps > App Manager)
2. Configure OAuth scopes (minimum: "Perform requests on your behalf at any time")
3. Set callback URL to `https://[your-site]/salesforce/oauth_callback`
4. SSL required for authorization

## Auth Provider Plugin

- Location: `/web/modules/contrib/salesforce/modules/salesforce_oauth/src/Plugin/SalesforceAuthProvider/SalesforceOAuthPlugin.php`
- Plugin ID: `oauth`
- Implements OAuth 2.0 Web Server Flow

## Configuration

- Consumer credentials (Consumer Key, Consumer Secret)
- Login URL (production vs sandbox)
- Callback URL: `/salesforce/oauth_callback`

## Common Mistakes

- **Wrong**: Using HTTP (non-SSL) for the callback URL → **Right**: OAuth requires SSL; use HTTPS
- **Wrong**: Reusing OAuth credentials across environments without configuring per-environment → **Right**: Auth credentials are not exported to config; configure each environment separately after config import

## See Also

- [JWT Authentication](jwt-authentication.md)
- [Configuration Management](configuration-management.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_oauth/src/Plugin/SalesforceAuthProvider/SalesforceOAuthPlugin.php`
- Salesforce docs: https://help.salesforce.com/articleView?id=connected_app_create.htm
