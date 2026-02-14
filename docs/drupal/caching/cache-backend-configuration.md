---
description: Configure Redis, Memcache, and APCu cache backends in settings.php
---

# Cache Backend Configuration

## When to Use

When you need to configure cache backends (Redis, Memcache, APCu) in settings.php. Backend configuration determines where cached data is stored and how it's accessed.

## Steps

1. **Install backend module and dependencies**
   ```bash
   # Redis
   composer require drupal/redis
   drush en redis

   # Memcache
   composer require drupal/memcache
   drush en memcache
   ```

2. **Configure backend in settings.php**
   ```php
   // Edit sites/default/settings.php
   ```

3. **Set default backend or per-bin backends**
   ```php
   // All bins use Redis
   $settings['cache']['default'] = 'cache.backend.redis';

   // Or per-bin configuration
   $settings['cache']['bins']['render'] = 'cache.backend.redis';
   $settings['cache']['bins']['page'] = 'cache.backend.redis';
   ```

4. **Configure connection settings**
   ```php
   // Redis connection
   $settings['redis.connection']['interface'] = 'PhpRedis';
   $settings['redis.connection']['host'] = '127.0.0.1';

   // Memcache connection
   $settings['memcache']['servers'] = ['127.0.0.1:11211' => 'default'];
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing backend | High-traffic production site | Use Redis or Memcache, not database |
| Choosing backend | Multi-server setup | Use shared backend (Redis/Memcache), not APCu |
| Choosing backend | Single-server low-traffic | Database backend acceptable |
| Configuring bins | Small stable bins (bootstrap, discovery) | Use ChainedFastBackend with APCu |
| Configuring bins | Large high-churn bins (render, page) | Use Redis or Memcache |

## Pattern

**Redis configuration** (recommended):
```php
// settings.php
$settings['redis.connection']['interface'] = 'PhpRedis';
$settings['redis.connection']['host'] = '127.0.0.1';
$settings['redis.connection']['port'] = 6379;
$settings['redis.connection']['base'] = 0;
$settings['redis.connection']['password'] = NULL;
$settings['cache']['default'] = 'cache.backend.redis';

// Optional: compression
$settings['redis_compress_length'] = 100;
$settings['redis_compress_level'] = 1;
```

**Memcache configuration**:
```php
// settings.php
$settings['memcache']['servers'] = ['127.0.0.1:11211' => 'default'];
$settings['memcache']['bins'] = ['default' => 'default'];
$settings['memcache']['key_prefix'] = '';
$settings['cache']['default'] = 'cache.backend.memcache';
```

**ChainedFastBackend** (APCu + Redis):
```php
// settings.php
$settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
$settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';

// ChainedFast uses APCu (fast) + configured default backend (consistent)
```

**Per-bin configuration**:
```php
// Different backends for different bins
$settings['cache']['default'] = 'cache.backend.redis';
$settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
$settings['cache']['bins']['page'] = 'cache.backend.redis';
$settings['cache']['bins']['render'] = 'cache.backend.redis';
```

Reference: `/sites/default/default.settings.php` (search for "cache")

## Common Mistakes

- Using database backend on high-traffic sites — Slow; use Redis/Memcache for production
- Not setting Redis eviction policy — Redis fills up; set `maxmemory` and `maxmemory-policy allkeys-lru`
- Using APCu on multi-server — Per-server cache causes inconsistency; use shared backend
- Mixing Redis and Memcache — Pick one; don't split bins across different shared backends
- Not monitoring memory usage — Redis/Memcache can run out of memory; monitor and adjust limits

## See Also

- [Cache Backends](cache-backends.md) — Backend types and features
- [Cache Bins](cache-bins.md) — Understanding cache bins
- Reference: [Redis module configuration](https://www.drupal.org/project/redis)
- Reference: [Memcache module configuration](https://www.drupal.org/project/memcache)
