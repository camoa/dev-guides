---
description: "Write an MCP-only tool as a native mcp_server #[Tool] plugin: the class, attribute defaults, registration and naming rules"
tldr: "Write a native mcp_server Tool plugin extending ToolPluginBase when the operation is MCP-only. Gotcha: without a defaultConfiguration() returning enabled TRUE it registers nothing, and checkAccess() allows everyone by default."
drupal_version: "^10 || ^11"
---

# Native Tool Plugins

**Version:** mcp_server 2.0.0-beta5; SDK `NameValidator` from mcp/sdk v0.8.1.

## When to Use

> Use a native `#[Tool]` plugin when the operation is MCP-only and you do not want a Tool API dependency. If the operation should also run from Drush, ECA or a controller, write a Tool API tool and bridge it instead.

## Decision

| If the operation... | Write... | Page |
|---|---|---|
| Is MCP-only | A native `#[Tool]` plugin (this page) | — |
| Should also run from Drush, ECA, PHP or the AI module | A Tool API tool, exposed through the bridge | [Defining a tool](../tool-api/defining-a-tool.md), [Tool API Bridge](tool-api-bridge.md) |

## Pattern

The README example omits `defaultConfiguration()`. **By the code, that example registers nothing.** `ToolPluginBase::defaultConfiguration()` returns `['enabled' => FALSE]`, and `McpServerFactory::registerTools()` creates each plugin with no configuration and skips it when `!$plugin->isEnabled()`. Every test tool overrides it. The README class with the two missing pieces, taken from the test tool `PermissionGatedTool.php`:

```php
namespace Drupal\my_module\Plugin\mcp_server\Tool;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Access\AccessResultInterface;
use Drupal\Core\Session\AccountInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\mcp_server\Attribute\Tool;
use Drupal\mcp_server\Plugin\ToolPluginBase;
use Mcp\Server\ClientGateway;

#[Tool(
  id: 'send_email',
  label: new TranslatableMarkup('Send Email'),
  description: new TranslatableMarkup('Sends an email to a recipient.'),
  inputSchema: [
    'type' => 'object',
    'properties' => ['to' => ['type' => 'string'], 'subject' => ['type' => 'string']],
    'required' => ['to', 'subject'],
  ],
)]
final class SendEmail extends ToolPluginBase {
  protected function defaultConfiguration(): array {
    return ['enabled' => TRUE];
  }
  public function checkAccess(AccountInterface $account): AccessResultInterface {
    return AccessResult::allowedIfHasPermission($account, 'send mcp email');
  }
  public function execute(array $arguments, ClientGateway $gateway): mixed {
    return ['success' => TRUE, 'message' => 'Email sent'];
  }
}
```

Place it in `src/Plugin/mcp_server/Tool/`. Then run `drush cache:rebuild`. `send mcp email` is an example permission your module would declare.

## Attribute defaults

From `mcp_server 2.0.0-beta5 src/Attribute/Tool.php`:

| Argument | Default | Sent to clients as |
|---|---|---|
| `inputSchema` | `[]` | `inputSchema`; `type` forced to `object`, empty sub-schemas sent as `{}` |
| `outputSchema` | `NULL` | omitted |
| `readOnly` | `FALSE` | `readOnlyHint` |
| `destructive` | `TRUE` | `destructiveHint` |
| `idempotent` | `FALSE` | `idempotentHint` |
| `openWorld` | `TRUE` | `openWorldHint` |

## Registration rules

- `checkAccess()` runs when the server is built: once per HTTP request, once per STDIO run. A denied tool is absent from `tools/list`, and a call returns the SDK's "tool not found".
- Names must pass the SDK `NameValidator` (`^[a-zA-Z0-9._/-]{1,64}$`); invalid names are skipped with a warning. A duplicate name is skipped; the first one wins.
- Derivative IDs use `__`, because stricter clients accept only `^[a-zA-Z0-9_]{1,64}$` (`WireSafeDerivativeDiscoveryDecorator` docblock).
- Progress and elicitation use the `$gateway` argument of `execute()`. `ClientGatewayAwareInterface` is called only by the bridge, on wrapped Tool API tools.

## Common Mistakes

- Copying the README example as-is. Add `defaultConfiguration()` returning `enabled => TRUE`.
- Importing Tool API's attribute. Both modules define a `#[Tool]`: use `Drupal\mcp_server\Attribute\Tool` here. `Drupal\tool\Attribute\Tool` belongs to Tool API tools, which another manager discovers.
- Leaving `checkAccess()` at its default. It returns `AccessResult::allowed()`, so everyone who reaches the server can call the tool.
- Leaving `destructive` at its default on a read tool. Set `readOnly: TRUE, destructive: FALSE` so clients can skip confirmation.
- Expecting hints to be enforced. `destructiveHint` and the others are hints to the client only; nothing in the module asks for confirmation.
- Reading `references/tools/index.md` from the README. It does not exist in the tree.

## See Also

- [Tool API Bridge](tool-api-bridge.md) → for the Tool API path
- [Defining a tool (Tool API)](../tool-api/defining-a-tool.md)
- [Server Configuration and Extension Points](server-configuration-and-extension-points.md) → for `hook_mcp_server_tool_alter()`
- Reference: `modules/contrib/mcp_server/src/Plugin/ToolPluginBase.php`, `src/McpServerFactory.php` (`registerTools()`), `src/Attribute/Tool.php`, `tests/modules/mcp_server_test/src/Plugin/mcp_server/Tool/PermissionGatedTool.php`; `vendor/mcp/sdk/src/Capability/Tool/NameValidator.php`
