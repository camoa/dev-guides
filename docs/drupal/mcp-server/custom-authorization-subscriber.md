---
description: "Write a custom per-call MCP authorization rule (API key, IP allowlist, role per tool) with an Mcp RequestEvent subscriber in Drupal"
tldr: "Subscribe to Mcp RequestEvent and throw McpAuthorizationDeniedException with 401 or 403 for rules OAuth scopes cannot express. Gotcha: use the Mcp event, not Symfony's, and SDK v0.8.1 turns the denial into JSON-RPC -32603."
drupal_version: "^10 || ^11"
---

# Custom Authorization Subscriber

**Version:** mcp_server 2.0.0-beta5 with mcp/sdk v0.7.1 or v0.8.1.

## When to Use

> Use this when you need a rule OAuth scopes do not express: an API key, an IP allowlist, mTLS, or a role check per tool. Enforcement at this version was not verified on a running site.

## Decision

| Need | Where to enforce |
|---|---|
| Who may reach the endpoint at all | Route permission `access mcp server` |
| Who may see a native tool | `checkAccess()` on the `#[Tool]` plugin |
| Who may run a bridged tool | The Tool API tool's `permission:` or `checkAccess()` ([Access control](../tool-api/access-control.md)) |
| A rule applied to MCP requests the SDK dispatches as events (tool name, user) | A `RequestEvent` subscriber (this page) |
| HTTP-level filtering before the SDK | A PSR-15 middleware tagged `mcp_server.transport_middleware` ([Server Configuration](server-configuration-and-extension-points.md)) |

## Pattern

Per-call authorization rides on the SDK's `Mcp\Event\RequestEvent`. Core ships no subscriber for it. Deny by throwing `McpAuthorizationDeniedException` with status 401 or 403; any other status throws `InvalidArgumentException`. The shape follows `mcp_server_oauth`'s `McpAuthorizeOAuthSubscriber` (derived from that file; not shipped as an example):

```php
namespace Drupal\my_module\EventSubscriber;

use Drupal\Core\Session\AccountProxyInterface;
use Drupal\mcp_server\Exception\McpAuthorizationDeniedException;
use Mcp\Event\RequestEvent;
use Mcp\Schema\Request\CallToolRequest;
use Symfony\Component\EventDispatcher\EventSubscriberInterface;

final class ToolRoleSubscriber implements EventSubscriberInterface {
  public function __construct(private readonly AccountProxyInterface $currentUser) {}

  public static function getSubscribedEvents(): array {
    return [RequestEvent::class => 'onRequest'];
  }

  public function onRequest(RequestEvent $event): void {
    $request = $event->getRequest();
    if ($request instanceof CallToolRequest
      && str_starts_with($request->name, 'tool_api__')
      && !$this->currentUser->hasPermission('use mcp write tools')) {
      throw new McpAuthorizationDeniedException('insufficient_scope', 403);
    }
  }
}
```

```yaml
# my_module.services.yml
services:
  my_module.mcp_tool_role_subscriber:
    class: Drupal\my_module\EventSubscriber\ToolRoleSubscriber
    arguments: ['@current_user']
    tags:
      - { name: event_subscriber }
```

`use mcp write tools` is an example permission your module would declare. `McpServerFactory` passes Drupal's `event_dispatcher` to the SDK, so `event_subscriber`-tagged services receive `RequestEvent`.

**What the client receives.** On SDK v0.7.1 the exception reaches `McpExceptionSubscriber` and becomes HTTP 401 or 403. On SDK v0.8.1 the SDK catches it and answers JSON-RPC internal error -32603 "Internal server error." On STDIO with SDK v0.7.1, the Drush command writes a -32001/-32002 error to STDOUT and the session ends; with v0.8.1 the client gets -32603.

## Common Mistakes

- Importing Symfony's `RequestEvent`. Use `Mcp\Event\RequestEvent`; `Symfony\Component\HttpKernel\Event\RequestEvent` never fires here.
- Returning a response from the subscriber. Throw `McpAuthorizationDeniedException`.
- Passing a 400 or 500 status. The constructor accepts only 401 and 403.
- Matching bridged tools without their prefix. The wire name is `tool_api__<config id>`; `McpToolConfig::getMcpWireName()` returns it.
- Following the README link `references/auth/index.md`. That file does not exist in the 2.0.0-beta5 tree.

## See Also

- [OAuth Scopes per Tool](oauth-scopes-per-tool.md) → for the shipped subscriber's configuration
- [Server Configuration and Extension Points](server-configuration-and-extension-points.md) → for middleware
- Reference: `modules/contrib/mcp_server/src/Exception/McpAuthorizationDeniedException.php`, `src/EventSubscriber/McpExceptionSubscriber.php`; `modules/contrib/mcp_server_oauth/src/EventSubscriber/McpAuthorizeOAuthSubscriber.php`; `vendor/mcp/sdk/src/Server/Protocol.php`
