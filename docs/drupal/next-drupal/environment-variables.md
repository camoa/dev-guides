---
description: "Configure Next.js connection to Drupal, authentication credentials, and feature flags using environment variables."
drupal_version: "11.x"
topic: "drupal/next-drupal"
---

## Environment Variables

### When to Use

Configure Next.js connection to Drupal, authentication credentials, and feature flags using environment variables.

### Items

#### NEXT_PUBLIC_DRUPAL_BASE_URL

**Description:** Base URL of your Drupal site. Public prefix makes it available client-side.

**Required:** Yes

**Example:**

```bash
NEXT_PUBLIC_DRUPAL_BASE_URL=https://drupal.example.com
```

**Gotchas:**
- Must be accessible from browser (for next/image)
- Use HTTPS in production
- No trailing slash

#### NEXT_IMAGE_DOMAIN

**Description:** Domain for Next.js image optimization allowlist.

**Required:** Yes (if using next/image)

**Example:**

```bash
NEXT_IMAGE_DOMAIN=drupal.example.com
```

**Gotchas:**
- Must match Drupal domain exactly
- No protocol, no trailing slash
- Add to next.config.js images.domains

#### DRUPAL_CLIENT_ID

**Description:** OAuth client ID for authenticated requests.

**Required:** If using OAuth authentication

**Example:**

```bash
DRUPAL_CLIENT_ID=a53b1d17-6b23-478d-8649-9aee63974c80
```

**Gotchas:**
- Server-side only (no NEXT_PUBLIC_ prefix)
- Generate UUID in Drupal OAuth consumer

#### DRUPAL_CLIENT_SECRET

**Description:** OAuth client secret for authenticated requests.

**Required:** If using OAuth authentication

**Example:**

```bash
DRUPAL_CLIENT_SECRET=3#9h$2DU#8qKb6&
```

**Gotchas:**
- Server-side only, never commit to version control
- Generate secure random string

#### DRUPAL_REVALIDATE_SECRET

**Description:** Secret for on-demand revalidation endpoint security.

**Required:** If using on-demand revalidation

**Example:**

```bash
DRUPAL_REVALIDATE_SECRET=U2Y5bbkKJ08Ua8F
```

**Gotchas:**
- Different from preview secret
- Server-side only
- Validate in revalidate API route

#### DRUPAL_PREVIEW_SECRET

**Description:** Secret for draft/preview mode security.

**Required:** If using draft mode

**Example:**

```bash
DRUPAL_PREVIEW_SECRET=kJ84Ua9F2bY5b8K
```

**Gotchas:**
- Different from revalidate secret
- Configured in Drupal Next.js site settings
- Validated by enableDraftMode helper

#### DRUPAL_USERNAME / DRUPAL_PASSWORD

**Description:** Basic auth credentials (development only).

**Required:** If using Basic auth

**Example:**

```bash
DRUPAL_USERNAME=admin
DRUPAL_PASSWORD=password
```

**Gotchas:**
- Never use in production
- Requires basic_auth Drupal module

#### DRUPAL_SITE_ID

**Description:** Site machine name for multi-site filtering.

**Required:** If using multi-site setup

**Example:**

```bash
DRUPAL_SITE_ID=marketing_site
```

**Gotchas:**
- Must match entity reference field value
- Used in filter parameters

#### DRUPAL_FRONT_PAGE

**Description:** Custom front page path (alternative to /home).

**Required:** No

**Example:**

```bash
DRUPAL_FRONT_PAGE=/front
```

**Gotchas:**
- Configured in NextDrupal client
- Resolves to / in Next.js

### Common Mistakes

- **Using NEXT_PUBLIC_ prefix for secrets** — Client-side exposure. WHY: Anything with NEXT_PUBLIC_ is bundled into client JavaScript.
- **Committing .env.local to git** — Credentials leak. WHY: Add to .gitignore.
- **Same secret for preview and revalidation** — Security issue. WHY: Different access levels, different purposes.
- **Missing trailing slash handling** — URL construction errors. WHY: Ensure base URL has no trailing slash.

### See Also

- Security Best Practices
- Authentication Patterns
- NextDrupal Client Configuration
