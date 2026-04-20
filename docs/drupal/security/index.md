---
description: Drupal security architecture, access control, XSS/CSRF/SQL injection prevention, authentication, and OWASP best practices.
guide-meta:
  concepts:
    - Drupal access system
    - permissions and roles
    - route access checks
    - AccessResult
    - entity access control
    - node grants
    - XSS prevention
    - Twig autoescape
    - CSRF protection
    - SQL injection prevention
    - trusted callbacks
    - security headers
  not:
    - tool-agnostic security theory
    - Klaro consent management
  requires: []
  complements:
    - drupal/routing
    - drupal/forms
    - drupal/twig
  specializes: development/security-practices
  category: drupal
---

# Drupal Security

## I need to...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand Drupal's security layers | [Security Overview](security-overview.md) | Understanding Drupal's defense-in-depth security model when architecting applications, evaluating modules, or responding to security advisories. |
| Map OWASP Top 10 to Drupal | [OWASP Top 10 in Drupal](owasp-top-10-in-drupal.md) | When evaluating Drupal applications against industry-standard security risks or conducting security audits. |
| Implement access control on routes | [Access System Architecture](access-system-architecture.md) | When designing routes, controllers, or entities that require access control -- understanding the architecture prevents security gaps. |
| Define permissions and roles | [Permissions and Roles](permissions-and-roles.md) | Defining what actions users can perform and grouping those permissions into roles. |
| Add access checks to routes | [Route Access Checks](route-access-checks.md) | Protecting routes (URLs) from unauthorized access before the controller executes. |
| Return access results correctly | [AccessResult Patterns](accessresult-patterns.md) | Returning access decisions from custom access checks, entity access handlers, or any code that determines access. |
| Control entity access | [Entity Access Control](entity-access-control.md) | Controlling access to entity operations (view, update, delete, create) through entity access handlers. |
| Implement node grants | [Content Access (Node Grants)](content-access-node-grants.md) | When entity access handlers are insufficient -- node grants enable database-level access filtering for complex content access rules (e.g., organic groups, taxonomy access, workflow states). |
| Prevent XSS attacks | [XSS Prevention](xss-prevention.md) | Whenever displaying user-generated content or building HTML output -- XSS (Cross-Site Scripting) is one of the most common web vulnerabilities. |
| Use Twig safely | [Twig Autoescape and Safe Markup](twig-autoescape-and-safe-markup.md) | Understanding Twig's automatic XSS protection when building themes or rendering output. |
| Prevent SQL injection | [SQL Injection Prevention](sql-injection-prevention.md) | Every database query -- SQL injection allows attackers to manipulate queries and access/modify unauthorized data. |
| Protect against CSRF | [CSRF Protection](csrf-protection.md) | Protecting state-changing operations (create, update, delete) from Cross-Site Request Forgery attacks where malicious sites trick users into performing unwanted actions. |
| Validate and sanitize input | [Input Validation and Sanitization](input-validation-and-sanitization.md) | Every point where user input enters the system -- validation ensures data integrity; sanitization prevents injection attacks. |
| Configure authentication | [Authentication System](authentication-system.md) | Understanding how Drupal identifies users and when to implement custom authentication providers (OAuth, SAML, LDAP, API keys). |
| Manage sessions securely | [Session Management](session-management.md) | Understanding session security to prevent session fixation, hijacking, and ensure proper session lifecycle. |
| Use trusted callbacks | [Trusted Callbacks](trusted-callbacks.md) | When using callbacks in render arrays (`#pre_render`, `#post_render`, `#lazy_builder`) -- Drupal requires explicit trust declaration to prevent arbitrary code execution. |
| Set security headers | [Security Headers (CSP, CORS)](security-headers.md) | Configuring HTTP security headers to prevent clickjacking, MIME sniffing, XSS, and control cross-origin requests. |
| Secure file uploads | [File Upload Security](file-upload-security.md) | Whenever users can upload files -- unrestricted file upload is one of the most dangerous vulnerabilities (remote code execution). |
| Follow security best practices | [Best Practices and Patterns](best-practices-and-patterns.md) | When establishing security standards for a project or conducting code reviews. |
| Avoid common mistakes | [Anti-Patterns and Common Mistakes](anti-patterns-and-common-mistakes.md) | During code review or when debugging security issues -- recognize dangerous patterns to avoid them. |
| Find security code references | [Code Reference Map](code-reference-map.md) |  |
