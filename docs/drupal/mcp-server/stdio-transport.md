---
description: "Run the Drupal MCP server over STDIO with drush mcp:server and its required account argument, and connect Claude Desktop, Claude Code or MCP Inspector"
tldr: "Use drush mcp:server with a required account argument when the client runs on the same machine. Gotcha: that account is the permission boundary, so never pass admin; an MCP client launching it without the argument never starts."
drupal_version: "^10 || ^11"
---

# STDIO Transport

**Version:** mcp_server 2.0.0-beta5; Drush 13+.

## When to Use

> Use STDIO when the MCP client runs on the same machine as the site and can launch Drush. It is the simplest setup and needs no HTTP permission or token.

## Decision

| If... | Then... |
|---|---|
| The agent should only read | Pass a dedicated low-privilege account |
| The agent needs no login at all | Pass `0` for an anonymous session |
| A user name is all digits | Pass the numeric ID; all-digit values are always IDs |
| You run Drush in a terminal with no argument | Drush shows a user picker |
| An MCP client launches it with no argument | The picker is skipped; Symfony reports the missing argument on STDERR and the server never starts |

## Pattern

The command is `mcp:server`, alias `mcps`, with one **required** argument: the account the session runs as. From `mcp_server 2.0.0-beta5 src/Drush/Commands/McpServerCommands.php`:

```php
#[CLI\Command(name: 'mcp:server', aliases: ['mcps'])]
#[CLI\Argument(name: 'account', description: 'User name or numeric ID to run the session as. An all-digit value is always read as an ID. 0 runs as anonymous.')]
public function server(string $account): void {
  $user = $this->loadAccount($account);
  $this->accountSwitcher->switchTo($user);
```

There are no other options. The examples below use a dedicated account named `mcp_agent`. The README uses `admin`; do not copy that.

**Claude Desktop**, adapted from the README. The README uses `"cwd"` with a relative `vendor/bin/drush`; whether Claude Desktop honours `cwd` was not verified, so use an absolute path:

```json
{
  "mcpServers": {
    "drupal": {
      "command": "/path/to/site/vendor/bin/drush",
      "args": ["mcp:server", "mcp_agent"]
    }
  }
}
```

**Claude Code** (composed from the Claude Code docs syntax `claude mcp add [options] <name> -- <command> [args...]`; not tested against this module):

```bash
claude mcp add --transport stdio drupal -- /path/to/site/vendor/bin/drush mcp:server mcp_agent
```

**Manual test and MCP Inspector:**

```bash
drush mcp:server mcp_agent
npx @modelcontextprotocol/inspector vendor/bin/drush mcp:server mcp_agent
```

## Common Mistakes

- Running as `admin`. The account **is** the permission boundary. Every tool runs with that account's rights.
- Treating the argument as client authentication. The code calls it "executor attribution, not client authentication". Anyone who can launch Drush already has full site access.
- Passing a blocked or unknown user. `loadAccount()` throws `InvalidArgumentException` before the handshake, so the client only sees the server exit.
- Printing to STDOUT from a module during bootstrap. The `interactAccount()` docblock warns that anything on STDOUT before the handshake corrupts the transport.
- Setting up OAuth for STDIO. STDIO sends no bearer token. The MCP authorization spec says STDIO implementations should not follow it and should take credentials from the environment.

## See Also

- [Authentication and the Acting User](authentication-and-the-acting-user.md) → for the transport/user table
- [HTTP Transport](http-transport.md)
- Reference: `modules/contrib/mcp_server/src/Drush/Commands/McpServerCommands.php`; https://code.claude.com/docs/en/mcp
