---
description: "Salesforce JWT Bearer Token authentication setup — standard vs GovCloud plugin, RSA key configuration"
tldr: "Use JWT when you need server-to-server authentication without interactive authorization. Use the GovCloud plugin only for Salesforce Government Cloud instances."
drupal_version: "11.x"
---

# JWT Bearer Token Authentication

## When to Use

> Use JWT when you need server-to-server authentication without interactive authorization. Use the GovCloud plugin only for Salesforce Government Cloud instances.

**Purpose:** JWT Bearer Token Flow for server-to-server authentication

## Decision: Standard vs GovCloud

| Situation | Choose | Why |
|---|---|---|
| Standard Salesforce instance | `SalesforceJWTPlugin` | Works for all non-gov instances |
| Government Cloud instance | `SalesforceJWTGovCloudPlugin` | Required for gov cloud auth endpoint |
| Interactive authorization acceptable | Consider OAuth | JWT requires RSA key infrastructure |
| Automated/background process | JWT | No user interaction needed |

**Decision Point - Standard vs GovCloud:**
- Use GovCloud plugin for government cloud instances
- Use standard plugin for all other instances

## Technical Requirements

- RSA key pair generation
- Public key uploaded to Salesforce Connected App
- No interactive authorization needed

Order of operations: generate the RSA key pair (the private key stays on the server), upload the public key to the Salesforce Connected App, then configure the plugin.

## Auth Provider Plugins

- Standard: `/web/modules/contrib/salesforce/modules/salesforce_jwt/src/Plugin/SalesforceAuthProvider/SalesforceJWTPlugin.php`
- GovCloud: `/web/modules/contrib/salesforce/modules/salesforce_jwt/src/Plugin/SalesforceAuthProvider/SalesforceJWTGovCloudPlugin.php`

## Configuration

- Consumer Key
- Login URL
- Encryption key (RSA private key)
- Salesforce username

## Common Mistakes

- **Wrong**: Using the standard JWT plugin with a GovCloud instance → **Right**: Use `SalesforceJWTGovCloudPlugin` for government cloud instances
- **Wrong**: Storing the RSA private key in version control → **Right**: Store the private key securely (environment variable, secrets manager, or Drupal key module)

## See Also

- [OAuth Authentication](oauth-authentication.md)
- [Configuration Management](configuration-management.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_jwt/src/Plugin/SalesforceAuthProvider/SalesforceJWTPlugin.php`
