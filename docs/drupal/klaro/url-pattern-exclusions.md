---
description: Disable Klaro on admin pages, previews, or specific URL patterns using regex
drupal_version: "11.x"
---

# URL Pattern Exclusions

## When to Use

> Disable Klaro on specific URL patterns where consent management isn't needed (admin pages, previews) or interferes with functionality.

## Decision

| If you need to exclude... | Pattern... | Why |
|---|---|---|
| All admin pages | `\\/admin\\/` | Consent not needed for logged-in admins |
| CKEditor media previews | `\\/media\\/.*\\/preview` | Klaro breaks preview rendering |
| Specific text format previews | `\\/media\\/full_html\\/preview` | Target only problematic formats |
| User profile pages | `\\/user\\/\\d+` | Exclude authenticated user areas |
| Custom admin routes | `\\/custom-admin\\/.*` | App-specific admin sections |

## Pattern

**Admin Exclusion** (`/admin/config/user-interface/klaro` → Advanced):

```yaml
advanced:
  disable_patterns:
    - '\\/admin\\/'  # All admin pages
    - '\\/media\\/.*\\/preview'  # All CKEditor previews
    - '\\/user\\/\\d+\\/edit'  # User edit forms
```

**Pattern Syntax** (regular expressions):
```yaml
# Escape forward slashes with backslash
'\\/admin\\/'  # Matches /admin/*

# Match any characters
'\\/media\\/.*\\/preview'  # Matches /media/{anything}/preview

# Match digits
'\\/node\\/\\d+'  # Matches /node/123

# Combine patterns
- '\\/admin\\/'
- '\\/user\\/\\d+\\/(edit|cancel)'
- '\\/media\\/full_html\\/preview'
```

**Enable Specific Patterns** (whitelist):
```yaml
# Disable Klaro by default but enable on specific patterns
enable_patterns:
  - '\\/public-content\\/'  # Only show on public content
  - '\\/blog\\/.*'  # Only blog section
```

**Reference**: Drupal routing system and PHP PCRE regular expressions

## Common Mistakes

- **Wrong**: Forgetting to escape forward slashes → **Right**: Pattern doesn't match; use `\\/` not `/`
- **Wrong**: Using glob patterns instead of regex → **Right**: `*.admin` doesn't work; use `\\/admin\\/.*`
- **Wrong**: Too broad exclusions → **Right**: Excluding `/user` disables on all user-related pages including public profiles
- **Wrong**: Not testing patterns → **Right**: Pattern matches unintended URLs; test thoroughly
- **Wrong**: Excluding frontend pages requiring consent → **Right**: Disables consent on pages with tracking; only exclude admin/preview
- **Wrong**: Adding patterns without clearing cache → **Right**: Changes don't take effect; clear Drupal cache after configuration

## See Also

- [Menu Integration](menu-integration.md)
- [Troubleshooting](troubleshooting.md)
- Reference: [Drupal Issue #3486803 (CKEditor Preview Fix)](https://www.drupal.org/project/klaro/issues/3486803)
