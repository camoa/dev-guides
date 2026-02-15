---
description: API security covering authentication (JWT, API keys), rate limiting, input validation, CORS, mass assignment prevention, and GraphQL security.
---

# API Security

## When to Use

Every API endpoint — REST, GraphQL, gRPC, webhooks — requires security controls. APIs are a prime attack vector: programmatic access, often less monitored than web UIs, frequently exposed to the internet.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| API authentication | **OAuth 2.0 + JWT** or API keys | Industry standard, stateless, scalable |
| Rate limiting | Token bucket or sliding window | Prevent abuse, DoS attacks |
| Input validation | JSON schema validation + type checking | Structured validation for API payloads |
| API authorization | Scopes (OAuth) or permission checks | Granular access control |
| API versioning | URL versioning (`/api/v1/`) | Clear deprecation path |
| Sensitive operations | Additional authentication step | Confirm high-risk actions |

## Authentication Strategies

**API Keys (simple, not recommended for user auth):**

```python
def generate_api_key():
    return secrets.token_urlsafe(32)

@app.route('/api/v1/data')
def get_data():
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return {"error": "Missing API key"}, 401
    user = db.execute("SELECT * FROM api_keys WHERE key_hash = ?",
                      [hashlib.sha256(api_key.encode()).hexdigest()]).fetchone()
    if not user or user['revoked']:
        return {"error": "Invalid API key"}, 401
    if is_rate_limited(api_key):
        return {"error": "Rate limit exceeded"}, 429
    return {"data": [...]}
```

**JWT (JSON Web Tokens):**

```python
import jwt

def create_jwt(user_id, scopes):
    payload = {
        'user_id': user_id,
        'scopes': scopes,
        'exp': datetime.utcnow() + timedelta(minutes=15),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def require_jwt(required_scope=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                if required_scope and required_scope not in payload.get('scopes', []):
                    return {"error": "Insufficient permissions"}, 403
                request.user_id = payload['user_id']
                return func(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return {"error": "Token expired"}, 401
            except jwt.InvalidTokenError:
                return {"error": "Invalid token"}, 401
        return wrapper
    return decorator
```

**JWT security best practices:**

- Short expiry (15 min for access tokens)
- Use refresh tokens for longevity (store server-side)
- Sign with HS256 (symmetric) or RS256 (asymmetric)
- Don't store sensitive data in JWT (it's base64, not encrypted)
- Validate `exp`, `iat`, `nbf` claims
- Use `aud` (audience) and `iss` (issuer) to prevent token reuse

## Rate Limiting

```python
import redis

redis_client = redis.Redis(host='localhost', port=6379)

def rate_limit_redis(key, max_requests=100, window=3600):
    now = time.time()
    redis_client.zremrangebyscore(key, 0, now - window)
    request_count = redis_client.zcard(key)
    if request_count >= max_requests:
        return False
    redis_client.zadd(key, {str(now): now})
    redis_client.expire(key, window)
    return True
```

## Input Validation for APIs

```python
from jsonschema import validate, ValidationError

article_schema = {
    "type": "object",
    "properties": {
        "title": {"type": "string", "minLength": 1, "maxLength": 200},
        "content": {"type": "string", "minLength": 1, "maxLength": 50000},
        "tags": {"type": "array", "items": {"type": "string"}, "maxItems": 10},
        "published": {"type": "boolean"}
    },
    "required": ["title", "content"],
    "additionalProperties": False
}

@app.route('/api/v1/articles', methods=['POST'])
def create_article():
    try:
        validate(instance=request.json, schema=article_schema)
    except ValidationError as e:
        return {"error": "Invalid input", "details": str(e)}, 400
```

## Mass Assignment Prevention

```python
# Bad: Mass assignment vulnerability
for key, value in request.json.items():
    setattr(user, key, value)  # Sets is_admin = True!

# Good: Explicit field allowlist
allowed_fields = {'email', 'name', 'bio'}
for key, value in request.json.items():
    if key in allowed_fields:
        setattr(user, key, value)
```

## CORS (Cross-Origin Resource Sharing)

```python
# Bad: Allow all origins
CORS(app, origins='*')

# Good: Specific origins only
CORS(app, origins=['https://yourapp.com', 'https://www.yourapp.com'])
```

## GraphQL Security

```python
# Depth limiting (prevent recursive queries)
def depth_limit_validator(max_depth):
    def validate(info):
        def measure_depth(node, current_depth=0):
            if current_depth > max_depth:
                raise GraphQLError(f'Query exceeds max depth of {max_depth}')
        measure_depth(info.field_nodes[0])
    return validate

# Disable introspection in production
def disable_introspection(info):
    if info.field_name in ['__schema', '__type'] and not is_development():
        raise GraphQLError('Introspection disabled')
```

## Common Mistakes

- **No rate limiting** — APIs get abused. Brute force, data scraping, DoS
- **Verbose error messages** — Don't expose database structure in errors. Return generic errors in production
- **No API versioning** — Breaking changes break all clients. Version APIs from day one
- **CORS misconfiguration** — `Access-Control-Allow-Origin: *` with credentials is dangerous
- **Mass assignment vulnerabilities** — Accepting all JSON fields allows privilege escalation
- **Exposing internal IDs** — Sequential IDs leak business metrics. Use UUIDs for public APIs
- **No authentication on "internal" APIs** — Internal APIs become external when containers get compromised
- **GraphQL N+1 queries** — Recursive nested queries cause DoS. Implement depth limiting and pagination
- **Not validating content-type** — Accept `application/json` only for JSON APIs

## See Also

- Previous: [Security Headers](security-headers.md) | Next: [File Upload Security](file-upload-security.md)
- Reference: [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- Reference: [OWASP API Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html)
