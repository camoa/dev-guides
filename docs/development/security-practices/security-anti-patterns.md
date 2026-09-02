---
description: Common security anti-patterns including security through obscurity, blacklist validation, client-side trust, weak passwords, plaintext storage, deprecated crypto, and no rate limiting.
tldr: "Learn from others' mistakes. These anti-patterns represent the most common security failures that lead to breaches. Recognizing them helps you avoid repeating them."
---

# Common Security Anti-Patterns

## When to Use

Learn from others' mistakes. These anti-patterns represent the most common security failures that lead to breaches. Recognizing them helps you avoid repeating them.

## Security Through Obscurity

**What it is:** Relying on secrecy of implementation details instead of strong security controls.

**Why it fails:**

- Attackers reverse-engineer applications
- Source code leaks happen (GitHub, disgruntled employees)
- Obscurity delays attackers but doesn't stop them

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

**Why it fails:**

- Infinite ways to encode/obfuscate malicious input
- New attack vectors emerge constantly
- Blacklists are always incomplete

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

**Real-world impact:** Countless XSS and SQL injection bypasses of blacklist filters.

## Trusting Client-Side Validation

**What it is:** Relying on JavaScript validation as a security control.

**Why it fails:**

- Attackers control HTTP requests completely
- Browser developer tools disable JavaScript
- Direct API calls bypass client entirely

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

**What it is:** Weak password requirements that allow easily-guessable passwords.

**Why it fails:**

- "Password123" meets "8+ characters, 1 number, 1 uppercase" requirement
- Credential stuffing attacks use leaked password databases
- Brute force attacks test common patterns

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

**What it is:** Storing sensitive data (PII, credentials, payment info) in plaintext.

**Why it fails:**

- Database dumps expose everything
- Insider threats
- Backups often have weaker security

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

**Real-world impact:** 2013 Target breach — 40M credit cards stolen due to inadequate encryption, $18.5M settlement.

## Using Deprecated Crypto

**What it is:** MD5, SHA-1, DES, RC4, or weak key lengths for security purposes.

**Why it fails:**

- MD5/SHA-1 collision attacks are practical
- DES/RC4 broken, can be cracked in minutes
- Moore's Law — key lengths that were safe in 2010 aren't safe in 2025

```python
# Bad: MD5 for passwords
import hashlib
password_hash = hashlib.md5(password.encode()).hexdigest()
# MD5 is NOT slow (designed for speed)
# Rainbow tables exist for MD5 hashes
# No salt = same password = same hash

# Bad: Weak key lengths
rsa_key = rsa.generate_private_key(key_size=1024)  # Broken
aes_key = os.urandom(16)  # AES-128 is OK but use 256

# Good: Modern algorithms
from argon2 import PasswordHasher
ph = PasswordHasher()
password_hash = ph.hash(password)

rsa_key = rsa.generate_private_key(key_size=4096)
aes_key = os.urandom(32)  # AES-256
```

**Real-world impact:** 2012 LinkedIn breach — 6.5M SHA-1 hashed passwords cracked within days (no salt).

## Inadequate Session Management

**What it is:** Predictable session IDs, no expiration, session fixation vulnerabilities.

**Why it fails:**

- Predictable IDs allow session hijacking
- Long-lived sessions remain valid after logout
- Session fixation allows attacker to set victim's session ID

```python
# Bad: Predictable session ID
session_id = str(user.id) + "_" + datetime.now().strftime("%Y%m%d")
# Attacker guesses other users' session IDs

# Bad: No expiration
# Session valid forever, even after logout

# Bad: Session fixation
# Don't accept session ID from URL parameter
session_id = request.args.get('session_id')  # Attacker-controlled

# Good: Secure session management
import secrets
session_id = secrets.token_hex(32)  # Cryptographically random

# Regenerate after login (prevent fixation)
session.clear()
session['user_id'] = user.id
session['created_at'] = time.time()

# Expire sessions
if time.time() - session.get('created_at', 0) > 3600:  # 1 hour
    session.clear()
    return redirect('/login')

# Invalidate on logout
@app.route('/logout')
def logout():
    session.clear()  # Server-side destruction
    return redirect('/')
```

**Real-world impact:** Session hijacking is a top attack vector, enables account takeover.

## Verbose Error Messages

**What it is:** Exposing technical details in error messages (stack traces, SQL queries, file paths).

**Why it fails:**

- Reveals internal structure to attackers
- Leaks database schema, framework versions
- Guides attackers to vulnerabilities

```python
# Bad: Detailed error in production
try:
    db.execute(f"SELECT * FROM users WHERE id = {user_id}")
except Exception as e:
    return f"Database error: {str(e)}", 500

# Returns to user:
# "Database error: You have an error in your SQL syntax near 'abc' at line 1"
# Attacker learns: MySQL database, vulnerable to SQL injection

# Good: Generic error for users, detailed logs server-side
try:
    db.execute("SELECT * FROM users WHERE id = ?", [user_id])
except Exception as e:
    logger.error(f"Database query failed: {e}", extra={
        'user_id': user_id,
        'query': 'SELECT users by id'
    })
    return {"error": "An error occurred. Please try again later."}, 500
```

**Real-world impact:** Information disclosure helps attackers plan attacks, speeds up exploitation.

## No Rate Limiting

**What it is:** Allowing unlimited requests to sensitive endpoints.

**Why it fails:**

- Brute force attacks succeed (password guessing, API enumeration)
- DoS attacks overwhelm resources
- Data scraping is trivial

```python
# Bad: No rate limiting on login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if authenticate(username, password):
        return redirect('/dashboard')
    return 'Invalid credentials', 401

# Attacker tries 10,000 passwords/second

# Good: Rate limiting
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")  # Max 5 attempts per minute
def login():
    # ... same as above ...
```

**Real-world impact:** Credential stuffing attacks succeed due to lack of rate limiting.

## Common Mistakes

- **Assuming users are non-technical** — Attackers are sophisticated. Don't rely on "they won't figure it out"
- **Copy-pasting code without understanding** — Stack Overflow answers may have security flaws. Understand before using
- **Not learning from breaches** — Every major breach has post-mortem analysis. Read them, learn patterns
- **Thinking "we're too small to be targeted"** — Automated scanners target EVERYONE. Size doesn't matter
- **Security by compliance checkbox** — PCI DSS compliance doesn't prevent breaches (Target was compliant). Focus on actual security

## See Also

- Previous: [Secure Development Lifecycle](secure-development-lifecycle.md) | Next: [Security Checklist](security-checklist.md)
- Reference: [OWASP Top 10 Proactive Controls](https://owasp.org/www-project-proactive-controls/)
