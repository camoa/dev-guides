---
description: Security testing for authentication, authorization, injection, XSS, and a security test checklist
---

# Security Best Practices

## When to Use
Writing tests for any code that handles authentication, authorization, user input, sensitive data, or external integrations. Security must be tested, not assumed.

## Security Testing Principles

**Defense in Depth**: Test multiple layers of security controls
- Input validation at API boundary
- Business logic authorization checks
- Data layer access controls
- Each layer should be tested independently

**Assume Breach**: Write tests that verify what happens when security is bypassed
- What if attacker provides malicious input?
- What if token is expired/forged?
- What if user tampers with session data?

**Test the Unhappy Path**: Security bugs live in error cases
- Invalid input handling
- Edge cases and boundary conditions
- Race conditions in concurrent access

## Common Security Vulnerabilities to Test

**SQL Injection**
```python
# Code under test
def get_user_by_email(email):
    # VULNERABLE: String concatenation
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return db.execute(query)

# Test MUST catch this
def test_sql_injection_prevented():
    malicious_email = "'; DROP TABLE users; --"

    with pytest.raises(SecurityError):
        get_user_by_email(malicious_email)

# SECURE implementation
def get_user_by_email(email):
    # Use parameterized queries
    query = "SELECT * FROM users WHERE email = ?"
    return db.execute(query, [email])  # DB library escapes parameters
```

**Cross-Site Scripting (XSS)**
```javascript
// Code under test - rendering user input
function displayUsername(username) {
  document.getElementById('user').innerHTML = username;  // VULNERABLE
}

// Test MUST catch this
test('username escapes HTML to prevent XSS', () => {
  const maliciousUsername = '<script>alert("XSS")</script>';

  displayUsername(maliciousUsername);

  const element = document.getElementById('user');
  // Should render as text, not execute script
  expect(element.innerHTML).toBe('&lt;script&gt;alert("XSS")&lt;/script&gt;');
  expect(element.textContent).toBe('<script>alert("XSS")</script>');
});

// SECURE implementation
function displayUsername(username) {
  document.getElementById('user').textContent = username;  // Auto-escapes
  // Or use framework that auto-escapes: React, Vue, Angular
}
```

**Insecure Deserialization**
```python
# VULNERABLE: Deserializing untrusted data
import pickle

def load_session(session_data):
    return pickle.loads(session_data)  # Can execute arbitrary code!

# Test MUST catch this
def test_rejects_malicious_serialized_data():
    malicious_payload = b"c__builtin__\neval\n(S'__import__(\"os\").system(\"rm -rf /\")'\ntR."

    with pytest.raises(SecurityError):
        load_session(malicious_payload)

# SECURE: Use safe formats like JSON
import json

def load_session(session_data):
    return json.loads(session_data)  # Safe - can't execute code
```

**Broken Authentication**
```typescript
// Test authentication edge cases
describe('Authentication', () => {
  test('rejects expired tokens', async () => {
    const expiredToken = createToken({ userId: 1, exp: Date.now() - 3600 });

    await expect(authenticateRequest(expiredToken))
      .rejects.toThrow('Token expired');
  });

  test('rejects tampered tokens', async () => {
    const token = createToken({ userId: 1 });
    const tamperedToken = token.replace('userId:1', 'userId:999');

    await expect(authenticateRequest(tamperedToken))
      .rejects.toThrow('Invalid signature');
  });

  test('uses timing-safe password comparison', () => {
    const correctHash = bcrypt.hash('secret123');

    // Both should take approximately same time to prevent timing attacks
    const start1 = performance.now();
    const result1 = bcrypt.verify('wrong', correctHash);
    const time1 = performance.now() - start1;

    const start2 = performance.now();
    const result2 = bcrypt.verify('secret123', correctHash);
    const time2 = performance.now() - start2;

    expect(result1).toBe(false);
    expect(result2).toBe(true);
    // Time difference should be negligible (< 10ms)
    expect(Math.abs(time1 - time2)).toBeLessThan(10);
  });
});
```

**Authorization Bypass**
```python
# Test MUST verify authorization checks
def test_user_cannot_access_other_user_data():
    user1 = create_user(id=1)
    user2 = create_user(id=2)

    document = create_document(owner=user2)

    # User1 tries to access User2's document
    with pytest.raises(Forbidden):
        document_service.get_document(document.id, requesting_user=user1)

def test_admin_can_access_any_user_data():
    admin = create_user(id=1, role='admin')
    user = create_user(id=2, role='user')

    document = create_document(owner=user)

    # Admin should be able to access
    result = document_service.get_document(document.id, requesting_user=admin)
    assert result.id == document.id
```

## Security Test Checklist

**Input Validation**
- [ ] Test maximum input length enforcement
- [ ] Test special characters are handled safely
- [ ] Test null/empty input handling
- [ ] Test type validation (reject strings where numbers expected)
- [ ] Test Unicode/emoji handling doesn't break parsing

**Authentication**
- [ ] Test password complexity requirements
- [ ] Test password hashing uses bcrypt/argon2 (not MD5/SHA)
- [ ] Test failed login attempts are rate-limited
- [ ] Test tokens expire after specified time
- [ ] Test token signature verification prevents tampering

**Authorization**
- [ ] Test users can only access their own data
- [ ] Test role-based permissions are enforced
- [ ] Test privilege escalation is prevented
- [ ] Test session fixation is prevented

**Data Protection**
- [ ] Test sensitive data is encrypted at rest
- [ ] Test sensitive data is encrypted in transit (HTTPS)
- [ ] Test passwords/secrets never appear in logs
- [ ] Test PII is masked in error messages

**API Security**
- [ ] Test CSRF protection for state-changing requests
- [ ] Test API rate limiting prevents abuse
- [ ] Test API authentication required for protected endpoints
- [ ] Test CORS headers restrict allowed origins

## Common Mistakes

- Not testing security because "it works" - Security bugs don't cause obvious failures; must test explicitly
- Testing happy path only - Security vulnerabilities are in edge cases and error handling
- Hard-coding secrets in tests - Use environment variables or test-specific secrets
- Skipping authentication in tests - Makes tests easier but hides security bugs; test with real auth
- Not testing authorization - Tests pass but users can access data they shouldn't
- Assuming framework handles security - Frameworks help but aren't magic; test your usage is correct

## See Also
- Previous: [TDD Anti-Patterns](anti-patterns.md) | Next: [Performance Best Practices](performance-best-practices.md)
- Related: [Writing Effective Specifications](writing-specs.md) (security in acceptance criteria)
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- Reference: [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
