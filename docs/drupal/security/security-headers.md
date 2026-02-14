---
description: Configuring Content Security Policy, CORS, HSTS, and other HTTP security headers to prevent clickjacking, MIME sniffing, and XSS.
---

# Security Headers (CSP, CORS)

## When to Use
Configuring HTTP security headers to prevent clickjacking, MIME sniffing, XSS, and control cross-origin requests.

## Steps
1. **Content Security Policy (CSP) via contrib module**
   ```bash
   composer require drupal/csp
   drush en csp -y
   ```

   Configure at `/admin/config/system/csp`:
   ```
   default-src 'self';
   script-src 'self' https://cdn.example.com;
   style-src 'self' 'unsafe-inline';  # Avoid unsafe-inline if possible
   img-src 'self' data: https:;
   ```

2. **Security Kit (SecKit) module for comprehensive headers**
   ```bash
   composer require drupal/seckit
   drush en seckit -y
   ```

   Enables:
   - X-Frame-Options (clickjacking protection)
   - X-Content-Type-Options (MIME sniffing protection)
   - X-XSS-Protection (XSS filter)
   - Referrer-Policy
   - Feature-Policy/Permissions-Policy

3. **CORS configuration in services.yml**
   ```yaml
   # sites/default/services.yml
   cors.config:
     enabled: true
     allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
     allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
     allowedOrigins: ['https://trusted-domain.com']
     allowedOriginsPatterns: ['/^https?:\/\/(.+\.)?example\.com$/']
     exposedHeaders: ['Content-Length', 'X-Drupal-Cache']
     maxAge: 3600
     supportsCredentials: true
   ```

4. **Custom headers in .htaccess (Apache)**
   ```apache
   # Force HTTPS
   <IfModule mod_headers.c>
     Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
     Header always set X-Frame-Options "SAMEORIGIN"
     Header always set X-Content-Type-Options "nosniff"
     Header always set Referrer-Policy "strict-origin-when-cross-origin"
   </IfModule>
   ```

5. **CSP in code (if not using contrib)**
   ```php
   // In controller or middleware
   $response->headers->set('Content-Security-Policy',
     "default-src 'self'; script-src 'self' https://cdn.example.com"
   );
   ```

## Decision Points
| At this step... | If... | Then... |
|---|---|---|
| CSP implementation | Many inline scripts/styles | Use `csp` module with reporting, gradually tighten |
| CSP implementation | Clean codebase | Start strict: `default-src 'self'` |
| CORS | Frontend on different domain | Enable CORS, whitelist specific origins |
| CORS | Same-origin only | Leave CORS disabled (default) |
| Deployment | Production | Set HSTS with long max-age |
| Deployment | Development | Skip HSTS or use short max-age |

## Common Mistakes
- Using `'unsafe-inline'` in CSP -- Defeats XSS protection; use nonces or hashes
- Allowing all origins in CORS (`*`) -- CSRF vulnerability if credentials allowed
- Not testing CSP in report-only mode -- Broken site when enforced
- Setting HSTS on HTTP -- Header ignored; requires HTTPS
- Forgetting CSP for iframes -- Embedded content can bypass restrictions
- Not configuring CSP for aggregated JS/CSS -- Drupal's aggregation may break strict CSP

## See Also
- Reference: https://www.drupal.org/project/csp
- Reference: https://www.drupal.org/project/seckit
- Reference: https://www.drupal.org/node/2715637 (CORS documentation)
- Reference: https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
