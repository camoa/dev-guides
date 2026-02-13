---
description: Configure PHP, MySQL/PostgreSQL, and Composer for Drupal testing environments
drupal_version: "11.x"
---

# Drupal Stack Setup

## When to Use

> Use when configuring the runtime environment for Drupal testing and builds in GitHub Actions.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| PHP 8.1/8.2/8.3 with extensions | `shivammathur/setup-php@v2` | Official, maintained, supports all Drupal requirements |
| MySQL database | Service container `mysql:8.0` | Matches production environments, stable |
| PostgreSQL database | Service container `postgres:15` | For projects using Postgres |
| Composer dependency management | Built-in Composer from setup-php | Faster than installing separately |

## Pattern

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mysql:
        image: mysql:8.0
        env:
          MYSQL_ROOT_PASSWORD: root
          MYSQL_DATABASE: drupal
        ports: ['3306:3306']
        options: --health-cmd="mysqladmin ping"
    steps:
      - uses: actions/checkout@v4
      - uses: shivammathur/setup-php@v2
        with:
          php-version: '8.2'
          extensions: gd, pdo_mysql, zip, opcache
          tools: composer:v2
```

## Common Mistakes

- **Wrong**: Using outdated PHP versions → **Right**: Drupal 10 requires PHP 8.1+, Drupal 11 requires 8.2+
- **Wrong**: Missing required extensions (gd, opcache) → **Right**: Installation fails silently, specify all extensions
- **Wrong**: Not setting health checks on database services → **Right**: Tests run before DB is ready

## See Also

- Previous: [Workflow Fundamentals](workflow-fundamentals.md)
- Next: [Matrix Testing](matrix-testing.md)
- Reference: [shivammathur/setup-php](https://github.com/shivammathur/setup-php)
