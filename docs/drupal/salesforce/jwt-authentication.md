---
description: Salesforce JWT Bearer Token authentication setup — standard vs GovCloud plugin, RSA key configuration
drupal_version: "11.x"
---

# JWT Bearer Token Authentication

## When to Use

> Use JWT when you need server-to-server authentication without interactive authorization. Use the GovCloud plugin only for Salesforce Government Cloud instances.

## Decision

| Situation | Choose | Why |
|---|---|---|
| Standard Salesforce instance | `SalesforceJWTPlugin` | Works for all non-gov instances |
| Government Cloud instance | `SalesforceJWTGovCloudPlugin` | Required for gov cloud auth endpoint |
| Interactive authorization acceptable | Consider OAuth | JWT requires RSA key infrastructure |
| Automated/background process | JWT | No user interaction needed |

## Pattern

**Required setup:**
1. Generate RSA key pair (private key stays on server, public key uploaded to Salesforce)
2. Upload public key to Salesforce Connected App
3. Configure plugin with: Consumer Key, Login URL, encryption key (RSA private key), Salesforce username

**Plugin locations:**
- Standard: `/web/modules/contrib/salesforce/modules/salesforce_jwt/src/Plugin/SalesforceAuthProvider/SalesforceJWTPlugin.php`
- GovCloud: `/web/modules/contrib/salesforce/modules/salesforce_jwt/src/Plugin/SalesforceAuthProvider/SalesforceJWTGovCloudPlugin.php`

## Common Mistakes

- **Wrong**: Using the standard JWT plugin with a GovCloud instance → **Right**: Use `SalesforceJWTGovCloudPlugin` for government cloud instances
- **Wrong**: Storing the RSA private key in version control → **Right**: Store the private key securely (environment variable, secrets manager, or Drupal key module)

## See Also

- [OAuth Authentication](oauth-authentication.md)
- [Configuration Management](configuration-management.md)
- Reference: `/web/modules/contrib/salesforce/modules/salesforce_jwt/src/Plugin/SalesforceAuthProvider/SalesforceJWTPlugin.php`
