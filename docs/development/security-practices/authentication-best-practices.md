---
description: Secure authentication covering password hashing (Argon2id, bcrypt), rate limiting, MFA, session management, and OAuth 2.0 with PKCE.
---

# Authentication Best Practices

## When to Use

Every system that identifies users needs secure authentication. This covers password-based authentication, multi-factor authentication, session management, and modern authentication protocols.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Hash passwords | **Argon2id** | 2025 gold standard - resists GPU/ASIC attacks |
| Hash passwords (legacy systems) | bcrypt (work factor 12+) | Industry standard, battle-tested |
| Prevent brute force | Rate limiting + account lockout | Slows automated attacks |
| Enhance security | Multi-factor authentication (MFA) | Passwords alone are insufficient |
| Enterprise authentication | OAuth 2.0 / OpenID Connect | Delegated authentication, single sign-on |
| API authentication | JWT with short expiry + refresh tokens | Stateless, scalable |

## Password Hashing

**Argon2id (recommended 2025+):**

```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher(
    time_cost=2,          # Iterations
    memory_cost=19456,    # 19 MiB (OWASP minimum)
    parallelism=1,        # Threads
    hash_len=32,
    salt_len=16
)

def register_user(username, password):
    password_hash = ph.hash(password)
    db.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)",
               [username, password_hash])

def authenticate_user(username, password):
    user = db.execute("SELECT * FROM users WHERE username = ?", [username]).fetchone()
    if not user:
        return False
    try:
        ph.verify(user['password_hash'], password)
        if ph.check_needs_rehash(user['password_hash']):
            new_hash = ph.hash(password)
            db.execute("UPDATE users SET password_hash = ? WHERE id = ?",
                      [new_hash, user['id']])
        return True
    except VerifyMismatchError:
        return False
```

**bcrypt (legacy systems):**

```php
$password_hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

if (password_verify($password, $user['password_hash'])) {
    if (password_needs_rehash($user['password_hash'], PASSWORD_BCRYPT, ['cost' => 12])) {
        $new_hash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);
    }
}
```

**NEVER use:**

- MD5, SHA-1, SHA-256 for passwords — too fast, no salt, vulnerable to rainbow tables
- Reversible encryption for passwords — passwords should be one-way hashes
- Custom hash algorithms — use vetted libraries

## Rate Limiting and Brute Force Prevention

```python
from flask_limiter import Limiter

limiter = Limiter(app=app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    if authenticate_user(username, password):
        return create_session(username)
    else:
        log_failed_login(username, request.remote_addr)
        failed_count = get_failed_login_count(username)
        if failed_count >= 5:
            lock_account(username, duration_minutes=30)
            return "Account temporarily locked", 429
        return "Invalid credentials", 401
```

**Account lockout strategies:**

- **Temporary lockout:** Lock for 30 minutes after 5 failed attempts
- **CAPTCHA:** Require CAPTCHA after 3 failed attempts
- **Progressive delays:** 1s, 2s, 4s, 8s delays between attempts
- **Alert user:** Email notification of failed login attempts

## Multi-Factor Authentication (MFA)

**MFA types (in order of security):**

1. **Hardware tokens** (YubiKey, Titan Security Key) — phishing-resistant
2. **TOTP apps** (Google Authenticator, Authy) — time-based codes
3. **SMS codes** — vulnerable to SIM swapping, but better than nothing
4. **Email codes** — weakest MFA, email accounts often insecure

**TOTP implementation:**

```python
import pyotp

def enable_mfa(user_id):
    secret = pyotp.random_base32()
    db.execute("UPDATE users SET mfa_secret = ? WHERE id = ?", [secret, user_id])
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=user['email'], issuer_name='YourApp')
    return qrcode.make(totp_uri)

def verify_mfa(user_id, code):
    user = db.execute("SELECT * FROM users WHERE id = ?", [user_id]).fetchone()
    totp = pyotp.TOTP(user['mfa_secret'])
    return totp.verify(code, valid_window=1)  # Allow 30s clock drift
```

## Session Management

```php
session_start([
    'cookie_httponly' => true,
    'cookie_secure' => true,
    'cookie_samesite' => 'Lax',
    'cookie_lifetime' => 3600,
    'gc_maxlifetime' => 3600,
    'use_strict_mode' => true,
]);
```

**Session security rules:**

- **Regenerate session ID after login:** Prevent session fixation
- **Expire sessions:** Idle timeout (30 min) and absolute timeout (24 hr)
- **Invalidate on logout:** Destroy session server-side
- **One session per user (optional):** Invalidate old sessions on new login

## OAuth 2.0 / OpenID Connect

**Use Authorization Code flow with PKCE** (Proof Key for Code Exchange). OAuth 2.0 Security Best Practices (RFC 9700 - Jan 2025):

- **Short-lived access tokens** (15 min) with refresh tokens
- **Bind tokens to client** (token binding, DPoP)
- Never use Implicit Grant or Resource Owner Password Credentials (ROPC) flow — deprecated in 2025

```javascript
const crypto = require('crypto');

function generatePKCE() {
    const verifier = base64URLEncode(crypto.randomBytes(32));
    const challenge = base64URLEncode(
        crypto.createHash('sha256').update(verifier).digest()
    );
    return { verifier, challenge };
}
```

## Common Mistakes

- **Storing passwords in plaintext** — NEVER. Always hash with Argon2id/bcrypt. Even in development
- **Using weak work factors** — bcrypt cost < 10 is too fast. Use 12+ (target 200-500ms hash time)
- **Predictable session IDs** — Use cryptographically secure random. NOT sequential IDs or MD5(username)
- **Not invalidating sessions on logout** — Client-side cookie deletion is insufficient. Destroy session server-side
- **Credentials in URLs** — `https://site.com/login?password=123` exposes passwords in logs, browser history, referer headers
- **No password complexity requirements** — Require minimum length (12+ chars). Check against compromised password lists
- **Weak account recovery** — Email-based password reset must use time-limited, single-use tokens. No security questions

## See Also

- Previous: [CSRF Prevention](csrf-prevention.md) | Next: [Authorization and Access Control](authorization-access-control.md)
- Reference: [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- Reference: [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- Reference: [OAuth 2.0 Security BCP RFC 9700](https://www.rfc-editor.org/rfc/rfc9700.html)
