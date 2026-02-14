---
description: Choose and configure a cache backend — Redis, Memcache, APCu, or database
---

# Cache Backends

## When to Use

When you need to choose where cached data is stored. Cache backends determine storage mechanism — database (default), memory (APCu, Redis, Memcache), or specialized backends (chained, null).

## DatabaseBackend (Default)

Stores cache in database tables. Default backend for all cache bins.

**Advantages:** No additional setup required, works everywhere, persistent across restarts, handles large items (with caveats).

**Disadvantages:** Slower than memory-based backends, database I/O overhead, can bloat database size.

```php
// Default (no configuration needed)
// Each cache bin gets its own table: cache_default, cache_render, etc.
```

**Gotchas:**
- Large cache entries (>1MB) cause database performance issues — consider serialization or chunking
- Cache table fragmentation on high-churn bins — periodic table optimization needed
- Not suitable for high-traffic sites — use memory backend instead

## APCu Backend

Stores cache in PHP's APCu extension (in-process memory cache).

**Advantages:** Fast (in-memory), no network overhead (process-local), good for single-server setups.

**Disadvantages:** Not shared across servers, limited memory size (configure php.ini), cleared on PHP-FPM/Apache restart, per-process.

```php
$settings['cache']['bins']['bootstrap'] = 'cache.backend.apcu';
$settings['cache']['bins']['discovery'] = 'cache.backend.apcu';
```

**Gotchas:**
- APCu is per-server — deployments cause cache misses across servers
- Memory limits in php.ini (`apc.shm_size`) — monitor usage to avoid evictions
- Best used with ChainedFastBackend for small frequently-accessed bins

## Redis Backend

Stores cache in Redis (remote in-memory key-value store).

**Advantages:** Very fast (in-memory), shared across servers (centralized), persistence options (RDB, AOF), large memory capacity, clustering support.

**Disadvantages:** Requires Redis server setup, network latency (mitigated by optimization), additional infrastructure cost.

```php
$settings['redis.connection']['interface'] = 'PhpRedis';
$settings['redis.connection']['host'] = '127.0.0.1';
$settings['cache']['default'] = 'cache.backend.redis';
```

**Gotchas:**
- Use PhpRedis extension, not Predis library (much faster)
- Configure Redis eviction policy (`allkeys-lru` for cache)
- Monitor Redis memory usage — set `maxmemory` to prevent OOM
- Network latency matters — prefer Unix sockets for local Redis

## Memcache Backend

Stores cache in Memcached (remote in-memory caching daemon).

**Advantages:** Very fast (in-memory), shared across servers, simple protocol, industry-standard.

**Disadvantages:** No persistence (lost on restart), no clustering (requires client-side sharding), less feature-rich than Redis.

```php
$settings['memcache']['servers'] = ['127.0.0.1:11211' => 'default'];
$settings['cache']['default'] = 'cache.backend.memcache';
```

**Gotchas:**
- Purely volatile — all cache lost on Memcached restart
- Use consistent hashing for multi-server setups
- Monitor evictions — set memory size appropriately

## ChainedFastBackend

Combines fast backend (APCu) with consistent backend (Database/Redis).

**Advantages:** Best of both worlds — fast reads, persistent storage. Reduces database/Redis load for hot items. Automatic fallback if fast backend full.

**Disadvantages:** Adds complexity, fast backend still per-server (stale data possible), write overhead (stores in both backends).

```php
$settings['cache']['bins']['bootstrap'] = 'cache.backend.chainedfast';
$settings['cache']['bins']['discovery'] = 'cache.backend.chainedfast';
```

**Gotchas:**
- Only use for small bins with stable data (bootstrap, discovery)
- Don't use for bins with frequent writes (render, data)
- Fast backend can serve stale data if not invalidated properly

## NullBackend

Discards all cache writes, always returns cache miss.

**Advantages:** Useful for testing, disabling problematic bins temporarily.

**Disadvantages:** No caching at all.

```php
$settings['cache']['bins']['page'] = 'cache.backend.null';
```

**Gotchas:**
- Only use for debugging or specific test scenarios
- Don't confuse with disabling a cache bin (this still runs cache logic, just doesn't store)

## Common Mistakes

- Using database backend on high-traffic sites — Switch to Redis/Memcache for performance
- Mixing Redis and Memcache for same bins — Pick one shared backend, don't split
- Not configuring Redis eviction policy — Redis fills up and stops accepting cache writes
- Using APCu on multi-server without ChainedFast — Cache inconsistency across servers
- Storing large objects in memory backends — Monitor memory usage; consider serialization

## See Also

- [Cache Backend Configuration](cache-backend-configuration.md) — Detailed configuration examples
- [Cache Bins](cache-bins.md) — Understanding cache bins
- Reference: `/core/lib/Drupal/Core/Cache/DatabaseBackend.php`, `/core/lib/Drupal/Core/Cache/ApcuBackend.php`
