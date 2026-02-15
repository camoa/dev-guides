---
description: Common security anti-patterns including security through obscurity, blacklist validation, client-side trust, weak passwords, plaintext storage, deprecated crypto, and no rate limiting.
---

# Common Security Anti-Patterns

## When to Use

Learn from others' mistakes. These anti-patterns represent the most common security failures that lead to breaches.

## Security Through Obscurity

**What it is:** Relying on secrecy of implementation details instead of strong security controls.

```python
# Bad: Hidden admin endpoint
@app.route('/super_secret_admin_panel_xyz123')
def admin():
    return render_template('admin.html')  # No authentication

# Good: Obscurity + real security
@app.route('/admin')
@require_authentication
@require_role('admin')
def admin():
    return render_template('admin.html')
```

**Real-world impact:** 2017 Equifax breach — attackers found admin portal via directory traversal, no auth required.

## Blacklist Input Validation

**What it is:** Trying to block known-bad inputs instead of allowing known-good inputs.

```python
# Bad: Blacklist dangerous characters
def sanitize_bad(user_input):
    dangerous = ['<script>', 'javascript:', 'onerror=']
    for pattern in dangerous:
        user_input = user_input.replace(pattern, '')
    return user_input
# Bypasses: <scr<script>ipt>, <ScRiPt>, %3Cscript%3E, <img src=x onerror=alert(1)>

# Good: Allowlist validation
def sanitize_good(user_input):
    if re.match(r'^[a-zA-Z0-9_-]{3,20}$', user_input):
        return user_input
    raise ValueError("Invalid input")
```

## Trusting Client-Side Validation

**What it is:** Relying on JavaScript validation as a security control.

```html
<!-- Bad: Client-side only -->
<script>
function validateForm() {
    const price = document.getElementById('price').value;
    if (price < 0 || price > 1000) { return false; }
    return true;
}
</script>
<!-- Attacker: curl -X POST -d "price=9999999" https://example.com/checkout -->
```

```python
# Good: Server-side validation (REQUIRED)
@app.route('/checkout', methods=['POST'])
def checkout():
    price = request.form.get('price', type=float)
    if price is None or price < 0 or price > 1000:
        return {"error": "Invalid price"}, 400
```

**Real-world impact:** 2019 British Airways breach — client-side payment validation bypassed, $230M GDPR fine.

## Insufficient Password Complexity

```python
# Bad: Weak requirements
def validate_password_bad(password):
    if len(password) >= 8:
        return True  # Allows: "password", "12345678", "qwerty123"

# Good: Strong requirements + compromised password check
def validate_password_good(password):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters")
    # Check against HaveIBeenPwned (k-anonymity API)
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    response = requests.get(f'https://api.pwnedpasswords.com/range/{prefix}')
    for line in response.text.split('\n'):
        if suffix in line:
            raise ValueError("Password compromised in a data breach")
    return True
```

**Real-world impact:** 81% of data breaches involve weak/stolen passwords (Verizon DBIR 2025).

## Not Encrypting Sensitive Data

```sql
-- Bad: Plaintext sensitive data
CREATE TABLE users (
    ssn VARCHAR(11),          -- Plaintext SSN
    credit_card VARCHAR(19)   -- Plaintext credit card
);

-- Good: Encrypted sensitive fields
CREATE TABLE users (
    ssn_encrypted TEXT,       -- AES-256-GCM encrypted
    -- Better: Don't store credit cards, use tokenization
);
```

**Real-world impact:** 2013 Target breach — 40M credit cards stolen, $18.5M settlement.

## Using Deprecated Crypto

```python
# Bad: MD5 for passwords (fast, no salt, rainbow tables exist)
password_hash = hashlib.md5(password.encode()).hexdigest()

# Bad: Weak key lengths
rsa_key = rsa.generate_private_key(key_size=1024)  # Broken

# Good: Modern algorithms
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)
rsa_key = rsa.generate_private_key(key_size=4096)
```

**Real-world impact:** 2012 LinkedIn breach — 6.5M SHA-1 hashed passwords cracked within days (no salt).

## Inadequate Session Management

```python
# Bad: Predictable session ID
session_id = str(user.id) + "_" + datetime.now().strftime("%Y%m%d")

# Good: Secure session management
session_id = secrets.token_hex(32)  # Cryptographically random
# Regenerate after login, expire sessions, invalidate on logout
```

## Verbose Error Messages

```python
# Bad: Detailed error in production
except Exception as e:
    return f"Database error: {str(e)}", 500
# Reveals: MySQL database, vulnerable to SQL injection

# Good: Generic error for users, detailed logs server-side
except Exception as e:
    logger.error(f"Database query failed: {e}")
    return {"error": "An error occurred. Please try again later."}, 500
```

## No Rate Limiting

```python
# Bad: No rate limiting on login
@app.route('/login', methods=['POST'])
def login():
    if authenticate(username, password):
        return redirect('/dashboard')
    return 'Invalid credentials', 401
# Attacker tries 10,000 passwords/second

# Good: Rate limiting
@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ... same logic ...
```

## Common Mistakes

- **Assuming users are non-technical** — Attackers are sophisticated
- **Copy-pasting code without understanding** — Stack Overflow answers may have security flaws
- **Not learning from breaches** — Every major breach has post-mortem analysis. Read them
- **Thinking "we're too small to be targeted"** — Automated scanners target EVERYONE
- **Security by compliance checkbox** — PCI DSS compliance doesn't prevent breaches

## See Also

- Previous: [Secure Development Lifecycle](secure-development-lifecycle.md) | Next: [Security Checklist](security-checklist.md)
- Reference: [OWASP Top 10 Proactive Controls](https://owasp.org/www-project-proactive-controls/)
