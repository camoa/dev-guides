---
description: Comprehensive pre-deployment security checklist covering authentication, input validation, XSS, CSRF, cryptography, API security, file uploads, dependencies, headers, logging, and compliance.
---

# Security Checklist

## When to Use

Use this checklist for security code reviews, deployment readiness assessments, and security audits. This is a quick reference distilling all sections into actionable items.

## Authentication and Authorization

- [ ] All endpoints require authentication (except explicitly public)
- [ ] Authorization checked on every request (not just once at login)
- [ ] Passwords hashed with Argon2id or bcrypt (work factor 12+)
- [ ] Multi-factor authentication (MFA) available
- [ ] Sessions expire after idle timeout (30 min) and absolute timeout (24 hr)
- [ ] Session IDs regenerated after login (prevent fixation)
- [ ] HTTPOnly, Secure, SameSite=Lax flags on session cookies
- [ ] Account lockout after 5 failed login attempts
- [ ] Rate limiting on login endpoint (5 attempts/minute)

## Input Validation and Output Encoding

- [ ] ALL user input validated server-side (allowlist, not blocklist)
- [ ] Type checking enforced (integers as integers, not strings)
- [ ] Length limits on all text inputs
- [ ] Context-specific output encoding (HTML, JS, SQL, URL)
- [ ] Template engine auto-escaping enabled
- [ ] No user input in SQL queries (parameterized queries only)
- [ ] No user input in OS commands (or properly escaped)
- [ ] File upload validation (magic bytes, not just MIME type)

## XSS Prevention

- [ ] Content Security Policy (CSP) configured
- [ ] CSP uses nonces or hashes for inline scripts (no 'unsafe-inline')
- [ ] All user-generated content escaped before display
- [ ] DOM manipulation uses textContent, not innerHTML
- [ ] No eval(), Function(), or setTimeout(string) with user data

## CSRF Protection

- [ ] CSRF tokens on all state-changing operations (POST/PUT/DELETE)
- [ ] SameSite=Lax or Strict on session cookies
- [ ] Origin/Referer validation on sensitive actions
- [ ] GET requests never modify state

## Cryptography

- [ ] AES-256-GCM for encryption at rest
- [ ] TLS 1.3 (or 1.2 minimum) for data in transit
- [ ] No hardcoded encryption keys (environment variables or KMS)
- [ ] Cryptographically secure random (secrets, os.urandom, not random)
- [ ] Argon2id/bcrypt for password hashing (never MD5/SHA-1)
- [ ] Key rotation plan in place

## API Security

- [ ] API authentication required (OAuth 2.0, JWT, or API keys)
- [ ] Rate limiting on all API endpoints
- [ ] Input validation with JSON schema
- [ ] API versioning implemented
- [ ] CORS configured with specific origins (not *)
- [ ] API errors don't expose stack traces or internal details

## File Upload Security

- [ ] File type validation (magic bytes + extension allowlist)
- [ ] Files stored outside web root
- [ ] Randomized filenames (UUIDs, not user-provided names)
- [ ] File size limits enforced (10MB max)
- [ ] Malware scanning on uploads (ClamAV)
- [ ] Files served with Content-Disposition: attachment

## Dependency Security

- [ ] Dependency vulnerability scanning (Dependabot, Snyk, npm audit)
- [ ] Lock files committed (package-lock.json, Pipfile.lock)
- [ ] No known vulnerabilities in dependencies
- [ ] Dependencies updated regularly (monthly)
- [ ] Unused dependencies removed
- [ ] 7-day cooldown for new package versions

## Security Headers

- [ ] Content-Security-Policy configured
- [ ] Strict-Transport-Security (HSTS) enabled
- [ ] X-Content-Type-Options: nosniff
- [ ] X-Frame-Options: DENY or SAMEORIGIN
- [ ] Referrer-Policy: strict-origin-when-cross-origin
- [ ] Permissions-Policy configured

## Logging and Monitoring

- [ ] Authentication events logged (login, logout, failures)
- [ ] Authorization failures logged
- [ ] Input validation failures logged
- [ ] No passwords or tokens in logs
- [ ] Structured logging (JSON format)
- [ ] Log retention policy (90+ days)
- [ ] Real-time alerting on suspicious activity
- [ ] Security logs sent to SIEM

## Sensitive Data Protection

- [ ] Sensitive data encrypted at rest (AES-256-GCM)
- [ ] HTTPS everywhere (no HTTP)
- [ ] No sensitive data in URLs (use POST, not GET)
- [ ] Payment data tokenized (not stored)
- [ ] PII minimized (only collect what's needed)
- [ ] Data retention policy enforced
- [ ] Backups encrypted

## Error Handling

- [ ] Generic error messages in production (no stack traces)
- [ ] Detailed errors logged server-side
- [ ] 404/403/500 errors don't leak information
- [ ] No database errors exposed to users

## Configuration

- [ ] Debug mode disabled in production
- [ ] Default credentials changed
- [ ] Directory listing disabled
- [ ] Unnecessary services disabled
- [ ] Security patches applied (OS, framework, dependencies)
- [ ] Secrets in environment variables or vault (not code)

## Infrastructure

- [ ] Database not accessible from internet
- [ ] Admin panels behind VPN or IP allowlist
- [ ] Principle of least privilege (IAM roles, file permissions)
- [ ] Network segmentation (DMZ, private subnets)
- [ ] Intrusion detection system (IDS) configured
- [ ] Regular backups (tested restore process)

## Security Testing

- [ ] SAST scan passed (CodeQL, Semgrep, Bandit)
- [ ] DAST scan passed (OWASP ZAP, Burp Suite)
- [ ] Dependency scan passed (npm audit, Snyk)
- [ ] Secret scanning passed (TruffleHog, git-secrets)
- [ ] Container scan passed (Trivy, Clair)
- [ ] Penetration testing completed (annually)
- [ ] Code review by security champion
- [ ] Threat model updated

## Compliance (if applicable)

- [ ] GDPR: Data processing agreements, consent mechanisms, right to deletion
- [ ] PCI DSS: Encryption, access control, logging, network segmentation
- [ ] HIPAA: Encryption, audit logs, access controls, BAA with vendors
- [ ] SOC 2: Security policies, access reviews, incident response plan

## See Also

- Previous: [Common Security Anti-Patterns](security-anti-patterns.md) | Next: [Code Reference Map](code-reference-map.md)
- Reference: [OWASP Application Security Verification Standard (ASVS)](https://owasp.org/www-project-application-security-verification-standard/)
