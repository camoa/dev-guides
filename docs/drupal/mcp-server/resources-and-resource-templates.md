---
description: "Serve read-only data to MCP clients with mcp_server resource provider and resource template provider plugins, their config, access and caching"
tldr: "Use resource providers for fixed URIs and resource template providers for parameterized URIs. Gotcha: a plugin registers only with an enabled config entry, and content caches permanently by default, so per-user content needs max-age 0."
drupal_version: "^10 || ^11"
---

# Resources and Resource Templates

**Version:** mcp_server 2.0.0-beta5; mcp_server_examples 1.0.0-beta1 (released 2026-07-29).

## When to Use

> Use resources to give an agent read-only data. Resources are read-only by protocol, so a site that serves only resources and read tools is read-only.

## Decision

| If you need... | Plugin type | Directory | Listed via |
|---|---|---|---|
| Fixed URIs, enumerable up front | `mcp_server.resource_provider`, `#[ResourceProvider]`, `ResourceProviderBase` | `src/Plugin/mcp_server/ResourceProvider/` | `resources/list` |
| Parameterized URIs (`drupal://entity/{entity_type}/{entity_id}`) | `mcp_server.resource_template_provider`, `#[ResourceTemplateProvider]`, `ResourceTemplateProviderBase` | `src/Plugin/mcp_server/ResourceTemplateProvider/` | `resources/templates/list` |

## Pattern

**A plugin is not enough. It must be listed and enabled in config.** `McpServerFactory` reads `mcp_server.resource_providers` and `mcp_server.resource_template_providers` and registers only entries with top-level `enabled` true. `mcp_server` ships no install config for either; the UI to toggle them is in `mcp_server_ui`. Shape from the test fixture `mcp_server.resource_template_providers.yml`:

```yaml
plugins:
  -
    id: test_completion_template
    enabled: true
    configuration:
      enabled: true
```

Return content as `CacheableResourceContent`. Adapted from the test provider `TestResourceProvider.php`:

```php
use Drupal\Core\Access\AccessResult;
use Drupal\Core\Access\AccessResultInterface;
use Drupal\Core\Cache\CacheableMetadata;
use Drupal\Core\Session\AccountInterface;
use Drupal\mcp_server\Resource\CacheableResourceContent;

public const URI = 'test://hello';

public function getResourceContent(string $uri): ?CacheableResourceContent {
  $content = ['uri' => $uri, 'mimeType' => 'application/json', 'text' => '{"hello":"world"}'];
  return CacheableResourceContent::fromArray($content, new CacheableMetadata());
}

public function checkAccess(string $uri, AccountInterface $account): AccessResultInterface {
  return $uri === self::URI ? AccessResult::allowed() : AccessResult::forbidden();
}
```

The class itself uses `Drupal\mcp_server\Attribute\ResourceProvider` and extends `Drupal\mcp_server\Plugin\ResourceProviderBase`.

## Access and caching

- `checkAccess()` runs on every read, before any cache lookup. A denial reaches the client as JSON-RPC internal error -32603 "Error while reading resource".
- Content is stored with the DTO's cache metadata. The default max-age is **permanent**. A max-age of 0 skips storage.
- For content that differs per user, set max-age 0. Enforcement at this version was not verified on a running site.
- `getResourceContent()` returning `NULL` throws "Resource not found".

## Content entities

`mcp_server_examples` holds `ContentEntityResourceTemplate`: URI template `drupal://entity/{entity_type}/{entity_id}`, JSON:API serialization, `module_dependencies: ['jsonapi']`, and `$entity->access('view', $account, TRUE)` on every read. Options: `require_canonical_url` (default TRUE) and `denied_entity_types`. Copy it into your module. In the examples project its namespace is `Drupal\mcp_server_examples\Plugin\ResourceTemplateProvider`. mcp_server 2.0.0-beta5 discovers `Plugin/mcp_server/ResourceTemplateProvider`, so move it under `Plugin\mcp_server\` when you copy it. The examples' tool plugins (`src/Plugin/Tool/`) sit outside `Plugin/mcp_server/Tool` for the same reason. Read from code, not run.

## Common Mistakes

- Adding a resource plugin and expecting it in `resources/list`. Add an enabled entry to the config object.
- Caching per-user content. Set max-age 0.
- Checking access only in `getResources()`. Access is enforced by `checkAccess()`; enumerate cheaply and check per URI.
- Depending on `mcp_server_examples`. It is an examples project; copy the pattern.

## See Also

- [Prompts](prompts.md) → for argument completion providers, which templates share
- Reference: `modules/contrib/mcp_server/src/Plugin/ResourceTemplateProviderInterface.php`, `src/Plugin/ResourceProviderInterface.php`, `src/Resource/CacheableResourceContent.php`, `config/schema/mcp_server.schema.yml`; `modules/contrib/mcp_server_examples/src/Plugin/ResourceTemplateProvider/ContentEntityResourceTemplate.php`
