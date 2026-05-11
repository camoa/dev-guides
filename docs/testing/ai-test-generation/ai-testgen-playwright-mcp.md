---
description: Playwright MCP setup — installing @playwright/mcp in Claude Code and what browser tools it exposes to AI agents.
tldr: Install with `claude mcp add playwright npx @playwright/mcp@latest`, then restart Claude Code. The MCP exposes browser_navigate, browser_snapshot (accessibility-tree, ~13.7k tokens), browser_click, browser_type, and others. Use Playwright MCP for test generation; Chrome DevTools MCP for performance traces. Never run MCP against production URLs — the agent will navigate, click, and fill forms.
---

# Playwright MCP Setup

## When to Use

> Use this guide when wiring Claude Code (or Cursor / Copilot) to drive a real browser for plan generation.

## Decision

| Use Playwright MCP | Use Chrome DevTools MCP |
|---|---|
| Test generation, browser automation | Performance traces, Web Vitals |
| Accessibility-tree based (~13.7k tokens) | DOM-based (~18k tokens) |
| Cross-browser (Chromium/Firefox/WebKit) | Chrome only |
| Pairs with Playwright Test Agents | Complement for debugging traces |

Both can coexist. Playwright MCP is the right tool for the test-generation loop.

## Pattern: install in Claude Code

One command:

```bash
claude mcp add playwright npx @playwright/mcp@latest
```

Restart Claude Code to load.

## Pattern: explicit config

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

## What Playwright MCP Exposes

| Tool | Purpose |
|---|---|
| `browser_navigate(url)` | Open URL |
| `browser_snapshot()` | Accessibility-tree snapshot (token-efficient) |
| `browser_click(ref)` | Click via ref from snapshot |
| `browser_type(ref, text)` | Type into element |
| `browser_select(ref, value)` | Select option |
| `browser_screenshot()` | Visual screenshot (heavier; use sparingly) |
| `browser_network_request(url)` | Fetch via the browser context |

## Pattern: codegen mode

Playwright MCP supports a `--codegen typescript` flag that emits real Playwright code as the agent navigates. Useful for one-off "show me the code I'd write to do this" inquiries — not for the structured Test Agents loop.

## Common Mistakes

- **Wrong**: Mixing Playwright MCP and Chrome DevTools MCP in the same agent call → **Right**: token cost doubles; pick one per task
- **Wrong**: Running MCP against production URLs → **Right**: the agent will navigate, click, fill forms; always route to a test environment
- **Wrong**: Skipping the MCP restart after install → **Right**: Claude Code doesn't auto-detect the new server

## See Also

- [Playwright Test Agents](ai-testgen-playwright-test-agents.md)
- Reference: https://github.com/microsoft/playwright-mcp
