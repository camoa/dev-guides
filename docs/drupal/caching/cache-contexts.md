---
description: Vary cached content by URL, user, language, and other request contexts
---

# Cache Contexts

## When to Use

When cached content varies based on request context. Cache contexts create separate cache entries for different variations — e.g., one cached version per language, per user role, per URL path.

## User Contexts

**Context Token:** `user`, `user.roles`, `user.permissions:{permission}`

| Context | Varies by... | Use when... |
|---|---|---|
| `user` | User ID | Content is personalized per-user (profile page, dashboard) |
| `user.roles` | User's role(s) | Content differs by role (admin tools visible to admins) |
| `user.permissions:{permission}` | Specific permission | Content gated by permission (edit links for editors) |

```php
// Vary by user ID (separate cache per user)
$build = [
  '#cache' => ['contexts' => ['user']],
];

// Vary by user roles (one cache per role combination)
$build = [
  '#cache' => ['contexts' => ['user.roles']],
];
```

**Gotchas:**
- `user` context creates cache entry per user — can explode cache size, use sparingly
- `user.roles` creates entry per unique role combination — user with 5 roles creates different cache key than user with 3 roles
- Anonymous users share user:0 — safe to cache heavily
- Don't use `user` when `user.roles` or `user.permissions` is sufficient

## URL Contexts

**Context Token:** `url`, `url.path`, `url.query_args`, `url.site`

| Context | Varies by... | Use when... |
|---|---|---|
| `url` | Full URL including query string | Content changes based on entire URL |
| `url.path` | Path only (no query string) | Content differs per page but not by query params |
| `url.query_args` | All query parameters | Content uses query string filtering |
| `url.query_args:{key}` | Specific query param | Content uses specific param (e.g., `?page=`) |
| `url.site` | Domain/subdomain | Multisite with different content per domain |

```php
// Vary by path only
$build = [
  '#cache' => ['contexts' => ['url.path']],
];

// Vary by specific query parameter
$build = [
  '#cache' => ['contexts' => ['url.query_args:page']],
];
```

**Gotchas:**
- `url` includes query args — cache miss on every unique URL
- Pagers automatically add `url.query_args:page` context
- `url.path` is language-aware when language is in URL

## Language Contexts

**Context Token:** `languages:{type}`

| Context | Varies by... | Use when... |
|---|---|---|
| `languages:language_interface` | UI language | Translatable UI strings in cached content |
| `languages:language_content` | Content language | Cached content includes translated entities |
| `languages:language_url` | URL language detection | Language determined from URL path prefix |

```php
$build = [
  '#cache' => ['contexts' => ['languages:language_interface']],
];
```

**Gotchas:**
- Multiple language types can be active — use the right one for your content
- Translated entities add language context automatically

## Route Contexts

**Context Token:** `route`, `route.name`, `route.menu_active_trails:{menu}`

| Context | Varies by... | Use when... |
|---|---|---|
| `route` | Route name + parameters | Content tied to current route (breadcrumbs, local tasks) |
| `route.name` | Route name only | Content varies by route but not route params |
| `route.menu_active_trails:{menu}` | Active menu trail | Highlighting active menu items |

```php
$build = [
  '#cache' => ['contexts' => ['route']],
];
```

**Gotchas:**
- `route` can create many cache variations with dynamic routes
- Menu active trails context needed for "active" CSS classes in menus

## Theme Context

**Context Token:** `theme`

| Context | Varies by... | Use when... |
|---|---|---|
| `theme` | Active theme name | Cached content includes theme-specific markup/assets |

```php
$build = [
  '#cache' => ['contexts' => ['theme']],
];
```

**Gotchas:**
- Usually not needed — render arrays are theme-agnostic by default
- Only add when caching theme-specific output (e.g., preprocess output)

## Session Context

**Context Token:** `session`, `session.exists`

| Context | Varies by... | Use when... |
|---|---|---|
| `session` | Session ID | Content stored in session (shopping cart) |
| `session.exists` | Whether session exists | Content differs for users with/without session |

```php
$build = [
  '#cache' => ['contexts' => ['session.exists']],
];
```

**Gotchas:**
- `session` context prevents Page Cache (creates session for anonymous users)
- Use `session.exists` for "logged in" indicator without per-session cache
- Avoid session contexts when possible — they reduce cacheability

## Timezone Context

**Context Token:** `timezone`

| Context | Varies by... | Use when... |
|---|---|---|
| `timezone` | User timezone setting | Displaying dates/times in user's timezone |

```php
$build = [
  '#cache' => ['contexts' => ['timezone']],
];
```

**Gotchas:**
- Creates cache entry per unique timezone — can be many variations
- Usually handled by date formatters automatically

## Request Format Context

**Context Token:** `request_format`

| Context | Varies by... | Use when... |
|---|---|---|
| `request_format` | Request format | Content served in multiple formats |

```php
$build = [
  '#cache' => ['contexts' => ['request_format']],
];
```

**Gotchas:**
- REST module adds this automatically
- Rarely needed in custom code

## Common Mistakes

- Adding too many contexts — Creates excessive cache variations, cache never hits
- Using `user` when `user.roles` would work — Creates per-user cache instead of per-role
- Forgetting contexts when content varies — Same cached content served to all users incorrectly
- Using `url` instead of `url.path` — Query strings create infinite cache variations
- Not using `Cache::mergeContexts()` when combining — Manual array merging doesn't optimize context order

## See Also

- [Cache Metadata Trinity](cache-metadata-trinity.md) — How contexts fit into cache metadata
- [Best Practices & Patterns](best-practices-patterns.md) — Context selection best practices
- Reference: [Cache contexts documentation](https://www.drupal.org/docs/develop/drupal-apis/cache-api/cache-contexts)
- Reference: `/core/lib/Drupal/Core/Cache/Context/` directory for all context classes
