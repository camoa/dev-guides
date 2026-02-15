---
description: Cryptography fundamentals including AES-256-GCM encryption, RSA asymmetric encryption, Argon2id password hashing, HMAC, secure random generation, and key rotation.
---

# Cryptography Basics

## When to Use

Cryptography protects data confidentiality (encryption), integrity (hashing), and authenticity (signatures). Use for sensitive data at rest and in transit, password storage, message authentication, and digital signatures.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Encrypt data (two-way) | **AES-256-GCM** | Industry standard authenticated encryption |
| Hash data (one-way) | **SHA-256** for integrity, **Argon2id** for passwords | Collision-resistant |
| Hash passwords | **Argon2id** (best) or bcrypt | Slow, salted, memory-hard |
| Generate random values | **Cryptographically secure RNG** (crypto.randomBytes, secrets) | Unpredictable |
| Digital signatures | RSA-4096 or Ed25519 | Verify authenticity |
| Key derivation | PBKDF2, Argon2, scrypt | Derive keys from passwords |

## Hashing vs. Encryption

**Hashing (one-way):**

```python
import hashlib
data = "sensitive data"
hash_value = hashlib.sha256(data.encode()).hexdigest()
# Same input = same hash (deterministic)
# Can verify integrity but can't recover original data
```

**Encryption (two-way):**

```python
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
ciphertext = cipher.encrypt(b"sensitive data")
recovered = cipher.decrypt(ciphertext)  # b"sensitive data"
```

## Symmetric Encryption (AES)

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

def encrypt_aes_gcm(plaintext, key):
    nonce = os.urandom(12)  # 96 bits for GCM
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    return nonce + ciphertext + encryptor.tag

def decrypt_aes_gcm(encrypted_data, key):
    nonce = encrypted_data[:12]
    tag = encrypted_data[-16:]
    ciphertext = encrypted_data[12:-16]
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag))
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()

key = os.urandom(32)  # 256-bit key
encrypted = encrypt_aes_gcm(b"Secret message", key)
decrypted = decrypt_aes_gcm(encrypted, key)
```

**Why AES-256-GCM:**

- **AES-256:** Industry standard, NIST approved, fast
- **GCM mode:** Authenticated encryption (detects tampering)
- **Alternatives:** ChaCha20-Poly1305 (better for mobile)

## Asymmetric Encryption (RSA)

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096)
public_key = private_key.public_key()

def encrypt_rsa(plaintext, public_key):
    return public_key.encrypt(plaintext, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))

def decrypt_rsa(ciphertext, private_key):
    return private_key.decrypt(ciphertext, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))
```

**Use RSA for:** Encrypting symmetric keys (hybrid encryption), digital signatures, SSL/TLS certificates.
**Don't use RSA for:** Encrypting large data (slow, size limits).

## Password Hashing

```python
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2, memory_cost=102400, parallelism=8, hash_len=32, salt_len=16)

password_hash = ph.hash("user_password")
# $argon2id$v=19$m=102400,t=2,p=8$...

try:
    ph.verify(password_hash, "user_password")
    if ph.check_needs_rehash(password_hash):
        new_hash = ph.hash("user_password")
except VerifyMismatchError:
    print("Password incorrect")
```

**Requirements:** Random per-user salt, intentionally slow, memory-hard (resists GPU/ASIC).

## Hashing for Integrity

```python
import hashlib
import hmac

# SHA-256 for file integrity
def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

# HMAC for message authentication
def create_hmac(message, secret_key):
    return hmac.new(secret_key, message, hashlib.sha256).hexdigest()

def verify_hmac(message, signature, secret_key):
    expected = create_hmac(message, secret_key)
    return hmac.compare_digest(expected, signature)
```

## Random Number Generation

```python
import secrets

# Good: Cryptographically secure random
session_id = secrets.token_hex(32)
api_key = secrets.token_urlsafe(32)
random_bytes = os.urandom(16)

# Bad: NOT cryptographically secure
import random
session_id = random.randint(1000000, 9999999)  # NEVER for security!
```

## Key Derivation

```python
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def derive_key(password, salt=None):
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32,
        salt=salt, iterations=600000)
    key = kdf.derive(password.encode())
    return key, salt
```

## Key Rotation

```python
class KeyManager:
    def __init__(self):
        self.keys = {
            'v1': load_key_from_env('ENCRYPTION_KEY_V1'),
            'v2': load_key_from_env('ENCRYPTION_KEY_V2'),
        }
        self.current_version = 'v2'

    def encrypt(self, plaintext):
        key = self.keys[self.current_version]
        ciphertext = encrypt_aes_gcm(plaintext, key)
        return f"{self.current_version}:".encode() + ciphertext

    def decrypt(self, encrypted_data):
        version, ciphertext = encrypted_data.split(b':', 1)
        key = self.keys[version.decode()]
        return decrypt_aes_gcm(ciphertext, key)
```

## Common Mistakes

- **Using MD5 or SHA-1** — Broken, collision attacks exist. Use SHA-256+ or SHA-3
- **ECB mode for encryption** — AES-ECB leaks patterns. Use GCM or CBC
- **Not using authenticated encryption** — CBC without HMAC allows padding oracle attacks. Use GCM
- **Hardcoded keys** — Keys in source code get committed to git. Use environment variables or KMS
- **Weak random for security** — `random.random()`, `Math.random()` are predictable. Use `secrets`, `os.urandom()`
- **Encrypting passwords** — Passwords should be hashed (one-way), not encrypted (reversible)
- **Rolling your own crypto** — Don't implement cryptographic algorithms. Use vetted libraries
- **Insufficient key length** — AES-128 acceptable, use AES-256 for future-proofing. RSA < 2048 is broken
- **No key rotation** — Compromised key compromises all data. Rotate quarterly
- **Storing plaintext keys with encrypted data** — Store keys separately (KMS, HSM)

## See Also

- Previous: [Logging and Monitoring](logging-monitoring.md) | Next: [Secure Development Lifecycle](secure-development-lifecycle.md)
- Reference: [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- Reference: [Cryptography library (Python)](https://cryptography.io/)
