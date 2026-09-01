---
description: Security best practices for modern web development - tool-agnostic principles covering OWASP Top 10, authentication, cryptography, supply chain security, and secure SDLC.
tracks: []
guide-meta:
  concepts:
    - OWASP Top 10
    - XSS prevention
    - SQL injection prevention
    - CSRF prevention
    - authentication best practices
    - authorization
    - security headers
    - Content Security Policy
    - CSP
    - Trusted Types
    - cross-origin isolation
    - COOP
    - COEP
    - Fetch Metadata
    - Clear-Site-Data
    - browser security policies
    - API security
    - file upload security
    - cryptography basics
    - secure SDLC
  not:
    - Drupal-specific security APIs
    - Drupal access system
  requires: []
  complements:
    - development/solid-principles
    - development/tdd-spec-driven
  category: dev-practices
---

# Security Best Practices

Atomic decision guides for building secure web applications across all languages and frameworks.

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand the security mindset and defense principles | [Security Mindset Overview](security-mindset-overview.md) | Every developer must adopt a security-first mindset from day one. Security is not a feature you add later — it's a fundamental requirement woven into every design decision, code commit, and deployment. |
| Know the most critical web vulnerabilities | [OWASP Top 10](owasp-top-10.md) | The OWASP Top 10 is the industry-standard baseline for web application security. Use this as your minimum security checklist — if your application is vulnerable to any Top 10 item, you have critical work to do. |
| Validate user input safely | [Input Validation](input-validation.md) | Validate ALL input from untrusted sources: HTTP requests (parameters, headers, body), file uploads, API calls, database reads (yes, even database — consider SQL injection into another app), message queues, external APIs, environment… |
| Escape output correctly for different contexts | [Output Encoding and Escaping](output-encoding-escaping.md) | Escape ALL output that includes untrusted data before rendering in HTML, JavaScript, CSS, URLs, SQL queries, OS commands, or any interpreter context. Different contexts require different escaping rules. |
| Prevent cross-site scripting attacks | [Cross-Site Scripting (XSS)](cross-site-scripting-xss.md) | Understand XSS attack vectors whenever your application displays user-generated content, accepts URL parameters, or renders data from any untrusted source. |
| Implement XSS prevention patterns | [XSS Prevention Patterns](xss-prevention-patterns.md) | Implement these defense-in-depth XSS protections in addition to (not instead of) input validation and output encoding. |
| Prevent SQL injection | [SQL Injection Prevention](sql-injection-prevention.md) | EVERY database query that includes any untrusted data — user input, URL parameters, cookies, HTTP headers, data from external APIs, even data read from your own database (defense in depth). |
| Protect against CSRF attacks | [CSRF Prevention](csrf-prevention.md) | Protect ALL state-changing operations: POST/PUT/DELETE requests, password changes, money transfers, profile updates, admin actions. GET requests should NEVER change state (by design, GET = read-only). |
| Implement secure authentication | [Authentication Best Practices](authentication-best-practices.md) | Every system that identifies users needs secure authentication. This covers password-based authentication, multi-factor authentication, session management, and modern authentication protocols. |
| Design proper authorization systems | [Authorization and Access Control](authorization-access-control.md) | Every operation that accesses resources must check authorization — reading data, modifying data, deleting data, accessing admin features. Authentication answers "who are you?", authorization answers "what can you do?" |
| Protect sensitive data | [Sensitive Data Protection](sensitive-data-protection.md) | Protecting Personally Identifiable Information (PII), payment card data, health records, authentication credentials, business secrets, and any data that would cause harm if exposed. |
| Configure security headers | [Security Headers](security-headers.md) | Configure security headers on ALL HTTP responses. Headers provide defense-in-depth against XSS, clickjacking, MIME sniffing, and other attacks. |
| Deploy CSP enforcement workflow, Trusted Types, or cross-origin isolation | [Browser Security Policies](browser-security-policies.md) | Deploy CSP through three phases — report-only discovery (days to weeks, not hours), analyze violations filtering extension noise, then enforce only when violations near zero. Trusted Types blocks DOM-sink XSS at runtime but requires framework/widget support audit before enforcement — third-party widgets that write raw strings to innerHTML will throw. COEP requires every embedded subresource to serve Cross-Origin-Resource-Policy or the browser blocks it. |
| Secure my APIs | [API Security](api-security.md) | Every API endpoint — REST, GraphQL, gRPC, webhooks — requires security controls. APIs are a prime attack vector: programmatic access, often less monitored than web UIs, frequently exposed to the internet. |
| Handle file uploads safely | [File Upload Security](file-upload-security.md) | Any feature that accepts files from users — profile pictures, document uploads, file sharing, import features, email attachments. File uploads are extremely dangerous: remote code execution, stored XSS, DoS, malware distribution. |
| Manage dependencies securely | [Dependency Security](dependency-security.md) | Every project uses third-party dependencies — npm packages, PyPI libraries, Maven artifacts, gems, Go modules. **Supply chain attacks** are the fastest-growing threat in 2025. |
| Implement secure logging | [Logging and Monitoring](logging-monitoring.md) | Security logging and monitoring are MANDATORY for every application. **A09:2021 Security Logging and Monitoring Failures** — insufficient logging allows breaches to go undetected for months. |
| Understand cryptography basics | [Cryptography Basics](cryptography-basics.md) | Cryptography protects data confidentiality (encryption), integrity (hashing), and authenticity (signatures). Use for sensitive data at rest and in transit, password storage, message authentication, and digital signatures. |
| Integrate security into development | [Secure Development Lifecycle](secure-development-lifecycle.md) | Integrate security into every phase of software development — from requirements gathering to deployment and maintenance. Security is not a gate at the end; it's woven throughout the entire process. |
| Avoid common security mistakes | [Common Security Anti-Patterns](security-anti-patterns.md) | Learn from others' mistakes. These anti-patterns represent the most common security failures that lead to breaches. |
| Quick security checklist | [Security Checklist](security-checklist.md) | Use this checklist for security code reviews, deployment readiness assessments, and security audits. This is a quick reference distilling all sections into actionable items. |
| Find security resources and tools | [Code Reference Map](code-reference-map.md) |  |
| Find sources and maintenance info | [Sources and Maintenance Manifest](sources-maintenance-manifest.md) | Web sources, code sources, and version history for the security best practices guide. |
