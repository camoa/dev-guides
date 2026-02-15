---
description: The OWASP Top 10 (2021) vulnerabilities with attack scenarios, real-world impact, and prevention strategies for each.
---

# OWASP Top 10 (2021)

## When to Use

The OWASP Top 10 is the industry-standard baseline for web application security. Use this as your minimum security checklist — if your application is vulnerable to any Top 10 item, you have critical work to do.

## The Top 10 Vulnerabilities

| Rank | Vulnerability | Description | Severity | Prevalence |
|---|---|---|---|---|
| **A01** | **Broken Access Control** | Users access resources they shouldn't (unauthorized data, admin functions) | Critical | 3.81% of apps |
| **A02** | **Cryptographic Failures** | Sensitive data exposed due to weak/missing encryption | High | Common |
| **A03** | **Injection** | Untrusted data sent to interpreter (SQL, NoSQL, LDAP, OS commands, XSS) | Critical | Merged XSS |
| **A04** | **Insecure Design** | Missing or ineffective security controls in design phase | High | New 2021 |
| **A05** | **Security Misconfiguration** | Insecure defaults, verbose errors, unnecessary features enabled | Medium-High | 90% of apps |
| **A06** | **Vulnerable/Outdated Components** | Using libraries with known vulnerabilities | High | Very common |
| **A07** | **Identification/Authentication Failures** | Weak authentication, session management flaws | Critical | Common |
| **A08** | **Software/Data Integrity Failures** | Untrusted updates, insecure CI/CD, deserialization attacks | High | New 2021 |
| **A09** | **Security Logging/Monitoring Failures** | Insufficient logging, no alerting on attacks | Medium | Detection lag |
| **A10** | **Server-Side Request Forgery (SSRF)** | Attacker makes server fetch malicious URLs | Medium-High | Increasing |

## A01: Broken Access Control

**Attack scenario:** User changes `userId=123` in URL to `userId=124` and accesses another user's data.

**Real-world impact:** 2019 Capital One breach exposed 100M+ records due to misconfigured IAM permissions.

**Prevention:**

- Deny by default — require explicit grants
- Enforce access controls server-side on every request
- Disable directory listing
- Log access control failures, alert on repeated attempts
- Invalidate JWT tokens on server after logout
- Rate limit API access

## A02: Cryptographic Failures

**Attack scenario:** Application stores credit cards in plaintext database. SQL injection exposes all cards.

**Real-world impact:** 2013 Target breach — stolen credit card data due to inadequate encryption.

**Prevention:**

- Classify data (public, internal, confidential, restricted)
- Encrypt sensitive data at rest (AES-256) and in transit (TLS 1.3)
- Don't store sensitive data unnecessarily
- Use proper key management (rotate keys, hardware security modules)
- Disable caching for sensitive responses
- Use strong password hashing (Argon2id, bcrypt) — NEVER reversible encryption for passwords

## A03: Injection

**Attack scenario:** SQL injection — `SELECT * FROM users WHERE name = '` **admin' OR '1'='1** `'`

**Real-world impact:** 2025 BusinessOn breach — SQL injection leaked 179,386 user accounts, 200M won fine.

**Prevention:**

- Use parameterized queries / prepared statements (SQL)
- Use ORM frameworks correctly
- Validate input against allowlist patterns
- Escape special characters for interpreter context
- Limit database permissions (least privilege)

## A04: Insecure Design

**Attack scenario:** Password reset flow allows unlimited attempts with no rate limiting or CAPTCHA. Attacker brute-forces reset codes.

**Real-world impact:** Design flaws cost 100x more to fix in production than during design phase.

**Prevention:**

- Threat modeling during design (STRIDE)
- Security requirements in user stories
- Secure design patterns library
- Principle of least privilege in architecture
- Segregation of tenants (multi-tenant apps)
- Limit resource consumption per user/tenant

## A05: Security Misconfiguration

**Attack scenario:** Cloud storage bucket left publicly readable, exposing customer PII.

**Real-world impact:** 2019 Capital One — S3 bucket misconfiguration exposed 100M records.

**Prevention:**

