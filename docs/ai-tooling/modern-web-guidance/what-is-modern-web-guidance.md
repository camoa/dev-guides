---
description: What Modern Web Guidance is — an Agent Skills plugin (not an MCP server) that injects web platform best practices into coding agents via a local offline CLI.
tldr: MWG is a set of Agent Skills distributed as a plugin — not an MCP server. The agent reads a SKILL.md instruction file and runs modern-web-guidance search/retrieve CLI commands offline (TensorFlow.js local embeddings, no API keys). Covers 102 web features and 128 developer use cases across CSS, HTML, JS, passkeys, performance, and accessibility.
drupal_version: ""
---

# What Is Modern Web Guidance

## When to Use

> Reach for this reference when you need to understand what Modern Web Guidance is before deciding whether to install it — or when someone asks "is this an MCP server?" The short answer: it is not an MCP server.

## Decision

**Skill vs. MCP — the distinction that matters:**

| | Agent Skill | MCP Server |
|---|---|---|
| What it is | A SKILL.md instruction file added to the agent's context | A running server process exposing tools via the Model Context Protocol |
| How it activates | Agent reads the skill instructions and calls a CLI | Agent calls server-hosted tool functions via JSON-RPC |
| Network required | No — the CLI runs fully offline (TensorFlow.js local embeddings) | Yes — requires a running server process |
| Modern Web Guidance | Yes — it is this | No — MWG does not ship an MCP server |

**Two skill packs** (selectable via `--choose` flag):

| Skill pack | System-prompt overhead | Coverage |
|---|---|---|
| `modern-web-guidance` | ~234 tokens | Modern browser APIs, CSS, forms, passkeys, built-in AI, privacy, WebMCP |
| `chrome-extensions` | ~181 tokens | Manifest V3, background workers, Chrome Web Store |

**How it works end-to-end:**
1. The skill is installed into your agent (via a plugin or CLI)
2. On a relevant web task, the agent runs `modern-web-guidance search "<query>"` — offline, no API keys
3. The agent runs `modern-web-guidance retrieve <guide-id>` to pull the guide into context
4. The agent uses that guide to generate production-quality, modern web code

**What problems it solves:**
- LLMs default to legacy patterns because training data contains vast amounts of older code
- Models frequently misuse modern APIs they technically know exist
- Models lack Baseline awareness — they recommend patterns without checking browser support

**Coverage:** 102 modern web features across CSS/Layout, HTML/DOM, JS/APIs; 128 real-world use cases.

## Common Mistakes

- **Assuming MWG is an MCP server** — it is not; no MCP server is included or required
- **Installing both skill packs when you only need `modern-web-guidance`** — use `--choose` to minimize token overhead if Chrome extension development is not in scope
- **Expecting MWG to replace deep framework knowledge** — it covers the web platform layer, not Drupal, React, etc.

## See Also

- [Install for Claude Code](install-claude-code.md) — setup steps
- [Install for Other Agents](install-other-agents.md) — cross-agent install catalog
- Reference: [GitHub README](https://github.com/GoogleChrome/modern-web-guidance)
- Reference: [Chrome Docs — Modern Web Guidance](https://developer.chrome.com/docs/modern-web-guidance)
