---
description: "Authentication is required for write operations (POST, PATCH, DELETE) and accessing restricted content."
tldr: "Authentication is required for write operations (POST, PATCH, DELETE) and accessing restricted content."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Authentication Patterns

### When to Use

Authentication is required for write operations (POST, PATCH, DELETE) and accessing restricted content.

### Decision

| Method | Best For | Security Level | Setup Complexity |
|--------|----------|----------------|------------------|
| HTTP Basic Auth | Development, internal tools | Low (credentials in header) | Low |
| Cookie-Based | Same-domain frontend | Medium (CSRF protected) | Medium |
| OAuth2 | Third-party integrations, mobile apps | High (token-based) | High |
| JWT | Stateless auth, microservices | High (signed tokens) | High |

### Items

#### HTTP Basic Authentication

**Description:** Simple username:password authentication via Authorization header.

**Setup:**
```bash
# Enable basic_auth module
drush en basic_auth

# Encode credentials
echo -n "username:password" | base64
# Output: dXNlcm5hbWU6cGFzc3dvcmQ=
```

**Usage Example:**
```bash
curl -X POST "https://example.com/jsonapi/node/article" \
  -H "Authorization: Basic dXNlcm5hbWU6cGFzc3dvcmQ=" \
  -H "Content-Type: application/vnd.api+json" \
  -d '{"data": {...}}'
```

**Gotchas:**
- Credentials sent with every request
- Only use over HTTPS in production
- User must have proper Drupal permissions
- No token expiration or refresh

#### Cookie-Based Authentication

**Description:** Traditional session-based auth using Drupal cookies.

**Login:**
```bash
curl -X POST "https://example.com/user/login?_format=json" \
  -H "Content-Type: application/json" \
  -c cookie.txt \
  -d '{"name":"username","pass":"password"}'
```

**Response includes:**
```json
{
  "current_user": {"uid": "1", "name": "admin"},
  "csrf_token": "...",
  "logout_token": "..."
}
```

**Use cookie in requests:**
```bash
curl -X GET "https://example.com/jsonapi/node/article" \
  -b cookie.txt
```

**Logout:**
```bash
curl -X POST "https://example.com/user/logout?_format=json&token={logout_token}" \
  -b cookie.txt
```

**Gotchas:**
- Requires same domain (or CORS with credentials)
- CSRF token needed for some operations
- Session timeout applies
- For cross-domain, set `cookie_samesite: None` in `services.yml`

#### OAuth2

**Description:** Token-based authentication with access/refresh tokens, via simple_oauth 6.1.1. It ships three grants: `client_credentials`, `authorization_code` and `refresh_token` (`modules/contrib/simple_oauth/src/Plugin/Oauth2Grant/`). An OAuth client is a Consumer entity from the required `consumers` module. For keys, scopes and consumer setup, see [MCP Server OAuth Setup](../mcp-server/oauth-setup.md).

**Setup:**
```bash
composer require drupal/simple_oauth
drush en simple_oauth
# Generate keys at /admin/config/people/simple_oauth
# Create scopes at /admin/config/people/simple_oauth/oauth2_scope/dynamic
# Create the client (Consumer) at /admin/config/services/consumer/add
```

| Client | Grant | Consumer settings |
|--------|-------|-------------------|
| Server, script, integration (machine-to-machine) | `client_credentials` | **Is Confidential?** on, a secret, and a default **User**; the token acts as that user |
| SPA, mobile or desktop app acting for a person | `authorization_code` with PKCE | Redirect URIs; untick **Is Confidential?** and leave the secret empty; tick **Use PKCE?**; add `refresh_token` to grant types for refresh |

**Token request: client_credentials (machine-to-machine):**
```bash
curl -X POST "https://example.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}&scope={scope_name}"
```

**Token request: authorization_code with PKCE (user-facing app):** send the user to `/oauth/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope_name}&state={state}&code_challenge={challenge}&code_challenge_method=S256`, then exchange the returned code:
```bash
curl -X POST "https://example.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}&code_verifier={verifier}"
```

**Legacy: password grant.** simple_oauth 6.x does not ship `grant_type=password`. It needs the separate `simple_oauth_password_grant` project. The OAuth 2.0 Security BCP (RFC 9700) says this grant MUST NOT be used, because the client handles the user's password. Use authorization_code with PKCE instead.

**Response (authorization_code; `client_credentials` returns no `refresh_token`, and `expires_in` is the consumer's access-token lifetime, 300 seconds by default):**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 300,
  "refresh_token": "..."
}
```

**Usage Example:**
```bash
curl -X GET "https://example.com/jsonapi/node/article" \
  -H "Authorization: Bearer {access_token}"
```

**Gotchas:**
- Requires Simple OAuth module
- Needs RSA key pair generation
- Tokens expire (use refresh tokens)
- Client ID/secret management required
- `client_id` must be in the POST body; the token controller reads it from there (`src/Controller/Oauth2Token.php`)
- `client_credentials` fails without a default user on the consumer, or when the consumer is not confidential or has no secret (`src/Repositories/ClientRepository.php`)
- `client_credentials` with no `scope` and no consumer default scopes returns `invalid_request`. Scopes are `oauth2_scope` names, and each scope must enable the grant type in use. The `invalid_request` check is in `src/Controller/Oauth2Token.php`; `src/Repositories/ScopeRepository.php` holds the name lookup and the grant-type check
- PKCE is required per consumer by **Use PKCE?**, and only for public (non-confidential) clients (`src/Plugin/Oauth2Grant/AuthorizationCode.php`)
- `authorization_code` returns a refresh token only when the consumer also enables the `refresh_token` grant (`src/Plugin/Oauth2Grant/AuthorizationCode.php`)

#### JWT (JSON Web Tokens)

**Description:** Stateless token-based authentication with signed tokens.

**Setup:**
```bash
# Install JWT module
composer require drupal/jwt
drush en jwt

# Configure secret key
```

**Usage Example:**
```bash
# Get JWT token (endpoint varies by configuration)
curl -X POST "https://example.com/jwt/token" \
  -d "username=user&password=pass"

# Use token
curl -X GET "https://example.com/jsonapi/node/article" \
  -H "Authorization: Bearer {jwt_token}"
```

**Gotchas:**
- Requires JWT contrib module
- Token signing key must be secure
- No built-in token revocation
- Token payload is visible (base64 encoded, not encrypted)

### Common Mistakes

**Using Basic Auth over HTTP:** Credentials are base64 encoded, not encrypted. WHY: Trivially decoded. Always use HTTPS in production.

**Not granting Drupal permissions:** Authentication proves identity, but permissions control access. WHY: User must have "Restful POST" permission and entity-specific permissions.

**Storing credentials in frontend code:** Hardcoded credentials are security vulnerabilities. WHY: Source code is often public or leakable. Use environment variables or secure storage.

**Forgetting to handle token expiration:** OAuth2 and JWT tokens expire. WHY: Security best practice. Implement token refresh logic.

**Using cookie auth cross-domain without CORS:** Browsers block cross-origin cookies by default. WHY: Security policy. Configure CORS properly and set `cookie_samesite: None`.

### See Also
- [Creating Resources (POST)](creating-resources.md)
- [Security Best Practices](security-best-practices.md)
- Drupal Simple OAuth module: https://www.drupal.org/project/simple_oauth
- Drupal JWT module: https://www.drupal.org/project/jwt
