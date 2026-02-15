---
description: Protecting sensitive data with encryption at rest (AES-256-GCM), encryption in transit (TLS 1.3), key management, tokenization, and data minimization.
---

# Sensitive Data Protection

## When to Use

Protecting Personally Identifiable Information (PII), payment card data, health records, authentication credentials, business secrets, and any data that would cause harm if exposed.

## Data Classification

| Classification | Examples | Protection Required |
|---|---|---|
| **Public** | Marketing content, press releases | None - already public |
| **Internal** | Employee directory, org charts | Access control |
| **Confidential** | Customer data, business plans | Access control + encryption in transit |
| **Restricted** | PII, payment data, health records, credentials | Access control + encryption at rest + encryption in transit + audit logging |

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Encrypt data at rest | **AES-256-GCM** | Industry standard, authenticated encryption |
| Encrypt data in transit | **TLS 1.3** | Successor to SSL, faster than TLS 1.2 |
| Manage encryption keys | Key Management Service (KMS) | Separates keys from encrypted data |
| Hash sensitive data | SHA-256 (for integrity), Argon2 (for passwords) | One-way, can't reverse |
| Tokenize payment data | PCI-compliant tokenization service | Remove sensitive data from your systems |
| Store PII | Minimize collection, encrypt at rest, log access | Compliance (GDPR, CCPA, HIPAA) |

## Encryption at Rest

```python
from cryptography.fernet import Fernet

def encrypt_data(plaintext):
    key = load_key()
    f = Fernet(key)
    ciphertext = f.encrypt(plaintext.encode())
    return base64.b64encode(ciphertext).decode()

def decrypt_data(ciphertext):
    key = load_key()
    f = Fernet(key)
    ciphertext_bytes = base64.b64decode(ciphertext)
    plaintext = f.decrypt(ciphertext_bytes)
    return plaintext.decode()
```

**Field-level encryption (encrypt specific columns):**

```sql
-- Good: Encrypt sensitive fields
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50),
    email VARCHAR(255),
    ssn_encrypted TEXT,
    credit_card_encrypted TEXT,
    created_at TIMESTAMP
);
```

## Encryption in Transit

**TLS 1.3 configuration (Nginx):**

```nginx
server {
    listen 443 ssl http2;
    ssl_protocols TLSv1.3 TLSv1.2;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256';
    ssl_prefer_server_ciphers off;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
}
```

## Key Management

```python
# Bad: Hardcoded key in source code
ENCRYPTION_KEY = "supersecretkey123"  # NEVER DO THIS

# Good: Key from environment variable
ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY')

# Better: Key from dedicated key management service
import boto3
def get_encryption_key():
    kms_client = boto3.client('kms')
    response = kms_client.decrypt(
        CiphertextBlob=base64.b64decode(os.environ['ENCRYPTED_KEY'])
    )
    return response['Plaintext']
```

**Key rotation:**

```python
KEYS = {
    'v1': load_key_from_env('ENCRYPTION_KEY_V1'),
    'v2': load_key_from_env('ENCRYPTION_KEY_V2'),
}
CURRENT_KEY_VERSION = 'v2'

def encrypt_with_version(plaintext):
    key = KEYS[CURRENT_KEY_VERSION]
    ciphertext = encrypt(plaintext, key)
    return f"{CURRENT_KEY_VERSION}:{ciphertext}"

def decrypt_with_version(versioned_ciphertext):
    version, ciphertext = versioned_ciphertext.split(':', 1)
    key = KEYS[version]
    return decrypt(ciphertext, key)
```

## Tokenization

```python
# Payment card tokenization (use PCI-compliant service like Stripe)
import stripe

def process_payment(card_number, expiry, cvv):
    token = stripe.Token.create(card={
        "number": card_number,
        "exp_month": expiry['month'],
        "exp_year": expiry['year'],
        "cvc": cvv,
    })
    # Store token in your database (NOT the card number)
    db.execute("INSERT INTO payments (user_id, card_token) VALUES (?, ?)",
               [user_id, token.id])
    # Card number NEVER touches your server/database
```

## Data Minimization

```python
# Bad: Collect everything "just in case"
user_data = {
    'name': request.form['name'],
    'email': request.form['email'],
    'ssn': request.form['ssn'],
    'credit_card': request.form['credit_card'],
    # Why do we need all this for a newsletter signup?
}

# Good: Collect minimum required
user_data = {
    'email': request.form['email']  # Only need email for newsletter
}
```

**Data retention policies:**

```python
def delete_old_records():
    db.execute("DELETE FROM users WHERE email_verified = FALSE AND created_at < ?",
        [datetime.now() - timedelta(days=30)])
    db.execute("DELETE FROM audit_logs WHERE created_at < ?",
        [datetime.now() - timedelta(days=90)])
```

## Common Mistakes

- **A02:2021 Cryptographic Failures is #2 OWASP Top 10** — Sensitive data exposure is extremely common
- **Storing unnecessary sensitive data** — Don't collect SSN if you don't need it. Every field is a liability
- **Encryption key in same database as encrypted data** — Store keys separately (KMS, environment variables, HSM)
- **Using weak encryption** — AES-128-ECB, DES, RC4 are broken. Use AES-256-GCM
- **Not encrypting backups** — Encrypted production database but plaintext backups
- **Logging sensitive data** — Never log passwords, credit cards, SSNs
- **Sensitive data in URLs** — Use POST requests, not GET with sensitive query params
- **Not using HTTPS everywhere** — Even non-sensitive pages need HTTPS
- **Caching sensitive responses** — Set `Cache-Control: no-store, private` for PII/payment data

## See Also

- Previous: [Authorization and Access Control](authorization-access-control.md) | Next: [Security Headers](security-headers.md)
- Reference: [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- Reference: [OWASP A02:2021 Cryptographic Failures](https://owasp.org/Top10/2021/A02_2021-Cryptographic_Failures/)
