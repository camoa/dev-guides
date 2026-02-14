---
description: Catalog of commonly used Drupal core services — database, entity_type.manager, config.factory, cache, logger, request_stack, current_user, renderer, file_system, messenger, state, and more.
---

# Core Services Reference

## When to Use

When you need to know what core services are available for injection — this catalog covers the most commonly used Drupal services.

## Database & Storage Services

### database
**Description**: Database connection
**Interface**: `Drupal\Core\Database\Connection`
**Usage**: Execute queries, transactions
```php
$this->database->select('node_field_data', 'n')->fields('n')->execute();
```

### entity_type.manager
**Description**: Manage entity types and load entities
**Interface**: `Drupal\Core\Entity\EntityTypeManagerInterface`
**Usage**: Load entities, get storage handlers
```php
$storage = $this->entityTypeManager->getStorage('node');
$node = $storage->load(1);
```

### entity.repository
**Description**: Entity loading and translation
**Interface**: `Drupal\Core\Entity\EntityRepositoryInterface`
**Usage**: Load entities by UUID, get translations
```php
$entity = $this->entityRepository->loadEntityByUuid('node', $uuid);
```

## Configuration Services

### config.factory
**Description**: Load and save configuration
**Interface**: `Drupal\Core\Config\ConfigFactoryInterface`
**Usage**: Get/set config values
```php
$config = $this->configFactory->get('system.site');
$name = $config->get('name');
```

### config.manager
**Description**: Configuration schema and dependencies
**Interface**: `Drupal\Core\Config\ConfigManagerInterface`

## Cache Services

### cache.default
**Description**: Default cache bin
**Interface**: `Drupal\Core\Cache\CacheBackendInterface`
**Usage**: Cache data
```php
$this->cache->set('my_key', $data, CacheBackendInterface::CACHE_PERMANENT, ['node:1']);
```

### cache.render
**Description**: Render cache bin
**Interface**: `Drupal\Core\Cache\CacheBackendInterface`

### cache_tags.invalidator
**Description**: Invalidate cache tags
**Interface**: `Drupal\Core\Cache\CacheTagsInvalidatorInterface`
```php
$this->cacheTagsInvalidator->invalidateTags(['node:1', 'node_list']);
```

## Logging Services

### logger.factory
**Description**: Create logger channels
**Interface**: `Drupal\Core\Logger\LoggerChannelFactoryInterface`
**Usage**: Get channel-specific logger
```php
$logger = $this->loggerFactory->get('my_module');
$logger->error('Error message');
```

### logger.channel.{channel_name}
**Description**: Specific logger channel
**Interface**: `Psr\Log\LoggerInterface`
**Usage**: Direct injection of specific channel
```yaml
arguments: ['@logger.channel.my_module']
```

## Request/Response Services

### request_stack
**Description**: HTTP request stack
**Interface**: `Symfony\Component\HttpFoundation\RequestStack`
**Usage**: Get current request
```php
$request = $this->requestStack->getCurrentRequest();
$param = $request->query->get('param');
```

### current_user
**Description**: Current user account
**Interface**: `Drupal\Core\Session\AccountProxyInterface`
**Usage**: Check permissions, get user ID
```php
if ($this->currentUser->hasPermission('administer nodes')) {
  // ...
}
```

### current_route_match
**Description**: Current route match
**Interface**: `Drupal\Core\Routing\RouteMatchInterface`
**Usage**: Get route parameters
```php
$node = $this->routeMatch->getParameter('node');
```

## Rendering Services

### renderer
**Description**: Render arrays to HTML
**Interface**: `Drupal\Core\Render\RendererInterface`
**Usage**: Render arrays
```php
$html = $this->renderer->renderRoot($render_array);
```

### theme.manager
**Description**: Theme management
**Interface**: `Drupal\Core\Theme\ThemeManagerInterface`

## File Services

### file_system
**Description**: File system operations
**Interface**: `Drupal\Core\File\FileSystemInterface`
**Usage**: File operations
```php
$this->fileSystem->copy($source, $destination);
```

### stream_wrapper_manager
**Description**: Stream wrapper manager
**Interface**: `Drupal\Core\StreamWrapper\StreamWrapperManagerInterface`

## Utility Services

### messenger
**Description**: User messages
**Interface**: `Drupal\Core\Messenger\MessengerInterface`
**Usage**: Display messages
```php
$this->messenger->addStatus('Operation successful');
```

### state
**Description**: Key-value state storage
**Interface**: `Drupal\Core\State\StateInterface`
**Usage**: Store temporary data
```php
$this->state->set('my_module.last_run', time());
```

### datetime.time
**Description**: Time and date utilities
**Interface**: `Drupal\Component\Datetime\TimeInterface`
**Usage**: Get request time
```php
$timestamp = $this->time->getRequestTime();
```

### module_handler
**Description**: Module management
**Interface**: `Drupal\Core\Extension\ModuleHandlerInterface`
**Usage**: Invoke hooks, check modules
```php
if ($this->moduleHandler->moduleExists('my_module')) {
  $this->moduleHandler->invokeAll('my_hook');
}
```

### language_manager
**Description**: Language and translation
**Interface**: `Drupal\Core\Language\LanguageManagerInterface`

### path.validator
**Description**: Validate URL paths
**Interface**: `Drupal\Core\Path\PathValidatorInterface`

### url_generator
**Description**: Generate URLs
**Interface**: `Drupal\Core\Routing\UrlGeneratorInterface`

Reference: `/core/core.services.yml` (complete list of 500+ services)

## Common Mistakes

- **Using deprecated services** — Check change records; e.g., `path.alias_manager` to `path_alias.manager`
- **Injecting concrete classes instead of interfaces** — Always type-hint against interfaces
- **Not checking if optional service exists** — Some services are only available when modules are enabled
- **Injecting too many services** — If you need 10+ services, your class is doing too much; refactor
- **Using database service for entity queries** — Use entity.query service instead

## See Also

- [Factory Services](factory-services.md)
- [core.services.yml](https://api.drupal.org/api/drupal/core!core.services.yml/)