- Repeatable hardening process (Infrastructure as Code)
- Minimal platform — remove unused features, frameworks
- Review/update configurations with patches
- Disable directory listing
- Segmented application architecture (containers, cloud security groups)
- Security headers (see [Security Headers](security-headers.md))
- Turn off detailed error messages in production

## A06: Vulnerable and Outdated Components

**Attack scenario:** Application uses Log4j 1.x. Attacker exploits Log4Shell (CVE-2021-44228) for remote code execution.

**Real-world impact:** 2025 Shai-Hulud worm — self-replicating malware spread through npm packages, compromised 25,000+ repos.

**Prevention:**

- Inventory all components (SBOM — Software Bill of Materials)
- Monitor for vulnerabilities (Dependabot, Snyk, OWASP Dependency-Check)
- Use components from official sources over secure links
- Prefer signed packages
- Monitor unmaintained libraries — plan migrations
- **7-day dependency cooldown** — wait 7 days before updating; would have prevented 8 of 10 major 2025 supply chain attacks

## A07: Identification and Authentication Failures

**Attack scenario:** Application allows unlimited login attempts. Attacker brute-forces common passwords.

**Prevention:**

- Implement multi-factor authentication (MFA)
- No default credentials (change admin/admin)
- Weak password checks (compare against compromised password lists)
- Limit failed login attempts, implement account lockout
- Use strong session ID generation
- Invalidate session IDs after logout, idle timeout
- Don't expose session IDs in URLs

## A08: Software and Data Integrity Failures

**Attack scenario:** Application auto-updates plugins from CDN without integrity checks. Attacker compromises CDN and injects malicious code.

**Real-world impact:** 2020 SolarWinds — build system compromised, malware distributed via trusted updates.

**Prevention:**

- Use digital signatures for software updates
- Verify integrity with checksums/hashes
- Review code/config changes
- Ensure CI/CD pipeline has proper segregation and access control
- Never deserialize untrusted data
- Use Subresource Integrity (SRI) for CDN resources: `<script src="..." integrity="sha384-..." crossorigin="anonymous">`

## A09: Security Logging and Monitoring Failures

**Attack scenario:** Attacker probes application for weeks. No alerts generated. Breach discovered 200+ days later via third-party notification.

**Real-world impact:** IBM 2025 report — average breach detection time: 204 days.

**Prevention:**

- Log authentication events (login, failed login, logout)
- Log access control failures
- Log input validation failures
- Use consistent log formats (JSON for parsing)
- Encrypt logs containing sensitive data
- Implement effective monitoring and alerting
- Establish incident response plan

## A10: Server-Side Request Forgery (SSRF)

**Attack scenario:** Application fetches user-supplied URL. Attacker provides `http://169.254.169.254/latest/meta-data/iam/security-credentials/` to steal cloud credentials.

**Real-world impact:** 2019 Capital One breach — SSRF combined with misconfigured IAM.

**Prevention:**

- Sanitize and validate all client-supplied URL data
- Enforce URL schema allowlist (http/https only, block file://, gopher://, etc.)
- Disable HTTP redirections
- Use allowlist for remote resource destinations
- Avoid sending raw responses to clients
- Network segmentation — isolate remote resource access functionality

## Common Mistakes

- **Treating OWASP Top 10 as complete security** — It's the MINIMUM baseline. Secure applications address dozens more vulnerability classes
- **"We'll fix security later"** — Retrofitting security is 100x more expensive than building it in. Capital One breach settlement: $190M
- **Compliance checkbox mentality** — PCI DSS compliance didn't prevent Target breach. Focus on actual risk reduction
- **Not tracking changes** — OWASP Top 10 evolves. A04 (Insecure Design) and A08 (Integrity Failures) are new in 2021. Subscribe to OWASP announcements

## See Also

- Previous: [Security Mindset Overview](security-mindset-overview.md) | Next: [Input Validation](input-validation.md)
- Reference: [OWASP Top 10:2021](https://owasp.org/Top10/2021/)
- Reference: [OWASP Top 10 Cheat Sheet](https://cheatsheetseries.owasp.org/IndexTopTen.html)
