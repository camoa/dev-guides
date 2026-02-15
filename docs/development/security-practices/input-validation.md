---
description: Input validation strategies including allowlist validation, type checking, length limits, and multi-layer validation patterns.
---

# Input Validation

## When to Use

Validate ALL input from untrusted sources: HTTP requests (parameters, headers, body), file uploads, API calls, database reads (yes, even database — consider SQL injection into another app), message queues, external APIs, environment variables.

## Decision

| If you need to... | Use... | Why |
|---|---|---|
| Accept known-good data | **Allowlist validation** | Safest — only accept explicitly permitted patterns |
| Reject known-bad data | Blocklist validation | Easily bypassed — attackers find new patterns |
| Validate data type | Type checking + range validation | Prevents type coercion attacks |
| Sanitize free-form text | Context-specific escaping | Different contexts (HTML, SQL, OS) need different escaping |

## Pattern

**Allowlist validation (PREFERRED):**

```python
# Good: Allowlist validation
import re

def validate_username(username):
    # Only alphanumeric + underscore, 3-20 chars
    if re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return username
    raise ValueError("Invalid username format")

# Bad: Blocklist validation
def validate_username_bad(username):
    # Try to block dangerous characters
    if any(char in username for char in ['<', '>', '"', "'"]):
        raise ValueError("Invalid characters")
    return username  # Still vulnerable to SQL injection, path traversal, etc.
```

**Type validation:**

```javascript
// Good: Strict type validation
function updateQuantity(productId, quantity) {
    const qty = parseInt(quantity, 10);
    if (isNaN(qty) || qty < 1 || qty > 1000) {
        throw new Error('Invalid quantity');
    }
    const id = parseInt(productId, 10);
    if (isNaN(id) || id < 1) {
        throw new Error('Invalid product ID');
    }
}

// Bad: Weak typing
function updateQuantity_bad(productId, quantity) {
    if (quantity > 0) {  // "999999999999999999999" > 0 is true
        // Vulnerable to type coercion attacks
    }
}
```

**Length validation:**

```php
// Good: Enforce length limits
function validateComment(string $comment): string {
    $comment = trim($comment);
    if (strlen($comment) < 1 || strlen($comment) > 2000) {
        throw new InvalidArgumentException('Comment must be 1-2000 characters');
    }
    return $comment;
}

// Bad: No length limits
// Attacker sends 10MB comment, causes DoS
```

## Validation Strategy

**Multi-layer validation:**

1. **Client-side** — UX convenience, NOT security (easily bypassed)
2. **API Gateway** — Rate limiting, basic format validation
3. **Application layer** — STRICT validation (the real security)
4. **Database layer** — Constraints as last resort (NOT NULL, CHECK constraints)

**Key validation rules:**

- Validate **before** using data, not after
- Reject invalid input — don't try to "fix" it
- Use type-safe languages' native type systems
- Validate length/range for all inputs
- Normalize data before validation (Unicode normalization, URL decoding)
- Validate redirects against allowlist

## Common Mistakes

- **Blocklist validation** — Incomplete and easily bypassed. Attackers find encoding variants (`<script>`, `%3Cscript%3E`, `<scr<script>ipt>`). Use allowlists
- **Trusting "internal" data sources** — Database data can be poisoned by SQL injection elsewhere. Validate on read. Message queues can receive malicious payloads
- **Validating after use** — Validate immediately when data enters your system, not just before database insert. Time-of-check/time-of-use vulnerabilities
- **Client-side validation only** — JavaScript validation improves UX but provides zero security. All validation MUST occur server-side
- **Type coercion attacks** — JavaScript `'0' == false` is true. PHP `'0e1234' == '0e5678'` is true (scientific notation). Use strict equality (`===`) and explicit type casting
- **Not validating file uploads** — File upload validation is complex (MIME spoofing, path traversal, malicious content)

## See Also

- Previous: [OWASP Top 10](owasp-top-10.md) | Next: [Output Encoding and Escaping](output-encoding-escaping.md)
- Reference: [OWASP Input Validation Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html)
