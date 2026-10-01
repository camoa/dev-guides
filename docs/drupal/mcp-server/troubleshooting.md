---
description: "Fix Drupal MCP server problems: missing native or bridged tools, denied calls, resource errors, HTTP 400/401/403/405/503 and STDIO exits"
tldr: "Match the symptom to its cause: a missing native tool lacks enabled TRUE, a missing bridged tool needs a cache rebuild, 401 and 403 trace to access mcp server or the token. Check watchdog before debugging the client."
drupal_version: "^10 || ^11"
---

# Troubleshooting

**Version:** mcp_server 2.0.0-beta5, mcp_server_tool_bridge 1.0.0-beta3, mcp_server_oauth 1.0.0-alpha1, mcp/sdk v0.7.1 or v0.8.1.

## When to Use

> Use this when a tool does not appear, a call is denied, or a client cannot connect.

## Decision

| Symptom | Likely cause | Fix |
|---|---|---|
| Native tool missing from `tools/list` | `defaultConfiguration()` does not return `enabled => TRUE` | Add the override; run `drush cache:rebuild` ([Native Tool Plugins](native-tool-plugins.md)) |
| Native tool missing for one user only | `checkAccess()` denies that account | Grant that account the permission `checkAccess()` tests |
| Bridged tool missing | Cache not rebuilt; `status: false`; `tool_id` unknown; `id` over 54 chars | Run `drush cache:rebuild`; enable the config; fix `tool_id` (check `drush tool:list`); shorten `id` |
| Bridged call returns `isError` "Tool plugin access denied" | Tool API access denied for the acting user | Grant the tool's `permission` to that user's role ([Access control](../tool-api/access-control.md)) |
| Bridged call returns `isError` plus "Input schema:" | Input validation failed | Fix the arguments to match the echoed schema; `null` values are dropped |
| Resource missing | No enabled entry in `mcp_server.resource_*providers` config; plugin outside `Plugin/mcp_server/...` | Add the config entry; move the class ([Resources](resources-and-resource-templates.md)) |
| Resource read returns -32603 "Error while reading resource" | `checkAccess()` denied, or content was `NULL` | Check the acting user's access to that URI; check the plugin returns content |
| HTTP 400 unsupported protocol version | Client sent `MCP-Protocol-Version: 2026-07-28` | Configure the client to use a handshake revision (`2025-11-25` or earlier) |
| HTTP 405 on GET | No GET stream in either SDK version | Use POST; ignore if the client falls back |
| HTTP 401 | Anonymous lacks `access mcp server`, or the bearer token is missing, invalid, expired or revoked | Authenticate, or issue a new token ([OAuth Client Connection](oauth-client-connection.md)) |
| HTTP 403 | The acting user lacks `access mcp server` | Add `access mcp server` to a scope the token holds, and to the user's role for the code flow |
| JSON-RPC -32603 "Internal server error." on `tools/call` | On SDK v0.8.1, a `RequestEvent` listener threw | Check `drush watchdog:show --filter=mcp_server`; review the token's scopes and your subscribers |
| HTTP 503 "MCP session lock timeout" | Two requests on one session at once | Retry after 1 second; send one request per session at a time |
| STDIO client shows the server exiting | Missing, blocked or unknown `account`; STDOUT noise | Pass a valid active account; run the command in a terminal to read STDERR |

## Commands

From the `mcp_server` README:

```bash
drush pm:list --type=module --status=enabled | grep mcp_server
drush watchdog:show --filter=mcp_server
drush cache:rebuild
```

The bridge logs to channel `mcp_server_tool_bridge`. The README also suggests `drush eval "print_r(\Drupal::service('mcp_server.server'));"`. That builds a full server as the Drush user and prints a large object.

## Common Mistakes

- Debugging the client first. Check `watchdog` for "Skipping tool", "Duplicate MCP tool name" and "Failed to register" messages.
- Testing access as `admin` and shipping as another user. Test with the real acting account.

## See Also

- [Native Tool Plugins](native-tool-plugins.md) | [Tool API Bridge](tool-api-bridge.md) | [Resources and Resource Templates](resources-and-resource-templates.md)
- Reference: `modules/contrib/mcp_server/README.md` (Troubleshooting)
