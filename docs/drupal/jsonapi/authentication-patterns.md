---
description: "Authentication is required for write operations (POST, PATCH, DELETE) and accessing restricted content."
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

**Description:** Token-based authentication with access/refresh tokens.

**Setup:**
```bash
# Install Simple OAuth module
composer require drupal/simple_oauth
drush en simple_oauth

# Generate keys (see module documentation)
```

**Token request:**
```bash
curl -X POST "https://example.com/oauth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=password&client_id={client_id}&client_secret={client_secret}&username={user}&password={pass}"
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9...",
  "token_type": "Bearer",
  "expires_in": 3600,
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
