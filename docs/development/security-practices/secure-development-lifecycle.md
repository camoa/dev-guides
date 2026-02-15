---
description: Integrating security into every development phase - threat modeling (STRIDE), SAST, DAST, security code review, penetration testing, secure CI/CD, and secrets management.
---

# Secure Development Lifecycle

## When to Use

Integrate security into every phase of software development — from requirements gathering to deployment and maintenance. Security is not a gate at the end; it's woven throughout the entire process.

## Decision

| Development Phase | Security Activity | Tools/Methods |
|---|---|---|
| **Requirements** | Threat modeling, security requirements | STRIDE, abuse cases |
| **Design** | Security architecture review, secure design patterns | Threat modeling, design review |
| **Development** | Secure coding, code review | SAST tools, peer review |
| **Testing** | Security testing, penetration testing | DAST tools, fuzzing |
| **Deployment** | Security configuration, secrets management | IaC scanning, vault |
| **Maintenance** | Vulnerability patching, security monitoring | Dependency scanning, SIEM |

## Threat Modeling (STRIDE)

| Threat Type | Description | Example | Mitigation |
|---|---|---|---|
| **Spoofing** | Impersonating user/service | Stolen credentials | MFA, certificate-based auth |
| **Tampering** | Modifying data/code | SQL injection, MITM | Input validation, HTTPS, integrity checks |
| **Repudiation** | Denying actions | "I didn't send that" | Audit logs, digital signatures |
| **Information Disclosure** | Exposing sensitive data | SQL injection leaks data | Encryption, access control |
| **Denial of Service** | Making system unavailable | Resource exhaustion | Rate limiting, auto-scaling |
| **Elevation of Privilege** | Gaining unauthorized access | Privilege escalation bugs | Least privilege, permission checks |

**Threat modeling process:**

```text
1. Diagram the system (DFD, trust boundaries, entry points)
2. Identify threats (STRIDE per component and data flow)
3. Rank by risk (Likelihood x Impact, DREAD scoring)
4. Mitigate (design controls, document decisions)
5. Validate (security testing, penetration testing)
```

## Static Application Security Testing (SAST)

```yaml
# GitHub Actions - CodeQL SAST
name: Security Scan
on: [push, pull_request]
jobs:
  codeql:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: github/codeql-action/init@v2
        with:
          languages: javascript, python
      - uses: github/codeql-action/analyze@v2
```

**SAST tools by language:**

| Language | Tools |
|---|---|
| JavaScript/TypeScript | ESLint security plugins, Semgrep, SonarQube |
| Python | Bandit, Semgrep, PyLint security |
| PHP | RIPS, Psalm, Phan |
| Java | SpotBugs, Checkmarx, SonarQube |
| Go | Gosec, StaticCheck |

## Dynamic Application Security Testing (DAST)

```yaml
# OWASP ZAP scan in CI/CD
- name: ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.7.0
  with:
    target: 'https://staging.example.com'
```

**DAST vs SAST:**

- **SAST:** Analyzes source code, finds potential vulnerabilities early, many false positives
- **DAST:** Tests running app, finds runtime issues, fewer false positives but slower

## Security Code Review Checklist

```text
[ ] Input Validation - allowlist, type checking, length limits
[ ] Output Encoding - context-specific escaping, auto-escaping enabled
[ ] Authentication/Authorization - checks on every request, secure sessions
[ ] Cryptography - strong algorithms, no hardcoded keys, secure random
[ ] Error Handling - no sensitive data in errors, fail securely
[ ] Dependencies - no known vulnerabilities, locked versions
[ ] Logging - security events logged, no sensitive data in logs
[ ] API Security - rate limiting, CORS configured, auth required
```

## Penetration Testing

| Type | Tester Knowledge | Use Case |
|---|---|---|
| **Black Box** | No knowledge of system | Simulates external attacker |
| **White Box** | Full knowledge (source code) | Comprehensive testing |
| **Gray Box** | Partial knowledge | Most common, balanced |

**When to perform:** Before major releases, after architecture changes, annually, after security incidents.

## Secure CI/CD Pipeline

```yaml
name: Secure Pipeline
on: [push, pull_request]
jobs:
  security-scan:
    steps:
      # 1. Secret scanning
      - uses: trufflesecurity/trufflehog@main
      # 2. Dependency scanning
      - run: npm audit --audit-level=high
      # 3. SAST
      - uses: github/codeql-action/analyze@v2
      # 4. Container scanning
      - uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:latest'
          severity: 'CRITICAL,HIGH'
      # 5. IaC scanning
      - uses: aquasecurity/tfsec-action@v1.0.0
      # 6. DAST (on staging)
      - uses: zaproxy/action-baseline@v0.7.0
```

## Secrets Management

```bash
# Bad: Secrets in code
API_KEY = "sk_live_abc123"  # NEVER

# Good: Secrets in vault (HashiCorp Vault, AWS Secrets Manager)
import hvac
client = hvac.Client(url='http://127.0.0.1:8200', token=os.environ['VAULT_TOKEN'])
db_password = client.secrets.kv.v2.read_secret_version(path='database')['data']['data']['password']
```

## Common Mistakes

- **Security as afterthought** — "We'll add security later" never works. Retrofitting costs 100x more
- **No threat modeling** — Building without understanding threats = vulnerabilities by design
- **Ignoring SAST/DAST findings** — Triage, don't ignore
- **Security gates block releases** — Integrate security into CI/CD, don't bolt it on at the end
- **No security training** — Developers can't write secure code without training
- **Secrets in version control** — Use `.gitignore`, secret scanning (TruffleHog, git-secrets)
- **Not patching quickly** — Patch critical issues within 48 hours
- **No bug bounty program** — External researchers find vulnerabilities. Use HackerOne/Bugcrowd

## See Also

- Previous: [Cryptography Basics](cryptography-basics.md) | Next: [Common Security Anti-Patterns](security-anti-patterns.md)
- Reference: [OWASP SAMM](https://owaspsamm.org/)
- Reference: [Microsoft Security Development Lifecycle](https://www.microsoft.com/en-us/securityengineering/sdl)
