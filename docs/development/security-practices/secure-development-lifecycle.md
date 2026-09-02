---
description: Integrating security into every development phase - threat modeling (STRIDE), SAST, DAST, security code review, penetration testing, secure CI/CD, and secrets management.
tldr: "Integrate security into every phase of software development — from requirements gathering to deployment and maintenance. Security is not a gate at the end; it's woven throughout the entire development process."
---

# Secure Development Lifecycle

## When to Use

Integrate security into every phase of software development — from requirements gathering to deployment and maintenance. Security is not a gate at the end; it's woven throughout the entire development process.

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

**STRIDE framework for identifying threats:**

| Threat Type | Description | Example | Mitigation |
|---|---|---|---|
| **Spoofing** | Impersonating user/service | Attacker uses stolen credentials | MFA, certificate-based auth |
| **Tampering** | Modifying data/code | SQL injection, MITM attacks | Input validation, HTTPS, integrity checks |
| **Repudiation** | Denying actions | User claims "I didn't send that email" | Audit logs, digital signatures |
| **Information Disclosure** | Exposing sensitive data | SQL injection leaks customer data | Encryption, access control |
| **Denial of Service** | Making system unavailable | Resource exhaustion, DDoS | Rate limiting, auto-scaling |
| **Elevation of Privilege** | Gaining unauthorized permissions | Privilege escalation bugs | Least privilege, permission checks |

**Threat modeling process:**

```text
1. Diagram the system
   - Data flow diagrams (DFD)
   - Identify trust boundaries (user ↔ web server ↔ database)
   - Mark entry points and assets

2. Identify threats (STRIDE)
   - For each component and data flow
   - What could go wrong?
   - Use STRIDE as checklist

3. Rank threats by risk
   - Risk = Likelihood × Impact
   - DREAD scoring: Damage, Reproducibility, Exploitability, Affected users, Discoverability
   - Prioritize high-risk threats

4. Mitigate threats
   - Design controls to prevent/detect/respond
   - Document security decisions
   - Track residual risks

5. Validate mitigations
   - Security testing
   - Penetration testing
   - Bug bounty programs
```

## Static Application Security Testing (SAST)

**SAST tools scan source code for vulnerabilities:**

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
| C/C++ | Clang Static Analyzer, Coverity |
| Go | Gosec, StaticCheck |

**Integrate SAST into CI/CD:**

```bash
# Run Bandit (Python SAST) in CI pipeline
pip install bandit
bandit -r ./src -f json -o bandit-report.json

# Fail build if high-severity issues found
bandit -r ./src --severity-level high --exit-zero
if [ $? -ne 0 ]; then
    echo "High-severity security issues found!"
    exit 1
fi
```

## Dynamic Application Security Testing (DAST)

**DAST tools test running applications:**

```yaml
# OWASP ZAP scan in CI/CD
- name: ZAP Baseline Scan
  uses: zaproxy/action-baseline@v0.7.0
  with:
    target: 'https://staging.example.com'
    rules_file_name: '.zap/rules.tsv'
    cmd_options: '-a'  # Include all alerts
```

**DAST tools (2025-2026):**

- **OWASP ZAP:** Open-source, actively maintained
- **Burp Suite Enterprise:** Commercial, comprehensive
- **StackHawk:** API-first DAST
- **Acunetix:** Web vulnerability scanner
- **Nikto:** Web server scanner

**DAST vs SAST:**

- **SAST:** Analyzes source code, finds potential vulnerabilities early, many false positives
- **DAST:** Tests running app, finds runtime issues (config, deployment), fewer false positives but slower

## Security Code Review

**Checklist for peer code reviews:**

```markdown
Security Code Review Checklist:

[ ] Input Validation
    - All user input validated (allowlist, not blocklist)
    - Type checking enforced
    - Length limits applied

[ ] Output Encoding
    - Context-specific escaping (HTML, JS, SQL, URL)
    - Template engine auto-escaping enabled

[ ] Authentication/Authorization
    - Authentication required for sensitive endpoints
    - Authorization checked on every request
    - Session management secure (HTTPOnly, Secure, SameSite)

[ ] Cryptography
    - Strong algorithms (AES-256-GCM, Argon2id, SHA-256)
    - No hardcoded keys or secrets
    - Secure random number generation

[ ] Error Handling
    - No sensitive data in error messages
    - Generic errors for users, detailed logs server-side
    - Fail securely (deny by default)

[ ] Dependencies
    - No known vulnerabilities (npm audit, safety check)
    - Minimal dependencies
    - Versions locked in lock files

[ ] Logging
    - Security events logged (auth, authz, validation failures)
    - No sensitive data in logs (passwords, tokens, PII)
    - Structured logging (JSON)

[ ] API Security
    - Rate limiting implemented
    - CORS configured correctly
    - API authentication required
```

## Penetration Testing

**Types of penetration testing:**

| Type | Tester Knowledge | Use Case |
|---|---|---|
| **Black Box** | No knowledge of system | Simulates external attacker |
| **White Box** | Full knowledge (source code, architecture) | Comprehensive testing |
| **Gray Box** | Partial knowledge (API docs, user credentials) | Most common, balanced |

**Penetration testing phases:**

1. **Reconnaissance:** Gather information (public records, DNS, subdomain enumeration)
2. **Scanning:** Identify open ports, services, vulnerabilities
3. **Exploitation:** Attempt to exploit vulnerabilities
4. **Post-exploitation:** Pivot to other systems, escalate privileges
5. **Reporting:** Document findings, risk ratings, remediation steps

**When to perform pentests:**

- Before major releases
- After significant architecture changes
- Annually for mature products
- After security incidents

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

## Security Champions Program

**Embed security expertise in development teams:**

```text
Security Champions Program:
1. Identify 1-2 developers per team interested in security
2. Provide security training (OWASP Top 10, secure coding)
3. Champions attend security guild meetings
4. Champions review security-sensitive code
5. Champions evangelize security best practices
6. Rotate champions every 6-12 months
```

## Common Mistakes

- **Security as afterthought** — "We'll add security later" never works. Retrofitting security costs 100× more than building it in
- **No threat modeling** — Building without understanding threats = vulnerabilities by design
- **Ignoring SAST/DAST findings** — Tools generate noise but also find real issues. Triage, don't ignore
- **Security gates block releases** — Security should enable fast, safe releases. Integrate security into CI/CD, don't bolt it on at the end
- **No security training for developers** — Developers can't write secure code without training. Invest in OWASP Top 10, secure coding courses
- **Secrets in version control** — `.env` files, API keys committed to git. Use `.gitignore`, secret scanning (TruffleHog, git-secrets)
- **Not patching quickly** — Known vulnerabilities exploited within days. Automate dependency updates, patch critical issues within 48 hours
- **No bug bounty program** — External researchers find vulnerabilities. HackerOne, Bugcrowd platforms make it easy

## See Also

- Previous: [Cryptography Basics](cryptography-basics.md) | Next: [Common Security Anti-Patterns](security-anti-patterns.md)
- Reference: [OWASP Software Security Assurance Maturity Model (SAMM)](https://owaspsamm.org/)
- Reference: [Microsoft Security Development Lifecycle](https://www.microsoft.com/en-us/securityengineering/sdl)
