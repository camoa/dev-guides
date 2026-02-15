---
description: Security tools and libraries mapped by category and language - SAST, DAST, dependency scanning, security libraries, OWASP resources, online scanners, and learning resources.
---

# Code Reference Map

## When to Use

Maps security topics to specific tools, libraries, and resources for each major programming language/framework.

## Static Application Security Testing (SAST)

| Language | Tools | Notes |
|---|---|---|
| **JavaScript/TypeScript** | ESLint (eslint-plugin-security), Semgrep, SonarQube, CodeQL | ESLint plugins catch common issues |
| **Python** | Bandit, Semgrep, Pylint, CodeQL | Bandit specifically for security |
| **PHP** | RIPS, Psalm, Phan, SonarQube | RIPS commercial, Psalm open-source |
| **Java** | SpotBugs, FindSecBugs, Checkmarx, SonarQube | FindSecBugs extends SpotBugs |
| **C/C++** | Clang Static Analyzer, Coverity, Cppcheck | Clang free, Coverity commercial |
| **Go** | Gosec, StaticCheck, Semgrep | Gosec designed for security |
| **Ruby** | Brakeman, RuboCop | Brakeman for Rails apps |
| **C#/.NET** | Roslyn Analyzers, SonarQube, Checkmarx | Roslyn built into Visual Studio |

## Dynamic Application Security Testing (DAST)

| Tool | Type | Best For |
|---|---|---|
| **OWASP ZAP** | Open-source | General web app scanning |
| **Burp Suite** | Commercial (free edition limited) | Manual pentesting + automation |
| **StackHawk** | Commercial | API-first scanning, CI/CD integration |
| **Acunetix** | Commercial | Comprehensive web vulnerability scanner |
| **Nikto** | Open-source | Web server scanning |
| **w3af** | Open-source | Web application attack framework |

## Dependency Scanning

| Ecosystem | Tools |
|---|---|
| **npm (JavaScript)** | npm audit, Snyk, Dependabot, Socket |
| **PyPI (Python)** | Safety, pip-audit, Snyk, Dependabot |
| **Maven (Java)** | OWASP Dependency-Check, Snyk |
| **RubyGems (Ruby)** | Bundler-audit, Dependabot |
| **Go modules** | Nancy, Snyk, Dependabot |
| **NuGet (.NET)** | dotnet list package --vulnerable, Snyk |
| **Composer (PHP)** | Roave Security Advisories, Snyk |

## Security Libraries by Language

### JavaScript/Node.js

```javascript
import Joi from 'joi';              // Schema validation
import DOMPurify from 'dompurify';  // HTML sanitization
import crypto from 'crypto';        // Built-in crypto
import bcrypt from 'bcrypt';        // Password hashing
import passport from 'passport';    // Authentication middleware
import helmet from 'helmet';        // Security headers
import rateLimit from 'express-rate-limit';  // Rate limiting
```

### Python

```python
import jsonschema        # JSON schema validation
import bleach            # HTML sanitization
from cryptography.fernet import Fernet  # Encryption
from argon2 import PasswordHasher       # Password hashing
import secrets           # Secure random (built-in)
from flask_limiter import Limiter       # Rate limiting
from flask_talisman import Talisman    # Security headers
```

### PHP

```php
filter_var($input, FILTER_VALIDATE_EMAIL);  // Built-in filters
htmlspecialchars($output, ENT_QUOTES, 'UTF-8');  // Built-in escaping
password_hash($password, PASSWORD_ARGON2ID);  // Built-in hashing
random_bytes(32);  // Secure random (built-in)
use PDO;  // Parameterized queries
```

### Java

```java
import javax.validation.constraints.*;  // Bean validation
import org.owasp.encoder.Encode;        // OWASP encoder
import javax.crypto.Cipher;             // Built-in crypto
import org.mindrot.jbcrypt.BCrypt;      // Password hashing
import org.springframework.security.*;  // Spring Security
```

## OWASP Resources

| Resource | URL | Description |
|---|---|---|
| **OWASP Top 10** | https://owasp.org/Top10/ | Top 10 web app vulnerabilities |
| **OWASP Cheat Sheet Series** | https://cheatsheetseries.owasp.org/ | Quick reference guides |
| **OWASP ASVS** | https://owasp.org/www-project-application-security-verification-standard/ | Security verification standard |
| **OWASP Testing Guide** | https://owasp.org/www-project-web-security-testing-guide/ | Comprehensive testing methodology |
| **OWASP API Security Top 10** | https://owasp.org/www-project-api-security/ | API-specific vulnerabilities |
| **OWASP Dependency-Check** | https://owasp.org/www-project-dependency-check/ | Dependency vulnerability scanner |
| **OWASP ZAP** | https://www.zaproxy.org/ | Web app security scanner |

## Online Security Scanners

| Tool | URL | Purpose |
|---|---|---|
| **Security Headers** | https://securityheaders.com | Check HTTP security headers |
| **Mozilla Observatory** | https://observatory.mozilla.org | Security and privacy scan |
| **SSL Labs** | https://www.ssllabs.com/ssltest/ | TLS/SSL configuration test |
| **HaveIBeenPwned** | https://haveibeenpwned.com | Check if email/password compromised |
| **CSP Evaluator** | https://csp-evaluator.withgoogle.com | Validate Content Security Policy |

## Security Standards and Frameworks

| Standard | Description | URL |
|---|---|---|
| **CWE Top 25** | Most dangerous software weaknesses | https://cwe.mitre.org/top25/ |
| **NIST Cybersecurity Framework** | Risk management framework | https://www.nist.gov/cyberframework |
| **SANS Top 25** | Most dangerous software errors | https://www.sans.org/top25-software-errors/ |
| **PCI DSS** | Payment card security standard | https://www.pcisecuritystandards.org/ |
| **GDPR** | EU data protection regulation | https://gdpr.eu/ |

## Learning Resources

| Resource | Type | URL |
|---|---|---|
| **PortSwigger Web Security Academy** | Free training | https://portswigger.net/web-security |
| **OWASP WebGoat** | Deliberately insecure app | https://owasp.org/www-project-webgoat/ |
| **Hack The Box** | Penetration testing practice | https://www.hackthebox.com/ |
| **CTF challenges** | Capture The Flag competitions | https://ctftime.org/ |

## See Also

- Previous: [Security Checklist](security-checklist.md) | Next: [Sources and Maintenance Manifest](sources-maintenance-manifest.md)
- Reference: [OWASP Projects](https://owasp.org/projects/)
